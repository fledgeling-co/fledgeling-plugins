---
name: defer
description: >-
  Decide which model a piece of work goes to, and produce the exact command that
  sends it there. One routing policy for every skill that hands work outside the
  session. Resolves user-preferred current model roles from the runtime first;
  a compatibility registry maps six task classes to calibrated lanes, each
  pinned to a model and an effort, with the CLI arguments, the environment GLM
  needs, and the check that proves the lane ran as routed. Narrows those lanes by
  what the work actually is, against a capability matrix measured over 106
  benchmark tasks, so a piece of work goes to the cheapest lane that scored level
  with Opus on that shape rather than to Opus by default. Where several lanes
  remain it picks the one with the most plan headroom per remaining day, measured
  — Claude and Codex report a real utilization percentage that is already on
  disk, and Grok, GLM and Gemini are counted locally against a budget you
  calibrate from a percentage you can see. Use when a skill needs a second
  opinion, an out-of-family verdict, a completeness critic, an implementation
  lane, or a design review, and whenever someone asks which model should do
  something, why a lane was chosen, what a lane costs, whether a cheaper model
  could do it instead, or whether one is out of allowance.
---

# defer

Handing work to another model is three decisions, and skills that make them
inline get them subtly wrong: which model, at what effort, and how you know it
really ran. This skill holds all three in one place so that every skill routes
the same way, and so that changing the policy is one edit rather than fourteen.

Resolve an explicit model choice or the current role preference first. For
compatibility lanes, the work class determines eligibility, recorded shape
evidence narrows the candidates, and live headroom breaks comparable choices.
Scores for older models are not measurements of their successors.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It requires a runtime preference record or live compatibility-picker output, turns the three rules above the class table into a bound ledger read back off the emitted argv, and requires the lane's receipt rather than its flags. Other models skip it.

## Route

First read current authorization and active project opt-out directives using
`references/runtime-preferences.md`; quoted examples are not directives. Then
resolve the preferred role: Opus 5 for intake, triage and
planning, Gemini 3.8 for implementation after those artifacts exist, and GPT-6
for orchestration, unless the task chooses otherwise. Discover exact runtime
selectors and dispatch through the native supported tool or CLI; preserve the
requested-to-serving model receipt. This path is actionable even when the legacy
registry has no row for the preferred model.

