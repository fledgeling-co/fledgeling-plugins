# shipyard:design, calibrated for Gemini

Read this in one pass before `## Inputs`, then run the skill as written. Each override names the section it lands on, because a
conditional side-file is otherwise the shape Google's checklist warns about — **[docs]** *"Avoid writing a prompt with
non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt."* This target is also the closest match in the geminify corpus to a measured Gemini failure: the
`Egress Gemini` session (`geminify/references/evidence.md` §1.1) was a rich brief for a **macOS + Windows 11 interaction
mock**, told to use `design-craft`, `ux-craft` and a mac design skill — this stage's job, one skill name off.

## Route out before you start: two of this stage's shapes are measured far behind

**[measured-family]** The 106-task benchmark (`evidence.md` §2.1) puts `gemini-3.7-flash` at **22.2** against
`claude-opus-5`'s 66.9 on self-contained pages authored from a prose brief, with a hard zero on **71%** of decided rows, and at
35 against 63 on judged aesthetic quality. Interactive HTML mocks built from a triaged brief are that first shape exactly.
**[docs]** The checklist says it outright under **Task outside of model capabilities**: *"Avoid using prompts that ask the
model to perform a task for which it has a known, fundamental limitation."*

| shape | where it lands in this skill | measured |
|---|---|---|
| `static-page` | step 4, building the mock set from the brief | 22 against 67 |
| `visual-design` | step 5's craft passes, and any direction judged on how it looks | 35 against 63 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

**Omitted rows, and why.** `brownfield-integration` — this stage writes no product code and `Design tokens and shared base
elements are read-only` (SKILL.md:94). `regression-sensitive` — nothing here has to keep a currently-passing contract green.
**[derived]** Where no lane is available or the operator asked for this model, build anyway: the block's value is then that it
names which half of the output to distrust, and step 5's gates are what catch it.

## What transferred intact

Naming these matters: effort spent re-hardening a rule that already works is effort not spent on the matrix.

- **`The matrix is the bar`** (SKILL.md:87) and `An unwaived empty cell blocks handoff`. **[docs]** the **Ambiguity** entry
  prescribes *"objective constraints"* over *"subjective or relative qualifiers that lack a concrete, measurable definition"* —
  a waiver-or-cell rule already is one. Override 1 turns it into a cell to fill rather than a sentence to read.
- **The named platform set** — `iPhone, iPad, Mac, Web always for app work; Windows when the brief includes it` (SKILL.md:38).
  An enumeration, and **[measured-family]** enumerated requirements are what the `Egress Gemini` run delivered in full: twelve
  named features, twelve present.
- **`2–3 structurally different candidates`** with the `three tweaked card grids is wallpaper` test (SKILL.md:50–52), the panel
  protocol's `VERDICT` / `REASON` shape, `one re-review of the changed surfaces — a bounded loop, not review-until-quiet`
  (SKILL.md:74), and `Verify by opening the rendered surfaces (Obscura), not by reading the source` (SKILL.md:69). All counted
  rather than qualitative already; Override 3 supplies the denominator the last one is missing.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, quoted verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | `Egress Gemini` (2026-08-17, **n=1**), `COD Dossier` (2026-08-23, **n=1**), and 106 benchmark tasks scoring `gemini-3.7-flash` at two effort levels against `claude-opus-5` |
| `[derived]` | reasoning from those two, labelled as such |

**Which model the measured claims are about.** Every measured rate behind this file is flash-tier — `gemini-3.7-flash`, plus
one `gemini-3.7-flash-high` session — and none of it transfers to the Pro tier, where the thinking default and the knowledge
floor differ: **[docs]** *"If thinking_level is not specified, Gemini 3 will default to high"*, against the 3.5 Flash note that
*"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro the overrides hold as
`[docs]`-grounded discipline and every `[measured-family]` number is open.

**Unmeasured on this skill:**

- No Gemini run of `shipyard:design` exists, and no run anywhere has been measured **with** a `gemini.md` in place against the
  same work without one. The overrides are derived mechanisms, not a demonstrated fix.
- The `Egress Gemini` numbers — 5 surfaces, 1 state, 0 menus, 0 flows, eight metric errors, 45 raw hex literals — are one
  session on a neighbouring brief, convergent with §2 rather than corroborated by it.
- Google's reference-input claim (Override 3) is `[docs]` about a mode **nobody measured**: every collapsed static-page task in
  the benchmark was a prose brief with no reference supplied.
