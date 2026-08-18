# Visualisation — form, motion and interaction, per reading

Route every chart's form and colour through **`dataviz`**. It owns the form
heuristic, the palette formula and the mark specs, and it is not optional
here: a report that argues from numbers and picks its own chart colours has
spent the credibility the evidence bought. `report-craft.md` §6 carries the
integrity rules and the five defects a blind panel found on real pages from
this skill.

This file covers what neither does: where the mark comes from, which form
each of the three readings gets, what may move, and what may be
interactive.

## The mark is in the DOM before anything runs

Three of this skill's rules collide on this point and all three win:

- **Self-contained, aiming at zero network requests.** A charting library
  loaded from a CDN is a live dependency on a document meant to outlast
  the CDN.
- **The figure exists without script.** A chart drawn at runtime is absent
  with JavaScript off — and absent in the PDF, which is the copy most
  likely to be forwarded.
- **Print gets ink, not a canvas.** The exporter checks that no transient
  frame froze into the page.

So the mark is in the DOM before anything runs: inline `<svg>`, or a
`<table>` where the data is small enough that the table *is* the better
figure. Script enhances what is already there and never creates it.

This is a constraint on the **runtime**, not on where the geometry comes
from. A build-time script that computes scales and emits SVG is fine and
is usually right; what may not ship is a library that draws on load.

## Three lanes, and the claim picks the lane

| Lane | Reach for it when | Ships | Prints |
|---|---|---|---|
| **CSS/DOM** | ≤ ~8 rows, one dimension, no axis maths — comparisons, shares, ranked bars, stat tiles | markup + tokens, no build step | yes, as ink |
| **TanStack Charts, compiled at build time** | anything needing a scale, ticks, a distribution, a time axis, layered marks, uncertainty | inline SVG, no library on the page | yes, as ink |
| **Hand-authored SVG** | a bespoke figure whose geometry *is* the argument — a mechanism, an annotated cutaway | inline SVG | yes, as ink |

Prefer the plainest lane that carries the claim. All three print, which is
the point of ruling out the fourth.

## Lane 1 — native CSS and DOM

The lane that gets skipped, and the right answer more often than it gets
used. A five-row comparison does not need a rendering pipeline: it needs a
table, one custom property per row, and tabular numerals.

```html
<figure class="fig">
  <figcaption>Drop rate by queue depth — the ceiling sits at 3,000/min.</figcaption>
  <table class="barset">
    <tr style="--v:6"><th>1,000/min</th><td><span class="bar"></span></td><td class="n">0.66%</td></tr>
    <tr style="--v:69"><th>3,000/min</th><td><span class="bar"></span></td><td class="n">6.88%</td></tr>
  </table>
</figure>
```

```css
.barset { border-collapse: collapse; width: 100%; }
.barset td.n { font-variant-numeric: tabular-nums; text-align: right; }
.barset .bar {
  display: block; height: .7rem; border-radius: 1px;
  width: calc(var(--v) * 1%); background: var(--series-1);
}
@media print { .barset .bar { background: var(--series-1) !important;
                              -webkit-print-color-adjust: exact;
                              print-color-adjust: exact; } }
```

What this lane buys: it is editable by a human a year from now, it themes
from the report's own tokens in both schemes with no second artifact, it
prints as ink with no export step, it works with script off, it is smaller
than the SVG equivalent, and the data is readable in the source as a table
— which is the accessible fallback the other lanes have to build
separately.

Five rules, each a defect this lane produces by default:

- **The value travels with the mark.** A number pinned to the right edge of
  the *track* sits at a distance proportional to how short the bar is.
  Let the value follow the fill; put it inside the fill, right-aligned in
  the on-fill colour, when the fill runs to the end.
- **One baseline under a group, not one per column.** A `border-bottom`
  per column plus a flex `gap` draws the axis as disconnected segments.
  Gap zero, `flex: 1` columns abutting so the borders join, bars centred
  with `max-width`.
