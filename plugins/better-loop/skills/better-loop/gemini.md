# better-loop, calibrated for Gemini

Read this once before step 1, then run the skill as written with these overrides.

The skill's subject is this file's subject one level down. better-loop exists because a schedule
re-sends what the session already knows; a Gemini run of it fails the same way, smaller — the six
steps get followed literally and completely, and the numbers they were meant to turn into cells stay
in prose. `Deliver that scope. The armed loop does the underlying work; this pass sets it up.` Two
artifacts are calibrated: this pass, and the tick protocol it leaves behind for later runs.

**What changed since this file was last written.** The skill now stamps `last_poll_at` on every
poll, registers a `SessionStart` sentinel, and carries a new operating rule — ``armed: true` is a
claim, `last_poll_at` is the evidence.` That is Override 1 written by the skill itself, so the
overrides point at it; step 6's report grew a ninth element, and step 5 no longer claims the skill
changes no settings.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md`. The strongest tier, and most of this file rests on it. |
| `[measured-family]` | Two recorded Gemini sessions of *other* skills — `Egress Gemini` (2026-08-17, a UI mock) and `COD Dossier` (2026-08-23, a research-and-authoring pipeline) — plus the 106-task `diolog-2.0` benchmark. **n=1 each for the sessions.** Neither invoked this skill. |
| `[derived]` | My reasoning from those, said as such — including every figure `scan_skill.py` reports, which is a static read of this text and not a run of any model. |

**No `[measured-here]` tier, and the previous version was wrong to use one** for the scan's counts:
that tier means a Gemini run of *this* skill, and none exists. Those rows are `[derived]` now.

**Which model the numbers are about.** Every measured rate here is flash-tier — `gemini-3.7-flash`,
plus one `gemini-3.7-flash-high` session — so do not project them onto Pro, where the overrides
stand as `[docs]`-grounded discipline and every `[measured-family]` number is open. **[docs]** The
defaults drift inside the family, so name the tier: *"The default thinking effort is now medium,
changed from high in Gemini 3 Flash Preview."*

**Unmeasured on this skill:** no Gemini run of `better-loop` has been observed. Nothing below is
measured on this target — not whether the step 6 report collapses, not whether the bounds get read
back off the armed state file, not whether the sentinel's registration is checked, not whether a
tick protocol written by this family gets executed by the next run. **[docs]** A caution about this
file's own shape: *"Avoid writing a prompt with non-linear logic or conditionals that require the
model to piece together fragmented instructions from multiple different places in the prompt."*
Read it in one pass; each override names its step.

## No route-out block, and why

**[derived]** None of the four shapes the corpus measures behind — `static-page`,
`brownfield-integration`, `visual-design`, `regression-sensitive` — is what this pass produces: one
bash probe, one markdown brief from a supplied template, one `Monitor` call. **[docs]** The sentence
it would have rested on — *"Avoid using prompts that ask the model to perform a task for which it
has a known, fundamental limitation."* — applies one level down: where the **tick's** work is one of
those shapes, the brief carries `lane_pick.py --task implementation --shape <shape>` (from
`defer/skills/defer/scripts/`) as a line the tick runs, not a model pinned into the brief.

## What transferred intact

- **The six steps are already a chained sequence with file outputs.** Probe →
  `docs/loops/loop-<slug>.md` → `preflight.sh` → `arm.sh` writes `.claude/loops/<slug>.json` and
  prints the `Monitor` line → the report reads that line. **[derived]** the scan finds **zero**
  qualitative skill references, so C4's usual conversion is done. **[docs]** *"make each step a
  prompt and chain the prompts together in a sequence"*.
- **The bounds already carry numbers** — 12 wakes/hour, 1800s doubling to a 4h cap, 25,000 bytes,
  500 register entries, a 30s interval floor, and now a heartbeat deadline of three intervals
  floored at 120s. **[docs]** *"Instead, provide objective constraints"*. These already are, which
  is why they survive here when the prose around them does not.
- **The new operating rule is already a readback.** ``armed: true` is a claim, `last_poll_at` is the
  evidence.` names a field, a comparison and the moment they disagree. Execute it; do not restate it.
- **`templates.md` ships filled artifacts** — a five-row ledger, a populated state file, the arming
  sequence — so the gap is what *you* fill in beside them. **The skill does not shout** (**[derived]**
  zero MANDATORY / CRITICAL / FORBIDDEN tokens in 838 lines), **delegation is capped** at `one agent,
  not several`, and **`preflight.sh` is a real gate**. Keep all four.

## The quota ledger — filled, not described

**[derived]** The scan returned 6 categorical rows across 4 phrasings. I bound **1** and dropped
**5** as prose rather than deliverable scope: `the whole state` / `the full state` for what the
watcher does *not* send (SKILL.md:18, :134; `templates.md`:24), and `every field` in the
route-to-better-goal test (SKILL.md:99; `failure-modes.md`:100). **[measured-family]** Why a table:
on `Egress Gemini` every *enumerated* requirement shipped — twelve named features — and every
*categorical* one shipped once or not at all: all states → 1, all menus → 0, all flows → 0. The rows
below are enumerations this skill states in prose and never counts; write the table into
`docs/loops/loop-<slug>.md` before arming, filled from the worked case:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| Every mechanism considered before choosing — SKILL.md step 1; `mechanism-choice.md` table | **8** candidate rows | 8 read, 1 chosen (watcher), 7 rejected in a line each | `8/8 considered · chose watcher · 7 rejected with reasons` |
| `resolve any errors in the harness or config` — `mechanism-choice.md`:37, the request itself | **9** error classes the probe can emit | 6 log classes + PROC-EXIT + PROC-STALL + NO-PROC | `9/9 classes have a branch in the tick protocol` |
| Every section of the tick protocol — `templates.md` | 7 tick steps + 5 sections = **12** cells | 12 written, 0 placeholder | `12/12 sections written, no template text left` |
| The report block — SKILL.md step 6 names the parts in prose | **9** named elements (the sentinel is the new one) | 9 | `9/9 elements in the report block` |
| Every terminal state the filter must match — `mechanics.md`; `failure-modes.md` #6 | 5 watcher emissions + **4** process states | 5 confirmed in `watch.sh`; PROC-EXIT/STALL/NO-PROC added to the stream filter | `5/5 emissions · 4/4 process states covered` |

The trap the skill half-names: `if this process crashed right now, would my filter emit anything?`
is a question in prose, and a question in prose is answered by agreeing with it.

## The bound ledger — read back off the armed loop, not off the brief

**[measured-family]** `geminify/references/evidence.md` §2.2 — across the benchmark, 58% of failing
UI assertions at `medium` and **86%** at `high` were bound-shaped, against 8% for opus; the most-
repeated bound failed on *every* instance in its set while the same run passed 37 of its 39 other
assertions. A bound is violated by what you did not write, so it survives every check of what you
did. **[docs]** Google names where constraints belong, in the **Recap** component: *"Concise repeat
of the key points of the prompt, especially the constraints and response format, at the end of the
prompt."* This table is that recap, carrying values. Fill it after `arm.sh` runs, from the state
file and settings:

| bound | stated | readback | observed | within? |
|---|---|---|---|---|
| wake budget | 12/h | `jq .max_wakes .claude/loops/benchmarks.json` | `12` | yes |
| repeat-after | 1800s, doubling, 4h cap | `jq .repeat_after …` | `1800` | yes |
| interval | ≥30s (preflight warns below) | `jq .interval …` | `120` | yes |
| heartbeat deadline | 3 × interval, floored at 120s | `jq '.last_poll_at' …` then `status.sh benchmarks` | `null` — no poll yet | n/a until armed |
| sentinel | 1 `SessionStart` hook, or 0 declared with `--no-sentinel` | `jq '[(.hooks.SessionStart//[])[]\|(.hooks//[])[]\|.command//""]\|map(test("sentinel"))\|any' .claude/settings.local.json` | `true` | yes |
| probe width | ≤50 lines, every line one you would act on | `<probe> \| grep -c .` | `6` | yes |
| loops armed in this repo | 1 per concern | `ls .claude/loops/*.json \| wc -l` | `1` | yes |
| `.claude/loop.md`, when composing with `/loop` | 25,000 bytes | `wc -c .claude/loop.md` | `1204` | yes |

**[derived]** Two of the skill's own prohibitions become counted properties here. `Narrow: only what
you would act on` is stated as taste and reads as taste; its readback is `grep -c .` plus a sentence
per line saying what you would do about it. `One loop per concern` is enforced by nothing. The
sentinel row's honest value is often `0` — `--no-sentinel` is legitimate only when the report says
so, because its cost is that nothing will ever report this loop's death.

## Override 1 — verification is asked for, and `armed` is a claim (steps 4–6)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* From the agentic template: *"Verify your claims by quoting the exact applicable
information (including policies) when referring to them."* **[derived]** Skills here are written for
a model that over-verifies, so verification scaffolding is stripped; inheriting that removal is the
defect, because `preflight.sh`, `arm.sh --dry-run` and `status.sh` only run if something runs them.
**[measured-family]** What fills the vacuum is well-formed and false: the `Egress Gemini` run wrote
itself a five-row review, all `PASS`, naming a browser engine that failed on all four invocation
attempts and never ran. The skill states the rule in its own words — ``armed: true` is a claim,
`last_poll_at` is the evidence` — and it holds one step earlier: `Monitor` returning is the evidence
that the loop is armed, `arm.sh` printing the line is not. So step 6 is pasted output, and a
denominator of zero is named rather than reported as a pass:

```
PREFLIGHT   preflight.sh --probe '…' --skills 'better-goal' --interval 120 → exit 0
            probe deterministic, 6 line(s) · /better-goal model-invocable · 1 warn
ARM         arm.sh --slug benchmarks … --dry-run → exit 0; then without it → exit 0
SENTINEL    registered on SessionStart — the settings readback above returned true
MONITOR     Monitor({ command: "…/watch.sh benchmarks …", persistent: true }) → returned,
            task id t_4f21. That return is the armed evidence.
NOT CHECKED heartbeat — last_poll_at is null until the first poll, wake:poll is 0/0. Read
            status.sh in an hour; do not assert either now.
```

## Override 2 — preflight is the gate, and a warning is not a pass (step 4)

`preflight.sh` exits `1` if any row **blocks** and `0` otherwise — a flag, not a count, and warnings
never move it. Three warnings matter as much as its blocks: a probe producing no output, a probe
over 50 lines wide, and a loop already armed here. **[derived]** Read the rows, not the exit code —
a clear exit with three warnings is an ungated arm, and the report says which. **Prove it can fail
before trusting it passing**: run it once against `date` as the probe and paste the non-zero exit
beside the real run. Provenance is `geminify/references/evidence.md` §5, where a one-line change to
that skill's own quote gate took the checked count to zero and turned every file green.

**Execution receipts, not only properties.** **[measured-family]** on `COD Dossier` a deterministic
auditor checked tags, citations and contrast thoroughly, had no check for whether prerequisite
skills had run, and returned exit 0 over two skipped invocations. `preflight.sh` shares the
blindspot: it cannot tell a written tick protocol from template text. Check that before `arm.sh` —
`grep -c '^<' docs/loops/loop-<slug>.md`, where unreplaced `<placeholders>` block arming.

## Override 3 — the retry ceiling (steps 2, 4, 5)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* Two attempts per tool, then change approach; a permanent error — `command not found`,
`jq` absent — gets one, and a hard capacity error pivots on attempt 1. **[measured-family]** Four
consecutive `Read` calls against a 25k-token ceiling with minor offset tweaks before pivoting (`COD
Dossier`), and four invocations of one absent tool with nothing changed (`Egress Gemini`).
**[derived]** The instance that bites here: when `preflight.sh` reports `probe determinism`,
re-running the same probe is the forbidden move — the failure is in the probe's *shape*, so attempt
2 is a different probe piped through `sed`/`sort`/`cut`, recorded in the brief's `## What the probe
means`. `jq` is required by `watch.sh`, `status.sh`, `sentinel.sh` and `arm.sh`'s settings write.

## Override 4 — the constants get read, not recalled; and read-then-answer (steps 1, 3)

**[docs]** *"Your knowledge cutoff date is January 2025."* For 3.7 Flash, *"users can expect updated
information for some domains while in others they may experience the model's knowledge is limited
to January 2025"*. **[measured-family]** The informative failure on `Egress Gemini` was Windows 10's
published accent colour on a Windows 11 app — a previous-generation value returned confidently.
`mechanics.md` is full of that hazard, its numbers pinned to a binary version and a docs snapshot:
25,000 bytes, 7 days, 50 tasks per session, the 60–3600s pacing clamp, the ~20-minute fallback fire,
the three-intervals-floored-at-two-minutes heartbeat deadline, and the v2.1.196 rule that a
scheduled fire only runs skills the model may invoke on its own. Read them out of the file.

**[measured-family]** The read-then-answer half, from `COD Dossier` §1.2.4: asked a question that
*named three skills*, the run answered from memory without loading any, then, asked to fix it,
inverted the error and launched a skill instead of answering. Both directions are wrong here. When
the request names a skill or file — `loop on /code-review every hour` — load it first, then write
the tick protocol; when the user asks about a loop, answer from `status.sh` rather than arming
something. `preflight.sh --skills` is the mechanical half only: it proves a skill *can* be invoked
from a wake, the trap `mechanics.md` names as a loop that ticks forever and reviews nothing.

## Override 5 — the tick protocol is a prompt, so write it as one (step 3)

The longest reach of any override here: `docs/loops/loop-<slug>.md` is read by every tick after
this pass ends. **[docs]** *"Be concise in your input prompts. Gemini 3 responds best to direct,
clear instructions."* The skill agrees — `Keep it short. Detail belongs in the source-of-record file
the tick reads.` — so the brief carries commands and branches, not rationale. **[docs]** On the
branches: *"provide instructions for handling missing data rather than assuming inserted data will
always be present and well-formed"*. Three go missing most often, and the skill names all three: the
already-seen failure that will not be reported again, the no-op tick, and the item blocked on a
person, which goes to `## Open questions` and does not park the loop.

**[measured-family]** The phrasing rule, from `COD Dossier` §1.2.1: composition phrased as a lens or
standard was satisfied by writing compliant-looking code, because nothing downstream depended on a
file only that skill produces. **[derived]** none of that phrasing is in `better-loop`, so it lands
on what you write into the tick: `review the failures with code-review's lens` gets skipped, while a
step that runs a command, writes a file, and is followed by a step reading that file, does not.

## One worked example, before the set

**[docs]** *"We recommend to always include few-shot examples in your prompts."* and *"you can
remove instructions from your prompt if your examples are clear enough in showing the task at
hand"*. Author **one** tick branch at full fidelity before the rest, in the brief:

```markdown
3. **If it is a failure:** classify the delta line, then take exactly one branch.
   - `Traceback|FAILED` → `tail -40 runs/current.log`; fix harness or config; restart with
     `scripts/run.sh --resume <run-id>`; `scripts/tick.sh benchmarks fixed "<one line>"`.
   - `OOM|Killed` → halve `concurrency` in `bench.config.json`; restart; verdict `fixed`.
   - `rate.?limit` → do nothing for one backoff period; verdict `held`; note the provider.
   - `exit code [1-9]` not matching the above → verdict `blocked`; write the question and your
     recommendation under `## Open questions`, then carry on with the next run.
   - `PROC-EXIT` with no matching log line → it died without writing; verdict `blocked`.
```

**[docs]** *"Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats."* Every later branch carries the same four parts in the same
order — trigger, command, ledger verdict, escalation — including where escalation is `none`.

## `thinking_level`

**[docs]** Choosing a mechanism against eight candidates, designing a deterministic probe and
writing an executable tick protocol is what `HIGH` is for — *"suitable for complex prompts requiring
deep reasoning, such as multi-step planning, verified code generation, or advanced function calling
scenarios"* — and Gemini 3.7 Flash defaults to `MEDIUM`. **[measured-family]** Paired across 106
tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7 points: this is what the
level is *for*, not a remedy — nothing in the two ledgers or Override 1 improves by raising it.
**[docs]** *"Higher thinking levels encourage the model to use more tools to explore and verify, so
lowering the level can reduce tool calls."* That governs this pass; the loop's cost is the probe's.

## Modules deliberately not written

**[derived]** The scan fired two at the three-trigger threshold — `gate` (4 hits) and
`bounded-constraint` (3) — both written above. Eight did not. **`visual`**: renders nothing.
**`states`**: the unhappy paths are the watcher's five emissions, the four process states and the
dead-loop state the sentinel reports, bound as quota rows rather than a matrix.
**`platform-values`**: the constants come from `mechanics.md`, not a vendor design system, so
Override 4 covers them. **`authorship`**: nothing is written for a reader to act on as fact.
**`delegation`**: capped already, in *What transferred intact*. **`injection`**: the probe reads the
repo's own tooling. **`count-contract`**: folded into the quota table. **`emphasis`**: zero tokens.
