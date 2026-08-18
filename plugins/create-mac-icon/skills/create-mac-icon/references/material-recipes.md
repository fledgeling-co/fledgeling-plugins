# Material recipes — raster looks rebuilt as layered SVG constructions

The library the fidelity loop feeds. Each recipe is a construction that has
either been validated by the deep-research evidence base or won a real
fidelity iteration in this marketplace; new wins get added here **the same
session they're confirmed**, with the fixture they came from. This file is
why the skill gets better over time instead of relearning material physics
per commission.

Rendering caveat: keep filters simple and test in the scoring renderer
(`rsvg-convert`) *and* a browser — filter/mask support varies, and a
construct that renders differently across the two is itself a finding.

## The core table (research-validated)

| Raster look | SVG construction | Why the flat default fails |
|-------------|------------------|----------------------------|
| Soft cast shadow | Duplicate the object's silhouette, dark fill at 10-18% opacity, `feGaussianBlur`, clip to the ground, opacity falls off with distance | A single offset dark path reads sticker-like |
| Translucent gel/glass | Radial + linear gradient stack in one hue family, low-opacity white top-edge highlight, darker interior shadow near the base, clipped reflection arc | One fill + one gradient reads as print, not material |
| Frosted white glyph on a hue tile | White fill at 78-92% opacity so the ground bleeds through thinner areas, plus fold/emboss shading (slightly darker white on turned faces) | Flat `#FFFFFF` is the "Big Sur re-tread" tell — the translucency cues ARE the era |
| Embossed edge / inner bevel | Base gradient + an inner-shadow approximation (inset dark stroke, blurred) + a 1-2px rim highlight on the lit edge + local low-radius blur | Material is carried by small luminance transitions, not by outline |
| Metallic / chrome accent | Multi-stop non-monotonic gradient (light-dark-light), narrow specular paths along edges, masked reflection shapes | One linear gradient can't produce local highlight geometry |
| Ambient occlusion | Small dark translucent shapes tucked under each overlap, respecting occlusion order | A global dark blur ignores topology and muddies 32px |
| Cushion tile (Tahoe ground) | Radial gradient + a 1-2% inner white stroke ring + gentle edge vignette | A dead-flat ground is instantly previous-era |
| Authored overlap blend | Literal overlapping semi-opaque shapes — let the renderer multiply/lighten | Baking the blend into one shape dies under system tinting (#10) |
| Curl / ribbon volume | Build as a **swept surface**, not a spiral outline: one cross-section curve swept along the roll axis, cut into bands, each band shaded by its facing angle to the single light; far-side bands seen from inside the roll go to shadow with a transmitted lift; free end tapers in opacity | A closed spiral path with one fill reads as a flat coil or a capped tube, not a curl |
| Emissive interior | Bright core shape under a translucent shell, soft `feGaussianBlur` bloom layer above, restrained halo radius | Glow painted as opaque colour doesn't light its surroundings |

## Before you author anything: look at the corpus

Open 4-6 exemplars from `references/corpus/apple-2026/` in your register and
sample values out of them. Not "study the style" — read numbers: ground
luminance range, brightest point relative to the key, accent saturation, the
hue of the darkest pixel in a shaded face, rim-light treatment, contact-shadow
falloff. Put them in the spec before the first line of the build script.

Every entry below was a failure that a glance at the corpus would have
prevented, found later at roughly four rounds each. The corpus is free.

## The rule the entries below keep proving

**Measure the reference; never assume a relationship.** Five separate entries
below are the same lesson learned five times, each after failed attempts that
reasoned about what the reference "must" look like:

- the curl's cross-section is a true circle at 1.0 foreshortening, not the 0.54
  that had been assumed, and its axis is tipped 13° off the blade's (r04);
- the block rides as a *wedge* with a 55-to-90px taper, not a lifted parallel
  copy, at a measured 38.9° (block pitch);
- the reference's darkest gel pixel is warm where ours had gone blue, at matching
  luminance *and* saturation, so only a darkest-pixel check could see it (r01,
  The Cast r06);
- the curl reads *darker* than the ground beside it, so three attempts that
  assumed "highlight is lighter than its surroundings" all failed (shaving curl);
- binning the reference by candidate coordinate separates geometry from lighting
  profile, and says when a plane's light is undetermined and should be left alone
  (r08).

The technique generalises: **fit or sample the property you are about to author,
on the reference, before authoring it.** Every attempt that skipped this step and
reasoned instead has failed here, and the failures cost roughly four rounds each.
A corollary from r08: box out any translucent overlay before fitting, since the
reference's curl sat across the region being measured and inflated the near field
by 0.024.

## Marketplace-confirmed wins (add new entries below, newest first)

- **2026-08 · improve-skill round 21 — a texture emitted as a filter does not
  downsample, it re-samples; and a texture's path budget is spent on the amplitude
  solve, which is a gradient.** The fixture ran twenty fidelity rounds against a
  *declared* envelope of `--max-paths 3000 --max-bytes 350000`, argued in writing
  each time, and never reconciled it with the *delivery* envelope the marketplace
  gate runs — `400 / 200,000`, the same script's default. Every round passed its own
  structure check while the shipped master failed the shipping one at 1042 paths /
  231,249 bytes. Two constructions were built and measured against the round-20
  master. **The first check, before either, is which region owns the overrun**: the
  torn-ground grain held 830 of the 1042 paths and 152,573 of the 231,249 bytes, so
  the 96-band swept shaving that the audit sheet also named was never the problem and
  was left alone — which mattered, because that feature had a standing warning
  against any further change to its rims.

  **(a) The filter answer matches at full size and fails one size down, for a reason
  that generalises to every `feTurbulence` texture.** One noise field in the object's
  own frame, lit by `feDiffuseLighting` from the icon's key, costs **no paths** and
  reproduced the strokes almost exactly at 1024: the grain's spectrum isolated in
  quadrature against a grain-free control agreed in all four octaves (0.0081 / 0.0034
  / 0.0019 / 0.0011 against 0.0077 / 0.0035 / 0.0017 / 0.0010 at 3-8 / 8-16 / 16-32 /
  32-64px), 16px RMS contrast identical to four decimals, plane means within 0.0006 L,
  and boundary-crossing continuity *improved* because both planes take the same field.
  It then read as leather at 256. **`feTurbulence` is point-sampled at device
  resolution while geometry is area-sampled**, so a stroke averages down on the way to
  a small raster and a filter re-samples. Measured as the sd of (pixel − 3×3 box mean)
  on clean patches of the *direct* small renders, the relief ran **1.5× the strokes'
  per-pixel residual at 256 and 3.3× at 128**, and nothing moved it: `baseFrequency`
  swept over 5× changes the residual by 0.0002, deadbanding the field into sparse
  marks makes it *worse* (sparse marks at matched sd are higher-amplitude marks), and
  terracing buys `edge_f1` by drawing contours the reference does not have. **The
  residual is set by amplitude, and holding the full-size texture fixes the
  amplitude.** So the noise-relief recipe holds for a *small, low-contrast* surface —
  the same fixture's iron face, 10% of the tile, has shipped it since round 12 — and
  does not hold for a whole ground plane in an icon that also ships at 256 and 128.
  Test any relief on the smallest delivered raster, rendered directly at that size,
  before believing a full-size statistic about it.

  **(b) The path budget is not the marks, it is the amplitude solve — and that solve
  is usually a gradient.** "Specify ornament in luminance, not in alpha" is right, and
  the obvious way to honour it is to cut each mark into pieces and re-solve
  `amp / (substrate − mark)` per piece. That subdivision *is* the path count: 79
  ridges had become 830 paths almost entirely through it. But check whether the
  substrate's field is a coordinate a gradient can express — a radial ramp about a
  fitted point source, a linear ramp along the key's axis, which is what the
  "fit the coordinate before you fit the curve" recipe hands you. If it is, then
  `1 / (substrate − mark)` is a gradient too and it can be the mark's own **stroke
  paint**: continuous where the piecewise solve is stepwise, free in paths rather than
  25× their cost, and unable to drift from the field it corrects because it rides the
  same coordinate. 830 paths → 316 with no change to any mark.

  **(c) With opacity out of the element, the marks merge.** All that is left on a mark
  is stroke width and dash pattern, so quantise those onto a small grid and emit one
  path per occupied cell with every mark in it as a **subpath**. `stroke-dasharray`
  restarts at the beginning of each subpath — verified in `rsvg-convert`, where the
  merged and separate forms render bit-identically — so the merge is exact for
  identical attributes. 316 paths → 102 on a 3 × 3 × 3 grid, 102 of 108 cells
  occupied, and the grid was swept from 3/3/3 to 5/5/2 with the composite flat to
  0.0016, so the coarsest one ships and the paths go to headroom. Final: **1042 paths /
  231,249 bytes → 314 / 142,554, and the 16px render bit-identical**, 32px agreeing to
  0.5/255, SSIM(before, after) 0.9996 at 32 and 0.8951 at 1024 with every fixture
  invariant — 16px RMS contrast, split polarity, block figure-ground, the honed
  boundary's step and ratio — holding to three decimals.

  **(d) Three traps in bucketing, each of which cost a build.** Bucket
  **representatives must be the range's ends**, `lo + (hi − lo)·i/(n − 1)`, not its
  centres, whenever anything downstream reads a *tail* — edge and threshold metrics do,
  and centres capped mark strength at 0.92 of the original maximum and cost 12% of the
  plane's Sobel edges at the same band sd. A bucket's shared random parameter must be a
  **quantile of its distribution, not a draw from it**: three draws from a wide dash
  distribution gave duties of 0.39, 0.91 and 0.96 against a mean of 0.58, and the 0.96
  pattern — near-continuous line, almost no ends — landed in the most populated bucket
  and cost 46% of the plane's edges on its own. And a shared dash pattern needs its
  phase put into **geometry**, by starting each mark a random fraction of one period
  back behind a clip that removes it, because `stroke-dashoffset` is a per-element
  attribute and merging was the whole point; without it the marks land in step and draw
  a moiré band across the field.

  **(e) The metric was partly paid by the error being fixed, so decompose before
  reading the verdict.** `edge_f1` at 1024 fell 0.1252 → 0.0910 and the convergence
  gate REJECTed on that one size at −0.0059 (net −0.0080). Rebuilding the *old*
  generator with its subdivision progressively removed — same marks, only the piece
  length — isolates why: 190 → 1042 paths and 14,958 plane edges, 400 → 698 and 14,439,
  900 (no subdivision) → 504 and 12,276. **0.0117 of the 0.0342 was subdivision
  artifacts** the reference does not have, and reintroducing them deliberately as
  subpaths — free in paths — made `edge_f1` *worse* (0.0910 → 0.0849), because it is an
  F1 and false edges cost precision. The rest is the tail: pixels clearing the metric's
  0.10 gradient threshold went 4.73% → 2.28%, and raising the amplitude to recover them
  costs more in SSIM than it returns. A similarity metric can be earning part of its
  score from a construction artifact, so when a cheaper emission loses ground on one
  sub-metric, rebuild the predecessor with the suspected artifact removed and read the
  difference rather than the total. Fixture: `plugins/improve-skill/assets`,
  `icon-notes.md` round 21, `loop-runs/r16/`.

- **2026-08 · resume-session "The Kept Place" — which faces an oblique projection
  reveals is computable, a corner trim is not the radius, and thickness is what
  stops a lid being a mortarboard.** A shut graphite ledger on porcelain with a
  vermilion register ribbon folding over its fore-edge. Six findings, four of them
  construction bugs that no palette work could have reached.

  **(a) The visible side faces are a property of the axes, so derive them rather
  than choosing them.** With the depth axis `Q` travelling down-**right**, the tile
  shows the top face, the near face and the **left** face; the right-hand face
  folds back onto the top and is never seen. The test is one cross product: along
  the edge two faces share, a vertex of each must fall on opposite sides. Painting
  the folded-back face instead left the visible one unpainted, and the silhouette's
  own fill showed through it as a dark tab beside the spine — a colour-looking
  defect with a geometric cause.

  **(b) A rounded polygon's corner is trimmed by `r / tan(theta/2)`, not by `r`.**
  Trimming by the radius and then drawing an arc of that radius is tangent only at
  90 degrees. On this projection's 154-degree corners the trim points land 84.6
  apart for a radius of 43.4 — nearly a full diameter — so each "corner" rendered
  as a **protruding half-disc** on the silhouette. Two of them, at 512px, on an
  otherwise finished tile. Clamp the tangent length to 0.46 of each edge and
  recompute the radius from it, and pass a zero-radius corner straight through.
  Related: **a hull written down by hand is often not convex.** The first hexagon
  used the base's far corner and the top's near corner, which put two reflex
  vertices in a polygon rounded as though convex; check the turn signs before
  rounding anything, since the spikes are the only symptom.

  **(c) Thickness, not material, is what separates a book from a mortarboard.** At
  `BOOK_T` 98 on a 452x436 plan the tile read as a graduation cap with the ribbon
  for a tassel, and two rounds of shading, blooms and rim work moved it not at all.
  At 152 it is a ledger. *Generalise:* sweep the dimension the object's identity
  rests on at 512px before authoring any material, and look at the silhouette while
  you do — this is `better-loop`'s step-height sweep applied to a solid's depth.

  **(d) A pale band under a dark lid is an open laptop, and it takes three changes
  together.** The page block first read as light spilling out from under a raised
  cover. Darkening it to the reference's *measured* value (a warm tan at Y 0.397,
  hue 33, sat 0.31 — not the ivory that "pages" suggests), recessing it 22px behind
  the boards so they visibly overhang, and bowing its outer profile inward with one
  quadratic (a real fore-edge is concave) fixed it. Each alone left the laptop read
  intact. The corollary is `design-craft`'s pale-element rule from the other side:
  when a mid-tone band must sit inside a dark body, its own boundary is the body's,
  and its ground-relation is a liability to publish (1.97:1 here) rather than a
  number to fix by lightening anything.

  **(e) An accent lying directly on porcelain has its luminance set by rubric #7,
  and the raster already knows the number.** At Y 0.205 the ribbon measured
  **2.87:1** against this ground by the dilated ring and failed; at Y 0.185 falling
  to 0.135 its median is 0.152 and it measures **3.58:1** by a clean patch pair.
  The Engine C raster's own ribbon sits at Y 0.132-0.138 on its lit faces. What
  keeps a deep accent from reading brown is not its hue but its **HSL lightness
  against the family** — 0.44 here, the marketplace's shared value, with the
  subject's own hue point at 16 degrees — and that is only visible on a shelf strip.
  This is `mac-craft`'s finding (e) with the numbers attached, and the two
  constraints (deep enough for 3:1, light enough not to be brown) leave a window
  roughly 0.14 to 0.19 wide in Y on this ground.

  **(f) A dome bloom buys the material read and costs figure-ground; quote both.**
  `apple-23`'s soft top bloom, hung at the key's own bearing rather than the face
  centre and clipped to the face, at 0.085 peak: the cover's median Y went
  0.038 -> 0.049, its ring figure-ground 8.90 -> 7.88:1, and 16px contrast
  0.2238 -> 0.2178. Worth it — the cover stops reading as flat paint — but it is a
  trade against the one number rubric #7 is about, so publish the pair rather than
  the improvement alone.

  **Device findings, from three-value mocks at 512px before any material existed.**
  A latching hook is a **power button**. A baton with a collar is a **cigarette**,
  and its rubric numbers came back the best on the sheet while its picture was the
  worst — accent 4.40:1, dark mass 10.07:1, and nothing legible. A pointed oval
  with a bright core is an **eye**, which `be-my-witness` owns. What collides on
  this shelf is the *silhouette class* rather than the metaphor: a ring is both a
  power symbol and `mac-doctor`'s gauge, and a bar with a warm band is
  `better-loop` in any orientation. Two mocks cost about ten minutes and killed
  three devices.

  **Sheet finding, extending `whats-left`'s.** Its `<colgroup>` fix is necessary
  and not sufficient: a twelve-item rubric walkthrough *inside* a verdict cell
  produced a 1400px-tall row with the seven renders floating in the vertical middle
  of it, and nothing errors. Moving the walkthrough to a section below the table,
  leaving three sentences and the decisive numbers in the cell, and setting
  `vertical-align: top` on the cells, took the shipping take's row from 1400px to
  **329px** with the renders at the top where they are compared.

  **Engine note.** Engine B can refuse for a reason that is neither a timeout nor a
  bad brief: the Arrow gateway returned `A positive credit balance is required for
  all requests, including BYOK` and wrote no file. That is a named unavailability
  to record on the sheet, with Engine A widened to three devices in its place —
  not a skipped step.

