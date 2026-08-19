# Mux — profile

- **Source:** macapp.supply (cover.jpg — marketing composite) · **Surfaces digested:** menu-bar-extra dropdown (dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** A network-switching menu-bar utility that shows its entire product surface as one disciplined NSMenu — TripMode's/One Switch's "invisible until needed" register, executed to the letter of the system menu grammar.
- **Cluster:** unassigned (candidate: menu-bar-utility / system-deferential — sole member so far)
- **Lineage:** native (high) — genuine AppKit `NSStatusItem` + `NSMenu`; 13pt-class body, 24pt menu rows, real translucent menu bar with auto-tinting glyphs, system-rendered separators/submenu chevrons/shortcut glyphs. Nothing iOS- or web-derived.
- **Era (chrome):** Liquid Glass native (macOS 26+) — dark translucent menu material with visible wallpaper bleed, ~10pt menu corner radius, capsule-ish menu-bar item highlight.

## Provenance caveat
The only asset is the marketing **cover**, a composite: a device-framed MacBook (rounded bezel + notch camera) showing the top-left screen corner, a colourful gradient wallpaper, and right-side brand type ("Your Mac, / always on the best network."). **Only the menu-bar-extra + its dropdown are design evidence**; the device frame, wallpaper, and headline are brand/marketing. All menu metrics are `(estimated)(inferred)` from a single render at derived scale ≈2.55px/pt (row pitch 63px ≈ 24pt; menu corner 25px ≈ 10pt) — no raw @2x screenshot. The one strong corroboration: the derived **24pt menu-item row pitch matches the kit's Regular menu item exactly** (`kit/macos-27.md` `(specified)`), evidence of real platform metrics rather than a hand-drawn mock.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| menu/width | ~240pt (~620px render) | (estimated)(inferred) | menu-bar-extra dropdown, sizes to content |
| menu/height | ~232pt (~592px render) | (estimated)(inferred) | 9 rows + 2 separators |
| menu/row-pitch | ~24pt (~63px render) | (estimated)(inferred) | matches kit Regular menu item 24pt (specified) |
| menu/corner-radius | ~10pt (~25px render) | (estimated)(inferred) | concentric-consistent top+bottom corners |
| menu/material | dark translucent vibrancy/glass | (estimated)(inferred) | wallpaper bleed visible (blue→graphite top→bottom); floating chrome, glass legitimate |
| type/item | ~13px SF Pro Regular, white/primary | (estimated)(inferred) | consistent with kit menu Body 13pt |
| type/section-header | ~11–12px, secondary label (gray) | (estimated)(inferred) | "Current Network" disabled header, Title Case |
| type/shortcut | ~13px, secondary/tertiary gray | (estimated)(inferred) | ⌘, and ⌘Q dimmed vs primary label |
| separator | ~1px inset hairline, low-contrast | (estimated)(inferred) | system-rendered; native ~29% separator |
| statusitem/glyph | monochrome template "fork/branch" (two diverging arrows) | (measured)(inferred) | brand mark carried from app icon into the bar as a template symbol |
| statusitem/highlight | soft light capsule/rounded-rect (menu-open state) | (estimated)(inferred) | matches kit menu-bar item selection (~13 radius, capsule) |
| accent | none rogue; only system highlight | (inferred) | no app-defined accent hue applied anywhere |

## Layout skeletons

**Menu-bar-extra dropdown (dark).** Single left-aligned text column; trailing axis carries submenu chevrons and keyboard-shortcut glyphs, both right-aligned to a shared edge. Three separator-delimited groups, top→bottom:
1. **State group** — disabled section header "Current Network" (secondary) over the live value row "Thunderbolt Ethernet ›" (primary, submenu).
2. **Config group** — "Preferred Network ›", "Recent Activity ›" (both submenus).
3. **App-commands group** — "Check for Updates…", "Preferences… ⌘,", "Quit Mux ⌘Q".

Menu bar above it: trailing status cluster — Mux fork-glyph (highlighted/open) · a second toggle-style glyph (unattributed; possibly a second Mux indicator or unrelated extra) · clock "20:41:00" (24-hour, seconds shown).

## Signature moves
- **[GOLDEN-NUGGET] The whole product is one menu.** No window, no toolbar, no visible Settings surface — the app deliberately owns zero custom chrome and inherits the macOS menu aesthetic wholesale. Character comes not from styling but from restraint: an "invisible-until-needed" networking utility.
- **State-first information architecture.** The menu opens by answering the user's actual question — *what network am I on?* — with a disabled header + live value at the very top ("Current Network → Thunderbolt Ethernet"), then offers configuration below. Recognition over recall, encoded in menu order.
- **One glyph does all the semantic work.** A custom "diverging fork / best-path" mark is the app's entire visual identity: glossy blue Liquid-Glass treatment on the icon squircle, reduced to a monochrome template symbol in the menu bar. The metaphor (routing/multiplexing to the best path) is legible at both sizes.

## Defects
- **None substantive** — the menu honours native grammar throughout: correct ellipsis usage ("Check for Updates…", "Preferences…" open views; "Quit Mux" does not), one-level submenus via chevrons, ≤3 separator groups, Title Case labels, dimmed (not hidden) shortcut glyphs, system-rendered separators.
- *Note, not a defect:* the "Current Network" header sits at native secondary-label contrast on the dark material (low ratio by design — it is a disabled header, a platform convention, not Contrast Dilution).
- *Composite artifact:* dark menu material over a bright wallpaper is internally consistent (menu-bar glyphs auto-tint dark over bright areas in either appearance), so this reads as genuine dark mode on a colourful wallpaper rather than a fake — but it is still a composed marketing render, not a raw capture.

## Rubric history
| Surface | Rubric | Native-tells | Failures / notes |
|---|---|---|---|
| menu-bar-extra dropdown (dark) | 13/14 | 9/10 | R#14 focus appearance not evidenced (static); many R checks (6,8,12,13) n/a for a menu → counted pass. Native #3 row-selection not evidenced (no active row shown); #9 toolbar n/a (no toolbar surface). |
