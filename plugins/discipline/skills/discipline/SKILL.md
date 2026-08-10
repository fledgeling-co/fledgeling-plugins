---
name: discipline
description: >
  Session-start operating defaults that cut token spend without cutting task success, tuned for
  Claude Opus 5 agentic coding. Ships a byte-stable block for the cached system prefix (Perch proxy,
  CLAUDE.md, or an output style) plus the evidence behind every clause. Use when someone asks to
  reduce token usage, stop hitting usage limits, make sessions cheaper, "why is this burning so many
  tokens", asks about context or prompt-cache economics, asks whether a terse/caveman/compressed
  output style is worth running — and when authoring or editing the injected block itself. Not a
  prose-compression style: compressed register is the lever this skill exists to argue against.
license: MIT
---

# Token discipline

Most of what a session spends is not what anyone typed. Every turn resends the conversation from the
top, and cache reads bill at 0.1× base input — so the lever is not shorter prose. It is *not
resending, not re-reading, and not re-opening a fresh prefix somewhere else.*

This skill is two artifacts, and keeping them apart is the point:

| Artifact | What it is | Where it lives |
| --- | --- | --- |
| **The block** | 881 bytes (~220 tokens, v4) injected into the request's `system` field at session start | `references/injected-block.md` — verbatim, byte-stable |
| **This file** | Why the block says what it says, what was rejected, what is measured vs assumed | Read when editing the block or debugging a session |

The block is not this file compressed. It is a separate, versioned, size-pinned literal.

**v1 (1,029 bytes) and v3 (736 bytes) still exist in the code and must stay there.** PERCH-0327 pins
the block per conversation and replays exact bytes, so a conversation opened before v4 keeps emitting
its own version for the rest of its life. Deleting or tidying either re-mints every older
conversation at full price.

## The measurement this exists because of

Caveman-style response compression was run as a paired arm on this operator's own agentic coding
benchmark. Full tables in `references/evidence.md`; the headline:

| diolog-swe-bench, Opus 5 @ xhigh, 106 paired tasks | pure | caveman | Δ |
| --- | --- | --- | --- |
| Score | 63.3% | 55.7% | **−7.61 pp** |
| Cost | $229.02 | $152.34 | −33.5% |
| Steps / task | 24.5 | 16.5 | −32.7% |

48 tasks worse, 15 better (p < 0.0001). Three findings drive every design choice below.

**1. The saving was mostly the agent doing less.** Steps fell 32.7%; tokens *per step* fell only
13.6%. About **78% of the token saving is the agent taking fewer steps**, not writing more tersely.
A cheaper run that investigated less is not an efficiency gain wearing a different hat — it is the
same task done worse, and every token metric rewards it.

**2. The harm is concentrated in long work.** On tasks the pure arm finished in 10–19 steps: 13
worse, 10 better, p = 0.68 — no effect. On tasks taking 20+ steps: **34 worse, 4 better, p < 0.0001**.
Short chat-shaped work is where compression is harmless. Long agentic work is where it bites.

**3. The register barely applied anyway.** Caveman forbids decorative structure; **97.5% of its runs
still emitted markdown**, against 98.9% for pure. You pay the instruction-following tax and the
behavioural distortion, and mostly do not get the register.

Independently, JetBrains measured caveman on Sonnet 5 at low effort: −8.5% output tokens against a
65% headline, the skill arm **11.6% more expensive overall**, and no quality difference (p = 0.82).
That null and the regression above are consistent: harmless on short low-effort work, harmful on long
high-effort work.

**Caveman is not overclaiming.** Its current README reports 8.5% for agentic runs, links the
JetBrains study, and warns savings "can go net-negative". The disagreement here is with its rules,
not its marketing.

## Why placement decides everything

The prompt cache matches an **exact byte prefix**. That gives two places to put a preamble, with
opposite economics:

