# Scheduling & concurrency — survey fan-out, the DAG, the 8-slot fleet, shared surfaces

## Survey fan-out (Phase 1)

The survey is read-heavy and embarrassingly parallel — use the Workflow tool with structured-output schemas so results come back as data, not prose. Typical shape:

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

## The 8-slot fleet (Phase 5)

Slot-refill beats wave-barriers: when a runner lands, anything newly unblocked starts immediately. Sketch (Workflow tool — the script owns the loop, agents do the work):

```js
// ready-queue + slot refill; items/deps come in via args
const done = new Set(args.alreadyMerged), running = new Map()
const parked = new Map(), attempts = new Map()          // id -> reason / restart count
const ready = () => args.items.filter(i => !done.has(i.id) && !running.has(i.id)
  && !parked.has(i.id) && i.deps.every(d => done.has(d)))
while (done.size + parked.size < args.items.length) {
  for (const item of ready().slice(0, 8 - running.size))
    running.set(item.id, agent(runnerPrompt(item), {label: item.id, model: 'opus', effort: 'high', agentType: 'claude'})
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

In practice you may prefer batches: run one workflow per "as many slots as are ready", return the ready-to-merge reports, finalize serially in-session, update ORCHESTRATOR.md, then launch the next workflow. That trades a little parallelism for much simpler state — fine. What is not fine: exceeding 8 concurrent runners, starting an item whose deps haven't merged, or two merges at once.

## Launching runners — verified model routing (field-learned 2026-07, motif-studio fleet)

The model override is the single most expensive thing to get wrong: a fleet of runners silently on the
session model (e.g. a Mythos-class model) at the background default effort (**xhigh**) burns tokens far
faster than Opus-at-high, and nothing in the launch result tells you it happened. Hard-won rules:

1. **Never launch runners as direct background `Agent` tool calls.** In the field, `model: 'opus'` on a
   backgrounded Agent call did not reliably stick (the user's UI showed the runners on the session model),
   and background agents default to **xhigh** effort with no per-call knob on that path. The reliable lane
   is a **single-agent Workflow wrapper** per runner — the Workflow `agent()` call exposes both knobs and
   they verifiably apply:

   ```js
   export const meta = { name: 'runner-<ID>', description: 'Fleet runner <ID> (opus, high effort)',
     phases: [{ title: 'Run' }] }
   const a = typeof args === 'string' ? JSON.parse(args) : args        // args can arrive JSON-encoded
   if (!a || typeof a.prompt !== 'string' || a.prompt.length < 100)
     throw new Error('args.prompt missing — abort before spawning')     // never spawn on an empty prompt
   phase('Run')
   return await agent(a.prompt, {label: 'runner:<ID>', model: 'opus', effort: 'high', agentType: 'claude'})
   ```

   **Workflow-inner agents cannot be re-invoked.** Two field consequences: (a) SendMessage revival
   never works for them ("No transcript found") — the handover doc is their only pause artifact;
   (b) a runner that ends its turn to WAIT for a background task (a Monitor, a build, an e2e run)
   is dead the moment it stops — its wrapper returns and the wake-up notification has nowhere to
   land. Put it in every runner prompt: "NEVER end your turn to wait for a background task — your
   wrapper returns when you stop and no notification can reach you; wait synchronously (foreground
   the command, or poll in a loop) instead." When it happens anyway, the orchestrator relaunches
   for the tail with a transcript-harvested handover (cheap if the runner committed first).

   The two guards are not optional decoration: in the field, `args` once reached the script as a JSON
   **string**, `args.prompt` was `undefined`, and every runner burned ~60k tokens politely replying
   "no task was provided" — the guard turns that into a fast, free failure.

2. **Set `effort` explicitly — and read the effort dial before you pick.** Full per-lane guidance is
   canonical in ship-pipeline's `references/model-and-effort.md`; the three facts that
   change launch decisions here: (a) an agent spawned with no `effort` runs at `high`, so a leaf reader
   left unset is over-spending — `low` is the level built for subagents; (b) a feature runner is
   long-horizon agentic work (multi-phase, >30 min), which is what **`xhigh`** is for — `effort: 'high'`
   is the fleet's deliberate cost choice, not the capability-matched setting, so if you raise a runner to
   `xhigh` raise its `max_tokens` too (start at 64k, since `max_tokens` caps thinking plus response text);
   (c) effort is the *primary* cost dial and model the second — where a review lane is routed a model tier
   down purely to save tokens, prefer keeping the stronger model at lower effort, which saves the same and
   keeps REVIEWER ≥ WRITER intact (that invariant is about capability class, not spend).

3. **Verify at two levels; trust neither the launch parameters nor a probe.**
   - *In the prompt*: make the runner's FIRST ACTION a self-check, written against the **tier** and never
     a dated id: "your system prompt states the model powering you; if it is not an Opus-class Claude
     model, reply exactly `WRONG-MODEL: <id>` and stop." A check that hardcodes last generation's string
     fires on every correctly-routed runner and stops the fleet before it starts — a newer model in the
     same tier is a pass, a different *tier* is the failure.
   - *On the wire*: after launch, grep the model id from the first assistant turn of each runner's
     transcript (`agent-*.jsonl` under the workflow run's transcript dir):
     `grep -o '"model":"[^"]*"' <transcript> | head -1`. A one-off probe agent is NOT sufficient evidence —
     in the field a foreground probe returned opus while the real background runners ran on the session model.

4. **Propagate the routing table downward — don't pin everything to Opus.** The runner itself spawns
   subagents (ship-feature fans out constantly), and those inherit the **session** model unless routed.
   Every runner prompt must carry — and instruct the runner to propagate into every prompt that itself
   spawns agents — the lane table (SKILL.md §"Model routing"): leaf readers + gate-runners → `haiku`;
   evidence lenses, adversarial finding-verifiers, e2e Phases 0–4, design leaf verifiers + page assembly,
   Sentinel verdict + Assumptions, Trivial/Small plan synthesis → `sonnet`; mechanical Phase B/E slices
   meeting the delegation criteria → the external executor lanes (the executor lane order (agy gemini-flash-3.7 `high` → grok grok-4.6 `high` → codex `gpt-5.6-terra` `medium` → Claude) by
   default, else ship-pipeline's `executor-lanes.md`); the three out-of-family review gates (triage spec review, plan
   review gate, work Phase D completeness critic) → codex `gpt-5.6-sol` at `max`, read-only; everything on
   the never-downgrade list (Large plan synthesis, work Phase A synthesis, Phase C conflicts,
   security/guardrails/client-asserted-identity lenses, gap-fix audit over
   cheap-lane code, e2e Phase 5 judgment + Phase 6 fixes, aesthetic direction + new composites,
   merge/finalize) → `opus`. Two invariants ride the table: **REVIEWER ≥ WRITER** — for every artifact
   the strongest reviewer is at least as strong as the strongest model that wrote it — and **per-lane
   wire verification**: each routed agent's prompt opens with the rule-3 self-check adapted to *its*
   lane's model, and you spot-grep `"model":"…"` from routed transcripts exactly as for runners (a
   downgrade that silently lands on the session model at xhigh is the expensive failure; an upgrade
   that silently lands on haiku is the corrupting one). The executor lanes are optimizations
   with an **Opus fallback** (ship-pipeline's `executor-lanes.md` §"Fallback") — a lane failure routes the work back
   to Opus, never to a sibling cheap lane, never silently skipped. The codex `max` review gates are
   **not** a cost lane and route sideways for independence, not savings: mandatory where available,
   exempt from the kill-switch, and their fallback is a *logged* in-family downgrade in the artifact
   and the ledger — an unlogged fallback reads as a skipped gate, so treat it as one.

5. **On a mid-run model/effort correction**: stop the runners (their killed state is recoverable), append
   each one's last-known progress to its prompt as a RESUME note (the on-disk worktree/spec/scratchpad
   artifacts are the memory), and relaunch through the workflow lane. Runners stopped on an external
   failure (session limit, network) relaunch the same way — same scriptPath + args; failed agents re-run
   live since only successes cache.

## The runner prompt (base template)

Every runner is an Opus agent launched through the **verified workflow lane above** (`model: 'opus'`,
`effort: 'high'`, `agentType: 'claude'` — full tool access so it can invoke skills). Base prompt — fill the ⟨⟩:

```
You are a feature runner in an orchestrated fleet. Deliver ONE feature by invoking the
ship-feature skill (Skill tool: "ship-feature:ship-feature") on it, from the repo root.

