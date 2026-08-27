# How the harness works

Ground truth for every claim in `SKILL.md`. Sources: the Claude Code binary
(`~/.local/share/claude/versions/2.1.229` and `2.1.247`, extracted strings),
<https://code.claude.com/docs/en/hooks.md>, and
<https://code.claude.com/docs/en/goal.md> for the built-in this skill replaces.

## The mechanism in one paragraph

`arm.sh` writes `.claude/goals/<slug>.json` and registers `guard.sh` as a
**command** hook on `Stop`, `StopFailure` and `SessionEnd`, plus `sentinel.sh` on
`SessionStart`, in `.claude/settings.local.json`. At the end of every turn Claude
Code runs `guard.sh`, which reads the state file, runs each gate's shell command,
and either allows the stop or answers `{"decision":"block","reason":…}` — feeding
the reason back as the run's next instruction. In parallel, `watch.sh` runs under
`Monitor` and emits a line only when the run's liveness changes. The guard sees
the end of every turn, the watcher sees the turns that never end, and the
sentinel sees the runs whose session is already gone.

## The hook may be written correctly and never load

Claude Code snapshots hook configuration and then watches for changes, but the
watcher **only watches directories that already held a settings file when the
session started**. The wording is Anthropic's own, from the `update-config` skill
bundled in the 2.1.247 binary:

> the settings watcher isn't watching `.claude/` — it only watches directories
> that had a settings file when this session started. The hook is written
> correctly. Tell the user to open `/hooks` once (reloads config) or restart —
> you can't do this yourself; `/hooks` is a user UI menu and opening it ends this
> turn.

So arming into a repo whose `.claude/` was empty at session start produces a run
that looks armed and verifies nothing. Observed on 2026-08-26: a run proved it
in-session by piping a payload to `guard.sh` by hand and getting the block
decision the harness had never produced on its own, then spent the rest of its
life running the gates manually.

The same skill notes that `Stop` fires outside the turn, so the in-turn proof it
prescribes for `PreToolUse`/`PostToolUse` hooks does not exist here. The proof is
the first ledger row instead: `arm.sh` writes `hook_live: "unproven"`, the guard
stamps `proven` on its first real firing, and `status.sh`, `watch.sh` and
`sentinel.sh` each report the unproven state rather than assuming it works.

`arm.sh` records `settings_preexisted` before it writes, because afterwards both
cases look identical.

## The events a Stop hook does not cover

| Event | Fires when | What the guard does |
|---|---|---|
| `Stop` | a turn ends normally | runs the gates, blocks or allows |
| `StopFailure` | *instead of* `Stop`, when an API error ended the turn | records the error; disarms as `api_error` on the third consecutive one |
| `SessionEnd` | the session is ending | disarms as `session_ended` |
| `SessionStart` | any session opens in the repo | `sentinel.sh` reports armed runs nobody is watching |

`StopFailure`'s own description in the binary: *"Fires instead of Stop when an
API error (rate limit, auth failure, etc.) ended the turn. Fire-and-forget —
hook output and exit codes are ignored."* Its matcher values include
`rate_limit`, `overloaded`, `authentication_failed`, `billing_error`,
`invalid_request` and `account_on_hold`. Because output is ignored it can record
but never instruct, which is why the disarm-on-third rule lives in the guard
rather than in a block reason.

`SIGKILL` reaches none of these, so the sentinel re-checks state at every session
start rather than trusting the events alone.

## Liveness comes from the transcript

A session's transcript at `$CLAUDE_CONFIG_DIR/projects/*/<session_id>.jsonl` is
appended to as the turn runs; measured on a live session, its mtime was 6 seconds
old mid-turn. That is the only liveness signal readable from outside the session,
and it separates a long turn from a dead run — which the ledger alone cannot do.

