# Decisive Timing for Context Compaction in Long-Horizon LLM Agents

## Executive Summary

*   **(High Confidence)** The timing of context compaction is critical to agent stability. Current frontier harnesses (Claude Code, Cursor) predominantly rely on reactive token-pressure thresholds (e.g., 80% to 95% of the context window), which frequently interrupt agents mid-tool-chain, destroying critical partial state and causing severe "context rot."
*   **(High Confidence)** Compacting context at a semantic task boundary rather than mid-task preserves architectural coherence. Frameworks such as SWE-agent and the CAT (Context As Tool) paradigm demonstrate that shifting from passively triggered compression to proactive compression at "appropriate milestones" significantly improves long-horizon task completion rates.
*   **(Medium Confidence)** Small, efficient models (e.g., Claude 3.5 Haiku, GPT-5.6-low) can reliably classify session state stability to generate a `should-compact` signal (0–10 score) when guided by strict evaluation frameworks. This requires explicit step-by-step deduction prior to generating a constrained JSON output, utilizing numerical anchor rubrics.
*   **(High Confidence)** Incremental, append-only summarization (rolling summaries) suffers from measurable memory entropy over successive turns. Benchmarks like SUMIE and BooookScore confirm that recursively summarizing a summary degrades factuality (with F1 scores dropping below 80.4%), necessitating hybrid architectures that separate immutable fact stores from lossy narrative buffers.
*   **(High Confidence)** Programmatic veto mechanisms exist to gate automatic compaction. Claude Code provides a deterministic `PreCompact` hook; an external classifier script can intercept the trigger and force an `exit 2` blocking error or a `decision: block` JSON payload if the agent is in an unresolved state, effectively halting compaction until a task boundary is reached.
*   **(Medium Confidence)** The financial and latency costs of compacting at an inopportune moment manifest in input-token volume spikes. Agents that lose their immediate working memory mid-edit are forced to re-explore the environment and re-read massive files, exacerbating the input-token dominance problem where input volume accounts for roughly 70% of total inference expenditure.

## Primary: 1. Answer this decisively: When should an LLM agent session compact its context — how is the TIMING decision made, as distinct from how a good summary is written?

The decision of *when* to summarize and prune a conversation history is an architectural control problem distinct from the natural language challenge of crafting the summary itself. As LLM agents transition from short-lived assistants to long-horizon autonomous operators, the timing of context truncation dictates operational stability.

### (1) Signals Used by Agent Harnesses to Trigger Compaction

The software engineering ecosystem currently exhibits a stark dichotomy between reactive, token-based heuristics and emerging proactive, task-based milestone detection.

