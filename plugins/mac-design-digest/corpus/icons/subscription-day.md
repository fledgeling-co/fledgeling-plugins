# Icon: Subscription Day

- **Era:** Big Sur unified (3D-render dialect — a rendered glossy scene, NOT Liquid Glass) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, SHA-1 `ab814877`) · **Category:** Lifestyle
- **What the app does:** tracks paid subscriptions and shows spend statistics (radar chart, category donut) across macOS/iOS/watchOS.

| Dimension | Reading |
|---|---|
| Background | Charcoal squircle, radial vignette ramp `#5B5B5B` (upper) → `#363636` (edges/bottom), recessed dial well `#262626` (measured, ±4 levels) |
| Glyph | Abstract data-viz emblem: a segmented category **donut ring** + a **radar/spider-chart hub** (matte 3D sphere `#4B4B4B` on hairline spokes `#636363`). Optically anchored just below true centre (sphere at ~x447/y470 of 894) — reads centred, composition weighted right |
| Overlay device | Two amber **sparkle stars** `#FFAD3E` top-right (badge/insight flourish); the amber ring terminates in an **arrowhead** (renewal loop) — integral, not overlaid |
| Light model | Single top-left key, soft top-down. Baked short drop-shadows under each floating segment + arrowhead; baked specular highlights on the upper edge of every colour bar and the sphere; background radial vignette. Effects are **baked in** (anti-HIG for macOS 26 layered icons) |
| Layer stack | bg vignette → recessed dial well → radial hairline spokes → 4 glossy colour segments → central 3D sphere hub → amber arrowhead (front of ring) → 2 sparkle stars (frontmost) |
| Palette economy | 1 neutral ground + **4 saturated hue families** in the ring (amber/cyan/purple/green) — exceeds the ≤2 floor; justified as a category legend, but a rubric miss. Amber `#FFD171` is the dominant focal accent |

## Signature devices
- **Renewal-arrow ↔ chart-arc fusion** `[GOLDEN-NUGGET]` — the dominant yellow donut segment terminates in an arrowhead, so the recurring-payment loop and the largest spend category are drawn with one stroke. The subject's two core ideas (it recurs; here's the breakdown) collapse into a single mark.
- **Radar/spider stat hub** — radial hairline spokes converging on a matte 3D sphere quote a statistics chart; this is a literal miniature of the app's in-product radar chart (see cover), not a generic gauge.
- **Category-colour donut** — 4-hue segmented ring encodes subscription categories, mirroring the app's coloured category chips.
- **Nocturnal charcoal ground with vignette** — dark-mode-first icon; the puffy glossy 3D elements are the entire brightness budget against a near-black stage.

## Failures
- **#6 Palette economy** — four saturated hue families (amber `#FFD171`, cyan `#42B3CA`, purple `#A65EE3`, green `#97D880`) plus amber stars. Purposeful (category encoding) but over the ≤2-family bar; reads busy at a glance.
- **#10 Variant robustness** — glyph meaning is colour-dependent (the 4 category hues *are* the content); a tinted/mono system render would flatten them to one tint and destroy the legend. Effects are baked (speculars, drop-shadows, vignette) rather than layered in Icon Composer, so the icon can't participate in the macOS 26 light/dark/clear/tinted system — a mild non-native tell.

## Soft passes (flagged)
- **#2 Grid** — sphere anchor is near optical centre, but the composition is crowded to the right and the stars push into the top-right safe zone.
- **#3 Silhouette** — filled solid, it reads as a "circular refresh/renewal wheel with sparkles"; the primary form is nameable, but the 4 category segments become identical arcs, so the donut-breakdown meaning lives only in colour.
- **#4 16px squint** — the gross form (amber circular-arrow ring on charcoal) survives, but the hairline spokes, the small cyan chip, the sphere gloss, and both stars smear to sub-pixel mush at menu-bar/Spotlight size.
- **#7 Figure-ground** — the coloured ring has strong contrast (amber lum 212 on bg 54), but the dark sphere hub is dark-on-dark (lum 75 on well 38, ~1.5:1 grayscale) and separates only via its 3D highlight, not tone.

## Resolution & provenance caveats
- Delivered as an **894×894 webp web render, pre-masked** (squircle corners are transparent, alpha=0) — not the native 1024 full-bleed layer. The unmasked background layer and true safe-zone margins can't be verified; mild webp softening. Hex values reliable to ±3–4 levels `(measured)`.
- **Cross-platform reuse:** the cover shows the same emblem on macOS, iOS, and watchOS — this is an iOS-style rendered 3D icon reused on Mac, not a Mac-bespoke layered design.
- **Icon↔app coherence (strong):** the icon's dominant amber matches the cover's pale-yellow brand wash; the radar-chart hub and multi-hue segments are faithful miniatures of the actual Statistics screen. The icon genuinely communicates its subject.

## Rhymes with
- The **3D-rendered "puffy/claymorphic" dark-dashboard** family — glossy Blender/Cinema4D-style emblems on a charcoal ground, common to finance/analytics/subscription trackers. Style-family hint for synthesis: *dark-ground 3D-render dashboard emblem* (glossy multi-colour ring-chart on near-black, top-lit, baked speculars). First of its kind in this corpus — needs 2 more to cluster.
