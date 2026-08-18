# Does create-skill actually work? The pipeline's own evals have not been run

**Nothing in this file is a measured result from create-skill's own eval suite.** No
pass rates, no scores, no judge verdicts, no costs. `evals/evals.json` holds **four
evals and 23 checkable assertions**, and nothing has been pointed at them: no grading
file, no results directory, no run output, and no runner script anywhere under this
plugin.

There is an awkward fact to state first, because it is the most quotable thing in the
audit that commissioned this file. **create-skill is the skill that requires every
other skill in this marketplace to ship an EVALS.md, and it did not have one.** Nine
plugins were in that state, including this one and its sibling `improve-skill`, which
define the standard between them.

The rest of this file does what the standard asks of an unevaluated skill: it says
plainly that no run happened, lists what was verified mechanically, names where this
pipeline's real evidence lives, and names the tasks that would settle the open
question.

## The recursion, stated straight rather than cleverly

create-skill is a pipeline whose output is other skills. That has two consequences and
both are in `evals.json`'s own notes:

**Its own evals check conduct, not quality.** All four assert that the pipeline's steps
happen and happen in the right order: that the discovery interview runs before any
research starts, that `skill-creator` is actually invoked rather than a SKILL.md being
hand-written, that the no-skill baseline is *run* rather than assumed, and that both
user checkpoints are asked before anything is generated. None of them looks at whether
the skill that comes out is any good.

**Quality is proven downstream, by the evals this pipeline builds for each new skill.**
That is deliberate rather than evasive: a pipeline grading its own output quality is
marking its own homework, and the interesting question is never "did create-skill run"
but "is the skill it produced worth its context window".

So the honest structure of the evidence is: the process is untested here, and the
results are tested there. The next two sections cover both halves.

## What the four evals assert

| Eval | Assertions | What it protects |
|---|---:|---|
| 1 `discovery-before-research` | 6 | Handed "a skill that helps with our release process", the pipeline must interview before researching. `AskUserQuestion` is called before `research_start`, the questions offer discrete options with a marked recommendation rather than only free text, at least one covers the trigger, one the output and one the definition of done, the run states what it already worked out from the repo rather than asking, the vagueness is named as insufficient rather than silently resolved, and **no skill files are written before the interview is answered** |
| 2 `skill-creator-and-evidence` | 6 | Handed a complete brief, no interview is needed. `skill-creator` is invoked rather than the SKILL.md hand-written, research runs on the **domain** rather than on the skill, every completed report is read in full and citation-verified before the build, the built skill carries an `evidence.md` citing the exported corpus, the user's stated constraint appears as an explicit rule, and `docs/deep-research/` holds the exports |
| 3 `no-skill-baseline-is-run` | 5 | **The load-bearing one.** Each prompt runs twice, with the skill and without. The baseline outputs exist on disk and were graded rather than asserted from expectation. An independent grader marks every assertion with quoted evidence. Any assertion the baseline also passes is identified as measuring the model rather than the skill. And if the skill loses an eval, that appears in the reported table rather than being omitted |
| 4 `checkpoints-before-generation` | 6 | Name options and icon concepts go to the user before any asset is generated, no icon or banner is created before both answers arrive, README and EVALS.md go through `create-luke-content` and pass the voice lint, the root README gains a row, and the commit is made by the orchestrating session with no git operations by subagents |

Eval 3 is the one worth running first, because it is the assertion this whole pipeline
rests on. A baseline that is assumed rather than executed is the single cheapest way for
a skill's evidence to be fiction, and the sibling record shows it is not hypothetical:
`be-my-witness`'s own run found **seven of fourteen baseline outputs contaminated**
because the runner inherited its working directory and the "no skill" arm could read the
skill off disk.

There is no adversarial case in the set. The standard asks for one, and eval 4's hurry
framing is the obvious place to put it: `improve-skill`'s equivalent suite already
carries a prompt that says "I'm in a hurry, skip the ceremony" and asserts the
checkpoints survive it. create-skill's four evals carry no such pressure, so every
assertion is being tested on a cooperative run.

## Where this pipeline's real evidence is

`evals.json` says output quality is proven by the evals this pipeline builds. That claim
is checkable, so here is what is actually on disk.

