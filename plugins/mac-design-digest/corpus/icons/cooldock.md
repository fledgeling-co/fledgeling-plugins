# Icon: Cooldock

- **Era:** Big Sur unified (baked top-down gloss on a squircle — not Liquid Glass) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply icon.webp, 512×512 (web render, ~7KB — half the 1024 master; heavy compression but the icon is two shapes so it holds up) · **Subject:** "second Dock to your Mac with live widgets"

| Dimension | Reading |
|---|---|
| Background | Full-bleed charcoal squircle, **vertical ramp #282828 (top) → #0A0A0A (bottom)** (measured), sky-logic light-top/dark-bottom in monochrome |
| Glyph | One **glossy white capsule** — abstract; horizontally centred (bbox x69–442, centre x255 vs canvas 256, symmetric 69/70px margins), sits **low** (centre y392, ~76% down), ~373px wide (~73% of canvas), ~94px tall, ~4:1 capsule. Own top-lit ramp **#FFFFFF → #A0A0A0** (measured) |
| Overlay device | None — the pill *is* the glyph, not a tool crossing the field |
| Light model | Single top-down source. Field lit top→bottom; capsule lit top→bottom with a short bottom micro-shadow implying it sits raised on the field; **baked specular rim on the top edge/corners** (top edge ~#737373, TL corner ~#9C9C9C) (measured) |
| Layer stack | (1) charcoal gradient squircle field → (2) baked top-edge specular rim → (3) white glossy capsule, lower third |
| Palette economy | **Zero hue families** — pure black/white/grey. Accent: none. Extreme economy; identity carried by one figure on a field |

## Signature devices
- **[GOLDEN-NUGGET] Dock-as-pill.** A single wide glossy capsule, centred and dropped into the lower third of a dark tile, literally depicts the product — a floating dock/widget bar on a dark surface. The icon and the app's actual dark floating dock (see cover.jpg) speak the same black-rounded-rectangle language; the icon is the product's own chrome reduced to one mark.
- **Committed monochrome minimalism.** Not a template gradient-glyph — a deliberate reductive direction: near-black field + one high-key white shape, no colour, no tool overlay. The boldness budget is spent entirely on restraint.
- **Big Sur baked gloss.** Charcoal vertical ramp + top-edge specular rim + a top-lit capsule with its own micro-shadow — classic pre-Tahoe hand-baked lighting, the opposite of Liquid Glass's "ship flat layers, let the system light them."

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black, the icon collapses to an anonymous squircle: the pill is an internal light figure, not part of the contour, so it vanishes from the silhouette. All identity lives in the internal figure-ground (white-on-black), none in the outline. You can name the *shapes* ("a capsule on a rounded square") but not the *subject* ("a dock") from shape alone — the icon relies on brand recognition, not self-evident metaphor.

## Soft passes (flagged, counted as pass)
- **#2 Grid** — horizontally optically centred, but the capsule sits deliberately low (76% down) for the "dock lives at the bottom" reading; bottom-heavy but purposeful.
- **#10 Variant robustness** — as a luminance-based monochrome mark it would *tint* cleanly (black field → dark tint, white pill → light tint, pill stays distinct). The real risk is the all-black field having weak separation from a dark Dock tray / dark wallpaper — a near-black icon is quiet in the Dock by nature. Soft, not a hard fail.
- **#11 Personality** — the "dock-as-pill" device is distinctive, but its meaning is only legible once you know the app; abstract to a cold viewer.

## Rhymes with
- (hint for synthesis, not a promotion) Dark minimalist utility tiles — near-black field carrying a single high-key glyph, Big-Sur baked gloss. Likely family neighbours among the digested notch/dock utilities (alcove, claude-notch-usage-companion, bartender-6) that pair a dark field with one minimal light element. Synthesis owns the cluster call.
