# gemini.md — `flagship`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `flagship` is unusual here because its whole product is *figures about other
sessions* — a roster, a berth clearance, a dispatch ledger, a finding routed to the peers it
invalidates. Nothing it emits is compiled and everything it emits is acted on by somebody else. The
risk is not a worse plan. It is a roster asked of one session and reported for the fleet, an
`available 6` quoted from recall, and a chase counted as sent.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — **no Gemini run of `flagship` has been observed.**
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`; neither watched a model coordinate anything.
  All of it is flash-tier (`gemini-3.7-flash`, one session on `-high`) and **not** to be projected
  onto Pro, where these overrides stand as `[docs]`-grounded discipline and every number is open.
  **[docs]** The defaults drift inside the family: *"If thinking_level is not specified, Gemini 3
  will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."*
- **Unmeasured on this skill:** no Gemini run of `flagship` at any tier · nothing measures Gemini
  coordinating peers or reading a berth registry · the bound rate below was measured on UI
  assertions, so its transfer to `cap that fan-out at four` and the tab ladder is `[derived]` ·
  `references/authority.md` was established against Claude peers · and nothing measures a Gemini
  conductor classifying a session before killing it, the one override whose failure is final.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns of:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, first.

## There is no route-out block here, and the omission is the finding

geminify writes a hand-this-work-to-another-model block only for skills whose work the benchmark
measured, and `flagship` fails both conditions. **Its work class is one the corpus abstains on:**
the bench measures a model *building*, so only `implementation` and `general` are shape-gated,
while a routing decision, a status judgement and a completeness call on a peer's queue sit in
`referral`, `verification` and `completeness`, where `lane_pick.py` returns the policy answer
unchanged. **And none of the four measured shapes is a thing it produces:** `static-page` and
`visual-design` (it renders nothing), `brownfield-integration` (its edits are its own ledger),
`regression-sensitive` (no contract a test currently passes). The instrument it does author —
`scripts/starvation_watch.sh` — is `greenfield-module`, level at 75 against opus's 75, exactly a
row that must not be written. **[docs]** *"Avoid using prompts that ask the model to perform a
task for which it has a known, fundamental limitation."*

## What transfers intact

`flagship` is a better-shaped prompt for this model than most skills here, because its rules are
already numbers. Three need no override. **Brevity and the report shape** — `Report deltas.` and
the three-line done / in hand / parked-by contract are already **[docs]** *"By default, Gemini 3
models provide direct and efficient answers."* and *"use a clear, explicit instruction to specify
the format and show the output structure in your few-shot examples."* **`## Startup` is already a
chain** — roster → join → manifest → machine → ask, each consuming the last: **[docs]** *"make each
step a prompt and chain the prompts together in a sequence."* **And the authority boundary needs no
translation** — **[docs]** *"Inhibit your response: only take an action after all the above
reasoning is completed. Once you've taken an action, you cannot take it back."* is the relay rule
from the other side: a laundered permission cannot be withdrawn from the runners already
dispatched under it, which is why `Ask the ledger, not the session.` also transfers unchanged.

The scan found **0** qualitative skill references and **0** shouted passages against 33 quota
candidates and 32 bounds, so there is no register to read down. The `visual` module fired on nine
hits and was **dropped**: all nine sit in `references/propagation.md`, and the skill renders nothing.

## Override 1 — the roster is the denominator (`## Startup`, `## Keep the fleet fed`)

