# Orchestration model — context, worktrees, and when to use agents

This is the reasoning behind how `ship-feature` runs. Read it before you start; it prevents the two failure modes that ruin a long conductor flow — **losing the thread** (context evaporates mid-pipeline) and **fragmenting the feature** (work scattered across branches that can't be merged as one).

## 1. Stay in-session and sequential across stages

The pipeline is a chain where each stage needs the *accumulated* understanding of the ones before it: the feature's intent, the UI decisions the design stage made, the nuances triage recorded, the plan's shape, what `/work` actually built, and what it deferred. If you delegate a whole stage to a subagent, that subagent starts cold — it sees only what you pass it, not the running understanding — and it returns a summary that *you* then have to re-absorb. Over eight stages that lossy round-trip compounds into drift.

So: **you invoke each stage-skill in this same session** (via the Skill tool). Its SKILL.md loads into your context, you execute it, and the understanding stays in one head — yours. You are the conductor holding the score from first note to last, not a dispatcher forwarding tickets.

This is also why you do **not** wrap the whole pipeline in a single `Workflow` script. A deterministic script can fan out beautifully, but it cannot make the judgment calls that live *between* these stages:
- Are triage's Essential Questions real blockers only the human can answer, or did triage just default them?
- Did `/work` leave genuinely-deferred scope, or is the feature complete?
- Is an e2e red a real product bug to fix, or an environment flake to reframe?
- Are the gates green *enough*, and the findings resolved *enough*, to justify an irreversible merge?

Those are conductor decisions. Keep them in-session.

## 2. Parallelism belongs *inside* each stage, not on top of it

Not delegating *stages* to subagents does **not** mean the run is single-threaded. Every stage-skill already fans out to subagents via the Workflow tool where it pays off:
- **triage** — parallel readers for codebase-grounding + the Sentinel lens scan.
- **plan** — one reader per subsystem the spec touches.
- **work** — file-disjoint implementation slices, plus review + adversarial-verify fan-out in the acceptance phase.
- **gap-fix** — one auditor per dimension, plus verify.
- **acceptance-e2e** — an Explore/general-purpose breadth-read of the feature's code.

That parallelism is safe and desirable, and it does **not** cost you context, for one reason: **those leaf agents re-read the persisted artifacts from disk** — the spec (which carries the verbatim feature description + every triage answer), the plan, the design-system mock UI — so each re-acquires the exact grounding it needs and returns a synthesized result. The wide, token-heavy reads happen in the leaves; the high-level thread stays with you. Let the stages fan out as they're written to; don't add your own agent layer on top of them.

Cost note — route the lanes, not everything strong. Heavy fan-out on the strongest model burns the interactive allowance fast, and the pipeline's back-loaded verification (Phase D/E, adversarial verify, completeness critic, e2e green-twice, the fail-closed merge) makes mid-pipeline downgrades safe. Single-feature runs use the same lane table as the fleet (ship-fleet's `references/scheduling-and-concurrency.md` carries the propagation mechanics):

