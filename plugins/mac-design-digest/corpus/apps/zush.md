# Zush — profile

- **Source:** macapp.supply (`sources/zush/`, cover composite + icon only — no standalone gallery shots) · **Surfaces digested:** AI Rename main window (dark, ~@2x, cropped in a marketing composite) · **Last updated:** 2026-07-19
- **One-sentence identity:** A friendly-AI consumer utility that wears a real Mac shell over a web body — Raycast's dark-plus-electric-accent palette pushed toward toy warmth by a glossy 3D-robot mascot; the before→after rename row is its whole value proposition drawn as a repeated unit.
- **Cluster:** unassigned (candidate: "consumer-AI dark" / friendly-utility — non-native, tracked separately from macOS clusters)
- **Lineage:** **web-electron (high)** — contrast evidence only; nothing here feeds macOS canon. Tells below.
- **Era (chrome):** custom dark theme (not Liquid Glass, not legacy-native) — self-drawn hidden-inset chrome wrapping real traffic lights.

## Lineage evidence (why web-electron, not native)

Judged from the **body, not the frame** — the frame (traffic lights + sidebar-toggle SF Symbol) is genuine, but the body is decisively web-styled:

1. **Cross-platform meta:** marketing states "for Mac and Windows" — one codebase on both ≈ Electron/web toolkit (SwiftUI can't ship Windows). Meta, not design evidence, but it corroborates the visual tells.
2. **Multicolor rounded-square sidebar icons** (blue eye, orange clock, purple pie, green stack, red chip, grey gear, blue info) — the iOS-Settings / web pattern. Native macOS sidebars use **monochrome SF Symbols** that take the accent tint on selection. This is the #1 tell.
3. **Saturated full-bleed selection:** the selected "AI Rename" row is a solid indigo rounded-rect with white text. Native selection = flat inset subtle fill with accent-*tinted* text, never a saturated capsule.
4. **Web-style buttons:** "Start Over" / "+" are ~8px rounded-rect grey fills, not macOS 27 capsule push buttons.
5. **Pill-chip vocabulary everywhere** (AI Title, Smart Title Name, PRO) — bordered/tinted web chips.
6. **Density:** body/label text reads ~15–16pt with generous row spacing — above the native 13pt-body / 24pt-control grammar.

## Tokens

*All values from a single cropped marketing render at ~@2x — halved to pt where noted, wide ranges, `(estimated)` throughout. The app window bleeds off the composite's right edge, so content-area width is unknown.*

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/content | ~#16171E–#181A22 (very dark blue-charcoal) | (estimated)(inferred) | not neutral #1E1E1E — cool/navy-tinted |
| bg/sidebar | ~#1A1C24 (marginally lighter/warmer than content) | (estimated)(inferred) | full-height, no visible material/vibrancy — flat opaque |
| accent/brand-indigo | ~#6C5CE7–#6D5DF0 | (estimated)(confirmed) | selection fill, "AI Title" chip, PRO pill, wordmark heading. **Hardcoded brand hue, not the system accent** — native tell |
| accent/brand-green | ~#34D571–#3BE37A | (estimated)(confirmed) | transformation "→" arrows, PRO star, ∞/robot status glyphs, wordmark "Zush" |
| text/primary | ~#F1F2F5 | (estimated)(confirmed) | new names, sidebar labels, H1 |
| text/secondary | ~#88899. grey ~#868892 | (estimated)(confirmed) | original filenames (de-emphasised) — ~4:1 on bg, borderline |
| type/h1 | ~20–22pt, bold ("AI Rename" content title) | (estimated)(inferred) | |
| type/sidebar-label | ~15–16pt regular | (estimated)(confirmed) | larger than native 13pt body |
| type/row-name | ~14–15pt; source regular-grey / new-name medium-white | (estimated)(confirmed) | |
| font/ui | SF Pro or a very close humanist sans (ø/æ render clean) | (estimated)(inferred) | brand/marketing face is a separate rounded geometric bold (Poppins/Satoshi-class) |
| radius/selection | ~12–14px on the selected sidebar row | (estimated)(inferred) | |
| radius/icon-chip | ~8px, chips ~28–32px | (estimated)(confirmed) | |
| radius/button | ~8px (Start Over, +) | (estimated)(inferred) | web rounded-rect, not capsule |
| radius/window | ~12–14pt observed corner | (estimated)(inferred) | closes a kit gap only for THIS app — do not generalise |
| chrome/sidebar | full-height, flat opaque dark, real traffic lights top-left + sidebar-toggle SF Symbol top-right; single flat nav list (no section headers) | (estimated)(inferred) | |
| row/file | two-line: ~64px rounded thumbnail + source name over green-→ new name; row ~55–60pt tall, hairline divider | (estimated)(confirmed) | |
| space/grid | reads ~8px-based, systematic | (estimated)(inferred) | can't verify magic numbers at this res |

## Layout skeletons

**AI Rename — main window (dark):**
- **Left:** full-height sidebar (est. ~240–260px). Top-left inline traffic lights; top-right sidebar-collapse glyph. Flat nav list of 8 items (AI Rename / Monitor / Activity / Statistics / Templates / BYOK-Offline / Settings / About), each a multicolor rounded-square icon + label; selected item = solid indigo rounded-rect + white text. Bottom rail: indigo "PRO" pill (leading) + two green status glyphs (∞, robot) trailing.
- **Right:** content pane. H1 "AI Rename" top-left. A collapsible **"Template"** section (chevron) holding two chips: indigo-bordered "AI Title" and green-tinted "Smart Title Name". Below, a scrolling **result list**: each row = thumbnail + grey original filename + green "→" + bright new name, hairline-separated. Bottom action bar: "Start Over" + "+" (both quiet dark rounded-rect buttons), left-aligned.
- Alignment: sidebar-content share a clean vertical seam; row content left-aligns to a shared axis; H1 aligns to first row's text column.

## Signature moves

- **[GOLDEN-NUGGET] The before→after rename row.** Grey, de-emphasised source filename → bright confident new name, joined by a green transformation arrow, repeated down the list. It renders the product's entire promise ("AI renamed your files") as one legible, scannable unit — and it's textbook hierarchy-via-de-emphasis (label whispers, value speaks). This is *demonstrate-don't-describe* for an AI tool where trust in the output is the conversion.
- **Two-accent brand system:** electric indigo (identity/selection) + electric green (transformation/status), on cool near-black. Systematic across UI and brand backdrop and icon — warm, consumer, unmistakably "friendly AI".
- **Mascot-anchored trust:** the glossy 3D robot (big glowing green eyes, smile) on an indigo→violet gradient is the aesthetic thesis — it buys first-impression forgiveness for an automated tool.

## Defects

*(All are native-fidelity tells, expected for Electron and correctly excluded from mac canon — not cross-platform anti-patterns. The app is competent within its web idiom.)*
- **Non-native selection** — saturated full-bleed indigo fill + white text. Native canon: flat inset subtle fill, accent-*tinted* text.
- **Multicolor sidebar icons** — should be monochrome SF Symbols taking the accent on selection.
- **Accent not system-bound** — hardcoded brand indigo (+ a second green accent); native selection/focus/primary should bind to the user's system accent.
- **UI-contrast (WCAG non-text)** — row dividers/card borders are hairline and read <3:1 on the dark bg (#10). Secondary filename grey is ~4:1, marginally under the 4.5:1 text floor (#9, borderline).

## Rubric history

| Surface | 14-pt | Native-tells | Failures |
|---|---|---|---|
| AI Rename main window (dark) | 12/14 | 4/10 | 14-pt: #10 hairline divider/border <3:1; #9 secondary grey ~4:1 borderline. Native: #1 web-electron; #3 saturated non-inset selection; #5 web density (~15–16pt body); #6 accent not system-bound (+ second brand accent). Passing native: real chrome (#10), quiet single-action layout (#7), consistent radii (#8), no glass-in-content (#2 n/a). |

## Brand-backdrop evidence (composite, NOT app UI — do not conflate)
Cover surround: near-black navy radial ground; wordmark "Zush" in brand green bold rounded sans; headline "AI File Renamer & Organizer" (indigo) / "for Mac and Windows" (white) in a friendly geometric bold; white body copy; 5 gold stars + green "Private Offline AI" shield pill. Confirms the indigo+green two-accent system and the consumer/approachable positioning. Icon: 3D-rendered white robot mascot, glowing green eyes, on indigo→violet gradient squircle — mascot-class icon, corroborates palette; not digested as an icon (Workflow A only).
