# Failure modes, and what fixes each

Every row below was observed in real `/goal` runs — 114 `/goal` invocations
across 13 projects between 2026-06-07 and 2026-08-09, read from
`~/.claude/history.jsonl` together with the prompts the user typed immediately
afterwards. The follow-up prompt is the evidence: it is what someone types when
the goal has just failed them.

## 1. The run stops and reports nothing

**Evidence:** `resume` typed six times consecutively. "Has goal been met? if
not, why have you stopped." "Re-enforce your need to complete the goal, don't
stop until it's met." "are you still working?" "help me understand why you
stopped." "what are you waiting on? continue until goal complete."

**Cause:** the 8-block override. The turn is reported as `reason: "completed"`,
so nothing marks it as a failure. Secondary cause: the `impossible` verdict,
which clears the goal outright.

**Fix:** raise `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` in preflight; bound the run
with the guard's own `max_iterations` and `deadline` so it ends deliberately;
write every turn to the ledger so the stop has a recorded reason.

## 2. The condition is a slash-command name

**Evidence:** `/goal /create-fleet-goal` — 13 occurrences. Also
`/goal /goal` and `/goal` with no argument.

**Cause:** `/goal`'s argument is the condition, verbatim. `/goal /create-fleet-goal`
sets the condition to the eight-character string `/create-fleet-goal`. The main
model reads it as a directive and does run the command, so the run *starts*
correctly — but the evaluator is then asked, every turn, whether
"`/create-fleet-goal`" has been satisfied. It cannot be. The goal either blocks
until the cap overrides it or is judged impossible and cleared.

**Fix:** detect the shape on entry, say so in one line, and replace the live
condition with a real one derived from what the command was going to do.

## 3. Nothing was actually verified

**Evidence:** "The web app looks terrible, was it visually verified?" "I don't
feel like you're giving it a visual review." "The background colour of the
screens you just reviewed is `f6f7fb` but the mock is `ffffff` — how was this
missed given the diffs and harness?"

**Cause:** the evaluator judges narration. A run that writes "all screens now
match the mock" satisfies a condition about screens matching the mock, whether
or not they do.

**Fix:** the guard runs commands. Put the real gate in `verify[]` —
the test suite, the typecheck, the design-review script, the diff count — so the
turn cannot end while the command fails. Narration is not evidence; exit codes
are.

## 4. The run stalls waiting for the user

**Evidence:** "Ask me questions to help unblock you" (×6 across projects). "I
need to leave — any questions or do you have everything you need to complete the
goal." "Use your own judgement and recommendations instead of relying on answers
from me" — written *into* six separate goal conditions, which is the user
working around this by hand.

**Cause:** a goal does not pause for input, so a run that asks a question burns
a turn against the cap and asks again. Compounded by default permission mode:
`/goal` changes no permissions, so an unallowed command waits forever.

**Fix:** preflight the permission mode. Put an explicit blocked-item policy in
the brief — park the item with a written reason, carry on with everything that
does not depend on it, and collect questions for one batch at the end.

## 5. Delivery agents die and nobody notices

**Evidence:** `/workflow-resume` typed five times consecutively in one project,
and again in four others. "Resume the failed `proofhouse-ph008-ph0032-work`
workflow agent, utilising the existing session context so that it's not lost."
"what happened to the workflow that was meant to be working on fixing the
issues/gaps?"

**Cause:** a goal condition about work being complete is orthogonal to whether
the agents doing the work are alive. Both can be false at once and only one is
being watched.

**Fix:** add a liveness check to `verify[]`. The Stop hook input carries
`background_tasks` and `session_crons`; the brief should name the workflow-resume
path so the next-action brief can point at it.

## 6. No progress visibility

**Evidence:** "how's it going?" "how's the progress going?" "keep me updated on
its progress every 2 mins." "any improvements/gains?" "goal met?" "is the goal
met?" "has the goal been met?"

**Cause:** the only status surface is `/goal` with no argument, which shows the
condition, elapsed time, turn count and the evaluator's last reason — none of
which says what was finished.

**Fix:** the per-turn `GOAL-PROGRESS:` line in the condition, plus the ledger
the guard appends to. `scripts/status.sh` reads the ledger, so the question is
answered without interrupting the run.

## 7. Model and effort drift mid-run

**Evidence:** "although I see you using curl claude-opus when i mentioned using
sonnet for speed and cost." `/effort` typed immediately after `/goal` in five
separate sessions.

**Cause:** the condition names a model or effort in prose; nothing enforces it.

**Fix:** put the model and effort in the brief as configuration, and where a
runner is spawned by a script, pin it there rather than in prose.

## 8. Resource contention

**Evidence:** "Use another simulator, separate to the iPhone 16 Pro 18.2
simulator (which is in use by the customer app)." "Two metro's will be running,
you need to work-around that." "a ledger to keep track of which simulator is in
use by which workflow." "Force quit the metro bundler first and re-run."

**Cause:** two runs in one repo competing for one simulator, one port, one dev
server, one remote host.

**Fix:** the resource ledger section of the brief, and a preflight check for the
ports and processes it names.

## 9. Quota, rate limits and connection drops

**Evidence:** "The quota is no longer exhausted." "local cli via proxy is now
capped." `/rate-limit-options`. "I saw `API Error: Connection closed
mid-response`… it didn't attempt a retry."

**Cause:** an exhausted account or a dropped connection ends turns; the goal
keeps blocking against a wall until the cap overrides it.

**Fix:** treat these as bounds, not failures — the deadline in the state file
ends the run cleanly rather than letting it grind. Where a recovery path exists
(`workflow-resume`, a proxy rebind), name it in the brief so the next-action
brief can cite it.

## 10. Context exhaustion mid-run

**Evidence:** "`I'm at the end of my usable context` — you've not even used half
it. Continue with all remaining work." "/compact" typed mid-goal. "there's
plenty of context remaining, keep iterating" — written into three separate goal
conditions.

**Cause:** a run armed at high context spends its turns compacting, and
compaction drops the early transcript the evaluator needed.

**Fix:** preflight context headroom. Keep the worklist in the brief on disk
rather than in the transcript, so a compaction loses narration and not state.

## 11. The goal lands in the wrong session

**Evidence:** "I realise that my prompt relating to 9router and perch was in
this session but it should have been in the ~/Dev/perch session, is the running
workflow working on ~/Dev/perch?"

**Cause:** goals are session-scoped and invisible across sessions; eight
projects were being driven at once.

**Fix:** the state file records `cwd` and `session_id`, the guard matches on the
session id, and the report names the project. A goal armed in the wrong repo is
visible immediately rather than an hour later.

## 12. Skills named in the condition silently do not run

**Cause:** since Claude Code v2.1.196 a scheduled fire only invokes skills
Claude is allowed to invoke on its own. Built-in commands (`/model`, `/clear`),
skills marked `disable-model-invocation: true` — including the bundled
`/verify` and `/code-review` — skills withheld by `skillOverrides` or a `Skill`
deny rule, and MCP prompts all arrive as **plain text** instead of executing.
The run reads the text and carries on as though it had run the skill.

**Fix:** preflight resolves every skill named in the condition and reports which
are model-invocable. Where one is not, either call it from the main turn rather
than a fire, or replace it with the underlying command.

---

## The pattern behind all twelve

Ten of the twelve are the same shape: **the goal's model of the world and the
world itself diverged, and nothing checked.** The condition said work was done,
or agents were alive, or the skill had run, and the only thing that could have
noticed was a small model reading a story the run told about itself.

The fix that generalises is not a better condition. It is putting a command
between the run and the exit.
