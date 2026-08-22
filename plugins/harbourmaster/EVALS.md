# EVALS — harbourmaster

## No agent panel was run, and that matters

**This skill has not been graded against a no-skill baseline, and no blind judge
panel scored it.** The session that built it was instructed not to spawn subagents
or run workflows, so the comparative evaluation the `create-skill` pipeline
normally performs did not happen. Nothing below substitutes for it.

What that leaves unanswered: whether an agent handed this skill actually routes
work better than an agent handed nothing. That is the question a panel exists to
settle, and it is open.

What *was* established is narrower and mechanical: the machinery does what it
claims on the machine it was built for. Every row below is a measurement, not a
judgement.

## Mechanically verified

`scripts/selftest.sh` — **10 passed, 0 failed**, exit 0. Run it on any machine
before trusting the skill there; several properties are OS-behaviour claims that
could differ on another macOS version.

| # | Property | Why it would fail silently |
|---|---|---|
| 1 | Pressure returns a verdict | — |
| 2 | Pressure read under 5 s | A slow governor is one nobody calls |
| 3 | Berths held across `exec` | Python marks descriptors close-on-exec by default; without `set_inheritable` every berth reads free while work runs |
| 4 | SIGKILL on the tree frees every berth, no reaper | The kernel-release guarantee is the whole design |
| 5 | Over-capacity weight refused with exit 64 | Would otherwise queue forever for something impossible |
| 6 | Refusal carries exit 75 and `retry_after_sec` | Callers cannot schedule without it |
| 7 | Refusal bounded by `--wait` | An unbounded call becomes a retry storm |
| 8 | `taskpolicy` present | No QoS clamping without it |
| 9 | Demoter is dry-run without `--apply` | It acts on processes it did not start |
| 10 | Thermal lane reports readability with a reason | Silence must not read as "cool" |

## Bugs the selftest found in this skill

Written down because they are the argument for having it, and each would have
shipped as a governor that appeared to work.

1. **`--wait 3` took 59.4 seconds.** The deadline was set after the pressure read,
   and the pressure read was unbounded — two full `ps` passes on a machine at load
   800. Fixed by starting the clock first, bounding and caching the snapshot, and
   running `ps` once. Now 3.5 s.
2. **The ceiling did not bind at acquisition.** Pressure was computed, then
   acquisition scanned every slot file on disk regardless — so with a ceiling of 3
   and slots 0–2 held, a fourth caller took slot 3. Pressure scaling was
   decorative. Fixed by scanning `range(ceiling)`.
3. **Degradation raised the ceiling.** A timed-out pressure read returned
   `unknown`, whose multiplier was 0.50 — more permissive than the machine's true
   `critical` 0.25 — so failing to read the machine *admitted more work*. Fixed by
   degrading to the worst multiplier.

A fourth finding was a correction to a claim rather than a defect: the berth is
held by the process **tree**, not the root, because descendants inherit the
descriptor. Killing a build's root does not free its berths while an orphaned
compiler runs. That is the desirable behaviour, and the docs and the test now say
so instead of the simpler thing that was not true.

## Verified by direct measurement, not by test

All on `Mac16,5` (M4 Max), macOS 26.6, 2026-08-22, under real load. Full table in
`skills/harbourmaster/references/evidence.md`.

- QoS lowers scheduler share: 11.4–19.7 %CPU → 0–5.2 %CPU per spinner.
- QoS is inherited by children: 52.7 %CPU → 0.2 %CPU mean per child.
- Demotion is reversible in place: 95.5% → 13.3% → 100.0%.
- The thermal lane detected a live limit: both P-clusters 99% busy with 0.01% and
  0.02% near-top residency, correctly declining to act because the dwell was unmet
  and AC was already in High Power.

## Not verified

- **Any comparison against not having the skill.** See the top of this file.
- **Whether calling skills adopt it.** `ship-fleet`, `ship-feature`, `code-review`
  and `test-campaign` have not been modified to call it. Until they are, the
  integration guidance is a proposal.
- **The thermal act path end to end.** Detection is proven on live data and the
  raise/lower calls are exercised only in the sense that `pmset -c powermode` was
  confirmed reachable. No run has yet observed a 60-second clamp, raised the mode,
  and stood back down — the machine was already in High Power throughout.
- **Behaviour on any other Mac.** Core counts, the frequency ladder, cluster
  layout and which sudo grants exist are all machine-specific. The ladder is read
  from hardware rather than hard-coded, which should travel; nothing else has been
  tried elsewhere.
- **Long-run stability.** No multi-day soak. Berth leakage via long-lived orphans
  is surfaced (`held_by_descendants`) but has not been observed over time.

## What would settle the open question

Three tasks, run with and without the skill, graded blind on whether the resulting
plan respects the machine:

1. "Ship the remaining twelve items in this repo" on a machine at load 400 — does
   the agent pick a concurrency number from measurement or from habit?
2. "Run the full test campaign for this macOS app" — does it route native
   execution to proctor and take a foreground turn, or start parallel runners that
   fight over the front?
3. "Verify this feature meets its acceptance criteria" — does it spend another
   vendor's headroom on the judgement, or this machine's cores?
