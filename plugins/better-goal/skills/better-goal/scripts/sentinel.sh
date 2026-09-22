#!/usr/bin/env bash
# better-goal sentinel — the report that reaches a human instead of a corpse.
#
# Registered by install.sh as a SessionStart hook. Every other part of this
# harness lives inside the session it is watching: the guard is a Stop hook, and
# the watcher is a Monitor that dies when its session does. So when a run died
# mid-turn, the STALL went to a session that could no longer act on it, and the
# state file read `armed: true` for fourteen days with nobody told.
#
# Two jobs. First, write a heartbeat for the session that is starting: hook
# configuration is snapshotted at process start, so a SessionStart firing is
# proof that the registration beside it was in the snapshot. arm.sh reads that
# heartbeat to say whether a run armed in this session will actually be judged.
# Second, report what is still armed in this repo and whether it is breathing.
# It reports only what somebody has not already been told, and says nothing at
# all when every run is healthy — SessionStart output is injected into context
# and paid for.
#
# Contract: stdout is one JSON object with hookSpecificOutput.additionalContext,
# or nothing. Always exits 0: a session must never fail to start because of this.

set -uo pipefail
INPUT="$(cat 2>/dev/null || true)"
command -v jq >/dev/null 2>&1 || exit 0

CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
NOW="$(date +%s)"
mtime_of() { [ -f "$1" ] && { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; } || echo 0; }
epoch_of() {
  local raw="$1" s
  s="${raw%Z}"; s="${s/T/ }"
  date -u -j -f "%Y-%m-%d %H:%M:%S" "$s" +%s 2>/dev/null || date -u -d "$raw" +%s 2>/dev/null || echo 0
}

OURS_RE='(better-goal|goal-harness).*(guard|goal-guard)\.sh'
SID_NOW="$(printf '%s' "$INPUT" | jq -r '.session_id // ""' 2>/dev/null || true)"
ROOT_NOW="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# --- heartbeat for the starting session --------------------------------------
# Which settings files register the guard right now. Those files are what the
# snapshot was just taken from, so a non-empty list here means the guard is
# loaded for this session.
REG_JSON='[]'
for f in "$CFG/settings.json" "$ROOT_NOW/.claude/settings.json" "$ROOT_NOW/.claude/settings.local.json"; do
  [ -f "$f" ] || continue
  if jq -e --arg re "$OURS_RE" '[(.hooks.Stop // [])[] | (.hooks // [])[] | .command? // ""] | map(test($re)) | any' "$f" >/dev/null 2>&1; then
    REG_JSON="$(jq -cn --argjson a "$REG_JSON" --arg f "$f" '$a + [$f]')"
  fi
done
if [ -n "$SID_NOW" ]; then
  mkdir -p "$CFG/better-goal/live" 2>/dev/null && \
  jq -n --arg s "$SID_NOW" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg g "${BASH_SOURCE[0]}" \
        --arg c "${CLAUDE_CODE_STOP_HOOK_BLOCK_CAP:-}" --argjson r "$REG_JSON" \
        '{session_id:$s, event:"SessionStart", at:$t, guard:$g, block_cap:$c, guard_registered_in:$r}' \
        >"$CFG/better-goal/live/$SID_NOW.json" 2>/dev/null || true
fi
# Heartbeats older than 30 days are sessions nobody will arm from again.
find "$CFG/better-goal/live" -name '*.json' -mtime +30 -delete 2>/dev/null || true

# --- runs armed in this repo -------------------------------------------------
find_root() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    [ -d "$dir/.claude/goals" ] && { printf '%s' "$dir"; return 0; }
    [ -f "$dir/.claude/goal-state.json" ] && { printf '%s' "$dir"; return 0; }
    dir="$(dirname "$dir")"
  done
  return 1
}
ROOT="$(find_root)" || exit 0

