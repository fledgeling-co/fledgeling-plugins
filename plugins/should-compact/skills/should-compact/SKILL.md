---
name: should-compact
description: >
  Score 0-10 whether NOW is a good moment to compact a coding-agent session, and say why in one
  line. Use this before running /compact, whenever a session feels long or expensive, when deciding
  whether to keep going or start fresh, when a PreCompact hook needs to decide whether to allow an
  automatic compaction, and whenever someone asks "should I compact", "is now a good time",
  "is this a good place to stop", "can I compact here" or "why did it compact in the middle of
  that". Reads only the last few turns plus an append-only session log it maintains itself, so it
  stays cheap enough to run on Haiku-class models and fast enough to sit in a hook. Scores the
  BOUNDARY, not the token count: an open tool chain or a half-finished edit is a hard zero however
  full the window is. Pairs with braindump, which writes the summary once this says go, and
  uses the session log as extra grounding. Not for writing the summary itself, and not a token
  budget — for where to CAP a conversation, that is a different decision.
license: MIT
---

# should-compact

Compaction is the lossiest operation an agent session has, and harnesses fire it on the wrong
signal. Claude Code compacts on **token pressure**: measured across 235 real events on this
operator's machine, the median compaction fired at **998,289 tokens of a 1M window — 99.8% full**.
A later 90-day recount (n=258 main-chain events) put the median at 987,636 — same finding, larger
sample. Token pressure knows nothing about whether the agent is between tasks or three files into
a refactor.

**Read that as a fraction of the wall, never as an absolute.** The wall moves: a proxy that arms
`autoCompactWindow` or `CLAUDE_CODE_AUTO_COMPACT_WINDOW` sets it, and once one does the same
"compacts when full" behaviour arrives at a much smaller number. Recounted over seven days and
3,778 transcripts on the same machine, **1,522 automatic compactions had a median pre-context of
267,313 tokens** — a quarter of the earlier figure, from an identical trigger against a lower wall.
Every headroom judgement here is therefore made against the caller-supplied wall, and a gate that
substitutes the hardware window for it will read a session at its limit as one with 700k to spare.

This skill scores the thing token pressure cannot see: **is the work at a seam right now?**

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It binds the five signals and the score/verdict/block consistency rules to a readback before the object is emitted, because the PreCompact hook branches on `score` alone. Other models skip it.

## What you produce

Two things, in this order. The reasoning comes first because writing the deduction before the
number is what makes a small model's score stable — asked for a bare score it anchors on the first
plausible digit and rationalises afterwards.

```json
{
  "reasoning": "Last turn wrote plan-0406.md and exited plan mode. No tool call is open. Two files were read this session and neither is half-edited. Log shows the research phase closed at 12:04.",
  "signals": {"open_tool_chain": false, "unsaved_edit": false, "active_error": false, "below_floor": false, "at_the_wall": false},
  "boundary": "planning→implementation",
  "score": 8,
  "verdict": "compact",
  "block": false
}
```

Then one line for a human:

> **8/10 — good moment.** Planning just closed and the plan is on disk, so the research bulk is
> spent and the distillate is already outside the context.

`verdict` is `compact` (7-10), `wait` (4-6) or `hold` (0-3).
`boundary` names the seam from the table below, or `null` when there isn't one.

## The score and the action are different questions

`score` answers *is this a good moment* — a judgement about the work.
`block` answers *should this compaction be stopped* — a decision about the window.

Most of the time they agree, and it is tempting to treat them as one field. They come apart in the
case that matters most, and getting this wrong is the failure this skill was caught making:

**A low score is not a licence to block when there is no window left.** Automatic compaction fires
at a median **99.8% of the window** (measured, n=235). By the time the trigger arrives the session
has almost nothing left to spend, so blocking does not buy a better moment — it buys a hard
overflow, and the work is lost rather than summarised. When `at_the_wall` is true, report the score
honestly and set `block: false` with the reason.

Blocking is for buying minutes at 60% full. It is never for refusing at 99%.

## What you read

Two layers, and deliberately nothing else. The whole point is to stay cheap enough to run often.

1. **The hot buffer** — the last 5-10 turns verbatim. This carries the only thing that matters
   most of the time: whether a tool call is open and whether an edit landed.
2. **The session log** — `~/.claude/should-compact/<session-id>.md`, which you also append to on
   every run. See below.

Do not read the full transcript. If the hot buffer and the log cannot answer the question, say so
in `reasoning` and score conservatively rather than going and fetching more.

## The rubric

Check the mechanical signals first. They are cheap, they are decisive, and they dominate: across
1,089 real turns of a comparable advisor, **98.07% of every hold came from one signal alone** — an
open tool chain. Get that one right and most of the job is done.

**Expect most moments to be clean, and do not go looking for a veto.** That 98.07% is the share of
*holds*, not how often a hold is right. At the moment 1,522 real automatic compactions actually
fired, an open tool chain was present **4.7% of the time**; a skill had been loaded within three
turns **7.0%** of the time. A scorer that assumes the interesting signal is usually there will
manufacture it, and the four vetoes below are the whole list.

