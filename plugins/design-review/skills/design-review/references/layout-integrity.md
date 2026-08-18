# Layout integrity

Tier 1. Deterministic, computed from `getBoundingClientRect()` and the DOM, no visual judgment.

This file exists because of a specific failure. A review of a 14-screen app ran the full gate set, reported zero contrast failures, zero overflow, zero target-size failures, a clean semantics pass and verified keyboard behaviour — and the surface had a 250px rail misalignment, a 75px column break, a 64px header offset, a zero-gap section boundary, a 242px void, two settings lists made of non-interactive labels, and one status token carrying four unrelated meanings. Every defect was computable. None was probed.

The lesson generalises: **a gate set that stops at WCAG will go green on a broken layout, and a green gate set reads as a verdict.**

## What is probed

`scripts/probes.js` → `probeLayoutIntegrity()`, included in `runAll()`.

**First, prove the page rendered at all — every probe below passes vacuously on a blank one.** An empty viewport has nothing to overflow, no rows to misalign and no text to overlap, so an all-green layout report and a page that renders nothing are the same output. This is not hypothetical: a real app shipped `@media (max-width:1000px){ .app{display:none} .gate{display:flex} }` ported from a mock whose `.gate` explainer element was never ported with it. Below 1000px `.app` was hidden, nothing replaced it, and `document.body.innerText` was fifteen characters — a black screen at 390 and 768 on every route, on which `scrollWidth === clientWidth` returned a confident PASS.

The precondition is cheap, and it belongs at the top of every viewport's run:

```js
const de = document.documentElement;
({
  inkHeight:  document.body.getBoundingClientRect().height,
  textLength: document.body.innerText.trim().length,
  visibleEls: [...document.querySelectorAll('body *')]
                .filter(el => el.getBoundingClientRect().width > 0 &&
                              el.getBoundingClientRect().height > 0).length,
  scrollable: de.scrollHeight > window.innerHeight,
})
```

A viewport whose `textLength` collapses to near-zero, or whose `scrollHeight` equals exactly the viewport height while a wider viewport scrolled to several thousand pixels, has **not rendered**. Record that as a Blocker in its own right and mark every other layout cell for that viewport `n/a: page did not render` rather than `done`. A green cell there is worse than an open one, because it is evidence of the wrong thing.

Where the cause is a media query hiding a container, check whether the element it reveals actually exists — `display:none` on the app plus a `.gate` that was never ported is a whole-page failure that greps clean in the stylesheet, since the rule itself is correct and only its counterpart is missing.

Almost every defect here lives inside a **repeated group** — any container with three or more visible element children sharing a class signature. A table body, a card grid, a settings list, a nav. `findRepeatedGroups()` finds them; the rest of the probes reason over them. The count is reported so you can tell "no findings" from "nothing matched".

