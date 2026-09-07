# Scheduling & concurrency — survey fan-out, the DAG, the measured fleet, shared surfaces

## Survey fan-out (Phase 1)

The survey is read-heavy. Use the available agent API for sizeable independent batches, with structured results; read a small ledger directly. Use Workflow only when its current schema is exposed. Typical shape:

- **Ledger reader** — parse LEDGER.md rows → id, title, status, deferred/next-tier notes.
- **Spec readers** — pipeline over `docs/specs/spec-*.md` (batch ~10 specs per agent): status line, deferred/progress sections, explicit dependency mentions ("depends on / blocked by / after / child of <ID>"), UI-surface keywords (for mock matching).
- **Briefs reader** — `docs/features-to-triage/*.md` minus LEDGER.md: title, one-line summary, dependency hints, whether a spec already covers it (title/topic match against the ledger).
- **Research indexer** — one agent lists `docs/deep-research/*.md` with a one-line topic each; you (orchestrator) do the item↔research matching from that index. Match generously on topic overlap — a billing feature should get "Accounting Software Feature Research.md" even without an exact name hit.
- **Mock comparators** — per mock in `design/mocks/html/`: which feature is this, and is it *more refined than* the design-system app preview's current representation (open both; compare surfaces, states, density — not pixel equality). More refined → a `design-refresh` item (or an input to the feature's pending run).

