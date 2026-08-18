# Does be-my-witness actually work? It was run, and here is the whole record

**These evals were run, on 2026-08-11, and the outputs are committed.** Fifteen
cases, both arms, one model. The record is not a summary written afterwards: 35 run
files, 11 judge verdicts and a full write-up sit in
`skills/be-my-witness/evals/`, and every number below was read out of them or
recomputed while this file was being written.

The headline: **the skill passed 50 of 54 assertions, the no-skill baseline passed
33 of 54.** Nine cases went to the skill, five tied, and one went to the baseline.
The loss is the most useful thing here and it gets its own section.

The comparison throughout is the skill against **no skill at all**. There is no
predecessor, so the only honest question is whether the file earns the context
window it costs.

## Where the evidence is

| What | Where | What it holds |
|---|---|---|
| The full write-up | `skills/be-my-witness/evals/RESULTS.md` | Per-case scores, the ties, the loss, the harness defect, the panel |
| The eval set | `skills/be-my-witness/evals/evals.json` | 15 cases in 7 coverage groups, 54 assertions, plus the run summary |
| The outputs | `skills/be-my-witness/evals/runs/` | 14 skill runs, 14 clean baselines, 7 quarantined baselines |
| The panel | `skills/be-my-witness/evals/panel/` | 11 verdicts across 2 judge families, plus the raw judge logs |
| The runners | `run-evals.sh`, `run-panel.sh` | Both committed, both isolate the baseline arm |

Both arms ran on `claude-fable-5 --effort high`, fresh context each, same prompts,
same fixtures. Grading is structural: every assertion is a checkable property of
the response, never a 1 to 10 rating.

## The report card

Recomputed from `RESULTS.md` on 2026-08-18, and the per-case denominators agree
with `evals.json` case for case.

| Case | Group | No skill | Skill | Outcome |
|---|---|---|---|---|
| BMW-01 | evidence-gates | 0/4 | 4/4 | **skill** |
| BMW-02 | evidence-gates | 1/4 | 4/4 | **skill** |
| BMW-03 | artifact-precedence | 2/4 | 2/4 | tie |
| BMW-04 | looking-protocol | 1/4 | 3/4 | **skill** |
| BMW-05 | adversarial-input | 2/4 | 4/4 | **skill** |
| BMW-06 | honest-reporting | 3/3 | 3/3 | tie |
| BMW-07 | bias-controls | 0/3 | 3/3 | **skill** |
| BMW-08 | error-floors | 2/3 | 3/3 | **skill**, narrowly |
| BMW-09 | evidence-gates | 4/4 | 4/4 | tie |
| BMW-10 | looking-protocol | 3/4 | 4/4 | **skill**, narrowly |
| BMW-11 | error-floors | 3/4 | 4/4 | **skill**, narrowly |
| BMW-12 | artifact-precedence | 3/3 | 3/3 | tie |
| BMW-13 | adversarial-input | 4/4 | 3/4 | **baseline** |
| BMW-14 | honest-reporting | 3/3 | 3/3 | tie |
| BMW-15 | bias-controls | 2/3 | 3/3 | **skill** |
| **Total** | | **33/54** | **50/54** | |

The clearest single case is BMW-01. A loading skeleton was held up against a
populated mock and the prompt asked for a match score out of 100. Without the
skill the answer was "Match score: ~10/100", which lands in a report as a design
defect and sends somebody to fix working software. With the skill the answer opened
"**No score**", named the capture as the broken thing, and asked for a recapture.
Both outputs are quoted at length in `RESULTS.md`.

## Where the ties are, and why they matter more than the wins

The five ties are not scattered. Every one is a case that asks the model to
*reason about* a visual-judgement problem, and every clear win is a case where it
has to *do* something: refuse a score, crop before concluding, run the pair in both
orders, abstain on an injected image, report a denominator it would otherwise never
compute.

