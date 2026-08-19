# Compressor — profile

- **Source:** macapp.supply (cover composite only; no true UI shots) · **Surfaces digested:** main window (dark, marketing composite in 3D perspective) · **Last updated:** 2026-07-19
- **One-sentence identity:** A consumer image-compressor that dresses a genuine native window frame in a fully custom, brand-coral design language — CleanShot-X-indie polish crossed with a warmed neo-grotesque product look, where an abstract quality/size dial is re-cast as three physical objects (leaf → scale → diamond).
- **Cluster:** unassigned (candidate: "warm-charcoal consumer utility")
- **Lineage:** unknown, leaning custom/non-native (low confidence) — genuine traffic-light chrome + centered title + native window radius, but a body that departs from native control grammar (Lucide-class line icons, brand-accent selection fills, icon-card radio group, oversized targets). A single perspective marketing render cannot separate heavily-styled SwiftUI from Electron. **None of this app's selection/accent/density evidence feeds macOS canon** regardless of the eventual verdict — its grammar is non-native by construction.
- **Era (chrome):** custom-drawn dark design language — no Liquid Glass evidence (flat opaque dark panels, no lensing/translucency), not legacy-native either.

## Provenance caveat (read before trusting any number)

Every value below is `(estimated)` and low-confidence. The only artefact is a **marketing composite**: the app window is rendered in ~15–20° perspective, resting on a lit surface, under studio lighting that gradient-shifts the darks. There is no orthographic screenshot, no visible menu bar, and almost no body text (the UI is icon-only). Pixel metrics are therefore proportional/qualitative, not measured. Colours are sampled from the render and carry lighting bias. Bring a straight-on screenshot to promote anything.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| accent/primary | ~#EA5A48 coral/vermilion (range #E85A48–#EC6757) | (estimated)(inferred) | Brand hue, **not** a system accent and not in the macOS-27 12-hue palette (sits between Red #FF4245 and Orange #FF9230). Same coral used in the marketing type — product and poster share one colour. |
| bg/chrome-titlebar | ~#2E2C2C warm near-black | (estimated)(inferred) | Dark mode avoids pure black; darks are marginally warm (R≥G≈B). |
| bg/panel | ~#383737 | (estimated)(inferred) | Section panel fill, one step up from deepest gap. |
| bg/deepest-gap | ~#2A2929 | (estimated)(inferred) | Inter-section troughs / window body base. |
| surface/card-unselected | ~#434343 | (estimated)(inferred) | Raised preset-card fill; unselected state. |
| surface/card-selected | coral #EA5A48 (solid fill) | (estimated)(inferred) | Selection = full saturated brand fill, white glyph + white dot. |
| glyph/on-accent | ~#FFFFFF | (estimated)(inferred) | White line icon on coral; non-text contrast ~3.2:1. |
| glyph/muted | mid-gray on dark card | (estimated)(inferred) | Unselected preset icons; risks <3:1 non-text floor. |
| divider | 1px near-invisible dark line | (estimated)(inferred) | Separates the three column sections. |
| radius/card | ~10–14px (perspective-uncertain) | (estimated)(inferred) | Preset cards + primary button; generous soft radius. |
| control/density | oversized / touch-adjacent | (estimated)(inferred) | Slider knob, cards, primary button all far exceed native 20–28pt control tier. |
| type/brand-wordmark | heavy grotesk, black ~#212220 ("Compressor"); coral tagline | (estimated)(inferred) | Marketing type only, not app UI — bold neo-grotesque single-word wordmark. |
| type/window-title | light-gray centered title, small | (estimated)(inferred) | Only text in the UI; native centered-title behaviour. |

## Layout skeletons

