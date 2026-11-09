# CLAUDE.md

<!-- ═══════════════════════════ TEMPLATE INSTRUCTIONS — DELETE THIS BLOCK ═══════════════════════════
This file is CLAUDE-STARTER.md from the team-files repo, copied into a new project per
NEW_PROJECT_BEST_PRACTICES.md §27 (day-one checklist). When scaffolding the project:

1. Copy this file to the repo root as CLAUDE.md and create AGENTS.md as a symlink:
       cp <team-files>/CLAUDE-STARTER.md CLAUDE.md && ln -s CLAUDE.md AGENTS.md
2. Copy CODING_PRACTICES.md and NEW_PROJECT_BEST_PRACTICES.md into docs/ (the paths below assume docs/).
3. Replace every <ANGLE-BRACKET> placeholder with project reality. Every command, path and hostname you
   write must exist in the tree or in package.json when you write it, because the agent will run or open
   it verbatim; leave a line out rather than fill it with a guess.
4. Delete any section that doesn't apply yet (e.g. Documentation map on day one) rather than leaving
   skeleton headings. Claude Code loads this file into every session and its docs target under 200 lines
   per CLAUDE.md, so keep the filled-in file under that; depth belongs in docs/.
5. Delete this instruction block.
═══════════════════════════════════════════════════════════════════════════════════════════════════ -->

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Operating rules — load before writing code

Two operating specs govern the code in this repo. They are the rules the `code-review:code-review` skill blocks on, so applying them **as you write** is what makes a review come back clean:

- **`docs/CODING_PRACTICES.md`** (cited as **CP §n**) — TypeScript boundary safety, NestJS, Next.js App Router + React 19, OWASP-aligned security, cross-cutting logic-bug patterns (CP §6.14), client React / React Native hygiene (CP §6.15), and the review checklist (CP §7).
- **`docs/NEW_PROJECT_BEST_PRACTICES.md`** (cited as **BP §n**) — stack defaults and day-one decisions: dependency versions (BP §1–§2), monorepo/pnpm/Turborepo (BP §17), the quality gate (BP §19), the Caddy + Docker dev stack (BP §20–§21), design tokens (BP §22), env/tenant-correct behaviour (BP §24), and changing security controls safely (BP §25). When a task is underspecified, take the BP default instead of inventing one; when you deliberately diverge, say so and why.

Each spec runs to roughly 22,000–25,000 tokens, so read the shared baseline plus the sections for the area you are changing, rather than both files end to end:

<ROUTING-MAP: keep the first two rows, then one row per area of this repo, with real paths. e.g.:

| You are changing | Read first |
|---|---|
| anything | CP protocol (top of the file), §1, §5, §7 |
| a mutation path (endpoint, Server Action, job, webhook) | CP §4, §6.1, §6.3, §6.8, §6.14 |
| `apps/api/**` (NestJS) | CP §2, §6.11 |
| `apps/web/**` (Next.js) | CP §3, §6.2, §6.4–§6.9, §6.12, §6.13, §6.15 |
| `apps/<native>/**` (Expo) | CP §6.13, §6.15; BP §18 |
| `packages/contract/**` or any wire shape | CP §6.10; BP §17 |
| auth, sessions, CSP, validation or RBAC middleware | CP §4, §6.1, §6.2, §6.7; BP §25 |
| the gate, test setup or CI | BP §15, §19 |
| Docker, Caddy, Storybook, design tokens | BP §20–§23 |
| a new dependency or a toolchain upgrade | BP §1, §2; CP §4 (A03) |
>

A change is done when the quality gate in **Commands** passes. Report its result, and quote the output of anything that failed. Before opening a PR, run the `code-review:code-review` skill on the diff: it checks the CP rules the gate can't, such as auth order, logging and contracts. Where that skill isn't installed, apply CP §7 as the review checklist instead.

Deliberate divergences from the specs are logged in <WHERE-DIVERGENCES-ARE-LOGGED — e.g. `docs/plans/<project>-v1.md` § "Deliberate divergences"> — check there before "fixing" something that looks non-compliant.

