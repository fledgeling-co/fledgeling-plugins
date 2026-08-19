# Fantastical — profile

- **Source:** macapp.supply (cover composite only; no standalone shots supplied — `shots: []` in meta) · **Surfaces digested:** main window — Week view (light content pane + dark agenda sidebar), Mac render inside a 3-device marketing composite · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple Calendar's week-grid literacy fused with a dense always-on agenda pane, warmed by one committed brand-red typographic accent — a power-user calendar that scans like a to-do app. Reference peers: Apple Calendar (the convention it inherits), BusyCal (density + agenda-pane sibling), Notion Calendar / Cron (modern-native rival), Things (the calm-pro indie polish it rhymes with).
- **Cluster:** unassigned — proposed `native-pro-agenda` (dense native productivity tools with one committed brand accent)
- **Lineage:** native (high) — AppKit-native macOS. Tells: real coloured traffic lights, real menu bar with status items (Control Center / Wi-Fi / battery / clock visible top-right of the desktop), macOS capsule segmented control (Day/Week/Month/Quarter/Year), pop-over "Today ‹ ›" capsule control, compact 13pt-class typography, source-pane + content split, red now-line. No iOS/Catalyst tells (no inset-grouped cards, no `UISwitch` pills, no full-bleed selection, no per-row chevrons). The iPad + iPhone in the same composite ARE iPadOS/iOS — contrast evidence only, not digested.
- **Era (chrome):** modern native, **liquid-glass (med)** — capsule segmented control + capsule Today pill are macOS 26 control shapes; but the two-tone dark-sidebar/light-content split is house styling and glass *lensing* is not confirmable from a small composite render `(insufficient-evidence)`. No glass-in-content violation either way — the week grid is fully opaque.

## Provenance caveat

Every pixel value below is `(estimated)` with wide ranges. The **only** evidence is a **marketing composite**: a 1200×628 cover in which the Mac window occupies ~430px of width (roughly the left third), floated behind an overlapping iPad. Window render scale is unknown → absolute pt cannot be measured; sizes are ranges anchored to the macos-27 kit and Apple-Calendar convention, which the app tracks. Colours are compression-affected — treat hexes as families, not samples. Evidence strength: `(inferred)` = this one surface only; nothing here is `(confirmed)` since a single surface was seen.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/content | white ~#FFFFFF, faint warm-grey wash on the day headers (estimated)(inferred) | | week-grid canvas; kit light window bg is #FFFFFF — matches |
| bg/sidebar | dark graphite ~#1C1C1E–#202022 (estimated)(inferred) | | the agenda/DayTicker pane is dark while content is light — a **two-tone window**; may be a theme/appearance setting, see Signature + Defects |
| accent/system | system blue ~#0A84FF (kit light Blue #0088FF) (estimated)(inferred) | | today date rendered as a filled blue circle (mini-cal + day header); binds the "native" selection role |
| accent/brand | Fantastical red ~#E0392B–#FF3B30 (estimated)(inferred) | | injected on the **year ("2025")**, the today-column weekday label ("MON"), section headers ("TODAY"), and the red now-line — identity/time-indicator role, NOT selection |
| text/primary-dark | #FFFFFF on sidebar (estimated)(inferred) | | month title, event titles, day numbers in the dark pane |
| text/primary-light | ~85% black on content (estimated)(inferred) | | day-header numerals, event-block titles; matches kit's 85%-black primary label |
| text/secondary | ~50–55% grey both panes (estimated)(inferred) | | event time ranges + locations/subtitles ("Greenhome Courts", "Online"); clean de-emphasis vs. titles |
| type/body | reads 13pt SF Pro Regular (estimated)(inferred) | | event titles; macOS 13pt body, not iOS 17pt — a lineage tell |
| type/time-meta | reads ~10–11pt SF Pro (estimated)(inferred) | | time ranges, hour gutter labels (8 AM…5 PM), day-of-week caps |
| type/month-title | reads ~17pt SF Pro Semibold (estimated)(inferred) | | "September 2025" sidebar header (Title2 class) |
| type/section-header | reads ~10–11pt, tracked UPPERCASE, brand-red ("TODAY 2025-09-15" / "TOMORROW …") (estimated)(inferred) | | agenda date-group headers — uppercase; native-tell #4 nuance, see Defects |
| selection/segmented | subtle light capsule fill on a lighter track ("Week" active) (estimated)(inferred) | | macOS 26 capsule segmented control; not full-bleed, not saturated — native-correct |
| today/treatment | filled blue date circle + red weekday label + pale-blue column wash + red now-line (estimated)(inferred) | | four redundant "today" cues stacked — see Signature |
| event/block-fill | desaturated pastels — lavender, powder-blue, tan (estimated)(inferred) | | calendar-identity-coloured from the ~12-hue system palette; dark title text sits on the tint |
| event/dot | small filled circle in the calendar's identity colour (estimated)(inferred) | | agenda rows; multi-colour event dots also under mini-cal dates |
| tag/pill | filled tan/orange capsule ("Book delivery", "Food markets") (estimated)(inferred) | | calendar-set / all-day tag pills |
| action/join | small blue capsule "Join" on video events (estimated)(inferred) | | inline contextual CTA — parsing DNA surfaced in the row |
| task/checkbox | open circle instead of a dot ("Pick up dry cleaning") (estimated)(inferred) | | tasks and events share one agenda list; reminders get a tickable circle |
| control/add | "+" glyph, top-right of the sidebar (estimated)(inferred) | | the one prominent create action |
| chrome/nav | "Today" in a capsule pop-over flanked by ‹ › chevrons, content-top-left (estimated)(inferred) | | date navigation cluster |
| grid/hairline | faint light-grey hour/day rules, likely <3:1 on white (estimated)(inferred) | | calendar convention; see Defects |

