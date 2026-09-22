# How the harness works

Ground truth for every claim in `SKILL.md`. Sources: the Claude Code binary
(`~/.local/share/claude/versions/2.1.229` and `2.1.247`, extracted strings),
<https://code.claude.com/docs/en/hooks.md>, and
<https://code.claude.com/docs/en/goal.md> for the built-in this skill replaces.

## The mechanism in one paragraph

`install.sh` registers `guard.sh` once, at user scope in `~/.claude/settings.json`,
as a **command** hook on `Stop`, `StopFailure` and `SessionEnd`, plus `sentinel.sh`
on `SessionStart`. `arm.sh` writes `.claude/goals/<slug>.json` and nothing else.
At the end of every turn Claude Code runs `guard.sh`, which reads the state file,
runs each gate's shell command, and either allows the stop or answers
`{"decision":"block","reason":…}` — feeding the reason back as the run's next
instruction. In parallel, `watch.sh` runs under `Monitor` and emits a line only
when the run's liveness changes. The guard sees the end of every turn, the
watcher sees the turns that never end, and the sentinel sees the runs whose
session is already gone.

## Hook configuration is snapshotted at process start

A hook registration written into any settings file while a session is running is
stored correctly and is not loaded by that session. It loads when the user opens
`/hooks` or restarts. This holds whether or not the file already existed.

Measured on 2.1.260, session `bf0a6e61`, 2026-09-22: every `stop_hook_summary`
record from 12 Sep 06:11Z to 22 Sep 02:56Z — 948 consecutive turns — lists the
same three Stop hooks, and `guard.sh` is not among them, while
`.claude/settings.local.json` was rewritten by `arm.sh` and `disarm.sh` four times
in that window (20 Sep 10:10Z, 21 Sep 13:40Z twice, 21 Sep 13:40Z) and carried the
guard in three of the four. `settings_preexisted` was `true` throughout. The
earlier reading — that only a `.claude/` with no settings file at session start
fails to load — came from the `update-config` skill bundled in the 2.1.247 binary:

> the settings watcher isn't watching `.claude/` — it only watches directories
> that had a settings file when this session started. The hook is written
> correctly. Tell the user to open `/hooks` once (reloads config) or restart —
> you can't do this yourself; `/hooks` is a user UI menu and opening it ends this
> turn.

That describes a narrower case than the one measured, and `arm.sh` ≤2.2.x printed
"should load live" from it. The run then built its own verifier
(`goal-verify-loop.sh`, one ledger row every ten minutes) and sat idle for twelve
hours behind seventy-seven identical rows.

Two consequences shape the harness now:

- **Register once, at user scope, and arm by writing state.** The guard exits in
  milliseconds in any session that has nothing armed, so it is safe everywhere,
  and a registration that was in the snapshot at startup is loaded for every
  later session. `arm.sh` runs `install.sh` when no registration exists.
- **Read load state from a heartbeat, never from the settings files.** `guard.sh`
  writes `~/.claude/better-goal/live/<session_id>.json` on every event it
  receives, before it looks for a goals directory, and `sentinel.sh` writes the
  same file at `SessionStart` with the list of settings files that carried the
  guard at that moment. `arm.sh`, `preflight.sh` and `install.sh` read the file
  for the current `CLAUDE_CODE_SESSION_ID`. A `Stop` heartbeat proves the guard
  fired; a `SessionStart` heartbeat with a non-empty list proves the guard was in
  the same snapshot as the sentinel. No heartbeat means not loaded, whatever the
  files say. The state records `hook_live` and `hook_evidence` (`guard`,
  `sentinel` or `none`).

`Stop` fires outside the turn, so the in-turn proof the `update-config` skill
prescribes for `PreToolUse`/`PostToolUse` hooks does not exist here; the
`SessionStart` heartbeat is what makes the answer available inside the arming
turn at all.

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

## Liveness comes from the guard's stamp and the transcript

Two signals, and the ledger's mtime is deliberately not one of them. `guard.sh`
writes `last_guard_at` into the state file on every `Stop` it handles for an
armed slug, so "when did the guard last run" is answered by the guard. A
session's transcript at `$CLAUDE_CONFIG_DIR/projects/*/<session_id>.jsonl` is
appended to as the turn runs; measured on a live session, its mtime was 6 seconds
old mid-turn. Together they separate a long turn from a dead run.

The ledger's mtime was the earlier signal, and it is what a substitute verifier
defeats: a loop appending a row every ten minutes keeps the ledger permanently
fresh, so the 2.2.x watcher read `QUIET` under its threshold for twelve idle hours
and never emitted `STALL`. `watch.sh` now emits `FOREIGN` once when the ledger
moves while the guard has never run.

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
separate. `install.sh` writes to `~/.claude/settings.json` — user scope — so the
guard is in every session's startup snapshot and arming never has to touch hook
configuration again. The state file that makes it act is per-repo, per-slug and
gitignored, so an armed run never leaks into a teammate's checkout. `disarm.sh`
leaves the registration in place (inert without armed state) and strips any
per-project copy that 2.2.x left in `.claude/settings.local.json`, so the next
session does not run every gate twice; `disarm.sh --uninstall` or
`install.sh --remove` takes the user-scope registration out.

## Resume behaviour

The state file and ledger survive `/clear`, `--resume` and a lost session; the
guard picks up where the ledger left off. What does not survive is the session
id: after a resume the hook payload carries a new one and the guard goes inert.
Re-arm with `arm.sh` from the resumed session, which rewrites `session_id` and
keeps the ledger intact. The resumed session's `SessionStart` wrote a fresh
heartbeat, so `arm.sh` can say in the same turn whether the guard is loaded.

## Non-interactive

`claude -p` runs a turn to completion in one invocation with no accumulated
prefix to re-bill, which makes it the cheap way to run a check that does not need
the session's context. The guard and watcher work the same way there; with
default text output nothing prints until the run ends, so add
`--output-format stream-json --verbose` when watching one.

## What `/goal` adds, and what it costs

`/goal <condition>` remains available and composes: `/goal /better-goal:better-goal <intent>`
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
