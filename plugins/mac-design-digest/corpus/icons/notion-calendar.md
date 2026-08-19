# Icon: Notion Calendar

- **Era:** Custom (flat monochrome brand-mark-as-icon — belongs to no macOS icon language: **not** Big Sur squircle, **not** Liquid Glass, **not** skeuomorphic rendering; motif quotes the classic wall-calendar / Apple Calendar "31" date-page) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply web render, `icon.webp` 204×204px — a small resized render, not a 1024 master. Corner/edge AA and any true squircle radius can't be assessed at this size; readings below are honest to what 204px shows (upscaled to 512 for inspection). Pixel-sampled to confirm the palette.

| Dimension | Reading |
|---|---|
| Background | **None — fully transparent** (all four corners + edges alpha 0, measured). No background field, no squircle fill; two black cards float free on the wallpaper. This is the load-bearing anomaly of the icon. |
| Glyph | **Object + numeral:** two stacked black rounded-rectangle cards (a back card offset up-left, a front card down-right), each ringed by a white keyline; the front card carries a white date field with a heavy black **"31"** — the canonical calendar date-page glyph. Pure `#000000` and `#FFFFFF` only (measured; edge greys are AA). "31" optically centred within the front card. |
| Overlay device | None — no diagonal tool, no badge. The *stacking offset* is the only compositional device. |
| Light model | **None.** Flat, zero lighting: no top-down gradient, no cast shadow, no specular, no glass. Depth is implied purely by card offset + the white keyline reading as the gap between stacked pages ("sticker" depth). Consistent by absence — nothing to be inconsistent. |
| Layer stack | back black card (white keyline) → front black card (white keyline) → white date field → black "31" numeral (front) |
| Palette economy | 0 hue families — pure achromatic. Black `#000000` + white `#FFFFFF`, **no accent**. Maximal contrast (21:1 internal), maximal austerity. |

## Signature devices
- **Stacked-cards depth without a shadow** — two offset rounded rectangles separated by a white keyline read as a stack of pages/events. Depth carried entirely by overlap + outline, never by lighting. `[GOLDEN-NUGGET]`
- **Monochrome brand-mark-as-icon** — the entire saturation budget is zero; the app's identity is the *restraint*. This is a flat vector logo dropped onto the app-icon slot, not a macOS-era icon.
- **Apple-Calendar "31" quotation** — the heavy date numeral on a page is the universal calendar glyph (and a direct nod to Apple's own Calendar icon), stripped to black-and-white. Subject-mining: the icon says "calendar" the instant you read the "31."

## Failures
- **#1 Mask discipline (FAIL):** artwork is a free-floating silhouette on transparency, not designed for the squircle. It fights the system mask — on macOS 26 it either floats unmasked (non-native, Electron/cross-platform tell) or would be crudely masked with no background field. There is no full-bleed layer for the system to round. Non-negotiable check, failed.
- **#10 Variant robustness (FAIL):** built entirely on black-on-transparent. In dark mode the black cards vanish into a dark wallpaper/Dock; a tinted or clear render would flatten the whole thing to one tint and destroy the black-card / white-keyline separation. Not an Icon Composer layered composition; no authored Default/Dark/Clear/Tinted variants.

## Soft passes (borderline — scored pass, flagged for synthesis)
- **#2 Grid adherence:** the "31" is optically centred within the front card, but with no squircle canvas there is no safe-zone/margin discipline to speak of — the mark floats with transparent bleed. Internal centring passes; canvas-level grid is absent.
- **#3 Silhouette test:** filled solid black, the white keylines and "31" vanish, leaving two overlapping rounded rectangles = "a stack of cards." Reads as a stack, but the *calendar* identity lives in the negative-space "31," not the outer silhouette. Passes as a stacked-object read; flagged that the subject cue is interior, not silhouette.
- **#4 16px squint:** the heavy "31" survives at menu-bar size thanks to maximal black-on-white contrast (verified on a 16px downscale). Risk: on a dark background the two black cards merge into one blob with no containing shape — legibility is background-dependent, not self-contained.
- **#5 Single light model:** passes vacuously — there is *no* lighting model at all, which is itself off-era for macOS (Big Sur wants soft top-down; Liquid Glass wants environmental). Flat by commitment.
- **#7 Figure-ground contrast:** internal contrast is maximal (21:1). Card-vs-background is contingent on the wallpaper because there's no self-contained field — excellent on light grounds, fails on dark. Scored pass on the internal reading, caveated.
- **#12 no-text:** "31" is numerals, but it functions as the canonical calendar date glyph (as on Apple's Calendar icon), not a word/label — the accepted calendar convention, noted for completeness.

## Rhymes with
- *(hint only)* Flat **monochrome brand-mark** icons that ignore the squircle and float a free silhouette on transparency — the logo-as-app-icon / cross-platform (Electron) delivery family, adjacent to Notion's own black-and-white house system. Style family: austere achromatic wordless brand marks. Also rhymes with any "calendar date-page / '31' quotation" icon. Confirm against future digests before clustering.

## Provenance / caveats
- All hex `(measured)` from the 204px render (pixel-sampled: only `#000000`, `#FFFFFF`, and AA greys present); `(inferred)` — single icon, single source.
- Transparent free-silhouette + zero lighting + Electron heritage (Notion Calendar descends from **Cron**, an Electron app) is a coherent set of **non-native tells** — this icon does not feed macOS icon canon. [Inference]
- **Brand-coherence with `cover.png`:** high. The cover reuses the *identical* black stacked-"31" mark, wordmark "Notion Calendar" in black, on a warm off-white ground (~`#F5F3EF`). The icon *is* the brand mark verbatim, so icon↔brand palette coherence is total (achromatic throughout); the cover's surrounding pastel doodle icons are decoration, while the product mark itself stays strictly black/white.
