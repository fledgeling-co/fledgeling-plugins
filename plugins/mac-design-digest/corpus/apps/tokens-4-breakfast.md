# Tokens 4 Breakfast — profile

- **Source:** macapp.supply (cover.png marketing composite + icon.png) · **Surfaces digested:** marketing cover composite + one app-representative status pill (menu-bar-extra chip) · **Last updated:** 2026-07-19
- **One-sentence identity:** an indie macOS menu-bar utility that reframes AI rate-limit anxiety as a warm breakfast-diner metaphor — iStat-Menus/Bartender glanceability dressed in cream, burnt-orange, and a literal coffee cup rather than pro-monochrome.
- **Cluster:** unassigned — candidate seed for a "warm-indie-utility" (amber-charcoal menu-bar) cluster
- **Lineage:** unknown (low) — the cover shows **no app window**: no chrome, no controls, no list, no settings. Only a marketing composite plus one status chip. Nothing diagnosable as AppKit vs Catalyst vs web. Contextual signals ("macOS menu bar app, no login, no cloud, one-time Pro," German indie) *suggest* a native/SwiftUI `MenuBarExtra`, but that is marketing inference, not pixel evidence. **No macOS-canon evidence is produced by this digest.**
- **Era (chrome):** unknown / custom-drawn — the opaque dark rounded chip carries no Liquid Glass lensing/vibrancy tell and no legacy-native tell; it reads as a custom-drawn marketing element.

