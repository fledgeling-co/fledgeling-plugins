#!/usr/bin/env bash
# better-loop tick ledger — one row per tick. Called from the tick protocol, and
# sharing its table shape with watch.sh so both write one readable ledger.
#   tick.sh <slug> <verdict> [note]
# Verdict is free text; use a small stable set (green|fixed|blocked|noop|stopped)
# so status.sh can summarise it.
set -uo pipefail
SLUG="${1:-loop}"; VERDICT="${2:-tick}"; NOTE="${3:-}"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LEDGER="$ROOT/docs/loops/loop-${SLUG}.ledger.md"
mkdir -p "$(dirname "$LEDGER")" || { echo "tick.sh: cannot create $(dirname "$LEDGER")" >&2; exit 1; }
if [ ! -f "$LEDGER" ]; then
  { echo "# Loop ledger — $SLUG"; echo; echo "| tick | at | verdict | note |"; echo "|---|---|---|---|"; } >"$LEDGER" \
    || { echo "tick.sh: cannot write $LEDGER" >&2; exit 1; }
fi
N="$(grep -c '^| [0-9]' "$LEDGER" 2>/dev/null | tr -d ' \n')"; N="${N:-0}"
printf '| %s | %s | %s | %s |\n' "$((N + 1))" "$(date '+%Y-%m-%d %H:%M')" "$VERDICT" "$NOTE" >>"$LEDGER" \
  || { echo "tick.sh: could not append to $LEDGER" >&2; exit 1; }
echo "tick $((N + 1)) recorded: $VERDICT ${NOTE:+— $NOTE}"
