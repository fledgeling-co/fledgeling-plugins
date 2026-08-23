# proctor, calibrated for Gemini

Read this in one pass before *What Proctor observes*, then run the seven stages
as written; each override names the section it lands on. The skill's thesis is
already the fix — *"a screenshot you looked at is an impression, a screenshot
with a frame status and a dirty-rect summary is an instrument reading"* is what
the one recorded Gemini failure collapsed. What changes on this family is that a
reading gets *claimed* where the instrument was meant to be read. proctor ships
no `scripts/`, so every instrument is an MCP tool return rather than an exit
code, and Override 1 is written against that.

## What transferred intact

- **The verdict vocabulary is already closed sets** — `granted`/`denied`/
  `unconfirmed`, `targetChanged`/`screenChanged`/`deliveredOnly`/`refused`,
  `ok`/`refused`/`indeterminate`. **[docs]** Google's remedy for answers out of
  bounds is to *"rephrase the instructions as a multiple choice question and ask
  the model to choose an option."*
- **The counts are already objective** — seven stages, seventeen assertion kinds,
  five stability runs, a fan-out capped at four, thirteen content and nine
  environment states enumerated in `references/methodology.md`. **[docs]** Under
  **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a
  concrete, measurable definition."* The traps section is a worked example set —
  **[docs]** *"We recommend to always include few-shot examples in your prompts."*

## Epistemic status

| Tier | Used | Source |
|---|---|---|
| `[docs]` | throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | n=1 run · n=106 tasks | `Egress Gemini` and `COD Dossier`, sessions of *other* skills; the `diolog-2.0` benchmark |
| `[measured-here]` | **no** | no Gemini run of proctor has been recorded |
| `[derived]` | marked | reasoning from the two above |

**Which model these numbers are about.** Every measured claim is flash-tier — the
benchmark rows are `gemini-3.7-flash` at `medium` and `high`, the two sessions
likewise. Do not project any of it onto the Pro tier: there the overrides hold as
`[docs]`-grounded discipline while every rate is open. Defaults differ too.
**[docs]** *"If thinking_level is not specified, Gemini 3 will default to high"*,
then *"The default thinking effort is now medium, changed from high in Gemini 3
Flash Preview."*

**Unmeasured on this skill:** nothing below is `[measured-here]`, and no run has
been measured *with* a `gemini.md` against the same work without one. The
benchmark watches a model *build*, not *test*, so Override 3's rate and the
routing figure are borrowed. Nothing about MCP returns, the iOS or guest lanes,
`cua` or `proctor_stability`. **[docs]** One self-limitation: *"Avoid writing a
prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions from multiple different places in the prompt."*

## Route out before the campaign starts

The campaign does not route out: **[measured-family]** the benchmark watches a
model build things, not drive an app or grade a flow. One lane differs —
authoring XCTest targets into the codebase edits an existing multi-file project
under compound acceptance criteria, the shape that collapsed hardest. **[docs]**
Under **Task outside of model capabilities**: *"Avoid using prompts that ask the
model to perform a task for which it has a known, fundamental limitation."*

| shape | proctor's work that lands in it | measured |
|---|---|---|
| `brownfield-integration` | authoring XCTest / Swift Testing targets into an existing Xcode or SPM project | 16 against opus's 46, hard zero on 79% of decided rows |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

Omitted: `static-page` (proctor authors no self-contained page), `visual-design`
(the skill routes *"does this look any good"* to `design-review`) and
`regression-sensitive` (proctor is read-only on the app under test).

## Override 1 — a tool return is quoted, or the claim is deleted

Lands on *Before anything else*, stages 4–6, and *Report*. **[docs]** *"Include
specific verification steps in either the system instructions or your prompts
directly."*, *"Review your output against the user's task"*, and *"Verify your
claims by quoting the exact applicable information (including policies) when
referring to them."* Stripping verification scaffolding suits a model that
over-verifies; inheriting that removal is the defect here.

**[measured-family]** The n=1 run filled that vacuum with a review asserting
*"Engine Verified: Google Chrome via `browser-use` CDP Harness"* for a driver
that failed all four invocations, and a 100% contrast pass rate never measured.

- **Every claim carries the tool, its arguments and the field it rests on** — not
  "contrast passes" but `proctor_assert` with `kind: contrast` scoped to
  `AXStaticText`, returning `passed:false` and an observed `3.65` on node 512.
- **`passed:true` over an empty node set is a predicate that matched nothing.**
  Print the population: `hasLabel` over nineteen `AXButton` nodes is a result,
  the same assertion resolving zero is a gate that never ran. And *"An assertion
  that could not be evaluated is not an assertion that passed"* — two integers.
