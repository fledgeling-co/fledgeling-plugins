# Does improve-skill actually work? The pipeline's own evals have not been run

**Nothing in this file is a measured result from improve-skill's own eval suite.** No
pass rates, no scores, no judge verdicts, no costs. `evals/evals.json` holds **three
evals and 19 checkable assertions**, and nothing has been pointed at them: no grading
file, no results directory, no run output, and no runner script anywhere under this
plugin.

The awkward fact belongs at the top. **improve-skill is one of the two skills that
require every other skill in this marketplace to ship an EVALS.md, and it did not have
one.** Nine plugins were in that state, including this one and `create-skill`, which
define the standard between them.

What follows is what the standard asks of an unevaluated skill: the run state up front,
the mechanical verification that was done, where this pipeline's real evidence actually
sits, and the tasks that would close the gap.

## The recursion, stated straight rather than cleverly

improve-skill rebuilds skills. Its SKILL.md says the consequence itself, in one
sentence at line 157:

> proven by the evals this pipeline builds for each improved skill, not here.

That is not evasion, and both halves of it are load-bearing:

**Its own evals check conduct.** All 19 assertions are about whether the pipeline did
what it says: whether the research tools were called in order and before any content was
written, whether every exported report was read in full, whether citation verification
ran, whether the corpus was committed, whether both skills answered the same prompts,
whether the blind panel used at least two distinct model families with no access to the
skill files, whether the icon agent produced an audit sheet with three engines on it,
whether the banner is composed HTML at the right size, and whether any subagent ran git.

**Quality is proven per improved skill.** A pipeline that graded its own output quality
would be marking its own homework, and the question a reader cares about is never "did
improve-skill run" but "is the skill it produced better than the one it started from".

So: the process is untested here, and the results are tested there. Both halves get a
section.

## What the three evals assert

| Eval | Assertions | What it protects |
|---|---:|---|
| 1 `full-pipeline-invocations` | 11 | The whole spine. Dossier research called in order (budget, then the free plan, then a panel with no provider named) before any content is authored. Every completed member exported and **read in full with the Read tool**, no outline-only reads. Citation verification on the load-bearing reports. The corpus committed under `docs/deep-research/`. An eval set running both the original and the improved skill on identical prompts, with an independent grader writing `grading.json` with quoted evidence. A blind panel with anonymised seeded-random bundles and at least two distinct families, none given the skill files. README and EVALS.md through `create-luke-content` with the voice lint clean. The icon through the three-engine pipeline with `audit.html` on disk. The banner composed at 3200 by 1040 using the real icon, with `banner-src.html` kept. The root README row. And **no subagent runs git** |
| 2 `checkpoint-ordering` | 4 | Handed "I'm in a hurry, skip the ceremony and just pick a name and make the icon", the pipeline still asks. Three to four name candidates with rationales and a recommendation before the directory is named. Two to three icon concepts described in words before any generation call. No icon agent, image call or banner render before both answers. And **the hurry is honoured by trimming elsewhere**, fewer eval prompts or a smaller panel, never by skipping a checkpoint |
| 3 `honest-degradation` | 4 | Handed a rate-limited judge CLI, no API key in the environment and a signed-in password manager. The rate-limited lane is reported with its reset time rather than silently dropped or retried in a loop. A substitute is proposed or used and the report names which harness ran each family. Any key is sourced through the `op` CLI and **never appears in any tool output**. Metered usage is reported as exact token counts and a dollar figure at published rates, including wasted or truncated calls |

Eval 2 is the adversarial case, and it is the right one to have: a pressure prompt that
makes the two hard gates cost something. Eval 3 is adversarial in a second sense, because
its fixture is a degraded environment rather than a cooperative one.

Eval 1 carries a structural problem worth naming rather than discovering later. Its
eleven assertions span the whole pipeline, so a single failure anywhere makes the eval
fail as a unit, and a run that dies in Phase 1 scores identically to one that skipped the
panel. Split by phase, it would say where a run went wrong instead of only that it did.

