# Chart honesty — the rules that make an encoding a true claim

A diagram that misleads is usually unclear. A chart that misleads is usually
*precise* — the geometry states a quantity, and the reader believes it. These are
the rules that keep the drawn thing and the claimed thing the same.

Several of them are executable. Where a script is named, run it and read its
exit code; where none exists, the rule is yours to hold.

## The baseline rules

**Length-encoded magnitude starts at zero.** Bars, columns and areas encode value
as length or area, and the reader judges the ratio between them. Truncating the
axis inflates that ratio without saying so — a 68→74 change on a 65–75 axis draws
as a sixfold difference. If the differences genuinely matter and are small, the
answer is a different form (line, slopegraph, dot plot) whose encoding is
position rather than length, not a zoomed bar.

Position-encoded forms (line, scatter, dumbbell, slopegraph) may use a non-zero
domain, and the domain then follows the data's range rather than its observed
extremes. Taking `min` and `max` as the bounds *is* the truncation.

**Never a dual axis.** Two y-scales on one plot invent a correlation: the
alignment of the two scales is arbitrary, so the crossing point is a drawing
decision, not a fact. Two charts, small multiples, or both series indexed to a
common base (=100 at t₀) on one axis.

**One shared scale per axis, and say what it is.** Every mark on an axis is
measured against the same domain, and both ends of a paired mark carry their real
value. `verify-slopegraph.py`, `verify-dumbbell.py`, `verify-beeswarm.py`,
`verify-bubble.py`, `verify-bump.py` and `verify-ridgeline.py` each assert that
the drawn geometry matches the values the file declares.

**Area encodes by area, not by radius.** Doubling a bubble's radius quadruples
its area and overstates the value fourfold. `verify-bubble.py` and
`verify-treemap.py` check this against the declared sizes.

**Flow is conserved.** In a Sankey, what enters a node leaves it; ribbon width is
the quantity, and stages carry equal totals. `verify-sankey.py` asserts it.

**Don't smooth sampled data.** A spline through sampled points draws values that
were never measured. Polyline is the honest mark.

**Don't connect across a discontinuity.** A gap in the data is drawn as a gap. A
line through a missing month asserts a value for that month.

**The connector in a paired mark is a gap, not a trajectory.** A dumbbell's line
encodes the distance between two values and says nothing about the path between
them — no rate, no monotonicity. Do not narrate it as movement.

## Missing and incomplete data

A missing value is disclosed, never imputed and never silently dropped. Dropping
incomplete rows without saying so changes the population being compared, and a
single drawn endpoint is indistinguishable from two coincident ones — that is,
from a genuine zero difference. Draw the known end and name the missing value, or
drop the row *and* record which rows went and why.

## Stating the order

When rows are sorted, say by what: one endpoint, signed change, absolute change,
or an order the subject supplies (chronological, geographic, ordinal). "By gap"
alone is ambiguous. An unstated order reads as arbitrary and invites the reader
to infer one that isn't there.

## Precision the data doesn't have

Don't print more significant figures than the measurement carries, don't render a
projection in the same weight as an observation, and don't let a smooth
interpolation imply sampling that didn't happen. Where a value is an estimate,
the chart says so on the chart, not in a caption somebody may not read.

## Colour must not carry the claim alone

Every quantitative claim survives greyscale. Identity comes from a legend and
selective direct labels as well as hue; status comes with an icon and a label;
polarity comes from position against a baseline as well as from two hues. The
palette gate (`references/series-palette.md`) enforces the perceptual half of
this; the redundancy is a design decision the gate cannot make for you.

## When the request asks for a misleading chart

Say what the construction would do to the reader, offer the form that answers the
same question honestly, and draw that. If the user reaffirms the original
request, that is their call — draw it, and annotate the distortion on the chart
itself (a marked axis break, a stated domain) so the artifact carries the caveat
rather than the conversation.
