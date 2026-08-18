# Visualisation — form, motion and interaction, per reading

Route every chart's form and colour through **`dataviz`**. It owns the form
heuristic, the palette formula and the mark specs, and it is not optional
here: a page that argues from numbers and picks its own chart colours has
spent the credibility the evidence bought. `page-craft.md` §7 carries chart
integrity — baselines, aspect ratio, area encoding, uncertainty, editorial
titles — and it is the part readers cannot catch for themselves.

This file covers what neither does: where the mark comes from, which form
each of the three readings gets, what may move in it, and what may be
interactive.

## The mark is in the DOM before anything runs

A published page is self-contained and aims at zero network requests, and
its figures have to survive JavaScript being off. So the chart is inline
`<svg>` or a `<table>` in the source, and script *enhances* what is
already there — adds the hover readout, the brush, the scrubbed transition
— rather than creating it. A figure drawn at load is absent without script
and absent to anything that reads the page without executing it.

This constrains the **runtime**, not the authoring. A build-time script
that computes scales and emits SVG is fine and is usually right. What may
not ship is a library that draws on load.

## Three lanes, and the claim picks the lane

| Lane | Reach for it when | Ships |
|---|---|---|
| **CSS/DOM** | ≤ ~8 rows, one dimension, no axis maths — comparisons, shares, ratios, ranked bars, stat tiles | markup + tokens, no build step |
| **TanStack Charts, compiled at build time** | anything needing a scale, ticks, a distribution, a time axis, layered marks, uncertainty bands | inline SVG, no library on the page |
| **Hand-authored SVG** | a bespoke figure whose geometry *is* the argument — a diagram, an annotated cutaway, a device drawn from the subject | inline SVG |

Prefer the plainest lane that carries the claim. A sunburst is a beautiful
way to make a two-level hierarchy harder to read than a sorted bar chart,
and on a page whose premise is evidence, a form chosen for impressiveness
spends what the evidence earned.

## Lane 1 — native CSS and DOM

The lane that gets skipped, and the right answer more often than it gets
used. A five-row comparison does not need a rendering pipeline: it needs a
grid, one custom property per row, and tabular numerals.

```html
<figure class="fig">
  <figcaption>Carpet pickup, same protocol, 14 machines — the top five.</figcaption>
  <table class="barset">
    <tr style="--v:91"><th>Miele C3</th><td><span class="bar"></span></td><td class="n">91%</td></tr>
    <tr style="--v:88"><th>Sebo E3</th><td><span class="bar"></span></td><td class="n">88%</td></tr>
    <tr style="--v:62"><th>Shark HZ400</th><td><span class="bar"></span></td><td class="n">62%</td></tr>
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
```

What this lane buys, and why it is worth reaching for first: it is
editable by a human a year from now, it themes from the page's own tokens
in both schemes with no second artifact, it prints, it works with script
off, it is smaller than the SVG equivalent, and the data is readable in
the source as a table — which is the accessible fallback the other lanes
have to build separately.

Four rules, each a defect this lane produces by default:

- **The value travels with the mark.** A number pinned to the right edge
  of the *track* sits at a distance proportional to how short the bar is —
  a 5%-wide bar leaves its label reading as a loose column of digits. Lay
  the row out so the value follows the fill, and put it inside the fill,
  right-aligned in the on-fill colour, when the fill runs to the end.
- **One baseline under a group, not one per column.** Giving each column
  its own `border-bottom` and separating columns with a flex `gap` draws
  the axis as disconnected segments. Set the gap to zero, let `flex: 1`
  columns abut so the borders join, and centre each bar with `max-width`.
- **`tabular-nums` on every figure**, in the table, the tick and the stat
  tile, or the digits do not align and the column reads as ragged.
- **A percentage-width bar is a bar chart, so it starts at zero.** The
  encoding is length. There is no honest truncated version of this lane.

Where this lane runs out: anything needing a computed scale, tick marks, a
non-linear axis, a second dimension, or a line through points. CSS cannot
draw a polyline honestly, and a "line chart" assembled from rotated divs
is a lie with extra steps. Those go to lane 2.

## Lane 2 — TanStack Charts as a build-time compiler

`@tanstack/charts` is a chart grammar in the Wilkinson / ggplot2 /
Vega-Lite / Observable Plot line: marks consume your rows directly,
channels describe the visual encodings, scales map them, and the engine
compiles a **renderer-neutral keyed scene** which it hands to a host. Its
own description is "a TypeScript visualization grammar for responsive,
accessible, server-rendered application charts", and the catalogue at
<https://tanstack.com/charts/catalog> is the best chart-form reference
available whichever lane you end up in.

