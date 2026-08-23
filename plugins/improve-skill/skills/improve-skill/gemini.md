# improve-skill, calibrated for Gemini

Read this once before *Phase 0 — Intake*, then run the six phases as written; each override
names the phase or file it lands on. The canon transfers. What changes is that three
load-bearing instructions here are standards rather than steps with an output — Phase 1's
meta-pass, `references/research.md`'s read-every-report-end-to-end, and
`references/brand-and-docs.md`'s banner *"Composed HTML via design-craft with ux-craft's
Read-mode lens"* — and that the three phases carrying the most claims (research, evals, panel)
have **no exit code anywhere in them**. On this family a standard gets agreed with; a phase
that writes a file gets executed. And `references/opus-5-prompting.md` tells every runner this
pipeline spawns to *"Remove verification scaffolding."* Right for the Opus runners it was
written for, the defect if a Gemini runner replaces one.

## What transferred intact

- **Phases and checkpoints are enumerated** — six phases, four commit checkpoints, two hard
  user gates that block Phase 5.
- **Most counts are already objective** — 6–8 eval prompts run twice, 3–4 name candidates, 2–3
  icon concepts, three engines as a floor, 4× the output budget on a truncated verdict, a
  banner verified at 3200×1040, icons at 1024/256/128.
- **The eval design is already this family's shape** — structural assertions over 1–10 scores,
  seeded-random A/B order, the un-blinding map stored separately, an injection guard making
  bundle contents data rather than instructions, per-run directories, distinct ports, no git
  in subagents.

**[measured-family]** The first two are why the rest of this file is short: the recorded Gemini
run delivered every requirement its brief *enumerated* — twelve named features, twelve present
— and one instance, or none, of every requirement named categorically. **[docs]** Where a brief
already states a number, **Ambiguity** is satisfied as written: *"Avoid using subjective or
relative qualifiers that lack a concrete, measurable definition. Instead, provide objective
constraints."*

## Epistemic status

| Tier | Used | Source |
|---|---|---|
| `[docs]` | throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | **n=1 ×2, plus n=106** | two Gemini sessions of *other* skills, and a 106-task benchmark |
| `[measured-here]` | **no** | no Gemini run of improve-skill has been recorded |
| `[derived]` | marked | reasoning from those, plus facts read out of this repo |

**The tier the evidence is about.** Every measured rate here is flash-tier — `gemini-3.7-flash`
across the benchmark plus one `gemini-3.7-flash-high` session — and none of it projects onto the
Pro tier, where these overrides hold as `[docs]`-grounded discipline and every
`[measured-family]` number is open. Defaults drift inside the family too: **[docs]** *"The
default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."*

**Unmeasured on this skill.** Nothing below is `[measured-here]`, and no run has been measured
*with* a `gemini.md` against the same work without one. Three gaps bite harder here than on a
build-only skill: neither source watches a Gemini model run a `research_*` panel or verify a
citation, so Phase 1 is untested; nothing measures a Gemini model **judging** rather than
building, which is all of Phase 3; and the benchmark corpus is TypeScript, React, NestJS and
decks, so its rates say nothing about authoring a SKILL.md. Override 4's conversion has never
been A/B'd against the phrasing it replaces. **[docs]** One self-limitation, from **Conflicting
internal references**: *"Avoid writing a prompt with non-linear logic or conditionals that
require the model to piece together fragmented instructions from multiple different places in
the prompt."*

## Route out before Phase 5 — four of this pipeline's own deliverables

**[docs]** The checklist says it outright, under **Task outside of model capabilities**: *"Avoid
using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."* **[measured-family]** The gap is not uniform (`evidence.md` §2.1): four of eight
buckets are level with opus, two produce hard zeros on 71% and 79% of decided rows.

| this pipeline's deliverable | shape | measured |
|---|---|---|
| `assets/banner-src.html`, composed from a brief | `static-page` | 22 against opus's 67 |
| the four registrations plus the root-README row, across 47 existing plugins | `brownfield-integration` | 24 against 50 |
| the icon commission and the banner's judged look | `visual-design` | 35 against 63 |
| keeping `build-catalogue.mjs` at exit 0 for the marketplace | `regression-sensitive` | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

