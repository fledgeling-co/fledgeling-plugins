# Team-files conformance map

Every numbered section of the two operating specs in `references/team-files/`, and where a scaffolded project carries it out. `scripts/check-conformance.py` fails when a section in those files has no row here, when a row names a section that no longer exists, or when a path cited below is missing, so a re-sync of the specs (`scripts/sync-team-files.sh`) cannot silently leave a new rule unmapped.

DESIGN.md from the same team-files repo is deliberately out of scope: it records one product's aesthetic, and each new project gets its own DESIGN.md from `design-md-from-website:design-md-from-website`.

Status meanings, one per row:

- **encoded**: the scaffold writes it as code, config or a gate, at the path given.
- **rule**: it governs code written later. The generated CLAUDE.md routes the area to that section of `docs/CODING_PRACTICES.md` or `docs/NEW_PROJECT_BEST_PRACTICES.md`, both copied into every project; nothing is generated because the scaffold has no code of that kind yet.
- **divergence**: the scaffold departs from it on purpose, with the row it writes into the project's `docs/DIVERGENCES.md`.

Paths are relative to `skills/create-swe-project/`.

## NEW_PROJECT_BEST_PRACTICES.md (BP)

| Section | Status | Where |
|---|---|---|
| BP §1 | encoded; divergence for Storybook and always-monorepo | `templates/base/pnpm-workspace.yaml` (TypeScript 6 and ESLint 9 holds), `templates/base/tsconfig.base.json` (strict, noUncheckedIndexedAccess), `templates/base/dot_nvmrc` + `templates/base/package.json.tmpl` (Node 24), `templates/web/tsconfig.json` (`@/*`, no baseUrl); `templates/fragments/divergences/header.tmpl`, `templates/fragments/divergences/web.tmpl` |
| BP §2 | encoded | `templates/base/pnpm-workspace.yaml` (minimumReleaseAge, strictDepBuilds, allowBuilds), `scripts/pin-latest.py` (every `latest` becomes the resolved caret range) |
| BP §3 | encoded | `templates/server-lib/lib/env.ts` and every server `lib/` file open with `import 'server-only'`; `templates/web/` follows the layout |
| BP §4 | encoded | `templates/data/lib/db.ts` (globalThis promise cache, `strictQuery: 'throw'`), `templates/data/lib/models.ts`, `templates/data/lib/types.ts`, `templates/data/scripts/lib/assert-local-db.ts.tmpl` |
| BP §5 | encoded | `templates/kv/lib/redis.ts` (node-redis, fails closed), `templates/kv/lib/rate-limit.ts` |
| BP §6 | encoded; AI Elements and tool `stopWhen` are rule | `templates/web/lib/ai.ts.tmpl`, `templates/api/src/ai.ts.tmpl` (one MODELS object, Gateway routing with dash normalisation, `Output.object`, credential check) |
| BP §7 | rule | `@vercel/blob` is a web dependency and `templates/csp/lib/csp-origins.ts` allows its upload host; the first upload route follows BP §7 |
| BP §8 | encoded | `templates/auth/lib/email.ts.tmpl` (Resend + React Email, result error checked), `templates/auth/emails/` |
| BP §9 | encoded; divergence for token lifetime | `templates/auth/lib/auth-server.ts.tmpl`, `templates/auth/lib/users.ts`, `templates/admin/lib/auth-admin.ts.tmpl`; `templates/fragments/divergences/auth.tmpl` |
| BP §10 | encoded | `templates/server-lib/lib/http.ts` (origin check, capped Zod body, 400 on malformed JSON), applied in every route under `templates/auth/app/api/` |
| BP §11 | rule | no webhook is scaffolded; the routing map sends any mutation path to CP §4/§6, and BP §11 governs the first webhook |
| BP §12 | encoded | `templates/csp/proxy.ts` + `templates/csp/lib/csp.ts` (nonce CSP), `templates/web/next.config.ts.tmpl` (static headers, short HSTS); audit logging is rule, stated in `templates/fragments/claude/admin.tmpl` |
| BP §13 | encoded | `templates/web/dot_env.example.tmpl`, `templates/base/dot_gitignore`, `templates/base/scripts/check-env.mjs`; scaffold.sh proves nested env files are ignored before the first commit |
| BP §14 | encoded | the web `script` npm script (`tsx --conditions=react-server`, added by scaffold.sh), `templates/fragments/caddy/` |
| BP §15 | encoded | `templates/server-lib/vitest.config.ts` (unit vs integration, `server-only` stub), `templates/auth/test/fake-redis.ts`, `templates/auth/lib/users.test.ts.tmpl` (in-memory replica set), `templates/web/playwright.config.ts.tmpl`, `templates/web/e2e/smoke.spec.ts.tmpl`, `templates/api/jest.config.js` |
| BP §16 | encoded | `templates/web/vercel.json`, explicit `maxDuration` on cron routes, `templates/fragments/deploy/web.tmpl`, `templates/api/src/app.module.ts` (in-process cron) |
| BP §17 | encoded; contracts are rule | `templates/base/pnpm-workspace.yaml`, `templates/base/turbo.json`, `templates/base/dot_gitignore`, `templates/web/Dockerfile.tmpl`; `packages/contract` arrives with the first cross-app feature, stated in `templates/fragments/claude/footer.tmpl` |
| BP §18 | encoded | `templates/rn/` (isolated install, default Metro, distinct ids, testIDs, Maestro by id, Node-env vitest) |
| BP §19 | encoded; divergence while unlinked | `templates/base/dot_husky/pre-push`, `templates/base/scripts/gate.mjs` (path-aware, fail-safe, GATE_FULL, SKIP_VERCEL_BUILD, `vercel build` when linked) |
| BP §20 | encoded | `templates/fragments/caddy/header.tmpl` (`*.localhost`, conf.d mirror, no sudo) |
| BP §21 | encoded | `templates/fragments/compose/` (127.0.0.1 ports, replica-set Mongo, per-service module and store volumes, shadowed members, masked native trees, 127.0.0.1 healthchecks) |
| BP §22 | encoded for tokens; divergence for Storybook | `templates/tokens/` (single source, drift gate); `templates/fragments/divergences/web.tmpl` |
| BP §23 | encoded | `templates/base/scripts/worktree-add.sh`, `templates/base/scripts/prune-merged-worktrees.sh`, `templates/base/dot_watchmanconfig`, TypeScript 7 `tsc` beside 6 in `templates/base/pnpm-workspace.yaml` |
| BP §24 | encoded; feature flags are rule | `templates/server-lib/lib/env.ts` (`appEnv()`), `templates/auth/lib/outbound.ts`, `templates/auth/lib/dev-login.ts`, `templates/push/lib/push.ts.tmpl`, `templates/web/eslint.config.mjs` (BFF restrictions) |
| BP §25 | rule | routed from the auth row of the generated CLAUDE.md (`templates/fragments/routing/auth.tmpl`) |
| BP §26 | encoded where lintable, otherwise rule | `templates/web/eslint.config.mjs` (`no-console`, BFF), every rule above that removes a listed anti-pattern |
| BP §27 | encoded | this table is the checklist's expansion; the decide-first items are the interview in SKILL.md §2 |

