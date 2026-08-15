# Processes — the CPU, memory and orphan lane

Absorbed from the former `process-hygiene` skill. The unit of a finding here is
a **family**, not a PID: one leaked server per session exit over two days is a
single finding with a count of 167, not 167 findings.

## Reading CPU correctly

`ps` reports `%CPU` over a short sampling window. It answers "what did this do
just now", not "is this stuck". Two processes that look identical there are
often opposites:

- 600% for two seconds — a build, a test run, a browser rendering. Leave it.
- 30% sustained for five hours — a spin loop. Investigate it.

`survey.sh` computes `sustained_pct` (cumulative CPU ÷ elapsed) for this reason.
Rank on that, investigate anything sustained above ~25% with no reason to be,
and treat a short spike as normal work.

Elapsed time from `ps` can be nonsense for processes started before a clock
adjustment — figures like `18392-14:35:33` (fifty years) appear for
`WindowServer` and other boot-time daemons. Sanity-check an implausible elapsed
value against `uptime` before drawing a ratio from it.

## Reading memory correctly

Rank by RSS, then identify the process before judging it. A virtualisation
process holding 20G is a VM doing its job.

An RSS around 32 KB on a process that should be larger means it has been paged
out entirely — a useful marker of something idle for a very long time.

`memory_pressure` can report a high free percentage while swap is nearly full.
Swap is the more honest number for whether the machine is under pressure. Swap
size is a symptom to report, never something to delete.

## Orphans

Walk the parent chain; do not just test `PPID == 1`. Some processes are
legitimately started detached, and some orphans sit below a wrapper that is
itself orphaned — a chain like `python <- uv <- launchd` is an orphan family two
levels deep, and a naive `PPID == 1` filter misses the leaf.

When a family has both live and dead members, build the kill list from chain
analysis and print the survivors before signalling anything, so the boundary is
visible and reviewable.

## The fd-holder mechanism

An stdio child exits when its input reaches EOF, and EOF arrives only when
*every* copy of the write end is closed — not merely the parent's. A long-lived
background process that inherited a duplicate keeps the channel open, and the
child blocks forever after its owner dies.

Diagnosed on this machine: 167 orphaned MCP servers over ~2 days, ~644 MB RSS,
30 seconds of CPU between them. A single-process reproduction will not show it —
the leak needs three processes: client, server, and an unrelated fd-holder.

**Symptoms:** an orphan family alive for days with negligible CPU whose members
do not exit though their parent is long gone.

**Confirm** by killing the suspected holder and watching whether the orphans exit
on their own. That converts a guess about the mechanism into a fact and
identifies the real culprit rather than the visible symptom.

**Typical holders:** background dev servers, browser drivers left by a test run,
`tail -f` on a log, daemons started from a session that has since exited.

The durable fix is a parent-death watchdog in the server, not more frequent
sweeping; `~/Dev/docker-mcp-guard` implements one and ships `mcp-guard` to wrap
any stdio MCP server. When this lane finds a recurring orphan family, that is
the recommendation.

## The gate

Terminate only when all of these hold, and say which were checked.

- **No established connections** — `lsof -nP -p PID | grep ESTABLISHED`.
- **No listening socket something depends on.** A listener with live peers is in
  use. A listener with none may still be a dev server the user will return to —
  check its cwd (`lsof -a -p PID -d cwd`) against active work first.
- **Parent chain dead**, or provably idle: negligible cumulative CPU across long
  elapsed time.
- **Nothing in flight** — cross-check against a running build, test, or a
  browser driven by a live session.

Prefer SIGTERM, wait, escalate to SIGKILL for what ignores it. Chromium ignores
SIGTERM routinely; that is expected.

**Signal by explicit pid, never by command pattern.** On a machine with many
worktrees checked out, a pattern that describes one fleet's process describes
every fleet's — a `pkill -f` here has previously killed another runner's
`cargo test`. Build the pid list from a `ps` snapshot and signal that list.

## The automated lane — `scripts/runaway.sh`

The 15m tier runs this unattended, so its gate is narrower than the manual one
above. It is called by `reclaim.sh`; run it directly to see what it would do.

**Nothing is signalled on first sight.** `ps` %CPU answers "what did this do just
now", and even sustained CPU reads 100% for a Rust compile as readily as for a
spin loop. The difference is only visible over time, so a process must be seen
runaway on `RUNAWAY_CONFIRMATIONS` separate runs spanning at least
`RUNAWAY_MIN_WATCH_SECONDS` before it is eligible. State is one line per process
in `~/.claude/mac-doctor/watchlist.tsv`, rewritten every run: a process that
stops being runaway leaves the list and starts again from zero.

The span requirement is not redundant with the count. Under load these runs
stack — measured on this machine at load 418, a 15m job still alive after 8
minutes having accumulated 0.02s of CPU — so three "separate" runs can otherwise
land within a minute of each other and confirm nothing.

Identity is pid plus the kernel's start timestamp, not pid alone. A recycled pid
would otherwise inherit another process's sightings and be killed on its first
run. `etime` is unusable for this: its one-second resolution wobbles between
samples, so a key built from it never matches itself.

