# Changelog

## 2.2.1 - 2026-09-01

Refreshes `gemini.md` against a `SKILL.md` that had changed since it was written. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 2.2.0 - 2026-08-28

Read against 22 real runs armed between 2026-08-13 and 2026-08-27, across 14
projects, from their state files, ledgers and session transcripts. Three
mechanical faults accounted for every case of a run that stopped without its
goal being met.

### The guard was often registered and never loaded

Claude Code's settings watcher only watches directories that already held a
settings file when the session started. `arm.sh` writes the Stop hook
mid-session, so arming into an empty `.claude/` wrote it correctly and never
fired it. The wording is Anthropic's own, from the `update-config` skill inside
the 2.1.247 binary: *"the settings watcher isn't watching `.claude/` ... Tell
the user to open `/hooks` once (reloads config) or restart, you can't do this
yourself."* One run on 26 August proved it in-session by piping a payload to
`guard.sh` by hand and getting the block decision the harness had never produced
on its own, then spent the rest of its life running the gates manually.

`arm.sh` now records `settings_preexisted` before it writes and prints which
case it is, `preflight.sh` warns on it, and the state carries
`hook_live: "unproven"` until the guard's first real firing stamps it `proven`.
A Stop hook fires after the turn, so that first ledger row is the only proof
available. `status.sh`, `watch.sh` (`NOTLIVE`) and the new `sentinel.sh` all
report the unproven state rather than assuming the hook works.

### Three more events, because a Stop hook misses two endings and a Monitor dies

`StopFailure` fires instead of `Stop` when an API error ends a turn, so the
guard was never asked at all: one run read `armed: true` at turn 17 of 800 for
fourteen days after `API Error: Connection refused`, and a second sat armed for
six days after its session ended mid-turn with the ledger eleven minutes old,
inside the stale threshold.

`guard.sh` is now registered on `StopFailure` and `SessionEnd` as well as
`Stop`. Neither can instruct the run (`StopFailure`'s output and exit code are
ignored by Claude Code), so both record: a ledger row and a distinct
`end_reason`, with three consecutive API-error turn ends disarming as
`api_error`. `sentinel.sh` runs on `SessionStart` and reports armed runs whose
guard never fired, armed runs gone cold while their session is silent, and
endings nobody has been told about, once each. It is the first part of the
harness that outlives the run it watches.

### Liveness from the transcript, not the ledger

Of 56 `STALL` notifications delivered across 14 runs, 34 arrived within ten
minutes of an assistant message and 22 of those in the same minute. Two turns in
one run answered with *"Watcher woke me, the ledger went stale because my turn
ended."* Each wake re-bills the whole session prefix.

`watch.sh` now reads the session transcript's mtime, measured at 6 seconds old
mid-turn on a live session, and stays silent while the session is writing. Its
stale threshold is three times the median of the run's last ten inter-row gaps,
floored at 25 minutes and capped at 240, because the fixed 25 was shorter than
the median turn length of several real runs (28.5 minutes on one, 95.7 on
another). `--stale N` pins it; `--alive 0` turns the transcript check off.

### Two registration bugs

`arm.sh` matched existing hook registrations by exact path, and the path carries
the plugin version, so a bump registered a second guard beside the first:
`graft` held both 2.0.0 and 2.1.0, and `goal-graft-instruments.ledger.md`
recorded 24 rows for 12 turns with every gate running twice. It now matches on
the script, the way `disarm.sh` already did.

`prior_block_cap` was recorded on every arming, so the second run in a repo
recorded the harness's own raised cap as the user's and `disarm.sh` restored it.
It is recorded only on the first arming now, and teardown leaves settings as
they were.

### The stuck detector counts the failing set, and only says so

The output fingerprint resets whenever a count, a path or an elapsed time moves,
so `orderly` recorded 88 of 137 turns at `repeat ×1` while the same two gates
were red on 73 of them, and ran to its 120-iteration bound with the goal unmet.
The failing set is now counted separately and named in the block reason from
`set_notice_after` turns (default 10).

It never disarms. Across 24 ledgers, 29 streaks of an identical failing set ran
8 turns or longer and then cleared, the longest 57 turns of
`ledger-drained, orchestrator-drained, worktrees-clean` on a backlog being
worked through item by item. A long streak is the normal shape of this work, so
disarming on one would kill healthy runs.

## 2.1.0 - 2026-08-23

`gemini.md`, the gated override file for a Gemini runner: the finish line as a
counted worklist, every gate proved able to fail before arming, and the state
file and hook registration read back off disk before the run is reported as
armed. Part of a repo-wide pass across 63 skills.

## 2.0.0 - 2026-08-13

Renamed from `goal-harness`, which was a hardening layer over `/goal`. This
version arms a mechanism it creates itself and nothing depends on the built-in:
a `command` Stop hook judged by exit code rather than by a small model reading
the transcript, plus a `Monitor` stall watcher for the failure a Stop hook
structurally cannot see. State moved to per-slug `.claude/goals/<slug>.json`
after two runs in one repo collided over the shared file, and `disarm.sh`
restores the block cap `arm.sh` raised.
