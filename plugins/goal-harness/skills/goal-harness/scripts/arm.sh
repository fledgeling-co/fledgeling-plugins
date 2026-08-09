#!/usr/bin/env bash
# goal-harness arm — write the state file and register the Stop guard.
#
#   arm.sh --state <path-to-goal-state.json> [--dry-run]
#
# --dry-run prints the exact settings diff and writes nothing. Always run it
# first; settings are load-bearing across every session in scope.

set -uo pipefail
SRC=""; DRY=0; CAP="${GOAL_HARNESS_BLOCK_CAP:-500}"
while [ $# -gt 0 ]; do
  case "$1" in
    --state)   SRC="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --cap)     CAP="${2:-500}"; shift 2 ;;
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
[ -n "$SID" ] || echo "arm.sh: warning — no session id; the guard will fire in every session in this project" >&2

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
echo
echo "── state: $STATE"
if [ -f "$STATE" ]; then
  diff -u <(jq -S . "$STATE") <(jq -S --arg s "$SID" '.armed=true | .session_id=$s' "$SRC") || true
else
  echo "(new file)"; jq -S --arg s "$SID" '.armed=true | .session_id=$s' "$SRC"
fi

if [ "$DRY" -eq 1 ]; then
  echo; echo "dry run — nothing written. Re-run without --dry-run to apply."
  exit 0
fi

mkdir -p "$ROOT/.claude"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak.$STAMP"
[ -f "$STATE" ]    && cp "$STATE"    "$STATE.bak.$STAMP"

printf '%s\n' "$NEW_SETTINGS" | jq . >"$SETTINGS"
jq --arg s "$SID" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg c "$ROOT" \
   '.armed=true | .session_id=$s | .started_at=$t | .cwd=$c | .iteration=0' "$SRC" >"$STATE"

grep -qxF '.claude/goal-state.json' "$ROOT/.gitignore" 2>/dev/null || \
  printf '\n# goal-harness\n.claude/goal-state.json\n.claude/settings.local.json.bak.*\n' >>"$ROOT/.gitignore" 2>/dev/null || true

echo
echo "armed: $(jq -r '.slug' "$STATE")  session=${SID:-<any>}  gates=$(jq -r '.verify | length' "$STATE")"
echo "backups: ${SETTINGS}.bak.${STAMP}"
echo "disarm:  $(dirname "$GUARD")/disarm.sh"
