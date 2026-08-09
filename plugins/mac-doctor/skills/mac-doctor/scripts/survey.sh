#!/usr/bin/env bash
# One measurement pass for a mac-doctor tier: disk, reclaim targets, processes,
# orphans, listeners, Docker. Read-only -- signals nothing, deletes nothing.
# Writes JSON to a temp file and prints the path.
#
# Everything here is bounded. A maintenance tool that costs minutes of disk I/O
# to decide it has nothing to do is worse than no tool, so expensive targets are
# measured by asking the owning tool rather than by walking the filesystem.
set -uo pipefail

OUT="$(mktemp -t mac-doctor-XXXXXX).json"

# Tier gates how much measurement is worth doing. This is not an optimisation --
# a full sizing pass measured 526s on the reference machine, so a 15m cadence
# running it would overlap itself and thrash the disk it exists to protect.
# Short tiers ask only questions with instant answers.
TIER="15m"
while [ $# -gt 0 ]; do
  case "$1" in
    --tier) TIER="${2:-15m}"; shift 2 ;;
    *) shift ;;
  esac
done
case "$TIER" in
  15m|1h)   DO_TARGETS=0; DO_WORKTREES=0 ;;
  12h|1d)   DO_TARGETS=1; DO_WORKTREES=0 ;;
  7d|full)  DO_TARGETS=1; DO_WORKTREES=1 ;;
  *)        DO_TARGETS=0; DO_WORKTREES=0 ;;
esac

# `timeout` is GNU coreutils and is absent from stock macOS. A wrapper that is
# not there fails open -- empty output, exit 0 through a pipe -- which reads as
# a real zero. Detect it, and fall back to a killer subshell rather than
# silently dropping the bound. See references/reclaim.md.
_TB=""
for c in timeout gtimeout; do command -v "$c" >/dev/null 2>&1 && { _TB="$c"; break; }; done
bounded() {
  local s="$1"; shift
  if [ -n "$_TB" ]; then "$_TB" "$s" "$@"; return $?; fi
  "$@" & local p=$! rc=0
  ( sleep "$s"; kill -TERM "$p" 2>/dev/null ) >/dev/null 2>&1 & local w=$!
  wait "$p" 2>/dev/null || rc=124
  kill "$w" 2>/dev/null; return $rc
}
esc() { printf '%s' "${1:-}" | sed 's/\\/\\\\/g; s/"/\\"/g'; }

# Size a path in KB, bounded. Emits `null` when the bound was hit and sets the
# global INCOMPLETE flag, because a measurement that did not finish must never
# be summable as a zero. The reference machine's two largest worktree roots
# (303 GB and 239 GB) both exceeded their bound, and a consumer totalling
# `size_kb or 0` reported 77 GB for a 620 GB set -- a 543 GB hole that looked
# exactly like a small, tidy number. Bound failures fail closed and say so.
INCOMPLETE=0
sz() {
  local k
  k=$(bounded "${2:-25}" du -sxk "$1" 2>/dev/null | awk '{print $1}')
  if [ -z "${k:-}" ]; then INCOMPLETE=1; echo "null"; else echo "$k"; fi
}

DEV_ROOT="${DEV_ROOT:-$HOME/Dev}"

