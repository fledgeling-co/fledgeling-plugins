# create-mac-icon icon notes

**Direction: "The Cast".** The studio's *Tahoe Gel-Glass* sub-register (a), porcelain
cushion tile carrying one coloured gel object, crossed with the device bank's #16 *the
icon performs the verb*, #17 *tile-as-machine with a diegetic aperture*, #5 *dual-function
primitive* and #21 *authored overlap*. The subject is a skill whose entire output is a mac
app icon, so the icon makes one on camera: a vermilion gel tile has just been lifted out
of an open plaster mould, and the cavity it came from is still open beneath it, empty
except for the warmth it kept. Solid and void, the same shape twice.

Runner-up: sub-register (c) *dark glass*, a mould lit from inside on charcoal. Rejected
on two counts. The dark deep-sea register belongs to the sibling `trawl` and two plugins
in one marketplace should not share a ground; and the whole argument here is that you can
*see* the negative the cast came from, which a dark ground puts in shadow. Also considered
and dropped: Direction 8 *Instrument Emblem*, because this skill has no gauge or chart to
quote, and Direction 7 *Diagonal Tool*, which the catalogue names as the most template-worn
move in the corpus.

**Signature.** Both the cast tile and the mould cavity are the marketplace's own
superellipse, the exact path in `squircle-path.txt` that masks every icon in this set,
not an approximation of it. So the artwork contains the shape it makes, at three removes:
the outer mask, the cavity, the cast. `build_icon.py` parses that path once and every
object in the icon is a scaled instance of it. The second half of the signature is the
warmth left in the empty cavity: a pooled peach bounce on the plaster floor, strongest at
the far end where the cast's mass sat longest and paling toward the near lip. That bounce
is the authored overlap the era's grammar asks for, it is the one thing a flat pre-masked
raster cannot fake under system tinting, and it is semantically true rather than decorative.

**Risk taken:** an isometric object in a set whose siblings are mostly frontal. It is held
by Tahoe grammar #7, which keeps the 3D miniature idiom alive in matte-satin materials
with real contact shadows and no gloss, and by the fact that a mould only reads as a mould
when you can see into it.

**Palette.** Two families only. Warm-neutral porcelain and plaster carry the ground and the
block (`#FFFEFC` to `#F7F3ED` to `#E8E1D6` cushion with a `#8A7A62` vignette; block face
`#FFFFFD` to `#F4F0E6` to `#DCD4C3`; per-face walls `#F6F1E5` to `#C8BDA6` on the lit side,
`#C6BCA9` to `#A2957C` on the shaded side; cavity `#7C7057` to `#D0C6AE`). One vermilion,
kin to Fledgeling's `#C4622D`, is spent on the cast and on the warmth the cast left behind,
and nowhere else: face `#FFE0C0` to `#FC9053` to `#F05821` to `#D8451A`, walls `#F86E2C`
to `#BC2E0C`, bounce `#FF9C60`. One soft top-left light: rim highlights, soft ambient
occlusion, real contact shadows, zero hard speculars, and no emissive interior, because
that sanctioned second source is trawl's and taking it would blur two siblings together.

**Deliberate avoidances.** The dark register (trawl). The blue and indigo ramp the corpus
census records as the template default across 271 chromatic hits. And every sibling glyph
device: trawl's net, create-swe-project's hull at first water, ship-armada's three hulls in
echelon, improve-skill's plane blade and shaving, armada-sync's stamped entry,
compaction-quality's sediment cylinder, design-review's frosted proof slabs.

## Audit: 11 of 12, zero failures on the non-negotiable 1 to 4

Full contact sheet with every take scored and every loser kept: `audit.html`.

Full-bleed 1024 artwork with the squircle as a *clip*, no baked corners and no baked drop
shadow. The focal group spans x 171 to 843 and y 241 to 793, so margins are 171 / 181 /
241 / 231 and the composition is optically centred. Checks 3 and 4 were verified on real
renders rather than imagined: a luminance-thresholded silhouette proof still names "a
rounded tile lifted off a block with an open recess", and the 32px render magnified six
times still carries the cast, the block and the warm cavity.

**The point is deducted at #7, figure-ground.** Measured, not assumed: the cast's dominant
top face is `#EB6D3D` against local porcelain of `#F4F0EA`, which is **2.72:1**, under the
3:1 bar. It survives grayscale comfortably, with 99 levels of separation, so the read is
never in doubt; the ratio simply does not clear the line. Deepening the gel would clear it
and would also walk back the r06 chroma match that closed most of the material gap, so the
point was conceded rather than bought.