| Check | Fires when | The defect |
|---|---|---|
| `shapeMismatch` | Sibling rows in one horizontal group hold different child counts | An optional element (a button that only some rows need) takes width from every column before it |
| `columnDrift` | Vertically-stacked rows with equal child counts whose *n*th column right-edge differs by >4px from the modal | Auto-width text columns in a flex row, or fixed widths that don't add up |
| `columnHeaderAlignment` | A header row's column centres sit >8px off the body columns they label | A header grid and a row's fixed widths are two independent lists of numbers; nothing keeps them equal |
| `touchingHeadings` | A section heading whose top touches the block above it | A container sitting outside the wrapper that carries the section margin |
| `rails` | Visible `h1`/`h2`/`h3` left edges cluster >8px apart | A full-bleed region over capped-and-centred content. Diverges further as the viewport widens, so it survives a single-width review |
| `textOverlap` | Two text boxes intersect by ≥3px on **both** axes | Annotation over an axis label, badge over text, sticky header over content |
| `deadSpace` | A flex/grid row of side-by-side children, ≥200px tall, whose shortest child is <55% of its tallest | A cross-axis alignment applied to a column shorter than its neighbour. At page scale this reads as generous whitespace |
| `columnVoids.voids` | A top-level band that renders at height 0, paints no ink at all, holds under 24px of ink in a box over 80px, or fills under 25% of its own height | A section that renders nothing still occupies its own margins. See below |
| `columnVoids.seams` | Never fires — it is the band-rhythm table, reported unfiltered | The whole-page form of the same defect, which no single band trips |
| `implicitTracks.spilledRows` | A grid with unequal columns holds more children than it declares tracks, and the trailing row holds fewer children than there are columns | The row template was written for N children and renders N+1, so `grid-auto-flow` invents a row. See below |
| `implicitTracks.emptyCells` | A grid child computes to zero width or height | An element emitted for a field the record does not carry. It occupies a track and paints nothing |
| `dividerProximity.violations` | A text **ink box** sits closer than 24px (16px under 900px wide) to a visible vertical rule | The rule reads as attached to the words rather than as the boundary between two cells. See below |
| `dividerProximity.crossings` | Text runs through a rule | The divider is drawn over the words |
| `dividerProximity.clipped` | A text ink box extends past an ancestor that clips or scrolls horizontally | The last cell of a too-tight row loses its final words. **Under-reports on Obscura** — see below |
| `affordance.unactionableRows` | A repeated row containing chip-shaped short text but nothing focusable | A settings list made of status labels. Every user reads them as controls. **Tier 2, not a gate** — see below |
| `affordance.pointerCursorNotFocusable` | `cursor: pointer` on something not reachable by keyboard | Mouse-only interaction |
| `tokenOverload` | A class whose name matches `warn\|error\|danger\|success\|ok\|info\|alert\|critical\|…` carrying ≥3 distinct strings | A status token that means four things has stopped being a signal — and every instance passes contrast individually, so no colour check notices |

## The column void — the defect `deadSpace` is structurally blind to

`probeDeadSpace` requires a **row**: side-by-side children of unequal height. The most common form of dead space on a marketing or content surface is a **column** defect and matches none of that — *a section that renders nothing still occupies its own margins*, so "no content" becomes 200px of dead space rather than an absence. A tenant with no video gets an empty video band rather than one fewer band; a disabled section collapses to zero height instead of being removed; a notice band ends up as 184px of padding around 104px of content.

`probeColumnVoids()` measures each top-level band's box against the union bbox of its actual **ink** — text run fragments, replaced elements, and any box carrying a border or a painted background. Boxes lie here in a way ink does not: a band whose only child is a full-height empty wrapper has a perfectly healthy `getBoundingClientRect()`.

Two outputs, answering different questions:

- **`voids`** — the flagged bands, by kind: `zero-height`, `no-ink`, `near-empty`, `low-fill`.
- **`seams`** — every band's height, ink height, fill percentage and **ink-to-ink gap from the previous band**, reported unfiltered. This is the one that finds the whole-page form. A surface whose seams read 92px, 205px, 229px has no single band that trips a threshold and is still three-quarters dead space; only the table shows it. Read it against the surface's own healthy rhythm — one real reference build sits at 49–62% fill, and 36% on the same system is the finding.

`low-fill` is the judgement-required kind and is deliberately noisier than the others: a deliberately sparse editorial foot and a section that lost its content measure identically. The probe reports the geometry; you decide. `zero-height` and `no-ink` need no judgement.

## The implicit track — the defect a screenshot reads as padding

`grid-template-columns: auto 1fr auto auto` and **five** children. `grid-auto-flow: row` is the default, so the fifth child lands on a row nobody authored, and nothing warns — not the browser, not the linter, not the diff.

The real instance: an index row's trailing arrow sat underneath its row number, on **every row, of every tenant, at every width**. Computed `grid-template-rows: 27.5px 16px` where one track was intended; 93px rows that should have been 61px; roughly 450px of dead height on a single governance page. It survived every look because a 16px orphan row reads as generous padding, and it survived the site's parity oracle because that oracle loaded `/`, where no index row exists (`parity-oracle.md`). The `@media (max-width: 640px)` variant dropped to three tracks against four remaining children — the same bug, one column narrower.

