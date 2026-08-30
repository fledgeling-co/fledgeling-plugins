# r04 — the emission

The user looked at the sheet and said C1 is far more vibrant than A1. They are right,
and rounds r01-r03 never addressed it: composite at 256 went 0.7205 -> 0.7155 ->
0.7204 -> 0.7196, ending fractionally BELOW the r00 baseline. Three rounds of motion
and no convergence. Those rounds fixed the halo's *footprint* on the porcelain and
the rule's *geometry*; none of them touched what the rule does to the bars, which is
where the difference actually lives.

EDIT CLASS: emission. The rule as a light source rather than a coloured fill.

## MEASURED, on the two 1024 renders in the same minute

Warm chroma (R−B) sampled INSIDE each bar, averaged across all three so one bar's
local shading cannot set the curve, as a function of px above the rule's top edge:

| px above rule | C1 reference | A1 master |
|---|---|---|
| 18  | **+174** | — |
| 28  | +154 | — |
| 40  | +121 | +26 |
| 55  |  +94 | — |
| 75  |  +64 | — |
| 100 |  +37 | — |
| 130 |  +15 | — |
| 165 |   ~0 | — |
| 20  | +103 | +37 |
| 70  |  +99 |  +4 |
| 110 |  +49 |  −9 |

And down the tall bar toward its foot (t = fraction of bar height):

| t | C1 luminance / R−B | A1 luminance / R−B |
|---|---|---|
| 0.78 | 81 / +58  | 39 / −7  |
| 0.88 | 105 / +117 | 47 / +14 |
| 0.94 | **141 / +191** | 63 / +34 |

Three separate facts fall out of that:

1. **The reference's bounce reaches ~165px up the bar; mine dies by ~50.** BOUNCE_H
   is 120 but the gradient's own stops put almost all the energy in the last 20%,
   so the effective reach is a quarter of the constant's value.
2. **The reference's bounce peaks near +174 chroma; mine peaks near +37.** Roughly
   4.7x too weak.
3. **The reference's foot GAINS luminance (39 -> 141); mine loses it (46 -> 39
   before recovering to 63).** This is the one that matters and it is a sign error
   in the material model. My graphite ramp darkens monotonically to the base, so
   the foot is the darkest part of the bar and the warm term is then painted onto
   near-black — which is why it reads as rust rather than as light. A surface lit
   from below gets BRIGHTER toward the light. The bounce cannot be a tint on top of
   a darkening ramp; the ramp itself has to turn around.

Both bloom footprints (below the rule, and lateral past its ends) already match
within a few points after r01/r02, which confirms the remaining gap is entirely
about the bars, not the porcelain.

## THE EDIT

- Turn the graphite ramp around near the foot: add a lit stop so the bar's own
  body brightens into the rule instead of darkening into it.
- Raise the bounce peak toward the measured +174 and spread its stops so the reach
  matches the measured ~165px rather than collapsing into the last 20%.
- Add the rule's own lip glow onto the bars' bottom edge, which is what produces
  the reference's L141 at t=0.94.

## WHAT MUST NOT MOVE (the coordinator's floor, checked every round)

| invariant | baseline to hold |
|---|---|
| named layers | 4 (bg / mid / fg / highlight) |
| figure-ground | 15.1:1 |
| self-contrast @32px | 0.706 |
| 16px legibility | gaps open, bar 2.06px, gap 1.22px |
| RULE_OVERHANG | 104px, unchanged |

Any of those going backwards means the material change went too far, and the round
is rejected regardless of what the composite says.

---

## RESULT — gate ACCEPT, +0.0150 net, and 256 finally above the r00 baseline

| size | r00 | r03 | **r04** |
|---|---|---|---|
| 1024 | 0.6449 | 0.6421 | **0.6471** |
| 256  | 0.7205 | 0.7196 | **0.7237** |
| 128  | 0.7167 | 0.7110 | 0.7100 |
| 32   | 0.9014 | 0.8960 | 0.8986 |
| 16   | 0.9129 | 0.9082 | 0.9125 |

256 is the size where material lives, and this is the first round to take it above
the r00 baseline rather than drifting below it. The three earlier rounds had moved
the halo's footprint and the rule's geometry; none had touched the emission.

## The three edits, in order of how much they bought

