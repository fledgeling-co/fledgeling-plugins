# Icon: Klack

- **Era:** skeuomorphic-quote (photoreal 3D render of a physical mechanical keycap — literal object, molded material, studio light; a modern indie icon deliberately quoting the pre-Yosemite object-icon tradition) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, **1024×1024 native master** — sharp, clean edges, low compression; not a resized web thumbnail) · **Category:** Utility (mechanical-keyboard sound layer for macOS — "satisfying sound with every keystroke")

| Dimension | Reading |
|---|---|
| Background | **transparent** (alpha 0 in all corners) — a free-floating object silhouette, no drawn field and no squircle; does not fill the mask |
| Glyph | monogram — a molded "K" legend on the keycap's top face. Warm ivory ramp `#F5EFE8`→`#FFFBF3` (not pure white). bbox ~184×216px, centre (519, 390): horizontally centred on canvas, optically seated on the dished top face |
| Overlay device | none — the object *is* the icon; no tool/badge/frame crossing it |
| Light model | soft studio light, upper-left bias (left shoulder highlight peaks `#BDBDBD`/189 vs right `#8B8B8B`/139). Matte-diffuse — no glassy specular hotspot; short soft ambient-occlusion pool under the skirt |
| Layer stack | transparent ground → keycap skirt/body in shadow `#0A0A0A`–`#0C0C0C` → dished top face `#1B1B1B` (lit) → soft shoulder rim highlight `#373737`→`#828282` → molded ivory "K" legend |
| Palette economy | effectively monochrome — one neutral (matte-black plastic) body + a single warm-ivory focal legend. 0 chromatic hue families; accent brightness reserved entirely for the glyph |

## Signature devices
- **The literal 3D keycap** — a matte-black mechanical keycap (doubleshot-style molded legend), shot from a 3/4 downward camera so both the dished top face and the tapered skirt read. This is textbook subject-mining: a keyboard-*sound* app rendered as the one physical thing a keystroke touches. The whole personality is in this one committed decision.
- **Diegetic monogram** — the "K" is not text laid *on* an icon; it is a legend molded *into* the top face, catching the same light as the plastic. It belongs to the object, which is why a single letter survives here where a slapped-on wordmark would fail.
- **Warm-neutral discipline** — the "white" legend is a warm ivory (`#FFFBF3`), not `#FFF`; it ties the icon to the product's cream brand ground (cover bg `#FFF7ED`) and keeps the render from feeling clinical.
- **Free silhouette on transparent** — deliberately refuses the Big Sur/Liquid-Glass squircle; presents as a physical prop with its own outline. The source of its charm and of both its rubric failures.

## Failures
- **#1 Mask discipline (FAIL):** the artwork is a free object on a transparent ground with a skirt protruding below the top-face's rounded square — it is not designed for the squircle. Under the macOS 26 system mask it would clip the keycap's own corners and leave the transparent zones empty, or the app must ship a separate filled tile (the cover proves one exists — see Notes). Consistent with the skeuomorphic era it quotes ("non-squircle outline"), but a fail against modern mask discipline.
- **#10 Variant robustness (FAIL):** a baked near-black raster with no layered/dark authoring. On a dark Dock, dark desktop, or under tinted/clear mode the `#1B1B1B`–`#0A0A0A` body has no light ground to separate from and the object nearly vanishes; a photoreal black render also cannot meaningfully accept a system tint. The composition depends on a light environment surviving behind it.

**Soft passes (flagged, scored as pass):**
- **#2 grid:** legend and object are horizontally centred (silhouette 84–939 → centre ~511; K centre x 519); vertically the mass sits high with the skirt weighting the lower third — correct for the 3/4 perspective, but it is object-optical, not grid-snapped.
- **#3 silhouette:** filled solid black, the rounded-square-over-trapezoidal-skirt reads as "a key," but the top-face/skirt separation that sells the 3D keycap collapses; nameable as a key, less certainly as *this* keycap.
- **#4 16px squint:** the keycap silhouette survives, but the "K" legend smears to a featureless grey blob — the monogram is not legible at menu-bar/Spotlight size (recovers cleanly by 32px). The subject (a key) reads; the brand initial does not.
- **#12 no-text check:** contains one letter, but as a molded diegetic legend on a physical object rather than applied typography; the photoreal render brushes the "no photographic elements" line without crossing it (it is CG, not a photo).

