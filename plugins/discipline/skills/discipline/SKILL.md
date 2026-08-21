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

Two supporting files carry what this one asserts. `references/evidence.md` holds every measurement in
full; `references/provenance.md` is the registry that marks each figure on two closed axes,
and **`scripts/block-check.py` reads that registry and fails the build** on an untiered figure, a
drifted literal, or an assumed number stated in the argument. Run it before any commit that touches
the block or a number:

```bash
python3 skills/discipline/scripts/block-check.py --verbose   # must exit 0
```

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

**Caveman is not overselling its mechanism, and the disagreement here is with its rules, not its
marketing.** Its README carries an "Honest number warning" — output tokens only, ~1–1.5k added per
turn, "on already-terse workloads they can go net-negative" — and its `docs/HONEST-NUMBERS.md` lists
the aggregate output reduction as *"Not published"*, which is more candid than this repo previously
credited. **Read 18 Aug 2026;** its headline figure is still 65%, and it does not itself cite the
JetBrains result. An earlier version of this file claimed otherwise. `references/evidence.md` §3
carries the retraction and why the date is now attached to the claim.

## Why there is no conciseness clause

The obvious clause — "be concise" — is the one thing this block will not say, and the reason is
sourced rather than aesthetic. Brevity instructions carry a measured accuracy cost: Giskard's Phare
benchmark records up to a **20-point** drop in hallucination resistance under one, and Renze & Guven
a math penalty under Concise CoT.

**But read the scoping before citing either, because this file got it wrong until 18 Aug 2026.** Both are `second-hand` or `unlocated`; Giskard's figure is an aggregate with no per-model breakdown and no
published list of which models were in the brevity condition, so the pairs usually quoted from it are
not in the source and Claude's inclusion is simply unknown. `evidence.md` §5 carries the full scoping.

A real effect, in a real direction, on models that mostly are not Claude, at a magnitude nobody here
has read in a results table. Enough to decline a conciseness clause; not enough to price one on Opus 5.

Cutting *presentation* is safe. Cutting *hedging* is not, because the hedge is the confidence signal —
which is why the quality floor enumerates what survives rather than asking for brevity and hoping.

## Why placement decides everything

The prompt cache matches an **exact byte prefix**. That gives two places to put a preamble, with
opposite economics:

- **In the cached prefix (the `system` field):** paid once per cache window, read cheap forever after.
  Any change invalidates the whole prefix and resends the conversation at full price.
- **After the last cache breakpoint:** costs 1.0× its own tokens *every turn, forever*, and never gets
  cheaper. **A token-saving preamble delivered the second way is a permanent tax that funds nothing** —
  it is the one placement guaranteed to lose money, because its whole justification was being paid for
  once.

So the block goes in the `system` field and is **byte-identical for the life of the session** — no
timestamp, no session id, no account name, no counter, no model-visible version string. The moment
something in it varies, it stops being a preamble and becomes a cache-miss generator.

**The most expensive thing this feature could do is edit itself.**

### Where to put it, in order, and when to stop

On Claude Code specifically: a *skill* injects as a user message at invocation, which is cache-safe
but not persistent. An *output style* modifies the system prompt and triggers native adherence
reminders — but it drops Claude Code's built-in software-engineering instructions unless
`keep-coding-instructions: true` is set, and it does not reach subagents. For a fan-out workload,
proxy injection is the only delivery that reaches every session.

That gives a ladder. Take the first rung available:

1. **Proxy injection into the `system` field.** Reaches every session including subagents. The only
   delivery that does.
2. **An output style** with `keep-coding-instructions: true`. System-prompt layer, cache-safe, but
   subagents do not see it and it cannot be changed mid-session. Fine for a single-session user.
3. **`CLAUDE.md`.** Loaded into the prefix and cache-safe, but shared with everything else in that
   file, so the block's bytes are not independently versionable.
4. **No `system`-field injection point at all — stop, and say so.**

Rung 4 is the one that matters, because the tempting move there is to put the block somewhere it will
at least be *read*: appended to a user turn, injected after the last cache breakpoint, or pasted into
a prompt template that lands late in the request. **Do not.** The section above is a proof that this
placement is a pure loss — full price for its own tokens on every turn, forever, to deliver
instructions whose entire purpose is to spend less. A block that costs more than it saves is worse
than no block, and unlike most wrong answers this one produces a metric that looks fine, because
visible output does shrink.

