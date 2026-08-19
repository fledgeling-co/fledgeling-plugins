# Bartender 6 — profile

- **Source:** macapp.supply (cover composite only; no standalone shots supplied) · **Surfaces digested:** settings main window — Menu Bar Style pane (focused), General pane (inactive, behind) · **Last updated:** 2026-07-19
- **One-sentence identity:** System Settings' own sidebar-and-grouped-form idiom worn as camouflage by a config-dense menu-bar utility, with one non-stock flourish — an elevated hero card titling every pane. Reference peers: macOS System Settings (the thing it imitates), Ice / Hidden Bar / One Switch (menu-bar-manager siblings), iStat Menus preferences.
- **Cluster:** unassigned — proposed `native-settings-idiom` (System-Settings-clone utilities)
- **Lineage:** native (med-high) — SwiftUI on macOS. Tells: SF Symbols throughout, real coloured/greyed traffic lights, native capsule switches, pop-up buttons with the double up/down chevron, System-Settings-clone sidebar, grouped inset form sections. No web/Electron tells (no kebab menus, no uppercase-tracked headers, no pointer-hand). Non-native evidence: none.
- **Era (chrome):** modern native, dark mode (Big Sur → Tahoe lineage). Rounded window corners, unified titlebar, a capsule "Apply to all" toolbar accessory that *may* be Liquid Glass — but this is a **dark still, so Regular glass vs. solid material is indeterminate** `(insufficient-evidence)`. No glass-in-content violations regardless.

## Provenance caveat