- **2026-08 · better-goal "The Held Needle" — an accent's *radial depth* decides
  whether it exists at 16px, a stop needs parallel flanks, and the shelf-collision
  metric cannot be satisfied by resizing.** A machined graphite dial on porcelain,
  with a vermilion accept band cut through the face and out to the rim and a graphite
  pawl standing proud of the bezel.

  **(a) Compute an accent's thickness in *display* pixels before authoring it, not
  its area.** The band was first drawn as a 36px-thick inlay in the bezel, spanning
  58° of arc — a perfectly reasonable-looking 1024px object. At 16px that is
  **0.56px thick**, so the render was a plain dark disc with no accent anywhere and
  the entire device was missing exactly where it has to survive. Nothing at 1024
  hints at this; the tile looks finished. Cutting the band inward to 116px of radial
  depth gives 1.8px at 16px and it reads.
  *Generalise:* for every element the identity depends on, divide its **smallest**
  dimension by 64 and ask whether the answer is over 1.5px. Arc length is free;
  radial depth is what is scarce. An accent that is long and thin dies before an
  accent that is short and fat, at equal area.

  **(b) A radial sector reads as a ribbon tab; a constant-width bar reads as
  hardware.** The stop was authored three ways. As a vermilion annular sector at the
  band's end it fanned outward and read as a folded bookmark at every size. As a
  54px-wide, 32px-proud constant-width bar in graphite it read as a stick poking out
  of the dial. What works is **two parts through the rim on one gradient axis**: a
  46px wall inside the face that caps the band, and a 96px × 22px boss on the rim
  that stands proud. Short-and-wide reads as cast into the body; long-and-narrow
  reads as bolted on. `_bar(deg, r0, r1, half)` — parallel flanks from a centre
  angle — is the primitive; `sector()` is the wrong one for any machined part.

  **(c) Put the mechanism in graphite and keep the accent for the semantic element.**
  The gate and the accept band are two ideas, and spending the warm hue on both made
  one contiguous warm L that no longer said which was which. Graphite for the pawl
  gives the tile its highest-contrast edge — a dark bar across a warm wedge — at
  precisely the one place the boundary closes, and it keeps the accent at 2.52% of
  the tile in one place.

  **(d) Re-run a body's seat edge AFTER an inset accent, so the accent borrows the
  body's boundary.** A warm gel object squeezed between a Y 0.833 porcelain ground
  and a Y 0.084 graphite body cannot clear 3:1 against both: measured 2.44:1 against
  the tile and 2.71:1 against the face. The corpus does not solve this with a value
  — apple-12's orange operator column is 2.29:1 against its own charcoal body — it
  solves it by **putting the accent inside a dark body**, so the edge the eye uses is
  the body's at 12:1. Drawing the rim's seat-edge stroke a second time over the band
  raises the band's boundary against the tile from 2.44:1 to 3.36:1 and costs one
  path. Do this for any accent that touches the ground directly.

  **(e) A graduation ring that closes is a clock, whatever the material does.** Two
  rounds shipped a full 36-tick ring with a pale needle near vertical, and no palette
  or lighting change moved the read. Opening the scale to a ~190° sweep with a clear
  sector, running from the foot of the travel to where the accent starts, makes it an
  instrument with a **direction** — and one engraved groove at the band's inner
  radius, running the same span, fills the face without adding graduations. This is
  the ux-craft finding again: when two material rounds do not move a read, the fault
  is in the construction.

  **(f) On a dial, light the face as a dome and put the terminator down-light.** An
  inner shadow on the up-light side inside the rim fights the face gradient — the
  gradient says the crown is lightest, the shadow says it is darkest — and two planes
  disagreeing about where the lamp is costs #8. Author the occlusion ring offset
  *toward* the light so what survives the face clip is the far arc. apple-23's dial
  "reads as domed glass with a soft top bloom", which is the construction, and its
  bloom belongs at the key's own bearing (≈0.34, 0.19 in object-bounding-box terms
  for a 118° key) rather than at the centre.

  **(g) One `scale` constant over every radial dimension, because object diameter is
  the lever on shelf collision — and it cannot clear the bar.** Swept 0.84 to 1.00
  (52.3% to 62.5% of tile width) against the worst 16px signature correlation over
  the other 37 icons: 0.871 `proctor` → 0.827 `proctor` → **0.810 `geminify`** →
  0.840 `mockup-fidelity`. There is no setting under 0.80. **Shrinking a dark
  centred object moves the flag from the dark-slab cluster onto the dark-box cluster
  rather than removing it**, and the cost curve is nearly flat in contrast (0.2710 to
  0.2998 RMS). Note the direction against ux-craft, which scaled its object *up* to
  buy contrast: the same knob buys distinctiveness run the other way, and neither
  commission can have both. Publish the curve rather than defending a size.

  **The second lever is the object's *vertical position*, and it is the one that
  cleared the bar** — worst pair 0.830 at `cy` 526, 0.810 at 498, 0.800 at 478,
  0.797 at 470, 0.795 at 466, for 0.0006 of contrast across the whole range. A 42px
  lift on a 1024 canvas is inside what a cast shadow's own reach below the object
  accounts for, so the composition reads no higher; check it side by side at 384px
  before taking it. Sweep *position* before concluding a collision is structural, and
  sweep both before adding a `DECIDED` entry: this commission needed neither in the
  end, and the whole 703-pair set came back green.

  **(h) Two out-of-family engines agreeing on one construction is the cheapest
  evidence this pipeline produces — and their shared mistake is evidence too.** Both
  Arrow vector takes and the GPT-Image raster drew the bezel as a **complete pale
  annulus**; the master had that catch on the lit arc only, so its rim read as a
  highlight rather than as a turned part. A full-circle hairline at a sixth of the
  lit arc's opacity was the whole fix. All three engine takes *also* put the accent
  band inside the graduation ring as a floating arc, which is the construction that
  dies at 16px — so the engines independently confirmed both the material to add and
  the placement to avoid.

  **(i) A vector engine can invert your meaning while satisfying every visual
  instruction, and a raster brief cannot fix it.** Handed "a band the reading has to
  be inside, with a stop at one end", both Arrow calls produced a **tachometer
  redline** — a ceiling not to be exceeded, needle pressed against it from below.
  Every colour, radius and count was honoured; the semantics were reversed. A goal is
  a floor you reach and hold and a redline is a limit you stay under, and nothing in
  a style brief distinguishes them. When an engine take's *reading* is wrong rather
  than its material, salvage the material and drop the composition — there is nothing
  to converge on.

  **(j) Check the output directory before believing a reported timeout.** One
  `generate_image` call returned a timeout error to its caller and wrote its SVG to
  disk regardless; the file was found afterwards and scored as a sixth take. Treating
  the error as "the engine is unavailable" would have cost an engine from the floor
  and lost the finding in (i), which came from exactly that take.

  **(i) A losing take can be the measurement that settles the brief.** The
  alternative value relation — a graphite bezel ring around a *porcelain* face — was
  built rather than argued about, and its face measures **1.00:1 against the tile**:
  the predecessor's exact defect, preserved inside a new ring. The third take, a
  disc half-sunk in a graphite housing, posted the sheet's *highest* 16px RMS
  (0.3216) while reading as a lump, because it bought the contrast with 52.8% of the
  tile in dark mass against the winner's 24.0%. **A high whole-image contrast number
  earned by dark area is not the same as figure-ground**, and only the object-versus-
  ground ratio separates them.

