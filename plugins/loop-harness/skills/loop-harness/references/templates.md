# Templates

## `docs/loops/loop-<slug>.md` — the source of record

`.claude/loop.md` is rendered from this. Keep the rendered file under 25,000
bytes; `write-loop-md.sh` checks.

```markdown
# Loop: <one line>

- **slug:** <kebab-slug>
- **mechanism:** monitor + dynamic pacing | dynamic | cron `*/5 * * * *` | bare loop.md
- **armed:** <YYYY-MM-DD HH:MM local>
- **expires:** <armed + 7 days>   ← recurring tasks self-delete here
- **job id:** <8-char id from CronCreate, or "dynamic">
- **wake signal:** <Monitor description, or "ScheduleWakeup only">
- **ledger:** docs/loops/loop-<slug>.ledger.md

## Each tick, in order

1. **Re-arm the wake signal if it is gone.** Call `TaskList`. If no Monitor
   named `<name>` is running, arm it — a resume never restores one:
   ```
   Monitor({ command: "<the filter>", description: "<name>", persistent: true })
   ```
2. **Check for work.** <the specific check — a log tail, a queue, a status API>
3. **If there is nothing to do:** say so in one line and go to step 6. Do not
   invent work to justify the tick.
4. **If there is work:** <what to do, concretely, with the commands>
5. **If something needs escalating:** <PushNotification criteria — an error the
   user would act on now, not routine progress>
6. **Append to the ledger:** `scripts/tick.sh <slug> "<verdict>" "<one line>"`
7. **Decide whether the loop continues.** If yes, re-arm per the mechanism
   below. If the stop condition holds, stop and say why.

## Stop when

- <the terminal condition — the run finished, the queue drained, the deploy
  reached a terminal state>
- <a bound — N consecutive no-op ticks, or a wall-clock deadline>

## Rescheduling

<dynamic:>
Call `ScheduleWakeup` as the last action of the turn with the sentinel prompt,
`delaySeconds` 1200–1800 while the Monitor is armed (it is the real signal and
this is the backstop), shorter only when actively watching something finish. To
end: `ScheduleWakeup {stop: true}` plus `TaskStop` on the Monitor.

<cron:>
The recurring cron fires the next tick automatically — do not call
`ScheduleWakeup` from a tick. To end: `CronDelete <job id>`.

## Notes

<Anything the tick needs and would otherwise re-derive: paths, credentials
location, which host, concurrency caps.>
```

## `.claude/loop.md` — the rendered active file

Plain Markdown, no required structure, written as if typing the `/loop` prompt
directly. It replaces the built-in maintenance prompt for a bare `/loop` and is
ignored whenever a prompt is supplied on the command line.

```markdown
Work the release/next branch, one tick at a time.

First call TaskList. If no monitor named "ci-watch" is running, arm it:
Monitor({command: "gh run watch --repo org/repo 2>&1 | grep -E --line-buffered
'completed|failure|cancelled|timed_out'", description: "ci-watch",
persistent: true})

Then: if CI is red, pull the failing job log, diagnose, and push a minimal fix.
If new review comments have arrived, address each and resolve the thread. If
everything is green and quiet, say so in one line and do nothing else.

Append one ledger row each tick:
  .claude/scripts/tick.sh release-next "<green|fixed|blocked>" "<one line>"

Stop when the PR is merged, or after 3 consecutive quiet ticks.
Full protocol and context: docs/loops/loop-release-next.md
```

Keep it short. Detail belongs in the source-of-record file the tick reads.

## `docs/loops/loop-<slug>.ledger.md`

```markdown
| tick | at | verdict | note |
|---|---|---|---|
| 1 | 2026-08-09 18:07 | fixed | 2 failing auth specs, pushed 3f2a1c |
| 2 | 2026-08-09 18:41 | green | nothing to do |
| 3 | 2026-08-09 19:12 | blocked | needs a decision — logged to open questions |
```

## Arming sequence

```
1. Monitor({command: "<filter covering success AND failure>",
            description: "<slug>-watch", persistent: true})

2. dynamic:  /loop <prompt>            — or run the first tick, then ScheduleWakeup
   cron:     CronCreate({cron: "<expr>", prompt: "<prompt>", recurring: true})
   bare:     /loop                     — reads .claude/loop.md

3. ScheduleWakeup({delaySeconds: 1500, prompt: "<sentinel>",
                   reason: "fallback heartbeat; monitor is the wake signal"})

4. CronCreate({cron: "<minute> <hour> <dom+6> <month> *",
               prompt: "loop-harness: loop <slug> expires tomorrow — re-arm it
                        or let it end. Brief: docs/loops/loop-<slug>.md",
               recurring: false})

5. scripts/tick.sh <slug> armed "mechanism=<x> job=<id> monitor=<name>"
```

Pick an off-minute for step 4 — `47 8` rather than `0 9` — so the one-shot
jitter window does not apply.

## Settings block

Only written when preflight found something to fix. Shown as a diff first.

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_CRON": "0"
  }
}
```

Most loops need no settings change at all. Say so rather than writing an empty
diff.
