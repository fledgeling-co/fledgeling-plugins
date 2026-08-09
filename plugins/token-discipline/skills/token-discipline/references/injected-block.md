# The injected block — v4

Everything between the fences is the literal. Perch writes it into the request's `system` field at
session start; a Claude Code install can paste it into `CLAUDE.md` or an output style. It is a
**literal**. No interpolation, no clock, no session id, no account name, no counter.

Byte count is pinned by a test (881). Changing the text means bumping the version and the pinned
number in the same commit — see `SKILL.md § Editing the block`.

```text
Report only deltas on plans, diffs, conclusions and explanations you have already shown; restate
them when asked, or to correct them.

Say in one sentence what you are about to do before the first tool call, then update only on a
finding, a change of direction, or a blocker. Lead the final message with the outcome.

Match a written file's length to what the task needs. No filler sections, no redundant summaries.

Keep direct lookups and sequential work in this thread. Delegate only large, genuinely independent
work; do not delegate verification.

Search first, then open the part you need.

This changes how much you write, never how much you do. Investigate, plan and verify as you
otherwise would, and take the steps the task needs.

Cut restatement, never reasoning. Uncertainty, caveats, security warnings, destructive-action
confirmations and required verification stay.
```

## Notes for whoever maintains this

**Why clause 6 exists, and why it is the whole point of v4.** Measured on diolog-swe-bench, the
caveman skill cut cost 33.5% on Opus 5 — and 78% of that saving came from the agent taking *fewer
steps* (24.5 → 16.5 per task), not from terser prose (tokens per step fell only 13.6%). Task score
fell 7.6 points with it. A block that shortens writing without saying so will be read as permission
to shorten working, because shortening the work is by far the cheaper way to satisfy it. Clause 6 is
the only clause here whose job is to *prevent* a saving.

**Why there is no register instruction.** No "be terse", no "drop articles", no fragments. Brevity
instructions have a measured accuracy cost (Renze & Guven, arXiv:2401.05618; Giskard Phare), and
telegraphic register does not reliably save tokens under BPE anyway — common function words are
single tokens, so dropping an article saves exactly one. See `evidence.md`.

**Why there is no version string in the text.** It would be useful at 3am and it costs prefix bytes
to learn something the proxy already logs. Perch logs the block version per turn; the model does not
carry it.

**Why no MUST, ALWAYS or CRITICAL.** Current models over-trigger on that register. The sourced form
of that claim is narrower than it is usually quoted as — Anthropic's prompting guide says it of Opus
4.5/4.6 and specifically about **tool and skill triggering**, not about every instruction on every
model — but the direction still holds for a block whose whole job is to be a default rather than a
demand. Every clause here is a statement about how the session works, with somewhere to go other
than over-complying.

**Why clause 2 grants a preamble rather than banning one.** Anthropic's own mitigation for the Opus 5
"tool call emitted as text" artifact is to give the model explicit permission to speak before a tool
call. Caveman forbids exactly that ("No preamble, plan, or progress note before or between calls"),
which runs against the documented fix. The cadence in clause 2 is Anthropic's recommended shape.

**Why the delegation clause names the exception in evaluable terms.** "Large, genuinely independent"
is something the model can assess. Without a recognisable exception the clause over-triggers in the
other direction and a genuinely parallel investigation gets crammed in-thread, which costs far more
than the hops saved. `do not delegate verification` is there because delegated verification is the
expensive kind: it pays a fresh prefix to re-derive context the main thread already has.

**Why the last line enumerates what survives.** Without it, a model told to spend fewer tokens prunes
caveats and reasoning first — cheapest to cut, most expensive to lose, and invisible in any per-turn
metric. Naming security warnings, destructive-action confirmations and required verification is not
padding: those are the three a token metric actively rewards dropping.

**What was considered for v4 and left out.** A preservation clause ("reproduce code, commands, paths,
identifiers and error strings exactly; keep every negation") — caveman's single best rule. It is
omitted here because this block never instructs prose compression, so mangled code is not a failure
mode it creates. Paying ~130 prefix bytes to insure against a risk another design carries is the
kind of drift the byte ceiling exists to stop. Restore it if a register clause is ever added.

## v3 — retained for replay, not for use

PERCH-0327 pins the block per conversation and replays the exact bytes that conversation started
with, so a conversation opened before v4 must keep emitting v3's 736 bytes for the rest of its life.
The literal below is retained verbatim in `TokenDisciplineBlock.v3Text`, and its digest is pinned by
a test. **It is not the current block — do not edit it, and do not copy from it when editing v4.**

```text
Report only deltas on plans, diffs, conclusions and explanations you have already shown; restate
them when asked, or to correct them.

Say in one sentence what you are about to do before the first tool call, then update only on a
finding, a change of direction, or a blocker. Lead the final message with the outcome.

Match a written file's length to what the task needs. No filler sections, no redundant summaries.

Keep direct lookups and sequential work in this thread. Delegate only large, genuinely independent
work; do not delegate verification.

Search first, then open the part you need.

Cut restatement, never reasoning. Uncertainty, caveats, security warnings, destructive-action
confirmations and required verification stay.
```

## v1 — retained for replay, not for use

Same contract, one generation further back. Retained verbatim in `TokenDisciplineBlock.v1Text`.

```text
Session defaults.

Everything already in this conversation is cached and cheap to keep. Re-emitting or rewriting
settled content is the expensive operation — repetition costs, not length. So point at what is
already in context rather than restating it, leave correct text alone unless a fact in it changed,
and don't re-summarise a plan or diff you have already shown.

Work stays in this thread unless a subtask genuinely needs its own context window, or is a wide
independent search whose intermediate output you don't need to see. Each delegation pays for a fresh
prefix, so a small hop can cost more than the answer.

Read narrowly: search first, then open the part you need. Opening a whole file to find one fact is
the largest avoidable cost in a session.

One artifact, once. No trailing verification pass — you already check your own work, and a second
one spends tokens without changing the answer.

When something has to go, cut restatement, never reasoning. The recap is disposable; the caveat and
the why are not.
```

**There is no v2.** It was drafted and never shipped, so no conversation was ever pinned at it. A
row naming `blockVersion: 2` is unreproducible and fails open to the caller's original bytes.
