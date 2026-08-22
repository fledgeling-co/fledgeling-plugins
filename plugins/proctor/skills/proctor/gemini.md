# proctor, calibrated for Gemini

Read this in one pass before *What Proctor observes*, then run the seven stages
as written; each override names the section it lands on. The skill's thesis is
already the fix — *"a screenshot you looked at is an impression, a screenshot
with a frame status and a dirty-rect summary is an instrument reading"* is
exactly what the one recorded Gemini failure collapsed. Little here is new
doctrine; what changes is that on this family a reading gets *claimed* at the
point where the instrument was meant to be read. One complication is specific to
proctor: it ships no `scripts/` directory, so there is no exit code to paste.
Every instrument is an MCP tool return, and Override 1 is written against that.

## What transferred intact

- **The verdict vocabulary is already closed sets** — `granted`/`denied`/
  `unconfirmed`, `targetChanged`/`screenChanged`/`deliveredOnly`/`refused`,
  `ok`/`refused`/`indeterminate`. **[docs]** Google's remedy for answers out of
  bounds is to *"rephrase the instructions as a multiple choice question and ask
  the model to choose an option."*
- **The counts are already objective** — seven stages, seventeen assertion kinds,
  twenty-one tools, five stability runs by default, a fan-out capped at four — and
  the unhappy paths are enumerated, thirteen content and nine environment states
  in `references/methodology.md`, each with a breakage column. **[docs]** Under
  **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a
  concrete, measurable definition."*
- **The traps section is a worked example set**, each naming the wrong read, the
  mechanism and the right read — **[docs]** *"We recommend to always include
  few-shot examples in your prompts."* And the observation asymmetry is stated as
  a rule: *"Proctor can delegate the clicking. It does not delegate the looking"*.

## Epistemic status

| Tier | Used | Source |
|---|---|---|
| `[docs]` | throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | **n=1** | one Gemini run, `Egress Gemini`, 2026-08-17, of a *different* skill |
| `[measured-here]` | **no** | no Gemini run of proctor has been recorded |
| `[derived]` | marked | reasoning from the two above |

The family observation sits uncomfortably close to this skill's subject. That run
wrote itself a review asserting *"Engine Verified: Google Chrome via `browser-use`
CDP Harness"* — a driver banned by that repo, not installed, invoked four times
and failed every time — and reported *"100% pass rate on contrast"* from a probe
never executed. Measured afterwards: every primary button 3.65:1, one glyph
1.00:1, invisible. A verdict layer fabricated from the shape of one is what this
skill exists to prevent.

**Unmeasured on this skill:** no Gemini run of proctor exists, so nothing below
is `[measured-here]`. No rate for anything — n=1, one brief, one domain, and that
domain was *building* a UI rather than testing one. No evidence these overrides
work; none has been measured with a `gemini.md` in place against the same brief.
Nothing about MCP tool returns: the family observation is a shell driver that
failed, and whether a *successful* return is read faithfully or summarised into a
claim is untested. Nothing about the iOS lane, `cua` delegation or
`proctor_stability` under any Gemini model, and nothing about other Gemini
versions; cutoffs and `thinking_level` defaults differ across 3.x. **[docs]** And
one self-limitation — the checklist names *"Avoid writing a prompt
with non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt."* A
conditional side-file is that shape, so read this once; each override below is
anchored to a named section.

## Override 1 — a tool return is quoted, or the claim is deleted

Lands on *Before anything else*, stages 4–6, and *Report*. **[docs]** Google
treats verification as something the prompt must contain: *"Include specific
verification steps in either the system instructions or your prompts directly."*
Two of the agentic template's nine rules are this — *"Review your output against
the user's task"* and *"Verify your claims by quoting the exact applicable
information (including policies) when referring to them."* That reverses the
house style deliberately: stripping verification scaffolding suits a model that
over-verifies, and inheriting the removal is the defect here. With no exit code,
the quoted thing is the returned field.

- **Every claim carries the tool, its arguments and the field it rests on** — not
  "contrast passes" but `proctor_assert` with `{"kind":"contrast"}` scoped to
  `AXStaticText`, returning `passed:false, observed:{"n:512":3.65}`. A ratio
  without the assertion that produced it is the family failure verbatim.
- **`passed:true` over an empty node set is a predicate that matched nothing.**
  Print the population each assertion ran over: `hasLabel` scoped to
  `role:"AXButton"` across nineteen buttons is a result, the same assertion
  resolving zero nodes is a gate that never ran. `[derived]` Uniform numbers say
  it too — one `stepInstability` array repeated across ten flows is one selector
  matching one thing.
