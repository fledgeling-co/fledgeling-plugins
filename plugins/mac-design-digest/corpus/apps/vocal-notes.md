# Vocal Notes — profile

- **Source:** macapp.supply (`tychospot.com/vocal-notes`) · **Surfaces digested:** main window — three-pane transcript reader (sidebar + list + detail), 1 surface, light, from marketing cover · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple Notes' three-column shell, faithfully reproduced and repurposed as an on-device Whisper transcription reader — Voice Memos' audio player and a word-synced highlight grafted into a Mail/Notes source-list-plus-preview-plus-reader chassis; native fidelity is total, originality is near-zero.
- **Cluster:** unassigned — belongs with an "Apple-Notes-shell native productivity" family (source-list + message-list + reader triad); nearest existing kin in corpus are other capture/notes/audio tools.
- **Lineage:** native (high) — every body tell is AppKit/SwiftUI `NavigationSplitView`: 13pt-class body, ~40pt Large source-list rows with inset selection, real coloured traffic lights + sidebar-toggle, borderless monochrome SF-Symbol toolbar, a capsule pop-up button, opaque content cards, sentence-case sidebar/section headers. No Catalyst tells (no inset-grouped card tables, no UISwitch pills, no per-row chevrons), no web tells (no uppercase-tracked headers, no kebab menus, no pointer-hand cursor). High confidence despite the marketing framing because the density and control grammar are unambiguously desktop-native.
- **Era (chrome):** liquid-glass (med) — the capsule-bezel pop-up ("Auto(English)"), large window radius, rounded opaque content cards and borderless toolbar are macOS 26/27-era signatures (per kit deltas, capsule is the new default bezel). Glass *material* itself is not visually confirmed: the toolbar band reads flat light, no obvious lensing — recorded `(insufficient-evidence)` for glass per the Liquid-Glass humility rule. A legitimately flat-chrome native window, current-era geometry.

> **Evidence caveat:** the only app UI is the window *inside a 2000×1250 marketing composite* (`cover.jpg`). The teal/green sunburst backdrop and the glossy chrome-glass headline "Transcribe All on Your Mac" are **brand evidence**, kept separate from the app-UI tokens below. The traffic-light cluster measures ~72px against the kit's 68pt spec, so image-px ≈ logical-pt here — measurements are more trustworthy than a typical render, but still marked `(estimated)` (possible resampling). Per Workflow A (UI only) no `icons/vocal-notes.md` is written — the waveform icon is recorded as brand context in Notes.

## Tokens

