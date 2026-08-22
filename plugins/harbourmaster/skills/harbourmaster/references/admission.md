# Berths, pressure, and the evidence for both

## The berth model

One berth is one weight unit. Capacity is 80% of core count — 12 on a 16-core
M4 Max — which is the top of the 60–80% band the machine is aimed at. The
ceiling is capacity scaled by measured pressure:

| Pressure | Multiplier | Ceiling here |
|---|---|---|
| healthy | 1.00 | 12 |
| busy | 0.85 | 10 |
| tight | 0.50 | 6 |
| critical | 0.25 | 3 |
| unknown | 0.50 | 6 |

`critical` does not reach zero on purpose. A governor that admits nothing is
indistinguishable from a broken one, and the machine cannot drain unless work is
allowed to finish.

Two hard gates close admission whatever the berth count says:

- **disk below 20 GiB free** — new work fails on write rather than running slowly.
- **swap above 90%** — the machine is paging, and concurrency deepens it.

Both return exit 75 with `retry_after_sec: 300` and advice that says plainly this
is not a queue you can wait out.

## Why the lock is the registry

Every alternative needs a process to notice a death and act on it. A TTL expires
late and frees a berth a live job still holds. A PID check races against reuse. A
written record survives the writer.

A POSIX advisory lock held on an open file descriptor is released by the kernel
when the last holder ends, for any reason, immediately. So the wrapper takes the
lock, marks the descriptor inheritable, and `exec`s the workload into it. The
workload itself holds the berth. Reading occupancy means trying each lock: the
ones that refuse are held right now by a live process.

**Descendants inherit the descriptor, so the berth belongs to the tree.** Killing
a build's root process does not free its berths while an orphaned compiler is
still running. That is the behaviour you want — the orphan is still spending the
machine — but it is also the one way a berth can leak, so `berths.py` reports
`held_by_descendants`: berths whose recorded claimant is gone while the lock is
still held. A standing count there on an idle machine means something was left
behind.

**The trap that would make this silently useless:** Python marks descriptors
close-on-exec by default (PEP 446). Without `os.set_inheritable(fd, True)` the
lock dies at `exec`, every berth reads as free while the workload runs, and the
whole file becomes a no-op that appears to work. There is an eval for this.

The `.meta` sidecars are hints for humans and are never trusted alone. A meta
file beside an unlocked slot is residue from a finished job.

## What was measured

All on `Mac16,5` (M4 Max, 12P+4E, 128 GB), macOS 26.6, 2026-08-22, under a real
load average between 370 and 830.

| Claim | Method | Result |
|---|---|---|
| Lock survives `exec` through `taskpolicy` | weight-3 job on `sleep 8`; read occupancy from another process | 3 berths held, correct project and label |
| Released on normal exit | same job, after completion | 0 in use |
| Released on SIGKILL of the tree, no reaper | weight-3 job, `kill -9` root and children | 3 → 0 within a second |
| Berth survives killing only the root | same job, root killed, orphan left alive | still held — the descendant holds the descriptor |
| QoS lowers scheduler share | 4 spinners, wrapped vs not | 11.4–19.7 %CPU each → 0–5.2 %CPU each |
| QoS is inherited by children | 2 parents × 3 children, wrapped vs not | 52.7 %CPU mean per child → 0.2 %CPU |
| Demotion is reversible | `taskpolicy -b -p` then `-B -p` on a live process | 95.5% → 13.3% → 100.0% |
| Pressure read is sub-second | `time pressure.py` | 0.36 s (2.47 s before replacing `memory_pressure` with `vm_stat`) |

## Choosing a weight

Weight is an estimate of cores wanted, not a priority.

| Work | Weight |
|---|---|
| One unit test, a lint, a typecheck of one package | 1 |
| A dev server, a watch process, a single agent runner | 2 |
| A parallel test suite | 4 |
| `cargo build --release`, `xcodebuild`, a full monorepo build | 6–8 |

Over-weighting is the safer error: it costs throughput, where under-weighting
costs the guarantee the whole thing exists for.

## The demoter

The wrapper governs what opts in. The demoter governs what did not, which on a
real machine is most of it. It runs only at `critical` pressure, never signals
anything, and only ever calls `taskpolicy`.

It will not touch processes owned by another user, agent runtimes (`claude`,
`codex`, `agy`, `grok`) unless `--include-agents` is passed, anything matching the
never-list (`WindowServer`, `Finder`, `Dock`, terminals, its own scripts), or
anything it has already demoted. It restores everything once pressure returns to
`healthy` — `healthy`, not merely off `critical`, so the machine cannot oscillate.

**The hazard, stated:** demotion can invert priorities, since a demoted process
holding a lock a normal-priority process waits on now holds it longer. macOS
mitigates this for its own primitives and cannot for everything. The allowlist is
compute engines rather than coordination for that reason, and nothing is
automatic below `critical`.

## The ceiling has to bind at acquisition

Computing a ceiling and then scanning every slot file on disk hands out berths
the ceiling just refused. That was a real bug here: with a ceiling of 3 and slots
0–2 held, a fourth caller took slot 3 and the pressure scaling was decorative.
Acquisition scans `range(ceiling)`, and the ceiling is re-read on every poll
because pressure moves under a waiting caller.

## Degradation goes toward caution

When the pressure read cannot be taken in time it returns `unknown`. `unknown`
carries the same multiplier as `critical` (0.25), not a middling one. The middling
value was a measured bug: on a machine whose true state was `critical`, a
timed-out read reported `unknown` at 0.50 and **raised** the ceiling from 3 to 6,
admitting work the governor had just refused. Not knowing is a reason to be
careful rather than a reason to average.

## The bound has to cover the whole call

`--wait 3` once took 59.4 seconds, because the deadline was set after the pressure
read and the pressure read was unbounded — two full `ps` passes on a machine at
load 800. The deadline now starts before anything slow, the snapshot is bounded
and cached on disk for five seconds so concurrent sessions share one reading, and
`ps` runs once per collection rather than twice. Measured after: 3.5 s for the
same refusal.
