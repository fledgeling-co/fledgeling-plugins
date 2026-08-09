# Reclaim rules

One section per target: how to measure it cheaply, what proves it safe, how to
reclaim it, and what it costs if the judgement is wrong.

The last column is the one that matters. "Regenerable" is not a property of a
directory name — `dist/` is regenerable only if something can still build it.

## Measuring without melting the disk

`du -sh` over a deep tree is expensive, and over many trees it is prohibitive.
Three cheaper approaches, in order of preference:

1. **Ask the tool.** `docker system df`, `xcrun simctl list`, `git worktree
   list`, `npm cache verify` all report their own footprint in milliseconds.
2. **Sample and multiply — only over a set you have shown to be uniform.**
   Size a handful of members, and check the spread before extrapolating. On the
   reference machine a 24-worktree stratified sample ran from 0.00 GB to 33.92
   GB; the mean was 3.26 GB, and multiplying it out produced per-repo totals
   exceeding the disk's used space. A mean over a skewed set is a fabricated
   number wearing a decimal point. When the max is more than ~5× the median,
   stop extrapolating and measure the aggregate parent instead — one `du` per
   worktree root is a handful of calls and is exact.
3. **Bounded `du`.** `du -sxk -d 0` behind a bound, treating the bound being hit
   as a measurement result ("larger than we will spend time proving") rather
   than an error.

Never block a 15m tier on a measurement that can take minutes.

### `timeout` does not exist on stock macOS

This is the trap that matters most in this file, because it fails *silently and
in the dangerous direction*.

`timeout` is GNU coreutils. A clean macOS has neither it nor `gtimeout`. So
`timeout 5 git worktree list` is "command not found" — empty stdout, and through
a pipe, exit 0. A caller writing:

```bash
registered=$(timeout 5 git -C "$repo" worktree list | tail -n +2 | wc -l)   # WRONG
```

gets `0` and reads it as "no worktrees are registered" when the truth is "the
command never ran". While gathering evidence for this skill, that exact line
reported 100 live, registered worktrees as abandoned — a number that would have
authorised deleting every one of them had the gate not caught it independently.

Use the `bounded()` helper in `scripts/worktree-audit.sh`, which prefers
`timeout`/`gtimeout` when present and otherwise backgrounds the command with a
killer subshell. Two rules generalise from this:

- **A bounding wrapper must fail closed.** If the bound cannot be applied,
  either run unbounded or report "not measured" — never return a value that is
  indistinguishable from a real zero.
- **Zero from a measurement is a claim, not a default.** Before acting on
  "found none", confirm the tool that found none actually executed.

The same applies to `realpath`, `sha256sum`, `sed -i`, and `date -d`, none of
which behave like their GNU namesakes here.

### A bound that fires is not a zero

The companion to the trap above, and the one that actually bit hardest while
building this skill.

`survey.sh` sizes each target behind a time bound. Two worktree roots (303 GB
and 239 GB) exceeded it, correctly returned `null`, and a consumer totalling
`size_kb or 0` reported **77 GB for a 620 GB set**. Nothing errored. The number
was small, plausible, and wrong by 543 GB — and it was used to *revise a
previous estimate downward*, which is the shape that makes this dangerous:
a partial measurement is most convincing when it contradicts something.

Three defences, all now in the scripts:

- `sz()` sets a global `INCOMPLETE` flag whenever a bound fires, and the survey
  emits `"measurement_incomplete": true` at the top level. Read it before
  totalling anything.
- Every sized entry carries `size_status` of `measured`, `timed_out` or
  `not_attempted`, so a null is never ambiguous about *why*.
- When totalling, report the count of unmeasured entries alongside the sum, or
  refuse to give a total at all. "77 GB across 15 of 17 roots, 2 unmeasured" is
  honest; "77 GB" is not.

The general rule: **absent is not zero.** It applies to a timed-out `du`, a
missing binary, an empty grep whose command never ran, and an API that returned
nothing because it was never called. Before reporting an aggregate, confirm
every input to it actually produced a value.

## Git worktrees

**Measure:** `git -C <repo> worktree list` for registration; `ls` the worktree
root for what is on disk. Size by sampling.

**Gate — all three, per worktree:**

```bash
git -C "$repo" worktree list --porcelain | grep -q "^worktree $wt$"   # registered?
git -C "$wt" status --porcelain                                        # empty?
git -C "$wt" log --oneline "$default_branch..HEAD"                     # empty?
```