So when no cached-prefix injection point exists, report that the block cannot be delivered in this
environment and leave it uninstalled. Do not improvise a placement, and do not install it "to try it"
— the cost is per turn and the benefit is unmeasured (see § *Honesty about the numbers*).

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
largest avoidable cost in a session"; that superlative is false often enough that v3 kept the
instruction and dropped the ranking.

**The two figures usually quoted here measure different things, and this file conflated them until
18 Aug 2026.** `134k` tool-definition tokens is a primary Anthropic observation of a high-complexity
multi-server setup before optimisation. `55k` is **not** "a typical multi-server setup" and not
Anthropic telemetry — it traces to a practitioner measurement of the **GitHub MCP server alone**, and
the "typical" framing accreted in retelling. Both stay `second-hand`: the 134k is `vendor-doc`, the
55k `independent`.

**And the clause now has a measured ceiling, smaller than it implies.** A 2,848-run decomposition of
Claude Code (`evidence.md` §6) finds a user-side layer can reach only ~**6.0%** of input cost,
practically nearer 5%; tool outputs alone are ~3.3%. In that study a 38.4% cut in delivered
tool-output tokens moved ~1.3% of input cost and **raised billed cost 6.8%**. Keep the instruction; do
not expect it to move the bill. It is also still the clause with no first-party way to measure whether
it works here (`evidence.md` §9).

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

**As a gate that can actually run, that ceiling is 1,200 bytes** — 300 tokens at the ~4 bytes/token
this block's register measures — with a 600-byte floor. v4 sits at 881, so there are **319 bytes of
headroom, about two clauses' worth**, and `scripts/block-check.py` fails the build past it.

The distinction matters because the previous wording pinned 881 and called it a ceiling. A pin makes
*every* proposed addition fail, so the section that was supposed to make cost visible before it
shipped instead refused all change and got ignored. A ceiling with headroom is a budget; a pin is a
freeze.

The reason for the ceiling is *not* input cost — cache makes a static block nearly free after the
first write. It is that persona and style prompts carry an accuracy cost that scales with their
length: MMLU 71.6% baseline → 68.0% with a ~5-token persona → 66.3% with a ~150-token one, and
**coding was the worst-hit category**. Those models were 7–8B and the authors flag that 70B+ was
untested, so treat it as a sizing prior rather than a law about Opus 5. Caveman injects ~1–1.5k
tokens — roughly ten times the longest persona in that study, aimed at the category it damaged most.

Conflating the two reasons leads to optimising the wrong variable. Keep it short for accuracy, not
for the input bill.

## Where the next gain is, and what it must not cost

v4 cuts output 16.3% at no measurable score cost. Caveman cuts 41% and pays 7.6 points. The gap
between those two numbers is the headroom, and the constraint on taking it is that every clause added
must leave step count and reasoning alone.

**Size that headroom honestly before spending effort on it.** Generated output is 10.4% of the bill on
the largest published decomposition (`evidence.md` §6), and the input cost a user-side layer can reach
is ~6%. So closing the entire gap between 16.3% and 41% would move low single digits of total spend —
and the same study's heaviest compression arm cut delivered tokens 38.4% while the bill went *up* 6.8%.
The three candidates below are worth taking because they are cheap and safe, not because the prize is
large. If a clause costs a point of task score, it is a bad trade at this ceiling whatever it saves.

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

## The cheapest spend signal nobody watches: the output-to-input ratio

Everything above is about the cost of a session doing its job. This is about the cost of a session
*not* doing its job, which is invisible to every measure here because the tokens look identical.

An agent that cannot write a file has one route left: emit the artifact as literal output. That is
indistinguishable from ordinary work in a token total and unmistakable in a ratio. Measured across 135
agent runs on one pipeline, 2026-08-21:

| Outcome | Runs | Sent to the model | Written back | Ratio |
|---|---|---|---|---|
| completed | 61 | 2,510,067 | 2,833,838 | **1.1×** |
| failed | 52 | 20,269 | 684,666 | **33.8×** |
| cancelled | 22 | 199,497 | 128,983 | 0.6× |

**A working run writes back about what it was sent. A run writing back thirty-four times what it was
sent is reciting an artifact it should be saving.** The signal was present from the first failure and
nobody computed it; the cost while it went unwatched was **813,649 output tokens on runs that produced
nothing** — 22% of all output in the window — plus 414 million cache-read tokens across the set, and
**74 of 135 runs producing no artifact at all**.

Three things follow, in order of how cheap they are:

- **Watch the ratio, not the total.** A threshold around 5× flags this class and is quiet otherwise.
  It needs no new instrumentation where input and output counts are already recorded per run.
