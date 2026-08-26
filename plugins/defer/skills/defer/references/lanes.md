# Lanes — who does what, on which CLI, with which arguments

Canonical. Every skill that hands work to another model routes through this file
and through `scripts/lane_pick.py`, which reads the same policy from
`scripts/lane_registry.py`. Change a lane here **and** in the registry, or the
selftest fails — which is the point, because a policy in two places drifts and
the drift is silent.

This file is the *policy* half: which lanes may do which class of work. The
*capability* half — which of those lanes is good enough for a particular piece,
measured rather than asserted — is `capability.md`.

## The matrix

| Task class | Lane | Model | Effort | Chosen by |
|---|---|---|---|---|
| **Implementation** — writing code | glm · grok · codex-sol · **codex-luna-max** · codex-sol-high · codex-terra-max · codex-terra-medium · gemini · opus | `glm-5.3` · `grok-4.6` · `gpt-5.6-sol` · **`gpt-5.6-luna`** · `gpt-5.6-sol` · `gpt-5.6-terra` · `gpt-5.6-terra` · `gemini-3.7-flash-high` · `claude-opus-5` | high · **xhigh** · medium · **max** · high · **max** · medium · high · xhigh | shape, then measured headroom, then the preference order |
| **Completeness critic** | glm · grok · gemini | `glm-5.3` · `grok-4.6` · `gemini-3.7-flash-high` | high · **xhigh** · high | measured headroom |
| **General** — anything neither referred nor a verdict | codex-terra · codex-terra-medium · glm · grok · gemini | `gpt-5.6-terra` · `gpt-5.6-terra` · `glm-5.3` · `grok-4.6` · `gemini-3.7-flash-high` | **high** · medium · high · xhigh · high | shape, then fixed |
| **Referral** — a decision put to another model | codex-sol · fable | `gpt-5.6-sol` · `claude-fable-5` | **medium** · **high** | fixed |
| **Verification** — task and same-family | opus | `claude-opus-5` | **xhigh** | fixed |
| **Design review** | opus · fable | `claude-opus-5` · `claude-fable-5` | xhigh · high | fixed |

Three rules sit above the table and hold everywhere:

- **`gpt-5.6-sol` never runs at `max`.** It is the referral lane at `medium` and
  the implementation lane at `high`. Anything that is not a referred decision
  goes to a terra lane or to `codex-sol-high`. The benchmark ranks `sol@max`
  second overall and tied with opus; the rule stands anyway, because `sol@high`
  holds 63.8 of that 66.6 at half the price. `capability.md` carries the figures
  if the rule is ever revisited.
- **Fable judges; it does not verify.** A referred decision, a fork, a design
  call — yes. Grading code against a ticket, or a delivered feature against its
  acceptance criteria — no: that is `claude-opus-5` at `xhigh`.
- **Design review stays inside Anthropic's family.** Opus and Fable only. No
  other family reviews rendered UI here.

The five codex lanes share one account, so they share one meter. Adding an effort
variant buys a cheaper lane, never more headroom.

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

**`DELIVERY_PENALTY`** — whether the artefact arrived at all. `gemini` carries
12 points, measured 2026-08-26: running as an autonomous builder it failed 8 of
12 dispatches and one completion report was fabricated — 4,406 bytes claiming
four schedulers created, against a ground truth of nothing created. A bench
cannot catch that, because a fabricated report grades as a delivered artefact.
Lift it when a dispatch set of 12 or more completes with no fabricated report
and a failure rate under 20%.

**`PREFERENCE_ORDER`** — the owner's tie-break, `glm` → `grok` → `codex-sol` →
`codex-luna-max` → … → `gemini`. It runs *last*, only between lanes already
agreed equivalent on the measured number, so policy never overrules a lane that
is genuinely better at the shape in front of it.

## Running a lane

`lane_pick.py --task <class> [--shape <shape>]` prints the argv and the
environment for the lane it chose. The templates it prints are these:

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
codex exec -m gpt-5.6-terra -c model_reasoning_effort="max" \
  -s read-only -o /tmp/lane.md "<prompt>" < /dev/null
codex exec -m gpt-5.6-terra -c model_reasoning_effort="medium" \
  -s read-only -o /tmp/lane.md "<prompt>" < /dev/null
codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" \
  -s read-only -o /tmp/lane.md "<prompt>" < /dev/null
codex exec -m gpt-5.6-sol -c model_reasoning_effort="high" \
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

## The timeout is part of the invocation

Every command in this file needs a bound of **900 seconds**, or backgrounding. The
harness default is 120 000 ms and the median lane call is **150 seconds**, so a lane run
at the default is killed about half the time — 23 of grok's 24 failures in the measured
window were exactly that, 3,240 seconds of wait on calls that would have succeeded. A
killed call leaves a truncated output file, which reads identically to a lane that
answered with nothing.

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
