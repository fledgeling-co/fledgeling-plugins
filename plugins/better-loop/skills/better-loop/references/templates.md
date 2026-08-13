# Templates

## `docs/loops/loop-<slug>.md` — the source of record

```markdown
# Loop: <one line>

- **slug:** <kebab-slug>
- **mechanism:** watcher | watcher + detached tick | monitor on a stream | dynamic | cron `*/5 * * * *`
- **probe:** `<the command>`
- **interval:** <N>s
- **bounds:** max-wakes <N>/h · repeat-after <N>s · dry-stop <N> · stop-when `<cmd>`
- **armed:** <YYYY-MM-DD HH:MM local>
- **ledger:** docs/loops/loop-<slug>.ledger.md

## What the probe means

<One paragraph mapping the probe's output to the world: what each line is, what
a change means, what a change does NOT mean. This is what the tick reads first,
so it does not have to re-derive it from the delta.>

## Each tick, in order

1. **Read the delta.** The wake carries what moved, not the whole state. Re-run
   the probe only if you need the rest.
2. **If the change is expected progress:** <what to do, concretely, with the
   commands>
3. **If it is a failure:** <diagnose and fix, or the escalation path>
4. **If it is a failure you have already seen:** it will not be reported again
   for a while. Either fix the cause or park it in writing — the loop is not
   going to remind you.
5. **If something needs escalating:** `PushNotification` for an error the user
   would act on now; not for routine progress.
6. **Append to the ledger:** `scripts/tick.sh <slug> "<verdict>" "<one line>"`
7. **Blocked on a person?** Write the question and your recommendation to
   `## Open questions` below, and carry on with the next item. Do not park the
   loop waiting for an answer.

## Stop when

- <the terminal condition, wired into --stop-when where a command can settle it>
- <a bound — N unchanged polls via --dry-stop, or a wall-clock deadline>

## Notes

<Anything the tick needs and would otherwise re-derive: paths, credentials
location, which host, concurrency caps.>

## Open questions

<Appended during the run. Empty at arm time.>
```

## `.claude/loops/<slug>.json`

Written by `arm.sh`, maintained by `watch.sh`, read by `status.sh`. Gitignored,
because the watcher executes the commands in it.

```json
{
  "slug": "release-next",
  "armed": true,
  "cwd": "/Users/you/Dev/project",
  "brief": "docs/loops/loop-release-next.md",
  "ledger": "docs/loops/loop-release-next.ledger.md",
  "probe": "gh pr checks 412 --json name,bucket --jq '.[]|\"\\(.name) \\(.bucket)\"' | sort",
  "stop_when": "gh pr view 412 --json state --jq '.state' | grep -q MERGED",
  "tick_cmd": null,
  "interval": 120,
  "max_wakes": 12,
  "repeat_after": 1800,
  "dry_stop": 0,
  "polls": 0, "wakes": 0, "ticks": 0
}
```

Two sidecars beside it: `<slug>.prev` (the last probe output, for the delta) and
`<slug>.seen` (the known-state register — fingerprint, times seen, earliest next
wake).

## `docs/loops/loop-<slug>.ledger.md`

Written by both `watch.sh` and `tick.sh`, one table. The suppressed rows matter
as much as the wakes: they are how a quiet loop proves it was working.

```markdown
| tick | at | verdict | note |
|---|---|---|---|
| 1 | 2026-08-09 18:07 | baseline | 6 line(s) [a1b2c3d4e5f60718] |
| 2 | 2026-08-09 18:23 | change | new [7f3e...] |
| 3 | 2026-08-09 18:25 | fixed | 2 failing auth specs, pushed 3f2a1c |
| 4 | 2026-08-09 18:55 | repeat | seen ×3 — suppressed until 19:25 [7f3e...] |
| 5 | 2026-08-09 19:40 | held | new — wake budget of 12/h spent [90ab...] |
```

## Arming sequence

```
1. scripts/preflight.sh --probe '<cmd>' --skills '<list>'

2. scripts/arm.sh --slug <slug> --probe '<cmd>' --interval 120 \
     [--stop-when '<cmd>'] [--tick-cmd '<cmd>'] [--dry-stop 6] --dry-run

3. scripts/arm.sh … (without --dry-run)

4. Monitor({ command: "<the line arm.sh printed>",
             description: "loop <slug>", persistent: true })
```

There is no step 5. No cron to schedule, no heartbeat to arm, no renewal
reminder, no settings change — the watcher has no expiry and nothing outside the
session to clean up.

## The detached tick

For work that does not need the conversation, this is the cheapest shape there
is: the change dispatches a fresh `claude -p` and the session is never woken.

```bash
scripts/arm.sh --slug docs-drift --interval 600 \
  --probe 'git log --oneline -20 -- src/api | cut -c1-9' \
  --tick-cmd 'claude -p "src/api changed. Update docs/api.md to match, commit as docs: sync." --model claude-sonnet-5'
```

Output goes to `.claude/loops/<slug>.tick.log`. Read it before trusting a run of
these: a detached tick that fails fails quietly, which is the trade for not
paying the prefix.

## When composing with the built-in `/loop`

`.claude/loop.md` is the rendered active file for a bare `/loop`. Plain Markdown,
no required structure, capped at 25,000 bytes — `write-brief.sh` renders and
size-checks it.

```markdown
Work the release/next branch, one tick at a time.

Read the delta in the wake first; re-run the probe only if you need the rest:
  gh pr checks 412 --json name,bucket --jq '.[]|"\(.name) \(.bucket)"' | sort

If CI is red, pull the failing job log, diagnose, and push a minimal fix. If new
review comments have arrived, address each and resolve the thread. If everything
is green and quiet, say so in one line and do nothing else.

Append one ledger row each tick:
  .claude/scripts/tick.sh release-next "<green|fixed|blocked>" "<one line>"

Stop when the PR is merged. Full protocol: docs/loops/loop-release-next.md
```

Keep it short. Detail belongs in the source-of-record file the tick reads.
