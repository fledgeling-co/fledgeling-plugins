# Changelog

## 0.8.1 - 2026-09-01

Refreshes `gemini.md` against a `SKILL.md` that had changed since it was written. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 0.6.0 - 2026-08-21

Lane assignments move to `defer`. This skill no longer names a model or an effort of its own — it points at `lane_pick.py` for the model, the effort and the argv, and at `lane_run.sh` to run and wire-verify one in a step. A pinned lane restated in seven files is a policy nobody can change, and this one had already drifted.

- **Verification lanes point at `defer` instead of naming a model.** Same-family validation and task verification are `claude-opus-5` at `xhigh` by policy, which is where this skill already sat.

## 0.1.0 — 2026-08-18

First release.

- Sweeps a tracker board card by card over MCP, tracker-agnostic: map your column
  names onto six roles once and the ledger remembers.
- Rebuilds the numbered requirement list from the description, every comment and
  every attached image **before** opening any completion record or diff.
- Locates the work — merged, unmerged branch, unpushed, worktree, or absent.
- Traces each requirement to its producer, routing to `spec-validation`.
- Judges testing adequacy on oracle rung, armed-versus-unarmed assertions and a
  stated denominator, drawing on `create-test-suite`.
- Grades out of family with one judge rather than a panel.
- Treats inconclusive as a blocking result rather than a pass.
- Refuses promotion past Done until eight preconditions hold for one named
  low-risk class; `check_verified_gate.py` names the missing ones.
- Writes briefs to `docs/features-to-triage/` and hands them to `ship-fleet`.
- Five bundled scripts, each red-armed against input it should reject.

Not evaluated against a no-skill baseline — see `EVALS.md`, which says so first.
