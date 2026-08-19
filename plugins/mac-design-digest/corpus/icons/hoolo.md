# Icon: Hoolo

- **Era:** custom (flat monochrome logomark — era-agnostic; participates in neither Big Sur depth nor Liquid Glass layering) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 512×512 web render — see resolution caveat) · **Category:** Productivity · **App:** local-first file-organizer ("keep your Mac workspace quiet, clean, reversible")

| Dimension | Reading |
|---|---|
| Background | flat `#0C0C0E` (measured) — near-black, faint cool; **no ramp, no gradient, no scene** |
| Glyph | mascot/monogram double-read — a stylized **owl face** in `#F7F7F6` (measured, off-white faint-warm): two ring-eyes (white annuli, black pupils) flanking an upswept negative-space brow-chevron that descends to a point between them. Optically centred (glyph bbox cols 89–422 / rows 161–360 of 512; horizontal centre ~255, mass balanced low by the eyes and up by the wings) |
| Overlay device | none (no diagonal tool, no badge, no frame) |
| Light model | **none** — flat two-tone; no directional light, no specular, no baked micro-shadow. The figure is a pure negative-space cut-out, not a lit object |
| Layer stack | back→front: `[near-black squircle field #0C0C0E]` → `[white owl glyph #F7F7F6]`. Two visual planes but a **single flat composite**, not Icon-Composer-separable layers |
| Palette economy | 2 colours total (near-black + off-white); 0 hue families + 0 accent. Figure-ground contrast ~19:1 |

## Signature devices
- **[GOLDEN-NUGGET] Owl-from-negative-space.** The owl is never drawn as a positive shape — it emerges entirely from white cut-outs on the black field (two ring-eyes + an upswept brow-chevron). The subject (name "Hoolo" = an owl hoot) is legible without a single rendered feature.
- **"oVo" double-read.** The same mark parses as a two-O-plus-V monogram — the doubled "oo" of *Hoolo* with a wedge between. A deliberate figure/letterform ambiguity, the kind of move that gives a flat mark a second life.
- **Logo-on-black treatment.** White brand-mark centred on a near-black rounded tile — a web/mobile-first icon idiom, not a Mac-native depth composition.

## Failures
- **#10 Variant robustness (Liquid Glass):** the composition depends on the black background tile being visible and is not authored as separable layers, so it cannot yield true dark/clear/tinted system renders. In tinted mode the system would tint the artwork, but the *meaningful* shape here is the negative space — tinting inverts legibility. Hard fail.

### Soft passes (scored pass, flagged)
- **#1 Mask discipline:** delivered as a **pre-masked raster** — a baked squircle with a ~13px transparent margin (opaque region 13–498 of 512), not Apple's full-bleed *unmasked* square. The glyph itself sits well inside the safe zone, but the baked corner shape risks double-masking or a size mismatch against the system squircle in macOS 26.
- **#3 Silhouette test:** the owl read is present but not singular — it competes with butterfly/bird and the "oVo" monogram reading. Nameable after a beat, not instantly.
- **#4 16px squint test:** the ~19:1 contrast carries a recognizable dark-tile-with-white-mark to menu-bar size, but the two ring-eyes' inner holes close to solid dots and the ring detail smears — it survives as a distinctive tile, loses its anatomy.

## Rhymes with
- Flat monochrome brand-marks dropped on a black rounded tile — the "white logo on black squircle" family common to web/dev-tool and cross-platform apps. **Opposite pole** from the corpus's expected Big Sur "tool-on-gradient" and Liquid Glass layered-glass families; no corpus siblings yet (first icon digested).

## Cross-icon / brand notes
- **Palette divergence, icon vs. brand:** the marketing surface (cover.webp) is airy sky-blue (~`#87ADCE` estimated) with green + yellow accents and soft floral imagery — friendly, warm, reversible. The icon shares **none** of it: stark black-and-white, no green. The brand's carrying accent (green) is absent from the app's face. A coherence gap worth flagging to synthesis.
- **Resolution caveat:** source is a **512×512 web render** (`hasAlpha: yes`), not a 1024 master; all pixel readings scaled from it and fine ring/edge detail may be softened by the downscale. Hex values reliable (large flat fields); sub-pixel edge geometry is `(estimated)`.
