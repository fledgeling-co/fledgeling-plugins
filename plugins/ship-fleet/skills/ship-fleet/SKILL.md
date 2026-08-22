---
name: ship-fleet
description: >-
  Backlog-wide feature-delivery orchestrator — surveys ALL remaining feature work in a repo and
  ships it. Reads the pipeline artifacts (ledger or tasks board, specs, plans, untriaged briefs,
  mocks, deep research, DESIGN md) and in-progress worktrees, writes ORCHESTRATOR.md (plan +
  ledger) and orchestrator-hierarchy.html BEFORE any work starts, then runs ship-feature per
  feature: dependency-ordered concurrent runners under a global agent budget, cross-family verify
  per item, merges serialized. Use when someone wants EVERYTHING remaining shipped —
  "orchestrate the remaining work", "ship everything left in the backlog", "survey what's left",
  "work through the backlog N at a time", "resume the orchestrator", "run the fleet" — even if
  they never say "orchestrator". Also the answer to "what work remains / is deferred / is
  blocked" across the pipeline. NOT for a single feature (ship-feature) or a single stage.
---

# Ship Fleet — backlog-wide feature orchestrator

Take **everything that remains** in a repo's feature pipeline and drive it to merged, verified
production code. You are the orchestrator: survey the pipeline, build one durable plan-and-ledger
(`ORCHESTRATOR.md`), then conduct concurrent `ship-feature` runs in dependency order — verifying,
merging, and updating the ledger as each lands. One feature = one run; your job is everything
between the runs.

```
preflight → survey → hygiene → artifacts (ORCHESTRATOR.md + hierarchy html, BEFORE execution)
  → serial pre-triage → fleet (dependency-ordered ship-feature runners, global agent budget,
    lane-routed subagents + executor lanes, out-of-family gates, per-item cross-family verify,
    serialized merges, ledger updated after every event)
```

Everything is **discovered inside the project — never hardcode paths**. Conventional layout
(markdown lane; the tasks lane swaps the ledger/specs for the board, per shipyard's
`references/tracker-adapter.md`): ledger at `docs/features-to-triage/LEDGER.md` (older repos
`docs/feature-specs/LEDGER.md` — pick what exists, never create both), specs `docs/specs/`,
plans `docs/plans/`, briefs `docs/features-to-triage/`, mocks under `design/`, research
`docs/deep-research/`, DESIGN md at root, worktrees `.worktrees/<ID>` on `ai/<id>`
(`git worktree list` is authoritative).

## Operating discipline

- **You stay in-session, on the session model, holding the map.** Runner agents are Opus at
  `effort: 'high'`, launched ONLY through the verified single-agent-Workflow lane in
  `references/scheduling-and-concurrency.md` — never as direct background Agent calls, whose
  model override has been observed not to stick and whose effort defaults to xhigh. Never hand
  the orchestration itself to a subagent.
- **`ORCHESTRATOR.md` is the memory, not the transcript.** Update it after every state change;
  a fresh session must be able to resume the whole fleet from that file alone. After compaction:
  re-read it, the DESIGN md, and the ledger before acting.
- **Plan before execution** — both artifacts written, shown, committed before the first slot.
- **Dependencies rule the schedule.** An item never starts before its internal dependencies have
  **merged** (not merely finished). External dependencies flag and skip an item; they never
  stall the fleet.
- **A global agent budget, not two independent caps.** Runner slots × each runner's inner ≤4
  waves multiply into the same rate limiter — budget the product (default: slots × wave ≤ ~16;
  8 slots means telling runners to run leaner waves, or run 4–6 slots at full width). Confirm
  fleet size with the user at the go-ahead.
- **Take the slot count from `harbourmaster`.** Its `berths.py` reports what this Mac can carry
  right now, and the loop re-reads it on every refill because pressure moves under a long fleet.
  The 8 above is what an uninstalled or unreadable governor falls back to, not the starting
  number. Resolve its path once in the conductor and pass that path into every runner's brief —
  a spawned agent does not reliably inherit `CLAUDE_PLUGIN_ROOT`, so a runner that re-derives
  the path finds nothing and reports harbourmaster missing on a machine that has it.
  `references/scheduling-and-concurrency.md` carries the resolution, the hand-down, and the
  soft-fail. Say in the go-ahead which slot count you used and whether it was measured.
- **Never destroy unmerged work.** Cleanup removes only the provably merged or empty; unique
  commits queue for resume or go to the user.
- **Report thinly; artifacts terse.** ORCHESTRATOR.md is rows and statuses, never prose.

## Phase 0 — Preflight (interactive: report, ask, then repair)

`references/preflight.md` in full. Structure check against the table above; offer the missing
skeleton; practices docs copied from the repo's own named team-files source (its CLAUDE.md says
where — never assume one); stray feature-shaped markdown offered into `features-to-triage/`;
the egress opt-out markers checked and recorded in ORCHESTRATOR.md; executor and review lane
availability probed (`executor-lanes.md` §availability) and recorded. Declined repairs degrade
gracefully — say what breaks and continue.

## Phase 1 — Survey