**#10 passes by construction:** four layers, `#bg` / `#mid` / `#fg` / `#highlight`, mapping
1:1 onto Icon Composer, with identity carried by shape and value and colour as the last ten
percent.

### Known liabilities

1. **Figure-ground is 2.72:1**, under the 3:1 bar, as above.
2. **The focal spans 65.6% of tile width**, a whisker over the 55 to 65% composition
   constant. Taken deliberately in fidelity round 1 to close a measured scale gap against
   the raster, and worth re-testing.
3. **The plaster block sits close in value to its own porcelain ground.** That is the
   porcelain register's nature and the reference does the same, but it makes the light
   Tinted variant the weakest of the four, carried by the cast alone.
4. **At 16px the cavity survives as a warm smudge**, not as a readable superellipse. The
   icon keeps its subject at menu-bar size but loses the "same shape twice" argument there.
5. **The cast is authored parallel to the mould** where both raster takes tilt it. This
   keeps the mirroring legible, which is the whole idea, and it permanently caps how close
   the fidelity score can get to the reference. It is a structural divergence, not a defect.
6. **LPIPS did not run** (no torch on this host), so the 1024 material number came from the
   weaker of the two available metric stacks and should be read as directional.

## Three engines

- **Engine A** is the shipping master, `icon.svg`, generated by `build_icon.py` so geometry
  and material are named constants and every fidelity round is a parameter edit rather than
  path surgery. 11/12.
- **Engine B**, `icon-engineB-arrow-626f04.svg`, Arrow 1.1 from the spec-as-brief, lost
  badly at 3/12: a 150 by 130.4 viewBox rather than square artwork, both superellipses
  softened into lozenges, a grey interior shadow z-fighting the dish rim, and no named
  layers. Nothing was salvaged geometrically. Its one real contribution was as a negative
  control: it proved the exact superellipse is load-bearing rather than decorative, because
  once the shape stops being specific, solid and void stop reading as the same shape twice.
- **Engine C** produced two rasters through GPT Image 2 with four porcelain-register
  exemplars from `corpus/apple-2026/` as reference images (Safari, Photos, Reminders, News).
  Both scored 9/12 and both **won the material comparison**, as the pipeline expects. Neither
  can ship: a flat pre-masked raster is failure mode #10 by definition, and both grounds are
  dead-flat white with no cushion, which the Tahoe grammar names as the previous era's tell.
  Both are kept, squircle-masked with the exact path, as `icon-engineC-*-masked.png`.

**C2 was chosen as the fidelity reference over C1** even though C1 has the stronger 16px
read. C1's cavity has no visible floor, so its mould reads as a hollow frame and the
negative stops being the negative of anything; C2's cavity has a floor, a lip and a pooled
bounce, which is the concept stated correctly. Matching the better score is not the same as
matching the better icon.

## The fidelity loop

Seven rounds against `icon-engineC-fe8278-2-masked.png`, one edit class each, plus one
measured correction after the loop closed. State in
`fidelity-runs/` with a `score.json` per round and a `rounds.json` ledger.

| Round | Edit class | 1024 | 32 | 16 | Gate |
|---|---|---|---|---|---|
| r00 | baseline, first draft | 0.6546 | 0.6947 | 0.7684 | baseline |
| r01 | coarse structure | 0.6584 | 0.7118 | 0.7804 | ACCEPT |
| r02 | material | 0.6588 | 0.7186 | 0.7840 | ACCEPT |
| r03 | material, per-face separation | 0.6628 | 0.7195 | 0.7853 | ACCEPT |
| r04 | detail | 0.6632 | 0.7176 | 0.7845 | ACCEPT |
| r05 | small-size repair | 0.6636 | 0.7205 | 0.7848 | ACCEPT |
| r06 | material, shadow chroma | 0.6678 | 0.7208 | 0.7857 | ACCEPT |
| r07 | material, plaster range | 0.6655 | 0.7198 | 0.7841 | rolled back |
| **r08** | **detail, block rim light** | **0.6685** | **0.7206** | **0.7855** | **ACCEPT, ships** |

Baseline to shipped: 1024 composite **0.6546 to 0.6685**, 32px 0.6947 to 0.7206, 16px
0.7684 to 0.7855, with no size worse than baseline. r07 passed the Pareto gate on tolerance
and was rolled back anyway, because all five sizes moved the wrong way and the round bought
nothing. r08 was taken after the loop had closed, for a visible artifact rather than for a
score: the block's lit edge peaked exactly where the cast occludes it, so the surviving
stub read as a stray hairline against the porcelain. It was re-scored rather than
eyeballed, and kept because it cost nothing.

