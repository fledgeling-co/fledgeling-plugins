---
name: better-goal
description: Hold a long autonomous run to a finish line using a Stop guard and a stall watcher this skill creates itself, with no dependence on the /goal command. Use when someone wants a run that keeps going until the work is actually done — "set a goal to ship the rest of the backlog", "keep going until every item is complete", "harden this goal", "make a goal for this" — and when a run has already misfired: "has the goal been met?", "why have you stopped?", "you stopped despite the goal being set", "are you still working?". Also use as a follow-up to the built-in command (`/goal /better-goal <intent>`, formerly goal-harness). Grounds the finish line in the repo's real worklist, writes the brief to docs/goals/goal-<slug>.md, turns "done" into runnable gates, preflights the settings that silently kill a run, arms a per-slug command Stop hook that verifies by exit code rather than by narration, and arms an out-of-band watcher that notices a run dying mid-turn. Stops deliberately when a gate fails identically turn after turn, rather than re-sending the same failure. NOT for interval or polling work (use better-loop) or for a single task that finishes in one turn.
---

# better-goal — a finish line that verifies itself

A long run needs three things the model cannot supply about itself: something
that decides whether the work is done, something that notices when the run has
died, and a record that answers "how's it going" without interrupting it. This
skill builds all three out of a command Stop hook, a monitor, and a file.

It does not use `/goal`. That command registers a prompt Stop hook whose verdict
comes from a small model reading the transcript — so it is judged on what the
run *said*, it cannot run a command, and Claude Code overrides any Stop hook
after 8 consecutive blocks while reporting the turn as `completed`. The guard
here replaces the evaluator with exit codes and raises that cap deliberately.
`references/mechanics.md` carries the evidence for each of those claims.

Deliver the harness. The armed run does the underlying work, so do not start it
in this pass. Make routine judgment calls yourself and check in only where two
readings would produce materially different gates.

`references/failure-modes.md` maps each observed failure to its fix.
`references/gate-craft.md` is how to turn "done" into commands.
`references/presets.md` carries the two recipes people ask for most.

## Protocol

### 1. Read the situation before writing anything

Establish three things, cheaply:

- **What already remains.** `ORCHESTRATOR.md`, `docs/features-to-triage/`,
  `docs/specs/`, `docs/plans/`, `LEDGER.md`, open worktrees, `git status`. A
  finish line phrased "until all items are complete" that never names the items
  cannot be verified by anything, because there is no list to count against.
- **What "done" looks like as a command.** The test command, the typecheck, the
  empty-queue check, the review gate. This is the gate set, and it is the whole
  point of the design: a run that claims the work is finished and a run that
  finished it look identical in a transcript and differ in an exit code.
- **Whether something is already armed.** `scripts/status.sh` lists every armed
  slug in the repo. Runs are per-slug, so a second one is fine — but two runs
  driving the same branch are not, and that is worth naming.

If nothing can be run, say so plainly and fall back to an artifact check
(the file exists, is non-empty, contains the marker). Name the limitation rather
than arming a gate that passes on narration.

### 2. Write the brief to `docs/goals/goal-<slug>.md`

The brief is unbounded and is where detail belongs. Template and worked example:
`references/templates.md`. It carries the objective, the enumerated worklist with
IDs, the gate commands, the blocked-item policy, the resource ledger (simulators,
ports, dev servers, remote hosts), the concurrency cap, and the stop conditions.

Match its length to the run. A brief padded with restated context is re-read
every turn and buys nothing.

### 3. Turn "done" into gates

`references/gate-craft.md` is the craft guide. The state file's `verify[]` is an
ordered list of `{name, cmd, timeout}`; each is judged on exit code alone, in the
repo root, every turn.

- **Fast gates first.** They run on every turn, so a 20-minute suite belongs
  behind a cheap proxy with the full run as a final gate.
- **One gate, one question.** `tests` and `typecheck` as separate entries name
  the failure precisely; combined into one `&&` they do not.
- **Include a liveness gate** where a fleet, workflow or background runner is
  doing the delivery. Whether the work is done and whether the agents doing it
  are alive are independent facts, and only one of them used to be watched.

### 4. Preflight

`scripts/preflight.sh` checks the conditions that end a run without an error:

| Check | Why it matters |
|---|---|
| Hooks enabled; `disableAllHooks` / `allowManagedHooksOnly` unset | The guard is a hook. Without hooks there is no harness |
| Permission mode | Nothing here changes permissions; in default mode an unallowed tool call stalls the run until someone answers |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | Default 8 consecutive blocks, then Claude Code overrides the hook and ends the turn as `completed` |
| Every skill named in the brief | A skill Claude may not invoke on its own arrives at a scheduled fire as plain text |
| Resource contention | Simulators, metro instances, ports, remote hosts — an evidenced stall cause |
| Context headroom and worktree state | A run armed at 90% context spends its turns compacting |

Report what failed and what you propose. Do not proceed past a failure silently.

### 5. Apply config, showing the diff first

