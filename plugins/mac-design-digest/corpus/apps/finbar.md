# Finbar — profile

- **Source:** macapp.supply (`sources/finbar/`) · **Surfaces digested:** search-palette results panel (light, from cover composite) · **Last updated:** 2026-07-19
- **One-sentence identity:** Spotlight's floating-palette grammar turned into a *quantified* menu-bar tree — Alfred/Raycast's keyboard-search ergonomics with a stock-AppKit skin and a count badge on every branch.
- **Cluster:** unassigned (candidate: `native-utility-launcher` / menu-bar-utility)
- **Lineage:** native (high) — 13–14pt-class body, ~26–28pt rows, SF Pro throughout, Title-Case gray section headers; almost certainly SwiftUI `List`/`Table` in a floating `NSPanel`. Non-native evidence: none material.
- **Era (chrome):** custom / non–Liquid-Glass (low) — flat opaque `#F8F8F8` panel, hard full-width per-row hairlines, and a **full-bleed saturated selection bar** (the pre–Big-Sur `NSTableView` selection idiom) sit *against* the current inset-rounded / glass grammar. Modern cues (SF Pro, capsule count pills, rounded window) coexist with a legacy-flavored list. No glass visible → `(insufficient-evidence)` for material; glass absence on a floating panel is a deviation from the macOS 26+ default but not a defect.

> **Provenance caveat (read before trusting pt values):** the only UI evidence is the app window embedded in a marketing cover composite (1200×630), cut off at the right edge. The window's retina scale is indeterminate, so absolute pt sizes are `(estimated)` and could be off by a ~2× factor. What survives that uncertainty: **relative density** (body text ≈ half the search-field text; rows ≈ half the search-header height) reads unambiguously native, and the sampled accent `#0088FF` is scale-independent and pixel-confirmed.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel | `#F8F8F8` (measured)(inferred) | | results + search-header background; softened off-white, not pure `#FFF` |
| accent/selection | `#0088FF` (measured)(inferred) | | **exact match** to macOS-27 kit System Blue (Light) — system accent, correctly bound |
| selection/style | full-bleed saturated fill, white label + white glyph, translucent-white count pill (measured)(inferred) | | no left inset, no rounded corners; legacy full-bleed idiom, not inset-rounded |
| selection/text | `#FFFFFF` on `#0088FF` ≈ 3.5–3.7:1 (estimated)(inferred) | | Apple's own selection combo; below AA 4.5:1 for normal text (see Defects) |
| icon/tint | `#0088FF` monochrome line-art (measured)(inferred) | | all row glyphs one accent hue; 3 node types: menu (window-outline), command (menu-item), script (`{}`) |
| type/search | ~16–18pt SF Pro Regular (estimated)(inferred) | | search-field text/placeholder, visibly larger than list body |
| type/body | ~13–14pt SF Pro Regular (estimated)(inferred) | | row labels; snaps to 13pt macOS Body |
| type/section-header | ~11pt SF Pro, gray `~#8E8E93`, **Title Case** (estimated)(inferred) | | "Menu Items", "Scripts" — native sentence/title-case header, NOT tracked uppercase |
| type/count-badge | ~11pt, dark number in gray capsule pill `~#E3E3E3` (estimated)(inferred) | | sits immediately after label, not right-aligned |
| row/height | ~26–28pt (estimated)(inferred) | | comfortable native list row |
| search-header/height | ~48–52pt (estimated)(inferred) | | tall Spotlight-style borderless search field |
| separator | ~1px `~#E5E5E5` hairline, **full-width, under every row** (estimated)(inferred) | | table-with-gridlines look, not source-list |
| chrome/search-field | borderless — the whole header *is* the field; left slot holds the **target app's icon** (Finder), not a magnifier glyph (measured)(inferred) | | contextual affordance: the icon tells you whose menu bar is being searched |
| window/corner | rounded (radius not measurable from crop) (assumed)(inferred) | | floating panel; no traffic lights (correct for a panel) |

## Layout skeletons

