# Changelog

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