### Three classes, two autonomy levels

| Class | Test | Verdict |
| --- | --- | --- |
| `runaway-cpu` | orphaned, ≥10 min old, ≥60% sustained | killed after confirmation |
| `orphan-family` | orphaned automation browser, ≥30 min old | killed after confirmation, whole tree |
| `idle-orphan` | orphaned, ≥24h old, ≤2% sustained, ≥5 sharing a name | **reported only, never killed** |

The idle class is the 167-MCP-server and 548-log-follower shape — near-zero CPU,
so the sustained test cannot see it. It is reported rather than reaped because
it costs RSS and not CPU, so there is no urgency to buy with the risk, and from
outside a hundred idle orphans are indistinguishable from another fleet's live
workers. Family size is the discriminator that makes it a finding at all: one
long-lived idle orphan is usually a daemon doing its job.

### Why orphans only, and why that is not enough

Nothing with a live owner is ever signalled. A build has cargo as a parent, a
dev server has a shell, a test has its harness; something is waiting on all of
them. A leak has nobody.

That rule alone would sweep up every GUI application, because macOS launches
those from launchd too — **measured on this machine, 93 applications sit at
PPID 1**, and your own Chrome is indistinguishable from a leaked one by parentage
alone. The discriminator is the automation flags: a driver-spawned browser
carries `--disable-field-trial-config`, `--headless`, `--remote-debugging-port`
or a scratch `--user-data-dir`, and renderers inherit them. A `.app` without
those markers, and anything below it, is never a candidate.

### Declaring an instrument

A deliberate CPU load fixture and a leak look identical from outside: both
orphaned, both burning a core, neither with an owner you can ask. That ambiguity
is real — a batch of load burners on this machine was killed by hand about
seventy seconds before their own runner would have reaped them.

So a runner that spawns load can say so. Any file under
`~/.claude/mac-doctor/instruments/` is read as TSV:

```
<pid>	<expires_unix_epoch>	<owner label>
```

An unexpired declaration makes the pid invisible to this lane. An **expired** one
does the opposite of protecting it: the declaration is the runner's own promise
about when the load should be gone, so a burner outliving its stamp is a
stranded instrument — precisely the leak worth reaping. Expiry is what separates
the two, and only the spawner can supply it.

Better still, make the load self-limiting so a dead runner cannot strand it at
all: `timeout 600 yes > /dev/null` gives the burner its own deadline and turns
the reap into an optimisation rather than the only exit.

### The false positive this cannot rule out

A deliberately detached long-running compute job — `nohup python train.py &` —
is orphaned, pegs a core, holds no connections, and is indistinguishable from a
spin loop by every test here. It will be killed after confirmation. The escape
hatch is `~/.claude/mac-doctor/protected`, one glob per line, matched against the
command line as well as against paths; or a declaration as above. Say this
plainly when recommending the lane to someone, rather than after it has happened.

### Tunables

`RUNAWAY_MIN_ELAPSED` (600), `RUNAWAY_SUSTAINED_PCT` (60),
`RUNAWAY_CONFIRMATIONS` (3), `RUNAWAY_MIN_WATCH_SECONDS` (1800),
`RUNAWAY_BROWSER_MIN_ELAPSED` (1800), `RUNAWAY_IDLE_MIN_ELAPSED` (86400),
`RUNAWAY_IDLE_MAX_SUSTAINED` (2), `RUNAWAY_IDLE_MIN_FAMILY` (5).

Lowering the thresholds for a test also lowers them for real work: at
`RUNAWAY_SUSTAINED_PCT=10` this machine's `swiftpm-testing-helper` became a
candidate. Never combine lowered thresholds with `--apply`.

### Verifying a reap

Count processes alive before and against after. A loop of `kill "$p" 2>/dev/null`
reporting `killed $(wc -l < pidfile)` prints the file's line count, not the
number of processes that died — a number that looks like a measurement and is
not. `runaway.sh` re-checks every pid with `kill -0` after escalating and reports
survivors as `KEPT` rather than claiming the kill.

## macOS specifics

- Killing a browser tree's leaf leaves renderers behind. Collect the whole tree —
  server, browser parent, renderers — signal it together, then sweep for
  reparented renderers.
- Root-owned daemons need sudo. Report with the exact command; launchd restarts
  most of them, so a kill is a reset rather than a removal.
- `bluetoothd` spinning against a disconnected device, `duetexpertd`, and
  `mds_stores` mid-reindex are common benign-looking offenders. Check whether
  anything is actually connected or indexing before calling one runaway.
- Automation-spawned Chrome carries `--disable-field-trial-config` and similar
  flags and has an automation parent. The user's own browser has neither.

## Things that look dead and are not

- `PPID == 1` while holding established connections. Detached at launch is not
  abandoned.
- A dev server with no peers whose cwd matches work in flight elsewhere.
- Days of elapsed time with minutes of CPU — that is a daemon by design. Check
  whether the user's own projects expect it running.