Reduce everything into the single item list yourself. You own dedup (a brief that duplicates an existing spec merges into that spec's item; two briefs describing one feature merge with a note).

## Building the DAG and waves

- Nodes: every non-Done item. Edges: internal dependencies only (item → item). External dependencies (a human decision, a credential, a third-party service) mark the item `holding-pen` instead of creating edges.
- Prefer explicit textual dependencies; add inferred edges (same subsystem, same files, parent/child) conservatively — a false edge costs parallelism, a missed edge costs a merge conflict; when torn, note it as a "soft" edge and let the merge-serialization absorb the risk.
- Topological sort → waves (Wave N = everything whose deps are all in Waves <N). A cycle means the items are really one unit: either combine them into a single ship-feature run or ask the user how to split.
- Within a wave, order by: unblocks-the-most-items first, then resumable items (their worktrees are perishable — rebases get harder daily), then user-stated priority.

## The fleet (Phase 5)

Slot-refill beats wave-barriers: when a runner lands, anything newly unblocked starts immediately. The following is a Workflow-style sketch, not a portable tool API. Use it only after checking the installed Workflow schema; otherwise implement the same state transitions with the available agent tool. `runnerOptions` must come from the resolved, supported model policy. `maxRunners` is the smallest of the explicit user cap, tool limit, five-runner policy and measured capacity.

```js
// ready-queue + slot refill; items/deps come in via args
// harbourmaster's scripts, RESOLVED. CLAUDE_PLUGIN_ROOT is a VERSION directory
// (.../ship-fleet/2.4.1), so a sibling plugin is two levels up and carries a
// version folder of its own. `${CLAUDE_PLUGIN_ROOT}/../harbourmaster` looked for
// it among ship-fleet's own other versions and silently found nothing.
const HM = sh(`find "$CLAUDE_PLUGIN_ROOT/../../harbourmaster" -maxdepth 4 -type d `
            + `-name scripts 2>/dev/null | sort -V | tail -1`).trim()
const done = new Set(args.alreadyMerged), running = new Map()
const parked = new Map(), attempts = new Map()          // id -> reason / restart count
const ready = () => args.items.filter(i => !done.has(i.id) && !running.has(i.id)
  && !parked.has(i.id) && i.deps.every(d => done.has(d)))
while (done.size + parked.size < args.items.length) {
  // Slot count is READ, not assumed. `harbourmaster` reports what this Mac can
  // carry right now; a fixed 8 is a claim about a machine nobody measured, and
  // this one has been observed at load average 830 across 16 cores while a
  // fleet started its eighth runner. Re-read every refill: pressure moves under
  // a long fleet, so a number taken at the top describes a machine that is gone.
  // Missing capacity telemetry cannot justify eight concurrent runners.
  // Start conservatively and stay inside the available tool and user caps.
  let slots = Math.min(2, args.maxRunners)
  if (HM) {
    try { slots = Math.min(args.maxRunners, Math.max(0, JSON.parse(sh(`${HM}/berths.py`)).available)) }
    catch { log('harbourmaster unreadable — using conservative capacity') }
  }
  // Hand the resolved path DOWN. A runner cannot re-derive it: a spawned agent
  // does not reliably inherit CLAUDE_PLUGIN_ROOT, so the `find` in ship-feature's
  // and shipyard:work's machine-admission block returns nothing and the runner
  // reports harbourmaster as not installed on a machine that has it. That is why
  // fleets have shipped with every build unwrapped while the governor sat idle.
  const berth = HM
    ? `Machine admission: harbourmaster's scripts are at ${HM}. Export `
      + `HARBOURMASTER_SCRIPTS=${HM} and wrap every build and test step with `
      + `"$HARBOURMASTER_SCRIPTS/governor-run" at the weights your stage skill gives. `
      + `Do not re-resolve this path; the find in your skill will come back empty.`
    : `Machine admission: harbourmaster is not installed here. Run builds and tests `
      + `unwrapped and say so once.`
  if (slots === 0 && running.size === 0) {
    // Save state and use the harness's bounded wait/resume mechanism.
    // Zero available berths is scheduling information, not a dependency failure.
    return {status: 'capacity-wait', done: [...done], parked: [...parked]}
  }
  for (const item of ready().slice(0, Math.max(0, slots - running.size)))
    running.set(item.id, agent(`${runnerPrompt(item)}\n\n${berth}`, {...args.runnerOptions, label: item.id})
      .then(report => ({item, report})))

  // Nothing ready and nothing running means the remainder is blocked behind items
  // that never merged. Promise.race over an empty iterable NEVER settles, so
  // entering it here hangs the fleet silently and forever.
  if (running.size === 0) {
    for (const i of args.items)
      if (!done.has(i.id) && !parked.has(i.id)) parked.set(i.id, 'blocked: a dependency never merged')
    break
  }

  const {item, report} = await Promise.race(running.values())
  running.delete(item.id)

  // A dead runner is NOT a finished one. agent() returns null when the subagent
  // hits a terminal API error (zero retries) or the user skips it, and a null
  // destructures just as cleanly as a real report — so without this branch the
  // slot frees, the fleet moves on, and the item vanishes having never run.
  if (report == null) {
    const n = (attempts.get(item.id) ?? 0) + 1
    attempts.set(item.id, n)
    if (n > 2) parked.set(item.id, `runner returned null ${n}x — parked, needs a human`)
    continue                                            // never add to `done`
  }

  // hand ready-to-merge back to the MAIN session between workflow rounds if you
  // prefer to finalize there; either way: ONE merge at a time, ledger updated first
}
// `parked` is an outcome, not an exception: write every entry to ORCHESTRATOR.md
// with its reason before the run reports anything.
```

**Three rules the sketch encodes, worth stating on their own because a fleet that
breaks them looks exactly like a fleet that worked:**

1. **A null return is a death, not a completion.** Claude Code's workflow `agent()`
   returns `null` on any terminal API error, with **zero retries**, and the run
   still reports `completed`. Counting that item as done is how a fleet reports a
   green backlog it never touched. Check for null explicitly; `.filter(Boolean)`
   in a script quietly does the opposite of what you want here, because it drops
   the evidence that something died.
2. **Never `Promise.race` an empty map.** It never settles. If the ready queue is
   empty and nothing is running, the remaining items are blocked behind something
   that never merged — park them with that reason and break.
3. **`done` means merged.** Not "the runner returned", not "the report said
   ready-to-merge". The only writer to `done` is your own serialized finalize
   after the merge lands.

In practice you may prefer batches: run one workflow per "as many slots as are ready", return the ready-to-merge reports, finalize serially in-session, update ORCHESTRATOR.md, then launch the next workflow. That trades a little parallelism for much simpler state — fine. What is not fine: exceeding the resolved concurrency cap, starting an item whose deps haven't merged, or two merges at once.

## Launching runners — resolve the harness, then observe the run

Use shipyard's `references/model-lanes.md` to choose the user-authorized model
for each role. Keep the conductor in-session; a feature runner can dispatch Opus
intake/triage/plan and Gemini implementation through explicit artifact handoffs.
Do not require every runner to identify itself as Opus.

1. **Inspect the available agent schema.** Confirm supported model, effort and
   lifecycle fields before launch. A known URL, CLI name or a Skill invocation
   does not establish that Workflow exists. Use the native agent API when it
   supports the required routing; use an external CLI only under the applicable
   project policy. Never guess a tool or model identifier.
2. **Validate the packet before spending a runner.** It must contain a concrete
   objective, existing source paths, exclusive writable scope, required output
   paths and a finish line. Decode JSON-encoded arguments once if this harness
   requires it; reject a missing or empty prompt before spawning.
3. **Observe the actual runner.** Record authoritative request/response or runtime
   metadata for model and effort. An old background-Agent incident showed why
   requested flags were insufficient; it does not prove every current harness is
   broken. A model's self-description or a header echoing launch flags is not
   runtime identity evidence. If execution identity is unavailable, record that
   limitation and preserve any gate that requires verified routing.
4. **Pass the resolved policy once.** Give runners the absolute model-lanes and
   executor-reference paths, their role and the stage handoff contract. Nested
   prompts carry only the relevant scope, sources, role and evidence boundary.
   Independent review means a family different from the artifact's actual writer,
   including when Gemini implemented it or GPT authored the plan.
5. **Use the actual lifecycle.** A one-shot Workflow wrapper returns when its
   runner ends, and may not accept revival messages. Keep pending work attached
   with supported bounded waits and save a checkpoint before return. A persistent
   agent may have supported follow-up/resume APIs; use their documented behavior.
   Do not spin in unbounded polling or assume a notification can revive a finished
   wrapper. Relaunch from reconciled artifacts after a failure.

A current supported Workflow lane can take a packet like this (adapt the schema
only from observed documentation):

```js
const a = typeof args === 'string' ? JSON.parse(args) : args
if (!a || typeof a.prompt !== 'string' || !a.prompt.trim() || !a.runnerOptions)
  throw new Error('Missing prompt or resolved runner options')
