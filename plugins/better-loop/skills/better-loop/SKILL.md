---
name: better-loop
description: >-
  Arm recurring or event-driven work as a change-gated watcher this skill creates itself, so a tick fires only when something has actually changed. Use when someone wants work that keeps running — "loop on this", "keep checking the deploy", "monitor the benchmark runs and fix errors", "create a loop prompt", "harden this loop" — and when a loop has already misfired: "what exactly is performing the loop, I expected to see a monitor", "I expected /loop to be able to be left", "the loop stopped", "why is this session so expensive". Also use as a follow-up to the built-in command (`/loop /better-loop <intent>`, formerly loop-harness). Picks the mechanism first, writes the tick protocol to docs/loops/loop-<slug>.md, preflights the probe for determinism and the skills the tick names, then arms a Monitor that polls a probe command and wakes the session only on a change — with a known-state register, a wake budget and a dry-stop, so a failure already reported is not re-sent turn after turn. Routes to better-goal when the work has a verifiable finish line. NOT for a one-off task that finishes in a single turn.
---

# better-loop — a loop that only speaks when something changed

A scheduled loop re-sends the same unmet condition, the same failing tasks and
the same status poll turn after turn, and each fire re-bills the session's whole
accumulated prefix. Measured across twelve heavy sessions, five did exactly that
and accounted for 91% of input between them. A smaller context window does not
help: nothing about a smaller window stops a loop from restarting.

So the loop here is not a schedule. It is a **probe** — one cheap deterministic
command whose output is the state you care about — polled by a watcher this skill
arms, which wakes the session only when the answer changes, and sends the delta
rather than the whole state. A quiet system costs nothing. A system that keeps
failing the same way costs one wake, then progressively fewer.

Deliver that scope. The armed loop does the underlying work; this pass sets it up.

`references/mechanism-choice.md` picks the mechanism. `references/mechanics.md`
is the ground truth. `references/failure-modes.md` maps each observed failure to
its fix.

## Protocol

### 1. Choose the mechanism

The decision that matters most, and the one the built-in `/loop` does not make.
Full table with worked cases: `references/mechanism-choice.md`.

| The next tick should start when… | Use | Why |
|---|---|---|
| Some observable state changes — a file, a queue, a CI result, a count | **`watch.sh` under `Monitor`** | The default here. No wake without a change |
| A log line or stream event appears | **`Monitor` on the stream directly** | Already event-driven; no probe needed |
| The work has a verifiable end state | **better-goal** | That is a finish line, not a cadence. Say so and route |
| The tick needs no session context | **`watch.sh --tick-cmd`** | Runs `claude -p` detached; no prefix to re-bill at all |
| Something genuinely must happen on a clock — a 9am digest | **`/loop <interval>` or `CronCreate`** | The only case where a schedule is right |

Most requests phrased as "keep doing X until Y" are a goal wearing a loop's
clothes. Route rather than arming the wrong thing.

### 2. Write the probe

The probe is the whole design. It should print, deterministically, the state the
loop reacts to — and nothing else:

```bash
gh run list --limit 5 --json status,conclusion,name --jq '.[]|"\(.name) \(.status) \(.conclusion)"'
pnpm test --run 2>&1 | grep -cE '✕|FAIL'
ls -1 docs/features-to-triage/*.md 2>/dev/null | wc -l
```

Two properties matter. **Deterministic**: two runs against an unchanged world
give identical output, so a timestamp, a duration, a PID or an unsorted listing
has to be stripped — otherwise every poll reads as a change and the loop is a
polling loop again. **Narrow**: only what you would act on. A wide probe turns
every unrelated tremor into a wake.

### 3. Write the tick protocol

`docs/loops/loop-<slug>.md` — the brief, committable and reviewable. Template in
`references/templates.md`. It needs an escalation branch, an explicit stop
condition, and what to do with an item that needs a human.

`.claude/loop.md` is only needed when composing with a bare `/loop`; it is capped
at 25,000 bytes and `scripts/write-brief.sh` size-checks it.

### 4. Preflight

`scripts/preflight.sh --probe '<cmd>' --skills '<list>'` runs the probe twice and
compares, so non-determinism is caught before it costs anything, and resolves
every skill the tick names — a built-in or `disable-model-invocation` skill
cannot be invoked by the model, so a tick told to run one reads the instruction
and carries on as though it had.

### 5. Arm it

`scripts/arm.sh --slug <slug> --probe '<cmd>' [--interval 120] [--stop-when
'<cmd>'] [--tick-cmd '<cmd>'] [--max-wakes 12] [--dry-stop N]` writes
`.claude/loops/<slug>.json` and prints the exact `Monitor` call. Run it with
`--dry-run` first.

Four bounds, and each answers a different way a loop goes wrong:

- **`--max-wakes`** (12/hour) — a floor under the cost of a probe that turns out
  to be noisier than expected. Past it the watcher writes to the ledger and says
  once that it has gone quiet.
- **`--repeat-after`** (1800s, doubling, capped at 4h) — a state already seen is
  worth one wake, then progressively fewer. This is what stops a flapping build
  or a recurring failure from being re-reported every time it returns.
- **`--dry-stop`** — exit after N unchanged polls, for work that should end when
  the world settles.
- **`--stop-when '<cmd>'`** — exit 0 means finished. If you find yourself
  reaching for this on every field, the work has a finish line: use better-goal.

There is no cron and no settings change, so there is no seven-day expiry and
nothing to clean up in settings afterwards.

### 6. Report what is watching

One block: the mechanism and why, the probe, the interval, what wakes the
session and what will not, the bounds, where the ledger is, how to read status
(`scripts/status.sh`), and how to stop (`TaskStop` on the monitor, then
`scripts/disarm.sh <slug>`).

## Delegation

This skill runs in-session. Spawn a subagent only to survey a backlog too large
to read directly — one agent, not several. The loop's own ticks are where the
work happens.

## Operating rules

- **A wake must carry new information.** That is the single rule the rest follow
  from. If a tick would say what the last one said, it should not happen.
- **Send the delta, not the state.** The watcher diffs against the last probe
  output and sends what moved. Re-sending the full state is how a loop pays for
  the same six failing tasks fifty times.
- **Prefer a detached tick to a wake** where the work does not need the
  conversation. `--tick-cmd 'claude -p "…"'` runs in a fresh process with no
  prefix to re-bill.
- **Check the wake ratio.** `status.sh` prints wakes against polls. A loop waking
  on most polls has a probe that is non-deterministic or too wide, and it costs
  what a cron would.
- **One loop per concern**, and check `preflight.sh` for one already armed.
- **A human verdict never blocks a tick.** Where the protocol has a review step,
  queue the item for the human on disk and carry on with the next one. The
  owner's standing instruction is explicit — *"don't wait on me for future
  rounds, I can provide my feedback later once the AI models have performed their
  own reviews"* — and a loop waiting on someone asleep is indistinguishable from
  one that crashed.
- **The ledger is the answer.** "How's it going" is read from the file, never by
  asking the loop — asking it costs a turn and tells you what the ledger already
  knew.