`probeImplicitTracks()` measures it from computed geometry, and the discrimination is the whole design:

- **Equal columns are a gallery and are skipped.** `1fr 1fr 1fr` means wrapping is the point and a ragged last row is a layout decision. An **unequal, content-sized** track list is a template for one row, and a child past the end of it is an orphan.
- **A full last row is wrapping that works.** The probe fires only when the trailing row holds *fewer* children than there are columns.
- **`shortOrphan`** is reported, not gated: an orphan row is usually much shorter than the rows above it because it holds one small thing. Treat `shortOrphan: true` as confirmation, not as the test.
- **`repeatedInstances`** counts the same class signature across the page. That number is what turns 16px into 450px, and it belongs in the finding.
- **`wouldBePx`** is the row height with the orphan track removed — the fix's payoff, measured, before you make it.

`emptyCells` rides along because it is the same defect one field earlier: a grid child computing to **zero width or height** is an element emitted for something the record does not carry. The real instance was `<time datetime="">` — invalid *and* empty — in a date column, on all thirteen rows of a page whose documents have no dates, while the `.idx--undated` variant that would have dropped the column sat in the stylesheet, commented, applied by nothing. Note the probe cannot use `visible()` here: that helper requires a non-zero rect, and the zero rect **is** the finding.

Fixtures: `evals/fixtures/implicit-tracks.html` and its control `implicit-tracks-clean.html`. The defective one returns `spilledRows: 4, emptyCells: 4`; the control returns `0, 0`; and neither reports the healthy four-card / three-column grid on the same page. A probe that fires on the control is miscalibrated and a probe that fires on neither never ran.

## The divider gutter — the defect that passes every check by construction

A stat row divided into three cells. The label and the number begin immediately to the right of each rule. Contrast passes, nothing overflows, the columns are even to the pixel, the grid is a textbook `repeat(3, 1fr)` — and the row reads as a table that was squeezed rather than a set of cells that were spaced.

**The reason no gate caught it is worth stating exactly, because it generalises.** The gutter is declared on one element and the rule is painted on another. A cell with `padding-left: 24px` carrying its own `border-left` satisfies any element-box check trivially: the padding *is* the gap, measured from the element's own edge. But the number a reader perceives is the distance from the **ink** to the line, and between those two numbers sit the cell's inner wrapper margins, the text element's own box, and — the case that bites — a neighbouring cell whose `padding-right` is a different value from its `padding-left`. The declared gutter and the perceived gutter are two different measurements, and only one of them is on screen.

So `probeDividerProximity()` measures ink. `Range.getClientRects()` on each text node returns one box per line box, which also means wrapped text is measured where it actually lands rather than where its container starts.

Three rule shapes are found:

- **`border-left` / `border-right`** on any visible box over 24px tall. This is how nearly every divided row is built.
- **Element rules** — an `<hr>`, `[role="separator"]`, or anything classed as a divider that computes to under 3px wide and over 24px tall.
- **`column-rule`**, which is reported rather than measured. The line sits between generated column boxes that have no node to measure, so the probe returns the column gap, the rule width, and whether `(gap - rule) / 2` clears the threshold. Saying "unmeasurable, check by eye" is the honest output; silence would read as a pass.

`declaredPadPx` is reported beside every violation precisely so the gap between declared and perceived is visible in the finding. A real page in this portfolio returned `gapPx: 14.5` against `declaredPadPx: 14` — the padding was doing what it said and was simply below the floor — while another returned `gapPx: 14.3` against `declaredPadPx: 0`, where the gutter came from somewhere else entirely and nobody had decided it.

**Two numbers, deliberately.** `dividerGutterPx: 16` is the floor — below it the layout is wrong. `dividerGutterWantPx: 24` is what a divided cell should carry at 900px and wider, and is what the probe reports against. Violations carry `belowFloor` so the blocking set and the attention set stay separable.