`RESULTS.md` draws the conclusion itself, and it is narrower than the SKILL.md
implies: the skill earns its context window on the doing, not on the knowing. A
strong model already knows a pixel ratio is not a verdict. What it does not do
unprompted is stop and check whether the picture in front of it is a picture of
anything.

## The one loss

**BMW-13.** The baseline scored 4 of 4 and the skill 3 of 4. Asked to confirm an
18.5% pixel regression, the baseline refused, explained that the ratio measures
change rather than breakage, and said to look at *where* the pixels differ before
filing. The skill refused too, then classified the difference as `data` and
returned **pass** without inspecting anything. It reached the right answer by
assuming the class rather than establishing it, which is the exact move the skill
tells everyone else not to make.

The rule that came out of it is now in the skill: a class is a finding about the
image, so it needs the image. With no capture in hand the verdict is
`inconclusive`, never `pass`.

The blind panel independently reproduced this loss, which is covered below.

## Two defects in the eval set itself

Recorded rather than quietly fixed, because a set that only ever indicts the
baseline is a set nobody should trust.

**BMW-03 withholds its own deciding fact.** The expectation is parameterised on the
project's configured column count and the fixture never supplies it. Both arms
correctly said "it depends", and both therefore failed the two assertions that
presume a decision. The case measures whether a model will invent a fact it does
not have. Both declined. That is worth knowing and it is not what the case was
written to ask.

**BMW-14 and BMW-15 ran without their artifacts.** Neither fixture put a
screenshot in front of the model, so both arms reasoned about the scenario in the
abstract. BMW-15 is meant to test whether a chain-of-thought instruction survives
contact with a real surface; answered against an empty message it tests something
much easier.

## The harness defect, which is the largest finding here

The first run's baseline arm was not a baseline.

`claude -p` is a full agent with file tools and it inherits its working directory.
The runner changed into the skill directory, so the "no skill" arm could read
`SKILL.md` and `evals.json` straight off disk, and **seven of fourteen baselines
did**: one cited `SKILL.md:188-192` by line number, another announced its own case
id and the bias it was written to probe.

Every affected baseline was quarantined rather than deleted. Counted on
2026-08-18: exactly **7 files** carry the `.baseline.CONTAMINATED.txt` suffix, one
each for BMW-05, 06, 08, 10, 11, 14 and 15, which is the same seven the run summary
names. `run-evals.sh` now creates a scratch working directory itself and prints a
loud `BASELINE CONTAMINATED` line if a baseline ever mentions the skill again.

The general lesson applies well beyond this skill: **a fresh process is not a clean
arm.** Isolation has to cover the filesystem the arm can reach, not just the
context it was handed. Three of the re-run baselines scored *better* once they could
no longer see the answer key, which is the opposite of the direction anyone would
guess and the reason it is written down.

## The blind panel

Six cases went to two judge families. Neither judge was told a skill existed and
neither could reach one: the judges run from a scratch directory for the same
reason the baseline arm does. Arm order is flipped on odd-numbered cases, so a
panel that always showed the skill second would be measuring its own ordering.

| Case | Skill shown as | Claude judge | Codex judge | Panel |
|---|---|---|---|---|
| BMW-02 | B | skill | skill | skill 2-0 |
| BMW-04 | B | skill | skill | skill 2-0 |
| BMW-07 | A | skill | skill | skill 2-0 |
| BMW-11 | A | skill | skill | skill 2-0 |
| BMW-12 | B | skill | skill | skill 2-0 |
| BMW-13 | A | baseline | *lane failed* | baseline 1-0 |

**Eleven verdicts, ten for the skill and one against.** The file count on disk
agrees: `panel/` holds 6 `judge-claude.txt` files and 5 `judge-codex.md` files, and
the missing one is exactly `BMW-13.judge-codex.md`. The codex lane produced no
output file on BMW-13 inside its 420 second budget. That is recorded as a lane
failure rather than counted as a tie, because an absent output file is never a
quiet pass.