- **Count the runs that produced nothing.** A 55% no-artifact rate is a spend problem before it is a
  quality problem, and it is the number least likely to be on anyone's dashboard.
- **Judge success from the artifact.** File exists, size, hash, checks passed — never the model saying
  it is done. A run that narrated success and wrote nothing bills exactly like one that worked.

**Tier: measured, n=1 pipeline, 135 runs, 2026-08-21.** The ratio is derived from two summed fields
rather than measured per turn, the counts are the pipeline's own accounting rather than a provider
invoice, and the 5× threshold is a judgement from this one distribution rather than a tuned value.
Nobody has measured whether watching it shortens anything; what is measured is that the signal was
there and unread.

## What was considered and rejected

Each is a trap, and the reason matters more than the verdict — someone will propose all of them again.

| Rejected | Why it is a trap |
| --- | --- |
| **A compressed / caveman register** | The measurement above. −7.6 pp score, and 78% of the "saving" was fewer steps. Output prose is the smallest axis and the only lever on the list with a measured accuracy cost. |
| **A general "be concise" instruction** | Prunes reasoning and caveats first, with a measured accuracy cost on non-Claude models. See § *Why there is no conciseness clause*; the quality floor enumerates survivors instead. |
| **Telling the model to skip a verification pass** | v1 did this and it contradicted the repo's mandatory CP §7 gate. Skipping is cheaper, so *every* token metric improves when the security gate stops running. Remove *your* verification instructions; do not add a prohibition. |
| **Strip tool definitions for unused servers** (~55k tokens, `independent+second-hand`) | The tool array is *in the cached prefix*. Ordinary mutation converts a paid-once cost into a paid-repeatedly one. **Narrower than it used to be:** tool search appends rather than swaps, and `mid-conversation-tool-changes-2026-07-01` adds/removes tools without invalidating the prefix. |
| **Proxy diffs and truncates the resent prefix on the wire** | Truncating history the model needs is a correctness bug wearing a savings costume, and it rewrites the prefix by construction. |
| **Local response cache keyed on request hash** | Byte-identical requests essentially do not occur in agentic sessions — every turn appends. A stale replay is a correctness bug. |
| **Make the model echo a version hash** | The proxy already knows the version and logs it free. |
| **Ship as a Claude Code output style** | Tempting — system-prompt layer, native adherence reminders. But it silently drops built-in software-engineering instructions without `keep-coding-instructions: true`, does not reach subagents, and cannot be changed mid-session. Viable for a single-session user; wrong for fan-out. |

## Honesty about the numbers

Every figure in this skill carries a **composed pair** of marks in `references/provenance.md`, and
`scripts/block-check.py` fails the build on a figure with no row, a mark outside either closed set, two
marks from the same family, an `assumed` figure stated outside a section like this one, or a living
source with no read date. The tiering is a gate, not a convention.

**The two families are orthogonal, and keeping them apart is the point.**

- **Independence** — a property of *the source*, and **not improvable by reading harder**:
  `first-party` · `independent` · `vendor-doc` · `self-report` · `anecdote` · `assumed`.
- **Verification** — a property of *our diligence*, and improvable by doing the work:
  `results-read` · `summarised` · `second-hand` · `unlocated` · `none`.

So `self-report+results-read` — caveman's README, read in full on 18 Aug 2026 — is a real and permanent
state, not a way-station. **Promotion runs along the verification axis only.** Reading a paper's results
section moves `second-hand` → `results-read`; nothing makes a competitor's self-report independent, and
the gate pins each row's independence mark so a change to it cannot be silent.

That distinction was the flaw this pass fixed. A single flat scale had `caveman-readme` filed as
"reported-not-verified", which conflated *we have not checked it* with *its author has a stake in it* —
so a reader fixing the first half would have appeared licensed to promote the second. It also forced
the PRISM study across two rows, one for its figures and one for its 7–8B scope, because one axis could
not carry both. Scope is now its own column.

**Where the marks land on the load-bearing figures:**

