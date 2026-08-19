# Looq: Preview Files for Mac — profile

- **Source:** macapp.supply (meta.json + cover.jpg + icon.png) · **Surfaces digested:** 0 native app surfaces — the only UI-adjacent asset is a marketing feature-grid cover with **no app window inside it** · **Last updated:** 2026-07-19
- **One-sentence identity:** A file-preview/Quick Look utility whose brand is *deliberately, completely achromatic* — black wordmark, black pill, gray body copy, a metallic-grayscale icon — so the colourful rendered files (syntax highlighting, Markdown, diagrams) supply all the colour; iA Writer's monochrome discipline applied to a developer-leaning "render everything" previewer.
- **Cluster:** unassigned (proposed hint: *achromatic-utility (brand)*) — sole candidate; and note this is **brand/marketing evidence, not native-UI evidence**, so it cannot seed a macOS style cluster on its own.
- **Lineage:** unknown (n/a) — **no app UI was supplied.** The cover is a web/marketing composite, not a Mac window; framework lineage is unassessable from these two assets. The meta.json markets AppKit affordances ("native AppKit tables", a Quick Look extension), which *suggests* an AppKit-native product, but marketing copy is not design evidence and does not establish lineage.
- **Era (chrome):** unknown — no chrome present. The **icon** reads Big Sur-era squircle (superelliptical), not a Liquid Glass / Icon Composer layered-glass treatment; that is icon evidence, not app-chrome evidence.

## What was actually supplied (honesty note)

Two files, **neither of which is an app screenshot**:

1. **cover.jpg** — a 4800×2520 (1.905:1, ~40:21) light-mode **marketing feature sheet**: top-left brand lockup (icon + "Looq" wordmark + tagline "Built to render the rest of your files."), a 3-column × 4-row grid of feature headline/description pairs, one black pill CTA ("Try free for 7 days →") bottom-left, and a "parcse.com / looq" footer bottom-right. There is **no rendered app window, no toolbar, no sidebar, no content pane** anywhere in the composite. Per the skill's boundary rule (an image showing no actual app UI is recorded honestly and skipped for native digestion), this cover yields **brand evidence only** and feeds **no macOS canon**.
2. **icon.png** — the 256×256 app icon (brand evidence; Workflow A run, so it is characterised as brand context below, **not** given a full Workflow-B icon digest and **not** eligible for icon canon).

Consequence for the corpus: **zero native-UI surfaces, zero rubric-scorable app windows.** The 14-point rubric below is applied to the *marketing composite as a designed layout* (useful as brand-competence evidence) and is explicitly non-native; the 10-point native-tells audit is **N/A** (no app surface to audit).

## Tokens

All values `(estimated)(inferred)` from one high-resolution marketing asset whose authored viewport is unknown — so absolute pixel sizes are meaningless and are given as **relative type roles + ratios**, per measurement-honesty rules. These are **brand tokens, not app-UI tokens.**

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/chroma | **NONE — fully achromatic** (black / grays / off-white only) | (measured)(inferred) | THE defining choice; not one accent hue anywhere on the cover |
| bg/cover | warm-neutral off-white ~#F6F6F7 | (estimated)(inferred) | near-white Swiss ground, subtly warm |
| ink/primary | near-black ~#0A0A0A | (estimated)(inferred) | wordmark + all feature headlines |
| ink/body | mid-gray ~#6E6E73 (system-secondary-gray-class) | (estimated)(inferred) | tagline, feature descriptions, footer |
| cta/fill | black pill, **capsule** radius | (estimated)(inferred) | single filled action; affordance carried by fill+shape, not colour |
| cta/label | white, bold, with "→" trailing glyph | (estimated)(inferred) | "Try free for 7 days →" |
| type/wordmark | bold grotesque (SF-Pro-Display-Bold / Inter-Bold-class), ~2× feature-headline size | (estimated)(inferred) | "Looq" — heavy weight, tight |
| type/feature-headline | bold, near-black, ~2× body size | (estimated)(inferred) | e.g. "Markdown rendering" |
| type/body | regular, gray, ~0.6–0.65× headline, lh ~1.45 | (estimated)(inferred) | 2-line descriptions |
| type/roles-count | ~4 distinct sizes (wordmark / headline≈tagline / body / footer) | (estimated)(inferred) | geometric-ish, <6 sizes → passes modular-scale check |
| layout/grid | 3 equal columns × 4 rows; shared column left-edges + shared row baselines; gutter ≈ 0.15× column width | (estimated)(measured) | disciplined, systematic |
| layout/measure | body columns ≈ 28–34 characters per line | (estimated)(inferred) | narrow (well under 65ch), not a fatigue risk |
| cover/aspect | 4800×2520 = 1.905:1 (≈40:21) | (measured)(inferred) | wide marketing banner |
| icon/ground | black **vertical gradient** (charcoal→black) on Big-Sur superelliptical squircle, subtle rim bevel | (estimated)(inferred) | brand context only |
| icon/motif | 5 nested concentric semicircle arcs ("rainbow"/aperture = a better *look*) rendered in **brushed-metal grayscale**, lower-centre, springing from ~65% baseline | (estimated)(inferred) | achromatic-metallic; reinforces the no-chroma brand |

