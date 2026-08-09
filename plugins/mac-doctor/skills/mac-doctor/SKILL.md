---
name: mac-doctor
description: Diagnose and reclaim a macOS dev machine that agent CLIs, node/dev servers, Docker and Xcode have silently filled up or bogged down. Runs at five cadences (15m/1h/12h/1d/7d) with autonomy that widens as the cadence lengthens. Use whenever the user mentions low or full disk, "no space left on device", ENOSPC, EMFILE, memory pressure, swapping, a machine that is slow or hot, runaway CPU, a fan that will not stop, leftover dev servers or browsers, orphaned processes, stale git worktrees, Docker eating the disk, DerivedData, node_modules sprawl, or wants to "clean up", "free space", "see what's eating disk", or "check the machine". Also use before a large build, install, or model download when free space is uncertain, when a build fails for reasons that smell like resources rather than code, and to install or inspect the scheduled maintenance agents.
---

# mac-doctor

Keep a working macOS dev machine from being strangled by its own tooling. Agent
CLIs, node and dev servers, Docker, and Xcode each leave debris that is
individually reasonable and collectively fatal — this finds it, proves what is
safe to remove, removes that, and records the rest.

Two things make this skill rather than a shell alias. First, most of the debris
is **indistinguishable from live state without checking**: a worktree with
unpushed commits looks exactly like an abandoned one, a dev server with no
peers looks exactly like a forgotten one. Second, the disk fills through
**accumulation, not events** — nothing is ever obviously wrong, so nobody looks
until a build fails.

## Arguments

The invocation may carry an argument, which arrives as `ARGUMENTS: <text>` at
the end of this file. Match it case-insensitively against the table below,
ignoring any leading dashes — people type `--setup`, `setup` and `install`
interchangeably, and a maintenance tool that argues about punctuation is a
worse tool.

| Argument | Action |
| --- | --- |
| *(none)* | Run the longest-cadence tier that is currently overdue — see below |
| `15m` `1h` `12h` `1d` `7d` | Run that tier |
| `install` `setup` `schedule` `agents` | Install the launchd agents, then show status |
| `uninstall` `remove` `disable` | `scripts/install-agents.sh --uninstall` |
| `status` `agents?` `scheduled` | `scripts/install-agents.sh --status`, plus the last ledger entry per tier |
| `report` `check` `dry` `dry-run` | Survey and explain at `7d` depth; change nothing, whatever the thresholds say |
| `worktrees` | `scripts/worktree-audit.sh` only, with verdicts |
| anything else | Treat it as intent, not a token. "docker is eating my disk" is a `12h` scoped to Docker; say which tier you chose and why |

Two things the argument controls that are easy to drop:

- **Pass the tier to the scripts.** `scripts/survey.sh --tier <t>` and
  `scripts/reclaim.sh --tier <t>`. Both default to `15m`, so an unpassed tier
  silently skips the expensive measurements and produces a confident, empty
  answer — the failure mode this skill exists to avoid.
- **`reclaim.sh` is dry-run unless given `--apply`.** Add it only for the bands
  the tier's autonomy actually permits, and never in `report` mode.

**Choosing the overdue tier when no argument is given:** read last-run times
from `scripts/install-agents.sh --status` (or the log mtimes in
`~/.claude/mac-doctor/logs/`), and run the *longest* cadence whose interval has
elapsed, since longer tiers include the shorter ones' work. With no history at
all, run `1h` — it is the widest band that still acts unprompted, so a first run
is useful without being a surprise.

## Modes at a glance

```
/mac-doctor            # longest overdue tier
/mac-doctor 15m|1h|12h|1d|7d
/mac-doctor report     # measure and explain, change nothing
/mac-doctor --setup    # install the launchd agents
/mac-doctor status     # what is scheduled, when each last ran, what it reclaimed
/mac-doctor worktrees  # audit only
```

Run `scripts/survey.sh --tier <tier>` first in every mode. It measures disk, the
known reclaim targets, processes ranked by *sustained* CPU, orphan families,
listeners with peer counts, and Docker, and writes JSON to a path it prints.
Read that rather than issuing the individual `du`/`ps`/`lsof` calls — it is one
pass, and several of these measurements are expensive enough to matter.

Sizing is deliberately bounded, and the bound is tier-gated: a full sizing pass
measured 526s, so a 15m cadence running it would overlap itself and thrash the
disk it exists to protect. Before totalling any sizes, check `sizes_totalable`
in the survey output — it is false whenever a measurement timed out or was
skipped, and a total built from partial data is how a 620 GB set once got
reported as 77 GB.

## The autonomy gradient

Each tier may do everything the shorter tiers may do, plus its own band. The
gradient exists because the cost of a wrong deletion does not scale with how
often you check — a 15-minute job that removes something irreplaceable is a
disaster, while a weekly proposal you read first is not.

