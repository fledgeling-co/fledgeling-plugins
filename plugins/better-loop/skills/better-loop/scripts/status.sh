#!/usr/bin/env bash
# better-loop status — answer "how's it going" from the state file and the
# ledger, without waking the loop or costing it a turn. Read-only.
#
#   status.sh          every loop in this repo
#   status.sh <slug>   one loop, with more ledger rows
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
WANT="${1:-}"
command -v jq >/dev/null 2>&1 || { echo "jq required"; exit 2; }

shopt -s nullglob 2>/dev/null || true
STATES=( "$ROOT"/.claude/loops/*.json )
[ "${#STATES[@]}" -gt 0 ] || { echo "no loops armed in $ROOT"; exit 0; }

ROWS=12; [ -n "$WANT" ] && ROWS=30

for STATE in "${STATES[@]}"; do
  SLUG="$(jq -r '.slug // "?"' "$STATE")"
  [ -n "$WANT" ] && [ "$SLUG" != "$WANT" ] && continue

  ARMED="$(jq -r '.armed // false' "$STATE")"
  if [ "$ARMED" = "true" ]; then
    # The watcher stamps last_poll_at on every poll. A Monitor dies with its
    # session and cannot say so, which is the one way "WATCHING" lies.
    IV="$(jq -r '.interval // 120' "$STATE")"; case "$IV" in ''|*[!0-9]*) IV=120 ;; esac
    SM="$(jq -r '.last_poll_at // empty' "$STATE")"
    case "$SM" in ''|*[!0-9]*) SM="$(stat -f %m "$STATE" 2>/dev/null || stat -c %Y "$STATE" 2>/dev/null || echo 0)" ;; esac
    HB=$(( $(date +%s) - SM ))
    DL=$(( IV * 3 )); [ "$DL" -lt 120 ] && DL=120
    if [ "$HB" -ge "$DL" ]; then
      echo "loop: $SLUG — SAYS WATCHING, BUT ITS LAST POLL WAS $(( HB / 60 ))m AGO"
      echo "      It polls every ${IV}s, so its Monitor is gone with the session that started it"
      echo "      ($(jq -r '.session_id // "session unknown"' "$STATE")). Restart it or end it with disarm.sh $SLUG."
    else
      echo "loop: $SLUG — WATCHING (last poll ${HB}s ago)"
    fi
  elif [ "$(jq -r '.ended_at // ""' "$STATE")" = "" ]; then
    echo "loop: $SLUG — armed but never started. Make the Monitor call arm.sh printed."
  else
    echo "loop: $SLUG — ended ($(jq -r '.end_reason // "unknown"' "$STATE")) at $(jq -r '.ended_at' "$STATE")"
  fi
  echo "probe: $(jq -r '.probe // "?"' "$STATE")   every $(jq -r '.interval // "?"' "$STATE")s"
  echo "polls: $(jq -r '.polls // 0' "$STATE")   wakes: $(jq -r '.wakes // 0' "$STATE")   detached ticks: $(jq -r '.ticks // 0' "$STATE")   budget: $(jq -r '.max_wakes // "?"' "$STATE")/h"
  echo "brief: $(jq -r '.brief // "—"' "$STATE")"

  # The ratio is the number worth looking at. A loop with as many wakes as polls
  # is a polling loop wearing a watcher's clothes: the probe is not deterministic
  # or is too wide, and each wake is re-billing the whole session prefix.
  P="$(jq -r '.polls // 0' "$STATE")"; W="$(jq -r '.wakes // 0' "$STATE")"
  if [ "$P" -gt 10 ] 2>/dev/null && [ "$W" -gt $((P / 2)) ] 2>/dev/null; then
    echo "  ** $W wakes in $P polls — the probe is changing almost every poll. Narrow it, or the loop costs what a cron would. **"
  fi
  Q="$(jq -r '.quiet_since // ""' "$STATE")"
  [ -n "$Q" ] && [ "$Q" != "null" ] && echo "  ** wake budget spent since $Q — changes are going to the ledger only **"

  LEDGER="$(jq -r '.ledger // ""' "$STATE")"
  [ -n "$LEDGER" ] || LEDGER="docs/loops/loop-${SLUG}.ledger.md"
  case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac
  if [ -f "$LEDGER" ]; then
    LM="$(stat -f %m "$LEDGER" 2>/dev/null || stat -c %Y "$LEDGER" 2>/dev/null || echo 0)"
    echo "ledger: last written $(( ( $(date +%s) - LM ) / 60 ))m ago — $LEDGER"
    echo "events: $(grep '^| ' "$LEDGER" | awk -F'|' 'NR>2{gsub(/ /,"",$4); print $4}' | sort | uniq -c | sort -rn | awk '{printf "%s×%s  ", $1, $2}')"
    grep '^|' "$LEDGER" | tail -n "$ROWS"
  else
    echo "ledger: nothing yet at $LEDGER"
  fi
  echo
done
echo "stop: TaskStop on the monitor, then $(dirname "$0")/disarm.sh <slug>"