**Reactive Token-Threshold Triggers**
The vast majority of commercial coding agents and command-line interfaces (CLIs) utilize reactive token-pressure limits. 
*   **Claude Code:** This harness implements an automatic compaction pass that triggers when the session reaches approximately 80% to 95% of the total context window (roughly 160,000 to 190,000 tokens for a 200K model) [cite: 1](https://institute.sfeir.com/en/claude-code/claude-code-context-management/deep-dive/), [cite: 2](https://institute.sfeir.com/en/claude-code/claude-code-context-management/cheatsheet/). The system automatically identifies the oldest messages, generates a structured summary, and replaces the history to free up space. Claude Code also supports a user-defined `--autocompact` window between 100K and 1M tokens [cite: 3](https://code.claude.com/docs/en/context-window).
*   **Cursor IDE:** The IDE relies on strict token budgets per request. The default chat cap is approximately 20,000 tokens, with Cmd-K focused operations limited to roughly 10,000 tokens [cite: 4](https://forum.cursor.com/t/context-window-must-know-if-you-dont-know/86786/2). When the conversation exceeds these bounds, Cursor prunes context unpredictably or truncates the history. Optimization guidelines strongly recommend reducing `cursor.contextLength` from 8,000 to 4,000 and heavily relying on manual focused selection to avoid mid-task truncation [cite: 5](https://saaswithalex.pages.dev/posts/reducing-cursor-token-usage).
*   **Aider:** Aider approaches the problem by generating a highly optimized, bounded repository map (repo-map) targeting roughly 1,024 tokens. This maintains a structural overview without exhausting the window [cite: 6](https://www.digitalapplied.com/blog/aider-deep-dive-cli-agentic-coding-tutorial-2026). Rather than purely automatic summarization, Aider introduced a `/handoff` command that explicitly extracts relevant context for the *next* focused task, enabling the human operator to manually declare a task boundary rather than waiting for a token threshold to force a lossy `/compact` [cite: 7](https://aiderdesk.hotovo.com/docs/features/handoff).
*   **OpenHands:** This platform employs an `LLMSummarizingCondenser` that automatically truncates conversation history when it exceeds a configured `max_size` or `max_context_length` of events. It keeps a set number of recent messages intact for immediate state while summarizing the older tail [cite: 8](https://docs.openhands.dev/sdk/guides/context-condenser).
*   **LangGraph:** LangGraph supports "Dynamic Pruning Strategies" where the framework dynamically determines whether a node should execute or pass through based on the status of upstream branches. By tracking branch IDs and calculating node status before execution, LangGraph skips nodes that are no longer relevant, allowing developers to isolate context across sub-agents (Context Quarantine) [cite: 9, 10](https://dev.to/techwalker/dynamic-pruning-strategy-in-langgraphjs-4ed5), [cite: 11](https://medium.com/fundamentals-of-artificial-intelligence/mitigate-context-distractions-in-ai-agents-using-context-engineering-3af25b88d837).
*   **Codex/AutoGPT-lineage:** These systems often rely on restricted environment boundaries, executing tasks in isolated containers where the environment itself resets [cite: 12](https://medium.com/ai-ml-interview-playbook/work-like-10-engineer-with-a-coding-agent-689f73afc06a). Adversarial peer models are sometimes dispatched purely to review diffs in read-only mode, keeping the primary agent's context clean of exploratory validation noise [cite: 13](https://www.reddit.com/r/ClaudeCode/comments/1vcr809/fable_keeps_telling_me_i_am_working_on/).

**Proactive Task-Boundary Detection**
Advanced research frameworks are abandoning raw token thresholds in favor of semantic task boundaries. 
*   **SWE-agent & CAT:** The trajectory-level supervision framework CAT (Context As Tool) and its associated model, SWE-Compressor, fundamentally alter this dynamic. Instead of relying on passively triggered compression heuristics that lead to semantic drift, CAT formalizes context management as a callable tool. The agent proactively compresses historical trajectories into actionable summaries specifically at "appropriate milestones" [cite: 14](https://arxiv.org/abs/2512.22087). 
*   **Praetorian Orchestration:** In a documented 16-phase deterministic AI orchestration framework, developers implement a "Compaction Gate." Before entering heavy execution phases, an external script (`compaction-gate-enforcement.sh`) checks context usage. If usage is between 75-85%, it flags a "Should compact" warning; if above 85%, it initiates a "Hard Block," refusing to spawn new agents until the context is cleanly compacted [cite: 15](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/).

<INFERENCE from="[cite: 7, 14, 15]">
The evolution of these harnesses indicates that reactive token limits are insufficient for autonomous stability. A robust `should-compact` classifier must ignore arbitrary token counts (unless critically close to the hardware limit) and instead evaluate the semantic state of the agent to identify discrete milestones, such as a successful test run, a committed file, or the conclusion of a search sub-routine.
</INFERENCE>

### (2) The Cost of Compacting at a Bad Moment

Compacting context at an arbitrary token threshold rather than a task boundary introduces severe operational penalties, destroying both accuracy and cost-efficiency.

**Loss of Partial State and Latent Disruption**
When an agent is mid-tool-chain (e.g., it has run a `grep`, opened a file, and identified a bug, but has not yet written the patch), its working memory contains highly sensitive, unresolved state. If a token threshold forces a compaction at this precise moment, the standard summarizer condenses the exploration steps into a high-level narrative. The precise line numbers, variable names, and immediate syntactic context are permanently discarded. 

Studies consistently demonstrate the "lost in the middle" phenomenon, where LLMs exhibit U-shaped attention curves [cite: 16](https://www.sundeepteki.org/blog/context-bench-a-benchmark-for-evaluating-agentic-context-engineering). Forcing a compaction at a bad moment exacerbates this by creating "context rot." An agent receiving a differently-framed summary mid-task will follow a divergent logical path than it originally intended, fracturing its architectural continuity [cite: 17](https://arxiv.org/html/2605.23296v1). Furthermore, interrupting latent state recursion—where a model refines an internal solution repeatedly over successive turns—destroys the agent's ability to maintain a stable compositional target [cite: 18](https://aman.ai/primers/ai/recursive-transformers/).

**Cost Asymmetry and Token Drain Geometry**
The cost structure of AI coding agents is dominated by input-token volume. A pragmatic analysis of coding agents like Cursor reveals they consume up to 10x more input tokens than output tokens, accounting for roughly 70% of total inference costs [cite: 5](https://saaswithalex.pages.dev/posts/reducing-cursor-token-usage). 

If compaction occurs mid-edit, the agent loses the immediate diff context and is forced to re-issue massive read commands (e.g., reading an entire 500-line file again) to recover the state it just lost. A 500-line file echo costs over 2,000 tokens of output that immediately become 2,000+ tokens of input on the next turn [cite: 19](https://hexaware.com/blogs/your-context-window-is-lying-to-you-and-its-costing-you/). Conversely, compacting exactly at a task boundary—after a patch is committed and tests pass—allows the agent to cleanly drop heavy file contents from context, replacing them with a lightweight 50-token summary of the completed objective.

### (3) Techniques for Classifying Session State from a Small Window

To build a short, cheap classifier that runs on Haiku-class (Claude 3.5 Haiku) or small models (GPT-5.6-low, Llama 3 8B), the classifier cannot read the entire 160,000-token history. It must operate on a highly constrained window to minimize latency and token expenditure.

**The Hybrid Dual-Layer Pattern**
The most effective technique is to feed the small classifier model a specific, dual-layer slice of memory:
1.  **The Hot Buffer:** The verbatim text of the last 5 to 10 conversational turns. This captures the immediate prosody, the exact tool outputs of the current moment, and any active error traces being debugged [cite: 20](https://chainofcraft.substack.com/p/summarization-memory).
2.  **The Running Event Log:** A highly compressed, append-only chronological log of major actions (e.g., `[2026-08-10 10:00] Ran test suite; [2026-08-10 10:01] Read auth.ts`). Using consistent prefixes makes the log parseable with standard UNIX tools, providing a timeline of the agent's evolution without the bloat of full file contents [cite: 21](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f?permalink_comment_id=6084615).

By presenting the small model with only this localized window, the classifier is asked to evaluate a highly specific condition: *Based on the recent sequence of tool calls and the current pending user instruction, is the agent in an unresolved exploration loop, or has it reached a stable checkpoint?* 

This approach mirrors the AURA (Automatic Understanding of Relational Actions) benchmark's methodology for "implicit-intent inference," which evaluates a model's ability to determine "is now a good time" to take a specific action based on a compact probe trace, rather than stuffing the full environment state into the prompt [cite: 22](https://arxiv.org/html/2606.05557v1).



### (4) Reliability of Small Models at Short Structured Classification

Deploying small models for complex routing decisions requires specific prompt engineering to counteract their innate limitations. Without strict structure, small models fail to assign consistent numeric scores and suffer from verbosity bias (conflating word count with thoroughness).

**G-Eval and Step-by-Step Deduction**
The "LLM-as-a-Judge" methodology proves that small models require frameworks akin to G-Eval. Instead of directly querying the model for a score from 0 to 10, the prompt must force the model to explicitly write out its step-by-step logic against a provided rubric *before* emitting the final token score [cite: 23](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80). Implementing this strategy forces the model to evaluate distinct decision steps that represent conditions met for each score level, significantly improving reliability [cite: 24](https://pmc.ncbi.nlm.nih.gov/articles/PMC12363684/). 

**Explicit Numeric Anchors**
While binary outcomes (e.g., `is_ready: true/false`) generally produce more stable evaluations for smaller models than subtle numeric scales [cite: 25](https://arize.com/guides/llm-as-a-judge/), a 0–10 score is viable if strictly anchored. The prompt must define exactly what a 2, a 5, and an 8 represent. 
*   **Score 0-3 (Veto Compaction):** Mid-edit phase. A file is open, a search is active, or an error was just thrown and is actively being debugged.
*   **Score 4-6 (Neutral/Wait):** Reading phase. The agent is mapping the repository or gathering requirements but hasn't formed a mutation plan.
*   **Score 7-10 (Allow Compaction):** Task boundary. A commit was successfully created, a tool returned a final success message, or a distinct sub-task from the user's prompt is verified complete.

**Constrained JSON Output**
To ensure reliability in a programmatic harness, the prompt must enforce constrained JSON output. Providing a schema where the model first outputs a `"reasoning"` key (fulfilling the deduction requirement) followed by an integer `"score"` key ensures that parsing failures are minimized and the linguistic trace is safely segregated from the control flow [cite: 26](https://wandb.ai/site/articles/exploring-llm-as-a-judge/). Furthermore, employing a swap-and-average technique over multiple few-shot examples calibrates the small model against positional bias [cite: 23](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80).

### (5) Rolling Summaries, Session Logs, and Measured Drift

As agents operate over days or weeks, maintaining context requires "incremental updating"—where a new chunk of recent messages is merged into an existing summary. While computationally cheaper than re-reading the whole transcript, this method introduces severe semantic degradation over multiple appends.

**Measured Drift in Incremental Summarization**
Empirical evidence from the SUMIE (Synthetic Benchmark for Incremental Entity Summarization) dataset demonstrates that state-of-the-art models struggle significantly to update summaries incrementally. Factuality degrades rapidly over successive turns, with F1 scores for state-of-the-art systems maxing out at roughly 80.4% [cite: 27](https://aclanthology.org/events/coling-2025/), [cite: 28, 29](http://arxiv.org/list/cs/2024-06?skip=1985&show=2000). 

Similarly, the BooookScore metric, which evaluates book-length summarization, reveals a distinct structural trade-off: incremental updating yields a higher level of granular detail, but suffers from significantly lower overall coherence (BooookScore) compared to hierarchical merging (summarizing discrete chunks and merging the summaries at the end) [cite: 30](https://www.confviews.com/iclr2024/). For example, GPT-4's incremental summaries scored 82.4 on coherence, while its hierarchical summaries scored 90.8 [cite: 31](https://liner.com/review/booookscore-a-systematic-exploration-of-booklength-summarization-in-the-era). 

**Memory Entropy and the Fact Store Solution**
Practitioners refer to this degradation as the "entropy of summarization." By the third or fourth recursive iteration, a rigorous technical derivation turns into a generic, lossy recap [cite: 20](https://chainofcraft.substack.com/p/summarization-memory). 

To prevent this drift, modern systems decompose memory into distinct architectural layers. The ActiveGraph framework treats the append-only event log as the immutable source of truth, from which state is deterministically folded forward, avoiding lossy summarization entirely for critical facts [cite: 32](https://arxiv.org/html/2605.21997v1). For a `should-compact` classifier maintaining its own log, the system must separate a "Fact Store" (an append-only, version-controlled list of hard constraints, file paths, and exact tool outputs that is never pruned) from the "Narrative Summary" (which is allowed to be lossy to provide high-level continuity) [cite: 20](https://chainofcraft.substack.com/p/summarization-memory). 

### (6) Vetoing Compaction via Claude Code Hooks

To operationalize the `should-compact` score, the agent harness must possess a mechanism to pause or veto an automatic compaction event. Claude Code's extension architecture provides exactly this capability via its Hook system.

**The PreCompact Hook**
Claude Code features over 30 lifecycle events, including a `PreCompact` hook that fires immediately before the system compresses the conversation history [cite: 33](https://claude.nagdy.me/learn/hooks/). A user-defined shell script attached to this event receives a JSON payload via `stdin` containing the session ID and the transcript path [cite: 34](https://yuanchang.org/en/posts/claude-code-auto-memory-and-hooks/). 

**Veto Mechanisms and Exit Codes**
Because Claude Code hooks execute deterministically outside the LLM sandbox in a standard shell environment, they enforce hard programmatic control. To block a poorly-timed compaction, the classifier script simply needs to evaluate the session and emit the correct exit code [cite: 35](https://blakecrosley.com/blog/claude-code-hooks-explained):
*   **Exit 0:** Success. Compaction proceeds normally. If `stdout` contains valid JSON, Claude parses it to adjust its behavior.
*   **Exit 1:** Non-blocking error. Claude Code treats this as a warning and proceeds with the compaction. This is a common failure point for developers expecting standard UNIX abort logic [cite: 35](https://blakecrosley.com/blog/claude-code-hooks-explained).
*   **Exit 2:** Blocking error. The script aborts the compaction process entirely. The script can also return a JSON payload on `stdout` (if exiting 0 with a block directive) such as `{"decision": "block", "reason": "active refactor in flight"}` to provide the model with awareness of why the compaction was delayed [cite: 36](https://github.com/MemPalace/mempalace/issues/858), [cite: 33](https://claude.nagdy.me/learn/hooks/).

<INFERENCE from="[cite: 33, 35, 36]">
By routing the Haiku-4.5 classifier's output through a Bash script hooked to `PreCompact`, the optimal design is achieved: Claude Code's native token-pressure gauge triggers the *request* to compact, but the small-model classifier acts as an absolute gatekeeper, evaluating the Hot Buffer and executing an `exit 2` if the 0-10 score falls below the task-boundary threshold.
</INFERENCE>

## Secondary: 2. What is the current state, and what is the strongest supporting evidence for it?

The current state of agentic context management is transitioning from reactive capacity management (keeping tokens under a limit) to proactive state management (ensuring the LLM has the exact context required for the immediate logical step). 

The strongest evidence supporting this shift is found in the architectural redesigns of frontier open-source and proprietary tools:
1.  **SWE-Compressor's Empirical Validation:** Training a model specifically to inject context-management actions into complete interaction trajectories allowed SWE-Compressor to reach a 57.6% solved rate on SWE-Bench-Verified. This significantly outperformed standard ReAct-based agents relying on static, passively triggered compression heuristics [cite: 14](https://arxiv.org/abs/2512.22087). By compressing at milestones rather than token limits, semantic drift is arrested.
2.  **Input-Token Cost Dynamics:** Evidence from production deployments indicates that re-reading large context arrays accounts for approximately 70% of coding agent costs. Tools like Aider achieve high efficiency not by summarizing vast histories, but by using specialized, bounded repo-maps and explicitly isolating distinct tasks via the `/handoff` command, ensuring the model's active window contains only task-relevant state [cite: 7](https://aiderdesk.hotovo.com/docs/features/handoff), [cite: 19](https://hexaware.com/blogs/your-context-window-is-lying-to-you-and-its-costing-you/).

## Secondary: 3. What are the contrasting viewpoints or competing evidence?

There is distinct methodological conflict in the literature regarding how context should be compressed when a boundary is reached:

*   **Parallel vs. Sequential Compaction:** A prevailing assumption is that a single LLM call can summarize a massive history sequentially. However, research on Parallel Context Compaction from Penn State argues that sequential summarization stalls agent inference for tens of seconds and is highly prompt-insensitive (the model ignores output length instructions). Parallel compaction splits the context into blocks and compresses them simultaneously across separate workers, restoring prompt sensitivity, accelerating throughput, and yielding run-to-run predictability [cite: 17](https://arxiv.org/html/2605.23296v1). 
*   **Hierarchical vs. Incremental Updating:** As evidenced by the BooookScore evaluations, there is an inherent trade-off in summarization styles. While incremental updating (appending new data to a running summary) preserves highly granular details, it suffers from severe organizational drift. Conversely, hierarchical merging (summarizing discrete chunks independently and then merging the summaries) produces higher structural coherence but loses crucial lower-level detail [cite: 30](https://www.confviews.com/iclr2024/). Systems must choose their poison based on whether the agent requires structural understanding or exact string retrieval.

## Secondary: 4. What changed recently, and what is the trajectory?

The trajectory of LLM agent design is moving rapidly toward decoupled memory systems and deterministic orchestration, heavily leveraging Small Language Models (SLMs) for routing and classification tasks.

*   **Decoupled Memory Architecture:** Architectures are increasingly separating the "Brain" (the generative LLM), the "Hands" (sandboxed tool execution environments), and the "Session" (an append-only event log) [cite: 37](https://addyo.substack.com/p/long-running-agents). By treating the event log as the immutable source of truth, frameworks like ActiveGraph can deterministically reconstruct an agent's state at any point without relying on lossy vector embeddings or recursive textual summaries [cite: 32](https://arxiv.org/html/2605.21997v1).
*   **Programmable Determinism via Hooks:** Tools like Claude Code are expanding their hook ecosystems (now featuring over 30 lifecycle events). This allows operators to enforce rigid guardrails—such as formatting rules, security blocks, and the aforementioned compaction gates—that run purely in the shell outside the LLM sandbox. This ensures that the model cannot hallucinate its way out of task-boundary logic [cite: 35](https://blakecrosley.com/blog/claude-code-hooks-explained).
*   **Delegation to SLMs:** Instead of burning frontier-model tokens (GPT-4o, Claude 3.5 Sonnet) on meta-cognitive tasks like determining "is now a good time to compact," architectures are increasingly routing these discrete classification tasks to sub-agents powered by highly capable SLMs (Llama 3 8B, Haiku-class models). When bounded by strict JSON schemas and CoT rubrics, these models offer near-frontier reliability at a fraction of the cost and latency.

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
| :--- | :--- | :--- | :--- | :--- |
| Claude Code compacts automatically at 80% to 95% of its 200k context window. | SFEIR Institute | 2025-09 | Documentation | [cite: 1](https://institute.sfeir.com/en/claude-code/claude-code-context-management/deep-dive/) |
| Sequential compaction stalls inference and retains fluctuating, unpredictable output volumes. | Penn State Univ. (arXiv:2605.23296v1) | 2026-05-22 | Peer-Reviewed Benchmark | [cite: 17](https://arxiv.org/html/2605.23296v1) |
| SWE-Compressor outperforms static baselines by compressing at "appropriate milestones" (CAT framework). | SWE-Agent Research (arXiv:2512.22087) | 2025-12-26 | Architecture Whitepaper | [cite: 14](https://arxiv.org/abs/2512.22087) |
| Small LLM judges require step-by-step logic (G-Eval) and explicit rubrics for numeric scoring reliability. | Weights & Biases / Adnan Masood | 2026-04-21 | Engineering Blog | [cite: 23](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80), [cite: 26](https://wandb.ai/site/articles/exploring-llm-as-a-judge/) |
| Incremental entity summarization suffers from severe drift (max F1 80.4%) on the SUMIE benchmark. | COLING 2025 / arXiv:2406.05080 | 2025-01-19 | Peer-Reviewed Dataset | [cite: 27](https://aclanthology.org/events/coling-2025/), [cite: 28, 29](http://arxiv.org/list/cs/2024-06?skip=1985&show=2000) |
| Incremental updating yields lower BooookScore coherence (82.4) but higher detail than hierarchical merging (90.8). | ICLR 2024 | 2024-05 | Peer-Reviewed Benchmark | [cite: 30](https://www.confviews.com/iclr2024/), [cite: 31](https://liner.com/review/booookscore-a-systematic-exploration-of-booklength-summarization-in-the-era) |
| Claude Code `PreCompact` hook requires an `exit 2` or `decision: block` JSON payload to veto compaction. | Blake Crosley / MemPalace Github | 2026-07 | Code Documentation | [cite: 35](https://blakecrosley.com/blog/claude-code-hooks-explained), [cite: 36](https://github.com/MemPalace/mempalace/issues/858) |
| ActiveGraph utilizes an append-only event log folded deterministically to eliminate lossy context drift. | ActiveGraph Research (arXiv:2605.21997v1) | 2026-05 | Architecture Whitepaper | [cite: 32](https://arxiv.org/html/2605.21997v1) |
| Cursor coding sessions consume up to 10x more input tokens than output, dominating costs. | Pragmatic Engineer Analysis | 2026-07-16 | Data Analysis | [cite: 5](https://saaswithalex.pages.dev/posts/reducing-cursor-token-usage) |

## Knowledge Gaps

*   **Exact Token Cost of Premature Compaction:** <MISSING_DATA> [Precise empirical measurements of token waste specifically caused by mid-edit compactions versus task-boundary compactions were unavailable in the provided literature. To quantify this fully, benchmark data comparing input-token overhead in interrupted versus uninterrupted tool-chains is needed.] </MISSING_DATA>
*   **Haiku-4.5 Specific Latency:** <INSUFFICIENT_EVIDENCE> [While small models are universally known to be faster, the exact millisecond latency overhead of invoking Haiku-4.5 or GPT-5.6-low as an inline classifier during a `PreCompact` shell hook could not be corroborated with specific published benchmarks.] </INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1.  **Prototype the G-Eval `should-compact` Prompt:** Develop and rigorously test a constrained JSON prompt on Haiku-4.5. The prompt must take a dual-layer input (a 10-turn hot buffer and an append-only log), output a step-by-step evaluation string, and conclude with an integer score (0-10) strictly anchored to specific task boundaries (e.g., "Score 7 = tests passed; Score 2 = grep active").
2.  **Implement the `PreCompact` Veto Script:** Write a shell script tailored for Claude Code's `PreCompact` lifecycle event that feeds the dual-layer context to the Haiku-4.5 classifier. Ensure the script correctly translates scores $< 7$ into an `exit 2` bash code to block the compaction, while preserving `stdout` logs for telemetry.
3.  **Evaluate Hybrid Memory Integration:** Transition the agent's memory architecture away from pure incremental summarization to mitigate the drift observed in the SUMIE benchmarks. Implement a system featuring a lossless, version-controlled "Fact Store" for critical constraints, running alongside a lossy "Narrative Summary." Evaluate the reduction in drift over a 50-turn session using a local LLM-as-a-judge script. 

## Model Architecture Comparison for Classifier Integration

When selecting the SLM to back the `should-compact` skill, evaluating the trade-offs between parameter scale, latency, and context window is essential for minimizing the overhead of the `PreCompact` hook.

| Model / Framework | Parameter Class | Max Context Window | Typical Use Case | License / Availability |
| :--- | :--- | :--- | :--- | :--- |
| **Claude 3.5 Haiku** | ~10B - 20B (Est.) | 200,000 Tokens | High-speed structured classification, JSON output | Proprietary API |
| **GPT-5.6-low / mini** | ~8B (Est.) | 128,000 Tokens | Latency-sensitive routing, tool calling | Proprietary API |
| **Llama 3 8B Instruct** | 8 Billion | 8,192 Tokens | Local classification, open-weights deployment | Open-Weights (Meta) |
| **SWE-Compressor** | N/A (Fine-tuned) | N/A | Trajectory-level context milestone detection | Academic Research |
| **Aider Repo-Map** | N/A (Algorithmic) | ~1,024 Tokens | Structural codebase orientation | Open-Source |

**Sources:**
1. [sfeir.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF99WIZWyxC5_yDwhnSJ_3HKl-nrespug3Pgkg5r5HHRTyUhwcEZ3qLj4varER1ZRCJBMAnSBK-2lsX45ScnOfe_YJZhrXhdhXCr4vyVz8M5jr0U7KCWoAFlrY9Rnuv6ueLRVllmCceiCyeiIV0XRI1rlb9mmebXVuRmxG1jZOcD2qYLK86tXbLYqI=)
2. [sfeir.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3Ed_hnoCF7KcLYU-NDRs6ETH19X13HKVAABbJ9KkefUeLjIarEb5Upb7tV5TMAo99huMDbYJIji70_EoSJME0-MJGJFk2RyhKqyhVdTWyEvh-G9xj4RRjROgxZoLhYLP4DEK98LD6pil_cQJhsadla6tGVDsVEXKkML9adpDtJ7Xe2AsJjsnbpiLd)
3. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHU6wnu4e5HqhHdzdTRXZnWGXR8uGLRUAEkBNPA6R5aCng_-rJRGvodyOjs8goO0R-jpP2yvUkYKcBa4uvvFnwxMHCLUujcQDJbn8S7B18ECkBiggnt_5c1WBulGFkOcKVxQCfC)
4. [cursor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGtbEfcUARQ9nU-WCBLgW4P-ZYL4YNpPtvBT01tCohQeEXDKbYqw2h_xlbBZmet-OSD1GSqZ3FZqQ6i7w6lC7oObIk5GS6tK2pt-z1Dt7ldFhgPvjahWt_EdVR-bK0OdBgW6iKVMXC0uLlzWqKqt33keNbuF3O8j6znRtMm8k5Y1r0v)
5. [pages.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQECH-9NJTo0vSsuUdLDBP9RTzqv3FsPRz-5D063pbBpvgMstq1FsA3rYrhqk5kqRSy0c5hYTTr7_gpV65V-BjV-RH1_c0eNk4Uc7RRj9KoJ9tKsAtjq2rHoHuUBEUps5I-bIuxOf7WM1cSN28iFyirCkAYRZC-h)
6. [digitalapplied.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFx4nmxi7yMONXU99K_Ky789Ec-Ij0Sp-CtO5RCnQJcJ_Nl-Tm3Notghz_tlQGljQJUwZrurjrNhKvkMxAQgPV5OW6lHiMZZo6s6QWa5GhOMAgqieth0_kRfuuDaG3yZsWesXkKpUFBDElCEVDhsgP8zmp-mgVlAwpuiOFoDroFXZc0cVABjsHrSUE=)
7. [hotovo.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHp9VK9x03SMKZmF2lG8fveZz7jiRth9_3z49wT4FcjTOE2Z05_o6wisz3ghMbhPH_BYxjHEvfdx35wIvdWM889Htb50TlhMkOMzcXDsg8cQvb3ZJiNc44WEWhAeKxwm4KZKsW5FtwtuA==)
8. [openhands.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEJFZFgADvdDHJSUFLXdO4MjoASAJdLTqbFh8pCLB1eKcA9hSGPcewlqBUJmreS0esqDnqo_UM-MX1oIk37L5z1tMn6L7VtfaTAi1ra2Y3FRJvDzN2qndOqxA94Ks57ZwPaLU1SUCPKjUnctCJ-)
9. [dev.to](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG6zmFAyM0P2LsncFxYlMCfKzFKRmYKSYAUI5vmFtG1Yg-VZQprIF1SiTqIS8KFDZKnIha_j9UcpAvHuvG-wi5sXM5L7q5pvBEkO-EOcuqK7w8-Ya6_Fp8DvGnA08SjsYkLALT2ZVKnJ9g0yVfypoVRFkep-ETTyT6ivhQd)
10. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQECSNexxwvlHPBnwuho3emxDci7tBVfh2YMtZccZGuGlRfCUgqEfhGaZD_lQMp8NoOcEhw4wFpgcuRzZa_CSrnfLH--ZimvO9z_j6jeftTgLLixx7jYniGPoFU1GaMB1i7EqY_IExRQNT8297O4QrYDcXKtvYiYQ3txGIyS1MZ3NFbr5arGhHKs4ayPBVa7Hk8QOhk=)
11. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHXYy578d6FumFWKz5JJDptWa0aB50wfHlu1FyniAh_G6KWOJg6K_PVhBZ4bVw9i6BLTxFa_NZfSS8c-3LiKk1fo-Q3U0jxFWkxMVQ-xVg2wTq5_pcZaJ3pmWFDt-RDgCbbfyD4R05K9UI5SA84iJwuOeCz731-vIJ-p_oF9lFtNMofwuxeN2m5OT63WoDpbJcaQzH69C8impfJMbUkwH9rNBu8fshIOcy2TTwZUN9ilPRiVPdTqSxQVRSuSJrCJJwodf4=)
12. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFNhW0cZy_bNTOCZPvshZptVyr9kfyNNZFml3r4dSPbGB8yE2eHthxjjYOM-R69u0SZ0HNiaOGsbtiIMjIkLDG_QB7kCa_oGxXdC6izfJFCHWLG1JkidqA5N8SijQexZLIPcgP7W_hkGEmWnSTJYClrWreMOptsYZYSl5qXXL_GAWLEn8asfh3uidjJLZ1E-8RQKsbAHwmGsw==)
13. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxGJfYpaCkkNtvpXAjlYoeG4xe0qChLtXV6cmj_YhbZIFDv1ODR1OR0BTed3GKNYEqDxV98klB8KMw17c3Nr9TgRsxnLvSGGcCj7jFoZSkWVCV2qo_PKcFyhxYGQVH1uT8QIGjloPrmkFlqK1RJhYrmuPFDQSfeYW-BwRjtfw36eDj8aHFFb2K-dtdbics1B2gzA==)
14. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE_TPXOMfzvDNb5tNpboKoju2-UhFhhP2X5BwJWdAkEbZg-HE1tMrv7eQKd8FCbsDRi6I_UgM9i5Nmx7cBZhYbPUGfj8I96yIewdhuSI3W54bcEqk9D4w==)
15. [praetorian.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwIjg22FGUUP6_VFn2QCZc8_eX8-IW8eeMqnVpjGggrNpwJ0cADSyKHZqMxrtC1yGW9N788Ds37koNEzs2RBEJYVVkiNTvTl9L95jYumlqR6Sm_qRWkPt777_Iy5rRD_h3bk70QVQY1xxZp4cjHdUCq4ldmGpEXiFb4000iSBGHgvxlu34bAxEwcfe11dUWfu6lt0MVUIo-ukbIiugTsT-4qmd3X_W5AI=)
16. [sundeepteki.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE0Zfer2rV8aLTRxo6QH9g2fpBiOaxPdBkD68fvtvWF5Z1ViBjVW5UxSJfqPulJi5bG2Iunxp9UmXUTepyiM9UNddhlLdDQmf8v6LnGGNxT3K8n7DRJ8ZGNnr560CtuS8OvJ3aWit9gd_v2S92vKXRN65xqUzVkzY5IZOTiD86-q5mnekJDlH7Z99irirAO5ZizjMtJ4DcCl7z6Ig==)
17. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHy6OgGwJUaBq5eL4IdKNhp261o5qRBMOJ8Na-nlUD8Od19Mu6RG5X9EYnu1f4sZ8zmD_yoDaQUOk2pNp2DVnCefWJMlHyD90pES2nrQ5xnYWJBb5ScTdWPBA==)
18. [aman.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHA7FbC7rVlXHtfwgDO7Utf080NmFDDFZ1qOnX9s6DSzRHqfERw8-8pM6iskohm2SnFa3JljvgNANdVsTV3-xYqQP24Xv6Q5n3paNI8uU0zdD0hbkGJsFcRgFBdqfo_4k5z6kaezWyjw==)
19. [hexaware.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXfTOMWnjPDhoW_vJzlogBlv_qQrfnV3-bGSGlPwbeubE0GY5upXJ_3b0YfrYgrqGio2uO1E0N_bsRnNzR8eK_69LbLglUE2hpuvd9ZRF_y357iM-4Kg8f7ImOTdDsBRV57rhxwWp-hBQFjnJhngv9y30HpWgsgK41WZOcYVRrRauANuwegJJgaw==)
20. [substack.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFwar_pvrjutnMLE_f4bZStXtZOgK6JllXByVX1dxN2zb0u3276Fw9F6NtnYh4-7rvSou5E8332m57K9l9GogRPznDC6PsB1tOGh3sK3CDMd7eEWqxcgd88M3uI0PeEBwKVimXALpUzSmPqAnR_aw==)
21. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF-K2F0q-Ah-inIV371K_TbZjawTd4nnLl6U0Rb1Kadr7ud9sKosEMCei1MWU49nsXfnWI9rtZFOumzhI_Uugm95cvanKXXQJJyzrICY2PIe4SY6mtLQMccwJaGty1Z_C9TIXDmQu73LnuRhJMWMipk4eOzbx9UzNCVdBmgEQ5fQ3gEf6nXg0HTJ0MDK6s2p3Vk9dm0)
22. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgnaDLpcV5-Uv7MWnU38qL6fazP5cnqn_3BKNsOoAgl0FdN6_9_EPpKccqrR4BugsHGuU4Ow_FuGpByg-ZfC0twGpUAw0VeRwWSH2IJrIfIYZsV5YHWFYxcw==)
23. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFsMsGdSk9O6INfg-UW1XDdiva3up33WxEdfJ6JDEjOgTve6_dpwcTo0GZP4MQwQkGChp__Vruq8M5uHPILo01kAKjucSeqxY8x5uk0hnsrF1ELFDs-UOGZoKqUNamFtlu-1mRRsOakQuFddXdBhuK6_agnokGlKPTwAN5SqobtqpJWb_7XKe6yo-OMdY46no1j0eKUxUdKsktAg1tgYPX44r8iuUc-ilpMIT1Jbrai-PXiKmqwNMDha3N1YL-G)
24. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFD8TkE4ikHNjSySGDoStFGFyXH9M1r52UTdgBxvQ4LRtqh8WQRuCbZ-RZV_6KFgcSVwHWgfi5jAT8YEg-pK1xB37ZY8DwSTJL8AuYHdABTD7qXSuVHe9OUM5CX3C2gVYJEecxaqDgAEw==)
25. [arize.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHn0qvfFCjisA2TOuct8T8lgXs77ferOmQanvRMtacmat34VoG8qpfHeNoMVJj4EPsKoqFgtja_lgE-RT9m1w6pRhvUPoyBo91U5OM2b8wBt6FYCzVjJjqL_G5bQHjg)
26. [wandb.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGHCbAa4xrZAv5QpF37UND5OAGuVQpSCwju48OIc7539hOkUgUEIwZ6G6gWIpUxqwue-6FQOBVksSgGYafRs9D8ZyMbH9k-PXkGaO4qIRm47yJO2YtcHP2ZOkzBlAJcNBwUTBH2aP3GgiUcmZOtcw==)
27. [aclanthology.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEC9sJ8kqhTyIN3PWM91DXWga6aBiR0wkG19srxOg-3Xhs8IXAvK5uZcT-QY48nw4FPTCPeWaLfR1hUF-05t-_5OdE9YtrqoqOHRNjoA6W_JgOe2GULiIPr7cB-0buMd__gPA==)
28. [aclanthology.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEJ1bEQTVFZSyDP1mdogZqDj1oLfvG-cF95qqWybcpyNlGlId0nll3eO5MynrZyPj8MDwxesrZ0LIEV5gVlktpWteMoYy5fglpdBhmwPxgg1-TvP44q1_TZIiyRYH0oYEWu40Tb8xErpQ==)
29. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETiRg90Viwf3muWdKAE-K5WXKf6z6O7UPOfOWKRwFMTvUp0gPVl-2y6BO4m4jQeJLV6yqXBYuMtCEEwvAmJfCFYJSJqfv8pYA9APFsS5SVQF8smP-yjd5NXCuI7uMqBRFfeikNfztHrKTU)
30. [confviews.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFc2NJwqVbrptvHl7jrudhqe7QE5Iaef16sDqbtudSdpLIWmeQdl6m6SfdTIDfghpnxLSlmfWDo3Bf_Ogj4G-2xB3p3uXjewyuEktsmMZyjmsvgfhiKKF5Rgw==)
31. [liner.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEOZthnmIB87Hbqpsb59Tmf6YRr_5cVZeYwn2RrOjTwo9p-CR4beoWC9KtK6aEbYlJp6qmQiOimLEd4gjdol_dpMU9pGBiAR4q89D44t04VbMM9ogkODR4UVpmscZVkkRRMnQ8HXzIZdYiYpsi-LwWjPwIoIyHinVxROxlyksjl9YZyrIKECiuUED2kVAujtS7DVRFKxFKK-a78)
32. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHRQ7Rr49reemiPTdCfDJt6LisEqHLlusygO0HRLRMmX8tvKj7-VEJvXFuM2-vucabVt7guR57Wm-rtGyBBK_H9oMdKKdOB0-DynYbP_XcusJl5XbEN1r7xow==)
33. [nagdy.me](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGYir838WrL9V8tZCXe33557p0wcKFi6OfMEhNWB2yd3yUMbOsieZwbZIe-eP2M-pgfa1dKbk8sDa8-v2vczWfgjh-QQ6GtNUSM4f2e0f9AiwKfogsaB0N3FLU=)
34. [yuanchang.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5jtmkKES49ta6bC7ueDR39kCsQhykyQi3ZLkVrN2NM2N0TdWsu-rG1hVgcAJVfOrVnemKUgkRgv_A3_VBYh9K-0nIBsk1FT6OfNdAI0Q28HoNI_gH4aK7sFrfkldh4LfNHlpAlToU-hQ7y6CC6TS4eq_l3Ecf6w==)
35. [blakecrosley.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEISeqQn0CRlYEsXyXFSihIDLJXr-Cpt4NP_G0TMt0naD-5V97ZEmSmr3y8H9G7F18FHZZl3a-e2WrGkvnTKmIYnt6dMhEF7eYKAM4KW2l6GCOHkALVUFQ4OhiH4Ii7EGCcmFcr3IhX_6p5aTmUmns=)
36. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH2cuUVK4PsCWOzDzWUJF4KPrHbv8aM6Q6gXVA_sjErwNRHMkQrL5DiJ40ovhzjCw9wXf8uqBGz1jq6BIg2R-lFWniH3dOjWscgJW9aKcIwrCkmR2AX61i-Hjm2CH_wjSGNSBw9oTfn)
37. [substack.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHK9vVQADfiOlpjjMUYJdBQHBX4cCZbWXeowxEfYgtcOTG2sBIXGx4d01pV_itzG-bLLya4c8Tf_b1xy5a3pfIuWnugevEbtOJdl_FEg3nHqGshUnT5zNp2FENzhSUepxtIcshu35M=)
