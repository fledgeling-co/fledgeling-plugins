# Visualisation — form, motion and interaction, per reading

Route every chart's form and colour through **`dataviz`**. This file covers what
that skill does not: which form each of the three readings gets, what may move,
what may be interactive, and why the chart is hand-authored SVG rather than a
charting library.

## The chart is inline SVG or a table, and that is not negotiable

Three of this skill's existing rules collide on this point and all three win:

- **Self-contained, aiming at zero network requests.** A charting library loaded
  from a CDN is a live dependency on a document meant to outlast the CDN.
- **The figure exists without script.** A chart drawn at runtime is absent with
  JavaScript off — and absent in the PDF, which is the copy most likely to be
  forwarded.
- **Print gets ink, not a canvas.** The exporter checks that no transient frame
  froze into the page.

So the mark is in the DOM before anything runs: inline `<svg>`, or a `<table>`
where the data is small enough that the table *is* the better figure. Script
enhances what is already there — adds the hover readout, the brush, the
transition between two states — and never creates it.

This is a constraint on the runtime, not on where the geometry comes from. A
build-time script that computes scales and emits SVG is fine and often right;
what may not ship is a library that draws on load.

## TanStack Charts is a vocabulary here, not a dependency

<https://tanstack.com/charts/catalog> is the most useful chart-form catalogue
available, and its grammar — marks, channels, scales, layered composition, in
the Wilkinson / ggplot2 / Vega-Lite / Observable Plot line — is the right way to
*think* about a figure even when you are writing the SVG by hand. Read it to
choose a form and to see how a form is normally composed.

Two things to hold while doing so:

- **Do not add it to a report.** The runtime rule above rules it out, and the
  library is **pre-alpha** — the docs track unreleased `main`, the newest
  published release is 0.12.0, and the API is documented as liable to shift.
  Pinning a report's figures to that is a maintenance debt on a document whose
  whole point is to still be readable in a year.
- **Take the form and the composition, not the code.** What transfers is "this
  claim wants a slopegraph", "a difference chart shades above and below",
  "percentile ribbons carry the uncertainty" — and the discipline of naming the
  mark, the channels and the scale before drawing anything.

The families worth knowing by name, because they map onto what a claim is
doing rather than onto what the data looks like:

| The claim is about | Families | Typical marks |
|---|---|---|
| change over time | trend, change | line, moving average, slopegraph, difference, arrows |
| how sure we are | range / uncertainty | band, error bars, percentile ribbon |
| what it is made of | composition | stacked area, normalised share, streamgraph, waterfall, funnel |
| how things compare | bar, comparison | sorted bars, grouped, lollipop, dumbbell, mirrored |
| whether two things move together | relationship | scatter, regression, connected scatter, log scale |
| the shape of the spread | distribution | histogram, box, ECDF, beeswarm, ridgeline, violin, hexbin |
| where it happens | spatial | choropleth, bubble map, contour, vector field |
| how it flows or nests | hierarchy, network | treemap, sunburst, sankey, force graph |
| one number in context | composition (KPI), polar | sparkline tile, gauge, donut with a centre total |

Prefer the plainest form that carries the claim. A sunburst is a beautiful way
to make a two-level hierarchy harder to read than a sorted bar chart.

## What each reading gets

Same data, same claim, same scales. What changes is how much apparatus is on
screen — never the geometry underneath.

| | **Primer** | **Brief** | **Technical** |
|---|---|---|---|
| **Shows** | one comparison, the finding only | the comparison that carries the decision | the distribution, the interval, the outliers |
| **Labels** | direct on the marks; no legend, no axis to decode | direct labels, units named in words | full axes, units, n, and the interval |
| **Interaction** | play — tap or drag to reveal; nothing to learn | filtering to the reader's own case | inspection — hover readout, brushing, a table behind a disclosure |
| **Annotation** | one, naming the finding | the comparison and its caveat | every unmeasured region marked, containment stated |

Three rules hold across all three, and they are what make the set trustworthy
rather than three different arguments:

- **The scales agree.** Round the *labels* for Primer, never the geometry. A
  reader who switches register and sees the data change has caught the document
  lying in one of the two.
- **Every register's figure ships its static frame.** Print runs no animation
  and neither does a browser with script off. Three readings means three static
  frames wherever the figure differs, not one shared frame that matches none.
- **A figure omitted from a register follows its claim.** If the claim carries
  `omit` and an `omitReason`, its figure goes with it. A chart with no
  accompanying claim is decoration that survived an edit.

## What may move

The motion test from `report-craft.md` applies unchanged: an animation is
admissible only if you can finish *"this motion lets the reader perceive ___
that would otherwise require a difficult mental comparison."* Energy, delight
and polish are not admissible answers, and on a report they are answers that get
stripped at print anyway — so motion earns its place twice or not at all.

What that admits, in practice:

- **A transition between two states of one encoding.** Measured to reduce
  tracking error across every transition type tested. Object-tracking around
  1.25s, value change around 2s.
- **A staged reveal that follows the argument** — the baseline, then the
  measured series, then the annotation — where each stage is a step the prose
  is also taking.
- **A scrubbed or pinned episode** where the reader drives the change and the
  change *is* the evidence. GSAP owns this; CSS scroll timelines own reveals,
  because they run off the main thread.

What it excludes: an idle loop, a chart that animates on every scroll past, a
number that counts up, and staging more elaborate than the change it depicts —
extreme staging measured *worse* than direct animation for value changes.

**Primer's motion budget is the largest and its interaction budget is the
smallest.** Reveal and analogy carry a first-time reader; a control panel does
not. Technical inverts it: little motion, much inspection.

## What may be interactive

Interaction is admissible when it lets a reader ask a question the static figure
cannot answer, and inadmissible when it hides something the static figure should
have shown. The failure mode is a chart whose finding is only visible after a
hover — which, by Tse's rule, means the finding is not on the page at all.

- **Keyboard first.** Every brush, filter, toggle and readout works without a
  pointer, or it does not ship.
- **The default view carries the claim.** Interaction refines; it never reveals
  the point.
- **Touch has no hover.** A readout that only exists on hover is absent on every
  phone.
- **Reduced motion still gets the interaction**, just without the tweening —
  the reduced branch is a first-class mode, not every duration set to zero.

## Integrity

`report-craft.md` §6 carries the chart-integrity rules and the five defects a
blind panel found on real pages produced by this skill — selective hatching of
unmeasured regions, unbounded uncertainty, unstated set containment, SVG
annotation type falling below a legible floor at narrow widths, and a linear
scale hiding a 33× spread. Read them before drawing; every one of them survived
an automated gate.

One rule from that list is worth repeating here because three readings multiply
it: **front-page arithmetic gets checked, so check it first.** Every ratio,
percentage and multiple on the first screen is recomputed from the ledger's own
numbers before the report ships — in each register, since a Primer that
re-expresses 95.4% as "about 19 in every 20" has done arithmetic the ledger
should record and the auditor cannot verify.
