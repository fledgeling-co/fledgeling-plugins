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

# Canonicalise before comparing paths. git reports the resolved path
# (/private/tmp/...), a shell glob yields the symlinked one (/tmp/...), and a
# string compare between them silently fails. That inverted this whole audit on
# first run: the one registered worktree was reported unregistered and therefore
# reclaimable, and the deregistered ones were reported unreadable. Under ~/Dev
# there is no symlink so it looked correct, which is the worst way for a bug
# like this to behave.
canon() { ( cd "$1" 2>/dev/null && pwd -P ) || printf '%s' "$1"; }

MAX_VERIFY_FILES="${MAX_VERIFY_FILES:-4000}"
REACHABLE_TIMEOUT="${REACHABLE_TIMEOUT:-60}"

# Blobs reachable from a ref that will still exist after the worktree goes.
# Built once per repo and cached, because `rev-list --objects --all` is a single
# history walk where `cat-file -e` per file is N lookups.
#
# Presence is weaker than reachability, and the difference is not academic: a
# blob can sit in the object database unreferenced, having come from an aborted
# commit or a discarded branch, and `git gc` will prune it. Content whose only
# witness is the directory being deleted is not preserved by the fact that git
# currently happens to have a copy.
_reach_repo=""; _reach_file=""
reachable_blobs() {
  local repo="$1"
  [ "$repo" = "$_reach_repo" ] && return 0
  _reach_repo="$repo"
  _reach_file=$(mktemp -t mdreach-XXXXXX)
  bounded "$REACHABLE_TIMEOUT" git -C "$repo" rev-list --objects --all 2>/dev/null \
    | awk '{print $1}' | sort -u > "$_reach_file" || :
  [ -s "$_reach_file" ] || return 1     # walk failed or was bounded out
  return 0
}

# Decide whether a DEREGISTERED worktree can be removed without losing anything.
#
# `git status` cannot run in one (its admin directory is gone), which is why an
# earlier version gave up and called them all unverifiable. That was
# over-conservative: the question is not "what does git say", it is "does this
# directory hold content that exists nowhere else", and that is answerable by
# hashing each file and asking whether the blob is reachable from a surviving
# ref.
#
# Commits need no separate check. They live in the parent repo, so deleting a
# worktree directory cannot destroy history even on an unmerged branch: the
# branch ref and its objects stay behind, and `git checkout <branch>` restores
# the tree. Verified on the fixture.
#
# Returns 0 = every file reachable from a surviving ref (safe)
#         1 = holds content reachable from nowhere else (keep)
#         2 = could not decide (too large, dotenv present, or the walk failed)
content_all_reachable() {
  local repo="$1" wt="$2" n=0 h
  if find "$wt" -maxdepth 2 -type f \( -name '.env' -o -name '.env.*' \) 2>/dev/null | grep -q .; then
    return 2
  fi
  reachable_blobs "$repo" || return 2
  while IFS= read -r f; do
    n=$((n + 1))
    [ "$n" -gt "$MAX_VERIFY_FILES" ] && return 2
    h=$(git -C "$repo" hash-object "$f" 2>/dev/null) || return 2
    grep -qxF "$h" "$_reach_file" || return 1
  done < <(find "$wt" -type f \
             -not -path '*/.git/*' -not -name '.git' \
             -not -path '*/node_modules/*' -not -path '*/dist/*' -not -path '*/build/*' \
             -not -path '*/.next/*' -not -path '*/.turbo/*' -not -path '*/target/*' \
             -not -path '*/.venv/*' -not -path '*/__pycache__/*' 2>/dev/null)
  return 0
}

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
    wtc=$(canon "$wt")

    is_registered=false
    while IFS= read -r r; do
      [ -z "$r" ] && continue
      [ "$(canon "$r")" = "$wtc" ] && { is_registered=true; break; }
    done <<< "$registered"

    # The decisive asymmetry, and the opposite of what it looks like:
    #
    #   REGISTERED   -> git can answer "clean?" and "merged?", so the worktree
    #                   can be judged. A registered worktree that is clean and
    #                   fully merged is a finished session, and reclaimable.
    #   UNREGISTERED -> the .git link points at an admin directory that no
    #                   longer exists, so `status` and `log` both fail and
    #                   `worktree repair` cannot re-attach it. Nothing can be
    #                   proven about it, so nothing may be done to it.
    #
    # "Unregistered, clean and merged" is therefore not a stricter gate, it is
    # an unsatisfiable one: unregistered is precisely the state in which clean
    # and merged are unknowable.
    if [ "$is_registered" != true ]; then
      # git cannot speak for this one, so ask the object database instead.
      content_all_reachable "$repo" "$wt"; rc=$?
      dirty="unknown"; unmerged="n/a"
      case $rc in
        0) verdict="reclaimable"
           reason="deregistered, but every file already exists in the object database, and commits live in the parent repo" ;;
        1) verdict="keep"
           reason="deregistered and holds file content found nowhere in the object database" ;;
        *) verdict="unverifiable"
           reason="deregistered, and too large or holds a dotenv file, so content cannot be cleared" ;;
      esac
    elif ! git -C "$wt" rev-parse --git-dir >/dev/null 2>&1; then
      verdict="unverifiable"; dirty="unknown"; unmerged="unknown"
      reason="registered but unreadable as a git worktree"
    else
      dirty=$(git -C "$wt" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
      unmerged=$(git -C "$wt" log --oneline "$db..HEAD" 2>/dev/null | wc -l | tr -d ' ')
      in_use=""
      lsof -a -d cwd -- "$wt" >/dev/null 2>&1 && in_use="a process is working in it"
      if [ -n "$in_use" ]; then
        verdict="keep"; reason="$in_use"
      elif [ "${dirty:-1}" -gt 0 ]; then
        verdict="keep"; reason="$dirty uncommitted change(s)"
      elif [ "${unmerged:-1}" -gt 0 ]; then
        verdict="keep"; reason="$unmerged commit(s) not in $db"
      else
        verdict="reclaimable"; reason="registered, clean, fully merged into $db, nothing working in it"
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