**Behaviour under ambiguity** (for trivial tasks, use judgment):

- **Decide routine calls; ask about real forks.** Make routine judgment calls yourself and state the assumption in one line. Check in only when different readings of the request would lead to materially different work, and name the readings when you do. If the request looks mistaken or a better approach exists, say so in a sentence and continue with the task as asked.
- **Simplicity first.** Minimum change that solves the problem. No speculative features, abstractions, or impossible-case handling. Test: would a senior reviewer call this overcomplicated?
- **Surgical changes.** Don't "improve" adjacent code; match existing style; mention unrelated problems instead of fixing them. Clean up only orphans your own change created. Test: every changed line traces to the request.
- **Goal-driven execution.** Turn the task into checkable success criteria before starting ("fix the bug" → "a test reproducing it passes; the gate stays green") and finish when they pass.

## Project overview

<ONE-PARAGRAPH: what the product is, who it's for, and the stack in one line — e.g. "a Next.js 16 App Router app + NestJS API in a pnpm/Turborepo monorepo, MongoDB + Redis, deployed on Vercel.">

## Repo layout

<LAYOUT-BLOCK: one line per app/package/top-level dir stating what it is and its cardinal constraint.
Keep it to what a new contributor needs to place code correctly — e.g.:

```
apps/web/            <what it is — and its boundary rule, e.g. "the BFF; the browser's only backend">
apps/api/            <what it is — e.g. "NestJS authority: persistence, domain logic, authZ">
packages/contract/   Shared Zod wire DTOs across api + web (one source of truth — CP §6.10)
docs/                Durable docs + the operating specs
```
>

<IF-MULTI-TIER: state the server-boundary rule here — which layer owns persistence/auth/secrets vs
session/aggregation/web-surface security, and that the browser calls only its own BFF (BP §24).>

## Commands

```bash
<ONLY-COMMANDS-THAT-EXIST-IN-package.json — the gate first, then dev servers, then utilities. e.g.:
pnpm gate            # typecheck + lint + test + build — run before claiming done
pnpm dev             # <what it starts>
pnpm stack:up        # <the Docker dev stack — BP §20/§21>
>
```

The quality gate is <GATE-MECHANISM per BP §19 — e.g. "the husky pre-push hook running `pnpm gate`; `SKIP_VERCEL_BUILD=1` skips only its Vercel build step; there is intentionally no hosted CI">. Run a single test file with <VERIFIED-SINGLE-TEST-INVOCATION>.

## Documentation map

<ONE-BULLET-PER-DURABLE-DOC: what it is, when to read it, when to update it. Rule: update the right doc
**in the same change** that makes its contents stale. Include at minimum:
- the plan/roadmap of record (read before building a feature; fold new ideas in here first)
- the operating specs (see "Operating rules" above)
- the design/UI reference, if any (mock/design system is the source of truth; keep it and the app in lockstep)
Delete this section on day one if the only docs are the operating specs.>

## Conventions (repo deltas — the operating specs carry the rest)

<ONLY-RULES-THAT-DIFFER-FROM-OR-BIND-THE-SPECS-TO-THIS-REPO, as checkable behaviours. e.g.:
- Wire shapes live in `packages/contract` (CP §6.10); bump its version with any contract change.
- Every trust boundary is Zod-validated, never cast (CP §1) — including AI/model output.
- <project-specific token/design-system rule>
Do NOT restate CP/BP rules here — cite them.>

## Keeping this file honest

`AGENTS.md` is a **symlink** to this file (non-Claude agents read the same text) — edit only `CLAUDE.md`, and never replace the symlink with a copy. Update this file in the same change as any behaviour/architecture shift; put new depth in `docs/` (a routed reference doc), not here — this file is loaded into every session, so every line must earn its place. **Working if:** diffs stay scoped to the request; every "done" report quotes the gate result; commands and paths cited here actually exist in the tree; docs and code land in the same change.
