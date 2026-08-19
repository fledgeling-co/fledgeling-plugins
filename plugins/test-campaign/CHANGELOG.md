# Changelog

All notable changes to the `test-campaign` plugin.

## 0.7.0 — 2026-08-19

A campaign could measure a repository thoroughly and a `warrant` in the same repository would
still refuse every tier, because neither plugin could read the other's state. And a case nothing
could settle resolved to `inconclusive` alongside cases an instrument merely failed to measure,
which sent half the work to the place that cannot fix it.

### Added

- **`unoracled: <reason>`, split from `inconclusive`.** The two arrive looking identical and have
  opposite remedies: `inconclusive` is an instrument problem and wants a better instrument;
  `unoracled` is a specification problem, where nothing was ever named that a check could read,
  and no instrument helps. Both hold the gate. The distinction is not new — a screenshot-judging
  pass over fifty surfaces once returned inconclusive on all fifty and the record said the
  verdicts were "for want of a judge rather than for want of an oracle", then every tool
  downstream collapsed the two halves into one status.
- **Phase 6a, oracle construction**, and `references/oracle-construction.md` behind it: a
  four-rung ladder from a specification-sourced outcome assertion, through a metamorphic relation,
  through a property-based invariant, to a recorded permanent limit in structural terms. Stop at
  the first rung that holds. Metamorphic relations are the standard answer to the oracle problem
  and the reason an unoracled case is tractable without a baseline; the evidence for them is
  directional rather than sized, and the reference says so.
- **`campaign.py export-warrant <dir> --root <repo>`** — writes `.warrant/suite-health.json` (the
  armed ratio, the effect-rung passes, the campaign's own gate) and `.warrant/oracle-coverage.json`
  (per surface, keyed by file path so warrant's `rollup_classes.py` can match it against the
  warrant's class globs). Nothing is inferred: a campaign that measured little exports little and
  the warrant still refuses the tier, which is the outcome that should follow.

### Why the export keys by path

The first cut keyed `oracle-coverage.json` by surface id, which matched no glob and rolled up to
zero coverage on every class — indistinguishable from a campaign that measured nothing. Caught by
running the full chain rather than by reading the schema. `rollup_classes.py` reads a list of rows
carrying `file`, `figures`, `sourced` and `unsourced`, and the export now emits exactly that.

### Changed

- `unoracled` is counted separately in `check` and `report`, named with its remedy in the blocker
  list, and folded into `unavailable` in the observation coverage rather than into `deferred`.

### Evidence

The two constraints on generating an oracle are measured and both are in the reference: roughly
half of LLM-generated test plans duplicate existing cases (50.5% duplicates, 22.5% invalid, 27%
valuable and new), so generation runs against a cell from the coverage model rather than
free-form; and the model that wrote the code may not be its sole oracle, because generated tests
demonstrably validate faulty behaviour and code in context biases later generation toward
mutually consistent but incorrect implementation/test pairs.
