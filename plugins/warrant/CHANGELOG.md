# Changelog

All notable changes to the `warrant` plugin.

## 0.2.0 — 2026-08-19

The planes could not tell a missing oracle from a missing judge, and `lot` would size a sample
over a suite nobody had measured. Found by running the pipeline on a real 211-item Done column:
143 items came back unverifiable in either direction and nothing could say why or what to do
about it.

### Changed

- **`lot_plan.py` refuses without `.warrant/suite-health.json`** — exit 3, naming `assay` as the
  step that produces it. Every number a plan produces is a number about items whose evidence is
  the test suite, so the plan inherits that suite's fault sensitivity, and more than half of over
  15,000 generated mutants survived a passing suite (`C18`). The forced order was written in the
  skill's prose and enforced nowhere; a run that skipped `oracle` and `assay` and went straight
  to `panel` passed every gate, then measured its own reviewer at 2-of-8 seed recall — the number
  the skipped plane existed to predict. `--unmeasured-suite` plans anyway and records the
  omission in the plan and on every run, the same way `--rate` records an override.
- **`lot_report.py` requires a sixth field: `oracle_mix`.** Absent is exit 2, like the other five.
  The skill already said in prose to "say which classes the audit covered", citing `C6` — roughly
  three quarters of what code review finds is not functional — and prose does not gate. The
  renderer now says so explicitly when no sampled case stands on an effect rung, rather than
  leaving a reader to notice that a lot was audited on whether surfaces looked right.
- **`ratchet.py` emits a work order instead of only a refusal.** `oracle_coverage` now carries the
  class's surface globs, the file that would satisfy it, and the two commands that produce it. It
  knew all of this and printed none of it, so a permanently-refused tier read as a verdict rather
  than as a finite task list. It does not walk the filesystem to do this: a 60k-file repository
  already timed out a scan during the run that prompted the change.
- **`warrant`'s forced order gains a step 0: `test-campaign`.** `oracle` and `assay` *measure*
  oracles and neither creates one, so a repository whose surfaces were never given a checkable
  property cannot climb past tier 0 however often the planes run. Absent evidence is an unmet
  condition here by design, which makes "never measured" and "measured badly" identical to
  `charter_validate.py`.

### Fixed

- The `lot-result.valid.json` fixture carried five fields and is now six, so each selftest that
  deletes one key still observes every field firing on its own.

### Evidence

`C18` (mutant survival), `C6` (the non-functional majority of review findings) and `C19` (rates
travel with their denominators) already sat in `references/evidence.md`; none of them was gating
anything. This release makes three of them checkable. `C1` is untouched and still bounds
everything: no powered non-inferiority reader study exists for code review or UI acceptance, so
there is no measured human baseline and none of this creates one.

## 0.1.0 — 2026-08-19

First release. Eight skills, a router, twenty-six scripts and eight reference documents, built from
a research panel commissioned for the `deputy.fledgeling.app` page and reused here rather than
re-run.

### Added

- **`warrant`** — the router and map: the eight skills, the forced order of the planes, the
  authority ladder, and what the pipeline deliberately is not.
- **`charter`** — writes and validates `.warrant/warrant.toml`, the only human-signed artifact.
  `charter_validate.py` is the outermost gate; nothing else runs without it.
- **`oracle`** — the deterministic plane: source-to-render lineage, tick-and-tie against the
  originating record, taxonomy validation. It runs before the model plane because the
  highest-consequence defect is a correctly rendered screen stating an unsupported figure, which no
  vision judge can see.
- **`assay`** — mutation survival over the tests CI actually selects, an eight-pattern scan for
  assertions that cannot fail, and the authored-versus-selected gap by surface.
- **`panel`** — one out-of-family grader, orthogonal lens lanes, and an adjudicator that routes a
  disagreement to the deterministic check that settles it. Evidence is snapshotted and
  content-addressed before anything judges it.
- **`feedback`** — escapes become permanent regression cases, and the corpus is the tier-2 entry
  condition. Replaces the prospective reader study an earlier design specified.
- **`lot`** — risk-limited acceptance of a queue, with the review order blind to the machine
  verdict and seeded known-bad items mixed in.
- **`ratchet`** — computes earned tiers, applies revocations immediately, writes promotions as
  proposals. A plain script rather than a model call.
- **`ledger`** — the hash-chained decision record, and a verifier that detects a single flipped
  byte in any historical row.

### Deviations from the build plan

- **The warrant is TOML rather than YAML.** `tomllib` is stdlib and there is no stdlib YAML parser.
  Shipping a hand-rolled YAML subset reader for the one file that gates everything else was the
  wrong risk. `lanes.toml` follows the same reasoning.
- **`calibrate` became `feedback`.** The plan's prospective reader study was cut on the owner's
  instruction: it spent human review time in order to remove human review time. The consequence is
  recorded rather than smoothed over — the tier ladder is now climbed on absence of escapes rather
  than on a measured sensitivity, which is weaker evidence, and `references/tiers.md` says so.
- **The panel gained the three lane roles.** The plan had one grader; `why-not-a-jury.md` and the
  lens/adjudicator split were added after the owner asked whether multiple models were needed.

### Known limits

No A/B eval against a no-skill baseline has been run. `evals/EVALS.md` opens with that fact, lists
what was verified mechanically, and names the tasks that would settle it.
