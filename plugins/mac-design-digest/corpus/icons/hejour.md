# Icon: Hejour

- **Era:** Big Sur unified (squircle format) — but a **flat, depthless variant** that strips the era's lighting kit · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/hejour/icon.png`, SHA-1 `5c3f6462`) · **Category:** Writing
- **Resolution caveat:** delivered **1221×1107, non-square** — a resized web render, not the 1024² master. Aspect is slightly distorted, so inner-card *proportions* are `(estimated)`; the flat fills sample cleanly so **palette hex are reliable `(measured)`**.

| Dimension | Reading |
|---|---|
| Background | **Flat** canary/lemon yellow `#FEE90A` — full-bleed, verified flat (corners + centre sample identical, no ramp) |
| Glyph | **Abstract checkmark**, carried as a **knockout** — the yellow field showing through the white card, not a painted stroke. Sits lower-right within the card; card itself is optically centred |
| Overlay device | **Frame / inner card** — a white squircle (`#FFFFFF`) echoing the system mask shape, holding the knockout glyph |
| Light model | **None — pure flat fills.** No modeled light source, no baked micro-shadow, no specular, no gradient. One consistent (absent) light model |
| Layer stack | back→front: (1) flat yellow field `#FEE90A` full-bleed base → (2) white squircle card `#FFFFFF` centred inner plane → (3) checkmark knockout (yellow field revealed *through* the card — negative space, not an added front layer) |
| Palette economy | **1 hue family** (yellow) + white. No accent beyond the field colour. As economical as an icon gets |

## Signature devices
- **Squircle-in-squircle** `[GOLDEN-NUGGET]` — the inner white card repeats the system mask's superellipse, a "card within the tile" motif. Nameable and confident.
- **Knockout glyph** `[GOLDEN-NUGGET]` — the checkmark is negative space (background bleeding through the card), so the glyph and the field are the *same* colour. Economical, but it makes figure-ground entirely value-fragile (see Failures).
- **Mono-hue-plus-white** — single committed brand colour, zero gradient, zero depth. A deliberate flat-App-Store reading over any Big Sur modeling.

## Failures
- **#7 Figure-ground contrast — FAIL.** White card vs yellow field measures **1.24:1** `(measured)`; the yellow-on-white checkmark is the same 1.24:1 inverted. Both pairings are high-luminance, so **in grayscale the card and its checkmark nearly vanish** — the icon depends 100% on the small hue difference between yellow and white. This is the icon's central weakness.

## Soft passes (flagged, scored as pass)
- **#3 Silhouette** — subject is nameable ("a check card"), but only via hue knockout; filled solid the whole icon is a plain rounded square. Value-dependent, not silhouette-robust.
- **#4 16px squint** — the bold white tile on yellow survives; the checkmark *detail* risks washing at menu-bar size because its value contrast is nil. The thick stroke saves it, barely.
- **#5 Single light model** — passes only because there is no light at all to be inconsistent; flatness itself is a choice, not a modeled light.
- **#9 Era coherence** — internally consistent flat language, but it borrows the Big Sur **squircle format without any Big Sur depth**, and adopts **no Liquid Glass treatment** — so against macOS 26 it reads a generation behind the current-era icon language.
- **#10 Variant robustness** — the composition (white card + check hole) would survive as pure *shape* in dark/tinted, but this is a single flat bitmap, **not an Icon Composer layered/glass icon**; its whole identity is the yellow field colour, which tinting would overwrite.

## Notes for synthesis
- **Icon↔app palette disconnect:** the icon commits to canary yellow `#FEE90A`, but the app UI (from cover) is a dark charcoal editor (`#1E1E1E`, matches the kit dark window bg) with a **green** task-completion accent (~`#49901A`/system-green family) `(estimated)`. **The icon's yellow appears nowhere in the product interface** — weak brand coherence between face and app.
- **Off-subject glyph:** a checkmark reads "to-do / done." Hejour is a *day-based notebook / writing* app; the checklist is one facet (visible in cover), so the icon communicates the todo sliver, not the "journal / daily page" core. Slightly mis-aimed subject-mining for a Writing-category app.

## Rhymes with
- (No prior icons in corpus yet.) Style-family hint: **flat iOS-superellipse knockout icons** — a single glyph knocked out of a saturated single-hue flat field; the checklist/todo-app vernacular (checkmark family, Things-adjacent motif but flatter and without depth). Watch for other flat-mono-hue indie icons to form a cluster.
