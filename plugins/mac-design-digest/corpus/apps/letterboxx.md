# Letterboxx — profile

- **Source:** macapp.supply · **Surfaces digested:** app window + stats dashboard (shot-1), reading pane + glass toolbar (shot-2, shot-5), Clean View popover (shot-3), highlight-colour menu + reading (shot-4), Message Diagnostics (shot-6); marketing composite cover · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple Mail's three-pane bones and NetNewsWire's reader calm, retargeted at email newsletters — a faithfully native reader whose one flourish is turning each mailbox into an analytics-and-diagnostics dashboard.
- **Cluster:** native-faithful reader (proposed — sole member so far)
- **Lineage:** native (high) — 13pt-class body, compact rows, real traffic lights, source-list sidebar with sentence-case section headers, borderless monochrome toolbar symbols in a single glass container group, secondary-grey list selection when the list isn't first responder. macOS-correct AppKit/SwiftUI. Non-native evidence: none in the app's own chrome (the rendered newsletter HTML in the detail pane carries third-party web typography — that is *content*, not the app's system).
- **Era (chrome):** Liquid Glass native (macOS 26/27 "Tahoe", med-high). Evidence: floating refractive toolbar symbol-group hovering at the detail-pane top-right (container-morphing, one continuous edge), capsule search field, generous ~12–14pt window radius, popover body radius reading ~16–20pt. Large opaque content (lists, dashboard cards) stays off-glass — glass discipline honoured.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#FFFFFF` | (measured)(confirmed) | window + reading-pane ground, light mode |
| bg/sidebar | ~`#F4F4F6` translucent (vibrancy) | (estimated)(confirmed) | source list, slightly recessed vs content |
| bg/stat-tile | ~`#F1F1F4` flat fill | (estimated)(confirmed) | dashboard cards; tonal, no heavy shadow |
| accent/primary | system blue ~`#0088FF` | (estimated)(confirmed) | matches kit light Blue; sidebar selection, links, unread dot |
| selection/sidebar | solid accent-blue inset-rounded fill, **white** label, ~6–8pt radius, ~4px inset | (measured)(confirmed) | the "prominent" source-list style (Mail/Reminders-like), not the subtle tinted default |
| selection/list | neutral-grey inset-rounded fill when list unfocused; accent-blue + white when focused | (measured)(confirmed) | correct secondary/active selection duality |
| type/list-title | ~13pt SF Pro — semibold + near-black when unread, regular + slightly muted when read | (estimated)(confirmed) | weight, not colour, carries unread |
| type/list-subLabel | ~11pt SF Pro, secondary grey | (estimated)(confirmed) | sender line + right-aligned date |
| type/stat-number | ~26–28pt SF Pro Bold, near-black | (estimated)(inferred) | value outranks its label (LargeTitle/Title1 class) |
| type/stat-label | ~13pt SF Pro, secondary grey, sentence case | (estimated)(confirmed) | paired with a system-hue glyph |
| type/section-header | ~11pt SF Pro Semibold, secondary grey, **sentence case** ("Filters", "Letterboxxes") | (estimated)(confirmed) | #1 sidebar authenticity tell — passes |
| type/table-header | ~10pt, secondary grey, **tracked UPPERCASE** ("APPEARANCE / COLOR / STATUS") | (measured)(confirmed) | diagnostics tables only — a web/enterprise tell, see Defects |
| row/list-height | ~38–40pt, two-line | (measured)(confirmed) | avatar + title + sender/date; 1px hairline divider inset past the avatar |
| row/sidebar-height | ~28–32pt (Medium tier) | (estimated)(confirmed) | glyph + label |
| radius/card | ~13pt | (measured)(inferred) | stat tiles |
| radius/popover | ~16–20pt | (estimated)(inferred) | Clean View panel; near kit popover 20 |
| radius/search | capsule / ~8pt | (estimated)(confirmed) | sidebar-top search field, ~28pt tall |
| radius/window | ~12–14pt | (estimated)(confirmed) | measure-from-screenshot; kit ships none |
| chrome/toolbar | floating glass symbol-group, detail-pane top-right: ~8 borderless monochrome SF Symbols (edit, chevron, copy, share-nodes, clipboard) + A / ⓘ / A text-size trio | (measured)(confirmed) | one continuous glass edge (container morph) |
| chrome/sidebar-width | ~160–200pt | (estimated)(confirmed) | reads narrower than the kit's 256 example |
| palette/highlight | Yellow · Mint · Sky · Rose · Lavender (system 12-hue subset) | (measured)(confirmed) | highlight menu + reading-pane marks; identity hues, separate from accent |
| palette/tile-glyphs | per-tile system hues (orange sun, blue clock, purple/pink calendars, green chart…) | (measured)(confirmed) | identity colour, correctly decoupled from the single accent |

## Layout skeletons

**Three-pane master–detail–detail** (all surfaces share this shell; window ~1440×900 logical, @2x):
- **Source list (~160–200pt):** capsule Search pinned top → collapsible **"Filters"** section (Inbox, Unread, Today, Yesterday, This Week, Last Week, All, Trash, Favorites, Highlighted, Reminders — each a monochrome SF Symbol + label) → collapsible **"Letterboxxes"** section (alphabetical user folders, each prefixed by an emoji/custom glyph: 🍎 Apple, 🏛 Berkshire Hathaway…). Solid-accent prominent selection.
- **Message list (~360–400pt):** a slim header showing the current letterbox's glyph + name; two-line rows = rounded-square sender avatar/logo (~28–32pt) + title (unread-bold) + sender subLabel + right-aligned date; trailing blue unread dot and/or yellow ★. Neutral-grey selection when not first responder.
- **Detail pane (fills remainder) — polymorphic**, the app's structural signature:
  1. *Rendered newsletter* (shot-2/5): third-party HTML rendered verbatim (its own centred bold headings, serif body) beneath the floating glass toolbar; a "Listen to this article" affordance sits above body.
  2. *Stats dashboard* (shot-1): responsive **card grid** of stat tiles (Today/Yesterday/This Week/Last Week/This Month/Last Month/Quarter/Year/Lifetime/First Newsletter/Averages), then list-cards Top Letterboxxes, Top Senders, Highlights — each row a leading glyph + name + right-aligned count. The app icon floats as a decorative tile mid-grid.
  3. *Message Diagnostics* (shot-6): a data surface — a **segmented composition bar** (Visible text / Markup / Styles / Images / Trackers & ads, each a system-hue dot + inline % + KB + thin progress bar) plus Background and Reader Surface tables (colour-swatch + hex + status columns).
  4. *Clean View popover* (shot-3): a detached rounded glass panel over the reader — header (icon + title + "Medium" pull-down) → "This newsletter · 9 removed / 16% smaller · 13 KB cleaned" → two mini stat-cards (Sender 80, All Time 3,758) → "View full breakdown in Message Diagnostics…" link row.

## Signature moves
- **The polymorphic third pane.** The detail column is not just a reader: it swaps between rendered-newsletter, a full analytics dashboard, and a developer-grade diagnostics view. One structural slot doing four jobs is what gives the app character beyond "another Mail clone."
- **Data-viz as the boldness budget.** Everywhere else the app is quiet and system-default; the one place it spends colour and composition is *data* — the diagnostics composition bar and the stat-tile grid, hue-coded to the 12-colour system palette. Classic 80/20: disciplined chrome, one expressive surface.
- **"Clean View."** A named tracker/ad/clutter stripper surfaced as a glass popover with its own removed-count telemetry (per-newsletter, per-sender, all-time) — a product signature rendered in native furniture.
- **Highlights named in system hues.** Yellow/Mint/Sky/Rose/Lavender — "familiar colors" pulled straight from the system identity palette, offered in a native pull-down with colour dots; marks persist inline in the reader. Ties a custom feature to platform colour vocabulary instead of inventing swatches.
- **Weight-not-colour unread.** Unread rows bold their title (+ a blue dot); read rows relax to regular. Hierarchy by de-emphasis, textbook.

## Defects
- **Tracked-UPPERCASE table headers** (Contrast/consistency, minor) → the Message Diagnostics tables label columns "APPEARANCE / COLOR / STATUS / DETECTED AT" in letter-spaced caps. HIG *lists-and-tables* wants sentence-case secondary column headers; tracked uppercase is a web/enterprise-ism and the one non-native seam in an otherwise faithful app. Canon fix: "Appearance / Color / Status" in secondary grey, no tracking. Sporadic (this surface only) → defect, not signature.
- **No hard defects elsewhere.** Glass stays on chrome, content opaque; selection grammar correct; accent single-bound with identity hues separate; no Focal Collision (the reader has no competing saturated CTAs). Marketing covers (device-free window on blue gradient + heavy grotesque headline) are brand evidence, not app UI.

## Brand evidence (cover / marketing, not app chrome)
- Backdrop: cyan→blue diagonal gradient; headline in a very heavy geometric-grotesque display ("A better home for your newsletters."), subhead in an SF-class sans, secondary grey. Brand blue matches the in-app accent — the one place brand and system colour deliberately rhyme.
- App icon (not digested under Workflow A): a stacked-airmail-envelopes-in-a-blue-tray render, glossy Big-Sur-material lineage — noted for a later icon pass, excluded from UI canon.

## Rubric history
| Surface | 14-pt | 10-pt native | Failures |
|---|---|---|---|
| shot-1 window + dashboard | 13/14 | 10/10 | #10 hairline divider/border contrast borderline <3:1 (platform-normal) |
| shot-2 reading + glass toolbar | 13/14 | 10/10 | #6 long measure = rendered newsletter HTML, not app type (n/a to chrome) |
| shot-3 Clean View popover | 13/14 | 9/10 | #10 borderline; popover morph n/a from still |
| shot-4 highlight menu + reading | 13/14 | 10/10 | — |
| shot-5 reading (Grow Omaha) | 13/14 | 10/10 | #6 as shot-2 |
| shot-6 Message Diagnostics | 12/14 | 8/10 | native #4 tracked-uppercase column headers; #9/#10 secondary-label contrast borderline in dense data |
