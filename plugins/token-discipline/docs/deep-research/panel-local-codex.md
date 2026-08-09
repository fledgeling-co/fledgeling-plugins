---
title: "Evaluating terse output prompt compression for Claude Opus 5"
run_id: dr_339418114792aa00
question: "How should a prompt-level \"terse output\" / compressed-response skill for a frontier coding agent (Claude Opus 5 in Claude Code) be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks? Specifically: what does the evidence say about (a) the measured accuracy/quality cost of brevity, conciseness, and \"compressed register\" system prompts on reasoning and coding tasks; (b) whether telegraphic/caveman-style register (dropping articles, function words, hedging) actually saves tokens under BPE/modern tokenizers versus degrading model performance; (c) how instruction placement (system prompt vs appended system prompt vs live turn) and prompt-cache economics change the real cost; (d) which token-reduction levers in agentic coding sessions are actually large (input reuse, tool schemas, subagent prefixes, read width, repetition) versus output prose; (e) documented failure modes where style/persona instructions interfere with instruction-following, tool-calling, and long-horizon agentic performance on Claude and other frontier models in 2025-2026."
provider: local-codex
model: Codex CLI
tier: max
archetype: technical
sources: 16
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-09T05:07:35.652Z
---
Reading additional input from stdin...
2026-08-09T05:04:05.541166Z ERROR codex_models_manager::cache: failed to load models cache: missing field `base_instructions` at line 94 column 5
OpenAI Codex v0.146.0
--------
workdir: /Users/lukerhodes/Dev
model: gpt-5.6-terra
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019fe4e8-20e4-7752-97cb-43d7286c9284
--------
user
<role>
You are a senior research analyst evaluating software stacks, infrastructure, APIs, or model architectures. Your output will directly Rebuilding an open-source 'caveman' terse-output skill for Claude Code. It measurably DECREASED task success on the operator's own agentic coding benchmark (diolog-swe-bench, Opus 5) while delivering only ~10% output-token savings versus a claimed 65%. I need to decide which rules to keep, rewrite, or delete, and what to replace them with, so the rebuilt skill is net-positive on both cost and task success..
</role>

<context>
This investigation supports a concrete decision. Keep this context tight, context bloat degrades long-running agentic output; domain knowledge belongs in the analysis lens below.
</context>

<core_directive>
Answer this decisively: How should a prompt-level "terse output" / compressed-response skill for a frontier coding agent (Claude Opus 5 in Claude Code) be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks? Specifically: what does the evidence say about (a) the measured accuracy/quality cost of brevity, conciseness, and "compressed register" system prompts on reasoning and coding tasks; (b) whether telegraphic/caveman-style register (dropping articles, function words, hedging) actually saves tokens under BPE/modern tokenizers versus degrading model performance; (c) how instruction placement (system prompt vs appended system prompt vs live turn) and prompt-cache economics change the real cost; (d) which token-reduction levers in agentic coding sessions are actually large (input reuse, tool schemas, subagent prefixes, read width, repetition) versus output prose; (e) documented failure modes where style/persona instructions interfere with instruction-following, tool-calling, and long-horizon agentic performance on Claude and other frontier models in 2025-2026.
</core_directive>

<research_questions>
Primary:
1. Answer this decisively: How should a prompt-level "terse output" / compressed-response skill for a frontier coding agent (Claude Opus 5 in Claude Code) be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks? Specifically: what does the evidence say about (a) the measured accuracy/quality cost of brevity, conciseness, and "compressed register" system prompts on reasoning and coding tasks; (b) whether telegraphic/caveman-style register (dropping articles, function words, hedging) actually saves tokens under BPE/modern tokenizers versus degrading model performance; (c) how instruction placement (system prompt vs appended system prompt vs live turn) and prompt-cache economics change the real cost; (d) which token-reduction levers in agentic coding sessions are actually large (input reuse, tool schemas, subagent prefixes, read width, repetition) versus output prose; (e) documented failure modes where style/persona instructions interfere with instruction-following, tool-calling, and long-horizon agentic performance on Claude and other frontier models in 2025-2026.

Secondary:
2. What is the current state, and what is the strongest supporting evidence for it?
3. What are the contrasting viewpoints or competing evidence?
4. What changed recently, and what is the trajectory?
</research_questions>

<scope_and_boundaries>
<include>
- Entities, technologies, geographies, segments, and time windows directly relevant to the core directive.
</include>
<exclude>
- Tangential background material, SEO aggregator content, and pre-scope introductory explainers.
- Model-side quantisation or serving-level compression
- Non-LLM text compression algorithms
</exclude>
<time_horizon>
2024 to present, weighted to 2025-2026 frontier-model behaviour
</time_horizon>
</scope_and_boundaries>

<source_discipline>
<prioritise>
- Primary and authoritative sources: official documentation, peer-reviewed literature, regulators, government databases, published benchmarks, raw datasets, court filings, filed financials.
- Official documentation, source repositories (including issues and PRs), vendor engineering blogs, peer-reviewed benchmarks, architecture whitepapers.
</prioritise>
<deprioritise>
- Aggregator sites, SEO-optimised listicles, marketing blogs, vendor comparison pages, and content farms. Do not rely on these as primary evidence; if cited at all, label them `[SECONDARY: promotional]` and corroborate from a primary source.
- Vendor landing pages, "top 10 tools" listicles, influencer posts, and vendor-commissioned analyst reports (label these `[SECONDARY: promotional]`).
</deprioritise>
<criteria_match_validator>
For each source integrated into the synthesis, briefly justify why it met the source-discipline criteria. Discard sources that cannot be justified rather than including them with a caveat.
</criteria_match_validator>
</source_discipline>

