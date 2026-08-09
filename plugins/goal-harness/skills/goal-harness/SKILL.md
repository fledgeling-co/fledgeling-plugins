---
name: goal-harness
description: Turn a rough intent into a hardened, armed /goal run that keeps going until the work is actually done. Use when someone wants a long autonomous run held to a finish line — "set a goal to ship the rest of the backlog", "create a goal prompt for this", "keep going until every item is complete", "make a <4k char goal", "harden this goal" — and when a goal has already misfired: "has the goal been met?", "why have you stopped?", "you stopped despite the goal being set", "re-enforce your need to complete the goal". Also use as a follow-up to the built-in command (`/goal /goal-harness <intent>`), where the active condition is a slash-command name that no evaluator can ever verify. Grounds the condition in the repo's real worklist, writes the brief to docs/goals/goal-<slug>.md, composes a transcript-verifiable condition under the 4,000-character limit, preflights the six settings that silently kill a goal, applies config after showing a diff, and arms a deterministic session-gated Stop guard with a progress ledger. NOT for interval or polling work (use loop-harness) or for a single well-scoped task that finishes in one turn.
---

# goal-harness — make a goal that survives the night

Claude Code's `/goal` is thinner than it looks. It registers one session-scoped
prompt Stop hook whose entire text is your condition, and after each turn a
small fast model reads the transcript and answers yes or no. It runs no
commands, opens no files, and **Claude Code overrides any Stop hook after 8
consecutive blocks**. A goal set for six hours of work stops on its own, with no
error, well before the work is done.

Your job is to close that gap: ground the condition in what actually remains,
write the long brief to a file, compose a short condition that transcript
evidence can settle, fix the settings that silently end the run, and arm a
guard that verifies by running commands rather than by reading narration.

Deliver that scope. Do not start doing the underlying work in this pass — the
armed run does the work. Make routine judgment calls yourself and check in only
where two readings would produce materially different goals.

`references/mechanics.md` is the ground truth for every claim above.
`references/failure-modes.md` maps each observed failure to its fix.
`references/presets.md` carries the two recipes people type most often.

## Protocol

### 1. Read the situation before writing anything

Establish three things, cheaply:

- **What already remains.** `ORCHESTRATOR.md`, `docs/features-to-triage/`,
  `docs/specs/`, `docs/plans/`, `LEDGER.md`, open worktrees, `git status`. A
  goal phrased "until all items are complete" that never names the items cannot
  be judged by anything — the evaluator has no list to check against, and
  neither will the guard.
- **Whether a goal is already active and what it says.** If this skill was
  reached via `/goal /goal-harness …`, the live condition is the literal string
  `/goal-harness …`. That is unverifiable by construction, and it is the single
  most common way a goal dies quietly. Say so in one line and replace it.
- **What "done" would look like as a command.** The test command, the typecheck,
  the empty-queue check, the review gate. If nothing can be run, say so plainly
  and fall back to a narration-checkable condition — but name the limitation.

### 2. Write the brief to `docs/goals/goal-<slug>.md`

The brief is unbounded and is where the detail belongs. Template and worked
example: `references/templates.md`. It carries the objective, the enumerated
worklist with IDs, the verification commands, the blocked-item policy, the
resource ledger (simulators, ports, dev servers, remote machines), the
concurrency cap, and the stop conditions.

Keep it to what the run needs. A brief padded with restated context costs
context on every read and buys nothing.

### 3. Compose the condition (≤4,000 characters)

Full craft guide: `references/condition-craft.md`. The shape that holds up:

- **One measurable end state**, not an aspiration.
- **The stated check** — the exact commands whose output must appear in the
  transcript. The evaluator only ever sees what the run surfaced.
- **A pointer** to the brief, so the run re-reads the worklist rather than
  drifting from memory.
- **A bound** — `or stop after N turns` / a wall-clock deadline. Without one a
  goal that cannot converge runs until the cap overrides it.
