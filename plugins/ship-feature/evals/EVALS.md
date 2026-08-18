# Does ship-feature actually work? What is evidenced, and what is not

**The eval suite for this skill is written down and has not been run.** Nothing in
`evals/evals.json` has produced a result. There are no pass rates, no scores, no
judge verdicts and no costs from it, because no runner and no panel has been
pointed at it yet. It holds eight prompts and 46 checkable assertions.

One thing about this conductor *has* been measured, in a sibling skill's eval run,
and this file separates that from everything else so a reader can tell which is
which.

## The one measured result, and exactly how far it reaches

In shipyard's rebuild evals (2026-08-15), one eval put **this skill's own
SKILL.md** in the tested arm.

- `plugins/shipyard/evals/evals.json`, eval `conductor-design-gates`, lists
  `../ship-feature/skills/ship-feature/SKILL.md` and shipyard's
  `skills/design/SKILL.md` as the new arm, against a committed snapshot of the
  predecessor conductor at `plugins/shipyard/evals/baseline/ship-feature-SKILL.md`.
- `plugins/shipyard/evals/records/grading-main.json` records that eval as **5 of 5
  assertions passed** for the new arm and **4 of 5** for the predecessor. The
  predecessor's failure was a genuine absence: no rendered-review gates named on
  its design phase.
- `plugins/shipyard/evals/records/panel-key.json` and `panel-results.tsv` record
  the blind panel on that eval: Option A was the new arm, and the Claude, xAI and
  Gemini judges all chose A, with the GPT seat empty. **Three votes to nil**, which
  is the claim the README makes and it checks out.

Four limits on that result, none of which are in the README:

1. **It is one eval, one run per arm.** Single runs carry sampling noise.
2. **Two skills were in the arm.** The conductor's SKILL.md was read alongside
   shipyard's design stage, so the result cannot separate what the conductor
   contributed from what the design stage did.
3. **It graded a description, not a run.** The task asked for the stage sequence
   and the design stage's gates in writing. It says nothing about what happens when
   a runner dies, when a gate goes red at 6pm, or when a completion record is
   missing its reviewer line.
4. **The grader itself flagged two of the predecessor's passes as thin.** Its notes
   in `grading-main.json` say "Thin pass, conductor old #3 and #5", so the 5 to 4
   margin is narrower in substance than in arithmetic.

None of the eight prompts in this plugin's own `evals/evals.json` is covered by
that eval. They exist because the four limits above are the interesting part.

## Which other claims lean on shipyard

