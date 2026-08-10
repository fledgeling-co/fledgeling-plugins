#!/usr/bin/env bash
# Deterministic reclaim for a tier. Defaults to DRY RUN.
#
#   reclaim.sh --tier 15m            what would happen (nothing is touched)
#   reclaim.sh --tier 15m --apply    do it
#
# Only the 15m and 1h bands are implemented here, because only those are
# deterministic enough to run unattended with no model. Everything from 12h up
# needs judgement (is this dev server still wanted, does this worktree hold
# work), so this script MEASURES those and writes a proposal the next
# interactive session reads. It never prompts: a prompt under launchd hangs
# forever holding the agent slot.
set -uo pipefail

TIER="15m"; APPLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --tier) TIER="${2:-15m}"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) shift ;;
  esac
done

STATE="$HOME/.claude/mac-doctor"
LEDGER="$STATE/ledger.jsonl"
PROTECTED="$STATE/protected"
mkdir -p "$STATE/findings" "$STATE/logs"
RUN_ID="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
freed_kb=0; actions=()

log() { printf '[%s %s] %s\n' "$RUN_ID" "$TIER" "$1"; }
act() { # act <label> <bytes_kb> <command...>
  local label="$1" kb="$2"; shift 2
  if [ "$APPLY" -eq 1 ]; then
    if "$@" >/dev/null 2>&1; then freed_kb=$((freed_kb+kb)); actions+=("$label"); log "reclaimed $label (~${kb}KB)"
    else log "FAILED $label"; fi
  else
    log "would reclaim $label (~${kb}KB): $*"
  fi
}
protected() { [ -f "$PROTECTED" ] || return 1; grep -qF -- "$1" "$PROTECTED" 2>/dev/null; }

# Only touch repos the user owns. A checkout of someone else's project is not
# ours to clean, however regenerable its build output looks -- and a stray
# `rm -rf` inside a third-party clone is indistinguishable from vandalism when
# they next pull. Owners come from ~/.claude/mac-doctor/owners (one per line),
# defaulting to "no remote at all" plus the ones configured here.
OWNERS_FILE="$STATE/owners"
owned_repo() {
  local repo="$1" url owner
  url=$(git -C "$repo" remote get-url origin 2>/dev/null) || return 0   # no remote: local, ours
  [ -z "$url" ] && return 0
  owner=$(printf '%s' "$url" | sed -E 's#^git@[^:]+:##; s#^https?://[^/]+/##; s#/.*$##')
  [ -f "$OWNERS_FILE" ] || return 1        # remote exists but no allowlist: refuse
  grep -qix -- "$owner" "$OWNERS_FILE"
}

# Walk up from a path to the repo root it belongs to.
repo_root() { git -C "$1" rev-parse --show-toplevel 2>/dev/null; }

free_before=$(df -k /System/Volumes/Data | tail -1 | awk '{print $4}')

# ---- 15m band ---------------------------------------------------------------
# Exited containers only. `exited`/`created` are states a running workload
# cannot be in, which is what makes this safe without judgement.
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  n=$(docker ps -aq --filter status=exited --filter status=created 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" -gt 0 ] && act "docker exited containers ($n)" 0 docker container prune -f
fi

# Automation temp dirs with no live owner. Age-gated so a running test's scratch
# directory is never removed mid-run.
for pat in "/tmp/playwright-"* "/tmp/.org.chromium."* "${TMPDIR:-/tmp}/claude-"*; do
  for p in $pat; do
    [ -e "$p" ] || continue
    protected "$p" && continue
    [ -n "$(find "$p" -maxdepth 0 -mtime +1 2>/dev/null)" ] || continue
    lsof -- "$p" >/dev/null 2>&1 && continue          # someone still has it open
    kb=$(du -sxk "$p" 2>/dev/null | awk '{print $1}')
    act "temp $p" "${kb:-0}" rm -rf -- "$p"
  done
done

# ---- 1h band ----------------------------------------------------------------
if [ "$TIER" != "15m" ]; then
  # Build output only, and only where a generator still exists -- "dist" is
  # regenerable because something can rebuild it, not because of its name.
  while IFS= read -r d; do
    repo=$(repo_root "$d") || repo=$(dirname "$d")
    [ -n "$repo" ] || repo=$(dirname "$d")
    protected "$d" && continue
    owned_repo "$repo" || { log "skip (not our repo) $d"; continue; }
    [ -f "$repo/package.json" ] || [ -f "$repo/Makefile" ] || [ -f "$repo/Cargo.toml" ] || continue
    [ -n "$(find "$d" -maxdepth 0 -mtime +7 2>/dev/null)" ] || continue
    lsof -a -d cwd -- "$repo" >/dev/null 2>&1 && continue   # a process is working here
    kb=$(du -sxk "$d" 2>/dev/null | awk '{print $1}')
    act "build output $d" "${kb:-0}" rm -rf -- "$d"
  done < <(find "${DEV_ROOT:-$HOME/Dev}" -maxdepth 3 \( -name dist -o -name .next -o -name .turbo -o -name .parcel-cache \) -type d -prune 2>/dev/null)
fi

# ---- 12h and beyond: measure and propose, never act -------------------------
if [ "$TIER" = "12h" ] || [ "$TIER" = "1d" ] || [ "$TIER" = "7d" ]; then
  prop="$STATE/findings/proposal-$TIER-$(date -u +%Y%m%dT%H%M%SZ).md"
  {
    echo "# mac-doctor $TIER proposal — $RUN_ID"
    echo
    echo "Generated headless, so nothing here has been applied. Run"
    echo "\`/mac-doctor $TIER\` in a session to review and act on it."
    echo
    df -h /System/Volumes/Data | tail -1 | awk '{print "Free: "$4" ("$5" used)"}'
    echo
    echo "## Candidates"
    command -v docker >/dev/null 2>&1 && docker system df 2>/dev/null | sed 's/^/    /'
  } > "$prop"
  log "wrote proposal $prop"
fi

free_after=$(df -k /System/Volumes/Data | tail -1 | awk '{print $4}')

# Ledger: record kept/skipped as carefully as reclaimed -- a target skipped
# thirty times while always idle is itself a finding, and only the record shows it.
if [ "$APPLY" -eq 1 ]; then
  # Serialising actions must not depend on grep's exit status. This script runs
  # under `set -o pipefail`, and a grep that filters every line exits 1, so the
  # old `|| echo '[]'` fallback fired even though python3 had already printed
  # `[]` -- emitting `[]\n[]` and splitting the record across two lines. It only
  # went wrong on runs that reclaimed nothing, which is most of them, so the
  # corruption hid in the common case and took the ledger with it. Recurrence
  # detection is the whole reason this file exists, and it needs valid JSONL.
  if [ "${#actions[@]}" -gt 0 ]; then
    actions_json=$(printf '%s\n' "${actions[@]}" \
      | python3 -c 'import sys,json; print(json.dumps([l.rstrip("\n") for l in sys.stdin if l.strip()]))')
  else
    actions_json='[]'
  fi
  printf '{"run_id":"%s","tier":"%s","mode":"apply","free_kb_before":%s,"free_kb_after":%s,"freed_kb_est":%s,"actions":%s}\n' \
    "$RUN_ID" "$TIER" "$free_before" "$free_after" "$freed_kb" "$actions_json" \
    >> "$LEDGER"
fi

log "done (mode=$([ "$APPLY" -eq 1 ] && echo apply || echo dry-run), free ${free_before}KB -> ${free_after}KB)"
