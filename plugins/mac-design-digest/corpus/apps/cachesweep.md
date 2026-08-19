# Cachesweep — profile

- **Source:** macapp.supply (cover composite only; no standalone UI shots supplied) · **Surfaces digested:** menu-bar extra panel (dark, environmental-blue-tinted glass) · **Last updated:** 2026-07-19
- **One-sentence identity:** iStat Menus' menu-bar-native residency crossed with a live disk-telemetry feed — a SwiftUI `MenuBarExtra` utility that reframes "how much can I reclaim?" as one giant number over Liquid Glass.
- **Cluster:** unassigned (candidate: menu-bar-glass-utility / glass-telemetry)
- **Lineage:** native (med-high) — macOS-correct SwiftUI `MenuBarExtra`; genuine `NSStatusItem` (highlighted in the menu bar) with an anchored popover caret, SF Symbols throughout, Liquid Glass material. Carries several SwiftUI-multiplatform/iOS list idioms (see Defects) — native lineage, not hand-tuned AppKit source-list. Non-native idioms are logged as tells, not learned as mac canon.
- **Era (chrome):** Liquid Glass native (macOS Tahoe / 26–27) — translucent panel adopts the wallpaper's blue/purple tint; capsule primary button; no hard opaque bar-lines.

## Evidence caveat
Single surface, and it is a **1200×630 marketing cover composite** (brand headline + Dock + wallpaper around the app), not a clean @2x screenshot. The app *window* (a menu-bar popover, top-right) is the design evidence; the giant "Cachesweep" wordmark, Download/GitHub buttons and "Free & open source · MIT · macOS 15+ · 13 languages" caption are brand evidence, analysed separately and never merged into UI tokens. All UI measurements are logical-point estimates at ~1× render scale — provenance is `(estimated)(inferred)` throughout. The panel background is Liquid Glass tinted by the wallpaper behind it, so no fixed background hex is recoverable — recorded as `(insufficient-evidence)`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| material/panel | Liquid Glass (Regular), adaptive wallpaper tint | (estimated)(inferred) | reads deep blue ~#13366F→#213380 here purely because the wallpaper is blue; NOT an app-chosen surface colour |
| bg/panel | (insufficient-evidence) | — | environmental tint; cannot separate app fill from lensed wallpaper in one still |
| radius/panel | ~16pt | (estimated)(inferred) | menu-bar popover corner; sits above kit's Popover-body 20 but window/panel radius is fragmented in this era |
| panel/width | ~340pt | (estimated)(inferred) | wider than a plain NSMenu dropdown; rich-panel width |
| type/hero-metric | ~34–38pt SF Pro, Regular/Light, white primary | (estimated)(inferred) | "120.3 MB" — the dominant element; scale-driven hierarchy |
| type/section-header | ~10–11pt SF Pro Semibold, **tracked UPPERCASE**, white ~50% | (estimated)(inferred) | "LIVE ACTIVITY", "DEVELOPER CACHES" — non-native tell (see Defects) |
| type/row-title | ~13pt SF Pro Semibold, white primary | (estimated)(inferred) | kit Body/Headline 13pt — platform-correct |
| type/row-path | ~11pt SF Pro Regular, white ~55% | (estimated)(inferred) | de-emphasised path metadata; kit Subheadline 11pt |
| type/button-label | ~14–15pt SF Pro Semibold, white | (estimated)(inferred) | "Clean Selected" |
| accent/primary | system blue (selection check + primary button) | (estimated → assumed system accent)(inferred) | reads brighter over glass; bound to selection + one CTA |
| status/growth | system green, ▲ up-triangle + delta ("340.5 MB") | (estimated)(inferred) | glyph-paired — colour never alone; the signature telemetry mark |
| badge/new | amber pill ~#BB861E fill, small "new" | (measured)(inferred) | on `~/Library/Caches` rows just written |
| control/primary-button | full-width capsule, h ~34–36pt (XL tier), capsule radius | (estimated)(inferred) | kit XL 36pt control tier; one prominent action |
| control/select | trailing circular checkbox ~18–20pt; selected = filled accent + white check; unselected = hollow gray ring | (estimated)(inferred) | iOS/SwiftUI selection idiom, not macOS inset-fill selection |
| icon/tile | rounded-square ~28pt, radius ~6–8, tinted fill (green for dev caches), monochrome SF Symbol (folder / shippingbox) | (estimated)(inferred) | iOS-Settings-style icon chip idiom |
| row/height | ~44–48pt, two-line (title + path) | (estimated)(inferred) | comfortable, leans iOS 44pt over macOS 24–28pt dense rows |
| space/section-pad | ~16pt block padding, 8pt grid, hairline separators | (estimated)(inferred) | proximity honoured; dividers between sections |
| brand/mark | white 4-point sparkle glyph (one large + one small) | (measured)(inferred) | echoes the app icon; appears in the panel header beside the wordmark |