`scripts/arm.sh --dry-run` prints the exact before/after for every file it would
touch and writes nothing. Run it, show it, apply on the user's OK. Settings are
load-bearing across every session in scope, so a change made here is felt outside
this run.

### 6. Arm the guard

`scripts/arm.sh --state <file>` writes `.claude/goals/<slug>.json` (armed flag,
session id, iteration counter, deadline, gates, ledger path, stuck bound) and
registers `scripts/guard.sh` once as a `command` Stop hook.

Two properties make this safe to leave running:

- **Session-gated.** The hook fires in every session in the project and exits 0
  immediately unless the session id matches. Other sessions are untouched.
- **Per-slug.** State lives at `.claude/goals/<slug>.json`, so two runs in one
  repo — a worktree and its parent, two features in flight — do not overwrite
  each other's gates. The guard evaluates only the slugs armed by its own
  session.

Each turn the guard runs the gates, appends a ledger row, and either lets the
turn end or blocks with a **next-action brief**. That reason text becomes the
run's next instruction, so write the brief as an instruction to act.

**Status is not an action.** The most common shape of a dead-but-armed run is a
turn that reads the state, says "the fleet is still running", and ends — which
verifies nothing, advances nothing, and spends a block against the cap. So the
brief names the next concrete action: merge the branch that is ready, refill the
free slot, correct the drifted row, resume the stalled runner. "Nothing to do" is
a conclusion the guard reaches from its own exit codes, never one the run asserts.

### 7. Arm the stall watcher

The Stop guard only fires at the *end of a turn*. A run that dies mid-turn — a
usage limit, a crashed delivery agent, a lost session, a workflow whose agents
all failed — never reaches a Stop event, so the guard never runs, the ledger
stops growing, and the run looks armed for as long as nobody looks. The guard
cannot close that gap, because the guard is inside the thing that died.

Arm something outside it. `scripts/watch.sh <slug>` is built for this: run it
under `Monitor` with `persistent: true` and it emits a line **only on a
transition** — the ledger going stale past its threshold, the gate set changing,
every gate going green, or the state file disarming. A healthy run produces no
output at all, so every line it emits is one worth waking for.

```
Monitor({ command: "<plugin>/scripts/watch.sh ship-remaining-work",
          description: "goal ship-remaining-work liveness",
          persistent: true })
```

Prefer this to a cron heartbeat. A cron wakes the run on a clock whether or not
anything changed, and each wake re-bills the whole session prefix; the watcher
wakes it only when the situation is different from the last time it woke.
Where the work genuinely has to survive the session closing, say so and use
`CronCreate` at 20–40 minutes on an off-round minute, and tell the user it
expires after seven days.

### 8. Report what is watching

Close with one block, not a narrative: the slug and its finish line, the gates
the guard runs each turn, the bounds (iterations, deadline, stuck limit), the
watcher and what wakes it, where the ledger is, how to read status
(`scripts/status.sh`), and how to stop early (`scripts/disarm.sh <slug>`, which
removes the hook, the watcher entry and the raised block cap together).

## Stop when the failure stops changing

A gate that fails identically turn after turn is not progress being made slowly;
it is a run that has already learned everything this turn can teach it. Blocking
on it again re-sends the same failing output, re-pays the whole session prefix,
and produces the same turn.

The guard fingerprints the failing gate set and its output each turn. When the
fingerprint repeats `stuck_after` times (default 3), it blocks **once** with an
escalation brief — change approach, park the item, or fix the gate itself — and
if the next turn produces the same fingerprint again it disarms with
`end_reason: "stuck"` and records why. The run ends deliberately, with a ledger
that names the wall it hit.

Set `stuck_after` higher for a gate that legitimately takes several turns to move
(a long migration, a flaky suite being stabilised) and lower for one that should
flip on the first correct fix.

## Delegation

This skill runs in-session. Spawn a subagent only to survey a backlog too large
to read directly — one agent, not several — and not to review the brief or check
the gates. The guard is the verifier.

**If this skill is itself running in a subagent**, the session id it can see is
the subagent's, not the driving session's, and `Monitor` armed there dies with
the subagent's thread. Write the brief and the state file, run preflight, leave
`session_id` empty, and hand back the one-line `jq` command that stamps the real
id plus the `Monitor` call. Say plainly that nothing is armed yet.

## Operating rules

- **A finish line nothing can settle is a defect.** Rewrite it before arming
  rather than arming a gate that passes whenever the run says it should.
- **Never arm past a failed preflight.** A run that stalls on a permission prompt
  at 3am looks exactly like a run that finished.
- **Bound every run.** Iterations, a deadline and a stuck limit, all in the state
  file, so it ends on your terms rather than on the block cap's.
- **The ledger is the answer.** When asked "is it still going", read the ledger.
  A ledger whose last row is an hour old answers the question too — that is a
  stalled run, not a quiet one.
- **`/goal` is optional and additive.** If someone wants the narrative indicator
  as well, print the condition line for them to paste; it judges the story while
  the guard judges the exit codes. Nothing in the harness depends on it.
