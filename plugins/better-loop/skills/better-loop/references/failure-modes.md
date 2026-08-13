# Failure modes, and what fixes each

Observed across real `/loop` use in `~/.claude/history.jsonl` (2026-06-15 to
2026-08-08), from session-cost telemetry, and from the documented behaviour in
`mechanics.md`. The follow-up prompt is the evidence.

## 1. The loop fires after the failure is already known

**Evidence:** five of the twelve heaviest sessions — 91% of input between them —
re-sent the same unmet condition, the same six failing tasks and the same status
poll turn after turn, paying the whole accumulated prefix each time. In one
session: "49M tokens is insane."

**Cause:** a schedule has no idea whether anything changed. It re-runs the tick
prompt, the tick re-reads the same state, and the wake re-bills the session's
whole prefix. A smaller context window does not help; nothing about a smaller
window stops a loop from restarting.

**Fix:** the watcher wakes only on a changed probe fingerprint, sends the delta
rather than the state, backs off on a state already seen, and holds a wake budget
per hour. Where the tick needs no conversation context, `--tick-cmd` runs it
detached and the session is never woken at all.

## 2. Nothing is visibly performing the loop

**Evidence:** "what exactly is performing the loop — i expected to see a monitor
or script running, did i invoke it incorrectly?" and, in the same session, "i
expected /loop to be able to be left".

**Cause:** a dynamic `/loop` schedules a wakeup and shows nothing. No process, no
monitor, no visible timer — the only artefact is a scheduled task the user never
sees. The loop was working; it was just invisible, and an invisible loop is
indistinguishable from one that failed to start.

**Fix:** the loop *is* a monitor now, so it appears in `TaskList` and in the
session's task display. `arm.sh` prints the probe, interval and bounds, and the
ledger gives it a surface between wakes.

## 3. The loop ticks and does nothing

**Cause:** the prompt names a skill Claude may not invoke on its own, so the fire
delivers it as plain text. `/verify` and `/code-review` bite most often, and
there is no error. A wake carries text the model reads, so this applies to the
watcher too.

**Fix:** `preflight.sh --skills` resolves every named skill. Where one is not
model-invocable, make it a shell command in the probe or the tick, or name the
plugin-qualified skill.

## 4. The loop stops on its own overnight

**Causes, in order of likelihood:** a dynamic tick that neither rescheduled nor
stopped (one ~20-minute fallback fire, then it ends); the seven-day expiry (fires
once, deletes itself, no warning); `/clear`; the session exiting.

**Fix:** the first two do not apply to a watcher — there is no wakeup to forget
and no scheduled task to expire. For the last, background the session. `/clear`
kills the monitor; `status.sh` shows the state file still armed with a stale
ledger, which is the signature.

## 5. The wake signal is deaf after a resume

**Cause:** `--resume` restores recurring tasks and unexpired one-shots, but
**background Bash and Monitor tasks are never restored**.

**Fix:** re-run the `Monitor` call `arm.sh` printed. Arming is idempotent, and
the state file and ledger carry across, so the loop resumes where it stopped
rather than re-establishing a baseline from scratch.

## 6. The monitor is silent through a failure

**Cause:** a filter matching only the success marker. The process crashloops and
the monitor emits nothing, which reads as still-running.

**Fix:** filters must cover every terminal state. `watch.sh` emits DONE, ENDED,
QUIET and GONE as well as CHANGE for exactly this reason. When writing a filter
for a stream directly, ask: if this process crashed right now, would anything be
emitted? If not, widen the alternation.

## 7. Every poll looks like a change

**Cause:** a probe that includes a timestamp, an elapsed time, a PID, a progress
percentage or an unsorted listing. The fingerprint differs every time, so the
change gate never closes and the loop is a polling loop again — at polling
prices.

**Fix:** `preflight.sh --probe` runs it twice against an unchanged world and
blocks if the two differ. `status.sh` prints the wake-to-poll ratio, which
catches a probe that degrades later.

## 8. Ticks run indefinitely with no stop condition

**Evidence:** "Don't allow samples to run infinitely" — written into the loop
prompt by hand.

**Cause:** a loop has no finish line by construction. Without a stop branch the
old one ran to the seven-day expiry; a watcher would run until the session ends.

**Fix:** `--stop-when` for a real end state, `--dry-stop` for work that should
end when the world settles. Where every field wants a stop condition, the work
has a finish line: route to **better-goal**.

## 9. No progress visibility

**Evidence:** "how're things going, any improvements/gains?"

**Cause:** ticks scroll past in the transcript and compaction removes them.

**Fix:** the watcher writes a ledger row for every poll that matters — including
the suppressed ones, so a quiet loop can prove it was working. `status.sh` reads
it, and asking it costs the loop nothing. Asking the loop itself costs a turn and
tells you what the file already knew.

## 10. Two loops competing

**Cause:** scheduled prompts fire only while the session is idle and there is no
catch-up. Two loops interleave, each delaying the other, and both appear slow.

**Fix:** watchers poll independently in background processes, so they do not
delay each other — but their wakes still land in one session and still queue.
`preflight.sh` flags a loop already armed. One loop per concern.

## 11. A human verdict blocks every tick

**Evidence:** the standing instruction, written by hand into loop prompts —
*"don't wait on me for future rounds, I can provide my feedback later once the AI
models have performed their own reviews"*.

**Cause:** a review step in the tick protocol that parks until an answer arrives.
A loop waiting on someone asleep is indistinguishable from one that crashed.

**Fix:** queue the item for the human on disk and carry on with the next one; let
model-side review gate the round; apply human verdicts whenever they land.

## 12. Scheduling fails outright

**Cause:** `CLAUDE_CODE_DISABLE_CRON=1`, `.claude` or `scheduled_tasks.json`
being a symlink, or the 50-task cap.

**Fix:** all four are `preflight.sh --cron` checks. None of them applies to a
watcher, which is one more reason it is the default.

---

## The pattern behind all twelve

Three shapes. **The loop was invisible** — running fine with no surface to check,
so it could not be told from a dead one (#2, #9). **The loop was running and
accomplishing nothing** (#3, #4, #5, #6, #8, #10, #11, #12). And **the loop was
working and that was the problem** (#1, #7): it kept telling the session things
it already knew, at the price of the whole prefix each time.

The first two are fixed by giving the loop a wake signal you can point at and a
file it writes to every tick. The third is fixed by making a wake require new
information.
