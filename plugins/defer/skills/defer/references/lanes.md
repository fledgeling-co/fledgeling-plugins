# Lanes — who does what, on which CLI, with which arguments

Canonical. Every skill that hands work to another model routes through this file
and through `scripts/lane_pick.py`, which reads the same policy from
`scripts/lane_registry.py`. Change a lane here **and** in the registry, or the
selftest fails — which is the point, because a policy in two places drifts and
the drift is silent.

## The matrix

| Task class | Lane | Model | Effort | Chosen by |
|---|---|---|---|---|
| **Implementation** — writing code | gemini · grok · glm · opus | `gemini-3.7-flash-high` · `grok-4.6` · `glm-5.3` · `claude-opus-5` | high · **xhigh** · high · xhigh | measured headroom |
| **Completeness critic** | grok · glm · gemini | as above | **xhigh** · high · high | measured headroom |
| **General** — anything neither referred nor a verdict | codex-terra | `gpt-5.6-terra` | **high** | fixed |
| **Referral** — a decision put to another model | codex-sol · fable | `gpt-5.6-sol` · `claude-fable-5` | **medium** · **high** | fixed |
| **Verification** — task and same-family | opus | `claude-opus-5` | **xhigh** | fixed |
| **Design review** | opus · fable | `claude-opus-5` · `claude-fable-5` | xhigh · high | fixed |

Three rules sit above the table and hold everywhere:

- **`gpt-5.6-sol` never runs at `max`.** It is the referral lane at `medium`.
  Anything that is not a referred decision goes to `gpt-5.6-terra` at `high`
  instead, which is the same context window at a fraction of the price.
- **Fable judges; it does not verify.** A referred decision, a fork, a design
  call — yes. Grading code against a ticket, or a delivered feature against its
  acceptance criteria — no: that is `claude-opus-5` at `xhigh`.
- **Design review stays inside Anthropic's family.** Opus and Fable only. No
  other family reviews rendered UI here.

## Running a lane

`lane_pick.py --task <class>` prints the argv and the environment for the lane it
chose. The templates it prints are these:

```bash
# gemini — effort is baked into the model id; there is no --effort flag
agy --model gemini-3.7-flash-high -p "<prompt>" > out.md 2>err.log

# grok — efforts are xhigh|high|medium|low; harness fallback is cursor-agent
grok -m grok-4.6 --effort xhigh -p "<prompt>" > out.md 2>err.log
cursor-agent -p --force --model grok-4.6 "<prompt>"

# glm — Claude Code pointed at the Perch proxy; the header is what selects Z.AI
ANTHROPIC_BASE_URL=http://127.0.0.1:8858 \
ANTHROPIC_API_KEY=local-proxy-supplies-the-real-credential \
ANTHROPIC_CUSTOM_HEADERS="X-Perch-Binding: glm" \
  claude --effort high -p "<prompt>"

# codex — -o is not optional; an absent or empty file is the failure signal
codex exec -m gpt-5.6-terra -c model_reasoning_effort="high" \
  -s read-only -o /tmp/lane.md "<prompt>" < /dev/null
codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" \
  -s read-only -o /tmp/lane.md "<prompt>" < /dev/null

# claude
claude --model claude-opus-5  --effort xhigh -p "<prompt>"
claude --model claude-fable-5 --effort high  -p "<prompt>"
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

## Which lanes are live, and what down looks like

A lane is available when a probe says so, not when you remember it working.
`scripts/lane_probe.sh` runs the cheap version of each.

As at 2026-08-21: **codex is out of allowance until 27 Aug 13:30**, and its
failure is worth recognising because it looks like a success — the header prints
`model: gpt-5.6-terra` and `reasoning effort: high` exactly as requested, then the
`-o` file is written empty. **Grok is at 98.8% of an observed plan period.** GLM,
Gemini, Opus and Fable are live.

## Substitution

When a lane is down, `lane_pick.py` picks the next one that still has headroom
inside the same task class. Two invariants survive every substitution:

- **REVIEWER ≥ WRITER.** Lowering a reviewer's effort keeps the invariant;
  lowering its model breaks it.
- **VERIFIER ∉ WRITER's family.** The `family` field in the registry is what
  makes this checkable: `xai`, `google`, `zai`, `openai`, `anthropic`. When every
  out-of-family lane is down, verification still runs in-family and is **recorded
  as degraded**, never quietly promoted.

Work never routes down to a cheaper sibling to get around a limit, and it is
never dropped. Claude is the fail-back.
