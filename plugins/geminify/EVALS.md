# Evals

Everything behind the numbers in the [README](README.md): what was run, what it showed, where the skill loses, and what none of it can tell you.

The comparison throughout is **the skill against no skill at all**. There's no predecessor to beat, so the only honest question is whether it earns the context window it costs.

## How it was run

Four arms. Two targets, chosen to sit at opposite ends of the module scan: `be-my-witness`, which renders images, ships probes and enumerates regions, and `clarify`, which renders nothing and ships no probe. Each target got a run with the skill and a run without it.

**The author in every arm is a Gemini model** (`gemini-3.7-flash-high`, via the `agy` CLI), not Claude. That matters twice over: it's out of family from the model that wrote the skill, and it's the family the artifact is written for. So the arms measure the skill, not a Claude model's ability to follow its own instructions.

Both arms are **pure prompt**. No filesystem, no tools, nothing to read. The target's whole `SKILL.md` is pasted in; the skill arm also gets `geminify`'s SKILL.md, both of its references, the bundled Google corpus, and the output its scanner produces when run against that target. That last inclusion is deliberate: the scan is what the skill supplies, so withholding it would have measured a crippled version.

### It took three attempts to build a baseline that wasn't cheating

Worth reading, because the first two looked fine.

**Attempt one** ran both arms with file access, in a copy of the repo. The baseline came back using `[docs]` tags, the phrase "quota ledger", `[measured-family]`, and this skill's own measured numbers. It had gone and read `plugins/geminify` in the same tree, which was sitting right there.

**Attempt two** staged the baseline in a tree with `geminify` removed. The baseline came back clean on a keyword check (zero mentions of the skill by name) and still reproduced the entire vocabulary, including the evidence tiers and the measured run's numbers. It had walked up one directory and found the treatment's copy in a sibling folder.

That's the shape of a check that lies: a keyword grep for "geminify" returned zero on a file that was following the skill closely. **Attempt three** removed the temptation instead of hiding it, by giving neither arm any tools at all. The baselines then came back with zero evidence tags, zero verifiable citations, and their own unsourced technical claims, which is what a genuine baseline looks like.

## Report card: structural assertions

Checkable properties of the artifact, not 1-10 scores. Scores from language models collapse toward the middle; "fifteen quoted vendor sentences, all fifteen verified" doesn't.

| Property | Skill · be-my-witness | No skill · be-my-witness | Skill · clarify | No skill · clarify |
|---|---|---|---|---|
| Evidence tags in the file | **20** | 0 | **21** | 0 |
| Distinct tiers used | 3 | 0 | 3 | 0 |
| Vendor quotes verified verbatim | **15 of 15** | 0 checked | **8 of 8** | 0 checked |
| Epistemic-status block up front | yes | no | yes | no |
| "Unmeasured on this skill" list | yes | no | yes | no |
| Quotes the target's own sentences | 2 | 0 | 3 | 2 |
| Counted deliverables | 2 | 1 | 1 | 1 |
| Reports a delivery fraction | 1 | 0 | **0** | 0 |
| Lines | 143 | 100 | 159 | 102 |

Read against the eval set's four output assertions:

| Eval | Skill · be-my-witness | Skill · clarify | Both baselines |
|---|---|---|---|
| E1 quota ledger with numbers | PASS | **FAIL** | FAIL |
| E2 citations are real | PASS | PASS | FAIL |
| E3 evidence tiers not inflated | PASS | PASS | FAIL |
| E4 no unearned modules | pass, non-discriminating | pass, non-discriminating | pass, non-discriminating |

The verification gate is `scripts/verify_quotes.py`, run against the bundled Google corpus plus the target's own SKILL.md. It pulls every double-quoted span out of a paragraph tagged `[docs]` and requires it to appear verbatim, folding the things honest citation legitimately varies: smart quotes, markdown, line wrapping, nested quote style, `[s]` alterations, elisions, and a quote that ends early on a full stop.

