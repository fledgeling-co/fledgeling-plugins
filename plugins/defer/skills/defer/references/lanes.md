# Lanes — who does what, on which CLI, with which arguments

Compatibility registry. Current user model preferences resolve first through
`runtime-preferences.md`; this file describes the calibrated fallback lanes.
For these lanes, `scripts/lane_pick.py` reads the same policy from
`scripts/lane_registry.py`. Change a lane here **and** in the registry, or the
selftest fails — which is the point, because a policy in two places drifts and
the drift is silent.

This file is the *policy* half: which lanes may do which class of work. The
*capability* half — which of those lanes is good enough for a particular piece,
measured rather than asserted — is `capability.md`.

## The matrix

| Task class | Lane | Model | Effort | Chosen by |
|---|---|---|---|---|
| **Implementation** — writing code | gemini · codex-astra-low · codex-sol-high · glm · grok · opus | `gemini-3.8-flash-high` · `gpt-6-astra` · `gpt-5.6-sol` · `glm-5.3` · `grok-4.6` · `claude-opus-5` | baked · **low** · high · high · high · xhigh | the plan condition, then shape, then headroom |
| **Hard** — what the workhorse tier could not hold | codex-astra-medium · codex-astra-high · opus | `gpt-6-astra` · `gpt-6-astra` · `claude-opus-5` | **medium** · **high** · xhigh | asked for, never fallen into |
| **Orchestration** | codex-astra-low · grok · glm | `gpt-6-astra` · `grok-4.6` · `glm-5.3` | **low** · high · high | measured headroom |
| **Completeness critic** | codex-astra-low · glm · grok · gemini | `gpt-6-astra` · `glm-5.3` · `grok-4.6` · `gemini-3.8-flash-high` | low · high · high · baked | measured headroom |
| **General** — neither referred nor a verdict | codex-astra-low · grok · glm · gemini | `gpt-6-astra` · `grok-4.6` · `glm-5.3` · `gemini-3.8-flash-high` | **low** · high · high · baked | shape, then headroom |
| **Referral** — a decision put to another model | codex-astra-low · codex-sol-high · fable · grok | `gpt-6-astra` · `gpt-5.6-sol` · `claude-fable-5` · `grok-4.6` | **low** · **high** · **medium** · **high** | headroom, across three families |
| **Verification** — task and same-family | opus | `claude-opus-5` | **xhigh** | fixed |
| **Design** — authoring | opus-design · fable | `claude-opus-5` · `claude-fable-5` | **medium** · **medium** | fixed; the plan condition applies |
| **Design review** — judging | opus · fable-high | `claude-opus-5` · `claude-fable-5` | xhigh · high | fixed |

### The tiers, and what the directive of 2026-09-09 actually says

Three statements, and everything above is their consequence.

**One workhorse tier, four lanes, no ranking inside it.** `gpt-6-astra` at **low**
is level with `gpt-5.6-sol` at high, `claude-fable-5` at medium and `grok-4.6` at
high. That is one claim with four members, so the classes that want a competent
reading — referral, general, orchestration, completeness — spread across them
rather than ordering them. They sit in three families, which is why independence
here is a lane choice rather than a compromise.

**Astra at medium and high is frontier, and reserved.** It is for the most
difficult problems, and the registry enforces that mechanically rather than by
asking nicely: both lanes carry `frontier: True`, `allowed_lanes()` filters them
out of every class, and `--hard` (or `--task hard`) is the only way to them. A
lane a router can reach is a lane a router will reach when it runs out of cheaper
options, which is exactly the drift a reservation is meant to stop.

**Design work stays on Opus and Fable, and authors at medium.** Medium is the
effort the directive gives design *given a rough plan already exists* — so the
`design` class carries that as a stated `condition`, and `--has-plan` is the
caller declaring it. Judging rendered UI is a different job: `design-review` keeps
the higher efforts, because a cheapened judgement is banked as a fact. `--hard`
is refused on both, and on verification, by `NO_ESCALATION`: a harder design
question is still a design question, and the answer to it is not another family.

**`gemini-3.8-flash-high` is the fast implementation lane, on a condition.** It is
the tokens-per-second pick when a spec or plan already exists, and that condition
is its `route_guard` rather than a footnote: with `--has-plan` it moves to the
front of the implementation class, without it to the back. The condition is not
decoration — see the delivery record below.

### What is measured here and what is not

Being honest about this is the difference between a routing policy and a
ranking someone made up, so the registry marks three things separately.

- **`gpt-6-astra` has no bench row**, here or on DeepSWE, at any effort. The
  `codex-astra-low` lane borrows `codex/gpt-5.6-sol@high`'s row under
  `evidence: "peer"`, because the directive names those two level — that is what
  "level with" means made checkable. A peer row clamps exactly as a proxy row
  does: never drop-in, never a hard block. And it is a **capability** claim only.
  `task_cost()` refuses to read a peer's cost, so one lane's bill never decides
  the other's route.
