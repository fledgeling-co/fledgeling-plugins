<p align="center">
  <img src="assets/banner.png" alt="better-loop: a porcelain icon of a bearing needle circling a fixed watch-point, one vermilion tick per pass, beside the wordmark and the line: a loop worth leaving alone" width="100%">
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> better-loop</h1>

<p align="center"><strong>A loop worth leaving alone.</strong><br />
A watcher that wakes the session only when something changed, and the sibling of <a href="../better-goal">better-goal</a>.</p>

<p align="center">
  <img alt="Version 2.0.0" src="https://img.shields.io/badge/version-2.0.0-D33C21">
  <img alt="SWE skill: session control" src="https://img.shields.io/badge/SWE_skill-session_control-434A55">
  <img alt="Wakes: on change only" src="https://img.shields.io/badge/wakes-on_change_only-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

Two reasons, and the second is the expensive one.

**`/loop` schedules a cron in the current session.** That is the whole mechanism, and every edge of it is a way for a loop to look fine while doing nothing. It **expires after seven days**: the task fires one last time, deletes itself, and nothing warns you. It fires **only while the session is idle**. It **never catches up** a fire it missed. It dies on `/clear`. And since **v2.1.196 a scheduled fire only invokes skills Claude may invoke on its own**: built-in commands and anything marked `disable-model-invocation` (the bundled `/verify` and `/code-review` included) arrive as **plain text**, with no error. A loop whose whole job was "run `/code-review` every hour" ticks correctly all day and reviews nothing.

**And a loop that fires on a schedule pays for every fire.** Measured across the heaviest sessions on this machine:

> 5 of 12 of the heaviest sessions (91% of input between them) re-sent the same unmet condition, the same six failing tasks, the same status poll turn after turn, paying the whole prefix each time.

A wake is not free and it is not cheap. It re-bills the accumulated session context, so a five-minute cron watching a deploy that changes twice in two hours buys 24 wakes to carry 2 pieces of news. Nothing about a shorter interval fixes that; the interval is the problem.

There is a third, softer reason. A loop has no surface. From the session that armed one:

> "what exactly is performing the loop; i expected to see a monitor or script running, did i invoke it incorrectly?"
> "i expected /loop to be able to be left"

Nothing was wrong. A dynamic loop is a scheduled wakeup with no visible process, so a working loop and a dead one look identical.

## What it does

### It runs the probe outside the session

The loop is a `Monitor` running `watch.sh`, a plain shell script that polls a **probe command** on an interval and compares the answer to last time. Polling costs nothing: no model, no context, no tokens. Only a **change** produces a line, and only a line wakes the session.

```text
18:04  baseline   BUILDING
18:06  (quiet)
18:12  CHANGE     BUILDING → ERROR      ← woke the session
18:31  repeat     ERROR seen ×3, suppressed until 19:01

polls 47 · wakes 2 · budget 12/h
```

Forty-seven polls, two wakes. A five-minute cron would have been 24 wakes for the same two pieces of news.

### It refuses to re-send a failure you already have

This is the fix for the defect above, and it is mechanical rather than advisory. Every probe answer is fingerprinted into a **known-state register**. The first time a state appears it wakes the session. The second time it is suppressed and backed off; the third, further. A state seen three times is not reported again for half an hour, then an hour, capped at four.

A suppressed change is not a lost one; it goes to the ledger, so a quiet loop can prove it was working:

```markdown
| 4 | 2026-08-09 18:55 | repeat | seen ×3, suppressed until 19:25 [7f3e...] |
```

Four bounds sit on top of it, all in the state file: a **wake budget** (default 12 per rolling hour, after which changes go to the ledger only), **repeat-after** backoff, **dry-stop** after N unchanged polls, and **stop-when**, a command that ends the loop when it exits 0.

And when a wake does happen, it carries **the delta**, the lines that moved, not the whole probe output. The full state is one re-run away if the tick needs it.

### The tick can skip the session entirely

For work that does not need the conversation, `--tick-cmd` dispatches a fresh detached `claude -p` on a change. The session is never woken and never billed for the prefix. It is the cheapest shape available, and the trade is real: a detached tick that fails fails quietly, so its log is worth reading.

### It picks the mechanism before writing anything

`/loop` does not make this decision; it schedules whatever you typed. The question that settles it is **what has to be true for the next tick to be worth running**.

| Answer | Mechanism | Why |
|---|---|---|
| "Something changed": a status, a queue, CI, a PR | **Watcher** (`watch.sh` under `Monitor`) | The change wakes the session. No wasted ticks, no expiry, and visible |
| "Something changed, and I don't need to see it" | **Watcher + detached tick** | The cheapest tick there is: no wake, no prefix |
| "A line appeared in a stream" | **`Monitor` on the stream directly** | No probe needed; the event is already a line |
| "The work is finished" | **[better-goal](../better-goal)** | That is a finish line, not a cadence. It routes rather than arming the wrong thing |
| "It's 9am" / "the first of the month" | **Fixed cron** | Wall-clock is the one case where a schedule is genuinely the right answer |
| "It has to run whether or not my laptop is open" | **Routines, a Desktop task, or GitHub Actions** | A session-bound loop needs the session open. Better to say so than arm something that will not survive |

Most requests phrased "keep doing X until Y" are a goal wearing a loop's clothes.

### The preflight blocks on a probe that lies

The headline check runs your probe **twice** and compares. A probe carrying a timestamp, a PID, a duration or an unsorted list changes on every poll, which turns a change-gated watcher back into a cron with extra steps, and it is invisible until the bill arrives.

