# Subscription Day — profile

- **Source:** macapp.supply (`subsday.appps.od.ua`, developer `appps.od.ua`) · **Surfaces digested:** Statistics dashboard, dark mode (1 surface, from marketing composite cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** A monochrome-dark subscription-spend dashboard that reserves *all* colour for the data — Copilot Money / Bobby / Rocket Money's consumer-fintech register delivered as an iOS-design-language app bridged onto Mac chrome, with a radar chart where its peers use bars.
- **Cluster:** unassigned — candidate for a "dark consumer-fintech dashboard" cluster (sole member so far). Lineage-gated: its iOS-derived body grammar is recorded as tells + corrections and does **not** feed macOS native canon.
- **Lineage:** catalyst / SwiftUI-multiplatform (med) — judged from the *body*, not the frame. The window wears a correct Mac frame (traffic-light cluster, centered title, trailing borderless SF-Symbol toolbar), but the content is iOS design language: capsule segmented control (not the macOS bordered segmented control), inline pill badges, iOS-scale density (large rounded display type, big controls, ~15–17pt-class body rather than 13pt). One indie shipping Mac + iPhone + Watch (all three appear in the cover) is the classic multiplatform-SwiftUI/Catalyst signature. Confidence medium because the exact bridge (Catalyst vs SwiftUI-multiplatform) can't be settled from one render — but the corpus consequence is identical either way.
- **Era (chrome):** custom (Big-Sur-era rounded lineage underneath) — a committed dark house style dominates over platform-material expression. No visible Liquid Glass lensing tells on the chrome; whether the tooltip card / segmented track are system materials vs flat fills is `(insufficient-evidence)` in dark mode. Not legacy (rounded, current-dated UI: "2025"/"January, 2026").

> **Evidence caveat:** the only app UI is the Mac window *inside a 1200×630 marketing composite* (`cover.jpg`) — a stylized product render on a yellow rounded-tile backdrop, flanked by an iPhone and Apple Watch (both **contrast evidence only**, excluded from mac canon). Scale is unknowable, so every pixel value below is a ratio/estimate at low confidence — no `(measured)` marks are honest here. The traffic lights render as three flat grey dots (either marketing desaturation or an inactive-window state — ambiguous). Everything outside the Mac window (yellow backdrop, the floating app icon, the iPhone/Watch) is **brand / contrast evidence** and is kept separate from app-UI tokens.

## Tokens

### App UI — Statistics dashboard, dark mode (all `(estimated)(inferred)` — single stylized render)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | near-black charcoal ~#1C1C1E–#222 | (estimated)(inferred) | Window background; close to kit dark window bg #1E1E1E, slightly warmer/darker. Reads near-uniform, footer zone marginally separated |
| bg/card-tooltip | lighter grey ~#38383C, softly translucent | (estimated)(inferred) | The "April / $49 / Apple Fitness+" floating tooltip and the badge/segmented fills sit ~1 tonal step above canvas |
| accent/system | **none used** | (estimated)(inferred) | No blue/system-accent anywhere; selection + toolbar + segmented control are all monochrome grey. See Signature moves |
| color/data-identity | category-palette hues (green Fitness+ glyph; green + white chart vertices) | (estimated)(inferred) | Colour enters ONLY through data/category identity, never chrome |
| type/hero-number | ~34–40pt-equiv, bold, SF Pro Display/Rounded | (estimated)(inferred) | "$369" / "$31" footer KPIs — the loudest elements on the surface |
| type/title | ~26–30pt-equiv bold | (estimated)(inferred) | "Statistics" section title |
| type/body-secondary | ~15–17pt-equiv, secondary grey | (estimated)(inferred) | "You have 8 active subscriptions in 2025" — iOS-scale, not 13pt AppKit body |
| type/label-caption | ~11–12pt-equiv, tertiary grey, 2-line | (estimated)(inferred) | "Yearly Payment Forecast" / "Average Monthly Cost" — quiet label under a loud value |
| badge/pill | grey capsule fill ~#3A3A3C, lighter text, height/2 radius | (estimated)(inferred) | "PRO" (in titlebar) and "2025" (beside title) |
| control/segmented | iOS-style capsule track, raised grey "Year" selected, no accent tint | (estimated)(inferred) | Year \| Category scope switch; capsule not the macOS bordered segmented control (lineage tell) |
| chrome/toolbar | trailing borderless monochrome SF Symbols: search · calendar · gear | (estimated)(inferred) | The single most native-correct element on the surface |
| chrome/title | centered "Subscription Day" + inline "PRO" pill | (estimated)(inferred) | App-name-as-window-title violates HIG toolbar rule; inline badge non-standard (see Defects) |
| divider/hairline | ~1px low-contrast separator under toolbar and above footer | (estimated)(inferred) | Two horizontal rules chunk the surface into title / chart / footer |
| stat-glyph/circle | monochrome SF Symbol (wallet, sync) in a subtle grey circle | (estimated)(inferred) | Leading each footer KPI |

### Brand / contrast (NOT app-UI tokens — kept separate)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | warm yellow ~#F5E285 with a faint tiled-rounded-rectangle (app-grid) pattern | (estimated)(inferred) | Marketing ground; playful/warm — deliberately opposite the dark app |
| icon/composition | dark rounded-squircle, 3D glossy: a yellow circular "restore/refresh" arrow orbiting a radar dial (dark sphere hub, thin spokes) with blue/purple/green arc segments + two gold sparkle stars | (estimated)(inferred) | **Brand context only (Workflow A, not an icon digest).** Rhymes tightly with the in-app radar chart and category hues — the icon *is* the dashboard's hero viz. Sparkles read as Pro/AI signal |
| contrast/iphone | dark month-calendar view, "$69.25 / January 2026 / Regular Month" green pill, app-grid of service logos | (estimated) `platform: iOS` | Excluded from mac canon; corroborates the monochrome-chrome / coloured-data grammar |
| contrast/watch | complication + notification "Subscription Day: …billed in 3 days" | (estimated) `platform: watchOS` | Excluded; evidences the multiplatform footprint that drives the lineage read |

## Layout skeletons

**Statistics dashboard (cover.jpg, dark):** unified toolbar across the top — leading traffic-light cluster, centered title + PRO pill, trailing 3-icon borderless group (search / calendar / settings); a hairline closes the toolbar. Content splits three ways vertically:
1. **Header row** — left: "Statistics" + "2025" pill, then a 2-line secondary subtitle ("You have 8 active subscriptions in 2025"); right, top-aligned: the "Year | Category" capsule segmented control. Left edge of the title shares a vertical axis with the subtitle and the leading footer KPI.
2. **Chart body** — a centered radar/spider chart (12 spokes, low-contrast grey web, one data polygon) with a selected white vertex on the right that anchors a floating tooltip card ("April · $49 · 🟢 Apple Fitness+ · $30"), and a green vertex at the bottom.
3. **Footer bar** — divided off by a hairline; two horizontally-laid KPI blocks, each = circled monochrome glyph + very large value + small 2-line caption ("$369 / Yearly Payment Forecast", "$31 / Average Monthly Cost").

## Signature moves
- **[GOLDEN-NUGGET] Greyscale chrome, coloured data — colour is spent only where information lives.** The entire UI shell is monochrome charcoal/grey: no system accent, monochrome selection, monochrome toolbar. Hue appears *exclusively* in the payload — the radar-chart vertices (green/white) and the category glyph badge (green Fitness+). The effect is Von-Restorff/signal-detection: because the field is greyscale, every coloured mark reads as pre-attentive *figure*, so "which subscription, which month" pops without a legend fighting the chrome. This is the app's whole character in one decision, and it's carried consistently across Mac, iPhone (green "Regular Month" pill, coloured service tiles on a dark grid) and Watch.
- **[GOLDEN-NUGGET] A radar chart as the hero subscription-spend viz.** Peers (Bobby, Rocket Money, Emma) reach for bars, pies, or lists; a 12-spoke polar chart for spend-around-a-year is a genuinely non-obvious, characterful choice — and it's echoed by the app icon's radar-dial motif, so brand and UI share one form. (Whether it *reads* better than a bar chart is a separate legibility question — see Defects on its gridline contrast.)
- **Value-over-label discipline in the KPIs.** "$369"/"$31" are the largest, brightest things on the surface; their captions are small tertiary grey — the number speaks, the label whispers. Correct stat-tile hierarchy (hierarchy-rhythm rule 7).

## Defects
- **App name as the window title (HIG toolbar violation).** `toolbars.md`: "Don't title windows with your app name… keep the title under 15 characters." "Subscription Day" is exactly the app name (16 chars). Native canon would leave it empty or carry the view title ("Statistics"). Compounded by the inline "PRO" pill inside the titlebar — AppKit titles are text-only.
- **iOS grammar on Mac chrome (lineage tells, excluded from canon).** The capsule segmented control is the iOS style, not the macOS bordered segmented control; density is iOS-scale (large rounded display type, big controls, ~15–17pt body vs the 13pt kit body); pill badges are inline. Per the lineage gate these are recorded as tells with their native corrections, never learned as mac taste.
- **Contrast Dilution risk on the radar web + dim secondary labels.** The radar gridlines are very low-contrast grey-on-charcoal (reads <3:1 — rubric #10); the dimmest secondary/tertiary greys ("You have 8 active…", the KPI captions) sit near or below the 4.5:1 text floor (#9). Defensible as data-chrome de-emphasis, but flagged: the chart is the hero viz, so a hero rendered near-invisible is a real cost, not just decoration.
- **Content typo in the shipped marketing cover:** "Apple **Fintess**+" (Fitness+). QA defect in brand material, not a design-token issue — noted because it's the cover the store displays.
- **Evidence poverty (not the app's fault):** one surface, dark only, from a render. Grid adherence (#1) is unverifiable, real pt sizes are estimates, and light mode, settings, list/detail, empty states, onboarding, and the actual traffic-light colours are all unseen.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Statistics dashboard (dark, marketing render) | 11/14 | #9 text contrast — dim secondary/tertiary greys near the 4.5:1 floor on charcoal · #10 UI contrast — radar gridlines & hairline dividers <3:1. Caveat: #1 grid adherence unverifiable from a render (counted pass-with-caveat, not a clean pass). #12/#14 N/A (no text inputs, no focus state in a static render) |
| — native-tells audit | 5/10 | FAIL #1 lineage reads iOS-design-language bridged (not AppKit-native) · #3 selection is iOS capsule, no accent tint · #5 iOS-scale density, not 13pt/20–28pt · #10 app-name window title + inline titlebar badge + grey traffic lights. PASS #2 no glass-in-content violation (glass itself insufficient-evidence) · #6 accent absent but identity colours correctly kept to data · #7 no competing CTAs · #8 corners plausibly concentric · #9 toolbar borderless grouped symbols (the most native-correct element). N/A #4 (no sidebar) |
