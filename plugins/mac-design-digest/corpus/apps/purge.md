# Purge — profile

- **Source:** macapp.supply (`sources/purge/`: cover + 2 marketing shots; app UI is embedded inside marketing composites) · **Surfaces digested:** main window (sidebar + content list), result/completion card, menu-bar-extra panel · **Last updated:** 2026-07-19
- **One-sentence identity:** A native-SwiftUI Mac disk-cleaner that dresses a destructive bulk-delete in reassurance — CleanMyMac's job done with Pearcleaner's restraint, its whole character carried by a Safe-to-Clean/Check-First risk taxonomy and "everything goes to Trash" reversibility.
- **Cluster:** unassigned (suggest `dark-native-utility`)
- **Lineage:** native (SwiftUI, Mac-only) — **med confidence**. Strong Mac tells: real source-list sidebar with inset-rounded accent selection, monochrome SF Symbols, sentence-case labels, 13pt-class body, a genuine `MenuBarExtra`. Consumer/iOS-leaning styling choices (circular multi-select checkboxes, card-ified list rows, full-width white capsule button) but **no Catalyst or Electron tells** (no inset-grouped UIKit tables, no `UISwitch` pills, no tracked-uppercase headers, no kebab menus, no web body sizes). Non-native styling never feeds macOS canon.
- **Era (chrome):** liquid-glass-adjacent (Tahoe/macOS 26–27 visual language: capsule chips + buttons, ~20px panel radii, translucent dark surfaces, rounded menu-bar-icon highlight) — **low confidence on the material itself.** Surfaces are *custom-drawn SwiftUI* (bespoke menu panel, result card, filter pills), not standard system chrome; no window frame / traffic lights are visible in any shot to date the frame, and dark-mode humility means true Liquid Glass cannot be distinguished from solid dark material in these stills.

> Provenance caution: all three surfaces are embedded inside 1280×720 marketing composites at an **unknown down-scale**, so pixel→pt conversion is not recoverable. Every token below is `(estimated)` with wide ranges; sizes are proportional reads, not clean measurements. Retina scale: indeterminate.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window (content) | `#1F2024` cool charcoal (estimated)(confirmed) | | sampled; content area, dark mode |
| bg/sidebar | `#1C1D22` slightly darker/cooler than content (estimated)(inferred) | | source-list surface |
| surface/row-card | `~#1F2024`, white-fill ≈+2–4% over bg (estimated)(inferred) | | content rows barely differ from bg → separated by hairline stroke, see Defects |
| surface/panel (menu, result card) | `#1A1A1A` near-black (estimated)(confirmed) | | menu-bar panel + result card read a touch warmer/darker than the window |
| border/hairline | white @ ~8–12% (estimated)(confirmed) | | card/panel outlines; very low contrast against surface |
| text/primary | `#FFFFFF` (estimated)(confirmed) | | matches kit dark primary |
| text/secondary | white @ ~50–55% (estimated)(confirmed) | | row descriptions, "moved to Trash", "to clean" — matches kit Secondary |
| text/tertiary | white @ ~25% (estimated)(inferred) | | result-card footnote "Empty your Trash…"; borderline legibility |
| accent/brand | azure-blue gradient `~#4DA3FF→#1E86F0` (estimated)(confirmed) | | app-icon "P" wordmark / brand blue; wordmark lockup on all covers |
| accent/semantic-safe | system green, tinted fill reads `~#346F4A` over dark (base ~`#30D158`) (estimated)(confirmed) | | "Safe to Clean" chip + sidebar "Safe to Clean" label; color always paired with label/glyph |
| accent/warning-tier | neutral gray (no color) for "Check First 12" (estimated)(inferred) | | risk tier signalled by count + clock glyph, not a warning hue |
| radius/panel | ~18–20px (estimated)(confirmed) | | result card + menu panel; matches kit popover-body 20 |
| radius/row-card | ~10–12px (estimated)(inferred) | | content list rows |
| radius/chip, /button | capsule (estimated)(confirmed) | | filter pills, "Done", "Clean Safe Items", equivalents chips |
| chip/height | ~24–28px (estimated)(inferred) | | filter pills + equivalents chips |
| button/primary style | **white-filled capsule** (`#F2F2F3`), full-width in panel (estimated)(confirmed) | | "Done"; primary is white, not accent-tinted |
| sidebar/width | ~200–230px in-composite (estimated)(inferred) | | cropped; cannot confirm against kit 256pt |
| sidebar/row-height | ~32–36px (estimated)(inferred) | | Medium/Large-tier rows |
| sidebar/selection | inset rounded fill, subtle, radius ~6–8 (estimated)(inferred) | | native selection grammar on "App Caches" |
| row/content-height | ~64–72px, two-line (estimated)(confirmed) | | title + 2-line description |
| type/title (content header) | ~16–18px bold ≈ Title2 (estimated)(confirmed) | | "App Caches" |
| type/body (row title) | ~13px semibold (estimated)(confirmed) | | item names |
| type/caption | ~10–11px ≈ Caption/Subheadline (estimated)(confirmed) | | "30 items · 2.9 GB recoverable", descriptions |
| glyph/success | thin-stroke circled checkmark, monochrome white (estimated)(inferred) | | result card |
| glyph/speed | ⚡ system yellow, paired with "done in 0.3 seconds" (estimated)(inferred) | | color+label, never alone |

