# Glance — profile

- **Source:** macapp.supply (cover composite only — no standalone shots supplied) · **Surfaces digested:** main document window (dark), rendered-markdown reading view with active find bar + table context menu · **Last updated:** 2026-07-19
- **One-sentence identity:** iA Writer's typographic reading-focus rebuilt as a native macOS document viewer — "no editor chrome," where the rendered content *is* the interface (peers: iA Writer, Bear, Apple Quick Look markdown preview).
- **Cluster:** unassigned (first app in corpus; provisional hint `native-minimal-reader`)
- **Lineage:** native (high) — genuine coloured traffic lights, document titlebar with "Edited" state, system find bar with "1 of 9" grammar, native context menu (leading SF Symbols, sentence case, destructive item divider-separated at bottom), system-blue selection. No iOS/web tells.
- **Era (chrome):** Liquid Glass native (macOS 26+) — capsule glass toolbar controls, two zoom buttons sharing one continuous morphed container, pill find field, rounded translucent context menu.

## Provenance caveat
Evidence is a **single marketing-cover composite** (1680×945), not a raw screenshot. The app window is a real capture placed on an iridescent Sequoia-style gradient with left-side brand type ("Markdown editor for Mac", "View .md files Instantly") — brand evidence, analysed separately from the window. Scale reads ~1× (traffic-light cluster ≈ 78px vs 68pt spec → downscaled marketing render), so **all pixel values are `(estimated)` with wide ranges**; ratios are more trustworthy than absolutes. Window right + bottom edges bleed off the frame — no sidebar is visible and the layout implies a single content pane, but "no source list" is inferred, not confirmed. Dark mode only; light mode unseen.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | ~#1C1C1E–#1E1E1E, dark | (estimated)(inferred) | matches kit dark window bg `#1E1E1E` |
| type/body (reading) | ~15–16px SF Pro, lh ~1.5× | (estimated)(inferred) | **deliberately larger than kit 13pt Body** — reading-optimized, the app's core move |
| type/h1 | ~28–30px, Bold | (estimated)(inferred) | "Welcome to Glance"; above kit LargeTitle 26pt |
| type/h2 | ~19–20px, Bold | (estimated)(inferred) | "Things to try"; ~Title2 17pt+ |
| type/code (inline) | monospace, subtle fill chip | (estimated)(inferred) | ``.md`` rendered as inline code |
| accent/primary | system blue ~#0091FF | (estimated)(inferred) | matches kit Dark Blue `#0091FF`; sole accent |
| find/active-match | bright yellow bg (~#FFEA00), black text | (estimated)(inferred) | the 1-of-9 current match |
| find/other-match | muted olive/tan bg | (estimated)(inferred) | the 8 dimmed non-active matches — two-tier find highlight |
| chrome/toolbar | glass capsules, ~36pt (XL-tier) controls, 3 groups | (estimated)(inferred) | zoom pair (morphed) · icon pull-down · share |
| chrome/titlebar | centred document title "glance.md" + "Edited" secondary subtitle | (estimated)(inferred) | classic AppKit document-window titlebar |
| find/field | pill field, magnifier + query + "1 of 9" + ▲▼ + ✕ | (estimated)(inferred) | right-aligned to content width |
| radius/toolbar-control | capsule (height/2) | (estimated)(inferred) | Liquid Glass bezel |
| radius/context-menu | ~10–12px | (estimated)(inferred) | rounded translucent popover |
| selection/table | 2px accent-blue outline + column ellipsis handle | (estimated)(inferred) | spreadsheet-style range selection, not list-row fill |
| table/header | Bold, subtle elevated fill | (estimated)(inferred) | Action / Shortcut columns |

## Layout skeletons
**Main window (dark, single pane):** Titlebar 33pt-class — traffic lights top-left (all coloured = focused), centred "glance.md" + "Edited" state, trailing toolbar of three glass groups (zoom −/+ morphed pair · Glance-icon pull-down w/ single chevron · share). Below chrome, a right-aligned floating find bar. Content column shares one left margin axis: large welcome app-icon → H1 → body paragraph → H2 → two-column markdown table (Action | Shortcut). Prose and table span nearly the full window width (no visible max-width prose rail). A table context menu (Insert Column Left / Right · —— · Delete Column) floats over the selected Shortcut column. No sidebar, no inspector, no bottom format bar.

## Signature moves
- **"No editor chrome" reading surface.** Single content pane, no source list, no inspector; the rendered markdown carries the whole UI. The interface *is* the typography — a genuinely restrained choice for a category that usually ships split-pane editors.
- **Reading-optimized body type above system size (~15–16px vs macOS 13pt Body).** The tagline "generous typography" is literal and systematic — the app trades chrome density for reading density.
- **Two-tier find highlight:** the active match is bright yellow/black; the other eight are dimmed olive. Von Restorff applied inside the find experience so the current hit reads pre-attentively against its own siblings.
- **Editor disguised as a viewer.** Marketing says "viewer," but the window shows editable cells (blue text caret after ⌘N) and full table-column operations via native context menu — complexity absorbed into contextual affordances (Tesler / progressive disclosure) rather than surfaced as toolbar chrome.
- **Friendly minimal mascot icon** (light squircle, faint spreadsheet grid, two-bar eyes + smile) softening an otherwise disciplined pro-adjacent tool — brand warmth without breaking the quiet chrome.

## Defects
- **Line Length Fatigue (soft / watch)** → welcome paragraph wraps near the window's right edge (~75–85 chars on a wide window) with no visible prose max-width → canon would cap reading measure at ~65–75ch, the one thing a reading-first app most owes its user. Unverifiable exact width on a downscaled composite; flagged as the honest miss.
- **Toolbar grammar minor deviation** → the pull-down uses the *colour* Glance app-icon glyph rather than a borderless monochrome SF Symbol (native toolbar convention). Systematic-purposeful (it reads as the document/format menu) so logged as a deviation, not a hard defect.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark, composite) | 13/14 | #6 measure (prose ~75–85ch, no rail); #1 grid + #10 UI-contrast noted unverifiable on downscaled composite (plausible-pass) |
| — native-tells audit | 9/10 | #9 toolbar pull-down uses colour icon not mono symbol; #3 table selection is range-outline not list-fill (context-appropriate); #4 sidebar N/A |
