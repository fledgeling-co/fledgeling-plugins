# mac-doctor icon: construction notes

**Direction:** 8 Instrument Emblem, rendered in direction 2's Tahoe gel porcelain
sub-register. Runner-up was 7 Diagonal Tool, the conventional cleaner-app answer,
dropped because the subject is not a tool acting on files; it is a gauge that
refuses.

**Device and signature move:** a capacity ring 290 degrees closed, with one wedge
lifted out of the gap. The gap is the message. The mark shows the problem and the
fix in one shape, which is why the ring is the carrier and the wedge is the only
warm element in the icon.

No sibling uses a ring gauge: trawl is a net and funnel, armada-sync is stacked
bars, dossier-report and create-mac-icon have their own devices.

## Values, sampled rather than assumed

The skill's step 4 exists because a master built from prose descriptions of what
a macOS icon looks like gets its relationships wrong. Both numbers below changed
the design.

**Ground.** Sampled from armada-sync, dossier-report and create-mac-icon at 256:
`(253,253,252)` top, `(245,238,231)` mid, `(237,233,223)` bottom. The family's
porcelain is **warm**. Apple's own is cool: Safari runs `(254,255,255)` to
`(223,227,235)`. Family consistency wins, so the ground is `#FDFDFC → #EDE9DF`
and not the platform sample.

**Gel falloff.** Safari's dial top to bottom: `(112,184,239)` → `(57,113,241)`.
About a 40% luminance drop at constant hue. The object is a value ramp, tone on
tone, never a hue shift.

**Contact shadow.** Under Safari's dial the ground reads `(205,215,232)` against
a local ground of `(233,234,235)`: roughly 12% darker and tinted toward the
object's own hue, not a neutral grey. So the graphite ring casts cool
(`#2A2F38`) and the ember wedge casts warm (`#C0430F`).

## Wedge placement, and why the first two attempts failed

Reported twice as wrong placement, and both times it was. The measurement that
finally explained it: the ember spanned radius 289 to 389 while the track's
outer edge sits at 322, so the wedge was overlapping the gap by 33px. It was
sitting partly ON the hole rather than clear of it, which is why it read as
hovering rather than lifted out.

Two other things were wrong with the original 70 degree gap. It is 19% of the
ring empty, where the machine this was built for was at 6% free, so it was not
even truthful. And a hole that wide cannot be matched by a wedge of the same
visible width without the wedge dominating the mark.

| gap / wedge / lift | what it does |
|---|---|
| 70 / 34 / 104 | wedge half the width of the hole, far out; reads as an unrelated bean |
| 70 / 48 / 88 | overlaps the track by 33px; hovers over the gap |
| **50 / 48 / 118** | **shipped.** Same visible width as the gap, sits just clear of it |

Worth leaving for whoever edits these constants: round caps extend the arc by
(W/2)/R radians at each end, 21.2 degrees in total here, so the authored 48
degrees renders as about 69. The authored number is not the number you see, and
that is most of why the first attempt was misjudged.

## What the raster take changed

Engine C won the material read, as the skill predicts, and lost everything
structural: it baked its own dark rounded-square frame inside the tile, and it
turned the freed wedge into a solid triangle so the mark read as a play button
beside a ring.

Converging the master on it would have imported both faults, which is the
documented case for the rule that the rubric outranks the gate. Two things were
salvaged instead:

1. **Concentric edge catches.** Round one authored the ring's rim light as a
   displaced copy of the arc, translated up. That produces no visible edge at
   all. A ring lit from above catches light along its *outer top curve* and
   bounces a weaker line along the *inner curve*, so the fix is two concentric
   strokes at `R ± W/2`, each with a gradient that fades as the curve turns away
   from the light. This is the single change that moved the master from flat to
   modelled.
2. **A bluer graphite body.** C's ring sampled `(60,81,110)` against the
   master's `(75,85,99)`. Part of why C looked richer was simply that it was
   cooler. `RING_HI` moved from `#5A6274` to `#5C6880`.

## Files

- `build_icon.py` emits `icon.svg`; geometry and material are named constants at
  the top, so a fidelity round is a parameter edit rather than path surgery.
- `icon.svg` is the shipped master. `icon.png` (1024), `icon-256.png`,
  `icon-128.png` are rendered from it with `rsvg-convert`.
- `icon-engineB-arrow.svg` and `icon-engineC-raster.png` are the losing takes,
  kept because an audit that hides its losers is not an audit.
  `icon-engineC-masked.png` is C with the family superellipse applied.
- `audit.html` scores all three; `audit-renders/` holds its sources.
- `icon-src.svg` is the original flat hand-authored take that preceded this
  commission, kept for the before and after.

## Known liabilities

- The master is still less volumetric at 1024 than take C. Closing that properly
  needs a bounded fidelity run against a raster whose composition is corrected
  first, because the current C would drag in its baked frame.
- Check 10, variant robustness, is untested. The mark has not been rendered
  against Dark, Clear or Tinted grounds, and a warm porcelain ground is exactly
  the kind that can collapse under Tinted.
- A ring gauge is legible but conventional. That is where the one lost rubric
  point sits, and no amount of material fixes it.
