---
name: recover-claude-code
description: >-
  Bring back Claude Code sessions, workflows and subagents that a crash interrupted, with the context they already had instead of restarting them from scratch. Use whenever a terminal, Ghostty, iTerm or the machine crashed or was force-quit and sessions were lost; when someone asks to recover, restore, reopen or resume their sessions, tabs, windows or agents; when a session was killed mid-task and its background workflows never reported; when work was in flight across several repos at once and the terminal died; after a jetsam or out-of-memory kill; or when a previous recovery attempt cold-started fresh agents and lost what they had already worked out. Also use before resuming any session by hand after a crash, because resuming the wrong way orphans a workflow's journal silently and a session that is still running must not be resumed twice. Finds every session touched in a chosen window across all project directories, separates the genuinely dead from the still-running, reopens each dead one in its own terminal tab at its original working directory under its original session id, and restores its interrupted workflow runs and subagents by promoting their transcripts rather than replaying their prompts.
---

# Recovering Claude Code after a crash

When a terminal process dies, the sessions inside it stop mid-sentence. Their transcripts,
their workflow journals and their subagents' accumulated context all survive on disk — the
work is not lost, it is unattached. This skill reattaches it.

The failure worth designing against is not losing the work. It is **recovering it badly**:
starting a replacement agent on the same prompt with none of its predecessor's context, so
it re-reads the same files, re-derives the same findings, and sometimes re-does work that is
already committed. A recovery that cold-starts looks like it worked and quietly costs an
hour.

Deliver what was asked, at the scope intended: recover the sessions that are actually dead
and the work they were actually owed. Resist widening into fixing the underlying work.

## 1. See what is there

```bash
python3 scripts/scan_crashed.py --minutes 60          # the default window
python3 scripts/scan_crashed.py --minutes 180 --json  # for the tab driver
python3 scripts/scan_crashed.py --project perch       # one project
```

Read-only. It reports, per session: whether it is live, its working directory, its peer
name, whether it was cut mid-turn, and for each workflow run how many `agent()` calls
returned against how many started, which agents were mid-tool, and where the run's script
is on disk.

It separates three states, and only one of them is yours to touch:

| State | What it means | What to do |
|---|---|---|
| `LIVE`, attached to a tty | in `~/.claude/sessions/` under a running pid, in a terminal tab | nothing — see §3 |
| `LIVE`, no tty | outlived the terminal that owned it | stop it first — see §2 |
| `WRITING` | no registry entry but the transcript moved in the last two minutes | wait, then rescan |
| `STOPPED` + interrupted work | dead, with a run or an agent that was still going | recover it |
| `STOPPED` + nothing interrupted | idle when it died, or owed only long-abandoned runs | leave it, or `--include-idle` |

The last row is a real distinction rather than a tidy one. A session that has been running for
days accumulates journals from runs abandoned long ago, and every one of them still reads as
"owed a result" — one carried 21, of which 3 belonged to the crash. The scan reports all of
them; `open_tabs.py` counts a run as interrupted only when one of its agents was still writing
within `--fresh-within` seconds of the process dying, so the recovered session is pointed at
the work that was actually cut rather than at a graveyard.

## 2. Stop the sessions that outlived the terminal

A terminal dying does not kill the sessions inside it. Measured on 2026-08-22: a Ghostty crash
took 22 sessions off the screen, and four were still running twenty minutes later — one of them
mid-run, re-arming a `caffeinate` child to keep the machine awake. Recovering on top of a
survivor gives two processes appending to one transcript and two agents on one worktree.

```bash
python3 scripts/kill_orphans.py                 # read-only
python3 scripts/kill_orphans.py --kill          # SIGTERM, so transcripts flush
```

The test is the controlling terminal, not parentage: a session in a healthy tab is parented to
`login`, and so is every other tab, so "not in my own process tree" would condemn all of them.
A session attached to a tab has a tty; one whose terminal died reports `??`. The calling
session is excluded by ancestry too.

Three things it will not do without being told, each for a reason:

- **A detached session that is `busy` is left alone.** Claude Code runs genuine background
  sessions with no terminal, and they are indistinguishable from a survivor by tty alone.
  `--all-detached` includes them once you have decided they are debris.
- **A session with no transcript is left alone.** A supervisor that keeps a warm pool registers
  sessions that were never used; they look exactly like crashed ones and come straight back.
  An idle slot writes nothing, so leaving it costs nothing.
- **SIGTERM, not SIGKILL.** The flush is what makes the next scan's brief accurate. `--force`
  escalates only what is still alive after `--wait`.

