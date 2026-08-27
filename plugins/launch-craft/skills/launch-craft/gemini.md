# launch-craft, calibrated for Gemini

Read this once before *Phase 1*, then run the four phases as written; each override
names the phase or file it lands on. The canon transfers. What changes is that this
pipeline's two most load-bearing instructions are **standards rather than steps with
an output** — Phase 3's *"Load `/design-craft` … Load `/ux-craft`"* and Phase 1's
*"Comprehensive product requirements"* — and that **the pipeline's own headline
deliverable lands in the exact shape the benchmark corpus measured this family
behind**: a self-contained interactive page authored from prose.

## Epistemic status

| Tier | Used | Source |
|---|---|---|
| `[docs]` | throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | **n=1 ×2, plus n=106** | two Gemini sessions of *other* skills, and a 106-task benchmark |
| `[measured-here]` | **no** | no Gemini run of launch-craft has been recorded |
| `[derived]` | marked | reasoning from those, plus facts read out of this skill |

**The tier the evidence is about.** Every measured rate here is flash-tier and none
of it projects onto the Pro tier. **[docs]** Defaults drift inside the family too:
*"If thinking_level is not specified, Gemini 3 will default to high."*

**Unmeasured on this skill.** Nothing below is `[measured-here]`. Three gaps bite:
nothing in either source watches a Gemini model drive `agy` recursively (Phase 1
calls this family through a CLI, so the conductor and the worker are the same
family); nothing measures a Gemini model running Mobbin MCP or Dossier panels; and
the corpus's UI rows are React behaviour tasks, not GSAP/Three.js scroll pages, so
Phase 3's motion work is adjacent to a measured bucket rather than inside one.

## Route out before Phase 3 — this pipeline's headline deliverable

**[docs]** The health checklist says it outright, under **Task outside of model
capabilities**: *"Avoid using prompts that ask the model to perform a task for which
it has a known, fundamental limitation."*

**[measured-family]** `evidence.md` §2.1: the gap is not uniform. Four of eight
buckets are level with opus. Two produce **hard zeros** — not lower scores.

| this pipeline's deliverable | shape | Gemini | opus | zero-rate |
|---|---|--:|--:|--:|
| the launch site itself (Phase 3) | `static-page` | 22.2 | 66.9 | **71% of decided rows** |
| `OVERVIEW.md` / `PRD.md` edits into an existing repo (Phase 1) | `brownfield-integration` | 16.1 | 46.4 | **79%** |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

Half of this is already built into the skill: Phase 1 spawns `agy` and Phase 3
routes through `design-craft`/`ux-craft`, so a Gemini conductor routes the two weak
shapes out by following the skill. The table is what it keeps in-session.

**Omitted deliberately:** `react-app-ui` (63.2 against 68.7) and `optimality`
(74.7 against 75.0), where this family scores level; the reference guides, because
the corpus measures code and pages rather than instruction files; and Phase 4's
gate, because the corpus watches a model *build*, so `lane_pick.py` returns policy
unchanged for `verification`.

**[docs]** One documented strong path applies directly to Phase 3: *"For UI
generation, the model shows high design adherence and parity based on a reference
input, whether it's a screenshot, an image, or a full design system."* The skill
already has three (Mobbin screens, `design/mocks/html/*.html`, and the palette in
`site-craft-and-gsap.md`). **[measured-family]** Every `static-page` task in the
corpus was a prose brief with **no** reference input, so hand the exemplar over
rather than describing the house style: that is the mode the vendor claims and the
corpus never measured.

## Override 1 — the ledger is a filled table before Phase 3 renders anything

**[measured-family]** In the recorded run an enumeration stated in prose *with an
explicit completeness condition attached* still delivered one of six, so a count has
to become a cell to fill and a fraction to report. **[docs]** That is **Ambiguity**:
*"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition. Instead, provide objective constraints (for example, 'write a summary of
3 sentences or less' instead of 'write a brief summary')."*

