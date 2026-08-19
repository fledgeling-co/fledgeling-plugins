# Icon: Compressor

- **Era:** skeuomorphic-quote (photoreal soft-3D object on alpha) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (sonnylab.com) · **Category:** Utility · **Subject:** app that turns images into lightweight WebP files
- **Resolution caveat:** 598×598 PNG with alpha — a downsampled web render, well below the 1024 master. Fine-detail and 16px behaviour are *inferred* from a 60px downsample, not measured at delivery sizes.

## One-line read
A reusable translucent silicone food-pouch (Stasher-style), pink zip-clip at the top, packed with fresh fruit (strawberry, blueberries, halved apple), floating as a cut-out object on transparency. The metaphor: *store food smaller while keeping it fresh* → *compress images smaller while keeping quality*. The cover tagline cashes the pun literally — "Smaller images. Same good taste."

| Dimension | Reading |
|---|---|
| Background | none — transparent alpha cut-out; no designed background field (composites onto system white). No squircle mask authored. |
| Glyph | object — a literal food-storage pouch. Optically centred but weighted right by the protruding zip-clip tab. Free silhouette, not mask-designed. |
| Overlay device | none (no diagonal tool, badge, or frame) |
| Light model | single soft top-front studio key; one short soft contact shadow down-and-right; glossy speculars baked on fruit + pink silicone; subsurface translucency on the bag wall. All lighting **baked in** (HIG says let the system apply effects). |
| Layer stack | contact shadow → rear bag wall → fruit mass (strawberry / blueberries / apple) → front translucent bag wall + sheen → pink zip band → pink clip tab |
| Palette economy | 4–5 hue families (rose-pink, strawberry-red, leaf-green, blueberry-navy, apple-cream/red) + translucent white — well over the ≤2-family guideline. Photoreal-fruit inherently blows the budget. |

## Palette (estimated from a downsampled render)
- **Bag body:** warm translucent near-white `#F7F4F1` → shadowed `#E6E1DC`; edge defined by shadow, not colour.
- **Pink zip + clip:** `#F0A8BC` mid, highlight `#F8CAD7`, shadow `#DD8AA2` — the one near-brand saturated moment.
- **Strawberry:** `#D22E24` → highlight `#E85A44`; pale-yellow seed speckles.
- **Leaf/stem:** `#6FA03C` → shadow `#4E7A2A`.
- **Blueberries:** `#2F3B58` navy → dusty bloom highlight `#6B7A94`.
- **Apple:** flesh cream `#F4E8CE`, skin red `#C63A2E`, seeds brown `#6B4A2A`.
- **Brand accent (from cover, not the icon):** coral-red ~`#F0563C`. The icon carries *no* coral — its nearest note is the deeper, warmer strawberry-red, and its dominant colour (rose-pink) is off-accent. Palette coherence icon↔brand is loose.

## Signature devices
- **[GOLDEN-NUGGET] The freshness-pouch metaphor** — a food-storage bag as the emblem for "compress but keep the quality." Genuinely subject-mined, non-template, memorable. This is the icon's entire soul; it earns Personality (#11) outright.
- **Translucency window** — the fruit is read *through* the front bag wall via subsurface transparency; the one place the render's craft is real depth, not decoration (#8 depth coherence passes on this).
- **Pink zip-clip as the single saturated anchor** — everything else is either translucent-neutral or fruit-local colour.

## Failures
- **#1 Mask discipline (fail)** — authored as a free-floating cut-out on alpha, iOS-sticker / App-Store-render logic. No background layer fills the squircle; since macOS 26 normalises away custom silhouettes, this either floats on auto-white or needs a system backdrop it wasn't designed with.
- **#4 16px squint (fail)** — the load-bearing detail (individual blueberries, apple seeds, strawberry) is exactly what smears to a colour mass at menu-bar/Spotlight size; the icon degrades to a pale pouch with a pink cap, and the app's meaning is entirely gone. On a light Dock the near-white body loses its edge (only the drop shadow separates it).
- **#6 Palette economy (fail)** — 4–5 hue families; the photoreal fruit can't be spent within the ≤2-family budget.
- **#10 Variant robustness (fail)** — no separable background/foreground layer model (not Icon Composer-authored); a dark / clear / tinted-monochrome render of a translucent fruit bag would be illegible. Composition depends on a light ground + the object's own colours.

## Soft passes (scored pass, flagged)
- **#2 Grid** — optically centred but the clip tab pushes weight right of centre; no real grid, being free-form.
- **#3 Silhouette** — nameable as *a pouch*, yes — but as a shape it reads as a food bag, never as "image compressor." Subject-communication is oblique; it leans on brand/tagline knowledge.
- **#7 Figure-ground** — the translucent silicone body is near-white and sits below 3:1 against a light canvas; it survives on the fruit mass + pink cap + drop shadow, not on body contrast.
- **#12 No-text** — free of words/UI, but the photoreal render leans into the *photographic* character the check (and HIG: "prefer illustrations to photos") discourages.

## Rhymes with
- The **photoreal soft-3D object-on-alpha** family — Blender/Spline product renders, App-Store-style literal-object icons floating on white. (Cross-check against other object-render icons already in the corpus for a cluster.)
- The **classic skeuomorphic literal-object** tradition (a real thing, photoreal materials, free outline) — quoted with modern clean studio rendering rather than felt/leather grunge.
- *Not* the Big Sur squircle family, and *not* Liquid Glass — it shares neither the mask nor the layered-glass model.

## Note for synthesis
Beautiful, characterful, and genuinely subject-mined — yet authored to web/iOS-render conventions, not macOS platform conventions. It trades all four system-facing checks (mask, 16px, palette economy, variant robustness) for one strong conceptual metaphor. If ≥2 more object-on-alpha photoreal renders land, this is a cluster worth naming ("product-render object icons") — with a standing caveat that the register wins Personality and loses Dock/Spotlight duty.
</content>
</invoke>
