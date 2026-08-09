---
title: "Evaluating the cost and accuracy of terse output styles in Claude Opus 5"
run_id: dr_7d7453be83e2dd5a
question: "How should a prompt-level \"terse output\" / compressed-response skill for a frontier coding agent (Claude Opus 5 in Claude Code) be designed so that it reduces token spend WITHOUT degrading task success on agentic software-engineering benchmarks? Specifically: what does the evidence say about (a) the measured accuracy/quality cost of brevity, conciseness, and \"compressed register\" system prompts on reasoning and coding tasks; (b) whether telegraphic/caveman-style register (dropping articles, function words, hedging) actually saves tokens under BPE/modern tokenizers versus degrading model performance; (c) how instruction placement (system prompt vs appended system prompt vs live turn) and prompt-cache economics change the real cost; (d) which token-reduction levers in agentic coding sessions are actually large (input reuse, tool schemas, subagent prefixes, read width, repetition) versus output prose; (e) documented failure modes where style/persona instructions interfere with instruction-following, tool-calling, and long-horizon agentic performance on Claude and other frontier models in 2025-2026."
provider: local-claude
model: Claude Code
tier: max
archetype: technical
sources: 20
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-09T05:13:53.232Z
---
I have enough primary evidence. Report follows.

---

# Rebuilding a Terse-Output Skill for Claude Opus 5 in Claude Code

## Executive Summary