For a calibrated compatibility lane, run the picker. It reads that registry and
its meters and prints a command:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/defer/scripts/lane_pick.py --task <class> [--shape <shape>]
```

The classes, and what each one is for:

| `--task` | For | Lanes | Effort |
|---|---|---|---|
| `implementation` | writing code | shape decides, then headroom | pinned per lane |
| `completeness` | the critic that finds what was promised and not delivered | glm · grok · gemini | high · **xhigh** · high |
| `general` | anything that is neither a referred decision nor a verdict | `gpt-5.6-terra` | **high** |
| `referral` | a decision or fork put to another model | `gpt-5.6-sol` · `claude-fable-5` | **medium** · **high** |
| `verification` | grading delivered work; same-family validation | `claude-opus-5` | **xhigh** |
| `design-review` | judging rendered UI | `claude-opus-5` · `claude-fable-5` | xhigh · high |

`--json` gives the same answer as a structured object with the argv and env
ready to spawn. `--report` prints every lane's meter without choosing, and
`--matrix` prints the measured capability table without choosing either.

The following rules describe the compatibility registry, not a restriction on
the current preferred-model path. Figures refer to the named recorded models:

- **`gpt-5.6-luna` at `max` is a recorded compatibility value lane.** On DeepSWE 1.1
  (113 tasks) it scores 67% ±4 for **$0.61 a task** — the same score as
  `grok-4.6` at `xhigh` to within both error bars, at 11% of its cost, and two
  points ahead of `gemini-3.7-flash` at under a third. That comparison does not override the
  current Gemini 3.8 implementation preference. It is 6 points behind `sol@max`, so reach
  past it when the work is genuinely hard rather than merely long.
- **The compatibility `gemini` lane (Gemini 3.7 Flash) is ranked behind glm, grok and sol**,
  and carries a 12-point delivery penalty on top of its bench score. That penalty
  is not a capability judgement: it failed 8 of 12 autonomous-builder dispatches
  and produced one fabricated completion report. `references/lanes.md` has the
  measurement and the condition for lifting it.
- **`gpt-5.6-sol` never runs at `max`.** It is the referral lane at `medium` and
  the implementation lane at `high`. Work that is not a referred decision goes
  to a terra lane or to `sol@high`.
- **Fable judges; it does not verify.** Forks, design calls and referred
  decisions, yes. Grading code or a ticket against its acceptance criteria, no —
  that is `claude-opus-5` at `xhigh`.
- **Design review stays on Opus and Fable.** No other family reviews rendered UI.

Full matrix, every command template, and the substitution rules for a lane that
is down: `references/lanes.md`.

## Say what the work is, not just what class it is

`--task implementation` says a lane will write code. `--shape` says what kind,
and it is the difference between routing on a general ranking and routing on
evidence about this piece of work:

```bash
lane_pick.py --task implementation --shape regression-sensitive
```

Eleven shapes are defined, each with the tell that identifies it and the guard
that applies when the chosen lane is a cheaper one — `--matrix` lists them.
The ones that most change the answer:

| shape | what it is | who wins |
|---|---|---|
| `brownfield-integration` | editing existing multi-file code under several acceptance criteria at once | opus, clearly. Everything cheap collapses here |
| `greenfield-module` | a new self-contained unit behind one acceptance surface | Gemini, level with opus, at a seventh of the cost |
| `regression-sensitive` | it must not break a contract that currently passes | `sol@high`, ahead of opus by 16 points |
| `algorithmic` | there is a stated complexity bound | anything. Every lane ties; take the cheapest |
| `static-page` | a self-contained page authored from nothing | the OpenAI lanes, ahead of opus. Gemini collapses |
| `deck` | slides | opus. Nothing measured level with it |

The numbers behind every cell, the gate thresholds, and what the evidence does
and does not support: `references/capability.md`.

Two properties of the gate are worth holding before you trust a route. **The
reference lane is the fail-back, never a competitor** — opus grades `REF` on
every shape by construction, and counting that as a pass would hand it every
route on the strength of being the yardstick. And **a shape only narrows a class
that the bench can speak to.** The corpus measures a model building something,
so `implementation` and `general` are gated and `verification`, `referral`,
`completeness` and `design-review` are not; passing `--shape` to those returns
the policy answer unchanged rather than a verdict the evidence cannot support.

Inside whichever band it lands in, **score leads and usage follows**: the best
measured lane wins unless another is within 5 points of it, and only then does
headroom choose between them. The output tells you which stage decided — `equal`
lists the lanes headroom picked among, `outrank` lists the ones set aside for
being further behind.

When the gate lands on a guarded lane it prints that shape's guard — the
condition under which the cheaper lane's known weakness stops mattering. Satisfy
it in the prompt. `--require-dropin` refuses the guarded band outright and falls
back to opus instead.


## Opus does not need `xhigh` for everything

The compatibility registry pins `claude-opus-5` to `xhigh` for `verification`
and `design-review`. That is a local setting, not a universal minimum. For a
current runtime route, start from supported defaults and calibrate effort on
representative work; use lower settings where quality holds. Anthropic recommends
removing redundant self-review, while task-specific acceptance gates still run.

Effort buys *thinking tokens*, not output quality per se. Measured on the codex
lanes, terra at `max` and terra at `medium` bill at the same per-Mtok rate and
differ by **4.8× on the bill**, because the expensive one spends far more tokens
before it writes anything. Do not transfer that numerical multiplier to Claude without a measurement.

| Run opus at | When |
|---|---|
| `xhigh` | Grading delivered work. Adversarial passes. Anything where a wrong pass is banked as a fact. Rendered-UI review |
| `high` | Building a feature under compound acceptance criteria. Anything that has to hold several constraints at once |
| `medium` | Extraction, arithmetic, JSON assembly, file streaming, censusing, mechanical refactors, applying a decision somebody else made |
| `low` | Read-only sweeps whose output is a list |

**The tell that effort is set too high: the agent's answer would not change if it
thought less.** A pass that streams 300 files and sums a column has no judgement
in it, and the four retrospective extraction agents behind
`~/Dev/dAIolog/docs/retro-2026-08-26/` are the worked example — file streaming,
arithmetic and JSON assembly, at a mean agent duration of 496 seconds across 386
agents. One equivalent pass ran on Sonnet in 88 seconds.

**Do not drop effort on the judgement classes to save time.** The fresh-context
verify stage rejected three of three ready-to-verify claims in that window, and a
cheaper lane there would have banked all three.

## Give the lane 900 seconds, or background it

**The most expensive failure in this system is not a lane refusing. It is the caller
giving up while the lane is still working.**

Measured 2026-08-26 across 140 lane-launching calls: **54 failed (38.6%), and 23 of
grok's 24 failures were the Bash tool's own 120-second default firing on a lane whose
median call is 150 seconds.** That is **3,240 seconds of pure wait — a third of the
entire out-of-family budget — spent on calls that were going to succeed.** Separate the
harness bound out and grok's own failure rate is **1 in 79**.

The failure is also silent in the worst way: a killed call leaves a truncated or empty
output file, which is indistinguishable from a lane that answered with nothing.

Two ways to run one, and never the default:

```bash
# 1 — an explicit bound, well past the median. `scripts/limit` where coreutils
#     `timeout` does not exist (macOS ships none; 40 calls died on that alone).
scripts/limit 900 codex exec -m gpt-5.6-luna ... -o /tmp/lane.md "<prompt>"

