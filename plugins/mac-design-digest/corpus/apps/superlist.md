# Superlist — profile

- **Source:** macapp.supply (cover composite only — no standalone shots) · **Surfaces digested:** desktop main window (list/document view, dark); iPhone "Inbox" recording screen (iOS, contrast-only) · **Last updated:** 2026-07-19
- **One-sentence identity:** Linear's dark desaturated discipline crossed with Notion's emoji taxonomy, given an oversized editorial display voice — every list is treated as a document with a magazine hero title.
- **Cluster:** unassigned — proposed non-native cluster "editorial-nocturnal web productivity" (kept OUT of macOS canon; see Lineage)
- **Lineage:** web-electron (high) — custom bundled typeface, circular checkboxes, app-defined accent, rounded-content-pane-on-chrome layout, emoji-as-icon sidebar. None of this evidence feeds macOS canon; native-tells below are recorded as tells + corrections only.
- **Era (chrome):** custom web design system (not Liquid Glass, not legacy-native) — a self-contained brand system rendered in a Mac window.

## Evidence provenance caveat
The only asset is a **marketing cover composite** (1200×630 OG image): a purple brand backdrop with wordmark + app icon, an angled iPhone render, and a flat (non-perspective) desktop window on the right. Only the desktop window and the sidebar strip beneath the phone are UI evidence. Because the render is at an **arbitrary/unknown zoom**, absolute pt values are meaningless — tokens below record **type-scale ratios and hex values** (reliable) and mark any px as `(estimated)` at render scale, never as native pt.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas (content pane) | `#232233` | (measured)(inferred) | desaturated indigo-navy, NOT neutral — deviates from kit dark window `#1E1E1E`; the tint is a brand choice |
| bg/chrome (sidebar + surround) | `#1D1C2B` | (measured)(inferred) | darker recessed surround; content sits as a rounded pane on top (top-left corner radius visible) |
| text/primary | `#FFFFFF` on canvas → 15.6:1 | (measured)(inferred) | titles, item labels; pure white (no 85%-black-equiv softening the kit uses) |
| text/secondary | `#747385` on canvas → **3.36:1** | (measured)(inferred) | breadcrumb, dates, durations — desaturated purple-gray; **below 4.5:1**, see Defects |
| accent/brand | periwinkle `#7974D2`; indigo dot `#5451A1` | (measured)(inferred) | app-defined accent (avatars, project dot), NOT the system accent — web tell |
| brand/warm | icon red-orange `~#E8442A→#C33` ramp | (estimated)(inferred) | the one warm hue in an otherwise cool palette — Von Restorff anchor |
| type/family | custom geometric grotesque (double-story a, single-story g), NOT SF Pro | (measured)(confirmed) | consistent across title, sidebar, body — bundled webfont; the single loudest non-native tell |
| type/display (doc title) | black/heavy weight, ~2 lines, tightest leading; largest tier | (estimated)(inferred) | "Production Planning: June Photoshoot" — the hero |
| type/section header | bold, ~0.5× the display size | (estimated)(inferred) | "Action Items" |
| type/item title | medium-bold white, ~0.85× the section header | (estimated)(inferred) | task labels, "Meeting transcript" |
| type/meta | regular, smallest tier, secondary gray | (estimated)(inferred) | date/time/duration row |
| type ramp | ≤5 distinct sizes, clear geometric steps (display ≫ section > item > meta) | (estimated)(inferred) | rubric #4 pass |
| control/checkbox | **circular** empty ring, ~24px at render scale | (estimated)(inferred) | web/iOS pattern — native macOS uses square/rounded-square NSButton |
| control/attachment row | full **capsule** outlined pill; faint border, fill = canvas | (measured)(inferred) | "Meeting transcript" card — outlined not filled; border < 3:1 |
| control/trailing button | circular icon button (list/lines glyph) on row + card | (estimated)(inferred) | hover-action affordance |
| sidebar/icons | **emoji** per item (💰 grinning 🌐) + disclosure `>` chevrons for groups | (measured)(confirmed) | Notion-style emoji taxonomy — recognition anchors, not SF Symbols |
| sidebar/labels | title case, secondary gray, custom font | (measured)(inferred) | no tracked-uppercase (one thing it gets right vs web norms) |
| nav/chrome | in-app `< >` back/forward chevrons top-left | (measured)(inferred) | web history nav, not a native toolbar |
| radius/pane | rounded content-pane top corner | (estimated)(inferred) | Linear/Notion "inset rounded canvas" layout |

