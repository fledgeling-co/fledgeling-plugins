# harbourmaster

A harbourmaster does not sail the ships. They decide which berth a vessel takes,
whether it may enter yet, and which ones wait outside — and they keep the register
of what is in port.

This skill does that for a Mac that runs many agents at once. It answers two
questions: **where should this work run**, and **may it start here yet**.

## The problem, measured

On 22 August 2026 this machine carried a load average of **830 across 16 cores** —
76 `claude` processes, 73 `node`, 19 `rustc`, 86 git worktrees, and a disk at 97%.
Meanwhile the fleet orchestrator was starting runners from a hard-coded count of
eight, with no reading of the machine at all.

No single decision was wrong. Nothing was counting them together.

## What it does

**Routes across five planes**, choosing whichever resource is least scarce right
now rather than whichever is nearest to hand:

| Plane | Spends |
|---|---|
| This Mac, via the wrapper | CPU, RAM, disk |
| An `anvil errand` container | another machine entirely |
| A `proctor` session | a machine-wide foreground turn |
| `defer` to another model | another vendor's plan headroom |
| Claude subagents | this session's rate limit and context |

**Admits local work through berths.** Heavy work runs through a wrapper:

```bash
governor-run --weight 6 --project anvil --label build -- cargo build --release
```

The berth is a file lock held on a descriptor the workload inherits, so the kernel
returns it when the work ends — however it ends. There is no TTL, no reaper and no
stale lease. If the machine is full the wrapper gives up in a bounded time and
exits 75 with JSON saying why and when to come back, because a call that hangs
past a tool timeout becomes a retry storm rather than a queue. The workload runs
under a macOS QoS class its children inherit, so wrapping a build also wraps the
sixteen compilers it starts.

**Detects thermal limiting the OS will not report.** On this chassis every
reported thermal signal is silent — `pmset -g therm` records nothing,
`ProcessInfo.thermalState` says `.nominal` while the die sits at 111 °C. So the
verdict is inferred from how much of its busy time each CPU cluster spends at the
top of its own frequency ladder, read from the hardware's own state table. When a
cluster stays clamped for more than a minute, macOS is raised to High Power, and
lowered again once it clears.

**Keeps a register.** `~/Dev/FLEET.md`, beside `ARMADA.md`: what is running, which
projects hold berths, current pressure, thermal verdict.

## Using it

```bash
scripts/berths.py            # what is free
scripts/pressure.py          # cpu, memory, disk — sub-second
scripts/ledger.py            # regenerate ~/Dev/FLEET.md
scripts/install.sh --status  # agents, grants, berths
scripts/selftest.sh          # prove the mechanism still works here
```

The background agents are optional and install nothing on their own. A one-shot
invocation cannot sample thermals across a dwell window or notice pressure between
sessions, which is the only reason they exist.

## What it does not do

It does not do the work, judge the result, or clean the machine. `mac-doctor` owns
reclamation, `defer` owns model routing, `proctor` owns native-app instrumentation.
When disk is the gate that closed admission, it says so and hands over.

## Honest limits

- **It governs what opts in.** Work started around the wrapper is invisible to the
  register. The background demoter exists for that gap and only acts at critical
  pressure, only on compute processes owned by you, and only ever by lowering
  priority — it never signals anything.
- **High Power is not always a remedy.** Measured here: both CPU clusters were
  clamped while the machine was already in High Power. The lane reported the state
  correctly and had nothing left to press.
- **Thermal detection needs root.** Without a passwordless `powermetrics` grant it
  reports `unobservable` and changes nothing, rather than reporting a cool machine.
- **Demotion can invert priorities.** A demoted process holding a lock a normal one
  waits on holds it longer. The allowlist is compute engines rather than
  coordination for that reason.

See `EVALS.md` for what was verified and what was not.
