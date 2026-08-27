# Failure modes, and what fixes each

Every row below was observed in real runs. Modes 1-15 come from 114 `/goal`
invocations across 13 projects between 2026-06-07 and 2026-08-09, read from
`~/.claude/history.jsonl` together with the prompts typed immediately afterwards;
the follow-up prompt is the evidence, because it is what someone types when the
run has just failed them.

Modes 16-18 come from a second corpus: 22 better-goal runs across 14 projects
between 2026-08-13 and 2026-08-27, read from their own state files, ledgers and
session transcripts. That corpus is why the harness now registers four hook
events rather than one.

## 1. The run stops and reports nothing

**Evidence:** `resume` typed six times consecutively. "Has goal been met? if
not, why have you stopped." "Re-enforce your need to complete the goal, don't
stop until it's met." "are you still working?" "help me understand why you
stopped." "what are you waiting on? continue until goal complete."

**Cause:** the 8-block override, which applies to any Stop hook. The turn is
reported as `reason: "completed"`, so nothing marks it as a failure. Secondary
cause when composed with `/goal`: the `impossible` verdict, which clears the
built-in goal outright.

**Fix:** `arm.sh` raises `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` and `preflight.sh`
blocks when it is unset; `max_iterations` and `deadline` end the run
deliberately; every turn writes a ledger row, so a stop always has a recorded
reason.

## 2. The condition is a slash-command name

**Evidence:** `/goal /create-fleet-goal` — 13 occurrences. Also `/goal /goal`
and `/goal` with no argument.