If a killed session reappears under a new pid, something is supervising it and killing again
just restarts the loop. Find the supervisor first — on this machine it was Relay
(`~/Dev/perch/macos/dist/Relay.app`), which respawned its warm-pool slots within seconds of the
Claude Code daemon being stopped.

**Then scan again.** Stopping a survivor is what turns it into a recoverable session: a run
that was still live held no interrupted work until its process died, and the busy egress
session on 2026-08-22 only became a recovery target after it was stopped.

## 3. Never touch a live session

A session in the registry under a running pid is being used, however long it has been quiet
— a runner can work for forty minutes without writing to the parent transcript. Resuming it
gives you two processes appending to one transcript and two agents on one worktree.

The scanner's liveness comes from `~/.claude/sessions/<PID>.json`, which carries
`sessionId`, `cwd`, `pid`, the peer `name` and a `status`. That file is the authority.
Confirm with `ListAgents` before acting if you want a second source — its names are the same
ones. Two probes that look plausible do not work: `ps` output does not contain the session
id, and the scratchpad directory is named by a per-process id that stops matching the
session id as soon as a session has been resumed once.

## 4. Reopen each dead session

```bash
python3 scripts/scan_crashed.py --minutes 60 --json > /tmp/scan.json
python3 scripts/open_tabs.py --scan /tmp/scan.json --dry-run   # read it first
python3 scripts/open_tabs.py --scan /tmp/scan.json
```

Per session it writes a brief and a bootstrap script into a working directory, opens a
Ghostty tab, and types one `source <script>` line. The script `cd`s to the session's
original working directory and runs:

```bash
claude --dangerously-skip-permissions --resume <session-id> "$(cat <brief>)"
```

Three things about that line are load-bearing:

- **The original session id, and never `--fork-session`.** A workflow's journal lives at
  `<project>/<SESSION-UUID>/subagents/workflows/<runId>/`, resolved from the session id at
  resume time. Fork it and every journal this recovery is trying to reach becomes
  unreachable, silently.
- **The brief is passed as an argument**, which submits it as a real first turn. Without it,
  Claude Code auto-submits "Continue from where you left off." on a session it restored
  mid-turn, and the session carries on as though nothing broke. Supplying the brief replaces
  that turn with one that says what happened. No escape keystroke is needed.
- **The brief points at git before it points at the transcript.** What landed in version
  control is what happened; an agent's own account is evidence of what it was attempting.
  Runners that commit incrementally usually kept most of their work, and the fastest way to
  waste the recovery is to rebuild something that is already on a branch.

`--dry-run` writes everything and opens nothing. Use it when the session list is long enough
that you want to read it first. `--include-idle` also reopens the sessions that were owed
nothing: those are resumed with no prompt, and with `CLAUDE_CODE_RESUME_PROMPT` set to a
stand-down line, because Claude Code auto-submits a continue prompt whenever it classifies the
restored transcript as an interrupted turn — on a session that was merely idle, that starts
work nobody asked for.

The brief names every agent that was in flight, not only the ones that died loudly. An agent
that reached the end of its turn without returning a result leaves no error anywhere and is
exactly the one whose context is worth promoting, so listing only the failures hides the best
recovery available.

If a tab fails to open, the ledger records it and the remaining tabs still open; source that
tab's bootstrap script by hand. The driver confirms the tab count moved before typing, because
a synthesised `cmd+T` is accepted on macOS and does nothing, and typing a bootstrap line into a
tab that never opened sends it into whichever session was focused. That confirmation reads the
count as "no tab group means one tab": Ghostty builds the tab group only once a window holds
two, so on a single-tab window the direct query errors — which on 2026-08-22 failed all ten
tabs of a recovery before anything was typed.

## 5. Restore the interrupted work, rather than restarting it

This is the part that decides whether the recovery was worth doing. Pick by what the journal
shows, not by habit.

**An agent that was mid-flight → promote its transcript.**

```bash
python3 scripts/promote_agent.py <path-to-agent-NNN.jsonl> --cwd <the agent's own cwd>
```

A subagent has no session of its own; its transcript is a sidechain under the parent. Copy
it, rewrite `sessionId`, drop `isSidechain` and `agentId`, and file it where `--resume`
looks, and the agent's whole context resumes — the files it read, what it had concluded, the
finding it had just closed. Measured: a promoted 95-line transcript named its item, its
branch and a closed finding from memory with no tools. Its replacement, started from the
same prompt, would know none of that.

**A background agent outside a workflow → promote it the same way.** A session driving
subagents directly owes nothing to a journal, so nothing reports them as lost, and the scan
lists them as `loose_subagents`. They promote exactly like a workflow agent: on 2026-08-22 an
mcp-router session died holding six, including two planners and a runner mid-item, and none of
them appeared in any run's ledger.

