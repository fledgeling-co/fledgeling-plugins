---
name: ship-feature
description: >-
  End-to-end feature delivery conductor — takes ONE feature (inline text or a markdown file) from bare idea to a merged, tested, production-ready feature by orchestrating the existing skills in a single in-session flow: design-craft (whole UI in the design system) → triage → plan → work (isolated git worktree) → deferred-work loop → gap-fix → acceptance-e2e (Playwright, run locally vs the branch) → commit, rebase, merge, push, clean up. Use whenever someone wants a feature taken ALL THE WAY — "ship this feature end to end", "run the full pipeline on <feature>", "take this feature from description to merged", "build and ship <feature.md>", "design, spec, build, test and merge <feature>", "do the whole feature for me" — even if they never name the individual skills. Prefer it over invoking triage/plan/work/gap-fix/acceptance-e2e one at a time whenever the goal is a finished, merged feature. NOT for a single stage (use that stage's skill) or the whole backlog (use ship-fleet).
---

# Ship Feature — end-to-end feature conductor

Take **one** feature from a bare description to **merged, tested, production code** by conducting the existing feature-delivery skills in sequence, in a single in-session flow. You are the **conductor**: you hold the feature's intent from the first read to the final merge, invoke each stage-skill in turn, verify its output, carry the right context forward, and make the judgment calls *between* stages that no single stage can make.

The order is fixed and each stage's real work is owned by its skill — you don't re-implement triage/plan/work here, you **run them and thread them together**:

```
feature (text / .md)
  → design-craft   represent the whole feature UI in the design system (elements/composites/mock pages)
  → triage         → docs/specs/spec-DIO-XXXX.md   (allocates the id)
  → plan           → docs/plans/plan-DIO-XXXX.md
  → work           implement in .worktrees/DIO-XXXX on branch ai/dio-xxxx  (local, no push)
  → deferred loop  re-work / child triage+plan+work for extra phases — ON THE SAME BRANCH
  → gap-fix        close remaining spec gaps in code                      (same branch)
  → acceptance-e2e comprehensive Playwright suite, run vs the branch locally, bugs fixed
  → finalize       commit → rebase → MERGE into the integration branch → push → clean up worktree(s)
```

## Inputs

- **A feature** — inline text, or a path to a markdown/text file describing the feature. This is the north star; you read it **in full** into context at the start and it stays authoritative for the whole run.
- **Optional: an existing pure HTML/CSS/JS mock UI** for the feature (a file, folder, or URL) — extra design context for the design-craft stage. When absent, Phase 1 authors the full UI reference itself, to the same coverage bar.
- The **target repository** is your product's repo — run from its root. It provides `CLAUDE.md`, a design system (e.g. `apps/web-design-system` + its `tokens/tokens.css`, plus an optional `DESIGN.md` design-language spec when one is provided or present in the repo), the `docs/` tree + `docs/feature-specs/LEDGER.md`, an e2e harness (e.g. `apps/web/e2e`), and the integration branch (`origin/staging`, else the repo default). Locate the repo's own equivalents rather than assuming this exact layout — the paths above are the common defaults, not a requirement.

Throughout: `<ID>` is the uppercase spec id (e.g. `DIO-0001`); `<id>` is its lowercase form (`dio-0001`, used in the branch name). `INT` is the integration branch you **detect** (never hardcode) — `origin/staging` if it exists, else the repo default from `git remote show origin`.

## How you must run this — read the orchestration model first

Before you start, internalise `references/orchestration-model.md`. The three load-bearing decisions:

1. **Stay in-session and sequential across stages.** Invoke each stage-skill in *this* session (via the Skill tool) so you keep the accumulated understanding — the feature intent, the design decisions, the spec's nuances, the plan, what `/work` built, what it deferred. Do **not** hand a whole stage to a subagent; a stage-level subagent loses the thread. Parallelism belongs *inside* each stage — every sub-skill already fans out to subagents via the Workflow tool, and those leaf agents re-read the persisted spec/plan/mock from disk, so they re-acquire grounding without you losing it.
2. **The pipeline's memory is on disk, not just the transcript.** Each stage persists its output (design-system files, `spec-<ID>.md` with the verbatim feature description + triage answers, `plan-<ID>.md`, the `/work` progress + reachability/clause tables, the e2e AC-matrix + specs). Re-read the relevant artifact at each phase boundary rather than trusting conversation memory — that's what makes the run **resumable** if the session is compacted or interrupted (re-enter at the phase whose artifact doesn't yet exist / isn't yet green).
3. **One feature = one branch = one worktree.** `/work` owns the worktree (`.worktrees/<ID>`, branch `ai/<id>`). You (the conductor) stay in the **main working tree** — that's where the docs live and where design-craft iterates. Deferred work and any *child* specs land on the **parent's** branch/worktree, never a new one (see Phase 4b), so the whole feature merges as a single unit.

## Operating discipline

Four habits keep a long conductor run honest — they matter *more* here than in a single skill, because a bad call early is inherited by every stage after it:

- **Scale to the feature — don't over-orchestrate.** The eight phases are a *floor of rigor*, not a mandate to inflate. A genuinely small change (a copy tweak, one new empty state, a single-surface tweak) should *not* spawn a sprawling mock system, child specs, or a hundred-case suite. Let the sub-skills' own size tiers lead (`/plan` classifies Trivial/Small/Standard/Large), compress phases that have nothing to do (a trivial UI change barely touches design-craft; a self-contained feature has an empty deferred loop), and match the change's real size. Over-building is the classic failure mode — a ten-line feature gets a ten-line feature's pipeline, run with the same discipline but not the same *volume*.
- **Surface assumptions; don't fabricate.** At each handoff, be explicit about the assumptions you're carrying forward (the design defaults, the triage assumptions, the scope calls). On *genuine* ambiguity — an essential triage question, a product decision in the deferred loop, two real interpretations of the feature — stop and ask rather than silently picking; the whole pipeline would otherwise inherit a wrong premise and faithfully build the wrong thing.
- **Deliver surgically.** The final merged diff should trace to *this feature*. No drive-by refactoring of adjacent code, no "improving" unrelated design-system components, faithful rebase-conflict resolution (integrate both sides, drop nothing), and stage only files you created or modified — never `git add .`. The sub-skills already enforce this; hold them to it and don't let the extra reach of an orchestrator become an excuse to sprawl.
- **Verify with oracles, not by re-reading.** Turn the feature into verifiable success criteria at Phase 0 and carry them as the acceptance oracle every stage measures against. Every gate is *actually run*, never inferred; every new critical path is *exercised* un-stubbed; the out-of-family gates run. Those acquire evidence no amount of thinking produces, and they are non-negotiable. What is not worth stacking is a separate pass whose only job is re-reading a stage's own output for correctness — the stages already do that internally, and a layer on top costs tokens without adding recall (the distinction, and where adversarial finding-verification is still worth aiming, is in `feature-spec-pipeline/skills/work/references/model-and-effort.md` §6). When e2e finds a real bug, the failing assertion *is* the reproduction — fix the code, then re-run the gate. "Done" means verified-green (Definition of done), never assumed-green.
- **Front-load the whole brief, then run.** A complete specification handed over once and left to execute is the condition this pipeline performs best under — which is what makes Phase 0's single consolidated question round and its acceptance criteria load-bearing: they complete the brief *before* eight phases start amplifying it. Discovering scope one phase at a time is how a stage builds faithfully against a premise the next stage contradicts.
- **Report thinly.** One sentence before a phase starts, an update only when something material lands or you change direction, outcome first at the close. Written artifacts get the same calibration — cover the substance and stop; a progress note is tables and decisions, not a narrative of the run (`model-and-effort.md` §7).

## The phases — run in order; none may be skipped

After each phase, verify its output against the **feature description** (and, once they exist, the spec + plan) before advancing. Fix drift before moving on. The run is not done until Phase 7 has merged and cleaned up — or has stopped at a gate and told the human exactly why.

### Phase 0 — Intake & grounding
Read the feature **in full** into context. **Establish its verifiable success criteria** — the handful of things that must be true for it to be *done* (the user-visible behaviours, the states, the guardrails). This is the acceptance oracle you carry through every stage: triage/plan refine it, `/work` builds to it, e2e asserts it, the pre-merge gate checks against it. A feature reduced to "make it work" forces re-clarification at every seam; a feature reduced to concrete criteria lets each stage run to a clear bar. Then locate the moving parts in the target repo so later stages don't re-discover them: the design system (`apps/web-design-system`, plus an optional `DESIGN.md` design-language spec when provided or present), the `docs/` tree + `docs/feature-specs/LEDGER.md`, the e2e harness (`apps/web/e2e`), and the integration branch `INT` (detect it now). If any required location is genuinely absent or ambiguous, or the feature has two real interpretations, ask **one** consolidated round of questions before building rather than guessing. Note whether an optional mock UI was supplied. Gauge the change's **size** here too — it sets how much of each phase is real work vs. a quick pass (see Operating discipline: scale to the feature).

### Phase 1 — Design representation (`design-craft`)
Invoke **`/design-craft`** to ensure the feature's **entire** UI is represented in the design system — every surface, state, **user interaction, user flow, and overlay (popup/modal/drawer/menu)** it needs, as design-system elements/composites/pages, adding new elements/composites where the system lacks them. **This bar holds with or without a supplied HTML mock:** when none exists (the normal case), design-craft *authors* the reference from the feature description + the existing design system — a mock is a hint, never a prerequisite, and its absence never licenses a thinner representation. Full procedure (the grounding inputs, the no-mock authoring path, the completeness bar, and how the resulting mock UI is **carried onto the feature branch** so it merges with the feature) is in `references/design-representation.md`. The output is twofold: the updated design-system mock UI **on disk** (the visual source of truth every later stage cites), and a short **UI inventory** you keep in context (surfaces × states × interactions/flows × overlays × components). Verify the mock renders before advancing — a design phase that "type-checks" but renders blank has represented nothing.

### Phase 2 — Triage (`triage` → spec)
Invoke **`/triage`** on the feature, **naming the design-system mock UI from Phase 1 as context** so the readiness review reflects the real surfaces. It allocates the id and writes `docs/specs/spec-<ID>.md`. Capture the `<ID>` it prints — every later phase keys off it.
- If triage ends **READY**, continue.
- If triage ends **NEEDS IMPROVEMENT** with Essential Questions, those are gaps only a human can settle. **Do not fabricate answers.** Surface the questions to the user, stop, and resume from Phase 2 (re-triage) once answered. Non-essential gaps triage already defaulted (its Assumptions block) — those don't block you.
- **Confirm its Codex cross-family review actually ran** (a `gpt-5.6-sol` `max`-effort read-only review of the spec against the codebase, per the triage skill's own gate) and that its findings were dispositioned. A missing verdict in the triage section means the gate was skipped, not that the spec was clean — send it back. An `unavailable → claude` downgrade is acceptable; carry it forward as a known weakness in the evidence.

### Phase 3 — Plan (`plan` → plan)
Invoke **`/plan <ID>`**. It writes `docs/plans/plan-<ID>.md` and moves the spec to `Ready for Work`. If plan ends **NEEDS TRIAGE**, the spec isn't plannable yet — loop back to Phase 2 (re-triage), don't invent a plan. As at Phase 2, **verify the plan review gate ran and landed**: the mechanical path check plus the Codex `gpt-5.6-sol` `max`-effort cross-family review, with every finding accepted-and-fixed, rejected-with-a-reason, or escalated. The plan is the artifact every later stage amplifies — an unreviewed plan is the most expensive thing you can carry forward.

### Phase 4 — Work (`work` → implementation)
Invoke **`/work <ID>`**. It creates `.worktrees/<ID>` on `ai/<id>` from `INT`, implements the plan (understand → implement → rebase → acceptance-review → resolve → finalize), and leaves the branch **local**. Make sure it treats the Phase-1 mock UI as UI truth. When it finishes, **read its `## Progress` section on the spec** — the reachability + clause tables and its "Deferred" note are the input to Phase 4b. The note also carries the **Codex lane accounting**: the out-of-family completeness critic that closes Phase D (`gpt-5.6-sol` at `max`) and the `medium`-effort executor's task / retry / revert counts. A progress note with no critic line either skipped Phase D's last reviewer or lost it to an unlogged fallback — chase that before you build on the result.

### Phase 4b — Deferred / additional-work loop (same branch)
`/work` delivers the plan, but a large feature often leaves **explicitly deferred items or additional phases**. Read the spec progress note + the plan and decide (full decision tree in `references/deferred-work-loop.md`):
- **Nothing deferred** → go to Phase 5.
- **Small, in-scope remainder** (a missed state, one more slice) → re-run **`/work <ID>`** (it reuses the existing worktree) or fold it into Phase 5's gap-fix.
- **Substantial new scope that deserves its own spec** → **`/triage`** a *child* spec (linked to the parent), **`/plan`** it, then **`/work`** it — but **on the parent's branch/worktree, not a new one** (see the reference for how to keep `/work` on `ai/<id>`). 
Loop until no outstanding phase or deferred item remains. Keep every child spec/plan path — Phase 6's e2e must cover them too.

### Phase 5 — Gap-fix (`gap-fix` → close remaining gaps)
Invoke **`/gap-fix <ID>`** against the spec (+ plan + feature + the Phase-1 mock UI). It re-audits the delivered code against the original spec and fixes every confirmed gap in code on the same branch, looping audit→fix until only optional Low items remain. This is the belt-and-braces finisher before tests — run it even if `/work` looked complete.

### Phase 6 — Acceptance E2E (`acceptance-e2e` → tests, run & fixed)
Invoke **`/acceptance-e2e`** to build a **comprehensive** Playwright suite covering **every** user flow, action, interaction, and menu the feature exposes — derived from the feature description + `spec-<ID>.md` + `plan-<ID>.md` **and every child spec/plan** from Phase 4b (hand it all of them; incomplete inputs give incomplete AC coverage). Crucial adaptation for a not-yet-merged feature: the suite must run against **the feature branch's app running locally**, not the deployed/production URL (production doesn't have the feature yet) — see `references/e2e-and-finalize.md`. Author the specs on the feature branch (so they merge with it), run the suite **green twice** (proves isolation + no flakes), and fix the tractable product bugs it surfaces. A real content/AC failure is the suite doing its job — fix the code, don't water down the assertion.

### Phase 7 — Finalize: commit → rebase → merge → push → cleanup
Only now, and only behind a **fail-closed pre-merge gate**, land the feature. Exact mechanics + the gate checklist are in `references/e2e-and-finalize.md`. In outline: confirm every gate is **actually green** (not inferred) and the e2e suite passed twice; commit anything outstanding on `ai/<id>`; do a final `git fetch` + rebase onto the **fresh** tip of `INT`, resolving conflicts faithfully; re-run the gates; **merge `ai/<id>` into `INT` directly (no PR)** and **push**; then remove the worktree(s) (`git worktree remove`) and delete the merged local branch(es). Finally set the spec header `Status: Done` (Merged) with the merge commit / date, and update the ledger row. **If any gate is red or unverifiable, STOP before the merge** and report exactly what blocks it — never push broken or unproven code, even in full-auto mode.

## Hard rules

- **The feature description is the north star; the spec is its authority downstream.** Human triage answers > triage assumptions > your inference. Never let a later stage quietly reverse a decision an earlier stage recorded.
- **Never skip a stage, and never fake a gate.** Every phase runs; every gate (typecheck / codegen / validate / lint / e2e) must be **actually executed**, not assumed. A green typecheck is not proof a feature works — the sub-skills already enforce this; hold them to it and don't merge on inferred green.
- **The out-of-family gates are gates, not garnish.** Three points in this pipeline route to Codex `gpt-5.6-sol` deliberately — the triage spec review and the plan review (both at `max` effort), and the completeness critic that closes `/work`'s Phase D (also `max`). They exist because every other reviewer here is Claude auditing Claude, and an author-judged oracle is how a family's blind spot ships green. Verify each one ran and its findings were dispositioned. If Codex was genuinely unavailable, the in-family fallback is a **logged downgrade you carry into the pre-merge evidence** — never a silent pass.
- **Respect the repo's egress opt-out, and don't treat it as a failure.** Every Codex call ships the artifact and the files it reads to OpenAI (`-s read-only` restricts writes, not the network). A repo whose `CLAUDE.md`/`AGENTS.md`/`ORCHESTRATOR.md` carries `ANTHROPIC-ONLY`, `NO EXTERNAL MODEL CLIS`, or `external-model-clis: off` is **opted out**: every gate runs in-family, that satisfies the pre-merge gate, and you neither request an exception nor report the run as degraded. Re-check the marker before each Codex call rather than once — it is the only kill-switch that reaches a stage already in flight.
- **Fail closed at the merge.** Full-auto means "auto-merge a genuinely green, verified feature," not "merge whatever's on the branch." Any red/unverifiable gate, any unresolved Critical/High/Medium finding, any e2e failure that's a real bug ⇒ stop before merge and report.
- **One branch, one merge.** All work — parent, deferred, and child specs — lands on `ai/<id>`. Don't fragment a feature across branches; don't open a second worktree.
- **Don't fabricate answers to Essential Questions.** If triage/plan surface a gap only the human can resolve, stop and ask; resume when answered.
- **Docs stay in the main tree; code stays on the branch.** The spec/plan/ledger are the pipeline's issue tracker (the markdown stand-in for a hosted tracker like Diolog Tasks), read from the main working tree — never commit them onto the feature branch. The design-system mock UI is code and rides the branch (Phase 1 reference). At Phase 7, **after** the merge, commit the docs on the integration branch itself (see `references/e2e-and-finalize.md`) so the merged feature has a durable, tracked record — untracked-forever docs are how a shipped feature ends up with no committed spec.
- **Stay in-session across stages; let stages fan out internally.** Don't wrap the pipeline in one Workflow script and don't delegate a stage to a subagent — you'd lose the thread. Re-read the on-disk artifact at each phase boundary.

## Definition of done

The run is complete only when: the feature's UI is represented in the design system; `spec-<ID>.md` (+ any child specs) and `plan-<ID>.md` (+ any child plans) exist; the implementation, deferred work, and gap-fixes are all on `ai/<id>` and green; a comprehensive e2e suite covering every flow/action/menu passed **twice** with tractable bugs fixed; the branch is rebased on the fresh `INT`, **merged, and pushed**; the worktree(s) and merged branch(es) are removed; and the spec + ledger read `Done`. If you stopped at a gate instead, say so plainly with the exact blocker — a stopped-at-a-gate run is a correct outcome, a silently-half-shipped feature is not.

## Resuming an interrupted run

Because state is on disk, re-enter at the first phase whose artifact is missing or not-yet-green: no `spec-<ID>.md` → Phase 2; spec but no `plan-<ID>.md` → Phase 3; plan but no `.worktrees/<ID>` / no `## Progress` note → Phase 4; progress note but deferred items open → Phase 4b; built but no gap-fix note → Phase 5; no e2e specs / suite red → Phase 6; all green but unmerged → Phase 7. Re-read the artifacts to rebuild context; don't restart from Phase 0.

## References

- `references/orchestration-model.md` — the context-preservation, worktree, agent-usage, and model-routing model, including the lane table subagents route by (read this first).
- `references/design-representation.md` — Phase 1 in full: the DESIGN.md + apps/web-design-system grounding, the optional mock, the completeness bar, and carrying the mock UI onto the feature branch.
- `references/deferred-work-loop.md` — Phase 4b decision tree + keeping child specs on the parent branch.
- `references/e2e-and-finalize.md` — Phase 6 local-app e2e run + Phase 7 fail-closed pre-merge gate, merge, push, and worktree cleanup.