The scan returned 2 quota rows and 6 relative qualifiers. Eight rows were added by
hand, because this skill's countable nouns are `platform`, `slice`, `timeline` and
`brief` rather than the deliverable nouns the regex reads.

| Scope | Where | Denominator | Filled |
|---|---|---|---|
| feature briefs traced into `PRD.md` | synthesis-protocol.md:65 | every file in `docs/features-to-triage/` | 14/14 · each with a requirement row id |
| PRD sections | SKILL.md:71 `"Comprehensive"` | 7 (vision · personas · matrix · API contracts · NFRs · security/BYOK · pricing) | 7/7 |
| feature-matrix status partitions | SKILL.md:71 | 4 (Built · In Progress · Triaged · Backlog) | 4/4 · counts 6/2/4/2 |
| platform badges | SKILL.md:47 | 5 (Windows · macOS · iPadOS · iOS · Linux) | 5/5 |
| platform switcher panes | site-craft-and-gsap.md:64 | 5, each with its own install command | 5/5 · `winget`/`brew`/App Store/App Store/`apt` |
| interactive mock slices | site-craft-and-gsap.md:48 | ≥ 3 (packet filter · pricing toggle · platform explorer) | 3/3 · each clickable |
| GSAP timelines | site-craft-and-gsap.md:38 | 3 named (hero entry · slice reveal · reduced-motion fallback) | 3/3 |
| Mobbin queries run | positioning-and-pricing.md:38 | 6 (4 screens + 2 flows) | 6/6 · 0 `n/a` |
| pricing tiers stated with exact figures | SKILL.md:88 | 2 ($9.99 perpetual · $4.99/mo) | 2/2 · both in copy and in the comparison matrix |
| validation assertions | SKILL.md:117 | 4 (contrast · em dashes · 320-2560px · script resolve) | 4/4 · `validate_site.py` exit 0 |

**[docs]** Shipped filled rather than described, because *"you can remove
instructions from your prompt if your examples are clear enough in showing the task
at hand."*

## Override 2 — the bound ledger, moved across by hand

The scan returned **0 bound rows** and counted 4 prohibitions as loose prose. Five
are attached to a countable property and were moved here by hand.

**[measured-family]** `evidence.md` §2.2 is the reason this override exists at all:
58% of failing UI assertions at `medium` and **86%** at `high` were bound-shaped,
against 8% for opus and 6% for the OpenAI lane. The most-repeated bound —
`has exactly one soft elevation shadow` — failed on *every* instance in its set while
the same run passed 37 of 39 other assertions. **A bound is violated by what you did
not write, so it survives every check that looks at what you did.** Read the produced
value off each instance rather than restating the rule.

| instance | property | stated bound | readback | within? |
|---|---|---|---|---|
| every copy block on the site | em dashes | 0 | `grep -c '—' <site>.html` | required |
| `<body>` at 320px and 2560px | horizontal scrollbar | 0 | `scrollWidth > clientWidth` per breakpoint | required |
| body text | contrast | ≥ 4.5:1 | computed ratio per text node | required |
| large text / headings | contrast | ≥ 3:1 | same probe, separate denominator | required |
| Three.js canvas | `devicePixelRatio` | ≤ 2 | read `renderer.getPixelRatio()` | required |
| elevated card surfaces | shadow layers | 1 | count box-shadow segments per card | required |

The last row is not in the skill. It is added because it is the exact rule the corpus
measured this family failing on every instance of, and this pipeline renders cards.

## Override 3 — the two design skills become two files a third phase reads

Phase 3 step 1 reads *"Load `/design-craft:design-craft` for typography, colour
hierarchies, elevation, and layout discipline. Load `/ux-craft:ux-craft` for
information density, keyboard navigation, scan paths, and micro-copy ergonomics."*
Composition phrased as a standard. The scan flagged zero qualitative skill
references; this one was found by reading, and it is a near-exact match for the
phrasing the mechanism below was measured on.