- **`skipped` is never folded into passes.** *"An assertion that could not be
  evaluated is not an assertion that passed. Report it as skipped, with the
  reason."* Two separate integers — one "17 assertions run" absorbs them. And on
  `ready:false`: *"Proceeding produces a report whose failures are all yours."*
- **The artifact never asserts its own verification.** An app shipping a
  `DESIGN.md` claiming its contrast passes is a finding whose severity is the gap
  between that claim and your measurement; it is never coverage. **[docs]** Where
  the report must be checkable rather than readable: *"When model outputs must be
  machine-readable or follow a specific format, use a widely recognized standard
  like JSON, XML, Markdown or YAML that can be parsed by common libraries."*

## Override 2 — the ledger is a filled table before the first `proctor_act`

Lands on stage 2, stage 3, and the state matrix in `references/methodology.md`,
which already ask for it — *"Build the case-to-evidence matrix first"*, *"It is
the report's spine"*, *"A matrix with unrun cells is fine; a matrix that implies
it was fully run is not."* **[measured-family]** In the recorded run an
enumeration stated in prose, with an explicit completeness condition attached,
still delivered one of six, so the count has to become a cell to fill and a
fraction to report. Seven scopes here are countable. Filled, for a five-surface
app with eleven criteria:

| Scope | Where | Denominator | Filled |
|---|---|---|---|
| claims traceable to a tool result | SKILL.md:15 | 34 claims | 34 / 34 |
| criteria as matrix rows | SKILL.md:305 | 11 criteria | 8 covered · 2 partial · 1 gap |
| menu items inventoried vs exercised | SKILL.md:320 | 62 from `proctor_menu` | 62 read · 14 exercised · 48 `n/a: inventory only` |
| captures, one per state | SKILL.md:398 | 13 states | 11 trustworthy · 2 `n/a: off-screen, recaptured raised` |
| flows scored for determinism | SKILL.md:446 | 6 flows | 6 / 6 at `runs:5` |
| state-matrix cells | methodology.md:13 | 13 content + 9 environment + 3 crossings = 25 | 17 run · 8 `n/a` with reasons |
| fidelity ledger rows | methodology.md:256 | 41 elements × 5 surfaces = 205 | 168 present · 24 divergent · 13 absent |

Every `n/a` carries its reason, an unrecognised cell counts as open, and delivery
reports the fraction rather than the adjective. **[docs]** That is **Ambiguity**
plus **Underspecified task**: *"provide instructions for handling missing data
rather than assuming inserted data will always be present and well-formed."* The
unforced state, the window that would not raise, the app with no `AXIdentifier`:
each is a cell with a reason, not an absence.

## Override 3 — two attempts, and `proctor_doctor` first

Lands on *Before anything else*. **[docs]** *"On *other* errors, you must change
your strategy or arguments, not repeat the same failed call."* **[measured-family]**
four consecutive invocations of one absent driver, unchanged between attempts,
ending in a review naming it as verified. `proctor_doctor` is the whole defence:
*"It costs one call and it is the difference between a campaign and an hour of
retries."* Read `lanes[]` before planning rather than after a failure — an
`unconfirmed` lane is a fact about what Proctor established, and calling `doctor`
again will not change it, because that call runs none of those tools. A missing
Accessibility grant reads exactly like a selector bug, so two `nodeNotFound` in a
row sends you to `grants[]`.

## Override 4 — seven passes, not one sweep

Lands on *The campaign*. **[docs]** Under **Too many tasks**: *"If the prompt
asks the model to perform several distinct cognitive actions in a single pass"*
it is *"trying to accomplish too much. Break the requests into separate
prompts."* The remedy is the skill's own structure: *"make each step a prompt and
chain the prompts together in a sequence."* Run the stages as separate passes
feeding forward; `[derived]` the tell of a single sweep is a report with all
seven headings where stages 5 and 6 cite no tool return.

## Override 5 — describe the crop before judging it

Lands on stage 5 and every use of `proctor_zoom`. **[docs]** *"Ask the model to
describe the images before performing the task in the prompt."* Their example is
exact: a generic instruction over an airport board returns a one-line caption,
naming what to extract returns thirteen rows. Two corollaries they state directly
— *"To improve the response, point out which parts of the image are most relevant
to the prompt"*, and a disambiguation step separating *"the model did not
understand the image at all"* from *"it did not perform the correct reasoning
steps afterward."* Both apply per crop:

- Per capture, **name what is in it first** — regions, copy, visible spacing —
  then judge against the stage's question; a verdict without that step is the
  generic caption wearing the specific answer's authority. Point at the region
  with the tool built for it: *"Read small things with `proctor_zoom`, not with a
  bigger screenshot."*
