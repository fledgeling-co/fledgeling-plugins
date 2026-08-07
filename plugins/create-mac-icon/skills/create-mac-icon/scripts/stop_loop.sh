#!/bin/bash
# stop_loop.sh — stop the loop WITHOUT orphaning its agent.
#
# Killing loop_runner.py alone leaves its `claude -p` child running, and that
# child keeps editing the fixture's build script. It happened once: a superseded
# agent added ~120 lines mid-round that its replacement had to detect and strip.
set -u
REPO="/Users/lukerhodes/Dev/fledgeling-plugins"
touch "$REPO/docs/LOOP-STOP"
pkill -f "loop_watchdog" 2>/dev/null
PIDFILE="$REPO/docs/.loop-child.pid"
if [ -f "$PIDFILE" ]; then
  CHILD=$(cat "$PIDFILE")
  if kill -0 "$CHILD" 2>/dev/null; then
    echo "killing agent process group $CHILD"
    kill -TERM -"$(ps -o pgid= "$CHILD" | tr -d ' ')" 2>/dev/null
  fi
  rm -f "$PIDFILE"
fi
pkill -f "scripts/loop_runner.py" 2>/dev/null
sleep 1
echo "stopped. remove $REPO/docs/LOOP-STOP before restarting."
