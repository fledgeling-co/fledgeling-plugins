# Raycast — profile

- **Source:** macapp.supply (marketing cover only — no gallery shots supplied) · **Surfaces digested:** command-palette "detail list" view (list + inspector), dark · **Last updated:** 2026-07-19
- **One-sentence identity:** Spotlight's ⌘K launcher grammar rebuilt as an extensible neutral stage — Alfred's utility with Linear's dark-neutral restraint, where the UI suppresses all colour so content carries it.
- **Cluster:** unassigned (candidate: graphite-command-palette / dark-neutral-pro-launcher)
- **Lineage:** native (med) — Raycast is a Swift/AppKit app [Inference from platform knowledge], corroborated in-image by genuine macOS `NSWorkspace` document icons in the list, SF Pro rendering, and native sentence-case gray section-header grammar; zero web tells (no pointer-hand, no tracked-uppercase headers, no kebab menus, no card grid, no 16px web body). BUT the surface is a fully custom-drawn HUD command-palette, so its tokens are Raycast house-style, not general macOS canon.
- **Era (chrome):** custom — dark near-black translucent floating panel (its own material language; predates/sidesteps Liquid Glass). No traffic lights, no title bar, no menu bar (legitimate for a HUD launcher panel).

## Provenance / evidence caveats

- Single image, and it is a **marketing composite**: black backdrop with red diagonal light streaks, the Raycast wordmark, and the headline "Your shortcut to everything." are **brand** evidence, not UI. The floating panel is the design evidence.
- The panel's **red glowing rim and the red tint bleeding into the panel interior are composite treatment**, not real app chrome — true interior background samples near-black `#090809` at the bottom where the backdrop is black; everywhere nearer the red streaks the interior reads reddish. This prevents a clean read of the panel's true material alpha (it may be a translucent vibrancy panel or an opaque dark surface — the composite red bleed is consistent with translucency but not proof of it → `(insufficient-evidence)`).
- **Retina scale is indeterminate** (marketing render, arbitrary scale). Panel measures ~1774px wide in-composite; if that is Raycast's ~750pt-class window the scale is ~2.37×. All pt conversions below carry this caveat and are `(estimated)`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel | `#090809`→`#0A0A0A` near-black | (measured)(inferred) | true interior sampled at panel bottom, clear of red composite glow |
| material/panel | dark translucent HUD (backdrop bleeds through) — alpha unrecoverable | (estimated)(inferred) | red bleed consistent with translucency; composite prevents confirmation |
| radius/panel | ~24–29px composite ≈ **~10–12pt** window corner | (estimated)(inferred) | scale-dependent; near native ~10pt window corner |
| radius/selection | ~14px composite ≈ **~6–8pt** | (estimated)(inferred) | inset rounded fill; near native menu/sidebar 8pt selection radius |
| text/primary | `#FFFFFF` (lum ~253) | (measured)(confirmed) | filenames, metadata values, "Metadata" header |
| text/secondary | ~`#909090` neutral gray (lum ~150 after removing red-glow contamination) | (estimated)(inferred) | section label + metadata "Name" label; ~6:1 on panel bg |
| text/disabled (scroll-fade) | filename dimmed to ~40% at list bottom edge | (estimated)(inferred) | bottom row "blob.heic" faded — a scroll-edge fade, not a disabled state |
| selection/fill | translucent white ~6–10%, **neutral (no accent tint)** | (measured)(inferred) | fill sits only ~4–6 lum above bg → very low contrast, see Defects |
| accent | **none present in UI** | (measured)(inferred) | no accent selection, no focus ring, no primary action; brand red lives only in the composite backdrop |
| space/row-pitch | **97px** uniform (rows 1–5) ≈ **~40–48pt** row | (measured→estimated)(confirmed) | pitch identical across all five rows; row rhythm is dead-on regular |
| layout/split | list : detail ≈ **35 : 65**, 1pt divider at x≈930 of ~306→~2080 panel | (measured)(inferred) | faint divider (lum ~30 on ~8) |
| search/field | no field chrome — large input text directly on panel; leading back-button (rounded-square ~15% white translucent fill) | (measured)(inferred) | native launcher convention; back-arrow is a borderless white SF Symbol |
| icons/list | genuine macOS system document icons (white page + "PNG" badge + thumbnail) | (measured)(inferred) | native tell — system-provided file icons |
| type/family | SF Pro (system) | (estimated)(inferred) | no web font tells |

## Layout skeletons

