# Pattern: list-table

Cross-app synthesis of content lists (message/item lists) and column-header data tables — the two share row grammar and selection rules, so they are digested together. Native-lineage evidence only. Kit floor: `kit/macos-27.md` — Body **13pt**; menu-item / list selection radius **8**; primary label 85% black light / #FFFFFF dark; secondary 50%/55%; separator `#3C3C43`@29% light.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Vocal Notes | message list (light) | rows ~64–72pt two-line (title + trailing time / 1-line preview / folder chip); **solid accent-blue full-width inset-rounded selection r~8–10, ~8px inset, knockout white text** (Mail/Notes house style); sidebar shows muted-grey inactive selection simultaneously | (estimated)(inferred) |
| Letterboxx | message list (light) | rows ~38–40pt two-line (avatar ~28–32pt + title + sender + right date); **weight-not-colour unread** (semibold+near-black unread → regular+muted read); trailing blue unread dot / yellow ★; 1px hairline divider inset past avatar; neutral-grey selection when unfocused | (measured)(confirmed) |
| Canary Mail | message list (dark) | avatar circle + sender (bold) + preview; selected row = **saturated indigo filled card `#2558C9`, white text** (Spark/Airmail house style — inconsistent with sidebar's neutral inset, flagged) | (measured)(inferred) |
| Picmal | `NSTableView` (light) | **column-header table**: Name/From/To/Size/Saving/Status w/ 1px vertical header separators, **zebra striping** (`#F4F5F5` even rows), title-case secondary-grey headers; ~28pt single-line rows; **per-row pop-up button in the "To" cell** (the cell IS the control) | (estimated)(inferred) |
| Mac 4 Breakfast | key/value table (dark) | two-column health table: left secondary-grey labels / right primary-white values (Condition/Battery health/Cycle count/Capacity/Temperature); status values in system green; `~13pt` body | (estimated)(inferred) |
| Glance | markdown table (dark) | 2-column Action/Shortcut table, bold header w/ subtle elevated fill; **range-selection = 2px accent-blue outline + column handle** (spreadsheet grammar, not row-fill) + native context menu (Insert/Delete Column) | (estimated)(inferred) |
| Purge | item list (dark) | rows ~64–72pt two-line (circular checkbox + glyph + bold title + 2-line secondary); risk-filter capsule pills w/ live counts above; rows near-invisibly separated (surface≈bg, flagged) | (estimated)(confirmed) |
| Autoshelf | rules list (dark) | inset-grouped rounded cards, ~50–56pt 2-line rows (`status pill + glyph + title over metadata`), hairline separators inset past text; rule-as-sentence metadata | (estimated)(inferred) |
| Klack | picker list (dark) | ~44pt rows: leading identity-colour "+" chip + label + trailing ▶ audition button; full-width hairline between rows | (estimated)(inferred) |
| Zipic | result list (light) | full-width white rounded **row-cards** on grey canvas (deviation from flat table), r~14–18; thumbnail + filename + status badges + trailing actions | (estimated)(inferred) |

## Converged rules

- **Content-list selection is a full-width inset-rounded fill at radius ~8** — apps: Vocal Notes, Letterboxx, Canary, Purge, plus sidebar-selection rule — **(canon)**. Fill hue diverges (see below) but the inset-rounded shape at r8 is invariant.
- **Two-level focus grammar: solid-accent fill on the focused pane, neutral-grey fill on the unfocused pane** — apps: Vocal Notes, Letterboxx — **(recurring)**; getting this wrong (both panes accent, or two different selection languages) is the corpus's most common list defect (Canary, Codeshot, Resurf, Sketch).
- **Unread / state carried by weight, not colour** — apps: Letterboxx (semibold unread → regular read), plus a blue dot — **(recurring)**; textbook de-emphasis.
- **Multi-line rows anatomy: `[leading avatar/glyph/checkbox] [primary title] [secondary metadata line] … [trailing count/date/action]`, secondary in grey** — apps: Vocal Notes, Letterboxx, Purge, Autoshelf, Canary — **(canon)**.
- **Row height splits by density tier: compact single-line ~24–32pt (tables) vs comfortable two-line ~40–72pt (message/item lists)** — apps: Picmal (~28 table), Mac 4 Breakfast (~28 kv), Letterboxx (~38–40), Klack (~44), Purge (~64–72), Vocal Notes (~64–72) — **(canon)**.
- **Tables: title-case secondary-grey column headers, 1px vertical separators, subtle zebra striping, live per-row controls where editable** — apps: Picmal (full table + inline pop-ups), Mac 4 Breakfast (kv), Glance (markdown table) — **(recurring)** for native; tracked-uppercase column headers are the flagged web/enterprise tell (Letterboxx diagnostics tables, Foldervitrine group subheaders).
- **Dividers should reach ≥3:1 but frequently do not** — apps: Purge (rows≈bg), Vocal Notes (~1.05:1 hairline), Room Service (~1.1:1), Autoshelf, Grape — Contrast Dilution is the single most frequent defect corpus-wide (72 apps); dark grouped lists lean on fill-step alone.

## Divergences

- **Selection fill hue.** System-accent solid (Vocal Notes, Letterboxx focused) vs **saturated brand/indigo card** (Canary `#2558C9`, Sketch layer) vs **neutral-grey** (Grape, Room Service, Codeshot content band). The saturated-card and neutral-grey readings both deviate from the general flat accent-tinted rule; saturated-card tracks the prosumer-email cluster (Spark/Airmail dialect), neutral-grey tracks the calm/monochrome cluster.
- **Flat list vs row-cards.** Native flat `NSTableView`/`List` rows (Picmal, Vocal Notes, Letterboxx) vs **individually floating rounded row-cards** on a canvas (Zipic, Autoshelf inset-grouped) — the card treatment is a System-Settings-adjacent consumer-warm house style, the biggest departure from native content-list grammar.
- **Table selection grammar.** Row-fill selection (message lists) vs **spreadsheet range-outline** (Glance: 2px accent outline + column handle) — context-appropriate divergence (a table of editable cells behaves like a spreadsheet, not a source list).
- **Multi-select control shape.** Native square checkboxes (Picmal) vs circular checkboxes (Purge) / trailing circular checkmark toggles (Cachesweep) — circles are the recurring iOS/SwiftUI tell.

## Generation guidance

- **Pick the density tier by content:** compact single-line ~28pt rows for a scannable data table; comfortable two-line ~40–72pt rows for a message/item list.
- **Row anatomy:** `[leading avatar (rounded-square ~28–32pt) / SF Symbol / square checkbox] [primary title 13pt SF Pro] [secondary metadata, middot-separated, grey] … [trailing date / count badge / one action]`. Carry state (unread, active) by **weight** (semibold vs regular), reinforced with a small blue dot — not by colour alone.
- **Selection:** full-width inset-rounded fill at **radius 8**. Default to the user's system accent (solid-accent + white text for a prominent Mail/Reminders list; low-alpha accent-tinted fill + accent text for the general case). Implement **two-level focus**: focused pane gets the solid-accent fill, the unfocused pane mutes to neutral grey. Use one selection language across the whole window.
- **Tables:** title-case secondary-grey column headers on a shared vertical axis, 1px vertical separators, optional subtle zebra (`~4%` grey even rows). If a cell is editable, make the cell *be* the control (Picmal's per-row pop-up ledger) rather than opening a dialog per item. Selection = row-fill for record lists, range-outline for spreadsheet cells.
- **Dividers must clear 3:1:** draw separators from the kit's Fills/Separator tiers (`#3C3C43`@29% light; Fills-tier white@8–10% dark). Do not let row surface equal the window background (Purge's rows-invisible miss) — step the row surface ~+4–6% lightness or use a real hairline.
- **Multi-select:** use **square** checkboxes, not circles (circles read iOS).
