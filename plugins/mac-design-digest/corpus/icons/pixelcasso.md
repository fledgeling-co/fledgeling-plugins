# Icon: Pixelcasso

- **Era:** custom (full-bleed art-reproduction icon) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (192×192 web render — resolution-limited, see Notes) · **App:** native image editor for Paint.NET users on Mac

| Dimension | Reading |
|---|---|
| Background | Near-flat gallery-black field, `#030608` warming slightly to `#1A150C` at the lower edge (estimated) — a museum-wall ground, not a sky-logic ramp |
| Glyph | Scene, not glyph: an oil-painted woman's profile portrait (floral crown, rosy cheek, gold hair). Skin highlight `#DFCABD`, cheek mid `#C8B8AE`, ochre/gold hair `#997F3F`→`#5D4E2B` (estimated). Optically offset to the **left third**, not grid-centred |
| Overlay device | `other` — a **pixel-dissolve**: the right/hair region quantizes into mosaic blocks (`#332F20` avg), the painting literally breaking into pixels |
| Light model | Painterly frontal/upper-left portrait light on the face against dark; matte, no specular, no macOS baked micro-shadow. Internally consistent but not the top-down macOS light model |
| Layer stack | (conceptual, technically one raster) back→front: near-black ground · oil-painted portrait · pixel-mosaic dissolve over the hair/right region |
| Palette economy | ~2 hue families — warm gold/ochre + skin neutrals — on near-black. Accent is the rosy cheek (`~#C57A78` estimated) and a small blue eye; saturation reserved for the focal face detail |

## Signature devices
- **[GOLDEN-NUGGET] The pixel-dissolve pun.** A classical Picasso-style oil portrait quantizes into mosaic blocks along the hair — a literal visual rebus of the name (Pixel + Picasso). Highly nameable, fully committed; this is where the icon's entire personality lives.
- **Full-bleed art reproduction as the icon.** No squircle glyph, no chrome, no tool overlay — the artwork *is* the icon, edge to edge.
- **Gallery-black ground.** The near-black field makes the pale portrait glow, borrowing museum-wall framing logic; also gives strong figure-ground separation.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black the icon is just a square; the subject is a painterly scene with no clean, nameable solid silhouette. A profile-void is not a readable glyph.
- **#10 Variant robustness — FAIL.** A single dark raster wholly dependent on its specific colours. No layered/vector composition, so mono, clear and tinted renders would destroy it; cannot be re-authored in Icon Composer without a rebuild.
- **#12 No-text / no-photo — FAIL (photographic clause).** No text, but the icon is a raster reproduction of an external oil painting — the "photographic element" HIG warns against, and non-vector. (Also a licensing/originality flag — see Notes.)

### Soft passes (flagged)
- **#2 Grid adherence** — subject mass sits left-of-centre rather than on the optical grid; acceptable for a scene but not centred.
- **#4 16px squint** — a pale profile face on black is still discernible at 16px, but the pixel-dissolve concept (the whole point) smears into generic low-res photo; the differentiator is invisible at Dock/Spotlight size.
- **#8 Depth coherence** — coherent, but it's one flat art plane; none of the stacked-plane macOS depth the era model expects.

## Rhymes with
- Full-bleed **scene / photo-hero** icons that drop an image into the squircle rather than a glyph (photo-editor family — Pixelmator/Acorn-adjacent in strategy, not palette).
- **Concept-pun** icons whose payload is a wordplay device rather than a tool metaphor. (Hint only — needs ≥2 more members before any icon cluster forms.)

## Notes
- **Resolution caveat:** source is a 192×192 web render, not the 1024 master. Mask-edge treatment, true corner clipping, and sub-pixel micro-shadows are unassessable; pixel-block sizes are read at 192px scale.
- **Brand-coherence gap:** the marketing cover is navy `#132238` + steel/cream gradient + a serif **"P"** monogram in a white rounded square. The icon carries *none* of that — near-black + gold + skin, no navy, no monogram. App-Store face and wordmark identity diverge; an icon should communicate the subject, and this one communicates "art app" via pun but shares no palette DNA with the brand system.
- **Originality/licensing flag for synthesis:** the portrait reads as an actual (or closely-imitated) Picasso-style painting. Shipping a famous artist's work as an app icon is an originality and rights risk worth recording, independent of the rubric.
- **Era note:** does not quote any macOS era (not Big Sur squircle-glyph, not Liquid Glass layers, not skeuomorphic-object). Classified `custom`: a full-bleed art-reproduction icon with a digital-dissolve device.
