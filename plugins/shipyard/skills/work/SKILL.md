---
name: work
description: >-
  Implement a planned feature end-to-end in an isolated git worktree using dynamic ultracode
  workflows — the pipeline's build stage. Reads the committed plan (docs/plans/<id>.md), the
  spec/ticket thread, and the design mock index, marks the item In Progress, then runs understand
  & specify (acceptance checklist built before code), implement (file-disjoint fan-out through
  the executor lanes: agy preferred, grok, codex, Claude fail-back, with typecheck gates and the
  wire-through + affected-test sweeps), rebase onto the detected integration branch, acceptance
  review with evidence tables and an out-of-family completeness critic, resolve findings, then a
  same-family validation in fresh context before setting Developer Review. Commits locally; no
  push, no PR. Use when the user says "work DIO-0001", "implement DIO-0001", or a planned feature
  is ready to build. Cross-family verification afterwards is the verify skill's job.
---

# Pipeline Worker — build, evidence, and self-verification

Implement a planned feature inside an isolated worktree, driven by dynamic workflows, and leave
the branch local with an **evidence-typed completion record**. You are the orchestrator: you own
every phase, gate, and judgment call; executors type, reviewers report, you decide.

Canonical shared rules — read before the first run, then follow by pointer:
`${CLAUDE_PLUGIN_ROOT}/references/` → `tracker-adapter.md` (substrate, statuses, comments),
`model-lanes.md` + `model-and-effort.md` (routing, REVIEWER ≥ WRITER, effort discipline),
`executor-lanes.md` + `codex-cli.md` (delegation), `evidence-rules.md` (what closes a claim),
`test-strategy.md` (the coverage bar), `operational-rules.md` (git/worktree/fan-out incidents).

## Inputs

- An id at `Ready for AI`, with `docs/plans/<id>.md` committed and — for user-facing work — the
  design mock index. A missing plan → work from the spec/ticket + thread and flag the absence.
  `<ID>` uppercase (files, `Resolves` line); `<id>` lowercase (branch).

## Setup (before any phase)

1. **Detect the integration branch — never assume.** Prefer `origin/staging` if it exists, else
   `git remote show origin | sed -n 's/.*HEAD branch: //p'`. Call it `INT`. Then:
   `git fetch origin` (all refs) and `git worktree add .worktrees/<ID> -b ai/<id> "$INT"`.
   Reusing an existing worktree requires the staleness check:
   `git -C .worktrees/<ID> merge-base --is-ancestor "$INT" HEAD || echo "STALE — rebase in C"`.
   `WT` = the absolute worktree path. The hardcoded-branch and stale-base failures behind this
   are in `operational-rules.md` §git.