## Layout skeletons

**Main window (cover.png) — master–detail, dark mode.**
- Left **source list** (~200–230px, cropped): brand lockup ("P" icon + "Purge") at top → single flat nav group: App Caches (selected, inset-rounded fill) · Dev Tools · Large Files · Settings · About, each with a leading monochrome SF Symbol, sentence case. Sidebar **footer**: capacity bar ("276.49 GB used … 217.89…"), a "✓ Safe to Clean" status line, and a primary "✦ Clean Safe Items" capsule button — the one prominent action, pinned bottom-of-sidebar.
- **Content** ("App Caches"): header row = title (bold) + subtitle "30 items · 2.9 GB recoverable" (secondary). Below it a **risk-filter row** of three capsule pills with live counts — "⊞ All 42", "✓ Safe to Clean 30" (green, active), "◷ Check First 12" — then a "Select All" circular check. Then a vertical **list of item rows**: circular checkbox · category glyph (folder/app) · bold title · 2-line secondary description. Trailing top-right: "↻ Sc…" (Scan) secondary capsule (cropped). Rows are near-invisibly separated (surface ≈ bg).

**Result / completion card (shot-1.png) — floating panel/sheet, centered stack, dark mode.**
- Circled checkmark → "**2.98 GB**" (display) → "moved to Trash" (secondary bold) → equivalence row "That's roughly [🖼 710 photos] or [♪ 355 songs]" (two capsule chips) → "⚡ done in **0.3 seconds**" → tertiary footnote "🗑 Empty your Trash to reclaim this space." → full-width white "Done" capsule. No traffic lights (correct for a sheet/panel).

**Menu-bar-extra panel (shot-2.png) — custom `MenuBarExtra` window-style popover, dark mode.**
- Rounded menu-bar icon with selected-state highlight anchors a ~18–20px-radius translucent panel: header row "**2.9 GB** to clean · 🕐 33m ago" (value bold, rest secondary) → hairline divider → tall (~50px) rows: "Clean Safe Files", "Scan now", "Open Purge", "Quit". Reads as a popover, not an `NSMenu` (rows ≈2× native 24pt menu-item height).

## Signature moves
- **[GOLDEN-NUGGET] Risk-tiered item taxonomy as the primary control.** The content filter isn't "All / recent / large" — it's **Safe to Clean (30) / Check First (12) / All (42)** with live counts and a green semantic tint on the safe tier. It re-frames a scary irreversible bulk-delete as a triaged, forgiving decision, and it recurs system-wide (sidebar "Safe to Clean" status, "Clean Safe Items" button, the whole safety pitch). This *is* the app's identity in one component (Forgiveness + loss-aversion, addressed structurally).
- **[GOLDEN-NUGGET] Reversibility written into the copy.** Never "deleted" — "**moved to Trash**", plus the footnote "Empty your Trash to reclaim this space." Destruction is always one step from undo; the marketing headline "Everything goes to Trash. Always." makes it the thesis.
- **Tangible-equivalents chips.** Freed space is re-expressed as "710 photos or 355 songs" — abstract GB rendered experiential (closes the description–experience gap; makes the payoff felt, not read).

## Defects
- **Contrast Dilution (surface separation)** → content rows and the window background sample the *same* tone (~`#1F2024`); rows are distinguished only by a white ~8–12% hairline, which likely falls **below the 3:1 non-text floor**. Canon: step the row surface ~+4–6% lightness or strengthen the divider so cards read as cards without squinting.
- **Non-native control grammar — circular checkboxes** for multi-select (rows + "Select All"). macOS multi-select uses **square** checkboxes; circles read as iOS/custom and blur the checkbox-vs-radio distinction. Minor, systematic (a style choice), so recorded as a native-tell rather than a hard defect.
- **Tertiary footnote legibility (marginal)** → result-card "Empty your Trash…" at ~25% white is at the edge of readable for a line carrying the app's core reassurance; consider Secondary tier.

## Rubric history
| Surface | Rubric | Native audit | Failures |
|---|---|---|---|
| main window (cover) | 12/14 | 8/10 | #10 hairline card/border likely <3:1 (rows ≈ bg tone); #9 secondary row text marginal; native: circular checkboxes (control grammar); traffic-light chrome not visible (n/a) |
| result card (shot-1) | 13/14 | 8/10 | #9 tertiary footnote ~25% white marginal; native: white-filled (not accent) primary + full-width capsule reads consumer/iOS (style choice, not a fail) |
| menu-bar panel (shot-2) | 13/14 | 7/10 | #10 panel border subtle; native #5: ~50px rows ≈2× native menu-item height — deliberate window-style popover, not `NSMenu` |