**Two rounds were driven by measurement rather than by looking.** r03 came from reading the
residual: a single gradient swept across a whole extrusion band reads as one bent surface,
so the block, the cavity and the cast were each split at their own corner into two front
faces with separate gradients. r06 came from sampling both images: the reference's darkest
gel pixel is `#DC2F0E` where the master's was `#A93411`, which is the difference between
translucent resin, which keeps its chroma where it turns away from the light because light
still travels through it, and an opaque solid, which goes brown. Raising the dark end of
the gel ramp without touching its luminance range was the largest single gain in the loop.

**Recipe confirmed for `material-recipes.md`** (not written there, because this commission
was scoped to `assets/` only; the orchestrating session should add it):

> **2026-08 · create-mac-icon "The Cast"**. A translucent gel object must keep its
> *saturation* in shadow, not just its luminance. Sampling the reference's darkest gel
> pixel against the master's caught a master whose shadows had gone brown (`#A93411` vs
> `#DC2F0E`) while its luminance range and mean saturation already matched, so the gap was
> invisible to a range check and obvious to a darkest-pixel check. Lesson: *check the dark
> end's hue, not only the ramp's endpoints*. A shadow that desaturates reads opaque, and
> opacity is the opposite of the era's whole material claim.

## Banner

`banner-src.html`, composed HTML rendered at viewport 1600 by 520 at 2x to `banner.png`
(3200 by 1040). The bench in the banner is the same bench the icon sits on: the two empty
cavities on the right are the same superellipse path under the same dimetric projection
(KX 1.0, KY 0.515, the icon's own frame), cut by the frame so the bench visibly continues
and there is another mould waiting, and the nearer one holds the same warm bounce at a
fraction of the strength. Any change to the icon's projection or palette must be re-derived
there or the plane tilts out of register with itself.

Type is **Sora**, whose bowls are drawn as squared circles rather than true ones, which is
the superellipse the icon is built from, in type. No sibling in this marketplace uses it
(the set currently runs Instrument Sans, IBM Plex Sans and Mono, JetBrains Mono, Archivo
and Schibsted Grotesk).

## Measured loop, `loop-runs/` (unmasked `icon-engineC-fe8278-2.png`, metric v2)

A second loop against the raster **as generated**, not the squircle-masked copy, so the
corner disagreement is baked into every number and only deltas mean anything. `r00-baseline`
is the r08 master re-scored under this reference. r01 (material) was REJECTed on 128px and
reverted by the harness.

### r02 · detail · ACCEPT, +0.0112 net, every size up

| size | r00 | r02 | Δ |
|---:|---:|---:|---:|
| 1024 | 0.5046 | 0.5082 | +0.0036 |
| 256 | 0.4164 | 0.4193 | +0.0029 |
| 128 | 0.3895 | 0.3905 | +0.0010 |
| 32 | 0.6304 | 0.6322 | +0.0018 |
| 16 | 0.7225 | 0.7244 | +0.0019 |

**Measured off the reference, in perpendicular luminance profiles across every convex
edge.** Nothing on either object is a cut edge; each arris is a rolled fillet wide enough
to be a surface rather than a stroke, and the master had drawn all three as one-pixel
steps:

- **block, top face → front wall.** Reference holds L 0.950 to the arris, then rolls
  monotonically to the wall's 0.680 over **26px** (0.897 / 0.853 / 0.763 / 0.691 at
  y 802/806/810/818, x=600), midpoint about 11px below the arris. Master: 0.900 → 0.705
  in a single pixel.
- **gel, face → side wall.** Reference 0.518 → 0.302 over **21–27px**, monotone, with
  **no bright line anywhere on the wall side**. Master had a `#FF9E6B` seam there
  (0.417 → 0.508 → 0.364), clipped to the wall — an invented highlight, the fourth time
  in this library's history that "the highlight is lighter than its surroundings" has been
  assumed where the reference has no such relationship.
- **gel crest.** The reference's bright band sits on the **face** side of that arris, not
  the wall side: +0.09 over the face at the lit left corner (0.685 against 0.593 forty px
  up), extinct by the right corner. That is a wrap highlight on a shoulder, and it is
  where a rolled edge's normal actually points at a top-left key.
- **cavity mouth.** Reference rolls **54px** into the near lip (0.819 → 0.974 crest) and
  **72px** at the right rim (0.744 → 0.989), the crest sitting *above* the surrounding
  top face. Master: a hard step of +0.25 with a dark hairline on the rim.

