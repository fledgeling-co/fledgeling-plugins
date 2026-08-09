# Failure modes, and what fixes each

Observed across real `/loop` use in `~/.claude/history.jsonl` (2026-06-15 to
2026-08-08) and from the documented behaviour in `mechanics.md`. The follow-up
prompt is the evidence.

## 1. Nothing is visibly performing the loop

**Evidence:** "what exactly is performing the loop — i expected to see a monitor
or script running, did i invoke it incorrectly?" and, in the same session, "i
expected /loop to be able to be left".

**Cause:** a dynamic `/loop` schedules a wakeup and shows nothing. There is no
process, no monitor, no visible timer — the only artefact is a scheduled task
the user never sees. The loop was working; it was just invisible, and an
invisible loop is indistinguishable from one that failed to start.

**Fix:** arm the wake signal explicitly and name it. When events drive the ticks
that is a Monitor, which *is* visible. Print the mechanism, the job ID and the
cadence at arm time, and keep the ledger so the loop has a surface.

## 2. The loop ticks and does nothing

**Cause:** the prompt names a skill Claude may not invoke on its own, so the
fire delivers it as plain text. `/verify` and `/code-review` are the two that
bite most often, and there is no error.

**Fix:** `preflight.sh` resolves every named skill. Where one is not
model-invocable, either call it from the main turn or name the underlying
command in the tick protocol.

## 3. The loop stops on its own overnight

**Causes, in order of likelihood:** a dynamic tick that neither rescheduled nor
stopped (one ~20-minute fallback fire, then it ends); the seven-day expiry
(fires once, deletes itself, no warning); `/clear`; the session exiting.

**Fix:** the heartbeat wakeup catches the first. The day-six renewal reminder
catches the second. For the fourth, background the session — that carries the
tasks over and keeps them firing without a terminal.

## 4. The wake signal is deaf after a resume

**Cause:** `--resume` restores recurring tasks and unexpired one-shots, but
**background Bash and Monitor tasks are never restored**. A loop whose ticks
were driven by a Monitor comes back on the cron alone.

**Fix:** the tick protocol calls `TaskList` first and re-arms the Monitor if it
is gone. Arming is idempotent, so this costs nothing when it is already running.

## 5. The monitor is silent through a failure

**Cause:** a filter matching only the success marker. The process crashloops and
the monitor emits nothing, which reads as still-running.

**Fix:** filters must cover every terminal state. See `mechanism-choice.md`.

## 6. Ticks run infinitely with no stop condition

**Evidence:** "Don't allow samples to run infinitely" — written into the loop
prompt by hand.

**Cause:** a loop has no finish line by construction, so without an explicit
stop branch it runs to the seven-day expiry.

**Fix:** an explicit stop condition in the tick protocol, and where the work
genuinely has an end state, route to `goal-harness` instead.

## 7. No progress visibility

**Evidence:** "how're things going, any improvements/gains?"

**Cause:** ticks scroll past in the transcript and compaction removes them.

**Fix:** `tick.sh` appends one row per tick; `status.sh` reads it. Asking costs
nothing and does not interrupt the run.

## 8. Two loops competing

**Cause:** scheduled prompts fire only while the session is idle and there is no
catch-up. Two loops in one session interleave, each delaying the other, and both
appear slow.

**Fix:** preflight lists existing scheduled tasks and flags a stale one from an
earlier run. One loop per concern.

## 9. Uneven or surprising fire times

**Cause:** jitter (up to 30 minutes late for recurring tasks) plus rounding of
intervals that do not divide their unit.

**Fix:** say what was rounded to and what the jitter window is at arm time, so
a fire at `:29` is expected rather than alarming.

## 10. Scheduling fails outright

**Cause:** `CLAUDE_CODE_DISABLE_CRON=1`, or `.claude` / `scheduled_tasks.json`
being a symlink, or the 50-task cap.

**Fix:** all four are preflight checks.

---

## The pattern behind all ten

Two shapes. Either **the loop was invisible** — running fine, with no surface to
check, so it could not be told from a dead one (#1, #7, #9) — or **the loop was
running and accomplishing nothing** (#2, #3, #4, #5, #6, #8).

Both are fixed by the same two moves: give the loop a wake signal you can point
at, and give it a file it writes to every tick.
