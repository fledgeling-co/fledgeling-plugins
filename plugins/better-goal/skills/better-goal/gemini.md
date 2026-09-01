# better-goal on Gemini

The skill's canon transfers. What does not is the assumption that a rule stated in
prose gets executed — and this skill is unusually exposed to it, because everything
it builds exists to stop a run claiming work it did not do. The same failure lands
one level up: a harness reported as armed and one that *is* armed differ in a file on
disk, not in a transcript. Since this file was last written the skill has made that
distinction its own — `arm.sh` registers **four** hook events rather than one, the
state carries `hook_live: "unproven"` until the guard's first firing stamps it
`proven`, and the operating rules add the line this file was already arguing for: *A
hook you cannot prove fired is not armed.* Read this before `## Protocol`.

## Epistemic status

**Tiers used.** `[docs]` — Google's guidance, quoted verbatim and gate-checked.
`[measured-family]` — Gemini runs of *other* skills: two sessions at n=1 each,
plus 106 benchmark tasks scoring `gemini-3.7-flash` at `medium` and `high` against
`claude-opus-5`. `[derived]` — reasoning from those plus this skill's own scripts.
**No `[measured-here]`:** n=0, no Gemini run of `better-goal` has been observed.
Every measured rate is flash-tier; on Pro these overrides hold as
`[docs]`-grounded discipline while every `[measured-family]` number is open, and
the defaults differ — **[docs]** *"The default thinking effort is now medium,
changed from high in Gemini 3 Flash Preview."* A side-file is also the shape
**[docs]** warns about — *"Avoid writing a prompt with non-linear logic or
conditionals that require the model to piece together fragmented instructions from
multiple different places in the prompt."* — so read it in one pass; every
override names its step.

**Unmeasured on this skill:** no Gemini run has armed a goal harness, so every
override is transfer plus docs; nothing has been measured *with* a `gemini.md`
against the same work without one, so there is no evidence the fixes work; nothing
measures Gemini writing shell gates or reading exit codes; the `hook_live` and
`end_reason` paths have run on Claude only; and O3's findings are read off
`preflight.sh`'s source rather than seen failing.

## No route-out block, and why

This pass produces a brief, a JSON state file, a `--dry-run` diff and a `Monitor`
call — none of the four shapes the corpus measured behind. The near miss is
`regression-sensitive`, since `.claude/settings.local.json` is load-bearing across
every session in scope, but `arm.sh` shows that edit as a diff and backs the file up
first. **[docs]** *"Avoid using prompts that ask the model to perform a task for
which it has a known, fundamental limitation."* — that applies to the **delivery**
work the armed run does, which belongs in that skill's file.

## What transfers intact

- **The architecture is already the fix.** A command Stop hook judged by exit code
  is what the `[measured-family]` evidence says this family needs: one run wrote
  itself a review claiming a browser engine that never ran and a contrast pass rate
  that inverted the truth. A guard running `pnpm test` cannot be told a story —
  failure mode #3 already, and #15's remedy (*make it a gate command instead*) is
  the same move; the scan found **0** qualitative skill references left to convert.
- **The four-event registration is that discipline one level out**, and needs no
  override: `Stop` runs the gates, `StopFailure` and `SessionEnd` record the deaths
  the guard never sees, `SessionStart` reports what is still armed — **[docs]**
  *"Ensure that the prompt's instructions provide a clear path for handling edge
  cases and unexpected inputs."*
- **The register is calm** — **0** emphasis tokens across the skill and its five
  references, where **[docs]** shouted instructions are where *"foundation model
  performance will no longer improve and in many cases will get worse"*. **[docs]**
  *"By default, Gemini 3 models provide direct and efficient answers."* Trim
  preamble, never a pasted receipt.

## O1 — the quota ledger (steps 1, 4, 5, 6, 8)

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition."* **[measured-family]** on one run every *enumerated*
requirement shipped (12 of 12) while every *categorical* one shipped once or not at
all: all states → 1, all menus → 0. Step 1 already says it — a finish line phrased
*"until all items are complete"* that never names the items cannot be verified,
because there is no list to count against. Write this ledger into the brief first,
and report the fraction at delivery:

| # | the scope, as the skill states it | number | readback |
|---|---|---|---|
| Q1 | *until all items are complete* (step 1) | 14 rows, `F-001`…`F-014` | `grep -c '^| F-' docs/goals/goal-<slug>.md` = the `Total:` line |
| Q2 | every worklist row carries a status and a gate | 14 of 14 | rows with an empty `Gate` cell, or a status outside pending/in-progress/merged/parked = 0 |
| Q3 | *every file it would touch* (step 5) | **3 written, 2 diffed** | `--dry-run` prints `── settings:` and `── state:`; the third is the `.gitignore` append, which no diff shows — name it yourself |
| Q4 | the preflight checks (step 4 table) | **7 of 7** | one row each in what you paste; the settings-file row decides whether anything fires at all |
| Q5 | the hook events `arm.sh` registers (step 6) | **4** | the per-event `jq` in O2 |
| Q6 | what step 8 closes with | **8 of 8** | one line each; O7 ships the block filled |