**What changed.** Three constants and three constructions, all in `build_icon.py`:
`FILLET_BLOCK` 26, `FILLET_GEL` 22, `FILLET_LIP` 16. Each fillet is one blurred stroke
laid along the arris and painted with **the adjoining face's own gradient**
(`url(#plasterFace)`, `url(#gelFace)`), clipped to the turned face — so the roll inherits
that face's lateral variation for free and the two gradients cannot drift out of
registration. The gel's seam moved from the wall side to the face side and became
`gelArris`, a gradient dying along +x to match the measured falloff. The cavity's rim
hairline moved from *on* the rim to `shift(cav_top, 0, FILLET_LIP)` — occlusion belongs
below a lip's crest, inside the recess, and the clip drops it on the near side where the
lip's inner face is the lit floor. Rendered roll widths came out 27–30px (block), ~30px
(gel), 20px (near lip), against the reference's 26 / 21–27 / 54.

**Where the reference was not followed, and why.** Its cavity lip is a 54–72px roll
cresting *brighter* than the top face, which leaves the mouth at roughly 0.03 boundary
contrast — the reference reads as a hole by its interior, not by its rim. Copying that
wholesale is prior learning #3's trap on a live figure-ground boundary, and liability #4
already has the 16px cavity down to a warm smudge. `FILLET_LIP` was capped at 16 for that
reason. It still cost something: mouth contrast (cavity floor against the rim face beside
it) fell 2.11:1 → 2.03:1. Cast figure-ground is untouched at 2.58:1 on this window, and
the 32px render still carries cast, block and warm cavity separately.

**What it cost.** 3079 bytes, 3 paths, 1 gradient, 1 clipPath; 33 paths and 40KB against
the envelope's 400 and 200KB. `self_contrast` identical to baseline at 32 and 16
(0.4342 / 0.3862), so nothing went mushy to buy the gain.

**Observed and deliberately not fixed:** a white stub of the `cavLip` far-rim highlight
survives just left of the cast's silhouette, where `notTile` stops masking it — the same
artifact class as the old loop's r08. It predates this round and folding it in would have
confounded the fillet measurement.

### r03 · detail · ACCEPT, −0.0051 net; SSIM up at four sizes, edges down at four

| size | r02 | r03 | Δ | ssim | edge_f1 |
|---:|---:|---:|---:|:---|:---|
| 1024 | 0.5082 | 0.5056 | −0.0026 | 0.8011 → 0.8022 | 0.0219 → 0.0092 |
| 256 | 0.4193 | 0.4178 | −0.0015 | 0.5419 → 0.5432 | 0.0783 → 0.0690 |
| 128 | 0.3905 | 0.3907 | +0.0002 | 0.3607 → 0.3627 | 0.2508 → 0.2478 |
| 32 | 0.6322 | 0.6311 | −0.0011 | 0.1855 → 0.1865 | 0.7539 → 0.7502 |
| 16 | 0.7244 | 0.7243 | −0.0001 | 0.2124 → 0.2121 | 0.9851 → 0.9851 |

The gate accepted on tolerance, not on a gain. Read it honestly: SSIM — 0.40 of the
composite at ≥128 — rose at four of five sizes, and `edge_f1` paid for it at four of five,
because a soft wash blurs exactly the gradient the Sobel keys on. The round bought
material, not score.

**Measured off the reference, by binning each object by depth inside its OWN silhouette**
(erode the material mask one pixel at a time, bin by shell index, read L and S per shell).
This is the technique the round turned on; nothing here is visible to a window probe,
because the quantity is a function of distance-to-edge, not of position.

- **the gel carries an omnidirectional rim.** d3 → d34, per quadrant:
  dL **+0.075 / +0.085 / +0.121 / +0.090** (NW/NE/SW/SE), dS **−0.084 / −0.108 / −0.171 /
  −0.135**. Mean **+0.093 L, −0.125 S** over 34px, and the maximum sits at the silhouette
  itself (0.5726 / 0.5736 / 0.5743 at d1/d2/d3, monotone down after). All four quadrants,
  including the two facing away from the key.
- **the plaster's rim is directional.** Same instrument on the block: **+0.128** on the
  near bottom roll against **+0.011** on the far top edge.
- **so they are two different effects.** A directional edge lift is the key rolling over an
  arris. An omnidirectional one cannot be — there is no light source at every azimuth. It
  is the short optical path through a translucent body at grazing angles. Same light, two
  materials, and only the translucent one carries a rim. This is prior learning #1's twin:
  #1 says translucency keeps saturation in shadow; this says it also loses saturation and
  gains luminance at the edge, and both are read off the material's own darkest/rim pixels
  rather than assumed.