## Dimension summary

| Check | Verdict | Evidence |
|---|---|---|
| 1 Mask discipline | **fail** | free object on transparent bg + protruding skirt; not designed for the squircle |
| 2 Grid adherence | soft pass | horizontally centred; vertical mass high with skirt below (perspective-correct, object-optical) |
| 3 Silhouette | soft pass | reads as "a key"; top-face/skirt 3D separation lost when filled solid |
| 4 16px squint | soft pass | keycap survives; "K" legend smears to a grey blob (legible again ≥32px) |
| 5 Single light model | pass | one soft studio source, upper-left bias, consistent across cap/shoulder/skirt/legend |
| 6 Palette economy | pass | monochrome body + single warm-ivory focal legend; 0 chromatic hues |
| 7 Figure-ground | pass | ivory `#FFFBF3` on `#1B1B1B` ≈ 19:1; survives grayscale trivially |
| 8 Depth coherence | pass | top face → shoulder rim → skirt shadow → base AO ordered correctly, one consistent occlusion |
| 9 Era coherence | pass | every device from one language — photoreal object, molded material, realistic soft light |
| 10 Variant robustness | **fail** | baked near-black raster; vanishes on dark/tinted grounds, cannot accept a tint |
| 11 Personality | pass | committed subject-mined keycap render; diegetic molded monogram — not glyph-on-gradient |
| 12 No-text check | soft pass | single molded legend letter, diegetic to the object; CG render, not a photo |

## Rhymes with
- Photoreal **single-object / hardware-render** icons — a literal physical prop rendered on transparent with soft studio light, echoing the pre-Yosemite skeuomorphic tradition rather than the squircle-and-glass eras.
- **Diegetic-monogram** marks where a brand initial is molded/engraved into a rendered object (keycap, button, dial) instead of typeset over it.
- The matte-monochrome-restraint family: near-black object + one warm off-white focal, no chromatic accent — its charm (tactile realism) and its failures (no squircle, dies on dark) are the same choice.

## Notes for synthesis
- **Resolution:** genuine 1024×1024 master, sharp; palette sampling reliable. Body top face `#1B1B1B`, skirt/shadow `#0A0A0A`–`#0C0C0C` (deepest edge `#070707`), shoulder rim highlight ramps `#373737`→`#828282`, legend `#F5EFE8`→`#FFFBF3`, background transparent. Light from upper-left (left shoulder 189 > right 139).
- **Icon vs brand-mark gap:** the cover art (and the in-shot menu-bar) render Klack's *shipping* brand mark as a **filled black squircle with a plain white "K"** on a warm-cream page (`#FFF7ED`) — i.e. a proper masked tile. The supplied `icon.webp` is instead the marketing/hero **keycap render**. The two are the same idea (black + K) executed for two different jobs; the keycap render is the expressive one and the squircle-K is the system-safe one. Worth flagging that the object icon's #1/#10 failures are already solved by the squircle variant the brand owns.
- **Palette coherence with product:** strong on the black-plus-warm-white axis (icon legend `#FFFBF3` ↔ cover ground `#FFF7ED`; keycap black ↔ squircle mark black). The cover's chromatic accents — a lilac highlighter (`~#E9A5F5`) and a mint toggle — appear **nowhere** in the icon; the icon commits harder to monochrome than the brand does. Not a defect: the restraint reads as premium.
- Single-app observation. Do **not** promote "photoreal keycap / diegetic-monogram / skeuomorphic-quote object icon" to canon on one icon — hold as a style-family hint for a future skeuomorphic-object cluster; needs ≥3 independent object-render icons to converge.