The README's evidence section points at
[shipyard's EVALS.md](../../shipyard/evals/EVALS.md) for "the full comparison". That
is accurate as far as it goes, and worth being precise about:

- The 37-of-37 headline in that file covers **nine evals of the shipyard stage
  skills**, of which this conductor is in one.
- The rules this conductor enforces at the stage boundaries (evidence rules, model
  lanes, the tracker adapter, second-opinion lanes) are all shipyard's files, and
  their evals are shipyard's too. This skill's contribution is the conducting: the
  order, the artifact demanded at each boundary, and the refusals.
- Nothing in shipyard's records tests the conducting itself. That is the gap this
  suite exists to close.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `skills/ship-feature/SKILL.md` frontmatter parses (opening and closing `---`, `name`, `description`) | Passes. `name: ship-feature` matches the directory and the plugin manifest. |
| SKILL.md length against the 500-line ceiling the conformance gate enforces | Passes, at 167 lines. |
| Every `references/` path named in SKILL.md resolves | Passes. `orchestration-model.md`, `deferred-work-loop.md` and `e2e-and-finalize.md` are this plugin's own; `model-lanes.md` and `second-opinion-lanes.md` belong to shipyard, and the prose names shipyard in both cases. |
| Every `references/` path named inside those three reference files resolves | Passes. Four resolve into shipyard, one into ship-fleet's scheduling reference. One apparent miss, `scripts/contract-check.mjs`, is an illustrative example quoted from a different repository rather than a file this plugin ships. |
| Do the skill's scripts fail closed on a bad fixture | **Not applicable, and worth stating: this plugin ships no scripts.** Every gate it describes is prose executed by a model, which is precisely why the assertions in `evals.json` are about conduct rather than about exit codes. |
| Everything the plugin claims to ship exists on disk | Passes. The full icon set, banner, banner source and audit sheet are present, and the repository conformance gate reports no failure for this plugin other than the missing evals this file and `evals.json` now supply. |
| README claims that name a file | All resolve. |

## What would settle it

Three runs.

1. **The six prompts that have a predecessor arm, run head to head.**
   `evals/evals.json` points six of its eight evals at
   `../shipyard/evals/baseline/ship-feature-SKILL.md`, the same committed snapshot
   shipyard already used, so the comparison is reproducible without writing a new
   baseline. Grade with an independent agent that never sees either skill, one pass
   or fail per assertion with quoted evidence.
2. **The two prompts about failure, run against the no-skill baseline instead.**
   `resume-from-partial-artifacts` and
   `unattended-question-parks-without-blocking` are about behaviour the predecessor
   did not have, so a predecessor arm would only measure an absence. The honest
   comparison there is the same prompt with no skill loaded.
3. **A live re-entry test, not a described one.** The resume eval currently
   supplies its disk state as text. Building it for real (a fixture repo with a
   spec, a committed plan, a worktree carrying eleven commits, two unwaived state
   matrix cells, and no completion record) turns "says it would re-enter at stage
   five" into "re-entered at stage five", which is the difference between grading
   the prose and grading the conductor. It is the most expensive of the three and
   the only one that tests the claim the skill actually makes.

## The eval set, in detail

Eight prompts. Every assertion is a checkable property of the conductor's conduct,
never a rating, because the conductor produces no artifact of its own to rate. What
it does produce is a sequence of decisions: which stage it invoked, which artifact
it demanded before advancing, where it refused to advance, and what it declined to
set itself.

| Eval | What it targets | Why it can fail | Arm |
|---|---|---|---|
| `stage-sequence-and-sanctioned-overlap` | Exactly one parallel pair, verify spawned fresh, an artifact named at every boundary | Running more stages in parallel, or running verify inline, both breach a load-bearing rule | Predecessor |
| `resume-from-partial-artifacts` | Re-entry at the earliest artifact that is missing or not green | Two unwaived state matrix cells make design not green even though a committed plan exists | No skill |
| `missing-critic-line-is-a-skipped-gate` | A documented failure mode: no critic line means the last reviewer was skipped or lost | A fully ticked clause table sits right beside the missing line, inviting the wrong call | Predecessor |
| `deferred-loop-branch-discipline` | Deferred and child work landing on the parent's branch | A week of genuinely new scope is the case that tempts a new branch | Predecessor |
| `premerge-gate-fails-closed` | Stopping at a red gate as a correct outcome | The verdict is COMPLETE, the suite went green twice, the failing spec is in code the feature never touched, and someone is waiting | Predecessor |
| `unattended-question-parks-without-blocking` | Settle, refer or park, with nobody to ask, and never invent | Three questions that must be routed three different ways | No skill |
| `scale-down-without-dropping-rigor` | The stages as a floor of rigor rather than a volume requirement | A one-file timeout change should not produce a mock, and should still get a verifier | Predecessor |
| `adv-done-from-green-gates` | **The adversarial case.** Every gate green, gap-fix found nothing, a demo at 9am, no verifier verdict | Reporting success because every dispatch returned green is the cheap wrong answer, and it looks completely reasonable | Predecessor |

No assertion in this set is marked `[control]`, and that is deliberate rather than
lucky: each one names an artifact, a refusal or a state transition that a model
answering cold has no particular reason to produce. If a run shows the no-skill
baseline passing any of them, that assertion is measuring the model rather than the
skill, and the honest response is to rewrite or drop it and say which.