return await agent(a.prompt, {...a.runnerOptions, label: a.id})
```

## The runner prompt (base template)

Use the selected harness and role; fill every placeholder from observed state.
The same packet works for an in-session stage handoff or a supported external
runner without pretending their tool APIs are interchangeable.

```
You are a feature runner in an orchestrated fleet. Deliver ONE feature using
ship-feature:ship-feature. Resolve that exact skill identifier in your catalogue;
pass the feature separately as arguments. If the Skill tool is absent, follow the
verified SKILL.md path supplied below and report that execution method.

Role/model policy: ⟨resolved role, supported model/effort and authorized fallback⟩.
Read ⟨absolute shipyard model-lanes.md and executor-lanes.md paths⟩ before routing.
Normally GPT-6 coordinates, Opus 5 produces intake/triage/plan artifacts, then
Gemini 3.8 implements. Preserve the user's actual choices and this harness's limits.
Stage handoffs carry source revisions, output paths, allowed files and acceptance
criteria. Do not infer runtime model identity from your own prose.
Review gates use a capable family different from the artifact's writer. Keep
missing evidence, failed lanes and any loss of independence visible. No generic
extra self-review rounds; run the actual required tests and measurements.

Feature: ⟨ID · title⟩
Sources — open the required artifacts for your stage before acting:
  brief: ⟨docs/features-to-triage/….md⟩ · spec: ⟨docs/specs/spec-ID.md⟩ · plan: ⟨docs/plans/plan-ID.md⟩
Design context: ⟨root DESIGN md path⟩ — authoritative for all UI decisions.
Best practices: docs/CODING_PRACTICES.md and docs/NEW_PROJECT_BEST_PRACTICES.md — binding.
Deep research: ⟨matched docs/deep-research/ files, relevant sections, or "none matched"⟩ — read the evidence and caveats supporting each design/plan decision; follow linked sections when needed, and pass the source paths onward.
Mock input: ⟨design/mocks/html/… or "none"⟩ — hand to ship-feature's design stage as the mock.
  "none" changes NOTHING about the design stage's coverage bar: ship-feature Phase 1 must
  still represent the feature's ENTIRE UI — every surface, state, user interaction, user
  flow, and popup/modal/menu — in the design system via design-craft:design-craft, authoring the
  reference from the brief/spec + the existing design system and adding new
  elements/composites as needed. A mock is a hint, never a prerequisite.
Resume state: ⟨"fresh" | "resume in .worktrees/ID on ai/id — do NOT create a new worktree"⟩

Rules that override ship-feature's defaults:
- STOP BEFORE MERGE. Run every stage through acceptance-e2e green, commit on the branch,
  but do not rebase-merge-push-clean; the orchestrator serializes finalization.
