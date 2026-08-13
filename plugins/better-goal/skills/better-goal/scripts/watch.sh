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
#   STALL     ledger has not moved for --stale minutes while still armed
#             (re-emitted on exponential backoff, never on every poll)
#   RESUMED   the ledger moved again after a STALL
#   DONE      disarmed with end_reason=met
#   ENDED     disarmed for any other reason (stuck, deadline, max_iterations)
#   GONE      the state file disappeared

set -uo pipefail

SLUG="${1:-}"; shift 2>/dev/null || true
STALE_MIN=25; INTERVAL=60
while [ $# -gt 0 ]; do
  case "$1" in
    --stale)    STALE_MIN="${2:-25}"; shift 2 ;;
    --interval) INTERVAL="${2:-60}";  shift 2 ;;
    *) shift ;;
  esac
done
[ -n "$SLUG" ] || { echo "watch.sh: usage: watch.sh <slug> [--stale MIN] [--interval SEC]" >&2; exit 2; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE="$ROOT/.claude/goals/${SLUG}.json"
[ -f "$STATE" ] || STATE="$ROOT/.claude/goal-state.json"

mtime_of() { [ -f "$1" ] && { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; } || echo 0; }

# Backoff so a run left stalled overnight wakes the session a handful of times
# rather than every $INTERVAL. Doubles from the stale threshold, capped at 4h.
STALE_SEC=$((STALE_MIN * 60))
next_stall_at=0
stalled=0
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

  if [ "$LM" -gt "$last_ledger_mtime" ]; then
    if [ "$stalled" -eq 1 ]; then
      echo "RESUMED goal $SLUG: the ledger moved again after a stall. Last row: $(tail -n 1 "$LEDGER" 2>/dev/null)"
    fi
    last_ledger_mtime="$LM"
    stalled=0
    next_stall_at=0
  fi

  # An armed run with no ledger yet is treated as starting from now, so arming
  # the watcher before the first turn does not fire a spurious stall.
  REF="$LM"; [ "$REF" -gt 0 ] || REF="$(mtime_of "$STATE")"
  QUIET=$((NOW - REF))

  if [ "$QUIET" -ge "$STALE_SEC" ] && [ "$NOW" -ge "$next_stall_at" ]; then
    stalled=1
    MINS=$((QUIET / 60))
    echo "STALL goal $SLUG: armed, but the ledger has not moved for ${MINS}m. The run may have died mid-turn (usage limit, crashed delivery agent, lost session). Check the delivery agents are alive, resume or restart what died, then continue the worklist in $(jq -r '.goal_file // "the brief"' "$STATE" 2>/dev/null). Ledger: $LEDGER"
    # Next stall report no sooner than double the quiet period, capped at 4h.
    STEP=$((QUIET)); [ "$STEP" -gt 14400 ] && STEP=14400
    next_stall_at=$((NOW + STEP))
  fi

  sleep "$INTERVAL"
done
