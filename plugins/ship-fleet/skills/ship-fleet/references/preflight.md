# Preflight — check and repair the project's pipeline conventions

> **Routing precedence:** use shipyard's `references/model-lanes.md`. Explicit user
> preferences and current supported models come before `defer:defer`'s measured
> fallback registry. CLI examples below describe their named lanes; they do not
> select a model for the user or establish current availability.

## Policy markers — active directives only

Before a routed call, read the current project policy and the user's existing
authorization. The scaffold's explicit opt-out is a line beginning
`OPT-OUT: external-models`. Also honor explicit legacy directives
`ANTHROPIC-ONLY`, `NO EXTERNAL MODEL CLIS`, or `external-model-clis: off`.
A quoted example, code sample, or explanation mentioning a marker is not itself
an opt-out. Interpret an actual directive rather than treating any grep hit as
policy. Apply the governing instruction priority; do not request permission again
when the conversation already authorizes the selected provider and action.


Run this before the survey, interactively. The point is that ship-fleet (and the skills it conducts) rely on a conventional layout; a repo that half-has it produces a half-blind survey. Check everything, report plainly, **offer** repairs — never restructure silently.

## 1. Structure check

Resolve each expected artifact **inside the project** (Glob; exclude `.worktrees/`, `node_modules/`):

| Check | Expected | Missing → offer |
|---|---|---|
| Ledger | `docs/features-to-triage/LEDGER.md` (or legacy `docs/feature-specs/LEDGER.md`) | Create `docs/features-to-triage/` + a fresh LEDGER.md: ask the user for a 3-letter project code, write the `Project code` / `Last allocated: 0` header + empty table (match the triage skill's format) |
| Specs dir | `docs/specs/` | Create empty dir |
| Plans dir | `docs/plans/` | Create empty dir |
| Briefs dir | `docs/features-to-triage/` | Create empty dir |
| Mocks | `design/mocks/html/` | Create empty dir; note the survey will have no design-refresh lane. Mockless features lose nothing downstream — ship-feature's design stage authors each feature's full UI (surfaces, states, interactions, flows, modals) in the design system regardless |
| Deep research | `docs/deep-research/` | Create empty dir; note runs proceed without research context |
| Design language | `DESIGN*.md` at project root | Ask the user for one (or point at design-md-from-website / design-md-from-screenshots skills); UI stages degrade without it |
| Best practices | `docs/CODING_PRACTICES.md` + `docs/NEW_PROJECT_BEST_PRACTICES.md` | See §2 |
| Git | repo root is a git repo with a detectable integration branch | Hard requirement — stop and sort this with the user |
| Codex CLI | `codex` on PATH, logged in, `gpt-5.6-sol` answering | See §5 — the pipeline's three out-of-family review gates degrade to in-family without it |

Present one consolidated report (found ✓ / missing ✗ / degraded consequence), then a single AskUserQuestion for the repairs rather than one prompt per item.

## 2. Best-practices docs from the repo's team-files source

If either practices doc is missing from `docs/`:

1. If `<the local clone of that source>` exists → `git -C <the local clone of that source> pull`; else offer to `git clone <the repo's own team-files/practices source, named in its CLAUDE.md — e.g. a team-files repo> <the local clone of that source>`.
2. Copy **only** `CODING_PRACTICES.md` and `NEW_PROJECT_BEST_PRACTICES.md` into the project's `docs/`.
3. Never copy anything into `docs/specs/` or `docs/plans/` — those directories are written exclusively by the triage and plan skills; seeding them from outside corrupts the pipeline's id/state assumptions.

If the clone fails (no network, no access), say so and continue — the fleet still runs, agents just lose the practices context.

## 3. Gather stray feature briefs

Feature ideas tend to accumulate as loose markdown. Scan the repo root, `docs/` (top level), and note-ish directories (`notes/`, `ideas/`, `drafts/`) for markdown that reads like a **feature description** — a product capability someone wants — rather than:

- specs (`spec-*.md`) or plans (`plan-*.md`) — pipeline-owned, leave them,
- architecture/ops/README/marketing/testing docs,
- research reports (those belong in `docs/deep-research/`).

For each candidate, show the user the filename + first heading/opening line and what makes it feature-shaped. Offer to `git mv` the confirmed ones into `docs/features-to-triage/`. Moved briefs become Untriaged items in the survey.

## 4. Monolith layout check

Read the **project-layout section of the repo's own copy** of `docs/NEW_PROJECT_BEST_PRACTICES.md` — §3 (single-app layout: `app/`, `components/`, `lib/` with server-only boundary, `scripts/`, `public/`) or §17 (pnpm-workspaces/Turborepo monorepo: `apps/*`, `packages/*`) if the repo is multi-app. The doc is the source of truth, not this file — it evolves; compare against what it *currently* says.

Report deviations (missing `lib/` server-only boundary, route handlers outside `app/api/`, apps outside `apps/`, phantom top-level dirs) as a short list with severity. **Only restructure if the user asks** — the fleet can run on a non-conforming repo; the check exists so new code from the fleet doesn't inherit a broken shape, and so the user can choose to fix structure first as its own work item (queue it in the ledger if they do).

## 5. Routed lane availability (check once, then refresh when state changes)

Resolve the role policy in shipyard's `references/model-lanes.md`: normally
GPT-6 coordinates, Opus 5 produces intake/triage/plan, and Gemini 3.8 implements.
Review gates select capable supported families different from the actual artifact
writer. No gate depends on Codex specifically, and a model name alone proves no
family independence or review quality.

Read the active project policy and existing user authorization before a routed
call. The scaffold uses `OPT-OUT: external-models`; explicit legacy restrictions
also apply. Search hits in quoted examples are not active directives. If a route
is restricted, record the permitted fallback and whether independence is lost;
correct policy compliance does not turn in-family evidence into independent proof.

For each selected route, confirm the tool or binary, supported model and effort,
then run a bounded inert probe. Do not install a missing CLI unprompted. Record
`<role>: <actual lane> available | unavailable (<reason>) -> <authorized fallback>`
with the check time. Give runners this resolved state and the actual reference
paths; they re-read policy before calls and refresh a failed availability probe
when there is evidence the state may have changed.

CLI mechanics belong in shipyard's `references/executor-lanes.md` and
`references/codex-cli.md`. Requested flags and echo headers are configuration
checks; authoritative response/runtime metadata is execution evidence. An empty
output, absent required verdict or timed-out call is incomplete, not a quiet pass.
Record unavailable execution identity rather than inventing a wire-verification
claim. Use bounded waits and preserve the runner's checkpoint on lane failure.
