#!/bin/zsh
# Set or clear a named hold. A session with an armed hold is waiting on its own
# watcher or a named release, not on a dispatch, so the idle probe reports it
# as "(held)" once on entry rather than as idle on every poll.
#
# Holds EXPIRE after 4 hours inside the probe, because a hold is a status claim
# and a status claim has a shelf life. Clearing on release is the caller's job:
#   set_hold.sh <name>          arm
#   set_hold.sh <name> --clear  release
set -u
mkdir -p "$HOME/.claude/flagship/holds"
name="${1:?usage: set_hold.sh <name> [--clear]}"
dir="$HOME/.claude/flagship/holds"
case "${2:-}" in
  --clear) rm -f "$dir/$name.hold"; print -r -- "cleared: $name" ;;
  *)       printf '%s\n' "$name" > "$dir/$name.hold"; print -r -- "held: $name" ;;
esac
