# defer

Handing work to another model is three decisions, and skills that make them
inline get them subtly wrong: **which model**, **at what effort**, and **how you
know it really ran**. `defer` holds all three in one place, so every skill routes
the same way and changing the policy is one edit rather than fourteen.

The routing rule is not "use the best model". It is: the work class decides the
family, and measured plan headroom decides which lane inside it.

## Install

```
/plugin install defer@fledgeling-plugins
```

## Route

```bash
python3 skills/defer/scripts/lane_pick.py --task completeness
```

```
task     completeness — Completeness critic
lane     glm (glm-5.3, zai family, effort high)
why      most headroom per remaining day (0.1250/day vs gemini 0.0289, grok 0.0017)
env      ANTHROPIC_BASE_URL='http://127.0.0.1:8858'  ANTHROPIC_CUSTOM_HEADERS='X-Perch-Binding: glm'
run      claude --effort high -p {PROMPT}
verify   relay-ledger (see references/wire-verify.md)
```

`--json` returns the same answer with argv and env ready to spawn. `--report`
prints every lane's meter without choosing. `lane_run.sh <task> "<prompt>"` does
the whole thing: picks, runs, checks the receipt, falls through to the next lane
in the class if the first produces nothing, and appends what it cost to
`~/.claude/defer-usage.jsonl`.

## The matrix

Six task classes, seven lanes, five model families. A cell holds the effort that
lane runs at for that class — pinned, because a lane that inherits its config
default is not the lane anyone chose.

| Task class | gemini | grok | glm | terra | sol | opus | fable |
|---|---|---|---|---|---|---|---|
| **implementation** — writing code | high | xhigh | high | — | — | xhigh | — |
| **completeness** — what was promised and not delivered | high | xhigh | high | — | — | — | — |
| **general** — neither referred nor a verdict | — | — | — | high | — | — | — |
| **referral** — a fork put to another model | — | — | — | — | medium | — | high |
| **verification** — grading delivered work; same-family validation | — | — | — | — | — | xhigh | — |
| **design-review** — judging rendered UI | — | — | — | — | — | xhigh | high |

Three rules sit above the table. They are the ones habit gets wrong, so they are
stated rather than left to be read off the grid.

1. **`gpt-5.6-sol` never runs at `max`.** It is the referral lane at `medium`.
   Work that is not a referred decision goes to `gpt-5.6-terra` at `high` — the
   same context window at a fraction of the price.
2. **Fable judges; it does not verify.** Forks, design calls and referred
   decisions, yes. Grading code or a ticket against its acceptance criteria, no —
   that is `claude-opus-5` at `xhigh`.
3. **Design review stays on Claude.** Opus and Fable only. No other family
   reviews rendered UI here, so the design-review row is the one place the
   out-of-family default is deliberately not applied.

## Why the policy leans the way it does

Opus is the primary model, so Claude is the subscription that got bought deep and
everything else is bought singly. Measured on 2026-08-21, Relay's pool held
**nine Claude accounts carrying a live seven-day meter** — the emptiest at 41%,
two at 100% — against exactly one account each for xAI, Z.AI, Google (the
Antigravity sign-in that `agy` and Relay share) and OpenAI. Grok sat at 98.8%
that day and Codex at 100%, with nothing behind either of them.

That asymmetry is the shape of the table above, and it cuts in two directions.

**Claude lanes are not balanced against anything, because they do not need to
be.** Verification and design review name a Claude model outright rather than
ranking a set, since the depth is there and correctness is what those classes buy.
Fable is metered at half the weekly pool of the same accounts, so the referral
class can afford a Claude judge alongside the OpenAI one.

**Everything else is rationed, which is why balancing exists at all.** The two
classes that fan out — `implementation` and `completeness` — balance across
grok, GLM and Gemini precisely because each of those is one subscription with no
second account to fall back on, and running the nominal best every time empties
it inside a week. Ranking headroom per remaining day is what stops a single lane
absorbing a class.

The deeper reason for spending the scarce lanes at all is the one thing the extra
Claude capacity cannot buy: **Claude checking Claude is not an independent
check.** A completeness critic and an out-of-family second opinion are worth a
scarce subscription in a way that another Opus call is not, which is why
`completeness` excludes Claude entirely even though Claude has the most room.

## The lanes

What `lane_pick.py` prints and `lane_run.sh` runs. Each lane carries the check
that proves it ran as routed, because the expensive failure in a multi-model
system is a plausible answer from the wrong model.

