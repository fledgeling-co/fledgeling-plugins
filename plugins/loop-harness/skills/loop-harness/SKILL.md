---
name: loop-harness
description: Turn a rough intent into a hardened, armed /loop that survives being left alone. Use when someone wants recurring or self-paced work — "loop on this until it's done", "keep checking the deploy", "monitor the benchmark runs and fix errors", "create a loop prompt", "set up a loop.md", "harden this loop" — and when a loop has already misfired: "what exactly is performing the loop, I expected to see a monitor", "I expected /loop to be able to be left", "did I invoke it incorrectly", "the loop stopped". Also use as a follow-up to the built-in command (`/loop /loop-harness <intent>`). Picks the mechanism first (Monitor for event-driven, dynamic pacing for self-paced, fixed cron for true polling, or goal-harness when the work has an end state), writes .claude/loop.md within its 25,000-byte cap, preflights the traps that make a loop silently do nothing — non-model-invocable skills, a disabled scheduler, a symlinked .claude, the seven-day expiry — applies settings after showing a diff, and arms the loop with its wake signal, a heartbeat, a renewal reminder and a per-tick ledger. NOT for work with a verifiable finish line (use goal-harness) or a one-off task.
---

# loop-harness — make a loop worth leaving alone

`/loop` is thinner than it looks. It schedules a cron in the current session,
and that is all it is: the cron expires after seven days, fires only while the
session is idle, never catches up a fire it missed, dies when the conversation
is cleared, and since v2.1.196 hands any skill Claude may not invoke on its own
to the run as **plain text** rather than executing it. A loop can therefore tick
on schedule for hours and accomplish nothing, with no error anywhere.

Your job is to choose the right mechanism for the work — polling is usually the
wrong one — write the tick protocol to a file, fix the settings that make a tick
a no-op, and arm the loop with the signal that actually wakes it, a heartbeat
that catches a tick which forgot to reschedule, and a ledger that answers "how's
it going" without interrupting the run.

Deliver that scope. Do not begin the underlying work in this pass — the armed
loop does the work.

`references/mechanics.md` is the ground truth. `references/failure-modes.md`
maps each observed failure to its fix.

## Protocol

### 1. Choose the mechanism before writing anything

This is the decision that matters most, and the built-in `/loop` does not make
it for you. Full table with worked cases: `references/mechanism-choice.md`.

| The next tick should start when… | Use | Why |
|---|---|---|
| A log line, file change, CI result or PR comment appears | **Monitor** (`persistent: true`) | The event wakes the session immediately. No polling, no wasted ticks, far cheaper |
| The work has a verifiable end state | **goal-harness** | A loop has no finish line; a goal does. Say so and route |
| Progress is real but the right interval varies | **`/loop <prompt>`** (dynamic pacing) | The run picks 60s–1h per tick via `ScheduleWakeup` |
| Something genuinely must be checked on a clock | **`/loop <interval> <prompt>`** | Fixed cron. The only case where polling is correct |
| It is the same maintenance sweep every time | **bare `/loop` + `.claude/loop.md`** | The file replaces the built-in maintenance prompt |

Most requests phrased as "keep doing X until Y" are a goal wearing a loop's
clothes. Route rather than arm the wrong thing.

If a Monitor is the wake signal, its filter must match **every terminal state**,
not just the happy path — a monitor that greps only for the success marker stays
silent through a crash, and silence is indistinguishable from still-running.

### 2. Write the tick protocol

Two files, one source of truth:

- `docs/loops/loop-<slug>.md` — the full brief, committable and reviewable.
- `.claude/loop.md` — the rendered active file Claude Code reads for a bare
  `/loop`. **Hard cap 25,000 bytes**; content past it is truncated with a
  warning. `scripts/write-loop-md.sh` renders, size-checks and writes both.

Template: `references/templates.md`. The tick protocol needs a no-op branch (a
tick with nothing to do must be cheap and silent), an escalation branch, an
explicit stop condition, and the ledger append.

