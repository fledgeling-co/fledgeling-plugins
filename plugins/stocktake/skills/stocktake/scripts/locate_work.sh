#!/usr/bin/env bash
# Where does a card's work actually live?
#
# A card sitting in a review column whose work is on a branch nobody merged is a
# DELIVERY failure, not an implementation one, and the two need different fixes.
# Four outcomes: merged / unmerged-branch / unpushed / absent.
#
#   locate_work.sh WEB-1234 [integration-branch] [remote]
set -uo pipefail

KEY="${1:?usage: locate_work.sh <card-key> [integration-branch] [remote]}"
BRANCH="${2:-$(git symbolic-ref --quiet --short HEAD 2>/dev/null || echo main)}"
REMOTE="${3:-origin}"

echo "card:        $KEY"
echo "integration: $BRANCH"

# Commits naming the key on the integration branch.
ON_BRANCH=$(git log "$BRANCH" --oneline --grep="$KEY" 2>/dev/null | head -20)
N_ON_BRANCH=$(printf '%s' "$ON_BRANCH" | grep -c . || true)

# Commits naming the key anywhere, including branches never merged.
ALL=$(git log --all --oneline --grep="$KEY" 2>/dev/null | head -40)
N_ALL=$(printf '%s' "$ALL" | grep -c . || true)

# Live worktrees whose path names the key.
WT=$(git worktree list 2>/dev/null | grep -i -- "$KEY" || true)

# Is the integration branch's copy actually pushed?
UNPUSHED=""
if git rev-parse --verify --quiet "$REMOTE/$BRANCH" >/dev/null 2>&1; then
  UNPUSHED=$(git log "$REMOTE/$BRANCH..$BRANCH" --oneline --grep="$KEY" 2>/dev/null | head -20)
fi
N_UNPUSHED=$(printf '%s' "$UNPUSHED" | grep -c . || true)

echo "commits on $BRANCH: $N_ON_BRANCH"
[ "$N_ON_BRANCH" -gt 0 ] && printf '%s\n' "$ON_BRANCH" | sed 's/^/  /'
echo "commits anywhere:   $N_ALL"

if [ -n "$WT" ]; then
  echo "worktrees naming the key:"
  printf '%s\n' "$WT" | sed 's/^/  /'
fi

# The verdict, in the vocabulary board_ledger.py accepts for --work-at.
if [ "$N_ON_BRANCH" -eq 0 ] && [ "$N_ALL" -eq 0 ] && [ -z "$WT" ]; then
  VERDICT=absent
elif [ "$N_ON_BRANCH" -eq 0 ] && [ -n "$WT" ]; then
  VERDICT=worktree
elif [ "$N_ON_BRANCH" -eq 0 ] && [ "$N_ALL" -gt 0 ]; then
  VERDICT=unmerged-branch
elif [ "$N_UNPUSHED" -gt 0 ]; then
  VERDICT=unpushed
else
  VERDICT=merged
fi

echo "work-at: $VERDICT"
# A key that appears nowhere may simply not be referenced in commit messages.
# Say so rather than letting `absent` read as "never built".
[ "$VERDICT" = absent ] && echo "note: no commit message names $KEY — the work may exist under another reference; check the card's comments for a sha before recording absent"
exit 0
