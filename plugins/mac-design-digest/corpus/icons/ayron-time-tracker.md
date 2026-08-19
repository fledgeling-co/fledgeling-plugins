# Icon: Ayron Time Tracker

- **Era:** custom (flat brand logomark — adopts no Apple depth-era language) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 672×672 — a resized web render, not the 1024 master; flat colours compress cleanly so composition reads are reliable, but sub-pixel edge crispness a native 1024 asset would show is unverifiable)
- **Subject fit:** app turns "tracked time into reports, insights and invoices" (Productivity). The icon communicates *brand*, not *subject* — an "A" monogram, no clock/timer/stopwatch metaphor. Coherent with the app's identity system rather than its function.

| Dimension | Reading |
|---|---|
| Background | flat `#D6FF3A` — single value at all four corners and mid-field, zero gradient (measured); an acid/chartreuse "safety-vest" lime, full-bleed to the mask edge |
| Glyph | custom angular italic **"A" monogram**, near-black `#0C0C0C` (measured); bbox 391×314px on 672 canvas = glyph height ~47% of frame; horizontally biased ~18px left of geometric centre (correct optical comp for a right-leaning mass), vertically centred (top 26.3% / bottom 26.9%) |
| Overlay device | none — single flat glyph on a flat field |
| Light model | none — dead flat, no modelled light, no shadow, no specular. Internally consistent (nothing to contradict), but the *absence* of any depth is exactly what makes it read web-brand-first, not mac-native |
| Layer stack | back → front: (1) flat lime field `#D6FF3A`; (2) flat black "A" `#0C0C0C`. Two opaque planes, RGB mode, **no alpha channel** — no authored foreground separation |
| Palette economy | maximal: 1 hue family (yellow-green) + 1 neutral (near-black). Two colours total; contrast 17.0:1 (measured) |

## Signature devices
- **[GOLDEN-NUGGET] The rising-"A" double-read.** The monogram is built as a heavy right stem + a diagonal leg ascending from bottom-left to a sharp apex, with a triangular counter aperture. It reads simultaneously as the letter A *and* as an upward diagonal / mountain-peak / ascending line — a "time goes up, productivity climbs" metaphor smuggled into a letterform. This is committed subject-mining, not template glyph-on-gradient.
- **[GOLDEN-NUGGET] Acid-lime + black athletic register.** `#D6FF3A` on `#0C0C0C` is a sport/performance palette (think hi-vis running gear, energy-drink branding), deliberately loud and un-corporate. The cover site confirms it as the whole brand's committed direction (lime CTAs, lime "Invoice out." headline on black). Palette coherence icon↔app is total.
- **Angular, italic-slanted geometric letterform** — no curves, all straight cuts and hard terminals; the forward lean gives velocity.

## Failures
- **#10 Variant robustness — FAIL.** Single fully-opaque flat RGB raster, no alpha, no authored Default/Dark/Mono Icon Composer layers. The glyph is defined purely by colour contrast against the lime field — there is no separable foreground layer for the system to tint or invert. In macOS 26 tinted/clear/mono appearances the composition does not survive gracefully: the whole square tints as one plane and the "A" (which *is* the negative of the field) collapses. This is the icon's one real native-craft gap — it's a legacy web-logo-on-a-square, not an appearance-aware layered icon.

## Soft passes (borderline — flagged for synthesis)
- **#2 Grid adherence (soft).** Optically centred and safely inside the zone, but the glyph runs conservative — ~47% frame height with generous ~26% top/bottom margins. It's calmer/smaller than the grid's inner square permits; a bolder mark would command the Dock more. Deliberate breathing-room, not a defect.
- **#4 16px squint (soft).** The heavy mass and single triangular counter survive at menu-bar size, but the fine apex tip and the narrow crossbar aperture partially close/soften at 16px. Reads as an A/wedge; loses its crispest letterform detail.

## Passing checks (evidence)
- #1 Mask discipline — bg full-bleed flat to all corners, no baked corner radius, glyph well inside safe zone.
- #3 Silhouette — nameable as an angular A (note: letter identity leans on the counter aperture; filled fully solid it would read as a wedge/peak).
- #5 Single light model — flat by commitment, no mixed lighting.
- #6 Palette economy — 1 hue + 1 neutral, accent *is* the whole field.
- #7 Figure-ground — 17.0:1, survives grayscale trivially.
- #8 Depth coherence — two clean planes, no z-fighting, no inconsistent shadows (none to be inconsistent).
- #9 Era coherence — uniformly flat/custom, no mixed-era quoting.
- #11 Personality — the rising-"A" + acid-lime register is a strong, nameable committed direction.
- #12 No-text — single-letter logomark, not a word or UI screenshot.

## Rhymes with
- Hint only (synthesis owns clustering): flat single-colour-field + bold logomark icons — the "startup brand mark dropped on a brand square" family. Rhymes on the *acid/athletic loud-palette* axis and the *flat-web-logo-not-mac-layered* axis. Likely neighbours are other monogram-on-flat-field icons and any hi-vis/neon-palette marks already in the corpus.
