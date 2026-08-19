# Soulver — profile

- **Source:** macapp.supply (meta.json + marketing cover) · **Surfaces digested:** 1 marketing composite containing the **iPad** app UI (note-list + document/answer view) · **Last updated:** 2026-07-19
- **One-sentence identity:** A calculator that pretends to be Apple Notes — a plain-text notepad whose right margin is a live spreadsheet; peers Numi, Calca, PCalc, with Bear/Notes.app as the shell it borrows.
- **Cluster:** unassigned (contrast evidence — see Lineage; do not seed a macOS cluster from this)
- **Lineage:** **ios-on-mac / iPadOS** (med confidence the *shown surface* is iOS-derived; high confidence it is **not** the macOS build). The evidence is the iPad app, shown inside a marketing device frame — iOS status bar "4:40 PM Sun May 31", uniform black tablet bezel, no traffic lights, touch-density rows. Soulver 3 *does* ship a genuine AppKit-native Mac app, but **that surface was not supplied**; nothing here may feed macOS canon.
- **Era (chrome):** N/A on the macOS era axis (not a Mac window). On the iOS axis it reads current-flat (SF Pro, inset rounded selection, hairline separators, no skeuomorphism). Marked `unknown` for the corpus era field.

## Tokens

All values `(estimated)` — source is a downscaled WebP marketing composite with compression artefacts, not a clean @2x screenshot. Ranges over false precision.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/brand-backdrop | `#FCFAF6` warm cream | (estimated)(inferred) | Marketing panel only — **brand**, not app chrome |
| bg/doc-canvas | `#FFFFFF` | (estimated)(inferred) | The editable document column (light mode) |
| bg/answer-column | `#F3F3F3` (~4–5% gray) | (estimated)(inferred) | Faint tint separating the right-hand results sheet from the white canvas — the load-bearing surface token |
| bg/note-list | `#FAFAFA` | (estimated)(inferred) | Left navigation panel |
| fill/selection | `#DDDDDD` on `#FAFAFA` | (estimated)(inferred) | Inset rounded-rect selection fill, ~10–12pt radius, no accent tint — iOS grammar (a Mac would accent-tint text) |
| ink/primary | near-black (~`#1A1A1A`, sampled edges `#525152`) | (estimated)(inferred) | Note titles, results, doc heading |
| ink/secondary | mid-gray (~`#8E8E93`) | (estimated)(inferred) | Dates, "N lines" counts, "#" heading marker, plain connective words ("of", "in", "tax") |
| syntax/number | system blue ~`#0088FF` (sampled muted `#2986CB`) | (estimated)(inferred) | Numerals & percentages; matches kit System Blue `#0088FF` light |
| syntax/unit-keyword | magenta–purple ~`#CB30E0`/`#FF2D55` (sampled `#B965B3`) | (estimated)(inferred) | Units & keywords: "km", "miles", "weeks"; currency sign sometimes magenta |
| syntax/reference | blue underline | (estimated)(inferred) | Underlined tokens = cross-line references / links ("20% of $1,480", "3 weeks") |
| caret/insertion | system blue | (estimated)(inferred) | Blue text-insertion caret after "today" |
| type/app-body | ~17–19px SF Pro Regular (touch density) | (estimated)(inferred) | **iOS 17pt-class, not macOS 13pt** — a density tell |
| type/app-title | ~17px SF Pro Semibold | (estimated)(inferred) | Note titles, doc `#` heading |
| type/app-meta | ~13px SF Pro Regular, secondary | (estimated)(inferred) | Dates, line counts |
| type/brand-display | high-contrast transitional/modern serif, Bold, ~64–72px | (estimated)(inferred) | "Notepad, meet calculator." — **brand**; reads like Tiempos Headline / Freight Display class (unidentified) |
| type/brand-body | humanist sans (SF Pro), ~28px | (estimated)(inferred) | Subtitle + "Mac · iPad · iPhone · one-time purchase" caption |
| chrome/device-bezel | `#313131` | (estimated)(inferred) | iPad hardware frame in the render, not app UI |

## Layout skeletons