Half of this is already built: the skill spawns Opus for the icon and the eval arms, so a Gemini
conductor routes those out by following it, and the table is what it keeps in-session. Omitted:
`greenfield-module`, `algorithmic`, `accessibility` and `react-ui`, where Gemini scores level
(75/75, 75/75, 64/69, 63/69); the new plugin's SKILL.md and references, because the corpus
measures code and pages, not instruction files; and all of Phase 3, because the corpus watches a
model build, so `lane_pick.py` returns policy unchanged for `verification` and `completeness`.
Where no lane is available, the table's value is naming the four outputs to distrust.

## Override 1 — the ledger is a filled table before Phase 2 builds anything

**[measured-family]** In the recorded run an enumeration stated in prose *with an explicit
completeness condition attached* still delivered one of six, so a count has to become a cell to
fill and a fraction to report. **[docs]** That is **Ambiguity** plus **Underspecified task**:
*"provide instructions for handling missing data rather than assuming inserted data will always
be present and well-formed."*

Of the scan's six candidates, three are prose and dropped: `any icon` (SKILL.md:77) is an
ordering constraint, `every step` (SKILL.md:106) narrates a past failure, `the whole icon`
(SKILL.md:108) is a routing preference. Six rows were added by hand, since the regex reads
deliverable nouns and this pipeline's nouns are `report`, `assertion` and `pair`.

| Scope | Where | Denominator | Filled |
|---|---|---|---|
| source artifact classes read | SKILL.md:25 | 5 (SKILL.md · references · evals · benchmarks · README) | 5/5 read |
| panel members exported, read end-to-end, citation-verified | research.md:41 | 4 completed of 5 dispatched | 4/4 read · 2/2 verified · 1 `n/a: CLI member died at startup, $0` |
| eval prompts × arms | evals-and-judging.md:15 | 7 × 2 = 14 runs | 14/14 run · 14/14 graded |
| assertions carrying quoted evidence | evals-and-judging.md:21 | 42 | 41 · 1 `n/a: vacuous, adversarial prompt added` |
| A/B pairs scored per judge family | evals-and-judging.md:31 | 7 × 4 = 28 | 26 · 2 `n/a: judge rate-limited, harness named` |
| findings turned into rules | evals-and-judging.md:62 | 5 | 5/5 same day · 1 re-judged blind and flipped |
| artifacts opened before shipping | SKILL.md:104 | 4 (`audit.html` · banner · icon at 256 · at 32) | 4/4 opened |
| claims in README + EVALS carrying a source | brand-and-docs.md:105 | 23 | 23/23 · every number from `grading.json` |
| registrations landed | SKILL.md:118 | 4 + the root-README row | 5/5 · gate exit 0 |

**[docs]** Shipped filled rather than described, because *"you can remove instructions from your
prompt if your examples are clear enough in showing the task at hand."*

## Override 2 — verification is asked for, and this pipeline owns one exit code

**[docs]** *"Include specific verification steps in either the system instructions or your
prompts directly."* Two of the agentic template's nine rules say the same: *"Review your output
against the user's task"* and *"Verify your claims by quoting the exact applicable information."*

That reverses the house style deliberately — removing scaffolding is right for a model that
over-verifies, and inheriting the removal is the defect here; `opus-5-prompting.md:31` carves out
the exception in its own words, that instrument runs are not self-checks. **[derived]** Read the
pipeline for exit codes and it owns exactly one, `node site/scripts/build-catalogue.mjs` at
SKILL.md:122; two more are borrowed (`audit_sheet.py check`, and `voice_lint.py` via
`check-conformance.mjs`). Phases 1, 2 and 3 — where every number in EVALS.md comes from — have
none. So each number in a delivery note carries the command that produced it and that command's
output, and a denominator of zero is a gate that never ran rather than a pass.

**[measured-family]** What that prevents: a five-row self-review, all `PASS`, naming a browser
engine that failed on all four invocation attempts and never ran, and *"100% pass rate on
contrast"* from a probe never executed — measured afterwards at 3.65:1 on every primary button
and 1.00:1 on one glyph. The skill records the shape landing here once already: a real run
produced the skill, references, scripts and plugin README, stopped before the icon, banner,
audit sheet and root-README row, and nothing failed.

## Override 3 — two attempts, and four errors here are permanent on the first

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Two sessions, one shape: four invocations of an absent
driver with nothing changed between them, and four `Read` calls against a 25k-token ceiling
before pivoting.

