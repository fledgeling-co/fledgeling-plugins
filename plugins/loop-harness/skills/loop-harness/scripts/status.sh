#!/usr/bin/env bash
# loop-harness status — answer "how's it going" from the ledger, without
# interrupting the run. Read-only.
#   status.sh [slug]        omit the slug to list every loop in this repo
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLUG="${1:-}"

if [ -z "$SLUG" ]; then
  shopt -s nullglob
  FOUND=( "$ROOT"/docs/loops/loop-*.ledger.md )
  if [ ${#FOUND[@]} -eq 0 ]; then echo "no loop ledgers in $ROOT/docs/loops"; else
    echo "loops in $ROOT:"
    for f in "${FOUND[@]}"; do
      b="$(basename "$f")"; s="${b#loop-}"; s="${s%.ledger.md}"
      printf '  %-24s %s ticks, last: %s\n' "$s" \
        "$(grep -c '^| [0-9]' "$f" | tr -d ' \n')" \
        "$(grep '^| [0-9]' "$f" | tail -1 | awk -F'|' '{print $3" "$4}' | sed 's/^ *//')"
    done
  fi
  echo
fi

BRIEF="$ROOT/docs/loops/loop-${SLUG}.md"
LEDGER="$ROOT/docs/loops/loop-${SLUG}.ledger.md"
[ -n "$SLUG" ] || exit 0
[ -f "$LEDGER" ] || { echo "no ledger for '$SLUG' at $LEDGER"; exit 0; }

if [ -f "$BRIEF" ]; then
  grep -E '^\- \*\*(mechanism|armed|expires|job id|wake signal)' "$BRIEF" | sed 's/^- //'
  EXP="$(sed -n 's/^- \*\*expires:\*\* *//p' "$BRIEF" | head -1)"
  if [ -n "$EXP" ]; then
    E="$(date -j -f "%Y-%m-%d" "$EXP" +%s 2>/dev/null || date -d "$EXP" +%s 2>/dev/null || true)"
    [ -n "$E" ] && [ "$(date +%s)" -ge "$((E - 86400))" ] && echo "  ** expires within 24h — re-arm or let it end **"
  fi
  echo
fi
echo "ticks: $(grep -c '^| [0-9]' "$LEDGER" | tr -d ' \n')"
echo "verdicts: $(grep '^| [0-9]' "$LEDGER" | awk -F'|' '{gsub(/ /,"",$4); print $4}' | sort | uniq -c | sort -rn | awk '{printf "%s×%s  ", $1, $2}')"
echo
echo "last 10 ticks:"; grep '^|' "$LEDGER" | tail -n 10
echo
echo "stop: Esc while it waits · CronDelete <job id> · $(dirname "$0")/disarm.sh $SLUG"
