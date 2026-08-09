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

## What ships: the vector, with the ember inline

The composition changed late and it is the change that mattered most.

Every earlier take had the ember **detached**, floating outside the ring, which
says "a piece came out". Inline, occupying part of the hole, it says what the
tool actually reports: three quantities at once. Dark for used, ember for just
reclaimed, and the remaining hole for free. It is also the conventional gauge
idiom, so it reads without being learned.

Mechanically the inline segment abuts the ring with **butt caps**, matching the
ring's own, and carries only an edge catch rather than a drop shadow. An inline
element with a float shadow reads as sitting on top of the track instead of in
it. Round caps would overlap the dark arc and round off the join.

Proportions were swept: at 34 degrees the ember is too slight to be the focal
accent the brief reserves it for, and at 52 it crowds the free gap. 44 degrees of
ember in a 72 degree hole leaves 28 degrees reading clearly as empty.

### Why not the raster

Take C won the material judgment outright and briefly shipped: its one
disqualifying fault, a baked dark frame, turned out to be croppable (inner tile
x 78-948, y 66-953, aspect 0.981). Composition is what lost it. Its ember is a
solid triangle baked outside the ring, so it cannot express the inline read, and
being pixels it cannot be changed to. It stays as the material reference.

## The wedge was never misplaced

Reported three times as wrong placement of the red section, and the placement was
correct every time. Measured on the rendered pixels: the hole in the ring spanned
-80 to -31 degrees, the ember -80 to -30. Identical, 50 degrees each.

The first two fixes moved the wedge. Both were wrong. The actual fault was the
**track**: a visible pale band filling the gap makes the mark read as a two-tone
ring with an orange blob nearby, rather than a ring with a piece removed. The eye
needs the gap absent, not merely lighter. Removing the track fixed that read, and
the user then chose C's material over the vector anyway.

The generalisable lesson, which cost two rounds: when a measurement says an
element is correctly placed and it still looks wrong, stop adjusting that element
and look at what it sits against.

Kept in the vector master's constants either way: a 50 degree gap rather than 70,
since 70 is 19% of the ring empty where the reference machine was at 6% free; and
a wedge matching the gap's visible width, which needs allowing for round caps
extending the arc by (W/2)/R radians at each end, 21.2 degrees in total.

## Files

- `build_icon.py` emits `icon.svg`; geometry and material are named constants at
  the top, so a fidelity round is a parameter edit rather than path surgery.
- `icon.svg` is the shipped master, emitted by `build_icon.py`; `icon.png`
  (1024), `icon-256.png` and `icon-128.png` are rendered from it.
- `icon-engineC-clean.png` is the deframed raster, kept as the material
  reference and the target for any future fidelity round.
- `icon-engineB-arrow.svg` and `icon-engineC-raster.png` are the losing takes,
  kept because an audit that hides its losers is not an audit.
  `icon-engineC-masked.png` is C with the family superellipse applied.
- `audit.html` scores all three; `audit-renders/` holds its sources.
- `icon-src.svg` is the original flat hand-authored take that preceded this
  commission, kept for the before and after.

## Known liabilities

- The master is still less volumetric than C at 1024. Closing that needs a
  bounded fidelity run against a raster regenerated with the inline
  composition, since the current C is detached and would pull the master back.
- Check 10, variant robustness, is untested. The mark has not been rendered
  against Dark, Clear or Tinted grounds, and a warm porcelain ground is exactly
  the kind that can collapse under Tinted.
- A ring gauge is legible but conventional. That is where the one lost rubric
  point sits, and no amount of material fixes it.
