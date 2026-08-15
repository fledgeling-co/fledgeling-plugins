---
name: ship-feature
description: >-
  End-to-end feature delivery conductor — takes ONE feature (a rough idea, inline text, a brief
  file, or a tracked ticket) from bare idea to a merged, verified, production-ready feature by
  conducting the ship-pipeline stage skills in a single in-session flow: intake (briefs +
  ideation, when handed a rough idea) → triage → plan ∥ design (all-platform mocks gated by
  design-review and be-my-witness) → work (worktree build through the executor lanes) →
  deferred-work loop → gap-fix → acceptance-e2e → cross-family verify (the only path to Done) →
  fail-closed merge, push, cleanup. Use whenever someone wants a feature taken ALL THE WAY —
  "ship this feature end to end", "run the full pipeline on <feature>", "take this from
  description to merged", "do the whole feature for me" — even if they never name the stages.
  NOT for a single stage (use that stage's skill) or a whole backlog (use ship-fleet).
---

# Ship Feature — the end-to-end conductor

Take **one** feature from a bare description to **merged, verified, production code** by
conducting the ship-pipeline stage skills in sequence. You are the conductor: you hold the
feature's intent from first read to final merge, invoke each stage skill, verify its artifact
landed, carry the right context forward, and make the between-stage judgment calls no single
stage can. You never re-implement a stage here — you run them and thread them together.

```
rough idea ──→ intake      briefs in docs/features-to-triage/ (+ proposed-by-ai siblings)
brief/ticket ─→ triage     readiness verdict + assumptions            → To Do
               plan  ──┐   committed docs/plans/<id>.md + test strategy → Ready for AI
               design ─┘   all-platform mocks + state matrix, review-gated   (parallel)
               work        build in .worktrees/<ID> on ai/<id>; evidence tables; D′ validation
                           → Developer Review
               4b loop     deferred / child specs — SAME branch
               gap-fix     close remaining gaps in code
               e2e         acceptance suite vs the branch, locally, green twice
               verify      cross-family acceptance vs the running app → Done | Needs More Work
               finalize    fail-closed gate → rebase → merge → push → cleanup
```

Canonical shared rules ride with the stage skills in the ship-pipeline plugin's `references/`
(tracker adapter, model lanes, evidence rules, second-opinion lanes, operational rules). This
skill's own references: `references/orchestration-model.md` (read first),
`references/deferred-work-loop.md`, `references/e2e-and-finalize.md`.

## Inputs

- **A feature**: a rough idea (route through `intake` first), inline text or a brief file
  (start at `triage`), or an already-tracked id (enter at the stage its status implies). Read it
  in full at the start; it stays authoritative for the whole run.
- The **target repo**, run from its root — its CLAUDE.md, design system, docs tree/ledger or
  tasks board, e2e harness, and integration branch (`INT`, detected, never hardcoded).

## The orchestration model (the three load-bearing decisions)

1. **Stay in-session and sequential across stages** — invoke each stage skill in *this* session
   so the thread survives; parallelism lives inside stages (their own Workflow fan-outs) and in
   the one sanctioned overlap: **plan ∥ design** once triage lands, since plan's non-UI slices
   and design's mocks share no artifact until the worker consumes both. The other exception:
   **verify runs as a fresh subagent by design** — its value is exactly that it does not share
   your context; spawn it, don't run it inline.
2. **The pipeline's memory is on disk** — every stage persists its artifact; re-read at each
   boundary rather than trusting transcript memory. That is what makes the run resumable:
   re-enter at the first stage whose artifact is missing or not green.
3. **One feature = one branch = one worktree.** The worker owns `.worktrees/<ID>` on `ai/<id>`;
   you stay in the main tree; deferred and child work land on the parent's branch, never a new
   one.

## Operating discipline

- **Scale to the feature.** The stages are a floor of rigor, not a mandate to inflate: a ten-line
  feature gets a ten-line feature's pipeline — same discipline, not the same volume. Let plan's
  tiers lead; a non-UI feature skips design with a recorded reason; a self-contained feature has
  an empty 4b loop.
- **Decisions defer before they escalate.** At every fork, run the decision gate
  (ship-pipeline `references/second-opinion-lanes.md`): look it up, divergence-test it, settle
  technical calls with a lane or panel, record assumptions with the alternative they beat. What
  genuinely survives — taste, cost, scope, risk, Essential Questions — goes to the human in an
  attended run, and **parks without blocking** in an unattended one (`Needs More Info` with an
  Easy-reply block; continue everything the question does not gate). Never fabricate an answer
  to an Essential Question.
- **Verify with oracles, not re-reading.** Establish the feature's verifiable success criteria
  at intake/triage and carry them as the acceptance oracle every stage measures against. Every
  gate actually runs; every critical path is exercised un-stubbed; the out-of-family gates and
  the cross-family verifier are non-negotiable. Don't stack extra re-read passes on stages that
  already self-review.
- **Deliver surgically; report thinly.** The merged diff traces to this feature. One sentence
  before a phase; an update on material findings; outcome first at the close.

## The phases

**0 — Intake & grounding.** A rough idea → invoke `intake` (briefs, trawl ideation,
proposed-by-ai siblings, research); pick the brief(s) to ship this run — siblings queue for the
fleet, they don't widen this feature. Then ground: success criteria, the repo's moving parts
(design system, docs/board, e2e harness, `INT`), the substrate lane
(tracker adapter). Attended + genuinely ambiguous → one consolidated question round now, in
clarify's shape — never scope discovered one phase at a time.

**1 — Triage.** Invoke `triage`. Capture the `<ID>`. NEEDS IMPROVEMENT → surface the Essential
Questions (attended) or park (unattended) and resume on answers. Confirm the out-of-family spec
review ran and was dispositioned — a missing verdict is a skipped gate, send it back; a logged
`unavailable → in-family` downgrade carries into the pre-merge evidence.

**2 ∥ 3 — Plan and Design, in parallel.** Invoke `plan <ID>`; for user-facing work invoke
`design <ID>` alongside (its mocks + state matrix are the worker's UI truth and the test
strategy's coverage bar; its design-review + be-my-witness findings must be actioned before
handoff). Verify both artifacts landed: the committed plan sha + gate note with findings
dispositioned; the mock index with no unwaived empty matrix cells. `Ready for AI` flips only
when both exist (or design was skipped with its recorded reason).

**4 — Work.** Invoke `work <ID>`. When it finishes, read the completion record: the Reachability
+ Clause tables (every row ✅), the executor + critic accounting (a missing critic line means the
last reviewer was skipped or lost to an unlogged fallback — chase it), the D′ same-family
validation outcome, the Reviewing-models line. Status `Developer Review`.

**4b — Deferred loop.** Read the record's deferred items + the plan
(`references/deferred-work-loop.md`): nothing → 5; small remainder → re-run `work <ID>`;
substantial new scope → child triage → plan → work **on the parent's branch**. Keep every child
id — e2e and verify must cover them.

**5 — Gap-fix.** Invoke `gap-fix <ID>` — the belt-and-braces finisher before tests; run it even
when work looked complete (a prior self-review commit certifies nothing).

**6 — Acceptance e2e.** Invoke `acceptance-e2e` with **all** requirement sources (description,
spec + children, plans, the mock index/state matrix — a menu the mock shows but the AC list
omits is still a flow to cover). Run against the branch's app locally, specs authored on the
branch, green **twice**, tractable bugs fixed. `references/e2e-and-finalize.md` §Phase 6.

**7 — Verify.** Spawn the `verify` stage as a **fresh agent** (no build context — that is the
point). It gathers typed evidence against the running app, routes the verdict out of family, and
sets `Done` or `Needs More Work`. On `Needs More Work`: loop → `gap-fix` (its verdict table is
the work order) → re-verify; three failed rounds parks the item with the blocker named.

**8 — Finalize.** Only behind the **fail-closed pre-merge gate**
(`references/e2e-and-finalize.md`): every box actually checked now — including the verifier's
verdict, the post-rebase e2e re-run, the a11y floor, and the S3 sign-off where triage flagged it.
Then commit → final rebase onto fresh `INT` → re-run gates → merge `--no-ff` → push → remove
worktrees, delete merged branches → record `Done (Merged)` + commit the docs on the integration
branch. Any red or unverifiable box → STOP, report the exact blocker, leave the branch local. A
stopped-at-a-gate run is a correct outcome; the rollback procedure (in the same reference) is
decided before it is needed.

## Hard rules

- **The feature description is the north star; human answers > triage assumptions > inference.**
  Never let a later stage quietly reverse a recorded decision.
- **Never skip a stage; never fake a gate.** Every gate actually executed; merge only on
  verified green. The out-of-family gates and the cross-family verifier are gates, not garnish —
  an unlogged fallback is indistinguishable from a skip and is treated as one.
- **Respect the egress opt-out** (per invocation); an opted-out repo runs in-family and that
  satisfies the gates, with the degraded-verification buy-back from
  ship-pipeline `references/model-lanes.md`.
- **One branch, one merge; docs in the main tree; only verify sets `Done`.**
- **Cap your own delegation**: the stage skills fan out internally; you spawn only what this
  file names (the verify agent, the parallel design/plan invocations). Don't wrap the pipeline
  in one Workflow script and don't hand a stage to a general subagent — you'd lose the thread.

## Definition of done

UI represented and review-gated; spec + plan (+ children) exist with their gates dispositioned;
implementation, deferred work, and gap-fixes on `ai/<id>`; e2e green twice covering every
flow/action/menu; **the cross-family verdict reads COMPLETE**; branch rebased, merged, pushed;
worktrees removed; spec/ticket and ledger read `Done`. Or: stopped at a named gate with the
exact blocker reported — plainly, as a first-class outcome.

## Resuming

Re-enter at the first missing/not-green artifact: no spec → 1; no plan/mocks → 2∥3; no worktree
or completion record → 4; deferred open → 4b; no gap-fix note → 5; no green suite → 6; no
verdict → 7; verified but unmerged → 8. Re-read the artifacts; never restart from 0.