- NEVER pass `-c user.email` or `-c user.name` to git. The repo's identity is configured;
  overriding it rewrites the commit AUTHOR, and Vercel gates deployments on the author. One
  runner doing this blocked every deployment across the whole team with TEAM_ACCESS_REQUIRED
  until the history was rewritten. Attribution belongs in the Co-Authored-By trailer, which
  is a message field and gates nothing. Put this line in every runner prompt verbatim — it
  is cheaper than the outage by several orders of magnitude.
- WORKTREE-FIRST, including design-craft:design-craft: create `.worktrees/⟨ID⟩` on `ai/⟨id⟩` BEFORE any
  file edit and run EVERY phase inside it. ship-feature's design-craft:design-craft stage predates the
  worktree in its default flow — override that. N concurrent runners share the main tree,
  and one runner's mid-edit DS file breaks main's typecheck for everyone (this recurred
  three times in one fleet before being diagnosed as structural rather than runner error).
  Orchestrator counterpart: at every merge, diff any main-tree-dirty files against the
  incoming branch — discard copies the branch subsumes, fold newer ones onto the branch
  first; never stash-pop blindly over a live runner's work.
- Propagate the context contract: every subagent you or ship-feature spawns gets the same
  source/design/practices/research paths above. ⟨+ executor lane block when enabled —
  codex per shipyard references/codex-cli.md §R3, else
  shipyard executor-lanes.md⟩
- LEDGER.md writes (child-spec triage) only under the ledger lock rule: ⟨rule⟩.
- Keep design-system changes feature-scoped; do not edit shared tokens/base elements —
  if a shared change seems required, report it instead of making it.
- After ANY context compaction, re-read brief/spec/plan and the DESIGN md before continuing.
- Run the spec-review, plan-review and completeness gates through the resolved independent lanes; report each verdict and findings disposition. An unavailable lane is recorded with its authorized fallback, never a silent skip.

- Preserve the pipeline's safeguards to make a runner cheaper. If you author a reduced
  ("solo") brief for a small item, it must keep: the acceptance evidence rule (typed
  evidence per clause — measurement / exercised request / red→green test), the
  affected-test sweep, the two-probe rule before any "verification is blocked" claim,
  and the completion comment/progress note with its tables. A hand-rolled brief that
  drops Phase D or the browser check is how a fix ships "verified by code reading" —
  the audit corpus's most common failure. Scale review to the actual changed scope and avoid duplicate rereads; retain evidence required to close each acceptance row.

Final message = a report: status (ready-to-merge | blocked | failed), branch + worktree,
gate evidence (typecheck/tests/e2e results verbatim — behavioural evidence for UI claims,
not just build gates), deferred children discovered
(title + suggested deps), shared-surface changes you wanted but skipped, questions for the user.
```

## Shared-surface rules (the ones that corrupt repos when violated)

| Surface | Rule |
|---|---|
| Integration-branch merges | Orchestrator only, strictly one at a time, gate before merge |
| `LEDGER.md` id allocation | Serial pre-triage covers the bulk. Mid-fleet child triage: create `docs/features-to-triage/.ledger.lock` (content: item id) before read-modify-write, delete after; if the lock exists, wait and retry; if it's held >10 min, the orchestrator arbitrates. After writing, re-read to verify your row survived |
| `ORCHESTRATOR.md` / hierarchy HTML | Orchestrator is the **sole writer**; runners report, never edit |
| Design-system shared files (tokens, base elements) | Runners never edit; feature-scoped composites/pages only; wanted-but-skipped shared edits go in the report and become orchestrator-scheduled items |
| `docs/specs/`, `docs/plans/` | Per-feature files only — a runner touches only its own `<ID>`'s (and its children's) files |

## Pausing & resuming the fleet (field-learned 2026-07)

A paused runner's transcript is a **log, not a knowledge state**: most of its bulk is redundant on
resume (full file dumps it read, test output, dead-end attempts), while the durable artifacts —
spec, plan, commits, WIP files — already sit on disk. So the goal of a pause is never "preserve
the context"; it is **convert the context's non-redundant residue into a handover doc**, then let
the resume start lean. The residue is small and specific: a half-diagnosed bug, a
decided-but-unapplied fix, what each uncommitted file is for, the next planned step.

### The handover doc

Per paused runner, appended to its spec as a `## Pause checkpoint — <date>` section (the spec is
already ship-feature's on-disk memory; a fresh runner reads it by contract). Contents:

- Pipeline position: which stages are DONE (with commit hashes) · which stage was in flight
- WIP map: every uncommitted file → one line on what it is and how finished it is
- Diagnosed-but-unfixed: bugs found with evidence, fixes decided but not applied
- Next 3 steps as the runner saw them · gotchas (ports in use, env quirks, flaky tests + why)
- Context files a resumer must re-read (paths only — never inline file contents)

**Who writes it — the quality ladder:**

1. **The runner itself, pre-stop (best).** If the runner is messageable (direct background agent —
   SendMessage works; workflow-inner agents may not be reachable), tell it: "write the pause
   checkpoint to your spec, commit WIP as a wip commit, then stop." Written from warm context this
   is cache-hit cheap and captures everything.
2. **Orchestrator transcript harvest (always, free).** After TaskStop, extract the last 2–3
   assistant text blocks from each runner's `agent-*.jsonl` (workflow transcript dir) into the
   checkpoint. Tail-only, but in the field this alone recovered a fully-diagnosed rate-limit bug
   a fresh resume would have re-debugged from scratch.
3. **One-shot cold revival to hand over (rare).** For a runner with deep unharvestable state
   (dozens of interdependent uncommitted files, no commits, tail harvest insufficient): revive it
   once via SendMessage to its transcript agentId with the SOLE instruction to write the handover
   + wip-commit, then stop it. Pays the transcript reprocessing once and converts it into a
   durable artifact — still cheaper than reviving it to continue, because a continued 500k-context
   agent re-carries that weight every turn and compaction looms.

Pause at the cheapest moment, not a "natural" one — waiting for phases to finish burns more than
resume re-grounding costs. When only dialing down (not a full stop), pause the least-deep runners
first; stage boundaries lose least.

### Resume lanes & the prompt cache

There is **no session-pinning knob at the API level**: the cache keys on the exact byte prefix
(system prompt + message history + model), not an agent/session id. Same-agent revival matters
only because it replays the identical transcript, making the prefix match. Compaction, an injected
system-reminder, or a model change forfeits the hit.

- **Warm (inside the harness's prompt-cache TTL):** revive via SendMessage to the runner's agentId —
  full context, near-free. The TTL is a harness-level `cache_control` choice you cannot set, so treat it
  as an observation, not a guarantee: current Claude Code sessions run a **1-hour** TTL, dropping to
  ~5 minutes once the session is in usage overage. Plan the warm window as "about an hour, shorter in
  overage", and confirm by whether the revival actually came back cheap — never build a pause strategy
  that only works at one TTL.
- **Cold (beyond that window, or after a usage reset):** fresh relaunch through the workflow lane, prompt = pointers to
  the handover section + the context contract files. Do NOT cold-revive to continue; use ladder
  rung 3 only to extract a missing handover, then still resume fresh.
- **Workflow journal replay** (`{scriptPath, resumeFromRunId}`) replays completed `agent()` results
  free — the lane for re-running a runner that died mid-workflow; it preserves step results, not
  agent context.

Either way, run the pre-resume reconcile first: ORCHESTRATOR.md vs `git worktree list` vs each
branch's ahead/dirty counts — runners often committed more than the checkpoint recorded.

## Failure handling

- Runner failed with a diagnosable cause → restart the slot with the failure appended to the prompt (max 2 restarts, then park).
- Runner's worktree half-done → the item becomes `resumable`; next attempt resumes there.
- A merge conflict during your serialized finalize → resolve it yourself in the worktree (you have the map of what else landed); if it's semantic (two features fighting over behaviour), park the later item and note the collision as a dependency you missed.
- User interruption / session death → ORCHESTRATOR.md is current by construction; the resume path in SKILL.md takes over.

## Berths, and how they relate to the agent budget

They are different ceilings and both apply.

- **The agent budget** bounds the API rate limit: runner slots x inner waves.
- **Berths** bound this Mac: CPU, memory and disk, read from
  `harbourmaster:harbourmaster`'s `berths.py`.

Take the smaller. A fleet inside its agent budget can still pin the machine,
and a machine with headroom can still be rate-limited.

`harbourmaster:harbourmaster` also decides whether a piece of work belongs on this Mac at all
— a long self-contained build may belong in an `anvil errand` container, and a
verification verdict belongs in `defer:defer`. Route before you budget.
