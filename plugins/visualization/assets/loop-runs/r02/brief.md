# r02 — the overhang

EDIT CLASS: geometry of the rule. One constant.

MEASURED off the reference at its own rule row (chroma > 25 for the rule, luminance
< 170 at rule_row - 120 for the bar group):

|          | rule span | bar group | overhang L / R |
|---|---|---|---|
| reference | 142..885 (743px, 72.6% of tile) | 240..775 (535px) | 98 / 110 |
| master r01| 190..833 (643px, 62.8%)         | 236..788 (552px) | 46 / 45 |

The bar groups are within 3% of each other. The datum is not: the reference runs
its rule more than twice as far past the outermost bar, and that is precisely the
concept's own argument — the baseline is wider than the data it carries, so it
reads as a datum the bars were measured against rather than a plinth cut to fit
them. r00/r01's 46px overhang reads as a base.

This is also the likeliest single cause of r01's global-similarity regression: the
composite compares whole frames, and the two icons disagreed about where the rule
ends by ~50px on each side.

EDIT: RULE_OVERHANG 46 -> 104, the reference's own mean. That puts the rule at
760px = 74.2% of the tile, above the 55-65% composition band — but the band governs
the focal object's mass, and a rule is not a blob: 52px tall, it occupies 3.8% of
the tile's area at that width. The reference, a corpus-steered take, sits at 72.6%
for the same reason.

RESULT: gate ACCEPT, net composite -0.0104 with no size regressing past tolerance —
r01's three regressions (128/32/16) all cleared. Composite at 128 went 0.7093 ->
0.7155, at 32 0.8950 -> 0.8998, at 16 0.9062 -> 0.9082.