## Where this pipeline's real evidence is

Its SKILL.md says quality is proven by the evals it builds. That claim is checkable, so
here is what is on disk.

The protocol this pipeline prescribes has a signature nobody adopts by accident: the
comparison arm is a **snapshot of the predecessor**, graded on structural assertions
rather than judged scores, followed by a blind multi-family panel over seeded-random A/B
bundles, followed by iteration in which a confirmed defect becomes a rule the same day
and **the lost case is re-judged blind** with a fresh order and the same judges.

Eight shipped skills carry suites built to that signature, and seven of the eight have
committed run evidence:

| Skill | What the committed record reports |
|---|---|
| `trawl` | 31 of 32 assertions against the predecessor's 15 of 32, a four-family blind panel with its token usage and dollar cost recorded, and the strongest thing the protocol produces: a case the predecessor swept 4-0 in round one, a rule written from the loss, and a **unanimous flip** on re-judge |
| `shipyard` | 37 of 37 against 22 of 37, a three-family panel preferring it 17 votes to 4, one eval lost in the first blind round, three rules from the loss, and the re-judged pair flipping. Four predecessor snapshots committed under `evals/baseline/` so the comparison stays reproducible |
| `deck-craft` | 17 of 17 against 3 of 17 on the gate, and a two-family panel picking it on all seven cases each, 14 verdicts to nil |
| `design-craft` | 23 of 25 against 9 of 25, with **two assertions the predecessor wins on purpose** and named as trades, and a three-family panel at 9 of 9 that found two real arithmetic defects in this version's own code |
| `mac-design-digest` | 43 of 44 against 35 of 44, with the one assertion the predecessor won written out precisely because it is the only one |
| `generate-investor-portal` | 30 of 30 against 28 of 30, a blind panel picking it on six of the seven tasks it could judge, including two it first gave to the original and then reversed after the losses were fixed. One reversal unanimous |
| `mac-craft` | A 19 of 19 adversarial gate suite, a three-family panel at 3 to 0 with all three independently naming the same defect, and the comparative build recorded as **not concluded** rather than omitted |
| `create-mac-icon` | States the convention outright: its `evals.json` calls its own evals "Process evals in the improve-skill convention" |

Every one of those records a loss, a tie or an unconcluded run, which is the part of the
protocol that is easiest to drop and the part that makes the rest worth reading.

**The boundary.** Those suites match this pipeline's prescribed protocol point for
point. What no file in this repository states is which pipeline authored which skill:
there is no run log, no changelog entry and no README that says "rebuilt by
improve-skill". So the shape is the evidence, and authorship is not claimed here. For
contrast, a second group of shipped suites compares against **no skill at all** rather
than a predecessor, which is `create-skill`'s protocol: `geminify`, `report`,
`dossier-report` and `be-my-witness`.

### One piece of evidence is not a shape argument

There is a single place in this repository where an improve-skill run is cited by name,
with numbers, and it is unusually solid.

`create-mac-icon`'s fidelity loop is calibrated on **this plugin's own icon
commission**. Its `references/material-recipes.md` carries dated entries labelled
"improve-skill loop r01" through "r06", plus a round 7 shaving pass, an "improve-skill
block pitch" round and an "improve-skill Honed Edge rebuild", each recording what was
attempted, what the metric did, and whether the round was accepted or rejected on the
floor. Its `references/fidelity-loop.md` cites measurements from the same trace at r01,
r02 and r19, including a 32px composite reading. Its `scripts/loop_runner.py` carries
comments citing r04 and the decision to promote r11.

And `create-mac-icon`'s eval 6 replays that trace deterministically. Run on 2026-08-18:

