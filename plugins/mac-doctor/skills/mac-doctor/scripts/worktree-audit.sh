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

# Decide whether a DEREGISTERED worktree can be removed without losing anything.
#
# `git status` cannot run in one (its admin directory is gone), which is why an
# earlier version of this script gave up and called them all unverifiable. That
# was over-conservative: the question is not "what does git say", it is "does
# this directory hold any content that exists nowhere else". That is answerable
# without the admin directory, by hashing each file and asking the parent repo's
# object database whether it already has that blob.
#
# Commits need no check at all. They live in the parent repo, so deleting a
# worktree directory cannot destroy history even on an unmerged branch -- the
# branch ref and its objects stay behind.
#
# Returns 0 = every file already in the object DB (safe)
#         1 = holds content found nowhere else (keep)
#         2 = could not decide (too large, or a notable ignored file present)
content_all_reachable() {
  local repo="$1" wt="$2" n=0 h
  # Files ignored by convention are regenerable and not worth hashing. Dotenv
  # files are the exception: gitignored, never in the object DB, and the one
  # thing in a worktree a person would actually miss.
  if find "$wt" -maxdepth 2 -type f \( -name '.env' -o -name '.env.*' \) 2>/dev/null | grep -q .; then
    return 2
  fi
  while IFS= read -r f; do
    n=$((n + 1))
    [ "$n" -gt "$MAX_VERIFY_FILES" ] && return 2
    h=$(git -C "$repo" hash-object "$f" 2>/dev/null) || return 2
    git -C "$repo" cat-file -e "$h" 2>/dev/null || return 1
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
