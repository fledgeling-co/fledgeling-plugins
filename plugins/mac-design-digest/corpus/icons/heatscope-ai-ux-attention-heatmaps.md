# Icon: HeatScope AI UX Attention Heatmaps

- **Era:** custom (contemporary flat mesh-gradient + grain, living inside a Big-Sur squircle) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply icon render (520×520, RGB, flattened against black with a baked outer drop shadow) · **Category:** Design

| Dimension | Reading |
|---|---|
| Background | Ramp — grainy thermal mesh gradient. Cool at top-right, hot at bottom: green `#99F998` → yellow `#E1D63E` → amber `#F2C313` → orange `#FD7E21`, washing to near-white `#EFEFEF`/`#ECFDEA` in the top-right corner (measured-from-render). |
| Glyph | Abstract negative-space **lightning bolt** carved by the black region against the gradient. Near-black ramp `#151515` (bottom-left) → `#313131` (top-left); bolt body sits at `~#1F1F1F`. Occupies the left third + a wedge notch driving to mid-right; optically weighted low-left, not centred. |
| Overlay device | None in the Apple "diagonal tool" sense — the device *is* the full-bleed diagonal figure-ground split (black vs thermal ramp). |
| Light model | Flat. No dimensional lighting, no specular, no baked micro-shadow. The only shadow present is the render wrapper's baked outer glow (`#6C6C6C`/`#919191` halo against the black backing), not part of the artwork's own light logic. |
| Layer stack | (back→front) 1. grainy thermal mesh-gradient field · 2. solid near-black lightning-bolt region (left + centre wedge) · 3. uniform film-grain/noise across the whole face. Render wrapper adds a baked rounded-rect corner + outer drop shadow on top. |
| Palette economy | Exceeds the ≤2-hue guideline — the ramp runs green→yellow→amber→orange→red, a full thermal spectrum — but it is **one coherent semantic ramp** motivated literally by the subject (an attention *heatmap*). Focal heat = the hot orange `#FD7E21`. |

## Signature devices
- **Negative-space lightning bolt over a thermal attention-heatmap ramp** — subject-mining done well: speed/energy (the bolt = "optimize UX decisions *faster*") crossed with heat/attention (cool-green → hot-red = the literal heatmap the product produces). A committed direction, not template-default.
- **Grain-over-mesh-gradient face** — uniform film noise laid over a soft mesh gradient; the current web-first / AI-startup gradient idiom.
- **Full-bleed diagonal figure-ground split** — no discrete framed glyph; the black field and the colour field share one edge that does all the work.
- **Cover coherence:** the cover art reuses the exact ramp — a green ground with a green→amber→red heatmap overlay on the dashboard, black "Heat Scope" wordmark beside the same mark. Icon and brand palette are genuinely one system, not stock.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black the icon is a featureless squircle; the bolt exists *only* as an internal colour boundary, so the subject is not nameable from outer shape alone. (It does survive grayscale as a tonal split — see #7 — but that is figure-ground, not silhouette.)
- **#10 Variant robustness — FAIL.** The entire identity is the multi-hue thermal ramp; there is no separable foreground glyph layer. Under macOS 26 tinted/mono rendering the ramp collapses and the bolt — defined purely by colour contrast — loses definition. Not authored as Liquid Glass layers.

### Soft passes (flagged, scored as pass)
- **#1 Mask discipline** — composition is squircle-safe (full-bleed field), but the render bakes its own corner radius *and* an outer drop shadow; a clean macOS master should ship square, unmasked, shadow-free. Treated as a render artifact, not proof of the submitted asset.
- **#2 Grid adherence** — legitimately a full-bleed field (safe-zone exempt), but the bolt's optical mass sits low-left rather than optically centred.
- **#4 16px squint** — at 16/32px the dark-left / thermal-right colour story survives and stays distinctive, but the bolt notch smears; the icon reads by *palette*, not glyph, at Dock/Spotlight size.
- **#6 Palette economy** — 4-hue thermal ramp; passes only because it is a single subject-justified semantic ramp.
- **#9 Era coherence** — internally consistent, but it borrows Big-Sur squircle geometry while using none of that era's lighting/depth and none of Liquid Glass's material system. Reads web-first, not native to any current macOS era.

## Rhymes with
- Contemporary flat **mesh-gradient + grain** indie/SaaS marks (AI-startup gradient-blob icons; Raycast-adjacent dark-plus-gradient faces).
- Icons where a **bold negative-space glyph** is cut from a coloured field rather than drawn as a dimensional object.
- Style-family hint (leave for synthesis): "grainy-thermal-gradient, glyph-as-negative-space" — distinct from both the Big-Sur dimensional-tool family and the Liquid-Glass layered-glass family.

## Notes for synthesis
- Resolution caveat: 520×520 render, not a 1024 master; RGB, flattened on black with baked corner + drop shadow. Hex values are `(measured)` but from a downscaled render — treat as `(estimated)` if promoted. Grain reads intentional (uniform, matches the aesthetic) rather than as pure compression noise.
- This is the first (or an early) member of a possible **flat-gradient / grain** icon cluster — do not promote its conventions to canon on one icon. Its two failures (#3, #10) are exactly the risks of the whole family: gorgeous at hero size, weak at 16px and under tinting.
