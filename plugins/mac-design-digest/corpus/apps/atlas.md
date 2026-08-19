# Atlas — profile

- **Source:** macapp.supply (cover.png marketing composite + icon.jpg) · **Surfaces digested:** main window / library ("Infinity" canvas mode), light · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple Photos' centered-title calm, stripped of all chrome and colour, turned into a designer's inspiration board — an Eagle/Pixave/Cosmos-class curator where the app furniture dissolves into four floating Liquid Glass islands so the user's imagery is the entire surface.
- **Cluster:** unassigned → proposed `quiet-gallery` (content-forward curator, creative audience) — sole member so far
- **Lineage:** native (high) — 13pt-class tracked SF Pro title, real coloured traffic-light cluster, floating glass toolbar islands with scroll-under-content behaviour, monochrome SF Symbols. No web/Catalyst tells (no 16px body, no kebab menus, no inset-grouped cards, no pointer-hand). Non-native evidence: none.
- **Era (chrome):** Liquid Glass native (macOS 26/Tahoe) — floating glass capsules over edge-to-edge content, capsule bezels, dark-glass segmented control, no opaque toolbar bar-line.

## Evidence caveat
Single image, and it is a **marketing composite**: the app window is staged on a light-gray backdrop (`#E2E4E6` est — brand, not app) with generous margin. The window interior is the design evidence; the backdrop is brand. No `shot-*` files were provided, so only one surface and one view-mode ("Infinity" freeform canvas) are witnessed — the disciplined Grid mode's spacing is unseen. Measurements are `(estimated)` from a retina composite; the freeform canvas is by-design non-gridded, so spatial-grid checks are largely not assessable here. The asterisk/sparkle icon is recorded as brand evidence only (Workflow A = UI only; no icon digest written).

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | `#FFFFFF` (near-white) | (estimated)(inferred) | window content is pure gallery ground; no tint |
| bg/backdrop | `#E2E4E6` | (estimated)(inferred) | marketing composite backdrop — **brand, not app** |
| type/title | "HELLO, ATLAS" ~13pt SF Pro Semibold, tracked caps (~+0.05–0.07em), label primary `#000`@85% | (estimated)(inferred) | Photos-style centered window title; personable "HELLO," not a functional name |
| type/subtitle | "869 ITEMS" ~10–11pt SF Pro, tracked caps, secondary gray ~`#8E8E93` | (estimated)(inferred) | item-count line under title; de-emphasised correctly (smaller + gray) — but see Defects |
| chrome/traffic-lights | standard 3-dot cluster (~68×14pt) inside a **white glass capsule** | (estimated)(inferred) | coloured = focused window; floats over content, not on a titlebar |
| chrome/sidebar-toggle | ~28pt white glass rounded-square button, light-gray sidebar SF Symbol | (estimated)(inferred) | separate glass island beside the traffic-light capsule (container morphing: two groups, one continuous edge each) |
| control/view-switcher | dark graphite glass **capsule** segmented control, ~44–52pt tall; segments Grid / Canvas / Infinity; selected = raised white capsule + black semibold label | (estimated)(inferred) | floating bottom-center; native segmented selection grammar (white capsule), not a full-bleed bar |
| control/import | ~44pt white circular glass button, gray tray-with-down-arrow SF Symbol | (estimated)(inferred) | floating bottom-right; single trailing action |
| radius/item | ~6–8pt on thumbnails | (estimated)(inferred) | opaque content items with soft shadow |
| radius/glass | capsule (h/2) on pills; ~10pt on the sidebar-toggle square | (estimated)(inferred) | concentric, steps down correctly |
| shadow/item | soft, low-opacity, ~y+4 / blur ~16 | (estimated)(inferred) | content-layer depth (never glass) — clean glass discipline |
| accent/primary | **none / neutral** — deliberately withheld | (inferred) | selection + emphasis rendered in white/graphite, not system blue; 100% of colour ceded to user content |

## Layout skeletons

**Main window — library, "Infinity" canvas mode (light):**
- Chromeless shell: no toolbar row, no visible sidebar (collapsed), no window border-line. Content is edge-to-edge on a white ground.
- Four floating Liquid Glass islands are the entire UI:
  - top-left: `[traffic-light glass capsule] [sidebar-toggle glass square]`
  - top-center: `HELLO, ATLAS` / `869 ITEMS` (centered title + count, over content, no bar)
  - bottom-center: `Grid · Canvas · [Infinity]` dark-glass segmented switcher
  - bottom-right: circular white-glass import button
- Content plane: inspiration items (video stills, UI screenshots, type specimens, stamps, dashboards) placed with generous, uneven whitespace — a freeform spatial canvas ("Infinity"), not a snapped grid. Items are opaque, small-radius, soft-shadowed.

## Signature moves
- **[GOLDEN-NUGGET] Chromeless content-first shell.** All app furniture is dissolved into four floating Liquid Glass islands over edge-to-edge imagery — no toolbar bar, no chrome frame, sidebar collapsed by default. The app disappears; the collection *is* the interface. Systematic and purposeful (a curator's board), and it honours the Liquid Glass Golden Rule cleanly (glass only on the four floating islands; every content item opaque with its own shadow).
- **[GOLDEN-NUGGET] Zero-accent UI.** The chrome contributes essentially no colour — selection/emphasis is neutral white-on-graphite, not the system accent. The entire colour budget is ceded to user content, so every thumbnail becomes the figure against a silent frame (Von Restorff by subtraction). Restrained colour strategy taken to its limit.
- **Floating dark-glass view-mode switcher** (Grid / Canvas / Infinity) bottom-center — spatial browsing modes are the app's core identity; "Infinity" (freeform canvas) is the marketed hero mode.
- **Personable centered title** ("HELLO, ATLAS" over "869 ITEMS") — Photos-schema window title made warm, the only chrome typography in the app.

## Defects
- **Contrast Dilution (mild, aesthetic-invited).** The "869 ITEMS" subtitle (gray ~`#8E8E93` on white ≈ borderline ~3.5–4:1) and the sidebar-toggle glyph (light gray on white glass, plausibly <3:1) sit under the WCAG floors for small text / non-text. This is the specific risk a near-white zero-accent shell courts — canon would push the subtitle to ~`#000`@50% (secondary label) and darken the toolbar glyph to a secondary-label weight for the 3:1 non-text floor.
- **Alignment unassessable (not counted as a fault).** The witnessed "Infinity" mode places items freeform, so container-alignment / grid-adherence rules don't apply — but that also means the corpus has no evidence of the app's disciplined Grid mode. Bring a Grid-mode shot to close this.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (Infinity mode, light) | 11/14 | #2 no shared alignment axes (intentional — Infinity freeform, not a true fault), #9 "869 ITEMS" subtitle contrast borderline <4.5:1, #10 sidebar-toggle glyph contrast likely <3:1 |
| main window — native-tells audit | 9/10 | #4 n/a (sidebar collapsed, headers unseen); all others pass — clean glass discipline, real chrome, neutral-but-not-misbound accent |
