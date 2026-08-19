# Icon: DriveMosaic

- **Era:** Big Sur unified (matte, non-glass; front-facing) — but composition is subject-literal, not the era's stock tool-on-field convention · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 1024×1024 RGBA, `321f7c2e`) · **Category:** Utility (treemap disk analyzer)

The icon is a stylized render of the app's own core view: a treemap of coloured rectangles packed inside a dark rounded-square. Subject-mining taken to its literal end — the product's output *is* its face. Every strength and every failure below traces to that single decision.

| Dimension | Reading |
|---|---|
| Background | Flat dark navy-charcoal field `#1A1B25` (measured); gutters `#181A23`; antialiased rim ~`#35373F`. Not black — a blue-biased near-black. |
| Glyph | Abstract geometric mosaic — 12 rounded-rect treemap cells of varied size, each a different muted hue, ~8px dark gutters (measured @1024). Fills the safe zone; tile field inset ~82px (~8%) inside the squircle. |
| Overlay device | None — no tool, badge, or frame. The tessellation is the whole composition. |
| Light model | Per-cell top-down linear gradient: every tile lighter at top, ~20L darker at bottom (blue-large `#689CC5`→`#5282AA`, terracotta `#C5755F`→`#A85E4B`). No specular, no cast shadow. Consistent direction across all cells — decorative per-cell shading, not a global scene light. |
| Layer stack | 2 planes: (back) dark navy field with a slightly darker baked squircle rim → (front) the gradient-shaded tile mosaic floating on dark grout. |
| Palette economy | None by the letter: 12+ hue families, one per tile, no reserved accent. Purposeful — the polychrome *is* a category legend (a treemap colour-codes file types). Muted/dusty register (all ~50–65% L), distinctly desaturated vs the cover's saturated version of the same rainbow. |

**Palette (measured):** field `#1A1B25` · tiles `#AF608A` magenta, `#8FA457` olive, `#5B93C0` steel-blue, `#C06951` rust, `#BA7D8B` mauve, `#69AB7C` green, `#7CB6B1` teal, `#A2825C` brown, `#6477A5` blue-violet, `#BFAF52` ochre, `#8667B6` purple, `#CB8E4D` amber · accent: none.

## Signature devices
- **The product as its own portrait** `[GOLDEN-NUGGET]` — the mark is a stylized treemap, the literal output of the app. Instantly on-message ("this thing draws coloured disk maps") at hero size; skirts the HIG "don't replicate UI components" line but abstracts far enough (no chrome, no labels, dark grout) to read as an emblem rather than a screenshot.
- **Muted-rainbow treemap** — a full 12-hue polychrome as semantic legend, pulled down to a dusty mid-century register. The saturation delta from the cover (vivid #7c5cff/hot-pink/teal) is the icon's one taste move: same concept, quieter voice.
- **Per-cell top-down gradient** — each tile individually shaded light-top→dark-bottom, giving soft embossed depth without any glass, gloss, or bevel line (edges are clean single fills).
- **Dark grout field** — tiles float on blue-black navy with even ~8px gutters, reading as a tiled mosaic / brick wall.

## Failures
- **#3 Silhouette (FAIL):** filled solid black the icon is a featureless rounded square — zero outline nameability. Identity lives entirely in the internal tessellation + colour; the mark has no memorable contour.
- **#6 Palette economy (FAIL, but justified):** 12+ competing hues, no accent reservation. Violates the ≤2-hue-family rule by the letter — but the polychrome is subject-driven (a category legend), so it's a signature move, not undisciplined confetti. Recorded as purposeful.
- **#10 Variant robustness (FAIL, era-forward):** the whole identity is the multicolour coding. A tinted or mono render collapses all 12 hues to one tint and the concept dies — confirmed by the grayscale pass, where tiles merge into a near-uniform gray brick wall (structure survives, category coding does not). On macOS 26 this icon cannot participate in tinted mode.

**Soft passes (flagged for synthesis):**
- **#1 Mask discipline (soft):** respects the squircle, but ships *pre-masked* — transparent corners (alpha 0) with a baked darker rim ring, rather than Apple's prescribed square unmasked bleed layer. The system re-masks fine, but the baked rounded container is a delivered artefact, not a system effect.
- **#4 16px squint (soft):** at 16px the mosaic gestalt survives — the five large blocks (blue, terracotta, magenta, olive, green) stay legible as "a colourful tile grid" — but the tiny cells (brown, blue-violet) smear into noise; the precise treemap reading is lost, only "colcoured mosaic square" remains.
- **#7 Figure-ground (soft):** tiles-vs-field contrast is strong (mid-tone on near-black); tile-vs-tile contrast is weak and collapses in grayscale.

## Rubric
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Mask discipline | soft pass | pre-masked squircle w/ baked rim + alpha corners, not square bleed |
| 2 | Grid adherence | pass | mosaic optically centred, even ~8% dark margin all sides |
| 3 | Silhouette | **fail** | solid-black = featureless rounded square, no contour identity |
| 4 | 16px squint | soft pass | large blocks survive; small cells smear to noise |
| 5 | Single light model | pass | consistent per-cell top-down gradient throughout |
| 6 | Palette economy | **fail** | 12+ hues, no accent — but subject-justified legend |
| 7 | Figure-ground | soft pass | tiles vs field strong; tile vs tile merges in grayscale |
| 8 | Depth coherence | pass | flat coplanar tiles on grout, no z-fighting |
| 9 | Era coherence | pass | uniform matte/soft treatment, no mixed-era quotation |
| 10 | Variant robustness | **fail** | tint/mono collapses the polychrome identity |
| 11 | Personality | pass | the app's own visualization as its mark — strong, committed |
| 12 | No-text | pass | no words/photo; UI-replication tension noted at #11 |

**Score: 9/12** — three hard fails (#3, #6, #10), three soft passes (#1, #4, #7). All three fails share one root: making the icon a full-canvas polychrome data pattern buys maximum subject-recognizability at hero size and pays for it in silhouette, economy, and tint-survival.

## Rhymes with
- Utility icons that render their own output/visualization as the mark (disk analysers, monitors, stats tools) — the "data-viz emblem" family (hint only; confirm against corpus).
- Muted mid-century colour-block palettes — dusty, desaturated rainbow on a dark ground.
- Dark-field flat-geometric utility icons generally (near-black navy container + soft-shaded shapes).
