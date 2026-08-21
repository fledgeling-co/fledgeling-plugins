---
name: defer
description: >-
  Decide which model a piece of work goes to, and produce the exact command that
  sends it there. One routing policy for every skill that hands work outside the
  session: six task classes mapped to seven lanes across five model families,
  each pinned to a model and an effort, with the CLI arguments, the environment
  GLM needs, and the check that proves the lane ran as routed. Where several
  lanes are eligible it picks the one with the most plan headroom per remaining
  day, measured — Claude and Codex report a real utilization percentage that is
  already on disk, and Grok, GLM and Gemini are counted locally against a budget
  you calibrate from a percentage you can see. Use when a skill needs a second
  opinion, an out-of-family verdict, a completeness critic, an implementation
  lane, or a design review, and whenever someone asks which model should do
  something, why a lane was chosen, what a lane costs, or whether one is out of
  allowance.
---

# defer

Handing work to another model is three decisions, and skills that make them
inline get them subtly wrong: which model, at what effort, and how you know it
really ran. This skill holds all three in one place so that every skill routes
the same way, and so that changing the policy is one edit rather than fourteen.

The routing rule is not "use the best model". It is: **the work class decides the
family, and measured headroom decides which lane inside it.**

## Route

Run this. It reads the policy and the meters and prints a command:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/defer/scripts/lane_pick.py --task <class>
```

The classes, and what each one is for:

| `--task` | For | Lanes | Effort |
|---|---|---|---|
| `implementation` | writing code | gemini · grok · glm · opus | high · **xhigh** · high · xhigh |
| `completeness` | the critic that finds what was promised and not delivered | grok · glm · gemini | **xhigh** · high · high |
| `general` | anything that is neither a referred decision nor a verdict | `gpt-5.6-terra` | **high** |
| `referral` | a decision or fork put to another model | `gpt-5.6-sol` · `claude-fable-5` | **medium** · **high** |
| `verification` | grading delivered work; same-family validation | `claude-opus-5` | **xhigh** |
| `design-review` | judging rendered UI | `claude-opus-5` · `claude-fable-5` | xhigh · high |

`--json` gives the same answer as a structured object with the argv and env
ready to spawn. `--report` prints every lane's meter without choosing.

Three rules hold above the table, and they are the ones most likely to be
violated by habit:

- **`gpt-5.6-sol` never runs at `max`.** It is the referral lane at `medium`.
  Work that is not a referred decision goes to `gpt-5.6-terra` at `high`.
- **Fable judges; it does not verify.** Forks, design calls and referred
  decisions, yes. Grading code or a ticket against its acceptance criteria, no —
  that is `claude-opus-5` at `xhigh`.
- **Design review stays on Opus and Fable.** No other family reviews rendered UI.

Full matrix, every command template, and the substitution rules for a lane that
is down: `references/lanes.md`.

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

Everything runs on a subscription, so the scarce thing is plan headroom in the
current window, not money. Raw usage is the wrong comparison — a lane holding 60%
with six days to run is tighter than one holding 80% that resets tonight — so
what gets ranked is headroom per remaining day:

```
allowance = (1 - used_pct) / days_left
```

Largest wins. Where two lanes sit within 20% of each other the meters cannot
honestly separate them, so the tie breaks on published price: Gemini $4.50, GLM
$5.80, Grok $8.00 per blended Mtok.

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

Call `lane_pick.py`, take the argv it prints, run it, verify it. Do not hard-code
a model id or an effort in a skill — a pinned lane in fourteen files is a policy
nobody can change. When a skill needs a lane the classes above do not cover, add
the class here rather than routing around this file.

Two things to pass along when you spawn a lane. Give it the evidence **inline**
rather than pointing it at the repo: both `claude -p` and the grok CLI load the
repo's instruction files, so a lane told to "read the repo" is neither blind nor
cheap. And record which lane answered, so a report can say who verified what.

## Scope

This skill decides routing and proves delivery. It does not write the prompt, and
it does not judge the answer that comes back — the calling skill owns both.
Deliver the routing decision and the verified invocation; leave the work itself
to the lane.
