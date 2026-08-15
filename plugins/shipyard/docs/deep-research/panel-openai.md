---
title: "Evidence-Backed Design Patterns for Autonomous Multi-Agent Software Pipelines"
run_id: dr_1525938e137e9f9d
question: "Evidence-backed design patterns and documented failure modes for autonomous multi-agent AI software-delivery pipelines (2024–2026), to inform a rebuild of a feature-delivery orchestration system that takes a rough product idea through triage → specification → planning → UI design mocks → implementation → testing → verification with minimal human intervention. Subtopics to cover: (1) heterogeneous multi-model orchestration — routing planning/reasoning to frontier models while delegating implementation to faster models, fallback chains across vendor CLIs (Claude Code, OpenAI Codex CLI, Gemini CLI, Grok/Cursor CLI), and measured evidence on same-family self-review blindness vs cross-family verification; (2) LLM-as-judge and panel/jury techniques — when multi-model panels beat single judges, structural assertions vs numeric scores, blind A/B judging, position and verbosity bias mitigations; (3) autonomous assumption-making — techniques for AI resolving ambiguity itself (divergence testing, second opinions, recorded assumptions with confidence) instead of asking the human, and failure modes when it guesses wrong; (4) automated test generation quality — AI-written unit tests, e2e UI automation (Playwright etc.), and visual regression coverage of states/flows/menus: what coverage disciplines actually catch regressions vs vanity suites; (5) task/kanban state machines for agent workflows — statuses like Triaged/Ready-for-AI/In-Review/Needs-More-Work, comment-thread handoff between agents, and evidence on ledger/artifact-based memory vs conversational memory; (6) known failure modes of long-running autonomous pipelines — scope drift, silent stage skipping, verification theater, rubber-stamp reviews, cascade failures from a wrong early assumption. Prefer primary sources: papers (SWE-bench/agent evaluations, LLM-as-judge literature), vendor engineering blogs, postmortems, benchmark data. Exclude: general prompt-engineering tutorials, RAG architectures, non-software agent domains."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: competitive
sources: 62
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-15T01:15:09.239Z
---
## Executive Summary

- **(High Confidence)** Build the rebuilt pipeline around **hard, artifact-backed stage gates**, not a conversational “manager agent.” Every transition should require machine-readable evidence: spec, assumptions ledger, plan, mock-state matrix, diff, test report, reviewer verdict, and release evidence. This directly addresses documented multi-agent failures in specification, inter-agent alignment, verification, and termination. [Why Do Multi-Agent LLM Systems Fail?](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/) ([mlanthology.org](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai))

