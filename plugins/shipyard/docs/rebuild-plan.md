# Ship pipeline rebuild — merged design plan

**Date:** 2026-08-15 · **Branch:** `ship-pipeline-rebuild`
**Sources merged:** four intake reads (diolog ship-feature/ship-fleet/feature-spec-pipeline; diolog-tasks-pipeline; fledgeling ship-armada + clarify; mattpocock/skills incl. wayfinder; eve-software-factory-template), the trawl feedback corpus (incl. `~/Dev/dAIolog/docs/reviews/pipeline-skills-improvement-analysis.md` — the WEB-4905 110-ticket audit, 46% delivered-as-specified), a four-backend Dossier research panel (OpenAI gpt-5.6-terra, Gemini, Perplexity sonar-deep-research, xAI grok-4.6; ~$9.70; fabrication check PASS on the two load-bearing reports), and the three Anthropic prompting documents read in full.

## The shape

Four plugins in fledgeling-plugins, replacing five plugins spread across two marketplaces:

| Plugin (working name) | Replaces | Role |
|---|---|---|
| `ship-pipeline` | feature-spec-pipeline + diolog-tasks-pipeline (merged) | The stage skills: `pipeline-intake`, `pipeline-triage`, `pipeline-plan`, `pipeline-design`, `pipeline-work`, `pipeline-verify`, `pipeline-gap-fix` + shared references (tracker adapter, model lanes, evidence rules, second-opinion lanes) |
| `ship-feature` v2 | diolog ship-feature | Conductor: one feature, idea → merged, orchestrating the stage skills |
| `ship-fleet` v2 | diolog ship-fleet | One repo's backlog: survey → ORCHESTRATOR.md → N ship-feature runners |
| `ship-armada` v2 | fledgeling ship-armada 1.2.1 | Portfolio: survey/plan/route/dispatch/daemon over ~/Dev |

One substrate abstraction kills the twin-drift problem: every stage skill reads/writes through a **tracker adapter** (markdown lane: specs + LEDGER.md; tasks lane: a tasks MCP), the same way wayfinder abstracts its tracker. The canonical phase text exists once.

## Design decisions and their evidence (traceability)

Every structural change below names its source. G-numbers = the 30 incident-backed rules from the ship-pipeline intake read; R-numbers = the WEB-4905 analysis recommendations (already applied in diolog 2.4.0, carried forward as the floor); MAST = arXiv:2503.13657; PoLL = arXiv:2404.18796; Petri = Anthropic 2025.

### 1. State machine and substrate
- **One status vocabulary, complete**: `To Do` (triaged) → `Ready for AI` (planned) → `In Progress` (worker started) → `Developer Review` (self-verified) → `Done` (cross-family verified) / `Needs More Work` (failed verification, loops to worker). *Evidence:* tasks-pipeline intake gaps 1–5 (no terminal state, no failure state, Todo overloaded, In Progress never written); user's requested vocabulary; panel (all four backends: explicit kanban state machines with artifact-gated transitions).
- **Transitions advance only on artifacts** — a status move without its artifact (triage comment, committed plan sha, evidence-typed completion comment, verifier verdict comment) is invalid; the artifact's absence is visible to the next stage. *Evidence:* OpenAI panel report ("a stage is complete only when the ledger contains the required artifact"); ship-feature's "missing verdict is a skipped gate"; MAST verification/termination failures.
- **Ledger/artifact memory, never conversational.** Comments carry a small machine-readable block alongside human prose. Thread-as-ledger for crash-safe counters (post intent before attempting; count markers to bound loops). *Evidence:* eve template's CI-fix counter; tasks-pipeline gap 15 (no schema); Gemini/Perplexity panels (stigmergy, artifact memory); G26.
- **Re-entry defined for every terminal-ish state**: `Needs More Work` → worker with the verifier's verdict table as input; parked items get an unpark procedure. *Evidence:* ship-fleet weakness F4; tasks gap 7 (no remediation stage).

