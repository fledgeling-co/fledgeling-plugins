<img src="assets/banner.png" alt="discipline" width="100%" />

# discipline

**Stop an agent buying cheap tokens with worse work.** A ~220-token block for the start of a session, plus the measured reason every line of it says what it says.


## The problem

The obvious way to cut an AI coding agent's bill is to make it talk less. There is a popular skill that does exactly that, and it is honest about its own numbers: about 8.5% off output tokens on real agentic work, against 65% on chat-style prose.

Run it on a real benchmark and something worse than "only 8.5%" shows up.

Across 106 tasks measured twice each on Claude Opus 5, the compressed-prose skill cut cost by a third, and cut task success by 7.6 points. Digging into where the saving came from explains why. The agent's steps per task fell by 33%. Its tokens *per step* fell by only 14%. So roughly **78% of the "saving" was the agent doing less work**, not writing more briefly.

That is the trap. Told to spend fewer tokens, the cheapest way to comply is to investigate less, and every token metric rewards it while the work quietly gets worse.

## What this does instead

It never asks for shorter prose. It targets the things that actually cost: restating what is already on screen, opening whole files to find one fact, and handing small jobs to sub-agents that each pay for a fresh context.

And it carries one clause the measurement bought:

> This changes how much you write, never how much you do. Investigate, plan and verify as you otherwise would, and take the steps the task needs.

Every other line can be satisfied by simply doing less. That one says not to.

## Does it actually work

Two separate checks, and they agree on the diagnosis.

**The benchmark.** 106 tasks, both arms, Claude Opus 5, graded by the benchmark's own rules.

| | baseline | compressed prose |
| --- | --- | --- |
| Task score | 63.3% | 55.7% |
| Cost | $229.02 | $152.34 |
| Steps per task | 24.5 | 16.5 |

48 tasks got worse, 15 got better. On short tasks the effect vanishes (13 worse, 10 better, which is statistically nothing). On tasks taking 20 or more steps it is decisive: **34 worse, 4 better**.

**The blind taste test.** 14 real pairs of finished work, three different AI judges from three different companies, none told which was which or what the benchmark thought.

| Judge | preferred baseline | preferred compressed |
| --- | --- | --- |
| Claude | 11 | 2 |
| GPT | 10 | 4 |
| Grok | 8 | 6 |
| **Total** | **29** | **12** |

All three leaned the same way, on a coin-flip-unlikely margin.

## Honest limits

- **It has not been shown to save money.** On a 106-task arm it scored level with no block at all (61.6% against 63.3%, p = 0.90) and cost 32.6% more. The quality half of the claim is measured and holds; the saving half is not, and that arm ran one sample per task against the baseline's two, so the cost figure is unresolved rather than settled. Read [EVALS.md](EVALS.md) before switching it on expecting a lower bill.
- Whether this block beats its own previous version is not measured either.
- The persona-length research behind the size target was run on much smaller models. It is a reason to keep the block short, not proof about Opus 5.
- The compressed-prose skill this replaces is **not** overselling itself. Its README reports the 8.5% figure, links an independent study, and warns savings can go negative. The disagreement is with its rules, not its marketing.

## Install

```
/plugin install discipline@fledgeling-plugins
```

## Credit

The idea of a terse-output skill, and the honest agentic number that started this investigation, come from [caveman](https://github.com/JuliusBrussee/caveman) by Julius Brussee (MIT). The independent measurement that first showed the gap between 65% and 8.5% was published by [JetBrains](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/).

## Deeper

- [`SKILL.md`](skills/discipline/SKILL.md): why each clause earns its bytes, and what was rejected
- [`references/evidence.md`](skills/discipline/references/evidence.md): every number, with what it rests on
- [`references/injected-block.md`](skills/discipline/references/injected-block.md): the literal itself
- [`EVALS.md`](EVALS.md): the deep half of the comparison, with the caveats stated
- [`docs/blind-panel/`](docs/blind-panel/): the raw verdicts and the withheld key
- [`docs/deep-research/`](docs/deep-research/): the four research reports behind it
