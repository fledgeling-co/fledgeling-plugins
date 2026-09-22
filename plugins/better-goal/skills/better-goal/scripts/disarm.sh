#!/usr/bin/env bash
# better-goal disarm — stop a run's guard, and clean up after the last one.
#
#   disarm.sh <slug>      disarm that run
#   disarm.sh --all       disarm every run in this repo
#   disarm.sh --uninstall  also remove the user-scope registration install.sh wrote
#
# Disarming is a state write. The guard stays registered at user scope (it is
# inert unless a run is armed by the ending session), because removing and
# re-adding a hook is what forces a restart every time — hook configuration is
# snapshotted at process start. A per-project registration left by better-goal
# 2.2.x is still cleaned out of .claude/settings.local.json here, so a later
# session does not run every gate twice.
#
# The watcher is a Monitor in the session, not a file: stop it with TaskStop.
set -uo pipefail
ALL=0; KEEP=0; SLUG=""; UNINSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --all) ALL=1; shift ;;
    --keep-hook) KEEP=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --remove) shift ;;   # accepted for compatibility; removal is now the default
    -*) shift ;;
    *) SLUG="$1"; shift ;;
  esac
done
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETTINGS="$ROOT/.claude/settings.local.json"
command -v jq >/dev/null 2>&1 || { echo "jq required"; exit 2; }

# A backup is a precondition, not a courtesy: if it fails we must not proceed to
# the destructive step, and we must never claim it happened. Reproduced on a
# read-only .claude/: the backup failed, the overwrite succeeded anyway, and the
# script printed "wrote" and exited 0 with the previous file unrecoverable.
backup() {
  cp "$1" "$1.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
    echo "${0##*/}: could not back up $1 — refusing to modify it" >&2; exit 1; }
}

shopt -s nullglob 2>/dev/null || true
STATES=( "$ROOT"/.claude/goals/*.json )
[ -f "$ROOT/.claude/goal-state.json" ] && STATES+=( "$ROOT/.claude/goal-state.json" )
[ "${#STATES[@]}" -gt 0 ] || { echo "no runs armed in $ROOT"; exit 0; }

TOUCHED=0
for f in "${STATES[@]}"; do
  s="$(jq -r '.slug // ""' "$f" 2>/dev/null || true)"
  [ -n "$s" ] || continue
  if [ "$ALL" -eq 0 ] && [ -n "$SLUG" ] && [ "$s" != "$SLUG" ]; then continue; fi
  if [ "$ALL" -eq 0 ] && [ -z "$SLUG" ] && [ "${#STATES[@]}" -gt 1 ]; then
    echo "several runs are armed here — name one, or pass --all:"
    printf '  %s\n' "$(jq -r '.slug' "${STATES[@]}" 2>/dev/null)"
    exit 2
  fi
  tmp="$(mktemp)"
  jq --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.armed=false | .ended_at=$t | .end_reason=(.end_reason // "disarmed")' "$f" >"$tmp" && mv "$tmp" "$f"
  echo "disarmed: $s   (state kept at $f)"
  TOUCHED=1
done
[ "$TOUCHED" -eq 1 ] || { echo "no run named '${SLUG}' in $ROOT"; exit 1; }

REMAINING=0
for f in "${STATES[@]}"; do
  [ "$(jq -r '.armed // false' "$f" 2>/dev/null || echo false)" = "true" ] && REMAINING=$((REMAINING + 1))
done

if [ "$REMAINING" -gt 0 ]; then
  echo "$REMAINING run(s) still armed."
elif [ "$KEEP" -eq 0 ] && [ -f "$SETTINGS" ] && jq -e . "$SETTINGS" >/dev/null 2>&1 \
     && jq -e '[.. | .command? // "" | strings] | map(test("(better-goal|goal-harness).*(guard|goal-guard|sentinel)\\.sh")) | any' "$SETTINGS" >/dev/null 2>&1; then
  # Legacy: arm.sh ≤2.2.x registered here per project. Remove ours; leave the
  # env cap, which is harmless and may be the user's own.
  backup "$SETTINGS"
  tmp="$(mktemp)"
  jq '
      def ours: test("(better-goal|goal-harness).*(guard|goal-guard|sentinel)\\.sh");
      def strip(ev): if .hooks[ev] then .hooks[ev] = (.hooks[ev] | map(select(
          ((.hooks // []) | map(.command? // "") | map(ours) | any) | not))) else . end
        | if (.hooks[ev] // []) == [] then del(.hooks[ev]) else . end;
      strip("Stop") | strip("StopFailure") | strip("SessionEnd") | strip("SessionStart")
    | if (.hooks // {}) == {} then del(.hooks) else . end' "$SETTINGS" >"$tmp" && mv "$tmp" "$SETTINGS" \
    || { echo "disarm.sh: settings rewrite failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; exit 2; }
  echo "removed a per-project registration left by an earlier better-goal from $SETTINGS (the user-scope guard is the one that fires)."
fi

if [ "$UNINSTALL" -eq 1 ]; then
  "$HERE/install.sh" --remove
fi

echo "the watcher is a Monitor in the session — stop it with TaskStop, or let it exit on its own (it ends when the run disarms)."
exit 0
