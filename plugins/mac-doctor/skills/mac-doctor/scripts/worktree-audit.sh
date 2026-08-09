#!/usr/bin/env bash
# Audit git worktrees and decide, per worktree, whether it is provably abandoned.
#
# Three gates, all of which must pass before a worktree may be removed:
#   1. unregistered  -- absent from `git worktree list`
#   2. clean         -- `git status --porcelain` is empty
#   3. merged        -- no commits absent from the default branch
#
# Unregistered ALONE is not abandonment. `git worktree prune` deregisters
# directories without deleting them, which is exactly how a machine ends up with
# worktrees git denies exist while they still hold unpushed work.
#
# Read-only. Prints JSON, removes nothing. Reclaim is the caller's decision.
set -uo pipefail

ROOT="${1:-$HOME/Dev}"
SIZE_SAMPLE="${SIZE_SAMPLE:-5}"   # worktrees to actually du; rest estimated
DU_TIMEOUT="${DU_TIMEOUT:-20}"

# `timeout` does NOT exist on stock macOS -- it ships with GNU coreutils as
# `gtimeout`, if at all. This matters more than it looks: `timeout 5 git ...`
# on a clean Mac is "command not found", which produces EMPTY STDOUT and exit 0
# through a pipe. A caller doing `timeout 5 git worktree list | wc -l` gets 0
# and reads it as "no worktrees registered" rather than "the command never ran".
# That exact mistake, made while gathering evidence for this skill, reported 100
# live registered worktrees as abandoned. Never let a bounding wrapper fail open.
_TIMEOUT_BIN=""
for c in timeout gtimeout; do
  command -v "$c" >/dev/null 2>&1 && { _TIMEOUT_BIN="$c"; break; }
done

bounded() {  # bounded <seconds> <command...>; returns 124 on timeout, like GNU
  local secs="$1"; shift
  if [ -n "$_TIMEOUT_BIN" ]; then "$_TIMEOUT_BIN" "$secs" "$@"; return $?; fi
  "$@" &
  local pid=$! rc=0
  ( sleep "$secs"; kill -TERM "$pid" 2>/dev/null ) >/dev/null 2>&1 &
  local watcher=$!
  wait "$pid" 2>/dev/null || rc=124
  kill "$watcher" 2>/dev/null
  return $rc
}

json_escape() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }

default_branch() {
  local repo="$1" b
  b=$(git -C "$repo" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null) && {
    printf '%s' "${b#origin/}"; return; }
  for c in main master develop; do
    git -C "$repo" show-ref --verify --quiet "refs/heads/$c" && { printf '%s' "$c"; return; }
  done
  git -C "$repo" symbolic-ref --quiet --short HEAD 2>/dev/null || printf 'HEAD'
}

sampled=0
echo "{"
echo "  \"collected_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
echo "  \"root\": \"$(json_escape "$ROOT")\","
echo "  \"worktrees\": ["

first=1
# Both conventions: Claude Code's EnterWorktree uses .claude/worktrees, while
# hand-made and skill-made worktrees commonly sit in .worktrees.
for wtroot in "$ROOT"/*/.claude/worktrees "$ROOT"/*/.worktrees; do
  [ -d "$wtroot" ] || continue
  case "$wtroot" in
    */.claude/worktrees) repo=$(dirname "$(dirname "$wtroot")") ;;
    */.worktrees)        repo=$(dirname "$wtroot") ;;
  esac
  git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || continue

  db=$(default_branch "$repo")
  registered=$(git -C "$repo" worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2}')

  for wt in "$wtroot"/*; do
    [ -d "$wt" ] || continue

    is_registered=false
    while IFS= read -r r; do
      [ "$r" = "$wt" ] && { is_registered=true; break; }
    done <<< "$registered"

    # A worktree whose .git link is broken cannot be interrogated. Report it as
    # indeterminate rather than clean -- "git can't read it" is not "it's empty".
    if ! git -C "$wt" rev-parse --git-dir >/dev/null 2>&1; then
      verdict="indeterminate"; dirty="unknown"; unmerged="unknown"; reason="not a readable git worktree"
    else
      dirty=$(git -C "$wt" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
      unmerged=$(git -C "$wt" log --oneline "$db..HEAD" 2>/dev/null | wc -l | tr -d ' ')
      if [ "$is_registered" = true ]; then
        verdict="keep"; reason="registered with git; may be an active session"
      elif [ "${dirty:-1}" -gt 0 ]; then
        verdict="keep"; reason="$dirty uncommitted change(s)"
      elif [ "${unmerged:-1}" -gt 0 ]; then
        verdict="keep"; reason="$unmerged commit(s) not in $db"
      else
        verdict="reclaimable"; reason="unregistered, clean, fully merged into $db"
      fi
    fi

    # Sizing is sampled: du across a full worktree set has been measured past
    # six minutes, and a maintenance tool must not cost that to decide anything.
    size_kb=null; size_kind="not_measured"
    if [ "$sampled" -lt "$SIZE_SAMPLE" ]; then
      s=$(bounded "$DU_TIMEOUT" du -sxk "$wt" 2>/dev/null | awk '{print $1}')
      if [ -n "${s:-}" ]; then size_kb=$s; size_kind="measured"; sampled=$((sampled+1));
      else size_kind="timed_out"; fi
    fi

    [ $first -eq 1 ] || echo ","
    first=0
    printf '    {"repo":"%s","path":"%s","branch_base":"%s","registered":%s,' \
      "$(json_escape "$(basename "$repo")")" "$(json_escape "$wt")" "$(json_escape "$db")" "$is_registered"
    printf '"uncommitted":"%s","unmerged":"%s","size_kb":%s,"size_kind":"%s",' \
      "$dirty" "$unmerged" "$size_kb" "$size_kind"
    printf '"verdict":"%s","reason":"%s"}' "$verdict" "$(json_escape "$reason")"
  done
done
echo ""
echo "  ]"
echo "}"
