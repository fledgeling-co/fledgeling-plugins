# Starting work: workflow, subagent, or a session of its own

Three planes. Pick by what the work needs to *own*, not by what is nearest to hand.

## Workflow

A script owns the loop; agents do the work; results come back as data. Right for
deterministic fan-out — one runner per item, schema-enforced output.

- Slot count comes from `harbourmaster`, re-read on **every refill**, never fixed. Pressure
  moves under a long run.
- `agent()` returns `null` on a terminal API error with **zero retries**, and the run still
  reports `completed`. A null is a death, not a completion. `.filter(Boolean)` drops the
  evidence that something died.
- `Promise.race` over an empty map **never settles**. If nothing is ready and nothing is
  running, park the remainder with a reason and break.
- **Workflow-inner agents cannot be revived.** `SendMessage` never reaches them and
  `ListAgents` does not list them. So a mid-flight correction is impossible on this plane — it
  has to travel forward to the verifier instead, with the omission attributed to the
  orchestrator rather than the runner.

## Subagent

Right for wide reading and search where you want the conclusion rather than the files. Costs
context and rate limit, not cores. Cap the fan-out at four when surveying repos.

## A session of its own — a Ghostty tab

Reach for this when the work needs its own context window, its own channel to the user, and
possibly its own fleet. A tab-launched session is a real peer: it appears in `ListAgents`, it
can be messaged, it can be corrected mid-flight, and it outlives your terminal.

`recover-claude-code` owns the hardened mechanism. Use `scripts/spawn_session.py` here, which
lifts it. The parts that are load-bearing are load-bearing because they failed silently first:

- **A new tab comes from the File menu, not a keystroke.** `ghostty +new-window` reports
  success and does something else. The AppleScript menu route is the one that works.
- **The brief is passed as a command-line argument**, which submits it as a real first turn.
- **For a new session there is no `--resume`, and never `--fork-session`.** (When *resuming*,
  the original session id is mandatory: a workflow journal resolves from the session id at
  resume time, so forking makes every journal unreachable — silently.)
- Write the brief and a bootstrap script to disk, then type one `source <script>` line. That
  keeps quoting and shell metacharacters out of the keystroke path entirely.
- **Dry-run first.** The keystroke route fails silently, so confirm the tab exists rather than
  assuming the command that opened it worked.

### Briefing a session you spawn

Give it the complete spec up front. Opus follows literally and will widen scope otherwise.
State the scope plainly, leave out verification scaffolding, cap its own delegation explicitly,
and calibrate the deliverable length — effort controls thinking, not visible length.

Include, always: the resolved `harbourmaster` scripts path (a spawned agent does not reliably
inherit `CLAUDE_PLUGIN_ROOT`, so a runner that re-derives it finds nothing and reports the
governor missing on a machine that has it); the lane inventory as measured, not as advertised;
the standing constraints on push, publish and deploy; and **who it reports to, with the
explicit note that its own channel to its user remains its own.**

### One thing to check before you spawn anything for a repo

`git ls-remote origin`. A repo can carry an origin URL for a repository that has **never been
created** — measured: 453 commits, an origin pointing at a name that returns `Repository not
found` while the same key authenticates fine elsewhere, and no `origin/main` ref, which is
indistinguishable from a remote nobody has fetched. Nobody found out because nobody tried.
Check before ordering a push, not after.

## Ending
A session that finishes should hand over rather than vanish: what it holds, where, and what is
owed. An orphan whose parent exited is recoverable only if it said so — one did, and its branch
was picked up; two others were simply gone.
