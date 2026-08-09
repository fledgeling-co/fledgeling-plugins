#!/usr/bin/env bash
# goal-harness disarm — stop the guard blocking. Leaves the brief and ledger.
#   disarm.sh              disarm the goal, keep the hook registered (inert)
#   disarm.sh --remove     also remove the Stop hook and put the block cap back
#                          to whatever it was before arm.sh ran (deleting the key
#                          only if there was nothing there to begin with)
set -uo pipefail
REMOVE=0; [ "${1:-}" = "--remove" ] && REMOVE=1
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE="$ROOT/.claude/goal-state.json"; SETTINGS="$ROOT/.claude/settings.local.json"
command -v jq >/dev/null 2>&1 || { echo "jq required"; exit 2; }

if [ -f "$STATE" ]; then
  tmp="$(mktemp)"
  jq --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.armed=false | .ended_at=$t | .end_reason="disarmed"' "$STATE" >"$tmp" && mv "$tmp" "$STATE"
  echo "disarmed: $(jq -r '.slug' "$STATE")"
else
  echo "no goal state in $ROOT"
fi

if [ "$REMOVE" -eq 1 ] && [ -f "$SETTINGS" ]; then
  cp "$SETTINGS" "$SETTINGS.bak.$(date -u +%Y%m%dT%H%M%SZ)"
  # arm.sh recorded whatever cap was there before it overwrote it. Restore that
  # rather than deleting the key, so a user who set their own does not lose it.
  # Passed as a jq --arg: interpolating it into the filter would not expand
  # inside single quotes, and would be injectable if it did.
  PC="$(jq -r '.prior_block_cap // ""' "$STATE" 2>/dev/null || true)"
  tmp="$(mktemp)"
  jq --arg pc "$PC" '
      if .hooks.Stop then .hooks.Stop = (.hooks.Stop | map(select(
          ((.hooks // []) | map(.command? // "") | map(test("goal-guard\\.sh")) | any) | not))) else . end
    | if (.hooks.Stop // []) == [] then del(.hooks.Stop) else . end
    | if $pc == "" then del(.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP)
      else .env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP = $pc end
    | if (.env // {}) == {} then del(.env) else . end
    | if (.hooks // {}) == {} then del(.hooks) else . end' "$SETTINGS" >"$tmp" && mv "$tmp" "$SETTINGS" \
    || { echo "disarm.sh: settings rewrite failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; exit 2; }
  if [ -n "$PC" ]; then
    echo "removed the Stop hook; block cap restored to $PC in $SETTINGS"
  else
    echo "removed the Stop hook and the block-cap override from $SETTINGS"
  fi
fi
echo "the built-in goal, if one is set, is cleared separately with: /goal clear"
