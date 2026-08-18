#!/bin/bash
# loop_watchdog.sh — keeps the icon fidelity loop running without a session attached.
#
#   LOOP_REPO=/path/to/workspace nohup bash loop_watchdog.sh > /dev/null 2>&1 &
#   bash loop_watchdog.sh /path/to/workspace            # same, in the foreground
#   touch "$LOOP_REPO/docs/LOOP-STOP"   # stops the runner AND this watchdog
#
# Checks every 60s. If the runner is gone it decides whether that was a clean
# finish (queue exhausted, budget spent, stop file) or a crash, and restarts only
# crashes, with a cap so a permanently broken round cannot thrash forever.
# Every decision is logged with a timestamp so the record survives the session.
set -u

# The runner is a sibling of this script, so derive it rather than assert a path:
# once the plugin is installed anywhere else, a hardcoded /Users/... path finds
# nothing, `pgrep` matches nothing, and the restart branch fires on a setup error.
# Resolve symlinks so invocation through a link or a relative path still works.
SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  _link=$(readlink "$SELF")
  case "$_link" in
    /*) SELF="$_link" ;;
    *)  SELF="$(dirname "$SELF")/$_link" ;;
  esac
done
SCRIPTS="$(cd "$(dirname "$SELF")" && pwd -P)"
SELF="$SCRIPTS/$(basename "$SELF")"   # absolute, so the usage lines below paste anywhere
RUNNER="$SCRIPTS/loop_runner.py"

# REPO is the workspace whose docs/ holds the loop's state (config, log, queue,
# stop file). That is a property of the workspace, not of the plugin, so it is not
# derivable from SCRIPTS — take it explicitly and refuse rather than guess.
REPO="${1:-${LOOP_REPO:-}}"
if [ -z "$REPO" ]; then
  echo "loop_watchdog.sh: no workspace given, so there is no docs/ to supervise." >&2
  echo "  LOOP_REPO=/path/to/workspace nohup bash $SELF > /dev/null 2>&1 &" >&2
  echo "  (run from the workspace root, LOOP_REPO=\$PWD is usually right)" >&2
  exit 2
fi
REPO="${REPO%/}"
CONFIG="${LOOP_CONFIG:-$REPO/docs/loop.config.json}"
LOG="$REPO/docs/loop.log"
WLOG="$REPO/docs/loop-watchdog.log"
QUEUE="$REPO/docs/loop-review-queue.md"
MAX_RESTARTS=8
restarts=0

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$WLOG"; }

# A missing config is a setup error, and the restart branch cannot fix one: the
# runner would exit instantly, eight times, and the eighth would file a review-queue
# entry blaming the rounds. Refuse here, naming the path, and spend no restarts.
if [ ! -f "$CONFIG" ]; then
  echo "loop_watchdog.sh: config not found: $CONFIG" >&2
  echo "  set LOOP_CONFIG, or put the config at \$LOOP_REPO/docs/loop.config.json" >&2
  [ -d "$(dirname "$WLOG")" ] && log "refusing to start: config not found: $CONFIG"
  exit 2
fi
if [ ! -f "$RUNNER" ]; then
  echo "loop_watchdog.sh: runner not found beside this script: $RUNNER" >&2
  exit 2
fi

log "watchdog started (pid $$), max $MAX_RESTARTS restarts, repo $REPO, config $CONFIG"
while true; do
  if [ -f "$REPO/docs/LOOP-STOP" ]; then
    log "stop file present; watchdog exiting"; exit 0
  fi

  # The narrow pattern is load-bearing, and so is dropping our own pid.
  # references/fidelity-loop.md: a bare `loop_runner.py` matches any command string
  # that merely mentions it — a tail, a grep, this watchdog's own nohup line — and
  # here that inverts the failure: a stray match reads as a live runner and
  # suppresses every restart. stop_loop.sh already uses this form.
  if pgrep -f "scripts/loop_runner.py" 2>/dev/null | grep -qvx "$$"; then
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
