# Does ship-armada actually work? The honest answer, for now

**The eval suite for this skill is written down and has not been run.** Nothing in
this file is a measured result. There are no pass rates, no scores, no judge
verdicts and no costs, because no runner and no judge panel has ever been pointed
at it. `evals/evals.json` holds eight prompts with 50 checkable assertions between
them, ready for the day someone spends the budget.

That is a legitimate state to ship in, and it is stated here rather than left out,
because an EVALS.md that simply omits the subject reads to every later visitor as
though the pipeline ran.

What follows is the part that is real: the checks that can be made by hand today,
what they found, which of this skill's public claims currently lean on a sibling
skill's evidence rather than its own, and the two or three specific runs that
would replace this page with numbers.

## What was checked by hand, on 2026-08-18

Every line below was run against the files in this plugin. Nothing is quoted from
memory.

| Check | Result |
|---|---|
| `skills/ship-armada/SKILL.md` frontmatter parses (opening and closing `---`, `name`, `description`) | Passes. `name: ship-armada` matches the directory and both plugin manifests. |
| SKILL.md length against the 500-line ceiling the conformance gate enforces | Passes, at 90 lines. |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all four. `references/manifest.md` and `scripts/check_completion.sh` are this plugin's own; `references/second-opinion-lanes.md` and `references/scheduling-and-concurrency.md` belong to shipyard and ship-fleet respectively, and the prose names the owning skill in both cases, so a reader can follow them. |
| `scripts/check_completion.sh` parses (`bash -n`) | Passes. |
| It refuses to run with no argument | Passes: exits 1 with its own usage line. |
| It reports a missing ledger | Passes: exits 2 with `NO-LEDGER` against a directory holding no `ORCHESTRATOR.md`. |
| It fails closed on a bad fixture | **Passes on the outcome and fails on the diagnosis.** See below. |
| Everything the plugin claims to ship exists on disk | One gap, outside this suite: `assets/icon.png` at 1024px is absent, which the repo conformance gate reports as an `icons` failure. The icon set ships 256 and 128 only. |
| README claims that name a file | All resolve. |
| Prior eval evidence anywhere in the repository | None exists. Details below. |

### The check that did not come out clean

`scripts/check_completion.sh` is the mechanised form of this skill's most
safety-critical rule: a project is complete when its ledger says so, never when
its dispatch returns. Its header documents three exit codes (0 for agreement, 1
for open items, 2 for no ledger).

Run against a directory that has an `ORCHESTRATOR.md` with an open row but is not
a git repository, it **exits 128 and prints nothing at all**. The script sets
`pipefail` alongside `errexit`, so the assignment
`int_branch=$(git remote show origin 2>/dev/null | sed ...)` inherits git's own
failure and kills the script on that line. The `NO-INT` message the next line
exists to print is never reached in that case.

The direction of the failure is the safe one: a non-zero exit means a caller
following the skill's instruction ("read its output rather than re-deriving the
check by hand") does not tick the project off. But the caller gets no reason, and
128 is not one of the three codes the script's own header tells it to expect. That
is a real defect in a gate, and it is recorded here rather than in a passing
column.

Two things about that script were **not** checked, because this pass ran no git
commands: the clean path that exits 0, and the two checks that need real
repository state (unmerged `ai/*` branches, leftover worktrees). Those are the
parts that actually do the work, and they remain unverified.

### One documentation drift worth naming

The README says the daemon is set up "with `/loop` or a scheduled routine".
SKILL.md says to use the `better-loop` skill instead of the built-in, because the
built-in's session cron expires after seven days and cannot hand a restricted
skill to the run. The skill is the newer and more specific instruction; the README
sentence predates it.

## Which claims here are really shipyard's

This matters because a reader currently cannot tell, and the answer for
ship-armada is blunt: **none of its claims rest on evidence about itself, because
there is none.**

- ship-armada's README carries no "does it actually work" section at all, so it
  makes no evidential claim that could be traced anywhere.
- Nothing in `plugins/shipyard/evals/` tests ship-armada. Its records name seven
  main evals plus two adversarial ones, and ship-armada appears in none of them.
  The only mentions of the fleet-and-armada family anywhere in the repository's
  committed eval records are incidental: `plugins/better-goal/evals/evals.json`
  uses "/ship-fleet" inside two of its own task prompts, and one shipyard panel
  bundle quotes the phrase inside an intake output. Neither grades anything about
  these skills.
