# Icon: Uninstally

- **Era:** big-sur (unified squircle) — a coherent Big Sur-era mark shipping into a Liquid Glass world · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/uninstally/icon.png`, genuine 1024×1024 PNG, crisp — not a resized web render) · **Category:** Utility
- **Subject the icon must communicate:** a free macOS uninstaller that cleanly removes apps and their leftover files. The mark reaches for the **cleaning** half of that (broom + sparkles), not the removal/trash half — the cover carries the trash-can idea instead.

| Dimension | Reading |
|---|---|
| Background | **ramp** `#9E93F3` (top) → `#523DC6` (bottom), single violet/indigo hue (~252°), light-at-top "sky logic". Baked into a pre-shadowed squircle on a transparent canvas (corner alpha 0). `(measured)` |
| Glyph | **object — a broom** in flat white `#FFFFFF`, crossing the tile diagonally (handle tip upper-right ~x640,y300 → brush head lower-left ~x420,y660). 6–7 tapering bristle strokes fan from a banded collar. Optically balanced: brush weight lower-left, handle upper-right, sparkle cluster upper-left. `(measured)` |
| Overlay device | **diagonal tool** — the broom is the Big Sur "tool at an angle crossing the squircle" device (Apple's own TextEdit-pen / Preview-loupe tradition), here a besom. |
| Light model | **top-down ambient.** Background gradient lighter at top; **no specular, no glass edge highlight.** Glyph is a flat opaque sticker with **zero self-shadow / modelled light.** One baked soft drop-shadow sits *outside* the squircle (alpha ~23 below), emulating the system shadow. |
| Layer stack | baked outer drop-shadow → violet gradient squircle field → white broom glyph (diagonal) → three white four-point sparkles (upper-left). Glyph + sparkles share one flat plane. |
| Palette economy | **one hue family** (violet ramp) + neutral white glyph. No competing accent — disciplined. Saturation lives in the whole field rather than a focal detail (standard for a white-glyph utility mark). |

## Palette
- **Background top:** `#9E93F3` (158,147,243) — light periwinkle `(measured)`
- **Background mid:** `#6553DB` (101,83,219) — mid violet-indigo `(measured)`
- **Background bottom:** `#523DC6` (82,61,198) — deep violet `(measured)`
- **Glyph (broom + sparkles):** `#FFFFFF` (255,255,255) — pure white, flat `(measured)`
- **Accent:** none — the background ramp carries the only hue `(measured)`

## Signature devices
- **[GOLDEN-NUGGET] Diagonal broom as the Big Sur tool-at-an-angle.** The besom crossing the tile lower-left→upper-right is a direct quotation of Apple's canonical "a tool laid across the squircle" move (TextEdit pen, Preview loupe) — subject-mined for a cleaner, and the single choice that gives the mark its era-native posture.
- **[GOLDEN-NUGGET] Sparkle trail (the "sparkle-clean" motif).** Three four-point stars scaling large→small trail off the brush into the upper-left negative space — the shorthand for "magically clean" that appears across the cleaner-utility category. It is the personality lift on an otherwise expected broom.
- **Monochrome-white glyph on a single-hue saturated field** — no second colour competes; the whole identity is one violet ramp plus white.

## Failures
- **#1 Mask discipline — FAIL.** The squircle **and** its drop-shadow are baked into the artwork on a transparent canvas rather than delivered as a full-bleed square for the system to mask and shadow. Under macOS 26/HIG ("provide square, unmasked layers; don't bake drop shadows — the system applies them") this double-shadows and risks a corner-radius mismatch when Tahoe re-masks it. Era-correct for Big Sur, non-conforming now.
- **#10 Variant robustness — FAIL.** The white glyph depends entirely on the violet field for contrast, and the mark is a single flat raster — not authored as separable Icon Composer background/foreground layers. It cannot generate legible dark / clear / tinted variants: strip or neutralise the background and a white broom is invisible on light. Both failures resolve the same way — re-author as square unmasked background + foreground glyph layers.

### Soft passes (flagged, scored as pass)
- **#4 16px squint — soft.** The bold broom silhouette survives as "a broom on violet," but the 6–7 thin bristle strokes and their gaps merge into a paddle, and the two smaller sparkles vanish; only the gestalt + largest sparkle hold at menu-bar size. Graceful degradation, but the bristle articulation is lost detail.
- **#8 Depth coherence — soft.** Only two planes (field + flat glyph). No micro-shadow under the broom, so the glyph reads as a pasted sticker rather than the 2–3 lit planes typical of the Big Sur era — coherent, but flatter than the era's depth convention.
- **#2 Grid adherence — soft.** Optically balanced across the diagonal, but the broom is large and its handle tip runs close to the upper-right safe-zone margin; balance is carried by the sparkle cluster counterweight rather than by centring.

## Rhymes with
- **Cleaner / maintenance utilities** (CleanMyMac-lineage) — broom/sparkle "sweep it clean" marks on a saturated field.
- **Big Sur diagonal-tool squircles** (TextEdit, Preview) — the tool-across-the-tile device, quoted for a modern indie utility.
- **Single-hue-ramp + white-glyph utility icons** — one violet/indigo gradient tile carrying a flat white object; a candidate cluster if 2+ more appear.

## Notes (resolution & synthesis)
- **Resolution:** genuine 1024×1024 PNG with crisp edges — flat/gradient hex values are reliable, geometry trustworthy. Not a macapp.supply web-resize.
- **Authoring caveat (load-bearing for synthesis):** the icon **bakes the squircle mask + drop-shadow** (corner alpha 0, outer shadow alpha ~23). This is the Big Sur convention that macOS 26 HIG explicitly discourages; it is the root of both rubric failures and the clearest "authored before Liquid Glass" tell in the corpus so far.
- **Brand coherence is strong.** The same violet (~`#6B4FE0`) is the app's accent across the cover — the headline highlight ("completely"), every feature glyph, and the trash-can's rim glow. The icon is a faithful brand mark. Note the split: the **icon** says *broom + sparkle* (cleaning), the **cover hero** says *trash can full of app icons* (removal) — two metaphors for one product; the icon chose the friendlier one.
- **Metaphor caution:** broom-for-cleaner is a category-expected choice (template-adjacent); the sparkle trail and the era-native diagonal posture are what keep it from reading as generic glyph-on-gradient.
