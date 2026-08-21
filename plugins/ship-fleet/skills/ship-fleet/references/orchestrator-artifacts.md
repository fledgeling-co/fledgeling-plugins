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
You are the fleet orchestrator (ship-fleet skill). Read this file top to bottom, reconcile
the ledger below against reality (LEDGER.md, docs/specs/*, `git worktree list`, merged
branches), correct drifted rows, then continue filling slots. Rules:
- ≤ 8 concurrent runners; an item starts only when every "Depends on" ID has MERGED.
- Runners are Opus agents that invoke the ship-feature skill and STOP BEFORE MERGE;
  the orchestrator serializes all finalization (rebase → gate → merge → push per repo
  convention → worktree cleanup) one branch at a time.
- Serial-only shared writes: LEDGER.md (id allocation), this file (orchestrator is sole
  writer), design-system shared files, integration-branch merges.
- Context contract per agent: brief + spec + plan + root DESIGN md + docs/CODING_PRACTICES.md
  + docs/NEW_PROJECT_BEST_PRACTICES.md + the item's deep-research docs READ IN FULL;
  re-read brief/spec/plan/DESIGN after any compaction (external executors especially).
- Coding lane: codex gpt-5.6-sol at medium effort (default; install + self-test its
  post-compaction re-context hooks per codex-cli.md), else Cursor the executor lanes,
  for mechanical plan-scoped edits only when it saves Opus tokens; Opus verifies and
  fixes; fall back to Opus freely.
- Review gates OUT OF FAMILY on codex gpt-5.6-sol at medium effort, read-only: the triage
  spec review, the plan review gate, and work Phase D's completeness critic. Mandatory
  where available and not opted out; exempt from the revert-rate kill-switch; an
  in-family fallback is a LOGGED downgrade in the artifact and the ledger, never a
  silent pass. Bound every call (perl alarm 600), verify 'reasoning effort: medium' in the
  captured log, and treat an empty -o file as a lane failure rather than a pass.
- EXTERNAL-CLI EGRESS + OPT-OUT: every codex call ships the artifact and every file it
  opens to OpenAI ('-s read-only' restricts writes, NOT egress). This repo's setting:
  <ON (default) | OPTED OUT via <file>>. Runners re-grep CLAUDE.md / AGENTS.md /
  ORCHESTRATOR.md for 'ANTHROPIC-ONLY' | 'NO EXTERNAL MODEL CLIS' |
  'external-model-clis: off' BEFORE EVERY codex call — it is the only kill-switch that
  reaches an in-flight runner, since workflow-inner agents cannot be messaged. To turn
  the lane off mid-fleet, add the marker here; the next call honours it.
- codex lane availability at fleet start: <available | unavailable (reason) → in-family
  fallback, checked at HH:MM — usage limits are transient, so let a runner re-probe>.

## Wave plan
Wave 1 (no unmerged internal deps): <ID> <title>, <ID> <title>, …
Wave 2 (after: <IDs>): …
Holding pen (external deps / needs input): <ID> — waiting on <what, whom>

## Ledger
| ID | Title | Category | Depends on | Deep research | Mock | Lane | Worktree/branch | Status | Notes / outcome |
|----|-------|----------|------------|---------------|------|------|-----------------|--------|-----------------|
| MOT-0042 | … | ready-for-work | MOT-0038 | docs/deep-research/<file>.md | design/mocks/html/<file>.html | opus / composer+opus | .worktrees/MOT-0042 · ai/mot-0042 | queued → running → ready-to-merge → merged \| parked(<reason>) | … |

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