Fan out per the scheduling reference. Classify every item: **Done** (verified + merged) ·
**Resumable** (In Progress / Developer Review, especially with a live worktree) ·
**Needs verification** (Developer Review with no verdict — the flagship gap: a verifier that
exists but is never invoked verifies nothing) · **Needs More Work** (failed verification —
gap-fix work orders) · **Ready for AI** · **To Do** (triaged, unplanned) · **Untriaged** ·
**Deferred follow-ups** (mined from progress notes and ledger — each a child item pointing at
its parent) · **Design refresh** (mock more refined than the built surface) · **Needs input**
(essential questions, external dependencies — record the question, don't block the fleet).
Extract per item: dependencies, matched research docs, matched mock.

## Phase 2 — Worktree & branch hygiene

`git worktree list` + `git branch --list 'ai/*'`. Per branch: complete-and-green → queue for
**verify-then-finalize**; partial with real work → Resumable in its worktree; empty or fully
merged (proven by `git branch --merged`) → clean up; ambiguous → surface, never guess-delete.

## Phase 3 — Orchestrator artifacts (before any execution)

`ORCHESTRATOR.md` (header contract, wave plan from the internal-dependency DAG, ledger table —
format in `references/orchestrator-artifacts.md`) and `orchestrator-hierarchy.html`
(self-contained visual: waves, edges, category/status colouring; refreshed at wave boundaries).
Cycles → merge into one combined run or ask. External-dep items → flagged holding pen.

## Phase 4 — Serial pre-triage

Triage every untriaged item **serially** before the fleet fans out — ledger id allocation is a
read-modify-write on a shared file, and concurrent runners racing it corrupt it. Child specs
minted later follow the ledger-lock rule in the scheduling reference.

## Phase 5 — Run the fleet

Slots filled with the highest-value ready item; refill on free — don't barrier on whole waves
when the DAG allows overlap (the ready-queue + `Promise.race` scheduler is in the scheduling
reference; guard the empty-race and null-return rules from shipyard's
`references/operational-rules.md`).

Each slot = one Opus runner (verified lane, first-action self-check, transcript-verified) whose
prompt invokes **`ship-feature`** on its item with: the item's paths and resume state, the
matched mock, the context contract below, the lane-routing propagation block — and **two stop
rules**:

- **Stop before verify.** Runners run ship-feature through e2e-green and report
  *ready-to-verify*. **You** spawn the `verify` stage per item as a fresh agent (that stage's
  fresh-context rule is structural: a runner cannot verify its own build). A *ready-to-verify*
  report is a claim about a bundle, so treat it as one: an item whose evidence bundle is empty
  goes back to its runner rather than into the verify queue, because verify's first act would be
  to find that out at the cost of a whole fresh agent. Verify's verdict sets
  `Done` or `Needs More Work`; `Needs More Work` re-queues the item as a gap-fix run in the same
  worktree. An item carrying `Unverified — no oracle` re-queues to phase 6 for oracle
  construction instead, because gap-fix closes a gap between the work and its spec and this is a
  gap between the spec and anything checkable.
- **Stop before merge.** You serialize finalization: one branch at a time — the fail-closed gate
  (which now requires the verdict comment), rebase, merge, push per repo convention, cleanup,
  ledger update. Two simultaneous merges into one integration branch is how fleets corrupt
  repos.

**A fleet is where a Done column is built, so it is where an unauditable one starts.** Each
item's verdict records the oracle rung its evidence stood on, and the fleet ledger carries the
mix across the whole run rather than a pass count. A fleet that closed forty items all proved by
`presence` has shipped forty items nobody can later audit in either direction — which surfaces
as an unverifiable backlog months afterwards, when the branch context is gone and re-deriving
each item's intent costs more than the original build.

Where the repository carries a `.warrant/`, run `campaign.py export-warrant` once at the end of
the fleet rather than per item: it is the step that lets the accumulated evidence earn a tier
instead of the warrant refusing one permanently. For auditing a Done column that already exists
rather than one this fleet is building, `warrant:lot` is the instrument — sampled under a
declared risk limit, blind, and seeded, rather than item-by-item.

After every runner event: update `ORCHESTRATOR.md` first, then act. Runner failure → read the
report and artifacts; retry sharper, resume in-worktree, or park with a reason.

**A runner that produced nothing needs a channel sweep before a sharper retry, and "read the report"
is not it.** The report is the channel closest to hand, which is why it gets read, and it is routinely
the one channel the cause is absent from. Measured on one pipeline, 2026-08-21: the reason a run died
appeared **36 times** in the run event stream, in **none** of the 56 run records carrying an error
(they held container and blob noise instead), and in **none of 285,950 lines** of the daemon log that
was actually being read and quoted. Enumerate before you conclude:

1. **The run's own record** — its status and its error field. Treat that field as *the last thing that
   failed*, never as the cause: a real failure followed by an infrastructure failure leaves only the
   second.
2. **The event stream**, if the runner emits one. This is where a harness usually writes the terminal
   reason, and it is the channel a human never opens.
3. **The token counts.** An output-to-input ratio far above 1 means the agent is emitting its artifact
   as literal output instead of writing a file — measured, **33.8:1 on failed runs against 1.1:1 on
   completed ones**, visible from the first failure. A ratio above roughly 5 is worth a look on its own.
4. **The granted capability set.** If the runner does not print what the agent was permitted to do,
   that is the first thing to add, not the last — and on the run this comes from it is the *only* thing
   that would have worked. A tool withheld from an agent's context produces **no refusal event at all**:
   the vendor documentation for the harness in question states that a denied tool's definition is removed
   from the request, so the model never sees it and cannot attempt it. There is nothing for a progress
   view to suppress and nothing for a log to carry. The agent was not blocked from writing a file; it was
   never told writing was possible. So "surface the refusals" is a fix for a different failure, and the
   manifest is the one that names an absence.

**Do not harden the output while the cause is unidentified.** The failure presents as a symptom class —
output too long, no artifact, timed out — and the symptom does not name the cause. On the run this rule
comes from, the visible symptom read as verbosity, so **41 commits** went into stricter output gates and
**15** into rewriting prompts before **one** touched the tool list, across twenty days in which 74 of
135 runs produced nothing. Gate work on an unexplained failure is how three weeks disappear.

**Put the terminal reason on the logger, and know that this is the one item here with a controlled
effect size.** A study of 20 programmers measured diagnosis time falling **60.7%** — 10.37 minutes
against 25.72 — when proactively-added error logs were present, at 1.4% runtime overhead. Nothing else
in this list has a number like that behind it.

**And preflight the next run rather than diagnosing it again.** If a job must persist a file and no
permitted tool can write one, fail before the model is invoked. That check costs nothing and is the only
intervention here that stops a run rather than explaining it afterwards. A workflow that
reports `completed` with dead agents, or a fan-out lost to rate limits mid-run, is the
`workflow-resume` skill's job — use it before relaunching anything, because a manual relaunch
cold-starts and re-pays for work the journal already holds. Discovered children join the DAG.
At the end: every item `Done` / parked-with-reason, statuses final, hierarchy refreshed, and the
needs-input items handed over as decisions rather than a list — in an attended run one
consolidated round; for a long unattended run's accumulated questions, the `whats-left` skill
builds the decision page. For a fleet expected to run to a verifiable finish line unattended,
arm it with `better-goal` at launch — the built-in stop mechanisms fail silently past eight
blocked turns, and a fleet is exactly the run length that trips them.

## Model routing

The lane table, effort discipline, and both invariants (REVIEWER ≥ WRITER; VERIFIER ∉ writer's
family) are canonical in shipyard's `references/model-lanes.md` +
`references/model-and-effort.md` — propagate them into every runner prompt rather than pinning
everything to Opus. Fleet-level notes: runner top level stays Opus-at-high via the verified
lane; executor lanes per `executor-lanes.md` (picked per slice shape by `defer`, Claude fail-back, verify-fix
loop, revert-rate kill-switch); the out-of-family review gates and the per-item verifier follow
their ordered lane sets and are **mandatory where available** — their fallback is a logged
downgrade in the artifact, never a silent pass; the egress opt-out is re-grepped before every
external call because it is the only kill-switch reaching runners already in motion.

**Never strip the pipeline's safeguards to make a runner cheaper.** The sanctioned low-cost
runner shape is exactly this file's runner prompt with leaner inner waves and cheaper leaf
lanes — never with fan-out, review phases, or evidence rules deleted (the hand-rolled "SOLO
runner" brief that stripped them is the audit corpus's most common shipped-broken pattern).

## The context contract (every agent, every lane)

Every agent touching a feature is given, by path, and told to read: the brief + spec + plan (as
they exist), the root DESIGN md, the repo's practices docs, and the item's matched deep-research
doc(s) — **in full, not skimmed**. Compaction rule in every prompt: after any compaction,
re-read the brief, spec, plan, and DESIGN md — the on-disk artifacts are the memory. For the
codex executor the rule is enforced mechanically by the re-context harness
(shipyard `references/codex-cli.md`); install and self-test it before the first delegation.

## Resuming

`ORCHESTRATOR.md` exists → never re-survey from scratch, never write a second orchestrator
file. Read it, reconcile against reality (statuses, `git worktree list`, merged branches),
correct drifted rows, continue at Phase 5 or the earliest phase whose output is missing.

## Guardrails

- **A fleet multiplies whatever the evidence layer gets wrong.** One campaign's captures being
  filed by filename is a bad page; twenty items' verdicts resting on the same shape is a Done
  column nobody can audit. Where the repo carries a campaign, `test-campaign`'s
  `capture-lineage.py <dir> --gate` runs once per repo rather than once per item, and its exit
  code gates the column — the cheapest place in the whole fleet to catch a mis-bound picture.
- Respect ship-feature's gates — never merge a branch whose pre-merge gate hasn't passed, never
  mark `Done` without the verifier's verdict, and follow the repo's push convention.
- Budget honestly and confirm the go-ahead with the user after presenting ORCHESTRATOR.md.
- Report failures as failures — a parked item with a reason beats a fake green. `done` means
  verified-and-merged per the ledger, never "the dispatch returned"
  (`operational-rules.md` §fan-out).
