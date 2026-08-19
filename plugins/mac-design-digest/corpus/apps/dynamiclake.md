# DynamicLake — profile

- **Source:** macapp.supply (cover composite only) · **Surfaces digested:** notch HUD (expanded Dynamic Island notification), dark · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple's iOS Dynamic Island transplanted onto the MacBook notch — a pure-black concave-shouldered morph pill that treats the camera housing like an iPhone's, in the manner of NotchNook / Boring Notch / alcove.
- **Cluster:** unassigned (candidate: `notch-hud / dynamic-island-clones`)
- **Lineage:** native (med) — a genuine Mac menu-bar utility drawing a borderless notch panel, BUT this surface's visual grammar is a deliberate 1:1 import of iOS Dynamic Island. Its density, materials, and layout are iOS-derived and are recorded as **tells + corrections only** — they must never feed macOS canon or native clusters.
- **Era (chrome):** custom — pure opaque #000000 fill, no Liquid Glass, no vibrancy, no NSVisualEffectView material; the "OLED-black" iOS metaphor, appearance-independent (stays black in light or dark system mode).

## Provenance caveat
Only a marketing **cover composite** was supplied (1830×1030), showing the island in situ on a periwinkle wallpaper — no device frame or headline text, so the visible island is genuine app evidence; the wallpaper is composite/brand backdrop, not app evidence. All pixel figures are from a **possibly-scaled composite**; retina scale is assumed @2x with **low confidence**. Absolute pt values are `(estimated)` with wide ranges — trust the *proportions*, not the point sizes. No standard Mac chrome (traffic lights, menu bar, toolbar, sidebar) is visible anywhere, so lineage cannot be confirmed from the body.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| surface/island-fill | `#000000` pure opaque black | (measured)(confirmed) | Not a macOS material; iOS OLED-black metaphor, appearance-independent |
| surface/backdrop | periwinkle gradient `#6970AD`→`#A093BF` (top→bottom) | (measured)(inferred) | Desktop wallpaper in the composite — brand/backdrop, NOT app evidence |
| island/body-width | ~1248px (~624pt @2x est) | (estimated)(inferred) | ~12% of a 14″ logical width; hangs from screen top-center |
| island/visible-height | ~348px (~174pt @2x est) | (estimated)(inferred) | Top edge is cropped at the screen top / notch anchor |
| island/shoulder | concave (inverse) fillets: top edge ~1341px flaring OUT to ~1248px body over first ~20px | (measured)(inferred) | **The signature geometry** — corners flare wider at the top, blending into the menu-bar/notch (Dynamic Island morph), not a normal inward corner radius |
| island/bottom-radius | ~40–50px (~20–25pt @2x est) | (estimated)(inferred) | Bottom-corner squircle |
| type/name | ~17pt SF Pro **Bold**, `#FFFFFF` | (measured color)(estimated size)(inferred) | Primary label; sender name |
| type/message | ~15–16pt SF Pro Regular, `#8B8B8B` (~55% white) | (measured color)(estimated size)(inferred) | Secondary label; 2-line preview; proper de-emphasis vs name |
| avatar | ~150px circle (~75pt @2x est), photo on teal tint | (estimated)(inferred) | iOS communication-notification avatar; larger than any Mac-native notification avatar |
| avatar/app-badge | green Messages glyph ~56px (~28pt est), overlapping avatar bottom-right | (estimated)(inferred) | System-green app-source badge — iOS notification composite |
| badge/unread | ~54px circle (~27pt @2x est), system red, white "2" | (measured color)(estimated size)(inferred) | Top-right; system red, glyph+number paired (legitimate status use) |
| padding/left-inset | ~64px body-edge→avatar (~32pt est) | (estimated)(inferred) | |

## Layout skeletons

**Notch HUD — expanded Dynamic Island notification (dark).** A single horizontal panel hanging from screen top-center, anchored to the notch, with concave shoulder fillets flaring outward to meet the screen edge. Left: circular avatar with a system-green app-source glyph badge overlapping its bottom-right. Center-left: a two-tier text stack sharing a left axis just right of the avatar — bold white sender name (row 1) over a 2-line ~55%-gray message preview (rows 2–3), each line ~28–32 chars. Right: a system-red numeric unread badge, vertically near the name row. A wide reserve of black negative space sits to the right of the text (the island is deliberately wider than its content — iOS Dynamic Island proportion). Everything on flat opaque black; no dividers, no timestamp, no action buttons.

## Signature moves
- **[GOLDEN-NUGGET] The concave shoulder morph.** The island's top corners flare *outward* (inverse radius) into the menu bar rather than rounding inward — the defining "liquid" Dynamic Island geometry, reproduced faithfully. This one curve is the entire product's identity; it is what separates a notch utility from a plain top-center banner.
- **Pure-black, appearance-independent surface.** The panel is `#000000` opaque in all system modes, borrowing the iPhone's OLED-bezel illusion so the notch reads as a seamless "island." Deliberately not a Mac material — a metaphor, not a mistake.
- **iOS communication-notification stack ported wholesale:** circular avatar + app-source glyph badge + bold name + gray preview + red count. Transmits "this is a message" with zero Mac-specific learning (Jakob's Law, fully exploited).

## Defects
These are **lineage tells** (deliberate iOS imports), recorded as corrections for canon hygiene — not sloppiness:
- **Non-native notification grammar** → real macOS notifications use a translucent light/dark material (NSVisualEffectView), app icon top-left, a timestamp, and appear top-*right*; this uses opaque black, notch-*center*, no timestamp. Correction: for a native Mac notification mock, use system material + top-right placement + timestamp. (For *this* product the deviation is the entire premise — a signature, not a flaw.)
- **iOS density/scale** → avatar (~75pt), badge (~27pt), body text (~15–17pt) are touch/iOS-scaled, well above the macOS 13pt-body / 20–28pt-control grammar. Correction: excluded from mac density canon.
- No genuine defects on accessibility or hierarchy: contrast and de-emphasis are strong (see below).

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Notch HUD (Dynamic Island notification) | 12/14 (applicable) | #1 grid unverifiable (scaled composite); #11–14 N/A (passive HUD — no controls, inputs, forms, or focusable elements). Passes #2 alignment, #3 proximity, #4 scale (2 sizes), #5 leading, #6 measure (~30ch), #7 de-emphasis (white/bold → 55%-gray/regular), #9 text contrast (>15:1 & >7:1 on black), #10 UI contrast (system red/green on black). |
| Native-tells audit | 4/10 (applicable) | **#1 FAIL** lineage grammar is iOS Dynamic Island, not native macOS notification. **#5 FAIL** iOS density/scale. Pass #2 (no glass violation — no glass present), #6 (system red/green used correctly as status/identity), #7 (no action collision — passive), #10 (legitimate borderless panel, no faked traffic lights). #3,#4,#8,#9 N/A (no selection/sidebar/nested-corners/toolbar). |

**Corpus verdict:** competent and unmistakably itself, but disqualified as macOS-native taste evidence — this is an *iOS-metaphor* surface. Its value to the corpus is as a documented tell (how a notch utility reproduces Dynamic Island), not as native canon input.