### 3. Preflight

`scripts/preflight.sh` checks the traps that make a loop tick and do nothing:

| Check | Why it matters |
|---|---|
| Every skill named in the prompt | Non-model-invocable ones arrive as plain text and never run — `/verify` and `/code-review` among them |
| `CLAUDE_CODE_DISABLE_CRON` | Set to `1` and `/loop` and the cron tools are gone entirely |
| `.claude` and `scheduled_tasks.json` not symlinks | Scheduling fails with an error |
| Existing scheduled tasks | 50 per session; a stale loop from an earlier run competes with this one |
| `loop.md` size and precedence | Project `.claude/loop.md` shadows `~/.claude/loop.md`; over 25,000 bytes is truncated |
| Interval maps to clean cron | `7m` and `90m` do not; they get rounded and the gaps go uneven |

### 4. Apply config, showing the diff first

`scripts/write-loop-md.sh --dry-run` prints the exact before/after for
`.claude/loop.md`, checks it against the 25,000-byte cap, and writes nothing.
Run it before the real write; it backs up any existing file.

Most loops need no settings change at all — say so rather than showing an empty
diff. Where preflight did find one (`CLAUDE_CODE_DISABLE_CRON`, a symlinked
`.claude`), there is no arming script for it: print the exact before/after
yourself and apply it on the user's OK. Settings are load-bearing across every
session in scope.

### 5. Arm it

In this order, so the loop has a wake signal before it has a schedule:

1. **The Monitor**, if events drive the ticks — `persistent: true`, filter
   covering success *and* failure signatures.
2. **The loop itself** — the mechanism chosen in step 1, run the first tick
   immediately rather than waiting for the first fire.
3. **The heartbeat** — a fallback wakeup at 1200–1800s. In dynamic pacing a tick
   that neither reschedules nor stops ends the loop; the heartbeat is what
   catches that. With a Monitor armed, keep the delay in that range: the Monitor
   is the signal and this is only the backstop.
4. **The renewal reminder** — a one-shot at day six. Recurring tasks expire
   after seven days: the task fires one last time and deletes itself. Without a
   reminder a long-running loop simply stops one morning.
5. **The ledger** — `scripts/tick.sh` appends a row per tick, called from the
   tick protocol.

### 6. Report what is watching

One block: the mechanism and why it was chosen, the job ID and cadence, what
wakes it, what ends it, the seven-day expiry date, where the ledger is, how to
read status (`scripts/status.sh`), and how to stop (`Esc` while it waits,
`CronDelete <id>`, or `scripts/disarm.sh`).

Name the job ID. It is what `CronDelete` needs and it is not recoverable from
the transcript once compaction has run.

## Delegation

This skill runs in-session. Spawn a subagent only to survey a backlog too large
to read directly — one agent, not several. The loop's own ticks are where the
work happens.

## Operating rules

- **Prefer an event to a poll.** A Monitor that streams a line when something
  happens beats a cron that asks every five minutes whether anything happened,
  on cost, on latency and on ticks wasted.
- **A silent filter is a broken filter.** Before arming a Monitor, ask: if this
  process crashed right now, would anything be emitted? If not, widen it.
- **Bound the loop.** A stop condition in the tick protocol, plus the seven-day
  expiry the user knows about.
- **One loop per concern.** Two loops in one session compete for idle time and
  both slow down.
- **A human verdict never blocks a tick.** Where the protocol has a review step,
  the loop queues the item for the human and *carries on with the next one*;
  it does not park until an answer arrives. The owner's standing instruction is
  explicit — *"don't wait on me for future rounds, I can provide my feedback
  later once the AI models have performed their own reviews"* — and a loop
  waiting on a person who is asleep is a loop that has stopped, indistinguishable
  from one that crashed. Write the queue to disk (a review file, a ledger
  column), let model-side review gate the round instead, and apply human verdicts
  whenever they land.
- **The ledger is the answer.** "How's it going" is read from the file, never
  inferred from the transcript.