The cost of not having it: across 14 real runs, 56 `STALL` notifications were
delivered, 34 of them within ten minutes of an assistant message and 22 in the
same minute. Two turns in one run answered the alert with *"Watcher woke me — the
ledger went stale because my turn ended."* Each of those wakes re-bills the whole
session prefix.

The stale threshold is now derived from the run's own cadence — three times the
median of its last ten inter-row gaps, floored at 25 minutes and capped at 240 —
because a fixed 25 was shorter than the median turn length of several real runs
(28.5 minutes on one, 95.7 on another).

## Why the guard is a command hook

`/goal` registers a **prompt** hook. The three hook types are not equivalent:

| Type | Tools | Default timeout | Judge |
|---|---|---|---|
| `prompt` | none | 30s | small fast model (Haiku) |
| `agent` | Read, Grep, Glob, Bash… up to 50 turns | 60s | small fast model unless `model` set |
| `command` | whatever the script runs | script's own | none — the exit code is the verdict |

A prompt hook cannot run a command, so it judges the *transcript*: the binary
appends "Based on the conversation transcript above, has the following stopping
condition been satisfied? Answer based on transcript evidence only." A condition
about the filesystem is therefore judged by whether the run *said* something
about the filesystem. `guard.sh` runs `pnpm test` and reads the exit code.

Agent hooks are documented as experimental; the docs recommend command hooks for
production, which is what the guard is.

## The block cap — the main cause of "why have you stopped"

From the binary's turn loop:

```
let cap = age(process.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP, 8);
if (cap > 0 && consecutiveBlocks > cap) {
  → "A hook blocked the turn from ending N consecutive times — overriding and
     ending turn. For Stop/SubagentStop hooks, check stop_hook_active in the
     input and return success while it's true. Set
     CLAUDE_CODE_STOP_HOOK_BLOCK_CAP to raise this limit."
  → return { reason: "completed" }
}
```

Note `reason: "completed"`. The turn is reported as a normal completion; nothing
in the transcript says the run was cut short. This applies to **any** Stop hook,
the guard included — it is not a `/goal` quirk, which is why `arm.sh` raises the
cap and `preflight.sh` blocks when it is unset.

The counter is consecutive: it resets on any turn that ends without a block. A
run is fine for short bursts and reliably dies on long ones. Nine turns of real
work is enough.

`0` disables the cap. Prefer an explicit large number plus `max_iterations` and
`deadline`, so the run still has a ceiling it chose.

### Why the official advice is wrong here

The documented fix — read `stop_hook_active` and exit 0 while true — is written
for hooks that need a single continuation (run the formatter, then let the turn
end). Applied to a long run it means: block once, then allow the stop on every
subsequent turn. The run disarms itself on turn two. `guard.sh` ignores
`stop_hook_active` deliberately and bounds the run with `max_iterations`,
`deadline` and `stuck_after` instead.

## How a Monitor line reaches the session

`Monitor` runs a script in the session's shell and turns each stdout line into a
`<task-notification>`. In 2.1.229 that notification is delivered as a
`queued_command` with `commandMode === "task-notification"` — the same path a
scheduled task uses, so it genuinely wakes an idle session rather than merely
appending to a log. Claude Code's own PR-watcher uses this shape.

Two consequences:

- **Every emitted line costs a full turn's input.** Waking a session re-bills its
  accumulated prefix. `watch.sh` therefore emits only on a transition — NOTLIVE,
  STALL, RESUMED, DONE, ENDED, GONE. Emitting on a transition is not by itself
  enough: measured, 34 of 56 delivered STALLs were transitions of the ledger while
  the session was mid-turn, which is why liveness now comes from the transcript.
- **A filter matching only success is silent through a crash**, and silence is
  indistinguishable from still-running. The watcher's terminal states cover
  stuck, deadline and max_iterations as well as met.

`persistent: true` keeps the watcher alive for the session rather than the
default 5-minute timeout. It ends by itself when the run disarms; `TaskStop`
ends it early.

## Per-slug state

