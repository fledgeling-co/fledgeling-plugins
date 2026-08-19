# Zonedial — profile

- **Source:** macapp.supply (Codenta) · **Surfaces digested:** marketing cover only — **no captured app window** · **Last updated:** 2026-07-19
- **One-sentence identity:** A world-clock utility whose only supplied evidence is a "network-glow" marketing composite — electric-blue-on-near-black in the reflex dark-dev-tool register, with macOS Notification-Center-style time cards standing in for real UI.
- **Cluster:** unassigned (insufficient native evidence — marketing-only)
- **Lineage:** unknown (low confidence) — Apple-ecosystem *intent* is unmistakable (a "Built for macOS" badge, the 9:41 placeholder time, Apple squircle flag emoji, SF-like type, Notification-tile card styling), but native vs Catalyst vs SwiftUI vs Electron is **unknowable** from a render carrying no window chrome, no controls, and no density evidence. Non-native evidence never feeds macOS canon — and neither does this, because there is no surface to read.
- **Era (chrome):** unknown / custom-rendered — the cards are dark translucent rounded rectangles that *evoke* Liquid-Glass/widget material, but material discipline cannot be audited on a marketing float.

## What this cover actually is

A 1536×1024 marketing composite, not an app screenshot. Two evidence layers, kept separate:

1. **Brand layer (the composite):** dark navy-to-black ground, a 3D dotted-map globe with great-circle connection arcs, four floating city time-cards (San Francisco / London / Tokyo / Sydney), a 3D physical clock, the Zonedial wordmark + tagline + body copy, a 4-up feature-icon row, two outlined badge buttons ("Built for macOS", "Available on GitHub"), and a Codenta footer. This is **brand evidence**, analysed but never promoted to macOS canon.
2. **Indicative UI layer (the time cards):** the closest thing to app design language, but marketing-rendered (9:41 placeholder, staged glow), so read as *aspirational card grammar*, marked `(estimated)(inferred)` and excluded from canon.

There is **no traffic-light chrome, toolbar, sidebar, menu bar, or window frame anywhere in the image.** Per HIG `windows.md`, getting the frame right is the single biggest native-feel contributor — and none is shown, so the cover contributes zero native-tells evidence.

## Tokens

All values are brand-layer or indicative-card readings from a marketing render — none are app-surface truth.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | `#000516` → `#00071A`, glow `#022776` behind globe (measured)(inferred) | | near-black navy, radial blue glow — brand backdrop, not a window bg |
| accent/brand-blue | `#0E6DFF`–`#2367FF` electric (measured)(inferred) | | tagline, feature icons, card abbr, links; **more saturated/indigo than macOS system blue** (kit Blue `#0088FF`/`#0091FF`) — a brand choice, see Defects |
| type/wordmark | white `#F5F4F7`, bold geometric-humanist sans (SF Pro Display Bold-class) (estimated)(inferred) | | large display lockup |
| type/tagline | brand-blue, medium, ~Title-class (estimated)(inferred) | | "Timezone Math for Your Schedule" |
| type/body | white, regular, 3 short lines (estimated)(inferred) | | marketing body, ~65ch-safe |
| card/fill | dark navy translucent `#031232`-class (measured)(inferred) | | Notification-tile look, floating over globe |
| card/radius | ~20–24px at render scale (estimated)(inferred) | | continuous-corner rounded rect; render-scale, not point-truth |
| card/text-primary | time `#EEEDF2` white, large, tabular (measured)(inferred) | | "9:41 AM" — the card's dominant element |
| card/text-secondary | city name white + Apple flag emoji, medium (measured)(inferred) | | header row |
| card/text-tertiary | abbr in brand-blue caps ("PDT"/"BST"); day ("Wed") in gray (measured)(inferred) | | blue is accent, gray is genuine de-emphasis |
| feature-icons | brand-blue line icons (globe/people/lightning/calendar), ~1.5–2px stroke (estimated)(inferred) | | 4-up row, hairline vertical dividers between |
| badge/button | outlined pill, hairline border, white label + white glyph (measured)(inferred) | | "Built for macOS", "Available on GitHub" — marketing CTAs |