**[measured-family]** `evidence.md` §1.2.1 — on the one recorded run carrying that
phrasing both skill invocations were skipped, and the model's own diagnosis named the
mechanism: the design rules were already in context, and the generated file did not
mechanically depend on any artifact only those skills produce.

**[docs]** The remedy is Google's own: *"Chain prompts: For complex tasks that
involve multiple sequential steps, make each step a prompt and chain the prompts
together in a sequence. In this sequential chain of prompts, the output of one prompt
in the sequence becomes the input of the next prompt."*

```javascript
await Skill({ skill: "design-craft:design-craft" })  // → docs/launch/DESIGN.md
await Skill({ skill: "ux-craft:ux-craft" })          // → docs/launch/UX.md
await Skill({ skill: "create-luke-content:create-luke-content" })  // → docs/launch/copy-draft.md
// Phase 3's markup step reads all three before writing a line of HTML:
await Bash({ command: "test -s docs/launch/DESIGN.md && test -s docs/launch/UX.md && test -s docs/launch/copy-draft.md || exit 1" })
```

The same shape applies to Phase 2's positioning audit, which the skill already
gates correctly on a file (`docs/positioning/00-decision.md`); copy that pattern
rather than inventing one.

## Override 4 — Phase 1 calls this family, so its output is untrusted until read

**[measured-family]** The `agy` lane returned a fully-formed acceptance verdict for a
*different project* when called from a repo worktree while another `agy` was live:
another repo's id, unrelated captures, a confident verdict, nothing in it flagging
that it answered a different question. `--new-project` from a neutral cwd is what
prevents it, and the skill already says so.

What the skill does not say: **read `/tmp/synthesis.md` for your own subject before
writing `OVERVIEW.md` or `PRD.md`.** An off-topic answer is a lane failure, not a
synthesis. Check that the repository name and at least two feature-brief titles you
supplied appear in the output before promoting any of it.

**[docs]** `agy` echoes no model header, so the family rests on the pinned flag
rather than a readback; and *"Grounding with Google Search connects the Gemini model
to real-time web content, and should be enabled whenever the model may need to know
obscure or recent facts"* — Phase 1 is grounded in supplied files instead, which is
the stronger constraint and the reason **[docs]** the strictly-grounded system
instruction belongs on it: *"If the exact answer is not explicitly written in the
context, you must state that the information is not available."*

## Override 5 — verification is asked for, and this pipeline owns one exit code

**[docs]** *"Include specific verification steps in either the system instructions or
your prompts directly."* Two of the agentic template's nine rules say the same:
*"Review your output against the user's task"* and *"Verify your claims by quoting
the exact applicable information."*

**[derived]** Read this pipeline for exit codes and it owns exactly one:
`validate_site.py` at SKILL.md:117. Phase 1's traceability check, Phase 2's voice
lint and Phase 3's slice count have none. So each number in a delivery note carries
the command that produced it and that command's output, and **a denominator of zero
is a gate that never ran rather than a pass**.

**[measured-family]** What that prevents, precisely: a five-row self-review, all
`PASS`, naming a browser engine that failed on all four invocation attempts and never
ran, and *"100% pass rate on contrast"* from a probe never executed — measured
afterwards at 3.65:1 on every primary button and 1.00:1 on one glyph, invisible.
This pipeline asserts WCAG AA on *all* text elements, which is the same claim in the
same shape.

**Add these `test -s` guards to the Phase 4 chain**, since the skill ships no gate
for them: `docs/launch/DESIGN.md`, `docs/launch/UX.md`, `docs/launch/copy-draft.md`,
`OVERVIEW.md`, `PRD.md`. And prove a gate can fail before trusting it passing:
geminify's own quote gate went green across every file after a one-line change took
its checked count to zero.

## Override 6 — describe the render before judging it

