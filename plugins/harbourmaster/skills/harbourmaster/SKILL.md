---
name: harbourmaster
description: >-
  Decide where a piece of work should run, and whether this Mac can carry it yet. Routes across five
  execution planes — this machine directly, a container on another machine through anvil errand, a
  native-app instrument session through proctor, another model or CLI through defer, and in-session
  Claude subagents or workflows — by asking which resource each one actually spends, then spending
  the one that is least scarce right now. Governs the local plane with berth admission: heavy work
  runs through a wrapper that holds its slot on a POSIX file lock the kernel releases when the
  process dies, so there is no reaper and no stale lease, refuses in a bounded time rather than
  hanging past a tool timeout, and runs the workload under a macOS QoS class that its child
  processes inherit. Keeps a cross-project ledger of what is running beside ARMADA.md, measures CPU,
  memory and disk pressure in under a second, and detects sustained thermal limiting from per-cluster
  frequency residency — the only method that works on a chassis where every OS-reported thermal
  signal is silent — raising macOS to High Power while it holds and standing back down after. Use it
  when choosing how many runners or agents to start, before launching builds, test suites or fleets,
  when a machine is pinned or hot or out of disk, when deciding whether work belongs on this Mac at
  all, and whenever ship-fleet, ship-feature, code-review or test-campaign needs a concurrency
  number it did not invent.
---

# harbourmaster

A harbourmaster does not sail the ships. They decide which berth a vessel takes,
whether it may enter yet, and which ones wait outside — and they keep the register
of what is in port.

This skill answers two questions, and the second only matters because of the first:

1. **Which plane should this work run on?** Five are available and they spend
   different resources. The wrong plane is not slower; it is billed to a resource
   that had none left.
2. **May it start on this Mac yet?** Only the local plane needs governing, because
   it is the only one whose scarcity this machine feels.

The measured problem it exists for: on 2026-08-22 this Mac carried a load average
of **830 across 16 cores** — 76 `claude` processes, 73 `node`, 19 `rustc` — while
`ship-fleet` was starting runners from a hard-coded count of 8 with no reading of
the machine at all. Nothing was wrong with any single decision. Nothing was
counting them together.

## Route first

Ask what each plane spends. Take the plane whose resource is cheapest right now,
not the one that is nearest to hand.

| Plane | Spends | Reach for it when |
|---|---|---|
| **This Mac** via `governor-run` | CPU, RAM, disk — the thing that is scarce | Building, testing, running anything that must touch this working tree |
| **`anvil-errand`** container on the node | Another machine entirely; nothing here | Long, self-contained, CPU-heavy work that needs no local state — benchmark runs, big builds, batch jobs |
| **`proctor`** instrument session | A machine-wide foreground turn, and little CPU | Driving or verifying a native macOS app — the accessibility tree, capture trustworthiness, geometry assertions |
| **`defer`** to another model or CLI | Another vendor's plan headroom | Judgment, verdicts, second opinions, out-of-family review, completeness critique — **unless the caller is running `tiered`, which turns this plane off** |
| **Claude subagents / workflows** | This session's rate limit and context | Wide reading, search and investigation across many files |

**A sixth resource has no plane and no meter: the conductor's attention.** When a caller runs
`tiered` — a frontier conductor delegating to cheaper sessions bound by directory — the `defer` plane
is off and the delegation happens through perch bindings instead. That changes what is scarce. A
cheaper tier needs more rounds per item, more explicit briefs, and its gate exit codes read rather
than its prose, so **each worker consumes conductor turns at a rate berths do not bound.** Berths cap
the CPU a fleet can spend; nothing caps the attention it costs. When advising a `tiered` caller on
fleet width, say so: the binding constraint is likely to be the conductor's context rather than the
machine's cores, and it will not appear in any reading this skill produces.

Two of those carry constraints worth holding in mind before you plan around them.

**`proctor` serialises on the foreground and already arbitrates it.** Synthetic
events enter one system-wide stream, so two campaigns actuating at once interleave
and the second one's click lands in whatever window the first raised. Proctor runs
its own machine-wide turn queue for exactly this. Do not build a second queue in
front of it — route foreground work there and let it take its turn. Read-only
proctor calls (`snapshot`, `find`, `capture`, `assert`) do not contend and need no
berth. Apple silicon also caps concurrent macOS guests at two, so a VM fleet is not
an escape.

**The errand plane refuses rather than degrading.** `anvil errand --check` reports
a stable refusal kind before anything starts. On this machine today the node is
configured (`node-LUKESFF`) and `errand.toml` is absent, so the lane answers
`errand_ticket_unavailable`. Check before planning work onto it; treat a refusal
kind as the fact and its sentence as commentary.

`references/routing.md` carries the full decision procedure, including what to do
when two planes are both viable and when work has to be split across them.

## Then admit

Local work goes through the wrapper. It takes berths, runs the command, and gives
them back by dying.

```bash
scripts/governor-run --weight 4 --project anvil --label "cargo build" \
  -- cargo build --release
```

- **`--weight`** is roughly the cores the job will want. A single test is 1; a
  `-j`-parallel build is 4–8. Ceiling is 80% of core count, reduced by measured
  pressure and never below 1, so the machine always drains.
- **Exit 75** means not admitted, with structured JSON on stderr naming the
  pressure, what is in use, and a jittered `retry_after_sec`. Return to your own
  scheduler and try later. Do not loop on the call.
- **Exit 64** means the invocation was wrong — usually a weight larger than the
  machine's whole capacity.
- Any other code is the workload's own.

Read the state without taking anything:

```bash
scripts/berths.py            # ceiling, in use, available, who holds what
scripts/pressure.py          # cpu/memory/disk, sub-second
scripts/ledger.py            # write ~/Dev/FLEET.md
scripts/install.sh --status  # agents, grants, berths
```

Three properties make the admission honest, and each was measured on this machine
rather than assumed. `references/admission.md` has the numbers and the tests.

- **The lock is the registry.** A berth is a POSIX advisory lock held on an open
  file descriptor that the workload inherits across `exec`. The kernel releases it
  when the last holder ends, for any reason including SIGKILL, so there is no TTL,
  no reaper and no stale lease. The descriptor is inherited by descendants too, so
  the berth is held by the process *tree* — killing a build's root process does not
  free it while an orphaned compiler is still running, which is right, since that
  compiler is still spending the machine. `berths.py` reports
  `held_by_descendants` for the case where that is a leak rather than a build.
- **Refusal is bounded.** Polling stops at `--wait` (15s by default) and returns
  exit 75. A call that blocks past a tool timeout becomes a retry storm, which is
  worse than the queue it was trying to be.
- **QoS is inherited.** The workload runs under `taskpolicy`, and children inherit
  it — measured at 52.7 %CPU per child unwrapped against 0.2 %CPU under a wrapped
  parent. Wrapping a runner therefore wraps the `cargo test -j16` it starts, with
  the caller doing nothing. This is what closes the gap between admitting a job and
  controlling what that job spawns.

## Pressure, and what it changes

`scripts/pressure.py` returns in well under a second and reports four verdicts —
`cpu`, `memory`, `disk` and the worst of them. Sub-second matters: a governor that
takes ten seconds to answer is one nobody calls.

The ceiling scales with the verdict — `healthy` 1.00, `busy` 0.85, `tight` 0.50,
`critical` 0.25 — and two hard gates close admission entirely regardless of berths:
disk below 20 GiB free, and swap above 90%. Those two are states where starting
more work makes the machine worse rather than merely slower.

Both disk axes are checked and the stricter wins. This machine has 72 GiB free,
which sounds comfortable and is 3.9% of the volume; APFS copy-on-write degrades
well before the bytes run out.

## Thermal

On this chassis every OS-reported thermal signal is silent. `pmset -g therm`
prints "No thermal warning level has been recorded" three times over,
`IOPMCopyCPUPowerStatus` returns `kIOReturnNotFound`, there are no thermal
`sysctl`s, and `ProcessInfo.thermalState` reported `.nominal` across 240 samples
while the die peaked at 111 °C. Any check built on one of those returns "not
throttling" forever.

So the verdict is inferred from frequency residency, which needs `powermetrics`
and root. Without that grant this lane reports `unobservable` and changes nothing —
which is the honest answer, not a claim that the machine is cool.

The statistic is **residency in the top states, per cluster**. A limiter clamps
rather than slopes, so a median compared against itself looks the same either way;
what separates them is how much of its busy time a cluster spends at the top of
its own ladder, and `powermetrics` prints that ladder inline so it is read rather
than assumed. Clusters are assessed separately because they clamp separately: one
sample here showed P0 holding 13% residency at 4512 MHz while P1 held 0% at both
top states and 59% at 3888 MHz.

When a busy P-cluster stays clamped for longer than 60 seconds, macOS is raised to
High Power on the **AC branch only**, and returned to Automatic after 180 seconds
clear. Only a mode this skill raised is ever lowered — a High Power setting the
user chose is theirs. `references/thermal.md` carries the derivation and its known
blind spots.

## The ledger

Live state is `~/.claude/harbourmaster/`: the berth locks, and an event journal
appended under an exclusive lock. `scripts/ledger.py` renders `~/Dev/FLEET.md`
beside ARMADA.md — pressure, which projects hold berths, thermal verdict, recent
events.

The split is deliberate. ARMADA.md is curated and skim-read; this is written many
times a minute by many sessions at once, and mac-doctor's equivalent JSONL ledger
has a `.corrupt-backup` file on disk from exactly that. FLEET.md is regenerated
and safe to delete.

Occupancy is never stored — it is read back from the locks, so it cannot drift
from reality or outlive the process that claimed it. What FLEET.md shows is
governed work only; anything started around the wrapper is invisible there, and
saying so on the page is why the demoter exists.

## Calling this from another skill

Ask for a number instead of inventing one, then wrap what you start.

**`ship-fleet`** replaces its fixed 8 slots with the available berths, re-read on
every refill rather than once at the top:

```js
const free = JSON.parse(sh(`${HM}/berths.py`)).available
for (const item of ready().slice(0, Math.max(1, free))) { /* start runner */ }
```

**`ship-feature`** and **`shipyard:work`** wrap builds and suites at weight 4–8,
and treat exit 75 as "wait and retry", not as a failing gate.

**`code-review`** and **`shipyard:verify`** route to `defer` before they route
here — grading is judgment, and judgment costs another vendor's headroom rather
than this machine's cores.

**`test-campaign`** splits by lane: web and unit suites take berths; native macOS
execution goes to `proctor` and takes a foreground turn instead. Its execution-plane
axis and this skill's plane table are the same axis, named twice.

`references/integration.md` has the call shapes per skill, including what each
should do on refusal.

## Scope

This decides placement and admission. It does not do the work, judge the result,
or clean the machine — `mac-doctor` owns reclamation, `defer` owns model routing,
`proctor` owns native-app instrumentation. When disk is the closing gate, say so
and hand over; do not delete anything from here.

Keep replies to the state and the next step. A berth report is two lines, not a
table. Reach for a subagent only when surveying many repos at once, and cap that
fan-out at four; a berth check and a routing decision need none.
