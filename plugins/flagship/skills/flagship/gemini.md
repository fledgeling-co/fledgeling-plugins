# gemini.md — `flagship`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names
the section it lands on. `flagship` is unusual here because its whole product is *figures about
other sessions* — a roster, a berth clearance, a dispatch ledger, a finding routed to the peers
it invalidates. Nothing it emits is compiled and everything it emits is acted on by somebody
else. The risk is not a worse plan. It is a roster asked of one session and reported for the
fleet, an `available 6` quoted from recall, and a chase counted as sent.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`:
  **no Gemini run of `flagship` has been observed.**
- **`[measured-family]` sources:** two single sessions (n=1 each) and a benchmark corpus of 106
  tasks at two effort levels — `geminify/references/evidence.md`. Neither watched a model
  coordinate anything.
- **The tier the evidence is about.** Every measured rate below was observed on
  `gemini-3.7-flash` (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not**
  to be projected onto the Pro tier. **[docs]** The defaults drift inside the family: *"If
  thinking_level is not specified, Gemini 3 will default to high."* against, from the 3.5
  Flash release notes, *"The default thinking effort is now medium, changed from high in
  Gemini 3 Flash Preview."* On Pro these overrides stand as `[docs]`-grounded discipline;
  every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `flagship` at any tier · no evidence a
  `gemini.md` fixes anything on either source · nothing measures Gemini coordinating peers or
  reading a berth registry · the bound-following rate below was measured on UI assertions, so its
  transfer to `cap that fan-out at four` is `[derived]` · `references/authority.md` was established
  against Claude peers, with no Gemini session recorded refusing or accepting a relayed grant.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns
  about: *"Avoid writing a prompt with non-linear logic or conditionals that require the model to
  piece together fragmented instructions from multiple different places in the prompt."* Read it
  in one pass, before the skill.

## There is no route-out block here, and the omission is the finding

geminify writes a hand-this-work-to-another-model block only for skills whose work the benchmark
measured, and `flagship` fails both conditions. **Its work class is one the corpus abstains on:**
the bench measures a model *building* an artifact, so only `implementation` and `general` are
shape-gated, while a conductor's deliverables — a routing decision, a status judgement, a
completeness call on a peer's queue — sit in `referral`, `verification` and `completeness`, where
`lane_pick.py` returns the policy answer unchanged. **And none of the
four measured shapes is a thing it produces:** `static-page` and `visual-design` (it renders
nothing), `brownfield-integration` (its edits are its own ledger and watcher),
`regression-sensitive` (it holds no contract a test currently passes). The one shape it does
author — an instrument like `scripts/starvation_watch.sh` — is `greenfield-module`, measured
level at 75 against opus's 75, exactly a row that must not be written. **[docs]** *"Avoid
using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."* Conducting is not one of them.

## What transfers intact

`flagship` is a better-shaped prompt for this model than most skills here, because its rules are
already numbers. Three need no override. **Brevity and the report shape** — `Report deltas.` and
the three-line done / in hand / parked-by contract are already **[docs]** *"By default, Gemini 3
models provide direct and efficient answers."* and *"use a clear, explicit instruction to specify
the format and show the output structure in your few-shot examples."* **`## Startup` is already
a chain** — roster → join → manifest → machine → ask, each consuming the last: **[docs]** *"make
each step a prompt and chain the prompts together in a sequence."* **And the authority boundary
needs no translation** — **[docs]** *"Inhibit your response: only take an action after all the
above reasoning is completed. Once you've taken an action, you cannot take it back."* is the
relay rule from the other side: a laundered permission cannot be withdrawn from the runners
already dispatched under it.

The scan found **0** qualitative skill references and **0** shouted passages against 33 quota
candidates and 31 bounds, so there is no register to read down. The `visual` module fired on nine
keyword hits and was **dropped**: all nine sit in `references/propagation.md`, a corpus of
*other* sessions' findings, and the skill itself captures nothing.

## Override 1 — the roster is the denominator (`## Startup`, `## Keep the fleet fed`)

`SKILL.md` names its scopes categorically: `Ask each session for its own state`, ask which
sessions a finding invalidates, `Pass tiered to every skill you invoke`, `Ask all three of every
number a session hands you`. Each is a set with a knowable size and none states it.
**[measured-family]** One run delivered **12 of 12** requirements the brief *enumerated* and
satisfied every requirement named *categorically* with one instance or none — all surfaces →
5, all states → **1**, all menus → **0**, all flows → **0** (§1.1.1, n=1) — while the skill it
followed stated six states *and* an explicit completeness condition in prose. **[docs]**
*"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition."*

`ListAgents` prints the denominator, so write it down before the first dispatch and report the
fraction after. Filled against a nine-session roster as the exemplar:

| scope, in `flagship`'s words | denominator | filled | reported |
|---|---|---|---|
| ask each session for its own state | `ListAgents` = 9 | 9 | `9 of 9` |
| idle shape asked, not inferred | 6 quiet (9 − 3 on berths) | 5 | `5 of 6, 1 prompt-parked` |
| finding propagated to what it invalidates | 4 named by the reporter | 4 | `4 of 4, attributed` |
| condition-gated rows re-checked | 3 in the ledger | 2 | `2 of 3, 1 n/a: host idle 0 min` |

A cell that cannot be filled reads `n/a: <reason>` — **[docs]** *"provide instructions for
handling missing data rather than assuming inserted data will always be present and
well-formed."* A session that never answered is `unknown`, never idle.

## Override 2 — the caps are bounds, and bounds are the measured failure (`## What you actually do`, `## Guardrails`)

`flagship` states its hardest invariants as prohibitions in prose: `cap that fan-out at four`,
`min(ship-armada's 3 concurrent projects, harbourmaster's available berths)`, `Do not send a third
chase to what two have not reached`, `Sample thermal at least three times across a minute`. **[measured-family]** That is the shape the
benchmark says gets *exceeded* rather than forgotten: classifying every failing UI assertion by
whether it states a bound or asks for a thing, **58%** of Gemini's failures at `medium` and
**86%** at `high` were bound-shaped,
against 8% for opus and 6% for the OpenAI lane; one rule — `has exactly one soft elevation
shadow` — failed on *every* card and *every* toast in its set, on a run that passed 37 of its
39 other assertions (§2.2). A bound is violated by what you did not write, so it survives every
check that looks at what you did. **[docs]** Google treats these as a component in their own
right — *"Restrictions on what the model must adhere to when generating a response, including
what the model can and can't do."* — and asks that *"all requirements, constraints, options, and
preferences are exhaustively incorporated into your plan."* So each becomes a row read back off
what you actually sent:

| bound, in `flagship`'s words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `cap that fan-out at four` | subagents live at once | count this turn's spawn calls | 4 | yes |
| token cap = `min(3, available)` | tokens issued this wave | grep the ledger for `token:` | 3, `available` 5 | yes |
| two chases, then the operator | chases per silent session | ledger `chases` column, max | 3 on one session | **no — escalate** |
| thermal sampled ≥ 3 times | samples before a clearance | count `pressure.py` calls | 1 | **no — re-sample** |

Report `2 of 4 bounds within, 2 breached and corrected`. A ledger filled from `SKILL.md` rather
than from the messages sent shows four greens, which is the failure itself.

## Override 3 — every figure carries its command, its output and its timestamp (`## Reading the machine honestly`, `scripts/`)

**[measured-family]** The run in §1.1.2 (n=1) wrote itself a review asserting a named browser
engine as verified when that engine had failed all four invocation attempts, and a *"100% pass
rate on contrast"* from a probe never executed — measured afterwards, every primary button was
3.65:1 and one glyph 1.00:1, invisible. A requested *shape* got completed where the procedure was
not specified, and a berth clearance, a fleet status and a propagated finding each have an obvious
shape and no compiler. **[docs]** *"Include specific verification steps in either the system
instructions or your prompts directly."* and *"Verify your claims by
quoting the exact applicable information (including policies) when referring to them."* So no
figure leaves this session without the command that produced it, that command's output, and the
time it was read.

Three specifics, all the skill's own: read the **occupant list** rather than the count, since
`available 0` has three causes and one is a full machine; quote `available`, `ceiling` and the
timestamp **together**; and say whether your own work is in the number. The message ships filled
— the shape, not a reading:

```
machine  2026-08-23 22:41:07 · scripts/machine_read.py
berths   ceiling 10 · in_use 7 · available 3 · occupants: anvil(6), atlas(1)
load     1m 14.2 · 5m 11.8 · max/core 0.89 · basis max(1m,5m); 1m<5m, falling
thermal  not_limited ×3 across 61s
you      2 berths, re-measure at launch; 1 spare after atlas, 3 of 3 committed
```