## Layout skeletons

**cover.jpg — marketing feature sheet (light).** No app UI. Single-screen web/brand composite:

- *Header lockup (top-left):* `[icon squircle] · [Looq wordmark]` on one row; tagline "Built to render the rest of your files." on the row below, left-aligned to the wordmark. Icon ≈ wordmark cap-height square.
- *Feature grid (middle, ~65% of canvas):* three equal columns, four rows. Each cell = a bold near-black **headline** over a 2-line gray **description**, small headline↔body gap, large row↔row gap (clean Gestalt grouping). Reading order front-loads the strongest features per column-row: Markdown rendering / 200+ file types / SQLite browser across the top row.
- *Footer band:* black **capsule CTA** ("Try free for 7 days →") anchored bottom-left; muted "parcse.com / looq" URL anchored bottom-right — the two lower corners balanced.

## Signature moves

- **[GOLDEN-NUGGET] Total achromatic commitment — the files bring the colour.** Not a single chromatic accent appears on the entire cover: black wordmark, black CTA, gray body, off-white ground, and an icon drawn in brushed *grayscale* metal rather than a literal rainbow. For a Quick-Look/preview utility this is a *purposeful* direction, not timidity — the product is a neutral frame, and its whole value proposition ("Built to render the rest of your files") is that the rendered content (syntax themes, Markdown, Mermaid, diffs) supplies every hue. The brand deliberately withholds colour so the content can own it. This is Swiss/International restraint pushed past its own convention: the family's "one red or blue" is dropped entirely.
- **Von-Restorff CTA by fill alone.** With zero colour in play, the single black *filled* pill is the one element breaking the flat gray-on-white field — action singularity achieved through shape and value contrast instead of a saturated hue. It works, but it is worth noting the affordance rests entirely on fill+shape (no colour signal).

## Defects

- **No app UI supplied (primary corpus limitation, not an app flaw).** The only UI-adjacent asset is a marketing grid with no window — so this "digest" produces no native surface, no lineage read, no chrome/material/selection evidence. The synthesis pass must treat Looq as **brand-only** until a real screenshot arrives. *What would close it:* any single app-window shot (Markdown view, SQLite browser, or the diff table).
- **Icon is achromatic-metallic on a Big-Sur squircle, not Liquid Glass / Icon Composer** (icon evidence) → for a current-era macOS product this reads slightly dated versus the layered-glass icon idiom; internally consistent with the monochrome brand, so it sits on the signature/defect boundary rather than being a clear fault. Recorded as observation, not canon.
- **Feature-count load (soft).** Twelve feature blocks exceed the ~5-chunk working-memory comfort span; mitigated (not eliminated) by the 3-column grouping and F-pattern-friendly "name first, description second" headings. Fine for a scan/browse surface; noted, not scored against the app.
- No taxonomy anti-pattern is triggered by the composite itself — grid, hierarchy, de-emphasis, and action-singularity are all clean. The composite is **competent but conventional** (a standard App-Store/Setapp-style feature sheet); its lone distinguishing decision is the achromatic direction above.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.jpg (marketing composite — **non-native brand evidence**, cross-platform 14-pt only) | 11/14 (3 N/A) | #11 Fitts, #12 input height, #14 focus — all **N/A** (static marketing image, no interactive/native controls); all applicable structural/type/hierarchy checks pass |
| — native app surface — | — | **None supplied.** 10-point native-tells audit not runnable (no app UI). |
