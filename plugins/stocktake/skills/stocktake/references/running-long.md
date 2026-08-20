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
| `inconclusive-reported` | Is every inconclusive row's reason recorded, in 30 characters or more? |
| `ungraded-reported` | Does every card the method never ran on say which of steps 1-6 were skipped? |
| `briefs-written` | Does every card with work remaining have a brief that names it and serves at most 3 cards? |
| `dispatched` | Was work actually handed to `ship-fleet` — at least one card, with per-card attributed deferrals for the rest? |
| `classified` | Does every graded card name the warrant defect class it was graded under? |
| `banked` | Did every terminal verdict reach `.warrant/ledger.jsonl` with an evidence digest? |
| `verified-gate` | If any card was promoted past Done, do all eight preconditions hold? |
| `suite` | Does the project's own test gate still pass? (yours, not shipped here) |

`gates.py selftest` runs 38 cases over fixture ledgers and exits 0 when all pass. Each case
was checked against a reverted gate, so a case that passes both ways is not in the set.

`dispatched` is the gate that separates a finished run from a finished audit, and it is the
one to reach for when a sweep reports success and the board has not moved. A run that handed
108 briefs to `ship-fleet` and a run that handed over nothing produce the same ledger without
it. It refuses a run that dispatched nothing, a reason repeated across more than three cards, and
a deferral naming nobody who decided it. The first version accepted any recorded deferral as
equal to a dispatch — which let the author of a sweep excuse itself, and one run deferred all
61 of its needs-work cards with a single invented sentence and passed. To declare an audit-only
run, skip this gate visibly rather than satisfying it with wording.

`classified` and `banked` are the same failure aimed at the warrant rather than the fleet.
`warrant_column.py` reads the warrant and returns a column; nothing appends the row that
the tier-3 entry condition counts. So a sweep can grade a whole board, consult the warrant
correctly on every card, and leave the ladder exactly where it found it. `banked` is inert
in a checkout with no `.warrant/`, which is the honest answer where warrant is not installed.

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