**1. The contact shadow was drawn ON TOP of the bloom, and it was cancelling it.**
This cost more of the emission than any gradient stop in the file, and it was a
draw-order bug wearing the costume of a material problem. Measured with and without
the ellipse, chroma on the porcelain at dy 40 below the rule read **67 vs 107**
against the reference's 146 — the shadow was eating 40 points of glow in exactly
the band where the glow is legible. A shadow over a light source is a contradiction
the eye reads instantly as "coloured object" rather than "emitter". Moved under the
bloom, narrowed and lightened. Free: it costs nothing anywhere.

**2. r01's halo measurement was contaminated, and the well was half the size it
should be.** r01 sampled the reference's ground at x=180 — but the reference's rule
spans 142..885, so that column sits ON the rule and was reading its falloff rather
than the porcelain's. Re-measured on genuine porcelain, C1 runs 190/146/76/36/10 at
dy 20/40/60/80/110 where the r03 master ran 170/67/37/21/9. BLOOM_RY 118 -> 150 with
the stops refitted brings it to 170/140/115/75/30. Also free.

**3. The graphite ramp had a sign error at the foot.** The reference's bar foot
*gains* luminance toward the rule (81 -> 105 -> 141 at t = 0.78/0.88/0.94); the old
master *lost* it (39 -> 47 -> 63). A surface lit from below gets brighter toward the
light, and a warm tint painted onto a ramp that darkens into its own light source
reads as rust rather than illumination. The ramp now turns around in its last 6%,
and the bounce stops are computed from the measured reference curve (`REF_BOUNCE`)
rather than hand-typed, so the gradient cannot drift from the measurement.

## THE TRADE THE LOOP COULD NOT DISSOLVE — reported, not buried

**Bar emission and small-size legibility are directly opposed, and there is no knee.**

`self_contrast` watches the render's p10 bin. That bin *is* the bar interiors —
bounding box x238..786, y297..700, measured, with no porcelain pixel in it. So
brightening the porcelain is free and brightening the bars is not, and the bounce is
the only term that reaches the bars.

Fitting the bounce to C1's measured +174 peak needs BOUNCE_PEAK ≈ 0.62. Swept
0.62 / 0.55 / 0.48 / 0.40 / 0.34 / 0.30 / 0.26 / 0.22:

| BOUNCE_PEAK | bar chroma @40px | sc 1024 | sc 64 |
|---|---|---|---|
| 0.62 | 113 | 0.663 | 0.608 |
| 0.48 |  84 | 0.686 | 0.694 |
| 0.34 |  57 | 0.706 | 0.698 |
| **0.26** | **39** | **0.733** | **0.737** |
| 0.22 |  31 | 0.737 | 0.741 |

The cost is near-linear in the gain — no threshold, no free region. 0.26 is the
largest value that holds every invariant. C1's bar chroma at 40px is 121; ours is
39, and closing that remaining gap would cost the 15.1:1 figure-ground and the 32px
legibility the coordinator named as the floor.

**Why this is a real finding rather than a tuning failure:** C1's own self-contrast
is **0.533** against our 0.737. The reference buys its vibrancy with figure-ground —
it is a flat pre-masked raster with no small-size obligations and no Dark/Clear/
Tinted variants to survive. We are holding a 12/12 rubric icon to a reference that
scores 8/12. Converging the last of the way is the documented trap: the rubric
outranks the gate, and the reference can itself fail checks the master passes.

**The honest options, if the remaining gap still matters:**

- **Accept it.** The emission now reads as a source: the ground blooms, the feet
  transmit, and the foot luminance lands at 145 against C1's 141. This is what
  shipped.
- **Spend figure-ground deliberately.** Lighten `GRAPHITE_LOW` toward the
  reference's own bar values. Buys the remaining vibrancy at 1024 and 256, costs
  the 32px read. A stated trade, not a free win.
- **Split further.** A third file for 256-and-above with the full 0.62 bounce.
  Buys everything at hero sizes and costs a third file that can drift — the
  two-file split is already a named liability.
- **Change the material.** The reference's bars are genuinely translucent, showing
  ground through them. That is a different construction (material-recipes' "(d)
  translucency is a construction, not an opacity"), not a gradient tweak, and it
  would be its own commission.
