# Marks, anatomy and interaction

The editorial register is a few fixed specs plus negative space. The data is the
only thing allowed to be loud. These specs sit *under* the skin — they say how
thick a mark is and where a label goes; `style-guide.md` says what colour it is.

## Mark specs

| Mark | Spec |
|---|---|
| Bar / column | ≤24px thick — cap it, let the band's leftover be air; grows from a single baseline |
| Line | 2px, round join and cap; 1.2px for non-focal series |
| Marker / end-dot | ≥8px (r ≥ 4), filled with the series colour |
| Area fill | the series hue at ~8–10% opacity — a wash, never a saturated block |
| Gridlines / axes | one step off the surface, hairline 1px, **solid** — never dashed |

Dashed gridlines read as "projection" or "threshold" when they are just a grid.
Dashing is reserved for meaning: optional, async, passive, or transit.

## The two spacers

- **Surface gap** — a 2px gap in the surface colour separates touching marks:
  every segment of a stacked bar, every adjacent bar, one consistent width.
- **Surface ring** — dots and end-markers carry a 2px ring in the surface colour
  so they stay legible where they cross a line or overlap. The ring is part of
  the hit target, not only spacing.

Never draw a border around a mark to separate it. The gap and the ring are the
mechanism; a stroke adds ink that isn't data.

## Labels and legend

**A legend is always present for two or more series.** One series needs no legend
box — the title already names it, and a box with one swatch restates the title.

- **Label selectively — never a number on every point.** Label the endpoint, the
  extreme, or the one series the story is about. Direct labels work *because*
  they are sparing.
- **Direct labels before gridlines; gridlines before a second axis** (and there
  is no second axis — see `chart-honesty.md`).
- **Measure before placing a label inside a mark.** Only set a label inside a bar
  or segment when the rendered text fits with padding on both sides. Otherwise
  move it outside the bar end, or drop it to the tooltip and the table view.
  Never `overflow: hidden` — cropping the first characters is worse than no
  label.
- **Text never wears the data colour.** Marks carry the series colour; labels,
  values, legends and axis text use ink / muted / soft. Identity comes from a
  coloured mark *beside* the text. The exception is a label set inside a filled
  region, where white or ink is chosen by the fill's luminance.
- **When end-labels collide, don't stack them.** Nudging labels apart detaches
  them from their lines. Use leader lines, facet into small multiples, or fall
  back to legend plus tooltip. Past ~4 converging series, small multiples is
  usually right.
- Bars → value at the tip. Columns → value on the cap. Lines → value at the end.
- Y-axis ticks round to clean numbers and carry the values you didn't label.

## Figures — when the form is a number

- **Stat tile**: label (sentence case) · value (sans semibold, auto-compact:
  1,284 / 12.9K / $4.2M) · optional signed delta against a *named* period ·
  optional 12-point sparkline in the de-emphasis hue with the current period in
  the accent.
- **Meter**: the fill carries severity; the unfilled track is a lighter step of
  the same ramp, so state reads across the whole bar.
- **Hero figure**: the one number a view leads with, ≥48px. In the diagram skin
  this is the one place Instrument Serif is permitted at size — the editorial
  register owns the page, unlike a product dashboard where a serif hero reads as
  off-brand. Exactly one per view.
- **Proportional figures for big numbers.** `tabular-nums` gives every digit the
  width of a zero, so `121` looks loose at display size. Reserve it for columns
  that align vertically — table rows, axis ticks.

## Interaction — for HTML charts only

A static diagram is the default and stays static. But an HTML **chart** with a
hover layer is more useful than one without, and the layer is part of the
deliverable rather than an upgrade. The exception is a bare stat tile.

- **Tooltips enhance, they never gate.** Every value a tooltip shows is reachable
  without it, through direct labels or the table view. Keyboard focus shows the
  same as hover.
- **The crosshair finds the X** on line and area charts, snapping to the nearest
  data position — readers aim at a date, never at a 2px line.
- **On bars, cells and dots the mark is the hit target**, and the hovered mark
  visibly responds.
- **One tooltip lists every series at that X**, values leading and series names
  secondary.
- **The hit target is bigger than the mark** — at least ~24px, including the
  surface gap. For dense scatter use a nearest-point layer so the pointer only
  has to be closest, not dead-centre.
- **Labels are untrusted data.** Series and category names arrive from CSVs, tool
  output and APIs. Insert them with `textContent`, never by concatenating into
  `innerHTML`.

Any script this adds must still satisfy the single-file contract: the chart's
complete meaning renders without JavaScript, and `self_check.py` passes.

## The table view

Every chart has a table-view twin — the WCAG-clean equivalent, in the same file.
It is what makes a colour encoding non-gating, what carries a value that wouldn't
fit as a label, and what a screen reader reads instead of a picture. A chart
whose values exist only in the geometry is not finished.
