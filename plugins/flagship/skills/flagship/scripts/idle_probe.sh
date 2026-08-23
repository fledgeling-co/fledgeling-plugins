#!/bin/zsh
# Which sessions are dispatchable, and whether heavy work can be admitted.
#
# READS `status` FROM THE SESSION FILE, NOT TRANSCRIPT MTIME.
#
# The first version of this probe used mtime on the transcript, which answers
# "did this session write recently" -- and that was read as "does this session
# have work". A session that answers the conductor and then stops is maximally
# fresh by mtime and idle in fact, so the probe reported ONE idle session while
# the runtime reported EIGHT. The operator saw it before the instrument did,
# which is the failure this loop exists to prevent, reproduced inside it.
#
# `status` is what the runtime itself publishes: idle | busy | shell, with
# `statusUpdatedAt` beside it. A session with no status yet is UNKNOWN and is
# never counted as idle -- absence is not evidence.
#
# Prints names, never durations: durations move every poll and would make every
# poll a change, turning a change-driven watcher back into a polling loop.
IDLE_SEC=${FLAGSHIP_IDLE_SEC:-300}
EXCLUDE_FILE=${FLAGSHIP_IDLE_EXCLUDE:-$HOME/.claude/flagship/idle_exclude}
BERTHS=${FLAGSHIP_BERTHS:-$HOME/Dev/fledgeling-plugins/plugins/harbourmaster/skills/harbourmaster/scripts/berths.py}

names=$(for f in $HOME/.claude/sessions/*.json(N); do
  _EXCL="$(cat $EXCLUDE_FILE 2>/dev/null)" python3 - "$f" "$IDLE_SEC" <<'PY' 2>/dev/null
import json,sys,os,time
d=json.load(open(sys.argv[1])); pid=d.get("pid")
if not pid or os.system(f"kill -0 {pid} 2>/dev/null")!=0: sys.exit()
name=d.get("name") or ""
if not name: sys.exit()
if name in [l for l in os.environ.get("_EXCL","").split("\n") if l]: sys.exit()
# Only an explicit idle counts. `shell`, `busy`, and a missing status are all
# "not known to be dispatchable" and must not be inferred into idle.
if d.get("status") != "idle": sys.exit()
since = d.get("statusUpdatedAt") or d.get("updatedAt")
if since and (time.time() - since/1000.0) < float(sys.argv[2]): sys.exit()
print(name)
PY
done | sort | tr '\n' ' ' | sed 's/ *$//')

avail=$(python3 "$BERTHS" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["available"])' 2>/dev/null)
[ -z "$avail" ] && avail=-1
if   [ "$avail" -lt 0 ] 2>/dev/null; then cap=unknown
elif [ "$avail" -eq 0 ] 2>/dev/null; then cap=none
elif [ "$avail" -le 3 ] 2>/dev/null; then cap=some
else                                       cap=lots
fi
[ -z "$names" ] && names=none
print -r -- "IDLE $names"
print -r -- "CAP $cap"
