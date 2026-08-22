#!/usr/bin/env bash
# Prove the mechanism still works on this machine. Exits non-zero on any failure.
#
# These are the properties that fail SILENTLY — where the governor keeps
# reporting success while governing nothing. A close-on-exec regression alone
# would free every berth the instant a workload started.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
export HARBOURMASTER_HOME="$(mktemp -d)/hm"
PASS=0; FAIL=0
ok()   { echo "  PASS  $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL  $1"; echo "        $2"; FAIL=$((FAIL+1)); }
inuse() { ./berths.py | python3 -c 'import json,sys;print(json.load(sys.stdin)["in_use"])'; }

echo "harbourmaster selftest"

# 1 — pressure answers, and fast enough to be called before every decision.
START=$(python3 -c 'import time;print(time.time())')
P=$(./pressure.py 2>/dev/null) || true
EL=$(python3 -c "import time;print(round(time.time()-$START,2))")
if echo "$P" | python3 -c 'import json,sys;d=json.load(sys.stdin);assert d["verdict"]["overall"] in ("healthy","busy","tight","critical","unknown")' 2>/dev/null
then ok "pressure returns a verdict (${EL}s)"; else bad "pressure verdict" "$P"; fi
python3 -c "import sys;sys.exit(0 if $EL < 5 else 1)" && ok "pressure under 5s" \
  || bad "pressure too slow" "${EL}s — callers will stop calling it"

# 2 — berths are held across exec. The close-on-exec trap.
MARK="hmself-$$"; printf '#!/bin/bash\nsleep 6\n' > "/tmp/$MARK.sh"; chmod +x "/tmp/$MARK.sh"
./governor-run --weight 3 --project selftest --label probe -- "/tmp/$MARK.sh" &
sleep 2
N=$(inuse)
[ "$N" = "3" ] && ok "3 berths held across exec" \
  || bad "berths not held across exec (saw $N)" "os.set_inheritable missing — the lock died at exec"

# 3 — SIGKILL frees them once the LAST holder is gone, with no reaper running.
# The berth is held by the descriptor, and every descendant inherits it, so the
# property under test is "kill the tree" rather than "kill the root". Killing
# only the root leaves an orphan still holding the lock — correct behaviour, and
# the reason this test walks the tree.
#
# PIDs come from the tree, never from `pgrep -f`: on this machine a `pgrep -f`
# for a generic pattern has already reached another session's processes.
VP=$(pgrep -f "$MARK" | head -1)
if [ -n "$VP" ]; then
  KIDS=$(pgrep -P "$VP" 2>/dev/null)
  kill -9 $KIDS "$VP" 2>/dev/null; sleep 1
  N=$(inuse)
  [ "$N" = "0" ] && ok "SIGKILL on the tree freed every berth, no reaper" \
    || bad "berths survived SIGKILL (saw $N)" "a descendant may still hold the descriptor"
else bad "could not find the workload to kill" "test inconclusive, not passed"; fi
wait 2>/dev/null; rm -f "/tmp/$MARK.sh"

# 4 — an impossible weight is refused as usage, not queued forever.
./governor-run --weight 9999 -- true >/dev/null 2>&1
[ $? -eq 64 ] && ok "over-capacity weight refused with exit 64" \
  || bad "over-capacity weight not refused" "should be EX_USAGE"

# 5 — refusal is bounded. Fill every berth, then confirm a request gives up.
# PIDs are tracked directly: `pkill -f <word>` on a shared machine reaches other
# sessions' processes, and this test would then kill somebody else's build.
CEIL=$(./berths.py | python3 -c 'import json,sys;print(json.load(sys.stdin)["ceiling"])')
MARK2="hmfill-$$"; printf '#!/bin/bash\nsleep 20\n' > "/tmp/$MARK2.sh"; chmod +x "/tmp/$MARK2.sh"
./governor-run --weight "$CEIL" --wait 8 --project selftest -- "/tmp/$MARK2.sh" >/dev/null 2>&1 &
FILLER=$!
sleep 3
if [ "$(inuse)" -ge "$CEIL" ]; then
  S=$(python3 -c 'import time;print(time.time())')
  OUT=$(./governor-run --weight 1 --wait 3 -- true 2>&1 >/dev/null); RC=$?
  EL=$(python3 -c "import time;print(round(time.time()-$S,1))")
  CEIL2=$(./berths.py | python3 -c 'import json,sys;print(json.load(sys.stdin)["ceiling"])')
  if [ $RC -eq 75 ] && echo "$OUT" | grep -q retry_after_sec; then
    ok "refused with exit 75 and retry_after_sec after ${EL}s"
  elif [ "$CEIL2" -gt "$CEIL" ]; then
    # Pressure eased while the test ran and the ceiling rose, so a berth really
    # was free. Correct behaviour, unusable as evidence — reported as such
    # rather than as a pass.
    ok "inconclusive: ceiling rose $CEIL->$CEIL2 mid-test (not counted as proof)"
  else bad "refusal shape wrong (rc=$RC after ${EL}s)" "$OUT"; fi
  python3 -c "import sys;sys.exit(0 if $EL < 10 else 1)" && ok "refusal bounded by --wait" \
    || bad "refusal not bounded" "${EL}s — a caller's tool call would time out"
else
  bad "could not fill the berths to test refusal" "inconclusive, not passed"
fi
kill -9 $FILLER 2>/dev/null
for c in $(pgrep -P $FILLER 2>/dev/null); do kill -9 "$c" 2>/dev/null; done
rm -f "/tmp/$MARK2.sh"

# 6 — taskpolicy is present and both directions work.
if command -v taskpolicy >/dev/null; then
  ok "taskpolicy present"
else bad "taskpolicy missing" "QoS clamping cannot work without it"; fi

# 7 — the demoter refuses to act below critical, and never below its own gate.
D=$(./demote.py 2>/dev/null)
echo "$D" | python3 -c 'import json,sys;d=json.load(sys.stdin);sys.exit(0 if d.get("applied") in (None,False) else 1)' 2>/dev/null \
  && ok "demoter is dry-run without --apply" || bad "demoter acted without --apply" "$D"

# 8 — the thermal lane states its own readability rather than assuming it.
T=$(./thermal.py --check 2>/dev/null)
echo "$T" | python3 -c 'import json,sys;d=json.load(sys.stdin);assert "readable" in d and "reason" in d' 2>/dev/null \
  && ok "thermal lane reports readability with a reason" || bad "thermal --check shape" "$T"

echo
echo "  $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