**[docs]** *"Ask the model to describe the images before performing the task in the
prompt."* The worked example is exact: *"Describe this image"* over an airport board
returns a one-line caption, while naming what to extract returns thirteen rows.

So at Phase 4 step 3 — open the generated site — name what is in each capture first
(which breakpoint, which slice is open, whether the Three.js canvas has drawn,
whether the reduced-motion fallback is the resting state), then judge.
**[measured-family]** The recorded run opened 4 images for a 10-cell artifact across
3 render calls, which is why the denominator here is one capture per breakpoint per
motion state, all opened, the fraction reported.

**[docs]** And for the reasoning half: *"A prompt can fail because the model did not
understand the image at all, or because it did not perform the correct reasoning
steps afterward. To disambiguate between those reasons, ask the model to describe
what's in the image."*

## Three shorter overrides

**7 — cap the fan-out, and keep the conductor off its own review.** Phase 1 already
spawns one `agy`; cap concurrency at four across the whole pipeline, and never
delegate a check of your own output. **[derived]** If the conductor is Gemini, the
Phase 1 `agy` call is same-family self-grading on the synthesis: record it beside the
output rather than treating it as independent corroboration. **[docs]** Forks stay
closed sets: *"rephrase the instructions as a multiple choice question and ask the
model to choose an option."*

**8 — `OVERVIEW.md` and `PRD.md` say only what the repository contains.**
**[docs]** Adopt Google's strictly-grounded system instruction verbatim for the
synthesis prompt, with the scanned corpus as the context. Its last clause matters
most: *"If the exact answer is not explicitly written in the context, you must state
that the information is not available."* That is `synthesis-protocol.md`'s own
invariant against speculative filler, made executable. **[docs]**
Brevity is the resting state — *"By default, Gemini 3 models provide direct and
efficient answers"* — so ask by name for the Backlog partition and the
non-functional requirements, which drop first.

**9 — a document named in the prompt is read, then answered.** **[docs]** *"Your
knowledge cutoff date is January 2025"*, and *"The knowledge cutoff date for Gemini
3.7 Flash is March 2026"* — so `design-craft`, `ux-craft`, `create-luke-content`,
`trawl` and `positioning` are loaded rather than recalled, and so are the GSAP and
Three.js APIs this skill pins by version. **[measured-family]** Asked a question
naming three skills, the recorded run answered from memory without loading any; told
to fix it, it inverted the error and launched a skill instead of answering. Load,
then answer, as two ordered steps.

## Two short notes

**`thinking_level`.** A four-phase synthesis, a positioning audit, a rendered site
and a conformance gate is what **[docs]** Google describes `HIGH` as being for —
*"multi-step planning, verified code generation"* — and 3.7 Flash defaults to
`MEDIUM`. Raise it for that reason only. **[measured-family]** It is not a remedy for
anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and
tied on 58. On the bound-shaped failures it was measurably *worse* (86% at `high`
against 58% at `medium`).

**[docs]** And leave sampling alone: *"we strongly recommend keeping them at their
default values for Gemini 3.x models. Changing these parameters (for example, setting
the temperature below 1.0) can cause unexpected behavior, such as looping or degraded
performance."*

**Modules not written.** `states` did not fire: this pipeline enumerates phases and
platforms, not interface states. `injection` did not fire and would restate nothing
this skill handles. `count-contract` did not fire: the counts here are already
contracts once Override 1 lands. `delegation` fired only as the cap in Override 7.
`emphasis` fired on one token, and the honest reading is that this skill barely
shouts; read its one emphatic line as a plain rule and do not add more.

**Out of scope, mentioned once.** `references/evidence.md` presents several
conversion and engagement figures (a 41% higher engagement score, 2.8x conversion,
100% feature recall across 106 tasks) with no citation and no method. That is a
defect in the skill for every model, so it belongs to `improve-skill` rather than
here; do not treat those numbers as grounded when writing copy that repeats them.
