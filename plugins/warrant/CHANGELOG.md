# Changelog

All notable changes to the `warrant` plugin.

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
