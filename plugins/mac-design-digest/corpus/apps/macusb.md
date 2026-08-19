# macUSB — profile

- **Source:** macapp.supply (`sources/macusb/`) · **Surfaces digested:** launch/welcome (cover composite), download progress, source & target configuration (macOS + Windows variants), install-config modal, operation-details confirm, creation progress · **Last updated:** 2026-07-19
- **One-sentence identity:** Balena Etcher's big-friendly-button flasher wizard rebuilt as a native-chrome Mac window — Apple's Setup Assistant cadence wearing iOS-sized controls.
- **Cluster:** unassigned (candidate: *dark guided-utility wizard* — dark-neutral product surface with iOS-consumer control sizing)
- **Lineage:** native (SwiftUI) — **med** confidence; macOS-correct window chrome and a genuine double-chevron pop-up button, but the *body* is styled in an iOS-consumer idiom (oversized controls, full-width filled buttons, floating centred modal). The iOS-idiom styling is recorded below as tells + corrections, **not** learned as mac taste.
- **Era (chrome):** custom — flat opaque dark theme (Big Sur-era flat-fill + rounded cards), **not** Liquid Glass (no lensing, no scroll-edge effect) and **not** legacy-native (no hard 1px bezels/gradient controls). A committed custom dark palette.

All screenshots are dark mode, @2x (1100×1580 px raw → ~550×790pt logical). The window is a **fixed-size portrait wizard**: the zoom traffic light renders grey/disabled in every shot while red+yellow are live — a genuine AppKit fixed-window tell, and evidence for native lineage.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | ~`#0B0B0D` near-black (estimated)(confirmed) | | dark window ground; not pure #000 |
| bg/card | ~`#1C1C1E`–`#2A2A2C` elevated grey (estimated)(confirmed) | | requirement/summary cards, one tonal step up from ground |
| bg/card-active | ~`#1E2A44` navy translucent + blue 1px border (estimated)(confirmed) | | the in-progress step card (shot-1, shot-6) |
| bg/status-success | ~`#16301C` green tint (estimated)(inferred) | | "System successfully detected" card |
| bg/status-warning | ~`#3A2A15` amber/brown tint (estimated)(confirmed) | | "All files… permanently erased" card |
| accent/primary | ~`#0A84FF`–`#0088FF` system blue (estimated)(confirmed) | | buttons, links, active step, focus ring — reads bound to system blue; kit dark blue is `#0091FF` |
| status/green | ~`#30D158` (estimated)(confirmed) | | success glyph + text; matches kit Green dark `#30D158` |
| status/amber | ~`#FF9F0A` (estimated)(inferred) | | warning glyph + text |
| type/window-title | ~18pt SF Pro Bold, leading-aligned after traffic lights (estimated)(confirmed) | | native titlebar, but left-aligned not centred |
| type/card-title | ~17–18pt SF Pro Bold (estimated)(confirmed) | | "Requirements", "Process overview" (Title2-class) |
| type/body | ~15px SF Pro Regular (estimated)(confirmed) | | **larger than 13pt macOS body** — iOS-density tell |
| type/section-label | ~14pt, Label-secondary grey, **centred between hairline rules** (estimated)(confirmed) | | "File selection", "Download steps" — non-native header treatment |
| type/button | ~17pt SF Pro Semibold, white on blue (estimated)(confirmed) | | oversized |
| space/base | 8pt grid, generous ~20pt card padding (estimated)(confirmed) | | disciplined but loose |
| radius/window | ~16–18pt (estimated)(inferred) | | measured from fixed portrait window corner |
| radius/card | ~14–16pt (estimated)(confirmed) | | large rounded-rect cards |
| radius/button | capsule (measured)(confirmed) | | full-pill primary + Done |
| control/primary-btn | **full content-width × ~45pt tall, capsule**, white label + circle-badged directional glyph (measured)(confirmed) | | iOS bottom-CTA transplanted; kit XL control is 36pt |
| control/checkbox | ~26pt filled-blue rounded-square + white check (measured)(confirmed) | | iOS-scale; kit macOS checkbox is 14pt |
| control/pop-up | ~34pt tall, double up/down chevron (measured)(confirmed) | | genuine native pop-up button — pro-native tell |
| control/text-field | ~34pt tall, ~8pt radius, blue focus ring ~3pt (estimated)(confirmed) | | focus ring evidenced in shot-4 |
| chrome/bottom-bar | flat opaque, hairline top divider, houses the full-width primary + optional text button below (measured)(confirmed) | | no glass; opaque is legitimate |
| chrome/traffic-lights | ~30px raw dia (~15pt @2x); zoom disabled-grey (fixed window) (measured)(confirmed) | | native cluster, ~57pt span vs kit 68pt — slightly compact |

## Layout skeletons

**Wizard shell (all surfaces).** Fixed portrait window ~550×790pt. Native titlebar (traffic lights leading, bold title just right of them, no toolbar). Single scroll column of full-width rounded cards, ~30pt side margins. Sections separated by a **centred label flanked by two hairline rules**. A persistent flat opaque **bottom action bar** carries one full-width saturated-blue capsule primary; a secondary action (Back) sits *below it* as centred plain text.

