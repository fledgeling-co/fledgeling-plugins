# create-mac-icon on Gemini

Read this once, then read `SKILL.md` normally. The canon transfers — the
directions, the rubric, the three engines, the loop, the ordering
`gate < panel < human`. What does not transfer is the assumption that a bound
stated in prose gets read back off the artifact, or that a score written into
`audit.html` came from a render someone opened. Each override below names the
section it lands on, so this is read in one pass: **[docs]** the checklist warns
against instructions requiring *"non-linear logic or conditionals that require
the model to piece together fragmented instructions from multiple different
places in the prompt."*

## Epistemic status

Tiers: `[docs]` (Google, quoted verbatim and gated), `[measured-family]` (Gemini
runs of *other* skills plus a 106-task benchmark), `[derived]`. **`[measured-here]`
appears nowhere — no Gemini run of `create-mac-icon` has been observed, n=0.**
Every rate here is flash-tier: `gemini-3.7-flash` over 106 tasks at both effort
levels, plus two single sessions. None of it is to be projected onto Pro, where
these overrides stand as `[docs]`-grounded discipline and every
`[measured-family]` number is open. Defaults drift inside the family too —
**[docs]** *"The default thinking effort is now medium, changed from high in
Gemini 3 Flash Preview."*

**Unmeasured on this skill:** whether any override here changes an outcome
(nothing has been measured with a `gemini.md` in place against the same work
without one); the transfer of override 1's bound failure, measured on **CSS cards
and toasts** rather than SVG material; Gemini **judging** anything, since
`references/evidence.md` already notes the panel literature is text judging
rather than vision-language judging of close icon variants; and
`rsvg-convert`-versus-browser divergence, the `structure` envelope and
`self_contrast` on a Gemini-authored master. Modules skipped: `emphasis` (2
tokens across 2,753 lines), `injection` (nothing third-party is ingested),
`count-contract` (it would restate override 1), `states` (the appearance variants
are enumerated in the rubric and counted as quota cells), and `platform-values`
(2 triggers against a threshold of 3, because this skill ships its own corpus —
its content is override 8).

## Route out before you spend the engine budget

**[docs]** *"Avoid using prompts that ask the model to perform a task for which it
has a known, fundamental limitation."* Two of this skill's shapes sit there on the
measured corpus. Not permission to give up: where no lane is available, the
block's value is naming which output to distrust.

| shape | where it lands here | measured (gem-flash vs opus) |
|---|---|---|
| `visual-design` | Engine A authoring, the material judgment, the shipping call | 35 against 63 |
| `regression-sensitive` | the loop's Pareto gate; every targeted one-constant edit | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape visual-design
```

**Rows omitted:** `static-page` (22 against 67), because `audit.html` is filled
from a template and gated by `audit_sheet.py check` — the two things those
prose-brief tasks lacked; `brownfield-integration`, because the commission
directory is the run's own; and `greenfield-module`, `algorithmic`,
`accessibility`, `react-ui`, never named and not produced here.

## What transfers intact

- **The counts are already numbers** — `≥10/12 with zero failures on 1–4`, three
  takes minimum, `256 / 128 / 96 / 64 / 32`, `400 paths / 200KB`, ten rounds,
  `PANEL_VETO = 3`. **[measured-family]** the benchmark's optimality bucket,
  where briefs state an explicit bound, scored 74.7 against opus's 75.0.
- **The composition is already an artifact chain.** The scan found **zero**
  qualitative skill references; each phase hands the next a file (`icon.svg` →
  `render-manifest.json` → `audit.html` → `score.json` → `panel.json` →
  `loop-runs/best-promoted/`), which is what **[docs]** prescribes for an
  overloaded pass: *"make each step a prompt and chain the prompts together in a
  sequence."* Nothing needs converting.
- **The corpus is the documented strong path.** **[docs]** *"For UI generation,
  the model shows high design adherence and parity based on a reference input,
  whether it's a screenshot, an image, or a full design system."*
- **Exit-code severity, stderr routing, `check $?` never a pipe's.**

## 1. Bounds, not requirements — the one that matters most here

Lands on: the 12-point rubric, the Tahoe grammar's nine tells, `fidelity.py
structure`. **[measured-family]** across 106 tasks, Gemini's failing UI assertions
were bound-shaped — `exactly N`, `no`, `not`, `only` — **58%** of the time at
`medium` and **86%** at `high`, against **8%** for opus and **6%** for the OpenAI
lane. The most-repeated failure was `has exactly one soft elevation shadow`, which
failed on *every card and every toast in its set* on a run that passed 37 of its
39 other assertions. The briefs stated it numerically. That is this skill's
grammar in another medium: `One soft top light, zero hard speculars`,
`≤2 hue families`, `contact shadow = blurred ellipse at 10–18% black`, `white
fill at 78–92% opacity`, `no baked corners/shadow`, one focal object at `~55–65%
tile width` — each a maximum a default idiom exceeds quietly.

**[docs]** Google names these a component in their own right — *"Restrictions on
what the model must adhere to when generating a response, including what the
model can and can't do."* — and places them in a recap at the end of the prompt.
So: **a bound ledger filled from the emitted SVG**, not from the spec, before
`audit.html` is written. Specimen of the shape, not a measurement:

| bound | stated | readback | observed | within? |
|---|---|---|---|---|
| soft shadows on the focal object | exactly 1 | `grep -c 'feGaussianBlur\|feDropShadow' icon.svg`, then name each and its light direction | 3 (contact, rim bloom, inner) | **no** |
| hue families | ≤ 2 | `grep -oiE '#[0-9a-f]{6}' icon.svg \| sort -u`, binned by hue angle | 2 (porcelain + one ember) | yes |
| raw hex beside tokens | 0 outside the token block | same grep, minus the declarations | 45 | **no** |
| path / byte envelope | 400 / 200,000 | `python3 scripts/fidelity.py structure --candidate icon.svg` | exit 0 | yes |

Report `N of N bounds within limit`. Row three is the live one:
**[measured-family]** a Gemini-authored artifact declared 11 custom properties and
used **45 raw hex literals** beside them, against a comparison master's 102 tokens
and 86 `var()` uses with none unresolved — nothing wrong on its face, the bound
violated by what was not written. And **prohibitions read as taste**:
`Don't bake gloss as your identity` and `zero hard speculars` are one requirement
in two registers, and the measured run treated the prohibition form as style
advice. Convert each into a counted property with a readback.

