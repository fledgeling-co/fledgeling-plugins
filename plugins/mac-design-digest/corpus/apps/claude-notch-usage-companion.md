# Claude Notch Usage Companion — profile

- **Source:** macapp.supply (icon.png + cover.gif, 155-frame screen recording) · **Surfaces digested:** notch bar (collapsed pill), notch HUD panel (expanded — "active sessions" page + "top projects" page) · **Last updated:** 2026-07-19
- **One-sentence identity:** Dynamic-Island-for-the-Mac-notch, in the NotchNook/Alcove genre, that reframes Claude token usage as spend — a bold dollar figure over a dimmed token count — with a terracotta pixel-invader as its face.
- **Cluster:** unassigned (proposed: `notch-companion` / dark-HUD menu-bar utility)
- **Lineage:** native (med confidence) — the notch-HUD genre is SwiftUI-native (NotchNook, Boring Notch, Alcove); SF Pro throughout, tonal-elevation cards, chromeless floating panel, no web tells (no tracked-uppercase headers, no kebab menus, no card-grid vocabulary). Menu bar and any settings window were not in the recording, so lineage rests on genre + type + material grammar, not on observed AppKit chrome.
- **Era (chrome):** big-sur-era dark HUD material, liquid-glass-adjacent. The panel reads as a solid near-black material with tonally-elevated cards; on a dark still the dark-mode-humility rule applies — cannot distinguish Regular glass from solid dark material, so recorded as opaque-dark `(insufficient-evidence)` for glass. The notch-HUD form factor itself is post-2021.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/notch-bar | `#000000` (measured)(confirmed) | | collapsed pill masks the physical notch; true black to blend with bezel |
| bg/hud-panel | `#0E0E0E` near-black (estimated)(confirmed) | | expanded HUD material; outer gutter around cards |
| bg/stat-card | `#161818`–`#181818` (estimated)(inferred) | | tonally elevated ~+8–10 L above panel — depth by tonal fill, not shadow or border |
| radius/hud-panel | ~22–26px (estimated)(inferred) | | large outer radius, notch-HUD convention; downscaled recording, wide range |
| radius/stat-card | ~12–14px (estimated)(inferred) | | steps down concentrically inside the panel |
| radius/toggle-pill | capsule (estimated)(confirmed) | | "⇄ all-time" / "⇄ active" segmented-style toggle in list header |
| accent/status | `#5FD08F` mint-green (estimated)(confirmed) | | circular progress ring + toggle glyph; ≈ system Green/Mint. Functional/"budget-remaining" color, NOT the user's system accent |
| brand/glyph | `#C8785A` clay/terracotta (measured)(confirmed) | rgb(200,120,90) sampled from icon.png | pixel-art space-invader creature = Claude brand color; identity color, kept separate from the green status color |
| type/stat-value | SF Pro Bold, Title-class (~22–26pt equiv) (estimated)(confirmed) | | `$238.41`, `$11060.05` — primary label tier, white |
| type/stat-label | SF Pro, ~Subheadline/Footnote (~11pt equiv), lowercase (estimated)(confirmed) | | `today`, `all-time`, `active sessions` — secondary gray, all-lowercase house style |
| type/stat-submetric | SF Pro, ~Footnote (~10–11pt equiv) (estimated)(confirmed) | | `107.5M`, `5009.3M` token counts — tertiary gray, demoted below the dollar figure |
| type/list-row | SF Pro Regular ~Body (13pt equiv) name; Semibold value (estimated)(confirmed) | | `Claude usage tracker fo…` (primary, truncates with ellipsis) · `$208.87` bold · `97.1M` tertiary |
| type/notch-percent | SF Pro Semibold, ~Body/Headline (estimated)(confirmed) | | `57%` white in the collapsed pill |
| text/primary | `#EDEDED`-class white (estimated)(confirmed) | | dollar values, project names |
| text/secondary | mid-gray ~50–55% (estimated)(confirmed) | | lowercase labels |
| text/tertiary | dim-gray ~25–30% (estimated)(confirmed) | | token sub-metrics, the `·` separator |
| space/card-gutter | ~10–14px (estimated)(inferred) | | between the two stat cards |
| space/label-to-value | ~4px (estimated)(inferred) | | tight; drives the "owned" grouping of each card |