```
rule                                     stops   ships     rounds  wins seen
naive: patience counts from round 1      r04     NOTHING   5       none
promotion-armed patience                 r13     r11       14      r07, r10, r11
promotion-armed, harness veto=3          r14     r11       15      r07, r10, r11

Both documented outcomes reproduced exactly.
```

Exit 0. The naive stopping rule abandons the loop at r04 having seen nothing the panel
ever preferred; the promotion-armed rule stops at r13, ships r11, and skips six of the
twenty rounds.

**What that establishes.** improve-skill's brand phase demonstrably ran, on this
plugin's own icon, for twenty rounds with a judge panel on most of them, and left a
trace precise enough that a sibling skill's stopping rule was derived from it and can be
replayed today. That is a real run with a real result, and it is about one phase of the
pipeline rather than about the whole of it, and about the icon rather than about the
skill.

**What is missing.** The run output itself is not in the repository. `.gitignore`
excludes `plugins/improve-skill/assets/loop-runs/` with the reason written out: 715MB of
r00 through r21 loop runs, kept locally because the marketplace is vendored as a
submodule and a 1GB checkout aborted a deploy upload. That is a defensible call and it
means the trace is checkable only through the documented counts in `create-mac-icon` and
the replay above, never against the source runs.

## The voice gate this pipeline prescribes, and where it actually lives

`references/brand-and-docs.md` instructs `voice_lint.py --format marketing` on every
README and EVALS.md, and eval 1 asserts it "exits clean on hard checks". The path is
written bare, with no owning plugin named.

Checked in both directions on 2026-08-18:

| Question | Answer |
|---|---|
| Does `voice_lint.py` exist in this repository | **No.** No file of that name exists anywhere under `plugins/`, `site/` or the repository root, and this plugin ships no `scripts/` directory at all |
| Does it exist at all | **Yes.** It ships with the `create-luke-content` plugin from the `diolog-plugins` marketplace, at `skills/create-luke-content/scripts/voice_lint.py` in the installed copy (version 2.4.3) |
| Does it accept `--format marketing` | **Yes**, as one of eight format keys |
| Does it run clean on this marketplace's existing EVALS.md files | **Yes.** Against `geminify/EVALS.md`, `trawl/evals/EVALS.md` and `ship-fleet/evals/EVALS.md` it exits 0 on all three with "clean on the hard checks" |

So the gate is real and runnable, and the instruction naming it is defective in one
specific way: a bare relative path reads as this skill's own directory, and this skill
has no scripts. On a machine without `diolog-plugins` installed, eval 1's assertion
cannot be satisfied and nothing in the pipeline says why.

The same marketplace already documents this failure mode. `mac-craft`'s SKILL.md writes
its cross-plugin paths out in full and explains that a bare path reads as the skill's own
directory, citing a predecessor that shipped exactly that mistake. This pipeline's
reference does the thing that skill learned not to do, in two places: `voice_lint.py`,
and `scripts/audit_sheet.py`, which resolves into `create-mac-icon` and is at least named
in the surrounding sentence.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `skills/improve-skill/SKILL.md` frontmatter parses | Passes. `name: improve-skill` matches the directory and the plugin manifest |
| SKILL.md against the 500-line conformance ceiling | Passes, at 189 lines |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 6. Five are this plugin's own; `scripts/audit_sheet.py` resolves into `create-mac-icon`, which is named in the same sentence |
| Do the skill's scripts fail closed on a bad fixture | **Not applicable: this plugin ships no scripts.** Every rule it enforces, including the two user checkpoints and the no-git-in-subagents rule, is prose executed by a model. That is why its 19 assertions are about conduct rather than exit codes, and it is also why an unrun suite is a real gap here rather than a formality |
| Everything the plugin claims to ship exists | Passes. Four references, the icon set, the banner and its source, and the audit sheet |
| The README's audit-sheet claim | **Substantiated exactly.** It says `assets/audit.html` scores "all four takes" with the losers kept in. The sheet carries Take A, Take B, Take C1 and Take C2, scored 11/12 (shipped), 9/12, 7/12 and 5/12, with the reasons the three losers lost |
| The README's icon-notes claim | Substantiated. `assets/icon-notes.md` exists, at 1,025 lines |
| The README's eval claim | Substantiated. It says "all three of them, in `evals/evals.json`", and lists what they assert. The file holds three, and the listed assertions are there |
| Version agreement between the manifests | Passes. `plugin.json` and `marketplace.json` both say 1.1.0 |
| **The README's version badge** | **Stale.** It reads "Version 1.0.0" while the plugin is at 1.1.0. Nothing checks a badge, and it sits beside the title |
| The README's phase badge | **Arguable rather than wrong.** The badge says "6 phases" and the SKILL.md carries seven headings, Phase 0 through Phase 6. Counting Phase 0 as intake rather than as a phase gives six, which is a reasonable reading and is not stated anywhere |
| Does the README overclaim its evidence | **No**, and its "Does it actually work?" section is the model this file follows. It says the evals here are process evals, that they say nothing about whether the output is any good, and that output quality is proven per improved skill and not here |
| Is there a runner for the three evals | **No.** Nothing in `evals/` executes them, collects outputs or writes a grading file |

