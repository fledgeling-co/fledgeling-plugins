# Changelog

## 0.1.1 - 2026-08-15

- Phase D gains the `code-review` skill as an additional lens over the branch diff where installed.
- The verifier's persistence bar names the `spec-validation` skill explicitly instead of re-deriving its rubric.

## 0.1.0 - 2026-08-15

Initial release. Seven stage skills (intake, triage, plan, design, work, verify, gap-fix) plus the router, merging the diolog feature-spec-pipeline and diolog-tasks-pipeline lineages onto one tracker adapter with a complete status machine (`Done` and `Needs More Work` exist; only `verify` sets `Done`).

- Typed evidence rules, the two-probe blocker protocol, and caveat propagation carried forward from the WEB-4905 audit fixes and made pipeline-wide.
- Cross-family verification as the only path to done; ordered out-of-family review lanes (codex, agy, grok) with wire verification and recorded degradation.
- The decision gate (look it up, divergence test, essential bar, second opinions, panels) replaces mid-run questions; access-control defaults are presumptively essential.
- Executor lanes: agy preferred, grok, codex gpt-5.6-terra, Claude fail-back; revert-rate kill-switch and per-lane accounting.
- New design stage: all-platform mocks and a state matrix, gated by design-review and be-my-witness with findings actioned.
- New intake stage: rough idea to briefs, trawl ideation, strict proposed-by-ai marking, Dossier research where the idea is thin.
- Evals: report card 37/37 vs the originals' 22/37; blind three-family panel 17-4; the lost triage round fixed and flipped 2-1 across three rounds. Records committed under `evals/records/`.
