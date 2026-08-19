# Icon: Wallspace

- **Era:** Custom (flat-minimal contemporary indie) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512, SHA-1 `7a77ceb2`) · **Category:** Utility (live wallpaper for Mac)

**Era note.** Not one of Apple's named languages. It borrows the Big Sur **uniform front-facing squircle** but strips every Big Sur depth convention — no top-down baked micro-shadows, no tool overlay, no material. The result is the contemporary **dark-charcoal-square + single white glyph** flat-minimal style (Raycast / Arc-dark / AI-utility family), shipping into the macOS 26 Liquid Glass era without engaging any glass layering. Classified `custom` rather than forced into `big-sur`, because the deviations from Big Sur (diagonal rather than vertical light, flat unlit glyph, zero material) are systematic, not incidental.

| Dimension | Reading |
|---|---|
| Background | Ramp, **diagonal** #333333 (top-left) → #0E0F0F (bottom-right), mid ~#2B2B2B (measured, 512px) |
| Glyph | Abstract four-pointed **sparkle / north-star**, concave-curved arms, flat #FFFFFF, optically dead-centre (255,256 on a 512 canvas), spans 310px ≈ **60% of canvas** — bold, confident sizing |
| Overlay device | None |
| Light model | Directional gradient implies a **top-left light** on the ground; the glyph is **flat and unlit** (no specular, no highlight, no anchoring micro-shadow) — foreground ignores the background's light |
| Layer stack | Two planes only: (back) charcoal diagonal-gradient squircle field → (front) flat white sparkle |
| Palette economy | **Achromatic** — zero hue families. Charcoal ramp + white glyph. Contrast white-on-#2B2B2B ≈ **14:1** |

## Signature devices
- **The AI-shine sparkle.** A clean, custom-drawn four-pointed star with softly concave arms (rounder/friendlier than the stock SF `sparkle`). It is the icon's whole personality — but it is a *category signifier* ("premium / curated / magic / new"), not a subject glyph. [GOLDEN-NUGGET, contested — see Failures]
- **Diagonal charcoal gradient.** Light runs corner-to-corner (top-left → bottom-right) rather than the canonical Big Sur vertical sky-ramp. Subtle, but it is the one place the background departs from convention.
- **Total icon↔brand coherence.** The cover uses the *exact* icon (charcoal rounded square + white sparkle) as the wordmark lockup and the in-app toolbar logo. Palette coherence between icon and app is total — the mark is the brand.

## Failures
- **#10 Variant robustness (Liquid Glass era) — FAIL.** Ships as a **dark-only flat raster** with no authored light / clear / tinted appearance. In the macOS 26 era this app targets, a permanently-dark square is exactly what the system's adaptive appearances move away from; there is no light-mode identity, and the composition assumes a fixed dark ground. Defensible as a deliberate brand choice, but a real robustness gap.

## Soft passes (flagged, scored as pass)
- **#4 16px squint — soft.** The sparkle survives at menu-bar size and stays nameable, but the concave arms flatten into a chunkier plus/diamond; detail is near its floor.
- **#5 Single light model — soft.** Coherent overall, but the flat unlit glyph carries none of the top-left light the ground establishes; the two planes are lit by different rules (flat-glyph-on-gradient convention rescues it).
- **#11 Personality — soft.** One nameable device (the sparkle), but it sits squarely inside the **dark-square-+-sparkle template**. Reads as committed *direction* only at the palette/craft level; the composition itself is category-default. The glyph does **not** communicate the subject — nothing here says "wallpaper / desktop / display." Subject-mining is absent; a sparkle would fit an AI assistant, a launcher, or a photo app equally.

## Rhymes with
- The **charcoal-squircle + single white symbol** cluster: Raycast, Arc (dark), and the broad AI/utility-launcher field. Also the generic **"AI sparkle" motif** family. First member of a potential *mono-minimal-dark* icon cluster in this corpus — hold for ≥3 before promoting.

## Provenance caveats (for synthesis)
- **512×512, not 1024** — a macapp.supply web render, and the **squircle mask is baked in** (transparent corners in the PNG). Mask discipline and true safe-zone margins are inferred from the masked render, not verified against an unmasked full-bleed layer. All hex values `(measured)` at 512px; ramp endpoints are corner samples.
