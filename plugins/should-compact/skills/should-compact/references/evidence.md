# Evidence

Every rule in `SKILL.md` traces to something here. Where this operator's own data and the published
literature disagree, the local measurement wins and the disagreement is stated rather than resolved
silently — one of them is about this machine.

## The trigger fires at the wall, not at 80%

Published guidance says Claude Code compacts at **80–95%** of the window
([SFEIR](https://institute.sfeir.com/en/claude-code/claude-code-context-management/deep-dive/), via
`docs/deep-research/compaction-timing-gemini.md`).

**Measured here: median 998,289 tokens of a 1M window — 99.8%**, across 235 real compaction events
(209 automatic, 26 manual) recorded on this machine over 90 days. The dataset is
`perch/docs/reference/compaction-events-2026-08-05.json`.

The difference is the reason `precompact_gate.sh` has a headroom rule at all. At 80% there is a
fifth of a window to spend waiting for a boundary; at 99.8% there is essentially none, so a veto
that does not check headroom converts a lossy compaction into a hard overflow.

A 90-day recount (INSAV-RECON counting rules, one response = one `(requestId, message.id)` group)
found **258 main-chain compaction events, median pre-compaction context 987,636** — the same wall,
on 4.4× the original sample. The distribution is bimodal: 59.3% of events fire above 900k (the
window filled) and 29.1% below 200k (someone typed `/compact`); the middle barely exists.

## The residue is nearly a constant, and the affine fit over-predicts it

Two fits, on two corpora from the same machine, disagreeing by a factor of two at the floor. The
later one is preferred, and this section says why rather than deleting the earlier one.

**The 90-day fit, n=1,037:**

```
post_context ≈ 50,958 + 0.117 × pre_context      crossover ~57,700
```

**The 7-day recount, n=1,522 automatic events (2026-08-14 … 2026-08-21, 3,778 transcripts):**

```
post_context ≈ 26,783 + 0.015 × pre_context      R² 0.045      crossover ~27,200
```

R² 0.045 is the finding rather than a weakness of it: **the residue barely tracks the input at
all.** Median post-compaction context was 31,189 tokens, and by pre-context band it moved from
23,317 (under 200k in) to 34,846 (over 800k in) while the input grew fivefold. Read as a share, a
compaction sheds 86% of a 200k context and 96.5% of an 800k one.

Against this corpus the 90-day model over-predicts by a median of **52,510 tokens** (p10 −92,354,
p90 −31,567 — it is high across the whole distribution, not on a tail).

**The floor moves, and here it is observed rather than fitted.** Both crossovers above are
extrapolations from an automatic corpus that contains no small compactions: 0 of 1,522 automatic
events started below 58,000 tokens, and 0 of them grew. The 58 **manual** events do reach down —
their minimum pre-context is 673 — and they settle it directly:

| pre | post | grew? |
|---|---|---|
| 673 | 14,114 | yes |
| 13,716 | 24,075 | yes |
| 15,602 | 17,015 | yes |
| **16,534** | **14,090** | **no** |
| 17,757 | 25,172 | yes |
| 74,139 | 24,091 | no |

14 of 58 manual compactions returned a larger context than they were given, and every one of them
started below 17,757 tokens. So the crossover is around **17,000–20,000**, not 57,700, and the
~58,000 hard-hold row was refusing compactions in the 20k–58k band that measurably work. That is a
conservative error rather than a dangerous one, which is exactly why it survived: nothing breaks
when a gate declines to compact a small session.

**One confound, stated because it runs against the finding rather than for it.** These summaries
were produced with Relay's compaction-quality addendum spliced into the summarisation prompt, which
asks for *more* to be carried across — verbatim constraints, corrections and rejected approaches.
That should inflate the residue, and the measured residue is smaller than the older fit predicts.
A stock corpus would be expected to sit lower still.

## What a compaction costs in wall-clock

Measured from transcript timestamps across **219 real compaction events**: the turn spanning a
compaction takes a median of **171.6 s**, against **12.1 s** for an ordinary turn — roughly
**160 seconds of extra waiting per compaction**. This is why "blocking is for buying minutes at 60%
full" is literally minutes, and it is the cost axis the token-only view of compaction cannot see.
The full time-priced analysis (which moved Relay's context budget off the token-only optimum) is in
`perch/docs/features-for-triage/context-budget-recommendation.md`.

## One signal dominates the holds, and holds are rare

Perch's `CompactionAdvisor` scored 1,089 real turns for whether a compaction would be safe.
**1,068 of them — 98.07% — were held on `midToolChain` alone.** Its other three checks were
evaluated on the remaining 1.9% of traffic.

That is why the rubric checks the mechanical signals first and treats an open tool chain as a hard
zero regardless of anything semantic. It is also why the skill can be cheap: most of the time the
answer is decided by one boolean.

**The base rate is the other half of that number, and it is small.** Classifying the three turns
before each of 1,522 real automatic compactions:

| signal at the moment of compaction | share |
|---|---|
| an open tool chain | 4.7% |
| a skill loaded within the last 3 turns | 7.0% |
| a skill loaded within the last 8 turns | 14.8% |
| a markdown file read recently | 45.5% |

Two things follow. A scorer should expect to find nothing most of the time, and 98.07% is not a
prior for "a veto is probably warranted". And the seam signals are **flat** across the
distribution: compactions that fired within three turns of a skill load had a median pre-context of
266,383 against 267,313 for the whole corpus, so an early compaction after a skill load is not
evidence of a bad seam-picker — it is what an evenly-distributed trigger looks like when it fires
often enough.

## The boundary table is shared, not invented

The seams in `SKILL.md` are the same table `braindump/SKILL.md` uses to decide when
compaction is worth its cost. Two skills disagreeing about what a boundary is would be worse than
either of them being slightly wrong.

`taskTransition` is described in `CompactionAdvisor.swift` as "the cheapest possible boundary, and
the only one where compacting costs nothing that was not already lost" — and the field is
deliberately never computed there, because the only source is a router call and a completed-turn tap
must not add a network hop. That gap is what this skill fills.

## What an ordinary summary loses

Scored across **121 real compaction events** (`braindump/scripts/score_retention.py`):

| class | retained by the built-in `/compact` | events |
|---|---:|---:|
| rejected approaches | 0.3% | 68 |
| standing constraints | 33.8% | 74 |
| user corrections | 63.1% | 34 |
| exact identifiers | 48.6% | 120 |
| file paths | 16.4% | 119 |

Constraint-violation rates run **0%** when the governing constraint survives into the summary and
**38%** when it is dropped.

This is why `FACTS` exists as a separate, never-pruned tier, and why the gate hands it to the
summariser rather than trusting the summariser to rediscover it.

## Why the log is append-only

Incremental summarisation decays, and the decay is measured:

- **SUMIE** (COLING 2025) — factuality on incremental entity summarisation tops out around
  **F1 80.4%** for state-of-the-art systems and falls over successive turns.
- **BooookScore** (ICLR 2024) — incremental updating scores **82.4** on coherence against **90.8**
  for hierarchical merging; it keeps more granular detail and loses structure.

So `session_log.py` has no rewrite mode and no compress mode. A log that summarises itself is a
summary of a summary, and by the third pass a precise constraint has become a generic recap.
Appending is what keeps FACTS trustworthy.

The two-tier split — an immutable fact store beside a lossy narrative — is the pattern
[ActiveGraph](https://arxiv.org/html/2605.21997v1) uses for the same reason: treat the append-only
event log as the source of truth and let only the narrative layer be lossy.

## Why reasoning comes before the score

Small models asked directly for a number anchor on the first plausible digit and rationalise
afterwards. The G-Eval line of work finds that forcing explicit step-by-step deduction against a
rubric *before* the score materially improves reliability, and that constrained JSON with the
reasoning key ordered first is what makes that stick in a programmatic harness
([W&B](https://wandb.ai/site/articles/exploring-llm-as-a-judge/)).

Binary outcomes are more stable still for small models ([Arize](https://arize.com/guides/llm-as-a-judge/)),
which is why the 0–10 scale carries an explicit anchor for each band and a coarse `verdict` field
alongside it — the band is what callers should branch on.

## Why a boundary beats a threshold

Trajectory-level supervision that compresses at "appropriate milestones" rather than on a passive
threshold reached **57.6% solved on SWE-Bench-Verified** (CAT / SWE-Compressor,
[arXiv:2512.22087](https://arxiv.org/abs/2512.22087)), outperforming ReAct agents on static
heuristics.

Aider reaches the same conclusion from the other direction: rather than waiting for a token limit to
force a lossy `/compact`, its `/handoff` command lets the operator declare the boundary
([docs](https://aiderdesk.hotovo.com/docs/features/handoff)).

## Compaction is the weak option

Measured against other context-management strategies, summarisation is the weakest: roughly
**+2.6 to +2.7 points** on task success, and *negative* for one frontier model, where moving work
into tool calls bought **+9.4 to +13.3**. Masking old tool outputs matched summarisation's solve
rate at about half the cost. (Cited in `braindump/references/evidence.md`.)

A high score therefore means compacting here would be *cheap*, never that it is *worth doing*.

## The hook contract, verified first-hand

Read out of the installed Claude Code 2.1.226 binary rather than from documentation, because the
blog sources disagree on details that decide whether a hook works at all:

- `blocked = (exitStatus === 2) || (parsedStdout.decision === "block")`.
- On exit 2 the reason is read from **stderr**; on exit 0 + `decision: block` it comes from `reason`.
- On exit 0, `newCustomInstructions` is built from the hook's **raw stdout** —
  `results.filter(succeeded && !blocked && output.trim()).map(output.trim()).join("\n\n")`. There is
  no `hookSpecificOutput.newCustomInstructions` path for this event, so a JSON envelope is handed to
  the summariser verbatim.
- **Exit 1 is a warning, not an abort.** Compaction proceeds.
- A blocked PreCompact hook aborts compaction on all three paths: precomputed
  (`Precomputed compact blocked by PreCompact hook`), reactive (returns `hookBlocked: true`) and
  manual (throws, with a "compaction blocked by PreCompact hook" banner).
- The matcher is matched against the **trigger** (`matchQuery: e.trigger`), so a hook needs both
  `manual` and `auto` to cover every event.

## Known gaps

- **No measured effect on task success.** Nothing here shows that vetoing a mid-task compaction
  produces better work than allowing it. The evidence says the loss is real and the boundary is
  cheaper; it does not close the loop.
- **Small-model agreement is unmeasured on real transcripts.** The rubric is built on what raises
  reliability in the literature, not on a scored corpus of this operator's own sessions.
- **The headroom estimate is an estimate.** `precompact_gate.sh` reads transcript bytes and divides
  (~3.5 chars/token, rounded toward over-counting because the safe failure is firing the wall rule
  early); it is a floor for deciding whether to veto, never a figure to render.
- **The residue is not predictable per compaction.** R² 0.045 on the 7-day recount: knowing the
  pre-context tells you almost nothing about the post-context beyond "roughly 30,000". The band —
  14,000 to 38,000 — is the reproducible part; the fitted line is not.
- **Both residue corpora are one machine, one operator.** The 7-day recount is 3,778 transcripts
  across many projects, which is breadth of work rather than breadth of installation, and its
  summaries carry a non-stock summarisation prompt (see the confound above).
- **A gate's silence was not checked for four months.** The inertness check in `SKILL.md` exists
  because a `PreCompact` gate ran on 1,522 consecutive compactions without vetoing one, and nothing
  in the design would have surfaced that. Any rule here that depends on a caller supplying a fact —
  the window, the model, the session — can fail the same way, and only an outside check finds it.
