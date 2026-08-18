# Evals — stocktake 0.1.0

## No comparative evaluation has been run

**There is no A/B result in this document, because none was produced.** The skill has
not been run against a no-skill baseline, no blind judge panel has scored its output,
and no win/loss table exists. Any badge or claim implying otherwise would be invented.

This matters more for this skill than most, because the thing it exists to catch is
exactly this: a report that reads as finished while the check behind it never ran.

What follows is what *was* verified, what was substituted, and the three tasks that
would settle the open question.

## What was verified, mechanically

Each bundled script was run and each gate was **red-armed** — deliberately given input
it should reject, to confirm it can fail rather than merely pass.

| Check | Given | Result |
|---|---|---|
| `board_ledger.py` refuses a `done` row with no judge or commit | `--verdict done` alone | refused |
| …refuses a `needs-info` row with no question | `--verdict needs-info` | refused |
| …refuses an `inconclusive` row with no reason | `--verdict inconclusive` | refused |
| …refuses a `needs-work` row with no brief | `--verdict needs-work` | refused |
| `gates.py covered` | a card with no verdict | exit 1 |
| `gates.py evidence` | a row that never says where the work lives | exit 1 |
| `gates.py briefs-written` | a brief path that is not on disk | exit 1 |
| `gates.py inconclusive-reported` | a reason under 30 characters | exit 1 |
| `gates.py verified-gate` | a card promoted with no preconditions | exit 1 |
| `check_verified_gate.py` with no config | — | exit 1, names all eight |
| …with the template, nothing asserted | — | exit 1 |
| …with one precondition asserted but no evidence | — | exit 1 |
| …with all eight held and evidenced for a named class | — | exit 0 |
| `locate_work.sh` against a real repository | a card key with five commits | reported `merged` |
| `verify_queue.sh` | a missing packet | `NO-PACKET`, did not proceed |
| …an empty lane output | — | `NO-VERDICT`, not treated as a pass |

Five gates, five refusals. Four exit paths on the Verified gate, all four correct.

## What was substituted, and by whom

**The research panel was neither run nor reused.** The originating project's
`status-check.md` describes a completed four-family panel on the adjacent question —
whether an automated verifier can replace a human acceptance step — but its report
files were not present on disk and could not be read. No replacement panel was bought,
because spending is the reader's decision and it was not asked for.

So the evidence base is that document's own primary-source-verified findings, cited in
`references/evidence.md` with each claim's provenance marked. The load-bearing ones —
the panel-independence result, the concurrent-read result, the regulatory constraints
on signatures — are verified at primary-source level there. **The gap: no independent
survey of board-triage practice specifically informs this skill.** Its process rules
come from measured practice in one codebase, not from literature.

**The discovery interview was not skipped.** Three decisions were put to the reader
before anything was written — how much of a board one run covers, whether the skill
may ever promote into a human's column, and where the skill lives — and all three were
answered. The name and icon checkpoint was also asked and answered.

## Where the rules came from

Every structural rule traces to something. The unusual ones and their sources:

- **One judge, not a panel** — nine frontier judges across seven families give ~2
  effective independent votes; the best single judge matches or beats the panel in all
  conditions tested. Verified against the paper's abstract.
- **Requirement list before the diff** — the same positioning failure as showing a
  reader the machine's marks first: across 429,345 real cases that cost specificity
  and detection while gaining nothing.
- **Inconclusive blocks** — laboratory practice treats it as a valid result; the one
  autonomous-diagnosis approval on record was granted *with* a mandatory can't-tell
  path that forced 38 of 819 cases to refer.
- **The five unarmed-assertion shapes** — observed directly, in one session, in work
  its author had already declared sound. Ten independent verifications of ten
  finished-looking commits returned ten findings and zero clean bills of health.

## What would settle it

Three tasks, in order of value:

1. **A seeded-defect run.** Take twenty finished cards, plant a known defect in a
   third of them, and see how many the skill catches and how many it invents. Without
   this its catch rate is unmeasured.
2. **The no-skill baseline.** The same twenty cards triaged without the skill, scored
   blind by a judge that never sees which side is which. This is the only honest answer
   to "does it earn its context".
3. **A drift check.** Re-run the same cards a week later on a newer model. A verifier
   whose behaviour moves invalidates every verdict it previously gave, which is why the
   Verified gate asks for a control chart.

Until at least the first two have run, treat this skill as unevaluated. It is built on
sourced findings and its machinery demonstrably refuses bad input — but neither of
those is evidence that its judgement is good.
