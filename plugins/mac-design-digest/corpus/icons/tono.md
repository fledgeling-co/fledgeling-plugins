# Icon: Tono

- **App:** Tono — "menu bar wallpaper manager" (Lifestyle) · **Source:** macapp.supply (`sources/tono/icon.png`, 512×512 RGBA, pre-masked)
- **Era:** Big Sur unified · **Rubric:** 11/12 · **Digested:** 2026-07-19

A three-quarter portrait of an American robin — matte-black head and back, vermillion breast, two-tone yellow-orange bill, white catchlit eye-ring — cropped bust-style against a flat warm-ivory field. An illustrative brand mascot, not a functional glyph: it says "nature / birds," not "wallpaper manager."

| Dimension | Reading |
|---|---|
| Background | Flat warm ivory ~`#FAF6F1` (near-flat; no sky-logic ramp). `(measured)` from composited-over-white samples — slight `#FAF7F2`→`#FBF7F1` drift is within compression noise. |
| Glyph | Object/mascot — a perched robin, three-quarter facing right. Optically balanced: black body mass anchors lower-left, head + beak point upper-right; portrait-cropped, bleeds to the squircle's lower & right edges rather than centered-glyph. |
| Overlay device | None — no diagonal tool, badge, or frame. The subject *is* the icon. |
| Light model | Single top-down / upper light. Breast ramps lighter-warmer at top (`#F52512`) to deeper red at the base (`#EA0C01`); matte-black plumage carries a cool-gray sheen band (`#232528`→`#3B3B3F`) for volume; beak top-lit; one specular catchlight in the eye. Soft, short baked self-shadow — no long dramatic cast. No glass rim-light/refraction. |
| Layer stack | ivory ground → black body/wing (sculpted sheen) → red breast plane → black head → yellow-orange bill → white eye-ring + black pupil + catchlight (frontmost) |
| Palette economy | 1 warm chromatic family (red→orange bill) + neutral ground/plumage/eye. Accent saturation reserved for breast + bill focal marks. Four visible colour zones — near the ≤2-family ceiling but disciplined. |

**Palette (measured, composited over white):**
- Ground: `#FAF6F1` warm ivory (flat)
- Plumage (black): `#000000` head · body/wing ramp `#232528`→`#292B2E`→`#3B3B3F` (cool near-black, faint blue undertone)
- Breast (red): `#F52512` (upper) → `#F11809` → `#EA0C01` (lower)
- Bill (accent): `#FB8A04` yellow-orange, two-tone (yellow upper → deeper orange lower)
- Eye: white ring `#FCFBF7`, black pupil, single grey catchlight

## Signature devices
- **Robin bust portrait** `[GOLDEN-NUGGET]` — a songbird cropped like a headshot, bleeding to the lower & right mask edges instead of a centered symbol. The identity is a *creature*, not a metaphor for the app's function.
- **Sculpted matte plumage** — black feathers modeled with a soft cool-grey sheen ramp (`#232528`→`#3B3B3F`), giving roundness under top light without any gloss. Committed illustration, not template glyph-on-gradient.
- **Catchlit eye-ring** — the white-ringed eye with a lone specular dot is the one true highlight in the piece and the anchor that keeps the bird identifiable when the near-black head/body merge at small sizes.
- **Flat ivory ground** — a warm cream field (not a gradient ramp) that lets the high-contrast bird carry the whole square.

## Failures
- **#10 Variant robustness (Liquid Glass era):** ships as a Big Sur-style pre-masked raster with a baked ivory ground — no Icon Composer light/dark/clear/tinted layers. In a tinted or mono system render the mostly-near-black bird collapses to a black blob and depends entirely on the baked cream background for figure-ground. Not authored for macOS 26 appearance variants.

## Soft passes (flagged, scored as pass)
- **#2 Grid adherence** — portrait-crop framing, optically balanced, but not a safe-zone-centered glyph; head/beak sit right-of-centre, counterweighted by the black body mass. Intentional composition, not a nudged one.
- **#4 16px squint test** — head (`#000`) and body (`#3B3B3F`) tonal separation is too fine to survive downscale; the bird reduces to a red-and-black blob. Saved — barely — by the vermillion breast, yellow bill, and white eye dot. Legible, detail-compressed.
- **#6 Palette economy** — four colour zones (ivory / black / red / yellow-orange); passes because red→orange is one warm ramp and the bill is a small focal accent, but it is at the ceiling.

## Notes (for synthesis)
- **Resolution caveat:** source is 512×512 — half the 1024 master and almost certainly a resized web render from macapp.supply. Palette hexes are reliable; sub-pixel edge treatment, any faint background vignette, and true drop-shadow character are not measurable at this fidelity.
- **Delivery form:** RGBA, pre-masked squircle (transparent corners; mask edge inset ~48px at 512 ≈ ~96px at 1024). Big Sur-era baked-mask delivery, *not* full-bleed Icon Composer layers — this is why #10 fails.
- **Brand coherence (icon ↔ app):** weak on palette, strong on theme. The cover UI is cool sage-green Liquid-Glass chrome over green nature photography; the icon is warm cream + red + black and shares none of that palette. But it is thematically coherent — the cover literally features rowan / mountain-ash berry clusters (orange-red), a classic robin food source. The bird stands in for "nature wallpapers," the app's content, rather than its mechanism.
- **Subject communication:** for a *menu-bar wallpaper manager* the icon communicates identity (a warm nature mascot) over function — legitimate for a Lifestyle app, but a viewer cannot infer what the app does from the icon. Nameable choice, worth flagging in ICONS synthesis.

## Rhymes with
- Warm-ground flat-illustration **animal-mascot** family, Big Sur era: a creature portrait on a flat cream/ivory field with sculpted matte shading and one saturated focal hue. Adjacent to indie wildlife/character icons that lead with brand personality rather than a tool glyph. (No other digested icons yet — first member of a potential "illustrated-creature-on-warm-ground" cluster.)