## Layout skeletons

**Marketing composite (whole cover):** two-column split. LEFT (~0–52% width): vertical brand stack top-to-bottom — icon+wordmark lockup → blue tagline → 3-line body → 4-up feature-icon row (equal columns, thin vertical rules) → two outlined badge pills → Codenta footer with vertical rule. RIGHT (~55–100%): a 3D dotted globe centered high, four city time-cards floating at varied depths around it connected by glowing great-circle arcs, a 3D clock resting bottom-right. Conventional F/Z marketing scan: brand thesis top-left, product-glamour render right, CTAs bottom-left.

**Indicative time card (component):** rounded dark translucent tile, ~16px internal padding. Three left-aligned rows on one axis: (1) flag emoji + city name; (2) large time value (dominant); (3) timezone abbreviation in accent blue, with an optional right-aligned day chip in gray on the Tokyo/Sydney variants. This is the app's *stated* card grammar — plausible for a menu-bar-extra dropdown or a small primary window, but unconfirmed.

## Signature moves

- **The "world-network" composite trope** — 3D dotted globe + great-circle connection arcs + floating city time-cards + a physical 3D clock. Competent and on-theme for a timezone tool, but a *familiar* marketing signature, not a distinctive design one. Reads as category-generic "global SaaS" glamour.
- **One-accent discipline (brand-level):** a single electric blue carries every non-white element — tagline, all four feature glyphs, card abbreviations, links, the Codenta mark — against near-black. Von Restorff by construction; the blue is the only chromatic event. This *is* a real, if reflexive, aesthetic commitment (Neo-grotesque-product / dark-utility family).
- **Jakob's-Law card schema:** the time cards borrow Apple's world-clock/Notification-tile anatomy (flag + city + big time + abbr) verbatim, so the concept parses in <1s. Whether the shipped app honors this is unknown.

## Defects

- **Accent-binding risk (watch-item, not confirmed):** the brand blue is `~#1666FF` electric/indigo — noticeably more saturated than the macOS system accent (`#0088FF` light / `#0091FF` dark). Fine as a marketing brand color; but if carried into the app's selection/focus/primary-action chrome unchanged, it would violate the native rule that the accent is *the user's* `controlAccentColor`, not the app's. Cannot confirm without an app screenshot.
- **No verifiable UI evidence (honesty flag, not an app defect):** the cover shows no window, so the app's real spacing grid, control density, chrome, and native-tells are entirely unaudited. Anyone treating the marketing cards as the app's UI would be building on staged renders (9:41 placeholder, glow).
- **Marketing-render Contrast watch:** brand-blue abbreviations (`#0E6DFF`) on the dark navy card (`#031232`) sit near the 4.5:1 text floor — plausibly passing at large size but worth measuring on the real surface; the hairline card border likely falls under the 3:1 non-text floor (again, render-only).

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| Marketing composite — indicative time-card only | 8/14 (of ~10 applicable; render, not app UI) | #10 UI contrast (hairline card border likely <3:1); #7 partial (city + time both near-white — size carries hierarchy, mild dilution); #6/#8/#11/#12/#13/#14 n/a (no paragraphs, no nesting, no interactive/form/focus elements on a static card) |
| Native-tells audit | 2/10 | #1 lineage unreadable (no chrome/controls); #10 no genuine window/traffic-lights; #3/#4/#5/#7/#9 n/a (no selection, sidebar, control density, actions, or toolbar present); loose passes only on dark-mode-authored card + accent-paired-with-label |

**Note for synthesis:** Zonedial contributes **brand evidence + one indicative widget-card grammar** and **zero native macOS canon evidence**. Do not cluster it or promote any token from it. A real app-window screenshot (menu-bar-extra dropdown or primary window) would be needed to classify lineage/era and audit native fidelity. The app icon (icon.png, 1024²) is out of scope for this UI digest — a separate Workflow-B icon digest owns it.
