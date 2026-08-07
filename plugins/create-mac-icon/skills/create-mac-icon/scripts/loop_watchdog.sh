#!/bin/bash
# loop_watchdog.sh — keeps the icon fidelity loop running without a session attached.
#
#   nohup bash loop_watchdog.sh > /dev/null 2>&1 &
#   touch docs/LOOP-STOP     # stops the runner AND this watchdog
#
# Checks every 60s. If the runner is gone it decides whether that was a clean
# finish (queue exhausted, budget spent, stop file) or a crash, and restarts only
# crashes, with a cap so a permanently broken round cannot thrash forever.
# Every decision is logged with a timestamp so the record survives the session.
set -u
REPO="/Users/lukerhodes/Dev/fledgeling-plugins"
RUNNER="$REPO/plugins/create-mac-icon/skills/create-mac-icon/scripts/loop_runner.py"
CONFIG="$REPO/docs/loop.config.json"
LOG="$REPO/docs/loop.log"
WLOG="$REPO/docs/loop-watchdog.log"
QUEUE="$REPO/docs/loop-review-queue.md"
MAX_RESTARTS=8
restarts=0

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$WLOG"; }

log "watchdog started (pid $$), max $MAX_RESTARTS restarts"
while true; do
  if [ -f "$REPO/docs/LOOP-STOP" ]; then
    log "stop file present; watchdog exiting"; exit 0
  fi

  if pgrep -f "loop_runner.py" > /dev/null; then
    sleep 60; continue
  fi

  last=$(tail -3 "$LOG" 2>/dev/null | tr '\n' ' ')
  case "$last" in
    *"queue exhausted"*|*"cost cap"*|*"stop file present"*|*"three consecutive errors"*)
      log "runner finished cleanly, not restarting. Tail: $last"; exit 0 ;;
  esac

  if [ "$restarts" -ge "$MAX_RESTARTS" ]; then
    log "runner has died $restarts times; giving up rather than thrashing. Tail: $last"
    {
      echo ""
      echo "## Watchdog gave up after $restarts restarts"
      echo ""
      echo "The runner kept dying. Last log lines:"
      echo ""
      echo "    $last"
      echo ""
      echo "Fix the cause, then restart with the command in loop_watchdog.sh's header."
    } >> "$QUEUE"
    exit 1
  fi

  restarts=$((restarts + 1))
  log "runner is down (restart $restarts/$MAX_RESTARTS). Tail: $last"
  cd "$REPO" || exit 1
  nohup python3 "$RUNNER" --config "$CONFIG" >> "$LOG" 2>&1 &
  log "restarted runner as pid $!"
  sleep 45   # let it get past its own startup before the next health check
done
