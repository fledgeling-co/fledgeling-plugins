---
title: "Designing and evaluating context compaction for LLM coding agents"
run_id: dr_1d81320ca18d6aa5
question: "How should an LLM coding agent write a context-compaction summary that maximally preserves the information a fresh session needs to continue work correctly, and how should such summaries be evaluated and benchmarked against a baseline summarizer? Cover: (1) measured evidence on what long-context agent summarization loses and why, especially user corrections, standing constraints, and negative knowledge (rejected approaches, dead ends), and whether recency/position effects or lost-in-the-middle explain the losses; (2) prompt-level techniques with measured results for summarization-for-continuation as distinct from summarization-for-a-reader: structured section schemas, verbatim-preservation instructions, extract-then-compress pipelines, salience/keep-drop criteria, and self-critique or verification passes; (3) evaluation methodology for continuation summaries: reference-free and reference-based metrics, exact-match recall of load-bearing spans, downstream task-success evaluation (does the next session complete the task), LLM-as-judge protocols and their known biases, and how to run a fair A/B benchmark of one summarizer against another on the same transcripts; (4) memory and continuity architectures for agents across context boundaries (external memory files, scratchpads, retrieval over prior transcripts, structured state) and measured comparisons against pure summarization; (5) server-side and harness-level compaction implementations in 2025-2026 (Anthropic's compact beta, agent frameworks) including default prompts, trigger thresholds, and what practitioners report losing."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 33
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-08T03:18:12.511Z
---

> **Errata 2026-08-11:** the `MISSING_DATA` cells for Claude Code /compact are now measured:
> trigger median 99.8% of the window; wall-clock median 171.6 s vs 12.1 s per ordinary turn;
> residue `~51k + 0.117 × pre`. Otherwise current — see `references/evidence.md` § Errata.
## Executive Summary

- **(High Confidence)** A continuation summary should be treated as a **lossy state checkpoint for another agent**, not as prose for a human reader. Its primary job is to preserve executable intent: current objective, acceptance criteria, user corrections, standing constraints, exact identifiers/commands/errors, completed work, rejected routes and why, and the next safe action. Anthropic’s own default compaction prompt explicitly frames the objective as preserving information needed to continue work in a future context, rather than producing a reader-oriented synopsis. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

- **(High Confidence)** Do **not** rely on one rolling natural-language summary as the sole memory layer. Maintain a small, structured, versioned handoff/state artifact in the repository or external store; preserve recent turns verbatim; retain the raw transcript for search/audit; and use the compaction summary as the active working checkpoint. Anthropic’s memory-tool and long-running-agent guidance independently recommend persistent files, progress artifacts, git history, and just-in-time retrieval rather than loading all history into working context. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) ([platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool))

