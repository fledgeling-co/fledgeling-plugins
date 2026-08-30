# r03 — the edge catch

EDIT CLASS: the bars' cross-section shading. One gradient's stops.

MEASURED across the tall bar at y=420, sampled at eleven fractions of its own width:

| | 0.01 | 0.08 | 0.25 | 0.50 | 0.75 | 0.92 | 0.99 | spread |
|---|---|---|---|---|---|---|---|---|
| reference | 128 | 108 | 91 | 94 | 92 | 100 | 135 | 44 |
| master r02|  42 |  49 | 59 | 60 | 56 |  51 |  49 | 18 |

The two profiles are inverted. The reference is BRIGHT at both edges and darkest in
the middle — a translucent body catching light on its turned edges, which is the
gel read. The master is dark at both edges and brightest in the middle, because
`round` was authored as a roundness fall: a solid opaque cylinder.

This is exactly the class of failure material-recipes warns about — three attempts
on a previous commission assumed "highlight is lighter than its surroundings" and
all three failed, because the property was never measured on the reference first.
Here the assumed relationship was the opposite one and it was equally wrong.

The reference's spread is 44 against the master's 18, so the master is also flatter
across the width than the reference by a factor of 2.4.

EDIT: invert `round` into an edge catch — bright narrow catches at both vertical
edges, the shaded edge cooler and narrower than the lit one, a slightly darker
core. Keep the amplitude below the reference's, because the reference's bars run
~40 luminance lighter overall and converging on THAT is the documented way to lose
16px contrast; the catch is the material, the overall value is not.

## RESULT — the gate rejected the edit on the whole-file candidate, and it was right

`gate` REJECT: 32px self_contrast 0.535 against a 0.598 baseline, past the 6% floor.
Net composite was +0.0111, so the similarity score liked it — which is the exact
case self_contrast exists for.

The first three attempts to save it by tuning amplitude (0.40 / 0.30 / 0.24 / 0.20)
and catch width (2.2% / 3.5% / 5.5%) all returned **identically** sc32 = 0.535.
That is not a tuning curve; it is a structural result, and it says the amplitude
was never the variable. Reading the 32px render's histogram directly: the catch
lifts the 10th percentile from 0.392 to 0.476 while leaving the darkest pixels
alone (0.153 -> 0.149) and the count below 0.35 unchanged at 97. The catch is not
brightening dark pixels — it is *deleting* the mid-dark ones. At 32px a 132px bar
is 4.1 pixels wide, and two lit edges plus a darker core is three values in four
pixels after antialiasing has spent two on the silhouette.

RESOLUTION: keep the catch where there is resolution for it, floor it where there
is not — `icon-small.svg`, same geometry, the plain roundness fall. The crossover
is measured rather than assumed:

| size | master (catch) | floor | floor gains |
|---|---|---|---|
| 48 | 0.7216 | 0.7059 | −0.016 |
| 40 | 0.5737 | 0.5890 | +0.015 |
| 32 | 0.5216 | 0.6000 | **+0.078** |
| 24 | 0.5137 | 0.5471 | +0.033 |
| 16 | 0.6451 | 0.6118 | −0.033 |

SMALL_BELOW = 48. 16px recovers on its own because a bar is 2 pixels by then and
the catch has averaged away entirely; 32 is the size with just enough room to be
hurt.

Shipped set: 1024 / 256 / 128 from `icon.svg`, 16 from `icon-small.svg`.
