#!/usr/bin/env bash
# better-goal arm — write the per-slug state file for a run whose guard is
# already registered at user scope.
#
#   arm.sh --state <path-to-draft-state.json> [--dry-run] [--cap 500]
#
# --dry-run prints the exact diff and writes nothing.
#
# Arming no longer writes hooks. Hook configuration is snapshotted when the
# Claude Code process starts, so a hook written here would load in the NEXT
# session and not this one — measured on 2.1.260 across 948 turns and four
# settings rewrites, whether or not a settings file already existed. The guard
# is registered once, at user scope, by install.sh (which this script runs when
# it finds no registration), and from then on arming is a state write that the
# already-loaded guard picks up on the very next turn.
#
# Whether the guard is loaded in THIS session is read from a heartbeat file the
# sentinel (SessionStart) or the guard (Stop) wrote under this session id —
# never inferred from what the settings files say, because the files and the
# running process disagree exactly when it matters.
#
# State lives at .claude/goals/<slug>.json, one file per run, so two runs in one
# repo — a worktree and its parent, two features in flight — do not overwrite
# each other's gates.

set -uo pipefail
SRC=""; DRY=0; CAP="${BETTER_GOAL_BLOCK_CAP:-500}"
need() { [ "$1" -ge 2 ] || { echo "${0##*/}: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --state)   need $# --state; SRC="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --cap)     need $# --cap; CAP="${2:-500}"; shift 2 ;;
    *) shift ;;
  esac
done
[ -n "$SRC" ] && [ -f "$SRC" ] || { echo "arm.sh: --state <file> is required" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "arm.sh: jq is required" >&2; exit 2; }
jq -e . "$SRC" >/dev/null || { echo "arm.sh: state file is not valid JSON" >&2; exit 2; }

SLUG="$(jq -r '.slug // ""' "$SRC")"
[ -n "$SLUG" ] || { echo "arm.sh: the state file needs a .slug" >&2; exit 2; }
case "$SLUG" in *[!a-zA-Z0-9._-]*)
  echo "arm.sh: slug '$SLUG' must be a bare kebab name — it becomes a filename" >&2; exit 2 ;;
esac

backup() {
  cp "$1" "$1.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
    echo "${0##*/}: could not back up $1 — refusing to modify it" >&2; exit 1; }
}

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCH="$HERE/watch.sh"
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
STATE="$ROOT/.claude/goals/${SLUG}.json"
LOCAL_SETTINGS="$ROOT/.claude/settings.local.json"
OURS_RE='(better-goal|goal-harness).*(guard|goal-guard|sentinel)\.sh'

SID="${CLAUDE_CODE_SESSION_ID:-$(jq -r '.session_id // ""' "$SRC")}"
[ -n "$SID" ] || { echo "arm.sh: no session id available (CLAUDE_CODE_SESSION_ID unset and none in the state file)." >&2
                   echo "        The guard refuses to act without one. Arm from the driving session." >&2; exit 2; }

# --- is the guard registered anywhere the next session will read? ----------
registered_in() {
  local f
  for f in "$CFG/settings.json" "$ROOT/.claude/settings.json" "$LOCAL_SETTINGS"; do
    [ -f "$f" ] || continue
    jq -e --arg re "$OURS_RE" '[(.hooks.Stop // [])[] | (.hooks // [])[] | .command? // ""] | map(test($re)) | any' \
      "$f" >/dev/null 2>&1 && printf '%s\n' "$f"
  done
}
REGS="$(registered_in)"
USER_REG=0; grep -qxF "$CFG/settings.json" <<<"$REGS" && USER_REG=1

# --- is it LOADED in this session? -------------------------------------------
HB="$CFG/better-goal/live/$SID.json"
HOOK_LIVE=unproven; HOOK_EVIDENCE=none; HB_LINE=""
if [ -f "$HB" ]; then
  HB_EVENT="$(jq -r '.event // ""' "$HB" 2>/dev/null || true)"
  HB_AT="$(jq -r '.at // ""' "$HB" 2>/dev/null || true)"
  case "$HB_EVENT" in
    Stop|StopFailure|SessionEnd) HOOK_LIVE=proven; HOOK_EVIDENCE=guard ;;
    SessionStart)
      # The sentinel fired at startup, so whatever registered the guard beside
      # it was in the snapshot too — if the guard was registered at that moment.
      if [ "$(jq -r '(.guard_registered_in // []) | length' "$HB" 2>/dev/null || echo 0)" -gt 0 ]; then
        HOOK_LIVE=proven; HOOK_EVIDENCE=sentinel
      fi ;;
  esac
  HB_LINE="$HB_EVENT at $HB_AT"
fi