The reason it belongs here rather than on the banned list: **one of its
hosts is static SVG, and the scene compiler runs in plain Node with no
DOM.** So it is used as a compiler at build time, and what reaches the
reader is inline SVG with no library, no runtime and no network request —
the runtime rule above satisfied exactly, with a real grammar behind the
geometry instead of hand-rolled path arithmetic.

**Its status is pre-alpha and that is a build-time risk, not a page
risk.** The README carries "It is pre-alpha and not ready for production
use" and tracks unreleased `main`; the published release is `0.14.0`. Held
at build time the exposure is bounded: pin the exact version, commit the
build script beside the page, and keep the emitted SVG in the page. If the
API shifts, the next page's script needs editing — the pages already
published keep rendering forever, because what shipped was markup.

### The recipe, measured

Verified 18 Aug 2026 on `@tanstack/charts@0.14.0`, Node v22.23.1, macOS —
no DOM, no browser, string out:

```js
import { defineChart, createChartScene, renderChartSvg, barY } from '@tanstack/charts'
import { scaleBand }   from '@tanstack/charts/scales/band'
import { scaleLinear } from '@tanstack/charts/scales/linear'

const def = defineChart({
  marks: [ barY(rows, { x: 'month', y: 'value' }) ],   // data FIRST, options second
  x: { scale: scaleBand },                             // the FACTORY, uncalled
  y: { scale: scaleLinear },
})

const svg = renderChartSvg(createChartScene(def, { width: 640, height: 320 }), {
  className: 'fig-pickup',
  ariaLabel: 'Carpet pickup by machine: the Miele leads at 91%.',
})
```

Then write `svg` into the page. Four things that behaviour pins down:

- **`ariaLabel` is required** — the renderer throws without it. The chart
  is accessible by construction, and the label is the place the editorial
  conclusion goes, not a description of the encoding.
- **The `description` option does not emit `<title>` or `<desc>`.** The
  long-description obligation stays yours: the caption and the structured
  table beneath the figure, as always.
- **Fills emit `var(--ts-chart-1, #2563eb)`.** The palette is overridable
  from CSS, so `dataviz`'s chosen colours land as `--ts-chart-N` on
  `:root` and **one compiled SVG serves both themes** — no second artifact
  and no inverted palette to measure separately.
- **Compact scales cover linear, band, point and ordinal only.** Temporal,
  log and piecewise scales come from the granular `d3-scale` modules,
  which the library is built to accept. §7's rule that a 33× spread wants
  a log axis therefore means installing `d3-scale`, not settling for
  linear.

### Two traps that produce a wrong chart with no error

Both were hit while measuring this, and both matter more here than in an
app, because a chart that renders confidently and wrongly is exactly the
class §7 exists to catch:

- **Data is the first positional argument.** `barY(rows, { x, y })` is
  correct. `barY({ data: rows, x, y })` passes the options object *as* the
  data source, which iterates to nothing: the mark group renders empty,
  the axes render fine, and nothing throws.
- **A called scale keeps its authored domain.** `scaleLinear()` resolves
  to its default `0–1`, so the axis reads `0.0 · 0.2 … 1.0` while the
  marks draw to their own extent — measured, four bars against a wrong
  axis, silently. Pass the factory uncalled (`scaleLinear`) and it infers
  the domain from the channel.

So the build script's own check is not "did it throw" but **did the marks
appear and does the axis span the data**: count the emitted mark elements
against the row count, and read the tick labels back. Two lines, and they
catch both traps.

### The vocabulary, which is the part that transfers

Even in lanes 1 and 3, name the mark, the channels and the scale before
drawing. The families map onto what a *claim* is doing rather than onto
what the data looks like:

| The claim is about | Marks and transforms |
|---|---|
| change over time | `line`, `area`, `difference`, `arrow`, `transform/rolling-window`, `transform/cumulative` |
| how sure we are | `area` as a band, `rule`, `box`, `tick` |
| what it is made of | `transform/stack`, `transform/normalize`, `transform/waterfall`, `transform/mosaic`, `waffle` |
| how things compare | `bar` sorted, `dot` as lollipop, paired `dot` as dumbbell, `transform/rank`, `transform/group` |
| whether two things move together | `dot`, `regression`, `link` |
| the shape of the spread | `transform/bin`, `box`, `violin`, `ridgeline`, `spatial/hexbin`, `spatial/density` |
| where it happens | `geo`, `spatial/contour`, `spatial/voronoi`, `vector` |
| how it flows or nests | `network/sankey`, `network/force`, `hierarchy/{tree,treemap,sunburst}` |
| one number in context | a stat tile in lane 1, `polar` where the claim is genuinely cyclical |
| the same claim across cases | `facet` — small multiples, which beat one crowded chart nearly always |

## Lane 3 — hand-authored SVG