- **`tabular-nums` on every figure**, in the table, the tick and the stat
  tile.
- **A percentage-width bar is a bar chart, so it starts at zero.** There
  is no honest truncated version of this lane.
- **`print-color-adjust: exact` on any mark carrying meaning by fill**, or
  the browser helpfully drops the background and prints an empty track.
  Colour is still never the only encoding — the value is beside it.

Where this lane runs out: a computed scale, tick marks, a non-linear axis,
a second dimension, or a line through points. CSS cannot draw a polyline
honestly, and a line chart assembled from rotated divs is a lie with extra
steps.

## Lane 2 — TanStack Charts as a build-time compiler

`@tanstack/charts` is a chart grammar in the Wilkinson / ggplot2 /
Vega-Lite / Observable Plot line: marks consume your rows directly,
channels describe the visual encodings, scales map them, and the engine
compiles a **renderer-neutral keyed scene** which it hands to a host. Its
own description is "a TypeScript visualization grammar for responsive,
accessible, server-rendered application charts", and the catalogue at
<https://tanstack.com/charts/catalog> is the best chart-form reference
available whichever lane you end up in.

The reason it belongs in a report at all: **one of its hosts is static
SVG, and the scene compiler runs in plain Node with no DOM.** So it is a
compiler at build time, and what reaches the reader is inline SVG with no
library, no runtime, no network request — and ink in the PDF. The runtime
rule is satisfied exactly, with a real grammar behind the geometry instead
of hand-rolled path arithmetic.

**Its status is pre-alpha and that is a build-time risk, not a document
risk.** The README carries "It is pre-alpha and not ready for production
use" and tracks unreleased `main`; the published release is `0.14.0`. Held
at build time the exposure is bounded: pin the exact version, commit the
build script into the report directory beside `claims.json`, and keep the
emitted SVG in the page. If the API shifts, the next report's script needs
editing — the documents already sent keep rendering forever, because what
shipped was markup. That property is why a pre-alpha dependency is
admissible here and a runtime one would not be.

### The recipe, measured

Verified 18 Aug 2026 on `@tanstack/charts@0.14.0`, Node v22.23.1, macOS —
no DOM, no browser, string out:

```js
import { defineChart, createChartScene, renderChartSvg, barY } from '@tanstack/charts'
import { scaleBand }   from '@tanstack/charts/scales/band'
import { scaleLinear } from '@tanstack/charts/scales/linear'

const def = defineChart({
  marks: [ barY(rows, { x: 'depth', y: 'dropRate' }) ],  // data FIRST, options second
  x: { scale: scaleBand },                               // the FACTORY, uncalled
  y: { scale: scaleLinear },
})

const svg = renderChartSvg(createChartScene(def, { width: 640, height: 320 }), {
  className: 'fig-drop',
  ariaLabel: 'Drop rate against queue depth: 0.66% at 1,000/min rising to 6.88% at 3,000.',
})
```

Then write `svg` into the block. Four things that behaviour pins down:

- **`ariaLabel` is required** — the renderer throws without it. The figure
  is accessible by construction, and the label is where the editorial
  conclusion goes, not a description of the encoding.
- **The `description` option does not emit `<title>` or `<desc>`.** The
  long-description obligation stays yours: the caption and the structured
  table beneath the figure.
- **Fills emit `var(--ts-chart-1, #2563eb)`.** The palette is overridable
  from CSS, so `dataviz`'s colours land as `--ts-chart-N` on `:root`, **one
  compiled SVG serves light, dark and print**, and the print block
  re-declares those tokens along with the rest.
- **Compact scales cover linear, band, point and ordinal only.** Temporal,
  log and piecewise scales come from the granular `d3-scale` modules,
  which the library is built to accept. §6's rule that a 33× spread wants
  a log axis therefore means installing `d3-scale`, not settling for
  linear — that defect shipped once already.