- **Neither astra nor Gemini 3.8 has a published price read into this file.**
  Both stand in at a predecessor's blended rate and are marked
  `price_evidence: "placeholder"`; `PLACEHOLDER_PRICES` names them. When any lane
  in a band is one of these the cost tie-break **abstains** and preference order
  decides, and the route says which stage was skipped. Ranking a measured $0.25
  against a stand-in $14.00 is not a cost comparison.
- **The Gemini delivery penalty has gone inert, and did not transfer.** It was
  measured on Gemini 3.7 Flash; the lane runs 3.8 as of 2026-09-09. The entry now
  carries `applies_to_model`, and `delivery_penalty_for()` checks it before
  subtracting anything — so the 12 points stop applying the moment the lane
  moves, and snap back if it moves back. The finding survives as the lane's
  `route_guard`, which is the honest shape for it: a condition on the brief
  rather than a subtraction from a score nobody measured.

### Probed 2026-09-09

`gpt-6-astra` answered through `codex exec` at **low, medium, high and max**, each
one echoing the requested `reasoning effort:` in its header and writing a real
answer to `-o`. The negative control is what makes those four evidence rather
than an echo of the flags: the same command with `-m gpt-6-bogus-xyz` failed at
the API with `400 invalid_request_error — The 'gpt-6-bogus-xyz' model is not
supported when using Codex with a ChatGPT account`, and wrote **no output file**.

Two CLI facts from the same run:

- **`--skip-git-repo-check` is required outside a trusted directory.** Without it
  `codex exec` exits 1 with *"Not inside a trusted directory and
  --skip-git-repo-check was not specified"* before reaching a model. Every codex
  lane's argv carries it.
- **codex 0.153.4 now warns on an unknown model**, before the API refuses it:
  `warning: Model metadata for 'X' not found. Defaulting to fallback metadata`.
  That is a useful pre-flight tell, and it is still not the check — an empty `-o`
  file remains the failure signal, because a *known* model prints a clean header
  on a run that produced nothing.

`max` is accepted and answering, and is refused anyway: `FORBIDDEN` rejects it on
all three astra lanes. The directive defines three tiers, and a fourth nobody
placed would be a routing decision made by an argument parser.

**`glm` was probed the same day and is DOWN**, on settings rather than on
anything about the model: the Perch proxy answered `409 {"code":
"no-eligible-account", ... "reason":"routing_forbidden"}` — *1 of 1 account
excluded from routing by settings*. It keeps its policy place; allow the account
in Perch, or add another, and re-probe. `lane_probe.sh` is what says whether a
lane is reachable today, and the lane carries `probe_state` so a route prints it.

### Retired, and why the record stays

Four GPT-5.6 lanes left together on 2026-09-09 — `codex-terra` at high, max and
medium, and `codex-luna-max` — plus `codex-sol` at medium. Astra is the
OpenAI-family spine now and no class routed to them. Nothing was found wanting:
`codex-sol-high` survives only because the directive names sol@high as a peer of
astra@low, which is why one GPT-5.6 lane is still routed and four are not.

They are recorded in `DECLINED` rather than deleted, because their measurements
are still the best evidence anyone has about that generation. Two rows are worth
knowing where they are. `gpt-5.6-terra@max` was the only non-Claude lane that
held opus on compound multi-group backend tasks — read it first if astra ever
measures short on brownfield integration. `gpt-5.6-luna@max` scored 67% ±4 on
DeepSWE 1.1 for **$0.61 a task**, the best score-per-dollar on the board; read it
first if astra's own cost is ever measured and comes back high.

## Two benches, and which one answers which question

Routing reads two evidence sources and they are kept apart on purpose.

**`diolog-swe-bench`** (`~/Dev/diolog-swe-bench`) produces
`scripts/capability_matrix.json`: eleven work *shapes*, graded head-to-head against
a reference lane. It is the only source that can say *this lane is good at
brownfield integration and bad at static pages*, and it is what the shape gate
reads. Its corpus is small and its absolute costs are not comparable to anything
outside it.

