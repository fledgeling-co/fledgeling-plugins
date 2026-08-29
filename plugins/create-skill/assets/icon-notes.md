# create-skill icon - spec, decisions and audit notes

Direction **"The Pour"**. Built with the `create-mac-icon:create-mac-icon` skill, dogfooded:
its `icon-directions.md` pipeline (three engines, written audit sheet),
`material-recipes.md` for the constructions, `assets/squircle-path.txt` for
the mask, and `scripts/fidelity.py` for the measured loop.

---

## The spec

**Concept (user-approved, not redesigned).** A porcelain casting flask with
molten vermilion being poured into it, the finished form implied beneath. The
signature move is that the pour is caught **mid-air**: a skill is the moment
an intention becomes an object, which is what create-skill does. Its sibling
`improve-skill` sharpens something that exists; this one makes something that
does not.

**Direction.** Tahoe gel-glass, sub-register (a) - porcelain cushion tile
carrying a coloured gel object. Runner-up was Direction 1, Object Tile, and it
was declined: the subject is not a noun sitting still, it is a transition
happening, and Object Tile has no grammar for a moment.

**Device.** Bank #16 (the icon performs the verb) crossed with #18 (edge-bleed
physicality - the stream is cut by the top of the mask, so the tile is a window
on a bigger bench rather than a print) and #22 (emissive interior under glass, where
the melt is the sanctioned second light source and lights its own walls).

**Silhouette.** A stream falling into a squat vessel. Rendered filled black it
is nameable at 160px and still at 32px (`build_icon.py` emits the geometry, so
the test is on the designed shape, not on a luminance threshold).

**Ground register.** Porcelain / daylight, matching the marketplace default.
The dark register belongs to the sibling `trawl` and is not used here.

**Palette.** Two hue families, no more.

| Role | Hexes |
|---|---|
| Cushion ground | `#FFFDF8` → `#F6EFE1` → `#DDD0B7`, vignette `#8A7A62` |
| Porcelain, lit flank | `#FDF7E9` → `#F0E5D0` → `#D2C0A4` |
| Porcelain, shaded flank | `#D8CDB8` → `#A99B80` → `#7C6B54` |
| Melt (the one accent, kin to `#C4622D`) | `#FC8014` → `#EE3E03` → `#D22103` → `#BC1302` → `#6E0901` |
| Interior glow (melt on its own walls) | `#FF4A08` |
| Exterior spill (melt past the rim, onto porcelain) | `#FF9C60` |

**Light model.** One soft key up and to the left, plus the melt as an emissive
second source. The melt lights; it never casts.

