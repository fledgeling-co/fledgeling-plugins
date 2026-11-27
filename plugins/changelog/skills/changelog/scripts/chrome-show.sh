#!/bin/bash
# Show a local HTML file in the running Google Chrome: reload the tab that already has it
# open, or open it in a new tab when none does. Never launches a second Chrome instance.
# Usage: chrome-show.sh <path-to-file.html>
# Prints "reloaded window N tab M" or "opened". Exits 1 when Chrome is not running.
set -euo pipefail

if [ $# -ne 1 ] || [ ! -f "$1" ]; then
  echo "usage: chrome-show.sh <existing-file.html>" >&2
  exit 2
fi

if ! pgrep -xq "Google Chrome"; then
  echo "Google Chrome is not running; not launching it" >&2
  exit 1
fi

# Tab URLs carry the resolved, percent-encoded path: ~/DevEx shows as /Volumes/LLMs/Dev/...
url=$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve().as_uri())' "$1")

result=$(osascript - "$url" <<'EOF'
on run argv
  set target to item 1 of argv
  tell application "Google Chrome"
    set wi to 0
    repeat with w in windows
      set wi to wi + 1
      set ti to 0
      repeat with t in tabs of w
        set ti to ti + 1
        if (URL of t) starts with target then
          tell t to reload
          set active tab index of w to ti
          set index of w to 1
          activate
          return "reloaded window " & wi & " tab " & ti
        end if
      end repeat
    end repeat
  end tell
  return "missing"
end run
EOF
)

if [ "$result" = "missing" ]; then
  open -a "Google Chrome" "$1"
  echo "opened"
else
  echo "$result"
fi