Q3–Q6 are `[derived]` from countable things the skill names in prose; Q4 grew from
six and Q6 from seven in the last release, which is the drift a ledger catches and
a memory does not. Q6 is `count-contract` extended: report all eight things step 8
names, hook-load line first when it is bad news — **[docs]** *"Prioritize critical
instructions: Place essential behavioral constraints, role definitions (persona),
and output format requirements in the System Instruction or at the very beginning of
the user prompt."*

## O2 — report `hook_live`, never `armed` (steps 4–6)

**[docs]** *"Include specific verification steps in either the system instructions
or your prompts directly."* and *"Verify your claims by quoting the exact
applicable information (including policies) when referring to them."* **This
reverses the house style deliberately:** removing verification scaffolding suits a
model that over-verifies, and inheriting that removal here is the defect. The
exposure is the word `armed` in a closing report nobody read back off disk, and the
operating rules now name that flag as the wrong one: *Report `hook_live` rather
than the state file's `armed` flag, because the two disagree exactly when it
matters.* After `arm.sh`, before step 8, paste this:

```
$ jq -r '"\(.slug) armed=\(.armed) hook_live=\(.hook_live) sid=\(.session_id|length) gates=\(.verify|length)"' .claude/goals/ship-remaining-work.json
ship-remaining-work armed=true hook_live=unproven sid=36 gates=4
$ jq -r '[.hooks|to_entries[]|"\(.key)=\([.value[].hooks[]|select(.command|test("better-goal"))]|length)"]|join(" ")' .claude/settings.local.json
Stop=1 StopFailure=1 SessionEnd=1 SessionStart=1
```

`unproven` is the correct reading at arming, not a fault: a Stop hook fires after
the turn, so the first ledger row is the only proof there is. Say that rather than
rounding it up to armed; an empty `session_id` is the guard refusing to act at all.

## O3 — `clear to arm` is not proof that anything will fire (step 4)

**[docs]** a receipt is machine-readable — *"use a widely recognized standard like
JSON, XML, Markdown or YAML that can be parsed by common libraries"* — and code
execution *"should be enabled whenever the model needs to perform any kind of
arithmetic, counting, or calculation"*, which a denominator is.

- **`[derived]`, the sharpest one: the hook-load check is a `warn`, and a warn does
  not set `FAIL`.** `preflight.sh` can print `hook load … a hook armed in this session
  will NOT fire` and still end `preflight: clear to arm`, exit 0. Read the rows, not
  the verdict line.
- **`[derived]`: a bare `preflight.sh` prints that verdict having checked no skill,
  no port and no process.** `--skills`, `--ports` and `--procs` are opt-in; unset,
  those loops emit no rows — a denominator of zero wearing a pass.
- **Paste the output including its final line**, and **prove each gate can fail
  before arming**, recording the exit codes.
- **Make `verify[0]` a prerequisite check** — `test -s docs/goals/goal-<slug>.md`. A
  gate set testing only final properties lets an upstream skip pass cleanly:
  **[measured-family]** an auditor returned exit 0 over two artifacts never produced.

## O4 — the bound ledger for arming (steps 3, 6)

`bounded-constraint` fired **below threshold** (2 of its 14 distinct triggers), so
it is not a module here — but the bounds are real and the failure is expensive.
**[measured-family]** across 106 tasks, 58% of Gemini's failing UI assertions at
`medium` and **86%** at `high` were bound-shaped — a stated maximum exceeded —
against 8% for opus, and the most-repeated one failed on *every* instance in its set
on a run that passed 37 of its 39 other assertions. **[docs]** constraints get
a *"Concise repeat of the key points of the prompt, especially the constraints and
response format, at the end of the prompt."* — this table, carrying values.

| bound | stated at | readback | expected |
|---|---|---|---|
| **one** guard per event, four events, no duplicates | step 6 | the per-event `jq` in O2 | `1 1 1 1` |
| **one gate, one question** — no `&&` chains | step 3 | `jq -r '.verify[].cmd' <state> \| grep -c '&&'` | `0` |
| every gate fails **now** | `gate-craft.md` | run each `cmd`, record `$?` | non-zero per unfinished gate |
| gates are **read-only** | `gate-craft.md` | `git status --porcelain` before and after one pass | identical |
| **one** subagent at most | `## Delegation` | count the survey agents spawned | `≤ 1` |
| a composed `/goal` condition ≤ **4,000** chars | `mechanics.md` | `printf '%s' "$CONDITION" \| wc -c` | `≤ 4000` |

The first row is per-event, not a total, for a reason the skill records: `arm.sh`
used to match by exact path, the path carries the plugin version, and a bump left
two guards running every gate twice a turn — `4` is also what two guards on two
events look like.

## O5 — passes with artifact dependencies (steps 1–8)

