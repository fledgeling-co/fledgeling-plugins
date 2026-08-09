#!/usr/bin/env bash
# goal-harness status — answer "is it still going / has the goal been met?"
# from the ledger rather than from the transcript. Read-only.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE="$ROOT/.claude/goal-state.json"
[ -f "$STATE" ] || { echo "no goal armed in $ROOT"; exit 0; }
command -v jq >/dev/null 2>&1 || { echo "jq required"; exit 2; }

ARMED="$(jq -r '.armed'  "$STATE")"; SLUG="$(jq -r '.slug' "$STATE")"
ITER="$(jq -r '.iteration // 0' "$STATE")"; MAX="$(jq -r '.max_iterations // 0' "$STATE")"
LEDGER="$(jq -r '.ledger // ""' "$STATE")"; case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER";; esac

if [ "$ARMED" = "true" ]; then
  echo "goal: $SLUG — ARMED"
else
  echo "goal: $SLUG — ended ($(jq -r '.end_reason // "unknown"' "$STATE")) at $(jq -r '.ended_at // "?"' "$STATE")"
fi
echo "turn: $ITER${MAX:+/$MAX}   started: $(jq -r '.started_at // "?"' "$STATE")   deadline: $(jq -r '.deadline // "none"' "$STATE")"
echo "brief: $(jq -r '.goal_file // "?"' "$STATE")"
echo "gates: $(jq -r '[.verify[]?.name] | join(", ")' "$STATE")"
echo
if [ -f "$LEDGER" ]; then
  echo "last 10 turns ($LEDGER):"; grep '^|' "$LEDGER" | tail -n 10
else
  echo "no ledger yet at $LEDGER — the guard has not run a turn"
fi
