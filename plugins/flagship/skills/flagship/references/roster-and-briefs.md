# The roster, and the brief that opens a coordination

## Build the roster from three sources

`ListAgents` for who is addressable, `~/.claude/sessions/<PID>.json` for liveness and cwd, and
git per repo for what is actually held. `scripts/roster.py` joins them.

**Reconcile ownership by cwd and pid, never by name.** A session appears to peers under a name
its own conductor does not use internally. Two sessions were established as one conductor's own
workers only after it counted processes per worktree (`pgrep -x claude` plus `lsof` on cwd)
rather than trusting the names it had been shown. Both had looked like orphans.

**Ask each session for its own state. Do not derive it.** Every figure taken from `ARMADA.md`
in one evening's survey was wrong in some detail, and one project's entry was stale in the
*index* while correct in the *detail* — with the index being what an orchestrator reads first.

## The opening brief

Cover these, in this order, and keep it to what the session needs rather than what you know:

1. **Who you are and what you are doing.** Name the skill and the scope.
2. **What you already know about them**, with figures and their provenance. A session that sees
   you have read its reckoning and its branch state answers at a different level than one
   handed a form.
3. **What you want back**: identity and branch state, remaining work from its own ledger rather
   than a generated headline, artifact reconciliation against `git worktree list` and
   `git branch --list 'ai/*'`, its decision-class items batched, and fleet-readiness.

**Every dispatch carries its own report obligation.** State what to send back when the work
is done — silence is not a state, and the three-line shape (done / in hand / parked-by) is
the default. If the dispatch offers a heavy-work token, state the no-answer default in the
same breath: no answer means no token, proceed serially. A session given work without a
named report will finish and wait, because from inside, finished-and-waiting looks like
compliance.
4. **The standing constraints.** The resolved `harbourmaster` scripts path (hand it down —
   a spawned agent does not reliably inherit `CLAUDE_PLUGIN_ROOT`, and a runner that re-derives
   it reports the governor missing on a machine that has it), exit 75 meaning wait and do other
   work rather than loop, judgement going out of family, and what must not happen: no push, no
   publish, no deploy.
5. **The channel.** Ask them to route coordination to you. **Say explicitly that their own
   channel to their user remains theirs** — otherwise they will refuse the whole brief, and be
   right to.
6. **Ask for the state and the next step in a few lines, not a ledger.**

## What a good reply looks like

The best replies in one evening all did the same four things, and it is worth asking for them:
corrected at least one of the conductor's premises with a measurement; reported from a ledger
rather than a report; separated what they had *proved* from what they had *not recorded*; and
named what a rejected option would have been better at when they declined something.

The worst thing a reply can do is agree. A session that accepts a wrong figure propagates it.
