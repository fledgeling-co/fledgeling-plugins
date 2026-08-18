# EVALS: should-compact

What was tested, on what, and what it proved. Every number here came from a run you can repeat;
where something is unmeasured it says so rather than leaving a gap for optimism to fill.

## The comparison

The baseline is **the same prompt with no skill at all**. That is the honest comparison for a new
skill, because it answers the only question that matters: does this earn the context it costs?

Everything ran on **Claude Haiku 4.5**, deliberately. This skill is built to sit in a hook and be
called often, so proving it on a frontier model would prove the wrong thing.

## The cases

Five situations, chosen to cover the whole scale rather than the easy ends:

| # | situation | expected |
|---|---|---|
| 0 | mid-tool-chain, an edit in flight, a test failing | 0-3, hold |
| 1 | planning just closed, plan written to disk | 7-10, compact |
| 2 | mid-exploration, still reading, nothing broken or finished | 4-6, wait |
| 3 | mid-edit **at 99.8% of the window** | low score, but **do not block** |
| 4 | a failed approach abandoned with its reason recorded | 9-10, compact |

Case 3 is the one the skill exists for, and it is the one both the baseline and the first draft of
this skill got wrong.

## Iteration 1: two real defects, found by running it

**The skill told the hook to block at the wall.** It scored 0 and instructed `exit 2`. That is the
failure the whole headroom rule exists to prevent: automatic compaction fires at a median 99.8% of
the window, so blocking there buys a hard overflow rather than a better moment. The rule was written
in the hook section and never reached the point where the score is decided.

The fix was conceptual, not cosmetic: **the score and the action are different questions.** `score`
judges the moment; `block` decides about the window. They agree almost always and come apart exactly
once, at the wall, which is precisely the case worth getting right.

**The gate was silently inert on macOS.** `precompact_gate.sh` bounded its scorer with `timeout`,
which is GNU coreutils and does not exist on macOS. Every path failed open. A hook that is
installed, armed and permanently silent is worse than one that is absent, because nothing about it
looks broken. It now falls back to `perl -e alarm`.

## Iteration 2: a rubric that disagreed with itself

Case 2 came back scored **3** with every hard-hold signal set to `false`. The rubric reserves 0-3
for four specific vetoes, so the score contradicted the signals emitted beside it, and a gate
branching on `score` would have vetoed a session the signals called safe.

Adding the invariant (*if no hard-hold signal is true, the score is 4 or above*) moved it to
**5/wait**. Case 4 gained the same way: naming the most specific boundary took it from 8
("research→implementation") to **9** ("a failed approach abandoned, with its reason recorded").

After iteration 2, all five cases land in their expected band.

## The blind panel

Anonymised A/B pairs, judges told only that two assistants answered and never that a skill existed.
Position was **balanced by construction** rather than shuffled, with the skill in slot A for three
cases and slot B for two, because an unlucky shuffle that put one side in the same slot every time
would confound the result with positional bias.

Two independent families:

| judge | wins for the skill | positions |
|---|---|---|
| Claude Fable 5 | 5 / 5 | tracked the skill across both slots |
| GPT-5.6-sol (high effort) | 5 / 5 | tracked the skill across both slots |

**10 / 10, unanimous.** The winner followed the skill rather than the slot, which is what rules out
the panel simply preferring whichever answer came first.

They judged on substance. On case 3 the GPT judge wrote that the baseline *"asserts that delaying is
safe without addressing the remaining token budget"*; the Claude judge that it *"would strand the
session if followed"*. Both picked the answer that is operationally correct, not the longer one.

## Where the baseline actually failed

Worth stating plainly, because a panel result reads as a preference and this was not:

- **Case 3.** The baseline said *"Yes, block this compaction."* Following that at 99.8% full loses
  the session instead of summarising it.
- **Case 4.** The baseline did not understand the question at all, and asked four clarifying
  questions about what "compact" meant.
- **Cases 0, 1, 2.** The baseline gave sound prose advice. It got the direction right and produced
  nothing a script could branch on: no score, no signals, no `block` field.

So the gain is two things, not one: a correctness flip on the case at the wall, and a machine-
readable verdict everywhere else.

## What is not measured

- **No effect on task success.** Nothing here shows a session that vetoed a mid-task compaction
  produces better work than one that did not. The evidence says the loss is real and the boundary is
  cheaper; it does not close that loop.
- **One run per cell.** Five cases, two arms, two judges, no repeats, so nothing here separates a
  real gap from a lucky sample on any individual case. The unanimity across two families is what
  carries the result, not any single row.
- **No real transcripts.** The cases are hand-built to be unambiguous. Agreement on this operator's
  own sessions, where the boundary is genuinely arguable, is untested.
- **Small-model spread.** Only Haiku 4.5 was run. GPT-5.6-low is named in the description as a
  target and has not been exercised.

## Reproducing

```bash
# one case, both arms
claude -p --model claude-haiku-4-5-20251001 "$(cat evals/prompt.txt)"                 # baseline
claude -p --model claude-haiku-4-5-20251001 "Follow this skill exactly.
$(cat skills/should-compact/SKILL.md)
$(cat evals/prompt.txt)"                                                              # with skill

# the session log and the gate, end to end
SHOULD_COMPACT_HOME=/tmp/sc skills/should-compact/scripts/session_log.py append \
  --session demo --score 8 --verdict compact --note "plan on disk" --fact "CONSTRAINT: ..."
```