The rest covers interval sanity, skills that would arrive as plain text, loops already armed in this repo, and (under `--cron`, for the composed case) the scheduler flags, a symlinked `.claude`, the 50-task cap, `loop.md` size and precedence, the seven-day expiry, and whether the interval maps to a clean cron at all. `7m` does not; it gives uneven gaps at `:56` to `:00`. `90m` cron cannot express.

> [!IMPORTANT]
> A watcher is only as good as its filter, and the failure is always the same shape: it watches for the success marker and goes quiet on a crash, which is indistinguishable from still running. Before arming one, ask whether it would emit anything if the process died right now. If not, widen it. Noise is cheaper than a missed failure.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install better-loop@fledgeling-plugins
```

## Using it

**On its own:**

```text
/better-loop monitor the benchmark runs, resolve any harness or config errors,
and restart the benchmarks as needed
```

**When a loop has gone quiet**, or when you cannot tell whether it is running. It reads the state file, the ledger and the live tasks rather than guessing.

**Composed with the built-in**, where a wall-clock cadence is genuinely what you want:

```text
/loop /better-loop keep checking the deploy and fix what breaks
```

`scripts/status.sh` answers "how's it going" without waking the loop or costing it a turn, and warns when the wake-to-poll ratio says the probe is too wide to be worth gating on. `scripts/disarm.sh` clears the state; `TaskStop` stops the monitor.

### The one thing a watcher cannot report about itself

A `Monitor` runs in the session's shell, so it dies when the session does — cleanly, on an API error, or on a crash — and the state file goes on reading `armed: true` with nobody told. In the sibling harness that shape left one run armed for fourteen days and another for six.

So `watch.sh` stamps `last_poll_at` on every poll, and two things read it. `status.sh` reports a loop whose last poll is older than three intervals as stopped rather than watching. And `sentinel.sh`, registered on `SessionStart`, tells the next session that opens the repo which loops died — once each, and nothing at all when every loop is polling. That hook is the only settings change this skill makes; `disarm.sh` removes it when no loop is left armed, and `arm.sh --no-sentinel` skips it.

## The rules that keep it useful

**A wake must carry new information.** Not a poll, not a repeat, not output already in the context. Everything else here follows from that.

**Prefer a change to a schedule.** A watcher that emits when something moves beats a cron asking every five minutes whether anything moved: on cost, on latency, and on ticks wasted.

**Bound the loop**: a wake budget, a repeat backoff, a dry-stop, and a stop-when. Four bounds, all in one file you can read.

**One loop per concern.** Two loops watching the same thing wake the session twice for one change.

**Give every tick a no-op branch.** Without one, a tick with nothing to do invents work to justify itself.

## What's in the box

```text
skills/better-loop/
  SKILL.md
  references/
    mechanics.md         how the watcher, Monitor and /loop actually work,
                         with the binary and doc citations
    mechanism-choice.md  the decision table, what a tick costs, worked cases
    failure-modes.md     the observed failures, each mapped to its fix
    templates.md         the brief, the state file, the ledger, the arming sequence
  scripts/
    preflight.sh         probe determinism first; --cron adds the scheduler checks
    arm.sh               writes per-slug state, registers the SessionStart
                         sentinel, and prints the Monitor call
    watch.sh             the loop itself: polls, fingerprints, suppresses repeats,
                         stamps the heartbeat, emits CHANGE / DONE / ENDED /
                         QUIET / GONE
    sentinel.sh          SessionStart: reports loops whose session died
    tick.sh              appends one ledger row per tick
    status.sh            reads state and ledger; flags a wake-heavy probe
    disarm.sh            <slug> | --all | --loop-md
    write-brief.sh       renders and size-checks .claude/loop.md, for the
                         composed case only
evals/evals.json         six cases plus the process evals
EVALS.md                 the measured result against the no-skill baseline
```

## Does it earn its place

Measured the same way as its sibling: each case run twice from an identical
fixture, once with the skill and once with nothing, graded blind. Across both,
**32 of 33 assertions against the baseline's 12**, and **8 preferences out of
8**.

The two cases that carry it are the ones where the baseline was not merely
thinner but wrong. Asked what performs a no-interval loop, it said there is no
timer and the loop ended with the turn; dynamic pacing schedules a real pending
wakeup, so acting on that answer means re-arming something already scheduled.
Told to run `/verify` every 30 minutes, it concluded `/verify` does not exist,
missing that it is a bundled skill a scheduled fire delivers as plain text.

Against that, one honest tie: on "don't arm a loop with a dead verifier" the
baseline matched it 3/3. Those scores predate the rebuild around change-gated
watchers, so they measure the earlier `/loop`-hardening skill.
[EVALS.md](EVALS.md) has the table, the tie, the three defects the run found in
these skills, and what was never measured.

## What it doesn't do

**It can't keep a loop running without the session.** A `Monitor` lives in the conversation, and `--resume` does not restore one. Backgrounding the session keeps it alive without a terminal, which is usually the fix; where the work genuinely has to run unattended, the skill routes you to Routines, a Desktop scheduled task, or GitHub Actions rather than arming something that will not last the night.

**It doesn't survive `/clear`.** The state file, the ledger and the brief stay on disk, so re-arming is one command, but the watcher itself is gone.

**It can't make a tick correct.** It can make a tick change-gated, bounded, and honest about whether it ran. What the tick does is still down to the protocol you wrote.
