#!/bin/bash
# stop_loop.sh — stop the loop WITHOUT orphaning its agent.
#
#   LOOP_REPO=/path/to/workspace bash stop_loop.sh
#   bash stop_loop.sh /path/to/workspace          # same thing
#
# Killing loop_runner.py alone leaves its `claude -p` child running, and that
# child keeps editing the fixture's build script. It happened once: a superseded
# agent added ~120 lines mid-round that its replacement had to detect and strip.
set -u
# The workspace holding docs/ is a property of the workspace, not of this plugin,
# so it cannot be derived from the script's own location once the plugin is
# installed elsewhere. Refuse rather than guess: stopping the wrong tree would
# touch a LOOP-STOP nobody reads and leave the real agent running.
REPO="${1:-${LOOP_REPO:-}}"
if [ -z "$REPO" ]; then
  echo "stop_loop.sh: no workspace given, so there is no docs/ to stop." >&2
  echo "  LOOP_REPO=/path/to/workspace bash $0" >&2
  echo "  (run from the workspace root, LOOP_REPO=\$PWD is usually right)" >&2
  exit 2
fi
REPO="${REPO%/}"
if [ ! -d "$REPO/docs" ]; then
  echo "stop_loop.sh: no docs/ under $REPO — is that the right workspace?" >&2
  exit 2
fi
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
