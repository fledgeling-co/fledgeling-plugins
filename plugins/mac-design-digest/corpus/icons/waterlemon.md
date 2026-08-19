# Icon: Waterlemon

- **Era:** Big Sur unified (object-on-plate) — *anachronistic for macOS 26; no Liquid Glass* · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.webp, 102×102 web render) · **Category:** Design (icon generator)

| Dimension | Reading |
|---|---|
| Background | flat #FFFFFF (pure white, ~85% of pixels) — no ramp, no colored field |
| Glyph | object — a fruit wedge; yellow/gold flesh ramp #FFDC00→#FFCE01→#FFD207, deeper amber rind #CE9301→#D29505, near-white pith line, dark-brown embedded seeds #3A231C; sits optically centered but weighted lower-left (rind base bottom-left, bright tip upper-right) |
| Overlay device | none |
| Light model | soft near-frontal top-down; glossy "candy/clay" specular sheen on upper flesh; short soft contact shadow under the wedge on the white plate; baked highlights, no hard hotspot |
| Layer stack | white squircle plate → soft contact shadow → fruit body (flesh + rind + pith) → embedded dark seeds → glossy specular sheen |
| Palette economy | 1 hue family (yellow→gold ramp) + dark-brown seed accent + flat white ground; accent (seeds) reserved for the focal detail — economical |

## Signature devices

- **The pun-glyph** `[GOLDEN-NUGGET]` — a *watermelon-slice silhouette rendered in lemon-yellow*: the name (water·MELON shape + LEMON color, seeds and all) made visual. The entire brand idea lives in one shape/color mismatch. This is where the icon's personality is.
- **Dogfooded material** — the glossy AI-3D "candy render" look is exactly what this app *produces* (the cover gallery is a shelf of the same soft-3D objects: potion bottle, knitted cat, glass basketball, coin jar). The icon advertises the output. On-brand, and confirmed by the cover using the identical yellow wedge top-left.
- **Object floated on flat white** — no Big Sur sky-ramp behind it; the fruit hovers on a bare white plate with only a soft contact shadow for grounding.

## Failures

- **#7 Figure-ground contrast** — bright-yellow flesh #FFD301 on white #FFFFFF measures ≈1.4:1, far under the 3:1 floor. In grayscale the flesh nearly dissolves into the plate; the silhouette survives *only* via the darker amber rind and the seed darks, not the body. The single most fixable defect (a colored field, or a darker rind ring, would rescue it).
- **#10 Variant robustness** — composition depends entirely on the white ground and isn't authored as Icon Composer layers, so dark/clear/tinted/mono renders would collapse (yellow flesh has no internal contrast once the white plate is gone). Not designed for macOS 26 appearance variants.

## Soft passes (flagged, scored as passes)

- **#1 Mask discipline** — rounded corners are baked into the web-preview PNG; fruit stays well inside the safe zone and doesn't fight the mask, but no true full-bleed square was available to judge baked-corner mismatch.
- **#2 Grid adherence** — optically centered but lower-left weighted; reads slightly off-axis, within safe margins.
- **#3 Silhouette test** — filled solid black it reads "a fruit wedge / fan," not specifically *watermelon* or *lemon*; the identity is carried by color + seed-dots, which vanish in pure silhouette. Nameable, but generically.
- **#9 Era coherence** — quotes the Big Sur object-on-plate convention (front-facing, soft baked shadow) but ships in the macOS 26 (Liquid Glass) era with no glass layers, and drops Big Sur's colored background ramp for flat white. Internally consistent as "3D fruit on white," but era-anachronistic.

## Rhymes with

- The **glossy 3D-object-mascot-on-white** family — the current wave of AI-generated "candy/clay render" app icons (its own cover gallery is the reference set). Big Sur object-on-plate descendants, but with a soft-body candy material instead of crisp vector + baked micro-shadow, and a bare white field instead of a sky-ramp.
- (First icon of this material family in the corpus — flagged for synthesis as a potential "candy-3D" cluster seed; needs ≥3 independent apps before any canon.)
