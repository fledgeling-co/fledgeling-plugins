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

Six task classes across seven lanes and five model families:

| `--task` | Lanes | Effort |
|---|---|---|
| `implementation` | gemini · grok · glm · opus | high · **xhigh** · high · xhigh |
| `completeness` | grok · glm · gemini | **xhigh** · high · high |
| `general` | `gpt-5.6-terra` | **high** |
| `referral` | `gpt-5.6-sol` · `claude-fable-5` | **medium** · **high** |
| `verification` | `claude-opus-5` | **xhigh** |
| `design-review` | `claude-opus-5` · `claude-fable-5` | xhigh · high |

Three rules sit above the table: **`gpt-5.6-sol` never runs at `max`** (it is the
referral lane at `medium`; other work goes to `terra` at `high`), **Fable judges
but does not verify** (grading code or a ticket is Opus at `xhigh`), and **design
review stays on Opus and Fable**.

## What makes it different

**It measures instead of guessing.** Everything here runs on a subscription, so
the scarce thing is plan headroom in the current window. Raw usage is the wrong
comparison — a lane holding 60% with six days to run is tighter than one holding
80% that resets tonight — so what gets ranked is headroom per remaining day,
`(1 - used_pct) / days_left`. Where two lanes sit within 20% of each other the
meters cannot honestly separate them, so the tie breaks on published price.

**It says which numbers are real.** Claude and Codex both report a utilization
percentage the vendor computed, sitting on disk already — Relay's `usage.json`
and codex's own `rate_limits` payload. Grok, GLM and Gemini expose no quota to
any CLI, so those are counted locally and divided by a budget, and the report
labels them Tier 2 rather than letting an estimate pass as a reading. A lane
whose usage cannot be measured never wins on a zero it did not earn.

**You calibrate a budget from a number you can see**, not from someone's estimate
of your plan:

```bash
lane_pick.py --calibrate gemini=62 grok=99
```

It reads the consumption it already counts, divides by your observed percentage,
and writes the budget back.

**It proves the lane ran.** Launch parameters have been observed not to stick,
and the most expensive failure in a multi-model system is a plausible answer from
the wrong model. Every lane carries a wire-verify method. The sharpest case is
GLM: it is Claude Code pointed at Perch's proxy, and `X-Perch-Binding: glm` is
the entire mechanism — drop the header and the identical command runs Claude,
succeeds, and answers. A GLM result is only a GLM result once Relay's ledger says
`model: glm-5.3`.

Codex has the opposite trap: on a run that produced nothing at all, the header
still prints `model: gpt-5.6-terra` and `reasoning effort: high` exactly as
requested. An empty `-o` file is the failure signal, not the flags.

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
| `skills/defer/scripts/lane_probe.sh` | cheap liveness probe per lane |
| `skills/defer/scripts/selftest.sh` | 13 policy invariants, runs no model, costs nothing |

`selftest.sh` is the guard against the policy drifting away from the prose: it
checks that sol is never `max`, that grok is `xhigh`, that Fable is absent from
verification, that design review is Anthropic-only, that completeness is not,
that no `grok-4.5` survives anywhere, that the GLM header is present, that the
price order is gemini < glm < grok, and that every model named in the registry
also appears in `lanes.md`.