| Figure | Mark |
| --- | --- |
| The 106-task paired benchmark, the blind panel, the effort sweep, the byte counts | `first-party+results-read` |
| JetBrains' Sonnet 5 A/B; the PRISM persona study | `independent+results-read` |
| Weinberger & Hozez's 2,848-run cost decomposition (arXiv:2607.12161) | `independent+summarised` |
| Cache reads at 0.1× base input; the exact-byte-prefix rule | `vendor-doc+results-read` |
| **Caveman's README figures, including the 65% headline** | `self-report+results-read` |
| **~134k tool-definition tokens** (Anthropic, before optimisation) | `vendor-doc+second-hand` |
| **~55k tool-definition tokens** — one MCP server, *not* "a typical setup" | `independent+second-hand` |
| Anthropic's tool-search and programmatic-calling gains | `self-report+second-hand` |
| Renze & Guven's 27.69%; Nayab et al.; the brevity counter-evidence | `independent+second-hand` |
| Giskard Phare's aggregate 20-point drop | `independent+results-read` |
| **Giskard's widely-quoted per-model pairs** | `independent+unlocated` — searched for, **not in the source** |
| The removed "96% reused input" claim | `anecdote+unlocated` |

Three of those were sitting a tier too high before this pass: the 55k (attributed to Anthropic when it
measures one practitioner's GitHub MCP install), caveman's README (filed as verified third-party rather
than as a self-report), and the Giskard pairs (quoted as figures when they cannot be found at all).

"Aggressive phrasing over-triggers" is sourced but scoped: said of Opus 4.5/4.6, about tool and skill
triggering, not about every instruction on every model.

**`assumed+none`** — not measured:
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
- **That this operator's own token split resembles the published one.** §6 of `evidence.md` measures
  generated output at 10.4% of the bill across 2,848 Claude Code runs, which supersedes the ~14% this
  file used to assume. But those runs are Haiku 4.5, Sonnet 5 and Opus 4.8 — **not Opus 5 at xhigh**,
  which is the only workload this block actually runs against. Nobody has counted the cache-read,
  cache-write, new-input and output shares on this traffic. The superseded 14% may not be restated
  outside a limits section; the gate checks.
- **The instrument exists; the answer does not.** PERCH-0333 ships a three-arm experiment enrolled at
  0% by default. Its results are **per cache-conversation segment**, not per session — a `claude` the
  user starts is not a Perch child and its segments are not summed. Do not report a figure from it as
  "total session tokens".

Do not let the measured numbers lend their credibility to the assumed ones. The tiers above are one
tier deeper than they were for exactly that reason: the rule was being broken a level above where it
was written to catch, by figures that had a citation and no audit.

## Editing the block

The block is size-pinned on purpose. An innocuous-looking tweak retroactively changes the cost of
every session started afterwards, so the checks are split by who can actually run them.

**What this repo gates, in `scripts/block-check.py` — run it and check the exit code:**

```bash
python3 skills/discipline/scripts/block-check.py --verbose   # must exit 0
```

It asserts each literal's byte count *and* its sha256 (a same-length edit is the one change no byte
count catches), that v3 and v1 are still retained, that v4 stays inside the 1,200-byte ceiling, that
the literal contains nothing that varies, that the register carries no `MUST`/`CRITICAL`, that the
quality floor still names all five survivors, that clause 6 is present, that the block has not
re-acquired v1's verification prohibition or grown a self-audit clause, and every provenance rule in
§ *Honesty about the numbers*. Piping it through `grep` makes `$?` grep's status and not the gate's.

The pins live in `BLOCK_PINS` at the top of that script, so **editing a literal means editing the gate
in the same commit.** That coupling is deliberate: it is the smallest mechanism that makes the cost of
a wording change visible before it ships.

**What a host harness must gate, and this repo cannot.** These name Perch identifiers; if you inject
by another route, the same three properties still have to hold somewhere:

1. `references/injected-block.md` and the harness's own literal (`TokenDisciplineBlock.text`) must not
   drift — compare on collapsed whitespace, so the markdown may wrap differently.
2. The version (`TokenDisciplineBlock.version`) is bumped in the same commit, and **the outgoing
   literal is added to the retained set before it is overwritten**. A version pinned but not retained
   fails open; one retained wrong silently rewrites the front of every warm prefix naming it. Rows
   only ever get added.
3. Per-conversation pinning replays the exact bytes a conversation opened with.

Then, whichever route you use: state in the commit what behaviour you expect to change. "Tightened
wording" is not a reason to invalidate every cache window.

**The ceiling is 1,200 bytes and v4 uses 881 of it.** Adding a line is not free even when it reads as
free, and the number is stated so the cost is arguable before it ships rather than after someone
notices the bill — 319 bytes of headroom is about two clauses, and the three candidates in § *Where
the next gain is* would spend roughly half of it. A proposal that needs more than the headroom is a
proposal to remove a clause.