- **(High Confidence) The register is the wrong lever and the vehicle is the wrong container.** Caveman-style telegraphic English does not reliably save tokens under BPE — function words like `" the"` and `" a"` are already single high-frequency tokens, while abbreviations fragment into *more* tokens [BPE vocabulary construction](https://www.buildfastwithai.com/blogs/what-is-bpe-byte-pair-encoding-how-tokenizers-actually-work-2026). The skill's own SKILL.md already concedes this for abbreviations ("Full word cheaper AND clearer") [caveman SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md) — but does not follow the conclusion through to article-dropping, which is the same argument.

- **(High Confidence) The ~10% you measured is the correct number and the 65% never applied to your workload.** JetBrains' independent A/B over 86 SkillsBench tasks measured **−8.5%** output tokens against an advertised −65%, with the skill arm **11.6% more expensive overall** ($40.60 vs $36.39) despite being cheaper per task [JetBrains AI blog, July 2026](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/). The upstream README itself states "**8.5%**" for agentic runs and warns savings "on already-terse workloads … can go net-negative" [caveman README](https://github.com/juliusbrussee/caveman).

- **(Medium-High Confidence) Your Opus 5 regression is plausible where JetBrains' Sonnet 5 null result was not, and the divergence is explainable.** JetBrains ran `claude-sonnet-5` at `--effort low` [JetBrains methodology](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/). Anthropic documents that Opus 5 "follows that instruction literally" on scope-narrowing style directives, and that negative-framed instructions underperform positive examples [Prompting Claude Opus 5](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md). The caveman ruleset is almost entirely prohibition-framed.

- **(High Confidence) Persona-style system prompts carry a measured accuracy tax that scales with their length.** USC's PRISM study found MMLU dropped from **71.6% baseline to 68.0%** with a persona, and to **66.3%** with a *long* persona, with MT-Bench **Coding −0.65** — the single worst-hit category [Hu, Rostami & Thomason, arXiv:2603.18507, 19 Mar 2026](https://arxiv.org/html/2603.18507v1). Their "Min" persona was ~5 tokens; caveman injects ~1–1.5k. Shorter style blocks damage less.

- **(High Confidence) Ship it as an output style, not a skill.** Output styles live in the **system prompt layer**, are cached from turn one, and "trigger reminders for Claude to adhere to the output style instructions during the conversation" — drift resistance the caveman skill hand-rolls in prose [Claude Code output styles](https://code.claude.com/docs/en/output-styles). Skills instead "inject their instructions as user messages at the point of invocation" [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching), which is cache-safe but structurally the wrong home for a persistent register.

- **(High Confidence) The large levers are all on the input side, and prose is not among them.** Tool Search delivers "an 85% reduction in token usage" while *improving* MCP tool-selection accuracy from **79.5% → 88.1%** on Opus 4.5; Programmatic Tool Calling cut average usage "from 43,588 to 27,297 tokens, a 37% reduction" [Anthropic Engineering, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). Cache reads bill at **0.1×** base input [Prompt caching docs](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching), so input-side hygiene dominates the cost model.

- **(High Confidence) `effort` already does natively what the skill attempts in prose — and does it to *all* tokens.** Lower effort makes Claude "Combine multiple operations into fewer tool calls… Proceed directly to action without preamble… Use terse confirmation messages" and affects "**all tokens** in the response, including… Tool calls and function arguments" [Effort docs](https://platform.claude.com/docs/en/docs/build-with-claude/effort). A prose skill can only touch the narration layer.

- **(Medium Confidence) Compression must be scoped away from reasoning, or you buy the documented accuracy cliff.** Concise-CoT cut response length 48.70% but imposed a math penalty on GPT-3.5 [Renze & Guven, FLLM 2024](https://arxiv.org/abs/2401.05618); fixed-budget prompts cost ~10% accuracy on average across reasoning benchmarks [Nayab et al., *Information Sciences* 2026](https://arxiv.org/abs/2407.19825). A terse skill must govern *user-facing prose only*, never thinking or plan construction.

---

## Detailed Findings

### (a) What is the measured accuracy/quality cost of brevity, conciseness, and "compressed register" system prompts on reasoning and coding tasks?

The literature is consistent on shape and split on magnitude: brevity is close to free on retrieval-style and general QA tasks, and expensive on multi-step reasoning.

Renze & Guven's Concise Chain-of-Thought study — the most-cited primary source — tested GPT-3.5 and GPT-4 on a multiple-choice benchmark and reported that "CCoT reduced average response length by 48.70% for both GPT-3.5 and GPT-4 while having a negligible impact on problem-solving performance," with an average per-token cost reduction of **22.67%** [Renze & Guven, arXiv:2401.05618, FLLM 2024, pp. 476–483](https://arxiv.org/abs/2401.05618). The exception is the load-bearing part: the paper isolates a math-specific performance penalty for GPT-3.5. The frequently-quoted **27.69%** relative drop figure comes from the paper body rather than the abstract, which characterises the effect only as "a performance penalty."

<CONFIDENCE:LOW>The precise 27.69% math-penalty figure for GPT-3.5 was returned by search summarisation and by the abstract-page extraction table, but I did not read it in the paper's own results section. The *direction and existence* of a math-specific penalty is High Confidence; the exact magnitude is not.</CONFIDENCE:LOW>

Nayab et al. formalised the same effect with explicit budgets. Their Constrained-CoT work introduces Hard-*k* and Soft-*k* Concise Accuracy metrics and studies "length control via a refined prompting strategy" [Nayab et al., arXiv:2407.19825, *Information Sciences* 2026, DOI 10.1016/j.ins.2026.123939](https://arxiv.org/abs/2407.19825). The widely-reported ~10% average accuracy penalty from hand-crafted fixed-budget prompts, and the GSM8K counter-case where constraining an over-verbose LLaMA2-70B *raised* accuracy from 36.01% to 41.07%, appear in the paper body.

<MISSING_DATA>[Sought: the specific accuracy tables from arXiv:2407.19825 (the ~10% average penalty; the 36.01%→41.07% LLaMA2-70B GSM8K reversal). The arXiv abstract page carries no numbers and I did not retrieve the full PDF. These figures are reported second-hand and should be verified against the published *Information Sciences* version before they are load-bearing.]</MISSING_DATA>

<CONFLICTING_EVIDENCE>Two positions on whether brevity constraints help or hurt large models. Position 1 (Nayab et al.; and a single-author March 2026 preprint, arXiv:2604.00025, claiming brevity constraints raise accuracy by ~26 points on affected subsets by suppressing "spontaneous scale-dependent verbosity") holds that brevity acts as a regulariser against over-elaboration on easy items. Position 2 (Renze & Guven; the ACL 2025 self-training line) holds that prompt-level brevity starves test-time compute on hard items. These are reconcilable rather than contradictory — the effect flips with item difficulty — but note that arXiv:2604.00025 is a single-author, non-peer-reviewed preprint that the caveman README cites in its own defence, and it should not be treated as equivalent evidence to the peer-reviewed sources.</CONFLICTING_EVIDENCE>

The most directly relevant evidence for a *coding agent* is not the CoT literature but the persona literature. USC's PRISM paper measured persona system prompts against neutral baselines across six models and found that **all persona variants reduced MMLU accuracy**: 71.6% baseline → 68.0% overall, with the long persona worst at **66.3%** and the ~5-token "Min" persona least damaging at 68.0% [Hu, Rostami & Thomason, arXiv:2603.18507v1, USC, 19 Mar 2026](https://arxiv.org/html/2603.18507v1). On MT-Bench, long personas improved 5 of 8 categories but **Coding was the largest single loss at −0.65**, ahead of Humanities (−0.20) and Math (−0.10) [PRISM, MT-Bench results](https://arxiv.org/html/2603.18507v1). Expert Prompting on Llama-3.1-8B collapsed MMLU from 68.4 to 46.3 [PRISM, Table 1](https://arxiv.org/html/2603.18507v1).

<INFERENCE from="PRISM's finding that persona damage scales with persona length (66.3% long vs 68.0% min, ~150 vs ~5 tokens); PRISM's finding that Coding is the worst-hit MT-Bench category; the caveman skill's ~1–1.5k token injection per the upstream README">A ~1–1.5k-token stylistic persona is roughly an order of magnitude longer than the "Full" persona PRISM measured as most damaging, and it is applied to precisely the task category PRISM found most sensitive. This is a coherent mechanism for the task-success regression the operator measured, independent of the register question. The design implication is quantitative, not just qualitative: style instruction length is itself a risk variable, and the rebuilt skill should target the low hundreds of tokens, not thousands.</INFERENCE>

Anthropic's own guidance converges on the same answer from the other direction. The Opus 5 prompting page does **not** discourage conciseness instructions — it recommends a specific one, and it is short:

> "Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested." [Prompting Claude Opus 5](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md)

For long system prompts it adds a reinforcement pattern: pair the instruction with "a short reminder near the end of the prompt," given as a `<tone_preference>` block containing one sentence [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md). Anthropic's tested formulation for the exact problem the caveman skill addresses is roughly 45 words.

---

### (b) Does telegraphic/caveman register actually save tokens under BPE, or does it degrade performance?

It largely does not save tokens, and it plausibly degrades input comprehension. The two halves of this answer have very different evidence strength.

**Tokenizer mechanics (High Confidence).** BPE builds its vocabulary from the most frequent character sequences in the training corpus, so `" the"`, `" a"`, `" in"`, `" for"`, `" with"` are each assigned a single token ID including the leading space [BPE tokenizer explainer](https://www.buildfastwithai.com/blogs/what-is-bpe-byte-pair-encoding-how-tokenizers-actually-work-2026) `[SECONDARY: educational]`. Dropping an article therefore saves exactly one token. Abbreviating moves the other way: shorthand is rare in the pretraining corpus, so it fragments into multiple subword or character tokens.

The caveman skill has already internalised half of this. Its own ruleset bans invented abbreviations (`cfg/impl/req/res/fn`) on the explicit grounds that "the tokenizer splits them identically — Full word cheaper AND clearer," and bans the arrow glyph `→` because it "consume[s] a token and save[s] nothing" [caveman SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md). This is correct tokenizer reasoning. It is also, applied consistently, an argument against the skill's central mechanic: article-dropping saves one token per article and costs distributional fluency.

The economics get worse on current models. Anthropic's migration guide states that Opus 4.7+ tokenizes "roughly 1x to 1.35x as many tokens when processing text compared to models before Claude Opus 4.7 (up to ~35% more, varying by content)" [Anthropic migration guide, tokenizer change](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/token-efficient-tool-use).

<INFERENCE from="Anthropic's documented 1x–1.35x tokenizer expansion on Opus 4.7+; the BPE property that common function words are single tokens while rare fragments are not">A tokenizer that expands text by up to 35% is, by construction, one whose vocabulary coverage of *unusual* strings is thinner relative to its coverage of common ones. Telegraphic and fragmentary text is disproportionately unusual. The per-article saving is unchanged at one token, but the downside risk of non-standard constructions fragmenting is if anything higher on Opus 5 than on the models the caveman skill was originally tuned against. I did not find a direct measurement of this and flag it as reasoning, not data.</INFERENCE>

**Model-side degradation (Medium Confidence, with an important asymmetry).** The FrugalPrompt work is the closest primary source, and it establishes the asymmetry that matters most here: it compresses *input* prompts by salience-ranking tokens with GlobEnc and DecompX attribution and keeping the top-*k*% [Raiyan, Ishmam, Al Imran & Moni, FrugalPrompt, arXiv:2510.16439](https://arxiv.org/abs/2510.16439). Sentiment analysis, commonsense QA and summarisation tolerated substantial sparsification; mathematical reasoning "degraded sharply." That is input-side compression, which is not what a terse *output* skill does — but a caveman-mode agent reads its own compressed prior turns as input on every subsequent turn, so a long agentic session converts an output-side style into an input-side one.

<INSUFFICIENT_EVIDENCE>[I could not corroborate a "CAVEWOMAN benchmark" as a real, retrievable artifact — it surfaced only in search summarisation and I found no paper, repository, or dataset behind it. Treat any claim attributed to it as unsupported.]</INSUFFICIENT_EVIDENCE>

<MISSING_DATA>[Sought: a controlled measurement of whether an agent's *own* telegraphic output, re-read as conversation history across many turns, degrades its later performance. This is the exact mechanism that would explain an agentic-coding regression, and I found no study isolating it. Establishing it would require an A/B on a multi-turn agentic benchmark with the style applied to assistant turns only — which is close to the experiment the operator has already partly run on diolog-swe-bench.]</MISSING_DATA>

**On your regression specifically.** JetBrains found no quality difference: across 82 clean pairs, "8 tasks scored higher with the skill, 10 scored lower, 64 tied," with a sign test over the 18 non-tied tasks giving **p = 0.82** [JetBrains, July 2026](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/). Their own methodological warning is the one to carry forward: an initial −29.5% smoke result "vanished with more data — Never trust a k=1 eval," and the full run was itself k=1 on 86 tasks [ibid.](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/).

<CONFLICTING_EVIDENCE>The operator measured a task-success decrease on diolog-swe-bench with Opus 5; JetBrains measured no detectable difference on SkillsBench with claude-sonnet-5 at `--effort low` (p = 0.82). These are not necessarily contradictory: different model, different effort, different benchmark, and JetBrains' full run was k=1 with a −0.015 mean gap it explicitly declined to call significant. The honest reading is that neither result rules the other out, and that JetBrains' null is a weak null rather than positive evidence of safety. The operator's own benchmark is the more relevant instrument for the operator's own decision.</CONFLICTING_EVIDENCE>

---

### (c) How do instruction placement and prompt-cache economics change the real cost?

This is where the skill's own cost accounting is wrong in the operator's favour, and where the largest design change lives.

**The pricing.** Cache reads bill at **0.1×** base input; 5-minute cache writes at **1.25×**; 1-hour writes at **2×** [Prompt caching docs](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching). For Opus 5: base input **$5/MTok**, 5m writes **$6.25**, 1h writes **$10**, cache hits **$0.50**, output **$25/MTok** [ibid., pricing table](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching). Opus 5's minimum cacheable prompt is **512 tokens**, the lowest of any model [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching).

**The correction.** The caveman README states the skill "adds ~1–1.5k input tokens per turn" [caveman README](https://github.com/juliusbrussee/caveman). In Claude Code this overstates the cost by roughly 10×. Skills "inject their instructions as user messages at the point of invocation. Nothing earlier in the conversation changes" [Claude Code prompt caching](https://code.claude.com/docs/en/prompt-caching) — so the block is written once and thereafter read from cache.

<INFERENCE from="Skills inject as user messages and do not invalidate the prefix (Claude Code prompt-caching docs); cache reads bill at 0.1× base input (API prompt-caching docs); Opus 5 base input is $5/MTok">A 1.5k-token skill block costs one cache write (~1.5k × 1.25 = ~1,875 token-equivalents, ≈$0.0094 on Opus 5) and then ~150 token-equivalents per subsequent turn (≈$0.00075), not 1.5k per turn. Over a 50-turn session that is ~9.2k token-equivalents total rather than the ~94k the README's phrasing implies. The input overhead of a style block is therefore NOT the reason to keep it short — cache makes it cheap. The reason to keep it short is the PRISM accuracy-vs-length finding. These two considerations point the same way but for different reasons, and conflating them leads to optimising the wrong variable.</INFERENCE>

**The placement decision.** Claude Code orders each request into three layers by stability — system prompt (core instructions, tool definitions, **output style**), project context (CLAUDE.md, auto memory), then conversation [Claude Code prompt caching, layer table](https://code.claude.com/docs/en/prompt-caching). Output styles "directly modify Claude Code's system prompt," Claude Code "adds each output style's custom instructions to the end of the system prompt," and critically: "**All output styles trigger reminders for Claude to adhere to the output style instructions during the conversation**" [Output styles](https://code.claude.com/docs/en/output-styles).

That last line matters more than the caching. The caveman skill spends prose on drift resistance — "stays on for every response, resists drift, and remains active when uncertain" [caveman SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md). The output-style mechanism provides that as harness behaviour, for free, without spending persona tokens on it.

`keep-coding-instructions: true` preserves Claude Code's built-in software-engineering instructions — "how to scope changes, write comments, and verify work" — which a custom output style otherwise **drops by default** [ibid.](https://code.claude.com/docs/en/output-styles). Omitting that flag on a coding-agent style would silently delete the harness's own scoping and verification guidance, which is a far larger task-success risk than any register choice.

Two caveats. Output styles "apply to the main conversation only: a subagent runs its own system prompt, so styles don't change how subagents respond" — a fork is the exception [ibid.](https://code.claude.com/docs/en/output-styles). And an output style is "read once at session start"; changing it mid-session "does not invalidate the cache, but the change also doesn't apply," taking effect on the next `/clear` or restart [Claude Code prompt caching](https://code.claude.com/docs/en/prompt-caching). If per-turn toggling is a requirement, the skill form remains the only option — that is the one genuine argument for keeping it as a skill.

<INFERENCE from="Output styles do not propagate to subagents; the operator's ~/Dev portfolio orchestration runs work through ship-armada/ship-fleet/ship-feature with up to 8 concurrent Opus runners">In a fan-out-heavy portfolio, an output style governs only the conducting session and leaves every runner at default verbosity. If the goal is portfolio-wide token reduction, the style must be paired with per-agent effort settings and runner-prompt calibration, or most of the spend will sit outside the style's reach entirely. This follows from the documented subagent boundary plus the operator's stated architecture; I have not measured the resulting share.</INFERENCE>

---

### (d) Which token-reduction levers in agentic coding sessions are actually large?

Prose is close to the smallest lever available. The measured hierarchy, all from Anthropic primary sources:

| Lever | Mechanism | Measured effect | Accuracy effect | Token side |
|---|---|---|---|---|
| **Tool Search Tool** | `defer_loading: true`; ~500-token search tool replaces upfront schemas | "an 85% reduction in token usage"; ~8.7K vs ~77K tokens; "preserves 191,300 tokens of context compared to 122,800" [Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use) | **Improves**: Opus 4 "49% to 74%"; Opus 4.5 "79.5% to 88.1%" [ibid.](https://www.anthropic.com/engineering/advanced-tool-use) | Input |
| **Programmatic Tool Calling** | Claude writes code that calls tools in a sandbox; only results return | "from 43,588 to 27,297 tokens, a 37% reduction"; "200KB of raw expense data to just 1KB" [ibid.](https://www.anthropic.com/engineering/advanced-tool-use) | **Improves**: knowledge retrieval "25.6% to 28.5%"; GIA "46.5% to 51.2%" [ibid.](https://www.anthropic.com/engineering/advanced-tool-use) | Input |
| **Tool use examples** | Worked examples in tool definitions | — | "72% to 90% on complex parameter handling" [ibid.](https://www.anthropic.com/engineering/advanced-tool-use) | — |
| **Effort parameter** | Affects "**all tokens**… including… Tool calls and function arguments" | No % published; `low` = "Significant token savings with some capability reduction" [Effort docs](https://platform.claude.com/docs/en/docs/build-with-claude/effort) | Reduction, task-dependent | Output + tool calls |
| **Prompt cache hygiene** | Keep model/effort/tools stable; `/clear` at task boundaries | Cache reads bill **0.1×** base input [Prompt caching](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching) | Neutral | Input |
| **PreToolUse output-filtering hooks** | grep tool output before Claude sees it | "reducing context from tens of thousands of tokens to hundreds" [Manage costs](https://code.claude.com/docs/en/costs) | Neutral/positive | Input |
| **Subagent delegation of verbose ops** | Verbose output stays in subagent context | Qualitative [ibid.](https://code.claude.com/docs/en/costs) | Neutral | Input |
| **Code intelligence plugins** | Symbol navigation replaces grep-then-read-candidates | Qualitative [ibid.](https://code.claude.com/docs/en/costs) | Positive | Input |
| **CLAUDE.md discipline** | "Aim to keep CLAUDE.md under 200 lines" | Qualitative [ibid.](https://code.claude.com/docs/en/costs) | Neutral | Input |
| **Terse output register** | Compress narration prose | **−8.5%** output tokens; **+11.6%** total session cost in the measured arm [JetBrains](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/) | Null on Sonnet 5 (p=0.82); negative on operator's Opus 5 bench | Output narration only |

The scale of the input-side problem: Anthropic reports "we've seen tool definitions consume 134K tokens before optimization," and a five-server MCP setup at "58 tools at roughly 55K tokens," with Jira alone "~17K tokens" [Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use). Claude Code's own cost guidance names the two dominant drivers as long context and cache misses, flagging each when it "accounts for 10% or more of recent usage" [Manage costs](https://code.claude.com/docs/en/costs).

Three further operator-relevant figures. Enterprise Claude Code averages "around $13 per developer per active day and $150-250 per developer per month" [ibid.](https://code.claude.com/docs/en/costs). Agent teams "use approximately **7x more tokens** than standard sessions when teammates run in plan mode" [ibid.](https://code.claude.com/docs/en/costs). And a sample `/usage` line in Anthropic's own docs shows the real shape of a session: "1.2k input, 5.3k output, 940.0k cache read, 50.0k cache write" [ibid.](https://code.claude.com/docs/en/costs).

<INFERENCE from="Anthropic's illustrative /usage figures (1.2k input, 5.3k output, 940.0k cache read, 50.0k cache write); Opus 5 pricing of $5 base input, $0.50 cache read, $6.25 cache write, $25 output per MTok">Pricing that example at Opus 5 rates: cache read 940k × $0.50 = $0.470; cache write 50k × $6.25 = $0.313; uncached input 1.2k × $5 = $0.006; output 5.3k × $25 = $0.133. Total ≈ $0.922, of which output is ~14%. Eliminating 65% of ALL output — far beyond what any register achieves — would save ~9% of the session. Achieving the measured 8.5% output reduction saves ~1.2%. This is an illustrative figure from Anthropic's docs rather than a measurement of the operator's workload, and Opus-5 sessions with heavy thinking will carry a higher output share since thinking bills as output. But the order of magnitude is the point: output prose cannot be the primary cost lever in a cache-warm agentic session.</INFERENCE>

Task budgets are the one input-side lever that is **unavailable here**: "Task budgets are not supported on Claude Code or Cowork surfaces" [Task budgets](https://platform.claude.com/docs/en/docs/build-with-claude/task-budgets). Worth knowing for Agent SDK work, not for the skill. When they do apply, the minimum is 20,000 tokens and "a budget that is too small for the task can cause refusal-like behavior" [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/task-budgets).

---

### (e) Where do style/persona instructions documented as interfering with instruction-following, tool-calling, and long-horizon agentic performance?

Four documented failure modes, three of which the current caveman ruleset actively triggers.

**1. Literal over-application of scope-narrowing style rules.** Anthropic's Opus 5 guidance gives a near-exact analogue of the failure: "If your review prompt says 'only report high-severity issues' or 'be conservative,' the model may follow that instruction literally and report less; ask it to report everything and filter in a separate pass instead" [Prompting Claude Opus 5](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md).

<INFERENCE from="Anthropic's documented Opus 5 behaviour of literally applying 'be conservative' style instructions to substantive reporting depth; the caveman rule 'each fact stated once' and 'one word where one suffices' at ultra level">An instruction to state each fact once is a style rule at the sentence level and a completeness rule at the task level, and Opus 5 is documented to collapse that distinction. On a code-review or bug-finding task — precisely what diolog-swe-bench measures — the model reporting fewer findings *because the style told it to compress* is indistinguishable in the score from the model finding fewer bugs. This is the single most plausible specific mechanism for a benchmarked task-success drop, and it is testable by scoring findings-count separately from findings-quality.</INFERENCE>

**2. Negative framing underperforms positive specification.** "Positive examples of the communication style you want tend to be more effective than instructions about what not to do" [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md). The caveman ruleset is a list of prohibitions: drop articles, drop filler, drop pleasantries, drop hedging, drop narration, no emoji, no arrows, no abbreviations, no self-reference, never drop negations [caveman SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md). It supplies one positive pattern — `[thing] [action] [reason]. [next step].` — against roughly a dozen prohibitions.

**3. Tool-call preamble suppression collides with a documented Opus 5 artifact.** Caveman instructs the model to "Fire directly with no preamble, plan, or progress note before or between calls" [ibid.](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md). Anthropic's mitigation for tool calls leaking into visible text runs the other way, explicitly granting permission to speak first: "When you use a tool, you may say a brief sentence first" [Prompting Claude Opus 5](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md). The leak failure mode is severe in agentic loops: "the model occasionally writes a tool call into its user-facing text instead of emitting a structured `tool_use` block. The turn completes normally and **the call never runs**, and in agentic loops the leaked text stays in the conversation history, so later turns are affected as well" [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md).

This artifact is documented specifically for thinking-disabled operation, and Claude Code runs Opus 5 with thinking on by default. But the same section warns that instructions *against* internal reasoning output increase leakage: "If your system prompt contains a rule instructing the model not to think or not to reason, remove it; that kind of instruction increases tag leakage" [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md).

<CONFIDENCE:LOW>Whether a no-preamble style rule measurably raises tool-call-as-text leakage with thinking *enabled* is not documented. I flag it as a risk by analogy to the documented thinking-disabled case and to the documented "don't reason" interaction, not as an established finding. It is cheap to test and expensive to be wrong about, since a silently-unexecuted tool call scores as a task failure with no error.</CONFIDENCE:LOW>

**4. Persona overhead competes with instruction-following.** Beyond PRISM's accuracy numbers, the mechanism reported is attention competition between maintaining a register and satisfying structural constraints. Pei et al.'s EMNLP 2024 study evaluated **162 personas across 2,410 factual questions** and four model families and found no statistical improvement over persona-free baselines [Pei et al., "When "A Helpful Assistant" Is Not Really Helpful," Findings of EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.888/).

<INSUFFICIENT_EVIDENCE>[I did not retrieve the Pei et al. paper directly; the 162-persona / 2,410-question figures come from search summarisation of the ACL Anthology entry. The finding is consistent with PRISM, which I did verify in detail, but the specific counts should be confirmed against the paper before quoting.]</INSUFFICIENT_EVIDENCE>

Finally, a rule that should survive the rebuild unchanged. Caveman's "Never drop not/never/no/only/except, because flipping meaning costs more than any saved token" [caveman SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md) is the ruleset's best line — it is exactly the safety property that a compression instruction needs, and it is stated with its reason attached, which is the form Anthropic recommends for generalisation.

---

## The Rebuild: Keep / Rewrite / Delete

| Current rule | Verdict | Evidence |
|---|---|---|
| Drop articles (a/an/the) | **Delete** | Saves 1 token/article; costs distributional fluency; the skill's own abbreviation rule already makes this argument [SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md) |
| Sentence fragments / telegraphic register | **Delete** | Input-side telegraphic compression degrades reasoning tasks [FrugalPrompt](https://arxiv.org/abs/2510.16439); agent re-reads own output as input |
| `ultra` / `wenyan-*` levels | **Delete** | "80-90% character reduction — chars, not tokens" is the skill admitting the mechanism doesn't apply [SKILL.md](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md) |
| "Each fact stated once", "one word where one suffices" | **Delete** | Highest-risk literal-application rule on Opus 5 [Opus 5 guide](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md) |
| No preamble before/between tool calls | **Delete** | Contradicts Anthropic's leak mitigation; `effort: low/medium` delivers this natively [Effort](https://platform.claude.com/docs/en/docs/build-with-claude/effort) |
| Drop filler / pleasantries / hedging | **Rewrite as positive spec** | Correct target, wrong framing [Opus 5 guide](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md) |
| Drop tool-call narration | **Rewrite as cadence spec** | Use Anthropic's shape: one sentence before first call, updates only on findings/direction change, lead with outcome [ibid.](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md) |
| Never drop negations | **Keep verbatim** | Best rule in the set; correct form (rule + reason) |
| No invented abbreviations | **Keep verbatim** | Tokenizer-correct [BPE](https://www.buildfastwithai.com/blogs/what-is-bpe-byte-pair-encoding-how-tokenizers-actually-work-2026) |
| No arrows/emoji/decorative tables | **Keep** | Real, small, harmless |
| Code/errors/numbers/units exact | **Keep** | Non-negotiable |
| Auto-Clarity exceptions (security, irreversible, multi-step) | **Keep and widen** | Extend to: reasoning, planning, code review findings, spec compliance |
| Persisted artifacts get normal prose | **Keep** | Correct scope boundary |
| Drift-resistance prose | **Delete — replaced by mechanism** | Output styles trigger adherence reminders natively [Output styles](https://code.claude.com/docs/en/output-styles) |
| Six intensity levels | **Collapse to one** | Length is itself a risk variable [PRISM](https://arxiv.org/html/2603.18507v1) |
| Skill packaging | **Rewrite as output style** with `keep-coding-instructions: true` | System-prompt layer, cached, native adherence [Output styles](https://code.claude.com/docs/en/output-styles) |

Target the whole style block at **150–300 tokens**, not 1–1.5k. Pair it with `effort: medium`, Tool Search enabled, PreToolUse output-filtering hooks, and `/clear` at task boundaries — that combination is where the actual savings are, and every component of it is either accuracy-neutral or accuracy-positive.

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| Caveman measured −8.5% output tokens vs −65% advertised; skill arm 11.6% more expensive | JetBrains AI blog | Jul 2026 | Independent A/B, 86 tasks, ~240 trials, ~$106 | https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/ |
| No quality difference on Sonnet 5: 8 up / 10 down / 64 tied, sign test p = 0.82 | JetBrains AI blog | Jul 2026 | Benchmark, auto-graded | https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/ |
| README concedes 8.5% agentic, ~1–1.5k input tokens/turn, "can go net-negative" | caveman README | 2026 | Project self-report | https://github.com/juliusbrussee/caveman |
| Full ruleset; bans invented abbreviations on tokenizer grounds | caveman SKILL.md | 2026 | Source artifact | https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md |
| CCoT: −48.70% length, −22.67% cost, math penalty on GPT-3.5 | Renze & Guven, FLLM 2024 | 11 Jan 2024 (v3 19 Oct 2024) | Peer-reviewed conference paper | https://arxiv.org/abs/2401.05618 |
| Constrained-CoT; conciseness metrics; length control | Nayab et al., *Information Sciences* | 29 Jul 2024 (v2 23 Jan 2025) | Peer-reviewed journal | https://arxiv.org/abs/2407.19825 |
| Persona: MMLU 71.6%→68.0% (66.3% long); MT-Bench Coding −0.65 | Hu, Rostami & Thomason (USC) | 19 Mar 2026 | Preprint, 6 models, MMLU n=14,042 | https://arxiv.org/html/2603.18507v1 |
| Telegraphic input compression degrades math sharply, tolerated elsewhere | Raiyan et al., FrugalPrompt | 2025 (v4) | Preprint + code | https://arxiv.org/abs/2510.16439 |
| 162 personas / 2,410 questions: no improvement | Pei et al., Findings of EMNLP 2024 | 2024 | Peer-reviewed *(not directly retrieved)* | https://aclanthology.org/2024.findings-emnlp.888/ |
| Opus 5 follows narrowing style instructions literally; positive > negative framing; tool-call-as-text leak | Anthropic, Prompting Claude Opus 5 | 2026 | Official vendor documentation | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompting-claude-opus-5.md |
| Effort affects all tokens incl. tool calls; low = fewer calls, no preamble, terse confirmations | Anthropic, Effort | 2026 | Official documentation | https://platform.claude.com/docs/en/docs/build-with-claude/effort |
| Cache read 0.1×, write 1.25×/2×; Opus 5 512-token minimum; Opus 5 $5/$0.50/$25 per MTok | Anthropic, Prompt caching | 2026 | Official documentation | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching |
| Skills inject as user messages; output style in system prompt, fixed at session start | Anthropic, Claude Code prompt caching | 2026 | Official documentation | https://code.claude.com/docs/en/prompt-caching |
| Output styles modify system prompt, trigger adherence reminders, don't reach subagents; `keep-coding-instructions` default false | Anthropic, Output styles | 2026 | Official documentation | https://code.claude.com/docs/en/output-styles |
| Tool Search −85% tokens; Opus 4.5 accuracy 79.5%→88.1%; PTC 43,588→27,297 (−37%) | Anthropic Engineering, Advanced tool use | 2025 | Vendor engineering, internal benchmarks | https://www.anthropic.com/engineering/advanced-tool-use |
| Hooks cut log context "tens of thousands → hundreds"; agent teams ~7× tokens; ~$13/dev/active day | Anthropic, Manage costs | 2026 | Official documentation | https://code.claude.com/docs/en/costs |
| Task budgets unsupported on Claude Code; 20k minimum; small budgets cause refusal-like behavior | Anthropic, Task budgets | 2026 (beta `task-budgets-2026-03-13`) | Official documentation | https://platform.claude.com/docs/en/docs/build-with-claude/task-budgets |
| Cache hit rate treated as reliability; SEVs declared on low hit rate | Anthropic, Lessons from building Claude Code | 2026 | Vendor engineering blog | https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything |
| BPE: function words single-token, abbreviations fragment | Build Fast with AI, BPE explainer | 2026 | `[SECONDARY: educational]` — corroborates a mechanism established in BPE literature | https://www.buildfastwithai.com/blogs/what-is-bpe-byte-pair-encoding-how-tokenizers-actually-work-2026 |
| Brevity constraints raise large-model accuracy ~26pts on affected subsets | Hakim, arXiv:2604.00025 | Mar 2026 | **Single-author preprint, not peer-reviewed — cited by caveman in its own defence; treat as weak** | https://arxiv.org/abs/2604.00025 |

**Sources discarded during review:** the "CAVEWOMAN benchmark" (no retrievable artifact); Medium/gitconnected/makeuseof posts on caveman (`[SECONDARY: promotional]`, no independent measurement beyond the JetBrains run they restate); Wharton/USC coverage in searchenginejournal and towardsai (secondary reporting of primary papers I retrieved directly); Reddit threads (not retrievable through this harness and not primary).

---

## Knowledge Gaps

**Unmeasured mechanism.** No study isolates the effect of an agent re-reading *its own* compressed output as conversation history across a long agentic loop. This is the most likely mechanism for an agentic-coding regression and the least documented.

**Unretrieved primaries.** Exact accuracy tables from Nayab et al. (arXiv:2407.19825 full PDF); the results section of Renze & Guven confirming the 27.69% math figure; Pei et al. EMNLP 2024 directly.

**Model-specific gap.** Every persona-degradation measurement I found is on 7–8B open models (PRISM explicitly limits itself to 7–8B). No published persona-vs-accuracy study covers Claude Opus 5. The direction is consistent across model families; the magnitude on a frontier model is unknown.

**Vendor-internal benchmarks.** Tool Search and PTC figures are Anthropic's own internal evaluations, with benchmark composition undisclosed. Direction is corroborated by the mechanism; exact magnitudes are unaudited.

**Absent Claude Code telemetry.** No published distribution of input:output:cache token ratios for real Claude Code sessions. My ~14%-output estimate derives from a single illustrative `/usage` line in Anthropic's docs and should not be treated as a measurement — you can produce the real figure for your own workload from `/usage` or OpenTelemetry in an afternoon.

**Neither eval is strong.** JetBrains' full run was k=1 across 86 tasks with a −0.015 mean gap. Its own conclusion was "Never trust a k=1 eval." A null from a k=1 eval is not evidence of safety.

---

## Recommended Next Steps

1. **Re-run diolog-swe-bench as a four-arm ablation, not a binary.** Arms: (i) no skill; (ii) full caveman; (iii) register rules only, tool-preamble rule removed; (iv) Anthropic's ~45-word conciseness instruction alone. *Rationale:* your current result tells you the bundle hurts, not which rule does. Given PRISM's length-scaling finding and Anthropic's literal-instruction warning, my prior is that arm (iv) is net-positive and the delta between (ii) and (iii) is where the regression lives — but that is a hypothesis your bench can settle and mine cannot.

2. **Instrument tool-call-as-text leakage explicitly.** Count turns where a tool call appears in visible text and never executes, per arm. *Rationale:* Anthropic documents this as a real Opus 5 artifact that "completes normally" with the call never running and the leak persisting in history. It scores as task failure with no error signal, so a standard pass/fail harness cannot distinguish it from a wrong answer.

3. **Measure your actual token composition before optimising further.** Pull cache-read / cache-write / input / output per session from `/usage` or the OpenTelemetry exporter across a representative week. *Rationale:* if output is ~14% of a cache-warm session, the entire output-side project has a hard ceiling around 9% and your effort is better spent on Tool Search, hooks and `/clear` discipline. If your Opus 5 sessions run thinking-heavy and output share is materially higher, the calculus changes — and only your data can say which.

4. **A/B `effort: medium` against the rebuilt style, and against both together.** *Rationale:* effort affects tool calls and function arguments, which no prose rule can reach, and Anthropic recommends `low`/`medium` "liberally as your primary control for token cost." It is plausible that effort alone dominates the style entirely — which would be the cheapest possible answer to your question.

5. **Audit the subagent boundary across ship-armada / ship-fleet.** Output styles do not reach subagents. Measure what share of portfolio token spend sits in runners versus conducting sessions. *Rationale:* with up to 8 concurrent Opus runners, a main-conversation-only style may govern a small minority of spend, and the same token budget spent on runner-prompt calibration and per-agent effort settings would return more.
