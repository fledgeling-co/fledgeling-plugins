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
- **Confirm the session, not the tab count.** The AppleScript probe counts the frontmost
  window's tab group, and a single-tab window reports 1 — a successful spawn measured
  `tabs_after: 1` on 23 Aug 2026 while the session existed perfectly. The verification
  that cannot mislead is the new session file in `~/.claude/sessions/` with the right cwd,
  plus its socket in `/tmp/cc-socks/`, read back a few seconds after spawn.

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

---

## Confirming the tab count is not confirming where the keystrokes go

**Measured 2026-08-23, and it delivered a brief into a live session's conversation.**

A tab was opened from the File menu. The tab **count** was confirmed to move 15 → 16 — the check this
reference already prescribes, and it passed honestly. The bootstrap line was then typed, and **focus
had not followed the new tab**, so it landed in a session sixteen hours into its own campaign. That
session read the brief and executed it: four paid research runs, $11.00, work its own user had not
asked for, while the new tab sat empty.

**A count moving proves a tab was CREATED. It does not prove keystrokes land in it.** Two claims, one
checked — the same single-field inference as every other instance in this corpus, in the one mechanism
whose failure mode is *typing into someone else's conversation*.

**The fix is to prove focus by attempt rather than by count.** `scripts/open_session.sh` types a
title-setting escape carrying a random marker, then reads the **front window's own title** back:

```
printf '\033]0;spawn-<pid>-<rand>\007'
```

**A shell that received the keystroke renames the tab. A live Claude session renders that text as a
prompt and never sets a title.** So the readback discriminates, and it discriminates in the safe
direction: the probe itself is inert if it lands in the wrong place — a stray line of prose in someone's
conversation rather than a brief they will act on.

If the marker does not come back, **nothing further is typed at all** and the script exits 2 saying so.

The rule generalises past Ghostty: **when a mechanism's failure mode is acting on the wrong target, the
confirmation must be of the target, not of the action.** Confirming that a tab exists, a file was
written, a message was sent or a process started tells you the action happened; only reading back
something only the intended target could have produced tells you where it happened.

## Recovery, and closing what is finished

**When a runner dies to an infrastructure fault, the recovery plane is transcript
promotion.** Measured 24 Aug 2026: Relay account switches killed two in-session workflow
runners mid-turn, and the orchestrator recovered both by promoting each runner's transcript
to a resumable session per `recover-claude-code` — re-dispatched with state reconciled from
git, not from the runner's last message. That reconcile-from-git-first shape ("do not treat
this as done") is the part worth copying: the dead runner's self-report ends at the kill,
and the repo is the only witness of what actually landed.

**Closing finished sessions is the conductor's cleanup, and it has rules.** Never kill
mid-flight work — a boundary report or a merged-and-holding state is the gate. Kill the
process, then tell the operator the tabs still need a manual close, because a killed
process leaves its tab shell behind and automating window-close keystrokes near the
operator's own tabs is how the wrong window dies. Classify before closing: finished with
clean handover, mid-queue, owing dispatched work, owner-gated, or the operator's own —
only the first closes. Measured the same night: twelve closed at clean boundaries took the
fleet from 32 processes to 20 with nothing lost; two candidates survived because one owed
gap-fixes and one held a pending verdict.