**Command-palette "detail list" view (dark).** Floating rounded HUD panel, no title bar / traffic lights.
- **Top strip — search bar:** leading rounded-square back-button (translucent white fill, white ← SF Symbol) + large query text (`.heic|` with text caret) set directly on the panel background (no bordered field). Full panel width.
- **Body — two-pane split (~35/65), 1pt divider:**
  - *Left (list, ~35%):* a gray Title-Case section header ("Section Label") sits above a vertical list of file rows. Each row = [system document icon] + [filename], left-aligned on a shared icon/text axis, ~97px pitch. The top row is pre-selected via a subtle neutral inset rounded fill; text stays white. Bottom row fades under a scroll-edge effect.
  - *Right (inspector, ~65%):* a rounded preview thumbnail of the selected file (16:9), then a "Metadata" section header (white), then metadata rows as label↔value pairs — "Name" (gray, left) / value (white, right-aligned to the pane edge), thin separator beneath. Panel bottom is cropped by the composite.

## Signature moves

- **[GOLDEN-NUGGET] Accent suppression — the neutral stage.** Selection is a low-contrast *neutral* gray inset-rounded fill with white (never accent-tinted) text; there is no focus ring, no primary-action colour, no accent anywhere in the chrome. Systematic and purposeful: the launcher stays chromatically silent so that content (file previews, and — across the product — per-extension colours) carries all the colour. This is the deliberate inverse of the native selection grammar, which tints selected text with the system accent. It is Raycast's entire visual temperament in one decision — and it costs the selection its contrast (see Defects).
- **[GOLDEN-NUGGET] Palette-as-stage grammar.** No window: a full-bleed near-black translucent HUD, search text with no field chrome, generous ~40–48pt rows. This is the ⌘K command-palette design language (peers: Spotlight, Alfred, Linear's command menu) rendered at HUD scale rather than as an AppKit list window.
- **[GOLDEN-NUGGET] Master–detail inside the palette.** A two-pane list+inspector (35/65) living *inside* the floating launcher — the command palette momentarily becomes a mini file browser with a metadata inspector. The "the palette can become any app" extensibility is Raycast's identity; the same shell hosts a launcher, a file list, and an inspector without ever growing window chrome.

## Defects

- **Weak focus/selection appearance (WCAG 2.4.13 / Contrast Dilution)** → the selection fill sits only ~4–6 lum above the panel background (≈1.3–1.5:1), and because every non-faded row is full-white text, the *only* cue that a row is selected is that barely-there fill. No accent tint, no ring, no weight change. In a keyboard-driven launcher the moving selection is the primary affordance, so a sub-2:1 selection state is a real cost of the accent-suppression signature. Canon would add a ≥3:1 contrast shift (accent-tinted text or a firmer fill).
- **Faint split divider (~<3:1 UI contrast)** → the 1pt list/inspector divider reads ~lum 30 on ~lum 8; borderline invisible. Minor.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| command-palette detail-list view (dark) | 12/14 | #10 faint split divider (~<3:1); #14 selection/focus contrast ~1.3–1.5:1 (no ≥3:1 shift) |

### Native-tells audit (10-pt) — command-palette view

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | AppKit-native lineage | pass (med) | system file icons, SF Pro, native section-header grammar; no web tells |
| 2 | Glass only on floating chrome; content opaque; no glass-on-glass | pass | the panel *is* the floating layer; list/inspector sit on near-opaque dark inside it |
| 3 | Selection: inset rounded fill + **accent** text/glyph | **fail (signature)** | inset rounded fill ✓ but neutral fill + white text, no accent tint — deliberate |
| 4 | Section headers sentence/title case, system font | pass | "Section Label" Title-Case gray SF Pro, not tracked uppercase |
| 5 | Density: 13pt body, 20–28pt controls, desktop rows | **fail (signature)** | ~40–48pt rows + large search input — launcher density, not native list density |
| 6 | Accent bound consistently | **fail** | no accent anywhere in UI (see signature) |
| 7 | One prominent action per view; dialog grammar | pass (n/a) | no dialogs; quiet back-button only |
| 8 | Concentric corners; child < parent | pass | panel ~10–12pt > selection ~6–8pt; preview thumbnail rounded |
| 9 | Toolbar: borderless symbols, grouped, one primary | n/a | launcher has no toolbar |
| 10 | Real chrome; no faked frame | pass | HUD legitimately has no traffic lights; red rim is composite, not a faked app frame |

**Native audit: ~7/10** (3 fails at #3/#5/#6 are all systematic Raycast house-style deviations → signature moves, not sloppiness; #9 n/a). Because this is a custom command-palette, treat #3/#5/#6 as Raycast-specific, **not** as evidence against native canon.