<depth_requirements>
- Factual findings with quantitative data where available (numbers, dates, specific named entities).
- Contrasting viewpoints or competing evidence wherever it exists.
- Named sources (author or organisation, publication date, URL).
- A confidence qualifier on every non-trivial claim: High, Medium, or Low.
- Extract exact latency numbers, API schemas, rate limits, and documented architectural trade-offs verbatim where available.
</depth_requirements>

<analysis_lens>
Apply these analytical frames where relevant, they tell you how to think about the findings, not only what to find:
- Build-vs-buy and operational trade-offs for the stated team size and constraints.
- Measured benchmark evidence over vendor claims
- Tokenizer-level reality of abbreviation and function-word deletion
- Prompt-cache and input-token economics in agentic loops
- Instruction-following interference from persona/style prompts
</analysis_lens>

<epistemic_bounding>
When data is unavailable, unreliable, or contested, use these tags inline. Do not estimate, extrapolate, or paper over gaps:
- `<MISSING_DATA>[what was sought, what was unavailable, what would be needed]</MISSING_DATA>`
- `<INSUFFICIENT_EVIDENCE>[claim that could not be corroborated, and why]</INSUFFICIENT_EVIDENCE>`
- `<CONFLICTING_EVIDENCE>[the positions, their sources, the nature of the disagreement]</CONFLICTING_EVIDENCE>`
- `<CONFIDENCE:LOW>[the claim]</CONFIDENCE:LOW>` for weakly-supported but load-bearing estimates
- `<INFERENCE from="[the cited claims it rests on]">[claim derived by reasoning; show the chain]</INFERENCE>`, this tag is required for every statement you assembled rather than read. A conclusion drawn from three sourced facts is an inference even when all three are correct, and naming which facts it rests on is what lets a reader check the step you took between them.
Do not present extrapolated or synthesised numbers as empirical findings.
</epistemic_bounding>

<citation_protocol>
Append an inline ``` to every quantitative claim, every attributed statement, and every regulatory or legal reference, at the point of the claim itself. Do not aggregate citations at the end of a paragraph or into a bibliography, that is where source attribution is lost. If a URL is not verifiable at synthesis time, use ``UNVERIFIED (unusable citation URL)`` rather than omitting or inventing one.
</citation_protocol>

<output_format>
Structure the report exactly as follows:
- ## Executive Summary, 5-8 bullets, each led by a `(High Confidence)` / `(Medium Confidence)` / `(Low Confidence)` qualifier; usable as a standalone briefing.
- ## Detailed Findings, one section per research question, using the question as the heading; narrative prose with inline citations, tables for comparative data.
- ## Evidence Table, | Claim | Primary Source | Publication Date | Evidence Type | URL |, mapping every major claim to a verifiable source.
- ## Knowledge Gaps, what could not be answered, categorised by cause.
- ## Recommended Next Steps, 3-5 follow-up investigations, each with a stated rationale.
- Include a comparison table with columns such as Parameter Count / Context Window / Latency / Cost / License, technical reality lives in tables, prose buries it.
</output_format>

<constraints>
- Do not fabricate citations, URLs, authors, or dates; use the unverified citation form when a source cannot be verified.
- Where data conflicts, present both positions with their evidence, do not silently pick one.
- Keep prose dense but readable; avoid filler phrases.
- Cite inline at the point of the claim, never aggregated at the end.
</constraints>

<core_directive>
Answer this decisively: How should a prompt-level "terse output" / compressed-response skill for a frontier coding agent (Claude Opus 5 in Claude Code) be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks? Specifically: what does the evidence say about (a) the measured accuracy/quality cost of brevity, conciseness, and "compressed register" system prompts on reasoning and coding tasks; (b) whether telegraphic/caveman-style register (dropping articles, function words, hedging) actually saves tokens under BPE/modern tokenizers versus degrading model performance; (c) how instruction placement (system prompt vs appended system prompt vs live turn) and prompt-cache economics change the real cost; (d) which token-reduction levers in agentic coding sessions are actually large (input reuse, tool schemas, subagent prefixes, read width, repetition) versus output prose; (e) documented failure modes where style/persona instructions interfere with instruction-following, tool-calling, and long-horizon agentic performance on Claude and other frontier models in 2025-2026.
</core_directive>
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’ll ground this in primary benchmark papers, Anthropic documentation, and source code/docs for Claude Code. I’ll distinguish measured findings from design inferences and flag gaps where no public controlled evidence exists.
web search: 
web search: site:arxiv.org conciseness prompt instruction performance benchmark language models brevity style system prompt ...
web search: 
web search: site:arxiv.org conciseness prompt instruction performance benchmark language models brevity style system prompt ...
web search: 
web search: site:platform.claude.com/docs/en/build-with-claude/prompt-caching pricing cache writes cache reads ...
web search: 
web search: "concise" prompts "performance" LLM benchmark paper ...
web search: 
web search: tokenizer abbreviation "tokens" LLM prompt compression language BPE study ...
web search: 
web search: site:docs.anthropic.com/en/docs/claude-code "output styles" concise ...
web search: 
web search: site:code.claude.com/docs output styles Claude Code ...
web search: 
web search: site:anthropic.com/engineering context engineering agents tool output large context 2025 ...
web search: 
web search: site:platform.claude.com/docs models Claude Opus 5 context window 2026 ...
web search: 
web search: arxiv Chain of Draft minimal words intermediate reasoning 2024 accuracy token reduction ...
web search: 
web search: "persona prompting" LLM "coding" benchmark paper 2025 ...
codex
## Executive Summary

- (High Confidence) Delete the caveman register. The operator’s own Opus 5 benchmark already shows lower task success for only ~10% output-token reduction; no public evidence establishes telegraphic English as safe for frontier coding agents. `UNVERIFIED (unusable citation URL)` (unusable citation URL)`

