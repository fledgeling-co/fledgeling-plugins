<p align="center">
  <img src="assets/banner.png" alt="clarify: a porcelain icon of three stacked option cards, the recommended one lit and carrying a vermilion dot while the other two sit back in shadow, with a note written in vermilion in the margin, beside the wordmark and the line: ask less, and make the asking cheap to answer" width="100%">
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> clarify</h1>

<p align="center"><strong>Ask less. Make the asking cheap to answer.</strong><br />
A SWE skill for Claude Code that decides whether to interrupt you, then writes the question so it takes one click.</p>

<p align="center">
  <img alt="Version 1.3.0" src="https://img.shields.io/badge/version-1.3.0-D33C21">
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

**With it, as of 1.3.0**

> Writing it as one migration file; everything here so far is single-file, and a single unit applies and rolls back together. Fable agreed and had nothing to add. Say the word if you'd rather split it.

Same fork. It stopped being a question, because the repo had already answered it and the parenthetical in the first version proves the agent knew that.

The question only survives when the fact that decides it is missing:

> **Does this migration carry a data backfill, or is it schema-only?**
> - **Schema-only** Runs in seconds; one file applies and rolls back as a unit.
> - **It backfills a large table** Ships the structure first and fills after, so nothing holds a lock during the backfill.

Two options, nothing marked, six words in the stem.

## How it works

Three parts, and they fail differently.

**The gate: is this a question at all?** Five steps, and the first one that resolves ends it. Sweep the conversation, the repo and earlier agent output first, because the answer is usually already somewhere. Then run a divergence test: sketch what you'd build under each reading, and if the sketches match, there's nothing to ask. That test is the one rule here with a measured result behind it; asking only on divergence lifted a code benchmark's pass rate from **70.96% to 80.80%** (p = 3.2e-05).

