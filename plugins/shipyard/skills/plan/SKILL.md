---
name: plan
description: >-
  Produce a codebase-grounded implementation plan plus a comprehensive test strategy for a
  triaged feature — the stage that everything downstream amplifies. Reads the spec/ticket and the
  design stage's mock index + state matrix where one exists, classifies a plan-size tier
  (Trivial/Small/Standard/Large), investigates the actual codebase (Workflow fan-out for big
  features), writes and COMMITS docs/plans/<id>.md, names the test seams and the unit/e2e/visual
  coverage against the state matrix, runs the mechanical path check, the all-tiers
  scope-narrowing check, and an out-of-family plan review, then sets status Ready for AI. Use
  when the user says "plan DIO-0001", "write the implementation plan", or a triaged feature needs
  its build plan. Runs in the current session; the worker consumes the plan verbatim.
---

# Pipeline Plan — the build plan and the test strategy, gated

Produce an implementation plan by investigating the actual codebase, write it to
`docs/plans/<id>.md`, **commit it**, link it with its sha, and move the status to `Ready for AI`.
The plan is the pipeline's highest-leverage trusted-first-output artifact — everything downstream
amplifies it — so it carries its own gates.

Substrate and statuses: `${CLAUDE_PLUGIN_ROOT}/references/tracker-adapter.md`. Lanes and effort:
`${CLAUDE_PLUGIN_ROOT}/references/model-lanes.md` — readers at `low`, Trivial/Small synthesis may
run mid-tier, Standard/Large synthesis and every gate stay on a frontier Claude at `high`.

## Inputs

- A triaged id at `To Do`. Read the spec/ticket + full thread (human answers authoritative), the
  triage Assumptions (the defaults for everything the description didn't pin down), and — for
  user-facing features — the design stage's mock index + state matrix. Design may still be
  running: plan the non-UI slices now and mark UI slices "awaiting mock index" rather than
  waiting idle. Optional `--dry-run`: write the plan file, no status/ledger updates.
- A `Needs More Info` item: first try to resolve the open questions the way triage should have
  (the decision gate in `${CLAUDE_PLUGIN_ROOT}/references/second-opinion-lanes.md`), plan on
  documented assumptions, and decline only when the *core* hinges on a genuine external
  dependency — even then, plan everything it does not block.

## Procedure

1. **Classify the tier** (Trivial / Small / Standard / Large) before writing — it sets the
   template and length budget; when in doubt, smaller. `references/plan-tiers.md`. The
   Standard↔Large tie-breaker is *new units of architecture in the target repo's own stack* (a
   new module, store/collection, page/route — read the repo's shape, don't assume any particular
   framework).

2. **Investigate at the tier's depth.** Standard/Large: Workflow fan-out, one reader per
   element/subsystem, each returning exact files, closest analogue, contracts, naming ambiguity;
   synthesize yourself. Trivial/Small: inline. Trace data features end-to-end (UI → client →
   API → service → store). Wave caps: `${CLAUDE_PLUGIN_ROOT}/references/operational-rules.md`.
   A plan grounded in real code is worth writing; a plan of assumptions is not.

