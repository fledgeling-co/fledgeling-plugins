# Audio Notes (formerly Email Me) — profile

- **Source:** macapp.supply (cover composite + icon) · **Surfaces digested:** menu-bar compose panel (light) · **Last updated:** 2026-07-19
- **One-sentence identity:** A quick-capture menu-bar utility styled like a consumer messaging app — one field, one gold "send" button, the paper-plane metaphor threaded from icon to CTA — closer in feel to a chat compose bar (Telegram/Spark send) than to a native macOS panel.
- **Cluster:** unassigned (cluster hint: *warm-consumer-utility*)
- **Lineage:** web-electron (low confidence) — frame reads native (genuine traffic lights, centered title) but the body is non-native (uppercase branded CTA, chat-compose bottom bar, oversized non-13pt text). Could equally be a heavily custom-styled SwiftUI menu-bar app; classified **non-native either way, so none of its styling feeds macOS canon**. Recorded as tells + corrections.
- **Era (chrome):** big-sur → Sequoia era (pre-Tahoe). Backdrop is the colourful Monterey/Ventura wallpaper; menu bar is translucent with Ventura Control-Center glyph and a charging-battery icon. **No Liquid Glass evidence** — content is flat opaque white.

> **Provenance caveat:** the only UI evidence is the app window *inside a marketing composite* (2114×1176, arbitrary scale, grainy yellow backdrop + headline typography around it). All pixel readings are ratio-based → `(estimated)`/`(assumed)`, never `(measured)`. The composite shows the **pre-rename "Email Me" UI** (window title literally reads "Email Me"); the microphone glyph in the bottom bar foreshadows the "Audio Notes" voice pivot.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#F7F7F8` light neutral sheet, light mode (estimated)(inferred) | | flat opaque content, faint off-white — not pure `#FFF` |
| accent/brand | goldenrod `~#E8C04A` (estimated)(inferred) | | the whole identity: icon background, menu-bar tint, and the single CTA all this one hue |
| text/title | `~#1C1C1E` (≈85% black), Semibold–Bold, ~15pt-equiv, **centered** (estimated)(inferred) | | native title *placement* (centered) but native window titles are rarely bold — mild deviation |
| text/placeholder | `~#8A8A93` secondary gray, Regular, **~16–18pt-equiv** (estimated)(inferred) | | notably **larger than native 13pt body** — density tell; placeholder doubles as the only field label |
| button/primary | gold capsule, **white UPPERCASE "SEND"** Bold + tracked, height ~44pt-equiv, radius = height/2 (estimated)(inferred) | | uppercase label = non-native; white-on-light-gold = contrast fail (see Defects) |
| glyph/action | monochrome `~#4A4A4A` (secondary label), ~24–28pt-equiv (estimated)(inferred) | | mic / photos / folder — borderless SF-Symbol-style glyphs, the one native-idiomatic element |
| radius/window | ~14–16px-equiv rounded corners (estimated)(inferred) | | can't verify against kit's unknown window radius |
| chrome/traffic-lights | genuine 3-dot cluster, **coloured** (focused window), leading inset ~1× top inset (estimated)(inferred) | | real macOS frame — the strongest native tell present |

## Layout skeletons

**Menu-bar compose panel (light)** — floating titled window anchored to the menu-bar paper-plane glyph, ~1.6:1 landscape aspect, single column, no sidebar/inspector/toolbar.
- **Top:** native title bar — traffic lights leading (left inset ≈ top inset), centered bold "Email Me" title. No toolbar row.
- **Body:** full-bleed multiline compose text area; placeholder "Write your message" top-left with ~40px-equiv inset from the window edge.
- **Bottom:** horizontal action bar — three borderless monochrome glyph buttons (mic / photos / folder) left-aligned, sharing the body's left axis; flexible gap; one gold capsule **SEND** primary pinned bottom-trailing.
- **Alignment:** glyph-cluster left edge and placeholder left edge share one vertical axis; SEND right edge tracks the text-area right padding. Container alignment holds.

## Signature moves
- **[GOLDEN-NUGGET] Single warm hue as the entire brand system.** One goldenrod (`~#E8C04A`) carries the icon background, the menu-bar tint, and the sole CTA — a *committed* (not restrained) colour strategy on an otherwise near-white sheet. Systematic and purposeful (warmth + "send" identity); this is the app's character, and it survives even though the app is non-native.
- **[GOLDEN-NUGGET] Reduction to one field + one action.** The panel is stripped to a compose area and a send button — "capture a thought and fire it off." Real product character (frictionless capture, Fogg-reduction), not anonymity. The paper-plane metaphor (icon → menu-bar glyph → gold SEND) is the connective tissue.

## Defects
- **Contrast Dilution (CTA label)** → white "SEND" on light-gold capsule reads **~1.8:1**, far below WCAG 4.5:1 → canon: dark-ink label on the gold, or a deeper/saturated gold with white. The one place the eye must land is the least legible text on screen.
- **Non-native button label** → UPPERCASE "SEND" → native macOS buttons use sentence/title case ("Send"). Tracked-uppercase is a web/CSS tell.
- **Brand accent overrides system accent** → the primary action binds to app-yellow, not `controlAccentColor` → native correction: selection/focus/primary bind to the *user's* system accent; a brand hue lives in content/icon, not as the control accent.
- **Persistent bottom format/compose bar** → a chat/messaging pattern (iMessage/Slack compose) → native correction: actions belong in a top toolbar or the window body, not a persistent bottom bar.
- **Non-native density** → placeholder ~16–18pt-equiv and a ~44pt touch-tier button → native is 13pt body with 24–28pt controls; this reads consumer/touch-friendly, not pointer-first.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar compose panel (light) | 10/14 | #9 white SEND on light-gold ~1.8:1; (#5/#6 n/a — empty compose, no paragraphs; #14 n/a — static, no focus state) |
| — native-tells audit | 4/10 | #1 non-native body; #5 non-13pt density + touch-tier button; #6 brand accent not system accent; #9 bottom compose bar not a native toolbar; (#3/#4 n/a — no selection/sidebar) |

## Brand / marketing evidence (composite backdrop — NOT app-UI evidence)
- **Backdrop:** grainy flat warm-yellow field (`~#F2C94C`) with subtle noise texture.
- **Headline:** heavy black grotesk, near-condensed, tight tracking, sentence case ("One-click menu bar access"); subhead same family, Bold, charcoal.
- **Icon (brand context, not digested as icon):** white origami paper airplane on a gold→orange radial gradient, soft top-left key light, drop shadow under the plane. Anchors the "send" metaphor and the goldenrod hue. Warm / friendly / consumer — reinforces the app's identity but marketing typography around the window must never be conflated with the app's own type.
