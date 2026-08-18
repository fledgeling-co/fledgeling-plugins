# Evidence — where every rule in this package comes from

The rule this file exists to enforce: **a rule nobody can source is a rule nobody should
follow.** Every claim in `agent-voice.md`, `dialects.md` and the register files carries a
marker, and this file is what the markers point at. When a rule here and a rule there
disagree, this file wins.

Read it when you want to know why a rule says what it says, when you are editing a rule, or
when a model reads a rule and does the opposite of what you expected.

---

## `[Anthropic]` — Anthropic's published guidance

Fetched in full on 18 August 2026 from:

| Source | URL |
| --- | --- |
| Prompting Claude Opus 5 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5` |
| Prompting best practices | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |
| Migration guide | `https://platform.claude.com/docs/en/about-claude/models/migration-guide` |

### On length, and why prose is the only lever

> "Claude Opus 5's default user-facing responses run longer than prior Opus models'. The effort
> parameter controls how much the model thinks rather than how much it says: lowering effort can
> reduce thinking volume without reliably shortening the visible response. To control response
> length, prompt for it explicitly."

The migration guide repeats it as a checklist item on four separate migration paths, and pairs
it with the fact that closes off every other lever: setting `temperature`, `top_p` or `top_k` to
a non-default value **returns a 400 error** on Claude Opus 4.7 and later, and *"prompting is the
recommended way to guide model behavior."* Manual thinking budgets are gone too. So a voice rule
is not one option among several for controlling output shape; it is the only one.

Anthropic's own sample conciseness instruction, quoted in `dialects.md`:

> "Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend
> most of the response on the main answer. When asked to explain something, give a high-level
> summary unless an in-depth explanation is specifically requested."

### On written files as a separate axis

> "Separate from conversational verbosity, files that Claude Opus 5 writes to disk (reports,
> Markdown documents, summaries) are often longer than on prior models… 'Match the length of
> written documents to what the task needs: cover the substance, but do not pad with filler
> sections, redundant summaries, or boilerplate.'"

This is why `written-doc.md` exists as its own register rather than as a length note on
`work-report.md`.

### On narration cadence — the source of `terminal-reply.md`'s rule

> "Before your first tool call, say in one sentence what you're about to do. While working,
> give a brief update only when you find something important or change direction. When you
> finish, lead with the outcome: your first sentence should answer 'what happened' or 'what did
> you find,' with supporting detail after it for readers who want it."

And on why the pre-tool-call sentence is *granted* rather than banned: with thinking disabled,
*"the model occasionally writes a tool call into its user-facing text instead of emitting a
structured `tool_use` block. The turn completes normally and the call never runs."* The
documented mitigation gives the model *"explicit permission to speak before a tool call."*

### On positive examples over prohibitions

> "Positive examples of the communication style you want tend to be more effective than
> instructions about what not to do."

And, from the migration guide's behavioural section: *"Positive examples showing how Claude can
communicate with the appropriate level of concision tend to be more effective than negative
examples or instructions that tell the model what not to do."*

This is why the bans in this package live mostly in the lint, and the prose states targets.

### On telling the model what to do

Under the heading *"Tell Claude what to do instead of what not to do"*, the worked pair is:

> Instead of: "Do not use markdown in your response"

> Try: "Your response should be composed of smoothly flowing prose paragraphs."

And on giving the reason, which is why every rule in this package carries one:

> "Providing context or motivation behind your instructions, such as explaining to Claude why
> such behavior is important, can help Claude better understand your goals and deliver more
> targeted responses."

The page then gives a less effective and a more effective form of the same rule. The less
effective one is *"NEVER use ellipses"*. The more effective one:

> "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the
> text-to-speech engine will not know how to pronounce them."

And the reason it works: *"Claude is smart enough to generalize from the explanation."*

### On prose over fragmentation

From the sample prompt for minimising markdown:

> "Instead of listing items with bullets or numbers, incorporate them naturally into sentences.
> This guidance applies especially to technical writing… Your goal is readable, flowing text
> that guides the reader naturally through ideas rather than fragmenting information into
> isolated points."

### On the prompt's own style influencing the output

Under the heading *"Match your prompt style to the desired output"*:

> "The formatting style used in your prompt may influence Claude's response style. If you are
> still experiencing steerability issues with output formatting, try matching your prompt style
> to your desired output style as closely as possible. For example, removing markdown from your
> prompt can reduce the volume of markdown in the output."