### Two traps that produce a wrong chart with no error

Both were hit while measuring this, and both matter more in a report than
in an app, because a chart that renders confidently and wrongly is exactly
the class §6 exists to catch:

- **Data is the first positional argument.** `barY(rows, { x, y })` is
  correct. `barY({ data: rows, x, y })` passes the options object *as* the
  data source, which iterates to nothing: the mark group renders empty,
  the axes render fine, and nothing throws.
- **A called scale keeps its authored domain.** `scaleLinear()` resolves to
  its default `0–1`, so the axis reads `0.0 · 0.2 … 1.0` while the marks
  draw to their own extent — measured, four bars against a wrong axis,
  silently. Pass the factory uncalled (`scaleLinear`) and it infers the
  domain from the channel.

So the build script's own check is not "did it throw" but **did the marks
appear and does the axis span the data**: count the emitted mark elements
against the row count and read the tick labels back. Two lines, and they
catch both traps. Anything the script emits is also checked against the
ledger's own numbers, per §6's front-page arithmetic rule.

### The vocabulary, which is the part that transfers

Even in lanes 1 and 3, name the mark, the channels and the scale before
drawing. The families map onto what a *claim* is doing rather than onto
what the data looks like:

| The claim is about | Marks and transforms |
|---|---|
| change over time | `line`, `area`, `difference`, `arrow`, `transform/rolling-window`, `transform/cumulative` |
| how sure we are | `area` as a band, `rule`, `box`, `tick` |
| what it is made of | `transform/stack`, `transform/normalize`, `transform/waterfall`, `transform/mosaic`, `waffle` |
| how things compare | `bar` sorted, `dot` as lollipop, paired `dot` as dumbbell, `transform/rank` |
| whether two things move together | `dot`, `regression`, `link` |
| the shape of the spread | `transform/bin`, `box`, `violin`, `ridgeline`, `spatial/hexbin` |
| where it happens | `geo`, `spatial/contour`, `spatial/voronoi`, `vector` |
| how it flows or nests | `network/sankey`, `network/force`, `hierarchy/{tree,treemap,sunburst}` |
| one number in context | a stat tile in lane 1, `polar` where the claim is genuinely cyclical |
| the same claim across cases | `facet` — small multiples, which beat one crowded chart nearly always, and paginate better |

## Lane 3 — hand-authored SVG

For the figure whose geometry is the argument: a mechanism, an annotated
cutaway, an instrument drawn from the subject's own world. This is where
the report's visual language lives, and it is the lane
`design-system.md` means by "chart grammar is never reused". Hold the type
size independent of the `viewBox` so annotations do not fall below the
legible floor at 400px — see §6.

## What each reading gets

Same data, same claim, same scales. What changes is how much apparatus is
on screen — never the geometry underneath.

| | **Primer** | **Brief** | **Technical** |
|---|---|---|---|
| **Shows** | one comparison, the finding only | the comparison that carries the decision | the distribution, the interval, the outliers |
| **Labels** | direct on the marks; no legend, no axis to decode | direct labels, units named in words | full axes, units, n, and the interval |
| **Interaction** | play — tap or drag to reveal; nothing to learn | filtering to the reader's own case | inspection — hover readout, brushing, a table behind a disclosure |
| **Annotation** | one, naming the finding | the comparison and its caveat | every unmeasured region marked, containment stated |

Three rules hold across all three, and they are what make the set
trustworthy rather than three different arguments:

- **The scales agree.** Round the *labels* for Primer, never the geometry.
  A reader who switches register and sees the data change has caught the
  document lying in one of the two.
- **Every register's figure ships its static frame.** Print runs no
  animation and neither does a browser with script off. Three readings
  means three static frames wherever the figure differs, not one shared
  frame that matches none.
- **A figure omitted from a register follows its claim.** If the claim
  carries `omit` and an `omitReason`, its figure goes with it. A chart with
  no accompanying claim is decoration that survived an edit.

