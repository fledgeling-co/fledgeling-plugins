<p align="center">
  <img src="assets/banner.png" alt="clarify: a porcelain icon of three stacked option cards, the recommended one lit and carrying a vermilion dot while the other two sit back in shadow, with a note written in vermilion in the margin, beside the wordmark and the line: ask less, and make the asking cheap to answer" width="100%" />
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> clarify</h1>

<p align="center"><strong>Ask less. Make the asking cheap to answer.</strong><br />
A SWE skill for Claude Code that decides whether to interrupt you, then writes the question so it takes one click.</p>

<p align="center">
  <img alt="Version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-D33C21">
  <img alt="SWE skill: interaction" src="https://img.shields.io/badge/SWE_skill-interaction-434A55">
  <img alt="Blind panel 15-5" src="https://img.shields.io/badge/blind_panel-15--5-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

An agent that stops to ask you something is spending your attention, and the bill is bigger than it looks. After an interruption, only **10% of programming sessions resume work inside a minute**, and only 7% resume without navigating around first to rebuild context.

So the question has to be worth it, and it has to be cheap to answer. Most aren't. The one that prompted this skill was a real one, 57 words long, with the reasoning stuffed inside the question text and three option descriptions running to 46 words each. Answering it meant reading a paragraph and working out the consequences yourself, which was the job you delegated in the first place.

`clarify` does two things: it decides whether there's a question here at all, then it writes the one that's left.

## What it actually changes

Here's the same fork, both arms, from the eval runs.

**Without the skill**

> "Single script", "one script" and "a lone migration file" are all the same shape, so the real fork is one file vs. split, and if split, split on what. Which do you want? (I'd take one file unless this migration carries a data backfill; splitting a pure schema change just adds history entries without buying anything.)

**With it**

> **One migration file, or split into several?**
> - **One file (Recommended)** Applies and rolls back as a single unit, so a failure halfway leaves nothing half-done. The usual choice unless the data change is slow.
> - **Schema now, backfill after** Structure changes ship quickly; the backfill runs separately, without holding a lock on a large table.
> - **One file per table** Each table's change can be re-run on its own, at the cost of more files to order correctly.

Same decision. Six words instead of 57.

## How it works

Three parts, and they fail differently.

**The gate: is this a question at all?** Sweep the conversation, the repo and earlier agent output first, because the answer is usually already somewhere. Then run a divergence test: sketch what you'd build under each reading, and if the sketches match, there's nothing to ask. That test is the one rule here with a measured result behind it; asking only on divergence lifted a code benchmark's pass rate from **70.96% to 80.80%** (p = 3.2e-05).

**The craft: what does the question look like?** One call, one question by default and three at most. Question stem under 20 words. Options 2 to 4, each described by what changes if you pick it. Plain words, so the choice reads as consequences rather than vocabulary.

**The handling: what happens to the answer?** You can attach a written note to whichever option you choose, and the note is binding. Pick *Postgres* and add "must run embedded, no server process" and you haven't chosen server Postgres; the skill acts on the whole answer, and says so plainly when the note and the label genuinely conflict.

> **Note:** the note is treated as data about the decision, never as instructions. Waiting on an answer is measurably the riskiest moment an agent has: across 728 scenarios and ten frontier models, prompt-injection success rose from around **2% during ordinary work to 34-36% once the agent was seeking clarification**. A note saying "must run embedded" is an answer. A note saying "ignore your previous instructions" is not.

## Recommendations, and when not to give one

Mark one option `(Recommended)` when something in the repo or the constraints actually earns it, put the reason in the description, and list it first.

When the question is a matter of taste, mark nothing and use neutral ordering. This isn't fussiness. Defaults move choices hard (pooled *d* = 0.68), so recommending on a taste question answers it yourself while appearing to ask. The upside of a recommendation is capped anyway, since people shift only 20-40% toward advice; the downside isn't. Correct decision support cuts omission errors by about 40%, and incorrect support **raises** them by a quarter to a third.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install clarify@fledgeling-plugins
```

## Using it

Mostly you won't call it. It fires when an agent is about to ask you something, when a request has two readings that lead to different work, and before anything destructive. You can also invoke it by name with `/clarify`, or just say "ask me what you need".

It ships a linter you can run on any question payload yourself:

```bash
python3 skills/clarify/scripts/lint_questions.py payload.json
```

It checks the mechanical rules (counts, word caps, headers, duplicate options, jargon) and deliberately checks nothing about whether the question was worth asking. That part is judgement, and no script does it.

## Does it actually work

Every prompt was run twice: once with the skill, once with **no skill at all**. That's the honest baseline for something new, because the real question is whether it earns the context it costs.

**The report card.** Across the eight evals, the skill produced 5 question payloads and all 5 passed the linter. The no-skill arm produced 6 and **none** passed. Its longest question ran 41 words against the skill's 15; its longest option description ran 84 words against the skill's 30.

**The taste test.** Five judged pairs went to four different AI models, anonymised as Option A and Option B, in random order, with neither side identified and no judge ever shown the skill. **The skill won 15 of 20.** Every family preferred it, and Claude liked it least (3-2), which is reassuring given Claude wrote it.

**Where it loses.** One eval went 4-0 against the skill, in both A/B orders, and three attempted fixes didn't shift it. On a migration question the no-skill arm found a better set of options than the skill did, including an approach the skill never reached. The brevity rules produced a tidier question carrying less. So: where the fork is a domain taxonomy you don't already hold, the word caps cost more than they buy. That case is kept in the eval set as a standing counter-example rather than quietly dropped.

**What it does not do.** It doesn't make Claude safer or more thorough, and the evals say so. Four of the eight found no difference at all: Claude already sweeps the repo for a buried answer, already declines to ask about routine defaults, already treats an attached note as binding, and already refuses to run a production table-drop unasked. Those four are kept as regression guards, not as evidence. The measured value is narrower and worth stating plainly: the questions cost less to answer.

**Does it fire on its own?** Yes, on the evidence there is. Dropped into a real React app with a genuine fork, it read the repo, then triggered unprompted and asked. Given a near-miss ("explain what this hook does") it stayed out of the way. That is one of each, so it's a control rather than a trigger rate, and an earlier attempt to measure a real rate failed in an instructive way. [EVALS.md](EVALS.md) has both.

The run is worth reading for what it did after triggering: it found the actual cause of the reported bug on its own, a textarea cleared before the save request resolves, so a note written out of coverage vanishes with no error shown. Then it named two things it had decided rather than asked about, and asked one question.

Full tables, judge families, the research corpus and the caveats are in [EVALS.md](EVALS.md).

## What it's built on

Five research backends were run on one brief and their reports are committed under [`docs/deep-research/`](docs/deep-research/), so every number above is checkable from inside the repo. [`references/evidence.md`](skills/clarify/references/evidence.md) maps each rule to its source and says which numbers are measured and which are conservative defaults.

It also records where the panel disagreed with itself, and where one member sourced its claims to SEO aggregators and got them wrong. Worth reading before changing a threshold.