**DeepSWE 1.1** (<https://deepswe.datacurve.ai/>, 113 tasks) is the most relevant
external board and lives in `EXTERNAL_BENCH["deepswe-1.1"]`. It cannot speak to
shape — it is one Pass@1 per model — but it carries a *measured cost per task*
across eighteen models, which is the number the local bench is worst at.

| Model | Pass@1 | $/task | Pass per $ |
|---|---:|---:|---:|
| `claude-opus-5` @max | 74% ±4 | 11.84 | 6 |
| `gpt-5.6-sol` @max | 73% ±3 | 6.46 | 11 |
| `claude-fable-5` @max | 70% ±4 | 21.63 | 3 |
| `glm-5.3` @max | 69% ±3 | 3.99 | 17 |
| **`gpt-5.6-luna` @max** | **67% ±4** | **0.61** | **110** |
| `grok-4.6` @xhigh | 67% ±2 | 5.50 | 12 |
| `gemini-3.7-flash` @high | 65% ±2 | 2.18 | 30 |
| `deepseek-v4-flash` @max | 53% ±4 | 0.46 | 115 |

**The transfer rule: only the relative ordering crosses between them.** `sol@max`
costs $6.46 a task on DeepSWE and $0.47 on the local corpus — an order of
magnitude apart, because the corpora are not the same size. A figure quoted from
one bench and compared against the other is the mistake this section exists to
prevent.

Where they disagree, both are recorded and the disagreement is the finding.
`gpt-5.6-luna` is the worked example: the local bench declined it as *dominated
and dearer*, DeepSWE measures it at a tenth of `sol@max`'s cost for six points
less, and `DECLINED["gpt-5.6-luna"]` now carries both with the cost half marked
superseded. **`gpt-5.6-terra` has no row on DeepSWE at all**, so the local
terra-versus-luna comparison cannot be checked there and is not treated as
settled.

## Two facts a bench cannot see

The shape gate grades a model *building* something. Two things it structurally
cannot measure are recorded separately, so neither is mistaken for a capability
score and either can be lifted without touching a number somebody else produced.

**`DELIVERY_PENALTY`** — whether the artefact arrived at all. Measured on Gemini
3.7 Flash, 2026-08-26: running as an autonomous builder it failed 8 of 12
dispatches and one completion report was fabricated — 4,406 bytes claiming four
schedulers created, against a ground truth of nothing created. A bench cannot
catch that, because a fabricated report grades as a delivered artefact.

Since 2026-09-09 the entry names `applies_to_model`, and `delivery_penalty_for()`
checks it before subtracting. The lane now runs Gemini 3.8, so the 12 points are
**inert** — not deleted, and not transferred either. That distinction is the
whole point of the field: a penalty measured on one model and quietly charged to
its successor is a delivery record about a model nobody measured, and a penalty
silently dropped is a finding nobody has to argue with. Point the lane back at
3.7 and the subtraction returns on its own. Recalibrate it properly when a
dispatch set of 12 or more completes with no fabricated report and a failure rate
under 20%, measured the same way.

The finding itself did not go inert. It survives as the `gemini` lane's
`route_guard` — route implementation there only when a spec or plan already
exists, hand the lane the plan path and the acceptance checks, and read the
artefact back rather than the report. That is the same failure mode expressed as
a condition on the brief rather than as a number subtracted from a score, which
is the honest shape for it once the measurement's subject has changed.

**`PREFERENCE_ORDER`** — the tie-break, `gemini` → `codex-astra-low` → `grok` →
`glm` → `codex-sol-high` → `fable`. It runs *last*, only between lanes already
agreed equivalent, so policy never overrules a lane that is genuinely better at
the shape in front of it. Since the 2026-09-09 directive makes the workhorse tier
a set of peers rather than a ranking, this order is a tie-break between equals —
and it does more work than it used to, because it is also what decides when the
cost stage abstains for want of a sourced price.

## Running a lane

`lane_pick.py --task <class> [--shape <shape>] [--hard] [--has-plan]` prints the
argv and the environment for the lane it chose. **Do not reconstruct a command
from this file.** `lane_run.sh` and `lane_probe.sh` no longer carry one either —
both build every command from the registry through `lane_pick.argv_for()`, which
is what the case statement they replaced got wrong: it held its own copy of five
models and drifted the first time a lane moved, silently. The templates below are
what the registry currently emits, printed here to be read rather than copied.

```bash
# gemini — effort is baked into the model id; there is no --effort flag.
# --output-format json is the only place a token count for this lane exists.
agy --model gemini-3.8-flash-high --output-format json -p "<prompt>" > out.md 2>err.log

# grok — efforts are xhigh|high|medium|low; harness fallback is cursor-agent
grok -m grok-4.6 --effort high -p "<prompt>" > out.md 2>err.log
cursor-agent -p --force --model grok-4.6 "<prompt>"

# glm — Claude Code pointed at the Perch proxy; the header is what selects Z.AI
ANTHROPIC_BASE_URL=http://127.0.0.1:8858 \
ANTHROPIC_API_KEY=local-proxy-supplies-the-real-credential \
ANTHROPIC_CUSTOM_HEADERS="X-Perch-Binding: glm" \
  claude --effort high -p "<prompt>"

# codex — -o is not optional; an absent or empty file is the failure signal.
# --skip-git-repo-check is not optional either outside a trusted directory.
codex exec -m gpt-6-astra -c model_reasoning_effort="low" \
  -s read-only --skip-git-repo-check -o /tmp/lane.md "<prompt>" < /dev/null
codex exec -m gpt-6-astra -c model_reasoning_effort="medium" \
  -s read-only --skip-git-repo-check -o /tmp/lane.md "<prompt>" < /dev/null   # frontier
codex exec -m gpt-6-astra -c model_reasoning_effort="high" \
  -s read-only --skip-git-repo-check -o /tmp/lane.md "<prompt>" < /dev/null   # frontier
codex exec -m gpt-5.6-sol -c model_reasoning_effort="high" \
  -s read-only --skip-git-repo-check -o /tmp/lane.md "<prompt>" < /dev/null

# claude
claude --model claude-opus-5  --effort xhigh  -p "<prompt>"   # verification, design review
claude --model claude-opus-5  --effort medium -p "<prompt>"   # design authoring
claude --model claude-fable-5 --effort high   -p "<prompt>"   # design review
claude --model claude-fable-5 --effort medium -p "<prompt>"   # referral, design authoring
```

## GLM is Claude Code wearing a different header

There is no `glm` binary. GLM-5.3 reaches you through Perch's local proxy on
`127.0.0.1:8858`, and **`X-Perch-Binding: glm` is the whole mechanism**. Drop the
header and the identical command runs Claude instead, succeeds, and returns
something plausible — the most expensive kind of silent failure this skill exists
to prevent. `~/Dev/glm/.claude/settings.local.json` carries the same three
variables for anyone working inside that directory; the environment form above is
what to use from anywhere else, because the settings file is directory-scoped.

Two consequences worth holding:

- **Perch must be running.** If the proxy is down the command fails to connect
  rather than falling back, which is the safe direction.
- **Relay attributes GLM by binding, not by working directory.** A GLM call made
  from `/tmp` still lands in the ledger under `/Users/lukerhodes/Dev/glm`. That is
  correct behaviour, not a mis-tag.

Verified 2026-08-21 from `/tmp`: the command above returned `LANE OK` and Relay's
spend ledger recorded `model: glm-5.3, bindingId: glm` for that request.

## The timeout is part of the invocation

Use a task-appropriate bound and an observable background/session handle for
long calls; **900 seconds** was the bound used for these recorded lanes. The
harness default is 120 000 ms and the median lane call is **150 seconds**, so a lane run
at the default is killed about half the time — 23 of grok's 24 failures in the measured
window were exactly that, 3,240 seconds of wait on calls that would have succeeded. A
killed call leaves a truncated output file, which reads identically to a lane that
answered with nothing.

## Which lanes are live, and what down looks like

A lane is available when a probe says so, not when you remember it working.
`scripts/lane_probe.sh` runs the cheap version of each, building every command
from the registry. It skips the frontier astra tiers unless you pass
`--frontier`, so the routine check does not spend them.

**Measured 2026-09-09:** `codex-astra-low` is **up** and answering. `glm` is
**down** with `409 no-eligible-account / routing_forbidden` — a Perch routing
setting, not a model or capability fact, and it clears by allowing that account
in Perch or adding another. Everything else was not re-probed that day; read this
paragraph as a snapshot rather than as current availability, which is what the
script is for.

Two failure shapes are worth recognising because they look like success. Codex
prints `model:` and `reasoning effort:` exactly as requested and then writes the
`-o` file **empty** — the header echoes what was configured, not what the API
served. And a GLM call without the binding header runs Claude, succeeds, and
returns something entirely plausible.

## Substitution

When a lane is down, `lane_pick.py` picks the next one that still has headroom
inside the same task class. Where a shape was given, it descends the capability
bands in order — drop-in, then guarded, then the reference lane — and it
descends on two conditions only: the band is empty, or every lane in it is at its
cap. Three invariants survive every substitution:

- **REVIEWER ≥ WRITER.** Lowering a reviewer's effort keeps the invariant;
  lowering its model breaks it.
- **VERIFIER ∉ WRITER's family.** The `family` field in the registry is what
  makes this checkable: `xai`, `google`, `zai`, `openai`, `anthropic`. When every
  out-of-family lane is down, verification still runs in-family and is **recorded
  as degraded**, never quietly promoted.
- **A refused lane stays refused.** A spent band never promotes a lane the
  capability matrix graded RED for that shape. The descent ends at opus, never
  below it.

Work never routes down to a cheaper sibling to get around a limit, and it is
never dropped. Claude is the fail-back.
