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
until
  a=$(python3 "$B" 2>/dev/null | python3 -c 'import json,sys;print(json.load(sys.stdin)["available"])' 2>/dev/null)
  [ -n "$a" ] && [ "$a" -ge "$WANT" ] 2>/dev/null
do sleep 20; done
python3 "$B" 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f\"FIRED for ${WHO}: available {d['available']} ceiling {d['ceiling']} in_use {d['in_use']}/{d['capacity']} at {d['sampled_at']} | {d['load_per_core']}/core\")
for c in d.get('claims',[]): print(f\"  holding: {c['slots']} {c['project']}/{c['label']}\")
"
