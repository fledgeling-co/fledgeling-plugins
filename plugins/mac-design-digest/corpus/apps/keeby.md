# Keeby — profile

- **Source:** macapp.supply (cover composite only — no gallery shots supplied) · **Surfaces digested:** menu-bar-extra menu + keyboard-profile panel (single composite, dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** Klack's premise (mechanical keyboard sounds for Mac) dressed as a disciplined menu-bar utility — a vividly orange brand hue held entirely to the icon while the running UI stays neutral dark glass with system-blue selection.
- **Cluster:** unassigned (candidate: *menu-bar-utility, warm-brand-restrained*)
- **Lineage:** native (med-high) — SwiftUI `MenuBarExtra`; SF Symbols menu items, sentence-case section headers, accent-blue menu selection at radius ~8, real desktop menu bar. Non-native evidence: none material.
- **Era (chrome):** Liquid Glass native (macOS 26/27) — dark translucent menu/popover material with soft floating shadow and ~16–20px panel radius; **dark-glass humility applies** — from one still I cannot separate Regular glass from solid graphite material, so material is `(insufficient-evidence)`.

> **Measurement confidence: LOW.** The only asset is a 1200×630 marketing cover; the actual app UI lives inside a MacBook device-frame at the bottom and is **partially cropped** (the menu's last row "Position" is cut off). All app-surface pixel values are `(estimated)` with wide ranges. Backdrop/brand values (top of the composite) are cleaner and marked `(measured)`. Source hash cover.png `cf1be53d`, icon.webp `8daa4b33`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/orange (wordmark) | `#FF8C16` (measured)(confirmed) | | lowercase bold "keeby" wordmark + keycap glyph |
| brand/orange (icon keycap) | `#F77507` (measured)(confirmed) | | deeper orange in the hero app icon |
| accent/selection | `#0A84FF` system blue (measured)(inferred) | | menu selection binds to **system** accent, NOT brand orange — accent discipline |
| bg/site-backdrop | `#F5F5F5` warm-neutral (measured)(confirmed) | | flat, no gradient; marketing surface only |
| ink/headline | `#171717` (measured)(confirmed) | | softened near-black, not pure #000 (avoids Contrast Dilution) |
| ink/cta-pill | `#0F0F0F` (measured)(confirmed) | | black pill CTA — action is black, orange is jewelry |
| ink/tagline | `#C2C2C2` on #F5F5F5 (measured)(inferred) | | secondary microcopy (marketing) |
| menu/material | dark translucent glass over desktop, reads ~graphite (estimated)(inferred) | | near-opaque at this scale; radius ~16–20px; soft drop shadow |
| menu/selection-radius | ~8px inset rounded fill, full-width (estimated)(inferred) | | matches kit "menu item selection radius 8" |
| menu/section-header | ~10–11pt, secondary gray, sentence case (estimated)(inferred) | | "Control" / "Configure" / "Keychron" — NOT tracked uppercase |
| type/menu-item | ~13pt SF Pro (Body), white/secondary (estimated)(inferred) | | one-line items with leading SF Symbol |
| menu/row-height | ~24pt menu rows; ~40–44pt profile-panel rows (estimated)(inferred) | | profile panel runs a more generous custom-popover cadence |
| status/soon-pill | small gray capsule, ~9–10pt gray label (estimated)(inferred) | | custom "Soon" badge on unreleased switch profiles |

## Layout skeletons

**Menu-bar-extra menu (right panel, primary command surface).** Orange keycap glyph sits in the macOS menu bar (trailing extras); clicking opens a dark rounded panel (~160–170px wide). Vertical stack: secondary-gray section header **Control** → item `Enable Keeby` (checkmark.circle glyph); gap; section header **Configure** → `Sound` (sliders glyph), `Switches` (keyboard glyph, **selected**: full-width `#0A84FF` rounded fill, white label + white trailing chevron ›), `Enable Visualizer` (checkmark.circle), `Position ›` (cut off). Every item is icon-leading, single-line; submenu items carry a trailing chevron. Grouping by titled sections with a between-group gap larger than within-group spacing.

**Keyboard-profile panel (left panel).** Separate floating dark panel; header **Keychron** (secondary gray). Rows: leading rounded-square keycap glyph + primary label + trailing status. `K2 Max · Gateron Red` is active (trailing checkmark.circle); `Cherry MX Blue` and `Holy Panda X` are dimmed with a trailing gray **"Soon"** capsule (upcoming/locked). Generous row height (~40–44pt), left-aligned label axis shared with the glyph column.

**Marketing cover (brand evidence, not app UI).** Flat `#F5F5F5` ground; top bar = orange lowercase "keeby" wordmark (left) + black "Download" pill (right). Center stack: hero app icon → two-line ultra-bold near-black headline "Your keyboard, / but better." (tight tracking, ~48px grotesque) → gray tagline → black capsule "⌘ Download for Mac" CTA → "$4.99 · One-time purchase" microcopy. Below: MacBook device-frame containing the app composite above.

## Signature moves
- **[GOLDEN-NUGGET] Brand hue quarantined to the icon.** The identity is loud orange (`#FF8C16`), but selection, focus, and the one prominent menu item bind to the **system** accent blue (`#0A84FF`) — the running UI is neutral dark glass. This is the native-correct "accent is the user's, not the app's" rule executed with unusual discipline for a consumer utility, and it repeats in the marketing: the CTA is **black**, not orange, so orange stays jewelry (wordmark + icon) rather than becoming a button color.
- **"Soon" status pills as a roadmap-in-the-menu.** Unreleased switch profiles render as dimmed rows with a quiet gray "Soon" capsule rather than being hidden — a disabled-don't-remove treatment that doubles as honest anticipation (Zeigarnik/Goal-Gradient), and the status label is always paired with text, never color alone.
- **Menu-bar-extra as the whole app.** No primary window, no traffic lights — the entire product is a `MenuBarExtra` menu + a profile popover. The architecture *is* the positioning: a background sound-layer you configure and forget.

## Defects
- **Contrast unverifiable on translucent material** → secondary-gray section headers and the "Soon" pills sit on dark glass over a light desktop; at composite scale I cannot assert ≥4.5:1 / ≥3:1. Not logged as a defect (quiet section headers are native-correct), but flagged `(insufficient-evidence)` — a real @2x menu capture is needed to confirm.
- **Colored menu-bar glyph** → the keeby menu-bar icon is a filled orange keycap rather than a monochrome template symbol. Increasingly common and not a hard failure, but a mild deviation from the classic tint-to-match-menu-bar template convention. Canon would use a template SF Symbol that inherits menu-bar tint.
- *No true defects confirmable from this asset.* The single cropped composite is insufficient to judge spacing rhythm, real interaction, or light mode.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar-extra menu (dark) | 12/14 | #9 text contrast on translucent glass unverifiable (insufficient-evidence); #6/#12/#13 N/A (no paragraphs/inputs/form-labels) |

**Native-tells audit (menu surface):** 9/10 applicable pass. ✅ native lineage · ✅ glass on floating chrome only · ✅ menu selection grammar (full-width accent fill r8 — correct for *menus*) · ✅ sentence-case section headers · ✅ density (13pt items, ~24pt rows) · ✅ accent bound to system blue, brand hue separate · ✅ single prominent item · ✅ plausibly concentric corners (panel ~18 / selection ~8) · ⊘ #9 window-toolbar N/A (menu-bar utility) — minor note: colored menu-bar glyph · ✅ real macOS menu bar, no faked frame.

## Notes for synthesis
- Functional twin of **Klack** (Tom Waddington) — same category (mechanical keyboard sounds), same menu-bar-utility architecture. Differentiate any Keeby-derived mock deliberately; do not clone Klack's trade dress either.
- Single low-confidence composite → **do not promote any Keeby observation toward canon**; it can at most corroborate an existing pattern. Best future asset: a real @2x screenshot of the open menu (and a light-mode capture) to confirm menu row height, panel radius, and glass material.
