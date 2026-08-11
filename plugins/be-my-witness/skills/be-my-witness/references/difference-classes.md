# Telling the difference classes apart

"The screenshot differs from the reference" is not a finding. Everything differs from
everything. The useful question is *what kind* of difference, because only two of the
five kinds mean the software is wrong, and reporting the other three as failures is
how a visual check earns its reputation for crying wolf.

The classes, and the discriminator for each. The discriminators are the hard part:
several classes look identical until you ask the right question.

## Framing

**What it is.** The two images are pictures of different amounts of the world — a
different crop, viewport, zoom or device pixel ratio.

**How to tell.** The pre-scan does most of it: compare aspect ratios and dimensions.
An aspect-ratio-of-ratios outside roughly 0.8–1.25 is framing, near-certainly.

But framing also hides inside *matching* aspect ratios. The tell is that **everything
scales together**: if every element is 1.3× larger and in the same relative place, the
difference is scale, not design. Check two distant landmarks and compare the ratio of
their separations; if it matches the ratio of the frame dimensions, it is framing.

**Verdict.** Never a failure. Re-crop to a common region and compare again. If you
cannot — the reference simply does not contain the region — record `not-comparable`
and say which region was missing from which side.

**Why this matters.** A structural score once reported four healthy surfaces as
"drifted" because a 440×275 card was compared against a 1440×900 viewport. Nothing
was wrong with any of them. Four false alarms is enough to teach a team to ignore the
tool.

## Data

**What it is.** Same layout, different content. Different names, counts, dates,
avatars, row totals, a list of seven where the mock drew three.

**How to tell.** The *shape* survives and the *fill* changes. Element boundaries land
in the same places; what sits inside them reads differently. A useful probe: describe
the region without reading any text. If both descriptions match, it is data.

**Verdict.** Not a failure — **unless the expected output named the value**. "The
total reads 38,000" is an expectation; "there are some rows" is not. Mocks are full
of placeholder data by construction, so a data difference against a mock is almost
never interesting.

**The trap.** A data difference can *cause* a layout difference: a longer string wraps
to two lines and everything below moves 20px. That is still data. Ask whether the
displacement is explained by the content change; if it is, do not promote it to
structure.

## Structure

**What it is.** A region moved, split, merged, disappeared, changed order, or changed
nesting.

**How to tell.** Enumerate the top-level regions in each image, in reading order, and
diff the lists. Structure differences show up as a changed sequence, a changed count,
or an element that crossed a boundary it used to sit inside.

**Verdict.** **This is the class that matters.** A missing control, a reordered
sequence, a section that lost its container — these are almost always real, and they
are what a visual check is for.

**The trap.** Responsive reflow is structure that is *supposed* to happen. Before
calling it a defect, confirm both images were captured at the same width. If they
were not, this is framing.

## Styling

**What it is.** Same structure, same data, different appearance: colour, weight,
size, spacing, radius, shadow, border.

**How to tell.** Everything is where it should be and reads differently. This class
needs the highest inspection scale — most styling findings are invisible below 2×,
and letter-spacing and weight need 3×.

**Verdict.** Against a **mock**, a finding at its severity — this is what mock
conformance means. Against a **test expectation**, only a failure if the expectation
named the property. A test that says "the button is present" is not violated by the
button being the wrong blue; a test that says "the danger button is red" is.

**The trap.** Anti-aliasing and font rendering differ across machines, renderers and
scale factors. A sub-pixel edge difference is not a styling finding. If the difference
is only visible at the boundary of glyphs or hairlines, it is rendering, not design.

## State

**What it is.** One image shows a loading, empty, error or partial state where the
other shows a populated one.

**How to tell.** The pre-scan flags the skeleton signature. Beyond that: uniform
placeholder blocks, spinner geometry, an empty-state illustration, or an error string.

**Verdict.** **A failure, and usually of the capture rather than the product.** A
screenshot of a skeleton is not evidence about the surface, and every finding derived
from it is void. Report it, discard any findings already drawn from that image, and
ask for a recapture.

**Why this is its own class.** It was folded into "data" on a real run, and the
consequence was a whole suite of scores computed against loading shimmer. Giving it a
name makes it something the protocol has to check for rather than something someone
might notice.

## The order to test in

Cheapest and most disqualifying first, because each one can make the later ones moot:

1. **State** — if it is a skeleton, nothing else you find is real.
2. **Framing** — if the frames are incomparable, every other difference is an artifact.
3. **Structure** — the class that matters; establish it before looking at appearance.
4. **Data** — separate content change from layout change.
5. **Styling** — last, at the highest scale, on what remains.

## When a difference belongs to two classes

Say so, and classify by the **most severe** reading, then explain the benign one. "The
totals row sits 20px lower (structure), which is fully explained by the longer segment
name above it wrapping to two lines (data)" is a complete finding and a reader can
decide. Picking one class silently and discarding the other is where a real defect
gets talked away.
