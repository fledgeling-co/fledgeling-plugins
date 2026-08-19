# Icon: Audio Notes formerly Email Me

- **Era:** Big Sur unified (dimensional object-at-an-angle, baked soft lighting) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.jpg`, 512×512 JPEG (resized web render of the 1024 master; not the shipping asset). Category: AI. App: capture a thought by voice or text, then send it.

| Dimension | Reading |
|---|---|
| Background | ramp #F3B606 (amber, top) → #FF9E11 (orange, lower-right), with a bright-yellow radial light burst in the lower-left corner (#FDF317 / #FBDC10). One warm hue family (amber→yellow). |
| Glyph | object — a white origami **paper airplane** tilted along the diagonal, nose up-right. Paper white #F5F5F3 / top-edge specular ~#F8F6F7; fold facets mid-gray #AEAEAE stepping to ~#8A8A8A on shaded underside. Optically centred on the grid, occupying the central safe zone; nose reaches toward the top-right but stays inside the margin. |
| Overlay device | none — the plane is the primary subject, not an overlay tool. (Its diagonal placement quotes Apple's "tool at an angle" convention but the object *is* the icon.) |
| Light model | Plane key-lit from upper-left (top faces bright, underside shaded); background glow originates lower-left. Baked matte-paper shading + a soft grounding contact shadow beneath the plane (#CB8A16 vs surrounding #F5B10A). No glass specular/refraction. |
| Layer stack | back → front: (1) amber→yellow gradient field with lower-left sunburst; (2) baked soft contact shadow under plane; (3) white paper-airplane object with multi-facet gray shading; (4) baked top-edge specular on the plane's leading fold. |
| Palette economy | 1 hue family (amber-yellow) + a white/grayscale glyph; no competing saturated accent. Accent = none (the amber field is the brand colour). |

## Signature devices
- **Origami send-plane** — a literal paper airplane rendered as folded-paper facets; the "send / dispatch" metaphor made tactile. This is the whole personality of the icon in one object.
- **Object-at-an-angle** — the plane tilts nose-up-right along the diagonal, the Big Sur convention that reads as motion/velocity (a send vector).
- **Sunburst backdrop** — amber-to-yellow gradient with a lower-left light burst rather than the canonical top-down sky ramp; warmer, more energetic than a straight vertical gradient.
- **Baked contact shadow** — a soft grounding shadow anchors the plane to the field. Coherent within Big Sur logic, but see Failures — this is an era-tell that fights current-era system effects.

## Failures
- **#10 Variant robustness (Liquid Glass) — FAIL.** A single baked raster: fixed amber background, baked lighting and contact shadow, not authored as Icon Composer layers. It cannot generate graceful dark/clear/tinted renders — the white glyph depends on the amber field for contrast, and the baked shadow/specular conflict with the system's dynamic effects on macOS 26 (Tahoe). Renders as a legacy static icon on the current OS.

**Soft passes (counted as passes, flagged for synthesis):**
- **#2 Grid** — optically balanced but tilts high-right with the tail near lower-centre; reads centred, not grid-perfect.
- **#5 Single light model** — plane key-lit upper-left while the background glow keys lower-left; the two origins don't perfectly agree, though the warm environment reads coherent.
- **#8 Depth coherence** — layer order is sensible, but the baked drop shadow is the era-tell noted in #10; coherent only inside Big Sur's baked-shadow logic.

**Passes worth naming:** #3 silhouette (instantly a paper airplane from solid black) and #4 16px squint (survives at menu-bar size, still clearly a plane pointing up-right) — the two Dock-duty checks are strong. #6 palette economy and #7 figure-ground (white-on-amber, easily ≥3:1, survives grayscale) both clean.

## Brand coherence (icon ↔ cover)
Cover promo is the same amber-yellow world; the identical paper-plane glyph appears as the app's menu-bar item and a yellow "SEND" button. Palette coheres tightly. Caveat for the product: the plane communicates **send/dispatch** cleanly but says nothing about **voice/audio capture** — the icon carries the "Email Me" half of the renamed product, not the "Audio Notes" half (no mic/waveform cue).

## Rhymes with
- Telegram's paper-plane send lineage and the generic "send / share / dispatch" glyph family.
- Big Sur single-object-on-warm-gradient utility icons (object-at-an-angle with baked micro-shadow) — style family: warm-gradient single-object Big Sur utility. *(Hint only — no cluster promotion from one icon.)*
