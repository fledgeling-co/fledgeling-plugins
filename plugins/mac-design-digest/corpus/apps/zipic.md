# Zipic — profile

- **Source:** macapp.supply (cover composite only — no standalone gallery shots supplied) · **Surfaces digested:** batch-results main window (light), Pro settings pane (light) · **Last updated:** 2026-07-19
- **One-sentence identity:** A CleanShot-adjacent consumer image compressor that turns each batch result into a "savings receipt" card — big blue ↓% badge, green success check, before→after byte counts — wrapped in modern System-Settings rounded-card chrome.
- **Cluster:** unassigned (candidate: rounded-card consumer utility — with Compressor, Compresto, Picmal, HiPixel)
- **Lineage:** native (SwiftUI/AppKit), confidence **med** — native evidence is strong but read off a rotated, downscaled marketing composite, not a clean screenshot
- **Era (chrome):** big-sur → sequoia (rounded grouped cards, SF Symbols, flat opaque chrome, system Blue accent) — **no Liquid Glass lensing evidence present**; chrome is opaque light, no scroll-edge effect visible

## Provenance caveat
All geometry below is `(estimated)` with wide ranges and **low geometric confidence**: the only evidence is the cover.png marketing composite, where both app windows are shown at a ~5° rotation with slight perspective and at reduced scale. Hues are reliable (rotation does not affect colour sampling); pixel distances are not. No standalone @1x/@2x screenshot exists in the source set.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| accent/primary (blue) | `#0080F8` (measured, hue-reliable)(confirmed) | scanned dominant saturated blue | ≈ system Blue (kit Light #0088FF); used for ↓% badge, format badge, checkbox, switch, tab selection |
| status/success (green) | `#30C840` (measured, hue-reliable)(confirmed) | scanned | ≈ system Green (kit #34C759); **always paired with a checkmark glyph** — correct status grammar |
| bg/canvas (main) | ~#ECECEE–#F2F2F4 light gray (estimated)(inferred) | | window content behind the row cards |
| surface/row-card | #FFFFFF, radius ~14–18px (estimated)(inferred) | | each result is its own floating white rounded card |
| bg/window (settings) | ~#E8E8EA light gray (estimated)(inferred) | | grouped-card settings background |
| surface/settings-card | #FFFFFF, radius ~10–12px (estimated)(confirmed) | | one setting per card |
| type/filename | bold ~14–15pt, near-black (estimated)(inferred) | | reads Headline/Title3-bold; primary row anchor |
| type/secondary | ~11–12pt, gray (estimated)(confirmed) | | before→after sizes; settings sub-labels |
| type/group-header (settings) | bold ~13pt, Title Case, + leading SF Symbol (estimated)(confirmed) | | e.g. "Notification Style", "Copy Action" |
| badge/reduction | filled blue capsule, white text, down-arrow + "NN%" (estimated)(confirmed) | | the signature element |
| badge/format | filled blue capsule "→ jpeg" (estimated)(inferred) | | conversion indicator, inline before filename |
| control/remove | solid dark circle (~#3A3A3C) + white minus, ~22–24px (estimated)(inferred) | | trailing destructive per-row control |
| control/row-glyphs | monochrome light-gray SF Symbols (folder / copy / undo) (estimated)(inferred) | | **contrast risk — see Defects** |
| chrome/left-rail (main) | icon-only vertical toolbar, ~44–52px wide, borderless monochrome SF Symbols (estimated)(inferred) | | add-file, archive, sort near top; info "i" + sliders near bottom |
| chrome/tab-bar (settings) | native preferences toolbar: 4 items icon-over-label (General/Compression/Pro/License), selected = rounded fill + accent icon+label (estimated)(confirmed) | | classic macOS Settings tab pattern |

## Layout skeletons

**Main window — batch results list (light).** Genuine traffic lights top-left; no title text in the bar. A narrow left **icon-only vertical rail** (borderless monochrome SF Symbols: add-document, archive, sort at top; info + adjustments pinned bottom) — a toolbar rendered as a side rail, not a source-list sidebar (no labels, no selection). Content area = a vertical stack of **full-width white rounded row-cards** on a light-gray canvas, generous inter-card gap. Each row-card, left→right: square rounded thumbnail (~56–64px) · bold filename (truncated middle) · green success check · [optional blue "→ format" capsule] · then a second line: blue "↓ NN%" reduction capsule + "orig-size → new-size" in secondary gray · trailing cluster of right-aligned actions (folder, copy, undo, solid-dark remove circle). Rows are noticeably taller/airier than a native compact table row.

**Settings — Pro pane (light).** Centered titlebar title "Pro" (reflects selected tab); traffic-light **minimize/zoom greyed/disabled** (correct settings-window tell), red live. Native preferences **tab bar** (icon-over-label ×4, "Pro" selected with rounded selection fill + accent). Below: a scroll of **one-setting-per-card** groups, each card = leading SF Symbol + bold Title-Case header + its control: segmented control (Normal/Notch/System), checkbox rows (Hide in Dock, Auto-Copy, Run in background, Preserve Metadata), a path-field + native switch (Auto-Compression, with "+" and info affordances in the header), and a second segmented control (LZW/ZIP). A dark-mode + Chinese-localized settings window sits occluded behind — dark mode and localization exist but are not measurable here.

## Signature moves
- **[GOLDEN-NUGGET] The compression result as a "savings receipt."** Filename + green check + a filled-blue **↓NN%** badge + literal before→after byte counts converts a dull batch job into a per-file scorecard. The blue percentage capsule is the whole personality of the app — it makes saved bytes feel earned. Reinforced by an inline "→ jpeg" format-conversion badge in the same blue capsule language.
- **[GOLDEN-NUGGET] Settings as labelled cards.** One setting per rounded white card, each with its own icon + bold header — more spacious and friendlier than stock System Settings (which packs many rows per card). Reads as consumer-warm without leaving native control vocabulary.
- **Toolbar-as-side-rail.** The primary actions live in a thin left vertical icon rail rather than a top toolbar — an uncommon but coherent placement for a single-view utility.

## Defects
- **Contrast Dilution (affordances)** → the trailing per-row action glyphs (folder / copy / undo) render as light-gray monochrome SF Symbols on white, estimated <3:1; the interactive affordances recede while the informational blue badge dominates. Canon: non-text UI ≥3:1 — darken idle glyphs or reveal on row-hover.
- **Target-size risk (est)** → those same trailing glyphs read ~18–22px; below the 24px WCAG floor unless padded with invisible hit area. Unverifiable under composite rotation — flag, not confirmed.
- **Row-card list vs native flat list (deviation, not defect)** → content rows are individually floating white cards on gray rather than a flat inset `NSTableView`; defensible as System-Settings-adjacent house style, but it is the app's biggest departure from native content-list grammar. Recorded as signature-leaning.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (batch results, light) | 12/14 | #10 idle action glyphs light-gray on white (<3:1 est); #11 trailing icons ~18–22px, below 24px floor (est) |
| settings — Pro pane (light) | 13/14 | #9 some checkbox sub-labels mid-gray on white, contrast borderline (est) |

## Native-tells audit
| Surface | Score | Notes |
|---|---|---|
| main window | 8/10 | native controls + real chrome + consistent system-Blue/Green accent; deviations: airy card-list rows heavier than native compact rows (#5), no native inset-selection grammar shown (#3 n/a) |
| settings — Pro pane | 9/10 | native pref tab bar, native segmented/checkbox/switch, disabled-greyed minimize/zoom (correct), Title-Case headers, opaque content; one-setting-per-card is spacious house style (mild #5) |
