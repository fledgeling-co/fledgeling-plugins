<p align="center">
  <img src="assets/banner.png" alt="goal-harness: a porcelain icon of a bearing needle locked on a mark, held by a vermilion ratchet, beside the wordmark and the line: a goal that survives the night" width="100%" />
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> goal-harness</h1>

<p align="center"><strong>A goal that survives the night.</strong><br />
A hardening layer over Claude Code's built-in <code>/goal</code>, and the sibling of <a href="../loop-harness">loop-harness</a>.</p>

<p align="center">
  <img alt="Version 1.0.2" src="https://img.shields.io/badge/version-1.0.2-D33C21">
  <img alt="SWE skill: session control" src="https://img.shields.io/badge/SWE_skill-session_control-434A55">
  <img alt="Arms: a verified Stop guard" src="https://img.shields.io/badge/arms-verified_Stop_guard-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

`/goal` is thinner than it looks, and the gap between what it appears to do and what it does is where long runs die.

Setting a goal registers **one session-scoped prompt Stop hook** whose entire text is your condition, capped at **4,000 characters**. After every turn a small fast model (Haiku by default) reads the transcript and answers yes or no. That model runs no commands and opens no files. It judges what the run *said*, not what is true.

Then there's the part that actually ends the run. **Claude Code overrides any Stop hook after 8 consecutive blocks**, and it reports that turn as `completed`. Nine turns of real work is enough to trip it. Nothing in the transcript says the goal failed; the session just goes quiet. There's a second silent exit too: the evaluator can return an `impossible` verdict, which clears the goal outright.

And a goal changes no permissions. In the default permission mode an unallowed tool call sits there waiting, which from the outside looks identical to a model that gave up.

This skill was built from 114 real `/goal` invocations across 13 projects between June and August 2026. What people typed straight afterwards is the evidence:

> `resume` (six times in a row)
> "Has goal been met? if not, why have you stopped"
> "are you still working?"
> "Re-enforce your need to complete the goal, don't stop until it's met"

And `/goal /create-fleet-goal`, typed 13 times, which sets the condition to the literal string `/create-fleet-goal`. The run starts correctly, because the main model reads it as a directive. The evaluator is then asked every turn whether "`/create-fleet-goal`" has been satisfied, which it never can be.

## What it does

Six steps, in order, and it stops there. It doesn't start the work; the armed run does that.

| Step | What happens |
|---|---|
| **Grounds the condition** | Reads `ORCHESTRATOR.md`, `docs/features-to-triage/`, specs, plans, the ledger and open worktrees, so "all remaining work" becomes a list with a count |
| **Writes the brief** | `docs/goals/goal-<slug>.md`: the worklist with IDs, the gate commands, the blocked-item policy, the resource ledger, the concurrency cap, the stop conditions |
| **Composes the condition** | Under 4,000 characters (counted, not estimated), pointing at the brief, with a bound, a blocked-item policy, and a per-turn `GOAL-PROGRESS` line |
| **Preflights** | Six settings that end a goal without an error, listed below |
| **Shows the diff** | Every settings change printed before/after. `arm.sh --dry-run` writes nothing |
| **Arms the guard** | A session-gated command Stop hook that runs real verification commands each turn and appends to a ledger |

### The preflight

| Check | Why |
|---|---|
| Trust dialog, `disableAllHooks`, `allowManagedHooksOnly` | `/goal` is part of the hooks system; any of these and it refuses |
| Permission mode | A goal changes no permissions, so default mode stalls the run |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | Default 8, then override. `0` disables the cap entirely |
| Every skill named in the condition | A skill Claude may not invoke itself reaches a scheduled fire as **plain text** and never runs. `/verify` and `/code-review` are both in that set |
| Ports, processes, simulators | Two runs fighting over one simulator is a documented stall |
| Context headroom, worktree state | A goal armed at 90% context spends its run compacting |

### The guard

The interesting part. Each turn `goal-guard.sh` runs the gate commands from `.claude/goal-state.json`, appends a row to the ledger, and either lets the turn end or blocks with a **next-action brief**: the failing gate plus its output, the iteration count, the remaining budget, and the path to the brief. That reason text becomes the run's next instruction, so it's written as one.

