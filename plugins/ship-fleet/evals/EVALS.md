# Does ship-fleet actually work? The suite, and the claim that did not hold up

**The eval suite for this skill is written down and has not been run.** Nothing in
it is a measured result: no pass rates, no scores, no judge verdicts, no costs. No
runner and no panel has been pointed at `evals/evals.json`, which holds nine
prompts and 56 checkable assertions. The ninth was added on 2026-08-20, covering the
evidence-integrity rules: routing a ready-to-verify item with no bundle back to its
runner, and running the campaign's capture gate once per repo rather than once per item.

There is also no measured result anywhere else. Unlike its sibling
[ship-feature](../../ship-feature/evals/EVALS.md), whose SKILL.md was in the tested
arm of one shipyard eval, **this skill has never been in any eval's arm**, and the
next section says so with the search that establishes it.

## Where this skill's evidence actually is

The README currently says the fleet's operating rules "are the part with the longest
evidence trail: nearly every line in its scheduling reference records a dated
incident from real fleet runs", and names four of them. Checked line by line on
2026-08-18:

| The claim | What is on disk |
|---|---|
| "nearly every line" of the scheduling reference "records a dated incident" | The file is 357 lines and carries **two** date stamps, both of them section headings reading "field-learned 2026-07". The incidents themselves are real and specific, but they are written without dates ("in the field", "has been observed"), so the trail cannot be followed to a run. |
| "the `git add -A` that swept three runners' work onto main" | Present, and **not in this plugin**. It is shipyard's `references/operational-rules.md`, line 13: one `-A` swept 1,164 insertions of three sibling runners' work. The string `git add -A` appears nowhere in ship-fleet's own directory. |
| "the `pkill` that killed a sibling's test run" | Same file, line 27: one `pkill -f vitest` killed a sibling runner's live test run. Also not in this plugin. |
| "the model override that didn't stick" | This one is genuinely ship-fleet's own, in SKILL.md line 44 and in the scheduling reference line 87. |
| "the seven runners lost to transport failures" | Not found anywhere under `plugins/`, in any skill, reference or record. The only occurrence of the phrase in the repository is the README sentence making the claim. |

So two of the four named incidents are shipyard's, one is this skill's, and one has
no source that could be located. That does not make the rules wrong: they read like
what they claim to be, rules paid for in real runs, and shipyard's copies carry
figures precise enough (1,164 insertions, a named test runner) that they plainly
come from somewhere. It makes the *evidence sentence* wrong, and an unfalsifiable
sentence in an evidence section is worse than an empty one, because a reader treats
it as having been checked.