- **2026-08 · ux-craft "The Spacing Circle" — a plan-view circle cannot be an
  object, a shelf strip is the only place a device collision exists, and an
  anisotropic region needs an anisotropic gradient.** Two reach envelopes as low
  pucks of gel on porcelain, crossing, with the accent existing only in the
  crossing.

  **(a) A plan-view circle with a radial gradient is a ball bearing, whatever you
  name the layer.** Two hand-authored rounds drew each reach zone as a circle
  filled with a focal-offset radial: at 1024 they read as two spheres with a leaf
  stuck between them, and the second round — narrowing the value range, killing
  the sheen, containing the lens light — improved the surface without touching the
  problem. The construction that reads as an object standing on a bench is a
  **foreshortened ellipse with a visible edge band**: `ry = r × 0.66`, the same
  outline dropped by a thickness of ~0.11 r to expose a band, the band a step
  darker than the face, a porcelain bounce stroked along the band's far arc, and
  two cast shadows (one tight at 0.30, one wide at 0.17) offset along the light
  axis from the band's base rather than the face's centre.
  *Generalise:* a region drawn in plan is a diagram; the same region drawn with a
  thickness is an object. If two material rounds do not move a read, the fault is
  in the construction and no parameter will find it.

  **(b) One user-space ramp across BOTH objects, not one radial per object.** With
  a radial per puck each one became its own little sun, which is most of the
  sphere read. A single `userSpaceOnUse` linear gradient spanning the whole union
  along the key axis, with the edge bands on a second ramp of the same axis a step
  darker, makes two objects read as two objects under one light. This is the
  mac-doctor/anvil "one key, one axis" rule applied across a *pair* rather than
  across the faces of one solid.

  **(c) A device collision exists only on the shelf strip, and a referred panel
  cannot see it.** The first framing here — two overlapping shapes with a lit seam
  — was measured, mocked and defensible in isolation, and rendered at 96px between
  its siblings it sat exactly between `geminify` (two overlapping capsules, warm
  blend) and `should-compact` (two dark slabs, vermilion seam). Two out-of-family
  lanes given the full taken-devices list as text did not catch it; the pixels did,
  in one second. The rescue was material rather than conceptual — pucks with bands
  and contact shadows are not in either neighbourhood, because neither sibling
  renders an object standing on the tile. *Generalise:* build the shelf strip
  before committing a device, and again after the material lands.

  **(d) A radial gradient on an anisotropic region has to carry the anisotropy
  explicitly.** The crossing of two circles is a vesica at roughly 1:2.4. Sizing
  its core gradient from the region's half-*width* (with a vertical stretch to
  compensate) put the falloff's dark stop well inside the lens, so the accent
  rendered as a half-sized blob clipped by an invisible edge and every hex was
  still correct. Size it from the half-*height* and squeeze x by
  `half_w / half_h` in the `gradientTransform`. Compute both from the circle
  intersection rather than measuring the render.

  **(e) Foreshortening costs contrast, and the currency is footprint.** Flattening
  the pucks took 16px RMS from 0.282 to 0.236 because the dark mass fell from 30%
  of the tile to 17%. A swept scale-up gave 0.244 at 67% tile width and 0.255 at
  73%; the second crowds the safe zone. Sweep the object's scale and publish the
  curve rather than defending a size — the grammar's 55-65% focal width assumes a
  compact object, and a deliberately flat one buys its legibility with width.

  **(f) An accent that is a relationship rather than a mark measures weak and
  reads fine — check it in grayscale, not in the ring.** Dilated-ring: the gel
  pucks read 6.45:1 against their surround while the crossing read only 1.45:1
  against the gel it sits in, because a light trapped in doubled gel has a
  near-black boundary by construction. The grayscale render settles it: the
  crossing survives as a visibly lighter lens, so #7 holds, but part of the
  signature is hue and #10 is an honest fail rather than a formality. Render
  grayscale before claiming a hue-carried accent is value-carried.

