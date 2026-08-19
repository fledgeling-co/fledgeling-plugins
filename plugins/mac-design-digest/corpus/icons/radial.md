# Icon: Radial

- **Era:** Big Sur unified (monochrome, front-facing, top-lit — **not** Liquid Glass) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 1024×1024, SHA-1 `bd5c3c3d`) · **App:** Radial — "a powerful radial (pie) menu for macOS" (Productivity)

| Dimension | Reading |
|---|---|
| Background | Vertical charcoal ramp #313131 (top) → #222223 (centre) → #141414 (bottom) — top-lit "sky logic", single neutral hue `(measured)` |
| Glyph | Abstract: a ring of **8 capsule dashes** on a circle (r≈285px on the 1024 canvas), evenly spaced with ~15° gaps. Optically centred on canvas centre (512,512). White→gray, top-lit emboss. `(measured)` |
| Overlay device | None — no diagonal tool, no badge, no frame |
| Light model | Single top-down source. Each capsule has a bright top edge (#FFFFFF) falling to a darker inner base = baked micro-emboss. Layered on top: a **rotational luminance fade** — dashes graduate bright at 12-o'clock (#F9F9F9) → dim toward the lower-left (#979797), quoting a loading spinner's motion trail. Soft rim highlight on the mask edge; no glass specular/refraction. |
| Layer stack | (1) charcoal gradient field on a squircle, mask + edge rim + soft outer shadow baked in → (2) ring of 8 embossed white/gray capsule dashes |
| Palette economy | One neutral family only (charcoal ↔ white). Accent: none. Focal saturation reserved by absence — the white dashes are the only bright element. |

## Signature devices
- **Segmented spinner ring** `[GOLDEN-NUGGET]` — 8 capsule dashes on a circle read simultaneously as (a) a loading spinner and (b) a radial/pie menu's wedge segments. The subject-to-icon mapping is literal and strong: 8 dashes = 8 menu wedges. The app's whole concept in one ring.
- **Rotational luminance fade** — the round-the-ring bright→dim gradient implies rotation/motion in a static image; a spinner convention borrowed to say "radial, in motion."
- **Capsule-dash emboss** — each pill has a top-lit highlight edge and inner micro-shadow, a restrained skeuomorphic pillow inside an otherwise flat monochrome field.

## Failures
- **#10 Variant robustness (Liquid Glass):** fails. This is a *baked dark composition*, not separable light/dark/tinted layers. The white ring depends entirely on the fixed charcoal ground for contrast; under the system's tinted/clear regeneration the ground would tint and the glyph would lose its figure-ground. Not authored in the Icon Composer layer model — it is a legacy-native (Big Sur) icon carried into the macOS 26 era.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline** — glyph sits well inside the safe zone, but the PNG is delivered **pre-masked**: transparent squircle corners (alpha 0) with a baked edge rim-highlight and soft outer drop-shadow. That fights the modern "ship a full-bleed square, let the system mask + shade" rule (HIG: don't bake shadows/edges). Likely the developer's own baked squircle, or a macapp.supply render preserving the PNG's mask — resolution honesty: can't distinguish from a static image.
- **#3 Silhouette** — filled solid, 8 disconnected capsules read as "a dashed/segmented circle." Nameable, but a ring of separate dots is inherently less instant than a single connected glyph; it reads "spinner" before "menu."
- **#4 16px squint** — the bright top dashes (14:1 contrast) carry a "dotted ring" down to menu-bar size, but the 8-count blurs and the dimmest gray dashes (#979797, ~5:1 on #202020) drop out first. Survives as a fuzzy dotted circle; loses its segment count.
- **#11 Personality** — one nameable device (the graded spinner ring), but a dashed circle is close to a stock loading-spinner motif; the committed minimalism is what lifts it above template, not the shape itself.

## Rhymes with
- Big Sur monochrome-glyph **dark-utility** family: single white glyph centred on a near-black charcoal squircle, no accent hue — the register of menu-bar launchers, command-palette tools, and small productivity utilities. (No sibling yet in this corpus — style-cluster hint only, not a promotion.)
- Its **cover art rhymes with nothing about the icon**: the marketing hero is vibrant purple Liquid Glass (a frosted radial menu over a magenta fan wallpaper); the icon is austere monochrome. Brand-colour incoherence noted — the icon carries the *form* of the product (the ring) but none of its *colour* identity.
