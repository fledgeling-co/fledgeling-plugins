# better-goal on Gemini

The skill's canon transfers. What does not is the assumption that a rule stated in
prose gets executed — and this skill is unusually exposed to it, because everything
it builds exists to stop a run claiming work it did not do. The same failure applies
one level up: a harness reported as armed and a harness that *is* armed differ in a
file on disk, not in a transcript. Read this before `## Protocol`.

## Epistemic status

**Tiers used.** `[docs]` — Google's guidance, quoted verbatim and gate-checked.
`[measured-family]` — Gemini runs of *other* skills: two sessions at n=1 each, plus
106 benchmark tasks scoring `gemini-3.7-flash` at `medium` and `high` against
`claude-opus-5`. `[derived]` — reasoning from those plus this skill's own scripts.
**No `[measured-here]`:** n=0, no Gemini run of `better-goal` has been observed.

**The tier the evidence is about.** Every measured rate here is flash-tier —
`gemini-3.7-flash` at both effort levels, plus one `gemini-3.7-flash-high` session.
Do not project them onto the Pro tier; there the overrides hold as `[docs]`-grounded
discipline while every `[measured-family]` number is open. Defaults differ by tier
too — **[docs]** *"The default thinking effort is now medium, changed from high in
Gemini 3 Flash Preview."*

**Read in one pass.** **[docs]** *"Avoid writing a prompt with non-linear logic or
conditionals that require the model to piece together fragmented instructions from
multiple different places in the prompt."* A side-file is that shape, so each
override is anchored to a step.

**Unmeasured on this skill:** no Gemini run has armed a goal harness, so every
override is transfer plus docs; no run anywhere has been measured *with* a
`gemini.md` against the same work without one, so there is no evidence the fixes
work; nothing measures Gemini authoring shell gates or reading exit codes; and O3's
preflight finding is read off `preflight.sh`'s arguments, not seen failing.

## No route-out block, and why

This pass produces a markdown brief, a JSON state file, a `--dry-run` diff and a
`Monitor` call. None of the four shapes the corpus measured behind — a
self-contained page authored from prose, a brownfield multi-file edit, judged
visual quality, a contract that must not regress — describes that;
`regression-sensitive` is the near miss, since `.claude/settings.local.json` is
load-bearing across every session in scope, but `arm.sh` makes that edit behind a
diff you show first. **[docs]** *"Avoid using prompts that ask the model to perform
a task for which it has a known, fundamental limitation."* — that applies to the
**delivery** work the armed run then does, which belongs in that skill's own file.

## What transfers intact

- **The architecture is already the fix.** A command Stop hook judged by exit code
  is what the `[measured-family]` evidence says this family needs: one run wrote
  itself a five-row review claiming a browser engine that never ran and a contrast
  pass rate that inverted the truth. A guard running `pnpm test` cannot be told a
  story — failure mode #3 already.
- **Failure mode #15** — a skill named in an instruction silently does not run —
  is the mechanism a Gemini run hit elsewhere, and its remedy (*make it a gate
  command instead*) is the right one. The scan found **0** qualitative skill
  references to convert; #15 handles them structurally.
- **The register is calm and brevity is the resting state** — **0** emphasis
  tokens across the skill and its five references, where **[docs]** shouted
  instructions are where *"foundation model performance will no longer improve and
  in many cases will get worse"*; and **[docs]** *"By default, Gemini 3 models
  provide direct and efficient answers."* Trim preamble, never a pasted receipt.

## O1 — the quota ledger (steps 1–2)

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition."* **[measured-family]** on one run every requirement the
brief *enumerated* shipped (12 of 12), while every requirement named
*categorically* shipped once or not at all: all states → 1, all menus → 0. Step 1
already says it — a finish line phrased *"until all items are complete"* that never
names the items cannot be verified, because there is no list to count against. So
write this ledger into the brief first, one row per scope with a number and the
command that reads it back, and report the fraction at delivery:

| # | the scope, as the skill states it | number | readback |
|---|---|---|---|
| Q1 | *until all items are complete* (step 1) | 14 rows, `F-001`…`F-014` | `grep -c '^| F-' docs/goals/goal-<slug>.md` = the `Total:` line |
| Q2 | every worklist row carries a status and a gate | 14 of 14 | rows with an empty `Gate` cell, or a status outside pending/in-progress/merged/parked = 0 |
| Q3 | *every file it would touch* (step 5) | 2 | files named by `arm.sh --dry-run` = files in the diff you showed |
| Q4 | *Every skill named in the brief* (step 4) | 2 named → 2 resolved | `preflight.sh --skills …` prints 2 `skill /…` rows |
| Q5 | the six preflight checks (step 4 table) | 6 of 6 | one line each in what you paste |

