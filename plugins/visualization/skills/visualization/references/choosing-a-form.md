# Choosing a form — and whether it should be a chart at all

Decide this **before** colour, and before opening a type reference. Most bad
charts pick colours first; most bad diagrams pick a layout first.

## Two families, one question

This skill draws two things, and the routing question is the same for both:
*what must the reader do with it?*

- **Quantities** — magnitude, trend, distribution, part-to-whole, polarity. The
  reader compares values. This is a **chart**, and the encoding is a claim about
  numbers, so the honesty rules and the palette gate apply.
- **Structure and behaviour** — components, flows, states, sequence, hierarchy,
  ownership. The reader traces relationships. This is a **diagram**, and the
  connector grammar and complexity budget apply.

A request often contains both. Split it rather than merging: an architecture
diagram with a bar chart bolted into one corner does neither job.

## Is it even a chart?

| The data is… | Use | Not |
|---|---|---|
| A single current value (+ maybe a trend) | **Stat tile** — value, delta, sparkline | A one-bar bar chart |
| A handful of headline numbers | **KPI row** of stat tiles | A grouped bar chart |
| The one number the page leads with | **Hero figure** (≥48px, sans) | — |
| A single ratio against a limit | **Meter** on a same-hue track | A two-slice pie |
| More than ~7 classes that all carry meaning | A **table**, or table + chart | More colours |
| A relationship with no quantities | A **diagram** — pick the type | A chart with invented numbers |

If a three-column table communicates the same thing, pick the table. If a
well-written sentence does, write the sentence.

## The job → the chart form

| Job (what the reader must do) | Default form | Colour job |
|---|---|---|
| Compare magnitude, low → high | bar / column; heatmap for a grid | sequential (one hue) |
| Trend over time | line; area for a single series | sequential, or 1 categorical |
| Tell distinct series apart | grouped/stacked bar, multi-line | **categorical** |
| One series is the point, the rest are context | **emphasis** — highlight one, grey the rest | 1 hue + grey |
| Above/below a baseline; delta to target | diverging bar, or line vs baseline | diverging |
| Part-to-whole | stacked bar (horizontal for long names) | categorical |
| Ordered-scale share (Likert, sentiment) | diverging stacked bar, centred on neutral | diverging |
| Before → after per item | dumbbell | 1 hue, 2 weights |
| Change between exactly two states, several items | slopegraph | 1 hue + emphasis |
| Rank movement across snapshots | bump | categorical |
| One distribution per series | ridgeline | 1 hue |
| Distribution of one variable, a dot per item | beeswarm | 1 hue |
| Two variables, third as area | bubble | categorical, `--pairs all` |

**Sequential is the safe default.** Reach for categorical only when the data's
job is genuinely identity, and for **emphasis** when the story is one series —
emphasis is the most underused form and usually the honest answer to "make this
chart clearer".

## Series-count ladder (categorical)

| Series | Treatment |
|---|---|
| 1–3 | colour alone is comfortable; direct-label |
| 4 | adjacent forms stay safe, but direct labels become mandatory; all-pairs forms (scatter, bubble, choropleth, small multiples) cap at **three** |
| 5 | the palette's ceiling — legend plus selective direct labels |
| 6+ | fold the tail into "Other", facet into small multiples, or use composite encoding (hue × shape) |

Never solve "too many series" by generating another hue. A generated sixth hue is
indistinguishable from an existing slot under CVD and fails the gate.

## Then route to the type reference

Once the form is chosen, load its type reference for the layout grammar, the
element patterns and the type-specific budget. The chart types carry honesty
rules the diagram types do not — read them before drawing, not after.
