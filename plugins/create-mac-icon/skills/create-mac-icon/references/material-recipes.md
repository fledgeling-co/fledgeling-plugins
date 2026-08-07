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

## Marketplace-confirmed wins (add new entries below, newest first)

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
