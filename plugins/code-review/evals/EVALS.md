# Evals

**Nothing in this file is a measured result about how well this skill works.** The eval suite exists
now, in [`evals.json`](evals.json), and it has not been run. No prompt has been executed with the
skill loaded, none without it, no judge has looked at any output, and there is no pass rate.
Shipping in that state is honest; shipping a file that quietly omits the subject is not, because it
reads as though the pipeline ran.

What follows is what was checked mechanically, what the eval set would settle, and what none of it
can tell you.

## What was checked, and what it found

Every figure below was measured on 20 August 2026 against the files in this plugin.

**The SKILL.md parses and carries the three expected keys.** `name` matches its directory, the
description runs to 1,568 characters and holds no embedded newline, and `allowed-tools` is declared. This check earned its place
on the sibling it was built alongside: a bare colon inside a plain-scalar description made the YAML
parser read a nested mapping, and no gate in this repo opens the second skill of a two-skill plugin.
Both files here are folded block scalars.

**It sits inside the length target.** 381 lines, 298 non-empty, against a 300-line target, and below
the 409-line fork it replaces. Depth sits in references: 4,229 lines across 16 files, opened per
phase rather than carried. Two of those files exist specifically to hold detail the SKILL.md used to
carry inline, and the ReportFindings reasoning moved into the output-format reference for the same
reason.

**The voice gates pass.** `agent_voice_lint.py --format skill` exits 0 on the SKILL.md with no
hard-check failures. `voice_lint.py --format marketing` exits 0 on the plugin README, including its
alt text.

**Every reference and script pointer in the SKILL.md resolves on disk.** Sixteen references and
three scripts, checked by path. All three scripts are committed executable.

**The Opus 5 prompting rules hold.** A search for verification scaffolding ("double check",
"re-verify", "confirm your answer") returns nothing across the skill and its references. A search
for pressure language ("CRITICAL:", "you MUST") returns nothing outside the severity taxonomy, where
`CRITICAL` is a severity name. The delegation cap is explicit at 8 shards, verifier waves of at most
8 concurrent and 1 sweep finder. Output length is calibrated per depth by a findings ceiling.

**Zero project leakage.** The skill and its references were generalised from a fork tuned to one
monorepo. A case-insensitive search for that project's names across all sixteen references and three
scripts returns nothing.

**The brand artifacts pass their own gates.** `banner_sheet.py check` exits 0: 3200x1040 from a
1600x520 layout, a linked web font rather than a local face, the real icon inlined rather than
redrawn, five display renders that resolve, and a written verdict. Two effects were silently dropped
by the render engine and rebuilt. `mask-composite` filled the aperture solid, inverting a hole into
a bar while passing every mechanical assertion, and an inset box-shadow was caught by the renderer's
own guard. Both are recorded in `assets/banner-verdict.md` rather than papered over.

## What the eval set would settle

Eight prompts, in `evals.json`. Three carry most of the weight:

- **Eval 4**, the adversarial one, hands the skill a confident false claim about which frameworks
  the repo uses. Runtime discovery is this skill's central generalisation, and this is the case
  where taking a fact on trust would look identical to establishing it, right up until a checklist
  is skipped that should have run.
- **Eval 5** loses a shard in a fan-out and asks for the report anyway. A harness that loses an
  agent reports the wave complete, so the reconciliation has to be deliberate.
- **Eval 6** hands it a clean two-file change and an invitation to just say so. An empty findings
  list is where the coverage ledger is easiest to drop and where dropping it does the most damage.

The other five cover a PLAUSIBLE finding surviving verification, a narrowed scope not reading as a
clean bill for the rest, two independent findings on one line both getting through, the gate command
coming from the package scripts rather than an assumed compiler, and the read-only boundary holding
against a direct instruction to apply the fixes.

## Caveats, stated rather than buried

**The comparison that matters has not been made.** This skill supersedes two working predecessors,
the built-in CLI review and a 330-line skill in another marketplace. Whether it is better than
either is exactly the question the eval set was written to answer, and it is unanswered. Everything
above is a property of the files, not of the results they produce.

**A mechanical pass is a weak guarantee.** Frontmatter parsing, line counts, pointer resolution and
lint exits say the artifact is well formed. They say nothing about whether the fourteen angles find
real bugs, whether the six verification gates refute the right things, or whether a runner holds the
read-only line when a user pushes back twice.

**No blind panel scored the icon or the banner.** The icon set passed its dimensional checks and one
pair of eyes looked at the renders; the judge lane that would have made it a measurement exited 1
mid-run. The banner's five mechanical rows passed and the verdict names its own liabilities.

**Some of the evidence is inherited rather than first-party.** `references/evidence.md` marks every
such rule `M (inherited)` and says those are worth re-sourcing before they are quoted outside this
skill. Four of the measurements behind the design decisions are in that class.

**Single runs would carry sampling noise.** When these evals are run, one execution per arm is a
data point and not a result. The prompts are written to be run more than once.
