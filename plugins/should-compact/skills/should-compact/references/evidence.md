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

## The residue is affine, and the flat "~51k" reading is wrong above small contexts

Fitted on **1,037 compaction events** across the same 90 days:

```
post_context ≈ 50,958 + 0.117 × pre_context
```

Two consequences, and they pull in different directions:

- **The floor stands.** Compaction shrinks the context only when `pre > ~57,700` — the fitted
  crossover, independently confirming the ~56–58k hard-hold row on a sample 4.4× larger than the
  one that set it.
- **"It leaves ~51,000 behind" is only true at the floor.** At a 250k context the residue is ~80k;
  at the 1M wall it is ~168k — 3.3× the intercept. Any reasoning about how much runway a compaction
  buys must use the relation. The fit is noisy above the floor (R² ≈ 0.25 on the earlier n=190
  sample), so treat the slope as central tendency, the floor as solid.

## What a compaction costs in wall-clock

Measured from transcript timestamps across **219 real compaction events**: the turn spanning a
compaction takes a median of **171.6 s**, against **12.1 s** for an ordinary turn — roughly
**160 seconds of extra waiting per compaction**. This is why "blocking is for buying minutes at 60%
full" is literally minutes, and it is the cost axis the token-only view of compaction cannot see.
The full time-priced analysis (which moved Relay's context budget off the token-only optimum) is in
`perch/docs/features-for-triage/context-budget-recommendation.md`.

## One signal dominates

Perch's `CompactionAdvisor` scored 1,089 real turns for whether a compaction would be safe.
**1,068 of them — 98.07% — were held on `midToolChain` alone.** Its other three checks were
evaluated on the remaining 1.9% of traffic.

That is why the rubric checks the mechanical signals first and treats an open tool chain as a hard
zero regardless of anything semantic. It is also why the skill can be cheap: most of the time the
answer is decided by one boolean.

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
- **The residue slope is central tendency, not a prediction.** R² ≈ 0.25 above the floor; a given
  compaction's residue varies widely around the affine fit. The floor is the reproducible part.
