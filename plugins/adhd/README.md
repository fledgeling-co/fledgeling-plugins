# adhd

Parallel divergent ideation for coding agents; the evidence-grounded successor to [uditakhourii/adhd](https://github.com/uditakhourii/adhd).

Ask a model an open-ended design question and you'll get the answer a senior engineer gives in thirty seconds. Correct, forgettable, and the same every time; when researchers over-sampled 4,000 ideas from one aligned model, roughly 95% were semantic duplicates. This skill widens the search properly, then converges on something you'd actually ship.

Run it with `/adhd <your problem>` on architecture decisions, API surfaces, naming, product positioning, or fuzzy bugs with no known root cause. Skip it for anything with one canonical answer; the skill will skip itself anyway.

## What it does

- **Spawns isolated branches** under a balanced frame portfolio: an ordinary stakeholder, an operational constraint, an adversary, a cross-domain mechanism, and one wild seat. Branches never see each other; sharing ideas mid-flight measurably homogenises the pool, so we don't.
- **Freezes the textbook answer first.** The baseline becomes a concrete ban list for the branches, and later the bar the shortlist has to clear.
- **Converges by mechanism, not score.** Ideas are merged when they share a cause, clustered by angle, and gated on soundness, feasibility and fit. No 1-10 novelty scores; LLM judges are measurably bad at those.
- **Boss-gates the recommendation.** The starred pick has to beat the frozen baseline head-to-head on your stated problem, blind and order-swapped. If nothing beats it, the skill says so and recommends the baseline. An honest "the boring answer wins" is a feature, not a failure.
- **Stamps a receipt** on every run: tier, frames spawned, ideas merged and floored, and the verdict. A light run reads as a deliberate choice rather than a broken one.

## Why v2 exists

The original skill won 5 of 6 benchmark problems against single-shot answers, and its one loss taught us the most: the creative pick didn't solve the stated problem, and a boring shippable baseline beat it on usefulness. The boss gate exists because of that loss.

The second fix came from a field report: the 10-year-old frame turning up on deeply technical problems, producing noise next to serious work. Frames now pass a fit floor before spawning (the wild seat is exempt by design), and a frame whose entire yield fails the quality floors is dropped from the output with a note in the receipt.

Every other change traces to a measured result in the 2024-2026 LLM-ideation literature; `skills/adhd/references/evidence.md` carries the citations. The short version: diversity comes from architecture, not from temperature or from asking the model to be creative.

## Tiers

| Tier | What you get | Cost |
|---|---|---|
| `--any` | 2 frames, quick shortlist | 3-4 agent calls |
| default | 5 frames, full convergence, 3 deepened winners | 8-14 agent calls |
| `--100` | 7 frames plus a cross-cluster hybridisation pass | 14-18 agent calls |

Note: the standard tier costs 5-10x a single answer. It's for decision points where the obvious answer being wrong is expensive, not for every keystroke.

## Files

- `skills/adhd/SKILL.md`: the loop itself.
- `skills/adhd/references/evidence.md`: the research grounding, with citations.
- `skills/adhd/references/frames.md`: frame seats, the synthesis template, fit floor, apoptosis rules.
- `skills/adhd/references/convergence.md`: floors, judge-bias defences, the boss gate.
- `evals/evals.json`: six structural evals covering the failure modes v2 was built to fix.

Found a run that misbehaved? The receipt line is designed to make that diagnosable; open an issue with it included.
