---
name: plan
description: >-
  Produce a detailed, codebase-grounded implementation plan for a feature spec in the markdown feature-spec pipeline. Reads docs/specs/spec-DIO-0001.md (the original details plus the triage assumptions/answers), classifies a plan-size tier (Trivial/Small/Standard/Large), investigates the actual codebase (fanning out via the Workflow tool for big specs), writes the plan to docs/plans/plan-DIO-0001.md, links it from the spec, and sets the spec status to Ready for Work. Use when the user says "plan DIO-0001", "write the implementation plan for this spec", "run the planner on DIO-0001", or asks for a build plan for a triaged feature spec. For an issue tracked in Diolog Tasks, use tasks-plan instead. Runs in the current session (Read/Glob/Grep/Write/Edit plus the Workflow tool for parallel investigation) — no issue tracker, no Agent SDK.
---

# Feature Spec Planner (markdown specs)

Produce an implementation plan for a feature spec by investigating the actual codebase, write it to a local markdown file, then link it from the spec and move the spec to `Ready for Work`.

Runs **in your current session** with `Read`/`Glob`/`Grep`/`Write`/`Edit`, `Bash`, and the `Workflow` tool. It uses no issue-tracker MCP (Diolog Tasks or otherwise) and invokes no Agent SDK script. The spec markdown file replaces a tracker issue + comment thread.

## Inputs

- A spec id (`DIO-0001`). The plan reads `docs/specs/spec-<ID>.md`. Optional `--dry-run` intent: write the plan file locally but make no status/ledger updates.

## Procedure