**Hard hold — score 0-3 whatever else is true:**

| signal | why it is a veto |
|---|---|
| a tool call is open, or a `tool_result` is pending | compacting splits the pair; the model resumes without the result it asked for |
| an edit is in flight — file read, change described, not yet written | the exact line numbers and variable names are what a summary throws away first |
| an error is actively being debugged | the traceback is the working state |
| context is below ~20,000 tokens | a compaction lands somewhere near 14,000-38,000 whatever it started from, so below this it makes the context **larger** — observed directly, not fitted |

A compaction never returns an empty window, and what it returns is **nearly a constant**. Across
1,522 automatic compactions the residue tracked the input barely at all — `26,783 + 0.015 x pre`,
R² 0.045 — with a median of 31,189 tokens whether the session came in at 180k or 900k. The earlier
affine reading (`50,958 + 0.117 x pre`) over-predicts this corpus by a median of 52,510 tokens, and
it moved the floor with it: fitted, the crossover sat at ~57,700; observed, every compaction that
grew its context started below 17,757 tokens and one at 16,534 already shrank. `references/evidence.md`
carries both fits and the reason to prefer the second.

So a compaction is close to "you get about 30,000 tokens back, whenever you take it". Between
~20,000 and ~58,000 tokens the older floor held back compactions that measurably work — a
conservative error, but an error. Above that the practical question is not how much survives; it is
what survives, which is what the boundary table is for.

Set `at_the_wall` when the session is within roughly 40,000 tokens of its limit. It does not change
the score — the moment is as bad as it is — but it forces `block: false`, for the reason above.

**The score has to agree with the signals you just wrote.** If every hard-hold signal is `false`,
the score is **4 or above** — 0-3 is reserved for the four vetoes in that table and nothing else.
"The work feels unfinished" is not one of them; that is what 4-6 is for. This is worth checking
before you emit, because the score and the signals are read by different callers and a row where
they disagree is worse than either being slightly off: a gate branching on `score` would veto a
session that the signals say is perfectly safe to compact.

**Score 4-6 — nothing is broken, nothing is finished.** Reading, mapping the repo, gathering
requirements, mid-exploration with no mutation plan formed yet. Compaction here is not dangerous, it
is just premature: you would pay three minutes to lose exploration you are still using.

**Score 7-10 — a real seam.** Use this table; it is the same one `braindump` scores
summaries against, so the two skills agree about what a boundary is:

| boundary | score | why |
|---|---|---|
| a failed approach abandoned, with its reason recorded | 9-10 | the dead-end reasoning is pure cost now, and the one thing worth keeping is a sentence |
| research → planning | 8-9 | research bulk is spent; the plan is the distillate |
| planning → implementation | 8-9 | the plan is in a file, so the context is recoverable from disk |
| debugging → next feature | 8 | traces pollute unrelated work |
| a named sub-task verified complete — tests green, commit made | 7-8 | the artifact is on disk and the path to it is short |
| implementation → testing | 5-7 | keep it if the tests reference code you just wrote |

Score the seam you can **evidence** from the buffer or the log. A boundary you infer from vibes is
the failure mode this rubric exists to prevent — if you cannot point at the turn that closed the
phase, you are looking at 4-6, not 8.

Name the **most specific** row that fits. An abandoned approach is not "research→implementation";
it is its own row, and it scores higher precisely because what is being dropped is reasoning that
has already been superseded rather than work that might still be referred to.

## The session log

Append one block per run. Never rewrite an earlier block, and never summarise the log into itself.

That rule is doing real work. Incremental summarisation measurably decays: on the SUMIE benchmark
factuality tops out around **F1 80.4%** and falls with each pass, and BooookScore records
incremental updating at **82.4** coherence against **90.8** for summarising chunks independently.
A log that rewrites itself is a summary of a summary of a summary, and by the third pass a precise
constraint has become a generic recap. Appending is what keeps it honest.

Two sections, because they decay differently:

```markdown
## FACTS
<!-- append-only, never rewritten, never pruned -->
- CONSTRAINT: "no Swift without a fresh decision" — 2026-08-10T12:04Z
- REJECTED: launcher wrapper — lifeline already owns ~/.local/bin/claude
- CORRECTION: budget is stated in tokens, not a percentage
- ID: docs/specs/spec-PERCH-0406.md · PERCH-0406 · f81bacc

## NARRATIVE
- 12:41Z · 8/10 · planning→implementation · plan written, no tool open
- 13:02Z · 2/10 · hold · mid-edit across 3 files
```

**FACTS is the tier that must never be lossy** — constraints, corrections, rejected approaches with
their reasons, and exact identifiers. These are the items a successor cannot re-derive, and
`braindump` measured what happens to them under an ordinary summary: rejected approaches
survive at **0.3%**, standing constraints at **33.8%**. Anything you put in FACTS survives because
it is never rewritten.