FIRST ACTION — model self-check: your system prompt states the model powering you. If it is
NOT an Opus-class Claude model, reply immediately with exactly "WRONG-MODEL: <that id>" and
stop. Check the TIER, never a dated id — a newer Opus is a pass; sonnet/haiku/another family is not.
MODEL ROUTING — you run on Opus at high effort; route the agents YOU spawn per lane, and
propagate this whole block into every prompt that itself spawns agents:
  · leaf readers + typecheck/lint gate-runners → model:'haiku'
  · evidence lenses (UI fidelity / clause table / reachability), adversarial finding-verifiers,
    e2e Phases 0–4, design leaf verifiers + page assembly, Sentinel verdict + Assumptions,
    Trivial/Small plan synthesis → model:'sonnet'
  · everything else — work Phase A synthesis, Phase C conflicts, security/guardrails/
    client-asserted-identity lenses, Standard/Large plan synthesis,
    e2e Phase 5 judgment + Phase 6 fixes, new composites/aesthetic direction, finalize →
    model:'opus' (Workflow agent() calls add effort:'high').
  REVIEWER ≥ WRITER always: never review an artifact with a weaker model than wrote it.
  Give every routed agent a first-action self-check for ITS lane's model. Mechanical
  Phase B/E slices may go to the external executor lanes ONLY per their references
  (codex gpt-5.6-sol at medium — the default, with its post-compaction re-context hooks
  installed and self-tested — else ship-pipeline executor-lanes.md): delegation criteria + Opus
  verify-fix loop + per-lane kill-switch; any lane failure falls back to Opus — never to
  a sibling cheap lane, never skipped.
  OUT-OF-FAMILY GATES (read-only, max effort): the triage spec review, the plan review
  gate, and work Phase D's completeness critic run on codex gpt-5.6-sol — NOT as a
  Claude subagent. They exist because every other reviewer here is Claude auditing
  Claude. Exempt from the kill-switch.
  BEFORE EVERY codex call, re-grep CLAUDE.md / AGENTS.md / ORCHESTRATOR.md for
  'ANTHROPIC-ONLY', 'NO EXTERNAL MODEL CLIS' or 'external-model-clis: off'. A hit means
  this repo OPTED OUT: run in-family, log 'codex: opted out (<file>) -> claude', do not
  request an exception. Re-check EVERY time, not once — every codex call ships the
  artifact and every file it opens to OpenAI (-s read-only restricts writes, NOT
  egress), and this grep is the only kill-switch that reaches you once you are running.
  Bound every call: perl -e 'alarm shift @ARGV; exec @ARGV' 600 codex exec … — never
  poll unbounded, it holds a fleet slot for nothing. Verify the wire: the captured log
  must contain 'model: gpt-5.6-sol' and 'reasoning effort: max', or it is a lane
  failure — a dropped flag silently inherits the user's config default. An empty -o
  file is a lane failure, never a pass; findings without a verdict line are PARTIAL.
  If codex is unavailable, run the in-family reviewer and LOG the downgrade.