The same rule covers the five instruments `flagship` ships, where its own governing sentence is
`Before running a check, ask what its output would be under the hypothesis you are ruling out.`
**[measured-here, on geminify's own gate]** one line added to a quote checker took the checked
count to zero and turned every file green, caught only by re-running the negative control;
**[measured-family]** on `COD Dossier` an auditor validated tags and citations thoroughly, had
no check that its prerequisite artifacts existed, and passed two skipped skill invocations with
exit 0 (§1.2.2). So print the basis a label was judged on — `starvation_watch.sh` reporting one
idle session while the runtime reported eight is this skill's own unreachable-`STARVED` case —
and check a receipt before a property: `open_session.sh` exits 2 when its title marker does not
return, and the new session file in `~/.claude/sessions/` is the confirmation that cannot
mislead, where a moving tab count proves only that a tab exists.

## Override 4 — two attempts, then a different move (`references/dispatch.md`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Both n=1 sessions ran the loop: one invoked a banned,
absent tool four consecutive times with nothing changed between attempts (§1.1.2); the other hit
a 25,000-token `Read` ceiling and retried four times with minor tweaks before pivoting to a
Python split (§1.2.3). `gemini-cli` ships a loop detector whose halt message names *"repetitive
tool calls"* (§7.2).

Four `flagship` errors look transient and are not; each pivots on attempt 1.
**`references/propagation.md` is 236 KB** and exceeds the read ceiling on the first call — read
it ranged or grep it, which is §1.2.3's exact shape inside this skill's own references.
**`governor-run` exit 75** is a ceiling to shed into rather than a queue to wait out. **A silent
session** is two chases and then the operator, since delivery and parking are indistinguishable
from the sender's side. **An empty lane output file** is a failure with a clean exit code, and
`references/lanes.md` records a meter at 84% while the lane returned `402`.

## Override 5 — drained is a chain of artifacts, not a report (`## Keep the fleet fed`)

`SKILL.md` holds the finding already: `every status this skill collects is rung one`, and the
standing instruction is `reckon` then `whats-left` before recording anything as finished.
**[measured-family]** The mechanism that breaks it is recorded (§1.2.1, n=1): a skill instructed
that every design decision `goes through` two named skills, and the run invoked neither — its own
diagnosis being that the guidance was already in context and nothing downstream depended on a file
only those skills produce. The scan flags **no** qualitative skill references here, so these
two are `[derived]` as the same shape: named, with nothing reading their output. **[docs]**
*"make each step a prompt and chain the prompts together in a sequence."*

```
1. reckon (by explicit path, when two cache versions exist) → reckon-<repo>.md
2. whats-left, focused on current work                      → whats-left-<repo>.html
3. the drained row cites both paths, plus the join rate from step 1
```

A drained row naming no file is a declaration: the skill's own case closed drained on green
gates, which attested the work that existed and nothing about what remained.

## Override 6 — ask the closed set; cap the fan-out (`## Keep the fleet fed`, `## Starting sessions`)

`SKILL.md` gives idle a four-row table and then five more shapes in prose — stopped-starting,
mid-long-call, throughput-capped, prompt-parked, finished-and-silent — and says `Ask; do not
infer`. Asking a session how it is going returns a mood; asking *which of these nine, and what is
your next concrete action* returns something checkable. **[docs]** *"The response is correct, but the model didn't stay within the
bounds of the options."* — the remedy is a multiple choice with one option back; and *"Avoid
premature conclusions: There may be multiple relevant options for a given situation."*, which is
why drained and capped must not be collapsed. `cap that fan-out at four. The conducting itself
is never delegated.` is read back in Override 2's first row, and **a brief you write is a
prompt** — one to a *Gemini* peer needs the two ledgers above written into it, where
`references/tiered-delegation.md` is right that an Opus worker's does not.

## Override 7 — what you cannot re-derive is stated as unavailable (`## The role's structural exposure`)

`flagship` names the exposure precisely: `re-derive what you can, and send the question rather
than the finding for what you cannot`, and `A stated inability beats a better number.` **[docs]**
Google's strictly-grounded system instruction ends on that clause: *"If the exact answer is not
explicitly written in the context, you must state that the information is not available."* Adopt
it verbatim for any figure you publish about another session. **[measured-family]** The adjacent
failure is measured at n=1 (§1.1.4): a previous-generation published accent colour returned
confidently — an old fact, not a guess. **[docs]** *"Your
knowledge cutoff date is January 2025."* So `~/Dev/ARMADA.md` figures are claims until a session
confirms them, index and detail both; and **a file or skill named in a message is loaded before
the answer is written.** §1.2.4 recorded both halves going wrong in one session: answering from
memory when three skills were named, then launching a skill when an answer was wanted. Read,
then answer, as two ordered steps.

## Override 8 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation,
or advanced function calling scenarios."* Conducting a fleet is multi-step planning, so `HIGH`
is what Google describes this work as needing; 3.7 Flash defaults to `MEDIUM` and the uplift is
unmeasured on this corpus. **[measured-family]** Do not raise it as a remedy for anything above:
paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7 points
(§2.3), and the bound-shaped share of failures *rose* from 58% to 86%. **[docs]** *"Higher
thinking levels encourage the model to use more tools to explore and verify, so lowering the level
can reduce tool calls."* — fewer tool calls is the wrong direction for a skill whose error is
quoting a figure it did not re-read.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and
response format, at the end of the prompt."*

1. Write the roster's size down before the first dispatch; report `N of N` after.
2. Fill the bound ledger from the messages you sent, not from `SKILL.md`.
3. Every figure ships its command, output, occupants and timestamp; paste what the instrument
   printed and check its receipt before its verdict.
4. One retry on a transient error; none on a 236 KB read, an exit 75, a second chase, or an
   empty lane file.
5. `reckon` and `whats-left` produce files the drained row cites by path.
6. Ask the nine-shape question as a closed set; cap subagents at four; conduct in session, and
   state as unavailable whatever you cannot re-derive.