**Layer plan (#10).** `#bg` cushion + vignette + the ground spill · `#mid`
flask body, rim annulus, cavity wall, pool, shadows, parting lines · `#fg` the
pour and the detached droplet · `#highlight` rim lights, the stream's two
flanks, the droplet specular, the cushion's inner rim. Maps 1:1 onto Icon
Composer.

**Geometry.** One dimetric ground plane with a single foreshortening constant
(`KY = 0.515`). Every horizontal surface - the mouth, the rim annulus, the
cavity, the pool - is the same disc at a different height, so they cannot drift
out of register. The pour is a **swept ribbon** (a centreline with a width
profile and a real hemispherical cap), never an outline: an outline reads as a
flat noodle, and the leading drop has to be part of the same body as the stream
or it looks stuck on.

---

## Distinguishing it from the siblings

`create-mac-icon` is the adjacent one and the distinction had to be
unmistakable. Theirs is a **finished tile leaving a mould** - solid, departing,
and built from the set's own superellipse at two removes. Mine is **liquid
entering one** - nothing has set, nothing is leaving, and the vessel is a
**round** two-part casting flask rather than a superellipse, so the two icons
do not share a single silhouette. Every other sibling device was checked at
render: trawl (deep-sea trawler, dark register), create-swe-project (hull at
first water), ship-armada (three hulls in echelon), improve-skill (plane iron
and shaving), design-review (window stack and reticle), armada-sync (list rows
with one lit), compaction-quality (banded disc).

---

## Per-take scores

Full contact sheet with real renders at 128/32/16 plus the ×6 squint: `audit.html`.

| Take | Engine | Score | One line |
|---|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG, `build_icon.py` | **11 / 12 - ships** | Passes all four non-negotiables; loses #7 because the flask's *lit* flank is 1.20:1 against the tile beside it (the reference has the same trade at 1.16:1) |
| B `icon-engineB-arrow-d2f7ef.svg` | Arrow 1.1 vector | 6 / 12 | Hard-fails #1 (baked corner radius and drop shadow) and #6 (a dusty mauve field is a third hue family) |
| C1 `icon-engineC-4a73ea.png` | GPT Image 2, 3 corpus refs | 9 / 12 | Fails #10 as any flat raster does; group sits low with a thin stream. Source of the two-part keyed flask |
| C2 `icon-engineC2-6c0a72.png` | GPT Image 2, 2 corpus refs | 10 / 12 | Wins the material read; fails #10. **The loop's reference** |

Measured figure-ground on the shipped 1024 render: melt vs tile **4.65:1**,
stream vs tile **4.49:1**, flask shaded flank vs tile **3.21:1**, flask lit
flank vs tile **1.20:1**.

---

## The fidelity loop

`fidelity.py` (numpy tier: luminance field + SSIM + edge F1 + mask IoU), take A
against take C2, round sources kept at `fidelity-runs/rNN.icon.svg`.

| Round | Edit class | 1024 | mean | Gate |
|---|---|---|---|---|
| r00 | baseline | 0.4268 | 0.5434 | - |
| r01 | material: contrast budget, deepen the dark end | 0.4525 | 0.5619 | ACCEPT +0.0924 |
| r02 | material: the melt's dark end | 0.4516 | 0.5604 | ACCEPT −0.0075 |
| r03 | composition: open the mid-air cascade | 0.4527 | 0.5602 | ACCEPT −0.0010 |
| r04 | material: reach the 3:1 figure-ground floor | 0.4525 | 0.5611 | ACCEPT +0.0046 |
| r05 | material: clear 3:1 cleanly | 0.4528 | 0.5600 | ACCEPT −0.0054 |
| feedback-r01 | human review: emission, notch, mouth, one key - **ships** | 0.5005 | 0.6253 | ACCEPT +0.3267 |

**Baseline 1024 composite 0.4268 → 0.4528 at r05 → 0.5005 after the human-feedback round.** Stopped after four
consecutive neutral rounds, which is the loop's stop condition. The residual
floor is composition, not material: C2's flask is larger, lower and lit across
the tile differently, and the metric cannot separate that from a material gap.

Two rounds were kept despite a flat composite, on the reference's own rule that
the score is a proxy for a human judgment: r03 made the signature mid-air
cascade legible, and r05 cleared a rubric floor the composite does not encode.

### What the measurements actually found

The `material-recipes.md` rule ("measure the reference, never assume a
relationship") earned its place twice here, both times against an assumption
that felt obviously true:

1. **Molten is not bright.** The first two drafts authored the melt as
   bright-and-yellow, reasoning that hot means light. Sampled on matched
   geometry, C2's melt sits at luminance **0.42 to 0.53** and hue **5 to 9
   degrees**; the drafts sat at **0.57 to 0.80** and hue **20 to 25**. The whole
   ramp moved 17 degrees toward red and about 0.22 down. That single correction
   is the difference between "peach plastic" and "material at temperature".

2. **A translucent stream is darkest along its axis.** The master was built
   with a bright hot core down the middle, which is what a lit rod looks like.
   C2's stream measures L 0.612 on its lit flank, **0.469 on its axis**, and
   0.504 on its shaded flank - the axis is the *darkest* part, because that is
   where the material is thickest and attenuates most. The core ribbon is now a
   dark axis and both flanks are lit; after the change the master reads
   0.631 / 0.469 / 0.510 against those three numbers.

A third finding is a construction rather than a colour: the two warm veils over
the melt (the stream's glow and the droplet's) were peach `#FF9C60`, the colour
the melt throws *onto porcelain*. Over the melt itself they were lifting it 0.12
in luminance and 8 degrees toward yellow. Light thrown by the melt onto the melt
is the melt's own colour; only what escapes past the rim goes peach.

---

## Round `feedback-r01` - four defects a human named, and the metric could not

The loop had stopped correctly at r05 on four consecutive neutral rounds. What
restarted it was a human putting take A beside its own rasters and naming four
differences. Three of them the metric stack cannot see at all; the fourth it had
**inverted**. The general form of all four is now recorded in
`create-mac-icon/references/material-recipes.md` (entry *"create-skill A vs C1 vs
C2, reviewed by eye"*); this is what applying them to the artifact they came from
actually cost and bought.

### What was measured off C2 before anything was authored

Every number below is sampled off `icon-engineC2-6c0a72-masked.png` at 1024, on
the reference's own geometry, not on the master's.

| Property | C2 | shipped master (r05) |
|---|---|---|
| pool luminance, p10 / median / p90 | 0.217 / 0.396 / 0.667 | 0.404 / 0.477 / 0.525 |
| pool hue, p10 / median / p90 | 4.3° / 14.4° / 33.5° | 12.7° / 16.2° / 19.9° |
| pool brightest pixel | 0.913 | 0.751 |
| hot core (top 2% of pool) | 110 × 163px patch, centroid (515, 532) | no core: top 2% starts at 0.584 |
| cavity wall where the pool lights it | `#FC6C26`, L 0.510, S 0.841 | `#F0E6D5`, L 0.908, S 0.113 - unlit |
| rim top face, far side | `#FCA76D`, L 0.711, S 0.566 | `#E7DBCB`, L 0.867, S 0.120 |
| rim band, far / near, at matched x | 30px / 52px | 38px / 38px - concentric |
| wall terminator at y=760, left→right | 0.867 → 0.723 → 0.570 → 0.522 → 0.506 → 0.444 → 0.303 | 0.819 → **0.905** → 0.831 → 0.697 → 0.545 → 0.469 |
| ground TL / TR / BL / BR / ML / MR | 0.917 / 0.790 / 0.849 / 0.596 / 0.908 / 0.797 | 0.898 / 0.839 / 0.798 / 0.751 / 0.913 / 0.861 |
| cast shadow centroid vs base centre | +294, +115 (21° below horizontal) | +42, +60 (near-vertical) |
| notch | slot at the front wall, centre 6.7° left of dead front, ~55px at the lip, closing ~110px down, melt in its top 75px; key tab 56 × 85px straddling the parting | none: plain circle, key drawn as a stroke |

### What changed

**(a) Vibrancy is emission, not saturation.** The pool was rebuilt to the
`material-recipes.md` emissive-interior construction: a hot core ramp
(`#FFE9A8` → `#FCCF47` → `#FBAE2E`) falling to a deep rim (`#D61501` → `#960B01`),
a separate blurred bloom layer over it, the cavity wall relit to the measured
`#FC6C26`, a warm bounce on the rim's top face strongest where the rolled lip
turns toward the melt, a warm inner-lip line at the measured L 0.916, and a tip
glow on the stream's leading bulb (C2's stream tip reads L 0.85 against a shaft
of 0.21-0.30 - the pour is lit by the pool it is about to join). The previous
round's constraint still holds and was not relaxed: the bulk of the melt is deep
red at L 0.24-0.32, hue 5-10. Brighter here is a hotter core and real bounce, not
a lighter fill.

**One bug found doing it, and it is the largest single cause of the muted read.**
`rimClip` was `<path d="{outer} {inner}"/>` with no `clip-rule`. Two subpaths
wound the same way, nonzero unioned them, and "the rim annulus" was silently the
whole outer disc - so every warm veil meant for the porcelain was being painted
straight across the melt. That is a *third* peach veil over the accent, on top of
the two this loop had already caught and removed by hand. With `clip-rule="evenodd"`
the pool's own colour comes back: the lune measured `#EB562E` L 0.452 S 0.805
before the fix and `#DA1A02` L 0.257 S 0.991 after, against C2's `#D51504`
L 0.238. Lesson worth keeping: **a clip that is quietly wrong reads as a material
failure, and a saturation check cannot tell the two apart.**

**(b) A primitive silhouette reads as generic.** The flask now carries the
parting notch as a real cut: an 80px slot opening at the mouth's near arc,
closing 96px down, its top 82px filled with melt that has run into it, a lit
cut-face on the key side and a shadowed one away from it, continuing into the
vertical seam with a 56 × 80px interlocking key. The horizontal parting is now
*interrupted* by that key rather than run underneath it - an interlock, not a box
laid on a line. At 128px the notch is a legible ~7px bite in the near rim with
melt in it; the key tab is a faint mark, consistent with liability 3.

**(c) The inner edge is not the outer edge scaled.** `mouth_in` is raised
`MOUTH_RISE = 11.0` above concentric, derived from C2's 30px far band against its
52px near band (a concentric annulus would make both 41). It is also interrupted
by the notch. The cavity and the pool still ride the same disc, so nothing drifts
out of register.

**(d) Light direction is rankable.** The wall gradient was transcribed from C2's
own terminator and is now monotonic left to right - the old ramp brightened again
at 12% and at the far right, two counter-lights in a one-key scene. The ground
was re-anchored so its peak is at the left-middle and its floor at the
bottom-right. The cast shadow was rebuilt from the **base disc** rather than the
silhouette, so it lies on the ground plane instead of climbing the wall it
belongs to, and it now runs down and to the right at the measured angle.

### Before and after

| | r05 (shipped) | feedback-r01 | C2 |
|---|---|---|---|
| composite 1024 | 0.4528 | **0.5005** | - |
| composite 256 / 128 / 32 / 16 | 0.4158 / 0.4281 / 0.7184 / 0.7849 | **0.4927 / 0.5340 / 0.7724 / 0.8271** | - |
| five-size mean | 0.5600 | **0.6253** | - |
| pool L, p10 → p90 | 0.404 → 0.525 (spread 0.121) | **0.302 → 0.585** (spread 0.283) | 0.217 → 0.667 (0.450) |
| pool hue spread (p10→p90) | 7.2° | **17.0°** | 29.2° |
| cavity wall, lit by the melt | L 0.908, S 0.113 | **L 0.50, S 0.79** | L 0.51, S 0.84 |
| ground TL/TR/BL/BR/ML/MR | .898/.839/.798/.751/.913/.861 | **.934/.802/.841/.630/.941/.772** | .917/.790/.849/.596/.908/.797 |
| wall terminator monotonic? | no (0.905 at 12%) | **yes** | yes |
| melt vs tile | 3.04:1 | **4.65:1** | 1.17:1 |
| shaded flank vs tile | 3.98:1 | 3.21:1 | 3.25:1 |
| lit flank vs tile | 1.01:1 | 1.20:1 | 1.16:1 |
| gate vs r05 | - | **ACCEPT +0.3267 net** | - |

The composite moving is the surprise, not the point. The brief for this round
expected a flat or slightly negative composite, because three of the four defects
are invisible to the metric stack and the fourth was inverted by it. What
actually moved the number is mostly (d) and the `rimClip` bug: aligning the
ground field and the cast shadow to C2's is a large, low-frequency luminance
change, which is exactly the kind of thing SSIM and the luminance field *can*
see. The notch and the non-concentric mouth are worth about nothing to the score
and are most of what makes the object look designed. **A gate ACCEPT here is
corroboration, not the reason.**

### What it cost

- **`shaded flank vs tile` fell 3.98:1 → 3.21:1.** Matching C2's ground means a
  darker bottom-right, and the shaded flank sits in it. Held deliberately above
  3:1 rather than tracking C2 all the way to its 0.596 corner: the rubric
  outranks the reference, and C2's own right-hand figure-ground is 1.19:1 at the
  silhouette edge, which is a check it fails and this master passes.
- **`lit flank vs tile` went 1.01:1 → 1.20:1** - slightly better, still liability 1,
  still the porcelain register's standing trade.
- **Two more paths, one more gradient, +7.9KB** (60,888 → 68,691 bytes). Within the
  complexity envelope; `structure` PASSes.
- **The pool's low end is still 0.09 short of C2's** (p10 0.302 against 0.217).
  Most of that residual is geometry, not material: C2's visible pool lune is a
  larger share of its cavity than this master's, so the same ramp integrates
  brighter. Closing it means moving the composition, which this round was scoped
  out of.

---

## Decisions made without asking

- **Round flask, not a superellipse one.** Distinctness from `create-mac-icon`
  outranked the appeal of reusing the set's curve, which is that icon's own
  signature.
- **Two-part flask with a keyed parting.** Came out of take C1 and is
  factually right (a casting flask is a cope and a drag). Kept even though the
  key vanishes below ~48px: it earns rubric #11 at large sizes and costs
  nothing at small ones.
- **The stream enters through the top edge rather than from a drawn ladle.**
  A ladle would be a third prop and the anti-checklist's failure mode #5 is
  metaphor pile-up. Edge-bleed is a sanctioned Tahoe device and it buys the
  same information for one less object.
- **Take C2 kept as the reference rather than the ship.** Pipeline rule: a flat
  raster is failure mode #10 by construction, whatever it scores.
- **Ground warmed slightly off the sibling constants** (`#F7F3ED` → `#F6EFE1`,
  `#E8E1D6` → `#DDD0B7`) during r01. Set kinship is preserved; the shift is
  small and it was the measured fix for a field sitting 0.09 lighter than the
  reference's.

---

## Known liabilities

1. **The flask's lit flank is 1.20:1 against the tile beside it.** Half the
   body separates from the ground by rim light and contact shadow alone, so it
   softens under grayscale or a heavy tint. This is the porcelain register's
   standing trade, the sibling `create-mac-icon` icon shares it exactly, and the
   reference itself sits at 1.16:1. First thing to look at if a Tinted variant
   reads weak.
2. **The flask's shaded flank is 3.21:1, down from 3.98:1.** Matching the
   reference's ground field put a darker corner behind the shadow side. Held
   above the 3:1 floor on purpose rather than tracking the reference all the way
   down; going further would trade a rubric check for fidelity points.
3. **The parting key and the detached droplet both disappear below ~48px.**
   The icon reads correctly at 16px, but the two devices that make it *this*
   icon are large-size only.
4. **The mass sits low** (bottom margin 105px against 227px at the sides),
   because the vessel stands on a ground plane while the pour occupies the
   upper half. Deliberate, but it makes the tile's top-left quadrant the
   emptiest region in the set.
5. **The fidelity composite sits at 0.5005 of a theoretical 1.0.** Most of the
   remaining distance is composition, not material: C2's flask is larger, lower
   and its pool lune is a bigger share of its cavity, and no further round can
   close that without abandoning this composition for C2's.
6. **Three of the four defects a human found were invisible to the whole metric
   stack, and the fourth was inverted by it.** The gate went on returning ACCEPT
   through four rounds that fixed none of them. Whenever this icon is revisited,
   put it beside its rasters first and measure the specific thing that looks
   wrong; a general metric will not have caught it.

---

## Round `banner-c1` - the banner moved to take C1, and the bench had to be re-derived

The README banner was showing take A. A human preferred C1's light direction, so
the banner now carries `icon-engineC-4a73ea-masked.png`. This is not an `<img
src>` swap: the bench is not a backdrop, it is the icon's own ground plane
continued past the tile, and take A supplied its numbers from `build_icon.py`
while C1 is a raster that supplies none. All four had to be measured off the
pixels.

### The new constants

| | take A | C1 | how C1's was got |
|---|---|---|---|
| `KY` | 0.515 | **0.399** | axis-aligned conic fit to the pool's own boundary |
| `POOL` | 512, 646 | **509, 541** | centre of that same fitted ellipse (rx 209, ry 83) |
| `LIGHT` | -0.81, -0.58 | **-0.43, -0.90** | shadow-rejecting linear fit to the tile ground's blue channel |
| `BASE` | (n/a) | **510, 747** | the foot's ground contact; new, see below |

### What the measurement cost to get right

- **Masking on warm saturated pixels does not work**, as already suspected: the
  pour is warm too, so the vertical extent takes in the whole stream and `KY`
  comes out above 1.
- **Neither does fitting the pool's near arc alone.** Take A was used as a
  control throughout - its truth is known, so any estimator can be scored. A
  one-flank arc returns `KY` 0.316 against a true 0.515. The fit only becomes
  sound when the traced arc reaches BOTH extremities: at coverage
  `|x-cx|/rx <= 0.98` it returns cx 512.0 (true 512), rx 212.4 (true 211) and
  `KY` 0.527 (true 0.515), and the error runs away to -16% by the time coverage
  drops to 0.86. Worth keeping: the residual is *lower* on the bad fits, so RMS
  will not tell you which one to believe. Coverage will.
- **A had to be read differently from C1.** On take A the melt's near boundary is
  the aperture's near lip, not a waterline - the pool below it is occluded, and
  the trace matches A's known mouth ellipse to within 0.9px. On C1 the same
  boundary IS the pool's own edge. Assuming either structure for both gives a
  garbage ellipse; the overlay is what settles it.
- **The answer was confirmed by eye, not by residual.** An ellipse on the fitted
  numbers lands on the melt's boundary; the same ellipse at take A's 0.515 rides
  up onto the lit far wall. Concentric rings drawn at 0.399 read as lying on the
  ground the flask stands on; at 0.515 they read as a steeper plane the flask is
  not on.

### What that forced in the banner beyond the three numbers

- **`BASE` is new.** The spill used to hang off `POOL`. Between takes the melt
  moved 105 units up the tile and the vessel did not, so a spill tied to the pool
  detached from the foot. It now hangs off the measured contact centre.
- **The cooling flask's melt is now placed as a fraction of its own aperture's
  `ry`, not in flat pixels.** The old 15 and 26 were tuned to 0.515; on a flatter
  plane a fixed drop pushes the melt clean outside its own clip and the vessel
  renders as a dark ring instead of a filled one.
- **The bench key is a linear ramp now, not a radial hotspot.** A radial
  gradient anywhere near a 1600x520 frame throws a divergent field whose
  direction across the frame is its own geometry rather than the azimuth it was
  given: a sweep of the placement distance ran the rendered direction from
  left 0.27 to left 0.89 without ever passing through the 0.43 the icon
  measures. A ramp along the measured vector hits it exactly.

Measured back off the finished render, the bench reads -0.42, -0.91 against the
icon's own -0.43, -0.90. For the record the take-A banner this replaces read
-0.94, -0.34 against its own icon's -0.81, -0.58, so it was never as closely in
register as its header claimed.

---

## Files

| File | What it is |
|---|---|
| `build_icon.py` | Engine A. Geometry and material as named constants; a fidelity round is a parameter edit, never path surgery |
| `icon.svg` | the shipped master, four named layers, generated - edit `build_icon.py`, never this |
| `icon.png`, `icon-256.png`, `icon-128.png` | exports, all from the master |
| `render_audit.py` | renders every take at the sheet's 2× sources, masks the rasters with the exact superellipse, writes the exports |
| `audit.html` + `audit-renders/` | the contact sheet, every take scored including the losers |
| `fidelity-runs/` | seven rounds: `rNN.icon.svg` and `feedback-r01.icon.svg`, each with `score.json`, residual and edge maps |
| `icon-engineB-arrow-d2f7ef.svg` | Engine B, Arrow 1.1 |
| `icon-engineC-4a73ea.png`, `icon-engineC2-6c0a72.png` (+ `-masked`) | Engine C, GPT Image 2 |
| `banner-src.html`, `banner.png` | the README banner, composed HTML at 1600×520 rendered 2× to 3200×1040 |