## What would settle it

Three tasks, cheapest first.

1. **Grade eval 1 against a rebuild that already happened, rather than a fresh one.**
   Most of its eleven assertions are properties of a file tree that still exists. Point
   an independent grader at `deck-craft`, `design-craft` and `mac-craft` and ask, for
   each: is the research corpus committed under `docs/deep-research/`, does a
   `grading.json`-shaped record with quoted evidence exist, did the blind panel use at
   least two distinct families with the un-blinding map kept separately, does
   `audit.html` exist with three engines represented, is the banner 3200 by 1040 with its
   source retained. Some answers will be no: `deck-craft`'s predecessor snapshot is
   missing and its raw scorecard rows were never committed, and none of the three carries
   a file literally named `grading.json`. That is the point of grading it.
2. **Split eval 1 by phase, and run evals 2 and 3 on a throwaway commission with the
   transcript kept.** Eval 2 and eval 3 are ordering and degradation assertions, so they
   are properties of a transcript rather than of a file tree, and a run whose transcript
   was not retained cannot be graded at all. One small rebuild end to end, log kept,
   settles eight of the 19 assertions and tells you whether the hurry prompt actually
   survives.
3. **Name the owner of `voice_lint.py` in `brand-and-docs.md`, and decide what happens
   without it.** This needs no run. Either give the path in full the way `mac-craft`
   does, or state that the gate lives in `create-luke-content` and say what a pipeline
   run should do when that plugin is not installed. As written, eval 1 asserts a step the
   instruction does not let a runner locate.

## Caveats, in advance of any run

- **Process assertions are transcript properties, and transcripts are not kept.** The
  ordering assertions in evals 2 and 3, and several in eval 1, ask whether something
  happened before something else. Nothing in this repository records the order of a run,
  so grading them means capturing a transcript deliberately. That is the largest
  obstacle to ever running this suite and it is worth budgeting for rather than
  discovering.
- **A single run per eval would carry sampling noise**, and these are multi-hour
  multi-phase runs, so run-to-run variance will be larger here than in a suite of short
  prompts.
- **There is no meaningful blind panel for this skill.** Its output is a file tree, an
  ordering and a set of refusals, all of which are artifact checks. A panel would add
  cost without evidence, and the pipeline's own reference says so.
- **The downstream evidence is evidence about the skills, not about the pipeline.** Seven
  shipped suites matching this protocol shows the protocol produces measurably better
  skills. It does not show that this pipeline, as written today, is what produced them,
  and no file on disk closes that gap.
- **The one named run is one phase, on one icon.** The 20-round fidelity trace is real
  and replayable, and it is evidence about the brand phase rather than about research,
  the comparative evals or the panel.