Unregistered **and** clean **and** fully merged means abandoned. Any check
failing means it is reported with what it holds.

**Reclaim:** `git -C "$repo" worktree remove --force "$wt"`, falling back to
`rm -rf` only when the worktree is unregistered (git will refuse to remove what
it does not know about).

**If wrong:** unpushed commits or uncommitted work are destroyed, with no undo.
This is the highest-consequence target on the machine, which is why it is 7d and
gated three ways.

**Expect most worktrees to fail the gate, and treat that as the gate working.**
On the reference machine all 217 were registered and clean, so zero were
reclaimable — while totalling **620 GB**, making them by a wide margin the
largest single consumer on the disk and *not* something this skill removes. The
right output there is a review list, not a deletion proposal. A worktree audit
that frequently returns a large reclaim is more likely mis-measuring than
finding treasure.

## Docker

**Measure:** `docker system df` (and `-v` for per-volume). Never `du` the
container directory; `Docker.raw` is sparse, so its apparent size overstates
real usage — 56G apparent against 44G real here.

| Action | Gate | If wrong |
| --- | --- | --- |
| `container prune -f` | state is `exited`/`created` | a stopped container's writable layer; recreate it |
| `image prune -f` | dangling only — no `-a` | nothing; dangling images are unreferenced by definition |
| `builder prune -f` | none needed | slower next build |
| `volume prune -f` | no container mounts it, name not protected | **data loss** — a dev database whose container is merely stopped looks unused |
| `system prune -a` | do not | removes every image not currently running |

Report named volumes separately from anonymous ones. An anonymous volume is
almost always scratch; a named one was named because someone cared.

## Xcode

**DerivedData** (43G): per-project subdirectories. Gate on source mtime — 14
days untouched. Reclaim by removing the project's subdirectory. If wrong, a full
rebuild.

**CoreSimulator** (19G): `xcrun simctl delete unavailable` is safe — those
devices cannot boot. Deleting whole runtimes is a 7d proposal because it removes
the ability to test against that iOS version until re-downloaded.

**iOS DeviceSupport**: keep the versions of devices actually attached recently.

## Package-manager caches

`npm cache clean --force`, `pnpm store prune`, `bun pm cache rm`,
`yarn cache clean`, `uv cache prune`, `brew cleanup --prune=7`.

All refill from the network. Safe to prune unprompted at 12h; the only cost is a
slower next install. The exception is anything the user builds offline or over a
metered connection — CocoaPods at 13G refills slowly enough to be a proposal.

## Build output in repos

**Gate:** repo has no file modified in 7 days, no running process has it as cwd
(`lsof -a -d cwd`), and a generator exists — a `build` script in `package.json`,
a `Makefile` target, a `Cargo.toml`. Without a generator it is not regenerable,
whatever it is called.

`node_modules` is deliberately *not* in the 1h tier despite being regenerable:
reinstalling is slow, sometimes network-dependent, and occasionally fails on a
lockfile that has drifted. It is a 7d proposal with the reinstall command.

## Agent-CLI state

`~/.claude` 16G, `~/.codex` 5.6G, `~/.cursor` 3.3G, plus `~/.grok`, `~/.gemini`.

Rotatable by age: `shell-snapshots`, `paste-cache`, `file-history`, `security`,
`logs`, `telemetry`, and the equivalents under the other CLIs.

**Session transcripts are not cache.** 13G across 23,214 `.jsonl` files here,
and they are the only record of what was done and why — this skill's own design
was mined from them. Archive to a compressed tarball, never delete, and only as
a 7d proposal.

Plugin caches (`~/.claude/plugins`, 2.4G) refetch from their marketplaces;
prunable once confirmed the marketplace is reachable.

## Processes

See [processes.md](processes.md) for the full lane — the connection and
idleness gate, orphan families, sustained-CPU ranking, and the fd-holder
mechanism that strands stdio children.

## Things that look reclaimable and are not

- **APFS local snapshots.** `tmutil listlocalsnapshots /` often shows
  `com.apple.os.update-*` entries. Those belong to the OS updater and are not
  yours to thin. Real Time Machine local snapshots (`com.apple.TimeMachine.*`)
  can be thinned with `tmutil thinlocalsnapshots`; none existed here.
- **Swapfiles** under `/System/Volumes/VM`. The kernel manages them. Their size
  is a symptom of memory pressure, worth reporting, never worth deleting.
- **Purgeable space.** The gap between `df` avail and APFS container free is
  space the OS reclaims on demand. Reporting it as free space overstates what
  the user has.