### 2. Decision deferral (the clarify integration)
- **The four-gate protocol from clarify runs inside triage and plan**, verbatim in spirit: (1) look it up (repo, thread, prior comments — never re-ask an answered question), (2) divergence test (sketch both readings; same sketch = no question; ClarifyGPT +9.8pp), (3) internal vs external (three-part essential-gap bar from sentinel-review; "when in doubt, assume and proceed"), (4) **second opinion / panel before the human**: technical questions route to other models, not the user.
- **Second-opinion lanes generalised to an ordered set** (single-vendor A1 weakness fixed): `claude --model claude-fable-5 --effort high` (fast, in-family), `codex exec -m gpt-5.6-sol` high/max (out-of-family default), `agy` gemini-flash-3.7 high, `grok` grok-4.6 xhigh (fallback harness: `cursor-agent`). Wire verification per lane (grep model + effort headers; empty output file = lane failure, not a pass). *Evidence:* clarify SKILL.md gate 4 + verified lanes; G6–G11; trawl (codex usage-limited episodes, agy as writer when codex down).
- **Panels only at high-leverage gates** (triage verdict on an ambiguous brief, plan-shape forks, design direction, final verification disagreement) — never per edit. 3 diverse families, blind pairwise, position-swapped, structural verdicts; disagreement = the escalation signal, not noise. *Evidence:* PoLL (panel > single judge, ~7× cheaper); Shi et al. position bias; MAST coordination cost; panel convergence.
- **Assumption records, not questions**: statement, confidence, evidence, alternative it beat ("assuming X rather than Y"), blast radius, falsifier, rollback. Escalate to the human only for: taste, cost, scope, risk tolerance, compliance/S3, auth/billing/retention/irreversible-schema, destructive/outward-facing. *Evidence:* OpenAI panel assumption-resolution order; clarify gate 3; sentinel internal/external bar; Ask-or-Assume (declined-to-ask baseline).
- **Questions that survive all gates go through AskUserQuestion in clarify's shape** (batched, ≤3, recommendation earned + reasoned, consequence-not-mechanism wording) — and in unattended runs are parked as `Needs More Info` with an "Easy reply" block instead of blocking the fleet.

### 3. Model routing
Central `model-lanes.md`, tier-named (never dated ids in self-checks — G6), REVIEWER ≥ WRITER preserved, wire-verified, recorded per gate in the completion comment:

| Lane | Model | Harness | Effort |
|---|---|---|---|
| Triage, plan, design direction, conductor | Opus 5 (`claude-opus-5`) or Fable 5 in-session | Claude Code | high |
| Implementation (preferred) | gemini-flash-3.7 | `agy` | high (high TPS) |
| Implementation (fallback 1) | grok-4.6 | `grok` (fallback `cursor-agent`) | high |
| Implementation (fallback 2) | gpt-5.6-terra | `codex` | medium |
| Same-family validation (vs plan + tests) | same family as implementer, stronger or equal tier | same CLI | high |
| Cross-family verification | gemini / gpt / grok — MUST differ from implementer family | agy / codex / grok | high–max |
| Verification fallback | Opus 5 agents | Claude Code | high |
| Leaf readers / gate runners | session model | in-session Workflow | low |

Availability-with-fallback is a *procedure*: probe the lane (cheap parse-check), on rate-limit/empty-artifact record "availability failure" in the ledger and take the next lane; never silently degrade below the family constraint for verification — an all-in-family verification is recorded as degraded, and buys back one extra adversarial round (fixes A2). *Evidence:* trawl §3 (codex outages, agy substitution, wire-verification doctrine); Petri + 17.6pp self-grading (held loosely) for the family constraint; eve template's "different vendor on purpose" + its inverted-risk warning (strong model belongs on review too).

### 4. Design stage (new, mandatory for user-facing features)
- Own stage between plan and work (parallelisable with plan where surfaces are known from triage). Interactive mocks covering **all surfaces, user flows, states, actions, menus** — the state-matrix (nav/forms/tables/modals/permissions/responsive × default/loading/empty/error/success) is the coverage bar and the later test oracle. *Evidence:* OpenAI panel UI state matrix; ship-pipeline weakness A3/A4 (design had no verification gate, no decision stage); user requirements.
- **Platform set: iPhone, iPad, Mac, Web always; Windows optional.** iOS/iPadOS/macOS (and Windows base) mocks route through `mac-design-studio`; Windows applies a Windows 11 aesthetic on top; web mirrors the mac layout. `mobbin` MCP is consulted during ideation whenever design-craft/ux-craft run. *Evidence:* user requirements; trawl §4 (design rejections happened despite skills being invoked — gates, not invocations, are what matter).
- **`design-review` and `be-my-witness` always run on the mocks; findings are actioned and the mock re-reviewed** (bounded loop: fix → one re-review; witness calibrated per its known over-flagging). *Evidence:* user requirement; trawl (be-my-witness over-flagging commit); design-representation render-verification bar kept.
- Design decisions recorded as assumptions; direction forks judged by a small panel when open. *Evidence:* Design-It-Twice (Pocock/Ousterhout: 3 briefed variants); prototype skill's variant discipline (structurally different, in-context, switcher).