## Layout skeletons

**Main window — Week view (two-tone split).** Leading **dark agenda sidebar** (~135px of the ~430px composite width; true width indeterminate, reads ~256pt-class): top row = "+" create button trailing; "September YYYY" title (year in brand red) with ‹ › month chevrons; a compact **mini-month calendar** (SUN–SAT column heads, day numerals white, today in a filled blue circle, tiny multi-colour event dots beneath dates); then a scrolling **agenda list** grouped by relative-date headers ("TODAY 2025-09-15", "TOMORROW 2025-09-16" — uppercase, brand-red), each row = identity-colour dot (or task circle) + time range (secondary) + title (primary) + optional location (tertiary), with filled tag pills and inline "Join" CTAs where relevant. Trailing **light content pane**: a toolbar row (Today capsule + ‹ › on the left; Day/Week/Month/Quarter/Year capsule segmented control centred, "Week" active) over a **week grid** — seven day columns (weekday cap + date numeral; today's cap red, today's numeral in a blue circle, today's column washed pale blue), an "all day" band of muted event pills, then an hour-ruled body (gutter labels left) carrying pastel event blocks and a **red now-line with a leading dot** at the current time. Content is fully opaque; the split is the composition's spine.

## Signature moves

- **[GOLDEN-NUGGET] Brand-red as typographic jewelry.** The year in "September **2025**", the today weekday label, the "TODAY" section header, and the now-line all carry Fantastical's red while everything structural stays neutral. Selection/focus still binds to the *user's* system blue (today circle, segmented fill) — so the red is spent only on identity + the time-indicator, never on the native selection role. Restrained accent budget (roughly one red moment per region) executed with discipline; it is the app's entire warmth in one hue.
- **[GOLDEN-NUGGET] Two-tone window — dark agenda pane against a light calendar canvas.** Unusual for AppKit, where the source list normally shares or *lightens* the window tone; here the DayTicker/agenda column is dark graphite while the grid is white. It hard-separates "what's next" (dark, scannable, list-shaped) from "when" (light, spatial, grid-shaped) by luminance alone. (May be an appearance/theme setting rather than the sole default — flagged in Defects/notes.)
- **[GOLDEN-NUGGET] The agenda pane replaces the calendar source-list.** Instead of the conventional list-of-calendars sidebar, the left column is a live schedule (mini-month + relative-date-grouped events + tasks). The app's information architecture puts *your day* where the OS idiom would put *your data sources* — subject-mined from the product's actual job.
- **Today, over-signaled on purpose.** Four redundant cues (blue date circle + red weekday cap + pale-blue column wash + red now-line) converge on the current moment. Redundancy that would be noise elsewhere is legibility here — in a dense grid you must never lose "now".
- **Inline contextual affordances.** A blue "Join" pill on video events and a tickable circle on tasks put the next action *in the row* — the natural-language-parsing lineage surfacing as one-tap follow-through.

## Defects

- **Uppercase tracked agenda group headers (native-tell #4, soft).** "TODAY / TOMORROW" are tracked uppercase — the letter of the "sidebar headers = sentence/title case, system font" rule is broken. Heavily mitigated: these are agenda *date-group* headers (relative-date labels are conventionally uppercase, cf. calendar/agenda idioms), not list-of-things section headers, and they carry a date. Records as a soft flag, not a hard defect.
- **Low-contrast non-text UI (#10).** Hour/day hairline rules and the desaturated pastel event fills likely fall <3:1 on white; separation and legibility ride on the dark *title text* over the tint rather than on the fill or border. Standard calendar practice, but near the WCAG 3:1 non-text floor. `(unverified — composite compression)`.
- **Secondary text on the dark sidebar (watch, not confirmed).** ~50–55% white time-ranges/locations on graphite read near the 4.5:1 text floor; verify on-device. `(unverified)`.
- **Mini-calendar day targets (#11).** Individual day cells in the mini-month read ~14–16px — below the 24px WCAG floor for a pointer target. Common in date pickers, noted not condemned.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window — Week view (light content + dark sidebar) | 12/14 | #10 hairline grid + pastel event fills likely <3:1 on white; #11 mini-calendar day cells ~14–16px < 24px floor; (#9 secondary text on dark sidebar borderline — noted unverified, not counted as the second fail; #14 no focus state recoverable from a still — n/a) |

**Native-tells audit (10-pt):** 9/10. The one soft item is #4 (uppercase agenda date-group headers — mitigated by relative-date convention). #6 (accent binding) is a *signature*, not a fail: system blue holds the selection/today role while brand red is confined to identity + the now-line. All others pass — AppKit-native lineage, opaque content / no glass-on-glass, capsule segmented selection (not full-bleed), 13pt-class dense body, one prominent create action, capsule/rounded corners, borderless grouped toolbar, and genuine coloured traffic lights with a real menu bar behind the window.