- **2026-08 · whats-left "The Open Crown" — the void is part of the silhouette,
  and three mocks died proving it.** A gateway with its keystone lifted out of
  the crown. Every finding here is about NEGATIVE space, which no material work
  can reach and no metric in this skill measures.

  **(a) A tapered void rising out of a round-topped opening is a bottle, and the
  material cannot save it.** Three three-value mocks failed in a row, each read
  in one second at 128px: a half-round voussoir ring severed at the crown is a
  perfume bottle with its stopper above it; flattening the arc to a segmental
  span is a squatter bottle; cutting the taper from 13 degrees to 5 is a bottle
  with a straighter neck. The defect is topological rather than geometric — the
  missing piece's socket connects to the opening below it, so the two voids read
  as ONE shape, and that shape is a body with a neck. Two fixes together, and
  both were needed: make the outer silhouette a RECTANGULAR block with the arch
  cut into it (a curved outer contour over vertical sides is a bottle's shoulder
  whatever fills it), and paint the socket as a solid recess so the porcelain
  shows through the opening only.
  *Generalise:* when a device is defined by a piece being absent, draw the void
  as a filled shape and squint at THAT. The object's own outline is not where the
  failure is.

  **(b) A recess whose only visible surface is one side wall reads as a loose
  stone standing in the hole.** With the camera above-right and the key
  upper-left, the socket's single visible face is its left wall, which turns away
  from the key, so it rendered as a dark tilted slab against the porcelain above
  the block's top edge — indistinguishable from a separate object. Cutting the
  socket as a STOPPED housing (`SOCKET_K = 0.62` of the block's depth) adds a
  back wall parallel to the near face, which is a plane the key can land on:
  measured, back wall 0.167 and side wall 0.130 against a front face of 0.256, so
  the recess sits below the face rather than beside it. It is a deliberate
  fiction — a real missing keystone leaves a full-depth cut — and it is the
  docked rubric check, paid knowingly for the silhouette.
  *Generalise:* a recess needs at least two faces at different values to read as
  depth. If the projection gives you only one, change the recess, not the light.

  **(c) A masonry joint is two strokes, and the pale one is what makes stones.**
  Incised single dark lines around the arch ring read as ink drawn on one slab.
  The raster take's advantage was that its courses were separate blocks, and the
  cheap version of that is a 3.4px dark groove plus a 2.2px pale lip offset 3.1px
  along `-LIGHT` (the key side) at 0.34 opacity. Same paths, same geometry, and
  the ring stops being a decal. This is mac-craft's valley rule at a scale where a
  full three-stop cross-section will not fit.

  **(d) A dark mass is how the porcelain register clears rubric #7, and it is
  worth the whole commission.** The predecessor measured 0.075 16px contrast on
  the family measure (n=36, median 0.196) and spent its accent on a 0.5% dot. The
  rebuild measures 0.275 with figure-ground 3.13:1 by the dilated-ring method,
  against 1.75:1 and 1.98:1 for the two diffusion takes of the same object —
  which is mac-craft's measured ceiling for this register showing up again, from
  the other side. The raster is the material target and never the contrast target.

  **(e) Three engines briefed once all drew the same object, and that is a
  reading of the DEVICE, not of the engines.** Both GPT Image takes and the Arrow
  take independently produced a gateway with a socket in its crown and the wedge
  above it. When the takes converge on the composition, the metaphor needs no
  explaining; when they diverge (ship-fleet's quay, where the raster reproduced
  the draft's letter-E), the convergence is the warning instead. Either way it is
  free evidence available before any material work starts.

  **(f) Sheet finding: a long verdict column collapses the contact sheet.** With
  the template's `min-width: 860px` and four prose verdicts, the browser gave the
  verdict cell 165px and every row grew to 1078px tall, with the renders floating
  in the vertical middle of a mostly-empty cell. Nothing errors and `check`
  passes. A `<colgroup>` of 212 / 700 / 74 / 378 and `min-width: 1360px` puts the
  rows back at 427px; `.sheet`'s own `overflow-x` absorbs the extra width, so the
  page body still does not scroll.

- **2026-08 · proctor "The Side Port" — a cylinder is one path with a derived
  gradient, an oblique box's silhouette is a convex hexagon, and a coaxial
  barrel is a camera.** Six findings from rebuilding a line-art window outline
  as a graphite casting with an ember hex fitting. Four are construction rules
  that no palette work could have repaired, one is a device-level misread caught
  only by looking, and the last is about the metric rather than the material.

  **Shade a cylinder with ONE path and a Lambert-derived multi-stop gradient;
  never tile its surface into bands.** The first draft cut each cylinder into 28
  flat quads, one per angular band, each carrying its own Lambert value — the
  physically correct construction, and `rsvg-convert` antialiased every seam into
  a thin light line, so the quill rendered as corrugated hose. The fix: sample
  the visible arc at ~22 angles, take each angle's Lambert term as its stop
  colour and its projected offset as its stop position, and hang the gradient on
  an axis measured **perpendicular to the tube's own screen axis** so the
  iso-lines run along the tube rather than skewing across it. One path, one
  gradient, no seams, and the values are still derived rather than eyeballed.

  **A cylinder's outline is the convex hull of both cap ellipses, not the swept
  front-facing band.** The band (arc at u0, then arc at u1 reversed) leaves the
  back of every cross-section unpainted, so whatever sits behind shows through as
  a stray ellipse — on a four-piece stepped assembly that produced two ghost
  ellipses nobody could place. Paint the hull; cap it separately.

  **A cylinder takes no falloff along its own axis.** Its normal has no component
  along that axis, so the Lambert term is constant there and any ramp along it is
  invented light. Worse, the "one shared falloff" that seemed like layer
  discipline was laid over a convex hull of the whole assembly, and a hull bridges
  every concavity — so a dark wash at 0.34 opacity sat over the porcelain in the
  waist between two pieces and read as a grey smear on the ground.

  **A box in this projection has a convex HEXAGONAL silhouette, so one rounded
  hexagon as a clipPath gives the whole casting a radius.** Vertices:
  top-front-left, top-back-left, top-back-right, bottom-back-right,
  bottom-front-right, bottom-front-left. This is the cheapest route to the Tahoe
  "poured, not drawn" radius on a hard-edged oblique box, and it was the loudest
  material difference between the raster takes and the master. Rounding each
  visible face separately does **not** work: the faces then pull apart at the
  corners and show ground through, and an underlay to fill those gaps has to be
  un-rounded, which puts the square corners straight back on the silhouette.

  **A sub-part takes its values from its own normals, not from its own palette.**
  A base plinth authored with its own darker set (top 0.28, front 0.104) read as a
  separate flat tray sitting under the casting. Given the body's values for the
  identical normals it read as one casting — and then it was dropped anyway,
  because the step carried no meaning and the seat shadow does the standing. Two
  lessons: match values across a shared normal, and a detail that survives only
  because it was authored is a detail to delete.

  **A graphite box with a coaxial round barrel on its face is a camera.** No
  amount of material work fixed it; three drafts read as a camcorder, which in
  this family is the worst available misread, since `design-review` owns the
  reticle and `be-my-witness` owns the lens. Two changes fixed it together: a
  **hex** union nut instead of a barrel, and a **portrait** case instead of a
  landscape one, with the fitting **low** on the flank rather than centred on it.
  The hex pays for itself twice — its three visible flats take three separate
  Lambert values (0.80 / 0.77 / 0.03 against the one key), which is more per-face
  separation than a smooth barrel of the same size can carry. Sanity-check any
  box-plus-protrusion device against "what appliance is this" before authoring
  material for it.

  **The 16px number rewards mass and is blind to whether the accent survived.**
  The family metric is the luminance standard deviation of the 16px downsample
  composited over white; the median across all 36 marketplace icons is 0.176,
  this commission's predecessor measured 0.102 and the shipped master 0.276. Both
  Engine C rasters measured **higher** than the master (0.308 and 0.320) while
  their accent was a single pixel at 16px and their figure-ground was 2.4:1,
  under rubric 7's floor. A large mid-value mass on a plain ground maximises the
  statistic; it does not make the tile say anything. Quote the number, then look
  at the ×6 magnification before believing it.

  **Negative result on Engine C steering.** Four same-register corpus references
  transferred the material and the ground treatment faithfully and transferred
  **emphasis** not at all: both rasters shrank the fitting the prompt named as
  the hero into a cable-gland-sized detail. Reference images steer how a thing is
  rendered, not what the picture is about.


- **2026-08 · design-craft "The Sample Fan" — translucency has a paint-order
  prerequisite, and one rotated body can be lit without per-edge geometry.** Five
  findings from a three-leaf fan of material samples on a porcelain cushion, four
  of them construction rules that no palette work could have repaired.

  **Anything that belongs to a back surface is painted before the front body, or
  masked subtractively.** The same defect arrived three times in one commission
  with every hex correct: the rejects' rim and seat strokes, run as one pass after
  all three bodies, painted their bright edges across the leaf standing in front
  of them; the front leaf's ambient occlusion, clipped to the leaf behind and
  emitted after its own face, filled the entire overlap region and read as a hard
  diagonal cut across the face; and the warm bounce in `#highlight` did it again
  more faintly, because the layer plan puts highlights above everything. This
  generalises anvil-errand's stray-catch entry into a rule with two remedies:
  emit a back-surface effect *before* the occluder's body, or mask it with
  `<mask>` carrying the occluder in black. A stray light leak is a paint-order
  bug, and it presents as a colour bug.

  **The thickness copy blocks the transmission it sits under.** A slab's side face
  is usually an offset copy of the body drawn behind it, which is invisible on an
  opaque object and fatal on a translucent one: an 11px offset covers ~95% of the
  body, so a frosted leaf at `fill-opacity 0.72` composited over its own opaque
  side face instead of over the dark leaf behind it. Its translucency was declared
  and not visible, and no measurement of the palette could see it. Mask the side
  face to the sliver that actually protrudes (`<mask>`: white tile, body in black)
  and the object behind reads through — which then became the tile's strongest
  material tell, the Photos-petal move at full amplitude.

  **A rim light can be one stroke whose opacity dies along the shared light
  axis.** On a body rotated to an arbitrary angle, authoring per-edge catch arcs
  means solving which edges the key reaches. Stroking the whole outline with a
  `userSpaceOnUse` gradient hung on the light axis — 0.85-0.95 alpha at the lit
  end, 0.18 at 0.42, zero at the shaded end — lights the correct edges for free
  and stays correct when the angle changes. Cheap, steady across renderers, and it
  survives being re-parameterised.

  **Rotate the geometry, not the group, when several bodies must share one light.**
  A `userSpaceOnUse` gradient referenced inside a `rotate()` group rotates with
  it, so three rotated leaves each get their own light direction and read as three
  objects under three lights. Emitting each body already rotated (circular arcs
  are rotation-invariant, so only the endpoints move) lets every face hang on one
  tile-space axis while each object keeps its own lit-to-shaded ramp.

  **A negative corner radius renders as a straight chord, without erroring.** Cut
  the specular and the occlusion copies with a `grow` parameter and the corner
  radius goes negative before the width does; `rsvg-convert` drew a hard diagonal
  across the finished face and reported nothing. Clamp every radius a grow
  parameter can reach: `max(4, min(r + grow, half_width, 0.45 * length))`.

  **Finished versus unfinished as a material distinction.** Where a composition
  has to say "several candidates, one committed", the cheapest legible device is
  not colour but completeness: give every body its gradient, seat edge, rim and
  cast shadow so all of them are real objects, and give only the chosen one a
  specular and a bloom. It reads at 128px as gloss and at 32px as one object being
  brighter, and it costs two paths.

  **The white-frost trap, confirmed a third time.** The raster engine again
  rendered the pale sample as a true white on a near-white ground at ~1.05:1; it
  dissolved by 32px. The shipped master's pale leaf is a warm off-white
  (`#FCF7EB`→`#CEBF9C`) with a real seat edge because of it — and it still
  measures only 1.13:1 against the cushion by the dilated-ring method, surviving
  small sizes by being flanked by two darker bodies rather than by separating from
  the ground. When a composition needs a pale element, plan for its neighbours to
  carry it and say so in the liabilities.

- **2026-08 · better-loop "The Stepped Rail" — a pale object on a pale ground is
  not there, and four ways a follower stops being hardware.** Confirmed on the
  commission that replaced a duplicate of its own sibling's dial; every entry
  below was found on a render rather than reasoned about.

  **Value first, material second: a porcelain object on a porcelain ground runs
  about 1.15:1, so it is not present.** The follower was authored porcelain for
  two rounds on the reasoning that the watcher should be the same material as the
  daylight it sits in. The part of it standing above the dark rail simply was not
  visible, and no amount of sheen, edge catch or top-face work moved it, because
  the problem is the value relationship and not the material. Re-authored in
  machined steel — one value band above the rail, well below the cushion — it
  reads against both at 3.08:1 and 2.92:1. `deck-craft` recorded the same
  relationship as a liability (three porcelain plates at 1.18:1 against its
  cushion); this is the same finding as a build rule. **Pick each object's value
  band against every neighbour it touches before choosing its material.**

  **A pale shape interlocking with a dark band resolves to a belt buckle.** A yoke
  the rail passes through, open on its up-light side, is a clean piece of
  engineering and an unreadable icon: pale jaws with a dark bar threaded through
  them is a figure-ground ambiguity, and the reading it settles on is a clasp. A
  saddle that grips one surface and breaks the silhouette in one direction only
  cannot go wrong the same way.

  **Two dark circles on a pale body are a face, at every size.** Roller pins at
  0.26 and 0.74 of the follower's width read as eyes from 512px down to 32px. Any
  paired feature at roughly a third and two thirds of a body's width will do this;
  a single continuous sole or bearing line carries the same "this is mounted" cue
  with no anthropomorphic read.

  **Three correct overlays on one small part make one dirty stripe.** A shadowed
  lip, a graphite bearing pad and a 42px warm spill at 0.22 alpha were each
  defensible alone and together browned the middle of the part, with every hex
  still measuring correct. Where an accent is 70px or more away from a part, what
  reaches it is an **edge kiss** — 18px at 0.16 — and not a wash. This is
  `anvil-errand`'s muddy-bounce finding at the scale of a single component.

  **A warm bounce onto cool graphite has to be in the pale spill hue, not the
  accent's.** At `ACCENT_HI` over a `#7A828E` tread the bounce reads as rust; at
  the accent's cream rim value (`#F6D3AC`, sampled as apple-05's lightest accent
  pixel) at 0.52 over a 66px run it reads as light. Corollary worth keeping: a
  bounce confined to a **clip path of the receiving surface** cannot spill onto the
  face below it, which is what turned a first attempt into a horizontal brown smear
  under the accent.

  **Draw an object's seat edge with its front face, before anything set into it.**
  The rail's `stroke` ran after the vermilion shim, so the step's own vertical edge
  drew a dark seam down the shim's up-light side. At 1024 it is a hairline; at 256
  it is a gap between two pieces that are supposed to be one assembly. Same class
  as the highlight-over-occluder bug: a layer-order defect presenting as a
  material one.

  **A foreshortened top face must stop where an occluder starts, not behind it.**
  The lower tread ran to the shim's far edge, and because a top face is a
  parallelogram its far corner emerged past the shim as a grey tab — which reads
  as a chipped step. Behind an occluder there is no visible surface; end the face
  at the occluder's near edge.

  **Sweep the one dimension the icon is about, at 32px, before polishing
  anything.** The step's height was swept at 178 / 212 / 240 on a 1024 canvas.
  Under about 190 the two runs merge into one thick band with a notch and the
  subject is gone; over about 230 they read as two separate bars. A 200px rise on
  a 124px section is the window, and it is roughly 3px of separation at 16px — the
  useful general form is that **a feature needs about 3px at the smallest target
  size, so about 190px on a 1024 canvas for a 16px target.**

  **Both raster takes drew the follower as a clip wrapped over the rail rather
  than a block cut flat**, and that is the salvage: a generous top radius plus one
  arc catch across the crown reads as machined where a boxy block reads as a tray.

  **Metric definition, not material.** The family's 16px contrast figure is RMS of
  **gamma-encoded** relative luminance on a 16px downsample, alpha-masked.
  Linearising first moves this commission from 0.2331 to 0.2840 and the 36-icon
  family median from 0.1805 to 0.2380 — same ranking, incomparable numbers.
  `deck-craft`'s recorded 0.174 reproduces only under the gamma-encoded form, so
  quote the definition with the number.

  **A gate the library does not have.** The predecessor scored 8/12 and still had
  to be thrown away, because it was `better-goal`'s dial with a different tick
  pattern. The 12-point rubric has no check for whether an icon differs from its
  siblings, and in a marketplace where one pipeline generates the whole family that
  is the failure mode most likely to ship. The cheap mechanical version is a
  nearest-neighbour distance on the 32px renders of the existing set, run before
  the direction is settled rather than after the master is built.

- **2026-08 · anvil-errand "The Struck Billet" — a profile silhouette cannot
  carry material, and three lighting bugs that all look like colour bugs.**
  Confirmed during the porcelain re-ground; recorded here because that
  commission's scope was its own plugin.

  **A profile silhouette cannot carry material. Extrude it.** The predecessor
  measured 77.3% locally uniform and no amount of gradient work moved it,
  because a profile has one visible face and one face can carry one gradient.
  Rebuilt as a solid, the measured profile extruded along one oblique axis with
  the horn tapering to a cone, every visible face valued by a single Lambert
  term against one key: 62.4% uniform, and 16px contrast 0.160 to 0.258. Hang
  every face gradient on one shared user-space axis so the faces read as one
  object under one light rather than as adjacent panels.

  **A recess's walls are not lit bands.** Authoring the arch's edge-on wall as
  its own shape rendered a 10px dark parallelogram lying along the arch's
  boundary, which reads as a scribe mark on the casting rather than as depth.
  Fill the recess with the shadow it casts and skip its walls entirely.

  **A warm bounce on cool graphite goes muddy long before it goes warm.** The
  porcelain bounce onto a dark body's lower edge has to be tight, brighter than
  seems right, and in the paler spill hue rather than the accent's own. Widen or
  dim it and the flank turns to mud with every hex still correct.

  **A highlight in `#highlight` paints over an occluder in `#fg`.** The tool's
  rim catch ran straight across the hot billet as a pale scratch, because the
  layer plan puts highlights above everything. Clip the highlight subtractively
  against whatever stands in front of it. This is a layer-order bug that
  presents as a stray light leak.

  Sibling separation worth keeping: this graphite is deliberately cooler than
  `improve-skill`'s warm charcoal whetstone, the one sibling close enough to
  collide in the metalworking register.

  **Template finding, not a material one.** `display:flex` on a `<td>` in
  `icon-audit-template.html` computes as flex in the scoring browser and still
  lays its children out as blocks, stacking all seven renders into a column, so
  the sheet reads as one tall strip per take and nothing errors. `deck-craft`'s
  commission hit the same thing independently. The flex now lives on an inner
  div. `white-space: nowrap` on `.take` also took that column to 519px and
  squeezed the verdict into a 124px ribbon.

- **2026-08 · mac-craft "The Registered Line" — a cut is a valley, a tool's
  registration edge is chosen by where its tail goes, and a family accent has a
  luminance.** Five findings, three of them silhouette properties that no amount
  of gradient work could have repaired.

  **(a) A groove is a valley cross-section; a monotonic ramp across its width is
  a lit slope.** Three consecutive rounds drew the scribed cut as [dark flank |
  bright band | light lip] and all three read as a *raised bar with a drop
  shadow* — at 48px, as an orange pencil lying on the frame. The construction is
  wrong in principle: a dark edge on one side and a light edge on the other is
  the signature of a **convex** form lit from the light side. A valley is dark at
  BOTH edges with its bright zone off-centre toward the key. It needs a second
  layer, because it is a second axis: the band's *length* ramp rides the shared
  key axis, and a separate `userSpaceOnUse` gradient spanning exactly the band's
  *width* carries the cross-section — stops `0/0.74 → 0.15/0.22 → 0.52/0 →
  0.88/0.16 → 1/0.46` of a deep accent, over the accent fill. Asymmetric, so the
  lit flank keeps less shadow than the shadowed one.
  *Generalise:* a cut is defined by both its edges being darker than its middle.
  One dark edge and one light edge is a solid, whatever you name the layers.

  **(b) Register a tool on the edge whose TAIL has somewhere to go.** The first
  draft put the marking gauge on the sash's top rail. Anatomically correct — and
  visually fatal, because a gauge's beam is perpendicular to the reference edge
  with its tail behind the stock, and on a near-plan projection that direction is
  straight up out of the tile. Truncating the tail to fit turned it into a lug and
  the tool read as a separate object stuck on the frame. Re-registering on the
  *left stile* points the tail horizontally, where the tile has width and the mask
  can cut it as a boundary (device #18) rather than clipping it as an accident.
  *Generalise:* pick the registration edge from the tail's exit direction, not
  from which face of the work reads best.

  **(c) A tool whose stock sits mid-beam is a plus sign.** With an 82-unit tail
  and a 62-unit working length, the stock landed in the middle of the visible beam
  and the whole assembly read as **+** — a UI affordance, not a tool. Push the
  stock to one end (long tail one side, short working length the other) and it
  reads as a T. Pure silhouette; invisible in every measurement, obvious in the
  first second of looking.

  **(d) The porcelain register has a figure-ground ceiling, and the ground truth
  is sitting on it.** Measured with the dilated-ring method: `apple-18`'s own
  object median against its ground is **1.92:1**, and the two raster takes for
  this commission came in at **1.27:1** and **1.40:1**. Rubric #7's 3:1 is
  reachable in this register only on the *darkest defining mass*, never on the
  object's median — a mid-tone object on near-white cannot get there without
  either a near-black object or abandoning the register. So budget the tiers
  explicitly: focal at ≥3:1 (here the tool, 3.36:1), the object's flanks ≥2.3:1
  (2.35:1), and record the mid-tone face's shortfall (1.76:1) as a **fail** in
  the audit rather than lightening the ground or blackening the object to hide it.

  **(e) A family accent has a LUMINANCE, and matching only its hue family reads
  as a different colour.** The cut was authored at the raster's measured hue
  (H 17–20°, S 0.84–0.91) and at L 0.30 — and on a 96px shelf strip beside four
  siblings whose shared `#E9562A` sits at L 0.447, it read brown. Nothing inside
  the tile said anything was wrong; the tile's own measurements all passed. The
  fix was to match the siblings' luminance exactly while keeping the subject's own
  hue point (`#DE5A1E`, H 19, against their shared H 12), which is also what stops
  a sixth sibling looking like a fifth copy.
  *Generalise:* joining an existing icon family, take the accent's **luminance
  from the family** and its **hue from the subject** — and read it on a shelf
  strip, because that comparison is the only place the error exists.

- **2026-08 · generate-investor-portal "The Strongroom, Open" — a lit interior
  behind a dark object, and four ways a shared light model lies to you.**

  **(a) A dilated-ring figure-ground measure reports an object against ITSELF
  when the object carries its own lit face.** The mac-doctor entry's rule (f)
  replaced hand-placed samples with a 45px `MaxFilter` ring, and this fixture
  found the ring's own failure mode: the door slab measured **1.07:1** against
  its surround, which would have been a hard #7 fail on the object the whole
  device rests on. The ring had swallowed the door's own warm-lit leading edge
  and the lit zone beyond it, so the measure was comparing the object to its
  brightest part. Clean patches on either side of the boundary that actually
  matters returned **2.2–2.5:1** (door face 0.079–0.094 against an unlit back
  wall at 0.008), with the whole opening at 6.75:1 against the porcelain.
  *Generalise:* box out the object's own lit faces before believing a ring
  number, and run both measures — a ring and a patch pair — because their
  disagreement localises the defect. Neither alone is trustworthy on an object
  that is also a light-catching surface.

  **(b) A recess's inner faces are lit OPPOSITE to the rim lights of an object
  standing in front of it, and the sign is computable rather than guessable.**
  Illumination is `-dot(N, L)`: with the family key travelling down-right, a
  recess's LEFT inner jamb (normal +x) is a back face and goes to shadow while
  the RIGHT one is lit, and the soffit is dark while the sill is bright. The
  first draft copied the object's own pattern — bright on the left, because that
  is where the key is — and the opening read as a beige picture frame stuck onto
  the tile rather than as a cut into it. Fixing the sign also makes the two light
  sources agree, since an interior emitter on the right lights the same jamb the
  key does. *Generalise:* for a recess, compute each face's sign from the one
  light vector; do not transfer the lighting of the objects around it.

  **(c) A small feature hung on the scene's shared key axis can land at that
  ramp's dark end and vanish.** The handwheel and the lower dogging bolt were
  authored with the shared graphite `userSpaceOnUse` gradient, per "one key, one
  axis". At their positions on that axis the ramp's *lit* stop is a mid grey, so
  against a dark door face the wheel read as a ghost and the bolt rendered as a
  crescent of its own offset shadow with no body at all. Both recovered with two
  dedicated values each — a lit value that is not on the shared ramp, plus a dark
  under-shadow. *Generalise:* the shared axis governs **faces**, not hardware. A
  stud, a boss or a wheel sitting ON a shaded plane is lit by the same key but
  measured against a different local ground, so it needs its own pair.

  **(d) The porcelain bounce onto a dark body's lower edge is in the corpus, and
  it is what stops a shaded flank reading as a hole.** Sampled off `apple-12`
  (Calculator): the dark body's bottom edge reads **V 0.318** against its own
  middle at **V 0.133** — the tile throws light back up into it. Authoring that
  as a bottom-anchored porcelain gradient at 0.20 falling to 0 over ~190px, over
  the body's own ramp, is one path. Without it the flank goes to near-black and
  the object stops being a face; with it the same geometry reads as satin.

  **(e) The composition trap here was that a dark mass buys the contrast and the
  accent buys none — and six sketches died proving it.** Rendered as three-value
  mocks at 1024/128/32/16 before any material was authored, the failures were
  each a *recognition* error no metric names: a pale bar across an ember disc is
  a **no-entry road sign**; a dark object with a pale inner panel is an
  **appliance or a screen**; a dark plate with one cut corner is a **file**; a
  lone warm dot on a dark mass is a **notification badge**. What survived was a
  large dark mass on porcelain with the accent spent as *interior light* — 16px
  luminance contrast **0.050 → 0.266** against a family median of 0.175, and the
  accent at 4.5% of the tile as a saturated core. *Generalise:* draw the
  three-value mock and look at it at 16px before authoring anything; the accent
  is where the meaning goes, and the dark mass is where the legibility comes
  from. Making the accent bigger buys nothing and costs the register.

- **2026-08 · ship-fleet harbour — a wake is a fan, a bollard is a moulding, and
  a quay bar with equal teeth is a letter.**

  **(a) A trailing wake is a DIVERGING FAN of fine foam streaks over a shallow
  trough, not one tapered band.** The first draft drew the wake as a single
  tapered translucent polygon with a foam line down each edge; at every size it
  read as a smear on the water rather than as a vessel moving. The raster take
  that won the material judgment draws five fine streaks whose lateral offset
  grows astern — `spread = 9 + 30·t^0.8` off the centreline, opacity falling as
  `(1−t)^1.25`, outer streaks starting two samples further aft than the inner
  ones — laid over one broad `feGaussianBlur`-softened trough of displaced water
  at 24% dark-warm. Rebuilding it that way is most of what makes a plan-view hull
  read as *under way* rather than *placed*, and it costs five polylines.
  *Generalise:* motion in plan view is carried by the divergence of the trail,
  not by its length or its opacity.

  **(b) Two concentric circles is a decal; a moulding needs four elements.** Flat
  bollards drawn as a dark disc plus a lighter disc read as paint applied to the
  pier surface — a plane error the eye catches instantly and no gradient work on
  the pier itself can repair. The construction that reads as an object standing
  proud: a blurred cast-shadow ellipse offset toward the light's far side, a
  rounded-rect body in the scene's key-axis ramp, a cap ellipse a step lighter
  than the body, and a small offset catch at ~0.55 white. Four elements, ~15px
  tall on a 1024 canvas, and they carry the toy-scale render more than the
  slab gradients do.

  **(c) The composition trap, which no metric will ever name for you.** A quay
  drawn as a *bar* spanning the tile with four equal piers off it **is a letter
  E**. It was the first draft here, and — independently briefed, with no sight of
  the draft — the raster engine produced the same E. Two fixes, both cheap: draw
  the SHORE rather than the quay, as a filled apron cut by the mask on three
  edges so the harbour reads as larger than the frame (device #18), and stagger
  the pier lengths (0.80 / 0.95 / 1.05 / 1.00 of the longest) so the teeth stop
  being a comb. Neither change appears in a residual; both were obvious in the
  first second of looking at a render.

  **(d) The ground register can be forced by a measurement.** On the family's
  pale vellum plate, the pier stone measured **1.11:1** against the water it sits
  in — the icon's entire signature move with no figure-ground. Deepening the
  basin to a warm sand field (`#A38C61→#6E5A33` at 0.27→0.47 over the plate) took
  stone/water to 1.52:1, berthed craft to 2.07:1 and the focal to 3.10:1. When a
  register choice and a contrast floor conflict, measure both before defending
  either; here "porcelain ground" survived as the stone rather than as the field.

  **(e) A rejected round that changes two things has to be split before you can
  learn anything from it.** r04 bundled a broad water-sheen ellipse with a warm
  re-hue of the clay and gated REJECT at −0.0121. Re-running with only the sheen
  (r05, −0.0114) put the cost on the sheen, not the clay — the tile already
  carried a plate radial, a vignette and the water ramp, and a fourth broad field
  bought nothing at any size. One edit class per round is the rule; one edit
  *within* the class is what makes a rejection informative.

  **(f) Measure a region against its own surround, never against a point you
  chose — a hand-placed sample hid this icon's one real defect for six rounds.**
  Sampling "the focal" and "the ground beside it" by eye returned a comfortable
  **3.10:1** and closed the rubric-#7 question. A dilated-ring measure — every
  pixel of the object's colour mask against a 45px `MaxFilter` dilation of that
  mask, median to median — returned **1.85:1**. The hand sample had landed on the
  hull's shaded side and on a bright patch of basin, and nothing in the loop
  caught it because the composite is a *similarity* score and the reference
  carries the same weakness. The ring measure is six lines of Pillow and numpy and
  it should run on every commission before #7 is scored.

  **(g) A whole-image contrast floor can fire in exactly the wrong direction, and
  the fix is to re-measure at the size it fired on.** Lightening the basin gained
  **+0.0800** of composite, the run's largest move, and `gate` rejected it because
  32px self-contrast fell 0.338 → 0.309. That statistic is a p90−p10 spread the
  tile *ground* dominates, and the edit had moved the ground toward the stone laid
  over it. At the same 32px, on an identical 37-pixel footprint, the focal's
  contrast against its own surround went the other way, 1.93 → 2.17:1, and the
  secondary objects 2.07 → 2.32:1. The loop reference already names this blind
  spot for object-level *flattening*; this is the same blind spot with the sign
  reversed — a ground converging on itself while its objects separate.
  *Generalise:* when the floor fires, render at that exact size and measure the
  object, not the image. The floor is evidence about the histogram, never about
  the mark.

  **(h) A three-tier value stack has no free parameter.** Light stone / mid water
  / dark vessels: deepening the water helps the light tier and hurts the dark one,
  by construction, and no global setting lifts both. Sweeping four basin depths
  made the trade explicit (focal 1.85 → 2.28:1 as the pier ratio fell 1.52 →
  1.28:1) and turned a taste argument into a choice with a number on it. Where a
  scene has three tiers, sweep the middle one and publish the curve before
  defending a setting; and when the trade is genuinely balanced, the real fix is
  local (shade the enclosed water, leave the open water bright), not another
  global gradient.

- **2026-08 · ship-feature "The Launch" — breaking water needs an asymmetric
  profile, and three scaffolds proved it the expensive way.**

  **(a) A symmetric envelope cannot make a wave.** Two scaffolds failed for
  opposite reasons before the third worked, and both failures are the same
  omission. A gaussian envelope modulated by ripples (tallest at the stem,
  decaying both ways) produces a *hill*, which renders as molten wax however
  its lumps are tuned. Twenty-one hard-edged filaments fanned off it produce a
  *sunburst*; narrowing the fan to a comb and adding a per-filament value ramp
  produces *flame*. What both are missing is the single feature that reads as
  "breaking": an **asymmetric profile whose lip overhangs its own hollow**.
  Author the crest's top edge as an explicit control polyline — a long windward
  rise, the peak just forward of the stem, then a short steep fall — resampled
  with smoothstep and given chop proportional to local height; then a lip
  crescent that reaches *past* the body's forward edge, and a darker lune
  tucked beneath it. Bright rolled edge over dark hollow is the whole read;
  either one alone is invisible.
  *Generalise:* asymmetry that carries meaning has to be authored as control
  points. A symmetric generator with an asymmetric parameter is still symmetric
  where it counts.

  **(b) Both ends of a shaped-envelope path must collapse, not just the top.**
  When the crest's top edge fell to zero at the tails but its bottom edge stayed
  a fixed distance below the waterline, the result was a two-pixel hairline of
  pure accent running the full span — indistinguishable from a drawn rule across
  the water, and invisible in the source. Tie the skirt to the same height term
  (`bot = base − h·k + s·(h/h_peak)^p`), with `p > 1` so the skirt falls away
  *faster* than the crest, or the wave grows a foot.

  **(c) Spray is a value ramp, not a shape.** Filaments filled with the accent
  root-to-tip read as fire whatever their geometry. Water thins as it flies, so
  each filament goes ember → foam → near-white along its own length. This is the
  one place `objectBoundingBox` gradient units are correct rather than the
  documented trap: the ramp is the water thinning along that filament's own
  axis, not the scene light, so each filament genuinely is its own object. (It
  still did not save the scaffold — see (a) — but the diagnosis is reusable.)

  **(d) Size the accent on the shelf, not in the reference.** Every large-crest
  round looked defensible at 1024 and read as an orange blob clamped under the
  bow at 128 and 250px, which is the size the icon actually lives at. Cutting
  the crest's height by a third and keeping three faint spreading arcs on the
  water bought back more "moving" per unit of accent area than any amount of
  crest did. Put the candidate at shelf size beside its siblings before deciding
  how big the accent should be.

  **(e) A clipPath's contents can silently brown an entire face.** An ember
  bounce gradient clipped to the hull at 0.66 opacity is not a bounce, it is a
  wash: it turned the whole forefoot bronze while every measurement of the ramp
  said the colours were right. A bounce is a kiss on the surfaces that *face*
  the emitter — 0.22 falling to 0.05 within 15% of the axis. The gate scored the
  fix at −0.0034, which is noise; the palette and figure-ground checks caught it
  immediately. Same shape of error as the dossier-report specular: a wide,
  low-amplitude, hue-only defect sits exactly in the composite's blind spot.

- **2026-08 · mac-doctor round 7 — breaking one boundary on purpose, and two
  ways a colour sweep pays you to be wrong.**

  **(a) A deliberate discontinuity is safe when it is a parameter of the shared
  generator.** The previous round's whole lesson was that continuity has to be a
  construction rather than a matched pair of edits. This round had to break the
  band's OUTER boundary — the accent segment stands proud of the ring, which is
  what makes it read as reclaimed rather than as a coloured slice of the same
  dial — while keeping the INNER one flush. Adding `grow` to the one `band()`
  generator does both: the outer radius is `R_OUT + grow`, `R_IN` is not a
  function of it, and every derived quantity (bevel angle, shoulder radii,
  stroke widths, the cast shadow, the section gradient's stops) is computed from
  `grow` inside the same function rather than restated. Verified on the render:
  inner radius 189.0–190.2 at every angle through both segments, outer 331 on
  the arc and 345 on the segment.
  *Generalise:* an intentional asymmetry belongs in the shared generator's
  signature. A second code path would deliver the same picture and lose the
  guarantee, which is the whole asset.

  **(b) A multiplicative value gain clips, and clipping flattens the ramp it was
  brightening — while the whole-image metric goes UP.** Sweeping the accent
  ramp's HSV value by a gain scored best at 1.14 and was unusable: three of the
  five face stops pinned at V=1.0, so the section's shoulder, its minimum and
  its outer stop became one colour. The measured p5–p95 luminance spread still
  rose, because the specular and the bevel wall own that statistic, not the
  face. Remap value affinely into `[v_lo, v_hi]` instead and the ramp stays
  monotone by construction.
  *Generalise:* when the edit is "make this ramp brighter", check the ramp's own
  stop ordering after the transform, not the image's spread. This is the same
  shape of error as r06's "find out which pixels own your percentiles".

  **(c) An error term over the channels the gap is in buys its score with the
  channel you left out.** The accent's gap against the reference was in R and G,
  so the first sweep scored |ΔR| + |ΔG| at p10 and p50 — and picked a ramp that
  cut G by raising saturation, which drove B to zero. The reference's median
  accent carries B=49 at saturation 0.80. Score all three channels even when you
  only mean to move two.

  **(d) A warm spill on the ground defeats a warmth-based boundary detector.**
  Checking that the segment's inner boundary matched the arc's, a detector using
  `R > B + 40` counted the accent's low-opacity spill on the porcelain as
  object, and reported the segment's inner radius 23px inside the arc's — an
  artifact indistinguishable, on the number alone, from the exact fault the
  build exists to prevent. `R > B + 90` separates the body from its own light.

  **(e) A specular is worth flooring below ~64px, and the profile proves it
  rather than the composite.** Two blind judges had preferred a flat predecessor
  at 32 and 16px while self-contrast and edge F1 both favoured the material
  rebuild. A radial profile along the key axis found the mechanism: at 32px the
  specular lifted the stroke's outer third to L 0.53 against a body of 0.23, so
  the lit edge dissolved into the ground and the stroke read thin and doubled.
  Rendering the ≤64px rasters from the same build with the specular's peak
  opacity at 0.30 drops that lift to +0.18 and *raises* 32px self-contrast,
  0.733 → 0.741. One parameter, one extra file, master untouched.
  *Generalise:* a highlight narrower than about two rendered pixels carries no
  material information and costs silhouette. Make it a size-aware render
  parameter rather than removing it from the master.

- **2026-08 · mac-doctor capacity ring — one `band()`, two hues, and the
  bevelled-puck section** — a ring gauge whose reclaimed segment sits INLINE in
  the same track. Two findings, both reusable.

  **(a) Continuity is a construction, not a pair of matched edits.** The segment
  and the arc measured identical inner and outer radii and still read as a broken
  circle, because the arc carried an inner edge-catch stroke that the segment did
  not: one boundary lit for 280 degrees and unlit for 40. Five hand-adjustment
  rounds moved the segment and never touched the cause. The fix is to emit the
  whole material stack from ONE function called once per segment, so every
  boundary, shoulder, bevel and cut-end radius is shared by construction and
  cannot drift apart later. Verified on the render: object at r=192 and ground at
  r=334 at every angle, through arc and segment alike.
  *Generalise:* when two parts of one object must read as one object, share the
  generator, not the numbers.

  **(b) A gel band is a bevelled puck: dark wall, inset face, section ramp.**
  Sampled off the raster, every terminus is a dark moulded wall around a paler
  inset cross-section face, and the same wall runs the long sides. Build it as
  two concentric strokes on the same arc — the shell at full width in an OPAQUE
  key-axis colour ramp, then the face at `W - 2·BEVEL` — and shorten the face arc
  by `degrees(BEVEL/R)` at each end so the CUT ENDS are bevelled too, which a
  stroke cap cannot do for you. Bevel measured at 0.08 of the band width.

  Three traps this cost, each worth its own line.
  **The wall must ramp COLOUR, not opacity.** Authoring it as an opacity ramp
  dissolved the wall to nothing on the unlit side and washed the whole mark out;
  a wall is opaque everywhere and only its colour changes with the light.
  **Light the shell, not the face.** Modelling only the inset face left the wall
  unlit, which reads as an inked outline round the shape.
  **`objectBoundingBox` gradient units are wrong for a multi-part object.** They
  rescale the axis to each shape, so a 40-degree segment got its own private
  light direction while the arc around it got another — a rubric-5 break on a
  mark whose whole point is that the two are one physical band. Every angular
  gradient goes in `userSpaceOnUse` on one shared axis.

  **And the key direction is measurable, not a default.** The 45-degree diagonal
  everyone reaches for put the segment at t=0.41 on the axis, the neutral point,
  and it came out muddy. Reading the raster instead — specular along the TOP,
  darkest body at the BOTTOM, left and right flanks equal at centre height —
  gives a near-vertical key tilted about 16 degrees, which lit both parts as one.

  **What it cost on the gate, and why it shipped anyway.** Every term improved at
  every size except SSIM at 1024, which fell 0.733 to 0.695 and tripped the
  Pareto gate — the documented mechanism, since new surface structure the
  reference carries at different coordinates raises local variance without
  covariance. Net composite +0.0730 across five sizes. A blind two-family panel
  (Claude, grok-4.5) then voted the rebuild the winner on OVERALL and MATERIAL
  unanimously, so it shipped: panel over gate, exactly as the ordering says.
  Both judges also preferred the flat baseline at 32/16px, where the measured
  self-contrast and edge F1 both favour the rebuild — a disagreement recorded
  rather than resolved.

- **2026-08 · clarify "The Drawn Card" — a gradient's dominant axis is the one it is
  measured along.** An extrusion wall 32px tall and 470px wide was given a
  gradient meant to run *down* it, written as a vector from `(x, y+h)` to
  `(x + 0.28w, y+body_h)` — a small lateral lean on a mostly-vertical run, or so
  it read. It is not: that vector is 132 long in x and 30 in y, so every point on
  the band projects past offset 1 and **the whole wall rendered as one flat
  colour**. Measured, the master's wall was 0.617 for 32 consecutive pixels where
  the reference ramped 0.702 → 0.628. The fix is two constructions, not one: a
  purely vertical `linearGradient` for the ramp, plus a *separate* horizontal
  overlay clipped to the same band for the lean. Lesson: *a gradient carries one
  axis; a second direction is a second layer.* The failure is invisible in the
  source, where the intent is legible, and invisible to a composite average,
  where a flat band and a ramped one differ by a few thousandths — it shows up
  only in a perpendicular profile.

  **The same fixture also has the cleanest case yet of the reference being the
  wrong target.** The raster was porcelain cards on a porcelain ground; at 16px
  that has no value separation between glyph and field, so the master converged
  faithfully onto a pale blob with two accent specks. Nine rounds of gate ACCEPTs
  had been buying similarity to a weakness. Moving the *glyph* down the value ramp
  (two of three cards to clay, the focal one left porcelain) took the 16px
  contrast spread 0.229 → 0.362 against the reference's 0.326 and cost 0.075 of
  1024 composite, gating REJECT on all five sizes. Ship it anyway: the check the
  rubric is protecting (#4, 16px identity) is one the reference itself fails, and
  the shelf the icon lives on is the real judge. *Before a small-size round, put
  the master at 16px beside the siblings it will sit next to — the reference is
  not that shelf.*

- **2026-08 · a spine crest on a warm-lit object is never `#FFFFFF`** — the
  dossier-report fold shipped a crease highlight as a pure white hairline at
  0.55 opacity. It is a hard specular in a scene lit by nothing white, which
  Tahoe grammar #6 rules out, and it reads as a *gloss streak rather than
  volume*. Warming it to the measured rim scatter (`#FFE7D6`), halving the
  opacity and widening the blur turns the same geometry back into a rolled
  edge. Crest hue comes from the scene's own rim scatter, never from the
  colour-picker's top-left corner.

  **The part worth keeping is how it was found.** Two blind judges named the
  defect independently, in the same words, on a round the composite had scored
  as an improvement. The fix that reversed the panel 2-0 on a reseeded order
  moved the composite by **+0.0011**, which is noise. So a highlight's *hue*
  sits in exactly the blind spot of an averaged pixel metric: it is a thin,
  high-frequency, low-area feature, and the scorer is integrating over an area
  where it barely registers. Run the panel on any round that touches a
  specular, whatever the gate says, and do not let a passing composite argue
  you out of a defect two humans-in-the-loop both named.

- **2026-08 · fitting a raster's plane, and why the residual lies** — deriving a
  banner's ground plane from a diffusion take means measuring geometry the
  generator never stored as constants. Fitting an axis-aligned conic to the
  pool's boundary works, with one trap that inverts the obvious check: **RMS is
  *lower* on the wrong fits.** An arc sampled from a single flank returns a
  confident, tight, badly wrong ellipse (KY 0.316 against a true 0.399); at 0.86
  coverage the fit collapses by 16%; only at 0.98 coverage does it recover the
  control's known constants (cx 512.0 against a true 512, rx 212.4 against 211,
  KY 0.527 against 0.515). **Check arc coverage, never residual** — a partial arc
  is a well-conditioned fit to the wrong problem.

  Two riders. Always fit a *known* artifact first as a control; the whole trap is
  only visible because a vector master with published constants was run through
  the same code. And note what the boundary you traced actually is: on the vector
  master the near melt edge is the aperture lip with the pool occluded behind it,
  while on the raster it is the pool edge itself — the same detector reading two
  different features, which no residual would ever reveal.

- **2026-08 · create-skill A rebuilt on the four eye-reviewed defects** — the
  fixes landed, and the round found a construction bug worth more than any of
  them.

  **A `<clipPath>` with two subpaths and no `clip-rule` silently unions them.**
  SVG's default fill rule is nonzero, so a clip meant to be an annulus (outer
  wall minus interior) becomes the whole disc, and every layer clipped to it
  paints straight across the middle. Here `rimClip` had been quietly spilling
  warm porcelain veils over the melt for the entire fixture's history — a third
  stray veil nobody had seen. Fixing it moved the pool lune from `#EB562E`
  (L 0.452, S 0.805) to `#DA1A02` (L 0.257, S 0.991), against C2's `#D51504`
  at L 0.238.

  Why it survived so many rounds: the defect is low-amplitude and spread over a
  wide area, which is exactly the shape a composite average cannot see. So when
  a material reads washed out and the gradients measure correct, **check the
  clip stack before touching the ramp** — and give any clipPath with more than
  one subpath an explicit `clip-rule="evenodd"`.

  **The metric's bias now has a direction, not just a size.** The round scored
  ACCEPT (+0.3267; five-size mean 0.5600 → 0.6253), but the gain came almost
  entirely from the light-direction fix and the clip bug, both low-frequency
  luminance changes SSIM genuinely sees. The two *structural* fixes — the
  parting-key notch and the non-concentric mouth — moved the composite by
  roughly nothing. The metric rewards broad luminance agreement and is blind to
  silhouette detail, which is why a run of ACCEPTs is not evidence that the
  shape is right.

  **The reference is not the ceiling.** Tracking C2's shaded flank would have
  taken figure-ground to 1.19:1, which C2 itself fails. The rebuild held its
  flank at 3.21:1 and took the rubric hit instead. Rubric outranks gate.

- **2026-08 · create-skill A vs C1 vs C2, reviewed by eye** — four differences a
  human saw immediately and the metric stack almost entirely missed. Worth
  reading as a set, because together they are what "the raster looks better"
  usually means.
  **(a) Vibrancy is emission, not saturation.** Measured, the shipped vector's
  accent was *more* saturated than both rasters (0.673 against 0.552) and still
  read as muted, because it was less bright (V 0.801 against 0.871) and, more
  importantly, was a filled shape rather than a light source. The rasters' pool
  has a hot core that lights the inner wall above it. Reach for the emissive
  interior recipe, not the saturation slider: a bright core under a translucent
  surface, a bloom layer, and visible bounce onto the surfaces it faces.
  **(b) A primitive silhouette reads as generic.** Both rasters cut a notch into
  the vessel's outer wall — a parting key, a real mechanical feature of a
  two-part flask. The vector drew a plain circle. The notch costs one path and
  is most of what makes the object look designed rather than defaulted. Ask what
  physical feature the object would actually have, and cut it.
  **(c) The inner edge is not the outer edge scaled.** In both rasters the inner
  opening is shaped by wall thickness and interrupted by the notch; in the
  vector it was a concentric circle. Concentric primitives are the signature of
  an object that was constructed rather than observed.
  **(d) Light direction is rankable, and the ranking was C2 > C1 > A.** The best
  take has one key, a visible terminator wrapping the cylinder, and a long
  directional cast shadow that agrees with both. Coherence of the light model is
  judged as a whole, not per-surface.
  **What this cost the instrument:** crude area, saturation and luminance-range
  measures reproduced *none* of (b), (c) or (d), and inverted (a). These are
  properties the current metric stack cannot see, which is the concrete reason
  the rubric and the panel outrank the gate. When a human names a difference,
  measure the specific thing they named rather than trusting a general metric to
  have caught it.

- **2026-08 · create-skill "The Pour" loop** — two measured corrections, both to
  assumptions that felt obviously right.
  **(a) Molten material is deep red, not bright yellow.** Sampled off the
  reference: L 0.42-0.53 at hue 5-9. The drafts were 17° too yellow and 0.22 too
  light, because "molten" reads as yellow-white in imagination and as dark red on
  the actual reference. A hue-and-luminance sample before authoring catches it;
  nothing else did.
  **(b) A translucent stream is DARKEST along its axis**, not brightest. The
  bright-core construction (glow in the middle, falling off to the edges) is the
  exact inverse of what a translucent pour does: the centre is the deepest path
  through the material, so it absorbs most. Build the core dark and let the edges
  carry the light. This is the same shape of error as the shaving curl reading
  darker than its ground, and it is the third time an assumed
  bright-where-you-expect-bright relationship has failed here.

- **2026-08 · improve-skill loop r06 (material, accepted)** — **find out which
  pixels own your percentiles before choosing what to edit.** The contrast budget
  is a whole-image statistic, so the regions that set it are not necessarily the
  ones that look wrong; measuring which pixels sit at p90 and p10 tells you
  whether an edit will move the number you are being judged on or a different
  one. Here it raised self-contrast 0.553 to 0.645 at 32px while figure-ground
  went 2.73 to 3.48:1, clearing the floor that had rejected the previous round.

- **2026-08 · improve-skill loop r05 (coarse structure, rejected on the floor)** —
  **"one key, one axis; finish is a step on it."** Hang every ground field's
  gradient on a single segment running from the key light's corner, express each
  material's finish as stop offsets along that one axis, and check the ordering
  predicate before rendering: the brightest ground must lie nearest the key. One
  axis makes a multi-material ground physically coherent by construction rather
  than by eye. Budget the master's p90-p10 spread before choosing an approach.

- **2026-08 · improve-skill loop r04 (coarse structure, the curl round)** —
  **fit the rims, then read the solid off the fit.** To rebuild a rolled or
  tubular form from a reference, fit circles to its two visible rims and derive
  the solid from that fit rather than assuming any of it. Doing so produced three
  numbers the previous four attempts had guessed wrong: the cross-section is a
  true circle at 1.0 foreshortening (not 0.54), the separation-to-radius ratio
  makes it a hoop at 2.5:1 (not a 1.36:1 pipe), and its axis bears 45.9° against
  the blade's 33°, so the roll is tipped nearly 13° off what had been built.

- **2026-08 · improve-skill loop r03 (small-size repair, rejected)** — before
  repairing a region toward the reference, re-score it with that region
  **absent**. If removal costs the same term the repair costs, the error is
  sitting inside the metric's tolerance radius around a true feature, and the
  metric will pay you to stay wrong. Measured here: an over-dark blob was
  earning edge recall by accident, so correcting it and deleting it moved the
  32px miss count the same way (11 to 18 to 24).

- **2026-08 · improve-skill loop r02 (detail): the metric was wrong, not the edit.**
  A fibre texture on the un-planed side was REJECTED by the gate and then
  PREFERRED OVERALL by the human reviewer. Both facts are correct, and the
  arithmetic explains the gap: uncorrelated detail inflates local variance while
  covariance stays near zero, so SSIM falls (0.651 to 0.548) even as edge
  alignment makes the largest single move of any round (1024 edge_f1 0.048 to
  0.347, against the reference's own 0.885). SSIM outweighs edge at every size,
  so the composite punishes surface texture on principle.
  **Do not read this as "texture loses".** Read it as: the composite cannot
  currently see surface texture as an improvement, so a texture round needs human
  or panel adjudication rather than the gate's verdict. The recovered source was
  kept at `assets/loop-runs/r02/build_icon.candidate-recovered.py` in the
  improve-skill plugin and is **no longer on disk** — which is itself the lesson
  the round bought: *a rejected round whose source is destroyed cannot be restored
  when the human disagrees.* The construction is recorded here precisely because
  the file it came from is gone.
  Reusable construction confirmed: a filter on a transformed `<g>` runs in that
  element's local frame, and the inverse-transform-on-contents idiom applies it
  without disturbing geometry or gradients.

- **2026-08 · improve-skill loop r01 (material, +0.1427 net)** — three findings,
  one of them a bug in our own icon rather than a mismatch with the reference.
  **(a) Single-emitter falloff mask.** Author a carried emitter's decay once, as
  a white `linearGradient` with varying `stop-opacity` along the emitter's axis,
  wrapped in a `<mask>` applied to the group holding *every* layer that emitter
  owns (bloom, glow, core, specular, ground spill). One gradient, one mask, so
  the emitter, the surfaces it lights and the ground beneath it cannot drift
  apart; they are one number. Give the falloff a floor when the emitter also
  carries identity at small sizes.
  **(b) Shadow hue is a separate check from shadow luminance and saturation.**
  The reference's darkest block pixels read warm (0.155, 0.132, 0.119); the
  master's read *blue* (0.096, 0.108, 0.128) at near-identical saturation, so
  both a luminance-range check and a saturation check passed it. Nothing in the
  scene emitted cool light. Re-hue with each stop's luminance held to ±0.01,
  which isolates the cast from the modelling.
  **(c) Check your own icon for single-light violations before blaming the
  reference.** The master's *brightest* ground was the corner furthest from its
  own key light. That is not a mismatch with the reference; it is the icon
  breaking its own stated light model.

- **2026-08 · improve-skill block pitch (gated round, +0.0657 net)** — a tool
  "riding" a surface is a **wedge, not a lifted copy**: a constant-rise lift
  produces a parallel top face that reads as an object lying flat. Measure the
  reference's actual angles (ground line 38.9°, shoulder 41.9°, front face
  55→90px deep) and make the lift **linear in local x** — which stays affine,
  so the whole top face is still one transform matrix and every texture and
  gradient rides it for free. Bonus catch: re-anchoring the face gradient to
  the *lifted* frame fixed an 88px registration bug worth +0.025 on its own.
  Lesson: *attitude is a taper; measure the reference's angles, and keep
  lifts affine so materials follow the geometry.*

- **2026-08 · create-mac-icon "The Cast" loop (r06)** — a translucent gel must
  keep its *saturation* in shadow, not just its luminance. Sampling the
  reference's darkest gel pixel against the master's caught shadows that had
  gone brown (`#A93411` vs the reference's `#DC2F0E`) while the luminance
  range and mean saturation already matched — invisible to a range check,
  obvious to a darkest-pixel check, and the loop's largest single gain.
  Lesson: *check the dark end's hue, not only the ramp's endpoints; a shadow
  that desaturates reads opaque.*

- **2026-08 · Ledgerline "stepped ledgerline" loop (eval commission, r01→r04)** —
  **(a) The frosted-panel fade is a bounded edit, not a global one.** Raster
  engines render "frosted white" as almost pure ground-bleed (measured 1.41:1
  boundary contrast), which looks like glass at 1024 and dissolves by 32px;
  copying it wholesale dropped the master to 1.02:1 and hard-failed rubric
  #7/#4. The construction that gets both: start the frost gradient ~40% down
  the mass bounding box, keep every figure-ground boundary above that line at
  full opacity (3:1 value gap), fade only the boundary-free region below.
  Lesson: *fade the frost where no boundary lives; never across a boundary.*
  **(b) Draw the lip bloom UNDER the mass.** A blurred white stroke along the
  glyph's top edge painted *before* the mass fill is occluded on its inner
  half, so the lit lip spills light onto the ground (the Tahoe tell) with one
  path and one blur. Painted above the mass it reads as a sticker halo.

- **2026-08 · improve-skill shaving curl (round 7)** — three failed attempts
  drew the curl as a spiral *outline* (a shell); the fix was a swept surface:
  one cross-section curve (near-straight tail easing into an open 0.78-turn
  hook) swept along the blade axis, cut into 96 bands, each lit by its real
  facing angle to the one top light. Two values measured off the raster
  rather than guessed, both load-bearing: the cross-section is a circle seen
  obliquely (compressed 0.54 along the roll axis — a true circle reads as a
  capped tin can), and the curl is **not** a pale shape on a dark ground
  (lit top L 0.576 vs ground L 0.635 beside it). Lesson: *measure the
  reference's actual luminance relationships before authoring — the
  "highlight = lighter than surroundings" assumption is a repeat trap.*

- **2026-08 · improve-skill "Honed Edge" rebuild** — the flat bar became a
  12/12 volumetric extruded solid: per-face gradients (top face lightest,
  front face mid, flank darkest), corrected before/after luminance polarity
  (+0.174 measured, where the raster's own take had it inverted), contact
  shadow under the leading edge. Lesson: *per-face gradient separation* is
  the cheapest volumetric move — three gradients on three faces beats any
  amount of filter work on one shape.
- **2026-08 · trawl v2→v4 manual loop** — matching the raster's richer
  orange required widening the gradient's luminance range (lighter top stop,
  darker base stop in the same hue), not saturating the mid-tone; and the
  silhouette's taper had to come from the reference's proportions, not the
  first draft's. Lesson: *material gaps often hide a luminance-range gap* —
  check the ramp's endpoints before adding layers.
- **2026-08 · compaction-quality A-v5** — the raster's depth read came from
  its contact shadows more than its gradients; adding two small blurred
  ellipses under the front elements closed most of the perceived gap.
  Lesson: *contact shadows are the highest ratio-of-effect-to-bytes layer.*

## Ring / annulus edge catch (mac-doctor, 2026-08)

A stroked ring lit from a single top source catches light in two places, and a
master that authors neither reads flat no matter how good its body gradient is.

The failure this replaces: authoring the rim as a **displaced copy** of the arc,
a narrower stroke of the same path translated upward. It produces no visible
edge, because the displaced copy sits *inside* the stroke width rather than
along its boundary.

The construction. Two concentric strokes at the annulus boundaries:

```
outer catch:  arc at radius R + W/2 - 5,  stroke-width ~9
inner bounce: arc at radius R - W/2 + 6,  stroke-width ~7
```

Each carries a vertical gradient that fades as the curve turns away from the
light, so the catch dies out rather than ringing the whole circle:

```
outer:  #C9D2E2 at 0.90 -> 0.22 by 38% -> 0 by 75%
inner:  weaker and inverted (y1=1 -> y2=0), #93A0B8 at 0.55 -> 0
```

The inner line is the bounce off the ring's own concave face, so it is always
weaker than the outer catch and starts from the opposite end of the gradient.
Both are drawn outside the drop-shadow filter group; inside it they get blurred
into the shadow and disappear.

Confirmed against a GPT Image 2 raster take that won the material judgment: the
gap between master and raster was mostly this, plus a cooler body (sampled
(60,81,110) against (75,85,99)).