**Search-palette results panel (single column, floating):**
- **Search header** (~48–52pt): [target-app icon] · [insertion caret] · ["Search" placeholder, gray] — borderless, full-bleed; hairline divider below.
- **Results list** (opaque `#F8F8F8`): repeating `[section header — gray Title Case] → [rows]`.
  - **Section headers:** "Menu Items", "Scripts" — small gray, left-inset ~16–20pt, extra whitespace above (the one place proximity is signaled).
  - **Row anatomy** (one shared icon-X and label-X axis top to bottom): `[disclosure chevron ›/⌄, optional] [accent-blue glyph, ~one indent per depth] [label] [gray capsule count pill, optional]`. Full-width 1px hairline under each row.
  - **Selection:** full-bleed `#0088FF` bar spanning edge to edge; chevron, glyph, label all invert to white; count pill → translucent white.
  - **Outline depth:** top-level menus (Apple/Finder/File/Edit/View/Go/Window/Help) expand to command children (About Finder, Settings…, Services… 24 → itself expandable). Depth by left indent of the icon.

## Signature moves

- **[GOLDEN-NUGGET] The quantified menu tree.** Every branch carries a live count pill — "File 38", "Edit 16", "Services… 24". The menu bar stops being an opaque set of dropdowns and becomes a *browsable, sized* outline: the badge is information scent (Pirolli & Card) telling you how much lives behind a node before you open it. This is the one device that separates Finbar from Spotlight/Alfred, which surface flat match lists with no depth signal.
- **App-icon-as-search-context.** The search field's leading slot holds the target app's icon (Finder here) instead of a magnifier glyph — a quiet, always-visible answer to "whose menus am I searching?" Doubles as scope indicator and brand-consistent (the app is *about* app menus).
- **Single-hue monochrome iconography.** Three node glyphs (menu / command / script `{}`) all rendered in the one system accent `#0088FF`, so the icon column reads as structure, not decoration — color carries type, never identity noise.

## Defects

- **Selection contrast (borderline, platform-standard).** White label on `#0088FF` ≈ 3.5–3.7:1 — under WCAG AA 4.5:1 for ~13–14pt normal text. It's Apple's own selection combo so it reads native, but by the rubric it's a genuine miss; a semibold weight on the selected row (native selected-row convention) would push effective legibility up.
- **Full-bleed selection vs. current native grammar (native-tell, defensible).** Current AppKit/Spotlight grammar is an *inset rounded* accent-tinted fill; Finbar uses the legacy full-bleed saturated bar. Systematic + purposeful (a strong single "Enter fires this" readout for a keyboard palette) + accessible → recorded as a **category-convention choice**, not a sloppy defect — but it's the app's clearest divergence from the macOS 26+ look. Runner-up reading: developer took the SwiftUI default.
- **Per-row hairline density (minor, Contrast-Dilution-adjacent).** A separator under *every* row (not just sections) adds horizontal grid noise and flattens the within-group vs between-group proximity ladder. A source-list treatment (separators only between sections, rows grouped by whitespace) would let the count badges and labels carry the structure instead.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| search-palette panel (light, from cover) | 12/14 | #9 selection text ~3.5:1 (white on systemBlue) borderline; #3 every-row separators flatten within/between-group spacing (section whitespace only weakly signals proximity) |

### Native-tells audit (10-pt) — search panel

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | AppKit-native lineage | Pass | 13–14pt body, ~28pt rows, SF Pro, Title-Case headers — native density |
| 2 | Glass only on chrome; content opaque | Pass (note) | panel flat opaque; no glass-in-content; glass simply absent (`insufficient-evidence` for era) |
| 3 | Selection: inset rounded, accent text/glyph | **Fail** | full-bleed saturated blue bar, white text — legacy idiom, not inset-rounded |
| 4 | Section headers sentence/title case, system font | Pass | "Menu Items"/"Scripts" gray Title-Case SF Pro |
| 5 | Density: 13pt body, 20–28pt controls, desktop rows | Pass | ~28pt rows, ~13–14pt body |
| 6 | Accent bound consistently | Pass | selection + all glyphs = `#0088FF`; exact system Blue |
| 7 | One prominent action per view; dialog grammar | Pass (n/a) | palette with single selection; no competing CTAs |
| 8 | Concentric corners; radii step down | Pass | capsule pills inside rounded window; no nesting violation |
| 9 | Toolbar: borderless symbols, grouped, single primary | N/A | no toolbar — floating search panel |
| 10 | Real chrome; genuine focus states | Pass | no traffic lights (correct for a panel); selection is a strong focus state |

**Native audit: 8/10** (1 fail #3, 1 N/A #9).