**Cause:** `/goal`'s argument is the condition, verbatim. `/goal
/create-fleet-goal` sets the condition to that literal string. The main model
reads it as a directive and does run the command, so the run *starts* correctly
— but the evaluator is then asked every turn whether "`/create-fleet-goal`" has
been satisfied. It cannot be, so the run either blocks until the cap overrides
it or is judged impossible and cleared.

**Fix:** the harness takes an intent, not a condition, and derives gates from it.
When someone types this shape at `/goal`, name it in one line and arm real gates
instead.

## 3. Nothing was actually verified

**Evidence:** "The web app looks terrible, was it visually verified?" "I don't
feel like you're giving it a visual review." "The background colour of the
screens you just reviewed is `f6f7fb` but the mock is `ffffff` — how was this
missed given the diffs and harness?"

**Cause:** a prompt-hook evaluator judges narration. A run that writes "all
screens now match the mock" satisfies a condition about screens matching the
mock, whether or not they do.

**Fix:** the guard runs commands. Put the real gate in `verify[]` — the test
suite, the typecheck, the design-review script, the diff count — so the turn
cannot end while the command fails. Narration is not evidence; exit codes are.

## 4. The run stalls waiting for the user

**Evidence:** "Ask me questions to help unblock you" (×6 across projects). "I
need to leave — any questions or do you have everything you need to complete the
goal." "Use your own judgement and recommendations instead of relying on answers
from me" — written *into* six separate goal conditions, which is the user
working around this by hand.

**Cause:** an armed run does not pause for input, so a run that asks a question
burns a turn and asks again. Compounded by default permission mode: arming
changes no permissions, so an unallowed command waits forever — mid-turn, where
the guard never sees it.

**Fix:** preflight the permission mode; the watcher's STALL catches the wait from
outside. Put an explicit blocked-item policy in the brief — park the item with a
written reason, carry on with everything that does not depend on it, and collect
questions for one batch at the end.

## 5. Delivery agents die and nobody notices

**Evidence:** `/workflow-resume` typed five times consecutively in one project,
and again in four others. "Resume the failed `proofhouse-ph008-ph0032-work`
workflow agent, utilising the existing session context so that it's not lost."
"what happened to the workflow that was meant to be working on fixing the
issues/gaps?"

**Cause:** a condition about work being complete is orthogonal to whether the
agents doing the work are alive. Both can be false at once and only one is being
watched. Worse, a run that dies mid-turn never reaches its Stop hook at all, so
the guard is not merely wrong — it is never asked.

**Fix:** `watch.sh` runs outside the turn loop and emits STALL when the run stops
breathing, naming the recovery path. Add a liveness command to `verify[]` as
well; the Stop hook input carries `background_tasks` and `session_crons`. The
watcher covers only the deaths that happen while its own session lives — mode 17
is what covers the rest.

## 6. No progress visibility

**Evidence:** "how's it going?" "how's the progress going?" "keep me updated on
its progress every 2 mins." "any improvements/gains?" "goal met?" "is the goal
met?" "has the goal been met?"

**Cause:** the only status surface was `/goal` with no argument — condition,
elapsed time, turn count and the evaluator's last reason, none of which says what
was finished.

**Fix:** `scripts/status.sh` reads the ledger, so the question is answered from a
file without interrupting the run or costing it a turn. Asking the run itself is
the expensive way to find out.

## 7. Model and effort drift mid-run

**Evidence:** "although I see you using curl claude-opus when i mentioned using
sonnet for speed and cost." `/effort` typed immediately after `/goal` in five
separate sessions.

**Cause:** the intent names a model or effort in prose; nothing enforces it.

**Fix:** put the model and effort in the brief as configuration, and where a
runner is spawned by a script, pin it there rather than in prose.

## 8. Resource contention

**Evidence:** "Use another simulator, separate to the iPhone 16 Pro 18.2
simulator (which is in use by the customer app)." "Two metro's will be running,
you need to work-around that." "a ledger to keep track of which simulator is in
use by which workflow." "Force quit the metro bundler first and re-run."

**Cause:** two runs in one repo competing for one simulator, one port, one dev
server, one remote host.

**Fix:** the resource ledger section of the brief, and `preflight.sh --ports
--procs` for what it names.

## 9. Two runs, one state file

**Evidence:** "utilise a different goal harness json file as another is using the
existing one."

**Cause:** a single `.claude/goal-state.json` per repo. A worktree and its
parent, or two features in flight, arm over each other — the second run's gates
replace the first's, and the first run then verifies work it was never given.

**Fix:** state is per-slug at `.claude/goals/<slug>.json`. The guard iterates
every file and evaluates only those whose `session_id` matches the hook payload,
so runs coexist and each stays inert in sessions not driving it.

## 10. Quota, rate limits and connection drops

**Evidence:** "The quota is no longer exhausted." "local cli via proxy is now
capped." `/rate-limit-options`. "I saw `API Error: Connection closed
mid-response`… it didn't attempt a retry."

**Cause:** an exhausted account or a dropped connection ends turns; the run keeps
blocking against a wall until the cap overrides it.

**Fix:** treat these as bounds, not failures — the deadline ends the run cleanly
rather than letting it grind, and the watcher reports the stall while it is
happening rather than after. Where a recovery path exists (`workflow-resume`, a
proxy rebind), name it in the brief.

## 11. The same failure, paid for again and again

**Evidence:** "49M tokens is insane." Five of twelve of the heaviest sessions —
91% of input between them — re-sent the same unmet condition and the same failing
set turn after turn, paying the whole accumulated prefix each time.

**Cause:** a guard that re-emits identical output has no way to distinguish a run
making progress from one going in circles, and every block re-bills the session.

**Fix:** the guard fingerprints the failing set. An identical fingerprint
escalates the reason and withholds the repeated gate output; past `stuck_after`
(default 3) it disarms and records `stuck_on`. Changed sets carry a delta line
instead. The watcher applies the same principle from outside — transitions only,
exponential backoff on a persisting stall.

## 12. Context exhaustion mid-run

**Evidence:** "`I'm at the end of my usable context` — you've not even used half
it. Continue with all remaining work." "/compact" typed mid-goal. "there's plenty
of context remaining, keep iterating" — written into three separate conditions.

**Cause:** a run armed at high context spends its turns compacting.

**Fix:** keep the worklist in the brief on disk rather than in the transcript, so
a compaction loses narration and not state. The guard reads the file, not the
conversation, so it is unaffected by a compaction.

## 13. The run lands in the wrong session

**Evidence:** "I realise that my prompt relating to 9router and perch was in this
session but it should have been in the ~/Dev/perch session, is the running
workflow working on ~/Dev/perch?"

**Cause:** session-scoped state, invisible across sessions; eight projects being
driven at once.

