# Evidence

Every load-bearing claim in this skill, with how it was established. The split that matters
is between what was **observed on a machine** and what was **read out of a shipped binary**:
the second kind is good enough to design against and not good enough to promise.

All work dated 2026-08-21 unless stated. Claude Code 2.1.238, Ghostty 1.3.1, macOS 26.6.

## Measured on this machine

| Claim | How |
|---|---|
| `~/.claude/sessions/<PID>.json` is a live-session registry carrying `sessionId`, `cwd`, `pid`, `name`, `status` | Read 22 records; cross-checked every `sessionId` against `ListAgents` peer names and against `ps` |
| A live session is identified by pid alive + command is claude | 21 live sessions correctly classified; the same code called all 21 dead when the guard compared `procStart` to `ps lstart` |
| `procStart` and `ps lstart` differ in format and timezone | `Fri Aug 21 04:43:24 2026` vs `Fri 21 Aug 14:43:24 2026` for pid 38275 |
| `updatedAt` is not a timer heartbeat | Busy sessions carried stamps 90+ minutes old while running |
| `ps` output does not contain the session id | `ps -eo command \| grep <sid>` empty for all 18 live sessions; `CLAUDE_CODE_SESSION_ID` present only in child process environments |
| The scratchpad directory is named by a per-process id, not the session id | Session `d351a7f1` wrote task output under `/private/tmp/claude-501/<project>/f61a4b81-…/` |
| `lsof` does not see transcripts | `lsof -c claude \| grep projects.*jsonl` → 0 matches while 21 sessions ran |
| `claude --resume <id>` keeps the original session id | 18 resumed sessions all appended to their existing `.jsonl`; no new files of comparable size appeared |
| `claude --resume <id> "<text>"` submits `<text>` as a real user turn | Probe session: transcript gained `{"type":"user", …"PROBE-MARK-BETA-5514…"}` with no `isMeta`, and the assistant answered `ACK` |
| Claude Code auto-submits a continue prompt on an interrupted turn | The crash's own transcripts: `{"type":"user","isMeta":true,…"Continue from where you left off."}` at 14:41:07, followed by `[Request interrupted by user]` |
| A subagent transcript is a sidechain under the parent session | Every line of `agent-a2104f8658caf6367.jsonl` carries `isSidechain:true`, `agentId`, and the parent's `sessionId` |
| **Promotion restores an agent's context** | Copied a real 95-line workflow-agent transcript, rewrote `sessionId`, dropped `isSidechain`/`agentId`, resumed with `-p` and no tools: it returned `ORD-0081`, branch `ai/ord-0081`, and a specific finding it had already closed |
| Workflow scripts and journals land under different project directories | Session `d351a7f1`: journals under `-Users-lukerhodes-Dev`, scripts under `-Users-lukerhodes-Dev-orderly`. Session `781039d7`: scripts under `-Users-lukerhodes-Dev-finance--worktrees-F199` |
| The scripts for the three "unrecoverable" runs were on disk the whole time | `ord-0081-wf_f7cd861f-b8c.js`, `ord-0107-wf_e313af91-67c.js`, `ord-0096-verify-r2-wf_49e80231-74e.js` |
| `ghostty +new-window` is unavailable on macOS | Returns "not supported on this platform" |
| A synthesised `cmd+T` silently fails | Tab count 21 → 21, no error raised |
| The `File > New Tab` accessibility click works | Tab count 21 → 22 |
| Typing via System Events works | `keystroke` + `key code 36` ran a command in the new tab |
| `open -na Ghostty.app --args --working-directory=… -e …` ignores the working directory | Command ran with an unrelated cwd |
| A `claude` spawned from inside a session saves no transcript | Child printed `⚠ Transcript saving is off — inherited CLAUDE_CODE_CHILD_SESSION marker`; no `.jsonl` appeared |
| Substring error-matching produces false failures | Of 30 agent transcripts in the crash window, one held a real `API Error: Connection lost mid-response`; every other "usage limit" hit was the agent discussing one |
| Ghostty crashed by null dereference | `~/.local/state/ghostty/crash/e229f439-….ghosttycrash`, minidump exception stream: Mach type `1` (`EXC_BAD_ACCESS`), code `1` (`KERN_INVALID_ADDRESS`), fault address `0x20`, timestamp `2026-08-21T04:32:44Z`, 14.4h uptime |

