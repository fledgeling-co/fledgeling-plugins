# Glyph — profile

- **Source:** macapp.supply (cover composite only — one app-window screenshot embedded in a marketing landing page; no standalone shots) · **Surfaces digested:** main window (three-pane markdown editor), light · **Last updated:** 2026-07-19
- **One-sentence identity:** Bear's warm paper calm crossed with Craft's rounded friendliness, applied to a Markdown notes editor — an editorial writing tool that themes macOS toward "paper" rather than platform-neutral gray.
- **Cluster:** unassigned (candidate seed for a "warm-editorial writing" cluster — first member)
- **Lineage:** native (med) — AppKit/SwiftUI-class density: 13pt-class chrome text, genuine coloured traffic lights, borderless monochrome SF Symbols toolbar, content-vs-sidebar two-tone. Heavy custom theming (solid brand-blue selection, custom tab pill, warm paper surfaces) but never breaks native density; a well-built Electron/Tauri can't be fully excluded from a single marketing shot, hence med not high.
- **Era (chrome):** custom (flat, warm-tinted, chromeless) — no Liquid Glass lensing / scroll-edge translucency evident, and not legacy-native (no hard 1px dividers, bezeled controls, or saturated full-bleed system-blue selection). A themed flat design sitting outside the standard material eras.

## Provenance note
All values read from a marketing **cover composite** in which the app window is scaled down (~1.2× effective; traffic-light and row measurements are internally inconsistent by ±20%, so metrics are **(estimated)** with wide ranges, never (measured)). Colours may carry slight composite shift — marked (estimated). Only the app window is design evidence; the surrounding serif-display headline, sticker chips, black pill nav, and monospace Homebrew command are **brand** evidence (recorded at bottom), not native canon.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/sidebar | #F8F7F5 (estimated)(inferred) | warm off-white (R>G>B), source-list + inspector share this "paper" tone |
| bg/inspector | #F3F3F0 (estimated)(inferred) | marginally warmer/greyer than sidebar; same paper family |
| bg/editor | ~#FFFFFF / #FEFEFE (estimated)(inferred) | content column reads whiter than chrome — deliberate two-tone (content vs sidebar material) |
| accent/selection | #5E9DC0 muted steel-blue (estimated)(inferred) | solid fill on selected sidebar row, white label+glyph; NOT the vivid system blue #0088FF, NOT bound to the user's system accent |
| accent/link | steel-blue, underlined (estimated)(inferred) | in-editor links; reads same muted-blue family as selection |
| type/ui-label | 13pt-class SF Pro Regular (estimated)(inferred) | sidebar rows, inspector labels — native chrome density |
| type/editor-body | ~14–16pt regular sans (estimated)(inferred) | reading body runs a touch larger than 13pt chrome for comfort; H1 bold ~24–28pt-class |
| type/section-header | secondary grey, title-case (sidebar) / tracked UPPERCASE (inspector) (estimated)(inferred) | inconsistent between panes — see Defects |
| type/inline-code | monospace on light-grey rounded chip (estimated)(inferred) | `todo.txt` pill in body |
| identity/pinned | filled yellow star (estimated)(inferred) | per-item identity colour, paired with label — correct |
| identity/task | red hollow ring "0 of 5 done" (estimated)(inferred) | status colour paired with label — correct |
| space/sidebar-row | ~34–40pt row pitch, generous vertical padding (estimated)(inferred) | roomy — larger than the compact 24–32pt tier; supports the spacious feel |
| radius/selection | ~8–10pt (estimated)(inferred) | inset ~12–14pt each side; matches kit sidebar-selection radius 8 |
| chrome/toolbar | unified single row, borderless monochrome symbols in ~3 groups (estimated)(inferred) | nav (←/→) · centred document-tab pill (+) · action cluster ({} / edit / preview / split / panel) |
| chrome/traffic-lights | genuine coloured red/yellow/green, focused (measured)(inferred) | real Mac frame |

## Layout skeletons