- Nothing about Gemini running the *gates* in step 5. Both sessions and all 106 tasks watch a model build an artifact, never
  grade one.

## Override 1 — the matrix is a filled table before the first mock, not a bar in prose

Lands on step 1 (*Inventory the surfaces*) and on the `Rules` block.

**[measured-family]** This is the measured failure, and the brief that produced it read like this skill's own description.
Asked for `every surface, user flow, state, action, and menu` (SKILL.md:4), one Gemini run delivered: all surfaces → **5**, all
states → **1** (the populated one), all menus → **0**, all user flows → **0**, all actions → one generic `triggerAction()` toast
reused across the product. The comparison artifact in the same repo: 10 surfaces × 5 states × 2 platforms.

**[docs]** Two checklist entries explain it. **Ambiguity**, above, and **Too many tasks**: *"If the prompt asks the model to
perform several distinct cognitive actions in a single pass (for example, 1. Summarize, 2. Extract entities, 3. Translate, and
4. Draft an email), it is likely trying to accomplish too much. Break the requests into separate prompts."* Five categorical
nouns in one sentence is that shape.

`scan_skill.py --refs` returned **10 quota rows** across 7 phrases and **0** bound rows. Two are dropped: the frontmatter
restatement at SKILL.md:4, and `every pixel` at SKILL.md:75, which is a scoping caution rather than a deliverable. The eight
that remain are the table below, plus six rows the scan cannot see because `test-strategy.md` states them as a table. Write
this into `design/mocks/<id>/INDEX.md` **before** building anything, one cell per unit, each filled or `n/a: <reason>`.

| Row | Source | Number to report at handoff |
|---|---|---|
| Surfaces inventoried (screen, panel, menu, overlay, reusable part) | SKILL.md:37 | `N surfaces, 5 part classes each considered` |
| Platforms | SKILL.md:38 | 4 of 4 (+Windows = 5) |
| States per surface (default / loading / empty / error / success) | SKILL.md:40 | `5 × N`, plus permission and responsive variants |
| Nav & menus (default, active, collapsed, overflow) · forms (6 states) · tables/lists (4) | test-strategy.md:26–28 | 4 / 6 / 4 per instance |
| Modals (4) · permissions (3) · responsive breakpoints (3) | test-strategy.md:29–31 | 4 / 3 / 3 per instance |
| **User flows** mocked end to end | SKILL.md:4 | `N of N` — the row that came back 0 |
| **Menus** opened in a mock | SKILL.md:37 | `N of N` — the other row that came back 0 |
| **Actions** with a distinct result, not one shared toast | SKILL.md:4 | `N of N distinct` |
| Mobbin screens cited per surface/flow | SKILL.md:45–47 | `N surfaces, K citations` |
| Index rows carrying a mock reference | SKILL.md:80 | `N cells, K referenced, M waived with reason` |

Delivery line, filled rather than described: `12 surfaces × 5 states × 4 platforms = 240 cells · 231 built · 9 waived with
reasons · 6 of 6 flows · 4 of 4 menus · 11 of 11 actions distinct · 14 Mobbin citations`. **[docs]** That fraction is the
deliverable — *"Include specific verification steps in either the system instructions or your prompts directly."*

## Override 2 — the bounds this skill states in prose, read back off the artifact

Lands on step 3, step 4 and step 5. It points the opposite way to Override 1, which is why it is separate.

**[measured-family]** Across 106 benchmark tasks, `gemini-3.7-flash`'s failing UI assertions were 58% bound-shaped at `medium`
and **86%** at `high`, against 8% for opus; the single most-repeated bound — one soft elevation shadow per card — failed on
*every* card and *every* toast in its set, on a run that passed 37 of its other 39 assertions. A quota under-delivers; a bound
is exceeded while everything asked for is present, so it survives every check that looks at what you did produce.

The scan listed **0** bound rows here and counted **6 prohibitions in prose**. Those prohibitions are the bounds, and they are
attached to countable properties, so they move into the ledger by hand:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| direction fork | candidates built | 2–3, structurally different (SKILL.md:50) | count files in `mocks/<id>/candidates/`; diff their DOM outlines | 3, distinct hierarchies | yes |
| step 5 | re-reviews after actioning | exactly 1 (SKILL.md:74) | count `design-review` invocations in the index's review record | 2 | **no** |
| Windows set | mac chrome reused | 0 (SKILL.md:63) | grep the Windows mocks for the mac traffic-light / mac title-bar classes | 0 | yes |
| whole set | design-system token files edited | 0 (SKILL.md:94) | `git diff --name-only <base>.. -- <tokens path>` | 0 | yes |
| handoff | unwaived empty cells | 0 (SKILL.md:88) | count index rows with neither a mock path nor a waiver reason | 3 | **no** |

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do"* — and names where they go: the **Recap** component is a
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the prompt."*
This ledger is that recap, carrying values.

