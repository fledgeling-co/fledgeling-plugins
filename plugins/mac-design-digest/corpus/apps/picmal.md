# Picmal — profile

- **Source:** macapp.supply (meta.json + cover.png + icon.png) · **Surfaces digested:** 1 — main window / batch-conversion queue, light (embedded in the marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** Permute's batch-media-converter job as a textbook AppKit data table — a zebra-striped `NSTableView` where every row's target format is a live pop-up button — whose only personality is one hardcoded royal-blue (#1B5BFF) borrowed from its fluid-marble icon; competent, native, and almost anonymous.
- **Cluster:** unassigned (proposed hint: *electric-accent native utility (light)*) — sole candidate member; needs ≥2 more apps to open a cluster.
- **Lineage:** **native — AppKit (high confidence).** The body, not just the frame, reads Mac: a real column-header `NSTableView` (Name / From / To / Size / Saving / Status / Fi… with 1px vertical header separators), zebra row striping, genuine pop-up buttons (double up/down chevron in an accent-filled well), square checkboxes, compact 13pt-class density, borderless titlebar segmented control, real coloured traffic lights. None of the Catalyst/iOS tells (inset-grouped cards, `UISwitch` pills, ~17pt density, per-row chevrons) are present.
- **Era (chrome):** **big-sur-class legacy-native (pre-Tahoe), no Liquid Glass.** Controls are rounded-rects (~6pt), not capsules; the pop-up buttons wear the classic Big-Sur blue-gradient chevron *well* rather than the flat macOS-27 capsule; the filled "Convert" primary is a ~6pt rounded-rect, not a capsule; the table header meets the titlebar on a hard opaque divider with no scroll-edge fade. This is a 2020–2024-idiom native app, not a macOS-26/27 glass rebuild. (Absence of glass is legitimate for a pro/utility table, but the *rounded-rect-not-capsule* control shapes date it specifically.)

## What was actually supplied (honesty note)

**No standalone screenshots** — `meta.json` ships an empty `gallery`/`shots`. The only UI evidence is the app window composited into the 2400×1260 marketing **cover**. Two things must not be conflated:

- **Brand evidence (the composite around the window):** near-white ground (#F9FAFB), a heavy black grotesque headline "All-in-one media converter for Mac" (SF-Pro-Display-Black class, left-aligned), two hard royal-blue (#1B5BFF) diagonal shard shapes bleeding off the top-right and bottom, and a "Picmal" wordmark + icon lockup bottom-left. This is a **Swiss/International** marketing composite — bold grotesk, near-white/near-black, one blue, hard geometry. Recorded here as brand context; it is *not* app-UI taste.
- **Design evidence (the window itself):** the batch-conversion queue analysed below.

Caveats bounding every number: (1) the window is a **marketing render at an indeterminate scale** (not a captured retina screenshot), so pixel values are `(estimated)` and row/control heights are given as pt-*class* ranges, not measured pt; only the cover's 2400×1260 aspect is `(measured)`. (2) The window **bleeds off the right edge** — the final "Fi…" column (File / Finished?) and any trailing toolbar controls are cropped. (3) No row is shown selected and no focus ring is visible, so selection grammar and focus appearance are **unobserved**, not passed.

## Tokens

All values `(estimated)(inferred)` unless noted — one marketing exposure, single surface, light mode only.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window-content | #FFFFFF | (estimated)(inferred) | table content rows (odd), light mode |
| bg/zebra-stripe | ~#F4F5F5 (≈4% gray) | (estimated)(inferred) | alternating even rows — subtle `NSTableView` striping |
| bg/titlebar | ~#F6F7F8 | (estimated)(inferred) | one hair darker than content; standard |
| accent/brand-ui | ~#3670F6 → #3C81F6 royal-blue | (estimated)(inferred) | pop-up chevron wells + "Convert" primary fill |
| accent/brand-core | #1B5BFF | (measured)(inferred) | icon body + marketing diagonals; the identity hue |
| type/row-title | ~13pt-class SF Pro, primary near-black (~85% black) | (estimated)(inferred) | filenames e.g. "webp-test.webp" |
| type/col-header | ~11–12pt-class SF Pro, secondary gray, **title case** | (estimated)(inferred) | "Name / From / To / Size / Saving / Status" — not tracked-uppercase (good tell) |
| type/from-label | ~12pt-class, secondary gray ~#888 | (estimated)(inferred) | source-format tags (WEBP/TIFF/PDF/SVG) |
| type/status-label | ~12pt-class, secondary gray, "Waiting" | (estimated)(inferred) | see Defects — ~3.5:1 |
| control/popup-button | white fill, ~6pt rounded-rect, ~24pt-class tall (Rg), value-left + accent-blue double-chevron well right | (estimated)(inferred) | classic Big-Sur pop-up; double chevron = choose-a-value (correct semantics) |
| control/checkbox | square, ~14–16pt, faint gray outline, unchecked | (estimated)(inferred) | leading row-select column |
| control/segmented | titlebar-centred 2-segment "Convert \| Compress"; selected = raised white segment in a gray track | (estimated)(inferred) | Big-Sur pill-in-track; used as top-level mode switch (see Defects) |
| button/primary | "Convert" — filled royal-blue, white label, ~6pt rounded-rect (NOT capsule) | (estimated)(inferred) | one prominent action, bottom-bar trailing |
| button/secondary | "Again" — refresh glyph + label, borderless/quiet | (estimated)(inferred) | correctly demoted vs primary |
| icon/row-status | monochrome gray ⓘ (info) and ⊖ (minus-circle) per-row glyphs; trailing share/export ↗ glyph | (estimated)(inferred) | status paired with glyph, no lone-colour signalling |
| row/height | ~28pt-class (single-line, padded) | (estimated)(inferred) | compact desktop density, not touch |
| divider/header-sep | 1px light vertical column separators + 1px bottom-bar rule | (estimated)(inferred) | hairline; <3:1 |
| cover/aspect | 2400×1260 (≈1.9:1) | (measured)(inferred) | marketing composite; window occupies right ~58% |

## Layout skeletons

**Main window — batch-conversion queue (light).** Single-pane document window, **no sidebar**. Top to bottom:

- *Titlebar:* leading coloured traffic-light cluster; a centred 2-segment control **Convert | Compress** as the app's mode switch (Convert active). No visible trailing toolbar group (cropped).
- *Table header row:* column titles on shared vertical axes — `[checkbox col] Name · From · To · Size · Saving · Status · Fi…` — secondary-gray, title-case, separated by 1px vertical hairlines. `From/To/Size/Saving/Status` are the conversion ledger.
- *Table body:* ~20 zebra-striped single-line rows. Row anatomy, left→right on the header axes: `[☐ checkbox] [filename primary-black (+ optional ⓘ/⊖ status glyph)] [FROM format, gray] [TO pop-up button — value + accent-blue chevron well] [Size "–"] [Saving "–"] [Status "Waiting" gray] [↗ share glyph]`. The `"–"` placeholders in Size/Saving read as quaternary/tertiary until a job runs.
- *Bottom bar* (separated by a 1px rule): leading `⊕` add-glyph + secondary text "20 images ready. Drag more images to add them."; trailing `[↻ Again]` (quiet) + `[Convert]` (filled royal-blue primary), anchored to the bottom-right corner.

## Signature moves

- **[GOLDEN-NUGGET] The table cell *is* the control — per-row format pop-ups.** Every row's "To" cell is a live pop-up button, so the whole `NSTableView` doubles as a bulk-configuration surface: you don't open a dialog per file, you set 20 target formats inline like editing a spreadsheet. It turns "batch convert" from a modal wizard into a scannable, directly-manipulable ledger (Name → From → **To**), with a single terminal "Convert". This is the app's one genuinely considered interaction decision.
- **[GOLDEN-NUGGET / boundary] One hardcoded royal-blue carries the entire identity.** #1B5BFF (icon marble + marketing shards) reappears as the UI accent (~#3670F6) on every chevron well and the Convert primary — deliberately *not* the macOS-27 system blue (#0088FF) and not bound to the user's `controlAccentColor`. Against an otherwise strictly-neutral white/gray table, that blue is the only personality in the room; it ties window → icon → marketing into one recognisable hue. A committed brand choice — and, on the native ledger, a tell (see Defects).
- **Verdict:** competent-but-almost-anonymous. Strip the blue and this is the default AppKit table an Xcode template would hand you. The signature is the *inline-pop-up ledger pattern* plus the *one-hue commitment*; there is no depth system, no custom type, no spatial flourish.

## Defects

- **Contrast Dilution (#9)** → secondary metadata (From tags, "Waiting" status) sample ~#888 on #FFF ≈ **3.5:1**, below the 4.5:1 AA floor for normal text. De-emphasis pushed one step too far — the ledger columns you actually read (source format, job status) are the quietest text on screen. *Correction:* darken secondary to ~#6E6E6E (≈4.6:1) or bump weight; keep the "–" placeholders quaternary.
- **Non-system accent binding** (native tell #6) → the brand royal-blue overrides `controlAccentColor` on the pop-up wells and primary. Internally consistent (a real house style), so it sits on the defect/signature boundary — recorded as a **tell + correction**, never learned as canon. *Native correction:* bind the Convert primary + pop-up wells to the system accent; keep #1B5BFF for the app's own iconography/marketing.
- **Accent repetition across the field (minor)** → ~20 accent-blue chevron wells stipple the table with the identity hue, thinning the Von-Restorff pop of the single Convert CTA. Not Focal Collision (the wells aren't filled competing CTAs), but the one saturated moment would land harder if the wells were quieter (system-tinted or neutral). *Correction:* neutral/secondary chevron wells; reserve saturated blue for the one primary.
- **Segmented control as top-level mode nav (borderline, native tell #7)** → Convert | Compress in the titlebar switches the app's two primary modes; the rule reserves segmented controls for *in-view scope*, not main navigation. Mitigated because the two modes are two views of one file-queue workflow (a very common macOS titlebar-accessory pattern), so this is a soft note, not a hard flaw.
- **Faint UI borders (#10, marginal)** → checkbox outlines and 1px header/column hairlines read <3:1 on white `(estimated)`. Borderline; standard-issue for AppKit tables.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window / batch-conversion queue (light) | 12/14 | **#9** secondary-text contrast ~3.5:1 (From/Status labels, estimated). **#10** marginal — faint checkbox/hairline borders <3:1 (estimated). **#14** focus appearance **unobserved** (no focused control in the render) — not counted as fail. Pass: grid/column alignment, Gestalt proximity, modular scale (≤3 sizes), de-emphasis hierarchy, action singularity (one filled primary), desktop control sizing, pop-up height (~24pt Rg). |
| — native-tells audit | 8/10 | **#6** non-system accent (brand royal-blue overrides system accent). **#3** selection grammar **unobserved** (no row selected) — n/a, not a fail. Pass: #1 AppKit-native lineage, #2 flat opaque content / no glass misuse, #4 title-case system-font column headers (no tracked caps), #5 13pt-class density + ~24/28pt controls, #7 one prominent action + correct primary/secondary grammar, #8 consistent ~6pt radii, #9 minimal borderless chrome (single primary lives in bottom bar), #10 genuine coloured traffic lights = focused window. |

## Aesthetic (design-craft vocabulary)

- **Adjectives (committed):** utilitarian · crisp · brand-bright.
- **Direction:** **Neo-grotesque product**, applied natively — light neutral ramp (white/#F4F5F5/#F6F7F8) + **one electric accent** (royal-blue). Not the warm-editorial default; a disciplined single-accent-on-neutral utility look. The *marketing* skin is a separate Swiss/International composite (heavy grotesk, near-white/near-black, hard blue diagonals).
- **Peers:** Permute / Handbrake / ImageOptim (media-converter function peers); accent-cousin to any neutral-native utility that spends its whole colour budget on one saturated action.
- **Audience:** consumer-utility / prosumer (drag-a-batch, set formats, convert) — not a deep pro tool.

## Psychology laws in play

- **Jakob's Law (exploited):** the spreadsheet-table + traffic-light chrome is instantly legible — users arrive already knowing how a column-header list of files behaves.
- **Von Restorff / signal-detection (exploited, then partly spent):** the single filled royal-blue Convert against a neutral field is the one thing the eye finds — but the ~20 blue chevron wells dilute that pop (see Defects).
- **Hick's Law / Tesler's Law (well-absorbed):** irreducible per-file complexity ("what should *this* become?") is compressed into one pop-up per row; the system infers "From", the user only picks "To", and one terminal button commits the batch.
- **Fitts's Law (exploited):** the Convert primary is large and pinned to the bottom-right corner — an effectively oversized target at a screen corner.
- **Processing fluency (mild friction):** the low-contrast secondary metadata (the columns you scan to verify a job) works against the very fluency the clean table sets up.

## Knowledge gap this app leaves open

One surface, one mode, light only, from a marketing render. To place Picmal properly the corpus needs: a **captured retina screenshot** (to promote every `(estimated)` token toward measured, and to confirm the ~6pt-not-capsule era read), the **Compress mode** and any **settings/format-options** surface (its form grammar is the untested lineage check), **dark mode**, and a **row-selected / focused** state (selection grammar and focus appearance are currently unobserved, not passed). Lineage is confidently native-AppKit; era is confidently pre-Tahoe. The open question is whether the app has any design system beyond "default table + one blue" — nothing seen so far suggests it does.
