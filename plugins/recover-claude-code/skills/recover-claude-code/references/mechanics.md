# Runtime mechanics

Measured against **Claude Code 2.1.238**, **Ghostty 1.3.1**, macOS 26.6, on 2026-08-21,
during and after a real crash: Ghostty died at 14:32:44 taking eighteen sessions and their
in-flight workflow agents with it.

Each claim below says how it was established. "Measured" means it was observed on this
machine. "Read" means it came out of the shipped binary's strings and has not been exercised.
Behaviour changes between versions; the disk layout is the part worth re-checking first
because it is observable without a disassembly.

## The live-session registry

```
~/.claude/sessions/<PID>.json
{"pid":38275,"sessionId":"781039d7-…","cwd":"/Users/me/Dev/finance",
 "procStart":"Fri Aug 21 04:43:24 2026","version":"2.1.238","kind":"interactive",
 "entrypoint":"cli","messagingSocketPath":"/tmp/cc-socks/38275.sock",
 "name":"finance-7c","nameSource":"derived","status":"busy","updatedAt":1787292747542}
```

**Measured.** One file per live session, named by pid, carrying the session id, the working
directory, the peer name that `ListAgents` shows, and a status. `/tmp/cc-socks/<PID>.sock`
exists alongside it. This is the liveness authority, and it is also where a crashed
session's working directory and label come from.

Two caveats, both measured:

- `procStart` and `ps lstart` are formatted differently **and sit in different time zones**
  (`Fri Aug 21 04:43:24 2026` against `Fri 21 Aug 14:43:24 2026`). Comparing them looks
  stricter than checking the pid and is worse: it fails for every live session, so the whole
  registry reads as dead. The registry file is named by pid, so a recycled pid overwrites the
  record rather than inheriting it; checking that the pid is alive and is still Claude Code is
  the guard that works.
- `updatedAt` is **not a timer heartbeat.** It moves on status change, so a busy session can
  carry a stamp two hours old. A freshness window on it drops live sessions.

### Two liveness probes that do not work

- **`ps` output does not contain the session id.** `CLAUDE_CODE_SESSION_ID` is in the
  environment of a session's *child* processes, which are transient, not in the top-level
  process's own argv. A `ps | grep <session-id>` probe returns nothing for a live session —
  measured against eighteen sessions that were all running at the time.
- **The scratchpad path is named by a per-process instance id, not the session id.** For a
  session started fresh the two coincide, which is what makes the probe look correct. After
  a resume they diverge: a session whose transcript is `d351a7f1-…` was writing task output
  under `/private/tmp/claude-501/<project>/f61a4b81-…/tasks/`. Measured.
- **`lsof` sees nothing.** Transcripts are opened, appended and closed rather than held, so
  no running process holds the `.jsonl` open. Measured.

## Resume keeps the session id

**Measured.** `claude --resume <id>` continues the original session: eighteen resumed
sessions all appended to their existing transcript files rather than creating new ones.
`--fork-session` is the documented opt-in that mints a new id.

This matters because the workflow journal path is built from the session id:

```
~/.claude/projects/<project>/<SESSION-UUID>/subagents/workflows/<runId>/journal.jsonl
                             ^^^^^^^^^^^^^^ resolved fresh at resume time
```

Forking, or resuming into a different session, lands in a directory that never held the run
and cold-starts with no warning.

## A positional prompt is submitted as a real turn

**Measured.** `claude --dangerously-skip-permissions --resume <id> "<text>"` in interactive
mode appends `<text>` as an ordinary user message (no `isMeta`) and the session answers it,
then stays interactive.

That removes the need to send an escape keystroke. When Claude Code restores a transcript it
classifies as an interrupted turn, it auto-submits a continue prompt — **measured**: the real
crash produced `{"type":"user","isMeta":true,"message":{…"Continue from where you left
off."}}` in every resumed session, and the user pressed escape to stop it. Handing over a
brief instead replaces that turn with one that says what actually happened.

Two related environment variables are **read, not measured**:
`CLAUDE_CODE_RESUME_PROMPT` replaces the auto-continue text
(`EWi(){return V.CLAUDE_CODE_RESUME_PROMPT||"Continue from where you left off."}`), and
`CLAUDE_CODE_RESUME_INTERRUPTED_TURN_MAX_AGE_MS` gates a suppression path. An attempt to
exercise both against a hand-crafted interrupted transcript did not reproduce the
`interrupted_turn` classification, so neither is relied on here. The positional prompt is
the measured route.

## The script and the journal are filed under different project directories

**Measured**, and this is what makes a crashed run look unrecoverable when it is not.

```
scripts dir   join(projectDir(LIVE cwd),     sessionId, "workflows", "scripts")
journal dir   join(projectDir(ORIGINAL cwd), sessionId, "subagents", "workflows", runId)
```

Read from the binary as `Rri(){return join(vM(er()), zt(), "workflows","scripts")}` where
`er()` is the live working directory, against `Phe(e){return join(_5() ?? RT(xn()), zt(),
"subagents","workflows", e)}` where `xn()` is the session's original cwd.

