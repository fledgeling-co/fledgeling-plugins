# Scheduling

`scripts/install-agents.sh` writes five launchd agents and loads them:

```
~/Library/LaunchAgents/gg.rhodes.mac-doctor.<tier>.plist   tier ∈ 15m 1h 12h 1d 7d
```

```bash
scripts/install-agents.sh              # write + load all five
scripts/install-agents.sh --tiers 15m,1h
scripts/install-agents.sh --uninstall
scripts/install-agents.sh --status     # loaded?  last exit code?  last run?
```

## Why launchd rather than cron

`launchd` runs in the user's GUI session, survives reboot, restarts a missed run
after sleep, and reports exit status — none of which cron does on macOS.

Claude Code's own `CronCreate` is unsuitable here for three separate reasons: it
only fires while a REPL is idle, it dies with the session, and recurring jobs
auto-expire after seven days. The 12h/1d/7d tiers would essentially never fire.

## Intervals

`StartInterval` (seconds from load) for the short tiers, `StartCalendarInterval`
for the daily and weekly ones so they land at a predictable hour:

| Tier | Key | Value |
| --- | --- | --- |
| 15m | `StartInterval` | 900 |
| 1h | `StartInterval` | 3600 |
| 12h | `StartInterval` | 43200 |
| 1d | `StartCalendarInterval` | 03:17 |
| 7d | `StartCalendarInterval` | Sunday 04:23 |

The daily and weekly times are deliberately off the hour. Every scheduler
defaulting to `0 3 * * *` puts its load on the same minute, and a maintenance job
competing with every other maintenance job is slower for no reason.

A missed run (machine asleep) fires once on wake — launchd coalesces rather than
replaying every interval, so a laptop closed for a week gets one 15m tick, not
672.

## Model and no-model paths

The 15m and 1h agents run `scripts/survey.sh` and `scripts/reclaim.sh --tier N`
directly. No model, no API spend, no Claude session. That is deliberate: a job
firing 96 times a day should not cost tokens, and everything in those tiers is
deterministic enough not to need judgement.

The 12h, 1d and 7d agents invoke `claude -p` with the tier as the prompt, so the
judgement calls (is this dev server still wanted, does this worktree hold work)
get a model. Two environment traps make this fail silently under launchd:

- **`PATH` is minimal.** launchd does not source your shell profile, so `claude`,
  `docker`, `git`, `node` and `brew` are all absent unless the plist sets
  `EnvironmentVariables.PATH` explicitly. The installer writes the invoking
  shell's `PATH` into the plist.
- **No TTY.** `claude -p` is fine headless, but anything prompting for input
  hangs forever holding the agent slot. Every command in the shell path is
  non-interactive, and `reclaim.sh` never prompts — it writes a proposal file
  the next interactive session reads.

## Logs and verification

`StandardOutPath` / `StandardErrorPath` →
`~/.claude/mac-doctor/logs/<tier>.{out,err}.log`.

Check an agent is really firing:

```bash
launchctl list | grep mac-doctor          # PID, last exit code, label
launchctl print gui/$UID/gg.rhodes.mac-doctor.15m | grep -E 'state|runs|last exit'
tail -20 ~/.claude/mac-doctor/logs/15m.out.log
```

A nonzero last exit code with no log output almost always means `PATH` — the
binary was not found, so nothing ran and nothing was written.

Rotate the logs from the 1d tier; an unrotated 15m log is a maintenance tool
becoming a disk problem.

## Uninstalling

`--uninstall` runs `launchctl bootout` for each label and removes the plists. It
leaves `~/.claude/mac-doctor/` in place, since the ledger is the record of what
was reclaimed and is worth more than the agents.