Feature: ⟨ID · title⟩
Sources — read all that exist, in full, before starting:
  brief: ⟨docs/features-to-triage/….md⟩ · spec: ⟨docs/specs/spec-ID.md⟩ · plan: ⟨docs/plans/plan-ID.md⟩
Design context: ⟨root DESIGN md path⟩ — authoritative for all UI decisions.
Best practices: docs/CODING_PRACTICES.md and docs/NEW_PROJECT_BEST_PRACTICES.md — binding.
Deep research: ⟨matched docs/deep-research/ files, or "none matched"⟩ — when present, read the
  ENTIRE document before design/plan decisions, and pass it to ship-feature as context.
Mock input: ⟨design/mocks/html/… or "none"⟩ — hand to ship-feature's design stage as the mock.
  "none" changes NOTHING about the design stage's coverage bar: ship-feature Phase 1 must
  still represent the feature's ENTIRE UI — every surface, state, user interaction, user
  flow, and popup/modal/menu — in the design system via design-craft, authoring the
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
- WORKTREE-FIRST, including design-craft: create `.worktrees/⟨ID⟩` on `ai/⟨id⟩` BEFORE any
  file edit and run EVERY phase inside it. ship-feature's design-craft stage predates the
  worktree in its default flow — override that. N concurrent runners share the main tree,
  and one runner's mid-edit DS file breaks main's typecheck for everyone (this recurred
  three times in one fleet before being diagnosed as structural rather than runner error).
  Orchestrator counterpart: at every merge, diff any main-tree-dirty files against the
  incoming branch — discard copies the branch subsumes, fold newer ones onto the branch
  first; never stash-pop blindly over a live runner's work.
- Propagate the context contract: every subagent you or ship-feature spawns gets the same
  source/design/practices/research paths above. ⟨+ executor lane block when enabled —
  codex per ship-pipeline references/codex-cli.md §R3, else
  ship-pipeline executor-lanes.md⟩
- LEDGER.md writes (child-spec triage) only under the ledger lock rule: ⟨rule⟩.
- Keep design-system changes feature-scoped; do not edit shared tokens/base elements —
  if a shared change seems required, report it instead of making it.
- After ANY context compaction, re-read brief/spec/plan and the DESIGN md before continuing.
- Run the three out-of-family gates on codex gpt-5.6-sol at max effort (triage spec review,
  plan review gate, work Phase D completeness critic) and report each verdict + the
  accept/reject tally in your handback; a genuine unavailability is a LOGGED in-family
  downgrade, never a silent skip.

- NEVER strip the pipeline's safeguards to make a runner cheaper. If you author a reduced
  ("solo") brief for a small item, it must keep: the acceptance evidence rule (typed
  evidence per clause — measurement / exercised request / red→green test), the
  affected-test sweep, the two-probe rule before any "verification is blocked" claim,
  and the completion comment/progress note with its tables. A hand-rolled brief that
  drops Phase D or the browser check is how a fix ships "verified by code reading" —
  the audit corpus's most common failure. Cost is cut by model/effort routing and
  scope, never by deleting verification.

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
