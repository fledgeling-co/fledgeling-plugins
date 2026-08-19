# Icon: Mac 4 Breakfast

- **Era:** Big Sur unified · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 256×256 web render, pre-masked with alpha) · **Subject:** menu-bar battery/power utility for Apple devices (Productivity)

| Dimension | Reading |
|---|---|
| Background | ramp, diagonal **#8B75EE (violet, TL) → #517EF3 (blue, BR)** — down the left edge #8873ED → #5F64E9 (estimated). Single purple→blue hue sweep, sky-logic bright-corner offset to top-left. |
| Glyph | object — a horizontal **battery** with terminal nub. Off-white rounded frame (#F0F1F1 / #E4E4E4), green gradient charge fill **#87ECB1 (top) → #62D993 → #2CC071 (base)**, white lightning-bolt knockout (#FFFFFF) centred. Optically centred horizontally, sits ~10px high of geometric centre (battery mid ≈ y118 vs canvas y128) to make room for the device row below. |
| Overlay device | **menu-bar device row** — a translucent lighter-violet capsule panel (~#767EDF over the field) in the lower third holding 5 saturated dots: red #F45D57, orange/amber #F4B62F, green #28BF3F, blue #3B7EEF, purple/magenta #BF6AEB. Not a corner badge, not a tool — a secondary status panel. |
| Light model | soft **top-down**, Big Sur baked-shadow. Short subtle micro-shadow under the battery frame lifts it off the field; green fill lit lighter at top; no hard specular, no glass refraction. One consistent source. |
| Layer stack | (back) purple→blue gradient field · translucent device-row capsule + 5 colour dots · off-white battery frame w/ soft drop shadow · green gradient charge fill · white lightning-bolt knockout (front) |
| Palette economy | 2 dominant hue families (violet-blue field + green object) = disciplined core; **but** the device row adds 5 more saturated hues — motivated (multi-device colour coding) yet it spends saturation budget away from the focal battery. Soft pass. |

## Signature devices
- **[GOLDEN-NUGGET] Menu-bar device row** — a frosted capsule of 5 colour-coded dots slung beneath the hero object. It quotes the app's actual home (a menu-bar utility, per the cover) and its "every Apple device" premise in one move; this is the one thing that lifts the icon above generic object-on-gradient.
- **Literal charging metaphor** — green fill + white lightning-bolt knockout reads unambiguously as "charging". No abstraction; the subject *is* the glyph.
- **Complementary field-vs-object contrast** — a violet-blue background against a green object is near-complementary, which is why the battery pops without an outline doing the work.

## Failures
- **#4 16px squint test — FAIL (detail smear).** At menu-bar/Spotlight size only the green battery bar survives as a clean read; the lightning bolt collapses into the green mass and the 5-dot device row degrades to an indistinct colour smudge. Two of the three glyph elements are lost at the size this icon most needs — and one of them (the device row) is a *communicated feature*, not decoration. The icon over-invests in detail the smallest render can't carry.

## Soft passes (flagged, not failures)
- **#2 grid** — visual weight is split between battery and device row rather than resting on a single optical-centre circle; balanced and intentional, but not a single-anchor composition.
- **#6 palette economy** — the 5-hue device row deviates from "accent saturation reserved for the focal element"; systematic and purposeful, contained in a pill, so the battery still dominates.
- **#10 variant robustness** — the white+green battery would survive a dark/tinted render (glyph not background-dependent), but the device row's meaning is colour-only and would flatten to one tone under tinted/mono, destroying it. Moot for a Big Sur icon, but the row is the element that would break if ported to Liquid Glass appearances.

## Rhymes with
- **bartender-6** and the menu-bar power-utility family (iStat Menus, AlDente, CleanMyMac) — single system-object on a saturated gradient field, menu-bar-native.
- Big Sur "one tool/object, front-facing, soft micro-shadow" cluster generally. The device-dot-row is its own small motif worth watching for across status/monitor utilities.

## Notes for synthesis
- Resolution: 256×256 web render — green ramp and dot hues are reliable; fine micro-shadow softness / any faint specular are not judgeable at this scale. Pre-masked (transparent corners), so mask-edge behaviour can't be read from a full-bleed square, but content sits comfortably inside (~6% margin).
- Strong icon↔product palette coherence: the violet→blue field and green status accent recur in the wordmark, the "Native for macOS" green pill, and the app's green charging chip on the cover. This is a coordinated brand system, not an icon designed in isolation.
- The translucent device-row capsule is a mild glass *quote*, but this is Big Sur object-language (baked shadows, front-facing gradient object), not Icon-Composer Liquid Glass. Classify big-sur, note the transitional nod.
