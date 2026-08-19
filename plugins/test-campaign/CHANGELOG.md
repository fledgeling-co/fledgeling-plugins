# Changelog

All notable changes to the `test-campaign` plugin.

## 0.8.0 — 2026-08-20

A campaign published 20 surface captures and cleared every gate this plugin owned — every case
accounted for, 46 of 49 checked under the strict rule, every `-glass` lane proved and witnessed.
The captures were of three unrelated documents: a project status report, the mock browser's own
index page, and a design accessibility doc. Twenty files held **six distinct images**; four groups
of four were byte-identical. A flow step captioned "Open pairing QR code sheet" showed a
questionnaire about Apple developer credentials.

Nothing was broken. `attach-shots.py` binds a picture to a surface on a slug of its **filename**;
`evidence-page.py` rendered it with an `alt` taken from the label, so a wrong image arrived under
a right-sounding caption; `campaign.py check` ran its artifact and duplicate detectors over
`RASTER_RUNGS` case evidence only, and the `shot` field the page actually renders was inspected by
nothing. The gated part of the campaign was sound and the ungated part was the part people look
at.

### Added

- **`references/capture-lineage.md` and `capture-lineage.py`** — `warrant:oracle`'s lineage plane
  with *picture* substituted for *figure*. There, a displayed number without a `data-source-ref`
  is the defect the plane exists to find; here, a published capture without a recorded target is.
  Four passes, all exact, none needing a model: **unsourced** (no manifest entry, or no target),
  **untied** (the target does not resolve to the subject's route), **shared** (two subjects, one
  sha256, undeclared), **unjudged** (published with no `be-my-witness` verdict — this one ratchets
  rather than blocks, for the same reason `strict-check.py` ratchets).
- **`--seed-swap`**, the gate watched to fail. Swapping two subjects' manifest entries must turn
  the tie pass red; a swap that passes means the pass reads nothing and every verdict it ever
  issued is worthless. That is the campaign's own arming rule turned on its own gate.
- **Phase 8a** in `SKILL.md`, between the differential and publication.
- **A fourth failure mode** in the opening: publishing a picture of one thing under the name of
  another.
- **Twelve tests** in `tests/run.sh` covering every new blocker in both directions, plus the
  seeded swap and the manifest it borrows and restores.

### Changed

- **`campaign.py check` audits the published shots**, not only raster-rung case evidence. Three
  new blockers: a shot that is not a usable capture, a shot repeating another subject's picture,
  and a shot bound to its subject by filename alone. The verdict now prints the wall's distinct-image
  count beside its cell count, so a gallery that repeats itself says so on its face.
- **`attach-shots.py` refuses to write an attachment no capture manifest corroborates.**
  `--filename-only` proceeds and stamps `"shotProvenance": "filename"` into the inventory, so the
  weakness travels with the data rather than being forgotten at the next read.
- **`evidence-page.py` badges every rendered capture** with how its subject was established —
  *witnessed*, *manifest*, or *filename*. It also anchors a flow step on the step's **own** id
  rather than one recomputed from the loop index, which used to renumber every anchor after a
  reordered step and silently repoint links a reader had already shared.
- **`witness-worklist.py` demotes a reference that is not a raster.** The measured campaign
  reported 20 judgeable pairs, 0 blind, every reference an unrendered `.html` path and
  `evidence/shots/mock/` absent — the pair template had never run and `pairs.json` was
  hand-authored metadata describing captures nobody took. Reporting that as judgeable is what let
  the whole comparison be skipped without anything saying so.
- **`assets/capture-pairs.template.mjs` writes `captures.json` as it shoots**, recording the URL
  the browser *ended up at* rather than the one it was sent to — a redirect to a login page is
  exactly the capture that otherwise gets filed as the dashboard.

### Why the four passes are deterministic

`be-my-witness`'s `prescan.py` returns `isEvidence: true, settled: true`, exit 0 against the worst
capture in that campaign: a real, contentful, settled image of the wrong document. Image statistics
cannot answer the subject question, and frontier multimodal models reach roughly 40% recall on
fine-grained UI diffs. Provenance answers it, and only if it is recorded while the shutter is open.

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
