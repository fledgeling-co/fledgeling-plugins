#!/usr/bin/env bash
# better-goal stall watcher — the out-of-band half of the harness.
#
#   Monitor({ command: "watch.sh <slug> [--stale 25] [--interval 60]",
#             description: "goal <slug> liveness", persistent: true })
#
# The Stop guard only fires at the END of a turn, so a run that dies mid-turn —
# usage limit, crashed delivery agent, lost session, workflow whose agents all
# failed — never reaches it. This watches from outside.
#
# It emits a line ONLY on a transition. A healthy run produces no output at all,
# which matters because every line here becomes a task-notification that wakes
# the session and re-bills its whole prefix. Silence is the design, not a gap:
# the ledger and status.sh are where "how's it going" is answered.
#
# Transitions emitted:
#   NOTLIVE   armed, but the guard has never fired for this run. Re-emitted on
#             a doubling backoff (15m, 30m, 1h, 2h, 4h…) while it stays so,
#             because the run is not verified and one notice was read once and
#             then worked around.
#   FOREIGN   something other than the guard is appending to the ledger. Said
#             once. A ledger row from a loop is not verification and cannot
#             block a turn; the run that built one sat idle twelve hours behind
#             a ledger that moved every ten minutes.
#   STALL     the guard has run at least once, has not run for --stale minutes,
#             and the owning session's transcript is cold
#             (re-emitted on exponential backoff, never on every poll)
#   RESUMED   the guard ran again after a STALL
#   DONE      disarmed with end_reason=met
#   ENDED     disarmed for any other reason (stuck, api_error, session_ended,
#             deadline, max_iterations)
#   GONE      the state file disappeared
#
# Liveness is read from two things and never from the ledger's mtime: the
# guard's own `last_guard_at` stamp in the state file, and the session
# transcript, which is appended to while a turn runs (measured 6 seconds old
# mid-turn). Of 56 STALLs delivered across 14 real runs, 34 arrived within ten
# minutes of an assistant message; the transcript check turns those into
# silence. A turn that runs longer than --stale is the normal case here.

set -uo pipefail

SLUG="${1:-}"; shift 2>/dev/null || true
STALE_MIN=0        # 0 = adapt to the run's own cadence; a number pins it
STALE_FLOOR=25     # never call a run stalled sooner than this
ALIVE_MIN=10       # a transcript written this recently means the session is working
INTERVAL=60
while [ $# -gt 0 ]; do
  case "$1" in
    --stale)       STALE_MIN="${2:-0}";    shift 2 ;;
    --stale-floor) STALE_FLOOR="${2:-25}"; shift 2 ;;
    --alive)       ALIVE_MIN="${2:-10}";   shift 2 ;;
    --interval)    INTERVAL="${2:-60}";    shift 2 ;;
    *) shift ;;
  esac
