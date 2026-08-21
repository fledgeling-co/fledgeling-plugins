# recover-claude-code

Your terminal crashed and took a dozen Claude Code sessions with it. The work isn't gone —
every transcript, every workflow journal, every subagent's accumulated context is still on
disk. It's just unattached. This brings it back.

## The problem it actually solves

Reopening the sessions is the easy half. The half that goes wrong is what happens to the
work that was in flight.

A background agent that was still running when the process died left behind a `started`
line in its run's journal and no result. Resume the run and that agent restarts **from its
original prompt with an empty head**. It re-reads the same files, re-derives the findings its
predecessor had already closed, and sometimes redoes work that is already committed on a
branch. Nothing reports a problem. It looks like the recovery worked, and it quietly costs
you an hour.

There's a worse version. On 2026-08-21 a real crash took eighteen sessions down. The recovery
tooling reported "no script path" for every interrupted run, so resuming them was impossible
and each one was rebuilt by hand from a fresh brief. The scripts had been on disk the whole
time — Claude Code files a workflow's script under the project directory of the shell's
working directory and its journal under the original one, so any session working in a
worktree splits its own state across two folders, and a lookup that only checks one reports
nothing. The same run also recorded a "machine-wide usage limit" in a repository's event log
that never happened; the tooling had matched the phrase "usage limit" inside agents that were
merely *discussing* rate limits. The actual cause was a null-pointer dereference in Ghostty.

Both of those are now tests.

## Usage

```
/recover-claude-code
```

Or just say what happened — "my terminal crashed, get my sessions back", "the machine
rebooted and I lost everything", "the last recovery started new agents from scratch".

## What it does

1. **Scans** every project directory for sessions touched in a window, and sorts them into
   live, still-writing, stopped-with-work-owed, and stopped-cleanly.
2. **Refuses to touch the live ones.** Liveness comes from `~/.claude/sessions/`, a pid-keyed
   registry carrying the session id, working directory, peer name and status. Quietness is
   not death: a runner can work for forty minutes without writing to the parent transcript.
3. **Reopens each dead session** in its own Ghostty tab, at its original working directory,
   under its original session id, with a brief handed over as the first turn so it wakes up
   knowing it crashed instead of carrying on as though nothing happened.
4. **Restores the interrupted work with its context.** A dead subagent's transcript is a
   sidechain; copy it, rewrite three fields, and it resumes as a session that still knows
   what it read and what it concluded. Measured: a promoted transcript named its item, its
   branch, and a finding it had already closed, from memory, with no tools.
5. **Reconciles against git first.** What landed in version control is what happened. An
   agent's own account is evidence of what it was attempting.

## What's in the box

| Script | What it does |
|---|---|
| `scan_crashed.py` | Read-only survey: liveness, owed work, agent states, script paths |
| `promote_agent.py` | Turns a dead subagent's sidechain transcript into a resumable session |
| `open_tabs.py` | Opens a tab per session and resumes it; `--dry-run` writes everything and opens nothing |
| `splice_result.py` | Records a finished agent's **real** result in a **copy** of a journal; refuses to invent one |
| `selftest.py` | Builds a fixture in the shapes a real crash leaves and asserts the scan reads it right |

## Two things it will not do

**It will not fabricate a journal result.** Splicing a distilled "this is roughly what it
achieved" into a run's journal makes a resume replay a lie, and this family of tooling has
already reported items merged whose branches were tens of commits short of the integration
branch. You finish the agent, then record what it actually returned.

**It will not use `--fork-session`.** A workflow journal is filed under the session id, so
forking orphans every run the recovery is trying to reach — silently.

## Requirements

macOS with Ghostty for the tab driver (the accessibility API is used to open tabs, because a
synthesised `cmd+T` is accepted and does nothing). Everything else is stdlib Python 3 and
works anywhere; on another terminal, run the generated bootstrap scripts yourself.

## Sibling skill

`workflow-resume` handles the opposite failure: a run that reported `completed` while losing
agents to API errors, where the process itself never died. Different shape, opposite
handling. This one is for when the process died.

## Evidence

`skills/recover-claude-code/references/mechanics.md` carries the runtime behaviour with what
was measured against which version, including the probes that look correct and are not.
`references/evidence.md` splits every claim into measured-on-a-machine and read-from-a-binary,
and records where two other model families disagreed about the design.
