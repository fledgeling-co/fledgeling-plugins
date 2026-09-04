# Evidence

Every zone on both pages traces to a count in a corpus of real status reports, and the two
corrections the renderer applies trace to specific errors observed being made and then
retracted. This file records where those numbers come from and what they do not establish.

## The corpus

Mined 2026-09-04 from Claude Code session transcripts under
`~/.claude/projects/`, covering the preceding 14 days.

| | |
|---|---|
| transcripts matched | 580 of 8,844 in the window |
| genuine status-report turns extracted | 1,193, after filtering echoed skill text |
| report units read by the mining lanes | 2,400 |
| mining lanes | 25 (23 corpus shards, 1 heading-frequency pass, 1 over six real report HTML artifacts) |
| distinct reporting concerns after merge | 634 |
| total occurrences | 8,959 |
| distinct metrics | 421 |
| distinct table shapes | 119 |
| projects represented | 27 |

Extraction filtered out skill-file text echoed into transcripts by fingerprinting heading
sets and dropping any shape appearing in more than four files, so the counts describe what
agents *wrote as reports* rather than what they quoted from their own instructions.

## The finding the pages are built around

Nine mining lanes independently reported the same structural fact, unprompted and in their
own words:

- *"Confession-first, not achievement-first: the single most consistent section after the
  headline is a self-correction block, and it is usually given more space than the wins."*
- *"11 of 20 entries open or pivot on a correction to what I told you."*
- *"It appears in ~15 of 38 turns and is never a footnote."*
- *"12 of 40 turns contain an explicit retraction of something the same agent said earlier."*

The corrections block carries the same four atoms every time: the earlier claim, the true
state, the mechanism that produced the error, and the check that caught it. That is why
`corrections` is a first-class zone with four columns rather than an appendix, and why it
renders an explicit empty state instead of being hidden — an absent zone and an empty one
read differently.

A second habit decides the visual grammar: *"numbers set against a named bar (10.03:1 vs
≥3:1, 57 observed vs 11 tolerable) — the bar, not the number, does the work."* The same
lane named the decoration to avoid: *"bare proportional bars duplicating an adjacent
percentage; masthead badges restating the h1; TOC on a page already scanned by heading."*

## Zone occurrence counts

Concerns were clustered from the 634 by keyword rules. The clustering leaks at the margins —
`per item status ledger` (113 occurrences) landed under FLEET on a field-name match — so
**rank order is reliable and per-cluster totals carry roughly ±15%**.

| cluster | occurrences | share |
|---|--:|--:|
| fleet and wave state | 1,335 | 14.9% |
| headline verdict | 1,007 | 11.2% |
| checks and gates | 898 | 10.0% |
| armed / falsifiability | 671 | 7.5% |
| self-correction | 626 | 7.0% |
| owner actions | 600 | 6.7% |
| findings and defects | 594 | 6.6% |
| verification verdicts | 475 | 5.3% |
| remaining work | 369 | 4.1% |
| limits and not-checked | 339 | 3.8% |
| delivered | 325 | 3.6% |
| git and branch state | 314 | 3.5% |
| reconciliation | 276 | 3.1% |
| deliberately not done | 246 | 2.7% |
| artifacts | 153 | 1.7% |
| tests and coverage | 151 | 1.7% |
| machine resources | 80 | 0.9% |

Roughly 80% of observed occurrences are placed in a zone. Concerns given no zone on purpose:
spec and board-card state (116 — belongs to the tracker), skill-invocation receipts (~90 —
process evidence about how the agent ran, not project state), research lanes (~40 —
session-scoped), lessons learned (~35 — belongs in memory files), per-package test counts
(~50 — the scalar is in checks, the breakdown belongs in the test tool's own output).

## The two corrections the renderer applies

Both are errors observed in the corpus being made and then retracted in a later report, so
the script fixes the data rather than trusting it.

**A check that examined nothing is not a pass.** A gate reporting `exit 0` over a zero
denominator was recorded as passing, and the retraction came later. `render.py` forces any
check with `state: "done"` and counts of `N/0` to `unmeasured`. Caught immediately in
testing: the sample data authored for the templates itself claimed `done` over `0/0`.

**An alarm that caught nothing is not armed.** An `armed` row asserting the check was
proved able to fail, while recording zero failing tests under the deliberate fault, is a
contradiction. `render.py` forces `armed: false` when `red` is 0.

## What this does not establish

- **No independent critic walked the taxonomy.** The workflow's completeness-critic agent
  stalled and was killed. The 80% coverage figure and the zone selection are self-reported by
  the pass that produced them.
- **The corpus is one developer's 14 days.** These are the reporting habits of Claude Code
  agents working in one portfolio, not a general finding about status reporting.
- **No measurement compares these pages against the chat updates they replace.** The claim
  that a page is more useful than a scrolling message is a design position taken from the
  corpus's own shape, not a result. `EVALS.md` records what was and was not run.
- **Dark mode, print and reduced-motion are source-level claims.** The rules are in the
  templates; Obscura accepts `Emulation.setEmulatedMedia` and does nothing, so nothing
  rendered proves them.

## Provenance of the templates

`assets/project-template.html` and `assets/dashboard-template.html` were authored by
`claude-opus-5` against the mined specification, through `visualization:visualization`,
`design-craft:design-craft` and `ux-craft:ux-craft`, with plain-language rules taken from
`eli5:eli5`. The chart forms — Sankey, dumbbell, beeswarm, slopegraph, treemap, heatmap
strip, stacked bar — are the visualization skill's own catalogue.

Two compromises in those files are declared rather than hidden. The checks bars share one
axis by normalising each value to its own limit, so bar length alone does not carry
direction when some limits are floors and others ceilings; the wording and colour do. And
findings are positioned by a 0–100 score that the underlying data does not have at that
precision — the contract carries `score` explicitly so the invention is visible rather than
implied.
