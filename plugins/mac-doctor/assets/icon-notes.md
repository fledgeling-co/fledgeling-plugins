# mac-doctor icon: construction notes

**Direction:** 8 Instrument Emblem, rendered in direction 2's Tahoe gel porcelain
sub-register. Runner-up was 7 Diagonal Tool, the conventional cleaner-app answer,
dropped because the subject is not a tool acting on files; it is a gauge that
refuses.

**Device and signature move:** a capacity ring 280 degrees closed, with one
reclaimed segment sitting inline in the same band. The gap is the message. The
mark shows the problem and the fix in one shape, which is why the ring is the
carrier and the segment is the only warm element in the icon.

No sibling uses a ring gauge: trawl is a net and funnel, armada-sync is stacked
bars, dossier-report and create-mac-icon have their own devices.

## Round 7 — three preferences taken off take C

Round 6 shipped an 11/12 master. Shown beside take C the user named three
things C still did better: "the brighter red, less gaps and the uneven wedge
that protrudes slightly from the circle." Each was swept and measured rather
than adjusted, and the round is `fidelity/runs/r03/`.

### 1 — the brighter red

The ember was orange; C's is scarlet. Sampled over the full 1024 renders on
one mask applied identically to both:

| | mean RGB | p10 | p50 | p90 | darkest | L spread |
|---|---|---|---|---|---|---|
| round 6 | (225,124,70) | (203,87,32) | (224,108,48) | (248,172,121) | (186,76,30) s0.84 | 0.376 |
| **round 7** | **(236,102,64)** | **(224,63,24)** | **(236,85,42)** | **(251,161,123)** | **(213,55,25) s0.88** | **0.407** |
| take C | (235,110,77) | (204,63,28) | (244,88,49) | (253,145,116) | (227,21,1) s1.00 | 0.424 |