State lives at `.claude/goals/<slug>.json`, one file per run. A single
`.claude/goal-state.json` collides when two runs share a repo — a worktree and
its parent, or two features in flight — and the second arm silently replaces the
first one's gates. The guard iterates every file in the directory and evaluates
only those whose `session_id` matches the hook payload, so several runs coexist
and each stays inert in sessions that are not driving it. This isolation pattern
is taken from the official `ralph-loop` plugin's stop hook.

`goal-state.json` is still read for back-compatibility.

## Repeat suppression

The guard fingerprints the failing set — gate names plus the detail lines — and
counts consecutive turns with an identical fingerprint. On the second identical
turn the block reason escalates and **withholds the gate output**, because
re-sending output the run has already seen buys nothing and costs the whole
prefix. Past `stuck_after` (default 3) the guard disarms and records `stuck_on`,
rather than continuing to pay for a failure that has stopped changing.

When the failing set does change, the block reason carries the delta ("was
[a, b], now [b]") so the run can tell progress from churn without re-reading the
ledger.

## Hook input available on Stop

The Stop event delivers, among others: `hook_event_name`, `session_id`,
`stop_hook_active`, `last_assistant_message`, `background_tasks` and
`session_crons`. The guard uses `hook_event_name` to stay inert if registered on
another event, and `session_id` for the isolation above. It refuses to act on a
state file with an empty `session_id` — a run that never fires is a better
failure than one that fires in every session in the repo.

## Permissions are not part of arming

Arming changes no permissions. In the default permission mode Claude still asks
before tool calls the settings do not already allow, and an unattended run stops
at the first unallowed command and waits — mid-turn, where the guard cannot see
it. That is what the watcher's STALL is for. Pair with auto mode, or pre-allow
the commands the brief names.

## Settings locations and precedence

Hooks merge across levels rather than replacing each other. Identical handlers
defined in more than one settings file run once; a plugin's or skill's copy stays
separate. `arm.sh` writes to `.claude/settings.local.json` — project scope,
gitignored — so an armed run never leaks into a teammate's checkout. `disarm.sh`
removes the hook and restores whatever block cap was there before arming, once
no run in the repo is still armed.

## Resume behaviour

The state file and ledger survive `/clear`, `--resume` and a lost session; the
guard picks up where the ledger left off. What does not survive is the session
id: after a resume the hook payload carries a new one and the guard goes inert.
Re-arm with `arm.sh` from the resumed session, which rewrites `session_id` and
keeps the iteration count and ledger intact.

## Non-interactive

`claude -p` runs a turn to completion in one invocation with no accumulated
prefix to re-bill, which makes it the cheap way to run a check that does not need
the session's context. The guard and watcher work the same way there; with
default text output nothing prints until the run ends, so add
`--output-format stream-json --verbose` when watching one.

## What `/goal` adds, and what it costs

`/goal <condition>` remains available and composes: `/goal /better-goal <intent>`
starts the harness under a built-in goal. It is additive only — nothing here
depends on it — and it carries three limits worth knowing before relying on it.

| Limit | Value | Source |
|---|---|---|
| Condition length | 4,000 characters | Binary constant `e0r=4000`; docs |
| Goals per session | 1 | Docs: setting a new one replaces it |
| Evaluator tools | none | Docs: "it can only judge what Claude has already surfaced" |

The transcript it judges is truncated to a budget; when it overflows the binary
prepends *"N earlier messages omitted… if the required evidence may be in the
omitted prefix, return `{"ok": false, …}`"*, so evidence produced early in a long
run stops counting.

And there is a third verdict beside met and not-met. When the evaluator judges
the condition impossible, Claude Code logs `Hooks: Prompt hook condition judged
impossible:`, fires `tengu_goal_failed`, emits `goal_status {met: false, failed:
true}` and **clears the goal**. The run ends with no error and no completion.
That failure mode is the reason the guard is a command hook.
