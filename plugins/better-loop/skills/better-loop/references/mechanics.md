# How the loop works

Ground truth for `SKILL.md`. Sources: the Claude Code binary
(`~/.local/share/claude/versions/2.1.229`, extracted strings), the `Monitor` tool
contract, and <https://code.claude.com/docs/en/scheduled-tasks.md> for the
built-in this skill replaces.

## The mechanism in one paragraph

`arm.sh` writes `.claude/loops/<slug>.json` and prints a `Monitor` call.
`watch.sh` runs under that Monitor, evaluates the probe command every
`--interval` seconds, and hashes the output. Identical hash, no output. Changed
hash, one line to stdout carrying the **delta** — and that line becomes a
`<task-notification>` delivered as a `queued_command` with
`commandMode === "task-notification"`, which is the same path a scheduled task
uses, so it wakes an idle session. No cron, no settings change, no expiry.

## Why change-gating, and what it saves

Every wake re-bills the session's accumulated prefix. That is the cost model the
whole design follows from: a tick is not cheap because the tick is short, it is
expensive in proportion to how long the session has been running.

Measured across twelve heavy sessions, five re-sent the same unmet condition, the
same failing tasks and the same status poll turn after turn, and accounted for
91% of input between them. A smaller context window does not help — nothing about
a smaller window stops a loop from restarting.

Three levers, in order of how much they save:

1. **No wake without a change.** The common tick is a hash comparison in a
   background process and costs nothing at all.
2. **The delta, not the state.** `watch.sh` diffs against the previous probe
   output and sends only what moved, capped at `--max-lines`.
3. **A detached tick instead of a wake.** `--tick-cmd 'claude -p "…"'` runs the
   work in a fresh process with no prefix to re-bill. Right whenever the tick
   does not need the conversation's context.

## The known-state register

`.claude/loops/<slug>.seen` holds each fingerprint the probe has produced, how
many times, and the earliest time it may wake the session again. A state seen
before is worth one wake, then progressively fewer: the backoff is
`repeat_after × times_seen`, capped at four hours.

This is what stops a flapping build, a recurring rate-limit or a failure that
returns after a fix from being re-reported at full price each time. The register
is capped at 500 entries so a high-cardinality probe cannot grow it without
bound.

## The wake budget

`--max-wakes` (default 12/hour) is a floor under the cost of a probe that turns
out noisier than expected. On exhaustion the watcher emits **one** QUIET line
saying so, then writes changes to the ledger only. `status.sh` surfaces the
wake-to-poll ratio, which is the number worth watching: a loop waking on most
polls has a non-deterministic or over-wide probe and costs what a cron would.

## Probe determinism

A probe whose output differs between two runs against an unchanged world makes
every poll a change. Timestamps, elapsed times, PIDs, unsorted directory
listings and progress percentages are the usual culprits. `preflight.sh --probe`
runs it twice and compares, which catches this before it costs anything.

Where the underlying command insists on including one, strip it:

```bash
gh run list --limit 5 --json name,status,conclusion --jq '.[]|"\(.name) \(.status) \(.conclusion)"' | sort
pnpm test --run 2>&1 | grep -cE '✕|FAIL'
```

## Monitor's own rules

From the tool contract, and both matter here:

- **Filters must match every terminal state.** A monitor watching only for the
  success marker is silent through a crashloop, and silence looks exactly like
  still-running. `watch.sh` emits on DONE, ENDED, QUIET and GONE as well as
  CHANGE for this reason.
- **Line-buffering is required at every pipe stage.** `grep` needs
  `--line-buffered`, `awk` needs `fflush()`, and `head` cannot flush at all — so
  `| head -N` delivers nothing until N matches accumulate. This applies to a
  monitor watching a stream directly; `watch.sh` prints whole lines itself.

Use Bash `run_in_background` instead of a monitor when you want exactly one
notification (a build finishing). Use a monitor when you want one per occurrence.
`persistent: true` keeps it alive for the session rather than the default
5-minute timeout.

## Resume

Background Bash and Monitor tasks are **never** restored on `--resume`. A loop
comes back deaf: the state file and ledger survive, the watcher does not. Re-run
the `Monitor` call `arm.sh` printed; `status.sh` shows whether the state file
still says `armed: true` with a stale ledger, which is the signature.