- **In the cached prefix (the `system` field):** paid once per cache window, read cheap forever after.
  Any change invalidates the whole prefix and resends the conversation at full price.
- **After the last cache breakpoint:** costs 1.0× its own tokens *every turn, forever*.

So the block goes in the `system` field and is **byte-identical for the life of the session** — no
timestamp, no session id, no account name, no counter, no model-visible version string. The moment
something in it varies, it stops being a preamble and becomes a cache-miss generator.

**The most expensive thing this feature could do is edit itself.**

On Claude Code specifically: a *skill* injects as a user message at invocation, which is cache-safe
but not persistent. An *output style* modifies the system prompt and triggers native adherence
reminders — but it drops Claude Code's built-in software-engineering instructions unless
`keep-coding-instructions: true` is set, and it does not reach subagents. For a fan-out workload,
proxy injection is the only delivery that reaches every session.

## What the block covers, and why each clause earns its bytes

Ordered by how many tokens it moves. Every clause has to do something Claude Code's own system prompt
does **not** already do — scope discipline and correction narration ship near-verbatim there, so they
are omitted rather than paid for twice.

**1. Report deltas, not restatements.** The largest clause by expected saving: don't re-emit plans,
diffs, conclusions or explanations already in the conversation. It states the rule and names its
escape hatches (restate when asked, or to correct) rather than teaching a cache mechanism it would
have to qualify.

**2. Progress narration, bounded — and permitted.** One sentence before the first tool call, updates
only on a finding, a change of direction, or a blocker, outcome first at the end. This is Anthropic's
own recommended cadence. It deliberately **grants** the pre-tool-call sentence that caveman bans:
Anthropic's documented mitigation for Opus 5 emitting a tool call as plain text — where "the call
never runs" and the leaked text persists in history — is to give the model exactly that permission.

**3. Written deliverable length.** Match a written file's length to the task. Opus 5's files run long
by default and this is the documented lever.

**4. Delegation default.** Opus 5 delegates readily, and each hop pays a *fresh prefix*. A default
with a named, evaluable exception ("large, genuinely independent") beats a ban, because a genuinely
parallel six-file investigation kept in-thread costs far more than the hops saved. Verification is
named as the thing not to delegate: it pays a fresh prefix to re-derive context the main thread holds.

**5. Read width.** Search first, open narrowly. Real and avoidable input cost. v1 called it "the
largest avoidable cost in a session"; that superlative is false often enough — tool schemas run to
~55k for a multi-server setup and have been observed at 134k — so v3 kept the instruction and dropped
the ranking.

**6. The work floor (new in v4).** *"This changes how much you write, never how much you do."* This is
the clause the measurement above bought. Without it, "spend fewer tokens" is satisfied most cheaply by
investigating less, and that is exactly what happened: −32.7% steps, −7.6 pp score. It is the only
clause here whose job is to **prevent** a saving.

**7. The quality floor.** "Cut restatement, never reasoning." Without this the block is a quality
regression with a good metric: told only to be brief, a model prunes caveats and *why* first, because
those are cheapest to cut and hardest to notice missing. It enumerates what survives — uncertainty,
caveats, security warnings, destructive-action confirmations, required verification — because those
five are exactly what a token metric rewards dropping.

## Register: declarative, never imperative

Every line is a statement about how the session already works, with an escape hatch, so the model has
somewhere to go other than over-complying.

The usual justification is that "Anthropic's guidance says aggressive phrasing (`CRITICAL:`,
`You MUST`) causes over-triggering". That is sourced but **narrower than it is normally quoted**: it
is said of Opus 4.5/4.6, about prompts written to fix **tool or skill undertriggering**. The direction
holds for a block whose job is to be a default rather than a demand, but do not cite it as a general
law. A test enforces the register directly, which is the honest guardrail.

Positive framing over prohibition is the better-sourced principle here, and it is why v4 reads as
seven statements rather than a list of bans: "positive examples of the communication style you want
tend to be more effective than instructions about what not to do."

