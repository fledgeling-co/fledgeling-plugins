#!/usr/bin/env bash
# better-goal disarm — stop a run's guard, and clean up after the last one.
#
#   disarm.sh <slug>      disarm that run
#   disarm.sh --all       disarm every run in this repo
#   disarm.sh <slug> --keep-hook   leave the Stop hook and block cap in place
#
# When no armed run is left, the Stop hook and the block-cap override are
# removed by default and the cap is restored to whatever it was before arming.
# Leaving them behind is why "delete the stop hooks" used to be a manual job.
#
# The watcher is a Monitor in the session, not a file: stop it with TaskStop.
set -uo pipefail
ALL=0; KEEP=0; SLUG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --all) ALL=1; shift ;;
    --keep-hook) KEEP=1; shift ;;
    --remove) shift ;;   # accepted for compatibility; removal is now the default
    -*) shift ;;
    *) SLUG="$1"; shift ;;
  esac
done
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
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

PRIOR_CAP=""; TOUCHED=0
for f in "${STATES[@]}"; do
  s="$(jq -r '.slug // ""' "$f" 2>/dev/null || true)"
  [ -n "$s" ] || continue
  if [ "$ALL" -eq 0 ] && [ -n "$SLUG" ] && [ "$s" != "$SLUG" ]; then continue; fi
  if [ "$ALL" -eq 0 ] && [ -z "$SLUG" ] && [ "${#STATES[@]}" -gt 1 ]; then
    echo "several runs are armed here — name one, or pass --all:"
    printf '  %s\n' "$(jq -r '.slug' "${STATES[@]}" 2>/dev/null)"
    exit 2
  fi
  [ -z "$PRIOR_CAP" ] && PRIOR_CAP="$(jq -r '.prior_block_cap // ""' "$f" 2>/dev/null || true)"
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
  echo "$REMAINING run(s) still armed — leaving the Stop hook registered."
elif [ "$KEEP" -eq 1 ]; then
  echo "no runs left armed; --keep-hook given, so the Stop hook stays registered (inert)."
elif [ -f "$SETTINGS" ]; then
  backup "$SETTINGS"
  # arm.sh recorded whatever cap was there before it overwrote it. Restore that
  # rather than deleting the key, so a user who set their own does not lose it.
  # Passed as a jq --arg: interpolating it into the filter would not expand
  # inside single quotes, and would be injectable if it did.
  tmp="$(mktemp)"
  jq --arg pc "$PRIOR_CAP" '
      if .hooks.Stop then .hooks.Stop = (.hooks.Stop | map(select(
          ((.hooks // []) | map(.command? // "") | map(test("(better-goal|goal-harness).*(guard|goal-guard)\\.sh")) | any) | not))) else . end
    | if (.hooks.Stop // []) == [] then del(.hooks.Stop) else . end
    | if $pc == "" then del(.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP)
      else .env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP = $pc end
    | if (.env // {}) == {} then del(.env) else . end
    | if (.hooks // {}) == {} then del(.hooks) else . end' "$SETTINGS" >"$tmp" && mv "$tmp" "$SETTINGS" \
    || { echo "disarm.sh: settings rewrite failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; exit 2; }
  if [ -n "$PRIOR_CAP" ]; then
    echo "removed the Stop hook; block cap restored to $PRIOR_CAP in $SETTINGS"
  else
    echo "removed the Stop hook and the block-cap override from $SETTINGS"
  fi
fi

echo "the watcher is a Monitor in the session — stop it with TaskStop, or let it exit on its own (it ends when the run disarms)."
exit 0
