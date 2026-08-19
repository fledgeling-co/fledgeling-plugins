# Icon: Fantastical

- **Era:** Big Sur unified (with a light skeuomorphic quote — the red header band) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, 102×102 web render — upscaled 5× for inspection; no @2x/1024 master) · **Category:** Productivity (calendar)

| Dimension | Reading |
|---|---|
| Background | Scene — full-bleed white calendar page (faintly cool `#F9F8FD` (measured)) crowned by a red header band, ramp `#F44B42` (top) → `#EE2502`/`#F22902` (bottom) with a baked dark shadow line `#C05043` onto the page (measured, 102px). Near-invisible light-gray gridlines (~`#F5–#F9` on `#FFF`, ~2% darker — subliminal at this size). |
| Glyph | Abstract — four soft-focus rounded-square event tiles scattered on the grid: green `#00E400`, amber/yellow `#FFBF01`, cyan/blue `#00ACFE`, magenta `#F85AE1` (measured). Each carries a gaussian bloom + short drop shadow → reads as slightly defocused stickers floating above the page. Not on the Apple grid — placement is calendar-metaphor scatter, weighting slightly bottom-right. |
| Overlay device | None (no diagonal tool, no badge, no frame). |
| Light model | Soft top-down. Red band lit at top, deepening to shadow at its lower lip; event tiles get a soft short drop shadow + bloom. No specular glass highlights, no refraction. |
| Layer stack | back → front: (1) white calendar page + ghosted gridlines; (2) red header band with baked under-shadow; (3) four bloomed multicolor event tiles with drop shadows. |
| Palette economy | **5 hue families** (red header + green/yellow/blue/magenta tiles) — far past the ≤2 rule. Deliberate: multicolor *is* the subject (color-coded calendars). Red is the brand accent (matches the red "cal" in the Fantastical wordmark, ~`#F43725`). |

## Signature devices
- **Red header band over a white page** — a wall/desk-calendar skeuomorphic quote used as the whole brand anchor; it is the one element that survives the 16px squint. `[GOLDEN-NUGGET]`
- **Scattered soft-focus multicolor event tiles** — gaussian-bloomed rounded squares standing in for color-coded entries; the "multicolor-as-subject" move (rhymes with Photos/App Store), not a single glyph. `[GOLDEN-NUGGET]`
- **Ghosted gridlines** — a grid rendered ~2% darker than white, reading as faint texture rather than structure; disappears entirely at small sizes by design.

## Failures
- **#3 Silhouette test** — filled solid black, the icon collapses to a featureless squircle; the red band, grid, and tiles all vanish. It is named through *color + internal structure*, never shape. This is an archetype trait of full-bleed scene icons (Calendar, Photos), not sloppiness — flag when comparing against single-glyph tool icons.
- **#6 Palette economy** — 5 saturated hue families vs the ≤2 rule. Purposeful (calendar color-coding) so it's a signature, but it *is* a rule break: recorded as failure-with-intent.
- **#7 Figure-ground contrast** — measured, all four event tiles fall **below the 3:1 floor on white**: yellow 1.65:1, green 1.74:1, blue 2.52:1, magenta 2.78:1 (only the red band clears it at 3.87:1). The saturated-fill-on-white choice trades contrast for cheer; separation is rescued only by the soft drop-shadow edge, not by luminance. Genuine weakness.
- **#10 Variant robustness (Liquid Glass)** — the composition depends on a white ground + multicolor; it is not authored as glass layers and would not translate to tinted/dark/clear renders. Expected — this is a pre-Liquid-Glass Big Sur icon.

## Soft passes (counted as pass, flagged)
- **#2 Grid adherence** — no centered glyph to grid; it's a scene-fill. The page fills the safe zone correctly and reads balanced, but the tile scatter loads the bottom-right slightly.
- **#4 16px squint** — the four tiles blur into indistinct dots and gridlines vanish, but the red-band-over-white gestalt survives and still reads "calendar."

## Rhymes with
- Apple **Calendar** — the red-header-over-white metaphor and date-page archetype (closest peer).
- **Photos / App Store** — multicolor-as-identity scene icons that name themselves by hue, not silhouette.
- Style family: full-bleed Big Sur *scene* icons that spend their whole personality on color and a metaphor object, deliberately failing the solid-silhouette + palette-economy rules that single-glyph tool icons must pass.
