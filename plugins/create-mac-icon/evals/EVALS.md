# How create-mac-icon was tested

Three process evals live in `evals.json`. They assert what's on disk after a
run, not what the run says about itself: an independent grader opens the
files, re-runs the checks, and quotes evidence. Two of the three ran on day
one (the third, iterate-against-a-reference, is exercised continuously by the
marketplace's own icon loops, which is where it came from).

## The report card

| Run | What it tested | Result |
|-----|----------------|--------|
| Full commission ("Ledgerline") | The whole pipeline with all three engines and the fidelity loop | 6 of 6 assertions passed |
| Honest degradation ("Kilnhand") | The pipeline with no image model available | 4 of 4 assertions passed |

Grading evidence: `results/iteration-1/` (each grading.json quotes the file
contents or command output that decided every assertion; the DELIVERY notes
are the runs' own accounts).

Highlights the grader verified rather than trusted:

- The Ledgerline master regenerated from its build script **byte-identical**
  to the shipped SVG, and re-passed the structure gate independently.
- The fidelity loop ran a baseline plus four rounds, total composite 1.273 to
  3.163, with the full trajectory on disk.
- The Kilnhand run stated its missing engines plainly, shipped three
  genuinely different hand-authored takes, applied three recipe-library
  constructions identifiable in the SVG source, and made no fidelity claim
  since no reference existed.

## The finding that changed the skill

The Ledgerline run surfaced something the research had predicted only
half of: the Pareto gate accepted a round that failed the 12-point rubric,
because the raster reference *itself* fails a rubric check (its frosted glyph
measures about 1.4:1 figure-ground, which dissolves at 32px). Converging on a
flawed reference dragged the master to 1.02:1. The fix, and the rule now in
`references/fidelity-loop.md`: the gate informs, the rubric decides shipping,
and the next edit gets bounded to regions the rubric doesn't police. The
construction that satisfied both (the bounded frost fade) is in
`references/material-recipes.md`.

## Caveats, stated rather than buried

- Two single runs carry sampling noise; the assertions check artifacts, not
  taste. Aesthetic quality is judged by the audit rubric and the blind panel
  (`scripts/judge_panel.py`), not by these evals.
- No baseline (skill-less) comparison ran: these are process evals measuring
  pipeline compliance, and a skill-less run trivially fails most assertions
  by never producing the artifacts. That asymmetry is the point, and it's why
  the numbers above shouldn't be read as a quality delta.
- The eval runs write to their own workspaces; merging their proposed recipe
  entries into the live library is the orchestrating session's job, on
  purpose (the Kilnhand run declined to self-append unconfirmed findings,
  which is the contract working as written).
