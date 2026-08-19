# Framer — profile

- **Source:** macapp.supply · **Surfaces digested:** cover.png (marketing composite — brand mark + "made in Framer" showcase mosaic; **no app UI window present**) · **Last updated:** 2026-07-19
- **One-sentence identity:** *Not determinable from the supplied evidence* — the only image is a marketing brand composite; no Framer app surface (editor canvas, layers/inspector panels, toolbar) was provided to profile. (Product-knowledge prior, not image evidence: Framer is a browser-based AI website builder / design tool; its macapp.supply "desktop app" is a web wrapper, peer to Webflow / Figma-in-a-window / other web-in-Electron design tools.)
- **Cluster:** unassigned — cannot assign without a UI surface
- **Lineage:** web-electron (**low confidence — external product-knowledge prior, NOT derived from the cover**, which contains zero app UI). Per persona rule, lineage must be judged from a UI *body*; none exists here, so this classification carries no evidentiary weight for canon and Framer contributes **no** macOS-native evidence.
- **Era (chrome):** unknown — no window chrome, toolbar, or app content visible

## Evidence caveat

The macapp.supply payload for Framer is a **cover + icon only** (empty `gallery`, no `shot-*` files). The cover is a pure marketing composite: the white Framer logo mark centred on a full-bleed pure-black field, ringed by a tight-gutter mosaic of ~18 **published showcase websites** ("made in Framer" gallery). Critically, every thumbnail is an *end-user website hero* (with website chrome like "VIEW PROJECTS" / "GET A QUOTE" / "Watch Reel" buttons) — **none is the Framer editor UI** (no macOS traffic-light chrome, no canvas, no layers tree, no properties inspector). Per the skill's cover rule, only the **brand layer** is analysable here; there is no app-window layer to extract. Consequently **no UI rubric, no native-tells audit, and no layout skeleton can be produced** — those require an actual app surface. Everything below is brand evidence, marked as such, and must never feed macOS UI canon or style clusters.

## Tokens (brand evidence only — from cover.png)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg-cover | `#000000` — pure black | (measured)(inferred) | ~11.9k exact (0,0,0) samples on a coarse grid; hard neutral black, **not** warmed or blue-black. Maximal-contrast stage for the mosaic |
| brand/mark-fill | `#FFFFFF` — pure white | (measured)(inferred) | The folded-F logo is pure #FFF; single-ink monochrome mark, no gradient in the cover render |
| brand/mark | Two offset chevron/flag counters stacked into an "F" (the Framer folded-ribbon mark) | (estimated)(inferred) | Hard geometric, sharp 45° cuts, no rounding; reads as origami/fold, not a letterform outline |
| brand/palette-economy | 2 values in the frame itself (black ground + white mark); **full-spectrum inside the mosaic** | (measured)(inferred) | The brand chrome is monochrome; the *content it frames* is deliberately maximalist (see signature) |
| brand/mosaic-gutter | ~0px — thumbnails butt against pure-black gutters ~8–14px wide | (estimated)(inferred) | Tight black grid; the black ground doubles as gutter, so tiles read as a single dense field |

## Layout skeletons

None — no app UI surface was provided. (Cover composition: a single centred logo mark on full-bleed black, framed by a ~4-column irregular mosaic of website thumbnails of varying heights — a masonry-style "gallery wall." This is brand/marketing layout, not app layout.)

## Signature moves

- **[GOLDEN-NUGGET — brand, not UI]** *Monochrome mark, maximalist frame:* the brand chrome is ruthlessly two-value (pure black + pure white), but it surrounds a mosaic that deliberately spans the entire aesthetic range map — Swiss ("midlife engineering"), editorial/fashion (i-D "ELLE, OH, ELLE"), terminal/hacker (green "FORMALIZATION / METHOD TRANSFER"), 3D-render (orange asterisk "Moving Brands Forward", pink objects), sports (Powerade/LSU), event poster ("superlocal 13–19 OCT"), AI-brand (purple "wishlabs"), automotive (white Porsche). The thesis is legible without a word of copy: *any look is buildable in Framer.* The restraint of the frame is what lets the range of the content read as intentional rather than noisy. Systematic and purposeful **as branding**; cannot be promoted as UI taste.
- **[brand]** *Pure-black stage:* unlike the warmed dev-tool blacks seen elsewhere in this corpus (e.g. Cursor's `#14120B`), Framer commits to hard `#000` — a gallery/curator move (black wall → the work is the subject), not a warmth move. Single data point, uncorroborated by any UI surface.

## Defects

- None assessable — a brand composite cannot fail the UI rubric or the native-tells audit (category mismatch). Not recording pseudo-defects against a non-UI surface.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.png (marketing composite) | N/A — not a UI surface | 14-point UI rubric and 10-point native-tells audit both inapplicable; no window chrome, controls, type ramp, or app content to measure — only a brand mark and a gallery of third-party websites |

## What would move this profile forward

Need ≥1 real Framer **app window** screenshot — the editor with its canvas, left layers/pages tree, and right properties inspector, ideally light *and* dark — to: (1) confirm/refute the web-electron lineage from the body (Framer's editor is a canonical web-in-a-window design tool and will likely read non-native — dense inspector, web type sizes, custom controls), (2) run both rubrics, (3) test whether the pure-black brand stage carries into product chrome or is brand-only. Until then Framer is a **brand digest, not a UI digest**, and contributes no macOS-native evidence. (Note: an app icon — a charcoal squircle with the white folded-F — was supplied but not digested here; this task is scoped to Workflow A / UI only.)
