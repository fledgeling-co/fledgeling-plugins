# Design system — reuse the project's, or derive one from the subject

A report should look like it belongs to something. Which something
depends on what already exists.

## Resolution order

1. **`DESIGN.md` at the project root** — the common case; 26 projects in
   this portfolio carry one.
2. **`design/DESIGN.md`, `docs/DESIGN.md`** — the same thing, filed
   differently.
3. **A sibling report's `DESIGN.md`** in `docs/reports/` — only when the
   new report is genuinely a companion to that one. Otherwise a sibling's
   system is a thing to differ from, not inherit.
4. **Generate one from the subject.**

Whichever wins, copy it into `docs/reports/<slug>/DESIGN.md`. The report
is self-contained; its design system should be readable beside it in a
year, after the project has moved on or the root file has been rewritten.

When reusing, note in the methods line which file it came from. When a
project's system and a report's needs genuinely conflict — the product is
a dark terminal tool and the report has to print — extend rather than
override, and record the extension in the copied file.

## Generating one

The generated system is derived from the **subject**, not selected from
taste. The test each decision has to pass: it maps to a named concept in
the material. A palette that would fit any topic expresses none.

Six things, and nothing else is needed to build:

**Register.** What kind of document is this pretending to be? A field
notebook, a control panel, an incident log, a specimen sheet, a
broadsheet, a maintenance manual, a court exhibit. This single choice
does most of the work, because it decides margins, rules, numbering,
labels and how loud a heading is allowed to be.

**The one visual device.** The thing the page is built around, drawn from
the subject — a timeline gutter, a fixed cross-section, a ledger column, a
tolerance band, a call-and-response of two panels. One, committed to.

**Palette logic**, with the justification stated. Not "blue and amber"
but "the two states the system can be in, plus the boundary between them,
which is the report's argument." Dominant colour with sharp accents
outperforms an evenly distributed set. Light and dark both ship; the PDF
is the light rendering.

**Type pairing** that belongs to this material, with a system-stack
fallback that is not embarrassing. Avoid the convergent defaults — Inter,
Roboto, Arial — not because they are bad faces but because they read as
unchosen.

**Motion signature** — what moves, and what perceptual job it does. If
the honest answer is "nothing needs to move", write that. A report with
no motion and a reason is better than one with reveals it cannot justify.

**Spacing scale and grid.** A real scale, stated as numbers, with
everything on it. Twenty blocks of ad-hoc spacing is not a design, it is
twenty accidents — and inconsistent alignment measurably costs reading
speed, where a consistent grid buys up to 22%.

## The file

```markdown
# DESIGN.md — <report slug>

**Register.** <what this document pretends to be, and why the subject asks for it>
**Device.** <the one visual device, and the concept it maps to>

## Tokens
--bg / --ink / --accent / --rule / --muted   (light)
… dark overrides
Spacing scale: 0 4 8 12 16 24 32 48 64 96
Type scale: 1.25 ratio from 17px body
Faces: <display> / <body> / <mono>, fallbacks: <system stack>

## Components
Block · figure + caption · KPI row · callout · citation marker ·
source registry · running header

## Motion
<what moves, the perceptual job, and the static frame it degrades to>

## Print
A4 portrait, 16/15/18mm. Light rendering. <what is suppressed>

## Do / don't
<three of each, specific to this subject>
```

## Varying between reports

The measured problem is real: layout similarity across the web fell 44%
over a decade, and the strongest correlate was shared use of a small
number of libraries — not shared palette. **The invariant that reads as
sameness is layout skeleton and motion signature.** Recolouring the last
report fixes nothing.

Before designing, read the sibling reports in `docs/reports/`. Treat
their section silhouettes, hero shapes, chart grammars and transition
metaphors as taken.

**Reuse freely** — and deliberately, because standardising the invisible
layer is what buys the budget to vary the visible one:

| Reuse | Never reuse |
|---|---|
| The claim ledger shape | Hero composition |
| Citation markup and behaviour | Section silhouette |
| The auditor and the exporter | Chart grammar |
| Focus styles, keyboard handling | Illustration system |
| Print rules and page geometry | Transition metaphor |
| The spacing-scale *discipline* | The scale's actual values |
| | Typography and palette |

## The review, run against the built page

A report fails the authored review if:

- its silhouette matches a sibling report once colour and copy are
  stripped
- changing the subject noun leaves the visual metaphor intact
- motion is repeated fade / slide / reveal recipes
- typography and texture are unrelated to the source material
- the hero is more specific than the evidence beneath it
- the same chart grammar appears regardless of data type
- there is no stated uncertainty or counterpoint anywhere in it

The last is not a visual test and belongs on the list anyway. A document
that resolves everything reads as generated, because a human with real
sources almost always has something they are unsure about.

The cheap silhouette check: screenshot this report and each sibling
full-length, greyscale, blur heavily, compare the block structure. If the
bands land in the same places, the skeleton was reused. Treat a match as
a prompt to look, not a verdict — there is no validated metric for
"recognisably templated", and this is a production heuristic.