## O2 — verify the harness, not only the work (steps 4–6)

**[docs]** *"Include specific verification steps in either the system instructions
or your prompts directly."* and *"Verify your claims by quoting the exact
applicable information (including policies) when referring to them."* **This
reverses the house style deliberately:** removing verification scaffolding suits a
model that over-verifies, and inheriting that removal here is the defect. Note
where the exposure sits — this skill's *product* is verification, so the risk is
not an unverified feature but the word `armed` in a closing report nobody read back
off disk. After `arm.sh`, before step 8, paste this:

```
$ jq -r '"\(.slug) armed=\(.armed) sid=\(.session_id|length) gates=\(.verify|length)"' .claude/goals/ship-remaining-work.json
ship-remaining-work armed=true sid=36 gates=4
$ jq '[.hooks.Stop[]?.hooks[]? | select(.command|test("guard.sh"))] | length' .claude/settings.local.json
1
```

A number in the report with no command beside it is not a fact, and an empty
`session_id` is the guard refusing to act — a run that never fires, reported as
armed. **[measured-family]** where verification was assumed, the vacuum filled with
a named engine that never ran and an audited-target count nothing produced.

## O3 — gate receipts, and the denominator that is zero (step 4)

**[docs]** for anything counted, code execution *"should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation"*, and a
receipt is machine-readable: *"use a widely recognized standard like JSON, XML,
Markdown or YAML that can be parsed by common libraries"*.

- **Paste the preflight output including its final verdict line**, not a claim
  about it — step 4 says report what failed, so report what passed, as rows — and
  **prove each gate can fail before arming**, recording the exit codes.
- **`[derived]`: a bare `preflight.sh` prints `preflight: clear to arm` having
  checked no skill, no port and no process.** `--skills`, `--ports` and `--procs`
  are opt-in in its argument parsing; unset, those loops never run and emit no
  rows — a denominator of zero wearing a pass. Pass the flags the brief earns and
  count the rows against Q4 and Q5.
- **Make the first gate a prerequisite check.** A gate set testing only final
  properties lets an upstream skip pass cleanly: **[measured-family]** on another
  skill a thorough auditor returned exit 0 over two design artifacts that were
  never produced. So `verify[0]` is `test -s docs/goals/goal-<slug>.md`.

## O4 — the bound ledger for arming (step 3, step 6)

`bounded-constraint` fired **below threshold** (1 of its 14 distinct triggers), so
it is not a module here — but its bounds are real and the failure is the expensive
one. **[measured-family]** across 106 tasks, 58% of Gemini's failing UI assertions
at `medium` and **86%** at `high` were bound-shaped — a stated maximum exceeded —
against 8% for opus; the most-repeated bound failed on *every* instance in its set
on a run that passed 37 of its 39 other assertions. A bound is violated by what you
did not write, so it survives every check that looks at what you did. **[docs]**
constraints get a *"Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt."* — which is this,
carrying values.

| bound | stated at | readback | expected |
|---|---|---|---|
| `guard.sh` registered **once** | step 6 | the `jq` count in O2 | `1` |
| **one gate, one question** — no `&&` chains | step 3 | `jq -r '.verify[].cmd' <state> \| grep -c '&&'` | `0` |
| every gate fails **now** | `gate-craft.md` | run each `cmd`, record `$?` | non-zero per unfinished gate |
| gates are **read-only** | `gate-craft.md` | `git status --porcelain` before and after one pass | identical |
| **one** subagent at most | `## Delegation` | count the survey agents spawned | `≤ 1` |
| a composed `/goal` condition ≤ **4,000** chars | `mechanics.md` | `printf '%s' "$CONDITION" \| wc -c` | `≤ 4000` |

## O5 — passes with artifact dependencies (steps 1–8)

**[docs]** *"Break the requests into separate prompts."*, and the chaining remedy:
*"make each step a prompt and chain the prompts together in a sequence"*. The
protocol is already eight ordered steps; the override is to make each one's output
a **file the next step reads**, so a skipped step fails rather than vanishes:
step 1 → the worklist rows · step 2 → `docs/goals/goal-<slug>.md` · step 3 →
`verify[]` in the state file · step 4 → the pasted preflight receipt · step 5 → the
shown dry-run diff · step 6 → `.claude/goals/<slug>.json` · step 7 → the `Monitor`
call · step 8 → a report quoting steps 4 and 6 back. **[measured-family]** on
another skill a composition instruction phrased as a lens rather than a step was
satisfied by writing compliant-looking code, and the model's own diagnosis named
the reason — nothing downstream depended on a file only that skill produced.
Failure mode #15 is that shape; prefer a gate command to a skill named in the brief.

## O6 — delegation and the forks it offers

