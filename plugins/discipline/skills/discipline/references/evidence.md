# Evidence

Every load-bearing claim in `SKILL.md` and `references/injected-block.md`, with what it rests on.
Sorted by how much weight it carries. **First-party measurements come first, because they are the
only ones taken on the workload this block actually runs against.**

Citations were dereferenced (38/38 resolved on the primary research run, 0 fabricated). Where a
figure was reported second-hand and not read in the paper's own results section, it says so.

**Every figure is marked in `references/provenance.md` on two orthogonal closed axes —
`independence+verification` — and `scripts/block-check.py` fails the build on an unmarked one.** That
file is the machine-readable index to this one: it carries both closed sets, the scope, the source, and
— for a living document — the date it was read. Read this file for the argument and that one for the
audit.

The two axes are kept apart because promotion runs along one of them only: reading a source more
carefully improves *verification* and never makes its author disinterested. A competitor's README read
in full is `self-report+results-read` permanently.

---

## The output-to-input ratio, and what it cost unwatched — added 2026-08-21

| Figure | Value | How measured | Limit |
|---|---|---|---|
| Ratio on completed runs | 1.1x, 2,510,067 in against 2,833,838 out over 61 runs | Summed token fields on the pipeline's own run records | Two summed fields, not per-turn |
| Ratio on failed runs | 33.8x, 20,269 in against 684,666 out over 52 runs | As above | As above |
| Output spent on runs that produced nothing | 813,649 tokens, 22% of window output | As above | Cancelled covers operator stops and stale sweeps alike |
| Cache reads across the set | 413,895,107 over 135 runs | As above | Pipeline accounting, not a provider invoice |
| Runs producing no artifact | 74 of 135, 55% | Run status counts | A floor on waste rather than a claim about intent |

**Tier: measured, n=1 pipeline, one twenty-day window, 2026-08-21.** The 5x alert threshold in SKILL.md
is a judgement from this single distribution rather than a tuned value, and nobody has measured whether
watching the ratio shortens a diagnosis. What is measured is that the signal separated failed from
completed runs from the first failure onward and was never computed, across twenty days in which 41
commits went into output gates and 15 into prompts before one touched the cause.

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

## 3. Caveman's own numbers — read 18 August 2026

**Mark: `self-report+results-read`.** Both documents were read here in full, and that changes nothing
about their independence — a README figure is its author's own performance claim, unaudited, and no
amount of careful reading promotes it. The date on this section is load-bearing: it is a claim about a living
document, and an undated one cannot be checked.