# 2 — better for anything on the critical path: launch it and carry on. The
#     verdict arrives as a notification rather than as a blocked terminal.
#     Bash(run_in_background: true), then reconcile at the next gate.
```

In Claude Code specifically, a foreground `Bash` call defaults to 120 000 ms. **Pass
`timeout: 900000` explicitly, or set `run_in_background: true`.** A lane call that
inherits the default will be killed at two minutes roughly half the time.

**Inspect completion status and the actual output file.** A clean exit or requested
model header can accompany empty output. Non-empty output establishes only that
bytes arrived; check that the requested artifact/verdict is complete and capture
the serving-model receipt before treating the lane as successful.

## Then verify the lane actually ran

Launch parameters have been observed not to stick, and the most expensive failure
in this system returns a plausible answer from the wrong model. Each lane's
`verify` field names its check; `references/wire-verify.md` has all four.

The one worth knowing before anything else: **GLM is Claude Code with a header.**
`X-Perch-Binding: glm` is the entire mechanism. Without it the identical command
runs Claude, succeeds, and answers — so a GLM result is only a GLM result once
Relay's ledger shows `model: glm-5.3`.

```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:8858 \
ANTHROPIC_API_KEY=local-proxy-supplies-the-real-credential \
ANTHROPIC_CUSTOM_HEADERS="X-Perch-Binding: glm" \
  claude --effort high -p "<prompt>"

tail -1 ~/Library/Application\ Support/Relay/spend/$(date +%Y-%m).jsonl   # → glm-5.3
```

The second rule, close behind: an absent or empty output file is a lane failure,
not a quiet pass. Codex prints a correct-looking header on a run that produced
nothing at all.

## How the choice is made

A route is decided in three stages, and each one answers a different question.

**Is this lane good enough?** The shape gate, from the capability matrix. Lanes
measured too far behind on this kind of work are set aside before anything else
is considered.

**Will the output be as good?** Score. Among the lanes that cleared the gate,
take the best measured on this shape and keep everything within 5 points of it.
That margin is what GREEN already means, so "close enough to opus to substitute"
and "close enough to each other to swap" are one claim at one size.

**Which of the equally good lanes can afford it?** Usage. Everything runs on a
subscription, so the scarce thing is plan headroom in the current window, not
money. Raw usage is the wrong comparison — a lane holding 60% with six days to
run is tighter than one holding 80% that resets tonight — so what gets ranked is
headroom per remaining day:

```
allowance = (1 - used_pct) / days_left
```

Largest wins. Where two lanes sit within 20% of each other the meters cannot
honestly separate them, so the tie breaks on **measured cost per task**:
`terra@medium` $0.14, `sol@medium` $0.20, `sol@high` $0.25, gemini $0.29, grok
$0.63, `terra@max` $0.67, glm $0.78, opus $2.16, fable $3.13. List price per Mtok
cannot break that tie — the five codex lanes all bill at one rate and differ by
nearly 5x on what a task costs, because effort buys tokens.

The order is deliberate. Ranking headroom before score trades real output quality
for load-spreading: it once sent greenfield work to a lane 13 points behind
because the better one was near its budget. Score-led down to the margin and
usage-led inside it makes that trade only where it costs nothing. A spent top
scorer never stalls a route — lanes at their cap drop out before the equivalence
set is built, so the next-best live lane leads.

Balancing exists at all because the depth is uneven. Opus is the primary model
here, so Claude was bought deep — nine accounts carried a live seven-day meter on
2026-08-21, the emptiest at 41% — while xAI, Z.AI, Google and OpenAI are one
account each. So the Claude classes name a model outright and do not rank, and
the fanning-out classes spread across the rest precisely because running the
nominal best every time empties a single-account lane inside a week. The five
codex lanes share one account and therefore one meter: adding an effort variant
buys a cheaper lane, never more headroom.

The scarce lanes are still worth spending on `completeness`, which excludes
Claude entirely: Claude checking Claude is not an independent check, and that is
the one thing the deeper pool cannot buy.

Meters come in two tiers and the report always says which. **Claude and Codex
report a real utilization percentage** the vendor computed, already on disk —
Relay's `usage.json` and codex's own `rate_limits` payload. **Grok, GLM and
Gemini expose no quota to any CLI**, so those are counted locally and divided by
a budget. Calibrate a budget from a percentage you can actually see rather than
from someone's estimate of the plan:

```bash
lane_pick.py --calibrate gemini=62 grok=99
```

`references/usage-sources.md` gives the source, the unit and the trust level for
each, along with what is measured, what is assumed, and what no vendor publishes.

## Using this from another skill

Follow `references/runtime-preferences.md` for explicit/current model roles.
Otherwise call `lane_pick.py`, use the returned compatibility argv, and capture
the execution receipt. Do not hard-code a new model ID or effort in sibling
skills. A direct `lane_run.sh` call still uses the compatibility registry; it
does not implement the current-role resolution automatically.

For a blind judgment, give the lane the bounded evidence **inline**
rather than unrestricted access to the source skill: both `claude -p` and the grok CLI load the
repo's instruction files, so a lane told to "read the repo" is neither blind nor
cheap. An implementation runner instead receives the real task artifacts and
its owned source paths. Record which lane answered in either case.

## Scope

This skill decides routing and proves delivery. It does not write the prompt, and
it does not judge the answer that comes back — the calling skill owns both.
Deliver the routing decision and the verified invocation; leave the work itself
to the lane.