## What may move

The motion test from `report-craft.md` §4 applies unchanged to anything
inside a figure: an animation is admissible only if you can finish *"this
motion lets the reader perceive ___ that would otherwise require a
difficult mental comparison."* Energy, delight and polish are not
admissible answers, and on a report they get stripped at print anyway — so
motion inside a figure earns its place twice or not at all. Interface
feedback is a separate budget, governed by §4's micro-interaction tier.

What that admits:

- **A transition between two states of one encoding.** Measured to reduce
  tracking error across every transition type tested. Object-tracking
  around 1.25s, value change around 2s.
- **A staged reveal that follows the argument** — the baseline, then the
  measured series, then the annotation — where each stage is a step the
  prose is also taking.
- **A scrubbed or pinned episode** where the reader drives the change and
  the change *is* the evidence. GSAP owns this; CSS scroll timelines own
  reveals, because they run off the main thread.

What it excludes: an idle loop, a chart that animates on every scroll
past, a number that counts up, and staging more elaborate than the change
it depicts — extreme staging measured *worse* than direct animation for
value changes.

**Animating a compiled figure means animating what is already in the
DOM.** Compile both states at build time, ship both, and let GSAP tween
between the mark positions — `data-ts-key` is stable per datum, which is
what makes object identity hold across the transition. Never re-render a
chart at runtime to animate it; that puts the figure back behind script
and out of the PDF.

**Primer's motion budget is the largest and its interaction budget is the
smallest.** Reveal and analogy carry a first-time reader; a control panel
does not. Technical inverts it: little motion, much inspection.

## What may be interactive

Interaction is admissible when it lets a reader ask a question the static
figure cannot answer, and inadmissible when it hides something the static
figure should have shown. The failure mode is a chart whose finding is only
visible after a hover — which, by Tse's rule, means the finding is not on
the page at all.

- **Keyboard first.** Every brush, filter, toggle and readout works without
  a pointer, or it does not ship.
- **The default view carries the claim.** Interaction refines; it never
  reveals the point.
- **Touch has no hover.** A readout that only exists on hover is absent on
  every phone.
- **Reduced motion still gets the interaction**, just without the tweening
  — the reduced branch is a first-class mode, not every duration zeroed.
- **Nothing interactive is load-bearing in print.** Whatever a filter or a
  brush would reveal is either on the static frame or stated in the
  caption.

## Charts as components — the states nobody designs

Where a figure's data is partial, bounded or missing, design that state
rather than letting the chart render an empty frame:

- **Sparse** — one or two points get a stat tile with its label, never a
  line pretending to be a trend.
- **Unmeasured** — every gap in the series is marked, not just the
  convenient one. §6 carries the measured failure.
- **Absent** — where the session has no data for a case the comparison
  otherwise covers, the cell says so. A blank cell reads as zero.

## Integrity

`report-craft.md` §6 carries the chart-integrity rules and the five defects
a blind panel found on real pages produced by this skill — selective
hatching of unmeasured regions, unbounded uncertainty, unstated set
containment, SVG annotation type falling below a legible floor at narrow
widths, and a linear scale hiding a 33× spread. Read them before drawing;
every one of them survived an automated gate.

One rule from that list is worth repeating here because three readings
multiply it: **front-page arithmetic gets checked, so check it first.**
Every ratio, percentage and multiple on the first screen is recomputed from
the ledger's own numbers before the report ships — in each register, since
a Primer that re-expresses 95.4% as "about 19 in every 20" has done
arithmetic the ledger should record and the auditor cannot verify.

## Generated imagery in a figure

Never for the chart itself. `media-gen-pro` is for the illustration beside
the argument, not for anything carrying a number, an axis, a label or exact
text — image models garble those and re-prompting garbles them differently.
`source-imagery.md` owns the provenance contract, the licensing rule and
the narrow case for a generated clip.
