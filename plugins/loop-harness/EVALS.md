# Evals: loop-harness

Run 2026-08-09 against Claude Code v2.1.226. Same protocol as
[`goal-harness/EVALS.md`](../goal-harness/EVALS.md): each case run twice from an
identical fixture, one arm with the skill and one with nothing, graded by an
independent agent that saw each response alone under an anonymous id with no arm
label.

## Result

| Case | What it probes | skill | baseline | preferred |
|---|---|---|---|---|
| L01 | Watching benchmark runs and restarting on failure | **5/5** | 1/5 | skill |
| L02 | "Loop until the feature is 100% complete" | 3/3 | 3/3 | skill |
| L03 | "What exactly is performing the loop?" | **4/4** | 1/4 | skill |
| L05 | `/verify` on a 30-minute interval | **3/3** | 1/3 | skill |
| | **assertions** | **15/15** | 6/15 | |
| | **preference** | **4/4** | 0/4 | |

Combined with `goal-harness`: **32/33 assertions against 12/33, and 8/8
preferences.**

## The two cases that justify the skill

**L03, where the baseline was confidently wrong.** Asked what is performing a
no-interval loop, it answered that there is no timer, that nothing was scheduled
outside the conversation, and that "when the turn ended, the loop ended with
it." That is not a thinner answer; it is the opposite of what happens. Dynamic
pacing schedules a real pending wakeup through `ScheduleWakeup`, and the loop
shows up in the scheduled-task list like any other. Acting on the baseline's
answer means re-arming a loop that is already pending.

The grader, who did not know which arm was which, put it this way:

> one response reasons about the request and one inspects the actual
> scheduler/harness state, and in L03 and L05 that difference produces a
> factually wrong answer, not just a thinner one

**L05, where the baseline missed the trap it was built for.** Told to run `/verify`
every 30 minutes, it concluded `/verify` does not exist, having found no
`commands/` directory in the fixture. The real failure is that `/verify` is a
bundled skill marked `disable-model-invocation`, so a scheduled fire delivers it
as plain text and it never runs, with no error. The baseline's toolchain finding
was sound; it just diagnosed the wrong thing, and would have produced a loop
that ticks correctly and verifies nothing.

## Where the baseline held its own

**L02 tied at 3/3.** Both arms found that the fixture's declared gates cannot
run (`tsgo` and `vitest` absent, no lockfile, no dependencies declared) and both
refused to arm a loop with no verification oracle. The grader preferred the
skill arm for naming the mechanism error outright and routing to `goal-harness`,
where the baseline stayed inside the loop framing. But the substantive catch,
that nothing could verify "100% complete", was found by both.

Stated plainly: on "don't arm a loop with a dead verifier", the skill did not
beat a capable model paying attention.

## What the eval found in the skill itself

The L05 arm followed step 4, went to run `scripts/arm.sh --dry-run`, found no
such script in `loop-harness`, and reported it as a skill gap rather than
improvising. That name belongs to `goal-harness`. Step 4 now points at
`write-loop-md.sh`, which already does the dry-run diff and the 25,000-byte
check, and says that most loops need no settings change at all.

The L01 arm found something better than what the reference said. `Monitor`
guidance was "widen the alternation so the filter covers failure signatures",
which is true and insufficient: a process that dies without writing a final line
produces **no log output at all**, and a hang simply stops the log, so no filter
over that log can emit in either case. That arm paired the tail with a liveness
poll and emitted `PROC-EXIT`, `PROC-STALL` and a periodic `NO-PROC`. That is now
in `references/mechanism-choice.md`, with `tail -F` so a rotated or
not-yet-created log does not leave a dead watcher.

It also hit a real constraint: a subagent has `Monitor` but not `CronCreate` or
`ScheduleWakeup`, and a Monitor it arms dies with its thread. Both skills now
say to build the artifacts and hand back the arming sequence rather than
reporting work as armed when nothing is scheduled.

**The scores above were produced before these fixes.**

## Limits of this run

- **4 of 6 cases.** L04 (a `7m` interval that does not divide 60) and L06
  (Monitor not restored on resume) were not run.
- **The fixture contains no benchmark harness**, which L01 correctly detects. So
  L01 measures the design handed back, not a loop observed running.
- **One grader, not a panel**, and **n=1 per cell**, so no variance estimate.
- Nothing here measures a loop over hours. Every claim about the seven-day
  expiry, jitter and resume behaviour comes from the binary and the docs
  (`references/mechanics.md`), not from this run.
