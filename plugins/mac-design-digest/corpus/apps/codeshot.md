# Codeshot — profile

- **Source:** macapp.supply (cover composite only; no in-app gallery shots supplied) · **Surfaces digested:** main window (3-pane: source-list sidebar / theme content-list / export canvas), light mode · **Last updated:** 2026-07-19
- **One-sentence identity:** ray.so / Carbon's "code → pretty PNG" job done as an honest three-pane AppKit utility — a CodeSnap-class tool wearing a stock Big Sur source-list frame; competent and platform-faithful, its only real character the swatch-row theme browser and the full-bleed orange export stage.
- **Cluster:** system-default-utility (suggested — a consumer dev utility that leans on stock AppKit chrome with near-zero custom styling)
- **Lineage:** native (AppKit / macOS-correct SwiftUI) — **high** confidence. Non-native evidence never feeds macOS canon; here there is none to exclude.
- **Era (chrome):** legacy-native (pre-Tahoe), Big Sur–Sequoia — **med-high**. Flat opaque light-gray sidebar, bezeled (non-capsule) pop-up, no Liquid Glass lensing, no scroll-edge effect, flat gray content selection band. No glass evidence anywhere → not Tahoe.

## Evidence & provenance caveat

Single input is the **marketing cover** (1680×900). Left half is a brand/marketing panel (wordmark, headline, feature list) — analysed but recorded as **brand evidence, not app-UI evidence**. Right half is the design evidence: the app window on a Big Sur gradient backdrop (the backdrop is marketing/desktop, not app chrome). The window is rendered at roughly @1x and **cropped on the right and bottom**, so all pixel metrics are `(estimated)` with wide ranges; colours are clean `(measured)`. No settings, empty-state, dark-mode, or onboarding surface supplied.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| chrome/sidebar-bg | `#E9E9EA` (measured)(inferred) | | flat opaque source list, light mode — no visible vibrancy/glass |
| chrome/content-bg | `#FFFFFF` (measured)(inferred) | | theme-list column background |
| chrome/titlebar-bg | `#E9E9EA` over sidebar (measured)(inferred) | | minimal titlebar; pop-up sits as a titlebar accessory, no real toolbar |
| text/sidebar-header | `#79797A` secondary gray, **sentence case** (measured)(inferred) | | "Editor" — system font, NOT tracked uppercase (native tell PASS) |
| text/label-primary | near `#000000` (measured)(inferred) | | theme names + sidebar row labels |
| selection/sidebar | subtle **inset rounded** fill (light gray/blue), label near-black (estimated)(inferred) | | "Themes" row — correct native inset-rounded grammar |
| selection/content-band | `#DCDCDD` **flat full-width band** (~8% black) (measured)(inferred) | | "Railscasts" selected row — colour-only, ~1.1:1, NOT accent-tinted — see Defects |
| control/popup | compact bezeled pop-up, ~20–22pt tall, double up/down chevrons (estimated)(inferred) | | "swift" language picker; pick-a-value grammar correct |
| row/theme | ~44–56px as-rendered (name row + swatch row); reads as generous list rows (estimated)(inferred) | | scale-limited; two-line item = label + 5-chip palette |
| radius/window | ~10–12pt (estimated)(inferred) | | kit ships no window radius; measured per-app |
| radius/code-card | ~10pt (estimated)(inferred) | | the rendered snapshot card (content, theme-dependent — not app chrome) |
| type/body | ~13px SF Pro-class (estimated)(inferred) | | theme names / labels; desktop density |
| canvas/export-bg | `#FF4406` vivid orange (measured)(inferred) | | **user-chosen export background**, NOT app chrome — a demo value |
| codecard/bg | `#222323` warm near-black (measured)(inferred) | | exported snapshot card = the *content*/theme output, not app chrome |
| — brand/panel-bg | `#F7F6FB` cool off-white (measured) | | **BRAND** (marketing panel), not app UI |
| — brand/headline | heavy geometric grotesk (SF Pro Display Black / Inter-class), two-tone: key words `#000`, connectors `~#888` (measured) | | **BRAND**; monochrome black feature-icon list |

## Layout skeletons

**Main window (3-pane split view).**
- **Zone A — source-list sidebar** (leading, ~140–150px as-rendered): section header "Editor" (secondary, sentence case) → 3 rows with leading multicolor glyphs + labels: Themes (selected, inset-rounded fill) · Window · Sizes. Navigation only — correct sidebar usage.
- **Zone B — theme content-list** (middle column, white): a vertically-scrolling single-column list. Each item = theme name (primary label) stacked above a **row of 5 circular color chips** previewing that theme's palette. Selected item ("Railscasts") gets a flat gray full-width band. This is the app's core browse surface.
- **Zone C — export canvas** (trailing, fills remaining ~half the window): a **full-bleed saturated color field** (#FF4406 in this render) acting as the preview stage; a **dashed rounded-rect crop guide** frames the padding; the **rendered code card** (dark, own decorative traffic lights, soft drop shadow, syntax-highlighted Swift) sits inside.
- **Titlebar accessory:** a centered pop-up ("swift") over Zone B/C — the language selector. Genuine colored traffic lights top-left (focused window).

## Signature moves
- **[GOLDEN-NUGGET] Swatch-row theme browser.** Rather than rendering 80+ full code thumbnails, each theme is previewed as *name + five circular color chips*. Systematic across the whole list, purposeful (lets you scan themes by color signature, not by reading names or parsing previews — a Hick's-Law reduction at the one real decision point), and cheap to render. This is the app's most distinctive, defensible design decision.
- **Full-bleed color canvas as export stage.** The "background/padding" setting is promoted to the dominant visual: ~half the window is a single saturated field with a dashed crop guide, making the rendered snapshot the unambiguous focal object (Von Restorff — the one loud thing is the output). More a demo value than committed brand, but the *decision to stage the output on a full color field* is real character.

## Defects
- **Faint colour-only selection (Contrast Dilution).** Theme-list selected row = `#DCDCDD` band on `#FFFFFF` ≈ **1.1:1**, communicated by colour alone (no accent tint, no checkmark, no focus glyph). Fails native selection grammar (macos-native-analysis §3.1) and the 14-pt UI-contrast check (#10). Canon fix: an **inset rounded accent-tinted fill with accent-coloured text**, or — since this is a "list options" table — a persistent **checkmark** on the active theme.
- **Accent not bound.** Selection/focus use gray, not `controlAccentColor`; the app never binds the system accent. (The multicolor theme chips are legitimate *identity* colours, correctly separate.) Canon: bind selection + focus ring + any one primary action to the user's accent.
- **Internal selection inconsistency.** The sidebar uses the correct **inset rounded** selection while the content list uses a **full-width flat band** — two different selection grammars in one window. Canon: unify on the inset rounded flat-fill grammar shared by sidebar and content list.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window (light) | 13/14 | #10 UI contrast — theme-list selection band ~1.1:1, colour-only. (#14 focus appearance unverifiable from a static shot — no focused field; not scored. #6 measure n/a — no prose.) |

### Native-tells audit (main window)
8/10 — **fails:** #3 selection grammar (content list = flat gray full-width band, not inset rounded accent fill) · #6 accent binding (selection uses gray, not the system accent). Passes: #1 native lineage · #2 no glass misuse (legacy flat chrome, content opaque — legitimate) · #4 sidebar header sentence-case system font · #5 desktop density · #7 pop-up pick-a-value grammar correct · #8 concentric corners (estimated) · #9 minimal chrome / borderless · #10 genuine traffic lights, focused.
