# Data Viz: Charts That Carry the Message

Design any chart, graph, KPI tile, or dashboard so the *data* does the talking. Use this whenever a deliverable visualizes numbers — a dashboard, a stats section on a landing page, a deck slide with a chart, a report figure. **Data slop — decorated charts that don't support a message — is the numeric cousin of AI slop**, and dashboards are where generated design most reliably gives itself away.

The governing rule inherits from SKILL.md ch. 5: a chart earns its place by answering a question the viewer actually has. A chart nobody asked a question of is decoration wearing axes.

## Phase 1: One message, then one form

Before drawing anything, state the message the chart exists to deliver ("signups tripled after launch", "region B lags every other region"). If you can't write the sentence, don't draw the chart — show the number, or nothing.

Then pick the form from the message, never from variety:

| The message is about… | Reach for | Never |
|---|---|---|
| Change over time (trend) | Line; area only when volume/cumulation is the point | Bars for 50 time points |
| Comparison between categories | Horizontal bars (labels stay readable), sorted by value | Pie; radar |
| Part-of-whole | Pie/donut **≤5 slices** with one slice as the story; otherwise a sorted bar | Pie with 8 slices and a legend-hunt |
| Distribution | Histogram, box, or dot strip | A line pretending bins are a trend |
| Correlation | Scatter (+ trend line when it's the message) | Dual-axis line pairs (they imply correlation by construction) |
| A single figure | A stat tile: big number + small label + comparison delta | A gauge; a lone pie at 73% |
| Ranked flows / funnels | Sorted bar or funnel with explicit stage-loss labels | Sankey unless flows genuinely branch |

One chart, one message. Two messages = two charts, or the stronger one wins. Sort categorical data by value (alphabetical order is information-free); time series keeps time order.

## Phase 2: Ink discipline — data over decoration

The chart's visual budget goes to the data marks; everything else whispers:

- **Gridlines**: horizontal only in most charts, 1px, low-contrast neutral (a tint of the background family, not mid-gray) — visible when sought, invisible when reading marks. Never vertical + horizontal grids by default.
- **Axes**: drop the axis line where gridlines already carry alignment; label units once in the axis title, not on every tick (`Revenue ($M)` then `0 · 5 · 10`). 4–6 ticks; round numbers.
- **Direct labeling beats legends** for ≤4 series: label the line at its endpoint in the series color. Legends, when unavoidable, sit adjacent to the data (top-left of plot area or right of line endpoints), ordered to match the visual stacking, never floating in a far corner.
- **No chart junk**: no 3D, no shadows or gradients on data marks, no background fills behind the plot, no icons inside bars. A bar is a flat rectangle in a deliberate color — trend over decoration.
- **Numbers use the type system**: `font-variant-numeric: tabular-nums` on every axis, tick, table column, and stat tile so digits align; data labels at 11–12px minimum with the tracking rules from `hierarchy-rhythm-review.md`.
- **Value outranks label** on stat tiles (the number speaks, the label whispers) — and the comparison ("+12% vs last month") outranks both in usefulness; a lone number without a reference point is a fact, not a message.
- **A value label travels with its mark, and "inside the track" is not "with the bar".** On a horizontal comparison bar, a value pinned to the right edge of the *track* sits at a distance proportional to how short the bar is — measured, a 5%-wide bar left its `$0.4m` roughly 700px away from the mark it belonged to, reading as a column of loose numbers rather than as two labelled bars. Lay the track out as a flex row and let the value follow the fill; when the fill reaches 100% and there is no room after it, put the value *inside* the fill, right-aligned, in the on-fill colour. Both cases then read as one object.
- **One baseline under a bar group, not one per column.** A common construction gives each column its own track with a `border-bottom` and separates the columns with a flex `gap` — which draws the axis as three disconnected segments with gaps in it. Set the gap to zero and let `flex: 1` columns abut so the borders join into a single continuous rule, then centre each bar inside its column with `max-width`. The bars keep their spacing and the axis becomes one line.

## Phase 3: Color as encoding, not paint

Chart color is semantic — it encodes series identity, magnitude, or deviation, and nothing else:

- **Categorical series**: distinct hues at matched lightness/chroma (build with `oklch()`, per SKILL.md ch. 6), max ~6 before grouping into "other". The story series gets the brand accent; context series get muted neutrals — *emphasis by desaturation of everything else* beats a rainbow of equals.
- **Sequential data** (low→high): one hue ramped in lightness. **Diverging data** (deviation from a midpoint): two hues through a neutral middle — and the midpoint must be meaningful (zero, target, average).
- **Colorblind-safe by construction**: never red-vs-green as the only distinction; check series pairs at similar lightness; give every encoding a **second signal** — direct labels, marker shapes, line dash, or position — so the chart survives grayscale (this is SKILL.md ch. 9's "never color alone" applied to data).
- Semantic red/green (loss/gain) is legitimate *when paired with sign or direction markers* (`▲ +4.2%` / `▼ −1.8%`).
- One palette across the whole dashboard: the same metric keeps the same color on every chart; two charts using the same color for different things is a near-miss-grade violation.
- **Count accent *marks*, not accent text.** An automated accent-budget check usually walks text-bearing leaves, so it scores a filled bar, a progress track, a status dot and a rule at zero. Measured on one surface: four accent-filled "complete" progress bars plus one accent chip read as five accent objects to the eye and as one to the gate. Judge the budget on the rendered capture by counting every mark that carries the colour, then demote until one thing does — the fill that means "complete" can be the neutral ink, because the word beside it already says so.

## Phase 4: Honesty rules

- **Bar charts start at zero** — length is the encoding, a truncated bar lies. Line charts may zoom the y-range to show variation, but label the range and don't dramatize noise.
- Aspect ratio shapes perceived slope — banking to ~45° average slope is the honest default; a tall narrow line chart manufactures drama.
- No dual y-axes to imply correlation; small multiples or an indexed (=100) series instead.
- Annotate what the viewer can't infer: the launch date on the spike, the target line, the anomaly's cause. An unexplained spike is a question the chart raises and refuses to answer.
- Sample honestly: aggregate (daily→weekly, or windowed means) once a series exceeds ~1,000 rendered points — beyond legibility it's also a perf problem.
- Real-looking data per `ai-slop-check.md` §14: organic values (`47.2%`, not `50%`), plausible seasonality and noise, no perfectly smooth generated curves.

## Phase 5: Charts are components — give them states

A chart on a real surface is an async component; design all its states (the five-states rule from ux-craft binds here):

- **Loading**: skeleton in the chart's actual shape (bars/line silhouette), not a spinner in a void.
- **Empty**: a designed message with a next action ("No data yet — connect a source"), never a blank plot with axes around nothing.
- **Error**: what failed + retry, in place.
- **Sparse**: 1–2 data points get a stat tile or dot-with-label, not a line pretending to be a trend.
- **Interactive states** when live: hover shows the precise value (tooltip follows `interaction-states-pass.md`); the crosshair/point highlight is the feedback.

**Accessibility floor**: every chart gets a text alternative that states the *message*, not the encoding ("Signups tripled after the March launch, from 1.2k to 3.8k/week" — not "a line chart of signups") — as visually-hidden text, a caption, or `aria-label`; data tables as a `<details>` fallback for dense charts are the craft bar. Contrast rules apply to data marks: series lines/bars need 3:1 against the plot background.

## Phase 6: Dashboard composition

- **Hierarchy first**: one primary chart or KPI row answers the page's main question; supporting charts are visibly subordinate (smaller, fewer ticks, quieter). Eight equal-weight widgets is the flat-hierarchy failure mode of dashboards — see the iso-styling rule in `hierarchy-rhythm-review.md`.
- KPI tiles in a consistent grammar: value, label, delta with direction, spark line only when the trend is genuinely part of the answer.
- Shared x-axes align vertically stacked time charts; shared scales for comparable charts (two charts of the same metric on different y-scales is a lie by layout).
- Density: dashboards run tighter than marketing surfaces (this is the expert-tool context where more visible data is right), but the spacing scale still governs — density means smaller steps on the scale, not off-scale values.

## Phase 7: Review pass

When reviewing a chart-bearing surface, flag on sight: pie >5 slices · unsorted categorical bars · truncated bar axes · dual y-axes · gradient/3D/shadowed data marks · vertical+horizontal default grids · legend-hunts where direct labels fit · red/green-only distinctions · same color meaning two things across charts · a chart with no statable message · missing loading/empty/error states on live charts · non-`tabular-nums` numerals · lone numbers with no comparison. Fix with the same remedial order as everything else: delete before decorate — the strongest fix for a weak chart is usually a sentence and one number.
