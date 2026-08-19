# Code Meter — profile

- **Source:** macapp.supply (codemeter.dev) · **Surfaces digested:** cover.png marketing composite — four app panels: All-providers list, Provider dashboard, Widgets & alerts, Usage-history charts (all dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar quota monitor for AI coding subscriptions that dresses itself as a physical usage *meter* — pixel-display readouts and green/amber/red gauges give iStat Menus' at-a-glance discipline a Playdate-retro instrument face.
- **Cluster:** terminal-instrument-dark (proposed; menu-bar-utility register — see cluster_hint)
- **Lineage:** native (med) — MenuBarExtra-style opaque popovers; SF-Symbol footer glyphs (gear/power/share/line-chart/refresh), OS-rendered Notification Center banners, and a window bg of exactly `#1E1E1E` (the kit's specified dark window ground) all read AppKit/SwiftUI. Uncertainty: the fully bespoke pixel-font theme could in principle be a Tauri/Electron shell reusing SF Symbols + real macOS notifications — no web tell (pointer-hand, kebab, uppercase-tracked *nav*) is visible to rule it in or out. Heavy custom theming means most distinctive choices are house-style, not learnable mac taste.
- **Era (chrome):** custom — bespoke dark instrument theme; not stock Liquid Glass chrome, not legacy-native. No system titlebar/traffic-lights present (popover surfaces).

> **Digest scope note.** cover.png is a marketing composite: four app panels floated at slight perspective on a dark warm-amber radial backdrop. The **panels are design evidence**; the brown vignette + the "Usage history / Widgets & alerts / All providers / Provider dashboard" caption labels are **brand/backdrop evidence**. Panels are enlarged (and two are tilted), so **all pixel sizes are `(estimated)` with wide ranges** — proportions and colours are the trustworthy readings, absolute pt are not. Retina scale indeterminate (composite render, not a screengrab).

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#1E1E1E` (measured)(confirmed) | | Popover/panel ground. **Exact match to kit dark window bg `#1E1E1E`** — a point of platform fidelity under all the custom theming. |
| bg/card | warm charcoal ~`#26221E`–`#2A2622` (estimated)(confirmed) | | Provider cards + stat tiles; a step lighter than ground, faintly warm (amber backdrop bleeds). Subtle elevation, no visible border-stroke > ~1px. |
| text/primary | `#E3E3E3` warm off-white (measured)(confirmed) | | Not pure `#FFF` — softened, like the kit's 85%-black discipline inverted. |
| text/secondary | warm gray ~`#8A857E` (estimated)(confirmed) | | Metric labels (Weekly/Suggestions/This Period), captions (Resets in…). |
| status/green (healthy) | `#74D98C`–`#77DA84` (measured)(confirmed) | | Low-usage rings, bars, values. A soft mint-lime — **brighter/limier than system green `#34C759`**. |
| status/amber (warning) | `#F2A644` (measured)(confirmed) | | Elevated usage (71–88%). Warm amber. |
| status/red (critical) | `#EC6756` coral (measured)(inferred) | | Near-full usage (96%). One instance seen (Minimax). |
| accent/brand-orange | `#D2683E`–`#D57048` terracotta (measured)(inferred) | | Single-hue accent on the **widget + history** surfaces (rings, chart line/fill, callouts). Distinct from the green/amber/red *status* system — see Defects (accent split). |
| track/unfilled | dark gray ~`#2C2A28`, ~10–15% over ground (estimated)(confirmed) | | Ring + bar unfilled portion; deliberately low-contrast (<3:1) instrument styling. |
| type/display | pixel/bitmap display face (custom), blocky mono (estimated)(confirmed) | | Wordmark "Code Meter", every gauge numeral ("42"), and tracked-caps labels (5-HOUR, WEEKLY, WINDOW). The character font. Silkscreen/Departure-Mono-class. |
| type/body | humanist/system sans, reads as SF Pro (estimated)(confirmed) | | Provider names, captions, notification body — clean neutral sans, NOT the pixel font. Clear two-typeface split. |
| gauge/ring | ~270° arc, thick round-cap stroke, value colour on dark track (estimated)(confirmed) | | Hero dashboard gauge large; list rings ~compact; widget rings thin-stroke. |
| badge/plan | capsule pill, translucent white ~8–10% fill, secondary text (estimated)(confirmed) | | Trailing plan tier: Max (5x) / Plus / Pro / Token Plan. |
| radius/card | ~12–14px card inside ~16–18px panel (estimated)(confirmed) | | Steps down concentrically (child < parent). |
| control/segmented | capsule-pill selection, light-gray fill + white text, secondary unselected (estimated)(inferred) | | Now·6H·1D·1W range switch (1D selected) on history view. |
| control/icon-button | bordered rounded-rect (~8px) SF-Symbol buttons in dashboard footer (estimated)(inferred) | | chart / share / gear / power — *bordered*, diverging from borderless-toolbar norm (see native audit #9). |

## Layout skeletons

**All providers (main menu-bar list) — dark.** Header: pixel-font wordmark "Code Meter", top-left. Vertical stack of ~7 provider **cards**, each a full-width row: [left] compact ring gauge with pixel-% inside · [glyph] brand logo (monochrome) + provider name (body sans, ~large) · [trailing] plan-tier pill. Second line inside card: metric label (secondary) + horizontal progress bar + trailing bold % (status-coloured). Footer bar: refresh countdown "00:04" (circular-arrow) at leading; borderless icon cluster (layout/split, gear, power) trailing. Ring value and bar value are *different windows* of the same provider, each status-coloured independently (Kimi: 71% amber ring, 44% green bar).

**Provider dashboard (single-provider detail) — dark.** Header: wordmark + provider selector "✳ Claude" (glyph + name). Hero: large ~270° green ring, centre pixel-numeral "42" + superscript %, tracked-caps "5-HOUR" beneath; "⏱ Resets in 2h 29m" centred caption. Two stat tiles side-by-side (WEEKLY 31% / SONNET 28%) each: tracked-caps label + glyph + bold % value + thin progress bar + reset caption. Full-width "🐢 UNDER PACE" card: bold green "−5.2% per hour" + secondary "Plenty of capacity remaining." + small green up-trend sparkline right. Footer: refresh "16:06" leading; four *bordered* icon buttons (chart/share/gear/power) trailing.

**Widgets & alerts — dark.** Top: desktop-widget card, two thin rings (5-HOUR 42% / WEEKLY 28%) in brand-orange with reset captions. Below: a fanned cascade of **OS-native Notification Center banners** (app icon + "Code Meter" + "now" + bold title + body): High Burn Rate, 50/75/90% Usage, Rate Limit Reached, Quota Running Out Soon. Notifications are system-rendered (native chrome), not app-drawn.

**Usage history — dark.** Top: 4-segment capsule control (Now·6H·1D·1W, 1D selected). Two stacked area charts: "WINDOW" (0/25/50% dashed gridlines, x=12·15·18·21·00, orange stepped line + gradient fill, bold "5%" current-value callout) and "USAGE" (same axes, rising to bold "36%"). Single-hue orange data-viz, dashed gridlines, tracked-caps section labels top-left.

## Signature moves
- **[GOLDEN-NUGGET] The meter *is* the metaphor.** A pixel/bitmap display face renders the wordmark and every numeral, wrapped in circular dial gauges and a green/amber/red traffic-light status ramp — the app costumes itself as a physical usage meter/instrument. Subject-mining ("meter" → LCD readout, dial, instrument panel) done fully: the boldness budget is spent on one committed idea, everything else (body sans, card grid) stays quiet. This is why it isn't anonymous.
- **[GOLDEN-NUGGET] Dual-window provider card.** Each row carries two independent quota readings — a ring (one window) + a horizontal bar (another window) — each status-coloured to its *own* threshold. A dense, pre-attentively scannable multi-provider board where the one at-risk provider (red 96% Minimax) pops out of a field of green.
- **Tracked-caps mono labels as house style.** 5-HOUR / WEEKLY / WINDOW / UNDER PACE in letter-spaced pixel caps. This *deviates* from native macOS type grammar (which forbids tracked-uppercase headers) — but here it is a deliberate terminal/instrument aesthetic, systematic across all four surfaces, so it is recorded as signature-with-caveat, not a defect.

## Defects
- **UI contrast (#10) — low-contrast instrument tracks.** Unfilled ring/bar tracks and card border-strokes sit <3:1 against the `#1E1E1E` ground. Conventional for dark gauges (the filled arc carries the signal), but strict WCAG non-text contrast fails on the empty track. Corrective: lift track to ≥3:1 or accept as a deliberate gauge convention.
- **Accent split / semantic ambiguity (contested).** The **live** surfaces (list, dashboard) use a green/amber/red *status* semantics keyed to usage; the **widget + history** surfaces use a single terracotta-orange *brand* accent — so the same 42% reads **green** on the dashboard but **orange** in the widget. Either a per-surface theming decision or a genuine inconsistency; from a marketing composite it cannot be settled. Native rule: status colour should map consistently and always pair with a value (the value-pairing it honours; the hue-consistency it strains). Marked low-confidence pending a real screenshot set.
- Focus appearance (#14) unobservable in a static marketing render — not scored.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| All providers (list) | 12/14 | #10 low-contrast ring/bar tracks; #14 focus unobservable (n/s) |
| Provider dashboard | 12/14 | #10 low-contrast gauge track + faint tile borders; #14 n/s |
| Widgets & alerts | 12/14 | #10 low-contrast widget-ring tracks; #14 n/s (notifications are native chrome, not scored as app design) |
| Usage history | 12/14 | #10 dashed gridlines <3:1; #14 n/s |

**Native-tells audit (representative, list + dashboard): ~7/10.** Passes: lineage native (med); opaque content, no glass-in-content/glass-on-glass; concentric corners; genuine popover chrome (no faked traffic lights); SF-Symbol glyphs; segmented control used HIG-correctly (in-view scope switching, not navigation). Deviations: tracked-uppercase labels vs sentence-case norm (#4-adjacent, house style); accent-binding split across surfaces (#6); dashboard footer uses *bordered* icon buttons vs borderless-toolbar norm (#9). Density (#5) not confirmable — render enlarged.

## Knowledge gap this app leaves
No light-mode evidence; no settings/preferences window; true control density (13pt-class body? row pt?) unmeasurable from an enlarged composite. A real @2x screengrab of the popover and the settings window would confirm lineage (native vs Electron) and let the pixel-font/gauge system be measured rather than estimated. First member of a would-be **terminal-instrument-dark** menu-bar cluster — needs ≥2 more menu-bar utilities in this register before any cluster identity promotes.