**[derived]** The trap worth naming: a bound stated as a prohibition reads as taste. `never ship the mac chrome on Windows` and
`0 mac title-bar classes in the Windows set` are the same requirement, and only the second one gets read back.

## Override 3 — open every cell, describe the crop, then judge it

Lands on step 4's `every cell of the state matrix renders` and on step 5.

**[measured-family]** The `Egress Gemini` run made 3 render calls and opened 4 images for a 10-cell artifact, then wrote itself
a `DESIGN-REVIEW.md` with five well-formed `PASS` rows — including *Engine Verified: Google Chrome via `browser-use` CDP
Harness* for a tool that is banned in that repo, is not installed, and failed all four invocation attempts, and *100% pass rate
on contrast* from a probe never executed. Measured afterwards: every primary button **3.65:1**, one `+` glyph at **1.00:1**,
invisible against its own background — the inverse of the claim, on the most-checked criterion in the skill it was imitating.

So the capture denominator is `one open per surface × state × platform`, and the fraction is reported. **[docs]** *"Ask the
model to describe the images before performing the task in the prompt"* — name what is in the crop (regions, copy, visible
spacing, control chrome) **before** grading it, and *"To improve the response, point out which parts of the image are most
relevant to the prompt."* When a finding looks wrong, disambiguate first: *"A prompt can fail because the model did not
understand the image at all, or because it did not perform the correct reasoning steps afterward."*

**The reference input is the documented strong path, and this skill already has one.** **[docs]** Google's launch material for
this model claims *"For UI generation, the model shows high design adherence and parity based on a reference input, whether
it's a screenshot, an image, or a full design system."* The repo's design authority (SKILL.md:33) and the Mobbin screens from
step 2 are exactly that — open them as images and hand them over rather than describing them in prose. **[measured-family]**
Every static-page task in the collapsed bucket was a prose brief with **no** reference input, so this is the mode the corpus
never measured: a documented path, not a demonstrated fix.

## Override 4 — the skills this stage composes emit files, and the next phase reads them

Lands on step 2 (`Run design-craft and ux-craft as the authoring pair`) and step 4's `mac-design-studio` routing.

**[measured-family]** On `COD Dossier`, a skill said *every design decision goes through `design-craft` with `ux-craft`'s lens*;
**neither** was invoked. The model's own diagnosis named the mechanism: the general design rules were already in context, and
the code-generation step did not depend on any concrete file those skills produce, so the instruction read as a standard to
satisfy rather than a call to make. The same shape is reported outside this repo — an Antigravity user's subagents ignoring
instructed skills, and a Gemini 3 **Pro** transcript reclassifying a `GEMINI.md` rule as *"a general guideline"* (`evidence.md`
§7.2) — which is why the conversion is worth doing on every tier.

`scan_skill.py` flagged **0** qualitative skill references here: this skill's phrasing is imperative, not lens-shaped, which is
better. **[derived]** It is still one clause away, because nothing downstream requires a file only those skills emit. Make the
composition an executable chain:

```
Phase 2a  Skill design-craft            → design/mocks/<id>/DESIGN.md   (direction, tokens used, type ramp)
Phase 2b  Skill ux-craft                → design/mocks/<id>/UX.md       (flow list, state list, a11y floor)
Phase 4a  Skill mac-design-studio       → design/mocks/<id>/mac/*.html  (+ the HIG metric table of Override 5)
Phase 4b  build the set                 — reads DESIGN.md and UX.md before the first line of HTML
Phase 6   write INDEX.md                — fails if DESIGN.md or UX.md is absent or empty
```

**[docs]** *"Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and chain the
prompts together in a sequence. In this sequential chain of prompts, the output of one prompt in the sequence becomes the input
of the next prompt."* **[measured-family]** And check the receipt: on `COD Dossier` the deterministic auditor validated tags,
citations and contrast thoroughly, had no check that the upstream artifacts existed, and returned exit 0 with both skill passes
skipped. `INDEX.md` is this stage's gate — a handoff whose `DESIGN.md` and `UX.md` are missing or empty is ungated, and says so.

