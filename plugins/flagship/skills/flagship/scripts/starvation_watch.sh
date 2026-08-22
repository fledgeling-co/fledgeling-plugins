#!/bin/zsh
# flagship — fleet starvation watch.
#
# Arm this with the Monitor tool BEFORE the first dispatch, persistent:
#   Monitor(command: "<this path>", persistent: true, description: "fleet starvation")
#
# It emits ONE line only when the armada's working state CHANGES, because a wake
# that carries no new information trains the conductor to ignore wakes.
#
# The failure it exists for: a fleet of live sessions that have all finished their
# last dispatch and are waiting for the next one. From inside the conductor's
# session that is indistinguishable from a fleet hard at work — both are silence.
# Measured: thirteen Opus sessions idle for three hours on a 16-core machine at
# 0.23 load per core, and the operator noticed before the conductor did.
#
# States, all four emitted so silence is never ambiguous:
#   STARVED     fleet idle while the machine is free  -> dispatch
#   OVERLOADED  the other direction; this machine has hit load 830 -> shed
#   THIN        disk is the closing gate -> hand to mac-doctor
#   WORKING     the all-clear, so a return to normal is also a wake

NCPU=$(sysctl -n hw.ncpu)
IDLE_PER_CORE=${FLAGSHIP_IDLE_PER_CORE:-0.50}   # below this, nothing much is running
HOT_PER_CORE=${FLAGSHIP_HOT_PER_CORE:-3.00}     # above this, shed rather than dispatch
MIN_ACTIVE=${FLAGSHIP_MIN_ACTIVE:-4}            # sessions expected to be writing
IDLE_SAMPLES=${FLAGSHIP_IDLE_SAMPLES:-3}        # ~3 min before calling it starved
INTERVAL=${FLAGSHIP_INTERVAL:-60}

prev=""; streak_idle=0; streak_hot=0

while true; do
  # A session that is working appends to its transcript. mtime is the cheapest
  # liveness signal that does not require asking every session and waiting.
  active=$(find "$HOME/.claude/projects" -name '*.jsonl' -mmin -3 2>/dev/null | wc -l | tr -d ' ')
  # macOS pgrep has no -c. `pgrep -fc` prints a usage error and reads as zero.
  live=$(pgrep -f 'claude' 2>/dev/null | wc -l | tr -d ' ')
  # The 1-minute average is itself a decaying average: it reads low in the trough
  # between bursts, so a go decision taken on it lands in the next burst. Measured:
  # 1m moved 5.30 -> 7.73 across 30s while 5m held at 5.18. Decide on the 5-minute
  # figure, report both, so a quiet moment is never mistaken for a quiet machine.
  load1=$(sysctl -n vm.loadavg | awk '{print $2}')
  load5=$(sysctl -n vm.loadavg | awk '{print $3}')
  per1=$(echo "$load1 $NCPU" | awk '{printf "%.2f", $1/$2}')
  per=$(echo "$load5 $NCPU"  | awk '{printf "%.2f", $1/$2}')
  # Never `df -h /` — that is the read-only system volume and reads ~5% against
  # a data volume at 87%, wrong by an order of magnitude in the reassuring direction.
  diskpct=$(df -P /System/Volumes/Data | awk 'NR==2{gsub("%","",$5);print $5}')

  hot=$(echo "$per $HOT_PER_CORE"  | awk '{print ($1>$2)?1:0}')
  idle=$(echo "$per $IDLE_PER_CORE $active $MIN_ACTIVE" | awk '{print ($1<$2 && $3<$4)?1:0}')

  [ "$hot"  = 1 ] && streak_hot=$((streak_hot+1))   || streak_hot=0
  [ "$idle" = 1 ] && streak_idle=$((streak_idle+1)) || streak_idle=0

  if   [ "$diskpct" -ge 95 ];       then state="THIN"
  elif [ $streak_hot  -ge 2 ];      then state="OVERLOADED"
  elif [ $streak_idle -ge $IDLE_SAMPLES ]; then state="STARVED"
  elif [ "$idle" = 0 ] && [ "$hot" = 0 ];  then state="WORKING"
  else state="$prev"; fi

  if [ -n "$state" ] && [ "$state" != "$prev" ]; then
    echo "$state — ${active} sessions wrote in the last 3min, ${live} claude procs, load/core ${per} (5m) / ${per1} (1m), disk ${diskpct}%"
    prev="$state"
  fi
  sleep "$INTERVAL"
done