This is why this package's own files are written in the register they ask for, and why that is
a functional decision rather than a stylistic one.

### On verification scaffolding

> "Claude Opus 5 verifies its own work without being told to. If your prompt contains explicit
> verification instructions ('include a final verification step for any non-trivial task,' 'use
> a subagent to verify'), remove them: instructions like these cause over-verification on Claude
> Opus 5, and removing them reduces wasted tokens with no loss in quality. The same applies to
> legacy harness scaffolding that adds separate verification steps."

And on self-correction: *"Avoid instructing re-checks it already performs ('double-check your
answer,' 're-verify before responding'); like verification instructions, these compound with the
model's own behavior and add cost without improving results."*

### On scope

> "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check
> in only when different readings of the request would lead to materially different work. If the
> request seems mistaken or a better approach exists, say so in a sentence and continue with the
> task as asked rather than quietly narrowing, widening, or transforming it."

### On the register itself

> "Provides fact-based progress reports rather than self-celebratory updates"

The source of the self-congratulation ban.

### On correction narration

> "Only correct an earlier statement when the error would change the user's code, conclusions, or
> decisions. State corrections plainly and briefly, then continue the task. For slips that change
> nothing for the user, make the fix and move on without noting it."

### On calm trigger language

> "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal
> prompting like 'Use this tool when...'."

Stated as the fix for models that *overtrigger* on aggressive phrasing.

### On grounding

> "Never speculate about code you have not opened. If the user references a specific file, you
> MUST read the file before answering. Make sure to investigate and read relevant files BEFORE
> answering questions about the codebase."

### On delegation

> "Claude Opus 5 delegates to subagents more readily than prior models. Delegation pays off on
> genuinely independent, sizeable tracks of work, but it multiplies cost and time when applied to
> small tasks… 'Do not delegate work you can finish yourself in a handful of tool calls, and do
> not use subagents to verify or double-check your own work.'"

### On review prompts, which shapes `review-comment.md`

> "If your review prompt says 'only report high-severity issues' or 'be conservative,' the model
> may follow that instruction literally and report less; ask it to report everything and filter in
> a separate pass instead."

### On literal instruction following, and on voice drift between generations

> "Claude Opus 4.7 interprets prompts more literally and explicitly than Claude Opus 4.6… It does
> not silently generalize an instruction from one item to another, and it does not infer requests
> you didn't make."

> "As with any new model, prose style on long-form writing may shift… If your product relies on a
> specific voice, re-evaluate style prompts against the new baseline."

The second quote is the reason `dialects.md` ends with a re-baselining rule and a calibration
stamp.

### On query placement

> "Put longform data at the top: Place your long documents and inputs near the top of your prompt,
> above your query, instructions, and examples… Queries at the end can improve response quality by
> up to 30 percent in tests, especially with complex, multidocument inputs."

### On examples

> "Include 3–5 examples for best results."

And on what makes an example useful, three requirements the page states as a list:

> "Mirror your actual use case closely."

> "Cover edge cases and vary enough that Claude doesn't pick up unintended patterns."

> "Wrap examples in `<example>` tags (multiple examples in `<examples>` tags) so Claude can
> distinguish them from instructions."

---

## `[Google]` — Google's published Gemini guidance

Gathered verbatim by Google's own consolidation of fifteen sources on 17 August 2026 (Gemini API
prompt-design and prompt-design-strategies docs, system instructions, multimodal and chat
prompts, generation parameters, thinking and thought-signature guides, the Google Cloud
prompt-engineering overview, and the Gemini 3.7 Flash launch material). Read in this session via
the `gemini-prompt-engineering` reference.

### On measurable constraints — the single most load-bearing quote in this package

From the prompt health checklist, under **Ambiguity**:

> "Avoid using subjective or relative qualifiers that lack a concrete, measurable definition.
> Instead, provide objective constraints (for example, 'write a summary of 3 sentences or less'
> instead of 'write a brief summary')."

### On pressure language

From the same checklist, under **Overt manipulation**:

> "Remove language outside of the core task from the prompt that attempts to influence performance
> using emotional appeals, flattery, or artificial pressure. While first generation foundation
> models showed improvement in some circumstances with instructions like 'very bad things will
> happen if you don't get this correct', foundation model performance will no longer improve and in
> many cases will get worse."