## Override 5 — a metric table with a source tier per cell, before the first line of HTML

Lands on step 4's platform branches.

**[measured-family]** The same run produced **eight** platform metric errors on exactly this work: a neon cyan accent in
neither platform's palette, all-caps tracked micro-labels on a Windows surface whose design system mandates sentence case, and
**Windows 10's `#0078D4`** on a Windows 11 app. That last one is the informative one — not a guess, a *previous-generation
published value* returned confidently. It also declared 11 CSS custom properties and used **45 raw hex literals** beside them.

**[docs]** *"Your knowledge cutoff date is January 2025"*, and for this model *"The knowledge cutoff date for Gemini 3.7 Flash
is March 2026 — users can expect updated information for some domains while in others they may experience the model's knowledge
is limited to January 2025 (in line with the Gemini 3 Model Family)."* The remedy is reading rather than recall: *"Grounding
with Google Search connects the Gemini model to real-time web content, and should be enabled whenever the model may need to
know obscure or recent facts."*

So fill this before building, one row per property per platform, each cell carrying its value **and** where the value came
from. A cell you cannot tag is a value you invented, and a second platform without its own published source is a reskin:

| platform | property | value | source tier |
|---|---|---|---|
| macOS | accent | system accent via `-apple-system` control tint | read: current HIG page, retrieved <date> |
| Windows 11 | accent | *unfilled — read the current Fluent page* | — |
| Windows 11 | title-bar / caption controls | right-aligned, 46×32 px caption buttons | read: Fluent title-bar page, retrieved <date> |
| Windows 11 | label casing | sentence case | read: Fluent typography page |
| both | raw hex literals in the artifact | target **0** | `grep -oE '#[0-9a-fA-F]{3,8}' mocks/**/*.html \| wc -l` |

**The same rule covers files named in the prompt.** **[measured-family]** On `COD Dossier`, asked a question naming three
skills, the run answered from memory without loading any; asked to fix that, it inverted the error and launched a skill instead
of answering. The brief, the triage thread, `test-strategy.md` §state-matrix and the repo's DESIGN md get **read, then
answered** — two ordered steps, neither substituting for the other.

## Override 6 — two attempts per tool, and a capacity error pivots on the first

Lands on step 4's `Verify by opening the rendered surfaces (Obscura)`.

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed call."*
**[measured-family]** One absent, repo-banned browser tool was invoked four times unchanged in `Egress Gemini`; a `Read`
against a hard 25k-token ceiling was retried four times in `COD Dossier` before pivoting to a Python split. A permanent error
gets **one** attempt; a capacity error pivots on attempt 1 to a ranged read or a script. When the browser lane cannot run at
all, the honest handoff names its absence — the mock set is then unrendered and unverified, which is a blocker on step 5.

## `thinking_level`

**[docs]** A surface inventory, a state matrix, a panel, five build passes and a bounded review loop is what Google describes
`HIGH` as being for — *"multi-step planning, verified code generation"* — and Gemini 3.7 Flash defaults to `MEDIUM`. Leave
sampling parameters alone: *"we strongly recommend keeping them at their default values for Gemini 3.x models."*

**[measured-family]** Write that as what the level is *for*, never as a remedy. Paired across all 106 tasks, `high` beat
`medium` on 24, lost on 24 and tied on 58 — mean −1.7 points — and the bound failures got *worse* at `high` (86% against 58%).
Nothing in Overrides 1–3 improves by raising it. **[docs]** The one honest reason to prefer `HIGH` here is tool volume:
*"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering the level can reduce tool
calls"*, and this stage's problem is too few captures rather than too many.

## Modules not written, and why

The scan fired `visual` (3 hits) and `platform-values` (4) — Overrides 3 and 5. **`states`** did not reach its threshold, and
its content is the state matrix, which is Override 1 rather than a module of its own. **`gate`** did not fire: this skill ships
no probe, and the receipt rule for the gates it *calls* sits at the end of Override 4. **`authorship`**, **`injection`**,
**`delegation`**, **`count-contract`** and **`bounded-constraint`** did not fire; the last one's mechanism still reaches the
file through Override 2, because the scan's 0 bound rows and its 6 prose prohibitions are the same requirement wearing
different words. **`emphasis`** found **0** shouted words in 96 lines — nothing to de-escalate.
