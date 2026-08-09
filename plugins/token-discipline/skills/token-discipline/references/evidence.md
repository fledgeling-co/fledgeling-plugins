# Evidence

Every load-bearing claim in `SKILL.md` and `references/injected-block.md`, with what it rests on.
Sorted by how much weight it carries. **First-party measurements come first, because they are the
only ones taken on the workload this block actually runs against.**

Citations were dereferenced (38/38 resolved on the primary research run, 0 fabricated). Where a
figure was reported second-hand and not read in the paper's own results section, it says so.

---

## 1. First-party: diolog-swe-bench, Opus 5

The measurement that caused this rebuild. Source: `~/Dev/diolog-swe-bench`, the Benchwarmer SQLite
store, graded by that repo's own canonical spec (`docs/SCORING.md`) — binary fail-to-pass for
behavioural dimensions, judge score for `optimality`/`ui`, mean of the two most recent clean decided
samples per (model, task).

**Arms:** `claude-opus-5` (pure) vs `claude-opus-5-caveman` (caveman `SKILL.md` body injected via
`--append-system-prompt`), both at `xhigh` effort. **106 tasks carry both arms.**

| | pure | caveman | Δ |
| --- | --- | --- | --- |
| Score | 63.3% | 55.7% | **−7.61 pp** |
| Cost | $229.02 | $152.34 | −33.5% |
| Tokens | 126.1M | 73.4M | −41.8% |
| Steps / task | 24.5 | 16.5 | −32.7% |
| Tokens / step | 48.6k | 42.0k | −13.6% |

**Direction, per task:** 48 worse, 15 better, 43 unchanged. Sign test over the 63 directional
tasks: **p < 0.0001**.

**By dimension:**

| Dimension | tasks | pure | caveman | Δ | worse / better |
| --- | --- | --- | --- | --- | --- |
| tool-use | 4 | 100.0% | 75.0% | −25.00 pp | 1 / 0 |
| backend | 42 | 54.8% | 46.4% | −8.33 pp | 8 / 3 |
| ui | 45 | 67.0% | 59.5% | −7.45 pp | 35 / 7 |
| optimality | 10 | 75.0% | 72.8% | −2.19 pp | 4 / 5 |
| frontend | 5 | 50.0% | 50.0% | 0.00 pp | 0 / 0 |

**The finding that shaped clause 6 — the harm is concentrated in long tasks:**

| Task length (pure arm) | tasks changed | worse | better | sign test |
| --- | --- | --- | --- | --- |
| 10–19 steps | 23 | 13 | 10 | p = 0.68 — no effect |
| 20+ steps | 38 | **34** | **4** | **p < 0.0001** |

**Decomposition of the token saving.** Steps fell 32.7% and tokens per step fell 13.6%;
`(1 − 0.327) × (1 − 0.136) = 0.582`, which is the observed −41.8% exactly. So **≈78% of the token
saving is attributable to the agent taking fewer steps**, not to terser prose.

**Register compliance, measured over 683 caveman and 370 pure run transcripts.** Caveman forbids
decorative structure. **97.5% of caveman runs still emit markdown bold or bullets, against 98.9% of
pure runs** — the register rule is very nearly a no-op. Median final-message length fell 2,690 →
1,979 chars (−26%), against a median 1.19M tokens per task. The prose the rule targets is a rounding
error; the behaviour change it caused is not.

**What this measurement does not establish.** Quality was scored by the bench's own graders, not by
a human. The tool-use dimension is 4 tasks. Two runs per (model, task) is a thin sample window, and
it is the window the bench's own spec requires rather than one chosen here.

---

## 2. Independent: JetBrains, Sonnet 5

[JetBrains AI blog, July 2026](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/)
— verified first-hand, not via research summary.

- SkillsBench, 86 of 87 tasks, 82 clean pairs, `claude-sonnet-5` at `--effort low`, Claude Code
  2.1.200 headless. ~240 billed trials, ~$106.
