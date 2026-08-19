# Icon: Compresto

- **Era:** Custom (flat monochrome brand-mark on a modern uniform squircle) — borrows the Big Sur–era squircle *container* but abstains from every era material signature: no gradient, no baked lighting, no glass · **Rubric:** 11/12 (4 soft passes, 1 hard failure #10) · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, **850×850** web render, delivered **pre-masked** (squircle already cut, corners transparent, ~12px feathered/antialiased edge; no strong baked drop-shadow in the pixels — the shadow you see on a white page is viewer compositing). Full-bleed 1024 unmasked Icon Composer master **not seen**; treat the mask as the site's render, not verified ship layers.
- **Subject:** batch media compressor — "compress videos, images, GIFs, and PDFs without noticeable quality loss." The mark encodes *compression* as an inward pinch to a narrow waist.

| Dimension | Reading |
|---|---|
| Background | **Flat `#171717`** (warm-neutral near-black, 23/23/23) — no ramp, no hue, no lighting. A single solid field |
| Glyph | Abstract — one large **concave-sided four-pointed "pinch-star"**: four arms sweep to the corners (up-left/up-right/down-left/down-right) and pinch to a narrow dark central waist. Off-white `#F2F2F2` (242/242/242, deliberately not pure `#FFF`). Optically **dead-centred**: glyph bbox centre (424,424) vs canvas centre (425,425). Wide stance — 557px W × 421px H (~1.32:1), ~65% of canvas width |
| Overlay device | None (no diagonal tool, badge, or frame) |
| Light model | **None — fully flat.** Two-tone vector fill, no gradient, no cast/inner shadow, no specular. Consistent by absence of any light source, not by a modelled one |
| Layer stack | back → front: [1] flat `#171717` squircle field · [2] flat `#F2F2F2` pinch-star glyph. Coplanar — two fills, **zero depth separation**. (Render adds the squircle mask; corners transparent.) |
| Palette economy | Extreme — **achromatic, 0 hue families**, 2 tones total, no accent. Figure-ground contrast `#F2F2F2`↔`#171717` = **16:1** (WCAG), survives grayscale trivially (it *is* grayscale) |

## Signature devices
- **The concave "pinch-star" — compression rendered as geometry.** Four concave arms squeezed toward a hollow central waist is the app's whole thesis in one shape: matter pushed inward, volume reduced, a narrow middle where the file "gets smaller." This is genuine subject-mining, not a stock glyph — a committed direction, not a template default `[GOLDEN-NUGGET]`.
- **Logo-first achromatic treatment.** Pure `#171717`/`#F2F2F2`, off-white over warm-neutral black. The icon behaves like a brand wordmark's monogram, not like a macOS utility icon — it rejects the entire gradient/depth/glass vocabulary the platform offers.
- **Hollow negative-space waist.** The dark field reads *through* the middle of the mark; the pinch is defined by absence, which is what makes the "squeeze" legible.

## Failures
- **#10 Variant robustness — HARD FAIL.** Single flattened bitmap with no authored background/foreground separation, so the system cannot derive proper dark/clear/tinted renders in the Liquid Glass era. Worse, the field is **near-black (`#171717`)**: against a dark Dock in Dark mode the squircle edge risks dissolving into the background, and a flat two-tone gives the tinted/clear modes nothing to composite. The glyph *is* dependent on the one dark background colour — exactly what the check penalises.
- **4 soft passes** (the score never travels without the asterisk):
  - **#1 Mask** — clean continuous-corner squircle, artwork well inside the safe zone, but delivered **pre-masked with transparent corners**, not the HIG-required square unmasked layer. Fine as a shipped render, unverifiable as authoring hygiene.
  - **#3 Silhouette / subject-nameability** — the silhouette is *crisp and memorable* (a distinct four-pointed concave star), so it passes as a mark. But the **subject is not nameable**: filled solid, no one reads "video/image compressor." The pinch→compress metaphor is only legible in hindsight, once primed. This is the icon's central tension — strong silhouette, weak function-communication.
  - **#5 Light model** — passes only because "flat" means no *conflicting* lights; there is no light model at all. Zero of the platform's dimensionality.
  - **#8 Depth** — trivially coherent (one plane) but wears the modern squircle while skipping all depth. Reads intentionally flat, not accidentally — so a soft pass, not a defect.

## Rhymes with
- **Flat monochrome brand-mark-on-squircle family** — logo-first, achromatic, depth-free marks that port a company's wordmark glyph onto a macOS squircle rather than authoring a native layered icon (the Vercel-triangle / Linear-monogram register, ported to the Dock). No exact digested peer yet; log as the seed of a probable **"flat achromatic logo-mark"** icon cluster once ≥2 more arrive.
- **Glyph-shape rhyme with Cachesweep** — Cachesweep's `sparkles` are also *concave-sided four-pointed* forms; Compresto is the same concave-star geometry scaled to a single dominant mark. Shape-language rhyme only — Cachesweep is blue-gradient + multi-sparkle, Compresto is flat-black + single-star. Worth watching whether "concave four-pointed star" is becoming a recurring corpus device.
- **Palette coherence with the app — deliberately absent.** The cover shows a warm floral-meadow wallpaper, a frosted cream glass panel, and a **macOS system-blue (`~#0088FF`) "Compress" CTA** — that blue is the app's real accent. The icon shares *nothing* with it: a stark achromatic mark fronting a warm, colourful, blue-accented UI. Icon↔UI are two separate palettes; the brand discipline is "monochrome logo stands apart," not "icon and UI are one system."
