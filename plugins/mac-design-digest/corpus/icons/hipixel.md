# Icon: HiPixel

- **Era:** Big Sur unified (non-conforming — baked shadow + non-full-bleed frame) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512, alpha) — Photography category · free/open-source native AI image upscaler
- **Subject fit:** the icon *demonstrates the app's function* — a before/after upscaling comparison (pixelated left, high-fidelity right) split by a diagonal comparison-slider divider. Subject-mined: the "after" half is Van Gogh's *The Starry Night*, tying the app to art-restoration/detail-recovery.

| Dimension | Reading |
|---|---|
| Background | No field — a floating glossy **white/silver bezel** `#E8EAED`→`#DDE0EF` (cool-lavender white) on a transparent canvas with a **baked** soft drop shadow. Corners fully transparent (alpha 0); artwork fills only the central ~80% (opaque 50–461 of 512), so it does **not** full-bleed the squircle. `(measured)` |
| Glyph | Scene/object hybrid: a **split before/after image** inside the frame. Left "before" = a blocky blue pixel-grid ramp `#244D86` → `#2A6CB4` → `#60C5FF`. Right "after" = *Starry Night* brushwork (navy → cyan `#ACE8F7`, moon golds). Optically centred; divider left-of-centre so "after" occupies the larger right two-thirds. `(measured)` |
| Overlay device | **Diagonal comparison divider** — a bright pure-yellow line `#FFFF66`, gently raked ~5° off vertical (top x≈209 → bottom x≈234). The one device doing all the semantic work. `(measured)` |
| Light model | Top-down: specular sheen along the bezel's top edge, baked soft drop shadow beneath (consistent). Interior is a **photographic/painterly bitmap** — self-lit content, no modelled form light (mild mixed-lighting tension). `(estimated)` |
| Layer stack | baked drop shadow → glossy white rounded-rect bezel → before/after bitmap (pixel-grid ‖ Starry Night) → yellow diagonal divider → top-edge bezel gloss. `(estimated)` |
| Palette economy | Disciplined: **one hue family (blue)** across both halves + **one accent (yellow)** on divider/moon + white bezel. Accent reserved for the focal divider. `(measured)` |

## Signature devices
- **[GOLDEN-NUGGET] The literal before/after split** — the app's entire function stated in one image: low-res blocks on the left resolve into brushstrokes on the right. Genuinely nameable and category-appropriate; this is where the icon's taste lives.
- **Diagonal comparison-slider divider** in shouting `#FFFF66` — the classic image-diff UI handle, borrowed into the icon to sell "transformation" and to force figure-ground where the two blue halves would otherwise blur together.
- **Subject-mining Van Gogh** — *The Starry Night* as the demo image reads as "we recover the detail of a masterpiece," a committed choice over a generic sample photo.
- **Glossy white photo-frame bezel** — a dated skeuo-lite gloss "picture frame" wrapping the sample (rhymes with pre-Big-Sur image-utility icons).

## Failures
- **#1 Mask discipline** — FAIL. Floating white rounded-rect with **baked** drop shadow on a transparent canvas; corners are alpha 0. Under the system squircle mask it reads as a sticker, and the baked shadow doubles the system's own shadow. Should be a full-bleed, unmasked, shadow-free square.
- **#3 Silhouette** — FAIL. Filled solid black it is an anonymous rounded rectangle; the entire before/after story lives in interior texture, so the silhouette carries zero meaning.
- **#4 16px squint** — FAIL. The pixel grid, the thin divider, and the Starry Night brushwork all smear into a blue-and-yellow blur at Dock/Spotlight size — the concept vanishes. Ironic for an upscaler: the icon is built from exactly the high-frequency detail that dies when downscaled.
- **#10 Variant robustness** — FAIL. A photographic/painterly interior cannot survive dark/clear/tinted/mono renders; a monochrome tint collapses both halves into one tone and destroys the comparison. (Era-appropriate for Big Sur, but a real weakness in the current Tahoe/Liquid-Glass regime of system-generated variants.)

**Soft passes (scored pass, flagged):** #2 grid (centred but split is asymmetric, divider left of centre); #5 light (bezel top-lit consistently, but interior bitmap has its own unrelated lighting); #7 figure-ground (the two halves are *both* blue — separation depends on texture + the loud yellow divider, not tonal contrast); #8 depth (sensible 2-plane stack, but the baked shadow z-fights the system shadow); #9 era (Big Sur front-facing squircle intent executed with flat-transition-era baked-shadow / floating-frame habits — not a clean single-era language).

## Rhymes with
- The **"sample-image-in-a-glossy-frame"** family — older image/photo-utility icons that wrap a demo picture in a white bezel rather than committing to a squircle field.
- **Before/after / split-screen demo** icons (comparison-slider tools, retouch/restore utilities) — the divided-canvas + diagonal handle device.
- Awaiting ≥2 more Photography/image-tool icons to test whether "demonstrate the function literally inside the frame" is a category convention or a one-off.
