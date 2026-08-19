# Grape — profile

- **Source:** macapp.supply (cover.jpg — marketing composite; single partial surface) · **Surfaces digested:** main window (4-pane notes workspace, dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple Notes' four-pane structure rebuilt in a committed near-black monochrome that *withholds* the system accent — Bear's calm dark restraint plus an AI companion pane; "the UI recedes so the note (and the AI) can think."
- **Cluster:** unassigned (candidate: near-black-monochrome / quiet-dark-notes)
- **Lineage:** native (medium) — 13–14pt body, desktop control density, genuine coloured traffic lights, source-list sidebar, borderless monochrome SF-Symbol-style toolbar, sentence-case section headers, exact system dark bg `#1E1E1E`. A well-built Tauri/Electron app *could* fake this, but density + sentence-case headers + system-bg argue native (or macOS-correct SwiftUI). Non-native evidence never feeds macOS canon; treated cautiously here given the composite.
- **Era (chrome):** big-sur (flat-native, post-Big-Sur) — no confirmable Liquid Glass grammar (flat opaque panes, neutral rounded selection, no lensing/container-morph). Dark-mode humility: cannot confirm *or* deny glass on the top toolbar strip from one dark still → `(insufficient-evidence)`. The near-black palette is a house-style choice layered over standard chrome, not custom-drawn chrome.

## Scale anchor
Traffic-light center-to-center measures **27px**, matching the macOS-27 kit cluster pitch (68pt-wide cluster → 27pt pitch) → the window is composited at **≈1× (1 cover-px ≈ 1pt)**. All values below read directly as points, but this is a JPEG marketing composite → provenance `(estimated)` with modest ranges.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas (content, editor + note-list) | `#1E1E1E` (measured)(inferred) | | **Exact match to macOS-27 kit dark window bg** — native fidelity signal |
| bg/sidebar | `#262626` (measured)(inferred) | | source list a hair *lighter* than content panes |
| fill/selection (sidebar row + note card) | `#3C3C3C` sidebar · `#353535` note card (measured)(confirmed) | | **neutral gray, NO accent tint** — the defining deviation; see Signature |
| text/primary | `~#E8E8E8–#FFFFFF` (estimated)(confirmed) | | white titles/body; JPEG peak read `#DDDDDD` |
| text/secondary | `#949494` (~55%) (measured)(confirmed) | | section headers, timestamps, count badges — matches kit Secondary label |
| accent/identity | Orange `#FB9800` (measured)(inferred) | | folder glyphs only; ≈ system Orange (kit dark `#FF9230`). Used as content identity, **not** bound to selection/focus |
| type/H1 (editor title) | `~22–24pt Bold`, sans (estimated)(inferred) | | Title1→LargeTitle tier; tight |
| type/list-title + section head | `~14–16pt Semibold` (estimated)(confirmed) | | note-list item titles, "notes" header |
| type/body | `~13–14pt Regular`, SF-Pro-class (estimated)(inferred) | | editor body + numbered lists; native density |
| type/meta | `~11–12pt Regular`, secondary gray (estimated)(confirmed) | | "2:34 PM · Imagine your MacBoo…" |
| space/base | 8pt grid, 4pt micro (estimated)(inferred) | | rows/columns snap near 4/8 within measurement error |
| radius/selection | `~8pt` (estimated)(inferred) | | inset rounded selection fill |
| radius/note-card | `~10–12pt` (estimated)(inferred) | | elevated selected-note card |
| radius/window | `~12pt` (estimated)(inferred) | | kit ships no window radius — measured here |
| chrome/toolbar-strip | `~52–60pt` tall, unified (estimated)(inferred) | | traffic-light top inset ≈22pt; reads as unified-toolbar tier |
| chrome/sidebar | `~240pt` wide, full-height, opaque `#262626` (estimated)(inferred) | | kit sidebar 256pt — close |
| layout/columns | sidebar ~240 · note-list ~325 · editor ~633 · AI pane ~370 (pt) (estimated)(inferred) | | four vertical panes, ~1570pt window |
| row/sidebar | `~38–40pt` (Large tier) (estimated)(confirmed) | | 38px consistent pitch across 7 folder rows |

## Layout skeletons

**Main window — four-pane notes workspace (dark):**
- **Pane 1 — Source list (~240pt):** top strip with genuine red/yellow/green traffic lights (left) + "new folder" glyph (right). Below: `Folders` header (secondary, sentence-case) → folder rows (~38pt) each = amber SF-folder glyph + label + right-aligned count badge. Selected row ("notes", count 13) carries a neutral-gray `#3C3C3C` inset rounded fill; label stays white (no accent).
- **Pane 2 — Note list (~325pt):** header = "notes" title (semibold ~15pt) + trailing search + compose glyphs, 1px divider under. Time-chunked sections (`Today`, `Previous 30 Days` — secondary, title/sentence case). Items = bold title + secondary metadata line (`timestamp · preview snippet`). Selected item = elevated `#353535` rounded card (~10pt radius); others flat.
- **Pane 3 — Editor (~633pt):** formatting toolbar = borderless monochrome symbols in a leading group (T / checklist / table / attach / blocks / draw), trailing utilities (⋯ overflow, gear, split-view toggle). Body = bold H1 title → body with inline-bold emphasis → H2 (`The simple answer`). Body runs the full column width (see Defects).
- **Pane 4 — AI companion (~370pt):** header = derivative-note title ("Using Two Different AirPods on …", truncated) + trailing `+` and history/clock glyphs. Body = AI-generated "kid-simple version" numbered rewrite of Pane-3's note. Reads as a second editor opened via the split-view toggle — source note beside its AI derivative.

## Signature moves
- **[GOLDEN-NUGGET] Accent-withheld monochrome.** Selection in both the sidebar and note list is a *neutral gray* inset fill (`#3C3C3C` / `#353535`) with white (not accent-tinted) label — the app systematically refuses the system-accent binding that native selection expects. Its single hue is spent on warm-amber folder glyphs (`#FB9800`, content identity, never on UI state). Systematic + purposeful (calm, content-first, low visual load) → a committed signature, not a defect — but it deviates from native selection grammar (recorded in Defects/native audit as the tradeoff).
- **[GOLDEN-NUGGET] The AI companion split.** The split-view toggle opens the source note beside an AI-generated *derivative* note (differently titled, a "kid-simple" numbered rewrite). The product's "thinks with you" pitch rendered as a two-editor layout with its own `+`/history chrome — the feature *is* the layout.
- System-fidelity tell: content panes use the **exact** macOS-27 kit dark window bg `#1E1E1E`, and section headers are sentence/title case — the app honours the platform's quiet grammar even while overriding its color.

## Defects
- **Contrast Dilution (borders)** → the 1px column dividers are `#262626`-on-`#1E1E1E` (≈1.1:1), effectively invisible; panes are separated by tone alone. Native/rubric #10 fail — canon wants ≥3:1 non-text separation (or a clearer material step between panes).
- **Line Length Fatigue** → editor body runs the full ~600pt column (~80 characters), past the 65–75ch comfort cap. Canon: `max-width ~65ch` on prose.
- **Accent not bound** (native-audit tradeoff, not a pure defect) → selection + focus + primary action carry no system accent; the deliberate monochrome costs a small Jakob's-Law prediction error (users trained on accent-selection). Logged as signature-with-tradeoff.
- Minor: a **gear (Settings) glyph in the editor toolbar** — macOS convention is a Settings *window* via ⌘, / the App menu, not toolbar chrome. Sporadic, low severity.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark, 4-pane) | 12/14 | #6 line length (editor body ~80ch), #10 border contrast (column dividers ≈1.1:1); #9 borderline (secondary meta on `#353535` card ≈3.5–4:1) |
| main window — native-tells | 8/10 | #3 selection not accent-bound (neutral gray), #6 accent not bound consistently (both = the deliberate monochrome signature) |

## Brand evidence (marketing backdrop — NOT app UI)
Near-black `~#0A0A0A` hero; two-tone bold grotesque display headline (white "The AI note taking app" + gray "that thinks with you", heavy geometric-ish grotesque with rounded terminals — display face, not the app's SF-Pro body); "Now in Beta" pill; one **filled white** "Download for Free" primary + **outlined ghost** "See Features" secondary (correct action singularity). Brand voice = confident monochrome grotesque — consistent with the app's in-window restraint. App icon (separate file): 3D purple grape cluster, emoji-adjacent, glossy — warm/playful, contrasts the austere UI (not digested here; Workflow A only).