- **A skipped prerequisite leaves its rows open, not passed.**
  **[measured-family]** on `COD Dossier` the auditor checked the final artifact
  thoroughly, never checked that the upstream skills had run, and returned exit 0
  over two invocations that never happened. Proctor's gates are returns, so the
  receipt is the return: a fidelity row needs a `be-my-witness` result quoted, a
  conformance row `native-foundation.md` read *this run*, an actuating stage
  `proctor_doctor`'s `lanes[]` row. A row without one is `n/a: prerequisite`.

## Override 2 — the ledger is a filled table before the first `proctor_act`

Lands on stage 2, stage 3 and the state matrix in `references/methodology.md`,
which already ask for it — *"Build the case-to-evidence matrix first"*.
**[measured-family]** in the recorded run an enumeration stated in prose, with an
explicit completeness condition attached, still delivered one of six. Filled:

| Scope | Where | Denominator | Filled |
|---|---|---|---|
| criteria as matrix rows | SKILL.md:305 | 11 criteria | 8 covered · 2 partial · 1 gap |
| menu items inventoried vs exercised | SKILL.md:320 | 62 from `proctor_menu` | 62 read · 14 exercised · 48 `n/a: inventory only` |
| captures, one per state | SKILL.md:398 | 13 states | 11 trustworthy · 2 `n/a: off-screen, recaptured raised` |
| state-matrix cells | methodology.md:13 | 13 content + 9 environment + 3 crossings = 25 | 17 run · 8 `n/a` with reasons |
| fidelity ledger rows | methodology.md:256 | 41 elements × 5 surfaces = 205 | 168 present · 24 divergent · 13 absent |

Every `n/a` carries its reason and delivery reports the fraction. **[docs]**
**Underspecified task**: *"provide instructions for handling missing data rather
than assuming inserted data will always be present and well-formed."*

## Override 3 — every bound is read back off the artifact

Lands on *Delegating*, *Scale*, stage 7 and the fidelity ledger. Override 2
catches a categorical scope collapsing to one instance; this catches the
opposite, the failure that reaches a report looking complete.
**[measured-family]** across 106 benchmark tasks, 58% of failing UI assertions at
`medium` and **86%** at `high` stated a bound rather than asked for a thing,
against 8% for opus, and the most-repeated bound failed on *every* instance:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| campaign | subagent fan-out | at most 4 | count of spawns in the session | 3 | yes |
| campaign | untrustworthy captures cited as evidence | 0 | cited ids ∩ returns with `trustworthy:false` | 0 (2 existed, both re-taken raised) | yes |
| report | skipped assertions counted as passes | 0 | the two integers printed separately | 17 run · 3 skipped | yes |
| fidelity ledger | rows per element per surface | exactly 1 | row count vs 41 × 5 | 205 | yes |

Two of those began as prohibitions in this skill's prose — *"Never treat an
untrustworthy frame as evidence"* and the skipped-assertion rule above — and the
conversion is the point: a prohibition reads as style advice, a counted property
with a readback does not. **[docs]** Google places it at the end deliberately, as
the **Recap** component: a *"Concise repeat of the key points of the prompt,
especially the constraints and response format, at the end of the prompt."*

## Override 4 — two attempts, and `proctor_doctor` first

Lands on *Before anything else*. **[docs]** *"On *other* errors, you must change
your strategy or arguments, not repeat the same failed call."* **[measured-family]**
four consecutive invocations of one absent driver, unchanged between attempts.
`proctor_doctor` is the whole defence: *"It costs one call and it is the
difference between a campaign and an hour of retries."* Read `lanes[]` before
planning. A missing Accessibility grant reads exactly like a selector bug, so two
`nodeNotFound` in a row sends you to `grants[]`.

**A capacity error pivots on attempt 1.** **[measured-family]** the `COD Dossier`
run met a hard token ceiling on `Read` and retried the same call four times with
minor tweaks before changing approach. `references/tools.md` is 1,009 lines, so
the first truncation goes to a line-ranged read or a `proctor_find` predicate.

## Override 5 — seven passes, not one sweep

Lands on *The campaign*. **[docs]** Under **Too many tasks**, a prompt asking for
*"several distinct cognitive actions in a single pass"* is *"trying to accomplish
too much. Break the requests into separate prompts."* The remedy is the skill's
own structure: *"make each step a prompt and chain the prompts together in a
sequence."* The scan found no qualitative skill composition needing conversion —
proctor's hand-offs already return an artifact — and **[measured-family]** the
one recorded skipped-invocation case turned on nothing depending on a file only
that skill produced, so a stage 5 row is filled by the returned classification.

## Override 6 — describe the crop before judging it

