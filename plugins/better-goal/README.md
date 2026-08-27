<p align="center">
  <img src="assets/banner.png" alt="better-goal: a porcelain icon of a bearing needle locked on a mark, held by a vermilion ratchet, beside the wordmark and the line: a goal that survives the night" width="100%">
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> better-goal</h1>

<p align="center"><strong>A goal that survives the night.</strong><br />
A run held to a finish line by gates it can actually fail, and the sibling of <a href="../better-loop">better-loop</a>.</p>

<p align="center">
  <img alt="Version 2.0.0" src="https://img.shields.io/badge/version-2.0.0-D33C21">
  <img alt="SWE skill: session control" src="https://img.shields.io/badge/SWE_skill-session_control-434A55">
  <img alt="Arms: its own Stop guard" src="https://img.shields.io/badge/arms-its_own_Stop_guard-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

A long run needs two things the conversation cannot give it: something that decides at the end of every turn whether the work is actually done, and something that notices when a turn stops ending at all. Claude Code ships `/goal`, which is neither.

Setting a goal registers **one session-scoped prompt Stop hook** whose entire text is your condition, capped at **4,000 characters**. After every turn a small fast model reads the transcript and answers yes or no. That model runs no commands and opens no files. It judges what the run *said*, not what is true, and "all screens now match the mock" reads as a pass.

Then there's the part that ends the run without saying so. **Claude Code overrides any Stop hook after 8 consecutive blocks**, and reports that turn as `completed`. Nine turns of real work is enough. There's a second silent exit: the evaluator can return an `impossible` verdict, which clears the goal outright. And a goal changes no permissions, so in the default permission mode an unallowed tool call sits waiting, which from outside looks exactly like a model that gave up.

This skill was built from 114 real `/goal` invocations across 13 projects between June and August 2026. What people typed straight afterwards is the evidence:

> `resume` (six times in a row)
> "Has goal been met? if not, why have you stopped"
> "are you still working?"
> "Re-enforce your need to complete the goal, don't stop until it's met"

And `/goal /create-fleet-goal`, typed 13 times, which sets the condition to the literal string `/create-fleet-goal`. The run starts correctly, because the main model reads it as a directive. The evaluator is then asked every turn whether "`/create-fleet-goal`" has been satisfied, which it never can be.

## What it does

It arms its own mechanism rather than borrowing one. Three pieces, all created here:

**A `command` Stop hook** (`guard.sh`), which runs your gate commands at the end of every turn and decides on exit codes. If they pass, the turn ends and the run is over. If they fail, it blocks with the failing gate, its output, the iteration count, the remaining budget and the path to the brief. That reason text becomes the run's next instruction, so it is written as one.

**The two events a Stop hook never sees.** `StopFailure` fires *instead of* `Stop` when an API error ends a turn, so a rate limit or a dropped connection used to leave the guard unasked; the same script is registered there and on `SessionEnd`, and each writes a ledger row and its own `end_reason` rather than leaving the run reading `armed: true`. That is not hypothetical: one run sat armed at turn 17 of 800 for fourteen days after `API Error: Connection refused`, and a second for six days after its session ended mid-turn.

**A stall watcher** (`watch.sh` under `Monitor`) plus **a sentinel** (`sentinel.sh` on `SessionStart`). The watcher covers a run wedged mid-turn on a permission prompt at 3am, which fires no event at all — but a `Monitor` dies with its session, so the sentinel reports whatever is still armed and cold to the next session that opens the repo. It is the only part of the harness that outlives the run.

Liveness comes from the session's own transcript rather than the ledger alone. Of 56 stall alerts measured across 14 real runs, 34 arrived within ten minutes of an assistant message: the watcher was waking a working session to ask whether it had died, at the price of the whole session prefix each time.

It stops at arming. It does not start the work; the armed run does that.

| Step | What happens |
|---|---|
| **Grounds the goal** | Reads `ORCHESTRATOR.md`, `docs/features-to-triage/`, specs, plans, the ledger and open worktrees, so "all remaining work" becomes a list with a count |
| **Writes the gates** | Every claim in the goal gets a command that exits non-zero when it is false. A claim with no such command is named as unverifiable rather than quietly accepted |
| **Writes the brief** | `docs/goals/goal-<slug>.md`: the worklist with IDs, the gate commands, the blocked-item policy, the resource ledger, the concurrency cap, the stop conditions |
| **Preflights** | The settings that end a run without an error, listed below |
| **Shows the diff** | Every settings change printed before/after. `arm.sh --dry-run` writes nothing |
| **Arms** | The guard on `Stop`, `StopFailure` and `SessionEnd`, the sentinel on `SessionStart`, then the watcher, then the ledger |
| **Proves the hook loaded** | Claude Code watches only a `.claude/` that already held a settings file at session start, so a hook armed into an empty one never fires. The state reads `hook_live: "unproven"` until the guard's first ledger row, and every surface reports that rather than assuming |

### The preflight