2. **Read the plan, spec/thread, and mock index from the main tree at absolute paths** (the
   worktree won't contain untracked docs). The plan is the build source of truth; the
   description + triage assumptions + human answers are the requirement source of truth.
3. **Mark `In Progress`** (status + one thread line naming the worktree) — the board is how two
   operators avoid working the same item.
4. Every code edit and git command runs **inside `WT`**; subagents get the absolute path and
   **disjoint file scopes**. Docs stay in the main tree, never committed onto the branch.
5. **Discover the repo's gates once**: its typecheck / codegen / validate / lint / test commands
   from CLAUDE.md, package scripts, or CI config. These are "the gates" below — the target
   repo's own, never an assumed toolchain.

## Running it — dynamic workflows, all phases mandatory

A large multi-slice plan is the expected input — decompose and deliver it in full. Defer a
subfeature only for a genuine **external** dependency (unbuilt upstream system, missing
credential/contract, a human-only product decision): post the blocker (with its dissolution
condition, per `evidence-rules.md`), build everything it does not block, stop only the blocked
slice. Never ship partial or stubbed work. Fan-out caps and retry rules:
`operational-rules.md` §fan-out.

**Conformance checks run after B and after C only** — a narrow, evidence-shaped question (did
this phase drift from, drop, or half-build a stated requirement?) answered with the clause, the
`file:line`, the gate actually run. No re-read passes after A, E, or F: stacking same-author
re-reads adds cost without recall, and the tokens saved pay for the browser/measurement evidence
Phase D requires (`model-and-effort.md` §6 draws the oracle-vs-re-read line).

### Phase A — Understand & specify

Parallel readers, one per plan slice/subsystem, each returning: exact files, contracts, closest
analogue, and the acceptance checks it fulfils. Synthesize ONE dependency-ordered build spec —
ordered slices, disjoint file sets, requirements covered. **Build the acceptance checklist now,
before code**: every Acceptance Criterion, Constraint & Decision, and triage Assumption (the
Clause table), and for every new user-facing capability its UI→producer wire (the Reachability
table), each row assigned to the slice that owns it. Re-deriving the list at review time is how
a requirement gets silently dropped; carry this same checklist into Phase D and fill it in, never
regenerate it. On a resumed run, rebuild from the FULL spec + plan — never from a previous
session's progress note.

### Phase B — Implement

Build in dependency order (the repo's own layering — schema/contract producers before consumers;
run the repo's codegen after contract changes). Parallelize only file-disjoint slices — never two
agents in one file. After each wave a gate subagent runs the scoped repo gates; the next wave
waits for green. Production code only.

**Executors — `executor-lanes.md` in full.** The default lane order for a plan-scoped slice:
**agy** (gemini-flash-3.7, `high`) → **grok** (grok-4.6, `high`; harness fallback cursor-agent)
→ **codex** (gpt-5.6-terra, `medium`, with the re-context harness — prefer it for slices long
enough to compact) → **Claude**. The never-delegate list, the prompt contract (absolute paths, a
distinctive-fact readback), the egress/opt-out grep per invocation, the verify-fix loop, and the
1-in-3 revert kill-switch all bind. Any lane failure routes back to Claude, logged.

**Each slice self-certifies** — "I edited these files" is not done: its checklist rows at
`file:line`, the real non-test caller reaching its new code, and for any critical seam the
real-path exercise actually run with the observed result. Exercise critical seams **test-first**:
write the real-path check, watch it fail, implement until green (a check written after the code
tends to encode the bug it was meant to catch).

**With the gate, two mechanical sweeps** (both in `test-strategy.md`): the **wire-through gate**
(every new endpoint/exported fn/action-seam field greps to a real non-test caller — a missing
caller is dead-on-arrival: fail the wave and wire it now) and the **affected-test sweep** (every
route/component/string/behaviour changed or inverted, every hit updated and RUN, with the
red@sha-before → green@sha-after proof recorded per behavioural requirement).

**Build surgically and simply**: every changed line traces to a checklist row; no drive-by
refactors; the minimum code that satisfies the row — this matters more under fan-out, where N
agents each over-building yields a conflict-prone diff that buries the real change.

### Phase C — Rebase onto `INT`

`git -C "$WT" fetch origin`, rebase onto the current tip, resolve every conflict faithfully
(integrate both sides — read the commit messages/PRs for each side's *why*; never drop existing
work or your own, never invent new behaviour). Mandatory even when Setup looked clean — the
rebase is where a stale-base duplication surfaces. Re-run the gate. Do NOT push.

### Phase D — Acceptance review vs the spec

Fill (never regenerate) both Phase A tables; every row closes per the **typed evidence rule**
(`evidence-rules.md`): static → `file:line`; visual → measurement; behavioural → exercised
request/response or red→green test; persistence → producer + stored row. No partial status; an
unclosable row is a blocker and the status stays put.

Fan out one reviewer per dimension — requirement completeness, correctness, guardrails
(the target repo's own load-bearing invariants, read from its CLAUDE.md + the plan's
constraints — never an assumed list), UI fidelity vs the mock index (measured, not read),
security (tenancy, visibility, injection, untrusted input), simplicity & surgical diff. Where
the `code-review` skill is installed, run it over the branch diff as one more lens — it carries
its own multi-pass sharding and verifier fan-out, and its findings merge into the same
disposition queue rather than a separate report. Findings
tagged Critical→Low with `file:line` and the exact clause violated. Never brief a reviewer to be
conservative — report everything, filter at disposition. **Adversarially verify aimed, not
blanket**: every Critical, every structural fix, anything reversing a locked decision. Criticals
cluster — any Critical on a high-trust surface buys one more full round. Exercise every
miss-class in `references/miss-classes.md` on the real path — reading the code is not the
exercise.

**Completeness critic — out of family, last.** Its only job is attacking the audit itself: which
checklist rows never got a satisfying `file:line`, which hop was never traced, which seam was
read but never exercised, which dimension went quiet on a large surface. Route per the ordered
review lanes (`second-opinion-lanes.md`): codex `gpt-5.6-sol` at `medium` (the R2 contract in
`codex-cli.md`) → agy → grok; all down or opted out → a Claude strong-model critic, recorded as
in-family. Give it the audit's own artifacts at absolute paths. Its output seeds the next round —
never straight into "resolved".

### Phase E — Resolve findings

Fix every confirmed finding at all severities — test-first for bugs, surgically, file-disjoint
fixes in parallel. Mechanical fixes may take the executor lanes on Phase B terms; diagnosis-hard
fixes and the never-delegate list stay with Claude. Re-gate, re-run the specific evidence checks
for each fixed row, then **one** targeted re-audit over fixed items + critic seeds — not a loop
until quiet.

### Phase D′ — Same-family validation (fresh context)

Before the status moves, the implementation's **own family** checks the work against the plan and
the tests, in a context that shares none of the build's premises: a fresh agent on the same lane
family that wrote the majority of the code (agy-built → a fresh agy/gemini agent; Claude-built →
a fresh Claude subagent), physically scoped to the pushed branch — it receives only the
ticket/spec text, the plan path, the branch name, and the mock index; never the build transcript
or the filled tables. It re-derives its own requirement list, checks it against the diff and the
test results, and returns discrepancies. Its findings route back through Phase E once. This is
the writer's family catching its own idiom-level slips cheaply before the cross-family verifier
spends real evidence-gathering on them; it does not replace `verify` and cannot set `Done`.

### Phase F — Finalize

Actually run the full repo gates — a gate that cannot run is recorded as a blocker, never an
implied pass. Commit outstanding fixes. **No push, no PR** (the conductor owns merge — see
"Merge mode"). Write the completion record (progress section or ticket comment, per the tracker
adapter) in the fixed shape: Summary · Branch (+`INT`, worktree) · Built by slice · Rebase ·
**Reachability table** · **Clause table** · Tests (red→green sha pairs; affected specs) ·
Acceptance review counts · **Implementation assumptions** (every call you made the spec didn't
determine — "assuming X (rather than Y)") · **Dropped or changed vs spec/plan** (an undisclosed
drop discovered later is a finding against this run) · Gates (actually run) · Executor + critic
accounting per lane · **Reviewing models** (wire-verified, so REVIEWER ≥ WRITER is checkable
from the artifact) · D′ validation outcome. Reconcile the plan's AC checkboxes — every unticked
box appears in the note as a blocker, deferral, or Dropped row. **Caveats propagate** verbatim
into any later record.

Two mechanical checks before the record is written, both cheap and both catching a shape prose
does not:

- **Scan the specs you added or touched for assertions that cannot fail** — the eight syntactic
  shapes in `evidence-rules.md` (`expect` with no matcher, expected == actual, constant vs
  constant, a swallowed `catch`, an un-awaited assertion, `skip`/`todo`, a discarded
  `expect.soft`, a spec file with zero assertions), or `warrant:assay`'s `cannotfail_scan.py`
  where the repo carries `.warrant/`. A hit is a candidate rather than a defect, but a red→green
  pair whose green comes from one of them discriminates nothing, and the pair is the evidence
  the whole clause table rests on.
- **Tie every screenshot in the record to its subject** — the URL the browser ended up at, and
  no two clauses sharing one sha256. `evidence-rules.md` carries why: a filename is written by
  whoever ran the capture, not by the app.

**Gate on the tables**: `Developer Review` is not set while any Clause or Reachability row is
not ✅. Then status → **`Developer Review`**. The item now awaits the `verify` skill — a
different family, a different session; nothing in this run may grade the ticket `Done`.

## Merge mode

An operator instruction to merge or push **changes the destination, never the bar**: run the
conductor's fail-closed pre-merge gate first (ship-feature `references/e2e-and-finalize.md`) —
every box actually checked now, including the verifier's verdict comment. A red or unverifiable
box means STOP and report the exact blocker; a merge instruction waives nothing.

## Commit convention

`<type>(<scope>): <summary under 72 chars>`, short body, `Resolves <ID>`,
`Co-Authored-By: Claude (AI Assistant) <noreply@anthropic.com>`. Stage only files you
created/modified — never `git add .`; never pass `-c user.email`/`-c user.name`.

## Guidelines

- Follow the target repo's CLAUDE.md. Production-ready code only.
- **Deliver what was asked, at the scope intended.** Routine judgment calls are yours; if the
  spec seems mistaken, say so in a sentence and continue as asked rather than quietly narrowing,
  widening, or transforming. Out-of-slice reach (a shared component, a global utility) is its own
  disclosed line item.
- Every phase A–F (+D′) runs to completion; a green gate is necessary, never sufficient
  (`evidence-rules.md`).
- Routing summary: readers/gate-runners `low` (cheapest tier) · evidence lenses `low–medium`
  (mid tier) · synthesis, conflict resolution, security/guardrails/identity lenses — strongest
  model, never downgraded · executors per `executor-lanes.md` · critic out-of-family at `max`.
  Step effort down before model down; hold effort constant per agent.
