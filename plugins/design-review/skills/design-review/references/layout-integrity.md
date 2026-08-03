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
| `columnDrift` | Rows with equal child counts whose *n*th column right-edge differs by >2px from the modal | Fixed widths that don't add up, or a wrapping cell |
| `columnHeaderAlignment` | A header row's column centres sit >8px off the body columns they label | A header grid and a row's fixed widths are two independent lists of numbers; nothing keeps them equal |
| `touchingHeadings` | A section heading whose top touches the block above it | A container sitting outside the wrapper that carries the section margin |
| `rails` | Visible `h1`/`h2`/`h3` left edges cluster >8px apart | A full-bleed region over capped-and-centred content. Diverges further as the viewport widens, so it survives a single-width review |
| `textOverlap` | Two text boxes intersect by ≥3px on **both** axes | Annotation over an axis label, badge over text, sticky header over content |
| `deadSpace` | A flex/grid row ≥200px tall whose shortest child is <55% of its tallest | A cross-axis alignment applied to a column shorter than its neighbour. At page scale this reads as generous whitespace |
| `affordance.unactionableRows` | A repeated row containing chip-shaped short text but nothing focusable | A settings list made of status labels. Every user reads them as controls |
| `affordance.pointerCursorNotFocusable` | `cursor: pointer` on something not reachable by keyboard | Mouse-only interaction |
| `tokenOverload` | A class whose name matches `warn\|error\|danger\|success\|ok\|info\|alert\|critical\|…` carrying ≥3 distinct strings | A status token that means four things has stopped being a signal — and every instance passes contrast individually, so no colour check notices |

## Thresholds

All of them live in one `LI` object at the top of the layout block, so they are decided once rather than per-review. The current values were calibrated against a surface with known defects until the true positives survived and the noise stopped. If you retune, retune against a surface you already understand.

```js
columnDriftPx: 2      headerDriftPx: 8      railDriftPx: 8
zeroGapPx: 1          overlapMinPx: 3       deadSpaceRatio: 0.55
deadSpaceMinPx: 200   controlTextMax: 24    semanticTokenTexts: 3
```

Two calibration lessons worth keeping:

**Overlap must be measured on both axes, not by area.** Adjacent inline spans abut constantly; a 1px × 15px touch is 15px² and is not an overlap. Requiring ≥3px on both axes removed ~40 false positives per screen and cost no true ones.

**Only semantic tokens can be overloaded.** A format utility — `.num`, `.t-data`, `.caption` — is *supposed* to carry many different strings. Flagging any token with many strings buries the finding that matters under the ones that don't.

## The `visible()` dependency

Every geometric probe is only as good as its visibility test. Content inside a collapsed `<details>` still returns a non-zero rect in Chrome, so a chart's table-view twin generates dozens of phantom overlaps. `visible()` therefore excludes `details:not([open])` subtrees and consults `Element.checkVisibility()` where available.

Any new geometric probe must route through `visible()` rather than testing rects directly.

## What this cannot catch

State it in Needs verification, every time:

- **Whether the alignment that holds is the right alignment.** These probes find disagreement, not wrongness. Three columns can agree perfectly on a grid that serves the task badly.
- **Optical alignment.** Mathematically aligned and optically wrong is invisible here — see `craft-visual.md`.
- **Whether a void is deliberate.** A 242px void in a hero is a defect; the same measurement in a deliberately sparse editorial layout is the design. The probe reports the geometry and the `align-items` value that produced it; the judgment is yours.
- **Hierarchy, rhythm, density, typography, copy.** None of it is geometric.
- **Anything in a state you did not drive.** These run against the DOM as it stands. An empty list, an error banner, or an open menu is a different DOM.

## Reading the output

Findings from this file are Tier 1 — deterministic, blocking. But three of them describe *disagreement*, and disagreement has two possible fixes:

- `columnHeaderAlignment` with `countMismatch: true` produces no deltas on purpose. Index-matching a 6-column header against a 7-column row (one leading with an icon) yields large, confident, meaningless numbers. When counts differ, measure the pair by hand and decide whether the header is missing a column or the row has an extra one.
- `rails` reports the clusters, not a verdict. Two rails can be correct — a full-bleed hero over capped body copy is a normal pattern. What is never correct is two rails nobody chose.
- `shapeMismatch` is restricted to horizontally-laid-out groups. A nav whose sections hold different item counts is not a defect, and the probe will not report it.