## 2. The quota ledger

Lands on: step 7's `Ask each row "what is wrong with this?"` and
`One silhouette across the set`. **[measured-family]** one run delivered
**12 of 12** enumerated features and **1 of 6** named states, **0** menus,
**0** flows — enumerations survive, categorical scopes collapse to one instance.
The scan found 21 categorical phrases here and **16 were prose**, past findings
rather than deliverable scope. Four of the five that remain become cells on one
commission; the fifth, varying direction and palette, applies across a session:

| scope | denominator | filled |
|---|---|---|
| audit rows read with `what is wrong with this?` | 1 per take | `__ of __` |
| icons sharing `assets/squircle-path.txt` | 1 per sibling icon in the repo | `__ of __` |
| identity-bearing elements checked at their smallest dimension | 1 per element | `__ of __` |
| figure-ground boundaries above the measured floor | 1 per boundary | `__ of __` |

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition."* — the scan found 62, and the ones inside a deliverable
instruction need a number before they are acted on. And **[docs]** *"We recommend
to always include few-shot examples in your prompts."* is why the 1024 hero is
authored at full fidelity first and the size set measured against it.

## 3. Verification, receipts, and the sheet as a claim

Lands on: step 7's three commands, its recommendation block, and `A gate ACCEPT
is evidence, never a verdict`. **[docs]** *"Include specific verification steps in
either the system instructions or your prompts directly."* and *"Verify your
claims by quoting the exact applicable information (including policies) when
referring to them."*

**[measured-family]** the closest match in the evidence base to what this skill
ships: a run wrote itself a review of five well-formed `PASS` rows naming a
browser engine that failed on all four invocation attempts and never ran, a
*"100% pass rate on contrast"* from a probe never executed — measured afterwards
at 3.65:1 on every primary button and 1.00:1 on one glyph, invisible — and an
audited-target count of 47 that nothing produced. Five rows, where the shape it
imitated has forty cells. That artifact is `audit.html` under another name.

- Every number in the sheet and the delivery note carries the command that
  produced it and that command's output — `discovered 4 take(s)`, `18 renders
  into audit-renders`, `OK — sheet present, filled, current, past the rubric bar,
  and every image resolves.` A denominator of zero is a gate that never ran.
- No score cell before the render it grades exists and has been opened, and a
  criterion not exercised is `not measured`, so a 12 with two unmeasured criteria
  is a 10 at best: **[docs]** *"If the exact answer is not explicitly written in
  the context, you must state that the information is not available."*
- **Neither gate has a prerequisite receipt.** `check` proves the sheet's images
  resolve and are newer than their sources, `structure` proves the envelope, and
  neither sees whether the corpus was sampled or the sheet opened —
  **[measured-family]** on another skill's run, a thorough auditor with no
  prerequisite check let two skipped upstream invocations through at exit 0. Write
  the receipt: exemplar filenames opened, values sampled, the sheet read.
- Prove a gate can fail before trusting it passing — **[derived]** from
  `geminify`'s own evidence, where a one-line change to its quote gate took the
  checked count to zero and turned every file green. A degraded metric tier is a
  refusal, not a caveat: `gate` exits **2** without torch.

## 4. Looking, before judging

Lands on: step 4, step 7's `open the sheet in a browser and read it`, and the
loop's residual critique. **[docs]** *"Ask the model to describe the images before
performing the task in the prompt."* and *"To improve the response, point out
which parts of the image are most relevant to the prompt."* Google's worked
example is step 4 exactly: *"Describe this image."* returns a one-line caption,
while naming what to extract returns thirteen rows. So do not open an exemplar
and form an impression — name what is in the crop, then read the six values step
4 lists (ground luminance, brightest point, accent saturation, darkest shaded
pixel, rim light, contact-shadow falloff) into the spec before the first line of
`build_icon.py`. Same for a residual: name the region, then judge it.

**A capture denominator:** every take × every rendered size opened, fraction
reported — **[measured-family]** the run that fabricated its review made 3 render
calls and opened 4 images for a 10-cell artifact. And **[measured-family]** every
task in the benchmark's worst bucket was a prose brief with **no** reference
input, so pass 2–4 corpus captures to Engine C as `referenceImages`.

## 5. Delegation, and one flag that is now wrong

Lands on: `Briefing the implement agent` and `The judged layers` in
`references/fidelity-loop.md`. The caps transfer as written: one background agent
per round, `do not delegate to subagents; spawn none`, one edit class per round,
the harness reverting rather than the agent. What does not is the panel's family
exclusion. `judge_panel.py --generator-family` defaults to `claude` because the
round agent is `claude -p`; a Gemini-driven round makes `claude`, grok and the
OpenAI judge all out-of-family, so the default excludes a legitimately
independent vote and leaves two decisive judges — which this skill's own
`references/evidence.md` says `cannot produce a majority in disagreement`. Pass
`--generator-family none`. **[derived]** from the skill's text and its cited
self-preference literature. And put step 2's 2–3 silhouette sketches to the user
as a closed set: **[docs]** *"you can rephrase the instructions as a multiple
choice question and ask the model to choose an option."*

## 6. The retry ceiling

Two attempts per tool, then change approach. **[docs]** *"On *other* errors, you
must change your strategy or arguments, not repeat the same failed call."*
**[measured-family]** four consecutive invocations of one absent tool with no
change between them in one session; four consecutive `Read` failures against a
token ceiling in another before pivoting. Here, `rsvg-convert` missing,
`media-gen-pro` unavailable or torch absent are **permanent on attempt 1**, and
the skill names each fallback — widen Engine A to 2–3 hand-authored takes, or
proceed with `--allow-degraded-tier` and say the material was never measured.
Never read the generated master: a 300KB SVG is ~88k tokens.

## 7. `thinking_level`

**[docs]** `HIGH` is for prompts *"such as multi-step planning, verified code
generation, or advanced function calling scenarios."* — which the bounded loop
is, so name `HIGH` for it and say the uplift is unmeasured on this work.
**[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on
24, tied on 58, mean −1.7 points, and bound-shaped failures rose at `high` (86%
against 58%) — not a remedy for overrides 1–3.

## 8. Read it rather than recall it

Lands on: step 0 (`read the repository you are adding to`) and the corpus.
**[docs]** *"Your knowledge cutoff date is January 2025."*, and from the 3.7 Flash
model card: *"The knowledge cutoff date for Gemini 3.7 Flash is March 2026 —
users can expect updated information for some domains while in others they may
experience the model's knowledge is limited to January 2025 (in line with the
Gemini 3 Model Family)."* The macOS 26 gel-glass grammar sits on the wrong side
of that floor for parts of the family, so recall returns the previous era.
**[measured-family]** that failure has been seen in this exact shape: a run put
**Windows 10's `#0078D4`** on a Windows 11 surface — a previous-generation
published value returned confidently rather than a guess, one of eight metric
errors in that artifact. The remedy ships with the plugin: 32 captures in
`references/corpus/apple-2026/` and the answer key beside them. Read the pixels.
The same rule covers step 0's family values — accent hex, ground register, export
sizes — which sit in the host repo's own files.

**A file named in a prompt gets loaded before the answer is written.**
**[measured-family]** asked a question naming three skills, one run answered from
memory without loading any; asked to fix that, it inverted the error and launched
a skill instead of answering. Read, then answer, as two ordered steps. Step 0
exists because the family rule and export sizes `are written in that repo's own
CLAUDE.md, and the skill did not read them`.