- (High Confidence) Replace it with a narrowly scoped “compact normal English for user-visible prose” policy that explicitly exempts reasoning, tool calls, code, test/command output, errors, identifiers, safety caveats, and verification. This preserves the agent’s operational language while removing low-value narration.

- (High Confidence) Do not impose word/token caps or “no hedging / no articles / no function words” rules globally. Concise-reasoning research is conditional: CCoT reduced output by 48.70% with little aggregate impact on one MCQA study, but caused a 27.69% math penalty for GPT‑3.5. [arxiv.org](https://arxiv.org/abs/2401.05618)

- (High Confidence) The largest practical token levers are context architecture, not conversational prose: cache stable system/tool prefixes; load tools on demand; constrain tool-result width; isolate high-volume work in subagents; and compact history with high-recall task state. Anthropic documents tool-search, code execution, and cache mechanisms specifically for this purpose. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching) [anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp) [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

- (High Confidence) For Claude Opus 5, a cached input token costs $0.50/MTok while output costs $25/MTok; output tokens are 50× more expensive than cache-read input tokens. <INFERENCE from="Anthropic prompt-caching price table">$25 ÷ $0.50 = 50</INFERENCE> [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) This makes concise final prose worthwhile, but only if it does not increase retries, tool calls, or failed-task cost.

- (High Confidence) Implement the policy as an opt-in Claude Code output style with `keep-coding-instructions: true`, not as a replacement system prompt and not as a persona. Claude Code warns that custom output styles otherwise omit its built-in software-engineering instructions. [code.claude.com](https://code.claude.com/docs/en/output-styles)

- (Medium Confidence) Treat concise external communication and concise reasoning as separate experiments. Chain-of-Draft reports comparable or better results using as little as 7.6% of CoT tokens, but it is a task-specific reasoning method, not evidence that an always-on caveman persona is safe for long-horizon coding. [arxiv.org](https://arxiv.org/abs/2502.18600)

## Detailed Findings

### 1. Answer this decisively: How should a prompt-level “terse output” / compressed-response skill for a frontier coding agent be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks?

Use a **communication policy, not a persona or compressed register**.

Recommended replacement:

```md
---
name: compact-coding
description: Compact user-visible status and final responses without changing engineering behaviour.
keep-coding-instructions: true
---

Use compact, normal English for user-visible prose.

- State only information that changes the user's understanding or next action.
- Prefer direct sentences and short bullets over preambles, repetition, and progress narration.
- Preserve exact commands, identifiers, file paths, code, error messages, test results, risks, blockers, and necessary uncertainty.
- If the user asks for an explanation, design rationale, review, or report, provide the necessary detail normally.
- Do not constrain or abbreviate tool calls, code, test output, exploration, verification, planning, or internal reasoning.
- Do not use telegraphic/caveman grammar, role-play, slogans, mandatory word limits, or “never hedge” rules.
```

(High Confidence) This design targets the actual discretionary material—assistant-facing chatter—rather than making the agent operate in a damaged linguistic register. <INFERENCE from="operator benchmark result; Anthropic output-style semantics; CCoT’s task-dependent penalty">A policy that confines compression to user-visible prose removes a known source of interference while retaining the only plausible output-token saving.</INFERENCE> `UNVERIFIED (unusable citation URL)` [code.claude.com](https://code.claude.com/docs/en/output-styles) [arxiv.org](https://arxiv.org/abs/2401.05618)

| Rule in the old skill | Decision | Replacement |
|---|---|---|
| Avoid repeating the task, obvious progress updates, and generic pleasantries | Keep | “State only information that changes the user’s understanding or next action.” |
| Prefer concise final status | Keep, narrow | “Changes / verification / blocker” in short bullets. |
| “Be terse” | Rewrite | Specify the target: user-visible prose only; do not constrain operational work. |
| “No unnecessary explanation” | Rewrite | Permit detail when asked, when reporting risk, or when validation needs interpretation. |
| Drop articles, function words, qualifiers, and complete grammar | Delete | Use ordinary concise English. |
| “No hedging” | Delete | Require calibrated uncertainty; software agents must distinguish verified from inferred. |
| Strict per-response word/token caps | Delete | Use an optional soft response budget only in an experiment; never cap code/task work. |
| Caveman persona / role-play | Delete | No persona. State behavioural constraints directly. |
| Suppress planning, exploration, checking, or tests | Delete | Explicitly protect these activities. |
| Compress tool output indiscriminately | Delete | Filter at source, preserve verbatim action-critical evidence. |

(High Confidence) Do not represent the policy as “think less,” “reason less,” or “answer with fragments.” Opus 5 has adaptive thinking on by default, and Anthropic recommends controlling effort through evaluation rather than generic prompt compression. [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)

#### Technical reality

| Deployment parameter | Claude Opus 5, standard API | Claude Opus 5, cache hit | Claude Opus 5, Fast mode |
|---|---:|---:|---:|
| Parameter count | Not published | Not published | Not published |
| Context window | 1M tokens | 1M tokens | 1M tokens |
| Max output | 128k tokens | 128k tokens | 128k tokens |
| Latency | “Moderate”; no public numeric SLA | Improved TTFT for long cached prefixes; no public numeric SLA | Up to 2.5× higher output speed |
| Cost | $5 input / $25 output per MTok | $0.50 cache-read per MTok | $10 input / $50 output per MTok |
| License | Proprietary | Proprietary | Proprietary |

(High Confidence) Anthropic does not publish Opus 5 parameter count or a fixed numerical latency SLA; “moderate” is its published comparative-latency label. [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/overview) [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

### 2. What does the evidence say about brevity, conciseness, and compressed-register prompts on reasoning and coding tasks?

(High Confidence) Concision can be beneficial when it removes redundant reasoning while preserving task-relevant structure; it is not evidence for malformed language. Renze and Guven’s 2024 preprint found CCoT reduced average output length by 48.70% on its GPT‑3.5/GPT‑4 MCQA evaluation with negligible overall performance change, but GPT‑3.5 math performance fell 27.69%. [arxiv.org](https://arxiv.org/abs/2401.05618)

(Medium Confidence) Chain-of-Draft reports matching or exceeding standard CoT accuracy while using as little as 7.6% of tokens on its evaluated reasoning tasks. Its method is minimal but informative intermediate drafts, not deletion of grammar from all agent communication. [arxiv.org](https://arxiv.org/abs/2502.18600)

(High Confidence) Neither study evaluates Claude Opus 5 running Claude Code on SWE-bench-like, tool-mediated, multi-turn repository tasks. <MISSING_DATA>What was sought: controlled Opus 5 / Claude Code / SWE-bench experiments comparing normal concise English, caveman register, output caps, and baseline. What is unavailable: a public study isolating those variables. What is needed: paired task-level evaluation with billed usage telemetry.</MISSING_DATA>

(High Confidence) Your benchmark result should therefore dominate general reasoning-paper results for this decision. <INFERENCE from="the operator’s matched environment is Claude Opus 5 + Claude Code + diolog-swe-bench; external studies test different models and tasks">Local, task-matched evidence has higher decision relevance than cross-domain prompting studies.</INFERENCE> `UNVERIFIED (unusable citation URL)`

### 3. Does telegraphic/caveman register save tokens under modern tokenizers, versus degrading performance?

(High Confidence) There is no defensible universal percentage saving. Claude’s tokenizer is model-specific; Anthropic provides `POST /v1/messages/count_tokens` precisely to measure a full request—including system prompt, messages, and tools—against the selected model. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

(High Confidence) The tokenizer changed for Claude 4.7-and-later models; Anthropic says the same text produces approximately 30% more tokens than on earlier models, varying by workload. This makes inherited token-saving claims especially unreliable. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

(Medium Confidence) Removing a word only saves tokens if that exact model tokenizer encoded it as one or more tokens; replacing it with an abbreviation can save nothing or cost more because subword tokenization is not word counting. <INFERENCE from="Anthropic’s model-specific count endpoint and its warning that token counts differ across tokenizer generations">Only empirical counts of the exact serialized request can establish savings.</INFERENCE> [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

(High Confidence) Run a tokenizer A/B before retaining any rule: count the entire current skill, the proposed normal-English policy, and the caveman version under `claude-opus-5`; then separately measure generated output and total billed cost in benchmark runs. Do not extrapolate from character count.

### 4. How do instruction placement and prompt-cache economics change the real cost?

| Placement | Claude Code behaviour | Cost / reliability implication | Recommendation |
|---|---|---|---|
| Custom output style | Added to end of system prompt; reminders are issued during the conversation | Persistent and cacheable after initial write, but broad behavioural influence | Use only the narrow replacement policy with `keep-coding-instructions: true` |
| `--append-system-prompt` | One-off addition to system prompt | Appropriate for an experiment; varies the prefix and can reduce cache reuse across cohorts | Use for A/B trials |
| Live user turn / slash command | User-level, task-scoped instruction | Lower blast radius; less reliable as a persistent global style | Best for temporary “brief final report” mode |
| Replacement system prompt / custom subagent system prompt | Replaces Claude Code default prompt | Can omit default engineering behaviour | Do not use for a terse-output feature |

(High Confidence) Claude Code says output-style instructions are added to the end of the system prompt, receive conversation reminders, and custom styles omit built-in engineering instructions unless `keep-coding-instructions` is true. [code.claude.com](https://code.claude.com/docs/en/output-styles)

(High Confidence) Cache hits require an exactly identical prefix through the cache breakpoint. Stable shared system instructions and tool definitions are cacheable; changing a global prompt per task or cohort prevents reuse for changed portions. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

(High Confidence) Opus 5 pricing is $5/MTok base input, $6.25/MTok for a five-minute cache write, $10/MTok for a one-hour cache write, $0.50/MTok cache read, and $25/MTok output. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

(Medium Confidence) A stable 100-token output-style instruction is economically negligible after cache warm-up, whereas a repeated 500-token final answer remains output-priced. <INFERENCE from="Opus 5’s $0.50/MTok cache-read price and $25/MTok output price">The stable prompt costs roughly 50× less per cached token than emitted prose; however, this does not justify a style that causes retries or failures.</INFERENCE> [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

### 5. Which token-reduction levers are actually large in agentic coding sessions?

| Lever | Evidence | Expected priority |
|---|---|---|
| Cache stable prompt, tool, and history prefixes | Tools, system messages, messages, tool use, and tool results can be cached. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Highest |
| Load tools on demand | Anthropic recommends a small cached always-loaded tool set and tool discovery as needed. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching) | Highest |
| Programmatic tool calling | Anthropic reports typical 20–40% token savings for production requests with 10–49 tools. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) | High where applicable |
| Filter data before it reaches context | Anthropic’s example reduces a 10,000-row sheet to five displayed rows. [anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp) | High |
| Clear or summarize stale tool outputs | Anthropic identifies old raw tool calls/results as low-hanging superfluous context. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | High, but preserve anchors |
| Use subagents for noisy, self-contained work | Claude Code isolates verbose subagent output, returning a summary; it also warns that many detailed subagent returns consume main-context space. [code.claude.com](https://code.claude.com/docs/en/sub-agents) | Medium |
| Shorten ordinary final prose | Output is expensive but is often a small share of an agent’s total trajectory | Medium; retain only the narrow policy |

(High Confidence) “Read width” is more important than prose style when tool results are large. Returning the five relevant records rather than 10,000 rows preserves the agent’s ability to reason while preventing context accumulation. [anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp)

(Medium Confidence) Never summarize or strip text needed as a verbatim edit anchor, failing-test evidence, exact API contract, or error reproduction. A 2026 preprint reports compression reduced patch application from 27/40 to 15/40 in a small SWE-bench-derived Go study after corrupting such anchors. [arxiv.org](https://arxiv.org/abs/2607.12161)

### 6. What are the documented failure modes where style/persona instructions interfere with instruction-following, tool calling, and long-horizon performance?

(High Confidence) The clearest documented Claude Code failure mode is configuration-level: a custom output style can remove its built-in software-engineering instructions. A terse style built without `keep-coding-instructions: true` can therefore change much more than prose. [code.claude.com](https://code.claude.com/docs/en/output-styles)

(Medium Confidence) Persona prompting is not reliably capability-improving. A 2025 Wharton technical report found no expert or low-knowledge persona reliably improved GPQA performance for any tested model, while low-knowledge personas were generally harmful. This is benchmark evidence, but it is not a Claude Code coding evaluation. [gail.wharton.upenn.edu](https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/)

(Medium Confidence) Persona effects are task- and model-dependent rather than uniformly harmful: persona prompting can help tasks whose objective is simulation or style, so “never use a persona” is too broad outside engineering. [arxiv.org](https://arxiv.org/abs/2402.10811)

(High Confidence) No primary source located establishes that dropping articles specifically causes Claude Opus 5 tool-call syntax errors. <INSUFFICIENT_EVIDENCE>Claim not corroborated: a direct causal link from caveman grammar to Opus 5 tool-call failure. The appropriate conclusion is risk-based, supported by the operator’s task-success regression and absence of demonstrated token benefit—not a fabricated mechanistic claim.</INSUFFICIENT_EVIDENCE>

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| CCoT cut response length 48.70%; GPT‑3.5 math penalty 27.69% | Renze & Guven | 2024-01-11 | Research preprint; code/data linked by authors | https://arxiv.org/abs/2401.05618 |
| Chain-of-Draft can use as little as 7.6% of CoT tokens on evaluated tasks | Xu, Xie, Zhao & He | 2025-02-25 | Research preprint | https://arxiv.org/abs/2502.18600 |
| Opus 5 context, output limit, pricing, thinking default | Anthropic | 2026-07-24 | Official model documentation | https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8 |
| Cache reads cost 0.1× base input; cacheable request elements and exact-prefix requirements | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| Count tokens under the model-specific tokenizer; newer tokenizer differs materially | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/build-with-claude/token-counting |
| Output styles modify system prompt and can omit coding instructions | Anthropic | Living documentation, accessed 2026-08-09 | Official Claude Code documentation | https://code.claude.com/docs/en/output-styles |
| Tool search and programmatic calling reduce tool-context cost | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching |
| Production requests with 10–49 tools typically save 20–40% tokens with programmatic tool calling | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling |
| Filter tool data before returning it to model context | Anthropic | 2025-11-04 | Vendor engineering article; direct architecture example | https://www.anthropic.com/engineering/code-execution-with-mcp |
| Clear stale tool results and retain structured task memory | Anthropic | 2025-09-29 | Vendor engineering article; direct agent-context guidance | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| Expert personas do not reliably improve factual benchmark accuracy | Wharton Generative AI Labs | 2025-12-07 | Technical report / preprint summary | https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/ |
| Compression can remove action-critical anchors and reduce coding success | Weinberger & Hozez | 2026-07-13 | Research preprint; directly agentic-code relevant | https://arxiv.org/abs/2607.12161 |

## Knowledge Gaps

- **Direct causal evidence:** <MISSING_DATA>There is no public paired benchmark of caveman grammar versus normal concise English for Claude Opus 5 in Claude Code on SWE-bench-style tasks.</MISSING_DATA>

- **Tokenizer evidence:** <MISSING_DATA>No public Claude Opus 5 tokenizer breakdown was found for the exact old skill. Use Anthropic’s count endpoint on the real serialized prompts.</MISSING_DATA>

- **Claude Code billing attribution:** <MISSING_DATA>Without run-level `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`, tool-call counts, retries, and pass/fail records, it is not possible to state what share of your bill prose represents.</MISSING_DATA>

- **Long-horizon behavioural mechanism:** <INSUFFICIENT_EVIDENCE>The observed success decrease is real for the operator’s benchmark, but public evidence cannot yet distinguish whether it arose from impaired instruction-following, lower-quality plans, missed verification, changed tool use, or another interaction.</INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1. Run a three-arm paired benchmark: baseline, current caveman skill, and the replacement policy. Hold model, effort, repository, task order, tools, and permissions constant. Measure solved rate and dollars per solved task.

2. Add telemetry per run: output tokens, uncached input, cache-read input, cache writes, tool-result input, tool-call count, turns, wall time, compactions, and retries. The decision metric should be **success-adjusted billed cost**, not token reduction.

3. Use Anthropic’s token-count endpoint to compare the old and replacement instructions under `claude-opus-5`, including the actual tool definitions. This resolves the claimed 65% saving before further prompt iteration. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

4. Prioritize context controls: tool-result filtering, dynamic tool loading, stable caching, and structured compaction. Test each independently before combining them.

5. Keep the replacement policy only if its lower confidence bound on task success is non-inferior to baseline and it reduces success-adjusted cost. Otherwise remove the global style entirely and use a per-task “brief final report” command.
tokens used
99,684
## Executive Summary

- (High Confidence) Delete the caveman register. The operator’s own Opus 5 benchmark already shows lower task success for only ~10% output-token reduction; no public evidence establishes telegraphic English as safe for frontier coding agents. `UNVERIFIED (unusable citation URL)`

- (High Confidence) Replace it with a narrowly scoped “compact normal English for user-visible prose” policy that explicitly exempts reasoning, tool calls, code, test/command output, errors, identifiers, safety caveats, and verification. This preserves the agent’s operational language while removing low-value narration.

- (High Confidence) Do not impose word/token caps or “no hedging / no articles / no function words” rules globally. Concise-reasoning research is conditional: CCoT reduced output by 48.70% with little aggregate impact on one MCQA study, but caused a 27.69% math penalty for GPT‑3.5. [arxiv.org](https://arxiv.org/abs/2401.05618)

- (High Confidence) The largest practical token levers are context architecture, not conversational prose: cache stable system/tool prefixes; load tools on demand; constrain tool-result width; isolate high-volume work in subagents; and compact history with high-recall task state. Anthropic documents tool-search, code execution, and cache mechanisms specifically for this purpose. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching) [anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp) [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

- (High Confidence) For Claude Opus 5, a cached input token costs $0.50/MTok while output costs $25/MTok; output tokens are 50× more expensive than cache-read input tokens. <INFERENCE from="Anthropic prompt-caching price table">$25 ÷ $0.50 = 50</INFERENCE> [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) This makes concise final prose worthwhile, but only if it does not increase retries, tool calls, or failed-task cost.

- (High Confidence) Implement the policy as an opt-in Claude Code output style with `keep-coding-instructions: true`, not as a replacement system prompt and not as a persona. Claude Code warns that custom output styles otherwise omit its built-in software-engineering instructions. [code.claude.com](https://code.claude.com/docs/en/output-styles)

- (Medium Confidence) Treat concise external communication and concise reasoning as separate experiments. Chain-of-Draft reports comparable or better results using as little as 7.6% of CoT tokens, but it is a task-specific reasoning method, not evidence that an always-on caveman persona is safe for long-horizon coding. [arxiv.org](https://arxiv.org/abs/2502.18600)

## Detailed Findings

### 1. Answer this decisively: How should a prompt-level “terse output” / compressed-response skill for a frontier coding agent be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks?

Use a **communication policy, not a persona or compressed register**.

Recommended replacement:

```md
---
name: compact-coding
description: Compact user-visible status and final responses without changing engineering behaviour.
keep-coding-instructions: true
---

Use compact, normal English for user-visible prose.

- State only information that changes the user's understanding or next action.
- Prefer direct sentences and short bullets over preambles, repetition, and progress narration.
- Preserve exact commands, identifiers, file paths, code, error messages, test results, risks, blockers, and necessary uncertainty.
- If the user asks for an explanation, design rationale, review, or report, provide the necessary detail normally.
- Do not constrain or abbreviate tool calls, code, test output, exploration, verification, planning, or internal reasoning.
- Do not use telegraphic/caveman grammar, role-play, slogans, mandatory word limits, or “never hedge” rules.
```

(High Confidence) This design targets the actual discretionary material—assistant-facing chatter—rather than making the agent operate in a damaged linguistic register. <INFERENCE from="operator benchmark result; Anthropic output-style semantics; CCoT’s task-dependent penalty">A policy that confines compression to user-visible prose removes a known source of interference while retaining the only plausible output-token saving.</INFERENCE> `UNVERIFIED (unusable citation URL)` [code.claude.com](https://code.claude.com/docs/en/output-styles) [arxiv.org](https://arxiv.org/abs/2401.05618)

| Rule in the old skill | Decision | Replacement |
|---|---|---|
| Avoid repeating the task, obvious progress updates, and generic pleasantries | Keep | “State only information that changes the user’s understanding or next action.” |
| Prefer concise final status | Keep, narrow | “Changes / verification / blocker” in short bullets. |
| “Be terse” | Rewrite | Specify the target: user-visible prose only; do not constrain operational work. |
| “No unnecessary explanation” | Rewrite | Permit detail when asked, when reporting risk, or when validation needs interpretation. |
| Drop articles, function words, qualifiers, and complete grammar | Delete | Use ordinary concise English. |
| “No hedging” | Delete | Require calibrated uncertainty; software agents must distinguish verified from inferred. |
| Strict per-response word/token caps | Delete | Use an optional soft response budget only in an experiment; never cap code/task work. |
| Caveman persona / role-play | Delete | No persona. State behavioural constraints directly. |
| Suppress planning, exploration, checking, or tests | Delete | Explicitly protect these activities. |
| Compress tool output indiscriminately | Delete | Filter at source, preserve verbatim action-critical evidence. |

(High Confidence) Do not represent the policy as “think less,” “reason less,” or “answer with fragments.” Opus 5 has adaptive thinking on by default, and Anthropic recommends controlling effort through evaluation rather than generic prompt compression. [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)

#### Technical reality

| Deployment parameter | Claude Opus 5, standard API | Claude Opus 5, cache hit | Claude Opus 5, Fast mode |
|---|---:|---:|---:|
| Parameter count | Not published | Not published | Not published |
| Context window | 1M tokens | 1M tokens | 1M tokens |
| Max output | 128k tokens | 128k tokens | 128k tokens |
| Latency | “Moderate”; no public numeric SLA | Improved TTFT for long cached prefixes; no public numeric SLA | Up to 2.5× higher output speed |
| Cost | $5 input / $25 output per MTok | $0.50 cache-read per MTok | $10 input / $50 output per MTok |
| License | Proprietary | Proprietary | Proprietary |

(High Confidence) Anthropic does not publish Opus 5 parameter count or a fixed numerical latency SLA; “moderate” is its published comparative-latency label. [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/overview) [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8)

### 2. What does the evidence say about brevity, conciseness, and compressed-register prompts on reasoning and coding tasks?

(High Confidence) Concision can be beneficial when it removes redundant reasoning while preserving task-relevant structure; it is not evidence for malformed language. Renze and Guven’s 2024 preprint found CCoT reduced average output length by 48.70% on its GPT‑3.5/GPT‑4 MCQA evaluation with negligible overall performance change, but GPT‑3.5 math performance fell 27.69%. [arxiv.org](https://arxiv.org/abs/2401.05618)

(Medium Confidence) Chain-of-Draft reports matching or exceeding standard CoT accuracy while using as little as 7.6% of tokens on its evaluated reasoning tasks. Its method is minimal but informative intermediate drafts, not deletion of grammar from all agent communication. [arxiv.org](https://arxiv.org/abs/2502.18600)

(High Confidence) Neither study evaluates Claude Opus 5 running Claude Code on SWE-bench-like, tool-mediated, multi-turn repository tasks. <MISSING_DATA>What was sought: controlled Opus 5 / Claude Code / SWE-bench experiments comparing normal concise English, caveman register, output caps, and baseline. What is unavailable: a public study isolating those variables. What is needed: paired task-level evaluation with billed usage telemetry.</MISSING_DATA>

(High Confidence) Your benchmark result should therefore dominate general reasoning-paper results for this decision. <INFERENCE from="the operator’s matched environment is Claude Opus 5 + Claude Code + diolog-swe-bench; external studies test different models and tasks">Local, task-matched evidence has higher decision relevance than cross-domain prompting studies.</INFERENCE> `UNVERIFIED (unusable citation URL)`

### 3. Does telegraphic/caveman register save tokens under modern tokenizers, versus degrading performance?

(High Confidence) There is no defensible universal percentage saving. Claude’s tokenizer is model-specific; Anthropic provides `POST /v1/messages/count_tokens` precisely to measure a full request—including system prompt, messages, and tools—against the selected model. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

(High Confidence) The tokenizer changed for Claude 4.7-and-later models; Anthropic says the same text produces approximately 30% more tokens than on earlier models, varying by workload. This makes inherited token-saving claims especially unreliable. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

(Medium Confidence) Removing a word only saves tokens if that exact model tokenizer encoded it as one or more tokens; replacing it with an abbreviation can save nothing or cost more because subword tokenization is not word counting. <INFERENCE from="Anthropic’s model-specific count endpoint and its warning that token counts differ across tokenizer generations">Only empirical counts of the exact serialized request can establish savings.</INFERENCE> [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

(High Confidence) Run a tokenizer A/B before retaining any rule: count the entire current skill, the proposed normal-English policy, and the caveman version under `claude-opus-5`; then separately measure generated output and total billed cost in benchmark runs. Do not extrapolate from character count.

### 4. How do instruction placement and prompt-cache economics change the real cost?

| Placement | Claude Code behaviour | Cost / reliability implication | Recommendation |
|---|---|---|---|
| Custom output style | Added to end of system prompt; reminders are issued during the conversation | Persistent and cacheable after initial write, but broad behavioural influence | Use only the narrow replacement policy with `keep-coding-instructions: true` |
| `--append-system-prompt` | One-off addition to system prompt | Appropriate for an experiment; varies the prefix and can reduce cache reuse across cohorts | Use for A/B trials |
| Live user turn / slash command | User-level, task-scoped instruction | Lower blast radius; less reliable as a persistent global style | Best for temporary “brief final report” mode |
| Replacement system prompt / custom subagent system prompt | Replaces Claude Code default prompt | Can omit default engineering behaviour | Do not use for a terse-output feature |

(High Confidence) Claude Code says output-style instructions are added to the end of the system prompt, receive conversation reminders, and custom styles omit built-in engineering instructions unless `keep-coding-instructions` is true. [code.claude.com](https://code.claude.com/docs/en/output-styles)

(High Confidence) Cache hits require an exactly identical prefix through the cache breakpoint. Stable shared system instructions and tool definitions are cacheable; changing a global prompt per task or cohort prevents reuse for changed portions. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

(High Confidence) Opus 5 pricing is $5/MTok base input, $6.25/MTok for a five-minute cache write, $10/MTok for a one-hour cache write, $0.50/MTok cache read, and $25/MTok output. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

(Medium Confidence) A stable 100-token output-style instruction is economically negligible after cache warm-up, whereas a repeated 500-token final answer remains output-priced. <INFERENCE from="Opus 5’s $0.50/MTok cache-read price and $25/MTok output price">The stable prompt costs roughly 50× less per cached token than emitted prose; however, this does not justify a style that causes retries or failures.</INFERENCE> [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

### 5. Which token-reduction levers are actually large in agentic coding sessions?

| Lever | Evidence | Expected priority |
|---|---|---|
| Cache stable prompt, tool, and history prefixes | Tools, system messages, messages, tool use, and tool results can be cached. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Highest |
| Load tools on demand | Anthropic recommends a small cached always-loaded tool set and tool discovery as needed. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching) | Highest |
| Programmatic tool calling | Anthropic reports typical 20–40% token savings for production requests with 10–49 tools. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) | High where applicable |
| Filter data before it reaches context | Anthropic’s example reduces a 10,000-row sheet to five displayed rows. [anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp) | High |
| Clear or summarize stale tool outputs | Anthropic identifies old raw tool calls/results as low-hanging superfluous context. [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | High, but preserve anchors |
| Use subagents for noisy, self-contained work | Claude Code isolates verbose subagent output, returning a summary; it also warns that many detailed subagent returns consume main-context space. [code.claude.com](https://code.claude.com/docs/en/sub-agents) | Medium |
| Shorten ordinary final prose | Output is expensive but is often a small share of an agent’s total trajectory | Medium; retain only the narrow policy |

(High Confidence) “Read width” is more important than prose style when tool results are large. Returning the five relevant records rather than 10,000 rows preserves the agent’s ability to reason while preventing context accumulation. [anthropic.com](https://www.anthropic.com/engineering/code-execution-with-mcp)

(Medium Confidence) Never summarize or strip text needed as a verbatim edit anchor, failing-test evidence, exact API contract, or error reproduction. A 2026 preprint reports compression reduced patch application from 27/40 to 15/40 in a small SWE-bench-derived Go study after corrupting such anchors. [arxiv.org](https://arxiv.org/abs/2607.12161)

### 6. What are the documented failure modes where style/persona instructions interfere with instruction-following, tool calling, and long-horizon performance?

(High Confidence) The clearest documented Claude Code failure mode is configuration-level: a custom output style can remove its built-in software-engineering instructions. A terse style built without `keep-coding-instructions: true` can therefore change much more than prose. [code.claude.com](https://code.claude.com/docs/en/output-styles)

(Medium Confidence) Persona prompting is not reliably capability-improving. A 2025 Wharton technical report found no expert or low-knowledge persona reliably improved GPQA performance for any tested model, while low-knowledge personas were generally harmful. This is benchmark evidence, but it is not a Claude Code coding evaluation. [gail.wharton.upenn.edu](https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/)

(Medium Confidence) Persona effects are task- and model-dependent rather than uniformly harmful: persona prompting can help tasks whose objective is simulation or style, so “never use a persona” is too broad outside engineering. [arxiv.org](https://arxiv.org/abs/2402.10811)

(High Confidence) No primary source located establishes that dropping articles specifically causes Claude Opus 5 tool-call syntax errors. <INSUFFICIENT_EVIDENCE>Claim not corroborated: a direct causal link from caveman grammar to Opus 5 tool-call failure. The appropriate conclusion is risk-based, supported by the operator’s task-success regression and absence of demonstrated token benefit—not a fabricated mechanistic claim.</INSUFFICIENT_EVIDENCE>

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| CCoT cut response length 48.70%; GPT‑3.5 math penalty 27.69% | Renze & Guven | 2024-01-11 | Research preprint; code/data linked by authors | https://arxiv.org/abs/2401.05618 |
| Chain-of-Draft can use as little as 7.6% of CoT tokens on evaluated tasks | Xu, Xie, Zhao & He | 2025-02-25 | Research preprint | https://arxiv.org/abs/2502.18600 |
| Opus 5 context, output limit, pricing, thinking default | Anthropic | 2026-07-24 | Official model documentation | https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8 |
| Cache reads cost 0.1× base input; cacheable request elements and exact-prefix requirements | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| Count tokens under the model-specific tokenizer; newer tokenizer differs materially | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/build-with-claude/token-counting |
| Output styles modify system prompt and can omit coding instructions | Anthropic | Living documentation, accessed 2026-08-09 | Official Claude Code documentation | https://code.claude.com/docs/en/output-styles |
| Tool search and programmatic calling reduce tool-context cost | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching |
| Production requests with 10–49 tools typically save 20–40% tokens with programmatic tool calling | Anthropic | Living documentation, accessed 2026-08-09 | Official API documentation | https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling |
| Filter tool data before returning it to model context | Anthropic | 2025-11-04 | Vendor engineering article; direct architecture example | https://www.anthropic.com/engineering/code-execution-with-mcp |
| Clear stale tool results and retain structured task memory | Anthropic | 2025-09-29 | Vendor engineering article; direct agent-context guidance | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| Expert personas do not reliably improve factual benchmark accuracy | Wharton Generative AI Labs | 2025-12-07 | Technical report / preprint summary | https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/ |
| Compression can remove action-critical anchors and reduce coding success | Weinberger & Hozez | 2026-07-13 | Research preprint; directly agentic-code relevant | https://arxiv.org/abs/2607.12161 |

## Knowledge Gaps

- **Direct causal evidence:** <MISSING_DATA>There is no public paired benchmark of caveman grammar versus normal concise English for Claude Opus 5 in Claude Code on SWE-bench-style tasks.</MISSING_DATA>

- **Tokenizer evidence:** <MISSING_DATA>No public Claude Opus 5 tokenizer breakdown was found for the exact old skill. Use Anthropic’s count endpoint on the real serialized prompts.</MISSING_DATA>

- **Claude Code billing attribution:** <MISSING_DATA>Without run-level `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`, tool-call counts, retries, and pass/fail records, it is not possible to state what share of your bill prose represents.</MISSING_DATA>

- **Long-horizon behavioural mechanism:** <INSUFFICIENT_EVIDENCE>The observed success decrease is real for the operator’s benchmark, but public evidence cannot yet distinguish whether it arose from impaired instruction-following, lower-quality plans, missed verification, changed tool use, or another interaction.</INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1. Run a three-arm paired benchmark: baseline, current caveman skill, and the replacement policy. Hold model, effort, repository, task order, tools, and permissions constant. Measure solved rate and dollars per solved task.

2. Add telemetry per run: output tokens, uncached input, cache-read input, cache writes, tool-result input, tool-call count, turns, wall time, compactions, and retries. The decision metric should be **success-adjusted billed cost**, not token reduction.

3. Use Anthropic’s token-count endpoint to compare the old and replacement instructions under `claude-opus-5`, including the actual tool definitions. This resolves the claimed 65% saving before further prompt iteration. [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/token-counting)

4. Prioritize context controls: tool-result filtering, dynamic tool loading, stable caching, and structured compaction. Test each independently before combining them.

5. Keep the replacement policy only if its lower confidence bound on task success is non-inferior to baseline and it reduces success-adjusted cost. Otherwise remove the global style entirely and use a per-task “brief final report” command.