The block also never asks the model to confirm it followed the block. A block that says "confirm you
are following these token-saving rules" spends output tokens auditing compliance with an instruction
whose entire purpose was spending fewer output tokens.

## Sizing

Target the whole block at **150–300 tokens**. v4 is ~220.

The reason is *not* input cost — cache makes a static block nearly free after the first write. It is
that persona and style prompts carry an accuracy cost that scales with their length: MMLU 71.6%
baseline → 68.0% with a ~5-token persona → 66.3% with a ~150-token one, and **coding was the
worst-hit category**. Those models were 7–8B and the authors flag that 70B+ was untested, so treat it
as a sizing prior rather than a law about Opus 5. Caveman injects ~1–1.5k tokens — roughly ten times
the longest persona in that study, aimed at the category it damaged most.

Conflating the two reasons leads to optimising the wrong variable. Keep it short for accuracy, not
for the input bill.

## Where the next gain is, and what it must not cost

v4 cuts output 16.3% at no measurable score cost. Caveman cuts 41% and pays 7.6 points. The gap
between those two numbers is the headroom, and the constraint on taking it is that every clause added
must leave step count and reasoning alone.

Three candidates, in the order the evidence supports them.

**1. Restore the preservation clause, then let the others push harder.** v4 deliberately omits
caveman's single best rule (*never alter code, commands, paths, identifiers or error strings;
reproduce them exactly*) on the grounds that this block never instructs prose compression, so mangled
code is not a failure mode it creates. That reasoning holds for v4 as written. It stops holding the
moment a clause is added that compresses anything, and the preservation clause is what makes such a
clause safe. It costs about 130 prefix bytes. Add it FIRST, not after.

**2. Target the final message, which is the one output surface with real slack.** Opus 5's
default final messages run long, and this block currently only says to lead with the outcome. A
length calibration on the closing message (put the detail in the artifact, not the message) is
presentational by construction: it cannot reduce investigation, because the work is already done when
the final message is written. This is the safest place to take more.

**3. Written deliverables, sharpened.** The block already asks for file length to match the task.
Opus 5's written files run long by default and this is the documented lever for it; the current
clause is a statement rather than a calibration.

**What must not be tried, on measured grounds.** Anything reaching thinking depth or step count. The
effort sweep settled this: dropping Opus 5 from xhigh to medium cost 4.93 points (40 tasks worse
against 20 better, p = 0.0135) to save 6.6% of cost. Thinking is where this workload's quality lives,
and a prompt that trims it lands in caveman's failure mode by a different route.

**The measurement any v5 owes.** v4 has never been compared against v3, and no version has been
compared against another version at all. A v5 claiming improvement needs a v4-versus-v5 arm on the
gate in `evals/evals.json`: output tokens down, and the score sign test against no-block still not
significant. A bigger output cut that breaks score parity is a regression wearing a better number.

## What was considered and rejected

Each is a trap, and the reason matters more than the verdict — someone will propose all of them again.

| Rejected | Why it is a trap |
| --- | --- |
| **A compressed / caveman register** | The measurement above. −7.6 pp score, and 78% of the "saving" was fewer steps. Output prose is the smallest axis and the only lever on the list with a measured accuracy cost. |
| **A general "be concise" instruction** | Prunes reasoning and caveats first, with measured accuracy cost. The quality floor enumerates survivors instead. |
| **Telling the model to skip a verification pass** | v1 did this and it contradicted the repo's mandatory CP §7 gate. Skipping is cheaper, so *every* token metric improves when the security gate stops running. Remove *your* verification instructions; do not add a prohibition. |
| **Strip tool definitions for unused servers** (~55k tokens is real money) | The tool array is *in the cached prefix*. Ordinary mutation converts a paid-once cost into a paid-repeatedly one. **Narrower than it used to be:** tool search appends rather than swaps, and `mid-conversation-tool-changes-2026-07-01` adds/removes tools without invalidating the prefix. |
| **Proxy diffs and truncates the resent prefix on the wire** | Truncating history the model needs is a correctness bug wearing a savings costume, and it rewrites the prefix by construction. |
| **Local response cache keyed on request hash** | Byte-identical requests essentially do not occur in agentic sessions — every turn appends. A stale replay is a correctness bug. |
| **Make the model echo a version hash** | The proxy already knows the version and logs it free. |
| **Ship as a Claude Code output style** | Tempting — system-prompt layer, native adherence reminders. But it silently drops built-in software-engineering instructions without `keep-coding-instructions: true`, does not reach subagents, and cannot be changed mid-session. Viable for a single-session user; wrong for fan-out. |

