#!/usr/bin/env bash
# Remove worktrees whose work is fully integrated (BP §23). A worktree is removed
# only when its tree is clean AND its HEAD is an ancestor of the integration
# branch, so nothing is lost: git keeps the branch and its history. Dry run by
# default; --apply acts. Run from the main checkout.
# Usage: scripts/prune-merged-worktrees.sh [--apply] [--base origin/main]
set -euo pipefail
APPLY=0 BASE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1; shift;;
    --base) BASE="$2"; shift 2;;
    *) echo "usage: scripts/prune-merged-worktrees.sh [--apply] [--base <ref>]" >&2; exit 2;;
  esac
done
if [ -z "$BASE" ]; then
  if git rev-parse -q --verify origin/main >/dev/null; then BASE=origin/main; else BASE=main; fi
fi
MAIN="$(git rev-parse --show-toplevel)"
git worktree list --porcelain | awk '/^worktree /{print substr($0, 10)}' | while read -r wt; do
  [ "$wt" = "$MAIN" ] && continue
  if [ ! -d "$wt" ]; then echo "stale registration (directory gone): $wt — run: git worktree prune"; continue; fi
  if [ -n "$(git -C "$wt" status --porcelain 2>/dev/null)" ]; then echo "keep (uncommitted changes): $wt"; continue; fi
  head="$(git -C "$wt" rev-parse HEAD)"
  if ! git merge-base --is-ancestor "$head" "$BASE"; then echo "keep (not merged into $BASE): $wt"; continue; fi
  if [ "$APPLY" = 1 ]; then
    (cd "$wt" && pnpm turbo daemon stop >/dev/null 2>&1 || true)
    git worktree remove "$wt"
    echo "removed: $wt"
  else
    echo "would remove (clean, merged into $BASE): $wt"
  fi
done
[ "$APPLY" = 1 ] || echo "dry run; pass --apply to remove"