**NARRATIVE is allowed to be lossy.** One line per run. It exists so the next run can see the shape
of the session without re-reading it.

`scripts/session_log.py` does the append and the tail read. Use it rather than hand-editing, so the
format stays parseable.

## Running as a PreCompact hook

This is where the score earns its keep: automatic compaction fires at the wall with no idea what the
agent is doing, and a hook can stop it.

`scripts/precompact_gate.sh` is the hook body. Claude Code's contract, verified against 2.1.226:

- **exit 2** → compaction is blocked; the reason is read from **stderr**.
- **exit 0** with `{"decision":"block","reason":"…"}` on stdout → also blocked.
- **exit 0** with plain text on stdout → the text becomes `newCustomInstructions` and compaction
  proceeds. Not JSON: the raw stdout *is* the instruction string, so an envelope gets handed to the
  summariser verbatim.
- **exit 1** → a warning. Compaction proceeds anyway. This is the trap; it is not an abort.

Install it with `hooks.PreCompact` on both matchers, `manual` and `auto` — the matcher is matched
against the trigger, so a hook on one covers half the events.

### A silent gate is not a gate that agreed

A `PreCompact` hook that never blocks looks exactly like a hook that examined every compaction and
approved it. Both produce no output and a clean exit 0, so the failure is invisible for as long as
nobody looks — and it has happened: a gate installed on both matchers, invoked on every one of
1,522 automatic compactions across seven days, vetoed **none** of them, because the session fact it
branched on was looked up by an id its caller does not have. Its own veto text appeared **zero**
times in 3,778 transcripts.

So prove the gate speaks, and prove it from outside itself. Two checks, both cheap:

```bash
# 1. Has it ever vetoed? Its own refusal text, in the transcripts, over a period you know
#    had compactions in it. Zero hits over hundreds of compactions is a broken gate.
grep -rl "<the exact string your gate writes to stderr>" ~/.claude/projects --include='*.jsonl'

# 2. Does it veto NOW? Feed the real hook body a real payload and read the exit code.
printf '{"session_id":"<a real one>","transcript_path":"<its transcript>",
        "hook_event_name":"PreCompact","trigger":"auto","custom_instructions":""}' \
  | <the exact command in settings.json>; echo "EXIT=$?"
```

Exit 2 with a reason on stderr is a live gate. Exit 0 at a context you expected it to hold is the
finding. Run the second check whenever the gate gains a new input — a session id, a model, a budget
— because that is when it acquires a new way to silently resolve nothing.

**Point `SHOULD_COMPACT_WINDOW_TOKENS` at the wall that actually binds.** The default is the model
window, which is right on a stock install. When a proxy enforces a lower context budget (Relay ships
one, stated in tokens), the enforced budget *is* the wall: auto-compaction fires there, so a gate
still reasoning about the 1M hardware limit computes headroom against a wall the session can never
reach and its at-the-wall rule goes inert. Set the variable to the enforced budget and everything
downstream — headroom, the never-veto rule, the block decision — stays correct without other change.

**Relay's managed minimum is 350,000 tokens.** When Relay supplies this variable, it writes its
current enforced floor (350,000 or higher), not an estimate from the transcript. This skill must use
that exact caller-supplied wall and must not clamp it upward or downward: raising an unknown 220,000
wall to 350,000 would make the gate veto at a wall it has already crossed, while lowering a supplied
350,000 wall would reintroduce the premature compactions the setting prevents.

The gate blocks only when `block` is true, which is the score AND the window agreeing — see "The
score and the action are different questions" above. `precompact_gate.sh` enforces the same rule
independently, by reading the transcript size, so a scorer that gets it wrong still cannot veto at
the wall.

## Handing off to braindump

When the verdict is `compact`, the session log is the best grounding available for the summary that
follows — FACTS is already the pinned tier `braindump` asks for, extracted incrementally
while the session was still fresh rather than reconstructed at the end from a 1M-token transcript.

Pass the log path to `/braindump:braindump`, or let the PreCompact hook emit the
FACTS block as `newCustomInstructions` so it lands in the summarisation prompt directly.

## What this is not

- **Not a token budget.** Where to cap a conversation is a different decision with different
  evidence; this only answers "is right now a seam". That decision has since been measured —
  Relay ships a context budget with the analysis behind it in
  `perch/docs/features-for-triage/context-budget-recommendation.md` — and the two compose: the
  budget picks the wall, this skill picks the moment short of it.
- **Not the summariser.** `braindump` writes the summary and scores retention.
- **Not a reason to compact.** A high score means compacting here would be cheap, not that it is
  worth doing. Compaction measures out as the weakest context-management strategy available —
  roughly +2.6 points on task success where moving work into tool calls buys +9.4 to +13.3. If the
  cheaper thing works (clear old tool results, write state to a file, start fresh pointed at it),
  say so.

Evidence and citations: `references/evidence.md`.