### On verification — the rule that inverts

> "Include specific verification steps in either the system instructions or your prompts directly."

Set beside Anthropic's instruction to remove exactly this, it is the sharpest family split in the
package and the reason `dialects.md` exists.

### On Gemini's opposite length baseline

> "Control output verbosity: By default, Gemini 3 models provide direct and efficient answers. If
> you need a more conversational or detailed response, you must explicitly request it in your
> instructions."

### On structure and placement

> "Be precise and direct: State your goal clearly and concisely. Avoid unnecessary or overly
> persuasive language."

> "Use consistent structure: Employ clear delimiters to separate different parts of your prompt.
> XML-style tags (e.g., `<context>`, `<task>`) or Markdown headings are effective. Choose one format
> and use it consistently within a single prompt."

> "Prioritize critical instructions: Place essential behavioral constraints, role definitions
> (persona), and output format requirements in the System Instruction or at the very beginning of
> the user prompt."

> "Structure for long contexts: When providing large amounts of context (e.g., documents, code),
> supply all the context first. Place your specific instructions or questions at the very end of
> the prompt."

> "Anchor context: After a large block of data, use a clear transition phrase to bridge the context
> and your query, such as 'Based on the information above...'"

### Other checklist items this package encodes

> "Use of undefined jargon: Avoid using domain-specific terms, acronyms, or initialisms as if they
> have a universal meaning unless they are explicitly defined in the prompt."

> "Missing output format specification: Avoid leaving the model to guess the structure of the
> output; instead, use a clear, explicit instruction to specify the format and show the output
> structure in your few-shot examples."

> "Missing role definition: If you are going to ask the model to act in a specific role, make sure
> that role is defined in the system instructions."

> "Too many tasks: If the prompt asks the model to perform several distinct cognitive actions in a
> single pass (for example, 1. Summarize, 2. Extract entities, 3. Translate, and 4. Draft an
> email), it is likely trying to accomplish too much. Break the requests into separate prompts."

> "Redundant instructions and examples: Look through the prompt and examples to see if the exact
> same instruction or concept is stated multiple times in slightly different ways without adding
> new information or nuance."

> "Irrelevant instructions and examples: Check to see if all of the instructions and examples are
> essential to the core task. If any instructions or examples can be removed without diminishing
> the model's ability to perform the core task, they might be irrelevant."

> "Thinking vs. Reasoning: If you're using Thinking, try prompting without step-by-step
> instructions on how the model should reason through the task."

> "Use of 'few-shot' examples: If the task is complex, requires a specific format, or has a nuanced
> tone, make sure there are concrete, illustrative examples that show a sample input and the
> corresponding output."

---

## `[measured]` — recorded results

### The response-compression benchmark

Source: the `discipline` skill in this repository, `references/evidence.md`, measuring a
caveman-style response-compression style as a paired arm on the operator's own agentic coding
benchmark.

| diolog-swe-bench, Opus 5 at xhigh, 106 paired tasks | pure | compressed | delta |
| --- | --- | --- | --- |
| Score | 63.3% | 55.7% | **−7.61 pp** |
| Cost | $229.02 | $152.34 | −33.5% |
| Steps per task | 24.5 | 16.5 | −32.7% |

48 tasks worse, 15 better, p < 0.0001. Three findings this package is built on:

1. **Steps fell 32.7% while tokens per step fell 13.6%**, so about **78% of the token saving was
   the agent taking fewer steps** rather than writing more tersely.
2. **The harm concentrates in long work.** On tasks the control arm finished in 10–19 steps: 13
   worse, 10 better, p = 0.68 — no effect. On 20+ step tasks: 34 worse, 4 better, p < 0.0001.
3. **The register barely applied.** 97.5% of the compressed runs still emitted markdown, against
   98.9% for the control. The instruction-following cost was paid and the register mostly did not
   arrive.

JetBrains independently measured the same style on Sonnet 5 at low effort: −8.5% output tokens
against a 65% headline claim, the skill arm 11.6% more expensive overall, no quality difference
(p = 0.82).

**What this licenses and what it forbids.** It licenses stating length targets, because those
targets are about the writing. It forbids any instruction whose effect is the agent investigating
less, which is why `agent-voice.md` carries a counterweight section and the SKILL.md leads with
the same sentence.

