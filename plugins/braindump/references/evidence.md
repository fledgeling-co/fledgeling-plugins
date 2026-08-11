# Evidence — where every number and rule in this skill comes from

Four deep-research reports back this skill, all read end to end and all
fabrication-checked clean (42/42, 33/33, 28/28 and 10/10 citations resolved).
The full corpus is in `docs/deep-research/`. Two of the reports independently
flagged the same measurement gap, and this skill's benchmark fills it.

## The measurements taken here

Run with `scripts/benchmark_vs_compact.py --arms cli` over every real
compaction event under `~/.claude/projects` with at least 20 prior rows. Each
event is a summary the built-in `/compact` actually wrote, scored against the
transcript it actually replaced, by normalised exact match.

| class | retention | events |
|---|---:|---:|
| user corrections | 63.1% | 34 |
| standing constraints | 33.8% | 74 |
| **rejected approaches** | **0.3%** | 68 |
| identifiers | 48.6% | 120 |
| file paths | 16.4% | 119 |
| median summary length | 20,585 chars | 121 |
| mean extractiveness | 0.09 | 121 |

**The 0.3% is the finding.** Both the local-Claude and gpt-5.6 reports state
plainly that no published study isolates negative-knowledge survival through
compaction, and both name it as a cheap gap for exactly this harness to fill.
The answer is that it does not survive at all.

Two caveats on comparing these to the skill's earlier figures. The earlier
table reported **medians** over 225 events; this reports **means** over the 121
events that have at least 20 prior rows, and the correction detector matches on
a 60-character prefix. Different statistic, different sample, so the numbers are
not directly comparable, and neither supersedes the other.

### Replication, 2026-08-08 — which numbers are load-bearing

A second `--arms cli` run over the 40 most recent qualifying events
(`docs/benchmark-cli-baseline.json`) separates the robust finding from the
noisy ones:

| class | 121 events | 40 events | reads as |
|---|---:|---:|---|
| **rejected approaches** | **0.3%** (n=68) | **0.0%** (n=11) | replicates |
| median length | 20,585 | 22,214 | stable |
| mean extractiveness | 0.09 | 0.08 | stable |
| identifiers | 48.6% (n=120) | 68.2% (n=39) | swings |
| file paths | 16.4% (n=119) | 23.7% (n=38) | swings |
| standing constraints | 33.8% (n=74) | 50.0% (n=28) | swings hardest |
| user corrections | 63.1% (n=34) | 41.7% (n=4) | n too small to mean anything |

The instrument is the same and the samples overlap, so the spread is sampling
noise at these instance counts, not a change in behaviour. What it establishes
is which claims this skill may lean on.

**The 0.3% survives replication because it is not really a percentage** — it is
the observation that negative knowledge is absent, and a floor of zero cannot
drift. Every other retention figure moves by 10–20 points between samples, so
each one is a per-sample observation and must be quoted with its n. Citing
"33.8%" as *the* constraint-retention rate overstates what 74 instances can
support; the defensible form is that standing constraints survive at roughly a
third to a half, and that both are far too low to rely on.

The two confounds being stable across samples is what makes the arms
comparable at all: a length or extractiveness gap in the head-to-head will be a
property of the arm rather than of which transcripts got drawn.

## Why two tiers, and why pinning

**ConstraintRot** (arXiv:2606.22528, 1,323 episodes, seven model families) is
the load-bearing external result. Constraint-violation rates: 0% with the
governing constraint in full context, 30% after compaction on average, 59% for
the worst family. The conditional decomposition is what matters: **0% when the
constraint survived into the summary, 38% when it was dropped.** Presence very
nearly determines compliance. Its Constraint Pinning mitigation restores 0%.

That converts a vague quality question into a binary presence question, which is
why this skill optimises span recall of a small must-survive set rather than
summary quality, and why those items are exempted from summarisation rather than
summarised well.

## Why paraphrase is the subtle failure

- A constraint of "use type hints everywhere" was compacted to "the user prefers
  a consistent code style with type hints", deleting the absolute quantifier.
  Constraint questions then scored 14.0% exact match (CogCanvas, arXiv:2601.00821).
- A scoped instruction — remove calls in `a.py`, leave `b.py` unchanged — was
  compacted into a global removal (Slipstream, arXiv:2605.08580). The same paper
  reports **roughly 90% of observed compaction failures are omissions**.
- Verbatim spans beat LLM-extracted artifacts by 15.9 points on LoCoMo (43.9% vs
  28.0%) and 22.0 points on LongMemEval-S (67.4% vs 45.4%) (CogCanvas).

## Why extract-then-compress, and why verification is against the transcript

- Extract-then-generate lifted FactCC from sub-10% baselines across four
  datasets, and self-extracted salient sentences worked about as well as oracle
  extractions (arXiv:2304.04193).
- **Intrinsic self-correction without external feedback does not reliably
  improve output and sometimes degrades it** (Huang et al., ICLR 2024,
  arXiv:2310.01798). So "re-read your summary and improve it" is not supported;
  re-reading the *transcript* to check coverage is a retrieval task with
  external evidence, and is.

## Why compaction is a last resort

- LOCA-bench (arXiv:2602.07962) at 128k: compaction bought +2.6, +2.7 and
  **−2.7** points across three models, where programmatic tool calling bought
  +13.3, +9.4 and +10.6.