- **A per-turn progress line** the run must echo (`GOAL-PROGRESS: <slug> <done>/<total> …`).
  This is what makes "has the goal been met?" answerable from the transcript.
- **The blocked-item policy** — what to do instead of waiting for the user,
  because a goal does not pause for input and a run that stalls on a question
  burns turns against the cap.

Count the characters before proposing it. If it will not fit, move detail into
the brief and keep the pointer.

### 4. Preflight

`scripts/preflight.sh` checks the six conditions that end a goal without an
error, and prints what it found:

| Check | Why it matters |
|---|---|
| Workspace trusted; `disableAllHooks` / `allowManagedHooksOnly` unset | `/goal` refuses outright — it is part of the hooks system |
| Permission mode | A goal does not change permissions; in default mode every unallowed tool call stalls the run |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | Default 8 consecutive blocks, then override. `0` disables the cap |
| Every skill named in the condition | A skill Claude may not invoke on its own reaches a scheduled fire as plain text |
| Resource contention | Simulators, metro instances, ports, remote hosts — evidenced stall cause |
| Context headroom and worktree state | A goal armed at 90% context spends its run compacting |

Report what failed and what you propose. Do not silently proceed past a failure.

### 5. Apply config, showing the diff first

Compute the settings changes, print the exact before/after for each file, then
apply on the user's OK. `scripts/arm.sh --dry-run` prints the diff and writes
nothing. Back up each file it touches. Settings are load-bearing across every
session in scope, so a change made here is felt outside this run.

### 6. Arm the guard

`scripts/arm.sh` writes `.claude/goal-state.json` (armed flag, **session id**,
iteration counter, deadline, verification commands, ledger path) and registers
`scripts/goal-guard.sh` as a `command` Stop hook in `.claude/settings.local.json`.

The session id is what makes this safe: the hook fires in every session in the
project, and the guard exits 0 immediately unless the id matches the session
that armed it. Other sessions in the same repo are untouched.

Each turn the guard runs the verification commands, appends a row to the ledger,
and either lets the turn end (everything passed, or a bound was hit) or blocks
with a **next-action brief** — the failing check plus its output, the iteration
count, the remaining budget, and the pointer to the file. That reason text
becomes the run's next instruction, so write it as an instruction.

Then print the `/goal <condition>` line. Both paths can be armed at once; the
guard verifies by running commands, `/goal` judges the narrative, and the run
ends when both agree.

### 7. Report what is watching

Close with one block, not a narrative: the condition (or its first line and the
file path), what the guard checks each turn, the bounds, where the ledger is,
how to read status (`scripts/status.sh`), and how to stop early
(`scripts/disarm.sh`, or `/goal clear`).

## The rule that inverts the standard advice

Claude Code's own hooks troubleshooting says a Stop hook should read
`stop_hook_active` and exit early while it is true. That is correct for a hook
that needs one continuation and wrong for a goal, which needs many — following
it disarms the goal on its second turn. The guard deliberately ignores
`stop_hook_active` and bounds the run with its own iteration count and deadline
instead, which is why raising `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` is not optional.
Reasoning and the exact override message: `references/mechanics.md`.

## Delegation

This skill runs in-session. Spawn a subagent only to survey a backlog too large
to read directly — one agent, not several — and never to check the condition or
review the brief. The guard is the verifier.

## Operating rules

- **A condition nothing can settle is a defect.** If neither a command nor the
  transcript could ever demonstrate it, rewrite it before arming rather than
  arming something that will be judged `impossible` and cleared.
- **Never arm past a failed preflight.** A goal that stalls on a permission
  prompt at 3am looks identical to a goal that finished.
- **Bound every run.** Iterations and a deadline, both written into the state
  file, so the run ends on your terms rather than on the block cap's.
- **One armed goal per session.** Re-arming replaces the state file; say so.
- **The ledger is the answer.** When asked "is it still going", read the ledger
  rather than inferring from the transcript.
