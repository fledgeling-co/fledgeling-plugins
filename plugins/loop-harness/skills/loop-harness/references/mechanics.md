# How `/loop` actually works

Ground truth for `SKILL.md`. Sources: the Claude Code binary
(`~/.local/share/claude/versions/2.1.226`, extracted strings) and
<https://code.claude.com/docs/en/scheduled-tasks.md>.

## Three modes, chosen by what you type

| Input | Mode | What happens |
|---|---|---|
| `/loop 5m check the deploy` | fixed interval | Converts to cron, calls `CronCreate(recurring: true)`, runs the first tick immediately |
| `/loop check the deploy` | dynamic pacing | No cron. The run calls `ScheduleWakeup` at the end of each turn with its own delay |
| `/loop` or `/loop 15m` | built-in maintenance prompt, or `loop.md` if one exists | Same scheduling rules; the prompt comes from the file or the built-in default |

Parsing is positional and then trailing: a leading `^\d+[smhd]$` token is the
interval; otherwise a trailing `every <N><unit>` clause is; otherwise the whole
input is the prompt and the mode is dynamic. `check every PR` has no interval —
"every" not followed by a time expression is left alone.

## Hard limits

| Limit | Value | Source |
|---|---|---|
| `loop.md` size | **25,000 bytes**, then truncated with an inline warning | Binary constant `dIo=25000` |
| `loop.md` locations | `./.claude/loop.md`, then `~/.claude/loop.md` | Binary: `pIo(join(cwd,".claude","loop.md")) ?? pIo(join(claudeDir,"loop.md"))` |
| Recurring task lifetime | **7 days**, then one final fire and self-delete | Docs, "Seven-day expiry" |
| Scheduled tasks per session | 50 | Docs |
| Minimum interval | 1 minute (cron granularity) | Docs |
| Dynamic-pacing delay | clamped to 60–3600s | `ScheduleWakeup` tool contract |
| Fallback wakeup if a tick neither reschedules nor stops | ~20 minutes, once, then the loop ends | Docs; behaviour added in v2.1.202 |

## The v2.1.196 trap — skills that arrive as text

From the docs: *"As of v2.1.196, a scheduled fire only runs skills that Claude
is allowed to invoke on its own. The following reach Claude as plain text
instead of executing:"*

- built-in commands such as `/permissions`, `/model`, `/clear`
- skills marked `disable-model-invocation: true`, **including the bundled
  `/verify` and `/code-review`**
- skills withheld by a `skillOverrides` setting or a `Skill` deny rule
- MCP prompts such as `/mcp__github__list_prs`

There is no error. The run receives the text, reads it as a note, and continues.
A loop whose whole job was "run /code-review every hour" ticks correctly forever
and reviews nothing. `scripts/preflight.sh` resolves every named skill.

## Jitter

Fire times are deliberately offset so every session does not hit the API at the
same wall-clock moment. The offset is derived from the task ID, so it is stable
per task.

- Recurring: up to **30 minutes late**, or up to half the interval for anything
  more frequent than hourly. An hourly job set for `:00` may fire at `:29`.
- One-shot at the top or bottom of the hour: up to **90 seconds early**.
- Dynamic-pacing loops: jitter does not apply, but the seven-day expiry does.

If exact timing matters, pick a minute that is not `:00` or `:30` — `3 9 * * *`
rather than `0 9 * * *` — and the one-shot jitter does not apply.

## What ends a loop

| Cause | Recoverable? |
|---|---|
| `Esc` while it waits for the next tick | Yes — clears the pending wakeup only |
| `ScheduleWakeup {stop: true}` | Yes, restart with `/loop` |
| A dynamic tick that neither reschedules nor stops | One ~20-minute fallback fire, then the loop ends |
| Seven-day expiry | Fires once more, deletes itself. **No warning** |
| `/clear` or a new conversation | All session-scoped tasks die |
| Session exits / terminal closes | Ticks stop. Backgrounding the session carries them over |
| `CLAUDE_CODE_DISABLE_CRON=1` | `/loop` and the cron tools are unavailable entirely |

There is **no catch-up**. A task whose time passes while the run is mid-turn
fires once when the session goes idle, not once per missed interval.

## Session scope and resume

Tasks live in the current conversation. `--resume` / `--continue` restores
recurring tasks created within the last 7 days and one-shots whose time has not
passed. Background Bash and Monitor tasks are **never** restored on resume — a
loop whose wake signal was a Monitor comes back deaf, and the Monitor must be
re-armed.

Claude Code stores the list in the project's `.claude` directory. Scheduling
fails with an error when that directory, or `scheduled_tasks.json` inside it, is
a symlink. (Before v2.1.216 it wrote through the link instead.)

## Monitor vs cron

The docs say it directly: *"When you ask for a dynamic `/loop` schedule, Claude
may use the Monitor tool directly. Monitor runs a background script and streams
each output line back, which avoids polling altogether and is often more
token-efficient and responsive than re-running a prompt on an interval."*

Monitor's own contract adds the rule that decides whether a monitor is any good:
the filter must match every terminal state, because a monitor watching only for
the success marker is silent through a crashloop, and silence looks exactly like
still-running. When in doubt widen the alternation — noise is cheaper than a
missed failure.

Use Bash `run_in_background` instead when you want exactly one notification (a
build finishing); use Monitor when you want one per occurrence.

## The built-in maintenance prompt

A bare `/loop` with no `loop.md` runs a built-in prompt that, each tick:
continues unfinished work from the conversation; tends the current branch's PR
(review comments, failed CI, merge conflicts); then runs cleanup passes such as
bug hunts or simplification when nothing else is pending. It does not start new
initiatives, and irreversible actions proceed only where the transcript already
authorized them.

`loop.md` replaces that prompt entirely. It defines **one** default prompt for a
bare `/loop` — not a list of separate scheduled tasks — and is ignored whenever
a prompt is supplied on the command line. Edits take effect on the next tick, so
the protocol can be refined while the loop runs.

## Provider caveat

On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform and
Microsoft Foundry: `loop.md` is not read, a bare `/loop` prints usage instead of
running the maintenance prompt, and a prompt with no interval runs on a fixed
10-minute schedule rather than dynamic pacing.