## Layout skeletons

**Desktop main window (dark).** Three zones on a two-tone dark ground:
- **Left sidebar** (full-height, on chrome `#1D1C2B`): vertical item list, each row = leading emoji-or-`>`-chevron + title-case label in secondary gray; collapsible groups (Personal, Work) via chevrons; flat items (Brand Deals, Potential Guest) via emoji. Generous row height.
- **Chrome gutter** above content: `< >` history nav sits in the recessed surround, left of the content pane.
- **Content pane** (rounded top-left corner, on `#232233`): single left alignment axis holds, top→bottom — breadcrumb (project dot + "Production Planning / June Photoshoot", slash separators, secondary gray) → **oversized display title** (2 lines, black weight) → **outlined capsule "Meeting transcript" row** (circular purple speech-bubble avatar + bold title + gray "Mon, Jun 10 · 9:41 AM · 32 minutes" + trailing circular list button) → **"Action Items"** section header → checklist rows (circular checkbox + white task title + calendar-glyph gray date, trailing circular avatar photos + hover list button). Right edge shows a bleed of a photographic cover image (per-list header art).

**iPhone "Inbox" screen (iOS — contrast evidence only, excluded from macOS canon).** Dark full-screen recording/transcription view: "Inbox" pill top-left, EN + ✕ controls top-right, centered audio **waveform in brand-colored bars** (red/pink/purple/blue — the palette made kinetic), circular record/avatar FAB bottom-right, pause control bottom-left. Confirms the brand's colorful-on-dark signature but is not Mac evidence.

## Signature moves
- **[GOLDEN-NUGGET] The document-hero title.** Each list opens with an oversized black-weight display heading dwarfing all chrome — a magazine/editorial hierarchy that reframes "a to-do list" as "a document." This single decision carries the app's whole prosumer-premium character; it's systematic (breadcrumb → hero → body repeats the article grammar).
- **Emoji as taxonomy.** Sidebar identity comes from per-item emoji, not SF Symbols — warmth + fast recognition scanning, borrowed wholesale from Notion.
- **One warm hue in a cool room.** A single red-orange brand mark (icon, and the waveform's warm bars) isolated against a uniformly desaturated indigo-navy palette — deliberate Von Restorff contrast; the accent that carries *interaction* is a cool periwinkle, so warmth stays purely brand.
- **Attachments as capsule rows.** Rich objects (a meeting transcript) render as full-capsule outlined pills inline in the document — a recognizable, tappable "chip that is also a row."

## Defects
- **Contrast Dilution (metadata)** → secondary gray `#747385` on `#232233` measures **3.36:1**, below the 4.5:1 body floor; dates, durations, and the breadcrumb all sit here. Canon fix: lift secondary to ≥4.5:1 (toward `#9A99AD`+) or enlarge, since these carry real scheduling data.
- **UI-contrast thinness** → the "Meeting transcript" capsule border and checkbox rings read faint (fill = canvas), likely <3:1 against `#232233`. Canon fix: 3:1 non-text minimum on any control edge that must be found.
- **Native-tells (as web-electron, corrections not defects):** custom typeface (→ SF Pro / respect system font); circular checkboxes (→ square NSButton); app-defined periwinkle accent (→ bind selection/focus to the *user's* system accent); tinted `#232233` canvas (→ neutral `#1E1E1E` system dark); in-app `< >` nav (→ real toolbar with menu-bar parity). These are correct *for a cross-platform web app*; they simply don't feed macOS canon.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| desktop main window (dark) | 12/14 | #9 secondary text 3.36:1 <4.5:1; #10 capsule/checkbox border likely <3:1 |
| — native-tells audit | ~2/10 | web-electron lineage: fails #1 native, #5 density, #6 system-accent binding, #3 selection grammar, #9/#10 toolbar; #2/#7/#8 N/A |