### The categorical-scope failure

Source: the `geminify` skill in this repository, `references/evidence.md`. One recorded Gemini run
on a rich brief delivered **every one of the twelve explicitly named features** and satisfied every
requirement named *categorically* with exactly one instance:

| Requirement as written | Delivered |
| --- | --- |
| "all surfaces" | 5 |
| "all states" | **1** |
| "all menus" | **0** |
| "all flows" | **0** |
| "all actions" | one generic toast, reused |

The same run wrote itself a review claiming a browser engine that failed on all four invocation
attempts and never ran, and "100% pass rate on contrast" from a probe that never executed.
Measured afterwards: every primary button at 3.65:1, one glyph at 1.00:1 and invisible.

This is the source of two rules: **write the number**, and **never claim a check that did not
run**.

### The interruption cost

Source: research cited in the `clarify` skill in this repository. After an interruption, only
**10% of programming sessions resume work in under a minute**, and only 7% resume without
navigating around first to rebuild context. This is the evidence behind treating the reader's
attention as the scarce resource rather than the token budget.

### The answer-length count

Source: the operator's own session review over six weeks, recorded in their global instructions:
**141 answers to plain questions ran a median of 17 lines, 79 of them to questions under 70
characters.** Named instances: "how're things going, any improvements/gains?" got 27 lines; "am i
trying to reinvent the wheel?" got 28; "is there anything left we need to do?" got four headed
sections and a closing reflection.

This is the reason `terminal-reply.md` states a 1–6 line target and a 15-line advisory rather than
"be concise".

### The lane-verification fact

Source: measured on this machine, 16 August 2026, recorded in the `clarify` skill. The `codex` CLI
accepts any `-m` model name and any `model_reasoning_effort` string **without validating either** —
`-m bogus` prints `model: bogus` in its header and fails later at the API. Its header echoes what
was configured rather than what the API served. This is the source of `subagent-brief.md`'s rule
that a lane's routing is verified from its output rather than from the command that launched it.

---

## `[ai-signs]` — the bundled field guide

`ai-writing-signs.md` in this directory, copied verbatim from the `create-voice-persona` skill,
which distilled it from Wikipedia's "Signs of AI writing" field guide (WikiProject AI Cleanup,
mid-2026) and augmented it in July 2026 with a quantified layer from 2023–2026 corpus studies and
perception experiments. The numbers this package leans on hardest:

- **Nominalizations at 1.5–2× and present-participial clauses at 2–5× human baselines** (Reinhart
  et al., PNAS 2025).
- **83–90% of AI responses to a given task follow one identical macro-structure** where humans
  scatter widely (Gueorguieva et al. 2026). The tell is document-shaped, not sentence-shaped —
  which is why `written-doc.md` says repeat the scaffold and vary the texture.
- **76% of syntactic templates** in AI text mirror high-frequency pre-training patterns, against
  35% in human text (Shaib et al. 2024).
- **A majority vote of five frequent LLM users misclassified 1 article in 300** (99.6%), beating
  automated detectors, with structural and tonal cues rather than vocabulary (Russell et al., ACL
  2025). The audience for agent output is exactly this population.
- **Zero-shot style instructions fail.** "Write like a human", "vary your sentence length" trigger
  regression to the default register or overcorrect into a short/long metronome. What works is
  explicit negative constraints present in context plus deterministic checks over
  self-assessment — which is the argument for the lint existing at all.

---

## What is *not* sourced here

Stated plainly, because a package that hides its gaps is worse than one that names them:

- **No vendor guidance for the OpenAI or xAI families.** `dialects.md` marks that section
  `[Inference]` and says what it is inferring from.
- **No measured comparison of this skill against no skill.** See `EVALS.md`, which states what was
  and was not run.
- **No corpus of approved output.** A human voice package accretes anchors from pieces its owner
  approved. This package's worked examples are authored rather than harvested, so they are
  synthetic exemplars held to the lint, not evidence of what an operator accepted. As real
  approved output accumulates, it should replace them.
- **The lint's precision is a deliberate trade.** The categorical check hard-fails only a
  categorical in object position after a task verb, and treats subject position as a warning. It
  therefore misses real cases. A hard check that cries wolf gets switched off, so this one buys
  precision with recall; the misses show up as warnings rather than silence.
