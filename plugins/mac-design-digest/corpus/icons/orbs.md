# Icon: Orbs

- **Era:** Big Sur unified (front-facing squircle, top-down baked light) — with a deliberate **Aqua/skeuomorphic gloss quotation** as its material · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, SHA-1 `4ab68048`) · **App:** Orbs — a native macOS radial-wheel launcher ("Ten apps. One orb. Hold ⌥, flick, release.") · orbs.studio
- **Resolution honesty:** 512×512 web render (half the 1024 master) with a **baked drop-shadow on a white plate** — i.e. an exported composite, not the delivered unmasked square layer. Palette hexes are clean `(measured)` within the render's tone; the true mask edge and whether the shadow is system-applied vs baked cannot be verified from this export.

| Dimension | Reading |
|---|---|
| Background | Flat pure black `#000000` `(measured)` full-bleed squircle field — opaque, no ramp, no translucency |
| Glyph | Abstract concentric **orb** (annular ring + recessed disc), optically centred, ~330–360px diameter on 512 canvas (~18% side margin) — round-glyph sizing, well inside safe zone |
| Overlay device | None (no diagonal tool, badge, or frame) — the glyph *is* the whole composition |
| Light model | Single **top-down** source; broad **baked specular cap** blown to `#FDFDFD` across the top third of the metallic ring, flaring slightly over the inner boundary; convex glossy ring, concave dark well below |
| Layer stack | back→front: (1) black squircle field `#000000` → (2) brushed-silver annulus, vertical gloss ramp `#FDFDFD`→`#7E7E7E` + baked top specular → (3) recessed near-black inner disc, top-lit `#1F1F1E`→`#0F0F10` (darkest at bottom) |
| Palette economy | **Zero hue families** — pure greyscale silver-on-black. No saturated accent (deliberate). Figure carried entirely by the silver ring's luminance |

## Palette (measured)

- **Background field:** flat `#000000`
- **Metallic ring ramp (vertical):** specular `#FDFDFD` (top) → `#BFBEBE` (upper) → `#7F7E7D` / `#7E7E7E` (sides) → `#8C8B8C` (bottom, slight ambient lift)
- **Inner recessed disc:** `#1F1F1E` (top) → `#1C1C1C` (centre) → `#0F0F10` (bottom)
- **Accent:** none

## Signature devices

- **The glossy monochrome orb — an Aqua/chrome-sphere quotation inside a Big Sur squircle.** A blown-out specular cap on a brushed-silver annulus reads as a lit glass/chrome dome. This one material decision carries the entire personality; it is the brand mark ("One orb"), reproduced identically on the cover.
- **Concentric-ring composition that diagrams the product.** A radial/orbital launcher is a wheel of concentric rings; the icon literally is concentric rings — subject-mined, not a generic dot.
- **Zero-hue discipline.** Silver-on-black with no accent places it in the hardware / pro-tool register (camera aperture, record button, volume knob), matching the cover's austere black/white/silver system — high icon↔brand palette coherence.

## Failures

- **#10 Variant robustness (Liquid Glass era) — FAIL.** The figure is wholly dependent on the opaque black field (silver-on-black *is* the contrast). Baked specular + no glass layers + an opaque black background give Icon Composer nothing translucent to recompose; this icon will not produce proper Default/Dark/Clear/Tinted glass variants and reads as a legacy (pre-Tahoe) icon in a macOS 26 world.

## Soft passes

- **#3 Silhouette test — SOFT.** Simple concentric shape reads instantly, but its *identity* is tonal, not silhouette-borne: filled solid, the orb collapses to a plain disc/dot; the ring-vs-well depth that makes it an "orb" is carried by the gloss ramp, not by outline. Names as a generic "dot/target" without its tone — on-subject ("orb") but leaning on lighting to be itself.

## Rubric ledger (11/12)

Pass: #1 mask, #2 grid, #4 16px squint (grey annulus on black holds — reads as a camera/record dot), #5 single light, #6 palette economy (monochrome), #7 figure-ground (mid-grey `#7E` on `#000` ≈ 4–5:1; specular ~21:1), #8 depth coherence (convex ring / concave well, consistent), #9 era coherence (consistent Aqua-gloss quotation within Big Sur grammar), #11 personality (strong, committed), #12 no-text. · Soft: #3. · Fail: #10.

## Rhymes with

*(hint for synthesis — style-family guess, not a promotion)*
- Glossy monochrome **hardware-dot** family: camera/PhotoBooth aperture icons, webcam/record-button orbs, Aqua-era glossy button spheres, volume/knob hardware icons. Shares: single centred convex glossy disc, top-down baked specular, zero hue, dark field. Distinct from the Big Sur "diagonal-tool-on-gradient" mainstream — no tool overlay, no coloured ramp.