**Main window (dark, marketing composite):**
- Window: dark, rounded corners, **genuine traffic lights** (red/yellow/green, correct order, top-left, coloured = focused) in a thin compact titlebar with a **centered** "Compressor" title. No toolbar.
- Body splits into two zones:
  - **Left preview zone (~60–65% width):** full-height, edge-to-edge image preview (mountain-lake photo). A small monochrome image-badge glyph sits in the top-left corner as an overlay indicator.
  - **Right control column (~35–40% width):** vertical inspector divided by 1px dividers into three stacked sections:
    1. **Quality slider** — small "adjustments/levels" glyph header; horizontal slider (coral-filled left portion, gray right, round white knob at ~55–60%); a discrete tick scale (~6–7 ticks) below, implying snap-to-level quality steps.
    2. **Preset selector** — small "image" glyph header; a 3-up row of equal-width tall rounded cards, radio-exclusive with a bottom dot indicator: **leaf** (eco / max compression) · **balance scale** (balanced — *selected*, solid coral) · **diamond** (best quality / least compression).
    3. **Primary action** — one full-width tall **coral** button, white download-into-tray glyph, **no text label**.

## Signature moves
- **[GOLDEN-NUGGET] The physical-metaphor preset trio.** The abstract quality-vs-filesize tradeoff is encoded as three familiar objects — leaf (light/eco) → scale (balance) → diamond (premium) — instead of numbers, percentages, or words. It makes a continuous engineering dial legible pre-attentively (picture-superiority + trained schemas). This is the app's taste layer in one decision.
- **The unifying coral.** A single warm brand hue (#EA5A48) carries the marketing wordmark's tagline *and* every active UI element (slider fill, selected card, primary button), so the app and its poster read as one object. Systematic and purposeful → signature, not defect (for a consumer brand); simultaneously a native-fidelity defect (accent should bind to the user's system accent).

## Defects
- **Focal Collision (soft)** — two fully-saturated coral regions (selected preset card + primary export button) compete inside one narrow column. Canon: tint selection subtly (inset accent-tinted fill, accent glyph) and reserve full saturation for the single action → one focal point.
- **Icon-only controls, no labels** — leaf/scale/diamond presets and the export glyph carry no text. Violates recognition-over-recall (Jakob's Law / Weinschenk): users must infer each preset's meaning. A tooltip or one-word caption per card would fix it without adding clutter.
- **Non-native selection & accent grammar** — solid brand-fill selection + hardcoded brand accent instead of a system-accent-bound inset tint (native-tells #3/#6). Signature for the brand; defect for native fidelity.
- **Muted-icon UI contrast (borderline)** — unselected preset icons (mid-gray on ~#434343) likely dip below the 3:1 non-text floor. Intentional de-emphasis, but pushed past the accessibility edge.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark, composite) | ~10/14 (est) | #8 action singularity (selection + primary both fully saturated coral) · #10 UI contrast (muted unselected icons risk <3:1). N/A: #4/#5/#6 (icon-only UI, no body text), #12/#13 (no text inputs/labels), #14 (static render, no focus state). |

### Native-tells audit (dark main window) — ~3/10 (est)
1. Native lineage — **FAIL/uncertain**: custom design language, web-default line icons, non-native controls.
2. Glass discipline — **PASS**: flat opaque panels; absence of glass is legitimate.
3. Selection grammar — **FAIL**: solid brand-colour fill, not inset accent-tinted fill with accent glyph.
4. Sidebar headers — n/a (no source list).
5. Density — **FAIL**: oversized touch-adjacent targets, not 20–28pt native controls.
6. Accent binding — **FAIL**: hardcoded brand coral, not the user's system accent (internally consistent though).
7. One prominent action — **PASS**: single bottom-trailing primary; selected card reads as state.
8. Concentric corners — n/a/can't-verify (perspective).
9. Toolbar — n/a (thin centered-title bar only).
10. Real chrome — **PASS**: genuine traffic lights, real window frame, focused-window colours.

**Verdict:** native-*framed*, non-native-*bodied*. A confident, warm, brand-forward consumer utility whose evidence teaches consumer-brand taste, not macOS-native canon.
</content>
</invoke>