All pixel values below are `(estimated)` — the only evidence is a **marketing composite** (device-free windows floated on a Tahoe-style wallpaper, no headline text). Window render scale is unknown, so absolute pt cannot be measured; sizes are given as ranges anchored to the macOS-27 kit and to System Settings convention, which the app tracks closely. Evidence strength: `(inferred)` = one pane; `(confirmed)` = re-evidenced across both panes.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | near-black navy ~#1A1C1E (estimated)(confirmed) | | dark mode; kit dark window bg is #1E1E1E — matches within range |
| bg/card-elevated | one tonal step up ~#26282C (estimated)(confirmed) | | hero header card + every grouped form container; depth by tonal-elevation, not shadow |
| accent/primary | system blue ~#0A84FF (kit dark Blue #0091FF) (estimated)(confirmed) | | binds selection + all switches + the one filled primary ("Complete") — single accent, no per-control colour drift |
| text/primary | #FFFFFF (estimated)(confirmed) | | labels, sidebar rows, titles |
| text/secondary | ~50–55% white grey (estimated)(confirmed) | | descriptions, "2 stops" count, inactive-window toolbar title |
| type/body-label | reads 13pt SF Pro, Regular/Medium (estimated)(confirmed) | | row labels + sidebar labels; density matches System Settings' 13pt body |
| type/section-header | reads 13pt SF Pro Semibold, Title Case (estimated)(confirmed) | | "Menu Bar Style", "Gradient Settings", "Bar Shape", "Border" — NOT tracked uppercase (native tell #2 pass) |
| type/hero-title | reads ~22–26pt SF Pro Bold, centred (estimated)(confirmed) | | the per-pane title inside the hero card (LargeTitle/Title1 class) |
| selection/sidebar | solid accent-blue fill, radius ~8, full-width minus ~4px inset, white glyph-tile + white text (estimated)(confirmed) | | System Settings **house-style** solid fill, not the general inset-translucent rule; mutes to no-fill when window inactive (bg pane) |
| sidebar/layout | flat list (no section headers), ~200–210px of window width, rows ~28–32pt (Medium tier), SF Symbol on ~18–20pt rounded monochrome tile per row (estimated)(confirmed) | | near-exact System Settings sidebar clone |
| radius/card | ~10–12pt on hero card + grouped containers (estimated)(confirmed) | | |
| radius/tile | ~5–6pt on sidebar symbol tiles + hero icon tile (estimated) | | concentric: child tile radius < parent card radius |
| control/switch | standard macOS capsule switch, blue when on (estimated)(confirmed) | | Show shadow / Seperate Pills / Apply to all = on; Draw Border = off (dimmed, not hidden — native tell) |
| control/popup | pop-up button, double up/down chevron, value-shows-selection ("Gradient", "Capsule") (estimated)(confirmed) | | correct pop-up (pick-a-value) grammar, not pull-down |
| control/gradient-editor | capsule gradient bar (blue→magenta), draggable ringed circular stops, "Add Stop" ⊕ + "N stops" count (estimated)(inferred) | | purpose-built custom control |
| chrome/toolbar-accessory | capsule pill "Apply to all" + inline switch, trailing (estimated)(inferred) | | glass vs. tinted-fill indeterminate in dark still |
| divider/row | hairline, <3:1 against dark fill (estimated)(confirmed) | | hierarchy carried by fill-step, not border contrast — see Defects |

## Layout skeletons

**Settings main window — split view (both panes).** Unified titlebar (traffic lights leading; sidebar-toggle SF Symbol + pane title at content-left; trailing toolbar accessory pill). Two columns: (1) fixed source-list sidebar — flat 9-item list, one symbol-tile+label per row, solid-blue selection; (2) scrolling detail pane on one shared left alignment axis: an **elevated hero header card** (centred icon tile → bold pane title → one-line secondary description) sits at top, then a vertical stack of grouped form sections. Each section = a Title-Case semibold header above a rounded container of left-label / right-control rows separated by inset hairlines. Between-section gaps are visibly larger than within-group row gaps (Gestalt proximity holds). Right-edge controls (pop-ups, switches, counts) share a right alignment axis. A live styled-menu-bar preview floats outside the window in the composite (product output, not chrome).

## Signature moves

- **[GOLDEN-NUGGET] Hero header card per settings pane.** Every pane opens with an elevated rounded card holding a centred icon tile + a LargeTitle-class pane title + a single explanatory line ("Configure the Bartender basics…" / "Customize the appearance of your menu bar…"). Stock System Settings jumps straight into groups; this device titles each "chapter" and orients the user inside a very configuration-heavy app. Systematic (both panes) + purposeful (wayfinding + onboarding) + accessible → signature, not defect.
- **[GOLDEN-NUGGET] System Settings as native camouflage.** The sidebar (solid-accent selection, symbol-on-rounded-tile rows, flat list) and the grouped inset form are a near-exact impersonation of macOS System Settings' own chrome. A menu-bar utility that deeply rewrites the OS's menu bar borrows the OS's settings skin so its power feels sanctioned and familiar — Jakob's Law weaponised.
- **Purpose-built gradient editor.** The capsule gradient bar with draggable ringed stops + "Add Stop"/"N stops" is a genuine custom control, subject-mined from the app's job (styling the menu bar needs a real colour tool), and crafted to native standards (capsule ends, accent-neutral chrome).

## Defects

- **Spelling — "Seperate Pills"** (should be "Separate"). A typo shipping in the live UI; a polish defect that undercuts the otherwise-System-Settings-grade fidelity. Fix: correct the string.
- **Low-contrast non-text UI (#10).** Row dividers and card borders sit <3:1 against the dark fill; all structural hierarchy rides on tonal fill-steps. Common convention in dark grouped forms, but it flirts with the WCAG 3:1 non-text floor. Canon would keep the fill-step but lift dividers/borders to ≥3:1.
- **Secondary description contrast (watch, not confirmed fail).** The mid-grey pane descriptions on dark read near the 4.5:1 text floor; verify on-device.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| settings — Menu Bar Style pane (focused, dark) | 12/14 | #10 dividers/borders <3:1; #14 no focus state visible (n/a from still) |
| settings — General pane (inactive, dark) | 12/14 | #10 as above; #14 n/a; re-evidences hero-card pattern + correct inactive-window accent muting |

**Native-tells audit (10-pt):** 9/10 both panes. The one soft item is selection grammar (#3): solid-accent fill rather than the general flat-inset-translucent rule — but this is System Settings' documented **house style**, so it reads as deliberate platform mimicry, not a defect. All other tells pass: native lineage, opaque content / no glass-on-glass, Title-Case system-font section headers, 13pt-class density, single-accent binding, one prominent action per view, concentric corners, borderless grouped toolbar, genuine traffic lights with correct focused/inactive muting.