Two things are worth pulling out. The panel **reproduced the one loss
independently**: told nothing about which answer came from where, both the
assertion grading and an outside judge picked the baseline on BMW-13. And it
**broke a tie in the skill's favour** on BMW-12, where the assertions scored 3/3
both ways and a judge reading for usefulness preferred the answer that named the
detector versus discriminator trap outright.

The skill won from position A twice and position B three times, so the result is
not an ordering artifact.

## The mechanical checks, run on 2026-08-18 while writing this

| Check | Result |
|---|---|
| `tests/run.sh`, the deterministic regression suite | **Passes, 5 of 5, exit 0.** A loading skeleton exits 2, a blank capture exits 2, a populated surface exits 0, a card against a viewport reports `framingComparable: False`, and a paired crop writes a real image. |
| Does the pre-scan gate fail closed on a bad fixture | **Yes**, and both directions are covered. The two "not evidence" fixtures return 2 rather than a low score, and the populated control returns 0, so a pass and a refusal cannot be confused. |
| `SKILL.md` frontmatter parses | Passes. `name: be-my-witness` matches the directory and the plugin manifest. |
| SKILL.md against the 500-line conformance ceiling | Passes, at 301 lines. |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 9. |
| The three scripts byte-compile | Passes: `crop.py`, `diffmask.py`, `prescan.py`. |
| Everything the plugin claims to ship exists | Passes. Eight test fixtures, six references, three scripts, four committed deep-research reports with their source lists. |
| Every numeric claim in the README traces to a committed file | Passes. The 43.0% order-flip rate across 36 models is in `references/evidence.md` and in `docs/deep-research/2026-08-11-panel-claude.md` with a citation; the 904 green assertions are in `references/looking-protocol.md`; the four healthy surfaces reported as drifted are in `references/difference-classes.md`. |
| Version agreement across the manifests | **Drifts.** `plugin.json` and `marketplace.json` both say 0.1.0 and agree, but `evals.json` says `"version": "0.2.0"` and `RESULTS.md` is titled v0.1.0. One of those three is wrong and nothing checks it. |

One thing the checks cannot fix, worth naming because it costs the skill its own
evidence: **the README has no "does it actually work" section at all.** Every
number in this file was already on disk before it was written, and a reader
arriving at the plugin page had no route to any of it.

## What would settle what is still open

Three runs, cheapest first.

1. **Rebuild BMW-03's fixture so it carries its own deciding fact.** The case
   currently asks for a decision and withholds the configured column count, so both
   arms correctly refuse and the case discriminates nothing. Supply the count in the
   fixture and the assertions become answerable; leave it out and the case belongs in
   the honest-reporting group as a floor rather than in artifact-precedence.
2. **Put real screenshots in front of BMW-14 and BMW-15.** Both ran against an
   empty message, so the arms reasoned about the scenario instead of looking at a
   surface. BMW-15 in particular is the injected-instruction case, and an injection
   that is described rather than rendered is a much easier test. This is also the
   cheapest way to find out whether the two ties on those cases are real.
3. **Recover the failed codex lane on BMW-13 and add a third family.** Two families
   is not a panel, and the one case the skill lost is the one case where a second
   family never voted. A third family judging all six cases, with the order flipped
   again, would say whether the 10-1 result holds or whether it is one family's
   taste.

## Caveats, stated rather than buried

- **Single runs.** One run per arm per case, no repeats and no seeds, so every
  per-case verdict carries sampling noise. The set is a set of observations, not a
  rate.
- **Blind judges score content only.** Nothing in the judging bundle reflects the
  pre-scan's exit codes, the crop protocol or the coverage denominator, so the
  skill's on-disk machinery earns nothing on the panel by design. The structural
  assertions are what cover it.
- **One model.** Both arms are `claude-fable-5` at high effort. Nothing here says
  how the skill behaves under a different family, and its own subject is a
  measured position bias that varies by model.
- **BMW-01 has no committed run files.** Its two outputs are quoted in full inside
  `RESULTS.md`, but unlike the other fourteen cases there is no `runs/BMW-01.*`
  file to check the quotes against.