Calibration: the fixture pair is a three-cell row at `padding: 5px` and the same row at `32px`. The tight row returns 15 violations — three text elements against five (cell, rule) pairs, since each cell's text is measured against both the rule on its own left edge and the rule on the next cell's — and the roomy row returns none. A probe that fires on the roomy row is measuring boxes again.

**Engine caveat, measured 14 Aug 2026.** On Obscura, a `overflow-x: hidden; white-space: nowrap` box whose text is wider than it reports `overflowX` as `auto` and clamps the text node's own client rect to the container width, so the overflow is arithmetically invisible. `evals/fixtures/divider-clipped.html` renders with two of its three cells cut mid-word — "340 observations across 28 consecutive windo", "of every token sent, measured at the boundar" — and the probe returns `clipped: 0` on that render. The screenshot and the probe disagree, and the screenshot is right.

That fixture is worth keeping for the general lesson rather than only for this probe: a page can be visibly broken and arithmetically clean on the engine measuring it, which is why this skill's rule is to open the capture and ask what is wrong with it rather than to read an exit code. `clipped` under-reports on Obscura and an empty array there is a known blind spot, not a pass. The gap measurement itself is unaffected and was verified correct to a tenth of a pixel against a fixture whose expected value was known.



All of them live in one `LI` object at the top of the layout block, so they are decided once rather than per-review. The current values were calibrated against a surface with known defects until the true positives survived and the noise stopped. If you retune, retune against a surface you already understand.

```js
columnDriftPx: 4      headerDriftPx: 8      railDriftPx: 8
zeroGapPx: 1          overlapMinPx: 3       deadSpaceRatio: 0.55
deadSpaceMinPx: 200   controlTextMax: 24    semanticTokenTexts: 3
bandMinHeightPx: 80   bandInkMinPx: 24      bandFillMin: 0.25
dividerGutterPx: 16   dividerGutterWantPx: 24
```

Five calibration lessons worth keeping. Every one came from driving the set to
convergence on a real surface: once the true defects were fixed, everything
still firing was a probe defect.

**Orientation is not optional.** `columnDrift` and `deadSpace` both assumed a
shape the DOM does not guarantee. Drift compared the *n*th child across the
members of horizontal groups, where the members *are* the columns and their
edges are supposed to differ — 40 findings, 13 real. Dead space fired on flex
columns, where uneven child heights are the point. Both now check the axis.

**A header candidate needs three tests, not one.** Walking to the previous
sibling latches onto a filter bar, a card head, a section heading. It must:
descend into a wrapper to find the header inside it, start its first column
where the body's starts, and be rejected outright when *any* column is off by
more than 10× the threshold — a real header is nearly aligned and drifts a
little, never wildly.

**Sub-pixel is not a finding.** `columnDriftPx` at 2 fires on layout rounding
and text metrics. 4 is the floor where a person can see it.

**Overlap must be measured on both axes, not by area.** Adjacent inline spans abut constantly; a 1px × 15px touch is 15px² and is not an overlap. Requiring ≥3px on both axes removed ~40 false positives per screen and cost no true ones.

**Only semantic tokens can be overloaded.** A format utility — `.num`, `.t-data`, `.caption` — is *supposed* to carry many different strings. Flagging any token with many strings buries the finding that matters under the ones that don't.

**Containers own their own spacing.** `rails` counted headings inside cards and
panels, which are indented by their container and say nothing about whether the
page's regions agree. `touchingHeadings` flagged a card head touching its own
body. Both now exclude the inside of a card.

## The `visible()` dependency

Every geometric probe is only as good as its visibility test. Content inside a collapsed `<details>` still returns a non-zero rect in Chrome, so a chart's table-view twin generates dozens of phantom overlaps. `visible()` therefore excludes `details:not([open])` subtrees and consults `Element.checkVisibility()` where available.

