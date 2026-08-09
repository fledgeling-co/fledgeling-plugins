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