**[docs]** *"Break the requests into separate prompts."*, and the chaining remedy:
*"make each step a prompt and chain the prompts together in a sequence"*. The
protocol is already eight ordered steps; make each one's output a file or pasted
receipt the next reads, so a skipped step fails rather than vanishes: 1 → worklist
rows · 2 → `docs/goals/goal-<slug>.md` · 3 → `verify[]` · 4 → the pasted preflight
rows · 5 → the dry-run diff · 6 → `.claude/goals/<slug>.json` **and the hook-load
line `arm.sh` prints** · 7 → the `Monitor` call · 8 → a report quoting 4 and 6 back.
**[measured-family]** elsewhere a composition instruction phrased as a lens rather
than a step was satisfied by compliant-looking code, because nothing depended on a
file only that skill produced.

## O6 — delegation, and the forks this skill offers

The cap is one, and the skill sets it: a subagent only to survey a backlog too large
to read directly, never to review the brief or check the gates — the guard is the
verifier. **[docs]** on forks, the failure to avoid is that *"the model didn't stay
within the bounds of the options"*, so resolve each as a closed set with the choice
written into the brief: watcher or cron, the `stuck_after` value, arm now or hand
back (the subagent branch), and what to do when the hook-load row warns. The skill
resolves that last one — arm anyway, tell the user to open `/hooks` once or restart,
say nothing is armed until they do, run the gates by hand meanwhile. On step 1's
survey, **[docs]** *"Prefer calling the tool with the available information over
asking the user, unless"* a later step needs the value; on step 5's apply, **[docs]**
*"only take an action after all the above reasoning is completed. Once you've taken
an action, you cannot take it back."*

## O7 — one worked example before the set (steps 2, 8)

**[docs]** *"We recommend to always include few-shot examples in your prompts."*
and *"you can remove instructions from your prompt if your examples are clear
enough in showing the task at hand"*. Author `F-001` at full fidelity — item, gate,
status — before the other thirteen. The closing block, shipped filled:

```
hook   LOADED — .claude/ held a settings file at session start; hook_live=unproven
       until the guard's first ledger row, the only proof a Stop hook can give
armed  ship-remaining-work — 14 rows, F-001…F-014, 0 rows without a gate
gates  4 of 4 hand-run before arming: brief-exists 0 · queue-empty 1 · typecheck 1 · tests 1
pre    preflight.sh --skills /ship-fleet:ship-fleet --ports 3000 → "clear to arm", 11 rows, 0 BLOCK, 2 warn
bounds 60 iterations · deadline 2026-08-24T09:00:00Z · stuck_after 3
watch  Monitor persistent — watch.sh ship-remaining-work (NOTLIVE/STALL/RESUMED/DONE/ENDED/GONE)
read   ledger docs/goals/goal-ship-remaining-work.ledger.md · status status.sh
stop   disarm.sh ship-remaining-work — all four registrations + the raised cap
```

`--stale` is unpinned: the watcher derives its threshold from the run's own median
turn length, and a fixed 25 was shorter than that on two of fourteen runs (28.5, 95.7).

## O8 — the retry ceiling, and recall as a source

**[docs]** *"On *other* errors, you must change your strategy or arguments, not
repeat the same failed call."* Two attempts per tool, then change approach; a
permanent error gets one — **[measured-family]** four consecutive invocations of an
absent tool with nothing changed between them. Here `preflight.sh` and `arm.sh`
both exit **2** with `requires a value` when a flag is passed last with nothing
after it, and a missing `jq` blocks the guard, the watcher, the sentinel and
`status.sh` together, so install it or say the harness cannot be armed. A gate
failing identically is the skill's own `stuck_after`, applied to you first.

**[docs]** *"Your knowledge cutoff date is January 2025."* The harness constants
are version-dependent — the 8-block cap, the 4,000-character condition, the hook
timeouts, the `Monitor` delivery path — and `references/mechanics.md` records which
version they came from, so read it rather than recall a number whose source is
three lines away. The scripts can disagree with the prose too: `arm.sh` seeds
`set_stuck_after` at 8 while `guard.sh` reads `set_notice_after` and defaults to 10,
so a readback written from memory looks for a key that is not there.
**[measured-family]** asked a question naming three skills, one run answered from
memory without loading any; `has the goal been met?` is answered from the ledger.

## O9 — `thinking_level`, as what it is for

**[docs]** `HIGH` is *"suitable for complex prompts requiring deep reasoning, such
as multi-step planning, verified code generation"*, which is what steps 1–6 are,
and Gemini 3.7 Flash defaults to `MEDIUM`. **Not a remedy:** **[measured-family]**
paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58,
mean −1.7 points. One real coupling — **[docs]** *"Higher thinking levels encourage
the model to use more tools to explore and verify, so lowering the level can reduce
tool calls."* — touches step 1's survey, read-heavy by design.

## Modules not written, and why

`visual` — nothing is rendered. `states` — the unhappy paths are eighteen failure
modes with fixes, and the three endings (`api_error`, `session_ended`, `stuck`) are
enumerated with their events. `platform-values` — the vendor values cited are Claude
Code's own, sourced in `mechanics.md`. `authorship` — the brief is read by the run,
not published to a reader who acts on it unverified. `injection` — nothing ingested
was authored elsewhere. `emphasis` — 0 tokens. `bounded-constraint` — below threshold,
folded into O4. `gate`, `delegation` and `count-contract` fired at 4, 4 and 3: they
are O3, O6 and O1's Q6.