It also drops zero-width elements, which has a consequence worth knowing before
you act on a `shapeMismatch`: **a cell reserved to hold a column, but rendering
empty, is not a fix.** It collapses, `visible()` drops it, and the row's shape
still fails to match its siblings. Give a reserved cell a `min-width`/`min-height`
or real content.

`textOverlap` additionally uses `getClientRects()` rather than the bounding box:
an inline element that wraps returns a rect spanning both line fragments, and so
"overlaps" everything sitting between its two lines.

Any new geometric probe must route through `visible()` rather than testing rects
directly, and must use per-fragment rects for anything inline.

## Report each sub-check's scope beside its zero

There are thirteen sub-checks here, and on a real surface most of them return zero.
Measured on `evals/fixtures/landing.html`, 18 Aug 2026: **12 of 13 returned 0 at
all seven viewports, and two of those zeros sat over defects that were genuinely
computable** — a five-way left-rail disagreement measuring 15/43/32/32/0/24px, and
a hero at 30% fill carrying a 747px void.

Neither was a bug. `probeSharedRails()` clusters `h1`–`h3` only and excludes
anything inside a card, panel or dialog, so a rail disagreement between card
interiors is outside its population by design. `probeDeadSpace()` needs a row to
measure across, and the hero is a column. **Both were working exactly as
documented and blind to the defect anyway** — which is the whole problem, because
the output gave a reader no way to tell that from a clean surface.

So the aggregate `layoutFindingCount` is not a verdict on the layout, and must
never be offered as one. Report the sub-checks individually and put each zero
beside the population it examined:

```
rails            0   examined 4 page-rail headings (h1-h3, card interiors excluded)
deadSpace        0   examined 6 rows (columns are outside this check)
columnVoids      2   examined 5 bands
textOverlap      0   examined 41 ink boxes
dividerProximity 0   3 rules found, 2 side borders excluded as box outlines
```

A zero with its denominator is a result. A zero on its own is the same output a
broken probe produces, and this file exists because a review went green on a
surface carrying five computable layout defects.

Two of the thirteen have a stated scope narrow enough that a defect of their own
kind can hide outside it — rails and dead space, above. When a surface's structure
puts the interesting geometry outside a check's population, say so in **Needs
verification** rather than only in your own reasoning: *"rail alignment across
card interiors was not measured — the probe clusters page-rail headings only."*

## Cluster by root cause before reporting anything

Geometry inflates, and the published numbers are larger than intuition suggests. **ReDeCheck** (Walsh, Kapfhammer & McMinn, ISSTA 2017) modelled 26 live pages across viewport widths from DOM coordinates and found 33 distinct responsive layout failures — while reporting **137 distinct viewport ranges**, i.e. 4.2 viewport inspections per real failure. On one page it produced **147 small-range findings that collapsed to a single underlying failure.**

This skill's own measured rate on one 14-screen surface — 2 real, 35 false — sits in the same range, which is mild evidence it was not a fluke of one bad page.

ReDeCheck also names the four mechanisms, and every one of them is reachable by the probes in this file:

- a collision caused only by **invisible padding** — the boxes touch, the ink does not;
- a protrusion that is **non-observable** because `overflow: hidden` clips it;
- **coincidental alignment** mislabelled as a defect;
- a **row inferred incorrectly**, producing a wrapping false positive.

**Verve** (Althomali et al., *STVR* 2021) exists specifically to sort DOM-reported layout failures into true positive, false positive and **non-observable**. That third category is the one prose loses and the one that matters here: a finding can be geometrically real and visually absent.

So: one finding per `{mechanism, root component, UI state, viewport interval}`, with repetition carried as a count rather than as rows. `run_review.py` prints `layoutRootCauseCount` beside `layoutFindingCount` — 15 findings resolving to 4 root causes is the normal shape — and the report ranks the clustered number. Collapse descendant events into their parent: two overlapping boxes inside one broken card is one broken card.

The ceiling worth knowing about: **VizAssert** (PLDI 2018) formalises the browser rendering algorithm and verifies layout assertions across *all possible* renderings rather than a sampled few, covering 14 accessibility and usability guidelines. That is what a provable layout check looks like. Everything in this file samples viewports instead, which is why the findings here are prompts with measurements attached rather than proofs.

