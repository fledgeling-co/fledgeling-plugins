# Supaste — profile

- **Source:** macapp.supply (cover + icon only; no in-app screenshots supplied) · **Surfaces digested:** 1 (main HUD panel, dark, from marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** Paste's horizontal clipboard shelf restyled as a true-black content gallery — a Raycast-grade dark HUD where every clip is a content-aware preview card.
- **Cluster:** unassigned (cluster hint: *dark-HUD-shelf* / floating-utility-gallery)
- **Lineage:** native (med confidence) — macOS density (13pt-class body, ~23pt controls) and system-font labels read AppKit/SwiftUI, but the surface is a heavily custom-drawn HUD skin so framework tells are largely painted over; no window chrome to confirm. Not web/Electron (no 16px web body, tracked-uppercase headers, kebab menus, or pointer-hand tells).
- **Era (chrome):** custom, Liquid-Glass-influenced — frosted translucent outer container over an opaque black content shelf; capsule-everything bezels match the macOS 26/27 capsule signature, but the solid-black chrome is a brand deviation from translucent Liquid Glass.

> **Measurement caveat (read first):** the only evidence is a marketing composite (2400×1260) with the app window shown at an *indeterminate* scale. All absolute-pt values below are `(estimated)` through an assumed **~1.85× composite scale**, derived from the macOS menu-bar clock ("09:41") reading ~24–26px for a nominally ~13–14pt element. **Ratios and proportions are trustworthy; absolute points are not.** No traffic-light cluster exists to calibrate (borderless HUD), so the scale is a single-reference inference.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel-content | `#000000` true black | (measured)(inferred) | inner content shelf; pure black sampled mid-panel — a deliberate OLED-gallery backdrop, not a translucent window bg |
| bg/frame-glass | frosted light, ~`rgb(187,217,228)` wallpaper-tinted | (measured)(inferred) | outer rounded container; wallpaper blurs through at left ("Supaste" end) and right ends → glass frame wrapping opaque content |
| selection/pill-active | `#FFFFFF` fill + `#000000` label | (measured)(inferred) | selected "History" chip = solid white capsule; **not** native accent-tinted inset selection |
| control/pill-inactive | dark translucent fill (~`#1A1A1C`), white label + gray count | (estimated)(inferred) | unselected category chips on black |
| accent/system | none bound | (measured)(inferred) | no system-accent on selection/focus/primary; chrome is accent-agnostic monochrome. Only saturation is *content* data (the `#0080FF` colour card) |
| type/label | SF Pro ~13–14pt logical | (estimated)(inferred) | wordmark, chip labels, card body; system font, sentence/title case |
| type/meta | ~10–11pt logical, secondary gray | (estimated)(inferred) | relative time, "24" counts, byte/size values — de-emphasised |
| control/pill-h | ~36pt logical (~66px composite) capsule | (estimated)(inferred) | chunky XL-tier capsule chips |
| control/circle-btn | ~23pt logical (~43px composite) diameter | (estimated)(inferred) | star / grid / export circular icon buttons — Rg/Lg tier, above 24px floor |
| radius/card | ~18–20pt logical (~34px composite) | (estimated)(inferred) | clip preview cards |
| radius/pill, radius/btn | capsule (infinite) | (measured)(inferred) | chips and icon buttons fully rounded |
| card/h | ~130–160pt logical (~240–290px composite) | (estimated)(inferred) | horizontal card shelf, single row |
| icon/source-favicon | ~16–18pt logical | (estimated)(inferred) | per-card provenance chip (Photos, Chrome, Mail) in footer |
| icon/toolbar-glyphs | SF Symbols monochrome (magnifier, star, 2×2 grid, export+badge) | (estimated)(inferred) | native symbol vocabulary |
| chrome/window | borderless floating HUD, frosted rounded frame, no traffic lights | (measured)(inferred) | legitimate window class (Spotlight/Paste-like); system menu bar visible top-right is desktop, not app |

## Layout skeletons

**Main HUD panel (horizontal clipboard shelf), dark**
- Outer: a wide, short floating rounded container — **frosted glass frame** (wallpaper visible through the left/right ends) enclosing a **pure-black content shelf**. Cropped at bottom in the composite.
- Row 1 — toolbar (~ leading→trailing): app identity (Apple-style mark + "Supaste") on the glass left end · inline search ("Search…" with leading magnifier, no visible bezel) · trailing cluster of 3 circular icon buttons (star = favourites, 2×2 grid = view/collections, export-with-badge). Left-aligned to a shared content inset shared by rows 2–3.
- Row 2 — category chips: horizontal capsule row — `History 24` (active, white fill) · `Prompts 24` · `Colors 24` · `Assets 24` · `Inspirations 24` · circular `+` (add collection). Each chip pairs a title (white) with a count in dimmer gray. Even inter-chip gaps.
- Row 3 — clip shelf: single horizontal row of equal-height preview cards, **content-type-aware**: image thumbnail (full-bleed photo) · text snippet (multi-line) · web screenshot · colour swatch (card fills with the actual colour, `#0080FF`) · document/link (white card + paper-plane glyph). Every card carries a footer meta row: source-app favicon + relative time (left), size/bytes (right). Even inter-card gaps > within-card padding.

## Signature moves
- **[GOLDEN-NUGGET] Content-type-aware clip cards.** The clipboard isn't a list — it's a visual shelf where each item renders *as its type*: a copied colour becomes a full-bleed colour card labelled `#0080FF`, an image becomes a thumbnail, a URL becomes a web screenshot, text becomes a legible snippet. Recognition-over-recall made structural. This is the app's entire character in one decision.
- **True-black gallery backdrop.** The content shelf is pure `#000` (measured), turning every preview card into a lit object. Systematic, purposeful (maximises card pop), and paired with a *glass* outer frame so it doesn't read as flat — a signature, not Contrast Dilution.
- **Counted collections as capsule tabs.** History / Prompts / Colors / Assets / Inspirations, each with a live `24` count — reframes a clipboard manager as a lightweight asset library for creatives.
- **Restrained monochrome chrome.** No brand accent anywhere in the UI; the only saturation on screen is user content. Rare discipline — but see Defects, it costs the native accent binding.

## Defects
- **Selection grammar deviation (native-tell):** the active "History" chip is a **solid white capsule with black text** — not the native flat inset-rounded fill with accent-tinted text/glyph. Reads like an iOS/web segmented toggle. Canon would tint selection with the system accent.
- **Accent unbound (native-tell):** selection, focus, and the notional primary action bind to *white*, not the user's system accent. Deliberate monochrome house style, but it forfeits the "accent is the user's" native rule.
- **Circular-background toolbar buttons:** native macOS toolbar actions are borderless monochrome symbols; here they sit in filled circular chips. Defensible on a glass HUD (era-appropriate capsule affordances) but a mild deviation from borderless-toolbar grammar.
- **Low-contrast chrome risk (soft):** circular button backgrounds are dark-gray on black (container edges near-invisible), and the `24` count badges are dim gray on dark chips — both hover near the 3:1 / 4.5:1 floors. `(estimated)` from a compressed composite; verify on a real capture.
- **Brand caution (not a UI defect):** the app pairs an Apple-logo glyph with its "Supaste" wordmark in both the cover headline and the panel identity — likely marketing dressing, but using Apple's mark as app identity is a trademark risk.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main HUD panel (dark) | 12/14 | #10 UI contrast — dark-gray circle buttons on black, near-invisible borders; #9 text contrast (borderline) — gray "24" counts on dark chips may miss 4.5:1 |

**Native-tells audit (10-pt): 7/10** — fails #3 selection grammar (white chip, not accent inset), #6 accent binding (no system accent), #9 toolbar (circular-background buttons vs borderless symbols, soft). Passes: #2 glass discipline (glass frame + opaque content, no glass-in-content), #5 density, #10 real chrome (legitimate borderless HUD).

## Icon (brand context only — not an icon digest)
Blue vertical-gradient squircle (light cyan top → deep `#0000FF`-ish bottom) with a single white rounded **capsule bar** near the top-centre — a paste-strip / clipboard-row abstraction, glossy top specular. Big-Sur-era material. Rhymes with the UI's capsule-everything language and blue content accent; reinforces the app's one motif (the clip capsule).