**Calls that never started → a fresh run of only those.** Write a new script containing the
outstanding items and launch it from the recovered session. Each prompt carries the branch as
authority and the predecessor's transcript path as evidence of what was in flight.

**A long prefix of completed calls you do not want to re-run → splice, then resume.**

```bash
python3 scripts/splice_result.py <wf_runId-dir> --list
python3 scripts/splice_result.py <wf_runId-dir> --agent-id <id> --result-file <file>
Workflow({scriptPath: "<from the scan>", resumeFromRunId: "<run id>"})
```

`resumeFromRunId` replays an `agent()` call from cache when the journal holds a `result` for
its key, and the miss flag is sticky: after the first miss nothing is consulted again. The
interrupted agent *is* that first miss, so everything after it re-runs — including calls
whose results are already on disk and whose work is already committed. Splicing closes that
by recording what the finished agent actually returned, under the key its own `started` line
already holds.

Two rules keep splicing honest, and they are why the script will not do it unattended:

- **Only a real result.** Finish the agent first (promote it, let it reach a conclusion) and
  splice what it returned. Distilling "what it looked like it had achieved" from a partial
  transcript manufactures the exact failure this tooling already suffers from — runs have
  reported items merged whose branches were tens of commits short of the integration branch.
- **Never edit the original journal.** The script writes a copy and prints the path, so the
  crash's own record survives and a second attempt costs nothing.

When the prefix is short, skip all of this and re-run the outstanding items. A splice is
worth its risk only when it saves real completed work.

### Relocating a run

`splice_result.py` writes its copy beside the original, which is not where a resume will look
for it. A resume rebuilds the journal path from the session id at the moment it runs:

```
<project-of-the-session's-original-cwd>/<SESSION-UUID>/subagents/workflows/<runId>/
```

So the copy has to be moved to that path under whichever session you are going to call
`Workflow(...)` from — normally the recovered session itself, which keeps its original id and
therefore its original path. Move the copy into place, keep the crash's own directory
somewhere else, and resume:

```bash
RUN=wf_xxxxxxxxxxx
BASE=~/.claude/projects/<project>/<SESSION-UUID>/subagents/workflows
mv "$BASE/$RUN" "$BASE/$RUN.as-the-crash-left-it"
mv "$BASE/$RUN.recovered" "$BASE/$RUN"
```

Two things to know before doing it. The project directory in that path comes from the
session's **original** working directory, not the one it is working in now — the same split
that hides the script (§4) also decides this path, so read it off the scan's `dir` field for
that run rather than constructing it. And the run id is reused rather than replaced on resume,
so the resumed run writes into this same directory: keeping the original under a different
name is what makes a second attempt possible.

## 6. Then say what state things are in

Report per session: what was recovered, what was left, and what is genuinely outstanding —
short, and shaped by what a reader would do next. A recovery report that lists everything
that went right buries the one item that did not come back.

Keep it to a few lines per session. Anything that could not be recovered gets a reason, not
a hedge.

## Scope, and what not to do

- **Do not resume a session that is live in a terminal**, and do not relaunch a run whose
  agents are still writing. That is the one irreversible mistake available here. A session
  that is alive but detached is the opposite case: stop it before recovering, or the recovery
  runs alongside it.
- **Do not use `--fork-session`** on anything this skill touches.
- **Do not fabricate a journal result**, however confident the partial transcript looks.
- **Delegation:** this work is sequential and cheap. Do it directly. One subagent is
  justified only when several repositories each need their branch state reconciled and those
  investigations are genuinely independent; never more than one per repository, and never to
  check work already done.
- Recovering the session is the task. Finishing the interrupted work is the session's own job
  once it is back, and that call belongs to whoever is watching it.

## References

- `references/mechanics.md` — the runtime behaviour this rests on, what was measured against
  which version, and the probes that look right and are not. Read it when something here
  contradicts what you are seeing, or before relying on a mechanism in a new Claude Code
  version.
- `references/evidence.md` — where each claim came from, and which are read from a binary
  rather than measured.
- `scripts/selftest.py` — builds a fixture in the shapes a real crash leaves and asserts the
  scan reads it correctly, including the freshness split, a loose-agent-only session, and the
  cwd fallback. Run it after changing the scanner.

Scripts, in the order they are used: `scan_crashed.py` (see what is there), `kill_orphans.py`
(stop the survivors), `open_tabs.py` (reopen), then `promote_agent.py` or `splice_result.py`
per interrupted item.

For a workflow run that *completed* while losing agents to API errors — a different failure,
with opposite handling — use the `workflow-resume` skill. This one is for the case where the
process itself died.
