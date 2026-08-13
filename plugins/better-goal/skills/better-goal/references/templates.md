# Templates

## `docs/goals/goal-<slug>.md`

The brief. The run re-reads it every turn, so it — not the transcript — is the
run's memory.

```markdown
# Goal: <one line, imperative>

- **slug:** <kebab-slug>
- **armed:** <YYYY-MM-DD HH:MM local>
- **project:** <repo path>
- **bound:** <N> turns / <deadline> / stuck after <N> identical failures

## Objective

<2–4 sentences: what finished looks like and why it matters. No restated context.>

## Worklist

| ID | Item | Gate | Status |
|---|---|---|---|
| F-001 | <what> | `<command that settles it>` | pending / in-progress / merged / parked |

Total: <n>.

## Gates

Run by the guard at the end of every turn. Exit 0 is the only thing that counts.

| Name | Command | Passes when |
|---|---|---|
| typecheck | `pnpm typecheck` | exit 0 |
| tests | `pnpm test -- --run` | exit 0 |
| queue-empty | `! ls docs/features-to-triage/*.md >/dev/null 2>&1` | no files left |

## Blocked-item policy

<What to do instead of asking. Where questions accumulate. What "parked" means.>

## Resources

| Resource | Reserved for this run | Conflicts with |
|---|---|---|
| iPhone 16 Pro simulator (18.2) | no — customer app holds it | use a second simulator |
| port 3000 | yes | stop other dev servers first |

## Delivery

- **Driver:** <skill or command, e.g. /ship-fleet:ship-fleet>
- **Model / effort:** claude-opus-5 / high
- **Concurrency cap:** <n>
- **If an agent dies:** <the resume path>

## Stop conditions

- All gates pass and the worklist has no pending items.
- The turn, deadline or stuck bound is reached.
- <domain-specific: quota exhausted, host unavailable…>

## Open questions

<Appended during the run. Empty at arm time.>
```

## `.claude/goals/<slug>.json`

Written by `arm.sh`, read by `guard.sh`, `watch.sh` and `status.sh`. One file per
run, so two runs in a repo do not overwrite each other's gates.

```json
{
  "slug": "ship-remaining-work",
  "armed": true,
  "session_id": "<uuid of the session that armed it>",
  "cwd": "/Users/you/Dev/project",
  "goal_file": "docs/goals/goal-ship-remaining-work.md",
  "ledger": "docs/goals/goal-ship-remaining-work.ledger.md",
  "started_at": "2026-08-09T18:04:11Z",
  "iteration": 0,
  "max_iterations": 60,
  "deadline": "2026-08-10T09:00:00Z",
  "stuck_after": 3,
  "verify": [
    { "name": "typecheck", "cmd": "pnpm typecheck", "timeout": 300,
      "detail": "pnpm typecheck 2>&1 | tail -n 20" },
    { "name": "tests", "cmd": "pnpm test -- --run", "timeout": 900,
      "detail": "pnpm test -- --run 2>&1 | grep -E '✕|FAIL' | head -n 20" },
    { "name": "queue-empty", "cmd": "! ls docs/features-to-triage/*.md >/dev/null 2>&1", "timeout": 30,
      "detail": "ls -1 docs/features-to-triage/*.md | head -n 20" }
  ]
}
```

`arm.sh` adds `repeat_count`, `escalated`, `last_fingerprint`, `last_failing` and
`prior_block_cap`; the guard maintains them. `verify[]` entries run in order, in
the repo root, and are judged on exit code alone. `detail` runs only when `cmd`
fails and is withheld on a repeat.

The file is gitignored, and must stay so: its `verify[]` commands are executed by
a Stop hook.

## `docs/goals/goal-<slug>.ledger.md`

Appended by the guard, one row per turn. This is the answer to "how's it going",
and `status.sh` reads it so asking costs the run nothing.

```markdown
| turn | at | verdict | failing | note |
|---|---|---|---|---|
| 1 | 18:07:22 | block | tests | 3 failing in auth.spec.ts |
| 2 | 18:19:04 | block | tests | same failure ×2 — output withheld, escalated |
| 3 | 18:31:41 | block | typecheck | failing set moved: was [tests], now [typecheck] |
| 4 | 18:44:02 | pass | — | all gates green; met, disarmed |
```

## Settings block

Written to `.claude/settings.local.json` by `arm.sh`, shown as a diff before it
is applied, and removed by `disarm.sh` once no run in the repo is armed.

```json
{
  "env": {
    "CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "500"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/skills/better-goal/scripts/guard.sh",
            "timeout": 1200,
            "statusMessage": "better-goal: verifying gates"
          }
        ]
      }
    ]
  }
}
```

The cap is a large number rather than `0` so the run still has a ceiling if the
state file is ever lost. `max_iterations` is the bound that should actually fire.

## The watcher

Armed in the session, not in settings — there is nothing to clean up afterwards.

```
Monitor({
  command: "${CLAUDE_PLUGIN_ROOT}/skills/better-goal/scripts/watch.sh ship-remaining-work --stale 25",
  description: "goal ship-remaining-work liveness",
  persistent: true
})
```

It emits nothing while the run is healthy. Every line it does emit wakes the
session and re-bills its prefix, so the transitions are deliberately few: STALL,
RESUMED, DONE, ENDED, GONE. Raise `--stale` for work with long quiet stretches (a
full test matrix, a large build); lower it for work that should write a ledger row
every few minutes.

## Optional: an agent-type gate alongside

For a run with a judgment component no command settles — "the portal looks like
an extension of the company's brand" — add a second Stop hook. Agent hooks get
tools and up to 50 turns, so one can open the artifact rather than read the
narration. They are documented as experimental; treat this as a supplement to the
command gate, never a replacement.

```json
{
  "type": "agent",
  "prompt": "Read docs/goals/goal-<slug>.md, then verify the judgment gates in its `## Gates` table against the actual files and rendered output. Return ok:false with the specific gate and what is wrong if any fails. $ARGUMENTS",
  "timeout": 300,
  "model": "claude-sonnet-5"
}
```

## Optional: composing with `/goal`

Additive only. Keep the condition to one sentence and let the gates carry the
work.

```text
/goal Every gate in .claude/goals/<slug>.json passes and the guard has disarmed
itself with end_reason=met. Worklist: docs/goals/goal-<slug>.md
```