The cap is one, and the skill sets it: a subagent only to survey a backlog too
large to read directly, one agent, never to review the brief or check the gates —
the guard is the verifier. **[docs]** on forks, the failure to avoid is that *"the
model didn't stay within the bounds of the options"*, so resolve each as a closed
set with the choice written into the brief: arm now or hand back (the subagent
branch), watcher or cron, the `stuck_after` value. On acting rather than asking,
**[docs]** *"Prefer calling the tool with the available information over asking the
user, unless"* a later step needs the missing value — step 1's read of
`ORCHESTRATOR.md`, `git status` and `status.sh`. And before step 5's apply,
**[docs]** *"only take an action after all the above reasoning is completed. Once
you've taken an action, you cannot take it back."*

## O7 — the count contract, extended (step 8)

The skill already promises counts: the worklist total, one ledger row per turn,
`status.sh`. Extend them twice — derive a count where the intent omits one, and
cover the **cells** rather than only the top-level items. Step 8 names seven things
to close with, so report seven. **[docs]** *"Ensure that all requirements,
constraints, options, and preferences are exhaustively incorporated into your
plan."*

## O8 — one worked example before the set (steps 2, 8)

**[docs]** *"We recommend to always include few-shot examples in your prompts."*
and *"you can remove instructions from your prompt if your examples are clear
enough in showing the task at hand"*. So author `F-001` at full fidelity — item,
gate command, status — before the other thirteen rows, and measure them against it.
The closing block, shipped filled rather than described:

```
armed  ship-remaining-work — 14 rows, F-001…F-014, 0 rows without a gate
gates  4 of 4 hand-run before arming: brief-exists 0 · queue-empty 1 · typecheck 1 · tests 1
pre    preflight.sh --skills /ship-fleet:ship-fleet --ports 3000 → "clear to arm", 11 rows, 0 BLOCK, 2 warn
bounds 60 iterations · deadline 2026-08-24T09:00:00Z · stuck_after 3
watch  Monitor persistent — watch.sh ship-remaining-work --stale 25 (STALL/RESUMED/DONE/ENDED/GONE)
read   ledger docs/goals/goal-ship-remaining-work.ledger.md · status scripts/status.sh · stop scripts/disarm.sh ship-remaining-work
```

## O9 — the retry ceiling

**[docs]** *"On *other* errors, you must change your strategy or arguments, not
repeat the same failed call."* Two attempts per tool, then change approach; a
permanent error gets one. **[measured-family]** four consecutive invocations of an
absent tool with nothing changed between them on one run, and four consecutive
`Read` failures against a token ceiling on another. Here, `preflight.sh` exits **2**
with `requires a value` when a flag is passed last with nothing after it — a
malformed command line, fixed on attempt 1; and a missing `jq` blocks the guard,
the watcher and `status.sh` together, so install it or say the harness cannot be
armed. A gate failing identically is the skill's own `stuck_after` — that rule
applies to you first.

## O10 — recall is not a source, and read-then-answer

**[docs]** *"Your knowledge cutoff date is January 2025."* The harness constants
are version-dependent facts: the 8-block cap, the 4,000-character condition, the
hook timeouts and the `Monitor` delivery path come from one Claude Code version and
`references/mechanics.md` records which — read it rather than recall a number whose
source is three lines away. A file or skill *named in the prompt* gets loaded before
the answer is written: read, then answer, two ordered steps, neither substituting
for the other. **[measured-family]** asked a question naming three skills, one run
answered from memory without loading any; asked to fix that, it inverted the error
and launched a skill instead of answering. And `has the goal been met?` is answered
from the ledger, whose last row being an hour old answers it too.

## O11 — `thinking_level`, as what it is for

**[docs]** `HIGH` is *"suitable for complex prompts requiring deep reasoning, such
as multi-step planning, verified code generation"*, which is what steps 1–6 are,
and Gemini 3.7 Flash defaults to `MEDIUM`. **Not a remedy, though:**
**[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on
24 and tied on 58, mean −1.7 points; nothing in O1, O2 or O4 improves by raising
it, and any uplift on this skill's work is unmeasured. One real coupling —
**[docs]** *"Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls."* — touches step
1's survey, read-heavy by design.

## Modules not written, and why

`visual` — nothing is rendered and no one looks at a capture. `states` — the
unhappy paths are failure modes with fixes, enumerated in prose that transfers.
`platform-values` — the vendor values cited are Claude Code's own, each sourced in
`mechanics.md`. `authorship` — the brief is read by the run, not published to a
reader who acts on it unverified. `injection` — nothing ingested was authored
elsewhere. `emphasis` — 0 tokens. `bounded-constraint` — below threshold, folded
into O4. `gate`, `delegation` and `count-contract` fired at 4, 4 and 3 and are O3,
O6 and O7.