### 5. Test strategy (comprehensive, not vanity)
- Planned at plan time (seams named — no test at an unconfirmed seam), authored fail-to-pass, and graded by the state-matrix: unit (logic, boundaries), e2e UI automation per flow/action/menu (via `acceptance-e2e` in the repo's own harness), visual states per surface. Anti-vanity: red@sha-before → green@sha-after proof (R3), tautology check (expected values from an independent source), affected-test sweep, mutation-style spot checks on changed logic. *Evidence:* R3; tdd skill's three anti-patterns; Meta TestGen-LLM filters; SWE-bench 7.8% false-positive study; median-21%-mutation-score study.
- **Evidence typing everywhere** (R2): static → file:line; visual → measured values or screenshot; behavioural → exercised request/response or named test red→green. No partial status. Caveats propagate. Green gates necessary, never sufficient.

### 6. Verification topology
- **Stage 1 — same-family validation** (writer's family, fresh context): checks work against plan + tests, fills nothing it inherited (re-derives its list). Physical isolation: fresh worktree checkout of the pushed branch, receives only ticket + criteria + branch. *Evidence:* eve template's reviewer isolation; tasks-verify fresh-session rule made enforceable (different agent, not honour-system).
- **Stage 2 — cross-family verification** (gemini/gpt/grok, ≠ implementer family; fallback Opus 5): `pipeline-verify` running `/acceptance-e2e` for behavioural claims with `/proctor` for computer/browser use; verdict comment with per-requirement typed evidence; sets `Done` or `Needs More Work`. *Evidence:* user requirement; R1; Petri; A1 fixed by the ordered lane set.
- Pre-merge gate stays fail-closed and gains: post-rebase e2e re-run, a11y/keyboard box, S3 sign-off box, rollback procedure (`git revert` path), verifier-comment-present box. *Evidence:* ship-pipeline weaknesses B4, A5, D4, F7.

### 7. Intake and ideation ("here's a rough idea for an app")
- `pipeline-intake`: a rough idea → one-or-many briefs in `docs/features-to-triage/*.md` (brief = what/why, audience, acceptance sketch, origin+date, research pointers). Uses `/trawl` for divergent ideation and explicitly proposes **additional features/concepts the target audience would likely want**, each as its own brief marked `proposed-by-ai`. Dossier panels (free lane first) gather market/technical context when the idea is thin. App-shaped ideas get the standard platform set (iPhone/iPad/Mac/Web, Windows optional) seeded as surface expectations for triage. *Evidence:* user requirement; ship-armada Route mode; grilling's facts/decisions split.
- The brief file becomes the task description when a tasks MCP is configured (tracker adapter); triage leaves its comment on the task; plan md committed and referenced by repo-relative path + sha (R6/G-provenance).

### 8. Operational hardening carried forward wholesale
- The 30 G-rules verbatim into references (git identity, agent() null returns, Promise.race empty, worktree-first universal — E5 resolved in favour of worktree-first, ≤4-agent waves reconciled with runner slots into one global budget (F1), codex mechanics, egress opt-out machinery, ledger locks, "done means merged", never git add -A, kill by process group).
- Scripted (not prose) checks where the failure was mechanical: completion-vs-ledger cross-check (ship-armada's biggest gap), path checks, wire greps, evidence-row presence lint. Ship as real files in the plugins, not heredocs (F3).
- Merge-ownership an explicit parameter (E4); vocabularies unified (E1–E3); reference-product commands parameterised via a per-repo setup doc (E6/E7, wayfinder-style config indirection).

## What is deliberately NOT changed
- clarify itself (it is a source, not a target).
- design-craft / ux-craft (user will move them later; the pipeline invokes them as installed).
- The non-technical comment discipline, sentinel lens vocabulary, plan tiers' anti-padding rules, model-and-effort §6/§7, the codex opt-out/egress machinery — all carried forward as-is (WEB-4905 "What NOT to change").
- gap-fix's two-consecutive-dry-audits loop vs work's single re-audit: both kept, with the reconciliation *stated* (work has the critic + front-loaded checklist; gap-fix is the finisher) — E10.

## Eval scope (Phase 3)
Structural-assertion evals on the three decision/evidence skills (triage, plan, verify) — old (diolog 2.4.0/1.10.0 snapshots) vs new on fixture briefs; blind 4-family panel (claude/codex/grok/cursor) on anonymised artifact pairs; process evals asserting the pipeline's own invocations (design gates run, statuses moved, evidence rows typed).

## Checkpoints
Names + icon concepts via AskUserQuestion after evals (improve-skill Phase 4 hard gate) — covering: final plugin names, whether diolog originals get deprecation pointers, Windows-lane default, and the tasks-MCP config shape.
