# Running a full sweep

A whole board is hours of serial verification and will outlive the session. Two things
follow: the state lives in a file rather than in the conversation, and the run is armed
with something that judges completion by exit code rather than by narration.

## The ledger is the worklist

`scripts/board_ledger.py` holds one row per card: key, column at intake, requirement
count, where the work was found, the verdict, the lane that graded it, and the column it
landed in. A resumed session reads the ledger and continues.

Write the row when the card is finished, not when it is started. A half-finished row is
indistinguishable from a finished one three hours later.

## Arm it with better-goal

The gate set, each judged on exit code — `scripts/gates.py <gate> <ledger-dir>`, or
`all` to run them in order:

| Gate | Question |
|---|---|
| `covered` | Does every card in scope have a ledger row? |
| `evidence` | Does every row carry what backs it — a sha, a lane, a verdict word, or a question? |
| `no-inconclusive-unreported` | Is every inconclusive row's reason recorded? |
| `verified-gate` | If any card was promoted past Done, do all eight preconditions hold? |
| `briefs-written` | Does every card with work remaining have a brief in features-to-triage? |
| `suite` | Does the project's own test gate still pass? (yours, not shipped here) |

## Two traps that make a long run report success while doing nothing

**A gate that compares a value with itself.** The same defect the skill hunts for in
product tests appears in the gates that judge the skill. Compare against a literal.

**A gate whose scope includes another session's work.** In a shared checkout, a
whole-tree cleanliness check or a repo-wide suite fails for edits this run never made,
and blocks it on work it cannot fix. Scope every gate to what the run is answerable
for: the shas in its own ledger rows, plus its own uncommitted files. Where a foreign
failure must be tolerated, tolerate it **by name with its reason printed every run**,
never silently.

## Cost, stated up front

Serial out-of-family verification runs roughly 10–25 minutes per card and does not
parallelise where the lane refuses concurrent instances. A 44-card board is most of a
working day of lane time. Say this before starting a full sweep, because the reader may
want a column rather than a board — and a run that is abandoned halfway is worse than a
scoped one that finished.