| Check | Why |
|---|---|
| Trust dialog, `disableAllHooks`, `allowManagedHooksOnly` | The guard is a hook; any of these and it never runs |
| A settings file already in `.claude/` | Claude Code watches only directories that held one at session start; without it the hook is written correctly and never fires |
| Permission mode | A goal changes no permissions, so default mode stalls the run |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | Default 8, then override. `arm.sh` raises it and records the prior value so `disarm.sh` can put it back |
| Every skill named in a gate reason | The model cannot invoke a `disable-model-invocation` skill from a guard reason. `/verify` and `/code-review` are both in that set |
| Ports, processes, simulators | Two runs fighting over one simulator is a documented stall |
| Armed runs already in this repo | Two runs sharing one state file was a real collision; state is per-slug now, and the preflight shows what is live |

### Stop when the failure stops changing

The defect that costs the most is not a run that stops early. It is a run that does not stop at all, re-sending the same six failing tasks turn after turn and re-paying the whole session prefix each time: 91% of the input in the heaviest sessions measured.

So the guard fingerprints the failing set. The first failure blocks with the full output. An identical second failure blocks with the output **withheld** (it is already in the context, verbatim, from last turn) and asks for a different approach instead. An identical third disarms the run and says why:

```text
better-goal: backlog: identical failure ×3, disarmed as stuck
```

The threshold is `stuck_after`, default 3. A run that is making progress never reaches it, because the fingerprint moves.

> [!IMPORTANT]
> The guard deliberately ignores `stop_hook_active`. Claude Code's own troubleshooting says a Stop hook should read that flag and exit early while it is true, and that advice is right for a hook needing one continuation; it is wrong for a goal, which needs many. Following it disarms the run on its second turn. The run is bounded by `max_iterations`, a deadline and the stuck-detector in the state file instead.

The state file records the **session id**, so the hook stays inert in every other session in the same project, and lives at `.claude/goals/<slug>.json`, so two runs in one repo do not collide.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install better-goal@fledgeling-plugins
```

## Using it

**On its own**, when you want a hardened run set up from scratch:

```text
/better-goal divide the remaining work into md files in docs/features-to-triage
then use /ship-fleet:ship-fleet until all items are complete
```

**After `/goal` has already misfired.** "Has the goal been met?", "why have you stopped?", "you stopped despite the goal being set". It reads the ledger and the state file rather than guessing from a transcript compaction may have eaten.

**Composed with the built-in**, if you want the evaluator's judgment as well as the gates:

```text
/goal /better-goal continue until every remaining item is shipped
```

It notices when the live condition is a slash-command name, says so in a line, and replaces it with one that can be settled. The guard is the mechanism either way; `/goal` is additive.

Once armed, `scripts/status.sh` answers "is it still going" from the ledger, and `scripts/disarm.sh` stops it.

## The rules that keep it honest

**A gate that cannot fail is not a gate.** If no command could ever demonstrate the claim, it is named as unverifiable up front rather than dressed as verified.

**Never arm past a failed preflight.** A run that stalls on a permission prompt at 3am looks exactly like a run that finished.

**Every run is bounded**: iterations, a deadline, and a repeat count, all in the state file, so it ends on your terms rather than on the block cap's.

**A wake carries new information or it does not happen.** Re-sending output already in the context is the expensive failure, not a safe default.

**The ledger is the answer.** Progress is read from a file, never inferred from a transcript.

## What's in the box

```text
skills/better-goal/
  SKILL.md
  references/
    mechanics.md      how the guard, the block cap and /goal actually work,
                      with the binary and doc citations
    failure-modes.md  eighteen observed failures, each mapped to its fix
    gate-craft.md     turning a claim into a command that exits non-zero
    presets.md        the two recipes people type most often
    templates.md      the brief, the state file, the ledger, the settings block
  scripts/
    preflight.sh      the checks; read-only, exits 1 if anything blocks
    arm.sh            writes per-slug state, registers the four hooks, raises the
                      block cap, prints the Monitor call; --dry-run shows the diff
    guard.sh          Stop: runs the gates, writes the ledger, blocks, escalates
                      on a repeat, disarms when stuck. StopFailure / SessionEnd:
                      records the endings a Stop hook never sees
    sentinel.sh       SessionStart: reports armed runs nobody is watching
    watch.sh          the stall watcher: NOTLIVE / STALL / RESUMED / DONE /
                      ENDED / GONE, with liveness read from the transcript
    status.sh         reads every armed run's state, ledger and hook_live
    disarm.sh         <slug> | --all; removes all four hooks, restores the cap
evals/evals.json      six cases plus the process evals
EVALS.md              the measured result against the no-skill baseline
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
the scores were produced before the fixes, and before the rebuild around
self-armed mechanisms. [EVALS.md](EVALS.md) carries the per-case table, the ties,
and what was not measured.

## What it doesn't do

**It can't verify a judgment with a command.** "The portal feels like an extension of the brand" has no exit code. The skill says so plainly rather than pretending, derives a measurable proxy where one exists, and offers an experimental agent-type gate (which gets tools and can open the artifact) as a supplement. It is never a replacement for someone looking.

**It doesn't survive `/clear`.** A new conversation drops the session. The state file and ledger persist on disk, so a resumed session can re-arm against the same brief, but the turn count and timer reset.

**It doesn't make the work correct.** It makes stopping honest. A run with weak gates will pass weak gates.