**The baselines score zero on that gate because they cite nothing, not because they cite badly.** Neither baseline puts a single sentence of Google's guidance in quotation marks. What they do instead is state Gemini's internals as fact.

## What the baseline actually wrote

The no-skill file for `be-my-witness` opens with a section on "Visual Tokenization & Image Resolution Geometry" and asserts that Gemini divides images into patches at "typically 258 tokens per tile/crop", that "internal bilinear filtering will still destroy typography below 7 px glyph height", and that the model carries a primacy bias. None of it carries a source. It also names its target models as "Gemini 1.5 Pro, 1.5 Flash, 2.0 Flash, and later", which is a knowledge-cutoff artefact rather than a choice.

Then it invents interfaces. It prescribes `crop.py --tiles --max-dim 1024`, a flag the skill's script doesn't accept, and a `box_2d` field for findings that the skill's verdict schema has no such thing.

That combination is the whole argument for the skill in one file: fluent, specific, confident, and unusable. A maintainer reading it has no way to tell the sourced parts from the invented ones, because nothing is marked.

## Taste test: the blind panel

Structural checks can't say whether a file is any *good*, so each pair went to an out-of-family judge (`grok-4.6` at `xhigh` effort) as Option A and Option B, with neither side identified, no mention that a skill existed, and the judge told to answer from the text alone.

**Each pair was judged twice, in both orders**, because a judge shown the same two things in reverse can produce the reverse verdict.

**The skill won every judgment: 4-0, both orders, both targets.** Presented first it won; presented second it won. No order flip in either pair, which is the result you want from a bias control and not the one you can assume.

On `be-my-witness`, both verdicts named the same defect in the loser, independently:

> "Option A asserts unverifiable Gemini mechanics and an invented `box_2d`/no-tools contract that would displace the skill's schema and script gates."

> "B states unsourced Gemini internals (258-token tiles, bilinear filtering, primacy bias, 'measurable' CoT harm) and adds a `box_2d` finding field as if they were established calibration for this skill."

And both named the same reason for the winner: that its claims were tagged and its `n=0` gaps listed, so they could be checked rather than believed.

On `clarify`, both verdicts again converged on one defect, and it's the same class:

> "B's opening table states Gemini 'tendencies' (sycophancy, menu expansion, 1M-token recall) as facts with no source or measurement, so the overrides cannot be checked and may be wrong."

> "It states Gemini failure modes (sycophancy, menu expansion, 1M-token recall) as operational fact with no source or measurement."

So across four independent judgments of two different pairs, the thing that decided every one of them was the same: whether a maintainer can check the file's claims about Gemini. That is the property the skill is built to produce, and it's the property a capable model does not produce on its own.

| Pair | Order | Winner |
|---|---|---|
| `be-my-witness` | skill first | skill |
| `be-my-witness` | baseline first | skill |
| `clarify` | skill first | skill |
| `clarify` | baseline first | skill |

### The first panel run was not blind, and that's why there were two

The first attempt ran the judge in the eval workspace. Its own trace gives it away:

> "The workspace looks like an eval for these files; I'll check the rubric and any existing `gemini.md` examples before scoring."

It found the skill, the corpus and the eval scaffolding, and judged with all of it in hand. Both of those verdicts also favoured the skill in both orders, and both are discarded from the count above. The blind run was re-staged in an empty directory with tool use forbidden. The verdicts held.

## Where it loses

**E1 fails on `clarify`, which is the skill's own weakest case.** The generated file carries the ledger's machinery, but never reports a delivery fraction, because `clarify` has almost nothing countable in it: the scanner finds a single quota row in its 516 lines. So on a skill whose deliverable is a decision rather than a set of artifacts, the central mechanic has little to bind to, and the file's value falls back on the citation discipline and the tiers. That's a real limit, not a rounding error, and the rule it suggests (derive a count from the skill's own units, or say plainly that there isn't one) is unwritten.