**Then it goes to another model before it goes to you.** Anything technical that survives the first three steps gets referred: fable-5 at high when speed is the point, then gpt-5.6-sol, gemini-3.7-flash-high and grok-4.6 at xhigh when independence is. Each lane pins its model and its effort, because a lane that inherits its config default isn't the lane you picked, and each is verified on the wire rather than trusted; an empty output file counts as a failed lane, not a quiet pass. A genuinely open, high-leverage fork goes to a three-family panel with the options in swapped order, and every member gets asked whether there's a better approach than the ones listed, because a missing option is a research failure and an out-of-family model is the cheapest thing that finds one. A question about the world (what competitors do, prior art, a vendor's actual behaviour) routes to Dossier instead, free lanes first, citations verified before anything leans on them.

**Then the last step, which is the one that changed in 1.3.0.** Not "are you sure" but "whose decision is this". If the axis is yours (craft, convention, anything reversible, anything where the alternative just loses) you take it and tell me in a clause what you took and why. If the axis is mine (taste, cost, scope, risk tolerance, my own systems) you ask, however certain you are. Certainty isn't a ticket past my axis, and it isn't a ticket past anything irreversible either.

**The craft: what does the question look like?** One call, one question by default and three at most. Question stem under 20 words. Two options, each described by what changes if you pick it. Plain words, so the choice reads as consequences rather than vocabulary.

**The handling: what happens to the answer?** You can attach a written note to whichever option you choose, and the note is binding. Pick *Postgres* and add "must run embedded, no server process" and you haven't chosen server Postgres; the skill acts on the whole answer, and says so plainly when the note and the label genuinely conflict.

> **Note:** the note is treated as data about the decision, never as instructions. Waiting on an answer is measurably the riskiest moment an agent has: across 728 scenarios and ten frontier models, prompt-injection success rose from around **2% during ordinary work to 34-36% once the agent was seeking clarification**. A note saying "must run embedded" is an answer. A note saying "ignore your previous instructions" is not.

## The recommendation went almost everywhere, and now it goes one place

The old rule had two shapes: mark an option when repo evidence earns it, mark nothing when it's a matter of taste. 1.3.0 didn't change that rule so much as collapse its territory. Once a fork the repo settles is a fork the agent settles, the "evidence earns it" case stops reaching you at all. What's left on your side of the line is the stuff nothing objective decides, which is precisely the case that was always meant to carry no mark.

So `(Recommended)` now has one home: the question you get asked *despite* the agent knowing the answer, because the action can't be undone. Dropping a table in production has a defensible recommendation and you should still be asked. There the mark goes on the reversible path, listed first, with the reason in its description and the row count in the question.

The linter enforces it. A mark on a question that hasn't declared `"irreversible": true` is a hard error, and the flag is declared rather than sniffed, because destructiveness can't be read out of prose. "Delete the stale flags this week, or quarantine them?" contains a destructive verb and is a pure scope question; a keyword rule would demand a mark on exactly the question that must not carry one.

Why bother: defaults move choices hard (pooled *d* = 0.68), and the upside of a recommendation is capped anyway, since people shift only 20-40% toward advice. Correct decision support cuts omission errors by about 40%, and incorrect support **raises** them by a quarter to a third. Small upside, large downside, and on a question about your taste "correct" isn't a category that applies.

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

**And 1.3.0 made that one worse before it made it better.** The two-option default was put to two out-of-family reviewers, and both refused it. Gemini said forcing exactly two "forces an artificial binary" wherever a domain has more than two valid strategies, and that readers anchor to clickable options rather than to prose beside them, so naming the third shape in the preamble doesn't substitute for listing it. Grok read the eval before answering and was blunter: the 4-0 "was not a missing fact a panel would fetch", and a hard cap "writes that collapse into the spec".

It shipped anyway, at two by default with a third slot when the referral earns it, because narrowing is now work the referral does rather than work the word count does. The compensating control is that every lane and panel member gets asked whether a better approach exists than the ones listed. Whether that actually recovers the 4-0 case is **unmeasured**, and it's the first thing to re-run. Both reviews are committed under [`docs/deep-research/`](docs/deep-research/) so you can read what they said rather than my summary of it.

The same reviewers changed the design in one place, which is the better advert for asking them. The gate was going to read "if you can name a recommendation, take it". Both spotted independently that this collapses into never asking: you can nearly always name a recommendation, and a reason produced after the fact turns someone else's trade-off into your decision. Grok's phrasing was that the loop closes on itself, "refer until you can recommend; if you can recommend, take it; the panel exists so you become sure". The shipped gate asks whose axis it is instead, which is a question you can get wrong in only one direction.

**What it does not do.** It doesn't make Claude safer or more thorough, and the evals say so. Four of the eight found no difference at all: Claude already sweeps the repo for a buried answer, already declines to ask about routine defaults, already treats an attached note as binding, and already refuses to run a production table-drop unasked. Those four are kept as regression guards, not as evidence. The measured value is narrower and worth stating plainly: the questions cost less to answer.

**Does it fire on its own?** Yes, on the evidence there is. Dropped into a real React app with a genuine fork, it read the repo, then triggered unprompted and asked. Given a near-miss ("explain what this hook does") it stayed out of the way. That is one of each, so it's a control rather than a trigger rate, and an earlier attempt to measure a real rate failed in an instructive way. [EVALS.md](EVALS.md) has both.

The run is worth reading for what it did after triggering: it found the actual cause of the reported bug on its own, a textarea cleared before the save request resolves, so a note written out of coverage vanishes with no error shown. Then it named two things it had decided rather than asked about, and asked one question.

Full tables, judge families, the research corpus and the caveats are in [EVALS.md](EVALS.md).

## What it's built on

Five research backends were run on one brief and their reports are committed under [`docs/deep-research/`](docs/deep-research/), so every number above is checkable from inside the repo. [`references/evidence.md`](skills/clarify/references/evidence.md) maps each rule to its source and says which numbers are measured and which are conservative defaults.

It also records where the panel disagreed with itself, and where one member sourced its claims to SEO aggregators and got them wrong. Worth reading before changing a threshold.
