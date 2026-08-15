#!/usr/bin/env bash
# Runaway and orphan process lane -- the third of the 15m band that `reclaim.sh`
# documented and never implemented.
#
#   runaway.sh              report only; nothing is signalled
#   runaway.sh --apply      terminate what earlier runs already confirmed
#
# Human-readable progress goes to stderr. stdout is TSV for `reclaim.sh` to fold
# into the ledger, one record per line:
#
#   KILLED <id> <count> <detail>     signalled this run
#   WATCH  <id> <count> <detail>     seen runaway, not yet confirmed
#   KEPT   <id> <count> <reason>     confirmed but refused by the gate
#   USER   <id> <count> <reason>     runaway but not ours to signal (root, GUI)
#
# ---------------------------------------------------------------------------
# Why a watchlist rather than a threshold
#
# One sample cannot tell a spin loop from a build. `ps` %CPU answers "what did
# this do just now", and even sustained CPU (cumulative / elapsed) reads 100%
# for a Rust compile as readily as for a `yes` loop. The difference is only
# visible over time, so nothing is killed on first sight: a process must be seen
# runaway on RUNAWAY_CONFIRMATIONS separate runs spanning at least
# RUNAWAY_MIN_WATCH_SECONDS of wall clock before it is eligible. State lives in
# ~/.claude/mac-doctor/watchlist.tsv and is rewritten every run, so a process
# that stops being runaway leaves the list and starts again from zero.
#
# The span requirement is not redundant with the count. Under load these runs
# stack -- observed on this machine at load 418, a 15m job still alive after 8
# minutes with 0.02s of CPU -- so three "separate" runs can otherwise land
# within a minute of each other and confirm nothing.
#
# ---------------------------------------------------------------------------
# Why orphans only
#
# The single rule that keeps this safe is that nothing with a live owner is ever
# signalled. A build has cargo as a parent, a dev server has a shell, a test has
# its harness; something is waiting on all of them. A leak has nobody. So the
# candidate set is processes whose parent is launchd, plus processes below an
# ancestor that is itself reparented (the `python <- uv <- launchd` shape from
# references/processes.md), bounded to four hops.
#
# That rule alone would sweep up every GUI application, because macOS launches
# those from launchd too -- your own Chrome has PPID 1 exactly like a leaked
# one. The discriminator is the automation flags: a driver-spawned browser
# carries --disable-field-trial-config, --headless, --remote-debugging-port or a
# scratch --user-data-dir, and renderers inherit them. A .app without those
# markers, and anything below it, is the user's own and is never a candidate.
#
# ---------------------------------------------------------------------------
# Written for bash 3.2. launchd runs these agents with a minimal PATH, so
# `/usr/bin/env bash` resolves to /bin/bash, which has no associative arrays --
# hence the parent-chain walk happening inside awk rather than in shell.
set -uo pipefail

APPLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) shift ;;
  esac
done

STATE="$HOME/.claude/mac-doctor"
WATCHLIST="$STATE/watchlist.tsv"
PROTECTED="$STATE/protected"
LOCKDIR="$STATE/runaway.lock"
mkdir -p "$STATE"

# Tunables. Defaults are deliberately conservative: ten minutes of life before
# anything counts as sustained, and 60% of a core averaged across that life.
MIN_ELAPSED="${RUNAWAY_MIN_ELAPSED:-600}"
MIN_SUSTAINED="${RUNAWAY_SUSTAINED_PCT:-60}"
CONFIRMATIONS="${RUNAWAY_CONFIRMATIONS:-3}"
MIN_WATCH="${RUNAWAY_MIN_WATCH_SECONDS:-1800}"
BROWSER_MIN_ELAPSED="${RUNAWAY_BROWSER_MIN_ELAPSED:-1800}"
# Idle orphan families: the 167-MCP-server and 548-log-follower shape from
# references/processes.md. Near-zero CPU, so the sustained test above cannot see
# them, and a day of life so a legitimately detached daemon is not mistaken for
# one. Family size is the discriminator that matters: one long-lived idle orphan
# is usually a daemon doing its job, while five identical ones is a leak.
IDLE_MIN_ELAPSED="${RUNAWAY_IDLE_MIN_ELAPSED:-86400}"
IDLE_MAX_SUSTAINED="${RUNAWAY_IDLE_MAX_SUSTAINED:-2}"
IDLE_MIN_FAMILY="${RUNAWAY_IDLE_MIN_FAMILY:-5}"