## CODING_PRACTICES.md (CP)

| Section | Status | Where |
|---|---|---|
| CP §1 | encoded in templates, rule after | explicit return types and Zod parsing across `templates/`; strict compiler flags in `templates/base/tsconfig.base.json` |
| CP §2 | encoded | `templates/api/src/app.module.ts` (`APP_PIPE` ValidationPipe, `APP_GUARD`), `templates/api/src/main.ts.tmpl` (shutdown hooks, docs off in production), `templates/api/jest.config.js` (@swc/jest, Jest 30 options) |
| CP §3 | encoded | `templates/web/app/layout.tsx.tmpl` (format-detection, async headers), per-page metadata, `templates/csp/proxy.ts` |
| CP §4 | encoded | A01 origin and scoped queries (`templates/server-lib/lib/http.ts`), A02 headers and docs gating, A03 cooldown and pins, A04 `timingSafeEqual` and secret length, A07 code flow, A09 `templates/server-lib/lib/logger.ts`, A10 fail-closed env |
| CP §5 | encoded | `templates/server-lib/lib/logger.ts` as the only console writer, enforced by `templates/web/eslint.config.mjs` |
| CP §6.1 | encoded | `templates/auth/app/api/auth/request-code/route.ts`, `templates/admin/app/api/admin-auth/request-code/route.ts` (origin, per-IP limit, equal response and timing), `templates/waitlist/app/api/waitlist/route.ts` (identical response and cookie for a known address) |
| CP §6.2 | encoded | strict SameSite cookies at Path=/ plus origin checks in `templates/auth/lib/auth-server.ts.tmpl` |
| CP §6.3 | encoded | atomic upserts in `templates/auth/lib/users.ts` and `templates/waitlist/lib/waitlist.ts`, self-clearing connection cache in `templates/data/lib/db.ts` |
| CP §6.4 | encoded for client IPs, rule for uploads | `templates/kv/lib/rate-limit.ts` takes the IP only from a proxy-written header (Vercel's `x-real-ip`, else the right-most X-Forwarded-For); upload-token rules govern the first upload route |
| CP §6.5 | rule | no anonymous demo path is scaffolded |
| CP §6.6 | encoded | React Email templates only; no raw-HTML email is generated |
| CP §6.7 | encoded; divergence for styles | `templates/csp/lib/csp.ts`, `templates/csp/proxy.ts`, smoke test on a production build; `templates/fragments/divergences/web.tmpl` |
| CP §6.8 | encoded | `templates/data/scripts/lib/assert-local-db.ts.tmpl`, `templates/base/dot_gitignore`, `templates/server-lib/lib/env.ts` (`requireSecret`, `optionalEnv`), `templates/base/scripts/check-env.mjs`, fail-closed Redis |
| CP §6.9 | encoded | `templates/web/eslint.config.mjs` (eslint-config-next core-web-vitals), labelled form controls, per-page metadata |
| CP §6.10 | rule | `packages/contract` with the first cross-app feature (`templates/fragments/claude/footer.tmpl`) |
| CP §6.11 | encoded | `templates/kv/lib/rate-limit.ts` (MULTI INCR + EXPIRE NX), refresh tokens hashed as keys |
| CP §6.12 | encoded | explicit `maxDuration` on `templates/web/app/api/health/route.ts`; one `vercel.json` |
| CP §6.13 | rule | no React Query layer is scaffolded |
| CP §6.14 | rule | routed from the mutation-path row of the generated CLAUDE.md |
| CP §6.15 | encoded in templates, rule after | labelled controls, `aria-live` status, pending state in `templates/auth/components/login-form.tsx`; RN testIDs and `accessibilityRole` in `templates/rn/App.tsx.tmpl` |
| CP §7 | encoded | the done criterion and review step in `templates/fragments/claude/header.tmpl` |

## Measured against the specs

Two findings from running the scaffold that the specs do not yet say, recorded so the next sync can carry them upstream:

- **NestJS 12 under Jest needs `--experimental-vm-modules` as well as Node 24.9+.** Jest 30 enables native `require(esm)` only when `vm.SourceTextModule` exists, which Node exposes behind that flag (`supportsSyncEvaluate` in `jest-runtime`). Without it every API suite fails with "Must use import to load ES Module". `templates/api/package.json.tmpl` sets it.
- **Next 16.4.5 stamps the nonce even when the proxy sets the CSP only on the response.** Measured on a production build: 9 of 9 scripts carried the response's nonce. CP §6.7 says the request header is required; setting both stays correct. What does break the nonce is a statically prerendered page, which is what the smoke test catches.