- The skills ship-armada dispatches to are separately evidenced.
  [ship-feature](../../ship-feature/evals/EVALS.md) has one eval of its own in
  shipyard's suite; the shipyard stage skills underneath it have nine, written up
  in [shipyard's EVALS.md](../../shipyard/evals/EVALS.md). None of that says
  anything about whether the portfolio layer routes, caps or ticks off correctly,
  which is the whole of what this skill does.

## What would settle it

Three runs, in the order they would pay off.

1. **A fixture portfolio, and the completion gate exercised against it.** Three
   throwaway git repositories under one directory plus an `ARMADA.md` covering
   them: one repo clean and merged, one with an unmerged `ai/*` branch, one with a
   leftover worktree. Running `check_completion.sh` against all three turns its
   exit-code contract into something that can fail, covers the two checks left
   unverified above, and gives the eight eval prompts a real disk state to be
   graded against instead of a described one. This is the cheapest of the three
   and unblocks the other two.
2. **The eight prompts run twice, with and without the skill.** The baseline arm
   is the same prompts with no skill loaded, which is the honest comparison for a
   skill with no committed predecessor snapshot. Grade with an independent agent
   that never sees the skill, one pass or fail per assertion with quoted evidence,
   into the `grading.json` shape shipyard's records already use. The two
   assertions marked `[control]` in `evals.json` are expected to pass on both arms
   and are there as guards, not discriminators; if any other assertion passes on
   the baseline too, it is measuring the model rather than the skill and should be
   rewritten or dropped, with the change recorded.
3. **The adversarial case, judged on its own.** `adv-done-without-verdict` is the
   one that matters most for a daemon nobody is watching: the mechanical gate
   passes, the ledger says every row is Done, and two of those rows carry no
   independent verification verdict. Reporting that project as shipped is the
   cheap wrong answer, and it is exactly the answer a run gets by trusting what
   the tooling returned. If the skill only wins one eval, this is the one worth
   winning.

## The eval set, in detail

`evals/evals.json` holds eight prompts. The assertions are checkable properties of
what the orchestrator did, never quality ratings, because an orchestrator produces
no artifact of its own to rate. What it does produce is conduct: which mode it
declared, what it wrote before it executed anything, where it stopped, what it
refused to tick off, and what it refused to touch. All of that is readable off a
written answer.

| Eval | What it targets | Why it can fail |
|---|---|---|
| `survey-freshness-before-planning` | The startup protocol: stamps compared against real commit dates, stale entries named rather than all silently refreshed | Six rows with known dates, three of them genuinely stale and one a decoy that looks stale and is not |
| `route-directive-not-build` | Route mode handing work to the target repo's pipeline instead of building it | Allocating a ledger id, writing code, or skipping the ORCHESTRATOR.md inbox row all fail it |
| `dispatch-cap-and-vehicle` | The three-project concurrency cap, one fleet per repo, and choosing the smallest sufficient vehicle | Seven projects and four in-flight lanes is a visible breach; so is a full spec pipeline for a model-id swap |
| `campaign-open-technical-call` | Which fork goes to another model and which goes to the human | Two questions, one technical and one about cost and priority, must be routed differently |
| `ownership-rule-refusal` | The manifest's ownership and activity rules, and the owner list living in configuration rather than in skill text | Six directories, two of them third-party, one a worktree copy, one stale, and no allow-list on disk |
| `daemon-unattended-parks-not-asks` | Unattended conduct: never blocking, assumptions recorded in the artifact, only `approved` campaigns executed | An ambiguous directive with nobody to ask, beside one approved and one proposed campaign |
| `completion-gate-uses-the-script` | The completion rule run as a script and decided on its exit code | Re-deriving the ledger check in prose fails it, as does treating the dispatch return as evidence |
| `adv-done-without-verdict` | **The adversarial case.** The gate passes, the ledger reads Done, and two items were never verified | Every source of truth the run can reach says finished; only the skill's own rule says otherwise |

Two assertions carry a `[control]` label. They are expected to pass on a no-skill
baseline as well, and are kept as regression guards on the shape of the output
rather than as evidence that the skill adds anything. Labelling them is the point:
an assertion that cannot fail measures the model, and in a suite the author wrote
knowing the intended answer, those are easy to accumulate by accident.
