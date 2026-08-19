# Usage — profile

- **Source:** macapp.supply (cover composite only; no gallery shots) · **Surfaces digested:** macOS menu-bar-extra panel + menu-bar readout strip (1 surface, light) · **Last updated:** 2026-07-19
- **One-sentence identity:** iStat Menus' domain rendered in an iOS-widget dialect — a colorful, glanceable telemetry dashboard that lives in the menu bar instead of an austere native readout.
- **Cluster:** unassigned — cluster hint `consumer-telemetry-dashboard` (colorful-widget menu-bar utility)
- **Lineage:** native (med) — a genuine Mac menu-bar-extra utility, almost certainly multiplatform SwiftUI; but the design *dialect* is iOS/WidgetKit-derived. The iOS and macOS surfaces are visually near-identical, so its density, segmented-as-nav, chip pills, and non-system accent are recorded as **iOS tells, excluded from macOS canon**. Catalyst not fully ruled out from a still.
- **Era (chrome):** big-sur (Sequoia-continuum vibrancy — opaque rounded panel, soft radii). NOT liquid-glass: no glass lensing observable; menu-bar strip material is `(insufficient-evidence)`.

## Provenance & scale caveat

Cover is a **marketing composite**: Sequoia sunburst wallpaper (brand), an iPhone frame running the iOS app (**contrast evidence only** — excluded from macOS canon), and the real macOS evidence — a menu-bar-extra dropdown panel plus a dense menu-bar readout strip. The rounded dark menu-bar "capsule" is a composite framing device, not a system element. All pixel values `(estimated)` at an **assumed ~1x scale** (panel measured 378px wide, which reads as ~1x for this much content); no @2x chrome exists to calibrate against.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| panel/bg | #FFFFFF / #F9F9F9 near-white (measured)(inferred) | | dropdown ground; cards only ~2-3% off panel tone |
| accent/brand-primary | #5953FD indigo-violet (measured)(inferred) | | disk gauge + primary identity hue; **not** the system accent |
| accent/processor | #2A9CF9 blue (measured)(inferred) | | processor-load bars, thermometer bulb |
| accent/network-up | #ED58AD hot pink (measured)(inferred) | | upload histogram; download partner ~#7A5FE0 purple (estimated) |
| type/stat-hero | ~20–24pt Bold (estimated)(confirmed) | | the big value per card; repeats across all 6 cards |
| type/card-title | ~13–14pt secondary gray (estimated)(confirmed) | | Disk / Bluetooth Devices — measurably lighter than the value |
| type/sub-metric | ~12–13pt secondary (estimated)(confirmed) | | 406,32 / 994,66 GB; Last 7 days |
| type/pill | ~11–12pt (estimated)(inferred) | | chip-tag labels |
| control/segmented | ~30pt tall, white selected pill (r~8pt) on gray track (estimated)(inferred) | | device switcher; iOS UISegmentedControl scale (kit Rg is 24) |
| pill/tag | gray capsule fill, capsule radius (estimated)(inferred) | | "Macintosh HD", "Normal" |
| radius/panel | ~12–16pt (estimated)(inferred) | | below kit popover 20pt if 1x; corner resolves over ~7px |
| radius/card | ~10–12pt (estimated)(inferred) | | concentric under panel |
| space/gutter | ~15–16pt (estimated)(inferred) | | column gutter & card v-gap; reads on 8pt grid (16) |
| space/card-padding | ~14–16pt (estimated)(inferred) | | content inset within each card |
| chrome/menubar-readout | dense inline stats, 3-letter vertical labels DSK/CPU/NET (measured)(inferred) | | iStat-style; the one austere-native surface |

## Layout skeletons

**menu-bar-extra panel (light):** floating rounded panel ~378×406pt on the wallpaper (no traffic lights — correct for a status-item dropdown). Vertical stack: (1) top segmented **device switcher** [MacBook Pro | iPhone 14 Pro], full-width, left-aligned to the card grid; (2) a **2-column × 3-row card grid**, ~16pt gutter, left column & right column edges share vertical axes. Each card: SF-Symbol glyph + Title-Case label (secondary) on row 1 → bold hero value → optional sub-metrics / chip tag / bespoke gauge. Gauges sit trailing (Disk donut) or full-width below (Processor Load histogram, Network Activity mirrored histogram). (3) trailing-bottom "…" more affordance. Grouping is carried by content + padding, **not** by borders (card edges are near-invisible).

**menu-bar readout strip (light, composite-framed):** a single dense inline row — circular gauge glyph · DSK 40.9% · CPU 12.9% · NET 24/10 kB/s (each with a 3-letter stacked label) · Wi-Fi · display · clock. This is the app's dense, native, iStat-register surface.

## Signature moves

- **[GOLDEN-NUGGET] Fixed per-metric identity palette instead of the system accent.** Indigo `#5953FD` = storage, blue `#2A9CF9` = processor, hot-pink `#ED58AD`↔purple = network — systematic across every card and shared verbatim with the iOS app. Each stat becomes pre-attentively identifiable by hue before its label is read. Legitimate as *identity* colors (separate from accent), but the app never binds to `controlAccentColor`, so it ignores the user's chosen accent — a deliberate brand trade, recorded as a tell too.
- **[GOLDEN-NUGGET] Bespoke WidgetKit-style gauge vocabulary** with a consistent stroke language: segmented dashed donut (disk %), symmetric up/down histogram (network activity), diagonal-hatched placeholder tiles (bluetooth empties). Not stock AppKit controls — a coherent, ownable data-viz set.
- **Split personality by surface.** A dense iStat-style menu-bar readout (austere, native, 3-letter labels) opens into a roomy, colorful, consumer WidgetKit dropdown. Glance layer = native-dense; detail layer = playful-consumer.

## Defects

- **Contrast Dilution (mild)** → card containers separated by only ~2-3% tonal fill (edges under 3:1); Bluetooth empty-slot hatch tiles and tertiary metadata (Last 7 days, pill labels) read ~gray-300 on white → canon: container edges ≥3:1 or a stronger tonal step; lift metadata to ~gray-500.

**Native tells (corrections, not canon):** segmented control used as *primary* navigation (Mac convention: pop-up/tab-view or a small pane) · ~30pt controls + ~20–24pt display numbers = iOS density, not 13pt/24pt AppKit · chip pills for tags · accent forced to app indigo rather than the system accent.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| menu-bar-extra panel (light) | 12/14 | #10 UI/border contrast (near-invisible card edges, hatch empties <3:1); #9 text contrast (soft — tertiary metadata borderline) |
| — native-tells audit | 4/10 | fails #1 (iOS dialect), #5 (density), #6 (non-system accent), #3-leaning (iOS segmented, not inset-rounded selection); passes #2 (no glass-in-content), #8 (concentric corners); #4/#7/#9/#10 N/A for a menu-bar-extra (no sidebar/toolbar/dialog/traffic-lights) |
