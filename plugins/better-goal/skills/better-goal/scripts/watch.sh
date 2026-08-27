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
#   NOTLIVE   armed, but the Stop hook has never fired — it was registered
#             mid-session into a .claude/ that Claude Code is not watching
#   STALL     the run is not breathing: the ledger has not moved for --stale
#             minutes AND the owning session's transcript is cold
#             (re-emitted on exponential backoff, never on every poll)
#   RESUMED   the ledger moved again after a STALL
#   DONE      disarmed with end_reason=met
#   ENDED     disarmed for any other reason (stuck, api_error, session_ended,
#             deadline, max_iterations)
#   GONE      the state file disappeared
#
# Liveness comes from the session transcript, not from the ledger alone. Of 56
# STALLs delivered across 14 real sessions, 34 arrived within ten minutes of an
# assistant message and 22 of those in the same minute: the watcher was waking a
# session to tell it that it might be dead, and each wake re-bills the whole
# session prefix. A turn that runs longer than --stale is the normal case here,
# not a failure — measured median gap between ledger rows was 28.5 minutes on one
# run and 95.7 on another, against a 25-minute default.

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

# The session's transcript is appended to while a turn runs, so its mtime is the
# only liveness signal readable from outside the session. The project directory
# name is derived from the cwd, so glob on the session id rather than encoding it.
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
# The median rather than the widest, because one 220-minute gap in an otherwise
# half-hourly run would otherwise push the threshold to the cap and blind the
# backstop entirely.
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

# Backoff so a run left stalled overnight wakes the session a handful of times
# rather than every $INTERVAL. Doubles from the stale threshold, capped at 4h.
next_stall_at=0
stalled=0
notlive_said=0
last_ledger_mtime=0

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
  LM="$(mtime_of "$LEDGER")"
  SID="$(jq -r '.session_id // ""' "$STATE" 2>/dev/null || true)"
  LIVE="$(jq -r '.hook_live // "unknown"' "$STATE" 2>/dev/null || echo unknown)"

  # A guard that has never fired is a different failure from a run that has
  # stopped, and it has a different fix: the hook is written correctly and was
  # never loaded, which only /hooks or a restart can change. Saying "the run may
  # have died" here sent live runs hunting for dead agents that were never there.
  if [ "$LIVE" != "proven" ] && [ "$notlive_said" -eq 0 ]; then
    STARTED="$(mtime_of "$STATE")"
    if [ "$((NOW - STARTED))" -ge 900 ]; then
      notlive_said=1
      echo "NOTLIVE goal $SLUG: armed, but the Stop guard has not fired once in $(( (NOW - STARTED) / 60 ))m, so nothing is verifying anything. It was registered mid-session and Claude Code only watches a .claude/ that already held a settings file when the session started. Ask the user to open /hooks once or restart — you cannot do it yourself. Until then, run the gates by hand each turn and say that is what you are doing."
    fi
  fi

  if [ "$LM" -gt "$last_ledger_mtime" ]; then
    if [ "$stalled" -eq 1 ]; then
      echo "RESUMED goal $SLUG: the ledger moved again after a stall. Last row: $(tail -n 1 "$LEDGER" 2>/dev/null)"
    fi
    last_ledger_mtime="$LM"
    stalled=0
    next_stall_at=0
    notlive_said=0
  fi

  if [ "$STALE_MIN" -gt 0 ]; then STALE_SEC=$((STALE_MIN * 60))
  else STALE_SEC=$(( $(adaptive_stale_min "$LEDGER") * 60 )); fi

  # An armed run with no ledger yet is treated as starting from now, so arming
  # the watcher before the first turn does not fire a spurious stall.
  REF="$LM"; [ "$REF" -gt 0 ] || REF="$(mtime_of "$STATE")"
  QUIET=$((NOW - REF))

  # The session wrote to its transcript recently, so the run is mid-turn rather
  # than dead. This is the check that turns 34 of 56 measured wakes into silence.
  TM="$(transcript_mtime "$SID")"
  if [ "$TM" -gt 0 ] && [ "$(( (NOW - TM) / 60 ))" -lt "$ALIVE_MIN" ]; then
    sleep "$INTERVAL"; continue
  fi

  if [ "$QUIET" -ge "$STALE_SEC" ] && [ "$NOW" -ge "$next_stall_at" ]; then
    stalled=1
    MINS=$((QUIET / 60))
    echo "STALL goal $SLUG: armed, and not breathing — the ledger has not moved for ${MINS}m and the session's own transcript is cold. The run may have died mid-turn (usage limit, crashed delivery agent, lost session). Check the delivery agents are alive, resume or restart what died, then continue the worklist in $(jq -r '.goal_file // "the brief"' "$STATE" 2>/dev/null). Ledger: $LEDGER"
    # Next stall report no sooner than double the quiet period, capped at 4h.
    STEP=$((QUIET)); [ "$STEP" -gt 14400 ] && STEP=14400
    next_stall_at=$((NOW + STEP))
  fi

  sleep "$INTERVAL"
done
