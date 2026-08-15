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
  or panel adjudication rather than the gate's verdict. The recovered source is at
  `plugins/improve-skill/assets/loop-runs/r02/build_icon.candidate-recovered.py`.
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
# Proposed addition to `references/material-recipes.md`

Two confirmed constructions and one composition trap from the ship-fleet
commission. Written here rather than appended directly because this commission
was scoped to its own workspace; splice the block below at the top of the
**Marketplace-confirmed wins** list (newest first).

---

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