Exit codes decide it, not narration. "All screens now match the mock" satisfies a Haiku reading a transcript. It does not satisfy `pnpm test`.

> [!IMPORTANT]
> The guard deliberately ignores `stop_hook_active`. Claude Code's own troubleshooting says a Stop hook should read that flag and exit early while it's true, and that advice is right for a hook needing one continuation; it's wrong for a goal, which needs many. Following it disarms the goal on its second turn. The run is bounded by `max_iterations` and a deadline in the state file instead, which is why raising the block cap isn't optional.

The state file records the **session id**, so the hook stays inert in every other session in the same project. Other work in the same repo carries on untouched.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install goal-harness@fledgeling-plugins
```

## Using it

Three ways in.

**On its own**, when you want a hardened run set up from scratch:

```text
/goal-harness divide the remaining work into md files in docs/features-to-triage
then use /ship-fleet:ship-fleet until all items are complete
```

**As a follow-up to the built-in**, which is the shape most people already type:

```text
/goal /goal-harness continue until every remaining item is shipped
```

It notices the live condition is a slash-command name, says so in a line, and replaces it with one that can actually be settled.

**After a goal has already misfired.** "Has the goal been met?", "why have you stopped?", "you stopped despite the goal being set". It reads the ledger and the state file rather than guessing from the transcript.

Once armed, `scripts/status.sh` answers "is it still going" from the ledger, and `scripts/disarm.sh` stops it.

## The rules that keep it honest

**A condition nothing can settle is a defect, not a constraint.** If neither a command nor the transcript could ever demonstrate it, it gets rewritten before arming. Arming something the evaluator will call `impossible` is worse than not arming at all.

**Never arm past a failed preflight.** A goal that stalls on a permission prompt at 3am looks exactly like a goal that finished.

**Every run is bounded.** Iterations and a deadline, both in the state file, so the run ends on your terms rather than on the block cap's.

**The ledger is the answer.** Progress is read from a file, never inferred from a transcript that compaction may have eaten.

## What's in the box

```text
skills/goal-harness/
  SKILL.md
  references/
    mechanics.md         how /goal actually works, with the binary and doc citations
    failure-modes.md     twelve observed failures, each mapped to its fix
    condition-craft.md   writing the <=4,000-character condition, with a worked example
    presets.md           the two recipes people type most often, and the originals
    templates.md         the brief, the state file, the ledger, the settings block
  scripts/
    preflight.sh         the six checks; read-only, exits 1 if anything blocks
    arm.sh               writes state and registers the guard; --dry-run shows the diff
    goal-guard.sh        the Stop hook; runs the gates, writes the ledger, blocks or allows
    status.sh            reads the ledger
    disarm.sh            stops the guard; --remove also unregisters the hook
evals/evals.json         six cases plus the process evals
EVALS.md                 the measured result against the no-skill baseline
```

## Does it earn its place

Measured, not asserted: each case run twice from an identical fixture, once with
the skill and once with nothing loaded, graded by an independent agent that saw
each response alone with no arm label.

Across both harness skills, **32 of 33 structural assertions against the
baseline's 12**, and the grader preferred the skill arm in **8 cases out of 8**.

Two results worth reading before you trust that number. On the `/code-review`
case the baseline scored the same 3/3: a capable model with the docs finds that
trap on its own, and the skill's headline claim is not what separates them
there. And the arming case is confounded, because the fixture is deliberately
thin and both arms spend real effort discovering it.

The run also found three defects in these skills, including a deadline parsed as
local time that disarmed a goal ten hours early on AEST. All three are fixed;
the scores were produced before the fixes. [EVALS.md](EVALS.md) carries the
per-case table, the ties, and what was not measured.

## What it doesn't do

**It can't verify a judgment with a command.** "The portal feels like an extension of the brand" has no exit code. The skill says so plainly rather than pretending, derives a measurable proxy where one exists, and offers an experimental agent-type gate (which gets tools and can open the artifact) as a supplement. It's never a replacement for someone looking.

**It doesn't survive `/clear`.** A new conversation drops the session goal. The guard's state file and ledger persist on disk, so a resumed session can be re-armed against the same brief, but the turn count and timer reset.

**It doesn't make the work correct.** It makes stopping honest. A run with weak gates will pass weak gates.