> **Provenance warning:** this is a **marketing-cover-only** digest. Everything below the pill line is *brand* evidence (backdrop, wordmark, headline), not app-UI evidence, and must never be conflated with the app's interior design or promoted to macOS canon. Bring a real menu-bar dropdown / settings screenshot to make this profile diagnostic.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| **UI — status pill (the only app-representative fragment)** | | | |
| chip/bg | `#16110E` warm near-black (est. #16110E–#28201C) (estimated)(inferred) | | opaque dark rounded-rect, not a system material; warm/brown-biased charcoal, matches icon plate |
| chip/radius | ~12–14px on ~52px-tall chip → radius/height ≈ 0.25 (estimated)(inferred) | | soft **rounded-rect, NOT capsule** — unlike macOS 27 menu-bar-item selection (capsule, 13pt on 25pt) |
| chip/pad-x | ~18–20px composite (estimated)(inferred) | | left/right inset glyph→edge |
| status/positive | `#34D399` emerald-mint (measured off-image)(inferred) | | "22%" value. **Custom green**, between system Green `#30D158` and Mint `#00DAC3` — not the system hue |
| type/value | ~18px composite, bold (SF-Pro-Display-class) (estimated)(inferred) | | "22%" — the one saturated element in the chip |
| type/label | ~13px composite, medium, `#736D66` warm grey (estimated)(inferred) | | "5h window" — secondary; ~3.9:1 on chip bg (see Defects) |
| glyph/status | color emoji ☕ (~25px) (measured)(inferred) | | NOT a template SF Symbol — see Defects / native-tells |
| **BRAND (marketing composite — brand evidence only, never app canon)** | | | |
| brand/ground | `#F7F0E2` warm cream, radial warm glows `#E0D3BA`→`#E9E0D0` (measured)(inferred) | | 1200×630 OG composite |
| brand/ink | `#15110D` warm near-black (measured)(inferred) | | headline + metadata; softened warm, not pure #000 |
| brand/accent-burnt | `#C2620E` burnt orange (measured)(inferred) | | tracked wordmark, "BUILT IN" caps |
| brand/accent-amber | `#FFA522` amber, applied as a slight orange gradient (measured)(inferred) | | headline emphasis line "across major AI platforms." |
| brand/grey | `#69635D` warm grey (measured)(inferred) | | subtitle "AI spend tracker for macOS" |
| brand/icon-plate | `#28201C` warm charcoal squircle (measured)(inferred) | | brand-lockup icon plate |

## Layout skeletons

**Marketing cover (1200×630 OG composite, brand — not app UI):** left-aligned rail at x≈72. Top-left brand lockup (charcoal squircle icon ~72px + tracked burnt-orange wordmark over warm-grey subtitle, tight vertical proximity). Top-**right**: floating dark status pill (the app fragment). Center-left: 3-line bold grotesque headline (black / black / amber-gradient emphasis line), then a medium subhead ("Ship before the limit hits."), then a middot-separated feature strip, then a tracked orange "BUILT IN 🇩🇪" caps label. Warm radial glows behind the lockup and right edge.

**Status pill (app-representative chip — menu-bar-extra pattern):** single horizontal row inside an opaque dark rounded-rect: [color ☕ glyph] — [big bold emerald "22%"] — [warm-grey medium "5h window"]. Value → label de-emphasis is the whole hierarchy; the one saturated element (green %) carries the glance. A faint float shadow sits beneath (marketing, not a system shadow).

## Signature moves
- **[GOLDEN-NUGGET] The breakfast-diner metaphor carried literally into the data layer.** Rate-limit dread is reframed as warmth: warm-charcoal + burnt-orange + a literal coffee cup, a "Tokens 4 *Breakfast*" pun, and a menu-bar chip that reads budget as "% + rolling-window." The single memorable decision is the *emotional reframe* of a stressful metric — the opposite of the pro-monochrome (iStat Menus / Bartender) house style for the same menu-bar-utility job.
- **Budget-as-headroom, green = healthy.** 22% shown in reassuring emerald (22% *used* → lots left). The one saturated pixel-cluster in a dark chip is the number that matters — textbook Von Restorff / signal-detection focus. Meaning survives colour-blindness because the % number is always present, not colour-only.

## Defects
- **Contrast Dilution (mild, measured):** the pill's secondary label "5h window" `#736D66` on `#16110E` ≈ **~3.9:1**, under the 4.5:1 WCAG floor for normal text. Fix: lift the grey toward `#8E8E93`-class (system secondary) or bump weight/size.
- **Non-native menu-bar glyph:** a **colour emoji ☕** as the status glyph rather than a monochrome **template SF Symbol**. A color emoji does not tint to the menu bar's light/dark appearance and is a legibility risk at status-item size — a common indie choice, but a native-feel tell. (HIG: menu-bar extras should also present a **menu, not a popover** — if this chip is a popover header, that is the usual, very common indie deviation; unconfirmed.)
- **Custom status green, off the system palette:** `#34D399` vs system Green `#30D158` — a deliberate-looking but non-system hue; if the app also uses amber/red states, verify the set stays distinguishable and paired with labels (colour never the sole signal).
- **Brand ⇄ icon inconsistency (note, not a UI defect):** the cover's brand-lockup mark is the ☕ **emoji**, but the shipped `icon.png` is a *different* custom illustration (flat orange cup with a white "token" chip in the coffee on charcoal). The face of the app disagrees with itself across surfaces.
- **Evidence gap (the real finding):** a marketing-cover-only submission yields almost no app-interior or native evidence. The corpus learns brand palette + one chip, and nothing about the app's window, controls, density, or lineage.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Marketing cover + status pill | 11/14 (checks 11–14 n/a — no interactive surface) | #9 text contrast (pill grey label ~3.9:1); #6 soft (feature strip is one long line, marketing-exempt) |

## Native-tells audit (10-pt) — mostly not assessable
| # | Check | Verdict |
|---|---|---|
| 1 | AppKit-native lineage | **insufficient evidence** — no window shown |
| 2 | Glass on chrome only, content opaque | pass (trivially — chip opaque, no glass present) |
| 3 | Selection = inset rounded accent | n/a — no selection |
| 4 | Sidebar headers sentence-case | n/a — no sidebar |
| 5 | Density 13pt body / 20–28pt controls | n/a — no real controls to measure |
| 6 | Accent bound consistently | partial — brand accent is orange, status is a *custom* green (fine as a status role, but green is off-system) |
| 7 | One prominent action; dialog grammar | n/a — no actions |
| 8 | Concentric corners | n/a — single element |
| 9 | Toolbar borderless symbols grouped | n/a — no toolbar |
| 10 | Real chrome / genuine traffic lights | n/a — no window chrome |

Assessable passes: 1 clean (#2), 1 partial (#6); 8 n/a for lack of window evidence.