What the numbers said before anything was authored: C's ember is a
near-constant hue, 10.5° at its core p10 and 14.6° at its p90, where the old
ramp ran 18–26° and read as the family accent (#C4622D, hue 21) rather than as
C's vermilion. C is also brighter through the midtones. So the edit is the old
ramp rotated onto a 9°→14° tilt (dark end reddest, lit end warmest, matching
C's direction), value-remapped into 0.82–1.00 and saturated 5% more. The
specular is untouched; it already matched C's brightest ember pixel.

**Two sweeps were discarded for measuring the wrong thing, and both are worth
recording.** A *multiplicative* value gain scored best of anything tried — and
was unusable: at gain 1.14 three of the five face stops clipped at V=1.0, so
the section's shoulder, its minimum and its outer stop all became one colour.
The whole-image spread still *rose*, because the specular and the bevel wall
own that number, so the metric paid handsomely for destroying the
cross-section. An affine remap into [v_lo, v_hi] keeps the ramp monotone by
construction. Separately, an error term over R and G alone — the two channels
the gap was in — bought its score by driving blue to zero; C's median ember
carries B=49 at saturation 0.80. The kept error is over all three channels.

### 2 — less gap

An 80° hole with a 40° ember leaves 20° clear a side. Swept 30–34 GAP_HALF,
i.e. 10–14° clear, at 1024/32/16. The deciding measurement is at 32px, taken
along the band's centreline through each side of the hole:

| clear per side | 32px peak L, ccw side | 32px peak L, cw side |
|---|---|---|
| 10° | 0.912 | 0.856 |
| 12° | 0.912 | 0.856 |
| **13°** | **0.916** | **0.871** |
| 14° | 0.916 | 0.918 |
| 20° (round 6) | 0.942 | 0.925 |

Ground is 0.941. The clockwise side is the tight one, and below 13° it stops
reaching ground at 32px — the ember starts to fuse with the arc it must stay
clear of. 13° chosen: a 34% cut in the visible gap that still keeps clearance
on both sides, which is the hard constraint. Abutting the used arc makes the
segment read as continuous with what is occupied, which was rejected earlier.

At 16px the picture is different and worth stating: the clearance was already
sub-pixel at 20° a side. It now reads L 0.79 and 0.89 against a ground of 0.94,
where round 6 read 0.95 and 0.92. The break is still much lighter than the
object and still present — softer, not gone.

### 3 — the wedge protrudes

C's does, and by far more than "slightly": fitting circles to C's ring gives
R_out 376 and R_in 227, and its wedge runs to r=448 — **48% of the band width
proud**, and starting 11px *outside* the ring's inner radius rather than on it.
That is not a segment of the band; it is a separate triangle laid over one,
which is precisely the composition this mark rejects. So the protrusion was
swept 0–13% and read by eye at 256: 10% is unmistakably proud while the segment
still belongs to the band. Measured on the shipped render, the graphite arc
ends at r=331 and the ember at r=345.

**The inner boundary did not move, and could not have.** `band()` now takes a
`grow` parameter that adds to the outer radius only; `R_IN` is not a function
of it. Every derived quantity — bevel angle, shoulder radii, stroke widths, the
cast shadow — is computed from `grow` inside the same generator rather than
restated, so there is still exactly one code path and the flush inner arc is a
property of the file rather than of a matched pair of edits. Verified on the
1024 render: inner radius **189.0–190.2** at every angle sampled through both
segments.

One measurement trap found on the way, because it looks exactly like the fault
this file exists to prevent: a boundary detector using `R > B + 40` counts the
ember's *spill on the porcelain* as object, and duly reported the ember's inner
radius 23px inside the arc's. The spill is a ground effect, not the object.
`R > B + 90` separates them.

### The small-size liability, closed

Round 6 left this open: both blind judges preferred the flat predecessor at 32
and 16px, and the named fix was to floor the specular below about 64px. It does
persist, and a radial profile through the key side says exactly what the judges
were seeing — at 32px the specular lifts the stroke's outer third to L **0.53**
against a body of **0.23**, so the lit edge dissolves toward the porcelain and
the ring reads thin and doubled.

`build(spec_scale=)` multiplies the specular's peak opacity and nothing else.
`icon-small.svg` is the master at 0.30, and `icon-64/32/16.png` render from it;
1024, 256 and 128 still come from the untouched master. At 0.30 the 32px lift
falls to +0.18 and self-contrast *rises*:

| | 16px | 32px | 64px |
|---|---|---|---|
| flat original | 0.590 | 0.673 | 0.702 |
| round 6 | 0.698 | 0.733 | 0.761 |
| **round 7 (floored)** | **0.724** | **0.741** | **0.765** |

What the three changes do at those sizes, separately: the redder ember *helps*
(both judges named the accent's chroma as the reason it wins at small size);
the tighter gap costs a little at 16px and nothing at 32; the protrusion is
0.44px at 32px and therefore neither helps nor hurts — it is a large-size
feature.

### What the instruments said

Gate ACCEPT against round 6, and the first round in this fixture to improve
every size at once. `edge_f1` rose at all five sizes, SSIM rose at 32 and 16 —
the sizes the complaint was about — and figure-ground moved 3.04:1 to 3.02:1,
still clear of the rubric-7 bar. Ring luminance spread went 0.436 to 0.450
against C's 0.439.

The blind panel ran two families (Claude Opus, grok-4.5 via cursor-agent),
seeing renders only. Both voted the new take the winner on overall, material
and **small size**, with silhouette a tie — reversing round 6's small-size
verdict. gpt-5.6-sol again did not run, for a missing API key; recorded in
`fidelity/runs/r03/panel/verdict-openai.json` rather than dropped. The honest
limit on that small-size win: the panel renders its strips from the master, so
it judged the un-floored specular. The rasters that ship at 64px and below are
the floored ones, which measure better than what the panel saw.

## Round 6 — the fidelity round, and what it changed

Five rounds of hand-adjustment had failed to land two faults. Both are closed,
and in each case the thing that was actually wrong was not the thing being
adjusted.

### Fault 1 — the ember did not sit cleanly in the band

Every measurement said the geometry was right, and every measurement was
correct: the segment and the arc shared an inner radius of 190 and an outer of
332 at every angle, on the rendered pixels. What broke the read was that the
**ring carried an inner edge-catch stroke and the segment did not**. The band's
inner boundary was therefore a lit arc for 280 degrees and an unlit one for 40,
and the eye reads that as a broken circle regardless of where the radii sit.

Moving the segment could never fix it, which is why five rounds of moving the
segment did not.

The fix is structural rather than cosmetic. `band()` in `build_icon.py` emits
the entire material stack — glass hairline, bevel wall, inset face, key
modelling, vertical shade, specular shoulder, ground bounce, and both cut-end
faces — for any arc, and it is called exactly twice: once for graphite, once for
the ember. Every boundary, shoulder and bevel radius is shared by construction
and cannot drift apart in a later edit. Verified on the 1024 render: the object
begins at r=192 and ends at r=334 at every angle sampled, through arc and
segment alike, and the inner-shoulder bounce is present in both (slate at 180
degrees, ember-hued at −55).

**The generalisable lesson**, and the second time this commission has taught a
version of it: when two parts of one object must read as one object, share the
generator, not the numbers. Matching constants by hand is a fact about one
moment; a shared function is a fact about the file.

### Fault 2 — the material was flat beside the raster

Take C is a gel torus; the master was one stroke with one linear ramp. Rebuilt
against numbers sampled off C rather than against a description of it.

**The ring body.** C runs from a darkest pixel of `(18,49,75)` at L 0.174 to a
near-white specular at `(246,252,255)`, a p5–p95 luminance spread of **0.439**.
The old master ran `#5C6880` to `#252B36`: a spread of **0.228** with no
specular at all. That single number is most of what "the raster looks richer"
meant. The rebuild measures **0.436**.

**The cross-section.** Sampled across the band at seven bearings, C's section is
a shallow radial ramp with its minimum near the band centre — and the drama is
**angular**, not radial: facing the key the profile climbs 0.28 → 0.84, level
with the centre it is flat at 0.28–0.30, and away from the key it falls to 0.20
with no outer lift at all. So the section is a `radialGradient` in user space and
the specular is a separate stroke faded along the key axis, rather than one
gradient trying to be both.

**The construction.** Every terminus in C is a bevelled puck: a dark moulded
wall around a paler inset cross-section face, the face lifting to L 0.36–0.53
against a body at 0.255, with a white hairline against the ground. That is two
concentric strokes on the same arc — the shell at full width, then the face at
`W − 2·BEVEL` — with the face arc shortened by `degrees(BEVEL/R)` at each end so
the **cut ends** are bevelled too, which a stroke cap cannot do for you. The
same grammar is in the corpus: apple-08's concentric ridges carry the identical
lit-shoulder / dark-terminator / bounced-inner-edge stack.

**The shadow hue.** C's darkest ring pixel measures saturation 0.76; the first
rebuild's measured 0.50 at the same luminance, so a range check and a mean
check both passed it while the shadow had quietly gone neutral. Re-hueing the
dark end to a deep blue took it to 0.75. The ember's dark end got the same
treatment: C's is `(227,21,1)` at saturation 0.996, where the old master's was
`#D8410F` — L 0.36 and visibly desaturated. A gel shadow that desaturates reads
opaque.

### Three construction traps, each of which cost a build

**A bevel wall must ramp colour, not opacity.** Authoring it as an opacity ramp
along the key axis dissolved the wall to nothing on the unlit side and washed the
whole mark out. A wall is opaque everywhere; only its colour changes with the
light.

**Light the shell, not the face.** Modelling only the inset face left the bevel
wall unlit, which reads as an inked outline drawn round the shape.

**`objectBoundingBox` gradient units are wrong for a multi-part object.** They
rescale the axis to each shape, so the 40-degree segment got its own private
light direction while the 280-degree arc got another — a rubric-5 break on a mark
whose entire point is that the two are one physical band. Every angular gradient
is now `userSpaceOnUse` on one shared axis.

### The key direction is measurable, not a default

The 45-degree diagonal put the ember at t=0.41 along the key axis, which is the
neutral point, and it came out muddy while the ring around it was lit. Reading C
instead — specular along the **top**, darkest body at the **bottom**, left and
right flanks equal at centre height — gives a near-vertical key tilted about 16
degrees left. That lights both parts as one object.

## What the loop said, and why the master ships anyway

Full run in `fidelity/`, kept as trajectory data.

| round | 1024 | 256 | 128 | 32 | 16 | mean | gate |
|---|---|---|---|---|---|---|---|
| r00 baseline | 0.4389 | 0.3530 | 0.3544 | 0.7763 | 0.8145 | 0.5474 | — |
| r01 material | 0.4302 | 0.3735 | 0.3915 | 0.7900 | 0.8265 | 0.5623 | REJECT |
| r02 detail | 0.4298 | 0.3730 | 0.3906 | 0.7901 | 0.8266 | 0.5620 | ACCEPT vs r01 |
| r03 round 7 | 0.4412 | 0.3866 | 0.4046 | 0.8037 | 0.8330 | 0.5738 | ACCEPT vs r02 |

The gate rejected r01 on one term. At 1024 `lum_delta` improved 0.1472 → 0.1428,
`edge_f1` improved, `self_contrast` improved, and only **SSIM** fell, 0.733 →
0.695 — the documented mechanism, since surface structure the reference carries
at different coordinates raises local variance without raising covariance. Net
composite across five sizes was **+0.0730**.

A blind panel then judged the rebuild against the previous master with C as the
reference. Two independent families ran (Claude Opus, grok-4.5 via cursor-agent);
both, seeing only renders and not knowing which was which, voted the rebuild the
winner on **overall** and on **material**, unanimously. Gate below panel is the
documented ordering, so it ships. The third family (gpt-5.6-sol) never ran, for
a missing API key — recorded, not dropped.

Both judges also preferred the *previous* master at 32 and 16px. That is worth
recording as a disagreement rather than resolving by assertion: the measured
numbers go the other way, with self-contrast 0.684 against 0.657 at 32px and
edge F1 0.928 against 0.910. Looking at the renders, what they are describing is
real but small — the specular lays a light streak inside the stroke at 32px.
Round 7 measured that streak, found the judges right, and floored it; see "The
small-size liability, closed" above.

## Where the rubric overruled the reference

Take C's own figure-ground measures **2.50:1**, below the rubric-7 bar of 3:1.
Converging the master onto C took it from 2.98:1 to 2.45:1 — a round that did its
stated job and failed the icon. r02 deepened the whole graphite ramp by about
0.06 L, which cost 0.0003 of mean composite and put figure-ground at **3.04:1**,
clearing the bar outright while holding the spread at 0.436 against C's 0.439.
The rubric outranks the gate, and this is what that costs when it bites.

## Variant robustness, now tested rather than assumed

Previously listed as an open liability. Re-run for round 7 because the ember's
hue moved and the claim could not be inherited
(`fidelity/runs/r03/variant-check.png`): rendered at 256 against Default, Dark
chrome, a monochrome Tinted recolour and grayscale, identity survives all four,
because it is carried by shape and value — dark arc, mid segment, empty hole —
with the accent doing the last 10%. Measured medians: ring 0.244, ember 0.450,
ground 0.927 by default; 0.245 / 0.350 / 0.594 under Tinted; 0.243 / 0.494 /
0.929 in grayscale. The ring-to-ember value gap narrows to 0.105 under Tinted,
which is the tightest of the four and still separates. Check 10 passes.

## Values, sampled rather than assumed

**Ground.** From armada-sync, dossier-report and create-mac-icon at 256:
`(253,253,252)` top, `(245,238,231)` mid, `(237,233,223)` bottom. The family's
porcelain is **warm**. Apple's own is cool: Safari runs `(254,255,255)` to
`(223,227,235)`. Family consistency wins, so the ground is `#FDFDFC → #EDE9DF`.

**Gel falloff.** Safari's dial top to bottom: `(112,184,239)` → `(57,113,241)`.
About a 40% luminance drop at constant hue. The object is a value ramp, tone on
tone, never a hue shift.

**Contact shadow.** Under Safari's dial the ground reads `(205,215,232)` against
a local ground of `(233,234,235)`: roughly 12% darker and tinted toward the
object's own hue. So the graphite arc casts cool and the ember casts warm — at
identical offset and blur, in one shadow group, so a warm segment and a cool arc
still sit on the same table.

**The accent** was kin to the family's `#C4622D`, hue 21 degrees, until round 7
moved it onto take C's own hue: a 9°→14° tilt, dark end reddest. That is a
deliberate departure from family kinship, made because the user compared the
two icons side by side and preferred C's red by name. The specular `#FFE0C4`
still matches C's brightest ember pixel `(254,226,193)` almost exactly.
Vibrancy is emission, not saturation, so the segment also spills a low-opacity
warm glow onto the porcelain it sits on — retuned to the new hue with it.

## The wedge was never misplaced

Reported three times as wrong placement of the red section, and the placement was
correct every time. Measured on the rendered pixels at round 6: the hole spanned
−95 to −15 degrees and the segment −75 to −35, centred, with 20 degrees clear
each side. Round 7 narrowed the hole to −88…−22 on a user preference, not on a
fault: 13 degrees clear each side, still centred, still clear on both.

The first two fixes moved the segment. Both were wrong. The third fault was the
**track**: a visible pale band filling the gap made the mark read as a two-tone
ring with an orange blob nearby rather than a ring with a piece removed. The eye
needs the gap absent, not merely lighter. The fourth and fifth were the missing
inner edge catch, fixed above.

The lesson, now bought three times: when a measurement says an element is
correctly placed and it still looks wrong, stop adjusting that element and look
at what it sits against.

## Why not the raster

Take C won the material judgment outright and briefly shipped; its one
disqualifying fault, a baked dark frame, turned out to be croppable (inner tile
x 78–948, y 66–953, aspect 0.981). Composition is what lost it. Its ember is a
solid triangle baked outside the ring, so it cannot express the inline read, and
being pixels it cannot be changed to. It stays as the material reference — which
this round finally used as one.

## Files

- `build_icon.py` emits `icon.svg`; geometry and material are named constants at
  the top, and the material stack is one `band()` function, so a fidelity round
  is a parameter edit rather than path surgery. It also emits `icon-small.svg`,
  the same build with `spec_scale=SPEC_SMALL`.
- `icon.svg` is the shipped master. `icon.png` (1024), `icon-256.png` and
  `icon-128.png` render from it; `icon-64.png`, `icon-32.png` and `icon-16.png`
  render from `icon-small.svg`, whose only difference is the floored specular.
- `render_audit.py` renders `audit-renders/` — every take at 256/128/96/64/32,
  displayed at 128/64/48/32/16. Take A's 64 and 32 sources come from
  `icon-small.svg` so the sheet shows the rasters that actually ship.
- `icon-engineC-clean.png` is the deframed raster, the material reference and
  the fidelity target.
- `icon-engineB-arrow.svg` and `icon-engineC-raster.png` are the losing takes,
  kept because an audit that hides its losers is not an audit.
- `audit.html` scores six rows — the shipped master, the round-6 master it
  replaced, the flat original, and the three losing takes; `audit-renders/`
  holds its sources.
- `fidelity/` is the run directory — per-round scores, residual and edge maps,
  the blind panels' per-judge verdicts, the variant check, the round-7 gap,
  protrusion and ember sweeps with their renders, and the samplers used for
  every material number quoted here. Kept as trajectory data.
- `icon-src.svg` is the original flat hand-authored take that preceded this
  commission, kept for the before and after.
- `banner-src.html` composes `banner.png` at 3200×1040 from `icon.png`.

## Known liabilities

- **The 16px clearance is softer than it was.** The tighter hole costs there:
  the clearance pixels read L 0.79 and 0.89 against a ground of 0.94, where at
  20° a side they read 0.95 and 0.92. At 32px both gaps still reach full ground.
  This is a chosen trade, not a defect — the user asked for the tighter hole and
  13° is the tightest setting that keeps both-side clearance at 32px.
- **The ember's dark end is still shallower than C's.** (213,55,25) at
  saturation 0.88 against C's (227,21,1) at 1.00. It is the one place the ramp
  did not fully close, and a gel shadow that desaturates reads opaque.
- **The accent has left the family hue.** It was `#C4622D` kin at 21 degrees and
  is now on take C's 9–14. That was the ask, but the next sibling icon should
  know the family accent and this one no longer agree.
- **The panel is two families, not three.** gpt-5.6-sol has now failed to run in
  two consecutive rounds for the same missing API key.
- **A ring gauge is conventional.** That is where the one lost rubric point sits,
  and no amount of material fixes it.
- **The rebuild is 23KB and 24 paths against the old 13KB and 7.** Still far
  inside the loop's complexity envelope, but the master is no longer something
  you would edit by hand — which is the point of the build script, and a
  dependency on it.