**Fix:** the state file records `cwd` and `session_id`, the guard matches on the
session id, and the arm report names the project. A run armed in the wrong repo
is visible immediately rather than an hour later.

## 14. Teardown is manual, and easy to forget

**Evidence:** "Delete the stop hooks." "Cancel the scheduled task."

**Cause:** a harness that arms itself but leaves the hook and the raised block
cap in settings after the run ends. The next unrelated session inherits both.

**Fix:** `disarm.sh` removes the hook and restores the prior block cap once no
run in the repo is still armed, and says how to stop the watcher. The guard also
disarms itself on met, stuck, deadline and max_iterations, so the common case
needs no teardown at all.

## 15. A skill named in an instruction silently does not run

**Cause:** built-in commands (`/model`, `/clear`), skills marked
`disable-model-invocation: true` — including the bundled `/verify` and
`/code-review` — skills withheld by `skillOverrides` or a `Skill` deny rule, and
MCP prompts cannot be invoked by the model. Told to run one, the run reads the
instruction and carries on as though it had.

**Fix:** `preflight.sh --skills` resolves every skill the brief expects the run to
invoke and reports which are model-invocable. Where one is not, make it a gate
command instead, or name the plugin-qualified skill.

## 16. The guard was registered and never ran

**Evidence:** *"The stall signal is the known mechanical gap — the guard's Stop
hook was registered mid-session and Claude Code reads hook config at session
start, so nothing has been appending rows while I've been working."* And, from
the same run: *"proven by running `guard.sh` by hand, which emitted…"* — the
script was correct; it was never invoked.

**Cause:** Claude Code's settings watcher watches only directories that already
held a settings file when the session started, so a hook written into an empty
`.claude/` mid-session never loads. Both cases look identical after the write.

**Fix:** `arm.sh` records `settings_preexisted` before writing and prints which
case it is; `preflight.sh` warns on it; the state carries `hook_live: "unproven"`
until the guard's first firing stamps it `proven`, and `status.sh`, `watch.sh`
(`NOTLIVE`) and `sentinel.sh` all report the unproven state. The recovery is the
user opening `/hooks` once or restarting — a UI menu the model cannot open.

## 17. The run died on an API error, and the guard was never asked

**Evidence:** a run whose transcript ends `API Error: Connection refused`,
interrupted by the user, with its state reading `armed: true` at turn 17 of 800
fourteen days later. A second run ended mid-tool-result with its ledger eleven
minutes old — inside the stale threshold — so no STALL was ever emitted, and sat
armed for six days.

**Cause:** `StopFailure` fires *instead of* `Stop` when an API error ends a turn,
so the guard never runs. `Monitor` dies with the session, so the watcher that
would have noticed is inside the thing that died — and where it survived long
enough to speak, it spoke into a session that could no longer act.

**Fix:** `guard.sh` is registered on `StopFailure` and `SessionEnd` as well as
`Stop`, so both endings write a ledger row and a distinct `end_reason` instead of
leaving the run armed. `sentinel.sh` runs on `SessionStart` and reports armed
runs whose session is gone to the next session that opens the repo, which is the
first mechanism here that outlives the run it watches.

## 18. The watcher woke a run that was working

**Evidence:** *"Watcher woke me — the ledger went stale because my turn ended"*,
twice in one run. Across 14 runs, 56 STALLs were delivered and 34 arrived within
ten minutes of an assistant message, 22 of them in the same minute.

**Cause:** a fixed 25-minute staleness threshold read from the ledger alone,
against runs whose median gap between ledger rows was 28.5 minutes in one case
and 95.7 in another. A long turn and a dead run look the same from the ledger.

**Fix:** the watcher reads the session transcript's mtime and stays silent while
the session is writing, and derives its threshold from the run's own median turn
length rather than a constant.

---

## The pattern behind all eighteen

Most are the same shape: **the run's model of the world and the world itself
diverged, and nothing checked.** The condition said work was done, or agents were
alive, or the skill had run, and the only thing that could have noticed was a
small model reading a story the run told about itself.

The fix that generalises is not a better condition. It is putting a command
between the run and the exit, a second one outside the turn loop for the turns
that never end, and a third outside the session entirely — because the last three
modes are all the same discovery, that every part of a harness living inside the
run dies with it.
