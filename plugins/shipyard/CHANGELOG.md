# Changelog

## 0.3.0 — 2026-08-20

`verify` gathered typed evidence and graded it out of family, and every rule about what closes a
claim was about the *kind* of evidence rather than its *integrity*. Three shapes got through: a
screenshot whose subject nothing corroborated, a green suite whose green came from an assertion
that cannot fail, and a verdict row that cited the verifier's own summary of an artifact rather
than the artifact.

### Added

- **`evidence-rules.md` §a screenshot is a claim about its subject.** A screenshot asserts two
  things and the pipeline only ever checked one: that pixels were captured, and that they are of
  the thing under verification. A test campaign published 20 captures of three unrelated documents
  and cleared every gate it had, because a filename is written by whoever ran the capture and not
  by the app. Two exact checks now follow every visual clause — **untied** (the recorded target is
  not the requirement's route) and **shared** (two requirements, one sha256) — and a screenshot
  whose subject nothing corroborates is the same status as no screenshot, not a weaker pass.
- **§artifact-forcing**, from `mockup-fidelity`. No artifact, no verdict; every row cites an
  artifact by path and by the value read from it; a row closes on a re-extracted artifact rather
  than on the code change. It is a precondition rather than an exhortation because prose does not
  hold — agents under effort pressure rationalise the shortcut, and models trained against
  reward-hacking learn to conceal it rather than stop.
- **§assertions that cannot fail**, from `warrant:assay`. Eight syntactic shapes that pass a suite
  while testing nothing. Over half of more than 15,000 generated mutants survived a passing unit,
  integration and system suite, so a green suite starts the question rather than answering it.
- **`verify` step 3a — the completeness critic.** One pass reading *only* the evidence bundle and
  the requirement table, with the app, the diff and the ticket closed, rejecting any row that
  reduces to "looks right" or a code read. Blind to the UI precisely so it cannot be talked into
  "it obviously works", and the one check in the stage that cannot be satisfied by sounding
  thorough.
- **`verify` structural rule 5** — the bundle is the verdict's evidence and the prose is not.
- **An Evidence-integrity section** in the posted verdict: subjects tied, the shared-artifact
  check, the cannot-fail scan with its denominator, the critic's verdict.

### Changed

- **`work` phase F** runs the cannot-fail scan over the specs it touched and ties every screenshot
  in the completion record to its subject, before the record is written. The red→green pair is the
  evidence the whole clause table rests on, and a pair whose green comes from an `expect` with no
  matcher discriminates nothing.
- **`verify`'s visual lane** records each screenshot's subject, target, channel and sha256, and
  runs `test-campaign`'s `capture-lineage.py --gate` over the set where the repo carries a campaign.

## 0.2.0 - 2026-08-19

- `verify` types each requirement's evidence by the oracle rung it stands on, and the per-requirement table carries the rung beside the status. "The element exists" and "publishing made it live" were the same word in a verdict and are different claims about the product.
- A requirement proved only by a weak rung (`touch`, `presence`, `structural`, `structural-visual`) reads `Unverified` rather than `Done`.
- New terminal shape: `Unverified — no oracle`, distinct from `Unverified — blocker`. A blocker is an instrument or access problem and may dissolve with better tooling; no oracle means nothing was ever specified that a check could read, and no tooling settles it. An item carrying one does not reach `Done` whatever the rest of the table says.
- The Tests lane prefers `/test-campaign` where installed, falling back to `/acceptance-e2e`.

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
