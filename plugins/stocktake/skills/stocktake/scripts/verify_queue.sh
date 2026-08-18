#!/usr/bin/env bash
# Serial out-of-family verification queue.
#
# Some lanes REFUSE concurrent instances: launching three at once has been
# observed to leave one alive and kill the others with empty logs and exit
# codes that look fine. So this waits for any in-flight run before starting the
# next, and reports a verdict or an explicit no-verdict per card.
#
# One judge per card, not a panel — a panel of nine frontier judges across seven
# families buys about two independent votes (references/evidence.md).
#
#   verify_queue.sh --lane-cmd 'grok -m X --effort high -p {PROMPT}' \
#                   --packet-dir /tmp/packets --out-dir /tmp/verdicts \
#                   --match 'grok -m X' KEY1 KEY2 ...
#
# {PROMPT} is replaced with the packet's contents. --match is the pgrep pattern
# used to detect an in-flight instance of the lane.
set -uo pipefail

LANE_CMD=""; PACKET_DIR=""; OUT_DIR=""; MATCH=""; TIMEOUT=2400
while [ $# -gt 0 ]; do
  case "$1" in
    --lane-cmd)    LANE_CMD="$2"; shift 2 ;;
    --packet-dir)  PACKET_DIR="$2"; shift 2 ;;
    --out-dir)     OUT_DIR="$2"; shift 2 ;;
    --match)       MATCH="$2"; shift 2 ;;
    --timeout)     TIMEOUT="$2"; shift 2 ;;
    *) break ;;
  esac
done
: "${LANE_CMD:?--lane-cmd is required}"
: "${PACKET_DIR:?--packet-dir is required}"
: "${OUT_DIR:?--out-dir is required}"
: "${MATCH:?--match is required (the pgrep pattern for an in-flight lane)}"
[ $# -gt 0 ] || { echo "no card keys given"; exit 2; }

mkdir -p "$OUT_DIR"

for KEY in "$@"; do
  PACKET="$PACKET_DIR/pkt-$KEY.txt"
  OUT="$OUT_DIR/v-$KEY.md"
  if [ ! -s "$PACKET" ]; then
    echo "NO-PACKET $KEY — $PACKET is missing or empty"
    continue
  fi
  # A packet much over ~50KB has been observed to run for half an hour without
  # reaching a verdict. Send the requirement list plus changed files, not a diff.
  SIZE=$(wc -c < "$PACKET" | tr -d ' ')
  [ "$SIZE" -gt 51200 ] && echo "WARN $KEY packet is ${SIZE}B — over the ~50KB ceiling"

  while pgrep -f "$MATCH" >/dev/null 2>&1; do sleep 15; done

  echo "START $KEY $(date +%H:%M:%S) (${SIZE}B)"
  PROMPT="$(cat "$PACKET")"
  # shellcheck disable=SC2086
  perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" \
    ${LANE_CMD//\{PROMPT\}/"$PROMPT"} > "$OUT" 2>"$OUT.log"

  if [ ! -s "$OUT" ]; then
    # An empty output file with a clean exit is a LANE FAILURE, not a pass.
    echo "NO-VERDICT $KEY — empty output; treat the lane as down and substitute a family"
  elif grep -q "VERDICT:" "$OUT"; then
    echo "DONE $KEY $(grep -m1 'VERDICT:' "$OUT") $(wc -c < "$OUT" | tr -d ' ')B"
  else
    echo "NO-VERDICT $KEY — output present but no VERDICT line ($(wc -c < "$OUT" | tr -d ' ')B)"
  fi
done
echo "QUEUE COMPLETE"