`SKILL.md` names its scopes categorically: `Ask each session for its own state`, ask which sessions
a finding invalidates, `Pass tiered to every skill you invoke`, `Ask all three of every number a
session hands you`. Each is a set with a knowable size and none states it. **[measured-family]** One
run delivered **12 of 12** requirements the brief *enumerated* and every *categorical* one with a
single instance or none — all surfaces → 5, all states → **1**, all menus → **0**, all flows → **0**
(§1.1.1, n=1) — while the skill it followed stated six states *and* a completeness condition in
prose. **[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."*

`ListAgents` prints the denominator: write it down before the first dispatch, report the fraction
after. Filled against a nine-session roster as the exemplar:

| scope, in `flagship`'s words | denominator | filled | reported |
|---|---|---|---|
| ask each session for its own state | `ListAgents` = 9 | 9 | `9 of 9` |
| idle shape asked, not inferred | 6 quiet (9 − 3 on berths) | 5 | `5 of 6, 1 prompt-parked` |
| finding propagated to what it invalidates | 4 named by the reporter | 4 | `4 of 4, attributed` |
| condition-gated rows re-checked | 3 in the ledger | 2 | `2 of 3, 1 n/a: host idle 0 min` |
| dispatches cleared by their own report | 7 sent | 5 | `5 of 7, 1 chased ×2, 1 vanished` |

A cell that cannot be filled reads `n/a: <reason>` — **[docs]** *"provide instructions for
handling missing data rather than assuming inserted data will always be present and well-formed."*
A session that never answered is `unknown`, never idle; one that has **left the roster** holding an
uncleared dispatch is a fourth value — `references/dispatch.md` records three vanishing after a
load-391 event, and the move is telling the operator what each held and that `claude --resume`
recovers it.

## Override 2 — the caps are bounds, and bounds are the measured failure (`## What you actually do`, `## Guardrails`)

`flagship` states its hardest invariants as prohibitions in prose: `cap that fan-out at four`,
`min(ship-armada's 3 concurrent projects, harbourmaster's available berths)`, `Do not send a third
chase to what two have not reached`, `Sample thermal at least three times across a minute`, and now
`The tab is the most expensive plane, so it is the last resort rather than the default.`
**[measured-family]** That is the shape the benchmark says gets *exceeded* rather than forgotten:
**58%** of Gemini's failing UI assertions at `medium` and **86%** at `high` were bound-shaped
against 8% for opus, and one rule — `has exactly one soft elevation shadow` — failed on *every*
card and toast in its set, on a run that passed 37 of its 39 other assertions (§2.2). A bound is
violated by what you did not write, so it survives every check that looks at what you did.
**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model
must adhere to when generating a response, including what the model can and can't do."* — and asks
that *"all requirements, constraints, options, and preferences are exhaustively incorporated into
your plan."* Each becomes a row read back off what you actually sent:

| bound, in `flagship`'s words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `cap that fan-out at four` | subagents live at once | count this turn's spawn calls | 4 | yes |
| token cap = `min(3, available)` | tokens issued this wave | grep the ledger for `token:` | 3, `available` 5 | yes |
| two chases, then the operator | chases per silent session | ledger `chases` column, max | 3 on one session | **no — escalate** |
| thermal sampled ≥ 3 times | samples before a clearance | count `pressure.py` calls | 1 | **no — re-sample** |
| the tab is the last resort | tabs opened this wave | `ls ~/.claude/sessions/` before and after | 2, both doable as background agents | **no — demote** |
| `only the first closes` | sessions killed, by class | classify each of the five before the kill | 12 killed, 12 clean-handover | yes |

Report `3 of 6 bounds within, 3 breached and corrected`. A ledger filled from `SKILL.md` rather
than from the messages sent shows six greens, which is the failure itself. The last row has no
undo: `references/spawning.md` names five classes — clean handover, mid-queue, owing dispatched
work, owner-gated, the operator's own — and a categorical read kills the other four.

## Override 3 — every figure carries its command, its output and its timestamp (`## Reading the machine honestly`)

**[measured-family]** The run in §1.1.2 (n=1) reviewed itself, asserting a browser engine as
verified when it had failed all four invocation attempts, and a *"100% pass rate on contrast"* from
a probe never executed — measured afterwards, every primary button was 3.65:1 and one glyph 1.00:1.
A requested *shape* got completed where the procedure was not specified, and a berth clearance, a
fleet status and a propagated finding each have an obvious shape and no compiler. **[docs]**
*"Include specific verification steps in either the system instructions or your prompts
directly."* So no figure leaves without its command, that command's output, and the read time.

Four specifics, all the skill's own: read the **occupant list** rather than the count, since
`available 0` has three causes and one is a full machine; quote `available`, `ceiling` and the
timestamp **together**; census the processes when load is high and the fleet small, per `OVERLOADED
with a low claude-process count points at the machine, not the fleet`; and say whether your own
work is in the number. The message ships filled — the shape, not a reading:

```
machine  2026-08-24 22:41:07 · scripts/machine_read.py
berths   ceiling 10 · in_use 7 · available 3 · occupants: anvil(6), atlas(1)
load     1m 14.2 · 5m 11.8 · max/core 0.89 · basis max(1m,5m); 1m>5m, rising
procs    ps -eo pcpu,comm · 24 claude, 0 CoreSimulator, 0 VM — consumers are ours
disk     87% on /System/Volumes/Data, steady across two reads 4 min apart
thermal  not_limited ×3 across 61s
you      2 berths, re-measure at launch; 1 spare after atlas, 3 of 3 committed
```

Two rows are there because one sample lies: a disk *transition* (87 → 97 → 89 in ten minutes,
nothing deleted) needs a second read before it gates, and a compile burst — 1m far above 5m,
draining inside five minutes — wants patience rather than intervention.

The instruments this skill ships get the same treatment, under its own sentence — `Before running a
check, ask what its output would be under the hypothesis you are ruling out.` **[measured-family]**
On `COD Dossier` an auditor checked tags and citations thoroughly, never checked its prerequisite
artifacts existed, and passed two skipped skill invocations at exit 0 (§1.2.2). So print the basis a
label was judged on, check a receipt before a property, and follow `references/dispatch.md`: `give
the summary something mechanical to disagree with`.

## Override 4 — two attempts, then a different move (`references/dispatch.md`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent
tool four consecutive times with nothing changed between attempts (§1.1.2); the other hit a
25,000-token `Read` ceiling and retried four times before pivoting to a Python split (§1.2.3).

Five `flagship` errors look transient and are not; each pivots on attempt 1.
**`references/propagation.md` is 236 KB** and exceeds the read ceiling on the first call — range or
grep it, §1.2.3's shape inside this skill's own references. **`governor-run` exit 75** is a ceiling
to shed into, not a queue to wait out. **A silent session** is two chases and then the operator.
**A session absent from the roster** is not a third chase at all — the dispatch stays uncleared and
the operator is told what it held. **An empty lane file** is a failure with a clean exit code;
`references/lanes.md` records a meter at 84% while that lane returned `402`.

## Override 5 — drained is a chain of artifacts, not a report (`## Keep the fleet fed`)

`SKILL.md` holds the finding already: `every status this skill collects is rung one`, and the
standing instruction is `reckon` then `whats-left` before recording anything as finished — now with
the sharper version beside it, `the session's own account of itself is the worst one available,
including the conductor's own`, measured on a session idle 77 minutes that believed it had been
working. **[measured-family]** The mechanism that breaks the chain is recorded (§1.2.1, n=1): a
skill said every design decision `goes through` two named skills, and the run invoked neither,
because the guidance was in context and nothing downstream depended on a file only those skills
produce. **[docs]** *"make each step a prompt and chain the prompts together in a sequence."*

```
1. reckon (by explicit path, when two cache versions exist) → reckon-<repo>.md
2. whats-left, focused on current work                      → whats-left-<repo>.html
3. the drained row cites both paths, plus the join rate from step 1
```

A drained row naming no file is a declaration: the skill's own case closed drained on green gates,
which attested the work that existed and nothing about what remained. Read that ledger **on the
branch the session works** — a trunk-based session's work was called two-day-old for reading `main`.

## Override 6 — ask the closed set; cap the fan-out (`## Keep the fleet fed`, `## Starting sessions`)

`SKILL.md` gives idle a four-row table and five more shapes in prose — stopped-starting,
mid-long-call, throughput-capped, prompt-parked, finished-and-silent — and says `Ask; do not
infer`. Asking how it is going returns a mood; asking *which of these nine, and what is your next
concrete action* returns something checkable. **[docs]** *"The response is correct, but the model
didn't stay within the bounds of the options."* — the remedy is a multiple choice; and *"Avoid
premature conclusions: There may be multiple relevant options for a given situation."*, which is
why drained and capped must not be collapsed. Read the roster's `status` word first: a session
showing `waiting` is parked on an unanswered `AskUserQuestion` and needs the operator, not a chase.

The same discipline runs on the spawn side, now ordered: in-session serial work, then workflow
fan-out and background agents in your own session, then a tab. `cap that fan-out at four. The
conducting itself is never delegated.` is read back in Override 2's first row, the tab in its
fifth. And **a brief you write is a prompt** — one to a *Gemini* peer carries the two ledgers
above, where `references/tiered-delegation.md` is right that an Opus worker's does not.

## Override 7 — what you cannot re-derive is stated as unavailable (`## The role's structural exposure`)

`flagship` names the exposure precisely: `re-derive what you can, and send the question rather
than the finding for what you cannot`, and `A stated inability beats a better number.` **[docs]**
Google's strictly-grounded system instruction ends on that clause: *"If the exact answer is not
explicitly written in the context, you must state that the information is not available."* Adopt
it verbatim for any figure you publish about another session. **[measured-family]** The adjacent
failure is n=1 (§1.1.4): a previous-generation accent colour returned confidently — an old fact,
not a guess. **[docs]** *"Your knowledge cutoff date is January 2025."* So `~/Dev/ARMADA.md` figures
are claims until a session confirms them, index and detail both, and **a file or skill named in a
message is loaded before the answer is written** — §1.2.4 recorded a run answering from memory when
three skills were named, then launching one when an answer was wanted.

## Override 8 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation,
or advanced function calling scenarios."* Conducting a fleet is multi-step planning, so `HIGH` is
what Google describes this work as needing; 3.7 Flash defaults to `MEDIUM` and the uplift is
unmeasured on this corpus. **[measured-family]** Do not raise it as a remedy for anything above:
paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58 (§2.3), and the
bound-shaped share of failures *rose* from 58% to 86%. **[docs]** *"Higher thinking levels
encourage the model to use more tools to explore and verify, so lowering the level can reduce tool
calls."* — fewer tool calls is the wrong direction for a skill whose error is a figure it did not
re-read.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and
response format, at the end of the prompt."*

1. Write the roster's size down before the first dispatch; report `N of N` after, `unknown` for a
   session that never answered and a named row for one that vanished.
2. Fill the bound ledger from the messages you sent, not from `SKILL.md` — six rows, the tab and
   the kill classification included.
3. Every figure ships its command, output, occupants, process census and timestamp; a disk or
   thermal transition needs a second read before it gates.
4. One retry on a transient error; none on a 236 KB read, an exit 75, a second chase, an absent
   session, or an empty lane file.
5. `reckon` and `whats-left` produce files the drained row cites by path, read on the session's
   own branch; ask the nine-shape question as a closed set after the roster's `status`; cap
   subagents at four and tabs at last resort; state as unavailable what you cannot re-derive.
