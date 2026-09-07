# The orchestrator artifacts — ORCHESTRATOR.md + orchestrator-hierarchy.html

Both live at the **project root**, both are committed, and both are written **before** the first fleet slot starts. `ORCHESTRATOR.md` is the machine the fleet runs on; the HTML is the human window into it.

## ORCHESTRATOR.md — plan + ledger in one file

Design goal: **a fresh session with zero conversation memory can resume the entire fleet from this one file.** That means it carries not just state but the operating rules. Keep it current — update it *before* acting on any state change, so a crash never loses an event.

Template (adapt sparingly; keep every section):

```markdown
# ORCHESTRATOR — <project name> remaining-work plan & ledger

**Status:** Planning | Running | Paused | Complete
**Updated:** <ISO date + what changed last>

## How to resume
You are the fleet orchestrator using ship-fleet:ship-fleet. Read this file,
reconcile the ledger against LEDGER.md, docs/specs/*, worktrees and actual merged
branches, then continue at the first incomplete item. Rules:
- Concurrency: <resolved cap>, the minimum of the user's cap, tool limit,
  five-runner policy and measured host capacity. Missing telemetry uses at most
  two runners within that cap; measured zero means no launch and a saved wait state.
- An item starts only when every "Depends on" ID has MERGED. Use
  ship-feature:ship-feature for one feature; pass the identifier and arguments
  separately. Runners stop before independent verification and before merge;
  the orchestrator owns per-item verification and serializes finalization.
- Serial-only shared writes: LEDGER.md allocation, this file, shared design tokens,
  and integration-branch merges. Each runner owns one explicit file/worktree scope.
- Model roles: <user-selected supported roles/IDs/efforts and authorized fallbacks>.
  Normally GPT-6 coordinates, Opus 5 produces intake/triage/plan, and Gemini 3.8
  implements after those artifacts land. A skill invocation does not switch models.
- Routing references: <absolute shipyard model-lanes.md, executor-lanes.md and
  relevant CLI-reference paths>. Read them rather than reconstructing a model list.
- Stage handoff: objective, brief/spec/plan revisions, DESIGN/mock index, relevant
  practices/research sources, allowed files, required outputs, checks and finish line.
  Read prerequisite artifacts before acting; reread after compaction and reconcile WIP.
- Independent review: choose a capable supported family different from the actual
  artifact writer. Record real model/effort metadata where exposed, verdict and
  findings disposition. Empty/partial results and unavailable identity remain visible.
  An in-family fallback is degraded evidence, not a substitute for an independent gate.
- Provider policy: <active directives and authorized providers, with source paths>.
  Interpret current policy, including the scaffold's anchored opt-out and explicit
  legacy directives. A marker quoted as an example is not an active restriction.
- Lane availability: <per selected role: available | unavailable (reason), observed
  at time, authorized fallback>. Refresh when state changes. Bound calls and waits;
  preserve checkpoints rather than silently skipping a failed or timed-out item.

## Wave plan
Wave 1 (no unmerged internal deps): <ID> <title>, <ID> <title>, …
Wave 2 (after: <IDs>): …
Holding pen (external deps / needs input): <ID> — waiting on <what, whom>

## Ledger
| ID | Title | Category | Depends on | Deep research | Mock | Lane | Worktree/branch | Status | Notes / outcome |
|----|-------|----------|------------|---------------|------|------|-----------------|--------|-----------------|
| MOT-0042 | … | ready-for-work | MOT-0038 | docs/deep-research/<file>.md | design/mocks/html/<file>.html | <actual writer / reviewer> | .worktrees/MOT-0042 · ai/mot-0042 | queued → running → ready-to-merge → merged \| parked(<reason>) | … |

## Deferred children discovered mid-fleet
| Child | Parent | Where it runs | Status |

## Needs input (consolidated for the user)
- <ID>: <the question, verbatim enough to answer>

## Event log (append-only, newest first)
- <date> <ID> merged (<commit>) — slot freed → started <ID>
```

Category values come from the survey: `resumable`, `ready-for-work`, `ready-for-plan`, `untriaged`, `deferred-child`, `design-refresh`, `needs-input`. Status transitions are the ledger's heartbeat — never batch them up; write each as it happens.

## orchestrator-hierarchy.html — the visual hierarchy

A **single self-contained HTML file** (inline CSS/JS, no external assets, no build step) that renders the remaining-work hierarchy at a glance:

- **Waves as horizontal bands**, top (ready now) to bottom (most-blocked); the holding pen as a visually distinct final band.
- **One card per item**: id, title, category badge, lane badge (opus / composer+opus), status colour (queued grey · running blue · ready-to-merge amber · merged green · parked red), and its worktree/branch when live.
- **Dependency edges** drawn between cards (SVG lines/arrows are fine; a nested indented tree is an acceptable fallback when edges would spaghetti).
- **Deferred children** nested under their parent card.
- A small legend + the `Updated:` stamp matching ORCHESTRATOR.md.

Regenerate (or update the status colours of) the file at minimum on: fleet start, each merge, each parking, fleet completion. It must always agree with the ledger table — generate it *from* the ledger data, don't maintain it by hand in parallel.

Both files are committed to the integration branch alongside the docs they summarize (commit message like `orchestrator: <event>`), so the fleet's history travels with the repo.
