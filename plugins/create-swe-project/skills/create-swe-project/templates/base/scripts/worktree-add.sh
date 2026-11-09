#!/usr/bin/env bash
# Create a worktree that is actually gated (BP §23). A bare `git worktree add`
# leaves no node_modules and no .husky/_, so typecheck fails and the pre-push
# gate silently does nothing. This runs a real pnpm install in the new tree;
# never symlink node_modules into a worktree (Turbopack's next build panics on it).
# Usage: scripts/worktree-add.sh <path> <new-branch> [<base>]   (base defaults to main)
set -euo pipefail
[ $# -ge 2 ] || { echo "usage: scripts/worktree-add.sh <path> <new-branch> [<base>]" >&2; exit 2; }
WT="$1" BRANCH="$2" BASE="${3:-main}"
git worktree add -b "$BRANCH" "$WT" "$BASE"
cd "$WT"
pnpm install --frozen-lockfile
[ -d .husky/_ ] || { echo "husky did not install in $WT; the pre-push gate would not run" >&2; exit 1; }
echo "worktree ready: $WT on $BRANCH (gate installed)"