The protocol this pipeline prescribes has a distinctive signature, written out in
`skills/create-skill/references/evals-and-judging.md`: because a new skill has no
predecessor, **the baseline is the same prompts run with no skill at all**, graded on
structural assertions rather than 1 to 10 scores, with a blind multi-family panel only
where the output is a matter of judgement, and reported in an EVALS.md carrying the
per-eval tables, the judge families and harnesses, the un-blinding location, the panel
cost and the caveats.

Four shipped skills in this marketplace carry suites built to exactly that signature,
and all four have committed run evidence:

| Skill | The evidence, as committed | What it reports |
|---|---|---|
| `geminify` | `plugins/geminify/EVALS.md` | Four arms across two targets, the author out of family in every arm, a structural table, four blind judgements in both orders, a costs section, and a "what none of this establishes" list. It also documents three attempts at building a baseline that was not cheating |
| `report` | `plugins/report/EVALS.md` | Three tasks each run twice, with the skill and with no skill, plus blind judges reading as the recipient. It records tasks where the baseline won |
| `dossier-report` | `plugins/dossier-report/EVALS.md` | A with-skill against no-skill table with a difference column, a blind panel, and the runs it lost written out |
| `be-my-witness` | `plugins/be-my-witness/EVALS.md` and its `RESULTS.md` | Fifteen cases both arms, 50 of 54 assertions against the baseline's 33, one case lost to the baseline, and an 11-verdict panel that reproduced the loss independently |

**What that establishes, and the boundary.** Those four suites match this pipeline's
prescribed protocol point for point, including the parts nobody would adopt by
accident: the no-skill baseline named as the honest comparison, the refusal to use
judged scores for structural properties, the requirement to report a case the baseline
won, and the un-blinding map kept separately. What no file on disk states is which
pipeline authored which skill. No run log, no changelog entry and no README in this
repository says "built by create-skill", so the shape is the evidence and authorship is
not claimed here.

The other side of the split is worth naming for the same reason. A second group of
shipped suites compares against a **predecessor** rather than against no skill, which is
`improve-skill`'s protocol rather than this one's: `trawl`, `shipyard`,
`mac-design-digest`, `generate-investor-portal`, `deck-craft`, `design-craft`,
`mac-craft` and `create-mac-icon`. One of those states the convention outright:
`create-mac-icon`'s `evals.json` describes its own evals as "Process evals in the
improve-skill convention".

## The voice gate this pipeline prescribes, and where it actually lives

`references/brand-and-docs.md` instructs a run of `voice_lint.py --format marketing` on
every README and EVALS.md until the hard checks are clean, and eval 4 asserts it. The
path is written bare, with no owning plugin named.

Checked in both directions on 2026-08-18:

| Question | Answer |
|---|---|
| Does `voice_lint.py` exist in this repository | **No.** No file of that name exists anywhere under `plugins/`, `site/` or the repository root |
| Does it exist at all | **Yes.** It ships with the `create-luke-content` plugin from the `diolog-plugins` marketplace, at `skills/create-luke-content/scripts/voice_lint.py` in the installed copy (version 2.4.3) |
| Does it accept `--format marketing` | **Yes.** `marketing` is one of eight format keys, alongside linkedin, blog, short, slack, email, review and brief |
| Does it run clean on this marketplace's existing EVALS.md files | **Yes.** Run against the three worked examples used as models for this file, `geminify/EVALS.md`, `trawl/evals/EVALS.md` and `ship-fleet/evals/EVALS.md`, it exits 0 on all three with "clean on the hard checks" |

So the gate is real and runnable, and the instruction that names it is defective in one
specific way: a bare relative path reads as this skill's own `scripts/` directory, and
this skill's `scripts/` holds `banner_sheet.py` and `render_banner.py` and nothing else.
On a machine without `diolog-plugins` installed, eval 4's assertion that the documents
"pass voice_lint" cannot be satisfied and nothing in the pipeline says why.

