<p align="center">
  <img src="assets/banner.png" alt="mac-doctor: your Mac fills up a hundred reasonable decisions at a time" width="100%">
</p>

# mac-doctor

Your Mac didn't fill up because of one thing. It filled up because a hundred sensible defaults each left something behind, and nothing was counting.

Claude keeps every transcript. Dev servers leave build output. Docker holds volumes for containers you stopped weeks ago. Xcode keeps DerivedData for a project you haven't opened since March. Every one of those is the right default on its own. Together they took a terabyte off my machine, and I found out when a build died at 2am with `No space left on device`.

mac-doctor runs in the background, clears what it can prove is safe, and tells you about the rest instead of guessing.

## What it actually adds

Claude is already good at this. Ask it to clean up your disk and it'll do a careful job. I tested that properly and the numbers are in [EVALS.md](EVALS.md); the short of it is that the skill doesn't make Claude smarter about your disk, because it didn't need to be.

What it adds is that this happens **without you**, and **without tokens**.

The 15-minute and 1-hour checks are plain shell. No model, no API call, no session. About eight seconds, ninety-six times a day, for nothing. Asking Claude the same question costs a conversation and roughly 120k tokens each time, and only happens when you remember to ask.

## Five cadences, widening autonomy

What each run may do on its own widens as the gap between runs grows. A 15-minute job that deletes something irreplaceable is a disaster; a weekly suggestion you read first isn't.

| Every | What it handles | On its own? |
|---|---|---|
| 15 min | Dead processes, exited containers, finished-run temp files | Yes, quietly |
| 1 hour | Build output in repos nobody's working in | Yes, quietly |
| 12 hours | Package caches, dangling Docker images | Dry run, then yes |
| 1 day | Unused Docker volumes, dead simulators, CLI state | Dry run, then yes |
| 7 days | Worktrees, node_modules, transcripts, simulator runtimes | Asks you first |

**Running low doesn't unlock anything.** When the disk gets tight it runs the bigger jobs sooner and puts the pending suggestions in front of you. It doesn't start deleting things it would normally ask about; a nearly-full disk is exactly when a mistake is hardest to undo.

## It refuses more than it deletes

A git worktree holding unpushed commits looks exactly like an abandoned one. A dev server nobody's using looks exactly like the one you'll come back to in ten minutes. You can't tell which is which without checking.

So the interesting part isn't the deleting. It's the part that won't.

- **Build output** needs a generator that can still rebuild it. A folder called `dist` isn't regenerable because of its name.
- **Docker volumes** must be mounted by no container, and named volumes get reported rather than pruned. Somebody named that volume because they cared what was in it.
- **Worktrees** need four proofs: git still knows about them, nothing's uncommitted, no commit is missing from the main branch, and nothing's working in them. If git has forgotten one, it's judged on whether every file's content is reachable from a ref that survives the deletion.
- **Other people's repos** are never touched. An ownership list keeps a stray `rm -rf` out of your clone of somebody else's project.

## Install

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install mac-doctor@fledgeling-plugins
```

Then:

```text
/mac-doctor --setup     # install the five scheduled jobs
/mac-doctor             # run whichever one is due
/mac-doctor report      # measure everything, change nothing
/mac-doctor status      # what's scheduled, when it last ran
/mac-doctor worktrees   # audit worktrees only
```

`report` is the safe first move. It measures and explains without touching anything.

## What it found on my machine

A 2 TB Mac at 94% full:

| | |
|---|---|
| Git worktrees | 620 GB across 218 directories, the biggest single item |
| Xcode DerivedData | 43 GB |
| `~/Library/Caches` | 40 GB, with CocoaPods alone at 13 GB |
| Simulators | 19 GB |
| Agent CLI state | 25 GB across Claude, Codex, Cursor, Grok and Gemini |
| Package caches | 19 GB of npm and pnpm |

A real run freed **73 GB** and took the machine from 93% used to 89%: 52.2 GB from twelve verified worktrees, 11.3 GB of CocoaPods cache, 4.2 GB of build output across nineteen directories, 2.8 GB from pnpm and bun, and about 1.5 GB from Docker and brew.

It also declined a few things, which matters more. It left the Playwright cache alone because a test was running against it. It left 25 named Docker volumes alone. It skipped npm's cache because something was actively writing to it.

## Three ways it learned to distrust its own numbers

Each of these happened while I was building it. Each is now a rule in the code rather than a note in a document.

**`timeout` doesn't exist on macOS.** It's GNU coreutils. So `timeout 5 git worktree list | wc -l` on a clean Mac is "command not found"; empty output, exit 0 through the pipe, and `wc -l` says `0`. That reported 100 live worktrees as abandoned. If the gate had believed it, they'd be gone.

**A mean over a lopsided set is invented.** I sampled 24 worktrees ranging from 0.00 GB to 33.92 GB. The average multiplied out to more than the disk held.

**A measurement that timed out isn't a zero.** Two directories ran past their time limit, correctly returned "unknown", and a total that treated unknown as zero reported **77 GB for a 620 GB set**. It was convincing precisely because it was small, and because it contradicted an earlier guess.

The survey now reports `sizes_totalable`, false whenever anything was skipped or timed out. It would rather give you a count and admit it can't give you a total.

## Where things live

```
~/.claude/mac-doctor/
├── ledger.jsonl        one line per run: reclaimed, kept, suggested, deferred
├── findings/           a readable report per run
├── logs/               per-tier scheduler output
├── protected           paths to never touch, one per line
└── owners              git owners whose repos may be cleaned
```

The ledger records what it **kept** as carefully as what it removed. Something skipped thirty runs in a row while always idle is worth knowing about, and only the kept entries make that visible.

## Uninstalling

```text
/mac-doctor uninstall
```

That removes the scheduled jobs and leaves `~/.claude/mac-doctor/` where it is. The ledger is worth more than the automation.

Note: the scheduled jobs run under launchd, which doesn't read your shell profile. The installer copies your `PATH` into each job for that reason; if a run exits non-zero with an empty log, that's almost always what happened.

Found something it got wrong? Open an issue on the [marketplace repo](https://github.com/fledgeling-co/fledgeling-plugins). Every measurement bug above turned up by running it against a machine that genuinely had the problem, so real reports are the useful kind.
