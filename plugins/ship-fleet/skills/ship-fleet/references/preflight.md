# Preflight — check and repair the project's pipeline conventions

> **Lane assignments are `defer`'s now.** Run
> `python3 <defer>/skills/defer/scripts/lane_pick.py --task <class>` for the model,
> the effort and the exact argv, or `lane_run.sh <class> "<prompt>"` to run and
> wire-verify it in one step. The classes are `implementation`, `completeness`,
> `general`, `referral`, `verification` and `design-review`. Three rules bind
> everywhere: `gpt-5.6-sol` never runs at `max` (it is the referral lane at
> `medium`, and other work goes to `gpt-5.6-terra` at `high`), Fable judges but
> never grades code or a ticket, and design review stays on Opus and Fable. What
> follows is this pipeline's reading of that policy, not a second copy of it.

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

## 5. Codex lane availability (check once, here)

Three review gates in this pipeline route **out of Claude's model family** on purpose — the triage spec review, the plan review gate, and work Phase D's completeness critic, each on `gpt-5.6-sol` at `medium` effort — plus a `medium`-effort implementation executor. Check the lane once at fleet start so every runner inherits the same picture instead of each discovering it mid-run.

**Check the repo opt-out FIRST — it outranks availability.** Every Codex call is data egress: `-s read-only` restricts writes, not the network, so the reviewer transmits the artifact and every source file it opens to OpenAI. The lane is **on by default and opted out per repo**:

```bash
grep -rlE 'ANTHROPIC[- ]ONLY|NO EXTERNAL MODEL CLIS?|external-model-clis:\s*off' \
  CLAUDE.md AGENTS.md ORCHESTRATOR.md docs/CODING_PRACTICES.md 2>/dev/null
```

A hit ⇒ record `codex: opted out (<file>)` in ORCHESTRATOR.md, tell every runner to run fully in-family, and stop here — an opted-out fleet is a correct fleet, not a degraded one. **Runners re-check this marker before every single Codex call**, not once: a fleet cannot message its own in-flight workflow agents, so this file is the only kill-switch an owner has if they ban external CLIs mid-run. Say so explicitly in the runner prompt. If the owner has not expressed a preference and the repo holds auth, secrets, tenancy or payment code, surface the egress tradeoff in the preflight report and let them decide before the first gate runs.

If there is no opt-out, probe availability:

```bash
command -v codex && codex --version                       # expect codex-cli 0.145.0+
codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" \
  -s read-only --skip-git-repo-check "Reply with exactly: OK" < /dev/null
```

Record the outcome in ORCHESTRATOR.md's header contract as `codex: available` or `codex: unavailable (<reason>) → in-family fallback`:

- **Available** → the three gates run on Codex; the executor lane is open.
- **Unavailable** — no binary, not logged in (`codex login`), a usage/rate-limit response, or the probe erroring — → every gate falls back to its Claude reviewer and every executor slice falls back to Opus. The pipeline still runs; the review evidence is just weaker, and **that has to be visible in the ledger** rather than discovered later. Don't install unprompted; offer `npm i -g @openai/codex` (or the Codex desktop app) and `codex login`.

Usage limits are a *transient* unavailability — a lane that fails at fleet start may work an hour later. Note the time, and let a runner re-probe rather than treating the fleet-start result as permanent. The **opt-out is not transient in the same way**: it is a standing owner decision, so a runner re-reads it to see if it has appeared, never to see whether it has expired.

Two operational rules the runner prompt must carry, both learned from a real fleet: **bound every Codex call** (`perl -e 'alarm shift @ARGV; exec @ARGV' 600 codex exec …` — there is no timeout flag and macOS has no `timeout(1)`) so a slot is never held by an unbounded polling loop, and **verify the effort on the wire** (`grep -qx "reasoning effort: medium"` on the captured log) because a dropped flag silently inherits the user's own config default. Full mechanics live in shipyard's `references/codex-cli.md`.
