#!/usr/bin/env bash
# loop-harness tick ledger — one row per tick. Called from the tick protocol.
#   tick.sh <slug> <verdict> [note]
# Verdict is free text; use a small stable set (armed|green|fixed|blocked|noop|stopped)
# so status.sh can summarise it.
set -uo pipefail
SLUG="${1:-loop}"; VERDICT="${2:-tick}"; NOTE="${3:-}"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LEDGER="$ROOT/docs/loops/loop-${SLUG}.ledger.md"
mkdir -p "$(dirname "$LEDGER")"
if [ ! -f "$LEDGER" ]; then
  { echo "# Loop ledger — $SLUG"; echo; echo "| tick | at | verdict | note |"; echo "|---|---|---|---|"; } >"$LEDGER"
fi
N="$(grep -c '^| [0-9]' "$LEDGER" 2>/dev/null | tr -d ' \n')"; N="${N:-0}"
printf '| %s | %s | %s | %s |\n' "$((N + 1))" "$(date '+%Y-%m-%d %H:%M')" "$VERDICT" "$NOTE" >>"$LEDGER"
echo "tick $((N + 1)) recorded: $VERDICT ${NOTE:+— $NOTE}"