### App UI — three-pane main window (light)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#FFFFFF` content, sidebar ~`#F4F4F5` translucent | (estimated)(inferred) | Content panes opaque white; sidebar a lighter desaturated gray (vibrancy material) |
| type/reader-title | ~22pt Bold, `#000`@~85% (Title1) | (estimated)(inferred) | "30-Second Demo Narration" — kit Title1 = 22pt |
| type/reader-body | ~15pt Regular, `#000`@~85%, lh ~22pt | (estimated)(inferred) | Kit Title2 size (15–17pt); loose reading measure ~45–55 chars/line |
| type/list-title | ~13pt Semibold, `#000`@~85% (Body-emphasized) | (estimated)(inferred) | Transcript row titles |
| type/body-secondary | ~13pt/11pt Regular, `#000`@~50% gray | (estimated)(inferred) | List preview snippet, sidebar counts, "Today"/"Saved on this Mac" headers, metadata line |
| type/metadata | ~11–12pt Regular secondary, middot-separated | (estimated)(inferred) | "Apr 15, 2026 at 16:28 · Launch Kit · EN" — clean de-emphasis |
| accent/primary | system blue ~`#0A6CFF` | (estimated)(inferred) | List selection fill + language pill; reads as `controlAccentColor` blue, not a brand override |
| sidebar/width | ~220–240pt, full-height | (estimated)(inferred) | Kit sidebar example is 256; this runs slightly narrower |
| sidebar/row | ~40pt pitch (Large tier), icon + label + trailing count | (estimated)(inferred) | Matches kit Large sidebar row (40); selection radius ~8 |
| sidebar/selection | gray inset-rounded fill (inactive-pane), ~4px insets, radius ~8 | (estimated)(inferred) | "All Transcripts" muted gray because focus is on the list pane — correct two-level selection |
| list/row | ~64–72pt, title + trailing time / 1-line preview / optional folder chip | (estimated)(inferred) | Mail/Notes message-row anatomy |
| list/selection | solid accent-blue full-width inset-rounded fill, radius ~8–10, ~8px L/R insets, knockout white text | (estimated)(inferred) | Notes/Mail content-list house style (solid accent, not the flat-tint general rule) |
| control/pop-up | capsule bezel, globe glyph + "Auto(English)" + chevron, h ~30–32pt | (estimated)(inferred) | Language selector; capsule = macOS 26/27 bezel signature |
| toolbar/icons | borderless monochrome SF Symbols, ~24–28pt hit, ~10 actions in 3–4 clusters | (estimated)(inferred) | Reader toolbar: transcribe/import · redo · language pill · copy/star/share/export/search |
| card/content | rounded panel, radius ~12–16, ~1px very-light hairline border, opaque | (estimated)(inferred) | Two cards in reader: audio-player + transcript body; borders near-invisible (see Defects) |
| player/scrubber | thin capsule track + circular knob; skip-15 / play / skip-15 / times / volume / AirPlay / more | (estimated)(inferred) | Voice-Memos-class transport; times tabular ("00:00:00" / "00:00:21") |
| highlight/word | amber-peach `~#FDE8C8` on "Record,"; gray `~#E5E5E7` on "editable," | (estimated)(inferred) | Inline transcript highlight — the one domain-specific token (word-timing / annotation) |
| radius/window | ~12–16px | (estimated)(inferred) | Kit window radius is a gap; useful observed data point |
| chrome/traffic-lights | genuine coloured 3-dot cluster ~72px + sidebar-toggle, leading inset ≈ top inset | (estimated)(inferred) | Real focused-window frame; calibrates px≈pt |

### Brand (marketing composite — NOT app-UI tokens)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | radial sunburst — teal/green center rays `~#3FD0C0`→`~#7BE0A0` over blue `~#2E5BE0`, indigo corners `~#3B1E8C` | (estimated)(inferred) | Sequoia-style abstract wallpaper; optimistic aqueous mood |
| brand/headline | glossy chrome-glass beveled type, light cyan-white, bold rounded sans | (estimated)(inferred) | "Transcribe All on Your Mac" — a Liquid-Glass *text* treatment (refractive highlights); brand voice, not app UI |
| icon/glyph | cobalt-blue `~#2F6BF6` waveform of rounded-capsule bars, centered on white squircle, top-light + soft drop shadow | (estimated)(inferred) | Big-Sur-era single-glyph-on-light-material icon; not run through icon rubric (Workflow A only) |

## Layout skeletons

**Main window — three-pane `NavigationSplitView` (light):**
- *Left — source list (~220–240pt, full-height, vibrancy):* traffic-light cluster + sidebar-toggle at top; a sentence-case muted section header "Saved on this Mac"; 8 rows on a shared left axis — each = leading monochrome SF Symbol + label + right-aligned secondary count (All Transcripts 35 / Starred 6 / Daily Ops 4 / Launch Kit 4 / Product Research 4 / Customer Voices 6 / Creator Workflow 4 / Field Notes 3). "All Transcripts" carries the gray inactive-pane inset selection. Footer: borderless "+ New Folder".
- *Middle — transcript list (~440pt):* a two-icon mini-toolbar top-right (duplicate/stack + trash); a "Today" muted date header; message rows = bold title (left) + right-aligned time / one-line secondary preview / optional folder chip (folder glyph + name). The focused-pane selection ("30-Second Demo Narration") is a solid accent-blue inset-rounded row with knockout white text. Multilingual content (EN/JA/ZH) demonstrates i18n.
- *Right — reader/detail (~680pt):* borderless SF-Symbol toolbar (transcribe/import · redo · capsule "Auto(English)" language pop-up · copy/star/share/export/search); Title1 headline; middot metadata line; a "Source Audio" label over an audio-player card (skip-15 / play / skip-15 / scrubber / elapsed+remaining / volume / AirPlay / more); a transcript body card with ~15pt loose-leading text and two inline word highlights. Both cards opaque on the white content area (content stays opaque — glass discipline honoured).

