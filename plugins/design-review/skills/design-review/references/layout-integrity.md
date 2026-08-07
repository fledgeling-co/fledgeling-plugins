# Layout integrity

Tier 1. Deterministic, computed from `getBoundingClientRect()` and the DOM, no visual judgment.

This file exists because of a specific failure. A review of a 14-screen app ran the full gate set, reported zero contrast failures, zero overflow, zero target-size failures, a clean semantics pass and verified keyboard behaviour — and the surface had a 250px rail misalignment, a 75px column break, a 64px header offset, a zero-gap section boundary, a 242px void, two settings lists made of non-interactive labels, and one status token carrying four unrelated meanings. Every defect was computable. None was probed.

The lesson generalises: **a gate set that stops at WCAG will go green on a broken layout, and a green gate set reads as a verdict.**

## What is probed

`scripts/probes.js` → `probeLayoutIntegrity()`, included in `runAll()`.

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

## Thresholds

All of them live in one `LI` object at the top of the layout block, so they are decided once rather than per-review. The current values were calibrated against a surface with known defects until the true positives survived and the noise stopped. If you retune, retune against a surface you already understand.

```js
columnDriftPx: 4      headerDriftPx: 8      railDriftPx: 8
zeroGapPx: 1          overlapMinPx: 3       deadSpaceRatio: 0.55
deadSpaceMinPx: 200   controlTextMax: 24    semanticTokenTexts: 3
bandMinHeightPx: 80   bandInkMinPx: 24      bandFillMin: 0.25
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