- **(High Confidence)** Use a **heterogeneous model panel only at high-leverage decision points**—triage, requirements challenge, architecture, code review, and final verification—not for every edit. A diverse Panel of LLM evaluators outperformed a single large judge across six datasets, was less susceptible to intra-model bias, and was reported as more than seven times cheaper in the study setting. [Verga et al., “Replacing Judges with Juries,” 2024](https://arxiv.org/abs/2404.18796) ([arxiv.org](https://arxiv.org/abs/2404.18796?utm_source=openai))

- **(High Confidence)** Do **not** allow a model family to be the only reviewer of its own work. Cross-family review is a useful independence control, not proof of correctness: Anthropic’s Petri experiments found GPT-5 judges systematically rated GPT-5-family targets as less misaligned than other judges did, while same-family Claude judges correlated especially highly. [Anthropic, Petri, 2025](https://alignment.anthropic.com/2025/petri/) ([alignment.anthropic.com](https://alignment.anthropic.com/2025/petri/?_bhlid=22fc72d25bdcd9bb586663c94f4f5884845d6990&utm_source=openai))

- **(High Confidence)** Replace scalar “quality scores” with **structural pass/fail assertions plus evidence**: acceptance criteria met, changed files explained, required paths executed, negative cases covered, visual states checked, and no unresolved high-severity reviewer objections. Numeric LLM scores are vulnerable to position, verbosity, and superficial-fluency bias. [Shi et al., “Judging the Judges,” 2024](https://arxiv.org/abs/2406.07791) ([arxiv.org](https://arxiv.org/abs/2406.07791?utm_source=openai)) [Zhou et al., “Mitigating the Bias of Large Language Model Evaluation,” 2024](https://arxiv.org/abs/2409.16788) ([arxiv.org](https://arxiv.org/abs/2409.16788?utm_source=openai))

- **(High Confidence)** Autonomous assumption-making should be **bounded and reversible**, not a blanket prohibition on clarification. Current coding agents struggle to recognize underspecification; studies find interaction improves outcomes when specifications are incomplete. The correct design is: generate competing interpretations, independently challenge them, choose the lowest-blast-radius reversible assumption, record it with confidence and falsifiers, and escalate only when the decision is irreversible or changes product policy/security/data semantics. [Vijayvargiya et al., “Interactive Agents to Overcome Ambiguity in Software Engineering,” 2025](https://arxiv.org/abs/2502.13069) ([arxiv.org](https://arxiv.org/abs/2502.13069?utm_source=openai))

- **(High Confidence)** Treat AI-written tests as **candidates requiring independent adequacy checks**, not proof. Meta’s TestGen-LLM deployment found that 75% of generated tests built, 57% passed reliably, and 25% increased coverage; those figures justify constrained use, not autonomous acceptance. [Alshahwan et al., “Automated Unit Test Improvement using LLMs at Meta,” 2024](https://arxiv.org/abs/2402.09171) ([arxiv.org](https://arxiv.org/abs/2402.09171?utm_source=openai))

- **(High Confidence)** “All tests green” is insufficient as a final gate. An empirical study of SWE-bench Verified found that 7.8% of patches counted as correct by the benchmark nevertheless failed the developer-written test suite. [“Are ‘Solved Issues’ in SWE-bench Really Solved Correctly?”, 2025](https://arxiv.org/abs/2503.15223) ([arxiv.org](https://arxiv.org/abs/2503.15223?utm_source=openai)) Final verification must therefore include independent regression tests, mutation/negative testing where feasible, UI-flow execution, and a reviewer who did not author the patch or its tests.

- **(Medium Confidence)** The market is converging on capable coding agents and background execution, but not on a vendor-neutral, auditable feature-delivery control plane. Cursor exposes autonomous background agents, but explicitly warns that auto-running terminal commands plus internet access creates prompt-injection and code-exfiltration risk. [Cursor Background Agents documentation](https://docs.cursor.com/background-agent) ([docs.cursor.com](https://docs.cursor.com/background-agent?utm_source=openai)) The underserved opportunity is a **cross-vendor task ledger, assumption provenance system, and evidence-gated verification protocol** above individual CLIs.

## Detailed Findings

### 1. Answer this decisively: Evidence-backed design patterns and documented failure modes for autonomous multi-agent AI software-delivery pipelines (2024–2026), to inform a rebuild of a feature-delivery orchestration system that takes a rough product idea through triage → specification → planning → UI design mocks → implementation → testing → verification with minimal human intervention.

#### Decisive operating model

**(High Confidence)** Rebuild the system as a **deterministic workflow engine supervising probabilistic workers**. Agents may propose, implement, test, and critique; only the state machine may advance work. This is the practical response to the failure categories identified across multi-agent systems: specification/system-design failures, inter-agent misalignment, and task-verification/termination failures. [Why Do Multi-Agent LLM Systems Fail?](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/) ([mlanthology.org](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai))

<INFERENCE from="MAST identifies specification, inter-agent alignment, and verification/termination as distinct failure categories; Codex’s published ExecPlan guidance externalizes long-running work into durable plan artifacts; documented community experience reports context drift and lost rationale after compaction.">The orchestration layer should own task state, evidence requirements, and transition rights; LLMs should never own all three simultaneously.</INFERENCE>

**Recommended stage order and non-skippable gates**

| Pipeline stage | State-machine status | Required artifact | Gate owner | Advancement rule |
|---|---|---|---|---|
| 1. Intake / triage | `Triaged` | Problem statement, target user, expected value, constraints, initial risk class | Triage panel | Must distinguish feature request, defect, discovery, and unsupported request. |
| 2. Specification | `Spec-Draft` → `Assumptions-Challenged` | Acceptance criteria, non-goals, data/security constraints, assumption ledger | Planner + independent challenger | No implementation before every material ambiguity is tagged as resolved, assumed, or escalated. |
| 3. Planning | `Ready-for-AI` → `Planned` | Executable plan, affected surfaces, dependency map, test strategy, rollback plan | Architecture judge | Plan must map each acceptance criterion to implementation and verification evidence. |
| 4. UI design mocks | `Mock-Ready` | State/flow matrix, mocks/screens, responsive variants, loading/error/empty states | Design verifier | Mocks must enumerate interaction states, not only happy-path screens. |
| 5. Implementation | `Implementing` | Atomic commits/diff, implementation log, decision updates | Builder | No direct transition to done; implementation automatically opens test work. |
| 6. Test generation and execution | `Testing` | Unit, integration, E2E, accessibility, visual, negative/mutation results | Test agent independent of builder | Generated tests must pass independently and demonstrate new behavioral coverage. |
| 7. Cross-family review | `In-Review` / `Needs-More-Work` | Structured defect list, severity, evidence, disposition | Reviewer panel | A reviewer cannot accept its own patch or its own tests. |
| 8. Verification / release | `Verified` → `Done` or `Escalated` | Requirements traceability matrix, execution artifacts, final verdict | Verification judge + deterministic checks | “Done” only if all mandatory structural assertions pass. |

**(High Confidence)** The system should reject “silent stage skipping.” A stage is complete only when the ledger contains the required artifact and its hash, the gate verdict, the model/provider used, inputs read, commands run, and the next-state transition. This makes omission detectable instead of inferred from chat prose. [OpenAI Cookbook, Codex Execution Plans](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md) ([github.com](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md?utm_source=openai))

#### 1A. Heterogeneous multi-model orchestration and fallback routing

**(High Confidence)** Use **capability tiers**, not permanent brand-to-role assignments. Model releases and availability change rapidly; benchmark scores are also increasingly unreliable as deployment-selection signals. On July 8, 2026, OpenAI reported that it estimated approximately 30% of SWE-bench Pro tasks were broken after an audit, explicitly warning that flawed evaluations can distort capability measurement. [OpenAI, “Separating signal from noise in coding evaluations,” July 8, 2026](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) ([openai.com](https://openai.com/index/separating-signal-from-noise-coding-evaluations/?utm_source=openai))

**Recommended routing table**

| Work type | Primary lane | Secondary/fallback lane | Why | Mandatory control |
|---|---|---|---|---|
| Triage, product interpretation, architecture, risky refactors | Frontier reasoning model | Different-family frontier model | High ambiguity and high blast radius justify slower, more expensive reasoning. | Two independent interpretations before commitment. |
| Repository mapping, code search, boilerplate, localized implementation | Fast coding model | Alternate vendor CLI in clean worktree | Lower ambiguity; throughput matters. | Builder cannot certify final correctness. |
| UI mock generation and visual critique | Multimodal frontier model | Different-family multimodal reviewer | Requires visual and interaction-state understanding. | Compare against explicit state matrix, not aesthetic score. |
| Unit-test drafting and test repair | Fast coding model | Different-family test critic | Cheap fan-out is valuable, but generated assertions are risky. | Mutation/negative-test or reviewer adequacy gate. |
| Security, data migration, authorization, payments, destructive operations | Frontier model plus deterministic tools | Human escalation if unresolved | Error impact outweighs autonomy benefit. | No autonomous production execution. |
| Final verification | Cross-family panel plus deterministic CI | Human only on high-severity disagreement | Independence reduces self-preference risk. | Blind pairwise review and evidence-only verdicts. |

**(Medium Confidence)** A practical default chain is: **Claude Code / Codex for primary planning or execution; Antigravity/Gemini, Cursor, or Grok Build as alternate execution/review lanes; direct API calls behind a vendor-neutral adapter for durable orchestration.** Claude Code supports noninteractive scripting, JSON output, model selection, MCP configuration, and a `--max-turns` control useful for bounded workers. [Anthropic Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage) ([docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/cli-usage?utm_source=openai)) Codex uses repository-scoped `AGENTS.md` instructions and supports durable planning documents for multi-hour work. [OpenAI Codex AGENTS.md specification](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/prompts/base_instructions/default.md) ([github.com](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/prompts/base_instructions/default.md?utm_source=openai)) [OpenAI Codex ExecPlans guidance](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md) ([github.com](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md?utm_source=openai))

**(Medium Confidence)** Do not assume Gemini CLI is a stable consumer fallback as of August 15, 2026. Google announced that Gemini CLI and Gemini Code Assist IDE extensions would stop serving free, Google AI Pro, and Google AI Ultra consumer traffic on **June 18, 2026**, with Antigravity CLI positioned as the replacement channel. [Google Developers Blog, May 2026](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) ([developers.googleblog.com](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/?utm_source=openai)) The routing table should therefore target **Gemini API/Antigravity capability**, not hard-code legacy Gemini CLI assumptions.

**(Medium Confidence)** Cursor is useful as an asynchronous implementation lane because its Background Agents API can create and manage repository agents and supports up to 256 active agents per API key. [Cursor Background Agents API documentation](https://docs.cursor.com/background-agent/api/overview) ([docs.cursor.com](https://docs.cursor.com/background-agent/api/overview?utm_source=openai)) However, it should not be the sole autonomous executor for sensitive repositories: Cursor documents that background agents auto-run terminal commands, have internet access, and can be manipulated by prompt injection into uploading code to malicious sites. [Cursor Background Agents security documentation](https://docs.cursor.com/background-agent) ([docs.cursor.com](https://docs.cursor.com/background-agent?utm_source=openai))

**(Medium Confidence)** Grok Build is now a viable CLI-shaped alternative rather than merely an API endpoint: the official `xai-org/grok-build` repository describes a terminal coding agent that edits files, executes shell commands, performs web search, manages long-running tasks, supports headless scripting/CI, and uses an Agent Client Protocol integration. [xAI Grok Build repository](https://github.com/xai-org/grok-build) ([github.com](https://github.com/xai-org/grok-build?ref=explainx&utm_source=openai)) Its role should be an alternate-family worker or reviewer until internal canary data demonstrates task-specific reliability.

**Same-family review blindness**

**(High Confidence)** Cross-family review should be mandatory for nontrivial feature delivery because same-family evaluators can show self-preference. Anthropic’s Petri study observed that GPT-5 judges systematically rated GPT-5, GPT-5 mini, and o4-mini targets as less misaligned than other judges did; it also found Claude Opus 4.1 and Claude Sonnet 4 judges had the highest pairwise correlation. [Anthropic, Petri](https://alignment.anthropic.com/2025/petri/) ([alignment.anthropic.com](https://alignment.anthropic.com/2025/petri/?_bhlid=22fc72d25bdcd9bb586663c94f4f5884845d6990&utm_source=openai))

**(Medium Confidence)** This is evidence for **independence controls**, not evidence that every cross-family verdict is superior. Anthropic separately reported high agreement between Claude Sonnet 4.5 and GPT-5 on one political-even-handedness evaluation—92% per-sample agreement—while noting that model agreement can exceed human-rater agreement. [Anthropic, “Measuring political bias in Claude”](https://www.anthropic.com/news/political-even-handedness) ([anthropic.com](https://www.anthropic.com/news/political-even-handedness?utm_source=openai)) The correct protocol is diversity plus calibrated rubrics, not vendor diversity alone.

<INSUFFICIENT_EVIDENCE>There is no robust public controlled study showing that a fixed “frontier planner + cheap implementer” vendor combination universally outperforms a single strong coding agent across real feature delivery. Existing evidence supports specialization, model diversity, and task-specific evaluation, but not a universal vendor ranking.</INSUFFICIENT_EVIDENCE>

#### 1B. LLM-as-judge, panel, and jury protocols

**(High Confidence)** Use **structural assertions first; LLM judgment second.** Deterministic checks should verify compilation, linting, test execution, requirements traceability, expected files, schema validity, accessibility invariants, and deployment-safe commands. LLM judges should assess residual semantic questions: whether the change meets intent, whether edge cases are omitted, whether a mock covers state transitions, or whether an assumption is unjustified. Anthropic recommends decomposing evaluation into clear structured rubrics and isolating dimensions rather than asking one LLM to judge everything at once. [Anthropic, “Demystifying evals for AI agents”](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) ([anthropic.com](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents?utm_source=openai))

**Recommended jury protocol**

1. **Blind inputs:** Remove provider/model identity, author role, and ordering signals.
2. **Pairwise comparison:** Compare candidate A versus B, then repeat with order reversed.
3. **Criterion-level verdicts:** `PASS`, `FAIL`, `UNKNOWN`, or `ESCALATE`; each must cite evidence from artifacts, code, tests, or screenshots.
4. **No holistic 1–10 score as release authority:** Numeric scores may be logged for analytics but cannot advance workflow state.
5. **Diverse jury:** One same-family critic for domain familiarity, one cross-family critic for independence, and one deterministic evidence checker.
6. **Disagreement policy:** If judges split on a high-severity criterion, automatically produce an adversarial test or counterexample attempt; escalate only if it remains unresolved.
7. **Judge calibration:** Sample completed work for expert review and measure disagreement by criterion, model, task type, and order.

**(High Confidence)** Blind pairwise judging and order reversal are necessary because position bias is real. A 2024 study evaluated 12 LLM judges across MT-Bench and DevBench, covering approximately 100,000 evaluation instances, and found non-random position bias varying by model and task. [Shi et al., “Judging the Judges,” 2024](https://arxiv.org/abs/2406.07791) ([arxiv.org](https://arxiv.org/abs/2406.07791?utm_source=openai))

**(High Confidence)** Length normalization or explicit “ignore verbosity unless required” instructions are also necessary because LLM judges can favor superficial fluency and verbosity over instruction-following quality. [Zhou et al., “Mitigating the Bias of Large Language Model Evaluation,” 2024](https://arxiv.org/abs/2409.16788) ([arxiv.org](https://arxiv.org/abs/2409.16788?utm_source=openai))

**(High Confidence)** Use panels only where a single judgment is consequential or semantically ambiguous. The Panel of LLM evaluators study found that panels made of diverse smaller models outperformed a single large judge across three judge settings and six datasets, reduced intra-model bias, and were reported as more than seven times cheaper in that research configuration. [Verga et al., 2024](https://arxiv.org/abs/2404.18796) ([arxiv.org](https://arxiv.org/abs/2404.18796?utm_source=openai))

#### 1C. Autonomous assumption-making

**(High Confidence)** The pipeline should not ask humans routine implementation questions. It should instead perform **assumption resolution** in the following order:

1. Retrieve repository conventions, prior decisions, existing behavior, tests, analytics, and design tokens.
2. Generate at least two materially distinct interpretations.
3. Have an independent challenger enumerate user-visible, security, migration, and backward-compatibility consequences.
4. Choose the option that is most reversible and least destructive.
5. Write an assumption record: statement, confidence, evidence, alternatives rejected, blast radius, testable falsifier, and rollback path.
6. Continue autonomously when the assumption is low-risk and reversible.
7. Escalate only when the choice changes compliance, billing, data retention, irreversible schema/state, authentication/authorization, contractual behavior, or more than one plausible user-facing product policy.

**(High Confidence)** Ambiguity detection itself is a weak point in current agents. A software-engineering study found models struggle to distinguish well-specified from underspecified instructions, while interacting for underspecified inputs improved performance because agents obtained missing information. [Vijayvargiya et al., 2025](https://arxiv.org/abs/2502.13069) ([arxiv.org](https://arxiv.org/abs/2502.13069?utm_source=openai))

**(Medium Confidence)** An uncertainty-monitoring agent should be separate from the implementer. A 2026 preprint on underspecified SWE-bench tasks reported that an uncertainty-aware multi-agent setup using OpenHands plus Claude Sonnet 4.5 achieved a 69.40% resolve rate versus 61.20% for a standard single-agent setup; the result requires independent reproduction before use as a production performance target. [“Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents,” 2026](https://openreview.net/pdf?id=a25dmoIflA) ([openreview.net](https://openreview.net/pdf?id=a25dmoIflA&utm_source=openai))

**(High Confidence)** The important design modification is that the “clarification” target need not always be a human. For low-risk questions, the system can query the codebase, tests, product telemetry, API contracts, mock repository, or a second model family. For high-risk questions, it must ask a human or halt.

<INFERENCE from="Coding agents struggle to detect underspecification; uncertainty-aware separation improves performance in a controlled underspecified benchmark; ungrounded assumptions create safety and wasted-compute risks.">The operational substitute for routine human questioning is not unilateral guessing. It is an auditable assumption-and-falsification loop with a risk threshold for escalation.</INFERENCE>

#### 1D. Automated test generation, E2E, and visual regression

**(High Confidence)** Require a **test portfolio**, not a unit-test quota:

| Test layer | Required purpose | Anti-vanity metric |
|---|---|---|
| Unit tests | Local logic, validation, boundary values, pure transformations | Mutation score or targeted mutant kills for changed logic |
| Contract/integration tests | Service boundaries, DB/API schema, error propagation | Producer/consumer and failure-path checks |
| E2E workflow tests | Critical user jobs across UI, auth, API, persistence | State-transition coverage: happy, error, empty, loading, retry, permission-denied |
| Accessibility tests | Semantics and keyboard operation | Role/name/state assertions; keyboard paths |
| Visual regression | Layout, hierarchy, responsive breakage, menus, overlays | Curated screenshots for state matrix—not screenshots of every page |
| Negative/regression tests | Prevent recurrence of the observed defect | Fails against the pre-fix behavior or intentional mutant |

**(High Confidence)** AI-generated tests require compile, stability, novelty, and behavioral-adequacy filters. Meta’s TestGen-LLM was deployed to improve existing human-authored tests and reported that 75% of generated test cases built correctly, 57% passed reliably, and 25% increased coverage. [Meta TestGen-LLM, 2024](https://arxiv.org/abs/2402.09171) ([arxiv.org](https://arxiv.org/abs/2402.09171?utm_source=openai)) The fact that only a subset survived these filters is the important operational lesson.

**(High Confidence)** Line or branch coverage alone is a vanity metric. A study of automatically generated patch-assessment tests reported median line coverage of 77% but median mutation score of 21%, illustrating that executing code is not equivalent to detecting faults. [Test-based patch clustering for automatically-generated patch assessment](https://pmc.ncbi.nlm.nih.gov/articles/PMC11269383/) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11269383/?utm_source=openai))

**(High Confidence)** Visual regression should be limited to **critical interaction states**, stabilized in a fixed browser/OS/container environment, and paired with semantic assertions. Playwright supports screenshot baseline comparison through `toHaveScreenshot()`, but warns that rendering differs across OS, browser version, hardware, power state, headless mode, and settings. [Playwright Visual Comparisons documentation](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/next/test-snapshots?utm_source=openai))

**Recommended UI state matrix**

| UI surface | Minimum visual states | Minimum functional assertions |
|---|---|---|
| Navigation | default, active, collapsed/mobile, overflow menu | keyboard navigation, correct route, focus visibility |
| Forms | empty, valid, invalid, server error, loading, success | validation messages, disabled/submission state, retry |
| Tables/lists | populated, empty, loading, pagination/filter states | sorting/filter correctness, selected-item persistence |
| Modals/menus | closed, open, long-content, destructive confirmation | focus trap, escape, outside-click policy, action result |
| Permissions | authorized, unauthorized, expired session | blocked server action, explanatory UI, no data leakage |
| Responsive surfaces | desktop, tablet, mobile breakpoints | no clipped controls, equivalent critical action path |

**(High Confidence)** Do not permit the builder to rewrite the tests that certify its own feature without independent review. The key benchmark warning is empirical: 7.8% of patches that SWE-bench considered correct failed the developer-written test suite. [“Are ‘Solved Issues’ in SWE-bench Really Solved Correctly?”, 2025](https://arxiv.org/abs/2503.15223) ([arxiv.org](https://arxiv.org/abs/2503.15223?utm_source=openai))

#### 1E. Task/kanban state machines, comment handoffs, and durable memory

**(High Confidence)** Use a task-MCP ledger as the system of record. It should store state, artifacts, explicit decisions, reviewer comments, evidence links, and transition events. Conversation context should be treated as disposable working memory, never as authoritative project memory.

**Recommended task object**

```json
{
  "task_id": "FEAT-184",
  "state": "In-Review",
  "parent_feature": "FEATURE-42",
  "goal": "User-visible objective",
  "acceptance_criteria": [],
  "non_goals": [],
  "assumptions": [
    {
      "id": "A-03",
      "statement": "Existing API error contract remains stable",
      "confidence": "medium",
      "evidence": [],
      "falsifier": "Contract test fails against current API",
      "blast_radius": "medium",
      "escalation_required": false
    }
  ],
  "artifacts": {
    "spec": "sha256:...",
    "plan": "sha256:...",
    "mock_matrix": "sha256:...",
    "diff": "git:...",
    "test_report": "sha256:...",
    "review_verdict": "sha256:..."
  },
  "review_threads": [],
  "allowed_transitions": ["Needs-More-Work", "Verified"],
  "model_runs": [],
  "evidence_requirements": []
}
```

**(High Confidence)** Durable repository artifacts are already emerging as the vendor-compatible control surface. Codex’s `AGENTS.md` mechanism scopes repository instructions by directory tree, while its published execution-plan guidance explicitly frames plans as self-contained durable documents for work that can take more than seven hours. [OpenAI Codex AGENTS.md specification](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/prompts/base_instructions/default.md) ([github.com](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/prompts/base_instructions/default.md?utm_source=openai)) [OpenAI Codex ExecPlans](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md) ([github.com](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md?utm_source=openai))

**(Medium Confidence)** Organic practitioner evidence indicates that conversational handoffs decay or become over-directive. One Claude Code user described the failure as: “Claude doesn't forget the code. It forgets the reasoning behind decisions,” citing a later reintroduction of a previously rejected billing approach after compaction. [r/ClaudeAI practitioner report, May 2026](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/) ([reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/?utm_source=openai)) This is anecdotal rather than controlled evidence, but it aligns with the design need for architecture decision records and assumption provenance.

**(Medium Confidence)** Comment threads should be structured handoffs, not free-form narration. Require each comment to identify: claim, evidence, severity, requested action, owner, and disposition. This makes disagreement queryable and prevents a later agent from treating unresolved commentary as settled fact.

#### 1F. Known failure modes and mandatory countermeasures

| Failure mode | Evidence | Pipeline symptom | Mandatory countermeasure |
|---|---|---|---|
| Scope drift | Multi-agent failure research identifies specification ambiguities and misalignment. [MAST, 2025](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/) ([mlanthology.org](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai)) | Feature expands beyond acceptance criteria. | Immutable non-goals; scope-diff judge; task split required for new requirements. |
| Wrong early assumption cascades | Coding agents struggle with underspecification. [Interactive Agents to Overcome Ambiguity, 2025](https://arxiv.org/abs/2502.13069) ([arxiv.org](https://arxiv.org/abs/2502.13069?utm_source=openai)) | Correct implementation of incorrect intent. | Assumption ledger, competing interpretations, reversible defaults, blast-radius escalation. |
| Verification theater | Patches can pass benchmark tests yet fail developer tests. [SWE-bench correctness study, 2025](https://arxiv.org/abs/2503.15223) ([arxiv.org](https://arxiv.org/abs/2503.15223?utm_source=openai)) | “Green CI” masks a product regression. | Independent test author/reviewer; negative tests; mutation checks; E2E critical paths. |
| Rubber-stamp self-review | Same-family preference observed in Petri. [Anthropic Petri, 2025](https://alignment.anthropic.com/2025/petri/) ([alignment.anthropic.com](https://alignment.anthropic.com/2025/petri/?_bhlid=22fc72d25bdcd9bb586663c94f4f5884845d6990&utm_source=openai)) | Builder claims its patch is correct. | Cross-family reviewer; blind artifacts; reviewer cannot edit certifying tests. |
| Stage skipping | Multi-agent verification/termination failures. [MAST, 2025](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/) ([mlanthology.org](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai)) | “Done” without mock, test, or review evidence. | State transition service validates artifact presence and gate signatures. |
| Context decay | Practitioner reports of compaction losing rationale. [r/ClaudeAI, May 2026](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/) ([reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/?utm_source=openai)) | Agent revives rejected design or duplicates work. | Ledger + ADRs + short bootloader handoff, not full chat replay. |
| Tool/prompt-injection exposure | Cursor warns autonomous agents can be induced to exfiltrate code. [Cursor Background Agents](https://docs.cursor.com/background-agent) ([docs.cursor.com](https://docs.cursor.com/background-agent?utm_source=openai)) | Agent follows hostile repo/web content. | Deny-by-default egress, secret isolation, sandboxed worktrees, approval for network/write escalation. |
| Benchmark overfitting / false confidence | OpenAI estimated approximately 30% of SWE-bench Pro tasks were broken. [OpenAI, July 8, 2026](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) ([openai.com](https://openai.com/index/separating-signal-from-noise-coding-evaluations/?utm_source=openai)) | Routing chosen from misleading leaderboard. | Internal shadow benchmark drawn from historical tasks and held-out production-like work. |

#### Competitor comparison: current delivery-agent offers

| Offer | Pricing / commercial model | Channel | Official positioning | Organic sentiment / observed gap |
|---|---|---|---|---|
| Claude Code | Claude subscription or API/enterprise cloud deployment; Anthropic’s May 27, 2026 price list shows Claude API standard pricing beginning at $5/M input and $25/M output for listed Claude 4.6/4.7 tiers. [Anthropic List Prices, May 27, 2026](https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf) ([www-cdn.anthropic.com](https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf?utm_source=openai)) | Terminal CLI, SDK, MCP, cloud platforms | Scriptable CLI with model selection, permissions, and MCP. [Anthropic documentation](https://docs.anthropic.com/en/docs/claude-code/cli-usage) ([docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/cli-usage?utm_source=openai)) | A user reports context compaction can preserve code while losing why design decisions were made. [r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/) ([reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/?utm_source=openai)) **Gap:** durable decision provenance is not a first-class cross-agent release control. |
| OpenAI Codex | ChatGPT plan credits and token-based rate card; team Codex-only seats introduced as pay-as-you-go on April 2, 2026, with new Business seats no longer available from June 24, 2026. [OpenAI, April/June 2026 update](https://openai.com/index/codex-flexible-pricing-for-teams/) ([openai.com](https://openai.com/index/codex-flexible-pricing-for-teams/?utm_source=openai)) | CLI, cloud, IDE, API | Durable `AGENTS.md` instructions and ExecPlans for long-running work. [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md) ([github.com](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md?utm_source=openai)) | One practitioner reported a refactor that passed tests but changed error propagation through several layers. [r/ChatGPTCoding, March 2026](https://www.reddit.com/r/ChatGPTCoding/comments/1s1flwj/removed/) ([reddit.com](https://www.reddit.com/r/ChatGPTCoding/comments/1s1flwj/removed/?utm_source=openai)) **Gap:** no independent mandatory verifier between implementation and release. |
| Google Gemini CLI / Antigravity | Gemini API is usage-priced; for example, Gemini 3.5 Flash standard paid pricing is listed at $1.50/M input and $9/M output. [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) ([ai.google.dev](https://ai.google.dev/gemini-api/docs/pricing?authuser=2&utm_source=openai)) | Legacy Gemini CLI transitioning to Antigravity CLI/API | Google announced the June 18, 2026 transition away from consumer Gemini CLI service toward Antigravity CLI. [Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) ([developers.googleblog.com](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/?utm_source=openai)) | Community backlash focused on transition disruption and uncertainty. [r/GoogleGeminiAI, June 2026](https://www.reddit.com/r/GoogleGeminiAI/comments/1u9fy84/google_took_6000_open_source_prs_for_gemini_cli/) ([reddit.com](https://www.reddit.com/r/GoogleGeminiAI/comments/1u9fy84/google_took_6000_open_source_prs_for_gemini_cli/?utm_source=openai)) **Gap:** orchestration should integrate provider capability through adapters, not provider-specific workflow semantics. |
| Cursor Background Agents | Subscription includes usage allowances; background agents are charged at selected-model API pricing, with user-set spend limits. [Cursor pricing](https://docs.cursor.com/account/pricing) ([docs.cursor.com](https://docs.cursor.com/account/pricing?utm_source=openai)) | IDE, web, mobile, API, GitHub-connected background VM | Autonomous asynchronous coding agents, PR workflow, agent follow-ups. [Cursor API docs](https://docs.cursor.com/background-agent/api/overview) ([docs.cursor.com](https://docs.cursor.com/background-agent/api/overview?utm_source=openai)) | Official documentation itself highlights prompt-injection and exfiltration risk from auto-running internet-connected terminal agents. [Cursor security docs](https://docs.cursor.com/background-agent) ([docs.cursor.com](https://docs.cursor.com/background-agent?utm_source=openai)) **Gap:** autonomy is ahead of auditable, independent release verification. |
| xAI Grok Build | SuperGrok listed at $30/month; API and enterprise plans are separately offered. [xAI pricing](https://x.ai/pricing) ([x.ai](https://x.ai/pricing?utm_source=openai)) | Terminal TUI/CLI, headless CI, editor protocol | Long-running terminal coding agent with shell, files, and web capabilities. [xAI Grok Build repository](https://github.com/xai-org/grok-build) ([github.com](https://github.com/xai-org/grok-build?ref=explainx&utm_source=openai)) | <MISSING_DATA>Direct, high-signal organic sentiment specifically about Grok Build’s reliability in enterprise feature-delivery pipelines was sought but was not sufficiently corroborated in the reviewed source set.</MISSING_DATA> |

**Underserved gaps**

1. **(High Confidence)** No reviewed vendor offers a vendor-neutral **evidence-gated task state machine** that persists specification, assumptions, reviews, test evidence, and transition rights across Claude Code, Codex, Antigravity/Gemini, Cursor, and Grok Build. <INFERENCE from="Vendor documentation emphasizes individual agent execution, repository instructions, background task management, and vendor-local collaboration; none documents a cross-vendor feature-delivery ledger with mandatory cross-family verification.">This is the strongest orchestration-layer opportunity.</INFERENCE>

2. **(High Confidence)** No reviewed vendor documents a first-class **autonomous ambiguity-resolution protocol** that records competing interpretations, confidence, falsifiers, and escalation thresholds before implementation. <INFERENCE from="Current coding-agent ambiguity research identifies underspecification as a major limitation; vendor products expose agents and instruction files but not a formal assumption-governance mechanism.">An assumption ledger with policy-aware escalation is a differentiated capability.</INFERENCE>

3. **(Medium Confidence)** No reviewed vendor presents an end-to-end **UI state/flow coverage discipline** tying product acceptance criteria to mocks, Playwright flows, accessibility assertions, and visual baselines. <INFERENCE from="Vendor materials expose code agents and visual/screenshot capabilities; Playwright provides visual comparison primitives; no reviewed offer documents requirements-to-state-matrix-to-verification traceability.">This is a practical gap for feature-delivery orchestration rather than another coding-agent wrapper.</INFERENCE>

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The current state is **capable but not autonomously trustworthy feature delivery**. Agents can perform substantial repository work, execute tools, generate tests, and run asynchronously, but the evidence base shows that verification, underspecification, benchmark validity, and cross-agent handoffs remain limiting factors.

- SWE-bench began as 2,294 real GitHub issues from 12 Python repositories, and its original ICLR 2024 evaluation found contemporary systems could resolve only the simplest issues. [Jimenez et al., SWE-bench, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html) ([proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html?utm_source=openai))
- More recent benchmark results cannot be treated as deployment readiness: OpenAI’s July 8, 2026 audit estimated roughly 30% of SWE-bench Pro tasks were broken. [OpenAI, July 8, 2026](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) ([openai.com](https://openai.com/index/separating-signal-from-noise-coding-evaluations/?utm_source=openai))
- LLM evaluation can be useful when grounded in explicit rubrics and calibrated against humans, but Anthropic warns that even sophisticated teams can encounter grading bugs, harness constraints, task ambiguity, and agents exploiting grader loopholes. [Anthropic engineering guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) ([anthropic.com](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents?utm_source=openai))
- Current commercial tools provide pieces of the system: command-line agents, background execution, repository instruction files, MCP, PR-oriented workflows, and model routing. They do not remove the need for an independent orchestration, evidence, and release-control layer. [Anthropic LLM gateway documentation](https://docs.anthropic.com/en/docs/claude-code/llm-gateway) ([docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/llm-gateway?utm_source=openai)) [Cursor Background Agents API documentation](https://docs.cursor.com/background-agent/api/overview) ([docs.cursor.com](https://docs.cursor.com/background-agent/api/overview?utm_source=openai))

**Strongest evidence hierarchy for the rebuild**

| Decision area | Strongest available evidence | Confidence |
|---|---|---|
| Use cross-family judges | Controlled panel study plus observed same-family judge bias | High |
| Use structural gates over scalar scores | Bias studies plus vendor evaluation guidance | High |
| Separate ambiguity monitor from implementer | Software-engineering ambiguity studies | High |
| Filter AI-generated tests with execution and adequacy checks | Meta industrial deployment results | High |
| Require independent verification beyond tests | SWE-bench patch-correctness study | High |
| Use durable artifacts over chat memory | Vendor long-plan architecture plus consistent practitioner reports | Medium |
| Route named vendor/model combinations by task | Internal canary evidence is required; public evidence is insufficient | Medium |

### 3. What are the contrasting viewpoints or competing evidence?

**(High Confidence)** There are three important tensions.

1. **Panel diversity versus coordination cost.** Diverse juries can outperform single judges and reduce intra-model bias, but multi-agent systems introduce coordination, communication, and termination failure modes. [PoLL, 2024](https://arxiv.org/abs/2404.18796) ([arxiv.org](https://arxiv.org/abs/2404.18796?utm_source=openai)) [MAST, 2025](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/) ([mlanthology.org](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai)) **Resolution:** use panels for gates and disagreements, not routine file edits.

2. **Autonomy versus clarification.** The requested design favors minimal human intervention, while ambiguity research finds asking targeted questions can materially improve performance. [Interactive Agents to Overcome Ambiguity, 2025](https://arxiv.org/abs/2502.13069) ([arxiv.org](https://arxiv.org/abs/2502.13069?utm_source=openai)) **Resolution:** minimize human questions through evidence retrieval and bounded assumptions, but retain escalation for irreversible or policy-defining decisions.

3. **Fast models versus frontier models.** Lower-cost models are attractive for implementation fan-out, but public benchmark results do not isolate whether a specific fast-model/frontier-planner mix is universally optimal. Benchmark quality itself is contested. [OpenAI benchmark audit, 2026](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) ([openai.com](https://openai.com/index/separating-signal-from-noise-coding-evaluations/?utm_source=openai)) **Resolution:** use a provider-neutral model registry and route based on internal canaries: task class, repo language, latency, token cost, retry rate, reviewer rejection rate, and escaped-defect rate.

<CONFLICTING_EVIDENCE>Panel studies support diverse ensembles for judging, while multi-agent failure research shows that additional agents can add specification, alignment, and termination failures. The disagreement is not whether multiple agents can help; it is whether they are applied to independently checkable, bounded roles or to open-ended conversational coordination.</CONFLICTING_EVIDENCE>

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** The trajectory from 2024 through August 15, 2026 is from coding assistance toward autonomous execution, but the bottleneck has shifted from code generation to **verification and operational control**.

- **2024:** SWE-bench established real-issue evaluation; LLM-as-judge research documented judge bias; Meta published industrial evidence that LLMs can improve tests only when filtered through build, reliability, and coverage checks. [SWE-bench, 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html) ([proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html?utm_source=openai)) [Judging the Judges, 2024](https://arxiv.org/abs/2406.07791) ([arxiv.org](https://arxiv.org/abs/2406.07791?utm_source=openai)) [Meta TestGen-LLM, 2024](https://arxiv.org/abs/2402.09171) ([arxiv.org](https://arxiv.org/abs/2402.09171?utm_source=openai))
- **2025:** Research increasingly documented multi-agent coordination failure, ambiguity limits, and same-family evaluation concerns. [MAST, 2025](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/) ([mlanthology.org](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai)) [Interactive Agents to Overcome Ambiguity, 2025](https://arxiv.org/abs/2502.13069) ([arxiv.org](https://arxiv.org/abs/2502.13069?utm_source=openai)) [Petri, 2025](https://alignment.anthropic.com/2025/petri/) ([alignment.anthropic.com](https://alignment.anthropic.com/2025/petri/?_bhlid=22fc72d25bdcd9bb586663c94f4f5884845d6990&utm_source=openai))
- **2026:** Vendor products added more persistent, asynchronous, and agentic execution surfaces—Cursor background-agent APIs, Codex durable planning patterns, and Grok Build CLI capabilities—while Google shifted consumer CLI strategy toward Antigravity. [Cursor API documentation](https://docs.cursor.com/background-agent/api/overview) ([docs.cursor.com](https://docs.cursor.com/background-agent/api/overview?utm_source=openai)) [OpenAI ExecPlans](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md) ([github.com](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md?utm_source=openai)) [xAI Grok Build](https://github.com/xai-org/grok-build) ([github.com](https://github.com/xai-org/grok-build?ref=explainx&utm_source=openai)) [Google transition announcement](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) ([developers.googleblog.com](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/?utm_source=openai))
- **July 2026:** Benchmark auditing became a first-order concern after OpenAI estimated that approximately 30% of SWE-bench Pro tasks were broken. [OpenAI, July 8, 2026](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) ([openai.com](https://openai.com/index/separating-signal-from-noise-coding-evaluations/?utm_source=openai))

<INFERENCE from="Agent execution channels are proliferating; benchmark validity is increasingly disputed; research repeatedly identifies verification, ambiguity, and coordination as dominant failure sources.">The durable competitive advantage will not be another model wrapper. It will be a control plane that makes autonomous delivery inspectable, reproducible, vendor-portable, and difficult to falsely certify.</INFERENCE>

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Diverse LLM panels outperformed a single large judge across six datasets, reduced intra-model bias, and were reported as over seven times cheaper in the study configuration. | Verga et al., *Replacing Judges with Juries* | 2024-04-29 | Research preprint; direct experimental evaluation; meets criteria as original methodology and results. | https://arxiv.org/abs/2404.18796 |
| LLM judges exhibit non-random position bias across models and tasks. | Shi et al., *Judging the Judges* | 2024-06-12 | Research preprint; approximately 100,000 evaluation instances; primary empirical study. | https://arxiv.org/abs/2406.07791 |
| LLM judges can favor verbosity/fluency over instruction-following quality. | Zhou et al., *Mitigating the Bias of Large Language Model Evaluation* | 2024-09-25 | Research preprint; primary bias analysis and mitigation experiments. | https://arxiv.org/abs/2409.16788 |
| GPT-5 judges showed potential preferential treatment toward GPT-5-family target models. | Anthropic, *Petri* | 2025 | Vendor research report; primary experimental data on multiple target/judge combinations. | https://alignment.anthropic.com/2025/petri/ |
| Multi-agent failures cluster around specification, coordination, and verification/termination. | Pan et al., *Why Do Multi-Agent LLM Systems Fail?* | 2025 | Conference/workshop research; taxonomy evaluated across five multi-agent systems and 150+ tasks. | https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/ |
| Coding agents struggle to detect underspecification; interaction provides valuable missing information. | Vijayvargiya et al., *Interactive Agents to Overcome Ambiguity in Software Engineering* | 2025-02-18 | Primary software-engineering agent study. | https://arxiv.org/abs/2502.13069 |
| Uncertainty-aware multi-agent clarification improved an underspecified SWE-bench setup from 61.20% to 69.40%. | Edwards and Schuster, *Ask or Assume?* | 2026-03-27 | Preprint/open review; relevant but awaiting stronger independent replication. | https://openreview.net/pdf?id=a25dmoIflA |
| Meta TestGen-LLM: 75% built, 57% passed reliably, 25% increased coverage. | Alshahwan et al., *Automated Unit Test Improvement using LLMs at Meta* | 2024-02-14 | Industrial deployment study; primary operational data. | https://arxiv.org/abs/2402.09171 |
| 7.8% of patches counted correct by SWE-bench failed developer-written tests. | *Are “Solved Issues” in SWE-bench Really Solved Correctly?* | 2025-03-19 | Empirical patch-correctness study; primary analysis of benchmark validation weakness. | https://arxiv.org/abs/2503.15223 |
| Approximately 30% of SWE-bench Pro tasks were estimated broken in OpenAI’s audit. | OpenAI, *Separating signal from noise in coding evaluations* | 2026-07-08 | Official technical audit; primary data-quality methodology, not a marketing-performance claim. | https://openai.com/index/separating-signal-from-noise-coding-evaluations/ |
| Claude Code supports scripted noninteractive use, JSON output, model selection, and turn limits. | Anthropic Claude Code documentation | Current as accessed 2026-08-15 | Official product documentation; authoritative for product capability. | https://docs.anthropic.com/en/docs/claude-code/cli-usage |
| Codex uses scoped `AGENTS.md` repository instructions. | OpenAI Codex repository | Current as accessed 2026-08-15 | First-party source code and instruction specification. | https://github.com/openai/codex/blob/main/codex-rs/protocol/src/prompts/base_instructions/default.md |
| Codex ExecPlans are intended as durable, self-contained planning artifacts for multi-hour work. | OpenAI Cookbook | Current as accessed 2026-08-15 | First-party engineering guidance; direct implementation pattern. | https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md |
| Cursor background agents can run autonomously but create prompt-injection/code-exfiltration risk. | Cursor documentation | Current as accessed 2026-08-15 | Official security documentation; authoritative for documented product risk. | https://docs.cursor.com/background-agent |
| Playwright visual snapshots require stable rendering environments because browser screenshots vary by environment. | Playwright documentation | Current as accessed 2026-08-15 | Official framework documentation; authoritative implementation constraint. | https://playwright.dev/docs/test-snapshots |
| Google announced consumer Gemini CLI service transition to Antigravity CLI on June 18, 2026. | Google Developers Blog | 2026 | Official vendor announcement; authoritative for channel availability transition. | https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ |

## Knowledge Gaps

### Benchmark-to-production transfer

<MISSING_DATA>Controlled, independently replicated evidence comparing complete feature-delivery pipelines—triage through UI design, implementation, testing, and release—across Claude Code, Codex, Antigravity/Gemini, Cursor, and Grok Build is unavailable. Needed: a public or internal benchmark with ambiguous product requests, stateful repositories, UI artifacts, real acceptance tests, and post-merge defect tracking.</MISSING_DATA>

### Optimal model-routing economics

<INSUFFICIENT_EVIDENCE>No credible public study establishes a universal vendor/model routing table for “frontier planning, cheap implementation, cross-family review.” Needed: internal canary experiments that measure cost per accepted feature, reviewer-rejection rate, time-to-verified completion, and escaped-defect rate by task type.</INSUFFICIENT_EVIDENCE>

### Same-family self-review magnitude in coding

<INSUFFICIENT_EVIDENCE>Same-family evaluation bias is evidenced in general evaluation and Anthropic’s Petri setting, but its precise magnitude for code review, test adequacy, and UI verification is not publicly established. Needed: blind coding-review trials crossing model family, author model, and task complexity.</INSUFFICIENT_EVIDENCE>

### Durable-memory architecture

<INSUFFICIENT_EVIDENCE>There is strong practical rationale for ledger/artifact memory over conversational memory, but limited controlled software-engineering evidence comparing task ledgers, repository documents, issue trackers, and raw conversation summaries over multi-day feature delivery. Needed: longitudinal experiments tracking stale-decision recurrence, duplicate work, and handoff accuracy.</INSUFFICIENT_EVIDENCE>

### Vendor-specific organic sentiment

<MISSING_DATA>High-signal, representative organic feedback on Grok Build and enterprise Antigravity CLI reliability was sought but was insufficiently corroborated. Needed: sustained issue-tracker, developer-forum, and enterprise-user evidence segmented by use case, repository size, and deployment model.</MISSING_DATA>

## Recommended Next Steps

1. **Run a 40–60 task internal routing bake-off.**  
   **Rationale:** Public benchmarks are now materially contested. Use historical bugs, small features, UI changes, refactors, and ambiguous tickets from your own repositories. Measure verified completion, retry count, cost, elapsed time, reviewer rejection, and post-merge defects by model role.

2. **Build the task-MCP ledger before expanding agent count.**  
   **Rationale:** A state machine with immutable artifacts, assumption records, review threads, and evidence-gated transitions will prevent silent skips, context loss, and unverifiable completion even when models change.

3. **Implement a cross-family verification pilot for high-risk changes.**  
   **Rationale:** Start with authentication, billing, migrations, permissions, and user-visible workflow changes. Enforce blind review, order-swapped pairwise judging, deterministic gates, and adversarial test generation on disagreements.

4. **Create a UI verification corpus and state matrix template.**  
   **Rationale:** Require every feature to enumerate desktop/mobile, loading, empty, error, permission, menu/modal, and keyboard-accessible states. Connect each state to Playwright functional and visual checks.

5. **Define an assumption-risk policy and escalation matrix.**  
   **Rationale:** Allow autonomous assumptions only when reversible and low blast radius. Require escalation for data loss, money movement, compliance, authorization, retention, externally visible policy, and irreversible migration decisions.

## Sources

- [Why Do Multiagent Systems Fail? | ML Anthology](https://mlanthology.org/iclrw/2025/pan2025iclrw-multiagent/?utm_source=openai)
- [Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models](https://arxiv.org/abs/2404.18796?utm_source=openai)
- [Petri: An open-source auditing tool to accelerate AI safety research](https://alignment.anthropic.com/2025/petri/?_bhlid=22fc72d25bdcd9bb586663c94f4f5884845d6990&utm_source=openai)
- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791?utm_source=openai)
- [Mitigating the Bias of Large Language Model Evaluation](https://arxiv.org/abs/2409.16788?utm_source=openai)
- [Interactive Agents to Overcome Ambiguity in Software Engineering](https://arxiv.org/abs/2502.13069?utm_source=openai)
- [Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/abs/2402.09171?utm_source=openai)
- [Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study](https://arxiv.org/abs/2503.15223?utm_source=openai)
- [Cursor – Background Agents](https://docs.cursor.com/background-agent?utm_source=openai)
- [openai-cookbook/articles/codex_exec_plans.md at main · openai/openai-cookbook · GitHub](https://github.com/openai/openai-cookbook/blob/main/articles/codex_exec_plans.md?utm_source=openai)
- [Separating signal from noise in coding evaluations | OpenAI](https://openai.com/index/separating-signal-from-noise-coding-evaluations/?utm_source=openai)
- [CLI reference - Anthropic](https://docs.anthropic.com/en/docs/claude-code/cli-usage?utm_source=openai)
- [codex/codex-rs/protocol/src/prompts/base_instructions/default.md at main · openai/codex · GitHub](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/prompts/base_instructions/default.md?utm_source=openai)
- [An important update: Transitioning Gemini CLI to Antigravity CLI - Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/?utm_source=openai)
- [Cursor – Overview](https://docs.cursor.com/background-agent/api/overview?utm_source=openai)
- [GitHub - xai-org/grok-build at explainx · GitHub](https://github.com/xai-org/grok-build?ref=explainx&utm_source=openai)
- [Measuring political bias in Claude \ Anthropic](https://www.anthropic.com/news/political-even-handedness?utm_source=openai)
- [Demystifying evals for AI agents \ Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents?utm_source=openai)
- [Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents](https://openreview.net/pdf?id=a25dmoIflA&utm_source=openai)
- [Test-based patch clustering for automatically-generated patches assessment - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11269383/?utm_source=openai)
- [Visual comparisons | Playwright](https://playwright.dev/docs/next/test-snapshots?utm_source=openai)
- [The failure mode I keep hitting in long Claude Code sessions — anyone else?](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/?utm_source=openai)
- [Anthropic List Prices — 2026-05-27](https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf?utm_source=openai)
- [Codex now offers pay-as-you-go pricing for teams | OpenAI](https://openai.com/index/codex-flexible-pricing-for-teams/?utm_source=openai)
- [Removed](https://www.reddit.com/r/ChatGPTCoding/comments/1s1flwj/removed/?utm_source=openai)
- [Gemini Developer API pricing  |  Gemini API  |  Google AI for Developers](https://ai.google.dev/gemini-api/docs/pricing?authuser=2&utm_source=openai)
- [Google took 6,000 open source PRs for Gemini CLI, killed it today, and the replacement 403s payin...](https://www.reddit.com/r/GoogleGeminiAI/comments/1u9fy84/google_took_6000_open_source_prs_for_gemini_cli/?utm_source=openai)
- [Cursor – Models & Pricing](https://docs.cursor.com/account/pricing?utm_source=openai)
- [Pricing: Compare Grok Plans | SpaceXAI](https://x.ai/pricing?utm_source=openai)
- [SWE-bench: Can Language Models Resolve Real-world Github Issues?](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html?utm_source=openai)
- [LLM gateway configuration - Anthropic](https://docs.anthropic.com/en/docs/claude-code/llm-gateway?utm_source=openai)
