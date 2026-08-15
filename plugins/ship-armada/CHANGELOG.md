# Changelog

## 2.0.1 - 2026-08-15

- Daemon mode arms through the `better-loop` skill rather than the built-in `/loop` (session crons expire after seven days and cannot carry restricted skills).

## 2.0.0 - 2026-08-15

- `scripts/check_completion.sh` mechanises the completion rule: the ledger is cross-checked against git reality (open rows, unmerged ai/* branches, leftover worktrees) before a project is ticked off. `Done` additionally requires the cross-family verification verdict.
- The repo-ownership allow-list moves from skill text to portfolio CLAUDE.md configuration.
- Route writes briefs through the shipyard `intake` skill (trawl ideation, proposed-by-ai marking); open technical calls in Plan go through the second-opinion lanes before reaching the user.
- Dispatch targets ship-fleet and ship-feature in this marketplace; the sibling-marketplace dependency is gone.

## 1.2.1 - 2026-08

- Completion rule added after a fleet whose runners died reported `completed`.

## 1.2.0 and earlier

Survey, Plan, Route, Dispatch and Daemon modes over ~/Dev/ARMADA.md; see git history.