For the figure whose geometry is the argument: a diagram of a mechanism, an
annotated cutaway, a device or document drawn from the subject's own
world. This is where the page's visual language lives, and it is the lane
`aesthetic-direction.md` means by "chart grammar is never reused". Keep the
type size independent of the `viewBox` so annotations do not fall below the
legible floor at 400px — see §7.

## What each reading gets

Same data, same claim, same scales. What changes is how much apparatus is
on screen — never the geometry underneath.

| | **Primer** | **Brief** | **Technical** |
|---|---|---|---|
| **Shows** | one comparison, the finding only | the comparison that carries the argument | the distribution, the interval, the outliers |
| **Labels** | direct on the marks; no legend, no axis to decode | direct labels, units named in words | full axes, units, n, and the interval |
| **Interaction** | play — tap or drag to reveal; nothing to learn | filtering to the reader's own case | inspection — hover readout, brushing, a table behind a disclosure |
| **Annotation** | one, naming the finding | the comparison and its caveat | every unmeasured region marked, containment stated, disagreement shown |
| **Motion budget** | largest — reveal and analogy carry a first-time reader | moderate | smallest — little motion, much inspection |

Three rules hold across all three, and they are what make the set
trustworthy rather than three different arguments:

- **The scales agree.** Round the *labels* for Primer, never the geometry.
  A reader who switches register and sees the data change has caught the
  page lying in one of the two.
- **Every register's figure renders from its own state.** Readers skip
  faster than animations complete, in every register, so no claim exists
  only inside an animated intermediate frame — and a scrubbed episode
  restores correctly on a reverse scroll.
- **A figure omitted from a register follows its claim.** If the claim
  carries `omit` and an `omitReason`, its figure goes with it. A chart with
  no accompanying claim is decoration that survived an edit.

## What may move

The motion test from `page-craft.md` §2 applies unchanged to anything
inside a figure: an animation is admissible only if you can finish *"this
motion lets the reader perceive ___ that would otherwise require a
difficult mental comparison."* Energy, delight, premium quality and
immersion are not admissible answers. Interface feedback is a separate
budget and is governed by §2's micro-interaction tier, not by this one.

What that admits: a transition between two states of *one* encoding
(measured to reduce tracking error across every transition type tested —
object-tracking around 1.25s, value change around 2s); a staged reveal
that follows the argument where each stage is a step the prose is also
taking; and a scrubbed or pinned episode where the reader drives the
change and the change *is* the evidence.

What it excludes: an idle loop, a chart that re-animates on every scroll
past, a number that counts up, and staging more elaborate than the change
it depicts — extreme staging measured *worse* than direct animation for
value changes.

GSAP owns the scrubbed and pinned episodes and the tween between two
compiled states; CSS scroll timelines own reveals, because they run off the
main thread. Three registers means the scrubbed episode may differ per
register — a Primer that scrubs through an analogy and a Technical that
scrubs through a distribution are two episodes, not one with different
labels.

**Animating a compiled figure means animating what is already in the
DOM.** Compile the two states at build time, ship both, and let GSAP tween
between the mark positions — `data-ts-key` is stable per datum, which is
what makes object identity hold across the transition. Never re-render a
chart at runtime to animate it; that puts the figure back behind script.

## What may be interactive

Interaction is admissible when it lets a reader ask a question the static
figure cannot answer, and inadmissible when it hides something the static
figure should have shown. The failure mode is a chart whose finding is
only visible after a hover — which, by Tse's rule, means the finding is not
on the page at all.

- **The default view carries the claim.** Interaction refines; it never
  reveals the point.
- **Keyboard first.** Every brush, filter, toggle and readout works
  without a pointer, or it does not ship.
- **Touch has no hover**, and a stray tap during scroll fires accidental
  triggers. A readout that only exists on hover is absent on every phone.
- **Reduced motion still gets the interaction**, without the tweening. The
  reduced branch is a first-class narrative mode, not every duration
  zeroed.
- **Canvas and 3D need a text equivalent** — a short description plus a
  structured table, in normal DOM order outside the canvas.

## Charts as components — the states nobody designs

A figure on a real page is not always populated. Where a figure's data is
partial, bounded or missing, design that state rather than letting the
chart render an empty frame:

- **Sparse** — one or two points get a stat tile with its label, never a
  line pretending to be a trend.
- **Unmeasured** — every gap in the series is marked, not just the
  convenient one. §7 carries the measured failure here.
- **Absent** — where the corpus has no data for a case the comparison
  otherwise covers, the cell says so. A blank cell reads as zero.

## Generated imagery in a figure

Never for the chart itself. `media-gen-pro` is for the illustration beside
the argument, not for anything carrying a number, an axis, a label or exact
text — image models garble those and re-prompting garbles them differently.
`source-imagery.md` owns the provenance contract, the licensing rule and
the narrow case for a generated clip.