## Honesty about the numbers

**Measured, first-party:** everything in "The measurement this exists because of", from the
Benchwarmer store, graded by diolog-swe-bench's own canonical spec. Two samples per (model, task) is
thin, and quality was machine-graded.

**Measured, third-party, verified first-hand:** JetBrains' Sonnet 5 A/B; the PRISM persona study;
caveman's own README figures.

**Sourced but narrower than usually quoted:** "aggressive phrasing over-triggers" (said of Opus
4.5/4.6, about tool/skill triggering). PRISM's length-scaling result (7–8B models only).

**Reported second-hand, not read in the source's results section:** Renze & Guven's exact 27.69%
math penalty; Nayab et al.'s accuracy tables; Pei et al.'s persona counts. Directions are sound;
treat the exact magnitudes as unverified.

**Assumed, not measured:**
- That this block's savings exceed its own cost on real traffic. It has not been A/B'd. The honest
  measurement is **total session tokens including cache misses**, never this-turn output length — a
  preamble can always be tuned to shrink visible output while forcing more turns to finish the same
  task, and the per-turn number improves while total spend rises.
- **That v4 saves anything. It did not on the one arm that has run.** 106 paired tasks, one
  sample each: score 63.3% -> 61.6% (32 worse / 30 better, p = 0.90, so no detectable
  difference), and cost $229.02 -> $303.77, **32.6% MORE than no block at all**. The work
  floor did its job on quality, and the saving did not appear. The cost arms are not on equal
  footing (one sample against two), so treat the cost number as unresolved rather than
  settled, and do not describe this block as a saving until a two-sample arm says so.
- **That v4 beats v3.** The arm compares v4 against no block, not against v3.
- **The instrument exists; the answer does not.** PERCH-0333 ships a three-arm experiment enrolled at
  0% by default. Its results are **per cache-conversation segment**, not per session — a `claude` the
  user starts is not a Perch child and its segments are not summed. Do not report a figure from it as
  "total session tokens".

Do not let the measured numbers lend their credibility to the assumed ones.

## Editing the block

The block is size-pinned on purpose. An innocuous-looking tweak retroactively changes the cost of
every session started afterwards, so:

1. Edit `references/injected-block.md` **and** `TokenDisciplineBlock.text` together — a test asserts
   they do not drift (compared on collapsed whitespace, so the markdown may wrap differently).
2. Bump `TokenDisciplineBlock.version` in the same commit, and **add the outgoing literal to
   `retainedTexts` before you overwrite it**. A version that is pinned but not retained fails open;
   one retained wrong silently rewrites the front of every warm prefix naming it. Rows only get added.
3. Update `pinnedUTF8Count` and the pinned digest; a size or wording change that does not bump the
   version fails the gate rather than shipping quietly.
4. Re-read the register, quality-floor and work-floor tests. They are worded for the current text.
5. State in the commit what behaviour you expect to change. "Tightened wording" is not a reason to
   invalidate every cache window.

Adding a line is not free even when it reads as free. The ceiling exists so that cost is visible
before it ships rather than after someone notices the bill.