## Read from the 2.1.238 binary, not exercised

| Claim | Where |
|---|---|
| A resumed run reuses the same run id | `let d = e.resumeFromRunId ?? "wf_"+TKf.randomUUID().slice(0,12)` |
| The cache key is a sha256 chain and the miss is sticky | `MVf(e,t,r)` builds `sha256(r ‖ e ‖ Rqv(t))`; the call site sets a flag after the first miss and never re-reads |
| `normalisedOpts` covers seven keys | `Rqv`: `schema, model, effort, isolation, agentType, disallowedTools, bashCommandClamp`, keys sorted |
| Only non-null results are journaled | The append is guarded on a non-null result |
| Snapshots are written at completion | `IVf` writes `<session>/workflows/<runId>.json` on the completion path |
| The scripts dir uses the live cwd; the journal dir the original | `Rri(){join(vM(er()), zt(),"workflows","scripts")}` vs `Phe(e){join(_5() ?? RT(xn()), zt(),"subagents","workflows",e)}`, with `er()` live and `xn()` original |
| `CLAUDE_CODE_RESUME_PROMPT` replaces the auto-continue text | `EWi(){return V.CLAUDE_CODE_RESUME_PROMPT \|\| "Continue from where you left off."}` |
| `CLAUDE_CODE_RESUME_INTERRUPTED_TURN_MAX_AGE_MS` gates suppression | `Gzm(e)` returns false when unset or `0`, and drives the suppression branch |
| The runtime can relink a run's transcript directory into the current session | `zeh()` symlinks `Phe(runId)` at the recorded transcript dir after asserting its journal exists |

An attempt to exercise the two resume environment variables against a hand-crafted
interrupted transcript did not reproduce the `interrupted_turn` classification, so neither is
used by this skill. The positional-prompt route is measured and is what the scripts do.

## Design input from other model families

The mechanism for giving a replacement agent its predecessor's context was put to three
families with the candidate options in rotated order, because it is the skill's central
choice and one worth having refuted.

- **Google (`gemini-3.7-flash-high`)** rejected all three listed options and composed a
  fourth: promote the transcript, finish it to a *real* conclusion, splice its genuine
  returned text into the journal under the existing `started` key, then resume so the
  never-started calls replay on an unbroken prefix. Its argument against splicing a distilled
  result — that it "pretends incomplete work is done" — is the reason `splice_result.py`
  refuses to generate one.
- **xAI (`grok-4.6`, xhigh)** returned `other` and argued the opposite on the journal:
  leave it immutable, emit a fresh run of only the outstanding items, make git the authority
  and the transcript merely evidence, gate on liveness first, and copy rather than move.
  Its sharpest point — that a sticky miss makes a resumed run re-execute later calls whose
  results are already on disk, duplicating committed work — is why the skill sizes the splice
  against the length of the completed prefix instead of always resuming. Part of its reply
  confabulated a narrative about other lanes' verdicts, so only its mechanism reasoning was
  used.
- **OpenAI (`gpt-5.6-sol`)** was unavailable: usage limit through 27 Aug. Reported, not
  retried.

The split between the two lanes that did answer is preserved in the skill rather than
resolved away: §4 defaults to the immutable path and reaches for the splice only when a long
completed prefix would otherwise be re-run.

## Prior art

A Dossier research run on checkpoint/restore designs for agent state, idempotent replay in
orchestrators, and whether reconciling against version control rather than an agent's claimed
results is documented practice was started on the free local lane
(`dr_25769da4d8898a65`). It **failed** after starting — the backing CLI exited on a SIGTERM,
on a machine that was already under the load described above — and returned nothing. Cost
$0.00. The paid six-backend panel ($2.25-$9.70) was available and not bought.

So this skill rests entirely on the measured runtime above and on the two out-of-family design
referrals, with no literature survey behind it. That is a real gap rather than a tidy one: the
prior art on durable execution and idempotent replay (Temporal, LangGraph checkpointers, Ray)
would likely sharpen the splice-versus-fresh-run decision in §4 of SKILL.md, which currently
rests on one measured mechanism and two models disagreeing about it.
