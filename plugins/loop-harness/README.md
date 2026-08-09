<p align="center">
  <img src="assets/banner.png" alt="loop-harness: a porcelain icon of a bearing needle circling a fixed watch-point, one vermilion tick per pass, beside the wordmark and the line: a loop worth leaving alone" width="100%" />
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> loop-harness</h1>

<p align="center"><strong>A loop worth leaving alone.</strong><br />
A hardening layer over Claude Code's built-in <code>/loop</code>, and the sibling of <a href="../goal-harness">goal-harness</a>.</p>

<p align="center">
  <img alt="Version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-D33C21">
  <img alt="SWE skill: session control" src="https://img.shields.io/badge/SWE_skill-session_control-434A55">
  <img alt="Picks: monitor, dynamic or cron" src="https://img.shields.io/badge/picks-monitor_dynamic_or_cron-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

`/loop` schedules a cron in the current session. That's the whole mechanism, and every one of its edges is a way for a loop to look fine while doing nothing.

It **expires after seven days**; the task fires one last time, deletes itself, and nothing warns you. It fires **only while the session is idle**. It **never catches up** a fire it missed. It dies on `/clear`.

Then there's the one that costs the most. Since **v2.1.196 a scheduled fire only invokes skills Claude is allowed to invoke on its own**. Built-in commands, and any skill marked `disable-model-invocation` (which includes the bundled `/verify` and `/code-review`), arrive at the run as **plain text**. No error. The run reads the text, treats it as a note, and carries on. A loop whose whole job was "run `/code-review` every hour" ticks correctly all day and reviews nothing.

The other half of the problem isn't mechanical, it's that a loop has no surface. From the session that armed one:

> "what exactly is performing the loop; i expected to see a monitor or script running, did i invoke it incorrectly?"
> "i expected /loop to be able to be left"

Nothing was wrong. A dynamic loop is a scheduled wakeup with no visible process, so a working loop and a dead one look the same.

## What it does

### It picks the mechanism first

This is the decision that matters most, and `/loop` doesn't make it; it schedules whatever you typed. The question that settles it is **what has to be true for the next tick to be worth running**.

| Answer | Mechanism | Why |
|---|---|---|
| "Something happened" (a log line, CI finishing, a PR comment) | **Monitor**, `persistent: true` | The event wakes the session as it happens. No wasted ticks, cheaper, and visible |
| "The work is finished" | **[goal-harness](../goal-harness)** | That's a finish line, not a cadence. It routes rather than arming the wrong thing |
| "Enough time has passed, but how much varies" | **Dynamic pacing** | The run picks 60 to 3,600 seconds per tick from what it just saw |
| "It's 9am" / "another five minutes" | **Fixed cron** | The only case where polling is actually right |
| "The same sweep as last time" | **Bare `/loop` + `.claude/loop.md`** | The file replaces the built-in maintenance prompt |
| "It has to run whether or not my laptop is open" | **Routines**, a Desktop task, or GitHub Actions | `/loop` needs the session open. Better to say so than arm something that won't survive |

Most requests phrased "keep doing X until Y" are a goal wearing a loop's clothes.

### Then it writes, preflights and arms

**Two files, one source of truth.** `docs/loops/loop-<slug>.md` is the full brief, committable and reviewable. `.claude/loop.md` is the rendered active file Claude Code reads for a bare `/loop`, and it's **capped at 25,000 bytes**; past that the tail is truncated with a warning, so the end of your protocol silently stops applying. `write-loop-md.sh` size-checks and refuses.

**The preflight** covers the traps: skills that arrive as text, `CLAUDE_CODE_DISABLE_CRON`, a symlinked `.claude` or `scheduled_tasks.json` (which makes scheduling fail outright), the 50-task-per-session cap, `loop.md` size and precedence, and whether the interval maps to a clean cron. `7m` doesn't; it gives uneven gaps at `:56` to `:00`. `90m` is an hour and a half, which cron can't express at all.

**Arming happens in an order**, so the loop has a wake signal before it has a schedule:

1. **The Monitor**, if events drive the ticks, with a filter covering failure as well as success.
2. **The loop itself**, running the first tick immediately rather than waiting for the first fire.
3. **A heartbeat** at 1,200 to 1,800 seconds. In dynamic pacing a tick that neither reschedules nor stops gets one fallback fire about twenty minutes later and then the loop ends; the heartbeat is what catches that.
4. **A renewal reminder** on day six, because of the seven-day expiry.
5. **The ledger**, one row per tick, via `tick.sh`.

> [!IMPORTANT]
> A monitor is only as good as its filter, and the failure is always the same shape: it watches for the success marker and goes quiet on a crash, which is indistinguishable from still running. Before arming one, ask whether it would emit anything if the process died right now. If not, widen it. Noise is cheaper than a missed failure.

> [!NOTE]
> `--resume` restores unexpired crons, but **Monitor and background Bash tasks are never restored**. A loop whose wake signal was a Monitor comes back deaf, so the tick protocol calls `TaskList` first and re-arms it. Arming is idempotent, so that costs nothing when it's already running.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install loop-harness@fledgeling-plugins
```

## Using it

**On its own:**

```text
/loop-harness monitor the benchmark runs, resolve any harness or config errors,
and restart the benchmarks as needed
```

**As a follow-up to the built-in:**

```text
/loop /loop-harness keep checking the deploy and fix what breaks
```

**After a loop has gone quiet**, or when you can't tell whether it's running. It reads the actual scheduled tasks and the ledger.

`scripts/status.sh` answers "how's it going" without interrupting the run, including a warning when the expiry is within a day. `scripts/disarm.sh` removes the active `loop.md` and prints what still has to be cancelled in the session, because a cron job and a Monitor are session state rather than files and no script can remove them.

## The rules that keep it useful

**Prefer an event to a poll.** A Monitor that streams a line when something happens beats a cron asking every five minutes whether anything happened, on cost, on latency, and on ticks wasted.

**Bound the loop.** A stop condition in the tick protocol, plus a seven-day expiry you know the date of.

**One loop per concern.** Two loops in one session compete for idle time and both get slower.

**Give every tick a no-op branch.** Without one, a tick with nothing to do invents work to justify itself.

## What's in the box

```text
skills/loop-harness/
  SKILL.md
  references/
    mechanics.md          how /loop actually works, with the binary and doc citations
    mechanism-choice.md   the decision table, worked cases, monitor filters, intervals
    failure-modes.md      ten observed failures, each mapped to its fix
    templates.md          the brief, the active loop.md, the ledger, the arming sequence
  scripts/
    preflight.sh          the traps; read-only, exits 1 if anything blocks
    write-loop-md.sh      renders and size-checks .claude/loop.md; --dry-run shows the diff
    tick.sh               appends one ledger row per tick
    status.sh             reads the ledger, warns near the expiry
    disarm.sh             removes the active loop.md, prints what's left to cancel
evals/evals.json          six cases plus the process evals
```

## What it doesn't do

**It can't keep a loop running without the session.** `/loop` needs the conversation open and the machine on. Backgrounding the session carries the tasks over and keeps them firing without a terminal, which is usually the fix; where the work genuinely has to run unattended, the skill routes you to Routines, a Desktop scheduled task, or GitHub Actions instead of arming something that won't last the night.

**It doesn't survive `/clear`.** A new conversation drops every session-scoped task. The brief and the ledger stay on disk, so re-arming is quick, but the loop itself is gone.

**It can't make a tick correct.** It can make a tick visible, bounded, and honest about whether it ran. What the tick does is still down to the protocol you wrote.
