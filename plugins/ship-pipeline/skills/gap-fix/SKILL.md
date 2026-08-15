---
name: gap-fix
description: >-
  After /work has implemented a feature spec, close whatever it still missed versus the original spec by auditing the delivered code and fixing the gaps in code. Re-enters the branch /work produced and ALWAYS re-audits the code against the spec (docs/specs/spec-DIO-0001.md) and plan — merging in any gaps you hand it (inline, a file, a `## Gaps` section, or a QA list) — then fixes them as production code, looping audit→fix until only Low items remain. Commits locally; no push, no PR — the branch stays local for review. Use whenever a built feature still falls short of its spec and you want it finished — e.g. "gap-fix DIO-0001", "the worker missed X, close it", "address what /work didn't cover for DIO-0001", "finish the gaps left after implementing DIO-0001", "the build doesn't fully match the spec — fix the code", or after a review/QA pass lists what's missing. Unlike spec-validation (audit-only), gap-fix fixes; unlike /plan and /work (full builds), it only finishes what's left. No issue tracker, no Agent SDK.
---

# Feature Spec Gap-Fixer (post-work remediation)

Finish the job `/work` started: close whatever the delivered implementation still misses versus the **original spec**, by **fixing it in code** on the same local branch `/work` produced. This is the pipeline's remediation step — it runs *after* `/work`, reuses `/work`'s acceptance-review + resolve + finalize muscle, and leaves the branch **local** for human review (no remote PR).

You run **in your current session** as the orchestrator, using `Read`/`Write`/`Edit`/`Glob`/`Grep`/`Bash` and the `Workflow` tool. No issue-tracker MCP (Diolog Tasks or otherwise), no Agent SDK. The spec markdown file is the requirement source of truth and the place you record your progress.

## Inputs

- A spec id (`DIO-0001`). `/work` should already have implemented it: branch `ai/<id>` in worktree `.worktrees/<ID>`, with `docs/specs/spec-<ID>.md` at `In Review` and a plan at `docs/plans/plan-<ID>.md`.
- **Optional provided gaps** — what a human/QA review (or any external check) found missing: inline in the prompt, a file path, or a `## Gaps` section in the spec. These are **merged into** the self-audit (see Phase A); they never replace it.
- Optional `--dry-run` intent: audit and report the gaps + the fixes you'd make, but change no code.

Throughout: `<ID>` is the uppercase id (e.g. `DIO-0001`, used in file names and the commit `Resolves` line); `<id>` is its lowercase form (e.g. `dio-0001`, used in the branch name).

## Setup (before any phase)

1. **Find the work branch and worktree.** From the target repo root:
   - If `.worktrees/<ID>` exists, reuse it. Let `WT` = its absolute path.
   - Else if the branch `ai/<id>` exists, recreate the worktree on it: `git worktree add .worktrees/<ID> ai/<id>`.
   - Else `/work` hasn't run (or its branch is gone): there's no implementation to fix. Say so and recommend running `/work <ID>` first — end with `NEEDS WORK`. (Do not start a build from scratch; that's `/work`'s job.)
