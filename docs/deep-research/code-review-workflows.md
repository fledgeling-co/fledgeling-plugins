# workflows

> Source: `~/Dev/dossier/workflows/index.html`. Published research page, captured 20 August 2026 for the `code-review` and `atlas-publish` skills. Live at https://dossier.fledgeling.app/workflows where published.

      
      [![](data:image/svg+xml;base64,<stripped>)
        **Margin**](https://margin.fledgeling.app/)
    
    

      
Proposed, not shipped
        Measured findings and a build plan, compiled with Dossier and Margin.

    
  

[Skip to the numbers](#numbers)

  
Dossier · Field report · July 2026
  
# The wave finished. A third of it never came back.

  
Fan out a few dozen Claude Code agents across a repo. One hits a rate limit, or the proxy restarts, or the connection drops for a second. That agent returns nothing, the script filters it out, and the run reports **completed**.

  
We pulled the runtime apart to find out why, then counted what it has already cost on one machine.

  
**Status** Everything measured here is measured. The fix is a plan, not a release.

  

    

      73
      harness failures in a single week of real sessions
    
    

      6.6h
      p90 time a session sat dead before a human noticed
    
    

      516
      workflow journals sitting on one Mac
    
    

      0
      retries an agent gets when the API errors
    
  

  
01 · The mechanism
  
## An API error gets no retry at all

  
The workflow runtime has three retry mechanisms, and they’re decent. A stalled agent gets five restarts. A throttled-looking response gets one retry after a 45 second sleep. A schema validation failure gets five nudges.

  
Not the API error. This is the entire path:

  
  
```
`// after the stall-retry loop, in the local agent runner
if (It.apiError) {
  let yr = `[${te}] failed: ${It.apiError}`;
  return A.push(yr),
         r({type:"progress", …}),
         null
}`
```

  claude 2.1.220, bundled runtime at ≈ byte 234M
  
  
A rate limit comes back fast, so it doesn’t even qualify for the throttle retry; that one needs the request to have run for over 90 seconds first. It goes straight to `null`. Then `parallel()` and `pipeline()` turn failures into `null` as well, and the `.filter(Boolean)` at the end of a generated script drops them on the floor.

  

    What each failure is worth
    | Failure | Handling | Retries |

    
      | No progress for 180 seconds | Watchdog aborts, agent restarts from its original prompt | 5 |

      | Throttled-looking response | Sleep 45 s, try once more | 1 |

      | Schema validation failure | Nudge in conversation | 5 |

      | **Rate limit, usage limit, dropped connection, 5xx** | Return `null` | 0 |

    
  

  
The tool result *does* carry a failures block and an error count. The status sitting next to it says `completed`.

  
02 · Why resume doesn’t save you
  
## The journal is filed under the session, not the run

  
This is the part worth knowing even if you never change a thing. The resume journal is written to a path built from the session id, and the session id isn’t stable.

  
  
```
`function Ste(e) {                                     // e = the runId
  let t = dW() ?? tS(gn());                           // project dir
  return join(t, kt(), "subagents", "workflows", e);  // kt() = CURRENT session id
}`
```

  the resolver, read from claude 2.1.220
  
  

    ~/.claude/projects/<project>/<SESSION-UUID>/subagents/workflows/<wf_runId>/journal.jsonl
    ↑ the session id is a parent segment, resolved fresh every time you resume
  
  
Auto-compaction mints a new session id. So the resume looks under a directory that has never contained that run, finds nothing, and cold-starts from phase one, while a complete journal sits intact one folder over. Long runs are the ones most likely to compact, which means the failure correlates neatly with the runs you most want back.

  
It’s filed and open, labelled `bug` and `has repro`. The reporter had a 61 KB journal with twelve entries sitting recoverable on disk while the resume started again from nothing.

  
03 · The count
  
## 516 journals, and the gaps are visible

  
A clean run shows exact parity: every agent that started returned a result. An interrupted one doesn’t. Each dot below is one agent attempt on a single machine.

  

    
The five largest workflow journals on one machine. Three of them show a large gap between agents that started and agents that returned a result: 96 started and 61 returned, 128 started and 78 returned, 107 started and 55 returned. The remaining two show exact parity at 164 and 269.

  

         wf_ba288763-50e
         459 KB · 96 started
**35 never returned**
       
************************************************************************************************************************************************************************************************

         wf_03879cb4-431
         293 KB · 128 started
**50 never returned**
       
****************************************************************************************************************************************************************************************************************************************************************

         wf_a66d310e-d8f
         264 KB · 107 started
**52 never returned**
       
**********************************************************************************************************************************************************************************************************************

         wf_6868590b-cff
         232 KB · 164 started
all returned
       
****************************************************************************************************************************************************************************************************************************************************************************************************************************************

         wf_d0f66a0d-ca4
         201 KB · 269 started
all returned
       
**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

  

    ** returned a result
    ** started, never returned
  
  
**One honest caveat:** a `started` entry is appended per attempt rather than per agent, so a gap isn’t a one-to-one count of lost work. The contrast between the parity rows and the 107/55 row is real all the same.

  
04 · Why you can’t salvage half
  
## The keys chain, and the first miss is fatal

  
Cached results are keyed by a sha256 chain over the previous key, the prompt bytes and the options. Not a positional index, which had been ambiguous until the binary settled it.

  
  
```
`function zSd(e, t, r) {              // (prompt, opts, prevKey)
  let n = createHash("sha256")
    .update(r).update("\x00")        // previous key
    .update(e).update("\x00")        // prompt bytes
    .update(Jq_(t)).digest("hex");   // normalised opts
  return `v2:${n}`;
}`
```

  
  
And the miss is harder than a prefix boundary. A sticky flag is set the first time a lookup misses, and after that **no lookup is consulted again for the rest of the run**, including ones whose key would still have matched. An orphaned journal isn’t a degraded resume. It’s a fully cold one.

  
One useful thing falls out of the same function: only `schema`, `model`, `effort`, `isolation` and `agentType` are normalised into the key. Labels and phases aren’t, so you can relabel or regroup agents freely without invalidating anything.

  
05 · The fix
  
## Three boundaries, because they cover different failures

  
Picking one is a category error. A proxy can’t know whether an agent already committed something, and a journal can’t keep a wave alive through a five hour usage window.

  

    

      
01 · Transport
      
#### The classifier

      
A 429 with somewhere to rotate becomes a silent account swap. A 529, a 504 or a dropped socket comes back as `x-should-retry` with an honest delay, so the client’s own loop absorbs it. Real 400s pass straight through.

    
    

      
02 · Orchestrator
      
#### The run index

      
A project-scoped map of run id to journal path, so a resume finds its history whichever session wrote it. Before spending anything it reports the predicted cache-hit rate, and **0% fails loudly** instead of quietly starting over.

    
    

      
03 · Supervisor
      
#### The ledger

      
A task isn’t done because a process exited zero. Record the worktree, the base commit, the output commit and the validation receipt, then reconcile what’s uncertain by reading git.

    
  
  
Three of the five research backends we put this to recommended adopting a durable execution engine instead. We’re not, and the reason is narrow: what we measured is a **lookup problem, not a durability problem**. The journal is intact on disk every single time. Temporal wants every model call and clock read inside an Activity and terminates a history at 51,200 events; DBOS wants an authoritative Postgres. Both are a second distributed system to fix a path that resolves wrong.

  
Worth noting which backends said what. The two that could read the actual repository recommended the light path; the three that could only search the web recommended the substrates, in a market where those four vendors publish heavily on exactly this question.

  
06 · The plan
  
## Cheapest thing first, and it’s an afternoon

  
Phase 0 is a file copy. If it works, the 516 journals already on disk become recoverable and the rest of the plan is de-risked before anyone writes code. If it doesn’t, that’s worth knowing cheaply.

  

    

      
0
      
Relocate one orphaned journal by handCopy a `wf_<runId>` directory into the current session’s tree and resume. Validates the whole premise.
      
an afternoon
    
    

      
1
      
Run index, rehydrate, predictResolve by run id across the project. Report the expected hit rate before spending a token.
      
days
    
    

      
2
      
Transport classifier and exhaustion contractRotate, or hand back a retryable status and the real reset time. Never a canned success.
      
days · parallel with 1
    
    

      
3
      
Durable record, supervisor, relaunchTask states including `uncertain`, leases, attempts, worktree and base commit, reconciliation by git.
      
weeks
    
    

      
4
      
Worker execution modelReal resumable workers for the expensive lanes, with a typed error stream per attempt. One lane at a time.
      
weeks · lane by lane
    
    

      
5
      
Evaluate a durable substrateDeferred. Two triggers only: waves that span machines, or two people resuming one run.
      
not scheduled
    
  

  
07 · Limits
  
## What none of this fixes

  

    - **Losing an agent mid-turn.** A killed agent re-runs whole under every system we looked at, Temporal included.

    - **Running out of quota on every account at once.** No retry boundary helps. Only queueing does, or paying for the overage.

    - **Prompt cache expiring between waves.** A cost leak rather than a correctness bug, and the one hour TTL is the lever, not orchestration.

    - **A resume button in the workflows view.** Retry and skip both abort a live controller, and the handler gates on the run still being `running`. Getting from a dead run back to a live one is a missing state machine, not a keybinding.

  

  

    
## Sources

    
1. 1Workflow (multi-agent) resume restarts from the beginning after auto-compaction, silently re-running completed agents. Labelled bug and has repro.GitHub issue · open · [anthropics/claude-code #65796, 6 Jun 2026](https://github.com/anthropics/claude-code/issues/65796)
1. 2Resume cache is unreachable for nontrivial workflows because dispatchers can’t transcribe args byte-exactly. Closed as not planned.GitHub issue · closed · [anthropics/claude-code #63102, 28 May 2026](https://github.com/anthropics/claude-code/issues/63102)
1. 3Bundled workflow runtime: the apiError path, the stall and throttle retry loops, the zSd cache-key chain, the sticky miss flag, and the TUI liveness gate.Primary · disassembly · claude 2.1.220, read from the shipped bundle
1. 4516 workflow journals across 39 session directories on one machine, with started and result counts parsed per run.Primary · disk survey · ~/.claude/projects, surveyed 30 Jul 2026
1. 5Dynamic workflows: the tool result carries a failures block and per-state agent counts alongside the run status.Documentation · [Claude Code docs, orchestrate subagents at scale](https://code.claude.com/docs/en/workflows)
1. 6Headless mode: stream-json emits a system/api_retry event per attempt carrying a typed error category, attempt number and retry delay.Documentation · [Claude Code docs, run Claude Code programmatically](https://code.claude.com/docs/en/headless)
1. 7Seven days across 8 to 11 concurrent sessions and 47 repositories: 1,268 human interventions, 73 of them purely to restart a fallen-over harness, p90 6.6 hours dead.Primary · audit · Agent supervision audit, 20 to 27 Jul 2026
1. 8One brief across five backends. Two with repository access recommended a light run index; three with web search only recommended a durable execution substrate.Research panel · Dossier panel dr_e34b627d7d5b9402, 30 Jul 2026
1. 9Event history warns at 10,240 events and terminates a workflow at 51,200 unless Continue-As-New is used. Activity retries default to 1 s initial, coefficient 2.0, 100 s maximum, unlimited attempts.Vendor documentation · [Temporal, events and event history](https://docs.temporal.io/workflow-execution/event)
1. 10Default service retry policy: 50 ms initial, factor 2, 60 s cap, 70 attempts, then pause.Vendor documentation · [Restate, service configuration](https://docs.restate.dev/services/configuration)
1. 11Workflow inputs and step outputs are checkpointed in Postgres; recovery re-executes and returns stored step outputs.Vendor documentation · [DBOS, architecture](https://docs.dbos.dev/architecture)
1. 12Steps are memoized and the function replays from the top; four retries in addition to the initial attempt by default.Vendor documentation · [Inngest, durable agents](https://www.inngest.com/docs/learn/durable-agents)
1. 13Checkpoints at super-step boundaries; successful sibling writes survive when another parallel node fails.Vendor documentation · [LangChain, LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
1. 14429 rate_limit_error is account-scoped, 529 overloaded_error is fleet-scoped, 504 is a timeout. The SDKs retry transient failures twice by default, honouring retry-after.API documentation · [Claude API errors](https://platform.claude.com/docs/en/api/errors)
1. 15A parallel agent workflow collapsing on an API error near completion, with users asking for checkpoint and resume. A companion thread reports a full usage window spent with no progress saved.Practitioner report · [r/ClaudeCode, Apr and Jun 2026](https://www.reddit.com/r/ClaudeCode/comments/1u2wqr4/a_feature_to_avoid_losing_an_entire_workflow_and/)
1. 16Weekly rate limits introduced alongside the existing five hour windows, with a stated aim of stopping account sharing and resale.Trade press · [TechCrunch, 28 Jul 2025](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/)
1. 17Usage credits let paid plans continue at standard API rates once included limits are reached.Vendor support · [Anthropic, manage usage credits](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans)

    
Findings marked as read from the binary come from the shipped `claude 2.1.220` bundle and were reproduced against files on disk. The research panel ran one brief across five backends; agreement between members is not corroboration, because they share a brief. Where they disagreed, the disagreement is reported rather than resolved.