- **the master had 44% of it** (mean **+0.041 L, −0.065 S**) and only in the quadrants
  where `gelShoulder` happens to sit — NW +0.062, SE +0.064 against SW **+0.005**. So the
  master's rim read as a lit top, not as a material property.

**What changed.** Two constructions in `build_icon.py`:

1. **Rim scatter by self-stroke.** `GEL_SCATTER = "#FFD7BC"` (lighter and less saturated in
   one move, which is what one measurement of each asked for), stroked along `tile_sil` at
   `RIM_SCATTER * 2` = 34px, clipped back to `tileSil` so only the inward half survives,
   blurred under `bM` so it decays to nothing about 40px in — the measured ramp. Result
   mean **+0.070 L, −0.111 S**: 75% of the reference's luminance lift and 89% of its
   desaturation, and now present in all four quadrants (SW +0.005 → +0.043).
2. **`notTile` → `mouldKey`.** The mould's rim lights now see a key that the cast both cuts
   out *and* shadows: the cast's near shadow is painted into the mask at
   `KEY_OCCLUSION = 0.88`, using `CAST_NEAR`, which is now named once and shared with the
   shadow itself so the two cannot drift. This removes the white `cavLip` stub the r02
   entry deferred — it was reading **L 0.845 against a local 0.384** — on the physical
   ground that a rim highlight at full strength inside a cast shadow is the single light
   model contradicting itself. Costs nothing measurable: SW boundary 1.31 → 1.27, E
   2.01 → 1.99, rim profile unchanged (isolated by building the two edits separately).

**Where the reference was not followed, and why.** Its rim runs at full strength all the
way round because its cast stands on open, lit porcelain on every octant but two. Ours
overhangs the open mouth on its lower-left, where the backing is the shaded far wall:
**L 0.515, against 0.832 on the reference's same octant**. Copying the rim wholesale there
took the lower-left figure-ground from 1.31:1 to **1.05:1** — prior learning #3 on a live
boundary. `rimLit` (white, minus a `bM`-blurred `cav_top` at `1 − RIM_SHADED`) holds the
wash to 15% over the mouth and leaves it untouched everywhere else, recovering that octant
to 1.13:1. Still short of 1.31, and that is this round's real cost.

**What it cost.** 40065 → 44440 bytes, 33 → 37 paths, +1 clipPath, +1 mask, +1 colour;
gradients and filters unchanged at 17 and 4, against the envelope's 400 paths / 200KB.
`self_contrast` 0.4342 → 0.4331 at 32 and identical at 16 (0.3862), and the 16px render is
pixel-indistinguishable — the wash's 40px ramp is 0.6px at that size, so it cannot reach
the small read either way. Both tracked rubric ratios are untouched: mouth contrast
1.729:1 and cast figure-ground 2.649:1, before and after, on windows re-derived this round
(a shape of half-extent r spans ±r·1.741 on screen, so the earlier windows in this file sat
on the wrong surfaces; the numbers are not comparable to r02's 2.03 / 2.58, the windows
are). Rubric score unmoved at 11/12.

**Observed and deliberately not taken:** the reference's plaster carries a granular grain
with a period of about 4–6px at 1024. It dies before 128px, and uncorrelated texture
inflates local variance while covariance stays near zero, so SSIM — the largest single
weight at the sizes where it would live — punishes it on principle. It is a real
difference from the reference and the wrong thing to chase under this metric.

## Files

| File | What it is |
|---|---|
| `build_icon.py` | Engine A generator. Edit the constants here, never `icon.svg`. |
| `icon.svg` | the shipping layered master, fidelity round 8 |
| `icon.png`, `icon-256.png`, `icon-128.png` | raster exports of the master |
| `icon-engineB-arrow-626f04.svg` | Engine B take, 3/12 |
| `icon-engineC-27539d.png`, `icon-engineC-fe8278-2.png` | Engine C rasters, as generated |
| `icon-engineC-*-masked.png` | the same two, masked with the set's exact superellipse |
| `render_audit.py` | renders every take at the sheet's 2x sources and masks the rasters |
| `audit.html`, `audit-renders/` | the contact sheet and its renders |
| `fidelity-runs/` | per-round candidates, scores, residuals, edge maps, `rounds.json` |
| `banner-src.html`, `banner.png` | the banner source and its 3200 by 1040 render |
| `squircle-path.txt` | the set's superellipse, copied from the skill's assets |