## Layout skeletons

**Menu-bar extra panel (single surface), top → bottom, ~340pt wide:**
1. **Header row** — leading sparkle brand glyph + "Cachesweep" wordmark (white semibold); trailing borderless refresh (`arrow.clockwise`) symbol. Anchored below the highlighted status item by a small popover caret.
2. **Hero block** — giant "120.3 MB" reclaimable figure (single dominant element), one secondary line "2 selected · 120.3 MB found in total".
3. **Primary action** — full-width capsule "Clean Selected", saturated system blue, the only filled button in the view.
4. **LIVE ACTIVITY section** — tracked-uppercase header + right-aligned "writing now" with a green pulse dot; rows = folder glyph, path, and a `size ▲ green-delta · timestamp` line ("1.58 GB ▲ 340.5 MB · just now"). This is the live-growth feed.
5. **DEVELOPER CACHES section** — same header treatment; scrollable multi-select list. Each row: leading tinted rounded-tile SF Symbol · title + path (two lines) · trailing size (or "–") · circular checkbox. General Cache selected (filled blue check); npm/Yarn/pnpm unselected (hollow ring). List scrolls under the panel edge / off-frame.

Alignment: three columns share vertical axes — leading icon-tile column, label/path column, trailing value+checkbox column.

## Signature moves
- **[GOLDEN-NUGGET] Live disk-telemetry feed inside a menu-bar panel.** The "LIVE ACTIVITY / writing now" section shows caches *growing in real time* — green ▲ deltas ("▲ 340.5 MB"), "just now / 5s" timestamps, amber "new" badges on freshly-written paths. The product's entire thesis ("shows you what's eating your space — live") is rendered as a running feed, not a static scan result. The green up-triangle delta is the character mark; it is always glyph-paired, so it stays native-legal while carrying the app's identity.
- **Scale-as-hierarchy hero number.** A ~36pt "120.3 MB" makes the reclaimable figure answer the user's one question pre-attentively; everything else defers to it. Von Restorff + processing fluency in one decision.
- **Brand sparkle continuity.** The icon's 4-point sparkle reappears as the in-panel header glyph — cheap, disciplined identity thread from Dock to content.

## Defects
- **Tracked-uppercase group headers** ("LIVE ACTIVITY", "DEVELOPER CACHES") → the native grammar (and macOS 27 kit) wants sentence/title-case system-font semibold section headers; tracked uppercase is the #1 non-native (iOS/web) header tell. Systematic across both sections → a house-style choice, but it reads SwiftUI-multiplatform, not AppKit. Canon would set sentence case, secondary colour.
- **Selection = circular checkmark, not inset accent fill.** macOS list selection grammar is a flat inset-rounded accent fill with accent-tinted text; Cachesweep uses trailing `checkmark.circle.fill` / hollow-ring toggles — an iOS/SwiftUI list idiom. Legible, but not the native selection move.
- **iOS-style tinted icon-chip tiles** (green rounded square holding a `shippingbox` symbol) → native macOS lists show plain SF Symbols or file icons; the coloured rounded-tile chip is a Settings-app/iOS idiom.
- **Contrast Dilution risk on glass** → secondary/tertiary white metadata (~25–50% white: "writing now", paths, timestamps) and the hollow unselected rings / hairline separators likely fall below 4.5:1 text and 3:1 non-text against the mid-blue glass. `(estimated)` — the environmental tint makes exact ratios unrecoverable from this composite; flag, don't assert.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar extra panel (dark/glass) | 11/14 | #9 secondary/tertiary text contrast on glass (est <4.5:1); #10 hollow rings + separators <3:1 (est); #14 focus state not evaluable from still |
| — native-tells audit | 7/10 | #3 selection idiom (circular check, not inset fill); #4 tracked-uppercase section headers; #5 density/rows lean iOS-comfortable (44px) |
