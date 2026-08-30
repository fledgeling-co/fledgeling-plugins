# visualization icon — the commission in one page

**Direction:** 2 Tahoe Gel-Glass, sub-register (a) — porcelain cushion tile carrying a
coloured gel object. Runner-up: 8 Instrument Emblem, rejected because putting the
product's own artifact on the tile says "analytics app" rather than *this* skill.

**Concept — the lit baseline.** Three graphite bars of unequal height standing on one
vermilion rule that runs the full width and glows. The baseline is the hero and the bars
are the context, because the skill's central honesty rule is that a length-encoded bar
starts at zero: the datum is what makes the bars mean anything.

**Family fit.** Porcelain ground, cool graphite gel, one warm accent, the shared squircle
from `squircle-path.txt` — same shelf as `warrant` and `should-compact`. The deliberate
separation from `warrant`, its nearest neighbour: warrant's bars are horizontal, of
decreasing width, in a descending sequence, four floating with only the narrowest lit and
landed — its accent is a bar. Here the bars are vertical, of unequal height in no order,
all three touching one rule, and the accent is the rule. Shelf check over 53 icons puts
the closest structural pair at 0.687 against a 0.80 flag, and warrant is not in the top
twelve.

## Four findings worth keeping

**1. A datum is defined by its overhang, and the number is measurable.** The concept says
the baseline is wider than the data it carries; the first draft spent 46px on that and it
read as a plinth cut to fit the bars. The corpus-steered raster reference overhangs its
own bar group by 98px left and 110px right on a bar group within 3% of the same width.
Raising the master to the reference's mean of 104 was a single-constant edit that cleared
three regressions the previous round could not fix, and it is the edit that made the rule
read as something the bars were measured *against*. Where a composition's argument is
about proportion, fit the proportion off the reference rather than choosing it.

**2. An edge catch is a resolution budget, not an amplitude.** Measured across the
reference's tall bar, luminance runs 128 / 108 / 91 / 94 / 92 / 100 / 135 edge to edge —
bright at both edges, darkest through the middle, which is a translucent body catching
light on its turned faces. The master had authored the opposite (dark edges, bright core:
an opaque cylinder). Correcting it raised the composite and *failed* the gate on 32px
self-contrast, and four amplitudes (0.40 / 0.30 / 0.24 / 0.20) with three catch widths
(2.2% / 3.5% / 5.5%) all returned **identically** 0.535. Identical results across a
parameter sweep mean the parameter is not the variable. The 32px histogram said why: the
catch lifted the 10th percentile from 0.392 to 0.476 while leaving the darkest pixels and
the count below 0.35 unchanged — deleting mid-dark pixels, not brightening dark ones,
because at 32px a 132px bar is 4.1 pixels and two lit edges plus a darker core is three
values in four after antialiasing has spent two on the silhouette.

The fix is a second file rather than a compromise: `icon.svg` keeps the catch,
`icon-small.svg` floors it, and the crossover is measured per size (self-contrast, master
vs floor — 48px: 0.7216/0.7059, 40px: 0.5737/0.5890, 32px: 0.5216/0.6000, 24px:
0.5137/0.5471, 16px: 0.6451/0.6118). SMALL_BELOW = 48. 16px recovers on its own because a
bar is 2 pixels by then and the catch has averaged away entirely; 32 is the size with just
enough room to be hurt.

**3. Emission is a draw-order problem before it is a material one.** The user said the
raster looked far more vibrant and was right; three rounds of material tuning had not
closed it. The largest single cause was that the contact shadow sat ON TOP of the halo
bloom, cancelling 40 points of chroma in exactly the band where the glow is legible
(measured with and without: 67 vs 107 against the reference's 146). A shadow over a
light source is a contradiction the eye reads instantly as "coloured object". The
second cause was a contaminated measurement — an earlier round had sampled the
reference's "porcelain" at a column that actually sits on its rule, so the halo was
fitted half the size it should have been. Only the third was a material constant, and
it was a sign error: the graphite ramp darkened toward the rule, so the warm bounce was
being painted onto near-black and read as rust rather than illumination.

**4. Lighting what a source touches is not the same as lighting the source.** r04 fixed
the bloom, the bounce and the ramp direction, and the icon still read as less vibrant
than the reference — because none of those touch the face of the rule. Its lower stops
ran `#C43F16` at 78% and `#8C2E0F` at the base, a dark rust, so the face fell away from
t≈0.20 and bottomed at red 147 where the reference holds 252-254 through t=0.63. Fitted
from the reference's own face column at the same offsets (its red at that depth, blue
set for the target R-B, its G-B gap preserved so the face stays orange as the red
rises), face mean red went 211 to 234 against the reference's 240, and all five sizes
improved. The generalisation: when an emitter still looks dim after its environment is
correct, measure the emitter's own cross-section — the environment and the source are
separate fits.

**The trade that would not dissolve, recorded rather than buried.** `self_contrast`
watches the p10 luminance bin, and that bin is entirely bar interior — no porcelain in
it. So ground emission is free and bar emission is not. Fitting the bounce to the
reference's measured +174 chroma needs BOUNCE_PEAK 0.62, which costs self-contrast at
every size (1024: 0.737 to 0.663). An eight-point sweep found the cost near-linear with
no knee. 0.26 is the largest value holding every invariant, leaving bar chroma at 39
against the reference's 121. The gap is legitimate: the reference's own self-contrast
is 0.533 against ours at 0.737 — it buys vibrancy with figure-ground, which a flat
pre-masked raster can afford and a 12/12 layered master cannot.

## Files

| file | what it is |
|---|---|
| `build_icon.py` | the generator. Geometry and material as named constants; every constant that was fitted carries its measurement in a comment. `--export` rasterises the shipped sizes. |
| `icon.svg` | the layered master, four named layers (bg / mid / fg / highlight). Ships 48px and above. |
| `icon-small.svg` | same geometry, catch floored. Ships below 48px. |
| `icon.png` / `-256` / `-128` / `-16` | the shipped exports. Each reproduces byte-identically from its stated source. |
| `icon-A2-fourbar.svg`, `icon-A3-edgebleed.svg` | the losing Engine A takes, scored on the sheet. |
| `icon-engineB-arrow-*.svg` | the Arrow take. Field-less, non-square viewBox, accent on the wrong object. |
| `icon-engineC-*.png` + `-masked.png` | the two raster takes. C1 masked is the loop's material reference. |
| `audit.html` | the contact sheet — six takes, all scored, `audit_sheet.py check` exit 0. |
| `loop-runs/` | the fidelity trajectory, one brief per round with its measurements. |