- **"Advertised saving: 65%. Measured saving: 8.5%."** Output tokens 592k → 542k.
- The skill arm was **11.6% more expensive in raw totals** ($40.60 vs $36.39) — driven by one
  dependency-audit trial crossing the 200k long-context tier ($8.29 vs $0.33). A comparable outlier
  hit the baseline arm in an earlier run, so it reflects the task, not the skill.
- **Quality: 8 better, 10 worse, 64 tied. Sign test p = 0.82 — no detectable difference.**
- Their own warning, worth carrying: an initial −29.5% smoke result "vanished with more data — Never
  trust a k=1 eval", and the full run was itself k=1.

**This is a null result, and it does not contradict §1.** Different model, different effort, different
benchmark, different task lengths. A k=1 null is a weak null, not evidence of safety. The honest
reading is that caveman is roughly harmless on short Sonnet work at low effort and harmful on long
Opus 5 work at xhigh — which is what both measurements, read together, say.

---

## 3. Caveman's own numbers — it is not overclaiming

Worth stating plainly, because an earlier internal brief criticised caveman for a 65% headline it no
longer carries alone. The current [README](https://github.com/juliusbrussee/caveman) reports both
figures side by side, links the JetBrains run, and adds:

> **Honest number warning.** Caveman only shrinks **output** tokens. Input and reasoning tokens are
> untouched, and the skill itself adds ~1–1.5k input tokens per turn. So whole-session savings run
> smaller than the output number, and on already-terse workloads they can go net-negative.

And: *"65% and 8.5% are both correct, and neither one is your number."* That is a fair
characterisation. **The disagreement in this repo is with the skill's rules, not with its
marketing.**

---

## 4. Anthropic documentation — the rules that make caveman misfire on Opus 5

All from [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5),
[Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices),
and the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide).

- **Literal instruction following.** "If your review prompt says 'only report high-severity issues'
  or 'be conservative,' the model may follow that instruction literally and report less." Caveman's
  *"State each fact once"* and *"One word when one word enough"* are that shape. On a benchmark,
  reporting less is indistinguishable from finding less.
- **Preamble permission is the documented fix, not the bug.** "When you use a tool, you may say a
  brief sentence first." Caveman: *"No preamble, plan, or progress note before or between calls."*
  The leak it guards against is severe — a tool call written as text "completes normally and the
  call never runs", and the leaked text stays in history.
- **Positive framing beats prohibition.** "Positive examples of the communication style you want tend
  to be more effective than instructions about what not to do." Caveman is roughly a dozen
  prohibitions against one positive pattern.
- **Long-horizon guidance runs the other way.** Anthropic's own agentic prompts ask the model to
  "plan out your work clearly", track progress, and "not stop tasks early". Caveman bans the
  narration those depend on. This is the documented counterpart of §1's 34:4 long-task result.
- **Remove verification instructions, do not add prohibitions.** Opus 5 self-verifies; carried-over
  verification instructions cause over-verification. The correct operation is deletion — which is why
  v3 dropped v1's "no trailing verification pass" rather than rewriting it.
- **Prompt style influences output style.** "The formatting style used in your prompt may influence
  Claude's response style." Caveman's `SKILL.md` is itself written in degraded telegraphic English.
- **`effort` is the native lever and it reaches further than prose.** Effort affects "all tokens in
  the response, including tool calls and function arguments". No prose rule can reach those.

---

## 5. Literature — brevity, personas, tokenizers