- **(Medium Confidence)** The strongest direct evidence for compaction failure is not yet a controlled study specifically isolating *user corrections*, *standing constraints*, and *negative knowledge*. But recent trajectory-grounded work shows real coding and browsing failures from omissions and meaning mutation; about **90% of reported compaction failures were omissions**, including a coding example where a scoped “leave `b.py` untouched” constraint became a global edit. This is highly relevant to corrections and rejected approaches, but it is not a category-specific prevalence estimate. [arxiv.org](https://arxiv.org/pdf/2605.08580) ([arxiv.org](https://arxiv.org/pdf/2605.08580))

- **(High Confidence)** Long-context degradation is not only truncation. Long-context models exhibit positional sensitivity—often strongest for information at the beginning or end and weaker in the middle—and accuracy can degrade as irrelevant context grows. Therefore, “keep everything until 200k/1M tokens” is not a reliable alternative to disciplined context management. [aclanthology.org](https://aclanthology.org/2024.tacl-1.9/) [aclanthology.org](https://aclanthology.org/2024.findings-acl.890/) ([aclanthology.org](https://aclanthology.org/2024.tacl-1.9/?utm_source=openai))

- **(High Confidence)** Benchmark the candidate skill against Claude Code’s native `/compact` using the **same cut points, transcripts, model configuration where controllable, repository snapshots, continuation prompts, tools, and token budget**. The primary outcome must be downstream continuation success—not ROUGE, summary pleasantness, or summary length. Pair this with exact recall of pre-annotated load-bearing spans and blinded source-grounded review.

- **(Medium Confidence)** A production-quality compactor should be an **extract → compress → verify** pipeline: first create a typed evidence ledger, then generate a concise handoff, then verify every mandatory item has an exact or entailed representation. A recent compaction study found that validating a candidate summary against held-out future trajectory behavior improved task accuracy by up to **8.8 percentage points** and reduced end-to-end latency by up to **39.7%**; this supports validation as a design direction, although the study is a May 2026 preprint rather than peer-reviewed work. [arxiv.org](https://arxiv.org/abs/2605.08580) ([arxiv.org](https://arxiv.org/abs/2605.08580))

- **(High Confidence)** Buy server-side compaction when operational simplicity is paramount; build a harness-level checkpoint layer when continuity correctness is paramount. Anthropic’s server-side API provides a configurable token trigger, a custom replacement prompt, pause-after-compaction control, and compaction-block accounting—but the same model creates the summary, the compaction sampling step incurs cost/rate-limit usage, and no separate cheap summarizer can be selected. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

---

## Detailed Findings

### 1. Answer this decisively: How should an LLM coding agent write a context-compaction summary that maximally preserves the information a fresh session needs to continue work correctly, and how should such summaries be evaluated and benchmarked against a baseline summarizer?

#### Decision: use a structured, state-preserving handoff—not a generic narrative summary

**(High Confidence)** The recommended design is a three-layer continuation package:

1. **Immutable anchors:** task statement, acceptance criteria, standing instructions, user corrections, non-negotiable constraints.
2. **Structured evolving state:** decisions, rejected approaches, verified observations, files changed, test results, unresolved risks, exact literals.
3. **Recent high-fidelity context:** the last several user/assistant/tool exchanges, preserved verbatim.

<INFERENCE from="Anthropic documents that compaction replaces older content with a summary; its pause-after-compaction example preserves the latest three messages verbatim; CAT separates stable task semantics, long-term memory, and high-fidelity recent interactions.">[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction)[arxiv.org](https://arxiv.org/abs/2512.22087)A coding-agent handoff should explicitly separate immutable intent, compacted historical state, and recent detailed interaction because these have different loss tolerances.</INFERENCE> ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

A fresh coding session does not need a literary account of the interaction. It needs to answer, without rereading the transcript:

- What exactly is the user asking for now?
- What constraints override older proposals?
- What has been done and verified?
- What must **not** be changed or retried?
- Which assumptions remain unverified?
- What precise command, test, file, error, identifier, API field, version, branch, or URL matters?
- What is the next safe action?

Anthropic’s default server-side prompt says the summary should contain “state, next steps, learnings” needed to continue in a future context. That is directionally right, but insufficiently explicit for coding continuity because it does not require preservation of corrections, negative knowledge, or exact operational literals. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

#### Why generic compaction loses the wrong things

**(Medium Confidence)** The direct empirical record supports three relevant failure mechanisms:

| Failure mechanism | Strongest evidence | Implication for a coding handoff |
|---|---|---|
| **Omission of future-needed state** | Slipstream reports omissions as roughly **90%** of observed compaction failures across its workloads. [arxiv.org](https://arxiv.org/pdf/2605.08580) | Explicitly inventory incomplete work, evidence, constraints, and rejected paths; do not depend on a salience guess embedded in free prose. |
| **Mutation / commission** | Slipstream documents a coding trace where a scoped instruction—remove calls in `a.py`, leave `b.py` unchanged—was compacted into a global removal instruction. [arxiv.org](https://arxiv.org/pdf/2605.08580) | Record scope boundaries and “must not” instructions as exact, protected text. |
| **Context-position degradation** | Long-context performance can be highest at context edges and substantially weaker in the middle; one ACL 2024 analysis ties this to U-shaped positional attention bias. [aclanthology.org](https://aclanthology.org/2024.tacl-1.9/)[aclanthology.org](https://aclanthology.org/2024.findings-acl.890/) | Do not assume an instruction remains usable merely because it remains present in a large context. Promote critical items to a fixed, structured state section. |
| **Semantic loss in session summaries** | LoCoMo found session-summary retrieval could have high retrieval recall but did not significantly improve downstream QA, likely because dialog-to-summary conversion lost useful information. [aclanthology.org](https://aclanthology.org/2024.acl-long.747.pdf) | Retrieval of a “relevant summary” is not proof that the summary contains action-ready evidence. |
| **Stale-state interference from full histories** | A 2026 50-task expense-agent preprint found pruning/summarization reduced stale-state errors versus full-history context, although its results are domain- and model-specific. [arxiv.org](https://arxiv.org/abs/2606.10209) | Retaining all history is not automatically safer; preserve authoritative current state and discard obsolete observations deliberately. |

([arxiv.org](https://arxiv.org/pdf/2605.08580))

**(Medium Confidence)** “Lost in the middle” and recency effects plausibly contribute to missed user corrections and standing constraints, but they do not fully explain compaction loss. Positional-bias studies measure retrieval/use of information in an intact long prompt; compaction introduces a second failure channel: the information can be omitted, generalized, inverted, or replaced before the next agent sees it. [aclanthology.org](https://aclanthology.org/2024.tacl-1.9/) [arxiv.org](https://arxiv.org/pdf/2605.08580) ([aclanthology.org](https://aclanthology.org/2024.tacl-1.9/?utm_source=openai))

<MISSING_DATA>Controlled studies were sought that independently measure recall of user corrections, standing constraints, and rejected/dead-end knowledge after real coding-agent compaction. The reviewed primary literature has strong evidence for context-position effects, knowledge updates, state drift, and compaction omissions, but no benchmark was found that reports category-specific loss rates for those three coding-continuity categories. A useful study would annotate them separately in real coding transcripts and measure exact preservation plus downstream task impact.</MISSING_DATA>

#### Required summary schema

**(High Confidence)** The following schema should replace a generic “summarize the conversation” instruction. It is deliberately biased toward operational correctness, temporal precedence, and preserving negative knowledge.

```markdown
# CONTINUATION HANDOFF — DO NOT TREAT AS A HUMAN-READABLE SUMMARY

## 1. Current Objective and Definition of Done
- Active user request:
- Deliverable:
- Acceptance tests / observable success criteria:
- Current phase: [investigating | implementing | testing | blocked | awaiting user]

## 2. Standing Constraints and User Corrections — HIGH PRIORITY
- Exact correction or constraint:
  - Source: [user / repo instruction / test / tool output]
  - Supersedes: [older belief or instruction]
  - Preserve verbatim when short:
- Must not:
- Scope boundaries:
- Security / compatibility / performance constraints:

## 3. Verified Current State
- Completed work:
- Files changed or created: `path` — exact purpose
- Git state / branch / commit / uncommitted changes:
- Commands run and outcome:
- Tests:
  - Passed:
  - Failed:
  - Not run:
- Exact errors, versions, IDs, API fields, paths, URLs, flags, or values:

## 4. Decisions, Rejections, and Dead Ends
- Decision: [chosen approach] because [evidence]
- Rejected approach: [approach]
  - Why rejected:
  - Evidence / failed command / failing test:
  - Do not retry unless [condition changes]
- Hypothesis still unverified:

## 5. Remaining Work and Next Safe Action
1. Immediate next action:
2. Then:
3. Blocking uncertainty:
4. What to inspect before editing:

## 6. Retrieval Pointers
- Raw transcript ranges / tool-output IDs / files worth reopening:
- Keep these recent messages verbatim if available:
```

<INFERENCE from="Slipstream’s statement-level validator checks facts, constraints, and intermediate results; LangChain’s default middleware schema separately preserves intent, decisions/rejections, artifacts, and next steps; Anthropic’s server API supports custom compaction instructions.">[arxiv.org](https://arxiv.org/pdf/2605.08580)[github.com](https://github.com/langchain-ai/langchain/blob/master/libs/langchain_v1/langchain/agents/middleware/summarization.py)[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction)The schema above makes those preservation targets mandatory, adds explicit temporal precedence for corrections, and turns negative knowledge into a first-class field.</INFERENCE> ([arxiv.org](https://arxiv.org/pdf/2605.08580))

#### Recommended replacement skill prompt

**(High Confidence)** Use this as the core prompt for a custom continuation-compaction skill. It is intentionally strict about evidence provenance and negative knowledge.

```text
You are creating a CONTINUATION HANDOFF for a fresh coding-agent session.
This is not a summary for a human reader. The raw transcript may become
unavailable. Preserve only information that changes what the next agent should
do, avoid, believe, verify, or retrieve.

Priority order:
1. Latest explicit user corrections and non-negotiable constraints.
2. Exact current task and acceptance criteria.
3. Verified repository/tool state and exact operational literals.
4. Rejected approaches, failed experiments, dead ends, and why they failed.
5. Remaining work and the next safe action.
6. Helpful background.

Rules:
- Newer explicit user instructions override older conflicting statements.
  Record the override and the superseded belief.
- Preserve short load-bearing literals VERBATIM: file paths, symbols, commands,
  versions, error strings, test names, IDs, flags, API fields, URLs, values,
  and “must not” constraints.
- Never convert a verified fact into a guess. Mark each uncertain item
  [UNVERIFIED].
- Never omit a rejected approach if retrying it would waste work or violate a
  user correction.
- Distinguish: [OBSERVED], [INFERRED], [DECISION], [REJECTED], [TODO].
- Do not include hidden reasoning, conversational filler, or duplicated logs.
- If evidence conflicts, retain both claims, name their sources, and state what
  would resolve the conflict.
- Output only the required structured handoff schema.
```

**(Medium Confidence)** Add a separate verifier rather than merely asking the same generation pass to “double-check.” The verifier should compare the draft handoff against an extraction ledger containing required facts and return: `MISSING`, `MUTATED`, `UNSUPPORTED`, `STALE`, or `OK`, with transcript offsets for every failure. Slipstream’s central result is that validation grounded in independent continuation behavior can catch summary insufficiency that source-only summarization metrics miss. [arxiv.org](https://arxiv.org/pdf/2605.08580) ([arxiv.org](https://arxiv.org/pdf/2605.08580))

#### Recommended production pipeline

| Stage | Input | Output | Purpose | Failure controlled |
|---|---|---|---|---|
| 0. Pin | Transcript events | Protected raw spans | Pin latest corrections, “must not” rules, exact literals, current user ask | Loss of constraints and identifiers |
| 1. Extract | Full pre-cut transcript | Typed evidence ledger | Produce atomic items with source offsets and status | Salience hidden in prose |
| 2. Compress | Ledger + transcript | Structured handoff | Fit state into target token budget | Context pressure |
| 3. Verify | Ledger + handoff | Missing/mutated-item report | Require all mandatory items to survive | Omission and meaning drift |
| 4. Preserve recent | Last `k` coherent exchanges | Verbatim context tail | Retain local tool/action continuity | Recent tool/action mismatch |
| 5. Persist | Handoff + ledger + raw transcript index | Repository or external state | Enable recovery/search after repeated compactions | Recursive-summary degradation |
| 6. Continue | Handoff + recent tail + repository snapshot | Fresh agent run | Test actual continuation ability | Cosmetic-quality false positives |

<INFERENCE from="Anthropic’s API explicitly permits pausing after compaction and reattaching the last three messages verbatim; LangChain preserves AI/tool pairs and recent messages; Slipstream validates compacted state using post-cut behavior.">[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction)[github.com](https://github.com/langchain-ai/langchain/blob/master/libs/langchain_v1/langchain/agents/middleware/summarization.py)[arxiv.org](https://arxiv.org/pdf/2605.08580)This staged design is more defensible than a single summary prompt because every high-risk loss category has an explicit representation and a check.</INFERENCE> ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

#### Fair A/B benchmark protocol: custom skill versus Claude Code `/compact`

**(High Confidence)** Run two related benchmarks and report them separately:

1. **Product A/B:** native Claude Code `/compact` versus the candidate skill in the actual Claude Code environment.
2. **Controlled prompt A/B:** same model, same decoding parameters, same transcript cut, same output cap, and same continuation agent; vary only the compaction instructions/pipeline.

<INFERENCE from="Anthropic states its default prompt varies by model and that custom instructions replace—not supplement—the default prompt.">[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction)The product A/B measures the user-facing systems; the controlled A/B isolates the custom compaction design. Combining them would incorrectly attribute hidden product behavior to prompt quality.</INFERENCE> ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

**Corpus construction**

| Requirement | Protocol |
|---|---|
| Unit of evaluation | A real transcript at a predefined handoff cut point, plus a frozen repository/worktree/container snapshot at that exact point. |
| Transcript mix | Stratify by: implementation, debugging, test failure, user correction, changed requirement, rejected approach, long tool output, and multi-file refactor. |
| Cut-point selection | Pre-register cut points before seeing candidate summaries. Include early, middle, and late transcript positions. |
| Critical-span annotation | Annotate atomic load-bearing spans: latest correction, standing constraint, exact literal, current state, decision, rejected route, evidence, next action. Each item gets source offsets and a required preservation mode: exact / semantic / retrievable. |
| Continuation task | Give a fresh agent only the repository snapshot, candidate handoff, fixed system prompt, and fixed follow-up goal. Do not provide raw history unless retrieval is part of the evaluated architecture. |
| Repetitions | Use multiple stochastic continuations per transcript and candidate; pair runs by transcript, seed where supported, and environment snapshot. |
| Blinding | Mask the identity of the summary generator from human reviewers and LLM judges. Randomize A/B display order; run each pair in both orders. |
| Leakage prevention | Hold out transcript families, repositories, and issue templates by split; ensure no continuation prompt contains the gold decision text. |

**Primary metrics**

| Metric | Type | Definition | Why it matters |
|---|---|---|---|
| Continuation task success | Downstream / primary | Test pass, issue resolved, correct tool state, or human acceptance according to a prewritten rubric | Measures whether the new session actually continues correctly |
| Constraint-violation rate | Downstream / primary | Fraction of runs violating a preserved “must not,” user correction, or scope boundary | Directly measures the most expensive failures |
| Exact load-bearing-span recall | Reference-based | Required exact spans reproduced byte-for-byte or via normalized literal match | Protects paths, commands, versions, IDs, flags, errors |
| Atomic-fact recall | Reference-based | Recall of annotated facts, decisions, rejections, and unresolved items | Measures completeness without rewarding verbosity |
| Contradiction / mutation rate | Reference-based | Handoff asserts a claim that contradicts the transcript or changes its scope | Catches dangerous “helpful” rewriting |
| Unsupported-claim rate | Reference-free, source-grounded | Reviewer flags a handoff item lacking transcript support | Measures hallucinated state |
| Summary size and compression ratio | Efficiency | Output tokens / source tokens | A guardrail, never the optimization target |
| Compaction latency and added cost | Efficiency | Wall-clock time, model calls, input/output tokens, billed iterations | Enables operational choice |

**(High Confidence)** Exact-match recall is indispensable for coding handoffs because source-path substitutions, identifier changes, command-flag omissions, and test-name drift can be semantically “similar” yet operationally wrong. Semantic scoring should supplement—not replace—it. [arxiv.org](https://arxiv.org/pdf/2605.08580) ([arxiv.org](https://arxiv.org/pdf/2605.08580))

**Reference-free review protocol**

1. Give the reviewer the raw pre-cut transcript, source-offset index, and one anonymized handoff.
2. Require an itemized verdict for each protected category: `present-and-correct`, `omitted`, `mutated`, `unsupported`, or `stale`.
3. Require the reviewer to cite transcript offsets for every positive or negative judgment.
4. Reject ungrounded free-form “quality” ratings from the main score.
5. Human-audit a stratified subset, especially disagreements and high-impact failures.

**(Medium Confidence)** LLM judges are useful for triage and source-grounded classification, but should not be the only decisive metric. Position bias has been demonstrated across large-scale pairwise judging experiments, and recent summary-evaluation work reports overlap/style biases and self-evaluation concerns. [arxiv.org](https://arxiv.org/abs/2406.07791) [aclanthology.org](https://aclanthology.org/2025.acl-long.702.pdf) ([arxiv.org](https://arxiv.org/abs/2406.07791?utm_source=openai))

**Judge controls**

- Use at least two judge families or one judge plus human adjudication.
- Randomize candidate order and score both `A/B` and `B/A`.
- Enforce equal summary-token caps before pairwise judgment.
- Prohibit the judge from inferring quality from style; require evidence offsets.
- Measure judge self-consistency by rerunning a held-out subset.
- Never use the candidate summarizer itself as the sole judge of its own output.
- Report human–judge agreement, order-flip rate, and abstention/disagreement rate.

**Statistical reporting**

**(High Confidence)** Treat transcript as the paired experimental unit. Report paired bootstrap confidence intervals for continuous metrics; McNemar’s test or a paired permutation test for binary task success; and effect size alongside significance. Do not pool multiple continuations from one transcript as independent samples. <INFERENCE from="The A/B design uses the same transcript and cut point for both candidates.">Paired analysis removes much of the variance caused by repository difficulty and transcript complexity.</INFERENCE>

#### Minimum acceptance gates for shipping the skill

| Gate | Ship criterion |
|---|---|
| Critical constraints | No unreviewed regression in exact recall of user corrections, scope boundaries, or “must not” items |
| Safety | No increase in contradiction/mutation rate |
| Continuation | Non-inferior downstream task success; prefer superiority with paired confidence interval excluding zero |
| Efficiency | Summary stays within the token budget and does not create unacceptable added latency/cost |
| Robustness | Performance holds across at least one correction-heavy and one dead-end-heavy slice |
| Auditability | Every handoff can be traced back to transcript offsets and repository state |

<INFERENCE from="Slipstream shows source-only summary metrics do not capture downstream sufficiency; LongMemEval and LoCoMo evaluate memory through downstream questions and temporal/knowledge-update behavior.">[arxiv.org](https://arxiv.org/pdf/2605.08580)[arxiv.org](https://arxiv.org/abs/2410.10813)[arxiv.org](https://arxiv.org/abs/2402.17753)A compactor should not ship on lexical-overlap gains alone; it must demonstrate preserved continuation behavior.</INFERENCE> ([arxiv.org](https://arxiv.org/pdf/2605.08580))

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

#### Current state of the evidence

**(High Confidence)** Long-context memory remains materially unreliable for long-running interactive systems even when the nominal context window is large. LongMemEval, accepted at ICLR 2025, evaluates extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention; its authors report an approximately **30% accuracy drop** for commercial assistants and long-context LLMs when maintaining information over sustained interactions. [arxiv.org](https://arxiv.org/abs/2410.10813) ([arxiv.org](https://arxiv.org/abs/2410.10813?utm_source=openai))

**(High Confidence)** LoCoMo provides complementary evidence: on very long multi-session conversations, long-context models substantially lagged a human benchmark; its authors found that session-summary-based retrieval did not materially improve performance despite strong retrieval recall, attributing this in part to information loss in converting dialogue to summaries. [aclanthology.org](https://aclanthology.org/2024.acl-long.747.pdf) ([aclanthology.org](https://aclanthology.org/anthology-files/pdf/acl/2024.acl-long.747.pdf?utm_source=openai))

**(Medium Confidence)** Recent compaction-specific evidence is stronger than generic summarization evidence for this decision. Slipstream analyzes coding and browsing trajectories, identifies silent downstream deviation after compaction, reports omission-dominant failure, and evaluates a continuation-grounded validation mechanism on SWE-bench Verified and BrowseComp. The paper is from Princeton and releases code, but remains an arXiv preprint as of August 8, 2026. [arxiv.org](https://arxiv.org/abs/2605.08580) ([arxiv.org](https://arxiv.org/abs/2605.08580))

**(Medium Confidence)** The newest agent-context research supports structured state rather than append-only histories. ACON reports **26–54%** peak-memory reduction while largely preserving task performance across AppWorld, OfficeBench, and multi-objective QA; CAT reports a **57.6%** SWE-bench Verified solve rate for its context-aware compressor. These are useful directional results but are preprints, not independently replicated production benchmarks. [arxiv.org](https://arxiv.org/abs/2510.00615) [arxiv.org](https://arxiv.org/abs/2512.22087) ([arxiv.org](https://arxiv.org/abs/2510.00615?utm_source=openai))

#### Current server-side and harness-level implementations

| Implementation | Parameter Count | Context Window | Latency | Cost | License | Technical reality |
|---|---:|---:|---|---|---|---|
| Anthropic server-side compaction beta | Not publicly disclosed for managed models | Up to **1M tokens** for listed supported models; compaction default trigger is **150,000 input tokens**, minimum configurable trigger **50,000**. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/context-windows)[platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) | No absolute latency SLA published. Compaction adds a sampling iteration. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) | Compaction usage contributes to billing and rate limits; sum `usage.iterations`, not only top-level usage. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) | Managed proprietary API beta | `context_management.edits: [{"type":"compact_20260112"}]`; supports custom replacement instructions and `pause_after_compaction`. |
| Claude Code `/compact` | Not disclosed | Product/model dependent; exact current auto-trigger policy was not found in official public documentation reviewed | <MISSING_DATA>Official absolute latency data not found</MISSING_DATA> | <MISSING_DATA>Official per-compaction billing data not found</MISSING_DATA> | Product service | Practitioner issues report both continuity loss and failures when compaction is attempted at or near exhaustion; treat reports as operational signals, not prevalence evidence. [github.com](https://github.com/anthropics/claude-code/issues/25620) |
| LangChain `SummarizationMiddleware` | Chosen by operator | Model dependent | One separate summarizer call when threshold is reached | Provider/model dependent | Open-source framework; confirm exact version license in procurement review | Default schema explicitly includes session intent, decisions/rejections, artifacts, and next steps; defaults to retaining **20 messages**. [github.com](https://github.com/langchain-ai/langchain/blob/master/libs/langchain_v1/langchain/agents/middleware/summarization.py) |
| LangChain Deep Agents | Chosen by operator | Model dependent; example compacts after e.g. **85%** of max input tokens when offload capacity is exhausted. [docs.langchain.com](https://docs.langchain.com/oss/python/deepagents/context-engineering) | Additional summary call; no official absolute benchmark found | Provider/model dependent | Open-source framework; confirm exact version license in procurement review | Adds offloading and structured in-context summaries. |
| Slipstream research system | Evaluated with Qwen3.5-9B and Seed-OSS-36B-Instruct | Study uses compaction thresholds of **4k**, **16k**, and **32k** tokens—not model context-window claims. [arxiv.org](https://arxiv.org/pdf/2605.08580) | Reported average query latency: **161.3s**, **251.8s**, **513.5s**, and **331.8s** across four reported workloads; synchronous compaction represented **44%**, **39%**, **36%**, and **26%** respectively. [arxiv.org](https://arxiv.org/pdf/2605.08580) | Study does not publish a generally usable production cost schedule | Research code released | Runs compaction asynchronously, validates against held-out future actions, and updates only if validation fails. |
| Recommended custom handoff harness | Match baseline model for fair A/B | Deliberate budget, e.g. handoff + recent tail must fit below a fixed fraction of available context | Measure in your environment | Measure tokens, calls, and wall time | Team-owned | Adds typed extraction, exact-span pinning, verification, persistent state artifact, and raw-history retrieval. |

([docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/context-windows))

#### Anthropic API implementation facts

**(High Confidence)** Anthropic’s currently documented server-side compaction beta uses beta header `compact-2026-01-12` and a request shape equivalent to:

```json
{
  "context_management": {
    "edits": [{
      "type": "compact_20260112",
      "trigger": { "type": "input_tokens", "value": 150000 },
      "pause_after_compaction": false,
      "instructions": "..."
    }]
  }
}
```

The documented default trigger is `{"type": "input_tokens", "value": 150000}`; `input_tokens` is the only supported trigger type; the minimum threshold is 50,000 tokens; and custom instructions replace the model-specific default prompt rather than supplementing it. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

**(High Confidence)** A client must append the complete response content, including the `compaction` block, back into subsequent `messages`; passing back only text silently loses the state that tells the API what history has been compacted. [github.com](https://github.com/anthropics/skills/blob/main/skills/claude-api/SKILL.md) [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([github.com](https://github.com/anthropics/skills/blob/main/skills/claude-api/SKILL.md))

**(High Confidence)** The documented API limitation most relevant to an agent harness is that the request model also performs the summary; a separate cheaper summarizer cannot be selected. Compaction can also fail when tools are defined if the model tries to invoke a tool during its internal summarization step; Anthropic recommends explicitly instructing the summary pass not to call tools. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

**(Medium Confidence)** Practitioner reports indicate a real operational continuity problem in Claude Code, including summaries forgetting prior instructions after compaction and failed compaction at full context. These reports are not controlled measurements and should not be used to quantify defect frequency. [github.com](https://github.com/anthropics/claude-code/issues/34556) [github.com](https://github.com/anthropics/claude-code/issues/25620) [github.com](https://github.com/anthropics/claude-code/issues/79948) ([github.com](https://github.com/anthropics/claude-code/issues/34556?utm_source=openai))

---

### 3. What are the contrasting viewpoints or competing evidence?

**(High Confidence)** The principal competing view is that larger context windows reduce the need for compression. This is partially true for capacity, but not sufficient for reliable continuation: Anthropic’s current documentation explicitly warns that recall and accuracy degrade as context grows (“context rot”), while ACL evidence shows information position can materially affect use even when the evidence remains in the prompt. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/context-windows) [aclanthology.org](https://aclanthology.org/2024.tacl-1.9/) ([docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/context-windows))

**(Medium Confidence)** The competing view that “a simple rolling summary is enough” is weak for high-stakes coding continuity. It is cheaper and often adequate for short tasks, but LoCoMo’s session-summary result and Slipstream’s omission/mutation examples show that a fluent summary can remain insufficient for future action. [aclanthology.org](https://aclanthology.org/2024.acl-long.747.pdf) [arxiv.org](https://arxiv.org/pdf/2605.08580) ([aclanthology.org](https://aclanthology.org/anthology-files/pdf/acl/2024.acl-long.747.pdf?utm_source=openai))

**(Medium Confidence)** The competing view that “external retrieval solves memory loss” is also incomplete. External storage can preserve raw information losslessly, but retrieval can surface irrelevant or conflicting fragments, requires the agent to formulate the right query, and introduces latency. Anthropic’s own context-engineering guidance advocates just-in-time retrieval but explicitly notes the trade-off: runtime exploration is slower and can waste context if the agent navigates poorly. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) ([anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))

**(High Confidence)** The best-supported architecture is therefore hybrid:

- persistent, structured state for always-important information;
- short verbatim recent context for local coherence;
- compaction for old trajectory history;
- retrieval over raw transcripts and durable artifacts for recovery;
- explicit tests/verification rather than trust in summary quality.

<INFERENCE from="Anthropic recommends memory files and just-in-time retrieval; CAT uses fixed task semantics, long-term memory, and recent high-fidelity interactions; LongMemEval evaluates retrieval/memory design choices rather than only full context.">[platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)[arxiv.org](https://arxiv.org/abs/2512.22087)[arxiv.org](https://arxiv.org/abs/2410.10813)This hybrid design is the least brittle approach because it avoids treating any single lossy summary or retrieval query as the sole source of truth.</INFERENCE> ([platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool))

---

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** Between 2024 and August 2026, the field moved from generic long-context and conversational-memory benchmarks toward explicit agent-context management: structured workspaces, persistent memory artifacts, compaction middleware, server-side compaction APIs, proactive context tools, and trajectory-grounded validation. [arxiv.org](https://arxiv.org/abs/2402.17753) [arxiv.org](https://arxiv.org/abs/2510.00615) [arxiv.org](https://arxiv.org/abs/2512.22087) [arxiv.org](https://arxiv.org/abs/2605.08580) ([arxiv.org](https://arxiv.org/abs/2402.17753?utm_source=openai))

**(High Confidence)** Anthropic’s current API reflects this shift: server-side compaction is now documented as the primary strategy for long-running conversations; it supports custom instructions, configurable triggering, preservation of recent messages via pause-and-resume, and usage accounting by compaction iteration. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/context-windows) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

**(Medium Confidence)** The research trajectory is moving from “when should we compress?” to “how can the system prove the compressed state is sufficient for its next actions?” Slipstream is the clearest current example; it uses future agent behavior as a held-out validation signal. This is a stronger evaluation framing than source-summary similarity, but needs independent replication on proprietary coding agents and real developer transcripts. [arxiv.org](https://arxiv.org/pdf/2605.08580) ([arxiv.org](https://arxiv.org/pdf/2605.08580))

**(Medium Confidence)** The operational trajectory is toward active memory architectures, not merely bigger windows: Anthropic exposes client-side memory files; LangChain exposes persistent summarization state and offloading; Letta exposes persistent memory blocks, files, and archival memory. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) [docs.langchain.com](https://docs.langchain.com/oss/python/langchain/context-engineering) [docs.letta.com](https://docs.letta.com/guides/core-concepts/memory/context-hierarchy) ([platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool))

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Server-side compaction defaults to a 150,000-input-token trigger; minimum configurable trigger is 50,000; custom instructions replace default prompt | Anthropic, *Compaction* | Undated; accessed August 8, 2026 | Official product documentation — primary and authoritative implementation source | https://platform.claude.com/docs/en/build-with-claude/compaction |
| Compaction produces a `compaction` block; complete response content must be returned in later requests | Anthropic, *Compaction* | Undated; accessed August 8, 2026 | Official product documentation — primary | https://platform.claude.com/docs/en/build-with-claude/compaction |
| Compaction incurs an additional sampling step and its usage contributes to billing/rate limits | Anthropic, *Compaction* | Undated; accessed August 8, 2026 | Official product documentation — primary | https://platform.claude.com/docs/en/build-with-claude/compaction |
| More context is not automatically better; accuracy and recall degrade with token growth | Anthropic, *Context windows* | Undated; accessed August 8, 2026 | Official product documentation — authoritative product guidance | https://platform.claude.com/docs/en/build-with-claude/context-windows |
| Long-context performance often peaks at the beginning/end and drops for evidence in the middle | Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* | 2024 | TACL peer-reviewed paper — primary research | https://aclanthology.org/2024.tacl-1.9/ |
| U-shaped positional attention bias helps explain lost-in-the-middle behavior | Hsieh et al., *Found in the Middle* | 2024 | ACL Findings peer-reviewed paper — primary research | https://aclanthology.org/2024.findings-acl.890/ |
| LongMemEval reports approximately 30% accuracy degradation for sustained-interaction memory | Wu et al., *LongMemEval* | ICLR 2025; preprint October 2024 | Peer-reviewed benchmark paper and released benchmark — primary | https://arxiv.org/abs/2410.10813 |
| Long conversational session summaries may have high retrieval recall yet insufficient downstream utility due to loss in summarization | Maharana et al., *Evaluating Very Long-Term Conversational Memory of LLM Agents* | ACL 2024 | ACL peer-reviewed benchmark paper — primary | https://aclanthology.org/2024.acl-long.747.pdf |
| Compaction omissions account for roughly 90% of observed failures; compaction can mutate coding scope constraints | Chen et al., *Slipstream* | May 9, 2026 | Open research preprint with released code — primary but not peer-reviewed | https://arxiv.org/pdf/2605.08580 |
| Trajectory-grounded validation improved task accuracy up to 8.8 points and latency up to 39.7% in reported workloads | Chen et al., *Slipstream* | May 9, 2026 | Open research preprint with experimental results — primary but preliminary | https://arxiv.org/abs/2605.08580 |
| ACON reports 26–54% peak-memory reduction while largely preserving task performance | Kang et al., *ACON* | October 1, 2025 | Open research preprint — primary but not independently replicated | https://arxiv.org/abs/2510.00615 |
| CAT uses fixed task semantics, long-term memory, and recent high-fidelity interaction context; reports 57.6% SWE-bench Verified | Liu et al., *Context as a Tool* | December 26, 2025 | Open research preprint — primary but preliminary | https://arxiv.org/abs/2512.22087 |
| LangChain’s default summary schema includes intent, decisions/rejections, artifacts, and next steps | LangChain source, `SummarizationMiddleware` | Current source; accessed August 8, 2026 | Official source repository — primary implementation evidence | https://github.com/langchain-ai/langchain/blob/master/libs/langchain_v1/langchain/agents/middleware/summarization.py |
| Persistent memory files enable cross-conversation storage and just-in-time retrieval | Anthropic, *Memory tool* | Undated; accessed August 8, 2026 | Official product documentation — primary | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool |
| Progress files, git commits, structured feature lists, and clean state help multi-session coding agents resume work | Anthropic, *Effective harnesses for long-running agents* | Undated; accessed August 8, 2026 | Vendor engineering report — authoritative practitioner evidence, not controlled academic research | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| Pairwise LLM judging has demonstrated position bias | Shi et al., *Judging the Judges* | June 2024 | Open research paper — primary evaluation research | https://arxiv.org/abs/2406.07791 |

---

## Knowledge Gaps

### Missing controlled evidence

<MISSING_DATA>There is no identified peer-reviewed coding-agent compaction benchmark that separately reports preservation of: (a) latest user corrections, (b) standing constraints, and (c) rejected/dead-end approaches. Needed: a public corpus of real or carefully simulated coding transcripts with atomic annotations, transcript offsets, frozen repository states, and post-handoff continuation tasks.</MISSING_DATA>

### Missing vendor observability

<MISSING_DATA>Official public documentation reviewed does not provide Claude Code `/compact`’s exact default prompt, exact automatic trigger policy, absolute latency distribution, per-compaction cost, or aggregate reliability/failure rate. Needed: product telemetry or a vendor-published benchmark with model/version/configuration details.</MISSING_DATA>

### Missing apples-to-apples external-memory comparison

<INSUFFICIENT_EVIDENCE>Memory papers and frameworks use different models, retrieval stacks, datasets, prompts, and scoring protocols. Claims that one memory product “beats” rolling summaries are not portable without a common continuation benchmark, fixed tool environment, and reproducible cost/latency accounting.</INSUFFICIENT_EVIDENCE>

### Benchmark integrity risk

<CONFLICTING_EVIDENCE>Long-term-memory systems increasingly report high benchmark scores, but public discussions around LongMemEval implementations raise concerns about evaluator choices, retrieval versus generation scoring, and potential benchmark-specific tuning. The benchmark remains useful for diagnostic slices, but should not be the sole procurement or architecture criterion. Source-based continuation A/B tests on the team’s own real coding traces are required.</CONFLICTING_EVIDENCE>

### LLM-judge reliability

<INSUFFICIENT_EVIDENCE>LLM judges can reduce manual review cost, but position, style, overlap, and self-preference biases make a single uncalibrated judge unsuitable as the primary release gate for continuation summaries. Needed: blinded human calibration data, order-swap tests, and source-offset-grounded judging.</INSUFFICIENT_EVIDENCE>

---

## Recommended Next Steps

1. **Implement the structured handoff skill plus a repository-backed `agent-state.json` or `CONTINUATION.md` artifact.**  
   **Rationale:** This is the lowest-risk design change: it makes corrections, constraints, decisions, rejections, artifacts, and next actions durable before attempting more sophisticated retrieval or asynchronous validation. [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) ([anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents))

2. **Build a 30–50 transcript pilot harness before optimizing the prompt.**  
   **Rationale:** Use real coding traces selected for corrections, scope boundaries, failed approaches, and tool-heavy debugging. Label load-bearing spans and measure exact recall, mutation, and fresh-session success. Use pilot paired discordance to calculate the required sample size for the final A/B.

3. **Run the two-track benchmark: native-product A/B and controlled-prompt A/B.**  
   **Rationale:** The native benchmark answers “is the skill better for our users?”; the controlled one answers “is the prompt/pipeline itself better?” Do not conflate the two because Anthropic’s defaults vary by model and are not fully exposed. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction) ([platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/compaction))

4. **Add a verifier before adding a retrieval system.**  
   **Rationale:** A typed extractor and span-level verifier directly target summary mutation and omission. Only add raw-transcript retrieval once evaluation shows that omitted information is often needed after the handoff and cannot fit in the state artifact. [arxiv.org](https://arxiv.org/pdf/2605.08580) ([arxiv.org](https://arxiv.org/pdf/2605.08580))

5. **Instrument every compaction.**  
   **Rationale:** Log source-token count, output-token count, compaction wall time, model/version, trigger reason, protected-span recall, verifier failures, retrieval calls, continuation result, and test result. This converts “it forgot something” reports into debuggable regressions and makes build-versus-buy decisions measurable.

## Sources

- [Compaction - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Memory tool - Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Slipstream: Trajectory-Grounded Compaction Validation for Long-Horizon Agents](https://arxiv.org/pdf/2605.08580)
- [Lost in the Middle: How Language Models Use Long Contexts - ACL Anthology](https://aclanthology.org/2024.tacl-1.9/?utm_source=openai)
- [2605.08580 Slipstream: Trajectory-Grounded Compaction Validation for Long-Horizon Agents](https://arxiv.org/abs/2605.08580)
- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791?utm_source=openai)
- [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813?utm_source=openai)
- [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://aclanthology.org/anthology-files/pdf/acl/2024.acl-long.747.pdf?utm_source=openai)
- [ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615?utm_source=openai)
- [Context windows - Claude Platform Docs](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [skills/skills/claude-api/SKILL.md at main · anthropics/skills · GitHub](https://github.com/anthropics/skills/blob/main/skills/claude-api/SKILL.md)
- [Feature Request: Persistent Memory Across Context Compactions (59 compactions, built our own) · I...](https://github.com/anthropics/claude-code/issues/34556?utm_source=openai)
- [Effective context engineering for AI agents \ Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://arxiv.org/abs/2402.17753?utm_source=openai)
- [Effective harnesses for long-running agents \ Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