# --- state -------------------------------------------------------------------
NEW_STATE="$(jq --arg s "$SID" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg c "$ROOT" \
  --arg hl "$HOOK_LIVE" --arg he "$HOOK_EVIDENCE" \
  '.armed=true | .session_id=$s | .started_at=$t | .cwd=$c | .iteration=0
   | .repeat_count=0 | .escalated=false | .last_fingerprint="" | .last_failing=""
   | .set_repeat_count=0 | .set_escalated=false | .last_failing_set=""
   | .stuck_after=(.stuck_after // 3)
   | .set_stuck_after=(.set_stuck_after // 8)
   | .hook_live=$hl | .hook_evidence=$he
   | del(.settings_preexisted) | del(.prior_block_cap) | del(.external_verifier)
   | del(.last_guard_at) | del(.hook_proven_at) | del(.reported_end)
   | .stop_failures=0 | del(.end_reason) | del(.ended_at) | del(.stuck_on)' "$SRC")"

echo "── state: $STATE"
if [ -f "$STATE" ]; then
  diff -u <(jq -S . "$STATE") <(printf '%s' "$NEW_STATE" | jq -S .) || true
else
  echo "(new file)"; printf '%s' "$NEW_STATE" | jq -S .
fi

# --- legacy: a per-project registration written by arm.sh ≤2.2.x -----------
# Two registrations (project-local at one cache path, user-level at another)
# both fire and run every gate twice a turn. Strip ours from the project-local
# file once the user-level one exists; the running session keeps its snapshot
# either way, so this changes nothing until the next session, which is exactly
# when the user-level one starts loading.
STRIP_LOCAL=0
if [ -f "$LOCAL_SETTINGS" ] && grep -qxF "$LOCAL_SETTINGS" <<<"$REGS"; then
  STRIP_LOCAL=1
  echo
  echo "── $LOCAL_SETTINGS carries a per-project registration from an earlier better-goal;"
  echo "   it will be removed so the user-scope guard is the only one that fires."
fi

if [ "$DRY" -eq 1 ]; then
  echo; echo "dry run — nothing written. Re-run without --dry-run to apply."
  [ "$USER_REG" -eq 1 ] || echo "(install.sh would also register the guard at user scope: $CFG/settings.json)"
  exit 0
fi

# --- register at user scope if nothing will load it next time ----------------
if [ "$USER_REG" -eq 0 ]; then
  echo
  "$HERE/install.sh" --cap "$CAP" || { echo "arm.sh: install.sh failed; not arming" >&2; exit 2; }
fi

mkdir -p "$ROOT/.claude/goals"
[ -f "$STATE" ] && backup "$STATE"
[ -n "$NEW_STATE" ] || { echo "arm.sh: could not build the new state; nothing written" >&2; exit 2; }
tmp="$(mktemp)"; printf '%s\n' "$NEW_STATE" | jq . >"$tmp" && mv "$tmp" "$STATE" || {
  echo "arm.sh: state write failed; $STATE left as it was" >&2; rm -f "$tmp"; exit 2; }

if [ "$STRIP_LOCAL" -eq 1 ] && jq -e . "$LOCAL_SETTINGS" >/dev/null 2>&1; then
  backup "$LOCAL_SETTINGS"
  tmp="$(mktemp)"
  jq --arg re "$OURS_RE" '
      def ours: test($re);
      def strip(ev): if .hooks[ev] then .hooks[ev] = (.hooks[ev] | map(select(
          ((.hooks // []) | map(.command? // "") | map(ours) | any) | not))) else . end
        | if (.hooks[ev] // []) == [] then del(.hooks[ev]) else . end;
      strip("Stop") | strip("StopFailure") | strip("SessionEnd") | strip("SessionStart")
    | if (.hooks // {}) == {} then del(.hooks) else . end' "$LOCAL_SETTINGS" >"$tmp" \
    && mv "$tmp" "$LOCAL_SETTINGS" || { rm -f "$tmp"; echo "arm.sh: could not clean $LOCAL_SETTINGS; left as it was" >&2; }
fi

grep -qxF '.claude/goals/' "$ROOT/.gitignore" 2>/dev/null || \
  printf '\n# better-goal\n.claude/goals/\n.claude/settings.local.json.bak.*\n' >>"$ROOT/.gitignore" 2>/dev/null || \
  echo "arm.sh: WARNING could not update .gitignore. The state file's verify[] commands are executed by the Stop hook, so it must never be committed." >&2

echo
echo "armed: $SLUG  session=$SID  gates=$(jq -r '.verify | length' "$STATE")  stuck_after=$(jq -r '.stuck_after' "$STATE")"
echo "guard:  registered at user scope in $CFG/settings.json (Stop + StopFailure + SessionEnd; sentinel on SessionStart)"
echo
case "$HOOK_EVIDENCE" in
  guard)    echo "hook load: LIVE — the guard already fired in this session ($HB_LINE). It runs the gates at the end of this turn." ;;
  sentinel) echo "hook load: LIVE — the sentinel fired at this session's start with the guard registered beside it ($HB_LINE)."
            echo "           hook_live=proven; the first ledger row lands at the end of this turn." ;;
  *)
    echo "HOOK NOT LOADED IN THIS SESSION — no heartbeat exists for session $SID."
    echo "  Hook configuration is snapshotted at process start, so the registration just written"
    echo "  (or one written mid-session earlier) loads from the NEXT session. Restart Claude Code,"
    echo "  or open /hooks once, then re-run arm.sh from that session. Until then the run is NOT"
    echo "  armed whatever the state file says. Do not build a substitute verifier: a loop that"
    echo "  appends ledger rows cannot block a turn, and it blinds the watcher that would have"
    echo "  reported the stall." ;;
esac
echo
echo "Arm the out-of-band watcher next — the guard cannot see a run that dies mid-turn:"
echo "  Monitor({ command: \"$WATCH $SLUG\", description: \"goal $SLUG liveness\", persistent: true })"
echo
echo "status:  $HERE/status.sh"
echo "disarm:  $HERE/disarm.sh $SLUG"