**Download / creation progress (shot-1, shot-6).** Header summary card → centred "steps/stages" rule-label → vertical stack of equal step cards. Completed steps: green ✓ glyph + label. Active step: navy-tinted card, blue download glyph, bold label, right-aligned % , determinate progress bar, speed + size counters. Pending steps: dim glyph + label. Bottom bar: abort action (styled inconsistently — see Defects).

**Source & target config (shot-2 macOS / shot-3 Windows).** "File selection" rule-label → grey Requirements info card (info glyph + bullet list) → row of [text-field | Select (bordered) | Download (bordered) | **Analyze (filled blue)**] → green success-detection card + right-aligned "Calculate Checksum" text-link → "USB Drive Selection" rule-label → Hardware Requirements card → "Select target USB drive:" label + native pop-up → amber WARNING card → bottom **Continue** primary.

**Install-config modal (shot-4).** Background dims; a **centred floating rounded card** (not a top-anchored sheet) with sliders glyph + title, a hairline under the title, a column of ~26pt blue checkboxes (one disabled/dimmed, correctly kept visible), a labelled text field with blue focus ring + helper text, and a trailing blue capsule **Done**.

**Operation-details confirm (shot-5).** Two stacked summary rows (system + drive) in one card → "Creation process" rule-label → Process-overview bullet card → clock-glyph note card → bottom **Start** primary + **Back** text.

## Signature moves
- **[GOLDEN-NUGGET] The persistent full-width blue capsule action bar with a circle-badged directional glyph** ("Continue →", "Start →", "Cancel ⊗", "Stop ⊗"). It is the app's entire visual identity in one recurring element: iOS's bottom primary button transplanted onto a Mac window. Purposeful (unmissable next-step in a linear flow — strong information scent + a Fitts's-Law-huge target) and systematic across every screen — but a non-native idiom (native primaries are compact capsules, not window-width bars, and never carry circle-badged glyphs).
- **[GOLDEN-NUGGET] Tinted status-card semantics.** Every state owns a full tinted card + matching glyph + text: navy = in-progress, green = success, amber = destructive warning. The wizard reads like a traffic-light board, and crucially **colour is never the sole signal** — each tint is paired with a glyph and a label. This is the app's genuine accessibility strength.

## Defects
- **Focal Collision** → shot-2/3 show two saturated-blue filled primaries in one view ("Analyze" in the button row *and* "Continue" in the bottom bar). Canon: one prominent action per view; the completed row's Analyze should demote to bordered once analysis succeeds, or Continue should be the lone primary.
- **Inconsistent abort styling** → shot-1 makes "Cancel" a loud full-width saturated blue; shot-6 makes the equivalent "Stop" a quiet dark ghost. Same action class, two treatments. The quiet ghost (shot-6) is the correct one; the loud blue Cancel (shot-1) is the defect.
- **Focal weight on the wrong control** → in shot-1 the single loudest element on screen is *Cancel* (an abort). Abort/destructive actions should never be the prominent default.
- **Non-native section headers** → centred labels flanked by hairline rules, with mixed capitalization ("File selection" sentence-case vs "USB Drive Selection" title-case). Native section headers are left-aligned, system-font, sentence-case, no flanking rules.
- **iOS-density controls** (native-tell, not a defect per se) → ~45pt buttons, ~26pt checkboxes, ~34pt pop-ups and ~15px body on a pointer-first platform; kit body is 13pt and controls top out at 36pt (XL toolbar tier).
- **Floating centred modal** instead of a native sheet (shot-4) → native modality anchors a sheet to the window's top edge; this is an iOS/web centred dialog.

## Rubric history
| Surface | Rubric | Native-tells | Failures |
|---|---|---|---|
| download progress (shot-1) | 13/14 | 5/10 | #8 lone prominent action is the abort (Cancel); native: iOS density, non-native rule-labels, iOS idiom |
| source & target — macOS (shot-2) | 12/14 | 5/10 | #8 dual saturated primaries (Analyze + Continue); #6 bullet measure borderline; native: density, centred rule-labels |
| source & target — Windows (shot-3) | 12/14 | 5/10 | same as shot-2 (OS variant) |
| install-config modal (shot-4) | 13/14 | 4/10 | native: floating centred modal (not sheet), ~26pt iOS checkboxes, density |
| operation-details confirm (shot-5) | 13/14 | 6/10 | correct hierarchy (Start primary + Back text); native: density only |
| creation progress (shot-6) | 13/14 | 6/10 | correct quiet abort (Stop ghost); native: density, rule-labels |

## Brand context (not a Workflow-B icon digest)
- **App icon** (`icon.jpeg`, 1024²): a black USB flash-drive at ~45° on a light-grey radial-gradient rounded-square, with heavy embossed grey outlines and a skeuomorphic drop shadow. Reads as an **early-2010s iOS-era icon** — flat mono palette (black + greys), no rich scene, no Big Sur squircle grid or Liquid Glass layering. Competent silhouette (the USB stick reads at Dock size) but era-dated relative to macOS 27. Marked `source: mock/brand`, excluded from any canon.
- **Cover** (`cover.jpeg`, 1920×1080): marketing composite — aurora blue/green ray backdrop + heavy white "macUSB" wordmark and tagline "Download. Flash. Boot." The app *window* inside (a dark welcome screen: USB icon, wordmark, "Download. Flash. Boot. The all-in-one USB creator for Mac", one blue "Start →" capsule, "macUSB by Kruszoneq · Support the project!" footer) is design evidence; the backdrop/wordmark are brand-only.