| Lane | Model | Family | Blended $/Mtok | Verify |
|---|---|---|---|---|
| `gemini` | gemini-3.7-flash-high | google | 4.50 | output non-empty |
| `glm` | glm-5.3 | zai | 5.80 | Relay ledger |
| `grok` | grok-4.6 | xai | 8.00 | grok session store |
| `terra` | gpt-5.6-terra | openai | 14.00 | codex header + `-o` file |
| `opus` | claude-opus-5 | anthropic | 30.00 | Relay ledger |
| `sol` | gpt-5.6-sol | openai | 35.00 | codex header + `-o` file |
| `fable` | claude-fable-5 | anthropic | 60.00 | Relay ledger |

```bash
# gemini — --output-format json is the only place a token count for this lane
# exists anywhere; agy records no model id, no tokens and no cost on disk.
agy --model gemini-3.7-flash-high --output-format json -p "<prompt>"

# grok — exhaustion arrives as a 402 in the transport, not on stdout.
grok -m grok-4.6 --effort xhigh -p "<prompt>"
cursor-agent -p --force --model grok-4.6 "<prompt>"     # harness fallback

# glm — the header is the entire mechanism. Without it this same command runs
# Claude, succeeds, and returns something plausible.
ANTHROPIC_BASE_URL=http://127.0.0.1:8858 \
ANTHROPIC_API_KEY=local-proxy-supplies-the-real-credential \
ANTHROPIC_CUSTOM_HEADERS="X-Perch-Binding: glm" \
  claude --effort high -p "<prompt>"

# terra / sol — on a run that produced nothing at all, the header still prints
# the requested model and effort. The empty -o file is the failure signal.
codex exec -m gpt-5.6-terra -c model_reasoning_effort="high" \
  -s read-only -o /tmp/lane.md "<prompt>" < /dev/null

# opus / fable — strip a leading marker glyph before matching a verdict; a
# headless call inherits the session's start hooks.
claude --model claude-opus-5  --effort xhigh -p "<prompt>"
claude --model claude-fable-5 --effort high  -p "<prompt>"
```

## How the choice is made

Everything runs on a subscription, so the scarce thing is plan headroom in the
current window, not money. Raw usage is the wrong comparison — a lane holding 60%
with six days to run is tighter than one holding 80% that resets tonight — so
what gets ranked is headroom per remaining day, `(1 - used_pct) / days_left`.
Largest wins. Where two lanes sit within 20% of each other the meters cannot
honestly separate them, so the tie breaks on the price column above.

Meters come in two tiers and the report always says which. **Claude and Codex
report a utilization percentage the vendor computed**, already on disk in Relay's
`usage.json` and codex's own `rate_limits` payload. **Grok, GLM and Gemini expose
no quota to any CLI**, so those are counted locally and divided by a budget,
which makes them an estimate wearing a number. Calibrate one from a percentage
you can actually see rather than from someone's estimate of the plan:

```bash
lane_pick.py --calibrate gemini=62 grok=99
```

It reads the consumption it already counts, divides by your observed percentage,
and writes the budget back. A lane whose usage cannot be measured never wins on a
zero it did not earn.

## What it refuses to do

- **Guess a quota endpoint.** `lane_budgets.json` has an `api` hook and it is
  deliberately unwired, because pointing it at a plausible URL would turn "we
  cannot measure this" into a confident wrong number.
- **Report a Gemini figure in dollars.** `agy` records no tokens and no cost
  anywhere on disk, so that lane is counted in model calls and says so.
- **Treat a lane's silence as agreement.** An absent or empty output file is a
  lane failure, never a quiet pass.
- **Write the prompt, or judge the answer.** The calling skill owns both.

## Files

| Path | What it is |
|---|---|
| `skills/defer/SKILL.md` | the routing decision and the three standing rules |
| `skills/defer/references/lanes.md` | the full matrix, every command template, substitution rules |
| `skills/defer/references/usage-sources.md` | per lane: the source, the unit, the trust level, the citation |
| `skills/defer/references/wire-verify.md` | how to prove each lane ran as routed |
| `skills/defer/scripts/lane_registry.py` | the machine-readable policy — models, efforts, argv, prices |
| `skills/defer/scripts/lane_pick.py` | the meters, the ranking, `--report` and `--calibrate` |
| `skills/defer/scripts/lane_run.sh` | pick, run, verify, record — what a skill should call |
| `skills/defer/scripts/lane_probe.sh` | cheap liveness probe per lane |
| `skills/defer/scripts/selftest.sh` | 13 policy invariants, runs no model, costs nothing |

`selftest.sh` is the guard against the policy drifting away from the prose: it
checks that sol is never `max`, that grok is `xhigh`, that Fable is absent from
verification, that design review is Anthropic-only, that completeness is not,
that no `grok-4.5` survives anywhere, that the GLM header is present, that the
price order is gemini < glm < grok, and that every model named in the registry
also appears in `lanes.md`.
