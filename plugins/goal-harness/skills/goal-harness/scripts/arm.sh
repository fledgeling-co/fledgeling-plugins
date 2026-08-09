#!/usr/bin/env bash
# goal-harness arm — write the state file and register the Stop guard.
#
#   arm.sh --state <path-to-goal-state.json> [--dry-run]
#
# --dry-run prints the exact settings diff and writes nothing. Always run it
# first; settings are load-bearing across every session in scope.

set -uo pipefail
SRC=""; DRY=0; CAP="${GOAL_HARNESS_BLOCK_CAP:-500}"
# `shift 2` fails with $# unchanged when a flag is passed as the last argument,
# so the same branch re-matches and the loop spins forever. Fail loudly instead.
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

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
GUARD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/goal-guard.sh"
SETTINGS="$ROOT/.claude/settings.local.json"
STATE="$ROOT/.claude/goal-state.json"
SID="${CLAUDE_CODE_SESSION_ID:-$(jq -r '.session_id // ""' "$SRC")}"
# The guard now refuses to act on a state file with no session id, so arming
# without one produces a goal that never fires rather than one that fires everywhere.
[ -n "$SID" ] || { echo "arm.sh: no session id available (CLAUDE_CODE_SESSION_ID unset and none in the state file)." >&2
                   echo "        The guard refuses to act without one. Arm from the driving session." >&2; exit 2; }

# The settings file is rewritten below, so it has to be readable as JSON first:
# an invalid one made the jq pipeline yield nothing and the redirect truncated
# the file to zero bytes, taking the user's other hooks and permissions with it.
if [ -f "$SETTINGS" ] && ! jq -e . "$SETTINGS" >/dev/null 2>&1; then
  echo "arm.sh: $SETTINGS is not valid JSON — fix or move it before arming; nothing written" >&2
  exit 2
fi

# F8: remember any cap the user already had, so disarm can put it back.
PRIOR_CAP="$(jq -r '.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP // ""' "$SETTINGS" 2>/dev/null || true)"

NEW_SETTINGS="$(
  { [ -f "$SETTINGS" ] && cat "$SETTINGS" || echo '{}'; } | jq \
    --arg guard "$GUARD" --arg cap "$CAP" '
    .env = ((.env // {}) | .CLAUDE_CODE_STOP_HOOK_BLOCK_CAP = $cap)
    | .hooks = (.hooks // {})
    | .hooks.Stop = (
        ((.hooks.Stop // []) | map(select(
           (.hooks // []) | map(.command? // "") | index($guard) | not )))
        + [{ hooks: [{ type: "command", command: $guard, timeout: 1200,
                       statusMessage: "goal-harness: verifying gates" }] }]
      )'
)"

echo "── settings: $SETTINGS"
if [ -f "$SETTINGS" ]; then
  diff -u <(jq -S . "$SETTINGS") <(printf '%s' "$NEW_SETTINGS" | jq -S .) || true
else
  echo "(new file)"; printf '%s\n' "$NEW_SETTINGS" | jq -S .
fi
NEW_STATE="$(jq --arg s "$SID" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg c "$ROOT" --arg pc "$PRIOR_CAP" \
  '.armed=true | .session_id=$s | .started_at=$t | .cwd=$c | .iteration=0 | .prior_block_cap=$pc' "$SRC")"

echo
echo "── state: $STATE"
if [ -f "$STATE" ]; then
  diff -u <(jq -S . "$STATE") <(printf '%s' "$NEW_STATE" | jq -S .) || true
else
  echo "(new file)"; printf '%s' "$NEW_STATE" | jq -S .
fi

if [ "$DRY" -eq 1 ]; then
  echo; echo "dry run — nothing written. Re-run without --dry-run to apply."
  exit 0
fi

mkdir -p "$ROOT/.claude"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak.$STAMP"
[ -f "$STATE" ]    && cp "$STATE"    "$STATE.bak.$STAMP"

[ -n "$NEW_SETTINGS" ] && [ -n "$NEW_STATE" ] || {
  echo "arm.sh: could not build the new settings/state; nothing written" >&2; exit 2; }

tmp="$(mktemp)"; printf '%s\n' "$NEW_SETTINGS" | jq . >"$tmp" && mv "$tmp" "$SETTINGS" || {
  echo "arm.sh: settings write failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; exit 2; }
tmp="$(mktemp)"; printf '%s\n' "$NEW_STATE"    | jq . >"$tmp" && mv "$tmp" "$STATE"    || {
  echo "arm.sh: state write failed; $STATE left as it was" >&2; rm -f "$tmp"; exit 2; }

grep -qxF '.claude/goal-state.json' "$ROOT/.gitignore" 2>/dev/null || \
  printf '\n# goal-harness\n.claude/goal-state.json\n.claude/settings.local.json.bak.*\n' >>"$ROOT/.gitignore" 2>/dev/null || \
  echo "arm.sh: WARNING could not update .gitignore. goal-state.json's verify[] commands are executed by the Stop hook, so it must never be committed." >&2

echo
echo "armed: $(jq -r '.slug' "$STATE")  session=${SID:-<any>}  gates=$(jq -r '.verify | length' "$STATE")"
echo "backups: ${SETTINGS}.bak.${STAMP}"
echo "disarm:  $(dirname "$GUARD")/disarm.sh"