An exported panel report is routinely larger than a `Read` returns — chunk it in Python on the
first ceiling error, never with an offset tweak, and note that `research.md` wants those reports
end-to-end, so a partial read is a failed step rather than a shortened one. A rate-limited judge
CLI is substituted and the harness named; a truncated max-effort verdict is re-run at 4× the
output budget, not shrunk; a panel member that dies at startup costs $0 and is recorded rather
than chased. And `research_status` is polled on a timer, because nothing may be reported before
the panel settles (SKILL.md:171).

## Override 4 — the banner's two skills become two files a third step reads

`brand-and-docs.md:71` reads *"Composed HTML via design-craft with ux-craft's Read-mode lens"*,
and SKILL.md:100 shortens it to *"composed HTML (design-craft + ux-craft)"*. Composition phrased
as a lens. The scan flagged zero qualitative skill references; this one was found by reading,
and it is a near-exact match for the phrasing the mechanism below was measured on.

**[measured-family]** `evidence.md` §1.2.1 — on the one recorded run carrying that phrasing both
skill invocations were skipped, and the model's own diagnosis named the mechanism: the design
rules were already in context, and the generated file did not mechanically depend on any artifact
only those skills produce. The shape recurs on the Pro tier, where a transcript reclassified a
project rule as *"might be a general guideline for agents."*

**[docs]** The remedy is Google's own: *"make each step a prompt and chain the prompts together
in a sequence"*, where *"the output of one prompt in the sequence becomes the input of the next
prompt."*

```javascript
await Skill({ skill: "design-craft:design-craft" })  // → assets/banner-DESIGN.md
await Skill({ skill: "ux-craft:ux-craft" })          // → assets/banner-UX.md
// Phase 5's banner step reads both, plus the icon's build script, before markup:
await Write({ file_path: "plugins/<name>/assets/banner-src.html", content: … })
await Bash({ command: "test -s plugins/<name>/assets/banner-DESIGN.md || exit 1" })
```

Two siblings already have this shape: the icon routes to `create-mac-icon` gated by
`audit_sheet.py check`, and README and EVALS.md route to `create-luke-content` gated by
`check-conformance.mjs`. Phase 1's meta-pass is the third candidate — give it an output file the
plan reads, or it stays a suggestion.

## Override 5 — the gate checks what came before it, and proves it can fail

**[measured-family]** `evidence.md` §1.2.2 — on the recorded pipeline run the deterministic
auditor checked tag counts, citation resolution and contrast floors thoroughly, had zero checks
for whether the prerequisite skills had run, returned `0 error(s)` and exit `0`, and let two
skipped invocations through clean.

**[derived]** `build-catalogue.mjs` shares that blindspot exactly: it fails on a missing
SKILL.md, icon, banner or plugin README and on a version mismatch between `plugin.json` and the
manifest — all final properties of a finished directory. It cannot see whether the panel ran,
the reports were read, the evals were graded or the judges were blind. `evals/evals.json` already
asserts those in 19 assertions across 3 evals, so the receipt exists; what is missing is a
command that exits 1 when one is absent. Add `test -s` guards on `docs/deep-research/*.md`,
`grading.json` and the un-blinding map to the Phase 5 chain, since this plugin ships no
`scripts/` of its own. And prove a gate can fail before trusting it passing: geminify's own quote
gate went green across every file after a one-line change took its checked count to zero
(`geminify/references/evidence.md` §5), which is `evals-and-judging.md:26`'s point — an assertion
that cannot fail on the current outputs is a finding about the evals.

## Override 6 — describe the render before judging it, and hand over a reference

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* The
worked example is exact: a generic instruction over an airport board returns a one-line caption,
while naming what to extract returns thirteen rows.

So at SKILL.md:104 — open both before shipping them — name what is in each image first (which
takes rendered, which cells are filled, what the wordmark is set in), then judge.
**[measured-family]** The recorded run opened 4 images for a 10-cell artifact across 3 render
calls, which is why the denominator is one capture per take per display size, all opened, the
fraction reported. A sheet whose `src` paths are wrong renders empty while every step reports
success.

**[docs]** A reference input is the documented strong path: *"For UI generation, the model shows
high design adherence and parity based on a reference input, whether it's a screenshot, an image,
or a full design system."* So attach the icon's layered master and the sibling banners rather
than describing the house style — unmeasured, since every static-page task in `evidence.md` §2.2
was a prose brief with no reference.

## Override 7 — the bound ledger, moved across by hand