**Main window — three-pane markdown editor (light):**
- **Left — source list** (~230–256pt est.): warm off-white. Top: traffic lights + sidebar-collapse glyph. Flat nav rows (icon + label + trailing count badge): New Note (selected, solid steel-blue fill, white text), Pinned·6, All Notes·325, Collections, Connections. Then a **section header "Notes"** (secondary grey, title-case, disclosure chevron + trailing sort/collapse glyphs), then Archive·75, Areas·5. Rows roomy (~34–40pt pitch).
- **Centre — editor**: whiter than chrome. Unified toolbar row (back/forward, greyed breadcrumb, centred white tab-pill with note title + "+", trailing action glyphs). Content: **H1 with a small grey "H1" gutter badge** in the left margin; "Source:" + underlined link; body paragraph with inline-code chip; **H3 "The system" with a grey "H3" gutter badge**; bullet list. Left-aligned, single measure column.
- **Right — inspector** (~300pt est.): warm off-white, rounded top-left corner concentric with window. Tab chips **Info** (selected — white elevated chip w/ soft shadow) | History (grey) + ✕. "Properties" heading with a list/`</>` segmented toggle (white chip = active). "+ Add property" (very light grey ghost action). **STATS** (tracked uppercase micro-header): Words 210 · Characters 1,208 · Reading time 1m 3s (label grey left / value dark right). **TASKS**: red ring "0 of 5 done". **OUTLINE** …

## Signature moves
- **[GOLDEN-NUGGET] Heading-level gutter badges** — each markdown heading carries a small grey "H1"/"H3" tag in the editor's left margin. Makes document structure legible in-place without a heavier outline chrome; the app's most memorable, most on-brand-for-Markdown decision.
- **Warm paper two-tone** — off-white *warm* chrome (#F8F7F5 sidebar / #F3F3F0 inspector, R>G>B) framing a pure-white content column. Reads "paper / editorial" where stock macOS reads neutral grey. Systematic across both chrome panes → signature, not accident.
- **Muted steel-blue selection + matching link blue** (#5E9DC0), solid fill with white text. A calm, bookish accent deliberately *not* the vivid system blue — the app choosing a restrained house colour over the platform accent. Character-defining, though it costs contrast (see Defects).

## Defects
- **Contrast Dilution / insufficient text contrast** — white label on the #5E9DC0 selection fill is ~2.7:1 (below the 4.5:1 floor); "+ Add property" and the right-hand toolbar action glyphs render very light grey (~<3:1). Canon fix: darken the selection blue or switch to a light accent-*tinted* fill with dark accent text (the general native selection grammar), and lift idle/disabled glyphs to ≥3:1.
- **Mixed section-header grammar** (minor tell, not a hard defect) — the sidebar header "Notes" is correctly title-case secondary system font, but the inspector headers **STATS / TASKS / OUTLINE** are tracked UPPERCASE — a web/iOS micro-header convention. Native inspectors favour title-case secondary labels throughout.
- **Selection treatment deviates from native grammar** (signature-adjacent) — inset rounded shape is correct, but the *solid saturated fill + white text* follows System Settings' house style rather than the general flat inset-tinted-fill rule, and the hue is the app's brand blue, not the system accent. Logged as deliberate house style; the contrast miss above is the actionable part.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (light) | 11/14 | #9 text contrast (white-on-steel-blue selection ~2.7:1; "Add property" light); #10 UI contrast (faint toolbar glyphs ~<3:1); #12/#14 unobservable (no visible text field / focus state) |

## Native-tells audit (main window)
8/10 — soft-fail #3 (selection is solid custom-blue + white text, not light accent-tinted fill with accent text) and partial #6 (accent internally consistent but bound to the app's brand blue, not the user's system accent). #4 passes on the sidebar header but the inspector's tracked-uppercase headers are a mild tell. Passes: native density, opaque content (no glass misuse), one quiet action, concentric corners, borderless grouped toolbar, genuine chrome.

## Brand layer (cover composite — NOT native evidence)
Landing page around the app shot: **serif display headline** ("A better *Markdown* app for your *notes*" — modern serif, italic accent words) with two inline **sticker chips** on tinted rounded highlights (purple M↓ Markdown badge on lavender; orange notes glyph on cream). Body/subhead in a **monospace-flavoured** sans; black **pill nav** ("Glyph · Features Pricing Manifesto · Try Free"); black filled "Download for Free" button beside a monospace `brew install --cask SidhuK/glyph/glyph` field; "Lifetime license $12.99" with EARLYACCESS code chip; GitHub/Discord/Twitter glyphs. Aesthetic family: **editorial/literary + playful sticker accents** — warm, indie, self-aware ("Manifesto"). This is brand/marketing evidence only; it corroborates the app's warm-editorial register but never feeds macOS canon.