log() { printf 'runaway: %s\n' "$1" >&2; }

# Records accumulate per process and are aggregated by finding id on the way
# out. The unit of a finding is a family, not a PID: 48 leaked burners are one
# record with a count of 48, because recurrence detection groups by id and 48
# separate rows read as 48 unrelated events.
RECORDS=$(mktemp "${TMPDIR:-/tmp}/mac-doctor-records.XXXXXX")
emit() { printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" >> "$RECORDS"; }
aggregate() {
  [ -s "$RECORDS" ] || return 0
  sort -t"$(printf '\t')" -k1,1 -k2,2 "$RECORDS" | awk -F'\t' '
    { key = $1 FS $2
      if (!(key in seen)) { seen[key]=1; kind[key]=$1; id[key]=$2; detail[key]=$4; order[++n]=key }
      procs[key]++; units[key] += $3 }
    END { for (i=1; i<=n; i++) { k=order[i]
        d = detail[k]
        if (procs[k] > 1) d = procs[k] " processes; first: " d
        printf "%s\t%s\t%s\t%s\n", kind[k], id[k], units[k], d } }'
}

# A stacked run must not double-count sightings or signal a family twice. The
# lock is a directory because mkdir is atomic; a lock whose owner is gone, or
# which is older than ten minutes, is stolen rather than left to disable the
# lane forever.
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  owner=$(cat "$LOCKDIR/pid" 2>/dev/null)
  stale=0
  [ -n "$owner" ] && ! kill -0 "$owner" 2>/dev/null && stale=1
  [ -n "$(find "$LOCKDIR" -maxdepth 0 -mmin +10 2>/dev/null)" ] && stale=1
  if [ "$stale" -eq 1 ]; then
    log "stealing stale lock from pid ${owner:-unknown}"
    rm -rf "$LOCKDIR" && mkdir "$LOCKDIR" 2>/dev/null || exit 0
  else
    log "another run holds the lock (pid ${owner:-unknown}); skipping"
    exit 0
  fi
fi
echo $$ > "$LOCKDIR/pid"
trap 'aggregate; rm -rf "$LOCKDIR" "$RECORDS"' EXIT INT TERM

NOW=$(date +%s)
MYUID=$(id -u)

# This script's own ancestry, so a wedged sibling reclaim.sh can never be its
# own victim.
self_chain=":"
p=$$
i=0
while [ "$i" -lt 12 ]; do
  self_chain="$self_chain$p:"
  p=$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')
  [ -z "$p" ] && break
  [ "$p" -le 1 ] 2>/dev/null && break
  i=$((i+1))
done

# `protected` holds one glob per line and is the escape hatch for a deliberate
# fixture -- a load generator for a benchmark, a long-running scratch process.
# Matched against the command line here, not just against paths.
protected_cmd() {
  [ -f "$PROTECTED" ] || return 1
  while IFS= read -r pat; do
    [ -z "$pat" ] && continue
    case "$1" in $pat) return 0 ;; esac
    case "$1" in *"$pat"*) return 0 ;; esac
  done < "$PROTECTED"
  return 1
}