**E4 doesn't discriminate.** The assertion was that a skill which renders nothing should get no capture protocol. Both arms honoured that: zero visual references in either `clarify` file, against 14 and 10 in the `be-my-witness` files. The module scan is doing the right thing, and so is a Gemini model with no skill at all, so the eval measures nothing. It's kept as a regression guard rather than as evidence.

**The skill's files are longer.** 143 against 100 lines, and 159 against 102. Some of that is the epistemic block and the tier tags, which is the cost of being checkable. Whether the rest earns its length is unmeasured.

## The scanner's own numbers

`scripts/scan_skill.py` is the skill's central mechanic, and two versions of it were wrong in ways that would have shipped quietly.

**Version one fired 7 of 8 modules on `clarify`.** A skill that renders nothing, ships no probe and spawns no agent was being told to write a capture protocol and a gate section. A classifier that says yes to everything discriminates as poorly as a gate that always passes. Fixed with a three-trigger threshold and more distinctive trigger words: `clarify` now triggers one module.

**Version one of the quota regex returned 83 rows for a 292-line skill.** Nearly all of them were ordinary prose distributives ("each traced", "every request", "any model"), burying the four real ones. Restricted to a vocabulary of countable deliverables it returns 26, with distributives counted but never listed.

What it looks like now, measured across four skills:

| Target | Quota rows | Top module | Modules fired |
|---|---|---|---|
| `design-craft` | 26 | `visual` (11 hits) | several |
| `deck-craft` | not counted | `authorship` (11) | several |
| `design-review` | not counted | `gate` (10) | several |
| `clarify` | **1** | none | **1** |

## The gate caught the thing it was built for, then caught itself

`verify_quotes.py` exists because of one mistake. While the first five of these files were being written by hand, the sentence "Verification is prompted rather than automatic" was put in quotation marks and attributed to Google in three separate files. Google never wrote it. It's a fair paraphrase of two real passages, promoted to a citation by the quote marks, and no amount of re-reading caught it.

On its first real run the same script caught a second defect nobody had noticed: a vendor clause quoted with three words missing.

Current state on those five hand-authored files: **60 of 60 vendor quotes verify** (16, 8, 7, 16 and 13 respectively). A negative control with an invented quote exits 1.

**And then the gate went green by accident.** A one-line change to its normaliser, added so `provide[s]` would match its source, also deleted the `[docs]` tag it was being asked about. Every file then reported `0 presented as [docs] claims` and the whole gate passed, negative control included. That was caught only because the negative control was re-run rather than assumed. It's the best argument in the skill for its own rule about proving a gate can fail, and it's why the tag is now detected on the raw paragraph.

The scorer used in this document had the same class of bug: it looked for `checked=` in the gate's output, which the gate has never printed, and reported zero verified citations for all four arms. On a file carrying fifteen verified citations. Assert against the probe's real return shape, or the numbers you publish are your regex's opinion.

## Costs

No metered API spend on the evals. The four arms and the judgments all ran on subscription CLIs (`agy` for the four authoring runs plus six discarded ones, `grok` for six judgments of which four count). The icon commission spent two billed image generations, one raster and one vector. No paid research panel was bought, because Google's own prompting corpus was already loaded in session and is the primary source a panel would have gone looking for.

## What none of this establishes

- **No rate for anything.** The family evidence behind the skill's rules is one recorded Gemini run on one brief in one domain. Everything derived from it is one honest data point that agrees with Google's published guidance, not a law.
- **No evidence the generated files work in production.** Nobody has run a skill under Gemini with its `gemini.md` in place and compared the delivered artifact against the same skill without one. That is the obvious next measurement, and it hasn't been made. Every number here is about the *file*, not about what a model does after reading it.
- **One judge family, four judgments.** Four for four in both orders is a clean result within one family, and one family is still not a panel. A second and third family would be the cheapest way to strengthen it.
- **Both arms are one sample each.** No repeats, no seeds, so run-to-run variance is unmeasured.
- **Nothing about other Gemini versions.** One model, one effort setting. The knowledge cutoff and the `thinking_level` default differ across the 3.x family.
