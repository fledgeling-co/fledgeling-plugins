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
# 60s, not 300s. The dwell exists only to skip a session mid-handoff; it is NOT
# what keeps the loop quiet -- the delta comparison and --repeat-after do that.
# Measured: at 300s the probe reported 2 idle while the runtime reported 8, and
# the operator counted 9. A threshold added for noise control was suppressing
# the signal, which is the same mistake as the mtime version one layer along.
IDLE_SEC=${FLAGSHIP_IDLE_SEC:-60}
EXCLUDE_FILE=${FLAGSHIP_IDLE_EXCLUDE:-$HOME/.claude/flagship/idle_exclude}
BERTHS=${FLAGSHIP_BERTHS:-$HOME/Dev/fledgeling-plugins/plugins/harbourmaster/skills/harbourmaster/scripts/berths.py}

names=$(for f in $HOME/.claude/sessions/*.json(N); do
  _EXCL="$(cat $EXCLUDE_FILE 2>/dev/null)" python3 - "$f" "$IDLE_SEC" <<'PY' 2>/dev/null
import json,sys,os,time
d=json.load(open(sys.argv[1])); pid=d.get("pid")
if not pid or os.system(f"kill -0 {pid} 2>/dev/null")!=0: sys.exit()
name=d.get("name") or ""
if not name: sys.exit()
# An exclusion EXPIRES. A session saying "stop counting me" is true when said
# and is a claim with a shelf life, not a permanent property -- exactly the
# failure recorded in the corpus, arriving in the instrument built to track it.
# Measured: a session was excluded on its own word hours earlier, went quiet,
# and stayed invisible until the operator asked about it by name.
#
# Format: "<name>" or "<name>|<unix-expiry>". A bare name is permanent and is
# only for a session its USER scoped out of the fleet; anything a session asked
# for itself gets an expiry.
_now = time.time()
_ex = {}
for _l in os.environ.get("_EXCL","").split("\n"):
    if not _l.strip(): continue
    _n, _, _t = _l.partition("|")
    _ex[_n.strip()] = float(_t) if _t.strip() else None
if name in _ex:
    _exp = _ex[name]
    if _exp is None or _now < _exp: sys.exit()
# `busy` and a missing status are genuinely "not known to be dispatchable" and
# must not be inferred into idle. `shell` is different and excluding it was a
# defect: a session sitting at a shell prompt is not working, and the two
# spawned wave-conductors on this machine live in `shell` between turns -- so
# the loop could never see them, and the operator asked about one directly
# after it had been quiet for seven minutes.
#
# Reported with its state attached rather than folded into idle, because the
# two want different handling: an `idle` session finished a turn and is
# waiting, a `shell` one may be between turns, may have dropped out of Claude,
# and is exactly the shape that goes unnoticed when it is real.
st = d.get("status")
if st not in ("idle", "shell"): sys.exit()
since = d.get("statusUpdatedAt") or d.get("updatedAt")
if since and (time.time() - since/1000.0) < float(sys.argv[2]): sys.exit()
print(name if st == "idle" else name + "(shell)")
PY
done | sort | tr '\n' ' ' | sed 's/ *$//')

avail=$(python3 "$BERTHS" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["available"])' 2>/dev/null)
[ -z "$avail" ] && avail=-1
if   [ "$avail" -lt 0 ] 2>/dev/null; then cap=unknown
elif [ "$avail" -eq 0 ] 2>/dev/null; then cap=none
elif [ "$avail" -le 3 ] 2>/dev/null; then cap=some
else                                       cap=lots
fi
# Capacity is only reported when there is somebody to give it to.
#
# Measured after one hour: 7 polls, 6 wakes -- a ratio better-loop's own rule
# calls out as "a probe too wide, costing what a cron would". The probe was
# deterministic, so it was width: several wakes were CAP moving between buckets
# with IDLE none. Capacity changing when nobody is waiting for it is not a
# dispatch, and waking for it spends the session to learn nothing actionable.
#
# So when nothing is idle, the line is constant and the fleet is silent no
# matter what the board does. The instant someone goes idle, capacity is
# reported with them, which is when it decides anything.
if [ -z "$names" ]; then
  print -r -- "IDLE none"
  print -r -- "CAP n/a"
else
  print -r -- "IDLE $names"
  print -r -- "CAP $cap"
fi
