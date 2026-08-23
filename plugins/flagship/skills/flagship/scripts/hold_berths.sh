#!/bin/zsh
# Exit the moment N berths are free, so a held release is a mechanism rather
# than a memory.
#
# Three states, because an exited watcher is otherwise ambiguous between
# never-armed and already-fired -- measured tonight when a pgrep found nothing
# and it was read as "not armed" while it had in fact just succeeded:
#   live process  -> ARMED
#   output file written -> FIRED (read it for the board)
#   neither       -> NEVER STARTED
# The first line is written immediately so "armed" is observable from the file
# too, not only from the process table.
set -u
WANT="${1:?usage: hold_berths.sh <n> <who>}"
WHO="${2:?usage: hold_berths.sh <n> <who>}"
B=/Users/lukerhodes/Dev/fledgeling-plugins/plugins/harbourmaster/skills/harbourmaster/scripts/berths.py
print -r -- "ARMED for ${WHO} at >= ${WANT} berths (pid $$)"
# ONE read: test the condition and report from the SAME snapshot.
#
# The first version tested `available` in the loop and then re-read the board to
# report it. Measured: it fired on >= 2 and reported `available 1`, because a
# berth was taken in the gap. Both reads were honest and the message contradicted
# its own trigger -- the release-figure expiry problem, inside the instrument
# built to solve it. A condition and the evidence for it have to come from one
# observation.
snap=""
while :; do
  snap=$(python3 "$B" 2>/dev/null)
  a=$(print -r -- "$snap" | python3 -c 'import json,sys;print(json.load(sys.stdin)["available"])' 2>/dev/null)
  [ -n "$a" ] && [ "$a" -ge "$WANT" ] 2>/dev/null && break
  sleep 20
done
print -r -- "$snap" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f\"FIRED for ${WHO}: available {d['available']} ceiling {d['ceiling']} in_use {d['in_use']}/{d['capacity']} at {d['sampled_at']} | {d['load_per_core']}/core\")
print('  (this board IS the one the condition fired on, not a later re-read)')
for c in d.get('claims',[]): print(f\"  holding: {c['slots']} {c['project']}/{c['label']}\")
"