transcript_age_min() {  # session_id -> minutes since last written, or "" if not found
  local sid="$1" newest=0 m
  [ -n "$sid" ] || { printf ''; return; }
  shopt -s nullglob 2>/dev/null || true
  for f in "$CFG"/projects/*/"$sid".jsonl; do
    m="$(mtime_of "$f")"; [ "$m" -gt "$newest" ] && newest="$m"
  done
  [ "$newest" -gt 0 ] || { printf ''; return; }
  printf '%s' $(( (NOW - newest) / 60 ))
}

state_set() { local f="$1"; shift; local tmp; tmp="$(mktemp)"
  jq "$@" "$f" >"$tmp" 2>/dev/null && mv "$tmp" "$f" || rm -f "$tmp"; }

LINES=""
add() { LINES="${LINES}$1
"; }

GUARD_LOADED_HERE=0; [ "$(jq -n --argjson r "$REG_JSON" '$r | length')" -gt 0 ] && GUARD_LOADED_HERE=1

shopt -s nullglob 2>/dev/null || true
STATES=( "$ROOT"/.claude/goals/*.json )
[ -f "$ROOT/.claude/goal-state.json" ] && STATES+=( "$ROOT/.claude/goal-state.json" )
[ "${#STATES[@]}" -gt 0 ] || exit 0

for STATE in "${STATES[@]}"; do
  jq -e 'type == "object" and has("slug")' "$STATE" >/dev/null 2>&1 || continue

  SLUG="$(jq -r '.slug' "$STATE")"
  ARMED="$(jq -r '.armed // false' "$STATE")"
  ITER="$(jq -r '.iteration // 0' "$STATE")"
  REASON="$(jq -r '.end_reason // ""' "$STATE")"
  REPORTED="$(jq -r '.reported_end // ""' "$STATE")"
  LIVE="$(jq -r '.hook_live // "unknown"' "$STATE")"
  SID="$(jq -r '.session_id // ""' "$STATE")"
  LEDGER="$(jq -r '.ledger // ""' "$STATE")"
  [ -n "$LEDGER" ] || LEDGER="docs/goals/goal-${SLUG}.ledger.md"
  case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac

  if [ "$ARMED" != "true" ]; then
    case "$REASON" in
      stuck|api_error|session_ended|max_iterations|deadline) : ;;
      *) continue ;;
    esac
    [ "$REPORTED" = "$REASON" ] && continue
    STUCK="$(jq -r '.stuck_on // ""' "$STATE")"
    add "- \`$SLUG\` ended at turn $ITER with end_reason=$REASON${STUCK:+ (on $STUCK)}. Nothing is verifying it now. Ledger: ${LEDGER#$ROOT/}"
    state_set "$STATE" --arg r "$REASON" '.reported_end=$r'
    continue
  fi

  # Liveness is the guard's own stamp. The ledger's mtime is not evidence: any
  # process can append to it, and one run's substitute verifier did, every ten
  # minutes, through twelve idle hours.
  LG="$(jq -r '.last_guard_at // .hook_proven_at // ""' "$STATE")"
  LGE=0; [ -n "$LG" ] && LGE="$(epoch_of "$LG")"
  [ "$LGE" -gt 0 ] || LGE="$(mtime_of "$STATE")"
  AGE=$(( (NOW - LGE) / 60 ))
  TAGE="$(transcript_age_min "$SID")"

  if [ "$SID" = "$SID_NOW" ]; then
    : # this session owns it; the guard will speak for itself at the end of the turn
  elif [ "$LIVE" != "proven" ]; then
    if [ "$GUARD_LOADED_HERE" -eq 1 ]; then
      add "- \`$SLUG\` is armed at turn $ITER but its guard never fired (hook_live=$LIVE): it was armed in session $SID before the guard was loaded. The guard IS loaded in this session, so re-arm from here — \`arm.sh --state <draft>\` — and it runs the gates from the next turn."
    else
      add "- \`$SLUG\` is armed at turn $ITER but its guard never fired (hook_live=$LIVE), and no settings file registered the guard when THIS session started either. Run the skill's \`install.sh\`, restart Claude Code, then re-arm. Nothing verifies anything until then."
    fi
  elif [ -n "$TAGE" ] && [ "$TAGE" -lt 10 ]; then
    : # the owning session wrote to its transcript in the last 10 minutes: alive.
  elif [ "$AGE" -ge 60 ]; then
    add "- \`$SLUG\` is armed at turn $ITER and the guard last ran ${AGE}m ago${TAGE:+, with its session silent for ${TAGE}m}. Its session is gone or wedged, so no gate is running. Either re-arm from a live session (\`arm.sh\` rewrites session_id and keeps the ledger) or disarm it (\`disarm.sh $SLUG\`). Ledger: ${LEDGER#$ROOT/}"
  fi
done

[ -n "$LINES" ] || exit 0

BODY="better-goal: runs in this repo that nobody is watching.

$LINES
Read the full picture with the skill's \`status.sh\`. Say this to the user rather than acting on it unprompted — one of these may be a run they still intend to resume."

jq -n --arg c "$BODY" '{hookSpecificOutput:{hookEventName:"SessionStart", additionalContext:$c}}'
exit 0
