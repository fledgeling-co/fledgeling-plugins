# Changelog

## 2.2.0 - 2026-08-28

### A loop cannot report that its own watcher died

`Monitor` runs the watcher in the session's shell, so it ends when the session
does, while the state file goes on reading `armed: true` with nobody told. The
sibling `better-goal` harness left one run in that state for fourteen days after
an API error and another for six days after its session ended mid-turn.
`better-loop` had the same exposure and no mechanism to catch it.

`watch.sh` now stamps `last_poll_at` on every poll, and `status.sh` reports a
loop whose last poll is older than three intervals as stopped rather than
watching. `sentinel.sh`, registered by `arm.sh` on `SessionStart`, tells the
next session that opens the repo which loops died, once each, and says nothing
when every loop is polling.

The heartbeat is an explicit epoch rather than the state file's mtime, because
the sentinel's own `reported_dead` flag rewrites the file and made a dead loop
read as freshly polled a second later.

Unlike a `Stop` hook, a `SessionStart` hook does not need to load in the session
that registered it, so the settings-watcher caveat that affects `better-goal`
does not apply here and no `/hooks` reload is needed.

### One settings change, where there were none

This is the first thing the skill writes outside `.claude/loops/` and
`docs/loops/`. `disarm.sh` removes the hook once no loop in the repo is still
armed, and `arm.sh --no-sentinel` skips registering it, at the cost of nothing
reporting a loop whose session dies. The README and SKILL.md say so rather than
claiming the skill leaves nothing in settings.

`arm.sh` also records the arming session's id, so `status.sh` and the sentinel
can name which session a stopped loop belonged to.

## 2.1.0 - 2026-08-23

`gemini.md`, the gated override file for a Gemini runner: the mechanism table,
the tick protocol's sections and the step 6 report as counted ledgers, with the
four bounds read back off the armed state file rather than off the brief. Part
of a repo-wide pass across 63 skills.

## 2.0.0 - 2026-08-13

Renamed from `loop-harness`, which was a hardening layer over `/loop`. This
version replaces the session cron with a watcher that polls a probe outside the
session: polling costs nothing, only a change wakes anything, the wake carries
the delta rather than the state, and `--tick-cmd` can dispatch the tick detached
so the session is never woken at all. The defect that prompted it: five of the
twelve heaviest measured sessions re-sent the same unmet condition and the same
failing tasks turn after turn, accounting for 91% of input between them.
