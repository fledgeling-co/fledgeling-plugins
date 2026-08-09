# mac-doctor

Your Mac did not fill up because of one thing. It filled up because a hundred
reasonable decisions each left something behind, and nobody was counting.

Agent CLIs keep transcripts. Dev servers leave build output. Docker keeps
volumes for containers you stopped weeks ago. Xcode keeps DerivedData for
projects you have not opened since March. Every one of those is the right
default in isolation. Together they take a terabyte, and you find out when a
build fails at 2am with `No space left on device`.

mac-doctor watches for that, cleans up what it can prove is safe, and tells you
about the rest instead of guessing.

## What makes it different from `rm -rf`

Most of the debris is **indistinguishable from live state without checking**. A
git worktree holding unpushed commits looks exactly like an abandoned one. A dev
server nobody is using looks exactly like one you will come back to in ten
minutes. So the interesting part of this tool is not the deleting — it is the
part that refuses to.

Every removal passes a gate first, and the gate is stricter the less
recoverable the mistake. Build output needs a generator that can rebuild it.
Docker volumes need to be unmounted by every container. Worktrees need three
separate proofs — unregistered with git, no uncommitted changes, and no commits
missing from the main branch — and if any one fails, you get told what it is
holding rather than losing it.

## Five cadences, widening autonomy

Runs as five scheduled jobs. What each is allowed to do on its own widens as the
gap between runs grows, because the cost of a wrong deletion does not scale with
how often you check. A 15-minute job that removes something irreplaceable is a
disaster; a weekly proposal you read first is not.

| Every | Does | On its own? |
| --- | --- | --- |
| 15 min | Dead processes, exited containers, finished-run temp files | Yes, silently |
| 1 hour | Build output in repos nobody is working in | Yes, silently |
| 12 hours | Package-manager caches, dangling Docker images | Dry-run, then yes |
| 1 day | Unused Docker volumes, dead simulators, CLI state rotation | Dry-run, then yes |
| 7 days | Worktrees, node_modules, transcripts, simulator runtimes | Asks you first |

The short tiers cost nothing to run — no model, no API calls, just shell. The
15-minute check completes in about eight seconds.

**Running low does not unlock anything.** When the disk gets tight it runs the
bigger jobs *sooner* and puts the pending proposals in front of you. It does not
start deleting things it would normally ask about, because a nearly-full disk is
exactly when a mistake is hardest to undo.

## Install

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install mac-doctor@fledgeling-plugins
```

Then:

```text
/mac-doctor --setup     # install the five scheduled jobs
/mac-doctor             # run whichever one is due
/mac-doctor report      # look at everything, change nothing
/mac-doctor status      # what is scheduled, when it last ran
/mac-doctor worktrees   # audit worktrees only
```

`report` is the safe first move. It measures and explains without touching
anything.

## What it found on the machine it was built for

A 2 TB Mac at 94% full:

| | |
| --- | --- |
| Git worktrees | 620 GB across 218 directories — the largest single item, and **none of it reclaimable**, because every one was live |
| Xcode DerivedData | 43 GB |
| `~/Library/Caches` | 40 GB (CocoaPods alone was 13 GB) |
| Simulators | 19 GB |
| Agent CLI state | 25 GB across Claude, Codex, Cursor, Grok, Gemini |
| Package caches | 19 GB of npm and pnpm |

The worktree line is the one worth reading twice. It is the biggest thing on the
disk and the tool will not delete any of it, because the check said it was all
in use. That is the tool working, not failing.

## Three ways it learned to distrust its own measurements

Every one of these happened while building it, and each is now a rule in the
code rather than a note in a doc.

**`timeout` does not exist on macOS.** It is GNU coreutils. So
`timeout 5 git worktree list | wc -l` on a clean Mac is "command not found" —
empty output, exit 0 through the pipe, and `wc -l` says `0`. That reported 100
live worktrees as abandoned. If the gate had trusted it, they would be gone.

**A mean over a lopsided set is invented.** Sampling 24 worktrees that ran from
0.00 GB to 33.92 GB gave an average that multiplied out to more than the disk
held.

**A measurement that timed out is not a zero.** Two directories exceeded their
time limit, correctly returned "unknown", and a total that treated unknown as
zero reported **77 GB for a 620 GB set**. It was believable precisely because it
was small and it contradicted an earlier guess.

So the survey now emits `sizes_totalable`, and it is false whenever anything was
skipped or timed out. The tool would rather give you a count and admit it cannot
give you a total.

## Where things go

```
~/.claude/mac-doctor/
├── ledger.jsonl        one line per run: reclaimed, kept, proposed, deferred
├── findings/           readable report per run
├── logs/               per-tier scheduler output
├── protected           paths to never touch, one glob per line
└── owners              git owners whose repos may be cleaned
```

The ledger records what it **kept** as carefully as what it removed. Something
skipped thirty runs in a row while always idle is itself worth knowing, and only
the kept entries make that visible.

`owners` is why it will not touch your clone of somebody else's project. A stray
`rm -rf` inside a third-party checkout is indistinguishable from vandalism the
next time they pull.

## Uninstalling

```bash
/mac-doctor uninstall
```

Removes the scheduled jobs and leaves `~/.claude/mac-doctor/` alone, because the
ledger is worth more than the automation.