**Brevity has a measured accuracy cost.**
- Renze & Guven, [arXiv:2401.05618](https://arxiv.org/abs/2401.05618) (FLLM 2024): Concise CoT cut
  length 48.70% with a math-accuracy penalty on GPT-3.5. *The frequently-quoted 27.69% figure is from
  the paper body; it was not read in the results section here. Direction: high confidence. Exact
  magnitude: not verified.*
- Nayab et al., [arXiv:2407.19825](https://arxiv.org/abs/2407.19825) (*Information Sciences* 2026):
  fixed output-length budgets cost accuracy on reasoning benchmarks. *Tables not retrieved; reported
  second-hand.*
- Giskard's Phare benchmark: hallucination resistance falls under a "be concise" system prompt.
- **Counter-evidence, stated rather than buried:** [arXiv:2604.00025](https://arxiv.org/abs/2604.00025)
  claims brevity constraints *raise* accuracy on items prone to over-elaboration. It is a
  single-author, non-peer-reviewed preprint that caveman cites in its own defence. The effect
  plausibly flips with item difficulty; that is a reason to scope compression away from reasoning,
  not a reason to compress.

**Persona prompts cost accuracy, and coding is the worst-hit category.**
- Hu, Rostami & Thomason (USC), [arXiv:2603.18507](https://arxiv.org/html/2603.18507v1) — verified
  first-hand. MMLU 71.6% baseline → 68.0% with a persona → **66.3% with a long persona**. Granularity
  tested: Full ≈150 tokens, Short ≈75, Min ≈5. §3.1c is titled *"Longer persona prompts damage
  more."* On MT-Bench, **Coding is the largest single loss at −0.65**.
  **Limitation the authors flag, and it is a real one: every model tested is 7–8B. Behaviour at 70B+
  was not tested.** So this is a prior for sizing the block, not a law about Opus 5.
- Pei et al., [Findings of EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.888/): 162
  personas across 2,410 questions, no improvement over persona-free baselines. *Not retrieved
  directly; counts reported second-hand.*
- Wharton (2025): no expert persona reliably improved GPQA; low-knowledge personas were generally
  harmful. Caveman is, structurally, a low-knowledge persona.

**Telegraphic register does not buy much under BPE.** Common function words (`" the"`, `" a"`,
`" for"`) are each a single token including the leading space, so dropping an article saves exactly
one token; invented abbreviations fragment into more. **Caveman already makes this argument itself**
— it bans `cfg/impl/req/res/fn` on the grounds that "Full word cheaper AND clearer" and bans `→` as
"own token, save nothing". Applied consistently, that is an argument against article-dropping too.
Anthropic's tokenizer changed at Opus 4.7+, producing ~1×–1.35× more tokens for the same text, which
does not help unusual constructions.

---

## 6. The lever hierarchy — why prose is the wrong target

From [Anthropic Engineering, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
and [Manage costs](https://code.claude.com/docs/en/costs). Vendor-internal benchmarks; direction is
mechanistically sound, exact magnitudes unaudited.

| Lever | Measured effect | Accuracy effect |
| --- | --- | --- |
| Tool Search Tool | −85% tokens (~77K → ~8.7K) | **Improves** — Opus 4.5 tool selection 79.5% → 88.1% |
| Programmatic Tool Calling | −37% (43,588 → 27,297) | **Improves** — GIA 46.5% → 51.2% |
| `effort` low/medium | Not published; reaches tool calls too | Task-dependent |
| Cache hygiene | Cache reads bill at 0.1× base input | Neutral |
| PreToolUse output filtering | "tens of thousands of tokens to hundreds" | Neutral |
| **Terse output register** | **−8.5% output tokens; +11.6% session cost in the measured arm** | Null on Sonnet 5; **−7.6 pp on Opus 5 (§1)** |

Tool definitions alone have been observed at 134K tokens; a five-server MCP setup runs ~55K. Against
that, compressing narration prose is the smallest lever on the board and the only one on this list
with a measured accuracy cost.

---

## 7. Open questions

- **No study isolates the mechanism.** In an agentic loop the assistant's own messages are its input
  on every later turn, so an output-side style becomes an input-side one as the session grows. That
  is the most plausible explanation for §1's 34:4 long-task result, and nothing published tests it
  directly. FrugalPrompt ([arXiv:2510.16439](https://arxiv.org/abs/2510.16439)) is adjacent: input
  compression is tolerated on retrieval-style tasks and "degrades sharply" on mathematical reasoning.
- **Whether v4 beats v3 is unmeasured.** The clause-6 argument is a correctness argument from §1, not
  an A/B result. Nothing here may be upgraded to a claim of saving until paired rows exist.
- **Session token composition is unmeasured for this operator.** If output is ~14% of a cache-warm
  session, the entire output-side project has a ceiling near 9%.