done
[ -n "$SLUG" ] || { echo "watch.sh: usage: watch.sh <slug> [--stale MIN] [--interval SEC]" >&2; exit 2; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE="$ROOT/.claude/goals/${SLUG}.json"
[ -f "$STATE" ] || STATE="$ROOT/.claude/goal-state.json"

mtime_of() { [ -f "$1" ] && { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; } || echo 0; }
epoch_of() {
  local raw="$1" s
  [ -n "$raw" ] || { echo 0; return; }
  s="${raw%Z}"; s="${s/T/ }"
  date -u -j -f "%Y-%m-%d %H:%M:%S" "$s" +%s 2>/dev/null || date -u -d "$raw" +%s 2>/dev/null || echo 0
}

CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
transcript_mtime() {  # session_id -> newest mtime, or 0
  local sid="$1" newest=0 m
  [ -n "$sid" ] || { echo 0; return; }
  shopt -s nullglob 2>/dev/null || true
  for f in "$CFG"/projects/*/"$sid".jsonl; do
    m="$(mtime_of "$f")"; [ "$m" -gt "$newest" ] && newest="$m"
  done
  echo "$newest"
}

# A pinned --stale is honoured. Otherwise the threshold comes from the run's own
# turn length: three times the MEDIAN of its last ten gaps, floored and capped.
adaptive_stale_min() {  # ledger -> minutes
  local led="$1" prev=0 t v gap gaps="" n mid m
  [ -f "$led" ] || { echo "$STALE_FLOOR"; return; }
  while read -r t; do
    v=$(( 10#${t:0:2} * 3600 + 10#${t:3:2} * 60 + 10#${t:6:2} ))
    if [ "$prev" -gt 0 ]; then
      gap=$(( v - prev )); [ "$gap" -lt 0 ] && gap=$(( gap + 86400 ))
      gaps="$gaps$gap
"
    fi
    prev="$v"
  done < <(grep -oE '^\| [0-9]+ \| [0-9]{2}:[0-9]{2}:[0-9]{2}' "$led" 2>/dev/null | awk '{print $4}' | tail -n 11)
  n="$(printf '%s' "$gaps" | grep -c .)"
  if [ "${n:-0}" -lt 1 ]; then echo "$STALE_FLOOR"; return; fi
  mid=$(( n / 2 + 1 ))
  m="$(printf '%s' "$gaps" | sort -n | sed -n "${mid}p")"
  m=$(( m * 3 / 60 ))
  [ "$m" -lt "$STALE_FLOOR" ] && m="$STALE_FLOOR"
  [ "$m" -gt 240 ] && m=240
  echo "$m"
}

next_stall_at=0
stalled=0
last_guard_epoch=0
notlive_next=0; notlive_step=900
foreign_said=0

while true; do
  if [ ! -f "$STATE" ]; then
    echo "GONE goal $SLUG: state file $STATE no longer exists. Nothing is being verified."
    exit 0
  fi

  ARMED="$(jq -r '.armed // false' "$STATE" 2>/dev/null || echo unknown)"
  LEDGER="$(jq -r '.ledger // ""' "$STATE" 2>/dev/null || true)"
  [ -n "$LEDGER" ] || LEDGER="docs/goals/goal-${SLUG}.ledger.md"
  case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac

  if [ "$ARMED" != "true" ]; then
    REASON="$(jq -r '.end_reason // "unknown"' "$STATE" 2>/dev/null || echo unknown)"
    if [ "$REASON" = "met" ]; then
      echo "DONE goal $SLUG: every gate passed and the guard disarmed itself. Ledger: $LEDGER"
    else
      STUCK="$(jq -r '.stuck_on // ""' "$STATE" 2>/dev/null || true)"
      echo "ENDED goal $SLUG: disarmed with end_reason=$REASON${STUCK:+ (stuck on $STUCK)}. Ledger: $LEDGER"
    fi
    exit 0
  fi

  NOW="$(date +%s)"
  SID="$(jq -r '.session_id // ""' "$STATE" 2>/dev/null || true)"
  LIVE="$(jq -r '.hook_live // "unknown"' "$STATE" 2>/dev/null || echo unknown)"
  EVID="$(jq -r '.hook_evidence // ""' "$STATE" 2>/dev/null || true)"
  LG="$(epoch_of "$(jq -r '.last_guard_at // .hook_proven_at // ""' "$STATE" 2>/dev/null || true)")"
  STARTED="$(mtime_of "$STATE")"
  LM="$(mtime_of "$LEDGER")"

  # The guard has not run for this run yet. "proven" via the sentinel means the
  # registration was in the startup snapshot, so the first Stop will fire; the
  # only thing to wait for is the end of the current turn. Anything else is a
  # run that is not being verified, and it stays news until it changes.
  if [ "$LG" -eq 0 ]; then
    if [ "$LIVE" != "proven" ] || [ "$EVID" != "sentinel" ]; then
      if [ "$NOW" -ge "$notlive_next" ] && [ "$((NOW - STARTED))" -ge 900 ]; then
        echo "NOTLIVE goal $SLUG: armed $(( (NOW - STARTED) / 60 ))m ago and the guard has not fired once, so nothing is verifying anything. Hook configuration is snapshotted at process start; a registration written mid-session loads only after /hooks or a restart. Restart, then re-arm from the new session (arm.sh reads the sentinel's heartbeat and says whether the guard is loaded). Do not build a loop that appends ledger rows in its place — it cannot block a turn and it blinds this watcher."
        notlive_next=$((NOW + notlive_step)); notlive_step=$((notlive_step * 2)); [ "$notlive_step" -gt 14400 ] && notlive_step=14400
      fi
    fi
    if [ "$foreign_said" -eq 0 ] && [ "$LM" -gt 0 ] && [ "$LM" -gt "$STARTED" ]; then
      foreign_said=1
      echo "FOREIGN goal $SLUG: the ledger at $LEDGER is being written to, but the guard has never run for this run. Whatever is appending rows is not the guard: it cannot block a turn ending, so it is a notifier at best, and its rows are not verification. Stop it before trusting the ledger."
    fi
    sleep "$INTERVAL"; continue
  fi

  if [ "$LG" -gt "$last_guard_epoch" ]; then
    if [ "$stalled" -eq 1 ]; then
      echo "RESUMED goal $SLUG: the guard ran again after a stall. Last row: $(tail -n 1 "$LEDGER" 2>/dev/null)"
    fi
    last_guard_epoch="$LG"
    stalled=0
    next_stall_at=0
  fi

  if [ "$STALE_MIN" -gt 0 ]; then STALE_SEC=$((STALE_MIN * 60))
  else STALE_SEC=$(( $(adaptive_stale_min "$LEDGER") * 60 )); fi

  QUIET=$((NOW - LG))

  # The session wrote to its transcript recently, so the run is mid-turn rather
  # than dead. This is the check that turns 34 of 56 measured wakes into silence.
  TM="$(transcript_mtime "$SID")"
  if [ "$TM" -gt 0 ] && [ "$(( (NOW - TM) / 60 ))" -lt "$ALIVE_MIN" ]; then
    sleep "$INTERVAL"; continue
  fi

  if [ "$QUIET" -ge "$STALE_SEC" ] && [ "$NOW" -ge "$next_stall_at" ]; then
    stalled=1
    MINS=$((QUIET / 60))
    echo "STALL goal $SLUG: armed, and not breathing — the guard last ran ${MINS}m ago and the session's own transcript is cold. The run may have died mid-turn (usage limit, crashed delivery agent, lost session). Check background agents and workflows, then resume the work or disarm with disarm.sh $SLUG. Ledger: $LEDGER"
    STEP=$((QUIET)); [ "$STEP" -gt 14400 ] && STEP=14400
    next_stall_at=$((NOW + STEP))
  fi

  sleep "$INTERVAL"
done