1. **Read the spec** at `docs/specs/spec-<ID>.md`. The `## Feature description` section is the original intent; the latest `## Triage` section carries the **Assumptions** (the defaults for anything the description didn't pin down) and any answers/edits the human added (authoritative). Summarize intent — don't transcribe the spec into the plan. If the spec status is `Needs More Info`, first try to resolve the open questions the way triage should have — from the codebase, the closest analogue, and the safer default — and plan on those documented assumptions. Decline to plan **only** when the *core* intent genuinely cannot be planned without a real **external (non-internal) dependency** — a product / policy / brand decision only the human can make, or an external contract / credential / system you lack. Even then, plan every part that dependency does not block and name only the blocked slice; reserve `NEEDS TRIAGE` for when the whole feature hinges on the missing external answer.

2. **Classify the plan-size tier** (Trivial / Small / Standard / Large) before writing — it sets the template and length budget. When in doubt, pick the smaller tier. See `references/plan-tiers.md`.

3. **Investigate the codebase at the tier's depth — fan out with the Workflow tool ("ultracode").** For Standard/Large specs, spawn parallel reader subagents — one per element/subsystem the spec references — each returning: the exact files to create/modify, the closest existing analogue, the interfaces/contracts, and any naming ambiguity. Synthesize their findings into the plan. For Trivial/Small specs, investigate inline (a workflow is overkill). Trace data features UI → query/mutation → resolver → service → schema end-to-end. A plan grounded in real code is worth writing; a plan of assumptions is not.

4. **Write the plan file.** Use `Write` to save it at `docs/plans/plan-<ID>.md` (uppercase id, e.g. `docs/plans/plan-DIO-0001.md`) in the **target repository** (the same repo the worker will run against). Start with the shared header, then the tier's template. Follow `references/plan-tiers.md` for the exact templates, quality criteria, and the anti-over-engineering rules (a 10-line diff gets a ~30-line plan, not a 260-line one).

5. **Scope-narrowing check (ALL tiers, mechanical — a grep and a diff, not a model).** Before any status move, compare every "Out of scope" line and every requirement the plan does **not** carry against (a) the spec's `## Feature description` and (b) the triage Assumptions. Any overlap is a narrowing, and silence in the plan file is not disclosure — surface it in the spec's `## Plan` section as its own line: *"The plan excludes <X>; triage assumption <N> ('<text>') appears to include it — edit here to keep it excluded, or re-run `/plan` to plan it in."* This check exists because the review gate below is skipped for Trivial/Small tiers, and small changes are exactly where a quiet descope otherwise meets no reader before `/work` inherits it as a premise.

6. **Plan review gate — before the status flips (Standard and Large tiers; skip for Trivial/Small).** The plan is the pipeline's highest-leverage trusted-first-output artifact — everything downstream amplifies it — so it gets its own gate, run after the file is written and before step 7:
   - **Mechanical path check (a script/grep, not a model).** Every file path the plan references must exist: extract the backtick-quoted paths from `plan-<ID>.md` and check each (`ls` / `git ls-files`), exempting only paths the plan explicitly marks *to be created*. A referenced-but-missing path means the plan was grounded in assumption, not code — re-investigate and fix it.
   - **Cross-family one-shot review — the Codex CLI, `gpt-5.6-sol` at `max` effort (mandatory where available).** The plan is the artifact every later stage amplifies, so its reviewer comes from **outside Claude's model family** rather than from the family that wrote it. Run it read-only and grounded in the real codebase:

     ```bash
     perl -e 'alarm shift @ARGV; exec @ARGV' 600 \
       codex exec -C "<repo root>" -m gpt-5.6-sol -c model_reasoning_effort="max" \
       -s read-only -o /tmp/codex-review-<ID>.md "<prompt>" < /dev/null \
       > /tmp/codex-review-<ID>.log 2>&1
     ```

     Full mechanics — the egress note, the repo opt-out, the availability check, the verbatim prompt contract (R1), finding disposition, fallback — are in `feature-spec-pipeline/skills/work/references/codex-cli.md`; follow it rather than re-deriving the invocation. Four things it will not let you skip: **(a) every call is egress** — `read-only` restricts writes, not the network, so the plan and every source file the reviewer opens go to OpenAI, and a repo whose `CLAUDE.md`/`ORCHESTRATOR.md` says `ANTHROPIC-ONLY` (or similar) is **opted out** — run in-family and log it, checking this **per invocation** so it can stop a run already in flight; **(b)** `read-only` still matters for accountability — the reviewer must not "helpfully" fix the plan it reviews, because *you* apply the changes; **(c) verify the wire** — `grep -qx "reasoning effort: max"` on the captured log, because a dropped flag silently inherits the user's config default and a real gate ran at `high` that way; **(d) bound it** — no timeout flag exists, an over-scoped `max` review burns its turn budget and writes **nothing**, and an empty `-o` file is a lane failure, never a pass. Keep the scope to the artifact plus the handful of files whose claims need checking; on an empty result retry **once** at `high` with a narrowed scope, logged as a downgrade, then fall back in-family.

     The reviewer reads the spec + plan cold and answers: Is every Acceptance Criterion *testable* (a checkable outcome, not a vibe)? Do the ACs cover **every spec clause, including every triage assumption**? Was any spec requirement or subfeature dropped or silently shrunk? Is every referenced analogue *real* — do the named files actually do what the plan claims (it opens them and checks)? Does the step ordering actually close — no circular dependency, no step that cannot follow the one before it? And when the plan adds a **replacement or parallel path** for a flow the product already serves (an engine swap, a v2 pipeline, a new provider behind a flag): does it carry the **Parity inventory** below?

     **Then evaluate and act — running the review is not the gate; acting is.** Per finding: **accept** it and fix the plan; **reject** it with a stated reason (it contradicts a human's authoritative spec answer, it expands scope the spec never asked for, or you verified the code and the finding is wrong); or **escalate** — a `Critical`/`High` finding exposing a genuine **external** dependency converts to `NEEDS TRIAGE` for the blocked slice only, per the guidelines below. Never flip the status on `MATERIAL DEFECTS` without resolving them. A finding adopted without checking is how a plan acquires work nobody asked for — Codex is a reviewer, not an authority.

     If the lane is unavailable or the repo opted out (no binary, not logged in, usage/rate limit, empty output, deadline fired, repeated errors, `ANTHROPIC-ONLY` policy), fall back to a **Claude strong-model** one-shot review of the same prompt — the strongest model regardless of what synthesized the plan — and **note it in the gate note**, recording the effort that was actually on the wire. An unavailable lane is a logged downgrade; an opted-out repo is a correct in-family run needing no escalation; a gate that produced findings but never emitted its verdict line is **PARTIAL** — its findings are evidence, and the missing verdict is never a pass.

   Findings → fix the plan (and re-run the failed check) before flipping status. Record the verdict, the accept/reject tally, and any downgrade in the plan's gate note. The gate costs one read; a plan defect costs the whole downstream pipeline.

7. **Link the plan from the spec and bump status** (skip in dry-run). Append a short pointer section to `docs/specs/spec-<ID>.md`:

   ```markdown
   ## Plan — <YYYY-MM-DD>

   Implementation plan: `docs/plans/plan-<ID>.md` (Plan size: [tier]).
   ```

   Then set the spec header `Status: Ready for Work` (and `Last updated`), and update the ledger row's Status to `Ready for Work`. Skip the status change only if the spec is already at `Ready for Work` or further downstream (`In Progress`, `In Review`) — never downgrade. The plan file lives in the repo with the code and is read from there; don't copy its contents into the spec — link by path so the two never drift.

8. Print a short summary (tier + the plan path + the gate outcome + the spec id). In dry-run, say the file was written locally and no spec/ledger updates were made.

## Workflow fan-out limits (avoid throttling)

When step 3 uses the `Workflow` tool to investigate in parallel:
- **Cap each wave at ≤4 concurrent agents.** Batch a larger fan-out into sequential waves of ≤4 — firing ~10+ agents at once trips a server-side rate limit ("temporarily limiting requests — not your usage limit") that fails most of the wave. Chunk the items and `await` each small `parallel(...)` batch before the next; don't pass all items to one `parallel()`.
- **Retry transient failures.** If an agent's result is an "API Error / Rate limited / temporarily limiting requests" string (or `null`), re-run it in a later small batch; never treat it as a real finding.
- **Prefer plain-text returns for long, file-reading subagents.** Schema-forced readers that read many files often finish without emitting the structured output; have each return a fixed-shape markdown fragment and reserve any `schema` for the single synthesis step.

## Guidelines

- **Ambiguity is not a reason to bail.** Resolve it yourself from the codebase, the closest analogue, and the safer default, and record the picks as plan assumptions — a plan built on documented internal assumptions is the correct output, not a failure. Reserve `NEEDS TRIAGE` for a genuine **external (non-internal) dependency** you cannot resolve (a product/policy/brand decision that is the human's to make, or an external contract/credential/system you lack), and even then plan everything that dependency does not block and flag only the blocked slice. Never punt a whole spec over gaps you could settle yourself.
- **Plan every requirement and subfeature the spec asks for.** Do not drop, shrink, or push a subfeature "out of scope" or to a follow-up because it is large, fiddly, or lower priority — if it has no external dependency, it belongs in this plan. Size is handled by the tier + decomposition, not by cutting scope.
- **Replacement/parallel paths get a Parity inventory.** When the plan routes an existing flow through a new engine/path/provider (even flag-gated with the old path as fallback), the plan MUST include a section enumerating the existing path's load-bearing behaviours — security guards (untrusted-input framing/sanitisation, injection envelopes), validation/reconciliation steps (e.g. output-vs-expected-structure checks), observability/metering (token/cost accounting, progress, tracing), and error semantics — each explicitly marked **keep / port / drop-with-rationale**. A new path that silently loses a guard the old path had is the classic engine-swap regression: it ships green because nothing asserts the *absence*. The worker's acceptance review audits against this inventory.
- Keep the plan scoped to the spec; don't extend to adjacent features or cleanup.
- Name specific file paths, functions, components, and analogues — but only where they're real (verify with Glob/Grep). A bad plan references files that don't exist or invents patterns not used in the codebase.
- **Mark rendered-appearance claims MEASURED or ASSUMED.** Glob/Grep verifies that code exists and what it says — never what it renders. Any plan statement about how something currently *looks or behaves on screen* must carry `(measured: <browser evidence>)` or `(assumed from source — verify in browser before building on it)`. A class string is not a rendered fact — overrides get silently discarded — and a false "reference implementation" premise read off source is how the worker inherits an unchallenged wrong truth. The read-only review gate above cannot catch these (it reads code, it does not render), so the marking is the only guard.
- When the change is trivial, a short plan is the correct output, not a failure.
- **Length is a tier constraint, not an outcome.** Written plans run long by default; `references/plan-tiers.md` sets the budget and a 10-line diff gets a ~30-line plan. Padding with empty sections is worse than omitting them — `/work` treats every section as work to do. Full length calibration in `feature-spec-pipeline/skills/work/references/model-and-effort.md` §7.
- **Model routing by tier (REVIEWER ≥ WRITER)** — and effort is the second dial, canonical in `feature-spec-pipeline/skills/work/references/model-and-effort.md`: readers at `low`, Trivial/Small synthesis at `medium`, Standard/Large synthesis and this gate at `high`. Step effort down before model down; a strong model at low effort keeps the capability class the invariant below is really about. Trivial/Small synthesis may run on a cheaper model (sonnet). Standard synthesis runs on the strongest model (opus) — or on glm-5.2-high via the zero CLI, in which case the step-5 gate is doubly mandatory. Large synthesis never downgrades. Whatever wrote the plan, the gate's reviewer must be at least as strong as the strongest model that wrote it — and step 5 routes it **out of family** to Codex `gpt-5.6-sol` at `max` effort, which satisfies that bar and adds the independence an in-family reviewer cannot.
