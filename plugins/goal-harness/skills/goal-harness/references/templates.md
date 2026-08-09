# Templates

## `docs/goals/goal-<slug>.md`

```markdown
# Goal: <one line, imperative>

- **slug:** <kebab-slug>
- **armed:** <YYYY-MM-DD HH:MM local>
- **project:** <repo path>
- **bound:** <N> turns / <deadline>
- **condition:** see `## Condition` below (also live in this session)

## Objective

<2–4 sentences: what finished looks like and why it matters. No restated context.>

## Worklist

| ID | Item | Gate | Status |
|---|---|---|---|
| F-001 | <what> | `<command that settles it>` | pending / in-progress / merged / parked |

Total: <n>. This table is the count the progress line reports against.

## Gates

Run every turn by the guard; the run should also run them before claiming done.

| Name | Command | Passes when |
|---|---|---|
| typecheck | `pnpm typecheck` | exit 0 |
| tests | `pnpm test -- --run` | exit 0 |
| queue-empty | `ls docs/features-to-triage/*.md 2>/dev/null \| wc -l` | prints 0 |

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

Stop and report when any of these holds:
- All gates pass and the worklist has no pending items.
- The turn or deadline bound is reached.
- <domain-specific: quota exhausted, host unavailable…>

## Open questions

<Appended during the run. Empty at arm time.>

## Condition

```text
<the ≤4000-character condition, verbatim>
```
```

## `.claude/goal-state.json`

Written by `arm.sh`, read by `goal-guard.sh` and `status.sh`.

```json
{
  "armed": true,
  "session_id": "<uuid of the session that armed it>",
  "cwd": "/Users/you/Dev/project",
  "slug": "ship-remaining-work",
  "goal_file": "docs/goals/goal-ship-remaining-work.md",
  "ledger": "docs/goals/goal-ship-remaining-work.ledger.md",
  "started_at": "2026-08-09T18:04:11Z",
  "iteration": 0,
  "max_iterations": 60,
  "deadline": "2026-08-10T09:00:00Z",
  "verify": [
    { "name": "typecheck", "cmd": "pnpm typecheck", "timeout": 300 },
    { "name": "tests", "cmd": "pnpm test -- --run", "timeout": 900 },
    { "name": "queue-empty", "cmd": "test \"$(ls docs/features-to-triage/*.md 2>/dev/null | wc -l)\" -eq 0", "timeout": 30 }
  ]
}
```

`verify[]` entries run in order, in the repo root, and are judged on exit code
alone. Keep each one fast enough to run every turn; a 20-minute suite belongs
behind a cheaper proxy check with the full run as a final gate.

## `docs/goals/goal-<slug>.ledger.md`

Appended by the guard, one row per turn. This is the answer to "how's it going".

```markdown
| turn | at | verdict | failing | note |
|---|---|---|---|---|
| 1 | 18:07:22 | block | tests | 3 failing in auth.spec.ts |
| 2 | 18:19:04 | block | tests | 1 failing in auth.spec.ts |
| 3 | 18:31:41 | pass | — | all gates green; goal met, disarmed |
```

## Settings block

Written to `.claude/settings.local.json` by `arm.sh`. Shown as a diff first.

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
            "command": "${CLAUDE_PLUGIN_ROOT}/skills/goal-harness/scripts/goal-guard.sh",
            "timeout": 1200,
            "statusMessage": "goal-harness: verifying gates"
          }
        ]
      }
    ]
  }
}
```

The cap is set to a large number rather than `0` so the run still has a ceiling
if the state file is ever lost. The guard's own `max_iterations` is the bound
that should actually fire.

## Optional: an agent-type gate alongside

For a goal with a judgment component no command settles — "the portal looks like
an extension of the company's brand" — add a second Stop hook. It gets tools and
up to 50 turns, so it can open the artifact rather than read the narration.
Agent hooks are documented as experimental; treat this as a supplement to the
command gate, never a replacement.

```json
{
  "type": "agent",
  "prompt": "Read docs/goals/goal-<slug>.md, then verify the judgment gates in its `## Gates` table against the actual files and rendered output. Return ok:false with the specific gate and what is wrong if any fails. $ARGUMENTS",
  "timeout": 300,
  "model": "claude-sonnet-5"
}
```