What is verbatim present in the [README](https://github.com/JuliusBrussee/caveman), and is to
caveman's credit:

> **Honest number warning.** Caveman only shrinks **output** tokens. Input and reasoning tokens are
> untouched, and the skill itself adds ~1–1.5k input tokens per turn. So whole-session savings run
> smaller than the output number, and on already-terse workloads they can go net-negative.

Its `docs/HONEST-NUMBERS.md` goes further than this repo previously credited: it lists the aggregate
output reduction as **"Not published"**, on the grounds that a harness exists but no reviewed raw
result is committed, and it tells the reader to measure their own A/B.

**A correction to an earlier version of this file.** Until 18 Aug 2026 this section claimed the
README "reports both figures side by side" and "links the JetBrains run". **Both documents were
fetched on 18 Aug 2026 and neither is true.** The README's headline is still 65%
("Average / 1214 / 294 / **65%**"); the string `8.5` does not occur in the README or in
`HONEST-NUMBERS.md`; neither mentions JetBrains; and the sentence *"65% and 8.5% are both correct,
and neither one is your number"* — previously quoted here as if from the README — is in neither file.

Two readings, and this repo cannot separate them: the README was rewritten after that claim was
written (it has visibly grown a proxy, a pixel mode, a browse tool and TOON encoding since), or the
claim was wrong when made. **That indistinguishability is the point.** It is why every row in
`provenance.md` pointing at a living document carries an `observed` date, and why this section
carries one in its heading.

The substantive position is unchanged and does not depend on the retraction: **the disagreement in
this repo is with the skill's rules, not with its marketing.** Caveman's own SKILL.md concedes the
ceiling on its own mechanism (invented abbreviations save zero tokens under the tokenizer; causal
arrows are their own token), and the honest-number warning above is a real one.

**Where caveman is straightforwardly better, stated because being fair about it matters more than
winning the comparison:**

- **It has a measured number on its own axis and works anywhere.** No proxy, no cache assumptions, no
  injection point: install and go, across 30+ agents by its own count (7 proxy wrap profiles, 5 MCP
  tools). This skill's best delivery — see SKILL.md § *Why placement decides everything* — needs a
  `system`-field injection point, and degrades to nothing without one.
- **On output-heavy work it wins outright.** Long explanatory answers, documentation generation,
  anything where the model talks far more than it reads. There the axis it attacks is the right one
  and this skill barely helps.
- **On short work it is close to harmless.** §1's own split says so: 13 worse / 10 better at p = 0.68
  under 20 steps.
- **The two are not exclusive, and nobody has tested the pair.** Running both is coherent — caveman
  shrinks what is written, this shrinks what is re-sent, re-read and re-delegated. The four-arm run in
  §9 is what would settle whether they compose or interfere, and it has never been run. Until it has,
  "pick one" is a convenience, not a finding.

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
- Giskard's Phare benchmark: instructions emphasising conciseness "degraded factual reliability across
  most models tested", and "in the most extreme cases" cost **up to 20 percentage points of
  hallucination resistance**. Published 30 Apr 2025; article read 18 Aug 2026.
  **`independent+results-read` for the aggregate, `independent+unlocated` for the per-model pairs, and
  narrower than this file used to say.** Giskard publishes that 20
  points as an *aggregate*: the article carries **no per-model figures**, so the widely-repeated pairs
  (84%→64% on Gemini 1.5 Pro, 74%→63% on GPT-4o) are **not in the source** — an earlier version of this
  file quoted them as though they were, and two independent research passes on 18 Aug 2026 failed to
  locate them. The article also never lists which models were in the brevity condition, so **whether
  any Claude model was included is unknown**, and this must not be reported either way. It is a reason
  the block carries no conciseness clause, never a measurement of one.
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

## 6. Independent replication — token reduction is not cost reduction

**The most important source in this file after §1, found 18 Aug 2026, and it was not available when
this skill was designed.** Weinberger & Hozez, *Token Reduction Is Not Cost Reduction*,
[arXiv:2607.12161](https://arxiv.org/abs/2607.12161) (submitted 13 Jul 2026, v5 12 Aug 2026, cs.CL).
Figures below read from the paper's own results section on 18 Aug 2026, with its confidence intervals.

**Scale:** 2,848 analysed runs of **Claude Code** (of 2,908 executed) across 103 tasks, 7
repositories and three models — Haiku 4.5, Sonnet 5, Opus 4.8 — inside a wider programme of 5,493
billed executions. That is roughly 27× this repo's own 106-task arm, on the same agent.

### It settles what this skill had been assuming

| Share of the actual bill | Measured | 95% CI |
| --- | --- | --- |
| Cache creation | 44.3% | [43.2, 45.3] |
| Cache reads | 35.4% | [34.5, 36.3] |
| **Generated output** | **10.4%** | **[10.0, 10.9]** |
| Uncached input | 1.3% | [1.1, 1.5] |

Cache operations are ~80% of the bill (~87% of the reconstructed four-component cost). Mean run
volumes: ~117k cache-read tokens and ~12k cache-creation tokens against ~**715 generated tokens**.
There is a dollar-weighted residual of +8.7% [7.2, 10.1] which the authors tie to thinking-effort
scaling; on Haiku 4.5 it grows from 11.0% to 18.3% with effort.

**So the ~14% output share this skill assumed is now measured at 10.4%** — the assumption was close and
slightly generous. `provenance.md` moves that row off `assumed` accordingly.

### It reproduces this repo's own v4 null, at 27× the scale

The paper's RTK-ML arm cut delivered tool-output tokens **−38.4%** and **billed cost rose +6.8%**
[+2.8, +11.3]. Success rates did not separate (96.2–97.8%, all CIs crossing zero). That is the same
shape as §1's v4 result — output down 16.3%, cost up 32.6%, score indistinguishable — arrived at
independently, in another lab, with a far larger sample.

Two findings sharpen it further:

- **Token reduction barely predicts cost reduction.** Across 100 Haiku tasks, Pearson **r = 0.154**
  [−0.051, +0.356] — the interval crosses zero. In the 5–20% reduction band, cost *increased* 24.7%
  [+6.3, +46.0].
- **The whole user-side project has a small ceiling.** A component attribution finds a user-side layer
  can reach only about **6.0% of input cost, practical ceiling nearer 5%**; tool outputs alone are
  ~3.3%. The 38.4% token cut moved ~1.3% of input cost.

### What this does and does not license

It licenses the central claim — that shrinking what the model writes is the smallest lever on the
board, and that a token dashboard and a bill can move in opposite directions. It is the strongest
external support this skill has, and it argues *against* the skill's own optimism about savings as much
as it argues against caveman's.

It does **not** license describing this block as a saving. The paper measures tool-output compression
and context-reduction arms, not a system-prefix behavioural preamble, and its baseline is unmodified
Claude Code rather than this literal. The honest reading: the ceiling on any output-side or
tool-output-side intervention is single-digit percentages of input cost, and one arm that cut tokens
by 38% paid 6.8% more. Nothing about v4 is measured here.

*Grade note: dereferenced and read here, but via fetch-and-summarise rather than the PDF, so the
figures above are `independent+summarised` rather than `results-read`. Re-read the PDF before quoting a CI in
anything load-bearing.*

### What it replaces: the 96% anecdote

An earlier generation of this skill opened with a headline claim: *"one practitioner measured 3.77B
tokens through a workspace in a day, 96% of it reused input."* It was the single load-bearing figure in
the file and it had no citation. It was removed before this version shipped, and two independent
research passes on 18 Aug 2026 confirm that was correct: the claim traces to a practitioner writeup
(attributed to Nate B. Jones / The Learning Atlas, July 2026) with **no methodology, no log export and
nothing reproducible attached.** Tier: **unauditable anecdote.** Nothing in this skill should ever have
rested on it.

It also produced a derived figure — "cut 65% of output on a turn where output is 4% of the bill and you
have cut ~2.6% of that turn" — which was wrong in a second way: the 4% residual was `100 − 96`, but that
residual is new input *plus* output, so 2.6% was an upper bound presented as an estimate. Both are gone.

**§6 is the honest replacement**, and it is better than the anecdote in every way that matters: a real
sample (2,848 runs), a real agent (Claude Code), published confidence intervals, and a *lower* output
share than the anecdote implied (10.4% measured, against the ~14% this skill went on to assume and the
4% the anecdote implied). The direction the anecdote pointed in was right. Its number was not evidence.

Worth keeping as a lesson rather than just a deletion: the figure survived several rewrites because it
was vivid, specific and directionally correct, which is exactly the profile of a number that does not
get checked.

## 7. The lever hierarchy — why prose is the wrong target

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

## 8. Open questions

- **No study isolates the mechanism.** In an agentic loop the assistant's own messages are its input
  on every later turn, so an output-side style becomes an input-side one as the session grows. That
  is the most plausible explanation for §1's 34:4 long-task result, and nothing published tests it
  directly. FrugalPrompt ([arXiv:2510.16439](https://arxiv.org/abs/2510.16439)) is adjacent: input
  compression is tolerated on retrieval-style tasks and "degrades sharply" on mathematical reasoning.
- **Whether v4 beats v3 is unmeasured.** The clause-6 argument is a correctness argument from §1, not
  an A/B result. Nothing here may be upgraded to a claim of saving until paired rows exist.
- **Session token composition is measured in general and unmeasured *here*.** §6 settles the general
  case on 2,848 Claude Code runs: generated output is 10.4% of the bill [10.0, 10.9], and a user-side
  layer can reach only ~6.0% of input cost. That supersedes this file's earlier assumption that output
  was ~14% with a notional ~9% ceiling — the assumption was close and slightly generous, and it is
  retained in `provenance.md` only so the argument's history stays auditable. What is still unmeasured
  is **this operator's own split**: nobody has counted the cache-read, cache-write, new-input and output
  shares on this traffic, and §6's models (Haiku 4.5, Sonnet 5, Opus 4.8) do not include Opus 5 at
  xhigh, which is the workload this block actually runs against.

## 9. The measurement that would settle the comparison, and has never been run

Named here because it is owed. The right instrument is **total session tokens including cache
misses**, across matched task cohorts, on **four arms**:

| Arm | What it tests |
| --- | --- |
| neither skill | the baseline |
| caveman only | the output axis alone |
| this block only | the repetition / read-width / delegation axes alone |
| **both** | whether the two compose or interfere |

The fourth arm is the one no run has ever included, and it is the only one that can answer whether
"pick one" is the right advice. §3 says the two are not exclusive; nothing has tested it.

**Do not use per-turn output length.** A preamble can always be tuned to shrink visible output while
forcing more turns, more tool calls or more delegation to finish the same task — the per-turn number
improves while total spend rises, and that failure mode is invisible to exactly the metric people
reach for first. §1's step-count decomposition is what that looks like when it happens.

Three secondary readings worth capturing in the same run:

1. **Cache read/write ratio** — does the block ever invalidate a prefix it should have ridden inside?
2. **Subagent spawn count** — the delegation clause's direct evidence.
3. **Total bytes read from disk** — the read-width clause's direct evidence, and **nobody has looked
   at it.** Clause 5 is currently the one clause in the block with no named way to measure whether it
   does anything.

If the four-arm run shows this block's arms indistinguishable from baseline on total tokens, the
argument in SKILL.md is wrong and the block should be cut back to whatever survives.