## `affordance.unactionableRows` is Tier 2

Measured over-fire rate on one 14-screen surface: **2 real, 35 false**. It found
both genuine cases — two settings lists whose only control was a `<span>` — and
flagged every status pill on the product: `Synced`, `Confirmed`, `Estimated`,
`Not yet`, `Registered`, `4/4 evidence`, a date.

The difference between "this chip is a setting" and "this chip is a status" is
semantic and is not in the DOM. Both are a rounded box with a short string in a
row's trailing column.

So treat it as a prompt to go and look, never as a blocking finding. The
question it answers well is *"which rows would a user try to click?"* — and that
list is worth reading even when most of it is fine.

**One engine-specific false positive on this probe.** Obscura does not render native form controls at all, so a real `<input type="radio">` renders as nothing — which is exactly the shape this probe fires on: a repeated row with chip-shaped text and nothing focusable. Before reporting an affordance finding on a row that should hold a native control, grep the source for `input type="radio|checkbox|range|color|date"` and report the check as unavailable for that row rather than as a defect.

## Fixed chrome over content — check it separately

Every overlap probe here compares elements *in the same flow*. Position-fixed chrome — a sticky header, a cookie bar, a floating action button, a media control bar, a chat launcher — is in no flow at all, so it occludes content while every overlap, overflow and dead-space check reports clean. The content is not overflowing anything; something is sitting on top of it.

It is one measurement, and it belongs in the gate set:

```js
const fixed = [...document.querySelectorAll('body *')]
  .filter(el => getComputedStyle(el).position === 'fixed' && visible(el));
// for each fixed box, intersect against text/interactive boxes beneath it
```

Two things make this bite in practice. It is **viewport-dependent** — chrome pinned at `bottom: 28px` clears the content at 1280×1024 and lands on it at 1920×1080, so a single-viewport pass proves nothing. And the occluded element is often chrome itself (a page number, a footer rule, a legal line), which reads as unimportant right up until it is the disclaimer a regulator expects to see.

Report it as an overlap finding, not a z-index note: the consequence is content the user cannot read, and severity follows what got covered.

## What this cannot catch

State it in Needs verification, every time:

- **Whether the alignment that holds is the right alignment.** These probes find disagreement, not wrongness. Three columns can agree perfectly on a grid that serves the task badly.
- **Optical alignment.** Mathematically aligned and optically wrong is invisible here — see `craft-visual.md`.
- **Whether a void is deliberate.** A 242px void in a hero is a defect; the same measurement in a deliberately sparse editorial layout is the design. The probe reports the geometry and the `align-items` value that produced it; the judgment is yours.
- **Hierarchy, rhythm, density, typography, copy.** None of it is geometric.
- **Anything in a state you did not drive.** These run against the DOM as it stands. An empty list, an error banner, or an open menu is a different DOM.
- **Anything measured before the page settled.** Every probe here reads geometry, and geometry is a function of time on a surface with an entrance animation or scroll-triggered reveal. Scroll the document and drain `document.getAnimations()` first; `runAll().settled` records whether that happened. A void probe run at load reports every unrevealed band as `no-ink`.

## Reading the output

Findings from this file are Tier 1 — deterministic, blocking. But three of them describe *disagreement*, and disagreement has two possible fixes:

- `columnHeaderAlignment` with `countMismatch: true` produces no deltas on purpose. Index-matching a 6-column header against a 7-column row (one leading with an icon) yields large, confident, meaningless numbers. When counts differ, measure the pair by hand and decide whether the header is missing a column or the row has an extra one.
- `rails` reports the clusters, not a verdict. Two rails can be correct — a full-bleed hero over capped body copy is a normal pattern. What is never correct is two rails nobody chose.
- `shapeMismatch` is restricted to horizontally-laid-out groups. A nav whose sections hold different item counts is not a defect, and the probe will not report it.