## Layout skeletons

**Notch bar (collapsed, always visible).** Full-notch-width rounded-black pill. Leading: terracotta pixel-invader glyph (~16–18pt). Trailing cluster: `57%` percentage label + circular green progress ring (~14–16pt) showing budget remaining. Horizontal, single row, ~28–32pt tall. Zero-click glanceable status.

**Notch HUD panel (expanded on hover/click).** Near-black rounded panel dropping below the notch; the collapsed bar persists as its header row (glyph + %/ring stay pinned at top). Body is a vertical stack:
1. **Stat card row** — two equal-width cards side by side, each a 3-tier stack: lowercase label (top, secondary) → bold currency value (Title-class, primary white) → token sub-metric (tertiary gray). Left card = `today`, right card = `all-time`.
2. **List card** — full-width tonally-elevated card. Header row: lowercase title (`active sessions`) at left, capsule toggle pill (`⇄ all-time`) at right. Below: 2–3 rows, each = project name (left, primary, ellipsis-truncated) + right-aligned bold dollar value + `·` + dimmed token count.
3. **Carousel dots** — two centered page dots at the panel bottom; content pages between `active sessions` and `all-time · top projects` (toggle pill relabels `⇄ active`).

Alignment: the two stat cards share top/bottom axes; the list card's left/right edges align to the stat-row span. Right-aligned dollar values form a shared trailing axis down the list.

## Signature moves

- **Usage-as-spend hierarchy** [GOLDEN-NUGGET]: the product's entire idea — "your Claude tokens cost real money" — is carried purely by de-emphasis. The dollar figure is bold primary white; the token count (the raw fact) is demoted to a dimmed tertiary sub-metric. Same treatment in the stat cards and in every list row. Nothing shouts; the ranking does the arguing. This is Refactoring-UI de-emphasis doctrine used as the message, not just as polish.
- **Two-color semantic split**: identity color (clay/terracotta pixel creature = Claude brand) is deliberately never the functional color; the functional/status color (mint-green ring + toggle) means "budget remaining." Status green is always paired with the `57%` glyph, never floating alone — HIG-correct status-color discipline.
- **All-lowercase micro-labels** (`today`, `all-time`, `active sessions`, `top projects`) as a calm typographic house style — not the tracked-uppercase web tell, not sentence-case Title either; a chosen quiet register that keeps the bold numerals as the only loud element.
- **Notch as the entire surface**: no window, no traffic lights, no toolbar — a Dynamic-Island mental model (Jakob's Law: users already know it from iOS) ported to the Mac notch, with a 2-page carousel standing in for a settings screen's worth of detail.

## Defects

- **Contrast Dilution (mild, non-text)** → stat-card fill `#18` on panel `#0E` is ≈1.2–1.4:1, below the 3:1 non-text floor; internal card boundaries are nearly invisible and lean on the panel's edge against the wallpaper to read as grouped. What canon would do: step the tonal elevation harder, or add a hairline `#FFFFFF @8%` fill-tier separator. Minor — it's a glanceable HUD, not a data table.
- **Tertiary metadata contrast (borderline)** → the dimmed token counts / `·` separator on the darkest card likely fall under 4.5:1. Acceptable as decorative secondary data (recognition, not reading), but noted.
- Neither is a systematic failure; both are the honest cost of the near-monochrome dark aesthetic.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| notch HUD panel (expanded) | 12/14 | #10 UI contrast (card/pill edges ~1.3:1 vs 3:1 floor); #9 borderline on tertiary token metadata. #14 focus not observable in recording (unseen, not scored). |
| notch bar (collapsed pill) | n/a (too small a surface for full rubric) | glanceable status only; passes de-emphasis + accent-discipline checks |

**Native-tells audit (expanded HUD):** ~7–8 applicable passes. Native lineage (1) pass; glass/content separation (2) pass with dark-glass humility; density (5) pass; accent discipline (6) pass with the noted brand-vs-status split; concentric corners (8) pass; real chrome / correctly chromeless (10) pass. Sidebar (4), toolbar (9), selection grammar (3), input height not applicable to a notch widget.
