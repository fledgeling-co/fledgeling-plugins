#!/usr/bin/env bash
# better-goal sentinel — the report that reaches a human instead of a corpse.
#
# Registered by arm.sh as a SessionStart hook. Every other part of this harness
# lives inside the session it is watching: the guard is a Stop hook, and the
# watcher is a Monitor that dies when its session does. So when a run died
# mid-turn, the STALL went to a session that could no longer act on it, and the
# state file read `armed: true` for fourteen days with nobody told.
#
# This runs at the start of every session in the repo, so the next person to open
# it is told what is still armed and whether it is breathing. It reports only
# what somebody has not already been told, and it says nothing at all when every
# run is healthy — SessionStart output is injected into context and paid for.
#
# Contract: stdout is one JSON object with hookSpecificOutput.additionalContext,
# or nothing. Always exits 0: a session must never fail to start because of this.

set -uo pipefail
INPUT="$(cat 2>/dev/null || true)"
command -v jq >/dev/null 2>&1 || exit 0

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

NOW="$(date +%s)"
mtime_of() { [ -f "$1" ] && { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; } || echo 0; }

# A session's transcript file is appended to as the turn runs, so its mtime is
# the one liveness signal readable from outside the session. Measured on a live
# session: 6 seconds old while the turn was in progress. The project directory
# name is derived from the cwd, so glob on the session id instead of encoding it.
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
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
  GOAL_FILE="$(jq -r '.goal_file // ""' "$STATE")"
  LEDGER="$(jq -r '.ledger // ""' "$STATE")"
  [ -n "$LEDGER" ] || LEDGER="docs/goals/goal-${SLUG}.ledger.md"
  case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac

  if [ "$ARMED" != "true" ]; then
    # A run that ended on its own terms is worth saying once, and only for the
    # endings nobody watched happen. `met` and a deliberate `disarmed` are not
    # news; stuck, an API error, a lost session and a spent bound are.
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

  LM="$(mtime_of "$LEDGER")"; [ "$LM" -gt 0 ] || LM="$(mtime_of "$STATE")"
  AGE=$(( (NOW - LM) / 60 ))
  TAGE="$(transcript_age_min "$SID")"

  if [ "$LIVE" != "proven" ]; then
    add "- \`$SLUG\` is armed at turn $ITER but its Stop hook has never fired (hook_live=$LIVE). It was registered mid-session, and Claude Code only watches a \`.claude/\` that already held a settings file at session start. In THIS session the hook is loaded, so re-arm from here (\`arm.sh --state\`) and the guard will run. Brief: ${GOAL_FILE:-none}"
  elif [ -n "$TAGE" ] && [ "$TAGE" -lt 10 ]; then
    : # the owning session wrote to its transcript in the last 10 minutes: alive.
  elif [ "$AGE" -ge 60 ]; then
    add "- \`$SLUG\` is armed at turn $ITER and has not moved for ${AGE}m${TAGE:+, with its session silent for ${TAGE}m}. Its session is gone or wedged, so no gate is running. Either re-arm from a live session or disarm it: \`disarm.sh $SLUG\`. Ledger: ${LEDGER#$ROOT/}"
  fi
done

[ -n "$LINES" ] || exit 0

BODY="better-goal: runs in this repo that nobody is watching.

$LINES
Read the full picture with the skill's \`status.sh\`. Say this to the user rather than acting on it unprompted — one of these may be a run they still intend to resume."

jq -n --arg c "$BODY" '{hookSpecificOutput:{hookEventName:"SessionStart", additionalContext:$c}}'
exit 0
