<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> should-compact</h1>

<p align="center"><strong>Is now a good moment to compact? A score out of 10, and one line saying why.</strong><br />
A SWE skill for Claude Code that judges the seam in the work rather than the fullness of the window.</p>

<p align="center">
  <img alt="Version 0.2.1" src="https://img.shields.io/badge/version-0.2.1-D33C21">
  <img alt="SWE skill: sessions" src="https://img.shields.io/badge/SWE_skill-sessions-434A55">
  <img alt="Blind panel 10-0" src="https://img.shields.io/badge/blind_panel-10--0-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

Compaction is the lossiest thing that happens in an agent session, and the
harness fires it on a signal that knows nothing about your work.

Claude Code compacts on token pressure. Measured across 235 real events on this
machine, the median compaction fired at **998,289 tokens of a 1M window**, which
is 99.8% full; a later 90-day recount over 258 events put it at 987,636. Same
answer, bigger sample. Token pressure cannot see whether the agent is between
tasks or three files into a refactor, so half the time it arrives in the middle
of something.

This skill scores the thing token pressure cannot see: **is the work at a seam
right now?**

## What you get

A JSON block a script can branch on, and one sentence a human can read.

```json
{
  "reasoning": "Last turn wrote plan-0406.md and exited plan mode. No tool call is open...",
  "signals": {"open_tool_chain": false, "unsaved_edit": false, "active_error": false,
              "below_floor": false, "at_the_wall": false},
  "boundary": "planning→implementation",
  "score": 8,
  "verdict": "compact",
  "block": false
}
```

> **8/10, good moment.** Planning just closed and the plan is on disk, so the
> research bulk is spent and the distillate is already outside the context.

The reasoning comes before the number on purpose. Asked for a bare score, a small
model anchors on the first plausible digit and justifies it afterwards.

## The one rule worth knowing

**The score and the block are different questions.** The score judges the moment.
The block decides about the window. They agree nearly always, and they come apart
in exactly the case that matters.

A bad moment is not a licence to block when there is no window left. Automatic
compaction fires at a median 99.8% full, so vetoing it there does not buy a
better moment; it buys a hard overflow, and the session is lost instead of
summarised. When the session is at the wall, the skill reports the low score
honestly and refuses to block anyway.

Blocking is for buying minutes at 60% full. It is never for refusing at 99%.

That distinction is not theory. It is the failure the skill was caught making in
its own evals, and fixing it was the change that made the rest work.

## What it reads

Two layers, and deliberately nothing else, because the whole point is to be cheap
enough to run often:

- **A hot buffer** of the last 5-10 turns, which carries the only things that
  usually matter: is a tool call open, and did the last edit land.
- **A session log** at `~/.claude/should-compact/<session-id>.md` that it appends
  to on every run.

It never reads the full transcript. If those two cannot answer the question, it
says so and scores conservatively rather than going and fetching more.

The log is append-only, and that is doing real work. Incremental summarisation
measurably decays: SUMIE tops out around F1 80.4% and falls with each pass, and
BooookScore records incremental updating at 82.4 coherence against 90.8 for
summarising chunks independently. A log that rewrites itself is a summary of a
summary, and by the third pass a precise constraint has become a generic recap.

So it keeps two tiers. **FACTS** is never rewritten: constraints, corrections,
rejected approaches with their reasons, exact identifiers. Those are the items a
successor cannot re-derive, and an ordinary summary loses them (rejected
approaches survive at 0.3%, standing constraints at 33.8%). **NARRATIVE** is one
line per run and is allowed to be lossy.

## The rubric

Mechanical signals first. They are cheap, decisive, and they dominate: across
1,089 real turns of a comparable advisor, **98.07% of every hold came from one
signal**, an open tool chain.

**0-3, hold, whatever else is true:** a tool call is open, an edit is described
but not written, an error is actively being debugged, or the context is below
~58,000 tokens (below that, compaction leaves more behind than it removes).

**4-6, wait.** Nothing is broken and nothing is finished. Mid-exploration.
Compaction here is not dangerous, just premature.

**7-10, a real seam.** A failed approach abandoned with its reason recorded
scores highest at 9-10, then research→planning and planning→implementation at
8-9, debugging→next feature at 8, a verified sub-task at 7-8.

Score the seam you can point at. A boundary inferred from vibes is the exact
failure the rubric exists to prevent.

## Running it in a hook

This is where it earns its keep, because automatic compaction fires at the wall
with no idea what you are doing.

`scripts/precompact_gate.sh` is the hook body. Install it on `hooks.PreCompact`
with **both** matchers, `manual` and `auto`; the matcher is compared against the
trigger, so a hook on one covers half the events.

Two traps worth knowing. Exit 1 is a warning, not an abort, and compaction
proceeds anyway. And point `SHOULD_COMPACT_WINDOW_TOKENS` at the wall that
actually binds: if a proxy enforces a lower budget than the model window, that
budget is the wall, and a gate still reasoning about 1M computes headroom against
a limit the session can never reach.

The gate enforces the never-veto-at-the-wall rule independently by reading the
transcript size, so a scorer that gets it wrong still cannot strand you.

## What it does not do

- **It does not write the summary.** That is `braindump`, which this hands the
  log's verbatim FACTS tier to as grounding.
- **It is not a token budget.** Where to cap a conversation is a different
  decision from where to break one.
- **It does not read your transcript.** By design, and that is what keeps it
  cheap enough for a hook.

## Does it beat not having it?

Ten out of ten on a blind panel, and one outright correctness flip.

Everything ran on Haiku 4.5 deliberately, because a skill built to sit in a hook
should be proved on the model that will run it. Five cases against the same
prompts with no skill, judged blind by Claude Fable 5 and GPT-5.6-sol with
neither told a skill existed and position balanced by construction. Both families
picked the skill 5/5, and they tracked it across slots, which rules out the panel
just preferring whichever answer came first.

The gain was two things. On the case at the wall the baseline said *"Yes, block
this compaction"*, which at 99.8% full loses the session; the GPT judge noted it
*"asserts that delaying is safe without addressing the remaining token budget"*.
On the rest the baseline gave sound prose advice and produced nothing a script
could branch on: no score, no signals, no `block`.

What is not measured is in [EVALS.md](EVALS.md), including the honest gaps: no
effect on task success, one run per cell, no real transcripts, and only one small
model exercised.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install should-compact@fledgeling-plugins
```

Then ask it directly, or wire it into `hooks.PreCompact`:

```
should I compact here?
```

## Licence

MIT.