## What ends a loop

| Cause | Recoverable? |
|---|---|
| `TaskStop` on the monitor | Yes — re-run the `Monitor` call |
| `disarm.sh <slug>` | Yes; the watcher also exits on its next poll |
| `--stop-when` satisfied | Deliberate: emits DONE and exits |
| `--dry-stop N` unchanged polls | Deliberate: emits ENDED and exits |
| The state file deleted | Emits GONE and exits |
| Session exits / terminal closes | The watcher dies with the session |

There is no seven-day expiry, because there is no scheduled task.

## When composing with the built-in `/loop`

`/loop /better-loop <intent>` works and is additive. The built-in's own limits
then apply, and they are the reason it is not the default here:

| Limit | Value | Source |
|---|---|---|
| `loop.md` size | 25,000 bytes, then truncated with an inline warning | Binary constant `dIo=25000` |
| `loop.md` locations | `./.claude/loop.md`, then `~/.claude/loop.md` | Binary |
| Recurring task lifetime | 7 days, then one final fire and self-delete, no warning | Docs |
| Scheduled tasks per session | 50 | Docs |
| Minimum interval | 1 minute | Docs |
| Dynamic-pacing delay | clamped to 60–3600s | `ScheduleWakeup` contract |
| Fallback if a tick neither reschedules nor stops | ~20 min, once, then the loop ends | Docs, v2.1.202 |

Three modes, chosen by what is typed: a leading `^\d+[smhd]$` token is a fixed
interval (cron, first tick immediate); otherwise a trailing `every <N><unit>`
clause is; otherwise the whole input is the prompt and the mode is dynamic
pacing. Fires land up to 30 minutes late for recurring tasks (or half the
interval under an hour), derived from the task ID so the offset is stable. There
is no catch-up: a fire whose time passes mid-turn happens once when the session
goes idle, not once per missed interval.

### The v2.1.196 trap

*"As of v2.1.196, a scheduled fire only runs skills that Claude is allowed to
invoke on its own."* Built-in commands, skills marked
`disable-model-invocation: true` — **including the bundled `/verify` and
`/code-review`** — skills withheld by `skillOverrides` or a `Skill` deny rule, and
MCP prompts all arrive as plain text instead. There is no error: the run reads
the text as a note and continues. A loop whose whole job was "run /code-review
every hour" ticks correctly forever and reviews nothing.

The same constraint applies to a wake from `watch.sh`, because a wake is text the
model reads. `preflight.sh --skills` resolves each one.

### Provider caveat

On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform and
Microsoft Foundry: `loop.md` is not read, a bare `/loop` prints usage instead of
running the maintenance prompt, and a prompt with no interval runs on a fixed
10-minute schedule rather than dynamic pacing. The watcher is unaffected.

## The watcher dies with its session, and cannot say so

`Monitor` runs the watcher in the session's own shell. When the session ends the
process ends with it, and nothing rewrites the state file, so `armed: true`
survives indefinitely. Measured in the sibling `better-goal` harness: one run
read `armed: true` at turn 17 of 800 for fourteen days after its session hit
`API Error: Connection refused`, and a second sat armed for six days after its
session ended mid-turn.

Two mechanisms close it, and neither is inside the loop:

- **A heartbeat.** `watch.sh` stamps `last_poll_at` (epoch) on every poll.
  `status.sh` and `sentinel.sh` read that rather than the state file's mtime,
  because anything that writes to the file — including the sentinel's own
  reported flag — refreshes the mtime and makes a dead loop look freshly polled.
  A heartbeat older than three intervals, floored at two minutes, is dead.
- **A `SessionStart` hook.** `sentinel.sh` runs at the start of every session in
  the repo and reports each dead loop once, via
  `hookSpecificOutput.additionalContext`. Unlike a `Stop` hook it does not need
  to load in the session that registered it — it needs to be on disk before the
  *next* session starts, which it is — so the settings-watcher caveat that
  affects `better-goal` does not apply here.

`disarm.sh` removes the hook once no loop in the repo is armed. `--no-sentinel`
at arm time skips it entirely and leaves settings untouched, which costs exactly
the reporting above.