2. **Read the spec and plan from the main working tree** at `docs/specs/spec-<ID>.md` and `docs/plans/plan-<ID>.md` (the worktree is branched from the integration branch and won't contain the untracked docs). The spec's `## Feature description` + the latest `## Triage` (Assumptions and any human answers/edits) are the **requirement source of truth** — human answers are authoritative. The plan is the secondary reference for *what was supposed to be built*. If the spec status isn't `In Progress`/`In Review`, flag that `/work` may not have completed and proceed cautiously.
3. Do all code edits and git commands **inside the worktree** (`WT`) — absolute paths or `git -C "$WT"`. When you fan out subagents, give each the absolute worktree path and a **disjoint** file scope. The spec/plan docs are NOT code — leave them in the main working tree; don't commit them onto the branch.

## How you must run this — ultracode dynamic workflows

You are the **orchestrator**, not a single-pass fixer. Drive the work as dynamic workflows, staying in control between phases (read each phase's result, then launch the next). Decompose a large gap set across workflows and deliver it in full — **don't bail because there are many gaps; that's what this approach is for.** Stop only on genuine missing information that makes a safe fix impossible — then append a blocker note to the spec and stop. Production code only — no mocks, stubs, placeholders, or fallbacks (CLAUDE.md guardrails).

### Workflow fan-out limits (avoid throttling) — apply to EVERY phase

- **Cap each wave at ≤4 concurrent agents.** Batch larger fan-outs into sequential waves of ≤4 and `await` each small `parallel(...)` before the next — firing ~10+ at once trips a server-side rate limit ("temporarily limiting requests — not your usage limit") that fails most of the wave. Don't pass all items to one `parallel()`.
- **Retry transient failures.** If an agent result is an "API Error / Rate limited / temporarily limiting requests" string (or `null`), re-run it in a later batch; never treat it as a real finding or result.
- **Prefer plain-text returns for long, file-reading subagents.** Schema-forced readers often finish without emitting structured output; have each return a fixed-shape markdown fragment and reserve any `schema` for the single synthesis step.

Run the phases **in order; none may be skipped.** After each phase, check its output against **both** the plan and the spec (original feature description + every triage answer); fix any drift before advancing. That check is a **conformance** question — did this phase drop or half-build a stated requirement — answered with evidence (the clause, the `file:line`, the gate you ran). It is not a second correctness review layered on a phase that already reviewed itself; `feature-spec-pipeline/skills/work/references/model-and-effort.md` §6 draws the line.

### Phase A — Audit the build vs the spec (always)
Fan out parallel reviewer subagents auditing the **implemented worktree code** against the spec's original feature description + every triage answer (especially human corrections and UI amendments), the plan, and any UI mocks. Use the **same dimension + invariant list as `/work` Phase D** so the two audits can't diverge and let a gap slip between them. One reviewer per dimension: (1) **requirement completeness** — every functional + UI requirement (and every plan Acceptance Criterion) is fully implemented, not partial or stubbed; (2) **correctness** — bugs, data flow, edge cases; (3) **guardrails** — no mocks/stubs/fallbacks; auth/BFF patterns; every authorization/ownership/attribution/governance decision enforced server-side at READ and WRITE (never on a client-supplied value); (4) **UI fidelity** — copy, badge labels, states vs the mocks; (5) **security** — visibility leakage, multi-company/tenant isolation, secrets, injection + untrusted input; (6) **simplicity & surgical diff (Karpathy)** — no speculative abstraction, dead scaffolding, unrequested config, or bloat, and no drive-by refactor outside the changed slice. **Adapt dimension 3's specifics to THIS repo's real invariants** (read its `CLAUDE.md` + the plan's *Constraints & Decisions*) — in one reference product (an IR app) that means prompts in the `prompts` collection, AI via the gateway (no direct provider SDK), MNPI enforced at READ and WRITE, citation-tag stripping; for any target repo, substitute *its* load-bearing rules. **Audit the WHOLE delivered surface on the branch against the FULL spec — never scope to the slice the latest progress note calls "in scope".** Enumerate every content kind, enum value, contract arm, and subfeature the branch actually ships (grep the diff, not the notes) and audit each: a progress note that says "site path only" does not exempt the deck/document/spreadsheet code that is nonetheless sitting on the branch — un-audited shipped code is exactly what breaks on first use. Reachability includes contract arms with no in-product producer (see `/work` Phase D). **Merge in every provided gap** (from the prompt / file / spec `## Gaps`) as additional findings to confirm. Tag each finding **Critical / High / Medium / Low** with `file:line` and the exact spec/plan/mock clause it violates. Then **adversarially verify — aimed, not blanket:** independent subagents confirm a finding is real against the actual worktree code, which is a precision filter, so spend it on every Critical, every structural fix, and anything reversing a locked decision rather than 1:1 on Lows. Never brief a reviewer to be conservative or to report only serious findings — that is followed literally and lowers recall; report everything and filter here. Close with a **completeness critic** subagent that attacks the audit itself — which acceptance clause was never matched to a `file:line`, which reachability hop was never traced, which critical seam was read but never exercised — and feed what it finds back into another audit round. A provided gap that the code already satisfies is recorded as already-met, not re-fixed.

### Phase B — Fix the gaps in code (implement)
Resolve **every confirmed gap at all severity levels** (Critical → Low) as production code in `WT`. For a gap that is a bug, fix it **reproduce-first** (write the failing check that demonstrates the gap against the real, un-stubbed path, then make it pass — Karpathy "goal-driven"); for a "missing requirement" gap, wire it end-to-end and exercise the real path, don't just add the symbol. Fix **surgically and simply** (Karpathy): the fix touches only what the gap names, matches existing style, adds no speculative abstraction, and does not extend into adjacent cleanup — every changed line traces to a confirmed gap. Parallelize ONLY file-disjoint fixes — **never two subagents editing the same file at once**; serialize overlapping ones. Respect dependency order (backend schema/service/resolver → `pnpm graphql:codegen` after schema changes → BFF → frontend). After each wave, a gate subagent runs the scoped `pnpm typecheck` / `pnpm graphql:codegen` / `pnpm validate:graphql` (the reference product's gates — substitute the target repo's own typecheck/codegen/validate commands) and reports failures; the next wave waits for green. Commit in `WT` (stage only files you created/modified — never `git add .`). **Loop Phase A → Phase B until *two consecutive* fresh audits — different reviewer lenses, plus the completeness critic — surface no new confirmed Critical/High/Medium** and only optional Low items remain (one quiet pass is a shallow fixpoint, not a dry one); document any Low you intentionally defer.

### Phase C — Finalize
Run the full gates (`pnpm validate:all`, `pnpm validate:graphql`, `pnpm typecheck`, `pnpm lint` — or the target repo's own equivalents, scoped sensibly) and commit any outstanding fixes in `WT`. **Do NOT push and do NOT open a PR** — the branch stays local for human review. Append a gap-fix progress section to the **spec in the main working tree** (`docs/specs/spec-<ID>.md`):

```markdown
## Gap-fix — <YYYY-MM-DD>

**Post-work remediation (local branch — no PR)**

**Audit:** <N gaps found — Critical/High/Medium/Low counts> (self-audit + <M provided>); <K already met, not re-fixed>.
**Closed in code:**
- `[Critical|High|Medium|Low]` <gap, one line> → <files changed / what now satisfies the spec clause>.
**Deferred:** <any Low intentionally left, with reason — omit if none>.
**Branch:** `ai/<id>` (local, rebased by /work on the integration branch it detected — e.g. `origin/staging` or `origin/main`; not pushed; worktree: .worktrees/<ID>).
**Gates:** validate:all / validate:graphql / typecheck / lint — <pass/fail>.
```

Keep the spec `Status: In Review` (refresh `Last updated`); never downgrade. **Do not edit `plan-<ID>.md`** — gap-fix closes gaps in the build, not in the plan document. (If a residual gap can't be fixed without a human decision, append a blocker note, leave status as-is, and stop — `NEEDS TRIAGE`.)

## Commit convention

`<type>(<scope>): <summary under 72 chars>` (types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`), a short body, a `Resolves <ID>` line, and `Co-Authored-By: Claude (AI Assistant) <noreply@anthropic.com>`. Stage only files you created or modified — never `git add .`.

## Guidelines

- **The spec is the authority.** A gap means the delivered code falls short of the spec (or a human triage answer); fix the code to meet the spec. Human answers override assumptions, which override your own inference. A provided "gap" that contradicts the spec (asks for something the spec scopes out) is **not** a gap — record it as out-of-scope and don't implement it.
- **Targeted finisher, not a rebuild.** Fix what's missing; don't re-implement what `/work` already delivered correctly, and don't extend into adjacent features or cleanup. If almost nothing was built (the branch is essentially empty), that's a `/work` job, not gap-fix — say so (`NEEDS WORK`).
- **Always audit, even when gaps are provided.** Provided gaps are a floor, not a ceiling — a QA list is rarely complete. Merge them into the dimension audit so you also catch what the reviewer missed.
- **Production code only.** Follow the target project's `CLAUDE.md`. No mocks/stubs/placeholders/fallbacks to "close" a gap. Block only on genuine missing information; never ship partial or stubbed work to dodge a block.
- **Do NOT push and do NOT open a PR.** The work stays local in the worktree, committed, for human review. The only writes outside the worktree are the spec progress note + `Last updated`.
- **Effort is the second dial.** `feature-spec-pipeline/skills/work/references/model-and-effort.md` is canonical: `low` for grounding/reader agents, `low`–`medium` for evidence lenses, `high` for the judging lenses; an agent spawned without an explicit effort runs at `high`. Step effort down before model down — a strong model at low effort keeps its capability class, so it satisfies the REVIEWER ≥ WRITER bar below where a model downgrade would not.
- **Model routing (cost note): the audit IS the value here.** The auditor must be **at least as strong as the strongest model that wrote the code under audit** — if external executor lanes (codex/composer/glm) implemented any of it, the audit runs on the strongest model (opus), no exceptions; and **security-lens findings are always found and verified on the strongest model** regardless of who wrote the code. Grounding/reader subagents can run cheaper (haiku) — they collect evidence, they don't judge it — but the judging lenses obey the REVIEWER ≥ WRITER bar above. Fixes follow the same split as `/work` Phase B: mechanical, well-specified fixes may take the external executor lanes (codex `gpt-5.6-sol` at `medium` by default, per `../work/references/codex-cli.md` §R3, else the ship-fleet skill's `references/cursor-composer.md` — delegation criteria + verify-fix loop + fail-back rule apply either way); judgment fixes stay on the strongest model. A gap-fix audit is itself a candidate for the out-of-family completeness critic (`codex-cli.md` §R2) when the code under audit was written by Claude — the same blind-spot argument applies.