3. **Write the plan** at `docs/plans/<id>.md` (lowercase id) using the tier template. Beyond the
   template, three sections are load-bearing here:
   - **Test strategy** — per `${CLAUDE_PLUGIN_ROOT}/references/test-strategy.md`: the named
     seams (existing preferred, highest possible, agreed here so the worker never tests at an
     unconfirmed seam), the unit/contract coverage for changed logic, the e2e flows (every user
     flow, action, and menu the feature adds — each traceable to an acceptance criterion), and
     the visual/state coverage read off the design stage's state matrix. Every acceptance
     criterion is **falsifiable at the base commit** — name the observation that would show it
     false and confirm it fails where the implementer starts.
   - **Parity inventory** — when the plan routes an existing flow through a new path (engine
     swap, v2, provider behind a flag): every load-bearing behaviour of the old path (guards,
     validation, metering, error semantics) marked keep / port / drop-with-rationale. A new path
     that silently loses a guard ships green because nothing asserts the absence.
   - **Audit coverage** — when the feature adds or alters a path that mutates tenant data, sends
     something to a human, produces AI output a human may act on, or reads a sensitive record:
     the plan names each **emit call site** (file + the function it sits in) and the
     **coverage-registry row** that declares it, so the worker writes both in one commit rather
     than meeting the gate in CI. Triage's audit inventory is the input; this step turns it into
     locations. Name every emit surface the repo has, not just the one you recognise — Diolog has three
     (`emitAuditRecord(` and `deliverAuditRecord(` in the API, `recordAuditEvents(` in the
     Next.js BFF, which cannot reach the in-process bus), and a plan naming only the API helper
     leaves a BFF route unlogged while reading as complete. Diolog's declaration is a row in
     `apps/api/src/modules/audit-log/audit-coverage.registry.ts`, enforced bidirectionally by
     `audit-coverage.spec.ts` (an unregistered emitter and a registered non-emitter both fail
     CI) with `audit-reachability.spec.ts` additionally requiring the emit to sit where a caller
     can reach it. Rule: `CODING_PRACTICES.md` → "Audit logging (A09)"; reference
     implementation: WEB-4787. A feature with genuinely no such path says so in one line —
     silence reads as forgotten, which is how an evidence gap ships.

4. **Scope-narrowing check (ALL tiers, mechanical).** Compare every "Out of scope" line and every
   requirement the plan does *not* carry against the description and the triage Assumptions. Any
   overlap is a narrowing and is surfaced in the spec/thread as its own line — "The plan excludes
   <X>; assumption <N> ('<text>') appears to include it — reply to keep it excluded, or it gets
   planned in." Small tiers skip the model gate below, and small tickets are exactly where a
   quiet descope otherwise meets no reader before the worker inherits it as a premise.

5. **Plan review gate (Standard/Large; before the status flips).**
   - **Mechanical path check**: every backtick-quoted path in the plan exists (`ls` /
     `git ls-files`), exempting only paths marked *to be created*. A missing path means the plan
     was grounded in assumption — re-investigate.
   - **Out-of-family review**: the ordered lanes in
     `${CLAUDE_PLUGIN_ROOT}/references/second-opinion-lanes.md` (codex `gpt-5.6-sol` `medium` first,
     then agy, then grok), read-only, per the R1 contract in
     `${CLAUDE_PLUGIN_ROOT}/references/codex-cli.md`: are the ACs testable and complete against
     every clause and assumption? Was anything dropped or silently shrunk? Is every referenced
     analogue real (it opens the files)? Does the ordering close? Does a replacement path carry
     its Parity inventory? Wire-verify, bound, egress/opt-out per invocation; empty output =
     lane failure → next lane; all lanes down → in-family strong-model review, recorded as a
     downgrade. Then **act** — accept / reject with reason / escalate; never flip status on
     unresolved material defects. Record verdict + tally in the plan's gate note.

6. **Commit and link.** `git add docs/plans/<id>.md && git commit -m "docs(plans): <id>
   implementation plan"` in the main tree. Then the pointer (spec section or one-line comment):
   "Implementation plan: `docs/plans/<id>.md` (committed: `<short sha>`, tier: <tier>)." Never
   claim repo presence without the sha. Status → **`Ready for AI`** (never downgrade; skip if
   already downstream). For user-facing features the status flips only when the design handoff
   exists too — plan and mocks are jointly what the worker consumes.

7. **Report**: tier, plan path + sha, gate outcome, id — one screen.

## Guidelines

- **Ambiguity is not a reason to bail; plan every requirement.** Internal gaps get documented
  assumptions; size is handled by tier + decomposition, never by cutting scope. Reserve
  escalation for genuine external dependencies, and plan around them.
- Name real files, functions, analogues — verified with Glob/Grep. Rendered-appearance claims
  carry MEASURED/ASSUMED marks (`${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md`).
- **Length is a tier constraint** — a 10-line diff gets a ~30-line plan; padding with empty
  sections is worse than omitting them, because the worker treats every section as work.
- REVIEWER ≥ WRITER: whatever synthesized the plan, its reviewer is at least as strong — and the
  gate routes out of family, which adds the independence an in-family reviewer cannot.
