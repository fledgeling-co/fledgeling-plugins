#!/usr/bin/env bash
# better-goal arm — write the per-slug state file and register the Stop guard.
#
#   arm.sh --state <path-to-draft-state.json> [--dry-run] [--cap 500]
#
# --dry-run prints the exact settings diff and writes nothing. Always run it
# first; settings are load-bearing across every session in scope.
#
# State lives at .claude/goals/<slug>.json, one file per run, so two runs in one
# repo — a worktree and its parent, two features in flight — do not overwrite
# each other's gates.

set -uo pipefail
SRC=""; DRY=0; CAP="${BETTER_GOAL_BLOCK_CAP:-500}"
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

SLUG="$(jq -r '.slug // ""' "$SRC")"
[ -n "$SLUG" ] || { echo "arm.sh: the state file needs a .slug" >&2; exit 2; }
case "$SLUG" in *[!a-zA-Z0-9._-]*)
  echo "arm.sh: slug '$SLUG' must be a bare kebab name — it becomes a filename" >&2; exit 2 ;;
esac

# A backup is a precondition, not a courtesy: if it fails we must not proceed to
# the destructive step, and we must never claim it happened. Reproduced on a
# read-only .claude/: the backup failed, the overwrite succeeded anyway, and the
# script printed "wrote" and exited 0 with the previous file unrecoverable.
backup() {
  cp "$1" "$1.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
    echo "${0##*/}: could not back up $1 — refusing to modify it" >&2; exit 1; }
}

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARD="$HERE/guard.sh"
WATCH="$HERE/watch.sh"
SETTINGS="$ROOT/.claude/settings.local.json"
STATE="$ROOT/.claude/goals/${SLUG}.json"
SID="${CLAUDE_CODE_SESSION_ID:-$(jq -r '.session_id // ""' "$SRC")}"
# The guard refuses to act on a state file with no session id, so arming without
# one produces a run that never fires rather than one that fires everywhere.
[ -n "$SID" ] || { echo "arm.sh: no session id available (CLAUDE_CODE_SESSION_ID unset and none in the state file)." >&2
                   echo "        The guard refuses to act without one. Arm from the driving session." >&2; exit 2; }

# The settings file is rewritten below, so it has to be readable as JSON first:
# an invalid one made the jq pipeline yield nothing and the redirect truncated
# the file to zero bytes, taking the user's other hooks and permissions with it.
if [ -f "$SETTINGS" ] && ! jq -e . "$SETTINGS" >/dev/null 2>&1; then
  echo "arm.sh: $SETTINGS is not valid JSON — fix or move it before arming; nothing written" >&2
  exit 2
fi

# Remember any cap the user already had, so disarm can put it back.
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
                       statusMessage: "better-goal: verifying gates" }] }]
      )'
)"

echo "── settings: $SETTINGS"
if [ -f "$SETTINGS" ]; then
  diff -u <(jq -S . "$SETTINGS") <(printf '%s' "$NEW_SETTINGS" | jq -S .) || true
else
  echo "(new file)"; printf '%s\n' "$NEW_SETTINGS" | jq -S .
fi

NEW_STATE="$(jq --arg s "$SID" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg c "$ROOT" --arg pc "$PRIOR_CAP" \
  '.armed=true | .session_id=$s | .started_at=$t | .cwd=$c | .iteration=0
   | .repeat_count=0 | .escalated=false | .last_fingerprint="" | .last_failing=""
   | .stuck_after=(.stuck_after // 3) | .prior_block_cap=$pc' "$SRC")"

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

mkdir -p "$ROOT/.claude/goals"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
[ -f "$SETTINGS" ] && backup "$SETTINGS"
[ -f "$STATE" ]    && backup "$STATE"

[ -n "$NEW_SETTINGS" ] && [ -n "$NEW_STATE" ] || {
  echo "arm.sh: could not build the new settings/state; nothing written" >&2; exit 2; }

tmp="$(mktemp)"; printf '%s\n' "$NEW_SETTINGS" | jq . >"$tmp" && mv "$tmp" "$SETTINGS" || {
  echo "arm.sh: settings write failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; exit 2; }
tmp="$(mktemp)"; printf '%s\n' "$NEW_STATE"    | jq . >"$tmp" && mv "$tmp" "$STATE"    || {
  echo "arm.sh: state write failed; $STATE left as it was" >&2; rm -f "$tmp"; exit 2; }

grep -qxF '.claude/goals/' "$ROOT/.gitignore" 2>/dev/null || \
  printf '\n# better-goal\n.claude/goals/\n.claude/settings.local.json.bak.*\n' >>"$ROOT/.gitignore" 2>/dev/null || \
  echo "arm.sh: WARNING could not update .gitignore. The state file's verify[] commands are executed by the Stop hook, so it must never be committed." >&2

echo
echo "armed: $SLUG  session=$SID  gates=$(jq -r '.verify | length' "$STATE")  stuck_after=$(jq -r '.stuck_after' "$STATE")"
echo "backups: ${SETTINGS}.bak.${STAMP}"
echo
echo "Arm the out-of-band watcher next — the guard cannot see a run that dies mid-turn:"
echo "  Monitor({ command: \"$WATCH $SLUG\", description: \"goal $SLUG liveness\", persistent: true })"
echo
echo "status:  $HERE/status.sh"
echo "disarm:  $HERE/disarm.sh $SLUG"