This is a documented failure mode elsewhere in the same marketplace. `mac-craft`'s
SKILL.md writes its cross-plugin paths out in full and explains that a bare
`references/...` reads as the skill's own directory, citing a predecessor that shipped
exactly that mistake. This pipeline's own reference does the thing that skill learned
not to do.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `scripts/banner_sheet.py check` on a deliberately empty directory | **Fails closed: exit 1**, with three named problems (`assets/banner.png is absent`, `no banner-src.html or banner-src.svg`, `banner-audit.html is absent, so no take was ever scored`) and the verdict "This banner is not signed off." A gate that cannot fail is not a gate, and this one demonstrably can |
| Both scripts byte-compile | Passes: `banner_sheet.py`, `render_banner.py` |
| `skills/create-skill/SKILL.md` frontmatter parses | Passes. `name: create-skill` matches the directory and the plugin manifest |
| SKILL.md against the 500-line conformance ceiling | Passes, at 248 lines |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 8. Seven are this plugin's own; `scripts/audit_sheet.py` resolves into `create-mac-icon`, and the prose names that skill in the same sentence |
| Everything the plugin claims to ship exists | Passes. Five references, two scripts, a licence, and the four evals |
| Version agreement between the manifests | Passes. `plugin.json` and `marketplace.json` both say 1.3.0 |
| **The README's version badge** | **Stale.** It reads "Version 1.0.0" while the plugin is at 1.3.0. Nothing checks a badge, and it is the first number a reader sees |
| Does the README overclaim | **No**, and it is unusually straight about it. Its "honest limits" section already says the evals here are process evals, that they do not check the skills produced, and that a single-run no-skill comparison understates a skill whose value is consistency rather than peak quality |
| `render_banner.py`'s five assertions | Present in the code and unrunnable here: it drives a browser, so it needs one. Its five checks are the viewport override read back rather than assumed, the font loaded and measured against a monospace control, every image decoded, nothing overflowing the frame, and the PNG exactly 3200 by 1040 |
| The reference's family-drift claim | **Not verified.** `brand-and-docs.md` says the set shows twelve different display faces across twenty-seven banners. Counting it means reading every plugin's `assets/`, and sibling agents were rebuilding assets in several plugins while this file was written, so any count taken now would be a moving target rather than a check |
| Is there a runner for the four evals | **No.** Nothing in `evals/` executes them, collects outputs or writes a grading file |

## What would settle it

Three runs, cheapest first.

1. **Run eval 3 against a real recorded run, not a fresh one.** Eval 3 is the only
   eval whose assertions can be graded off artifacts that already exist. Point it at
   `be-my-witness`'s committed eval directory, which holds 14 skill runs, 14 clean
   baselines, 7 quarantined ones and a write-up, and ask an independent grader whether
   each of the five assertions holds: were both arms run, do the baseline outputs exist
   on disk, was every assertion marked with quoted evidence, was any assertion the
   baseline also passed identified as measuring the model, and does the reported table
   include the case the skill lost. All five are answerable from that directory today,
   and the answers will not all be yes: the ties are reported, so is the loss, and the
   quarantine record is unusually good, but "an independent grader" is a claim about a
   process that left no separate grading file.
2. **Run evals 1 and 4 on a throwaway commission, and record the transcript.** Both
   are ordering assertions ("before", "no files written until", "no asset generated
   until"), which means they are properties of a transcript rather than of a file tree,
   and a run with no transcript kept cannot be graded at all. One small skill built
   end to end, with the session log retained, settles nine of the 23 assertions.
   Add the missing adversarial case in the same pass: eval 4 under hurry pressure,
   mirroring `improve-skill`'s eval 2.
3. **Name the owner of `voice_lint.py` in `brand-and-docs.md`, and decide what happens
   without it.** This needs no run. Either give the path in full the way `mac-craft`
   does, or state that the gate lives in `create-luke-content` and say what a pipeline
   run should do when that plugin is not installed. The current instruction is
   unsatisfiable from this repository alone and reads as though it were not.

## Caveats, in advance of any run

- **Process assertions are transcript properties, and transcripts are not kept.** Most
  of the 23 assertions ask whether something happened before something else. Nothing in
  this repository records the order of a run, so grading them means capturing a
  transcript deliberately rather than reading the result afterwards. That is the single
  biggest obstacle to ever running this suite, and it is worth knowing before budgeting
  for it.
- **A single run per eval would carry sampling noise**, and these are long multi-phase
  runs, so run-to-run variance is likely to be larger here than in a suite of short
  prompts.
- **There is no meaningful blind panel for this skill.** `evals-and-judging.md` says a
  panel is only worth running where the output is a matter of judgement rather than an
  artifact check, and this pipeline's output is a file tree and an ordering. A panel here
  would add cost without evidence.
- **The downstream evidence is evidence about the skills, not about the pipeline.** Four
  shipped suites matching this pipeline's protocol shows the protocol produces
  measurable skills. It does not show that this pipeline, as written today, is what
  produced them, and no file on disk closes that gap.