{
echo "{"
echo "  \"collected_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
echo "  \"host\": \"$(hostname -s 2>/dev/null)\","

# ---- disk -------------------------------------------------------------------
read -r _ blocks used avail capacity _ < <(df -k /System/Volumes/Data | tail -1)
free_pct=$(awk -v a="$avail" -v b="$blocks" 'BEGIN{printf "%.2f", (b>0)? a/b*100 : 0}')
state=$(awk -v p="$free_pct" 'BEGIN{print (p<2)?"critical":(p<5)?"low":(p<15)?"tight":"healthy"}')
container_free=$(diskutil info /System/Volumes/Data 2>/dev/null | awk -F'[()]' '/Container Free Space/{gsub(/[^0-9]/,"",$2); print $2}')
echo "  \"disk\": {"
echo "    \"total_kb\": $blocks, \"used_kb\": $used, \"avail_kb\": $avail,"
echo "    \"free_pct\": $free_pct, \"state\": \"$state\","
echo "    \"container_free_bytes\": ${container_free:-null}"
echo "  },"

# ---- reclaim targets --------------------------------------------------------
# Sizes come from the owning tool where one exists; du only for plain dirs.
# Skipped entirely on short tiers -- see the TIER gate above.
echo "  \"targets\": {"
if [ "$DO_TARGETS" -eq 1 ]; then
printf '    "derived_data_kb": %s,\n'   "$(sz "$HOME/Library/Developer/Xcode/DerivedData" 240)"
printf '    "core_simulator_kb": %s,\n' "$(sz "$HOME/Library/Developer/CoreSimulator" 120)"
printf '    "user_caches_kb": %s,\n'    "$(sz "$HOME/Library/Caches" 300)"
printf '    "npm_cache_kb": %s,\n'      "$(sz "$HOME/.npm" 60)"
printf '    "pnpm_store_kb": %s,\n'     "$(sz "$HOME/Library/pnpm" 60)"
printf '    "bun_cache_kb": %s,\n'      "$(sz "$HOME/.bun" 30)"
printf '    "claude_home_kb": %s,\n'    "$(sz "$HOME/.claude" 120)"
printf '    "claude_projects_kb": %s,\n' "$(sz "$HOME/.claude/projects" 120)"
printf '    "codex_home_kb": %s,\n'     "$(sz "$HOME/.codex" 60)"
printf '    "cursor_home_kb": %s,\n'    "$(sz "$HOME/.cursor" 60)"
printf '    "trash_kb": %s\n'           "$(sz "$HOME/.Trash" 20)"
else
INCOMPLETE=1
echo "    \"skipped_for_tier\": \"$TIER\""
fi
echo "  },"

# ---- worktree roots (aggregate, exact -- never extrapolated from a sample) ---
# Measured, not sampled. On the reference machine a 24-worktree stratified
# sample implied ~770 GB; the true aggregate was 620 GB. Skewed sets defeat
# means. Counts are free; sizes are the expensive part and are 7d-only.
echo "  \"worktree_roots\": ["
n=0
for d in "$DEV_ROOT"/*/.worktrees "$DEV_ROOT"/*/.claude/worktrees; do
  [ -d "$d" ] || continue
  cnt=$(ls -1 "$d" 2>/dev/null | wc -l | tr -d ' ')
  [ "$cnt" -eq 0 ] && continue
  [ $n -gt 0 ] && echo ","
  if [ "$DO_WORKTREES" -eq 1 ]; then s=$(sz "$d" 900); else s=null; INCOMPLETE=1; fi
  st="measured"; [ "$s" = "null" ] && { [ "$DO_WORKTREES" -eq 1 ] && st="timed_out" || st="not_attempted"; }
  printf '    {"path":"%s","count":%s,"size_kb":%s,"size_status":"%s"}' "$(esc "$d")" "$cnt" "$s" "$st"
  n=$((n+1))
done
echo ""
echo "  ],"
# Any consumer totalling sizes must read this first. A partial total presented
# as a whole one is how 620 GB became 77 GB.
# True whenever ANY size is absent -- failed bound or never attempted. The
# question it answers is "can these sizes be totalled?", and the answer is no
# either way. A flag that only covers failures leaves the skipped-tier case
# looking complete at zero, which is the same 620-GB-as-77-GB bug one layer up.
echo "  \"sizes_totalable\": $([ "$INCOMPLETE" -eq 1 ] && echo false || echo true),"

# ---- docker (asks docker, never du's Docker.raw: it is sparse) --------------
echo "  \"docker\": {"
if command -v docker >/dev/null 2>&1 && bounded 10 docker info >/dev/null 2>&1; then
  echo "    \"available\": true,"
  echo "    \"df\": ["
  bounded 20 docker system df --format '{{.Type}}|{{.TotalCount}}|{{.Active}}|{{.Size}}|{{.Reclaimable}}' 2>/dev/null \
   | awk -F'|' '{printf "%s      {\"type\":\"%s\",\"total\":\"%s\",\"active\":\"%s\",\"size\":\"%s\",\"reclaimable\":\"%s\"}", (n++?",\n":""), $1,$2,$3,$4,$5}'
  echo ""
  echo "    ],"
  printf '    "exited_containers": %s,\n' "$(bounded 15 docker ps -aq --filter status=exited 2>/dev/null | wc -l | tr -d ' ')"
  printf '    "dangling_images": %s\n'    "$(bounded 15 docker images -qf dangling=true 2>/dev/null | wc -l | tr -d ' ')"
else
  echo "    \"available\": false"
fi
echo "  },"

# ---- processes: sustained CPU is the runaway signal, not instantaneous %CPU --
echo "  \"processes\": ["
ps -Ao pid,ppid,stat,pcpu,rss,time,etime,user,comm,command 2>/dev/null | awk '
  function tosec(t,  n,p){n=split(t,p,":"); if(n==3) return p[1]*3600+p[2]*60+p[3]; if(n==2) return p[1]*60+p[2]; return 0}
  function el(e,  d,r,n,p,dy){dy=0; if(index(e,"-")){split(e,d,"-"); dy=d[1]; r=d[2]} else r=e
    n=split(r,p,":"); if(n==3) return dy*86400+p[1]*3600+p[2]*60+p[3]; if(n==2) return dy*86400+p[1]*60+p[2]; return dy*86400}
  function esc(s){gsub(/\\/,"\\\\",s); gsub(/"/,"\\\"",s); return s}
  NR==1{next}
  { cmd=""; for(i=10;i<=NF;i++) cmd=cmd (i>10?" ":"") $i
    cs=tosec($6); es=el($7); r=(es>0)?cs/es*100:0
    if (cs < 60 && $5 < 200000) next          # drop the long tail; keeps output small
    printf "%s    {\"pid\":%s,\"ppid\":%s,\"stat\":\"%s\",\"rss_kb\":%s,\"cpu_seconds\":%d,\"elapsed_seconds\":%d,\"sustained_pct\":%.2f,\"comm\":\"%s\",\"command\":\"%s\"}",
      (n++?",\n":""), $1,$2,esc($3),$5,cs,es,r,esc($9),esc(substr(cmd,1,240)) }'
echo ""
echo "  ],"

# ---- orphans (reparented to PID 1, excluding OS-owned paths) ----------------
echo "  \"orphans\": ["
ps -Ao ppid,pid,rss,time,etime,command 2>/dev/null | awk '$1==1' \
 | grep -vE '/(System|usr/libexec|usr/sbin|sbin|Library/Apple)/' \
 | awk '{cmd=""; for(i=6;i<=NF;i++) cmd=cmd (i>6?" ":"") $i
     gsub(/\\/,"\\\\",cmd); gsub(/"/,"\\\"",cmd)
     printf "%s    {\"pid\":%s,\"rss_kb\":%s,\"cpu_time\":\"%s\",\"elapsed\":\"%s\",\"command\":\"%s\"}",
       (n++?",\n":""), $2,$3,$4,$5,substr(cmd,1,240)}'
echo ""
echo "  ],"

# ---- listeners with peer counts: the strongest in-use signal ----------------
echo "  \"listeners\": ["
bounded 20 lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | tail -n +2 | awk '{print $2, $1, $9}' | sort -u \
 | while read -r lpid lcmd laddr; do
     peers=$(bounded 5 lsof -nP -p "$lpid" 2>/dev/null | grep -c ESTABLISHED)
     printf '%s    {"pid":%s,"command":"%s","addr":"%s","established":%s}' "${SEP:-}" "$lpid" "$lcmd" "$laddr" "${peers:-0}"
     SEP=$',\n'
   done
echo ""
echo "  ]"
echo "}"
} > "$OUT"

echo "$OUT"
