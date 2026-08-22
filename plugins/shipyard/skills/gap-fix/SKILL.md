---
name: gap-fix
description: >-
  Close whatever a built feature still misses versus its original requirements by auditing the
  delivered code and fixing the gaps in code — the pipeline's remediation stage and the re-entry
  path from Needs More Work. Re-enters the branch the worker produced, merges the verifier's
  verdict table (and any human/QA gap list) into a fresh full audit, fixes every confirmed gap as
  production code through the executor lanes, and loops audit→fix until two consecutive fresh
  audits go dry, then returns the item to Developer Review for re-verification. Use when verify
  set Needs More Work ("gap-fix DIO-0001"), when a QA pass lists what's missing, or when a built
  feature falls short of its spec. Unlike verify (audit-only), gap-fix fixes; unlike work (full
  builds), it only finishes what's left.
---

# Pipeline Gap-Fix — remediation, and the road back from `Needs More Work`

Finish the job the worker started: close whatever the delivered implementation still misses
versus the **original requirements**, in code, on the same branch — then hand the item back to
`verify` rather than grading it yourself. This is the failure path existing on purpose: a
`Needs More Work` verdict is a work order, not a dead end.

Shared canon by pointer: `${CLAUDE_PLUGIN_ROOT}/references/` → `tracker-adapter.md`,
`model-lanes.md`, `executor-lanes.md`, `evidence-rules.md`, `operational-rules.md`, and the
worker's `../work/references/miss-classes.md`.

## Inputs

- An id at `Needs More Work` (the verifier's verdict table is the primary gap list) or
  `Developer Review`/`In Review` with provided gaps (inline, a file, a `## Gaps` section, a QA
  list). Provided gaps **merge into** the self-audit; they never replace it — a QA list is a
  floor, not a ceiling.
- Optional `--dry-run`: audit and report the gaps + intended fixes; change no code.

## Setup

1. Find the branch: reuse `.worktrees/<ID>`; else `git worktree add .worktrees/<ID> ai/<id>`;
   else there is nothing to fix — say so and recommend `work` (`NEEDS WORK`). Check the base
   staleness (`merge-base --is-ancestor`) before trusting a reused worktree.
2. Read the spec/ticket + full thread, the plan, and the verifier's verdict from the main tree
   at absolute paths. Human answers are authoritative; the verdict's `Missed`/`Partial` rows and
   their evidence are confirmed findings arriving pre-verified.
3. Post the round marker **before** working (crash-safe counter, `tracker-adapter.md`): count
   prior gap-fix rounds from the thread; **three rounds without reaching `Done` parks the item**
   with a blocker note naming what keeps failing — a converging loop shrinks its gap list every
   round, and one that doesn't is diagnosing the wrong layer.
4. All code edits inside `WT`; disjoint scopes; docs stay in the main tree.

## Phase A — Audit the build vs the requirements (always, even with a verdict in hand)

Fan out reviewers over the **whole delivered surface on the branch against the full
requirements** — grep the diff, never scope to what the latest progress note calls "in scope";
un-audited shipped code is exactly what breaks on first use. Same dimensions and invariant
sourcing as work Phase D (requirement completeness, correctness, guardrails from the repo's own
CLAUDE.md, UI fidelity vs the mock index, security, simplicity/surgical), same typed-evidence
rules, same miss-class exercises on the real path. Merge in the verifier's rows and any provided
gaps as findings to confirm; a provided gap the code already satisfies is recorded already-met,
not re-fixed; a provided "gap" that contradicts the spec is out-of-scope, recorded, not built.
Adversarial verification aimed at Criticals/structural/locked-decision reversals. Close with the
**out-of-family completeness critic** (ordered lanes, R2 contract in
`${CLAUDE_PLUGIN_ROOT}/references/codex-cli.md`) attacking the audit itself; its output seeds the
next round.

## Phase B — Fix the gaps in code

Every confirmed gap at every severity, reproduce-first for bugs (the failing check against the
real un-stubbed path, then green), wired end-to-end for missing requirements — never just the
symbol. Surgical: the fix touches what the gap names; no adjacent cleanup. File-disjoint fixes in
parallel; repo gates between waves; mechanical fixes may take the executor lanes
(`executor-lanes.md` terms — name the fix's shape on the `--shape` call, and note that a gap fix
against code that already ships is usually `brownfield-integration` or `regression-sensitive`,
the two shapes where the cheap lanes lose most); judgment fixes, security, and the never-delegate
list stay with Claude. Commit as you go (never `git add .`).

**Loop A → B until two consecutive fresh audits — different reviewer lenses, plus the critic —
surface no new confirmed Critical/High/Medium.** One quiet pass is a shallow fixpoint, not a dry
one. Document any Low intentionally deferred.

## Phase C — Finalize and hand back

Run the full repo gates. Append the gap-fix record (section or comment, per the tracker
adapter): audit counts (self + provided + verifier rows; already-met count), closed-in-code list
(severity → files → the clause now satisfied, with typed evidence per row), deferred Lows,
branch, gates actually run, executor + critic accounting, reviewing models. Caveats propagate.
Then status → **`Developer Review`** — `verify` re-runs, fresh context, fresh verdict. Gap-fix
never sets `Done`; the stranger does.

If a residual gap needs a human decision: post the blocker with its dissolution condition, leave
the status, stop (`NEEDS TRIAGE`).

## Guidelines

- **The requirements are the authority** — human answers over assumptions over inference.
- **Targeted finisher, not a rebuild.** An essentially empty branch is a `work` job (`NEEDS
  WORK`).
- Production code only; no stubs to "close" a gap; never push, never PR — the conductor owns
  merge.
- REVIEWER ≥ WRITER: the audit runs at least as strong as the strongest model that wrote the
  code under audit; security lenses always on the strongest model; readers cheap.
  Commit convention as the worker's.