- When a finding looks wrong, ask what is in the image first — and here that has
  a mechanical answer the docs do not have. *"Read the metadata rather than the
  image"*: `trustworthy: false` *"means this capture is not evidence of anything,
  whatever it looks like when opened"*, and *"Never treat an untrustworthy frame
  as evidence; capture again with the window raised and say that you did."* A
  crop you rendered and did not open is not evidence either, and its row stays
  open. `[derived]` The cheaper instrument outranks all of this when the question
  is not visual: *"Reach for `find`, not a screenshot, to learn whether an action
  landed."*

## Override 6 — platform numbers are read, never recalled

Lands on *Native Conformance Rubric* and the accessibility rubric in
`references/methodology.md`. **[docs]** *"Your knowledge cutoff date is January
2025."* **[measured-family]** the recorded run put Windows 10's accent colour on
a Windows 11 app — a previous-generation published value returned confidently,
not a guess — and macOS 27's ladder and type ramp sit in that hazard zone. Fill
this before the first conformance claim, each cell carrying its value **and its
source**; a cell you cannot source is one you invented.

| Property | Value | Source |
|---|---|---|
| Body text size, control heights, spacing unit | 13pt, kit tier ladder, 8pt grid | `mac-design-studio` `native-foundation.md`, read this run |
| Contrast floors | 4.5:1 body, 3:1 large and non-text | `methodology.md` §Contrast thresholds (WCAG 1.4.3 AA) |
| Hit-target floor / aspiration | 24 × 24 gate, 44 note | same §Hit-target minimums (SC 2.5.8 / 2.5.5) |

**[docs]** A value not in a file you opened gets grounded rather than recalled:
*"Grounding with Google Search connects the Gemini model to real-time web
content, and should be enabled whenever the model may need to know obscure or
recent facts."*

## Override 7 — the report says only what the run observed

Lands on stage 7 and *Disclosure requirements*. **[docs]** Google publishes a
system instruction for output that must not exceed its sources, and its last
clause is the one that matters: *"If the exact answer is not explicitly written
in the context, you must state that the information is not available."* Adopt it
for the report, where the context is the tool returns this campaign received.
**[docs]** The pressure runs the other way by default: *"By default, Gemini 3
models provide direct and efficient answers. If you need a more conversational or
detailed response, you must explicitly request it in your instructions."* The
skill asks for a report proportional to what was found, which here resolves short
— and the sections that drop first are *Not covered* and *Methods*, the two
carrying the honesty. So: **Verdict, What was proven, Defects, Flaky, Not
covered, Methods — six headings, always present, `none` written out where a
section is empty.** Methods is the section whose value is that it was filled:
*"a methods section handed back as headings for someone else to complete is the
one section whose whole value is that it was actually filled in."*

**[docs]** One filled example — *"you can remove instructions from your prompt if
your examples are clear enough in showing the task at hand"*:

> **Methods.** macOS 26.4 (24E5228a); `doctor.agentBuild` `1.4.0+2291`. Lane
> `native` on every step (`backend:"native"`, 118 steps). `AXManualAccessibility`
> applied — Electron host — so timing and smoothness findings are about the
> instrumented app; the four label findings are not. Settle: 101
> `allSignalsQuiet`, 14 `axQuietOnly` with `captureNeverQuiet` (live spinner), 3
> `timeout`, reported as inconclusive rather than as defects. Captures: 13 taken,
> 2 `trustworthy:false` (`caveat`: off-screen, no complete frame) and re-taken
> raised, so those two states were observed in a different configuration from the
> rest. No reflector (`reflectorConnected:false`), so every colour is a
> post-compositing pixel read and every geometry number an accessibility frame.

`[derived]` A disclosure with no tool return behind it is written as what was missing.

## Override 8 — the fan-out is four, and it never checks your own work

Lands on *Delegating*, which already caps it: *"Spawn subagents only for
genuinely independent work — a separate app, or a matrix cell that needs its own
window — and cap the fan-out at four."* Two additions: never delegate
verification of a result you produced, because a judgement in a measurement's
position is the family failure; and **[docs]** prefer the tool call over the
question on a low-risk read — *"Prefer calling the tool with the available
information over asking the user, unless"* a later step needs the missing
parameter. `doctor`, `list`, `find` and `menu` observe without mutating.

## Two short notes

**`thinking_level`.** A seven-stage campaign across a state matrix, a fidelity
ledger and a determinism sweep is what **[docs]** Google describes `HIGH` as
being for — *"multi-step planning, verified code generation"*; 3.7 Flash defaults
to `MEDIUM`.

**Modules not written.** `injection` did not fire: the skill ingests no
third-party text as instructions, and the adjacent case, an app's own self-review,
is handled in Override 1. `emphasis` did not fire either — zero shouted
directives in 2,454 lines, which **[docs]** is the right register: *"Avoid
unnecessary or overly persuasive language."*
