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
BERTHS=${FLAGSHIP_BERTHS:-$HOME/Dev/fledgeling-plugins/plugins/harbourmaster/skills/harbourmaster/scripts/berths.py}
MIN_HELD_SEC=${FLAGSHIP_MIN_HELD_SEC:-600}   # ignore short holds; lower it to self-test
IDLE_PER_CORE=${FLAGSHIP_IDLE_PER_CORE:-0.50}   # below this, nothing much is running
HOT_PER_CORE=${FLAGSHIP_HOT_PER_CORE:-3.00}     # above this, shed rather than dispatch
MIN_ACTIVE=${FLAGSHIP_MIN_ACTIVE:-4}            # sessions expected to be writing
IDLE_SAMPLES=${FLAGSHIP_IDLE_SAMPLES:-3}        # ~3 min before calling it starved
INTERVAL=${FLAGSHIP_INTERVAL:-60}

prev=""; streak_idle=0; streak_hot=0; prev_leak=""; prev_daemon=""; streak_daemon=0

# An OS daemon can be the largest consumer on the machine while no session owns it,
# and every load figure then reads as fleet pressure. Measured 23 Aug 2026:
# coreaudiod at 170.6% for five and a half hours with no audio client running, ahead
# of every application process. It does not clear on its own and it needs sudo, so
# the useful thing a watcher can do is name it rather than fix it.
DAEMON_PCT=${FLAGSHIP_DAEMON_PCT:-80}
DAEMONS=${FLAGSHIP_DAEMONS:-'coreaudiod|WindowServer|mds_stores|mdworker|syspolicyd|XprotectService'}

runaway_daemon() {
  ps -Ao pcpu=,comm= -r 2>/dev/null | awk -v pct="$DAEMON_PCT" -v pat="$DAEMONS" '
    { name=$2; sub(/.*\//,"",name)
      if ($1+0 >= pct+0 && name ~ pat) { printf "%s at %.0f%%; ", name, $1 } }' | sed 's/; $//'
}

# A berth is held until the process TREE exits, so a command ending in a tail, a
# supervisor, a dev server or a --watch never returns it. You cannot see that in the
# command you wrapped: the case this was written from was `node scripts/local-capture.mjs`,
# whose `docker logs -f` sat three levels down, so no lint on the wrapped string would
# have caught it. What IS visible is the work-to-wall ratio. Measured on that leak:
# 0.08s of CPU against 7,490s elapsed, about 1e-5. Not proof, since a process genuinely
# blocked on IO looks the same, which is why this is a warning naming the running
# descendant rather than a verdict.
leaked_berths() {
  local out="" pid etime cpu esec csec desc
  for pid in $(python3 "$BERTHS" 2>/dev/null       | python3 -c 'import sys,json;d=json.load(sys.stdin);print("\n".join(sorted({str(o.get("pid")) for o in (d.get("occupants") or []) if o.get("pid")})))' 2>/dev/null); do
    read -r etime cpu <<< "$(ps -o etime=,time= -p "$pid" 2>/dev/null | tr -s ' ')"
    [ -z "$etime" ] && continue
    esec=$(echo "$etime" | awk -F'[-:]' '{n=NF; s=$n; if(n>1)s+=$(n-1)*60; if(n>2)s+=$(n-2)*3600; if(n>3)s+=$(n-3)*86400; print s}')
    csec=$(echo "$cpu"   | awk -F'[-:]' '{n=NF; s=$n; if(n>1)s+=$(n-1)*60; if(n>2)s+=$(n-2)*3600; print s}')
    [ -z "$esec" ] || [ "$esec" -lt "$MIN_HELD_SEC" ] 2>/dev/null && continue
    # under 0.1% of wall clock spent on CPU, across the whole tree's own accounting
    if awk -v c="$csec" -v e="$esec" 'BEGIN{exit !(e>0 && c/e < 0.001)}'; then
      desc=$(pgrep -P "$pid" 2>/dev/null | head -1)
      desc=$(ps -o command= -p "${desc:-$pid}" 2>/dev/null | cut -c1-60)
      out="${out}${out:+; }pid ${pid} ${etime} elapsed, ${cpu} CPU, running: ${desc}"
    fi
  done
  print -r -- "$out"
}

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

  # An OS daemon burning cores nobody owns, reported on its own axis: a session
  # reading load alone attributes it to the fleet and holds work that was never
  # the cause. Two samples before speaking, so a transient spike stays quiet.
  daemon=$(runaway_daemon)
  [ -n "$daemon" ] && streak_daemon=$((streak_daemon+1)) || streak_daemon=0
  if [ $streak_daemon -ge 2 ] && [ "$daemon" != "$prev_daemon" ]; then
    echo "OS DAEMON — $daemon (not fleet work; needs sudo to clear)"
    prev_daemon="$daemon"
  elif [ $streak_daemon -eq 0 ] && [ -n "$prev_daemon" ]; then
    echo "OS DAEMON cleared — $prev_daemon is back under ${DAEMON_PCT}%"
    prev_daemon=""
  fi

  # Independent of the load state: a leaked berth stalls a fleet on a quiet machine.
  leak=$(leaked_berths)
  if [ "$leak" != "$prev_leak" ]; then
    [ -n "$leak" ] && echo "BERTH LEAK — $leak" || echo "BERTH LEAK cleared"
    prev_leak="$leak"
  fi

  if [ -n "$state" ] && [ "$state" != "$prev" ]; then
    echo "$state — ${active} sessions wrote in the last 3min, ${live} claude procs, load/core ${per} (5m) / ${per1} (1m), disk ${diskpct}%"
    prev="$state"
  fi
  sleep "$INTERVAL"
done
