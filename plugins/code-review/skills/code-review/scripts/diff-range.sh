#!/usr/bin/env bash
# diff-range.sh — resolve the range under review and measure it.
#
# Deterministic replacement for the ref-guessing every review otherwise repeats by hand.
# Prints KEY=VALUE lines on stdout; diagnostics go to stderr.
#
#   ./diff-range.sh                  # auto-resolve the base
#   ./diff-range.sh --base main      # pin the base
#   ./diff-range.sh --outgoing       # unpushed commits only (prepush mode)
#   ./diff-range.sh --files          # also print CHANGED_FILES, one path per line
#
# Exit 0 with CHANGED=0 when there is nothing to review — that is an answer, not an error.
# Exit 2 only when the working directory is not a git repository.

set -uo pipefail

BASE=""
WANT_FILES=0
OUTGOING=0

while [ $# -gt 0 ]; do
  case "$1" in
    --base) BASE="${2:-}"; shift 2 ;;
    --files) WANT_FILES=1; shift ;;
    --outgoing) OUTGOING=1; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "diff-range.sh: unknown argument: $1" >&2; exit 2 ;;
  esac
done

git rev-parse --git-dir >/dev/null 2>&1 || { echo "diff-range.sh: not a git repository" >&2; exit 2; }

default_branch() {
  git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' && return 0
  for b in main master trunk develop; do
    git rev-parse --verify --quiet "refs/heads/$b" >/dev/null && { echo "$b"; return 0; }
  done
  return 1
}

RESOLVED_BY="explicit"
if [ -z "$BASE" ]; then
  if [ "$OUTGOING" -eq 1 ] && git rev-parse --verify --quiet '@{push}' >/dev/null 2>&1; then
    BASE='@{push}'; RESOLVED_BY="@{push}"
  elif git rev-parse --verify --quiet '@{upstream}' >/dev/null 2>&1; then
    BASE='@{upstream}'; RESOLVED_BY="@{upstream}"
  else
    db="$(default_branch || true)"
    if [ -n "$db" ] && [ "$(git rev-parse --abbrev-ref HEAD)" != "$db" ]; then
      BASE="$db"; RESOLVED_BY="default-branch"
    elif git rev-parse --verify --quiet 'HEAD~1' >/dev/null 2>&1; then
      BASE='HEAD~1'; RESOLVED_BY="HEAD~1 (fallback — confirm this is the intended range)"
    else
      BASE=''; RESOLVED_BY="none — repository has a single commit"
    fi
  fi
fi

HEAD_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

if [ -n "$BASE" ]; then
  # Two-dot for the outgoing set (what these commits changed); three-dot for a review range
  # (what this branch changed since it diverged), which is what a reviewer means by "the diff".
  if [ "$OUTGOING" -eq 1 ]; then RANGE="$BASE..HEAD"; else RANGE="$BASE...HEAD"; fi
  RANGE_FILES="$(git diff --name-only "$RANGE" 2>/dev/null)"
  SHORTSTAT="$(git diff --shortstat "$RANGE" 2>/dev/null)"
  COMMITS="$(git rev-list --count "$BASE..HEAD" 2>/dev/null || echo 0)"
else
  RANGE=""; RANGE_FILES=""; SHORTSTAT=""; COMMITS=0
fi

WT_FILES="$(git diff --name-only HEAD 2>/dev/null)"
WT_SHORTSTAT="$(git diff --shortstat HEAD 2>/dev/null)"

parse_stat() { echo "${1:-}" | grep -oE '[0-9]+ (insertion|deletion)' | awk '{s+=$1} END {print s+0}'; }
RANGE_LOC="$(parse_stat "$SHORTSTAT")"
WT_LOC="$(parse_stat "$WT_SHORTSTAT")"

# The unit under review is the union: a review usually runs before the commit, and reviewing
# only one of the two misses half the work. --outgoing is the exception; it gates commits only.
if [ "$OUTGOING" -eq 1 ]; then
  ALL_FILES="$RANGE_FILES"; LOC_DELTA="$RANGE_LOC"
else
  ALL_FILES="$(printf '%s\n%s\n' "$RANGE_FILES" "$WT_FILES" | grep -v '^$' | sort -u)"
  LOC_DELTA=$((RANGE_LOC + WT_LOC))
fi
FILE_COUNT="$(printf '%s\n' "$ALL_FILES" | grep -cv '^$' || true)"

echo "BRANCH=$BRANCH"
echo "HEAD=$HEAD_SHA"
echo "BASE=${BASE:-none}"
echo "BASE_RESOLVED_BY=$RESOLVED_BY"
echo "RANGE=${RANGE:-none}"
echo "COMMITS_AHEAD=$COMMITS"
echo "FILE_COUNT=$FILE_COUNT"
echo "LOC_DELTA=$LOC_DELTA"
echo "WORKTREE_DIRTY=$([ -n "$WT_FILES" ] && echo yes || echo no)"
echo "WORKTREE_INCLUDED=$([ "$OUTGOING" -eq 1 ] && echo no || echo yes)"
echo "CHANGED=$([ "$FILE_COUNT" -gt 0 ] && echo 1 || echo 0)"

# Shard thresholds, so the caller does not re-derive them from the depth table.
echo "SHARD_STANDARD=$([ "$FILE_COUNT" -ge 30 ] || [ "$LOC_DELTA" -ge 2000 ] && echo yes || echo no)"
echo "SHARD_DEEP=$([ "$FILE_COUNT" -ge 15 ] || [ "$LOC_DELTA" -ge 1000 ] && echo yes || echo no)"
echo "FLEET_SIZE=$(awk -v l="$LOC_DELTA" 'BEGIN{n=int((l+149)/150); if(n<2)n=2; if(n>8)n=8; print n}')"
echo "FINDING_FLOOR=$(awk -v f="$FILE_COUNT" 'BEGIN{print (f<4)?f:4}')"

if [ "$WANT_FILES" -eq 1 ] && [ "$FILE_COUNT" -gt 0 ]; then
  echo "CHANGED_FILES<<EOF"
  printf '%s\n' "$ALL_FILES"
  echo "EOF"
fi
