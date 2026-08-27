#!/usr/bin/env bash
# better-loop disarm — mark the loop ended and say what is left to cancel.
#
#   disarm.sh <slug>       end one loop
#   disarm.sh --all        end every loop in this repo
#   disarm.sh <slug> --loop-md   also remove .claude/loop.md (only relevant when
#                                the loop was composed with the built-in /loop)
#
# The watcher is a Monitor in the session, not a file. Marking the state ended
# makes it exit on its next poll; TaskStop ends it immediately.
set -uo pipefail
ALL=0; RM_LOOPMD=0; SLUG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --all)     ALL=1; shift ;;
    --loop-md) RM_LOOPMD=1; shift ;;
    -*) shift ;;
    *) SLUG="$1"; shift ;;
  esac
done
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
command -v jq >/dev/null 2>&1 || { echo "jq required"; exit 2; }

backup() {
  cp "$1" "$1.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
    echo "${0##*/}: could not back up $1 — refusing to modify it" >&2; exit 1; }
}

shopt -s nullglob 2>/dev/null || true
STATES=( "$ROOT"/.claude/loops/*.json )
[ "${#STATES[@]}" -gt 0 ] || { echo "no loops armed in $ROOT"; }

TOUCHED=0
for f in "${STATES[@]}"; do
  s="$(jq -r '.slug // ""' "$f" 2>/dev/null || true)"; [ -n "$s" ] || continue
  if [ "$ALL" -eq 0 ] && [ -n "$SLUG" ] && [ "$s" != "$SLUG" ]; then continue; fi
  if [ "$ALL" -eq 0 ] && [ -z "$SLUG" ] && [ "${#STATES[@]}" -gt 1 ]; then
    echo "several loops are armed here — name one, or pass --all:"
    printf '  %s\n' "$(jq -r '.slug' "${STATES[@]}" 2>/dev/null)"
    exit 2
  fi
  tmp="$(mktemp)"
  jq --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.armed=false | .ended_at=$t | .end_reason=(.end_reason // "disarmed")' "$f" >"$tmp" && mv "$tmp" "$f"
  echo "ended: $s   (state kept at $f)"
  TOUCHED=1
done
[ "$TOUCHED" -eq 1 ] || { echo "no loop named '${SLUG}' in $ROOT"; exit 1; }

if [ "$RM_LOOPMD" -eq 1 ]; then
  TARGET="$ROOT/.claude/loop.md"
  if [ -f "$TARGET" ]; then
    backup "$TARGET"; rm "$TARGET" || { echo "${0##*/}: could not remove $TARGET" >&2; exit 1; }
    echo "removed $TARGET (backed up)"
    [ -f "$HOME/.claude/loop.md" ] && echo "note: ~/.claude/loop.md is no longer shadowed and now applies to a bare /loop"
  else
    echo "no .claude/loop.md in $ROOT"
  fi
fi

# Remove the SessionStart sentinel once no loop in the repo is still armed, the
# same way the loop leaves nothing else behind.
REMAINING=0
for f in "${STATES[@]}"; do
  [ "$(jq -r '.armed // false' "$f" 2>/dev/null || echo false)" = "true" ] && REMAINING=$((REMAINING + 1))
done
SETTINGS="$ROOT/.claude/settings.local.json"
if [ "$REMAINING" -eq 0 ] && [ -f "$SETTINGS" ] && \
   jq -e '[(.hooks.SessionStart // [])[] | (.hooks // [])[] | .command? // ""] | map(test("better-loop.*sentinel\\.sh")) | any' "$SETTINGS" >/dev/null 2>&1; then
  backup "$SETTINGS"
  tmp="$(mktemp)"
  jq '.hooks.SessionStart = ((.hooks.SessionStart // []) | map(select(((.hooks // [])
        | map(.command? // "") | map(test("better-loop.*sentinel\\.sh")) | any) | not)))
      | if (.hooks.SessionStart // []) == [] then del(.hooks.SessionStart) else . end
      | if (.hooks // {}) == {} then del(.hooks) else . end' "$SETTINGS" >"$tmp" && mv "$tmp" "$SETTINGS" \
    || { echo "disarm.sh: settings rewrite failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; }
  echo "removed the SessionStart sentinel from $SETTINGS"
elif [ "$REMAINING" -gt 0 ]; then
  echo "$REMAINING loop(s) still armed — leaving the SessionStart sentinel registered."
fi

echo
echo "still to cancel in the session (these are not files):"
echo "  watcher       TaskStop <task id — find it with TaskList>; it also exits on its next poll now the state is ended"
echo "  cron job      CronDelete <id — find it with CronList>, only if one was scheduled alongside"
echo "  dynamic loop  ScheduleWakeup {stop: true}, or press Esc while it waits"
echo
echo "brief and ledger kept under docs/loops/"
exit 0