**iPad app — three-zone reading layout (portrait/near-square render):**
- **Left panel (note list + folders), ~35% width, `#FAFAFA`:** top iOS status bar; a trailing toolbar cluster of 4 borderless monochrome SF-Symbol icons (compose/new-note, book, gear/settings, sidebar-toggle). Below: note rows — bold title + gray date subtitle (tight ~2px pair) on the left, right-aligned gray "N lines" count on a shared trailing axis; selected row carries an inset rounded gray fill. A hairline separator floats the bottom folder group: "General" (selected, rounded fill, filled-folder glyph, trailing "New Folder" text action), then "Finance / Travel / Work" as outline-folder rows.
- **Centre column (document canvas), `#FFFFFF`:** markdown-ish `#`-prefixed heading (gray `#`, near-black title); then natural-language calculation lines, one per row, generously leaded (~1.5×+), with live per-token syntax coloring (numbers blue, units/keywords magenta, operators/connectives gray) and blue-underlined cross-references.
- **Right column (answer sheet), `#F3F3F3`:** right-aligned near-black results on a faintly tinted panel, each vertically aligned to its source line ("$296.00", "149.1 mi", "$1,437.50", "June 21"). The tint + right-alignment is the whole product metaphor: a text editor with a spreadsheet's answer margin.

**Marketing composite (brand evidence, separate from app):** left ~48% is a warm-cream brand panel — app icon top-left, black modern-serif display headline, humanist-sans subtitle, muted-gray platform/pricing caption. Right ~52% is the iPad device render. The backdrop is **warm-editorial**; the app inside is **cool-flat-utility** — a deliberate romanticising gap worth noting, not conflating.

## Signature moves

- **[GOLDEN-NUGGET] The answer-sheet column.** A live, right-aligned results margin on a ~5%-gray panel, each answer locked to its source line. This single layout decision *is* Soulver — "notepad, meet calculator" made literal. Transplantable to a Mac mock as a genuine pattern (opaque content column, not glass).
- **Semantic syntax coloring as hierarchy.** Numbers=blue, units/keywords=magenta, connectives=gray, results=black. Von Restorff at the token level: the operands you care about pop out of otherwise near-monochrome prose. Doubles as processing-fluency aid — you parse the maths without reading the sentence.
- **The Notes.app disguise (Jakob's Law).** The entire shell — note list with date subtitles + line counts, folder tree, compose toolbar — is deliberately conventional Apple-Notes, so the *novel* thing (calc-as-you-type) rides in on a fully-predicted interface.
- **Cross-line references as blue underlines.** Underlined tokens ("20% of $1,480", "3 weeks") signal live links between lines/variables — spreadsheet references wearing hyperlink clothing.

## Defects

- **Colored-token contrast (soft, semantic-softened).** System-blue `#0088FF` and the magenta keyword hue against `#FFFFFF` land near ~3:1 — under the 4.5:1 AA text floor. Mitigated because numerals also carry meaning by shape/position and results render near-black; still a low-vision finding, not a free pass. → Canon would darken the token hues on white or add weight.
- **Low-contrast selection.** Gray `#DDDDDD` fill on `#FAFAFA` note-list is a ~1.1:1 fill delta — legible on iOS but weak. → A Mac surface would use an accent-tinted inset selection with accent-colored label.
- No magic-number spacing, no focal collision, no line-length fatigue — spacing and de-emphasis are disciplined. This is a *considered restrained* design, not a template.

## Native-mac tells (why this must not feed canon)

Scored as if it were a Mac surface — it is not, so it "fails" by platform, which is the finding:
- Density is iOS 17pt-class touch, not macOS 13pt/24pt (#5 fail).
- iOS status bar + tablet bezel, no traffic lights, no menu-bar (#1, #10 fail).
- Selection is neutral gray inset, not accent-tinted (#3 partial); no system-accent binding — the blues are content syntax, not `controlAccentColor` (#6 fail).
- Toolbar is an iOS top-nav icon row, not a macOS unified toolbar (#9 partial).
Corrections for a Mac mock: 13pt body, 24–28pt rows, real toolbar + menu-bar parity, accent-tinted selection, opaque content columns (answer sheet stays opaque — never glass-in-content).

## Rubric history
| Surface | 14-pt | Native-mac (10) | Failures |
|---|---|---|---|
| iPad note+document view | 12/14 | ~3/10 (platform mismatch, not craft) | #9 colored-token contrast ~3:1 on white; #10 selection/separator fill contrast weak (<3:1). Native audit low **only** because it is an iPad surface. |