Observed on disk twice: session `d351a7f1` had its journals under
`-Users-lukerhodes-Dev` and its scripts under `-Users-lukerhodes-Dev-orderly`; session
`781039d7` had scripts under `-Users-lukerhodes-Dev-finance--worktrees-F199`. Any session
working in a subdirectory or a worktree splits its own workflow state across two project
directories.

The consequence: a script must be found by **searching every project directory for the run
id**, not by joining a path onto the journal's. Looking only beside the journal reports "no
script path", which makes `resumeFromRunId` look impossible and sends the recovery down the
hand-authored path — which is exactly what happened on 2026-08-21.

## A snapshot exists only for a completed run

**Read**, consistent with what was observed. `<session>/workflows/<runId>.json` is written at
completion. A run killed by a crash has none, so any tool that reads `scriptPath` out of the
snapshot reports nothing for precisely the runs that need recovering. The script itself is
persisted at launch and survives.

## Resume reuses the run id, and the cache is a sticky prefix

**Read.** `let d = e.resumeFromRunId ?? "wf_" + randomUUID().slice(0,12)` — a resumed run
writes into the same `wf_<runId>` directory rather than a new one.

The key is a chain: `sha256(previousKey ‖ prompt ‖ normalisedOpts)`, and after the first miss
the cache is not consulted again for the rest of the run. So replay is a prefix, not a set,
and an agent that was mid-flight is the first miss — every later call re-runs, including ones
whose results are on disk.

`normalisedOpts` covers `schema, model, effort, isolation, agentType, disallowedTools,
bashCommandClamp` with keys sorted. `label` and `phase` do not affect the key, so agents can
be relabelled or regrouped freely. (Two more keys than the seven-month-old note in
`workflow-resume`'s own mechanics doc, which lists five.)

Only non-null results are journaled, so a failed agent is never poisoned into the cache.

## A subagent transcript is a promotable sidechain

**Measured.** Every line of `agent-<id>.jsonl` carries `isSidechain: true`, an `agentId`, and
the *parent* session's `sessionId`; `agent-<id>.meta.json` beside it holds
`{"agentType":"workflow-subagent","spawnDepth":1,"model":"opus"}`.

Rewriting `sessionId`, dropping `isSidechain` and `agentId`, and writing the copy to
`<project-of-target-cwd>/<new-uuid>.jsonl` makes it resumable. A promoted 95-line workflow
agent, resumed and asked from memory with no tools, returned its item id, its branch, and a
specific finding it had already closed.

## Ghostty on macOS

All **measured** against Ghostty 1.3.1:

- `ghostty +new-window` → "not supported on this platform". The CLI's own help says to use
  `open -na Ghostty.app` instead.
- **A synthesised `cmd+T` does nothing and reports success.** `keystroke "t" using command
  down` through System Events left the tab count at 21 both before and after, with no error.
  Ghostty's own keybind table does bind `super+t` to `new_tab`; the synthetic event does not
  reach it.
- **Clicking `File > New Tab` through the accessibility API does work** — 21 → 22. So
  Accessibility permission is granted and only the keystroke route is affected.
- **Typing text through System Events works** — `keystroke "<text>"` then `key code 36`
  landed a command in the new tab and it ran.
- Tabs are enumerable as `radio buttons of tab group 1 of window 1`, which is how the count
  is confirmed before anything is typed.
- `open -na Ghostty.app --args -e <cmd>` runs the command but **`--working-directory` is
  ignored** (the process inherited an unrelated directory), and it opens a window rather
  than a tab unless the system's window-tabbing preference says otherwise. Hence the menu
  route plus a `cd` inside the bootstrap script.

## Spawning a `claude` from inside a Claude session

**Measured.** The child inherits `CLAUDE_CODE_CHILD_SESSION=1` and prints
`⚠ Transcript saving is off — inherited CLAUDE_CODE_CHILD_SESSION marker`, so it writes no
transcript at all. Any headless recovery step run from inside a session must clear
`CLAUDE_CODE_CHILD_SESSION` and `CLAUDECODE` first. A tab opened through Ghostty takes its
environment from the GUI and is unaffected.

## Field notes

- **An API error is only an API error when the transcript ends in one.** Matching the phrase
  anywhere turns an agent that merely *discussed* rate limits into a failure. On 2026-08-21
  that produced a false diagnosis that reached a repository's own event log: "a machine-wide
  usage limit at 14:32:45 killed all three runners". The only genuine agent-side error in
  that window was `API Error: Connection lost mid-response`, and the actual cause was the
  terminal dying at 14:32:44 — a null-pointer dereference in Ghostty
  (`EXC_BAD_ACCESS / KERN_INVALID_ADDRESS` at `0x20`, crash report in
  `~/.local/state/ghostty/crash/`), under a machine that had already logged a jetsam event
  with one process holding ~131 GB resident.
- **Git is the authority on what happened.** Runners that commit incrementally keep most of
  their work through a crash: one lost runner had four commits on its branch and another had
  a 176-line commit that closed its blocking finding. Reconcile against branch ancestry
  before deciding anything is outstanding.
- **A locked worktree naming a live pid is legitimate.** Check the pid before unlocking.
