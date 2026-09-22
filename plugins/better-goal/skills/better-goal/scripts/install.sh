#!/usr/bin/env bash
# better-goal install — register the guard ONCE, at user scope, so arming never
# has to touch hook configuration again.
#
#   install.sh [--dry-run] [--remove] [--cap 500] [--scope user|project]
#
# WHY THIS EXISTS. Claude Code snapshots hook configuration when the process
# starts. A hook written into any settings file mid-session — user, project or
# local, whether or not that file already existed — is stored correctly and
# never loaded until the user opens /hooks or restarts. Measured on 2.1.260:
# the same three Stop hooks ran for 948 consecutive turns across four rewrites
# of .claude/settings.local.json by arm.sh and disarm.sh, and the guard was in
# none of them. So arming by writing a hook is arming for the NEXT session, and
# the run that asked for it gets nothing.
#
# The guard is safe to leave registered everywhere: it exits in a few
# milliseconds unless the repo has .claude/goals/ AND a state file there was
# armed by the session that is ending. Registering it once at user scope means
# every later session starts with it loaded, and arm.sh becomes a pure state
# write that takes effect on the very next turn.
#
# Idempotent. Re-running replaces an older registration (the plugin cache path
# carries the version, so exact-path matching would accumulate one guard per
# version and run every gate N times a turn).

set -uo pipefail
DRY=0; REMOVE=0; CAP="${BETTER_GOAL_BLOCK_CAP:-500}"; SCOPE=user
need() { [ "$1" -ge 2 ] || { echo "${0##*/}: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --remove)  REMOVE=1; shift ;;
    --cap)     need $# --cap; CAP="${2:-500}"; shift 2 ;;
    --scope)   need $# --scope; SCOPE="${2:-user}"; shift 2 ;;
    *) shift ;;
  esac
done
command -v jq >/dev/null 2>&1 || { echo "install.sh: jq is required" >&2; exit 2; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARD="$HERE/guard.sh"; SENTINEL="$HERE/sentinel.sh"
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
case "$SCOPE" in
  user)    SETTINGS="$CFG/settings.json" ;;
  project) ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; SETTINGS="$ROOT/.claude/settings.json" ;;
  *) echo "install.sh: --scope must be user or project" >&2; exit 2 ;;
esac

if [ -f "$SETTINGS" ] && ! jq -e . "$SETTINGS" >/dev/null 2>&1; then
  echo "install.sh: $SETTINGS is not valid JSON — fix it first; nothing written" >&2; exit 2
fi

OURS_RE='(better-goal|goal-harness).*(guard|goal-guard|sentinel)\.sh'

if [ "$REMOVE" -eq 1 ]; then
  NEW="$( { [ -f "$SETTINGS" ] && cat "$SETTINGS" || echo '{}'; } | jq --arg re "$OURS_RE" '
    def ours: test($re);
    def strip(ev): if .hooks[ev] then .hooks[ev] = (.hooks[ev] | map(select(
        ((.hooks // []) | map(.command? // "") | map(ours) | any) | not))) else . end
      | if (.hooks[ev] // []) == [] then del(.hooks[ev]) else . end;
    strip("Stop") | strip("StopFailure") | strip("SessionEnd") | strip("SessionStart")
    | if (.hooks // {}) == {} then del(.hooks) else . end')"
else
  NEW="$( { [ -f "$SETTINGS" ] && cat "$SETTINGS" || echo '{}'; } | jq \
    --arg guard "$GUARD" --arg sentinel "$SENTINEL" --arg cap "$CAP" --arg re "$OURS_RE" '
    def drop_ours: map(select(((.hooks // []) | map(.command? // "")
                               | map(test($re)) | any) | not));
    .env = ((.env // {}) | if has("CLAUDE_CODE_STOP_HOOK_BLOCK_CAP") then . else .CLAUDE_CODE_STOP_HOOK_BLOCK_CAP = $cap end)
    | .hooks = (.hooks // {})
    | .hooks.Stop = ((.hooks.Stop // []) | drop_ours
        + [{ hooks: [{ type: "command", command: $guard, timeout: 1200,
                       statusMessage: "better-goal: verifying gates" }] }])
    | .hooks.StopFailure = ((.hooks.StopFailure // []) | drop_ours
        + [{ hooks: [{ type: "command", command: $guard, timeout: 120,
                       statusMessage: "better-goal: recording an API-error stop" }] }])
    | .hooks.SessionEnd = ((.hooks.SessionEnd // []) | drop_ours
        + [{ hooks: [{ type: "command", command: $guard, timeout: 120,
                       statusMessage: "better-goal: recording the session ending" }] }])
    | .hooks.SessionStart = ((.hooks.SessionStart // []) | drop_ours
        + [{ hooks: [{ type: "command", command: $sentinel, timeout: 60,
                       statusMessage: "better-goal: checking for stalled runs" }] }])')"
fi
[ -n "$NEW" ] || { echo "install.sh: could not build the new settings; nothing written" >&2; exit 2; }

echo "── settings: $SETTINGS"
if [ -f "$SETTINGS" ]; then
  if diff -u <(jq -S . "$SETTINGS") <(printf '%s' "$NEW" | jq -S .); then
    echo "(already registered — no change)"; CHANGED=0
  else CHANGED=1; fi
else
  echo "(new file)"; printf '%s\n' "$NEW" | jq -S .; CHANGED=1
fi

# Is the registration LOADED in the session running this script? The only
# evidence is a heartbeat the sentinel or the guard wrote under this session id.
SID="${CLAUDE_CODE_SESSION_ID:-}"
LIVE=""
if [ -n "$SID" ] && [ -f "$CFG/better-goal/live/$SID.json" ]; then
  LIVE="$(jq -r '"\(.event) at \(.at)"' "$CFG/better-goal/live/$SID.json" 2>/dev/null || true)"
fi

if [ "$DRY" -eq 1 ]; then
  echo; echo "dry run — nothing written."
  exit 0
fi

if [ "$CHANGED" -eq 1 ]; then
  mkdir -p "$(dirname "$SETTINGS")"
  if [ -f "$SETTINGS" ]; then
    cp "$SETTINGS" "$SETTINGS.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
      echo "install.sh: could not back up $SETTINGS — refusing to modify it" >&2; exit 1; }
  fi
  tmp="$(mktemp)"; printf '%s\n' "$NEW" | jq . >"$tmp" && mv "$tmp" "$SETTINGS" || {
    echo "install.sh: write failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; exit 2; }
fi

echo
if [ "$REMOVE" -eq 1 ]; then
  echo "removed better-goal's Stop, StopFailure, SessionEnd and SessionStart registrations from $SETTINGS."
  echo "The running session keeps its startup snapshot; the removal applies from the next session."
  exit 0
fi

echo "registered: Stop + StopFailure + SessionEnd -> guard.sh; SessionStart -> sentinel.sh ($SCOPE scope)"
echo "block cap:  CLAUDE_CODE_STOP_HOOK_BLOCK_CAP=$(jq -r '.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP' "$SETTINGS") (env is also read at startup)"
echo
if [ -n "$LIVE" ]; then
  echo "loaded in THIS session: yes — heartbeat $LIVE. Arming now takes effect on the next turn."
else
  echo "loaded in THIS session: NO — no heartbeat for session ${SID:-<unknown>}."
  echo "  Hook config is snapshotted at process start, so this registration is live from the"
  echo "  next session onward. Restart Claude Code (or open /hooks once) before arming a run."
  echo "  Until then nothing verifies anything, and running the gates by hand is not a substitute."
fi
exit 0
