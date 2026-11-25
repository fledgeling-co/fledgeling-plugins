# Changelog

## 0.6.0 - 2026-11-25

- **New stage, `shipyard:steward`.** Looks after an open pull request until it merges or closes:
  merges the base in when it conflicts, fixes checks the change broke, answers small review
  comments, and escalates redesign requests, unresolved security problems, disagreements between
  people and any issue that has failed three pushes. It acts only on comments from the author,
  accounts with write access and bots the house rules name; reads house rules from
  `.claude/skills/steward/SKILL.md` on the base branch; never merges, approves, force-pushes,
  deletes branches, pushes tags or edits the files that set the rules; and keeps its attempt counts
  in one status comment so a stateless CI pass can read them. It runs one pass per CI event on a
  self-hosted runner, opted in by a `steward` label, or as a local watch paced by
  `better-loop:better-loop`. Ported from the design of Anthropic's `/steward` and PR Steward, run on
  our own runners and models.
- **Verify starts the app the repository's way.** The serving ladder gains a first rung: when the
  repository ships `.claude/skills/verify/SKILL.md`, verify follows it, taken from the integration
  branch, so a change cannot redefine how it is checked.
- **Verify records the commit it graded** (head and merge base), so the finalize gate can tell when
  a rebase or a later commit has outrun the verdict.
- **`model-and-effort.md` §8** says how to give a Workflow runner a time budget when the harness
  cannot append one, keeps verify and the review gates on elapsed time only, and marks third-party
  text quoted in a brief with `<pasted_content>` tags. `model-lanes.md` names Claude Opus by the
  roster's `opus` alias and links the Opus 5.5 migration guide.
- The steward names how to undo each push (`git revert <sha>`).
- `gemini.md` files: a new one for `steward` (its limits as nine rows read back off git and the pull
  request, outside text in labelled blocks), and refreshes for the router (eight stages) and `verify`
  (the graded commit). `verify_quotes.py` exits 0 on all three.

## 0.5.5

Second-opinion lanes read their model and effort from the model roster's daily tier (`scripts/roster.py`): Opus, Gemini Neon, Grok and Meta Wonder at xhigh. The pinned `claude-fable-5`, `gpt-5.6-sol`, `gemini-3.7-flash-high` and `grok-4.6` are gone, and the tier has no OpenAI lane.

## 0.5.3 - 2026-09-01

Closes the auditor findings on `gemini.md`: filled the exemplars the overrides only described, corrected counts and citations that disagreed with the target `SKILL.md`, and brought the file inside the 150-250 line bound. `verify_quotes.py` exits 0.

## 0.5.2 - 2026-09-01

Refreshes `gemini.md` against a `SKILL.md` that had changed since it was written. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 0.5.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

## 0.4.0 - 2026-08-21

Lane assignments move to `defer`. This skill no longer names a model or an effort of its own — it points at `lane_pick.py` for the model, the effort and the argv, and at `lane_run.sh` to run and wire-verify one in a step. A pinned lane restated in seven files is a policy nobody can change, and this one had already drifted.

- **`references/model-lanes.md` is rewritten rather than patched.** It now reads as this pipeline's view of `defer`'s table: which class each stage belongs to, and what that class allows.
- **Every `model_reasoning_effort="max"` becomes `"medium"`, and the grep that verifies it moves with it.** The recorded research panel behind the rebuild plan keeps the models that actually ran it.

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