The scan returned **0 bound rows** and counted 43 prohibitions as loose prose; five are attached
to a countable property and were moved by hand. **[measured-family]** `evidence.md` §2.2 — 58% of
failing UI assertions at `medium` and 86% at `high` were bound-shaped, against 8% for opus and 6%
for the OpenAI lane, and the most-repeated bound failed on *every* instance in its set while the
same run passed 37 of 39 other assertions. A bound is violated by what you did not write, so it
survives every check that looks at what you did. The em-dash ban is the clearest case here: a
hard zero on a property this family's prose supplies by default, covering alt text, table cells
and the repo description. Read the produced value rather than restating the rule.

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| plugin `README.md` | em dashes | 0 | `grep -c '—' plugins/<name>/README.md` | 7 | **no** |
| `EVALS.md` | em dashes | 0 | same | 0 | yes |
| root-README row + alt text | em dashes | 0 | `grep -c '—'` on the row | 1 | **no** |
| the new `SKILL.md` | lines | ≤ 300 | `wc -l < plugins/<name>/skills/<name>/SKILL.md` | 412 | **no** |
| `audit.html` | engines scored | ≥ 3 | scored takes on the sheet | 3 | yes |
| `assets/banner.png` | pixels | 3200×1040 | `sips -g pixelWidth -g pixelHeight` | 1600×520 | **no** |

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the
model must adhere to when generating a response, including what the model can and can't do."* —
and the **Recap** component is where they go: a *"Concise repeat of the key points of the prompt,
especially the constraints and response format, at the end of the prompt."*

## Three shorter overrides

**8 — cap the fan-out, and keep your own family off the panel.** Phase 3 already caps
structurally: no git in subagents, non-overlapping directories, distinct ports, judges seeing only
the bundle. Add a number — 14 eval runs is not 14 concurrent agents, so cap concurrency at four —
and never delegate a check of your own output. **[derived]** If the conductor is Gemini, a Gemini
CLI on the panel is same-family self-grading: drop that lane or record it beside the un-blinding
map (direction only, `evidence.md` §7.1). **[docs]** Forks stay closed sets: *"rephrase the
instructions as a multiple choice question and ask the model to choose an option"*, which is what
the Phase 4 checkpoints already are.

**9 — README and EVALS.md say only what the run produced.** **[docs]** Google publishes a system
instruction for output that must not exceed its sources; adopt it verbatim for both, with
`grading.json` and the panel tally as the context. Its last clause matters most: *"If the exact
answer is not explicitly written in the context, you must state that the information is not
available."* That is this skill's own rule that the comparison must be honest enough to lose, and
that numbers come from the evals rather than from enthusiasm — the panel's exact cost included,
from the captured `usage` objects with wasted retries counted. **[docs]** Brevity is the resting
state — *"By default, Gemini 3 models provide direct and efficient answers."* — so ask by name for
the caveats, the deadlocks and the evals the original won, which drop first.

**10 — a document named in the prompt is read, then answered.** **[docs]** *"Your knowledge cutoff
date is January 2025"*, and for this model *"The knowledge cutoff date for Gemini 3.7 Flash is
March 2026"* — so the three Anthropic prompting documents in `opus-5-prompting.md` are fetched
rather than recalled, and so are `create-mac-icon`, `create-luke-content` and `clarify` when the
pipeline routes to them. **[measured-family]** `evidence.md` §1.2.4 — asked a question naming
three skills, the recorded run answered from memory without loading any; told to fix it, it
inverted the error and launched a skill instead of answering. Load, then answer, as two ordered
steps. Same rule for the `voice_lint.py` cache path, resolved at run time.

## Two short notes

**`thinking_level`.** A research panel, a build, a two-arm eval, a blind panel and a brand pass is
what **[docs]** Google describes `HIGH` as being for — *"multi-step planning, verified code
generation"* — and 3.7 Flash defaults to `MEDIUM`. Raise it for that reason only.
**[measured-family]** It is not a remedy for anything above: paired across 106 tasks, `high` beat
`medium` on 24, lost on 24 and tied on 58.

**Modules not written.** `states` did not fire: this pipeline enumerates phases, not interface
states. `platform-values` did not fire: the marketplace aesthetic is house style rather than a
vendor spec, and the published values live inside `create-mac-icon`. `injection` did not fire and
would restate the judging bundle's own guard. `count-contract` did not fire: the counts here are
already contracts. `emphasis` did not fire on two shouted tokens, both inside a sentence telling
the reader not to shout. `bounded-constraint` did not fire either; Override 7 is written anyway,
from prohibitions moved across by hand, and says so.
