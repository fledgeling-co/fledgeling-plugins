# launch-craft, calibrated for Gemini

Read this once before *Phase 1*, then run the four phases as written; each override names the phase,
file or line it lands on. The canon transfers. Three things do not. The pipeline's two most load-bearing
instructions are **standards rather than steps with an output** — Phase 3's `Load
/design-craft:design-craft` and `Load /ux-craft:ux-craft` (SKILL.md:108-109) and Phase 1's
`Comprehensive product requirements` (SKILL.md:71). Its headline deliverable lands in the exact shape
the benchmark corpus measured this family behind: a self-contained interactive page from prose. And
**its one exit code checks one of the four things Phase 4 credits it with** (O5).

## Epistemic status

| Tier | Used | Source |
|---|---|---|
| `[docs]` | throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | **n=1 ×2, plus n=106** | two Gemini sessions of *other* skills, and a 106-task benchmark |
| `[measured-here]` | **no** | no Gemini run of launch-craft has been recorded |
| `[derived]` | marked | reasoning from those, plus facts read out of this skill and its two scripts |

**The tier the evidence is about.** Every measured rate here is flash-tier and none of it projects onto
Pro. **[docs]** Defaults drift inside the family: *"If thinking_level is not specified, Gemini 3 will
default to high."*

**Unmeasured on this skill.** Nothing below is `[measured-here]`. Four gaps bite: nothing watches a
Gemini model drive `agy` recursively (Phase 1 calls this family through a CLI, so conductor and worker
are one family); nothing measures a Gemini model running Mobbin MCP, `/trawl:trawl`, or the Dossier
panels `/positioning:positioning` opens; the corpus's UI rows are React behaviour tasks, not
GSAP/Three.js scroll pages, so Phase 3's motion work is adjacent to a measured bucket; and Override 5's
script findings are read off source, not seen failing.

## Route out before Phase 3 — this pipeline's headline deliverable

**[docs]** The health checklist says it outright, under **Task outside of model capabilities**: *"Avoid
using prompts that ask the model to perform a task for which it has a known, fundamental limitation."*
**[measured-family]** `evidence.md` §2.1: the gap is not uniform — four of eight buckets are level with
opus, and two produce **hard zeros** rather than lower scores.

| this pipeline's deliverable | shape | Gemini | opus | zero-rate |
|---|---|--:|--:|--:|
| the launch site itself (Phase 3) | `static-page` | 22.2 | 66.9 | **71% of decided rows** |
| `OVERVIEW.md` / `PRD.md` edits into an existing repo (Phase 1) | `brownfield-integration` | 16.1 | 46.4 | **79%** |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

Half of this is already built in: Phase 1 spawns `agy` and Phase 3 routes through
`design-craft`/`ux-craft`, so following the skill routes both weak shapes out. **Omitted deliberately:**
`react-app-ui` (63.2 against 68.7) and `optimality` (74.7 against 75.0), level for this family; the four
reference guides, because the corpus measures code not instruction files; and Phase 4's gate, because
the corpus watches a model *build*.

**[docs]** One documented strong path applies directly to Phase 3: *"For UI generation, the model shows
high design adherence and parity based on a reference input, whether it's a screenshot, an image, or a
full design system."* The skill has three — Mobbin screens, `design/mocks/html/*.html`, the palette in
`site-craft-and-gsap.md` §1. **[measured-family]** Every corpus `static-page` task was a prose brief
with **no** reference; hand the exemplar over.

## What transferred intact

- **The four phases already chain on artifacts** — `OVERVIEW.md`, `PRD.md`,
  `docs/positioning/00-decision.md`, the site, exit 0: the shape **[docs]** Google prescribes, *"make
  each step a prompt and chain the prompts together in a sequence."*
- **Every hard count survives.** 5 platforms, 2 pricing tiers with exact figures, ≥ 3 interactive
  slices, 4 status partitions, 0 em dashes. **[measured-family]** `evidence.md` §2.1's `optimality`
  bucket is why: 74.7 against opus's 75.0 where the brief states a number.
- **`--new-project` from `/tmp`** (SKILL.md:67) is correct and load-bearing, and **Phase 2 gates
  composition on a file** — `00-decision.md` exists or `/positioning:positioning` runs, the pattern
  Override 3 copies to Phase 3.
- **Every skill is named in full, `plugin:skill`.** A bare name returns `Unknown skill` and the phase
  silently does not happen.

## Override 1 — the ledger is a filled table before Phase 3 renders anything

**[measured-family]** In the recorded run an enumeration stated in prose *with an explicit completeness
condition attached* still delivered one of six, so a count has to become a cell to fill and a fraction
to report. **[docs]** That is **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition. Instead, provide objective constraints (for example, 'write a summary
of 3 sentences or less' instead of 'write a brief summary')."*

The scan returned `quota rows 2 · bound rows 0 · relative 6 · qual skills 0 · emphasis 1`; nine rows
below were added by hand, because this skill's countable nouns are `platform`, `slice`, `timeline`,
stance item and `brief` rather than the deliverable nouns the regex reads.

| Scope | Where | Denominator | Filled |
|---|---|---|---|
| feature briefs traced into `PRD.md` | synthesis-protocol.md:65 `Every file` | the count `run_synthesis.py --dry-run` prints | 14/14 · each with a requirement row id |
| PRD sections | SKILL.md:71 `Comprehensive` | 7 (vision · personas · matrix · API contracts · NFRs · security/BYOK · pricing) | 7/7 |
| feature-matrix status partitions | SKILL.md:71 | 4 (Built · In Progress · Triaged · Backlog) | 4/4 · counts 6/2/4/2 |
| stance items read out of `00-decision.md` | SKILL.md:83 **and** positioning-and-pricing.md:12 | **6, not 4** — the two lists disagree | 6/6 · territory · hero line · category frame · beachhead persona · the single word to own · the named enemy |
| platform badges | SKILL.md:126 | 5 (Windows · macOS · iPadOS · iOS · Linux) | 5/5 |
| platform switcher panes | site-craft-and-gsap.md:60 | 5, each with its own install command | 5/5 · `winget`/`brew`/App Store/App Store/`apt` |
| interactive mock slices | site-craft-and-gsap.md:48 | ≥ 3 (packet filter · pricing toggle · platform explorer) | 3/3 · each clickable |
| GSAP timelines | site-craft-and-gsap.md:39 | 3 named (hero entry · slice reveal · reduced-motion fallback) | 3/3 |
| Mobbin queries run | positioning-and-pricing.md:40-41 | 6 (4 screens + 2 flows) | 6/6 · 0 `n/a` |
| pricing tiers stated with exact figures | SKILL.md:88 | 2 ($9.99 perpetual · $4.99/mo) | 2/2 · in copy and in the matrix |
| Phase 4 assertions actually executed | SKILL.md:140-143 | 4 stated | **1/4 by the script** — Override 5 |

Read the stance row twice: SKILL.md:83 asks for four items, positioning-and-pricing.md:12 asks for four
*different* ones overlapping on two, so a run satisfying either alone has read four of six and looks
complete. **[docs]** The table ships filled because *"you can remove instructions from your prompt if
your examples are clear enough in showing the task at hand."*

## Override 2 — the bound ledger, moved across by hand

The scan returned **0 bound rows** and counted 4 prohibitions as loose prose; six are attached to a
countable property and were moved here by hand. **[measured-family]** `evidence.md` §2.2: 58% of failing
UI assertions at `medium` and **86%** at `high` were bound-shaped, against 8% for opus and 6% for the
OpenAI lane, and `has exactly one soft elevation shadow` failed on *every* instance in its set while
that run passed 37 of 39 other assertions. **A bound is violated by what you did not write, so it
survives every check that looks at what you did.**

| instance | property | stated bound | readback | within? |
|---|---|---|---|---|
| every copy block on the site | em dashes | 0 | `grep -c '—' <site>.html` | required |
| `<body>` at 320px and 2560px | horizontal scrollbar | 0 | `scrollWidth > clientWidth` per breakpoint | required |
| body text | contrast | ≥ 4.5:1 | computed ratio per text node | required |
| large text / headings | contrast | ≥ 3:1 | same probe, separate denominator | required |
| Three.js canvas | `devicePixelRatio` | ≤ 2 | `renderer.getPixelRatio()` | required |
| the canvas when out of view | CPU | 0% | the `visibilitychange` teardown actually fires | required |
| elevated card surfaces | shadow layers | 1 | count box-shadow segments per card | required |

The last row is not in the skill. It is the exact rule the corpus measured this family failing on every
instance of, and this pipeline renders cards.

## Override 3 — the two design skills become two files a third phase reads

Phase 3 step 1 reads `Load /design-craft:design-craft for typography, color hierarchies, elevation, and
layout discipline` and `Load /ux-craft:ux-craft for information density, keyboard navigation, scan
paths, and micro-copy ergonomics`. Composition phrased as a standard. The scan flagged zero qualitative
skill references; this one was found by reading, and it is a near-exact match for the phrasing the
mechanism below was measured on.

**[measured-family]** `evidence.md` §1.2.1 — on the one recorded run carrying that phrasing both skill
invocations were skipped, and the model's own diagnosis named the mechanism: the rules were already in
context, and the generated file depended on no artifact only those skills produce. **[docs]** The remedy
is Google's own: *"Chain prompts: For complex tasks that involve multiple sequential steps, make each
step a prompt and chain the prompts together in a sequence. In this sequential chain of prompts, the
output of one prompt in the sequence becomes the input of the next prompt."*

```javascript
await Skill({ skill: "design-craft:design-craft" })  // → docs/launch/DESIGN.md
await Skill({ skill: "ux-craft:ux-craft" })          // → docs/launch/UX.md
await Skill({ skill: "create-luke-content:create-luke-content" })  // → docs/launch/copy-draft.md
// Phase 3's markup step reads all three before writing a line of HTML:
await Bash({ command: "test -s docs/launch/DESIGN.md && test -s docs/launch/UX.md && test -s docs/launch/copy-draft.md || exit 1" })
```

`/trawl:trawl` and the Mobbin calls take the same treatment: one file each, read by the copy step.

## Override 4 — Phase 1 calls this family, and `run_synthesis.py` does not call it

**[derived]** SKILL.md:66 offers two branches — run synthesis via `scripts/run_synthesis.py` *or* invoke
`agy` directly. Read the script: it globs the briefs, plans, specs and mocks, prints four counts, and
its last line is `Synthesis ready for agy execution with --new-project from /tmp.` It never spawns `agy`
and exits 0 either way, so only the second branch produces `/tmp/synthesis.md`. Take it — and take the
first too, with `--dry-run`, because the brief count it prints is the denominator for Override 1's
traceability row.

**[measured-family]** The `agy` lane returned a fully-formed acceptance verdict for a *different
project* when called from a repo worktree while another `agy` was live — another repo's id, a confident
verdict, nothing flagging that it answered a different question. `--new-project` from a neutral cwd
prevents it. What the skill does not say: **read `/tmp/synthesis.md` for your own subject before writing
`OVERVIEW.md` or `PRD.md`.** Check that the repository name and two feature-brief titles you supplied
appear in it before promoting any of it.

## Override 5 — the exit code checks one of the four assertions it is credited with

**[derived]** Phase 4 step 2 lists four assertions behind `validate_site.py` (SKILL.md:140-143). Read
the script: it checks em dashes. The other three are absent — no contrast computation, no viewport at
any width, no resolution check, only a case-insensitive substring match for `gsap`, `three` and
`<canvas`. It also checks two things the skill never lists (five platform names, both prices) by that
same test, so `mac` matches `machine`. **Its exit 0 licenses the contrast claim it never measured.**

| assertion, SKILL.md:140-143 | executed? | if you claim it, the readback is |
|---|---|---|
| WCAG AA contrast, all text elements | **no** | a compositing ratio per text node, denominator printed |
| zero em dashes | yes | the script's own output, quoted |
| no horizontal scrollbar 320-2560px | **no** | `scrollWidth > clientWidth` at each breakpoint |
| external scripts resolve with fallbacks | **substring only** | network status per `<script src>` |

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* So each number in a delivery note carries the command that produced it and that command's
output, and **a denominator of zero is a gate that never ran rather than a pass**.

**[measured-family]** What that prevents: a five-row self-review, all `PASS`, naming a browser engine
that failed on all four invocation attempts, and *"100% pass rate on contrast"* from a probe never
executed — measured afterwards at 3.65:1 on every primary button and 1.00:1 on one glyph, invisible.

**Add `test -s` guards to the Phase 4 chain** for `docs/launch/DESIGN.md`, `docs/launch/UX.md`,
`docs/launch/copy-draft.md`, `OVERVIEW.md` and `PRD.md`. And prove a gate can fail before trusting it
passing: geminify's own quote gate went green across every file after a one-line change took its checked
count to zero.

## Override 6 — describe the render before judging it

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* The worked
example is exact: *"Describe this image."* over an airport board returns a one-line caption, while
naming what to extract returns the thirteen rows.

So at Phase 4 step 3, name what is in each capture first — which breakpoint, which slice is open,
whether the Three.js canvas has drawn, whether the reduced-motion fallback is the resting state — then
judge. **[measured-family]** The recorded run opened 4 images for a 10-cell artifact across 3 render
calls, so the denominator is one capture per breakpoint per motion state, all opened, the fraction
reported. **[docs]** *"A prompt can fail because the model did not understand the image at all, or
because it did not perform the correct reasoning steps afterward. To disambiguate between those reasons,
ask the model to describe what's in the image."*

## Three shorter overrides

**7 — cap the fan-out, and keep the conductor off its own review.** Phase 1 spawns one `agy` and
`/positioning:positioning` opens Dossier panels; cap concurrency at four, and never delegate a check of
your own output. **[derived]** If the conductor is Gemini, that `agy` call is same-family self-grading:
record it beside the output, not as independent corroboration. **[docs]** Forks stay closed sets:
*"rephrase the instructions as a multiple choice question and ask the model to choose an option."*

**8 — `OVERVIEW.md` and `PRD.md` say only what the repository contains.** **[docs]** Adopt Google's
strictly-grounded system instruction verbatim for the synthesis prompt, scanned corpus as context; its
last clause matters most: *"If the exact answer is not explicitly written in the context, you must state
that the information is not available."* That is `synthesis-protocol.md`'s invariant against speculative
filler, made executable. **[docs]** Brevity is the resting state — *"By default, Gemini 3 models provide
direct and efficient answers"* — so ask by name for the Backlog partition and the NFRs, which drop
first.

**9 — a document named in the prompt is read, then answered.** **[docs]** *"Your knowledge cutoff date
is January 2025"*, and *"The knowledge cutoff date for Gemini 3.7 Flash is March 2026"* — so the five
skills this pipeline names are loaded rather than recalled, and so are the GSAP and Three.js APIs it
pins by version. **[measured-family]** Asked a question naming three skills, the recorded run answered
from memory without loading any; told to fix it, it inverted the error and launched a skill instead of
answering. Load, then answer, as two ordered steps.

## Two short notes

**`thinking_level`.** A four-phase synthesis, a positioning audit, a rendered site and a conformance
gate is what **[docs]** Google describes `HIGH` as being for — *"multi-step planning, verified code
generation"* — and 3.7 Flash defaults to `MEDIUM`. Raise it for that reason only. **[measured-family]**
It is no remedy for anything above: across 106 paired tasks `high` beat `medium` on 24, lost on 24, tied
on 58, and on bound-shaped failures was *worse* (86% against 58%). **[docs]** Leave sampling at *"their
default values for Gemini 3.x models."*

**Modules, written and not.** The scan earned `visual`, `gate` and `authorship` at three triggers each;
they are Overrides 6, 5 and 8. `bounded-constraint` did not reach the threshold and Override 2 carries
it anyway, from prohibitions moved across by hand. `states` did not fire (this pipeline enumerates
phases and platforms, not interface states); nor did `injection` or `count-contract`, whose counts
become contracts once Override 1 lands. `delegation` fired only as Override 7's cap, `emphasis` on one
token — read that line plainly and do not add more.

**Out of scope, mentioned once.** `evidence.md`'s conversion figures (41% engagement, 2.8x, 100% recall)
carry no citation and no method, and `run_synthesis.py`'s dead branch is a defect for every model: both
belong to `improve-skill`. Do not repeat those numbers in copy as if grounded.
