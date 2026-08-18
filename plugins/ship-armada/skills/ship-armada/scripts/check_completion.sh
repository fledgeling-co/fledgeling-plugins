#!/usr/bin/env bash
# check_completion.sh — the armada's completion rule, mechanised.
#
# "A project is complete when its ledger says so, never when its dispatch
# returns." A fleet whose runners died reports `completed` (workflow agent()
# returns null on terminal API errors with zero retries and the run finishes
# clean), so before ticking a project off, this script cross-checks its
# ORCHESTRATOR.md ledger against git reality:
#   - every ledger row must read merged/Done or parked-with-reason
#   - every row claiming merged must have its branch actually reachable from
#     the integration branch (or deleted after a real merge)
#   - leftover ai/* branches and .worktrees/ entries are reported
#
# Usage: check_completion.sh <repo-path>
# Exit codes: 0 = ledger and git agree the work is done
#             1 = open/unproven items (printed) — do NOT tick the project off
#             2 = nothing to verify against: no ORCHESTRATOR.md ledger, or the
#                 path given is not a directory
#
# There is no code 3+, and there is deliberately no path that exits without
# printing why. Both were true by accident until 2026-08-19: in a directory with
# no git repo this exited 128 in silence, because errexit killed it on a failing
# `git remote show` before the NO-INT branch could report.
set -euo pipefail

repo="${1:?usage: check_completion.sh <repo-path>}"
# Without this guard a bad path dies inside `cd` under errexit, so the caller
# gets a bash line-number error instead of one of the documented codes.
cd "$repo" 2>/dev/null || { echo "NO-PATH: $repo is not a directory"; exit 2; }

orch="ORCHESTRATOR.md"
[[ -f "$orch" ]] || { echo "NO-LEDGER: $repo has no ORCHESTRATOR.md"; exit 2; }

# `|| true` because this whole line is allowed to fail. Under `set -euo pipefail`
# a non-git directory makes `git remote show origin` exit 128, pipefail
# propagates it, errexit kills the script, and the NO-INT branch below becomes
# unreachable: the caller gets a bare 128 with nothing on stdout or stderr,
# against documented codes of 0, 1 and 2 only. Failing closed was right; failing
# silently was not.
int_branch=$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p') || true
# `--quiet` hides the ref, not a "not a git repository" fatal, so this needs its
# own redirect or the NO-INT diagnostic arrives behind a raw git error.
git show-ref --verify --quiet refs/remotes/origin/staging 2>/dev/null && int_branch="staging"
[[ -n "$int_branch" ]] || { echo "NO-INT: cannot determine integration branch"; exit 1; }

fail=0

# 1. Ledger rows that are neither done nor parked
open_rows=$(grep -E '^\|' "$orch" | grep -viE 'merged|done|parked|^\| *id|^\| *-' || true)
if [[ -n "$open_rows" ]]; then
  echo "OPEN-ROWS (ledger rows not merged/Done/parked):"
  echo "$open_rows"
  fail=1
fi

# 2. ai/* branches with commits not reachable from the integration branch
git fetch origin --quiet 2>/dev/null || true
for b in $(git branch --list 'ai/*' --format='%(refname:short)'); do
  if [[ -n "$(git log "origin/$int_branch..$b" --oneline 2>/dev/null | head -1)" ]]; then
    echo "UNMERGED-BRANCH: $b has commits not on origin/$int_branch"
    fail=1
  fi
done

# 3. Leftover worktrees
wt=$(git worktree list --porcelain | grep -c '^worktree .*\.worktrees/' || true)
if [[ "$wt" -gt 0 ]]; then
  echo "LEFTOVER-WORKTREES: $wt entries under .worktrees/ (resume or clean before ticking off)"
  fail=1
fi

if [[ "$fail" -eq 0 ]]; then
  echo "COMPLETE: ledger and git agree — every item merged/parked, no unmerged ai/* work"
fi
exit "$fail"