- JetBrains' "Complexity Trap" (DL4Code @ NeurIPS 2025, arXiv:2508.21433):
  observation masking matched or slightly exceeded LLM summarisation's solve
  rate on SWE-bench Verified at about half the cost.
- Anthropic's own long-running-agent guidance moves handoff out of compaction
  and into durable files, noting compaction "doesn't always pass perfectly clear
  instructions to the next agent". Hence this skill's escape hatch.

## Why the keep-short rule on the pinned tier

- IFScale: frontier models reach only 68% instruction-following accuracy at 500
  instructions, with a documented bias toward earlier instructions
  (arXiv:2507.11538). A bloated pinned tier competes with itself.
- ReasoningBank found retrieval at k=1 outperformed k=4 (49.7 vs 44.4,
  arXiv:2509.25140). More retrieved context was worse, not better.

## Why the benchmark reports length and extractiveness

- Faithfulness gains often turn out to be extractiveness artifacts: several
  proposed methods failed to beat a trade-off-curve control at matched
  abstractiveness (arXiv:2108.13684), and judges score copied text generously.
- Verbosity bias inflates judge scores independent of quality.

A rewrite that produces longer, quote-heavier summaries will therefore "win" on
naive scoring without being better. Both confounds print beside every score.

## Why the evals avoid judge scores

- G-Eval correlates with human raters at ρ ≈ 0.514 on SummEval, against
  inter-human agreement of roughly 0.8-0.9 (arXiv:2303.16634).
- Self-preference bias is well documented and stronger in more capable models
  (arXiv:2410.21819), which disqualifies judging a Claude-written summary with a
  Claude judge.
- Position bias is systematic in pairwise comparison and only partly mitigated
  by order swapping (arXiv:2410.02736).

Hence: deterministic span recall is the primary metric, and any judged layer
uses a different model family, swapped orders, and matched token caps.

## What the research says we still cannot claim

- **Downstream continuation success is the gold-standard metric and this skill
  does not measure it.** Span recall is close to a direct measure for the
  constraint class specifically, because presence nearly determines compliance,
  but "the next session actually finished the task" is a stronger claim than
  anything measured here.
- **The head-to-head is underpowered for small effects.** Sample size scales
  with the inverse square of the minimum detectable effect, and agent runs carry
  large stochastic variance (arXiv:2605.30315). Report the effect, the n and the
  MDE; do not report a bare percentage.
- The LOCOMO agent-memory leaderboard is contested to the point of being
  unusable for design decisions, and is not relied on here.

## Server-side compaction, for the harness that wants it

The Messages API exposes compaction directly: beta header `compact-2026-01-12`,
edit type `compact_20260112`, default trigger 150,000 input tokens with a 50,000
minimum. Two facts matter for this skill:

- **`instructions` replaces the default prompt entirely**, it does not
  supplement it. Anything you rely on must be restated.
- **`pause_after_compaction: true`** returns the summary before continuing, so
  the caller can re-insert pinned content verbatim. That is the API-level form
  of the Tier 1 idea.

Usage is billed as an extra sampling iteration, and top-level token counts
exclude it — sum `usage.iterations`.

## Errata and later measurements — 2026-08-11

Recorded after a grounding pass against 90 days of this operator's transcripts (counting rules:
one response = one `(requestId, message.id)` group; scripts in `perch/scratch-contextcost/`).

- **The trigger measurement is confirmed and sharpened.** 258 main-chain compaction events, median
  pre-compaction context **987,636 tokens** — the wall, on 4.4× the original sample. The
  distribution is bimodal: 59.3% of events above 900k, 29.1% below 200k (manual `/compact`), and
  the middle nearly empty.
- **The residue is affine, not flat.** `post ≈ 50,958 + 0.117 × pre` (n=1,037, R² ≈ 0.25 above the
  floor). "A compaction leaves ~51k" is true only near the ~57.7k crossover below which compaction
  grows the context; at the wall the residue is ~168k. This corrects this file's implicit
  only-the-summary-survives framing and is consistent with the parallel-compaction finding that
  summary output is nearly input-invariant (~3× output growth across 48× input, arXiv:2605.23296 —
  lifted from the retired grok research file, its one distinctive contribution).
- **Wall-clock, previously a named gap.** The turn spanning a compaction takes a median **171.6 s**
  against **12.1 s** for an ordinary turn (n=219) — ~160 s of extra waiting per event. This fills
  the `MISSING_DATA` cells in the gpt-5.6 research file and re-weights asynchronous compaction
  (Slipstream) from curiosity to obvious next lever.
- **ConstraintRot's 0%/38% figure was read from the abstract only.** No scenario counts, domains,
  or mitigation implementation were ever verified. The two-tier design it motivates is
  independently supported by the paired case study, but treat the specific percentages as
  unreplicated.
- **The CogCanvas figures are single-source.** Only the gemini research file reports them, citing
  two different HTML versions of one arXiv id, and it is the most secondary-source-dependent file
  in the corpus. Unreplicated.
- **Research-file status.** `compaction-local-claude.md` and `compaction-openai-gpt56.md`: current,
  with the errata above. `compaction-gemini.md`: single-source caveats above apply.
  `compaction-xai-grok.md`: superseded — its two concrete Claude Code claims (~150k trigger,
  75–95% auto-trigger) are both wrong at the measured 99.8%.