| Tier | Band | Autonomy |
| --- | --- | --- |
| **15m** | Dead processes, exited containers, finished-run temp dirs | Acts silently |
| **1h** | Build output in repos with no active session; leaked browser trees | Acts silently |
| **12h** | Package-manager caches, dangling Docker images and build cache | Dry-run, then acts |
| **1d** | Unused Docker volumes, unavailable simulators, agent-CLI cache rotation | Dry-run, then acts |
| **7d** | Worktrees, node_modules in dormant repos, transcripts, simulator runtimes, Docker.raw | Proposes, waits |

Per-tier target lists, thresholds and reclaim commands are in
[references/tiers.md](references/tiers.md).

**Urgency raises frequency, never permission.** When free space is critical the
correct response is to run the longer tiers *sooner* and surface their
proposals, not to let a short tier delete things it normally would not. A
machine at 2% free is exactly when a mistaken deletion is least recoverable, so
the gate does not soften under pressure. Say plainly that the reclaimable space
is sitting behind an approval, and what it is.

## The verification gate

Nothing is deleted that has not passed the gate for its class. State which
checks you ran. Full per-target rules:
[references/reclaim.md](references/reclaim.md).

- **Regenerable** — the artifact can be rebuilt by a command that already exists
  in the repo or tool (`dist/`, `.next/`, DerivedData, package caches). Cheap to
  be wrong about; still confirm the generator exists.
- **Unreferenced** — nothing points at it and nothing is using it: an exited
  container, a Docker volume no container mounts, an orphan process family with
  no established connections and negligible cumulative CPU.
- **Irreplaceable-if-wrong** — worktrees, anything under a repo that is not
  build output, transcripts. These need the three-gate check below and, at 7d,
  a human.

Worktrees reclaim only when **registered** in `git worktree list`, clean per
`git status --porcelain`, fully merged into the default branch, and with no
process holding them as a cwd.

Registration is what makes the other checks possible, not what makes a worktree
unsafe. A worktree git no longer knows about has a `.git` link pointing at a
deleted admin directory, so `status` and `log` both fail and `worktree repair`
cannot re-attach it: nothing can be proven, so nothing is done. Those are
reported `unverifiable` for a human. `scripts/worktree-audit.sh` prints a
per-worktree verdict.

Processes get the connection and idleness checks in
[references/processes.md](references/processes.md) — the CPU/memory/orphan lane,
absorbed from the former `process-hygiene` skill.

## What is never touched

Live connections, whatever their appearance. Root-owned system daemons — report
them with the command and let the user run it, since most need sudo and launchd
restarts them anyway. Running containers and the volumes they mount. Interactive
sessions (`S+` with a controlling TTY). The user's own browser, as opposed to
automation-spawned trees. Anything under a path the user has listed in
`~/.claude/mac-doctor/protected` (one glob per line).

`git worktree prune` deregisters worktrees without deleting their directories,
which is how a machine ends up with directories that `git worktree list` denies
exist. Treat "unregistered" as one signal of three, never as proof of
abandonment.

## Recording findings

Every run appends one record to `~/.claude/mac-doctor/ledger.jsonl` and writes a
readable report to `~/.claude/mac-doctor/findings/<timestamp>.md`. Schema and the
stable `id` rules are in [references/ledger.md](references/ledger.md).

Findings need consistent IDs or recurrence detection cannot work — the same leak
recorded two ways reads as two unrelated events. Record what was **kept** as
carefully as what was reclaimed: a target skipped across thirty runs while always
idle is itself a finding, and only the kept entries make that visible.

Record bytes reclaimed per target. Over weeks this is what tells you which
source is actually growing, as opposed to which one is merely large.

## Scheduling

`scripts/install-agents.sh` writes and loads five launchd agents under
`~/Library/LaunchAgents/gg.rhodes.mac-doctor.<tier>.plist`, logging to
`~/.claude/mac-doctor/logs/`. `--uninstall` removes them.

The 15m and 1h agents run the shell path only, which needs no model and no API
spend. The 12h, 1d and 7d agents can open a Claude session for the judgement
calls; see [references/scheduling.md](references/scheduling.md) for that wiring,
the `StartInterval` values, and how to check an agent is actually firing.

## Reporting

Lead with what changed: bytes reclaimed by target, free space before and after,
what was kept and why, and anything waiting on the user. Include the numbers —
"freed 38G, now 151Gi free (was 113Gi)" is the sentence someone wants.

Keep the report proportionate to what was found. A clean 15m tick is one line.
Do not pad a quiet run to look thorough; the point of a frequent tier is that it
is usually boring.

When a 7d proposal is ready, present it with `AskUserQuestion` — the reclaim
grouped by target with sizes, recommendation first — rather than as prose the
user has to reply to in sentences.

## Scope

Deliver the tier that was asked for. Investigate a cause when a finding recurs
across runs or the user asks; otherwise record the observation and move on
rather than opening a root-cause investigation inside a routine tick.

Do the survey and verification directly — it is a handful of tool calls and the
evidence needs to stay in one place. Delegate to at most one subagent, and only
to investigate a recurring cause across many repositories.
