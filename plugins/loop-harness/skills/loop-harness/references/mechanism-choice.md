# Choosing the mechanism

The built-in `/loop` does not make this choice for you — it schedules whatever
you typed. Most of the value in this skill is here.

## The question that decides it

**What has to be true for the next tick to be worth running?**

| Answer | Mechanism | Why |
|---|---|---|
| "Something happened" — a log line, a file changed, CI finished, a comment landed | **Monitor**, `persistent: true` | The event wakes the session as it happens. Zero wasted ticks |
| "The work is finished" | **goal-harness** | That is a finish line, not a cadence. A loop cannot verify one |
| "Enough time has passed, but how much varies" | **`/loop <prompt>`**, dynamic pacing | The run picks 60s–3600s per tick from what it just saw |
| "It is 9am" / "another 5 minutes elapsed" | **`/loop <interval> <prompt>`** | Fixed cron. The only case where polling is right |
| "It is the same sweep as last time" | bare **`/loop`** + `.claude/loop.md` | The file is the standing prompt |
| "It has to run whether or not my laptop is open" | **Routines** (cloud) or a **Desktop scheduled task** | `/loop` needs the session open. Say so rather than arming something that will not survive |

## Worked cases

**"Monitor the progression of all of the benchmark runs and resolve any errors
in the harness or config, then restart the benchmarks as needed."**

Event-driven, not time-driven — the interesting moments are a run failing or
finishing. Monitor on the harness log with a filter covering both:

```
tail -f runs/current.log | grep -E --line-buffered \
  "sample_complete|Traceback|FAILED|OOM|Killed|rate.?limit|exit code [1-9]"
```

plus a 1800s heartbeat so a silent harness still gets checked. A five-minute
cron here spends most of its ticks discovering nothing changed.

**"Keep working on iterating the compression improvements."**

No end state and no external event — dynamic pacing. The tick protocol needs a
no-op branch, because otherwise every tick invents work to justify itself.

**"Keep implementing until you've verified the feature is 100% complete."**

Not a loop. "100% complete" is a verifiable end state, so this is
`goal-harness`, and a loop here will tick past completion forever.

**"Check the deploy every 5 minutes and tell me what happened."**

Genuinely time-based, genuinely short-lived. Fixed cron at `*/5`. Add the stop
condition — deploy reaches a terminal state — or it runs for seven days.

**"Tell me when the build finishes."**

Neither a loop nor a goal: one notification. Bash `run_in_background` with a
command that exits when the condition holds (`until grep -q "Ready in" dev.log;
do sleep 0.5; done`). A Monitor here stays armed until timeout long after the
event.

## Monitor filters

A monitor is only as good as its filter, and the failure is always the same
shape: it watches for success and goes quiet on failure, which is
indistinguishable from still working.

```bash
# Wrong — silent on crash, hang, or any non-success exit
tail -f run.log | grep --line-buffered "elapsed_steps="

# Right — progress plus the failure signatures you would act on
tail -f run.log | grep -E --line-buffered \
  "elapsed_steps=|Traceback|Error|FAILED|assert|Killed|OOM"
```

Before arming, ask: *if this process crashed right now, would my filter emit
anything?* If not, widen it. For poll loops over a job's status, emit on every
terminal state — `succeeded|failed|cancelled|timeout` — not just success.

Mechanics that bite:

- Every pipe stage must flush per line: `grep --line-buffered`, `awk` with
  `fflush()`. `head` cannot flush at all, so `| head -N` delivers nothing until
  N matches accumulate.
- Only stdout is the event stream. Merge stderr with `2>&1` for a command you
  run directly, or its failures never reach the filter.
- Handle transient failures in poll loops (`curl … || true`) so one bad request
  does not kill the monitor.
- Poll intervals: 30s+ for remote APIs, 0.5–1s for local checks.
- A monitor producing too many events is stopped automatically. Filter to the
  lines you would act on — which means both good news and bad, not only good.

## Choosing an interval, when you do need one

Only these map cleanly to cron:

| Pattern | Cron | Note |
|---|---|---|
| `Nm`, N ≤ 59 | `*/N * * * *` | |
| `Nm`, N ≥ 60 | `0 */H * * *` | H = N/60 and must divide 24 |
| `Nh`, N ≤ 23 | `0 */N * * *` | |
| `Nd` | `0 0 */N * *` | midnight local |
| `Ns` | `ceil(N/60)m` | one-minute granularity |

`7m` gives uneven gaps at :56→:00. `90m` is 1.5h, which cron cannot express.
Round to the nearest clean interval and say what you rounded to.

Avoid `:00` and `:30`: every user who asks for "9am" gets `0 9`, so the whole
fleet lands on the same instant. When the request is approximate, pick an
off-minute — `57 8 * * *` rather than `0 9 * * *`. Jitter already offsets fires
by up to 30 minutes; an off-minute is still the bigger lever for a one-shot.

## When it must outlive the session

`/loop` needs the session open and the machine on. If the work genuinely has to
run unattended, say so and route:

- **Routines** — cloud, no machine needed, minimum interval 1 hour, fresh clone
  so no local files.
- **Desktop scheduled tasks** — local files and tools, survives restarts.
- **GitHub Actions** — a `schedule` trigger in CI.
- **Backgrounding the session** carries `/loop` tasks into a background session
  that keeps running without a terminal, which is the cheapest fix when the only
  problem is the terminal closing.