The other half of that README sentence points at
[shipyard's EVALS.md](../../shipyard/evals/EVALS.md) for "the rebuild's eval story
for the stages underneath it". That is accurate and it is worth being explicit
about the boundary: those nine evals test the stage skills a fleet runner
eventually invokes. **None of them tests scheduling, concurrency caps, ledger
locking, worktree hygiene, merge serialisation or recovery from a dead runner**,
which is the entire subject of this skill.

For completeness, the search behind "never in any eval's arm": no
`grading.json`, `benchmark.json`, results directory, panel key or run output exists
under this plugin; `plugins/shipyard/evals/baseline/` holds committed snapshots of
the predecessor plan, triage, verify and ship-feature skills and **no fleet
snapshot**, so there is no predecessor arm to compare against either; and the two
places the name appears in committed eval material are both incidental. One is
`plugins/better-goal/evals/evals.json`, where two task prompts tell the model to use
`/ship-fleet`, which grades better-goal. The other is a shipyard panel bundle
quoting "use ship-fleet" inside an intake output's prose.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `skills/ship-fleet/SKILL.md` frontmatter parses (opening and closing `---`, `name`, `description`) | Passes. `name: ship-fleet` matches the directory and the plugin manifest. |
| SKILL.md length against the 500-line ceiling the conformance gate enforces | Passes, at 174 lines. |
| Every `references/` path named in SKILL.md resolves | Passes, all eight. `orchestrator-artifacts.md`, `preflight.md` and `scheduling-and-concurrency.md` are this plugin's own; `codex-cli.md`, `model-and-effort.md`, `model-lanes.md`, `operational-rules.md` and `tracker-adapter.md` belong to shipyard, and the prose names shipyard in each case. |
| Every `references/` path named inside those three reference files resolves | Passes. Three resolve into shipyard. |
| Do the skill's scripts fail closed on a bad fixture | **Not applicable: this plugin ships no scripts.** Every rule it enforces, including the concurrency cap and the merge serialisation, is prose executed by a model. That is why the assertions in `evals.json` are about conduct rather than about exit codes, and it is also why an unrun suite is a real gap rather than a formality. |
| Everything the plugin claims to ship exists on disk | Passes. Full icon set, banner, banner source, audit sheet, and the three references. The repository conformance gate reports no failure for this plugin other than the missing evals this file and `evals.json` now supply. |
| README claims that name a file | All resolve. |

## What would settle it

Three runs, cheapest first.

1. **The eight prompts run twice, with the skill and with no skill.** No
   predecessor snapshot exists, so the no-skill arm is the honest baseline. Grade
   with an independent agent that never sees the skill, one pass or fail per
   assertion with quoted evidence, into the `grading.json` shape shipyard's records
   already use. The single `[control]` assertion is expected to pass on both arms;
   any *other* assertion passing on the baseline is measuring the model rather than
   the skill, and gets rewritten or dropped with the change recorded.
2. **A fixture repository, so hygiene and re-entry are graded against disk.**
   `hygiene-never-destroys-unmerged-work` and `adv-completed-with-dead-agents`
   currently supply their branch and worktree listings as text, which grades what
   the skill says it would do. A throwaway repo carrying the real states (one
   provably merged branch, one worktree with unique commits, one scratch-only
   worktree, one orphan with no ledger row) turns them into checks on what it does.
   This is the run that would tell you whether the fleet destroys work, which is the
   most expensive way it can fail.
3. **Commit a snapshot of the predecessor fleet skill.** The diolog ship-fleet 1.x
   SKILL.md was the source of almost all of this material, and shipyard's evals
   directory already carries four predecessor snapshots for exactly this purpose.
   Adding a fifth turns "the rules survive here" into a comparison that can be
   graded, and it is the only way to check the restructuring did not lose a rule on
   the way across.

Fixing the README's evidence sentence is not on that list because it needs no run:
it needs the three verifiable incidents attributed to the file that actually holds
them, and the fourth either sourced or removed.

## The eval set, in detail

Eight prompts. Every assertion is a checkable property of the orchestrator's
conduct, never a rating. A fleet orchestrator ships no feature of its own, so what
it produces is a plan, a ledger and a set of refusals, and all three are readable
off a written answer.

| Eval | What it targets | Why it can fail |
|---|---|---|
| `artifacts-before-execution` | The plan and ledger written, shown and committed before the first runner starts | Nine backlog items and free slots make starting work first the tempting order |
| `survey-classification-completeness` | Every item classified, including the flagship gap: Developer Review with no verdict is not done | A ledger with six rows, two orphan briefs, a deferred note buried in a progress comment, a stale mock and a founder question |
| `serial-pretriage-ledger-lock` | Id allocation serialised because it is a read-modify-write on a shared file | Four briefs and six idle slots is exactly the setup that invites parallelising it |
| `agent-budget-is-a-product` | Slots multiplied by inner waves, not two independent caps | A user asking for eight slots tonight, where the arithmetic has to be shown and reconciled |
| `dependency-order-requires-merge` | A dependency must have merged, not merely finished | The blocking item is green and unmerged, which reads as done to a scheduler that is not looking |
| `hygiene-never-destroys-unmerged-work` | Cleanup touching only the provably merged or empty | Four branches, three worktrees, one orphan nobody remembers, and a rule that unmerged work is never destroyed |
| `stop-before-verify-and-before-merge` | Both stop rules, and the reason each is structural | A runner cannot verify its own build, and two simultaneous merges corrupt the integration branch |
| `adv-completed-with-dead-agents` | **The adversarial case.** The workflow reports `completed` with two runners returned null, and one report claims ready to merge | The framework said completed and a runner said green, so every source the run can reach agrees. Ticking the items off is the cheap wrong answer |

One assertion carries a `[control]` label, in the hygiene eval: a run handed a
branch listing will use it whether or not a skill told it to. It is kept as the
floor the eval sits on and named so nobody counts it as evidence.
