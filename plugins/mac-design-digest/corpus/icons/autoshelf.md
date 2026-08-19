# Icon: AutoShelf

- **Era:** flat-transition (visual language) — structurally non-conforming / custom · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/autoshelf/icon.png`, actually a 128×128 AVIF web render) · **Category:** Productivity
- **Subject the icon must communicate:** an app that watches folders and auto-files loose files where they belong.

| Dimension | Reading |
|---|---|
| Background | **transparent — no field** (alpha 0 at all four corners and in inter-element gaps). The glyph floats on nothing; there is no squircle tile. `(measured)` |
| Glyph | Two flat objects: a tilted dog-eared **document** `#FC5128` (bbox x30–95, y18–93 of 128 — the dominant anchor, tilted ~10–15° CCW) above a shallow charcoal **shelf/tray curve** `#3F3F3F` (bbox x31–96, y107–121). A visible gap between them stages the file *dropping onto* the shelf. Horizontally centred (content centre ~x63 of 128). `(measured)` |
| Overlay device | none (no diagonal tool crosses the plane). The dog-ear is intrinsic to the document; the shelf is a base element, not an overlay. |
| Light model | **flat / lightless** — no gradient (document is uniform `#FC5128` from y=35 to y=83), no baked shadow, no specular. The folded corner is a flat lighter tint `#FD8D63` standing in for a highlight, not a lit bevel. |
| Layer stack | transparent ground → charcoal shelf curve (behind/below) → vermillion document (tilted, front) → coral folded-corner tint (on document). |
| Palette economy | one hue family (vermillion `#FC5128` + its tint `#FD8D63`) + one neutral (charcoal `#3F3F3F`). Accent saturation reserved for the focal document. Disciplined. |

## Palette
- **Document body:** `#FC5128` (252,81,40) — vivid vermillion / orange-red, flat `(measured)`
- **Folded corner (dog-ear):** `#FD8D63` (253,141,99) — lighter coral tint of the same hue `(measured)`
- **Shelf / tray:** `#3F3F3F` (63,63,63) — charcoal, near-black `(measured)`
- **Background:** transparent (0,0,0,0) `(measured)`

## Signature devices
- **[GOLDEN-NUGGET] File-dropping-onto-shelf narrative.** The composition is subject-literal: a document mid-drop above a catching shelf/tray directly depicts "the app files your files." Rare for a utility to animate its own verb in a static mark.
- **Shelf-curve as a smile.** The charcoal curve reads simultaneously as a shelf/tray and as a friendly grin under the document — a two-reading device that buys warmth without an added element.
- **Dog-eared document** as the universal "paper / file" signifier — the single detail that makes the orange square unambiguously a *document*.
- **Flat tint-as-highlight.** The lighter coral fold flags the dog-ear purely by hue step, no lighting model invoked — consistent with the flat vocabulary.

## Failures
- **#1 Mask discipline — FAIL.** Transparent background, free-form floating glyph; the artwork does not fill or acknowledge the squircle. In the Dock it would read as a small object on the wallpaper, not a filled tile. Root cause of both failures.
- **#10 Variant robustness — FAIL.** With no background field and a two-value scheme (orange glyph + charcoal shelf on transparency), the mark would not survive dark/clear/tinted system renders: on a dark wallpaper the `#3F3F3F` shelf all but vanishes, and tinted/mono modes collapse the orange-vs-charcoal relationship. Both failures resolve by seating the glyph on a squircle field (a warm off-white, or a soft sky ramp echoing the cover).

### Soft passes (flagged, scored as pass)
- **#2 Grid adherence — soft.** Horizontally centred and optically balanced, but the object occupies only ~52% of canvas width; true grid/safe-zone conformance is moot without a tile.
- **#4 16px squint — soft.** The vermillion document survives as a solid orange chit; the ~14px shelf curve (≈1.7px at 16) smears to a faint smudge, so the *file→shelf* concept collapses to "an orange document" at menu-bar size.
- **#7 Figure-ground — soft.** Holds on a light background (vermillion ≈3.3:1 on white, charcoal strong); fails on dark wallpaper where the shelf disappears — a direct consequence of the missing field.

## Rhymes with
- Flat single-object **utility glyphs** (file cleaners / auto-organisers) and iOS-style app-store marks that float one flat object rather than filling a squircle tile.
- Flat-transition-era free-form silhouettes (Yosemite–Catalina visual language) — simple fills, free outline — deployed here as a modern indie utility mark.
- Cross-note for synthesis: sits opposite the current Liquid-Glass / Big-Sur-squircle convention; if 2+ more transparent free-form utility glyphs appear, this becomes a nameable "floating-object utility" icon cluster.

## Notes (resolution & synthesis)
- **Resolution caveat:** source is a 128×128 AVIF web render (file carried a `.png` extension but is ISO-Media/AVIF; converted via `sips -s format png`). Flat-interior hex values are reliable; edge geometry, tilt angle, and any sub-2% gradient/texture are soft at this scale. No 1024 master to confirm.
- **Transparency is genuine**, not a strip artifact as far as can be told — corners are cleanly alpha-0. Either the shipping icon truly floats a free-form glyph, or macapp.supply removed a background. Flag prominently: the structure is non-native.
- **Brand coherence with the cover is strong:** the identical `#FC5128` document + `#3F3F3F` shelf headline the cover hero, and the vermillion recurs as the per-rule glyph in the app's dark-mode UI. The icon is a faithful brand mark, not a detached render.
