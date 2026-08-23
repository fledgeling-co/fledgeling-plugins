# better-loop, calibrated for Gemini

Read this once before step 1, then run the skill as written with these overrides.

The skill's subject is this file's subject one level down. better-loop exists because a schedule
re-sends what the session already knows; a Gemini run of it fails the same way, smaller — the six
steps get followed literally and completely, and the numbers they were meant to turn into cells stay
in prose. `Deliver that scope. The armed loop does the underlying work; this pass sets it up.` Two
artifacts are calibrated here: this pass, and the tick protocol it leaves behind for later runs.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md`. The strongest tier, and most of this file rests on it. |
| `[measured-family]` | Two recorded Gemini sessions of *other* skills — `Egress Gemini` (2026-08-17, a UI mock) and `COD Dossier` (2026-08-23, a research-and-authoring pipeline) — plus the 106-task `diolog-2.0` benchmark. **n=1 each for the sessions.** Neither invoked this skill. |
| `[measured-here]` | `scan_skill.py` over this SKILL.md and its four references, 2026-08-23: 794 lines, 6 quota rows (1 kept), 3 bound rows, **0 qualitative skill references, 0 emphasis tokens**. A scan of the text, not a Gemini run. |
| `[derived]` | My reasoning from those, said as such. |

**Which model the measured numbers are about.** Every measured rate behind this file is flash-tier
— `gemini-3.7-flash`, plus one `gemini-3.7-flash-high` session — so read them as claims about Flash
and do not project them onto the Pro tier, where the overrides below stand as `[docs]`-grounded
discipline and every `[measured-family]` number is an open question. **[docs]** The defaults drift
inside the family, so name the tier rather than ranking it: *"The default thinking effort is now
medium, changed from high in Gemini 3 Flash Preview."*

**Unmeasured on this skill:** no Gemini run of `better-loop` has been observed. Nothing below is
measured on this target — not whether the step 6 report collapses, not whether the bounds get read
back off the armed state file, not whether a tick protocol written by this family gets executed by
the next run. No comparison exists between a run with this file and one without, and nothing here is
a rate. **[docs]** A caution about this file's own shape: *"Avoid writing a prompt with non-linear
logic or conditionals that require the model to piece together fragmented instructions from multiple
different places in the prompt."* Read it in one pass; each override names its step.

## No route-out block, and why

**[derived]** The corpus measures a model *building* an artifact and names four shapes far enough
behind to route away: `static-page`, `brownfield-integration`, `visual-design`,
`regression-sensitive`. None is what this pass produces — one bash probe, one markdown brief from a
supplied template, three shipped scripts, one `Monitor` call — so a four-row table copied whole
would route away work never measured as hard, and there is none here. **[docs]** The sentence it
would have rested on — *"Avoid using prompts that ask the model to perform a task for which it has
a known, fundamental limitation."* — applies one level down: where the **tick's** own work is one
of those shapes, the tick protocol carries `lane_pick.py --task implementation --shape <shape>`
(from `defer/skills/defer/scripts/`) as a line the tick runs, not a model pinned into the brief.

## What transferred intact

- **The six steps are already a chained sequence with file outputs.** Probe →
  `docs/loops/loop-<slug>.md` → `preflight.sh` → `arm.sh` writes `.claude/loops/<slug>.json` and
  prints the `Monitor` line → the report reads that line. **[measured-here]** the scan found **zero**
  qualitative skill references, so C4's usual conversion is already done. **[docs]** *"make each
  step a prompt and chain the prompts together in a sequence"*.
- **The bounds already carry numbers** — 12 wakes/hour, 1800s doubling to a 4h cap, 25,000 bytes,
  500 register entries, a 30s interval floor. **[docs]** *"Instead, provide objective constraints"*.
  These already are, which is why they survive here when the prose around them does not.
- **`templates.md` ships filled artifacts** — a five-row ledger, a populated state file, the arming
  sequence — so the gap is in what *you* fill in beside them. **The skill does not shout**
  (**[measured-here]** zero MANDATORY / CRITICAL / FORBIDDEN tokens), **delegation is capped** at
  `one agent, not several`, and **`preflight.sh` is a real gate** that exits with the count of
  failing rows. Keep all four.

## The quota ledger — filled, not described

**[measured-here]** The scan returned 6 categorical rows. I bound **1** and dropped **5** as prose
rather than deliverable scope: `the whole state` / `the full state` describing what the watcher
does *not* send (SKILL.md:18, :120; `templates.md`:24), and `every field` in the route-to-better-goal
test (SKILL.md:97; `failure-modes.md`:100). **[measured-family]** Why a table and not a sentence: on
`Egress Gemini` every *enumerated* requirement shipped — twelve named features — and every
*categorical* one shipped once or not at all: all states → 1, all menus → 0, all flows → 0. The
rows below are enumerations this skill states in prose and never counts; write the table into
`docs/loops/loop-<slug>.md` before arming. Filled from the benchmark-monitoring worked case:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| Every mechanism considered before choosing — SKILL.md step 1; `mechanism-choice.md` table | **8** candidate rows | 8 read, 1 chosen (watcher), 7 rejected in a line each | `8/8 considered · chose watcher · 7 rejected with reasons` |
| `resolve any errors in the harness or config` — `mechanism-choice.md`:37, the request itself | **9** error classes the probe can emit | 6 log classes + PROC-EXIT + PROC-STALL + NO-PROC | `9/9 classes have a branch in the tick protocol` |
| Every section of the tick protocol — `templates.md` | 7 tick steps + 5 sections = **12** cells | 12 written, 0 placeholder | `12/12 sections written, no template text left` |
| The report block — SKILL.md step 6 names the parts in prose | **8** named elements | 8 | `8/8 elements in the report block` |
| Every terminal state the filter must match — `mechanics.md`; `failure-modes.md` #6 | 5 watcher emissions + **4** process states | 5 confirmed in `watch.sh`; PROC-EXIT/STALL/NO-PROC added to the stream filter | `5/5 emissions · 4/4 process states covered` |

The trap the skill half-names: `if this process crashed right now, would my filter emit anything?`
is a question in prose, and a question in prose is answered by agreeing with it.

## The bound ledger — read back off the armed loop, not off the brief

**[measured-family]** `geminify/references/evidence.md` §2.2 — across the benchmark, 58% of failing
UI assertions at `medium` and **86%** at `high` were bound-shaped, against 8% for opus; the most-
repeated bound failed on *every* instance in its set while the same run passed 37 of its 39 other
assertions. A bound is violated by what you did not write, so it survives every check that looks at
what you did. **[docs]** Google names where constraints belong, in the **Recap** component:
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at
the end of the prompt."* This table is that recap, carrying values. Fill it after `arm.sh` runs,
from the state file:

| bound | stated | readback | observed | within? |
|---|---|---|---|---|
| wake budget | 12/h | `jq .max_wakes .claude/loops/benchmarks.json` | `12` | yes |
| repeat-after | 1800s, doubling, 4h cap | `jq .repeat_after …` | `1800` | yes |
| interval | ≥30s (preflight warns below) | `jq .interval …` | `120` | yes |
| probe width | ≤50 lines, every line one you would act on | `<probe> \| grep -c .` | `6` | yes |
| loops armed in this repo | 1 per concern | `ls .claude/loops/*.json \| wc -l` | `1` | yes |
| subagents spawned | 1 max, survey only | count of `Task` calls this pass | `0` | yes |
| `.claude/loop.md`, when composing with `/loop` | 25,000 bytes | `wc -c .claude/loop.md` | `1204` | yes |

**[derived]** Two of the skill's own prohibitions become counted properties here. `Narrow: only what
you would act on` is stated as taste and reads as taste; its readback is `grep -c .` plus a sentence
per line saying what you would do about it. `One loop per concern` is enforced by nothing.

## Override 1 — verification is asked for, and `armed` is a claim (steps 4–6)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* From the agentic template: *"Verify your claims by quoting the exact applicable
information (including policies) when referring to them."* **[derived]** Skills here are written for
a model that over-verifies, so verification scaffolding is deliberately stripped; inheriting that
removal is the defect, because `preflight.sh`, `arm.sh --dry-run` and `status.sh` only run if
something runs them. **[measured-family]** What fills the vacuum is well-formed and false: the
`Egress Gemini` run wrote itself a five-row review, all `PASS`, naming a browser engine that failed
on all four invocation attempts and never ran, and a contrast pass rate from a probe never executed.
The skill knows this failure in its own domain — `a report that reads as though it armed something,
when nothing is watching, is the same failure as an invisible loop`. `Monitor` returning is the
evidence that the loop is armed; `arm.sh` printing the line is not. So step 6 is pasted output, and
a denominator of zero is named rather than reported as a pass:

```
PREFLIGHT   preflight.sh --probe '…' --skills 'better-goal' --interval 120 → exit 0
            probe deterministic, 6 line(s) · /better-goal model-invocable · 1 warn
ARM         arm.sh --slug benchmarks … --dry-run → exit 0; then without it → exit 0,
            wrote .claude/loops/benchmarks.json
MONITOR     Monitor({ command: "…/watch.sh benchmarks --interval 120 …", persistent: true })
            → returned, task id t_4f21. THIS is the armed evidence.
NOT CHECKED wake:poll ratio — 0 polls so far. Read status.sh benchmarks in an hour.
```

## Override 2 — preflight is the gate, and a warning is not a pass (step 4)

`preflight.sh` exits with the **count of failing rows**, and warnings do not count. Three of its
warnings matter as much as its blocks: a probe producing no output, a probe over 50 lines wide, and
a loop already armed here. **[derived]** Read the rows, not the exit code — a clear exit with three
warnings is an ungated arm, and the report says which. **Prove it can fail before trusting it
passing**: run it once against `date` as the probe and paste the non-zero exit beside the real run.
Provenance is `geminify/references/evidence.md` §5, where a one-line change to that skill's own
quote gate took the checked count to zero and turned every file green.

**Execution receipts, not only properties.** **[measured-family]** on `COD Dossier` a deterministic
auditor checked tags, citations and contrast thoroughly, had no check for whether prerequisite
skills had run, and returned exit 0 over two skipped invocations. `preflight.sh` shares the
blindspot: it cannot tell whether the tick protocol exists or is still template text. So check that
before `arm.sh` — `test -s docs/loops/loop-<slug>.md && grep -c '^<' docs/loops/loop-<slug>.md` —
where a non-zero count of unreplaced `<placeholders>` blocks arming.

## Override 3 — the retry ceiling (steps 2, 4, 5)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* Two attempts per tool, then change approach; a permanent error — `command not
found`, `jq` absent, a `--help` that errors — gets one. **[measured-family]** Four consecutive
`Read` calls against a 25k-token ceiling with minor offset tweaks before pivoting (`COD Dossier`),
and four consecutive invocations of one absent tool with nothing changed between them (`Egress
Gemini`); on a hard capacity error, pivot on attempt 1. **[derived]** The instance that bites here:
when `preflight.sh` reports `probe determinism`, re-running the same probe is the forbidden move —
the failure is in the probe's *shape*, so attempt 2 is a different probe piped through
`sed`/`sort`/`cut`, with the fix recorded in the brief's `## What the probe means`. Read the repo's
constraints first: `jq` is required by `watch.sh` and `status.sh`, and `arm.sh` refuses a slug that
is not a bare kebab name.

## Override 4 — the constants get read, not recalled; and read-then-answer (steps 1, 3)

**[docs]** *"Your knowledge cutoff date is January 2025."* For 3.7 Flash, *"users can expect updated
information for some domains while in others they may experience the model's knowledge is limited
to January 2025"*. **[measured-family]** The informative failure on `Egress Gemini` was not a guess
but Windows 10's published accent colour on a Windows 11 app — a previous-generation value returned
confidently. `mechanics.md` is full of that hazard, its numbers pinned to a binary version and a
docs snapshot: 25,000 bytes, 7 days, 50 scheduled tasks per session, the 60–3600s dynamic-pacing
clamp, the ~20-minute fallback fire, and the v2.1.196 rule that a scheduled fire only runs skills
the model may invoke on its own. Read them out of the file, and name it in the report.

**[measured-family]** The read-then-answer half, from `COD Dossier` §1.2.4: asked a question that
*named three skills*, the run answered from memory without loading any of them, then, asked to fix
it, inverted the error and launched a skill instead of answering. Both directions are wrong here.
When the request names a skill or a file — `loop on /code-review every hour`, `monitor the runs in
docs/plans/bench.md` — load it first, then write the tick protocol; when the user asks a question
about a loop, answer it rather than arming something. `preflight.sh --skills` is the mechanical
half and only that: it proves a skill *can* be invoked from a wake, which is the trap `mechanics.md`
names as a loop that ticks correctly forever and reviews nothing.

## Override 5 — the tick protocol is a prompt, so write it as one (step 3)

The longest reach of any override here: `docs/loops/loop-<slug>.md` is read by every tick after
this pass ends. **[docs]** *"Be concise in your input prompts. Gemini 3 responds best to direct,
clear instructions."* The skill agrees — `Keep it short. Detail belongs in the source-of-record file
the tick reads.` — so the brief carries commands and branches, not rationale. **[docs]** And on the
branches: *"provide instructions for handling missing data rather than assuming inserted data will
always be present and well-formed"*. Three go missing more often than any other, and the skill names
all three: the already-seen failure that will not be reported again, the no-op tick with nothing to
do, and the item blocked on a person, which goes to `## Open questions` and does not park the loop.

**[measured-family]** And the phrasing rule, from `COD Dossier` §1.2.1: an instruction phrasing
skill composition as a lens or standard was satisfied by writing compliant-looking code, and the
model's own diagnosis named the mechanism — nothing downstream depended on a file only that skill
produces. **[measured-here]** the scan finds none of that phrasing in `better-loop` itself, so it
lands entirely on what you write into the tick: `review the failures with code-review's lens` gets
skipped, while a tick step that runs a command, writes a file, and is followed by a step reading
that file, does not.

## One worked example, before the set

**[docs]** *"We recommend to always include few-shot examples in your prompts."* and *"you can
remove instructions from your prompt if your examples are clear enough in showing the task at
hand"*. Author **one** tick branch at full fidelity before the other eight, in the brief:

```markdown
3. **If it is a failure:** classify the delta line, then take exactly one branch.
   - `Traceback|FAILED` → `tail -40 runs/current.log`; fix harness or config; restart with
     `scripts/run.sh --resume <run-id>`; `scripts/tick.sh benchmarks fixed "<one line>"`.
   - `OOM|Killed` → halve `concurrency` in `bench.config.json`; restart; verdict `fixed`.
   - `rate.?limit` → do nothing for one backoff period; verdict `held`; note the provider.
   - `exit code [1-9]` not matching the above → verdict `blocked`; write the question and your
     recommendation under `## Open questions`, then carry on with the next run.
   - `PROC-EXIT` with no matching log line → it died without writing; verdict `blocked`.
   - `PROC-STALL` ≥600s → capture `sample -f runs`; verdict `blocked`.
```

**[docs]** *"Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats."* Every later branch carries the same four parts in the same
order — trigger, command, ledger verdict, escalation — including where escalation is `none`.

## `thinking_level`

**[docs]** Choosing a mechanism against eight candidates, designing a deterministic probe and
writing an executable tick protocol is what Google describes `HIGH` as being for — *"suitable for
complex prompts requiring deep reasoning, such as multi-step planning, verified code generation, or
advanced function calling scenarios"* — and Gemini 3.7 Flash defaults to `MEDIUM`.
**[measured-family]** Paired across 106 benchmark tasks, `high` beat `medium` on 24, lost on 24 and
tied on 58, mean −1.7 points, so this is what the level is *for* and not a remedy: nothing in the
two ledgers or Override 1 improves by raising it. **[docs]** And one trade-off on a skill whose
subject is cost: *"Higher thinking levels encourage the model to use more tools to explore and
verify, so lowering the level can reduce tool calls."* That governs this authoring pass — the armed
loop's cost is set by the probe.

## Modules deliberately not written

**[measured-here]** The scan fired two at the three-trigger threshold — `gate` (4 hits) and
`bounded-constraint` (3) — both written above. Eight did not. **`visual`**: renders nothing.
**`states`**: the unhappy paths are the watcher's five emissions and the four process states, bound
as a quota row rather than a matrix. **`platform-values`**: the constants come from `mechanics.md`,
not a vendor design system, so Override 4 covers them. **`authorship`**: nothing is written for a
reader to act on as fact. **`delegation`** (below threshold): already capped, carried as a
bound-ledger row. **`injection`**: the probe reads the repo's own tooling; wrap third-party output
before it reaches the tick. **`count-contract`**: folded into the quota table. **`emphasis`**: zero
emphasis tokens in 794 lines.