| Lane | Model |
|---|---|
| Leaf readers (triage grounding, plan investigation, work Phase A) + gate-runner subagents | haiku |
| Evidence lenses (UI fidelity, clause table, reachability) · adversarial finding-verifiers · e2e Phases 0–4 · design leaf verifiers + page assembly from existing composites · Sentinel verdict + Assumptions (with the triage gate) · plan synthesis Trivial/Small | sonnet |
| Mechanical work Phase B/E slices meeting the delegation criteria | the executor lane order — **agy gemini-flash-3.7 `high` → grok grok-4.6 `high` → codex `gpt-5.6-terra` `medium` → Claude** (ship-pipeline `references/executor-lanes.md` + `codex-cli.md` §R3) |
| **The three out-of-family gates: the triage spec review · the plan review gate · work Phase D's completeness critic** | **codex `gpt-5.6-sol` at `max`, read-only** — sideways, not down |
| Plan synthesis, Standard tier | opus (or glm-5.2-high + the plan skill's mandatory review gate) |
| Plan synthesis Large · work Phase A synthesis · Phase C rebase conflicts · security/guardrails/client-asserted-identity lenses · gap-fix audit over cheap-lane code · e2e Phase 5 judgment + Phase 6 fixes · design aesthetic direction + new composites · merge/finalize/conflict resolution · the Phase 4b deferred-loop classification (small-remainder vs child-spec) | opus — never downgrade |

**Effort is the column this table doesn't have.** Model sets the capability class; `effort` sets how much work happens inside it, and an agent spawned without one runs at `high`. Per-lane levels — `low` for leaf readers and gate-runners, `low`–`medium` for evidence lenses, `high` for synthesis and judgement, `xhigh` with `max_tokens` ≥64k for a long-horizon runner — plus the rule that a review lane should drop *effort* rather than *model* when you need it cheaper, are canonical in ship-pipeline's `references/model-and-effort.md` and `references/model-lanes.md`.

Two invariants bind every lane: **REVIEWER ≥ WRITER** — for every artifact the strongest reviewer is at least as strong as the strongest model that wrote it — and **wire-level model verification** (a first-action self-check for the lane's model + a transcript grep; launch parameters have been observed not to stick), plus the per-lane revert-rate kill-switch from ship-pipeline's `references/executor-lanes.md`. The executor lanes are optimizations with an **Opus fallback**: any lane failure (binary/key missing, wrong model on the wire, repeated errors, kill-switch tripped) routes the work back to Claude — never to another cheap lane, never silently skipped.

The **Codex `max` gate row is a different kind of routing** and shouldn't be read as a cost lane. It is there for *independence*, not savings: every other reviewer in this pipeline is Claude auditing Claude's own output, and a reviewer from the same family shares the blind spot that let the defect through. So those three checks move **sideways** out of family rather than down a cost tier, and they satisfy REVIEWER ≥ WRITER on their own terms. They are mandatory where Codex is available; where it isn't, the in-family fallback runs and the downgrade is **recorded in the artifact** — an in-family review of in-family work is weaker evidence, and whoever reads the pre-merge gate deserves to know which one they got. The kill-switch does not apply to them: a reviewer that keeps finding real defects is working, not thrashing.

## 3. The pipeline's memory is on disk, not just in the transcript

This is the fact that makes everything above work. Each stage writes durable artifacts:

| Stage | Durable artifact(s) |
|---|---|
| design | the mock index + state matrix (`design/mocks/<id>/INDEX.md`), review-gated |
| triage | `docs/specs/spec-<ID>.md` (verbatim feature description + triage answers/assumptions), `LEDGER.md` |
| plan | `docs/plans/<id>.md` (committed, referenced by sha) |
| work | the implementation on `ai/<id>`, `## Progress` note on the spec (reachability + clause tables, deferred list) |
| gap-fix | `## Gap-fix` note on the spec |
| acceptance-e2e | `apps/web/e2e` specs + the AC-traceability matrix |

Two consequences you should exploit:
- **Re-read at each phase boundary.** Don't trust the transcript for what the spec or plan says at the moment you hand off — open the file. It's authoritative and it may have been edited (by a human, or by a re-triage).
- **The run is resumable.** If the session is compacted or interrupted, you don't restart — you re-enter at the first phase whose artifact is missing or not-yet-green (the SKILL.md "Resuming" section maps this out). Disk is the checkpoint.

## 4. One feature = one branch = one worktree

Worktrees are already central to this pipeline — `/work` creates `.worktrees/<ID>` on branch `ai/<id>`, and `/gap-fix` re-enters it. Your job is to **not disturb that**, and specifically:

- **The conductor lives in the main working tree.** That's where the docs are (`docs/specs`, `docs/plans`, `LEDGER.md` — every sub-skill reads them from the main tree because they're untracked on the feature branch) and where the design stage iterates on the mock UI. You never `cd` into the worktree yourself; `/work` and `/gap-fix` do their code edits there via absolute paths.
- **Never open a second worktree.** The naive reading of "child spec → child `/work`" would have `/work` create `.worktrees/DIO-child` on a *new* branch — fragmenting the feature so it can't "be merged" as one unit. Keep all implementation — parent, deferred, child — on `ai/<id>` in the one worktree (see `deferred-work-loop.md` for the mechanics).
- **The worktree is the local sandbox for e2e too.** The feature isn't on production yet, so the acceptance suite runs against the app served from the feature branch's worktree, not the deployed/production URL (see `e2e-and-finalize.md`).
- **The final phase collapses the worktree.** After the merge + push, `git worktree remove .worktrees/<ID>` and delete the merged local branch — the worktree existed only to isolate the in-progress feature from the main tree; once merged it has no reason to linger.

## TL;DR

You are an in-session conductor. Run stages **sequentially in your own context** to keep the thread; let each stage **fan out internally** to do wide work; treat **disk as the shared memory and the resume checkpoint**; keep the whole feature on **one branch in one worktree** that `/work` owns and the final phase removes. Delegation and worktrees are tools the *stages* wield — your job is to sequence them and judge the seams.
