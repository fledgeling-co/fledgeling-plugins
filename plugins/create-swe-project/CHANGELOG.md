# Changelog

## 1.13.1 - 2026-11-09

Two findings from an automated security review of 1.13.0's templates, both fixed:

- **`readJson` read a body with no Content-Length whole before applying its cap.** It now streams the body with a running byte count and cancels at the cap, and answers a malformed Content-Length with 400. A test feeds a 64 KB chunked stream against a 256-byte cap and asserts fewer than 20 chunks are pulled.
- **`clientIp` trusted the left-most X-Forwarded-For entry**, which the client writes, so the per-IP limits on sign-in and the waitlist could be dodged by rotating that header. It now reads `x-real-ip` only on Vercel, which sets it, and otherwise the right-most entry, which the nearest proxy appended; with neither, callers share one bucket. Referral counts remain unverified against someone with many real addresses, and the generated CLAUDE.md says to confirm by email before a count earns a reward.

## 1.13.0 - 2026-11-09

The team-files operating specs are now bundled and carried out by the templates, not only copied beside them. Measured on this machine before the change, every scaffold shipped a CLAUDE.md citing `docs/CODING_PRACTICES.md` and `docs/NEW_PROJECT_BEST_PRACTICES.md` while neither file existed: `~/Dev/bella-team-files` held only a `.claude/` directory, and the copy step warned and carried on.

- **Bundled specs.** `references/team-files/` holds CP, BP and CLAUDE-STARTER at team-files commit `00b2d4c` (DESIGN.md excluded as one product's aesthetic). `scripts/sync-team-files.sh` refreshes it; `scripts/check-conformance.py` exits 1 while any of the 48 numbered sections lacks a row in `references/team-files-conformance.md`.
- **CLAUDE.md on CLAUDE-STARTER's shape**: a per-module CP/BP routing map, the gate as the done criterion with `code-review:code-review` before a PR, and `docs/DIVERGENCES.md` for every deliberate departure.
- **Toolchain (BP §1, §2, §23):** pnpm pinned to 12.18.0 instead of whatever the caller's directory resolved (from inside dAIolog that was 8.15.1, which has no catalogs); release-age cooldown and a build-script allowlist; `scripts/pin-latest.py` rewrites every committed `latest` to the caret range installed; Node 24.9+ with `.nvmrc`; TypeScript 7 `tsc` beside a 6.0 compiler API, replacing the retiring `@typescript/native-preview`.
- **Security (BP §9, §10, §12, §24; CP §4, §6.1–§6.11):** nonce CSP in `proxy.ts` for web and admin; short HSTS; origin check, per-IP limit and a size-capped Zod body on every state-changing route; sign-in codes consumed by an atomic compare-and-delete; single-use refresh tokens via GETDEL; atomic find-or-create; identical responses with sends after the response; `__Host-` cookies in production; secrets refused under 32 characters; non-production email limited to `OUTBOUND_ALLOWED_DOMAINS` and production APNs refused outside production; dev login decided by a server component instead of `NODE_ENV` in client code; Swagger off in production; `APP_PIPE` validation with forbidNonWhitelisted.
- **Data (BP §4, §5; CP §6.3, §6.8):** node-redis replaces ioredis; `strictQuery: 'throw'`; connection caches clear on a failed connect; MULTI-based rate limiter; a guard for destructive scripts against non-local databases.
- **Testing (BP §15):** Vitest unit and integration projects with a `server-only` stub, an in-memory Redis fake and a Mongo replica set; Playwright replaces the Obscura harness and its `@smoke` tests check the CSP nonce and headers on a production build.
- **Gate (BP §19):** `scripts/gate.mjs` runs env parity, lint, typecheck, test, build (`vercel build` once linked), e2e smoke, swift and cargo, scoped to the packages a push changed and full whenever the range can't be computed. `SKIP_GATE` is gone; `GATE_FULL=1` and `SKIP_VERCEL_BUILD=1` remain.
- **Local dev (BP §17, §18, §20, §21, §23):** `*.localhost` hosts with no sudo; compose on 127.0.0.1 with a replica-set Mongo, per-service module volumes, shadowed members and masked native trees; Expo on pnpm's isolated install with default Metro; `scripts/check-env.mjs`; worktree add/prune scripts; a `git check-ignore` self-test before the first commit.
- **Latent template failures the new gate exposed and fixed:** NestJS 12 under Jest needs `--experimental-vm-modules` as well as Node 24.9+; `@sentry/nextjs` 11 moved `withSentryConfig` to `/config`; node-redis 6's native addon needs `serverExternalPackages`; the canary's EXIT trap made a healthy run exit 1.
- **Waitlist no longer reveals membership** (CP §6.1). Joining with an address already on the list used to return that person's position and share code. Every join now gets the same response and a fresh opaque viewer cookie; only a real insert stores it, so only the browser that joined sees its status. The lookup by share code is gone, and a route test proves identical responses for new and known addresses.
- `upgrade.sh` carries a project's pinned ranges into its renders, so an untouched package.json is not upgraded back to `latest`.

Verified 2026-11-09: `canary.sh` scaffolded all four permutations (all modules, saas, native, site) and each full gate passed; arming runs turned the env-parity check and the CSP smoke test red against deliberate breakage and green on restore.

## 1.12.2 - 2026-09-01

Refreshes `gemini.md` against a `SKILL.md` that had changed since it was written. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 1.12.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

## 1.12.0 - 2026-08-27

- **Positioning Audit & Integration**: The launch pipeline now checks for existing positioning documents in `docs/positioning/` (e.g. `00-decision.md` or `10-territory-*.md`) and invokes `/positioning:positioning` if absent, ensuring all product messaging and feature value propositions are evidence-grounded before drafting copy.
- **Initial Comprehensive Technical `PRD.md` Generation**: Added `PRD.md.tmpl` to template base and updated the launch pipeline (Phase O) to generate an initial comprehensive technical requirements document covering **ALL** briefs in `docs/features-to-triage/*.md` with complete feature traceability matrices, persona mappings, and non-functional requirements.
- **Enhanced `OVERVIEW.md` Architecture & Context**: Added structured Mermaid system architecture and direct grounding pointers to `docs/positioning/00-decision.md` and `docs/deep-research/`.

## 1.11.0 - 2026-08-22

- Initial launch pipeline and multi-platform scaffolding architecture.
