#!/usr/bin/env bash
# Block up to <seconds> for one worker to finish. Prints its status line.
#   tools/wait-worker.sh <youtube-id> <seconds>
set -uo pipefail
ID="$1"; LIMIT="${2:-540}"
DIR="$HOME/Movies/motion-craft-corpus/$ID"
end=$(( $(date +%s) + LIMIT ))
while :; do
  st="$(cat "$DIR/worker.status" 2>/dev/null)"
  case "$st" in
    *'"state": "done"'*|*'"state":"done"'*|*'"state": "failed"'*|*'"state":"failed"'*) echo "$st"; exit 0 ;;
  esac
  if [ -s "$DIR/worker.pid" ] && ! kill -0 "$(cat "$DIR/worker.pid")" 2>/dev/null; then
    printf '{"id":"%s","state":"failed","note":"worker process died without writing a final status"}\n' "$ID" | tee "$DIR/worker.status"
    rm -f "$DIR/worker.pid"; exit 0
  fi
  [ "$(date +%s)" -ge "$end" ] && { printf '{"id":"%s","state":"running"}\n' "$ID"; exit 0; }
  sleep 15
done