# ---- declared instruments ---------------------------------------------------
# A deliberate CPU load fixture and a leak look identical from outside: both are
# orphaned, both burn a core, neither has an owner you can ask. That ambiguity
# is what made a batch of ANV-0377's load burners get killed by hand on this
# machine about seventy seconds before their own runner would have reaped them.
#
# So a runner that spawns load can say so. Any file under
# ~/.claude/mac-doctor/instruments/ is read as TSV:
#
#   <pid>	<expires_unix_epoch>	<owner label>
#
# An unexpired declaration makes the pid invisible to this lane. An EXPIRED one
# does the opposite of protecting it: the declaration is the runner's own
# promise about when the load should be gone, so a burner outliving its stamp is
# a stranded instrument, which is exactly the leak worth reaping. Expiry is what
# separates the two, and only the spawner can supply it.
INSTRUMENTS="$STATE/instruments"
declared=":"
if [ -d "$INSTRUMENTS" ]; then
  for f in "$INSTRUMENTS"/*; do
    [ -f "$f" ] || continue
    while IFS=$'\t' read -r dpid dexp dlabel; do
      case "$dpid" in ''|*[!0-9]*) continue ;; esac
      case "$dexp" in ''|*[!0-9]*) continue ;; esac
      if [ "$dexp" -gt "$NOW" ]; then
        declared="$declared$dpid:"
      else
        log "instrument ${dlabel:-unlabelled} pid $dpid expired $((NOW - dexp))s ago; eligible"
      fi
    done < "$f"
  done
fi

# ---- candidate scan ---------------------------------------------------------
# One ps pass. `command` is last because it is the only field that can contain
# spaces; everything before it is fixed-shape, which is what lets awk take
# fields 1..7 and join the rest.
CANDIDATES=$(ps -Ao pid=,ppid=,stat=,uid=,rss=,time=,etime=,command= 2>/dev/null | awk \
  -v min_el="$MIN_ELAPSED" -v min_pct="$MIN_SUSTAINED" -v br_el="$BROWSER_MIN_ELAPSED" \
  -v idle_el="$IDLE_MIN_ELAPSED" -v idle_pct="$IDLE_MAX_SUSTAINED" -v idle_fam="$IDLE_MIN_FAMILY" \
  -v myuid="$MYUID" -v selfchain="$self_chain" -v declared="$declared" '
  function tosec(t,  n,p){n=split(t,p,":"); if(n==3) return p[1]*3600+p[2]*60+p[3]; if(n==2) return p[1]*60+p[2]; return 0}
  function el(e,  d,r,n,p,dy){dy=0; if(index(e,"-")){split(e,d,"-"); dy=d[1]; r=d[2]} else r=e
    n=split(r,p,":"); if(n==3) return dy*86400+p[1]*3600+p[2]*60+p[3]; if(n==2) return dy*86400+p[1]*60+p[2]; return dy*86400}
  function is_gui(c){ return (c ~ /\.app\/Contents\/MacOS\//) }
  function is_auto(c){ return (c ~ /--(disable-field-trial-config|remote-debugging-port|remote-debugging-pipe|headless|enable-automation|test-type)/ \
                            || c ~ /--user-data-dir=(\/tmp|\/var\/folders|\/private\/var\/folders)/) }
  function is_browser(c){ return (c ~ /(Google Chrome|Chromium|chrome-headless-shell|chromedriver|geckodriver|msedgedriver|playwright|puppeteer|obscura)/) }
  function is_system(c){ return (c ~ /^\/(System|usr\/libexec|usr\/sbin|sbin|Library\/Apple|Library\/PrivateFrameworks)\//) }
  # Orphan-family membership. Direct reparenting to launchd, or descent from an
  # ancestor that is itself reparented -- but a session leader (stat contains
  # "s") or a non-automation GUI app anywhere up the chain means the process has
  # an owner, and the walk stops there.
  function orphaned(p,  a,hops){
    if (!(p in pp)) return 0
    if (pp[p] == 1) return 1
    a = pp[p]; hops = 0
    while (hops++ < 4) {
      if (!(a in pp)) return 1                                   # parent vanished mid-scan
      if (st[a] ~ /s/) return 0                                  # session leader: owned
      if (is_gui(cm[a]) && !is_auto(cm[a])) return 0             # the user own app: owned
      if (pp[a] == 1) return 1
      a = pp[a]
    }
    return 0
  }
  {
    pid=$1; cmd=""; for(i=8;i<=NF;i++) cmd=cmd (i>8?" ":"") $i
    pp[pid]=$2; st[pid]=$3; ui[pid]=$4; rs[pid]=$5
    cs[pid]=tosec($6); es[pid]=el($7); cm[pid]=cmd
  }
  END {
    # Pass one: apply the gates that do not depend on other processes, and count
    # each surviving name so family size is known before anything is classified.
    for (pid in pp) {
      cmd = cm[pid]
      if (ui[pid] != myuid) continue                             # root and system daemons are reported, never signalled
      if (index(selfchain, ":" pid ":")) continue                # never our own ancestry
      if (index(declared, ":" pid ":")) continue                 # an unexpired declared instrument
      if (st[pid] ~ /\+/) continue                               # foreground of a tty: interactive
      if (st[pid] ~ /^Z/) continue                               # zombie: the parent reaps it, not us
      if (is_system(cmd)) continue
      if (is_gui(cmd) && !is_auto(cmd)) continue                 # the user own application
      if (!orphaned(pid)) continue

      # comm for the ledger id: the executable basename, versions and pids
      # stripped, so one leak reads as one finding across runs.
      n = split(cmd, w, " "); base = w[1]
      k = split(base, s, "/"); nme = s[k]
      gsub(/[0-9]+$/, "", nme); gsub(/-[0-9a-f]{8,}$/, "", nme)
      if (nme == "") nme = "unknown"

      elig[pid] = 1; name[pid] = nme
      pct[pid] = (es[pid] > 0) ? cs[pid] / es[pid] * 100 : 0
      fam[nme]++
    }

    # Pass two: classify. Only now is family size known, which is the whole
    # discriminator for the idle class.
    for (pid in elig) {
      nme = name[pid]; p = pct[pid]
      class = ""
      if (es[pid] >= min_el && p >= min_pct)                      class = "runaway-cpu"
      else if (is_browser(cm[pid]) && is_auto(cm[pid]) && es[pid] >= br_el) class = "orphan-family"
      else if (es[pid] >= idle_el && p <= idle_pct && fam[nme] >= idle_fam) class = "idle-orphan"
      if (class == "") continue

      printf "%s\t%s\t%d\t%d\t%.1f\t%s\t%s\n", pid, class, cs[pid], es[pid], p, nme, substr(cm[pid],1,200)
    }
  }')

if [ -z "$CANDIDATES" ]; then
  # An empty watchlist is the normal state; clear any stale entries so a process
  # that recovered does not carry its old sightings into a future run.
  : > "$WATCHLIST"
  log "no candidates"
  exit 0
fi

# ---- stable identity --------------------------------------------------------
# A PID alone is reusable, so a recycled number could inherit another process's
# sightings and be killed on its first run. Identity is PID plus the kernel's
# own start timestamp, which never drifts -- unlike `etime`, whose one-second
# resolution wobbles between samples and would break every key match.
cand_pids=$(printf '%s\n' "$CANDIDATES" | cut -f1 | tr '\n' ',' | sed 's/,$//')
LSTARTS=$(ps -p "$cand_pids" -o pid=,lstart= 2>/dev/null)

started_key() { # started_key <pid> -> pid-SatAug15123212026
  printf '%s\n' "$LSTARTS" | awk -v want="$1" '
    $1 == want { s=""; for(i=2;i<=NF;i++) s = s $i; print want "-" s; exit }'
}

# ---- watchlist merge --------------------------------------------------------
NEW_WATCHLIST=$(mktemp "${TMPDIR:-/tmp}/mac-doctor-watch.XXXXXX")
CONFIRMED=$(mktemp "${TMPDIR:-/tmp}/mac-doctor-confirmed.XXXXXX")
trap 'aggregate; rm -rf "$LOCKDIR" "$RECORDS"; rm -f "$NEW_WATCHLIST" "$CONFIRMED"' EXIT INT TERM

printf '%s\n' "$CANDIDATES" | while IFS=$'\t' read -r pid class cpusec elapsed pct name cmd; do
  [ -n "$pid" ] || continue
  key=$(started_key "$pid")
  [ -n "$key" ] || continue                       # process exited between the two ps calls

  prev=$(awk -F'\t' -v k="$key" '$1==k {print; exit}' "$WATCHLIST" 2>/dev/null)
  if [ -n "$prev" ]; then
    first=$(printf '%s' "$prev" | cut -f2)
    seen=$(printf '%s' "$prev" | cut -f3)
    seen=$((seen + 1))
  else
    first=$NOW
    seen=1
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$key" "$first" "$seen" "$NOW" "$class" "$name" >> "$NEW_WATCHLIST"

  watched=$((NOW - first))
  if [ "$seen" -ge "$CONFIRMATIONS" ] && [ "$watched" -ge "$MIN_WATCH" ]; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$pid" "$class" "$name" "$seen" "$watched" "$pct" "$cmd" >> "$CONFIRMED"
  else
    emit WATCH "$class:$name" 1 \
      "pid $pid, ${pct}% sustained over ${elapsed}s, sighting $seen/$CONFIRMATIONS, watched ${watched}s/${MIN_WATCH}s"
  fi
done

mv -f "$NEW_WATCHLIST" "$WATCHLIST" 2>/dev/null

[ -s "$CONFIRMED" ] || { log "nothing confirmed this run"; exit 0; }

# ---- the expensive gate, only for what is already confirmed -----------------
# lsof is slow enough to matter every fifteen minutes, so it runs against a
# handful of confirmed candidates rather than against every process.
established() { lsof -nP -p "$1" 2>/dev/null | grep -c ESTABLISHED | tr -d ' '; }

# Every descendant, collected before anything is signalled. Killing a browser
# tree's leaf leaves renderers behind, so the whole family is signalled together.
family_of() {
  local root="$1"
  ps -Ao pid=,ppid= 2>/dev/null | awk -v root="$root" '
    { pp[$1]=$2; pids[n++]=$1 }
    END {
      fam[root]=1; print root
      for (pass=0; pass<8; pass++)
        for (i=0; i<n; i++) {
          p=pids[i]
          if (!(p in fam) && (pp[p] in fam)) { fam[p]=1; print p }
        }
    }' | sort -un
}

while IFS=$'\t' read -r pid class name seen watched pct cmd; do
  [ -n "$pid" ] || continue
  kill -0 "$pid" 2>/dev/null || { log "pid $pid gone before signalling"; continue; }

  if protected_cmd "$cmd"; then
    emit KEPT "$class:$name" 1 "matches ~/.claude/mac-doctor/protected"
    continue
  fi

  # An idle orphan family is reported, never signalled. It costs RSS rather than
  # CPU, so there is no urgency to buy with the risk -- and from outside, a
  # hundred idle orphans are indistinguishable from another fleet's live
  # workers. The autonomy gradient says the 15m tier acts only where no
  # judgement is needed, and this needs judgement. Recorded every run it
  # persists: the count across runs is the signal, not any single sighting.
  if [ "$class" = "idle-orphan" ]; then
    emit USER "$class:$name" 1 \
      "orphaned ${pct}% CPU, alive $((watched))s under watch; suggested: kill by explicit pid after checking cwd"
    continue
  fi

  est=$(established "$pid")
  if [ "${est:-0}" -gt 0 ]; then
    emit KEPT "$class:$name" 1 "$est established connections; in use despite being orphaned"
    continue
  fi

  fam=$(family_of "$pid")
  count=$(printf '%s\n' "$fam" | grep -c . | tr -d ' ')

  if [ "$APPLY" -eq 0 ]; then
    emit KILLED "$class:$name" "$count" \
      "DRY RUN: would TERM then KILL pid $pid and $((count-1)) descendants (${pct}% sustained, confirmed $seen runs over ${watched}s)"
    continue
  fi

  # SIGTERM, wait, escalate. Chromium ignores SIGTERM routinely; that escalation
  # is expected rather than a sign anything went wrong.
  #
  # Signalled by explicit pid, never by command pattern. A `pkill -f` on this
  # class of machine has previously killed another runner's `cargo test` -- with
  # many worktrees checked out, a pattern that describes one fleet's process
  # describes every fleet's. The pid list here comes from the ps snapshot above
  # and from nothing else.
  # shellcheck disable=SC2086
  kill -TERM $fam 2>/dev/null
  sleep 3
  survivors=""
  for f in $fam; do kill -0 "$f" 2>/dev/null && survivors="$survivors $f"; done
  if [ -n "$survivors" ]; then
    # shellcheck disable=SC2086
    kill -KILL $survivors 2>/dev/null
  fi

  still=0
  for f in $fam; do kill -0 "$f" 2>/dev/null && still=$((still+1)); done
  if [ "$still" -eq 0 ]; then
    emit KILLED "$class:$name" "$count" \
      "pid $pid + $((count-1)) descendants, ${pct}% sustained, confirmed $seen runs over ${watched}s"
    log "killed $class:$name family of $count (root pid $pid)"
    # A killed identity must not linger on the watchlist, or a recycled PID
    # inherits its sightings. Filtered with awk rather than `grep -v`: this
    # script runs under `set -o pipefail`, and a grep that filters every line
    # exits 1, so the `&& mv` never fires precisely when the watchlist held
    # nothing but this entry -- the same defect the ledger writer in reclaim.sh
    # carries a scar for.
    key=$(started_key "$pid")
    if [ -n "$key" ]; then
      awk -F'\t' -v k="$key" '$1 != k' "$WATCHLIST" > "$WATCHLIST.tmp" 2>/dev/null
      mv -f "$WATCHLIST.tmp" "$WATCHLIST" 2>/dev/null
    fi
  else
    emit KEPT "$class:$name" "$count" "$still of $count survived SIGKILL; likely uninterruptible"
  fi
done < "$CONFIRMED"
