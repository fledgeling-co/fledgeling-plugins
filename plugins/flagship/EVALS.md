# EVALS — flagship

## No comparative eval was run, and this section says so rather than omitting it

The `create-skill` pipeline calls for a no-skill baseline and a blind cross-family
judge panel. **Neither ran.** Three reasons, all of them real rather than
convenient:

1. The skill was built *inside* the run it distils — sixteen live sessions on the
   machine at the time — so spawning a benchmark fleet beside them would have
   contended for the exact resource the skill exists to ration.
2. The out-of-family lanes were down. Codex was usage-limited for five days, one
   lane returned `402 balance exhausted`, one was not installed at all, and the sole
   survivor was a one-shot that cannot execute anything. A blind panel needs
   heterogeneous judge families; there was one family available, and it was the
   writer's own.
3. The user asked for a repeatable skill, not a benchmark.

Inventing numbers here would have been the same failure the skill is about, so
there are none. What follows is what was actually verified.

## What was verified mechanically

**`scripts/machine_read.py` runs end to end** against this machine and returns a
correct, honest read: `harbourmaster` auto-resolved to the source tree,
`heavy_slot_token: 3` derived as `min(3, available berths)`, thermal sampled with
the pessimistic verdict kept, disk reported at 13.75% free from `pressure.py`
rather than from `/`, and the berth block carrying an explicit
`"MEANS": "registered governor-run claims, NOT machine load"` so the number cannot
be mistaken for capacity. The disk advice fired at the right threshold.

**`scripts/roster.py` runs end to end** and found **16 sessions, 16 live**, each
with branch, worktree count, `core.hooksPath` and origin. It immediately answered a
portfolio question that had been asked of sessions one at a time over the preceding
hour — every `core.hooksPath` is relative (`.husky/_`) where set, so a shared-config
hazard found in one repo does not apply anywhere else. **That is the strongest
evidence available for the skill's central claim**: the script produced in one call
a cross-session fact that eight individual conversations had not established.

**Both scripts are read-only** and neither mutates any repository or registry.

## What is unproven

- **Whether the skill beats no skill.** Untested. The honest prior is that its
  *rules* were each derived from a measured failure, and its *coordination value*
  rests on one evening's evidence rather than a controlled comparison.
- **Whether `scripts/spawn_session.py`'s tab route works as lifted.** The mechanism
  is `recover-claude-code`'s, which is proven for *resuming*; the new-session
  variant (no `--resume`) has not been driven. Dry-run first, and treat a tab that
  did not appear as the expected failure rather than a surprise — the keystroke path
  fails silently, which is why the skill insists on confirming.
- **Whether the R1–R5 router reduces escalations in practice.** It cut one
  evening's queue from ~20 to ~10 by inspection. That is an anecdote, not a rate,
  and the operator's own 36% override figure has not been re-measured across the
  ~714 questions since it was taken.

## The three tasks that would settle it

1. **Hand two sessions the same twelve-repo portfolio**, one briefed with this skill
   and one without, and grade on structural assertions: was a concurrency number
   measured or invented; was a cross-session finding propagated; was an
   authorisation relayed; did any peer refuse an instruction.
2. **Replay the reckon-defect case.** Give a conductor three sessions' reports, one
   containing a tool defect, and check whether it reaches the other two. That is the
   skill's core claim and it is cheap to test.
3. **Drive `spawn_session.py --dry-run` then for real**, and confirm the tab exists
   and the brief landed as a first turn rather than as an auto-submitted "continue".

## Process note

Phase 0 answered from the session's own material; the two genuinely open forks
(name, placement) went to the user via `AskUserQuestion` and were answered
`flagship` and its own plugin. **The Phase 4 icon-concept checkpoint has not been
asked**, and no icon or banner exists yet — so this plugin is not yet
catalogue-complete, and `site/scripts/build-catalogue.mjs` will say so.

## Added in 1.5.0 — measured in live conduct, 23 Aug 2026

No comparative panel ran for these either; the measurements below are from a live
conducting night with 19–23 sessions on the machine, which is the population the
skill exists for. Each rule in this release is the correction of a failure that
night, and each carries the number that produced it:

- **Finished-and-silent is a distinct idle shape.** Six sessions completed
  dispatched work and reported nothing, some for hours, while the conductor read
  their quiet as progress and the operator asked twice why the machine was idle.
  One three-line status chase recovered four answers inside minutes. The dispatch
  ledger and the completion-report obligation exist to make that recovery the
  default rather than an accident.
- **Prompt-parked sessions cannot be reached by dispatch.** Three sessions each
  sat through two unanswered chases while blocked at Relay's interactive
  account-switch prompt, where a message queue is never reached. The operator's
  in-tab `continue` was the only unstick. Hence: escalate after two chases, never
  three.
- **Ledger movement, not roster quietness, distinguishes working from stopped.**
  Measured both directions: an idle-looking row was mid-86-commit reconciliation;
  a genuinely stopped row had asked its user a question that was its own to
  answer. The inverse holds too — a session that reads forty files and closes a
  row as stale commits nothing, so absent movement is *unknown*, not idle.
- **The drained tier refills before it retires.** One repo at a complete 54-row
  ledger ran intake in the evening and shipped all three new briefs, verified,
  the same night. Two other "drained" summaries that evening sat on top of named,
  buildable rows the sessions' own ledgers held. Retirement is the operator's
  call after declining refill; intake under a utilisation directive is the
  default.
- **Condition-gated items met their conditions unmet with.** A ten-minute
  undisturbed-CPU measurement stayed parked for days while the host idled under
  0.6 per core twice in one evening; the condition and the dispatch never met
  until the conductor went looking. The ledger now names conditions beside the
  dispatches waiting on them.
- **Spawn verification moved from tab count to session file.** A successful
  spawn measured `tabs_after: 1` because the AppleScript probe counts the
  frontmost window's tab group; the session itself existed. Session file plus
  socket is the check that cannot mislead.
