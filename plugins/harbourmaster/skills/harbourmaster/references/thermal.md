# Thermal limiting: why it must be inferred, and how

## Every reported signal is silent on this chassis

Checked on `Mac16,5` (M4 Max, macOS 26.6) on 2026-08-22, and independently by the
zephyr project on 2026-08-05:

| Source | Result |
|---|---|
| `pmset -g therm` | "No thermal warning level has been recorded" / "No performance warning level has been recorded" / "No CPU power status has been recorded" |
| `IOPMCopyCPUPowerStatus` | `kIOReturnNotFound`, no dictionary |
| `IOPMGetThermalWarningLevel` | `kIOReturnNotFound`, level untouched |
| `ioreg -n IOPMrootDomain` | none of `CPU_Speed_Limit`, `CPU_Available_CPUs`, `CPU_Scheduler_Limit` |
| thermal `sysctl`s | none exist |
| `ProcessInfo.thermalState` | `.nominal` across 240 samples while the die peaked at 106.92 and 111.25 °C |

Those three `pmset` lines are the registry keys being **absent**, not a clean bill
of health. A check built on any of the above reports "not throttling" forever, on
a machine that is throttling.

## The statistic, and the error it corrects

zephyr first looked for frequency to **decline** as temperature rose, found none
up to 115.42 °C, and concluded nothing throttled. That was wrong, and the
correction is this file's whole basis: **a limiter clamps, it does not slope.**
The capture had been inside the limited regime for its entire duration — 925
samples spanning 87.67–115.42 °C never once exceeded 4104 MHz and never touched
the top two states, on a chip whose P-cores reach 4512 MHz.

So a median compared against itself is flat whether the chip is free or clamped.
What separates them is **how much of its busy time a cluster spends at the top of
its own ladder**.

`powermetrics` prints that ladder inline on every residency line:

```
P0-Cluster HW active residency:  74.61% (1260 MHz: 27% ... 4416 MHz: 3.0% 4512 MHz: 13%)
```

The top is therefore **read from the hardware's own state table**, not learned
over time and not hard-coded — which matters because it is per-SKU and a constant
would be wrong on any other Mac.

## Per cluster, because they clamp per cluster

One sample on this machine, 2026-08-22:

| Cluster | Residency at 4512 MHz | Residency at 3888 MHz | Verdict |
|---|---|---|---|
| P0 | 13% | 2.4% | reaching the top |
| P1 | 0% | 59% | clamped |

A machine-level average, or a peak taken across both, reports that machine as
healthy. Peak frequency alone also misses it: P1 touched 4044 MHz for 2.9% of the
window, which reads as "near the top" while 59% of its time sat at 3888.

The rule: a P-cluster busy above 60% that spends under 2% of its active time at
or above 93% of its ladder top is **limited**. E-clusters are excluded — a clamp
there is the scheduler working, not heat.

## Acting on it

- **Dwell 60 s.** The verdict must hold continuously; any change resets the clock,
  so a flickering machine never accumulates one.
- **Raise:** `sudo pmset -c powermode 2` — the **AC branch only**. High Power on
  battery trades the user's charge for clock they did not ask for.
- **Clear 180 s**, longer than the dwell on purpose, then back to `powermode 0`.
- **Only what we raised is lowered.** A High Power setting the user chose is
  theirs; reverting it silently would be the tool overruling them.

## Known limits, stated

- **Not validated against observed throttle onset.** Every threshold is a reasoned
  choice, set to fail toward silence. A false positive raises the machine's power
  draw and heat for no reason, which is worse than saying nothing.
- **High Power is not always a remedy.** Measured here: both P-clusters were
  clamped (0.01% and 0.02% near-top residency at 99% busy) *while AC was already
  in High Power*. The lane detects the state correctly and has nothing left to
  press. It reports rather than promising a fix.
- **The read needs root.** Without a passwordless `powermetrics` grant the lane
  reports `unobservable` and changes nothing. On this machine the grants already
  exist, installed by zephyr on 2026-08-08 as `/etc/sudoers.d/zephyr-powermetrics`
  and `zephyr-pmset`; harbourmaster reuses them and installs nothing.
- **Sampling costs.** `powermetrics` at 1 Hz for the dwell window is why this runs
  on a 300 s LaunchAgent cadence rather than inside an admission decision.
- **Power source matters.** `pmset -g custom` reports per source and reading the
  wrong branch reports a mode the machine is not in.
