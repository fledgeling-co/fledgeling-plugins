# Visualisation — form, motion and interaction, per reading

Route every chart's form and colour through **`dataviz`**. `page-craft.md` §7
carries chart integrity — baselines, aspect ratio, area encoding, uncertainty,
editorial titles — and it is the part readers cannot catch for themselves.
This file covers what neither does: which form each of the three readings gets,
what may move in it, what may be interactive, and where the chart comes from.

## The mark is in the DOM before anything runs

A published page is self-contained and aims at zero network requests, and its
figures have to survive JavaScript being off. So the chart is inline `<svg>` or
a `<table>` in the source, and script *enhances* what is already there — adds
the hover readout, the brush, the scrubbed transition — rather than creating it.
A figure drawn at load is absent without script and absent to anything that
reads the page without executing it.

This constrains the runtime, not the authoring. A build-time script that
computes scales and emits SVG is fine and often right. What may not ship is a
library that draws on load.

## TanStack Charts is a vocabulary here, not a dependency

<https://tanstack.com/charts/catalog> is the best chart-form catalogue
available, and its grammar — marks, channels, scales, layered composition, in
the Wilkinson / ggplot2 / Vega-Lite / Observable Plot line — is the right way to
*think* about a figure even when writing the SVG by hand.

Two things to hold while reading it. **Do not add it to a page**: the runtime
rule above rules it out, and the library is **pre-alpha** — the docs track
unreleased `main`, the newest published release is 0.12.0, and the API is
documented as liable to shift, which is a poor bet for a page meant to still
render in a year. And **take the form, not the code**: what transfers is "this
claim wants a slopegraph", "percentile ribbons carry the uncertainty", and the
discipline of naming the mark, the channels and the scale before drawing.

The families worth knowing by name, because they map onto what a *claim* is
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
| one number in context | composition, polar | sparkline tile, gauge, donut with a centre total |

Prefer the plainest form that carries the claim. A sunburst is a beautiful way
to make a two-level hierarchy harder to read than a sorted bar chart — and on a
page whose whole premise is evidence, a form chosen for impressiveness spends
the credibility the evidence bought.

## What each reading gets

Same data, same claim, same scales. What changes is how much apparatus is on
screen — never the geometry underneath.

| | **Primer** | **Brief** | **Technical** |
|---|---|---|---|
| **Shows** | one comparison, the finding only | the comparison that carries the argument | the distribution, the interval, the outliers |
| **Labels** | direct on the marks; no legend, no axis to decode | direct labels, units named in words | full axes, units, n, and the interval |
| **Interaction** | play — tap or drag to reveal; nothing to learn | filtering to the reader's own case | inspection — hover readout, brushing, a table behind a disclosure |
| **Annotation** | one, naming the finding | the comparison and its caveat | every unmeasured region marked, containment stated, disagreement shown |
| **Motion budget** | largest — reveal and analogy carry a first-time reader | moderate | smallest — little motion, much inspection |

Three rules hold across all three, and they are what make the set trustworthy
rather than three different arguments:

- **The scales agree.** Round the *labels* for Primer, never the geometry. A
  reader who switches register and sees the data change has caught the page
  lying in one of the two.
- **Every register's figure renders from its own state.** Readers skip faster
  than animations complete, in every register, so no claim exists only inside an
  animated intermediate frame — and a scrubbed episode restores correctly on a
  reverse scroll.
- **A figure omitted from a register follows its claim.** If the claim carries
  `omit` and an `omitReason`, its figure goes with it. A chart with no
  accompanying claim is decoration that survived an edit.

## What may move

The motion test from `page-craft.md` §2 applies unchanged: an animation is
admissible only if you can finish *"this motion lets the reader perceive ___
that would otherwise require a difficult mental comparison."* Energy, delight,
premium quality and immersion are not admissible answers.

What that admits: a transition between two states of *one* encoding (measured to
reduce tracking error across every transition type tested — object-tracking
around 1.25s, value change around 2s); a staged reveal that follows the argument
where each stage is a step the prose is also taking; and a scrubbed or pinned
episode where the reader drives the change and the change *is* the evidence.

What it excludes: an idle loop, a chart that re-animates on every scroll past, a
number that counts up, and staging more elaborate than the change it depicts —
extreme staging measured *worse* than direct animation for value changes.

GSAP owns the scrubbed and pinned episodes; CSS scroll timelines own reveals,
because they run off the main thread. Three registers means the scrubbed episode
may differ per register — a Primer that scrubs through an analogy and a
Technical that scrubs through a distribution are two episodes, not one with
different labels.

## What may be interactive

Interaction is admissible when it lets a reader ask a question the static figure
cannot answer, and inadmissible when it hides something the static figure should
have shown. The failure mode is a chart whose finding is only visible after a
hover — which, by Tse's rule, means the finding is not on the page at all.

- **The default view carries the claim.** Interaction refines; it never reveals
  the point.
- **Keyboard first.** Every brush, filter, toggle and readout works without a
  pointer, or it does not ship.
- **Touch has no hover**, and a stray tap during scroll fires accidental
  triggers. A readout that only exists on hover is absent on every phone.
- **Reduced motion still gets the interaction**, without the tweening. The
  reduced branch is a first-class narrative mode, not every duration zeroed.
- **Canvas and 3D need a text equivalent** — a short description plus a
  structured table, in normal DOM order outside the canvas.

## Generated imagery in a figure

Never for the chart itself. `media-gen-pro` is for the illustration beside the
argument, not for anything carrying a number, an axis, a label or exact text —
image models garble those and re-prompting garbles them differently.

Where a generated asset does earn its place: caption it as generated, keep the
provenance in the methods note, use the `svg: true` path for diagrams and vector
artwork so the text stays text and the artwork scales, and resize any raster to
the width it displays at before wiring it in.
