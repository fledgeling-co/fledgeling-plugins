# Forma — profile

- **Source:** macapp.supply (cover composite only) · **Surfaces digested:** main window / infinite canvas, light mode (1 surface) · **Last updated:** 2026-07-19
- **One-sentence identity:** Excalidraw's hand-drawn mind-map warmth rebuilt on a monospaced engineering-notebook grid — a terminal-flavoured whiteboard where every note is a black tile on graph paper.
- **Cluster:** unassigned (candidate seed for a "mono-canvas / drafting-table" cluster)
- **Lineage:** native (med) — the window *frame* reads genuinely AppKit/SwiftUI (real macOS traffic lights rendering over a fully transparent titlebar, no web-chrome tells), but the entire body is a custom-drawn canvas, so it yields almost no native-*control* evidence. Whiteboard = custom surface regardless of framework; treat its interior as brand-custom, not mac canon.
- **Era (chrome):** custom / non-participating — no Liquid Glass anywhere (correct: content stays opaque), but the chrome is a bespoke transparent titlebar + floating dark tool bar, not a standard unified glass toolbar. Not classifiable as Liquid-Glass-era or legacy-native; it opts out of the material system entirely.

> Provenance caveat: the only input is a marketing cover composite; the app window sits inside a blue-gradient brand panel and is rendered at ~1.8× (≈@2x, inferred from a 73px traffic-light centre-to-centre vs the 40pt native cluster span). All pixel values below are `(estimated)` from a scaled render; logical-pt figures are original-px ÷ ~1.8 with wide error. Colours are clean `(measured)` off the render but from one surface only, hence `(inferred)`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | `#ECECEC` warm light-gray (measured)(inferred) | | infinite board ground; NOT pure white — a paper tone, ~#FFFFFF kit window bg softened |
| canvas/texture | square grid + centred "+" tick marks + fine speckle noise (estimated)(inferred) | | graph-paper / drafting motif; a content-layer texture, not chrome |
| surface/card | `#2F2E2D` warm charcoal (measured)(confirmed) | | sticky-note tiles; **identical hex to the tool bar** — one dark-surface token, good consistency |
| surface/toolbar | `#2F2E2D` (measured)(confirmed) | | floating bottom tool bar shares the card surface exactly |
| text/on-dark | `~#D2D2D2` off-white mono (measured)(inferred) | | card body; ≈9:1 on card, passes |
| text/secondary | `#A2A2A2` (measured)(inferred) | | breadcrumb; ≈2.1:1 on #ECECEC — fails 4.5:1 (see Defects) |
| text/muted-on-dark | `~#444444` (measured)(inferred) | | "Clear Canvas" ghost label; ≈1.2:1 on #2F2E2D — near-invisible |
| accent/primary | `#FFD501` vivid yellow (measured)(inferred) | | active-tool fill (System-Yellow-adjacent #FFCC00/#FFD600); a BRAND accent, not system blue — does not bind to selection/focus |
| control/checkbox | `#5E5D5C` unchecked, ~4–5pt radius (measured)(inferred) | | ≈2.1:1 on card — below 3:1 UI floor |
| type/body | monospace, ~13–15pt logical, lh ~1.4–1.5 (estimated)(inferred) | | a modern coding mono (Berkeley Mono / Commit Mono class — not identified); used for ALL text |
| radius/card | ~18–22px orig → ~10–12pt logical (estimated)(inferred) | | soft, friendly; steps down to ~4–5pt on nested checkboxes (concentric) |
| radius/tool-button | ~10–14px orig → ~6–8pt logical (estimated)(inferred) | | yellow Card button, segmented tool chips |
| elevation/card | soft drop shadow, low blur, ~0 spread (estimated)(inferred) | | cards float as physical tiles on the board |
| chrome/titlebar | fully transparent; traffic lights + breadcrumb over live canvas (measured)(inferred) | | genuine macOS lights #FE5F58/#FEBC30/#2BC83E in correct order |
| chrome/toolbar-bar | floating dark bar, ~80px orig → ~44pt logical tall, rounded top corners (estimated)(inferred) | | bottom-anchored tool palette |
| connector/edge | black hand-drawn bezier, ~2px stroke, organic wobble, pen-nib terminus (estimated)(inferred) | | mind-map links between cards |

## Layout skeletons

**Main window — infinite whiteboard canvas (light):**
- **Frame:** transparent unified titlebar. Traffic lights top-left (genuine, ~73px cluster). Centre: a breadcrumb path — small "forma" cluster-glyph + `forma / product launch` in secondary-gray mono. No NSToolbar, no sidebar, no source list.
- **Canvas:** full-bleed #ECECEC graph paper (square grid + "+" ticks + noise), pannable/zoomable (inferred, freeform).
- **Cards:** freely positioned #2F2E2D rounded tiles. Two kinds — *checklist cards* (mono title line, then rows of unchecked box + label: "design → update guidelines / landing page / icon set"; "dev → API endpoints / unit tests / deploy") and *note cards* (plain text: "Marketing", "Product Launch" [larger, central hub], "Research competitors", "Submissions due Dec 1."). Placement is user-arranged, so inter-card spacing is not a design grid — internal card padding ~16–20px orig is consistent.
- **Connectors:** hand-drawn black beziers radiating from the central "Product Launch" hub to the satellite cards; one edge terminates in a rendered pen-nib cursor.
- **Bottom tool bar (floating, dark):** left cluster — `Card` (yellow filled, active tool) │ pen/marker `2` │ eraser `3` (numerals = keyboard accelerators). Centre — a mo–su weekday **line sparkline** (function ambiguous from a still; activity/streak widget or decorative). Trailing — `Clear Canvas` (ghost, muted, destructive kept recessive).

## Signature moves
- **[GOLDEN-NUGGET] Monospace-everything on graph paper.** Every text element — breadcrumb, card titles, checklist items, tool labels, weekday ticks — is one monospaced face; paired with the "+"-tick grid and paper noise it commits fully to a drafting-table / engineering-notebook register (Terminal-hacker family softened, not costume-worn). This single decision *is* the app's character.
- **[GOLDEN-NUGGET] Inverted note polarity.** Whiteboards default to light/pastel stickies; Forma makes notes near-black #2F2E2D tiles with light text on a pale board — maximal figure-ground, the cards read as physical objects. Systematic across every card → signature, not defect.
- **Hand-drawn bezier connectors + visible pen-nib cursor.** Organic wobble and a rendered nib inject craft/warmth against the rigid mono grid — the same tension Excalidraw exploits. A deliberate warmth gesture.
- **Visible keyboard accelerators on tools (Card=1 implied, Pen 2, Eraser 3).** Discoverability/expert signal baked into the tool chrome (information scent).

## Defects
- **Contrast Dilution (text) — fails rubric #9.** Breadcrumb #A2A2A2 on #ECECEC ≈2.1:1; "Clear Canvas" ~#444 on #2F2E2D ≈1.2:1 (near-invisible). De-emphasis pushed well past the 4.5:1 floor. Canon fix: secondary text to ~#6B6B6B on this ground (≥4.5:1); a destructive ghost action can stay quiet but must clear ~3:1 to be legible.
- **UI-contrast shortfall — fails rubric #10.** Unchecked checkboxes #5E5D5C on card #2F2E2D ≈2.1:1, below the 3:1 non-text floor. Lift the box stroke/fill or add a hairline.
- **Flat in-card hierarchy (minor).** Card titles ("design", "dev") share the mono size/weight/colour of their checklist items; hierarchy rests only on position + the checkbox glyphs. A single weight or tier step would earn the title. Borderline house-style, not a hard fail.
- **Accent not bound to the user's system accent (native deviation).** The one saturated colour is a fixed brand yellow, and no selection/focus grammar is visible — deviates from "accent is the user's". Acceptable as a custom canvas app's house style; noted as a tell, not learned as mac canon.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window / canvas (light) | 11/14 · native 7/10 | 14pt: #9 text contrast (breadcrumb 2.1:1, Clear Canvas 1.2:1), #10 checkbox 2.1:1; #2/#12/#13/#14 n/a (freeform canvas, no forms/inputs/visible focus). native: #6 accent-binding fail (brand yellow, not system accent); #3/#4/#9 n/a or custom (no native selection/sidebar/NSToolbar); frame, glass discipline, corners, chrome, one-action all pass. |