## Signature moves
- **[GOLDEN-NUGGET] The audio-anchored transcript reader is the whole product idea in one card.** Strip the Apple-Notes shell away and the single decision that makes this a *transcription* app rather than a notes app is the reader's pairing of a "Source Audio" player card with a word-synced inline highlight (amber "Record," advancing with the scrubber, gray "editable," as a secondary state). The one place the app spends its originality budget is binding text to timeline; everything else is inherited platform grammar. This is Jakob's-Law-correct: near-total convention adoption buys instant familiarity, and the app is honest about where it innovates.
- **[GOLDEN-NUGGET] House-style solid-accent list selection done right.** The list uses the Mail/Notes solid-blue full-width inset-rounded selection with knockout white (title + preview + folder chip all invert), while the *sidebar* simultaneously shows a muted gray inactive-pane selection — the correct two-level focus grammar that many clones get wrong by painting both panes accent-blue. The eye lands on exactly one row per pane.

## Defects
- **Contrast Dilution (mild) — content-card hairline borders.** The audio-player and transcript-body cards are bounded by a `~1px` near-white border (`~1.05:1` against the white content area) — functionally invisible; the cards read as separated by whitespace alone. Fine as a quiet look, but fails rubric #10 (non-text ≥3:1). Canon fix: a `separator`-tier hairline (`#3C3C43`@29% light) or a faint fill-tier surface step so the card edge is perceptible.
- **Toolbar action density (watch-item, not a fail).** The reader toolbar carries ~10 borderless actions across 3–4 clusters — above HIG's "≤3 groups" guidance, though borderless/monochrome and legitimately reader-heavy (transcribe, import, redo, language, copy, star, share, export, search). Not a defect (pro-tool toolbars exceed), but the trailing 5-glyph run (copy/star/share/export/search) blurs into one undifferentiated cluster; grouping or a `⋯` overflow would sharpen scent.
- **Near-clone identity (taste note, not an anti-pattern).** The shell is Apple Notes/Mail so faithfully that the app has almost no visual identity of its own beyond the icon and cover — "competent but anonymous" on the originality axis. For a utility this is a defensible choice (familiarity > distinctiveness), recorded honestly rather than as a flaw.
- **Evidence poverty:** one surface, one state, light only, from a marketing render — settings, empty state, onboarding, recording/in-progress state, dark mode, and strict 8pt-grid verification are all unseen.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window — three-pane reader (light composite) | 12/14 | #10 UI contrast — content-card hairline borders `~1.05:1`, below 3:1 (near-invisible). Passes: #1 spacing reads on-grid at px≈pt · #2 three clean alignment axes across panes · #3 proximity (metadata tight under title, section gaps larger) · #4 ~5 sizes (22/15/13/12/11) geometric-ish · #5 title tight / body ~1.5 · #6 reader measure ~45–55 chars · #7 strong de-emphasis (secondary grays for counts/preview/metadata) · #8 action singularity (accent only on selection, no competing filled CTAs) · #9 primary text 85%-black ≥4.5:1 · #11 pointer targets fine (desktop calibration). N/A→pass: #12/#13 (no visible inputs/form labels) · #14 (no focus state in a still) |
| — native-tells audit | 10/10 | Passes: #1 AppKit/SwiftUI-native body · #2 glass only on chrome, content cards opaque, no glass-on-glass · #3 selection grammar (sidebar inset-rounded gray inactive + list solid-accent house style) · #4 sentence-case sidebar/section headers ("Saved on this Mac", "Today") · #5 13pt-class density, ~40pt Large rows, desktop heights · #6 accent bound consistently to system blue (selection + language pill) · #7 one prominent region per view, borderless toolbar (no competing primaries) · #8 concentric radii (cards ≤ window; selection 8 steps down) · #9 borderless monochrome SF-Symbol toolbar (dense but grouped — watch-item, not fail) · #10 genuine coloured traffic lights + sidebar toggle, no faked frame |
