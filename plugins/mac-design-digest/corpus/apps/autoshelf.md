# AutoShelf — profile

- **Source:** macapp.supply (meta.json + cover.png[AVIF] + icon.png[AVIF]) · **Surfaces digested:** 1 — main window / Rules list, dark (embedded in the marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** CleanMyMac's brand-forward utility warmth applied to a Things-calm grouped rule list — a set-and-forget file organizer whose entire personality is one saturated orange-red hue against disciplined charcoal.
- **Cluster:** unassigned (proposed hint: *warm-accent utility (dark)*) — sole candidate member; needs ≥2 more apps to open a cluster.
- **Lineage:** native (low confidence) — **Catalyst not excluded.** The chrome and nav read SwiftUI-native (genuine coloured traffic lights, `sidebar.left` toggle SF Symbol, SwiftUI-style `List` selection, SF Symbol nav icons); the *body* reads iOS (inset-grouped rounded card tables, tracked-uppercase section headers, pill toggles, tall 2-line rows). This is the classic "iOS-first, shipped to Mac" ambiguity. Its iOS-derived list grammar is recorded as **tells + corrections and must never feed macOS canon**, whichever way the lineage finally lands.
- **Era (chrome):** big-sur-class modern (flat rounded dark idiom, 2020+). **No confirmable Liquid Glass** — chrome is flat opaque, which is legitimate for a utility (absence of glass is not a defect); dark-mode humility means glass-vs-solid is unresolvable from this still regardless.

## What was actually supplied (honesty note)

One real app-UI surface — unlike a marketing-only cover. The 1200×630 OG composite puts the brand lockup (illustrated sky/hills, the icon's orange file dropping onto a dark "shelf/smile", "AutoShelf" wordmark + "File & Folder Cleaner for Mac" subhead) on the **left**, and the **actual app window** on the **right ~50%**. The window is the design evidence; the sky/hills/wordmark are brand evidence and are not conflated below.

Two important caveats bounding every number here:
1. The window is **perspective-warped a few degrees** and **bleeds off the right and bottom** — so it is cropped and non-orthogonal. All pixel values are `(estimated)` with wide error bars; only the 1200×630 cover aspect is `(measured)`.
2. Files arrived as **AVIF renamed `.png`** (ftyp box) — converted via `sips -s format png` before reading.

## Tokens

All values `(estimated)(inferred)` unless noted — one warped, cropped exposure.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window-content | #141416 charcoal (approx) | (estimated)(inferred) | content pane, dark mode |
| bg/group-card | ~#1A1A1C — one step lighter than content | (estimated)(inferred) | inset rounded card behind each group |
| bg/sidebar | #0C0C0E near-black (approx) | (estimated)(inferred) | darker than content — standard dark two-tone |
| accent/brand | orange-red ~#E5401C / #E8431E | (estimated)(inferred) | THE app accent; matches the app-icon file color |
| selection/sidebar | solid saturated brand orange-red rounded-rect fill, radius ~10–12pt, white label + white glyph | (estimated)(inferred) | **signature** — not the standard flat translucent/vibrant inset selection |
| type/sidebar-item | ~15px SF Pro (Title3/Body-emphasized class), white primary | (estimated)(inferred) | sidebar labels run larger than content titles |
| type/row-title | ~13–14px SF Pro Semibold/Bold, primary white | (estimated)(inferred) | e.g. "Trash .dmg files" |
| type/row-subtitle | ~11–12px SF Pro Regular, tertiary gray | (estimated)(inferred) | middle-dot metadata triple |
| type/section-header | ~10–11px tracked UPPERCASE, tertiary gray | (estimated)(inferred) | non-native tell (see Defects) |
| control/status-toggle | custom pill ~30×18; green track+knob = on, red/maroon = off; knob stays LEFT both states | (estimated)(inferred) | diverges from NSSwitch (green/accent, knob-RIGHT when on) |
| icon/rule-glyph | orange-red outline document-with-gear, ~24pt | (estimated)(inferred) | custom brand-colored "rule" iconography |
| icon/sidebar-symbols | monochrome white SF Symbols (list.bullet / square.grid.2x2 / clock / gearshape / info.circle) | (estimated)(inferred) | native-affiliation signal |
| chrome/sidebar | ~256pt-class fixed sidebar; sidebar-toggle glyph at top strip | (assumed)(inferred) | width matches kit 256pt; warp-uncertain |
| chrome/traffic-lights | coloured red/yellow/green = focused window | (estimated)(inferred) | genuine macOS chrome |
| chrome/toolbar | minimal — controls + sidebar-toggle + left-aligned "AutoShelf" title; no visible trailing group | (estimated)(inferred) | title reads as a content-top navigation title, not centered toolbar title |
| list/grouping | inset-grouped rounded cards, hairline left-inset row separators | (estimated)(inferred) | iOS/SwiftUI-multiplatform idiom, not flat AppKit list |
| cover/aspect | 1200×630 (OG social card, 1.91:1) | (measured)(inferred) | marketing composite; window occupies right ~50% |

## Layout skeletons

**Main window — Rules list (dark).** Two-column split: a fixed near-black **sidebar** (left) + a charcoal **content pane** (right).

- *Sidebar top strip:* window traffic lights (leading) + `sidebar.left` toggle symbol (trailing). Below: a flat vertical nav list of 5 items — Rules, Templates, Activity, Settings, About — each `[SF Symbol · label]`, ~40pt rows, left-aligned, no section headers. The selected item (Rules) is a solid brand-orange-red rounded-rect fill spanning the row minus small insets, white glyph + white label.
- *Content pane:* left-aligned "AutoShelf" title at top, then a vertically scrolling **grouped list**. Each group = a tracked-uppercase header (ORGANIZERS / SCREENSHOTS / NO GROUP) over an inset rounded card enclosing its rows. Row anatomy, left→right on shared column axes: `[status-toggle pill] [orange file-with-gear icon] [bold title over tertiary middle-dot metadata subtitle]`. Rows ~50–56pt (2-line), hairline separators inset to start under the text. Disabled rows (e.g. "Trash .mpkg files") dim title+icon in place and show a red toggle. Content bleeds off the right/bottom of the composite.

## Signature moves

- **[GOLDEN-NUGGET] Single-hue brand commitment.** One orange-red (~#E5401C) does all the identity work: the sidebar selection is a *solid saturated* fill of it (System-Settings-strength, not the translucent vibrant selection), the rule icons are drawn in it, and it stands in for the system accent throughout. Against an otherwise strictly-neutral charcoal field, the whole app's personality is that one warm color — a committed direction, and a deliberate rotation *off* the reflexive electric-blue/acid accent that dark dev-tool UIs default to.
- **[GOLDEN-NUGGET] Status-toggle as traffic-light.** The per-row enable/disable control is a custom green(on)/red(off) pill that doubles as an at-a-glance status light — the single place saturated color is spent inside the content field, and it's spent on *meaning* (is this rule live?). Semantic color paired with position, exactly where a set-and-forget tool needs a glance-check.
- **Rule-as-sentence subtitle.** Each row's metadata is written as plain English — condition · action · destination ("Extension is .dmg · Move to Trash · Downloads") — so an automation configuration is *scannable prose*, not a decoded form. Recognition over recall, applied to config.

## Defects

- **Tracked-uppercase section headers** (native tell #4) → evidence: "ORGANIZERS"/"SCREENSHOTS"/"NO GROUP" in wide-tracked caps, tertiary gray. Canon/HIG would use **sentence-case system-font secondary** headers; ALL-CAPS also carries a mild scanning cost (uniform word shapes). *Correction:* sentence case, system font, secondary label color.
- **Non-system accent binding** (native tell #6) → the brand orange-red overrides the user's `controlAccentColor` for selection and icons. Internally consistent (a real house style), so this sits on the defect/signature boundary — recorded as a **tell + correction**, not learned as canon. *Native correction:* bind selection/focus to the system accent; keep the brand hue for the app's own iconography.
- **Color-meaning collision (minor)** → RED marks a merely *disabled* rule toggle, but red conventionally means destructive/error, so an inert paused rule can misread as a problem. *Correction:* gray-off (or the brand hue) for disabled; reserve red for genuine danger.
- **Contrast Dilution (soft, #9/#10)** → tertiary subtitle ~4:1 and hairline separators/group-card edges <3:1 on the dark ground `(estimated)`; the disabled row is intentionally sub-threshold. Borderline, not egregious.
- **iOS-grouped-table density on Mac** (native tell #5) → tall 2-line inset-card rows import an iPhone-Settings rhythm rather than compact desktop list density. Part of the lineage-ambiguity picture, not a standalone flaw.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window / Rules list (dark) | 12/14 | #9 secondary-text contrast ~4:1 borderline (estimated); #10 hairline separator + group-edge contrast <3:1 (estimated). Structure, hierarchy, de-emphasis, action-singularity, modular scale all pass. |
| — native-tells audit | 6/10 | #3 selection is solid saturated brand fill (not standard flat/vibrant); #4 tracked-uppercase headers; #5 iOS row density; #6 non-system accent. Pass: lineage-chrome, no glass-in-content, concentric-ish corners, minimal borderless toolbar, genuine traffic lights, one-prominent-thing. |

## Knowledge gap this app leaves open

One surface, one mode. To place AutoShelf properly the corpus needs: **light mode** (to confirm the charcoal/orange values and whether the selection fill survives on white), a **settings or template-editor surface** (to see this app's form grammar — the strongest lineage tell), and ideally a **clean orthogonal screenshot** rather than a warped marketing render, which would promote the estimated tokens toward measured. Lineage stays native/low-confidence (Catalyst not excluded) until a form or an AX-inspectable surface settles it.