Lands on stage 5 and every use of `proctor_zoom`. **[docs]** *"Ask the model to
describe the images before performing the task in the prompt."* Their example is
exact: a generic instruction over an airport board returns a one-line caption,
naming what to extract returns thirteen rows. And *"To improve the response,
point out which parts of the image are most relevant to the prompt"*.

- Per capture, **name what is in it first** — regions, copy, visible spacing —
  then judge; a verdict without that step is the generic caption wearing the
  specific answer's authority. When a finding looks wrong, *"Read the metadata
  rather than the image"*, since `trustworthy: false` *"means this capture is not
  evidence of anything, whatever it looks like when opened"*. A crop you rendered
  and did not open leaves its row open too.
- **Supply the reference when one exists.** **[docs]** *"For UI generation, the
  model shows high design adherence and parity based on a reference input,
  whether it's a screenshot, an image, or a full design system."* Stage 5 has
  both halves — mock slices for `be-my-witness`, `native-foundation.md` for the
  mockup-free case. Unmeasured: every measured task was a prose brief.

## Override 7 — platform numbers are read, never recalled

Lands on *Native Conformance Rubric* and the accessibility rubric in
`references/methodology.md`. **[docs]** *"Your knowledge cutoff date is January
2025."* **[measured-family]** the recorded run put Windows 10's accent colour on
a Windows 11 app, a previous-generation value returned confidently. macOS 27's
ladder sits in that zone; a cell you cannot source is one you invented.

| Property | Value | Source |
|---|---|---|
| Body text size, control heights, spacing unit | 13pt, kit tier ladder, 8pt grid | the native-conformance rubric's `native-foundation.md`, read this run |
| Contrast floors | 4.5:1 body, 3:1 large and non-text | `methodology.md` §Contrast thresholds (WCAG 1.4.3 AA) |
| Hit-target floor / aspiration | 24 × 24 gate, 44 note | same §Hit-target minimums (SC 2.5.8 / 2.5.5) |

**The same rule covers files: read, then answer.** **[measured-family]** asked a
question naming three skills, the recorded run answered from memory without
loading any, then over-corrected and launched a skill instead of answering. When
a prompt or this skill names `references/tools.md` or `native-foundation.md`,
load it and then write the answer — two ordered steps. **[docs]** *"Grounding
with Google Search connects the Gemini model to real-time web content, and should
be enabled whenever the model may need to know obscure or recent facts."*

## Override 8 — the report says only what the run observed

Lands on stage 7 and *Disclosure requirements*. **[docs]** Google's system
instruction for output that must not exceed its sources ends where it matters:
*"If the exact answer is not explicitly written in the context, you must state
that the information is not available."* The context is this campaign's tool
returns. **[docs]** Brevity is the resting state — *"By default, Gemini 3 models
provide direct and efficient answers"* — and the sections that drop first are
*Not covered* and *Methods*. So: **Verdict, What was proven, Defects, Flaky, Not
covered, Methods — six headings, always present, `none` where a section is
empty.** **[docs]** One filled example, since *"you can remove instructions from
your prompt if your examples are clear enough in showing the task at hand"*:

> **Methods.** macOS 26.4 (24E5228a); `agentBuild` `1.4.0+2291`. Lane `native` on
> every step (`backend:"native"`, 118 steps). `AXManualAccessibility` applied —
> Electron host — so timing findings are about the instrumented app; the four
> label findings are not. Settle: 101 `allSignalsQuiet`, 14 `axQuietOnly` with
> `captureNeverQuiet` (live spinner), 3 `timeout`, reported as inconclusive
> rather than as defects. Captures: 13 taken, 2 `trustworthy:false` (off-screen)
> and re-taken raised. No reflector, so every colour is a post-compositing read.

## Two short notes

**Delegation, and `thinking_level`.** *Delegating* already caps the fan-out at
four. Never delegate verification of a result you produced — a judgement in a
measurement's position is the family failure — and **[docs]** prefer the tool
call over the question on a low-risk read: *"Prefer calling the tool with the
available information over asking the user, unless"* a later step needs the
missing parameter. A seven-stage campaign is what **[docs]** Google describes
`HIGH` as being for — *"multi-step planning, verified code generation"*; 3.7
Flash defaults to `MEDIUM`, and the uplift here is unmeasured. It is not a remedy
for anything above: **[measured-family]** paired across 106 tasks, `high` beat
`medium` on 24, lost on 24, tied on 58.

**Modules not written.** `injection` did not fire: the skill ingests no
third-party text as instructions, and the adjacent case, an app's own self-review,
is handled in Override 1. `emphasis` did not fire either — zero shouted
directives in 2,645 lines, which **[docs]** is the right register: *"Avoid
unnecessary or overly persuasive language."*
