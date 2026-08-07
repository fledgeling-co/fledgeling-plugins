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
| Curl / ribbon volume | Build as a lit ribbon: face and back carry different gradients, edge highlight along the outer curve, contact shadow where it meets the ground | A spiral path with one fill reads as a flat coil, not a curl |
| Emissive interior | Bright core shape under a translucent shell, soft `feGaussianBlur` bloom layer above, restrained halo radius | Glow painted as opaque colour doesn't light its surroundings |

## Marketplace-confirmed wins (add new entries below, newest first)

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
