# Evidence

Every load-bearing claim, with how it was established. Measured on `Mac16,5`
(Apple M4 Max, 12 performance + 4 efficiency cores, 128 GB), macOS 26.6, on
2026-08-22 unless stated, under real load between 370 and 830.

## The problem this exists for

| Claim | Source |
|---|---|
| Load average 830.03 / 199.89 / 967.67 across 16 cores | `uptime`, 2026-08-22 |
| 76 `claude`, 73 `node`, 19 `rustc`, 3 `cargo` processes | `pgrep -f \| wc -l` |
| 266 runnable threads on 16 cores | `ps -Ao state=` |
| Disk 72 GiB free of 1.8 TiB (3.9%) | `shutil.disk_usage` |
| Swap 3.7 GB of 5.1 GB used | `sysctl vm.swapusage` |
| 86 git worktrees across `~/Dev` | `ls -d ~/Dev/*/.worktrees/*/` |
| `ship-fleet` fills slots from a hard-coded 8 with no machine reading | `ship-fleet` 2.4.0, `references/scheduling-and-concurrency.md` |

## The admission mechanism

| Claim | Method | Result |
|---|---|---|
| Berths held across `exec` through `taskpolicy` | weight-3 job, occupancy read from another process | 3 held, project and label correct |
| Released on normal exit | same job after completion | 0 |
| Released on SIGKILL of the process tree | `kill -9` root and children | 3 → 0, no reaper |
| Berth survives killing only the root | root killed, orphan alive | still held — descendant holds the descriptor |
| Refusal bounded and structured | fill the ceiling, request one more at `--wait 3` | exit 75 at 3.5 s with `retry_after_sec` |
| Pressure read is sub-second | `time pressure.py` | 0.31–0.43 s warm, ~2 s cold |

## macOS QoS

| Claim | Method | Result |
|---|---|---|
| `taskpolicy -b` lowers scheduler share | 4 spinners, wrapped vs not | 11.4–19.7 %CPU each → 0–5.2 %CPU each |
| Children inherit the class | 2 parents × 3 children, wrapped vs not | 52.7 %CPU mean per child → 0.2 %CPU |
| Demotion is reversible in place | `taskpolicy -b -p` then `-B -p` on a live process | 95.5% → 13.3% → 100.0% |
| No cgroup equivalent exists on Apple silicon | Gemini referral, corroborated by absence of any `cpulimit` and by `taskpolicy(8)` | admission plus QoS is the available lever |

## Thermal

| Claim | Source |
|---|---|
| `pmset -g therm` records nothing on this chassis | measured 2026-08-22; three "has been recorded" negatives |
| `IOPMCopyCPUPowerStatus` → `kIOReturnNotFound`; no `CPU_Speed_Limit` in `ioreg` | zephyr `ThermalLimitInference.swift`, 2026-08-05 |
| `ProcessInfo.thermalState` reported `.nominal` while the die hit 106.92 / 111.25 °C | zephyr, same source |
| `powermetrics` requires root | measured — "powermetrics must be invoked as the superuser" |
| A limiter clamps rather than slopes; use the max against the ladder, not the median against itself | zephyr `thermal-guard-no-throttle-onset-finding.md`, corrected 2026-08-08 |
| M4 Max P-core ladder tops at 4512 MHz | read inline from `powermetrics` residency output |
| P-clusters clamp independently | one sample: P0 13% residency at 4512 MHz, P1 0% at both top states and 59% at 3888 MHz |
| This Mac was thermally limited while already in High Power | 15-frame run: both clusters 99% busy, 0.01% and 0.02% near-top residency, AC `powermode 2` |
| `pmset` powermode: 0 Automatic, 1 Low Power, 2 High Power; per power source | zephyr `curve-learning-power-mode-provenance.md`, confirmed via `pmset -g custom` |
| High Power measured at +40% fan RPM and +6.7 W over Automatic at identical load | zephyr fleet measurement, 2026-08-08 |
| Passwordless `pmset` and `powermetrics` already granted | `sudo -n -l`; `/etc/sudoers.d/zephyr-pmset`, `zephyr-powermetrics`, installed 2026-08-08 |

## Plane constraints

| Claim | Source |
|---|---|
| Synthetic events contend globally; two campaigns interleave | `proctor` 0.6.0 SKILL.md, "Scale" |
| Proctor runs its own machine-wide foreground turn queue | `proctor_apps` tool contract |
| Apple silicon caps concurrent macOS guests at two | `proctor` 0.6.0 SKILL.md |
| The errand lane refuses by stable kind before starting anything | `anvil-errand` 0.1.0 SKILL.md |
| The node is configured as `node-LUKESFF`; `errand.toml` absent | `~/.anvil/node.toml`; `ls ~/.anvil/errand.toml` |
| Model lanes are ranked on headroom per remaining day | `defer` 1.0.0 SKILL.md |
| A JSONL ledger written by concurrent sessions has corrupted here | `~/.claude/mac-doctor/ledger.jsonl.corrupt-backup-20260810T101042` |

## Referral

The admission shape was put to an out-of-family model. Gemini
(`gemini-3.7-flash-high`) proposed FD-held slot leases, a bounded poll returning
`EX_TEMPFAIL`, and `taskpolicy` clamping, and named its own weakness: an admitted
slot that then runs `cargo test -j16` unwrapped. That weakness was closed by
measuring QoS inheritance, which it had raised as an open question.

Two further lanes were attempted and both were unavailable: `codex`
(`gpt-5.6-sol`) returned "You've hit your usage limit… try again at Aug 27th", and
`grok` (`grok-4.6`) returned HTTP 402, "Grok Build usage balance exhausted". So
this design rests on one out-of-family opinion plus direct measurement of its two
load-bearing claims, rather than on a three-family panel.
