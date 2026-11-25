# Changelog

## 2.5.0 - 2026-11-24

Two cuts to e2e wall time that keep the evidence:

- **The second green run covers the feature's specs plus anything that failed or retried in the
  first**, not the whole suite again. The full suite still runs twice when the branch touches what
  every spec shares: seed data, global fixtures, auth or tenant setup, or the harness config.
- **The post-rebase e2e rerun is skipped only for a rebase that changed nothing**: the branch head,
  the integration branch's tip and their merge base must be the same three commits recorded at the
  last green run, and the finalize report names them. Any difference means rerun.

And one new finalize box: every changed rule file (`CLAUDE.md`, `REVIEW.md`, `.claude/**`,
`.github/**`, `CODEOWNERS`, hooks, CI config) is listed in the report, and a change that removes or
loosens a check, rule or protection stops the run at the gate for a person to merge. Adding a rule
or a check does not.

Also in this release:

- **A verdict covers the commits it graded.** `shipyard:verify` now records the head and merge base
  it graded, and the finalize gate runs `git range-diff` after the final rebase: a feature patch the
  conflict resolution changed, or a code commit made after verify, goes back to verify or stops the
  run. This is Claude Ship's stale-approval rule.
- The report names the person who started the run as the owner of the merged change.
- A branch a person takes to a pull request after a stopped run can be handed to
  `shipyard:steward`.
- `gemini.md` refreshed for the sixteen-box gate, the narrowed second e2e run and the stale-verdict
  check; `verify_quotes.py` exits 0.

## 2.4.2 - 2026-09-01

Refreshes `gemini.md` against a `SKILL.md` that had changed since it was written. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 2.4.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

## 2.3.0 - 2026-08-21

Lane assignments move to `defer`. This skill no longer names a model or an effort of its own — it points at `lane_pick.py` for the model, the effort and the argv, and at `lane_run.sh` to run and wire-verify one in a step. A pinned lane restated in seven files is a policy nobody can change, and this one had already drifted.

- **The three out-of-family gates run `gpt-5.6-sol` at `medium`, not `max`.** Same lane, same read-only sandbox; the effort was the only thing above what the work needs, and `max` is now ruled out everywhere.

## 2.2.0 — 2026-08-20

### Changed

- **Phase 7 names the three gates inside `verify` that decide whether its evidence means
  anything** — each closing a way a verdict is confident and hollow. Every screenshot's subject is
  proved rather than inferred from its filename (a campaign once published 20 captures of three
  unrelated documents and cleared every gate it had); every cited suite is scanned for assertions
  that cannot fail before its green is spent (over half of more than 15,000 generated mutants
  survived a passing suite); and a bundle-only completeness critic rejects rows that reduce to
  "looks right" or a code read.
- **Two standing rules added.** A gate whose pass and whose could-not-run look identical has not
  been run — record which it was. And evidence is what the bundle holds rather than what the note
  says about it: a row citing a summary of an artifact is a TODO in a verdict's clothes.

## 2.1.0 - 2026-08-19

- Phase 6 invokes `test-campaign` where installed, falling back to `acceptance-e2e`. A case the campaign cannot settle resolves to `unoracled` and phase 6a builds the missing oracle, rather than the case passing quietly.
- A requirement returned as `Unverified — no oracle` routes back to phase 6 rather than to gap-fix: gap-fix closes a gap between the work and its spec, and this is a gap between the spec and anything checkable.
- Phase 7 notes that verify's table now carries the oracle rung per requirement.

## 2.0.0 - 2026-08-15

Moved from diolog-plugins and rebuilt as the conductor over the shipyard stages.

- Design runs in parallel with plan, gated by design-review and be-my-witness.
- Cross-family `verify` runs as a fresh agent before any merge; `Needs More Work` loops through gap-fix and re-verification, parked after three failed rounds.
- Four new pre-merge gate boxes: the verifier's verdict, a post-rebase e2e re-run, the keyboard/accessibility floor, and S3 sign-off where triage flagged it.
- A rollback procedure (revert the merge as one unit) is decided in the reference, not improvised during an incident.
- Decisions defer through the second-opinion lanes; unattended runs park questions instead of blocking.

## 1.5.3 and earlier

See the diolog-plugins history; this plugin's lineage lived there as ship-feature 1.x.
