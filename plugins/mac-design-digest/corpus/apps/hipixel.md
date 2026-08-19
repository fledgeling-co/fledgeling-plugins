# HiPixel — profile

- **Source:** macapp.supply (`sources/hipixel/`) · **Surfaces digested:** none (no app UI present — icon + marketing cover only) · **Last updated:** 2026-07-19
- **One-sentence identity:** A free/open-source AI image-upscaler whose entire visual identity is a single before/after comparison-slider (pixel-mosaic ↔ Van Gogh's *Starry Night*, split by a yellow diagonal), carried verbatim from a Big-Sur-era app tile into a full-bleed marketing cover — concept-as-brand, in the register of Topaz/Pixelmator-style "look what it fixes" upscaler marketing.
- **Cluster:** unassigned (no UI evidence to place it)
- **Lineage:** unknown (low) — **cannot be classified**: no window chrome, controls, or content surface is visible in either supplied image. The tagline claims "Native … for macOS" but marketing copy is not design evidence. Nothing here may feed macOS canon.
- **Era (chrome):** icon reads **Big Sur-era app tile (2020–2024)** — rounded-rectangle squircle on the standard ~80% grid, glossy raised white bezel, soft realistic drop shadow. **Not** Liquid Glass / Icon Composer (no layered translucent glass, no specular parallax, no Mono/Tinted treatment visible).

> ⚠ **This is not a UI digest.** Workflow A was requested, but the source contains no app UI surface. Everything below is icon-anatomy and marketing-brand evidence. The UI corpus gains no native-surface tokens, no lineage, no pattern evidence from HiPixel. To digest HiPixel's actual UI, supply screenshots of the app window (drop zone / queue / before-after viewer / settings).

## Tokens

All tokens are icon or marketing-brand values — none are app-UI tokens. Hex `(measured)` by pixel sampling (icon composited over white; it ships with a transparent shadow gutter).

| Token | Value | Provenance | Notes |
|---|---|---|---|
| icon/grid-occupancy | opaque body 50–461px in 512 canvas = **80.3%** of edge | (measured)(inferred) | Matches Big Sur icon grid (824/1024 ≈ 80.5%) — shape geometry is platform-faithful |
| icon/frame | cool blue-white raised bezel; top highlight `#FFFFFF`, lower/side `#BAC0E1`→`#D5D9EA` | (measured)(inferred) | Top-lit glossy bevel = Big Sur photo-frame material, not flat |
| icon/blue-ramp (pixel side) | navy `#265387` → royal `#2A6CB4` → sky `#75B7F5` | (measured)(inferred) | 3-step blue ramp forming the low-res "before" mosaic |
| icon/accent-divider | saturated warm yellow ~`#EFCE1E` (est.) | (estimated)(inferred) | Diagonal comparison-slider line; the one warm hue against an all-blue field |
| icon/painting-side | *Starry Night* blues + pale moon `#EEEFC4` | (measured)(inferred) | Photographic/illustrative full-bleed fill of the "after" half |
| brand/headline-type | high-contrast serif (Times/Didone-class), white, ~italic-leaning wordmark | (estimated)(inferred) | Cover headline "HiPixel — Make Your Images Crystal Clear" |
| brand/headline-pill | frosted-glass rounded capsule, translucent cool-grey `~#586C85` over the art | (estimated)(inferred) | Marketing chrome (not app chrome); blurred backdrop, soft border |
| brand/cover-motif | full-bleed before/after: left mosaic `~#202B47`, right sharp painting | (measured)(inferred) | The product's single idea blown up to fill the frame |

## Layout skeletons

No app-UI surfaces to skeleton. For completeness, the two brand artifacts:

- **cover.jpg (2400×1260, marketing composite):** full-bleed before/after split (pixelated left half ↔ *Starry Night* right half) as background; the app icon floated dead-center, ~400px, slightly above the vertical midline; a frosted-glass headline capsule in the lower third spanning the middle. Device-frameless. This is brand evidence, not window evidence.
- **icon.png (512×512, app tile):** squircle on ~80% grid → raised white beveled frame → inset rounded image tile (concentric corner) → before/after fill divided by a diagonal yellow slider.

## Signature moves

- **[GOLDEN-NUGGET] The comparison-slider as the whole brand.** The pixel-mosaic ↔ *Starry Night* split, cut by a yellow diagonal, is not just the icon — it is scaled up to *become* the entire marketing cover. One product idea (upscaling = blurry→crisp) expressed identically at 16px and at 2400px. This is unusually disciplined concept-coherence and is HiPixel's entire recognizable identity. It demonstrates value rather than describing it (the visual before/after does the persuading).
- **Single warm accent in an all-blue field.** Every surface is blue except one saturated yellow line (icon divider) and the pale moon — the yellow is the only Von-Restorff element, and it reads as "the seam where bad becomes good."

## Defects

- **Photographic full-bleed inside a heavy bezel (icon construction).** The icon stuffs a full illustrative image into the tile behind a thick raised white frame. Current HIG guidance ("match, don't reproduce"; avoid photographs and heavy inner bezels; Liquid Glass wants a simple layered glyph) treats this as a dated construction. Canon icon would use a bold, simple glyph of the before/after idea, not a shrunk painting.
- **16px squint-legibility risk.** At Dock/Spotlight sizes the pixel-vs-painting distinction and the thin yellow diagonal collapse toward "a blue square with a yellow streak." The concept that carries the cover does not survive down to 16px — the opposite of the icon design imperative (icons live or die at Dock/Spotlight sizes).
- **Register mismatch (brand, not defect-in-craft).** The cover's high-contrast serif in a frosted-glass pill signals *editorial/premium*, which sits in tension with the "free and open source" utilitarian positioning. Noted as a positioning observation, not a measurable flaw.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| (none — no app UI) | n/a | The 14-point UI rubric and 10-point native-tells audit require a UI surface; none present. Icon assessed via icon-anatomy notes above, not scored here (Workflow A was requested; icon canon is Workflow B). |
