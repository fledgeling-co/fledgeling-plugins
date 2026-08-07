---
name: slipway
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/*)
description: Scaffold a complete, working new project in ~/Dev from a project idea — the slipway is where new ships are launched. Use this whenever the user wants to start a new project, app, product, or prototype — "new project", "set up a project", "scaffold X", "spin up an app for…", "start building <idea>", "greenfield", "I have an idea for…" — even if they never say "scaffold". Interviews up front (modules, React Native/Expo vs native SwiftUI for mobile, macOS window-with-sidebar-and-search vs menu-bar style, codename with 3 generated options plus custom, bundle-id prefix), then one script renders the whole project from templates — pnpm/Turborepo monorepo, Next.js (latest) web app with security headers and AI SDK wiring, optional NestJS API (SWC dev/prod parity), native SwiftUI macOS and iOS apps via XcodeGen with Info.plists, representative bundle ids, build/sign/notarize/dmg scripts, optional Expo/React Native mobile app with monorepo Metro config, design-tokens package with drift gate, Mongoose/Redis data layer, Caddyfile + /etc/hosts instructions, docker-compose dev stack, Dockerfiles, husky pre-push gate, CLAUDE.md/AGENTS.md wired to the operating specs and the ARMADA manifest, git init, pnpm install, and the typecheck+build gate run. Script-first by design — the model makes decisions, the script makes files. NOT for adding an app to an existing project (edit it directly, following its conventions) and NOT for feature work after setup (use ship-feature).
---

# Slipway — launch a new project

Take a project idea to a **completely set-up, working project** in `~/Dev/<codename>`: gate-green, git-initialised, native projects generated, conventions wired. The trick is that `scripts/scaffold.sh` + `templates/` already contain everything common between projects (distilled from zephyr, perch, fledgeling-app, dAIolog and the team-files operating specs) — so your job is the **decisions**, and the script's job is the **files**. Do not hand-write files the templates cover; that is what makes setup cheap.

## 0 — Doctor

Run `<skill-dir>/scripts/doctor.sh` (read-only JSON) before the interview so recommendations match the machine: no macos/ios module without xcodegen, no 1Password seeding without `op`, no rust without cargo. Mention anything missing that the chosen modules would need.

## 1 — Understand the idea, generate codenames

From the user's idea, decide which modules fit and generate **three codename options**: single word, lowercase, evocative rather than descriptive — the portfolio precedent is zephyr, perch, anvil, loupe, tare, sift, margin. Check `ls ~/Dev` first and never propose a name that collides with an existing directory.

## 2 — Ask the clarifying questions up front (one round)

One `AskUserQuestion` call, all questions together, before anything is created:

- **Codename** — the 3 generated options (put your recommended one first, marked "(Recommended)"); the built-in Other lets them type their own. Show what each implies: `~/Dev/<codename>`, `<codename>.local`.
- **Modules** (multiSelect) — `web` Next.js app · `api` NestJS API · `macos` SwiftUI app · `ios` SwiftUI iOS app · `rn` React Native (Expo) mobile app · `tokens` design-tokens package · `data` Mongoose+Redis layer · `auth` sign-in + emails + dev login · `admin` allowlisted admin console · `push` APNs notifications · `waitlist` referral-loop pre-launch waitlist · `observability` Sentry wiring (inert until DSN) · `rust` cross-OS core crate. **Infer before asking**: a product with accounts implies auth (which implies data); "admin", "back office", "moderation" implies admin; a native/mobile app with alerts implies push; a SaaS gets web+tokens+data+auth by default; a marketing site gets web+tokens only; an unvalidated/pre-launch idea adds waitlist. Put the inferred set in the options as the recommended choice and let the user adjust — ask rather than guess only when the idea genuinely doesn't settle it. Implications are automatic in the script (push→auth→data→web; admin→data).
- **Mobile approach** (only when the idea implies a mobile app and the modules answer hasn't settled it) — native Swift/SwiftUI (`ios`, XcodeGen, simulator-first) vs React Native/Expo (`rn`, one codebase for iOS+Android, hoisted pnpm + monorepo Metro per BP §18). Recommend Swift when the app is Apple-only or needs deep platform integration; Expo when Android matters or the team iterates fastest in React.
- **macOS style** (only when macos selected) — **window** (Recommended): native NavigationSplitView shell with sidebar + top nav with search · **menubar**: MenuBarExtra agent app, no Dock icon (LSUIElement). Passed as `--macos-style window|menubar`.
- **Bundle-id prefix** (only when macos/ios/rn selected) — `app.<codename>` (Recommended) · `dev.<codename>` · `com.<codename>` · custom. Apps get `.mac` / `.ios` / `.mobile` suffixes — distinct identity per sibling app from day one (BP §18).
- **GitHub org** — where the repo will live: `fledgeling-co` (personal-product studio) · `lprhodes` (experiments/personal) · `Diolog26` / `DiologIR` (Diolog work) · none for now. Infer from the idea (a Diolog feature → Diolog org; a product → fledgeling-co; a quick experiment → lprhodes) and put the inferred org first. Passed as `--github-org`: the remote is set and the `gh repo create --push` command lands in next-steps — nothing is pushed without the user running it.
- **macOS distribution** (only when macos selected) — **direct** (Recommended): Developer ID + notarized DMG, no sandbox · **mas**: Mac App Store / TestFlight, App Sandbox on (a review requirement). Passed as `--macos-dist`; it selects the entitlements file, so it must be asked up front, not retrofitted.
- **Design reference** (only when a UI surface is selected) — a site or brand to bootstrap `DESIGN.md` from (via design-md-from-website, which measures real computed styles), or skip to design fresh later. Passed as `--design-ref`; recorded in the manifest and next-steps.
- **1Password** — which account/team id and vault this project's secrets live in. Run `op account list` and `op vault list --account <id>` first and present the real values as options (plus "skip"). The chosen pair is passed as `--op-account` / `--op-vault` and seeded into `apps/web/.env.local` (identifiers only — actual secret values are resolved later by `scripts/env-pull.sh` via the op CLI, straight into the file, never through your context).

AskUserQuestion takes at most 4 questions per call — batch them (codename + modules + mobile/macOS + org in the first round; distribution + design ref + 1Password in a second round only when those questions apply). Still front-load everything: both rounds happen before anything is created.

Anything else (ports, host, gate type, versions) has a good default in the script — don't ask about it.

## 3 — Run the scaffolder

```bash
<skill-dir>/scripts/scaffold.sh \
  --codename <codename> --display "<Display Name>" \
  --description "<one sentence>" \
  --modules web,tokens[,api,macos,ios,rn,data,auth,admin,push,rust] \
  [--macos-style window|menubar] [--macos-dist direct|mas] [--bundle-prefix app.<codename>] \
  [--github-org <org>] [--design-ref <url>] \
  [--op-account <1password-account>] [--op-vault <vault>]
```

The script does all of this itself: renders every file with substitution, assembles Caddyfile / docker-compose / CLAUDE.md / README from per-module fragments, allocates free ports by scanning the machine's Caddy configs, copies `CODING_PRACTICES.md` + `NEW_PROJECT_BEST_PRACTICES.md` from `~/Dev/bella-team-files` into `docs/`, symlinks `AGENTS.md → CLAUDE.md`, creates the feature-pipeline dirs (`docs/features-to-triage` + LEDGER, `docs/specs`, `docs/plans`, `design/mocks/html`), inits git with a first commit, runs `pnpm install`, runs the `typecheck + build` gate, and generates the `.xcodeproj`s with xcodegen. `--plan` emits the machine-readable plan (every file it would write, ports, modules) without writing — show it before the real run when the user seems unsure; `--dry-run` prints the human summary; it refuses to overwrite an existing directory; it never runs sudo. Shared external dep ranges live once in the workspace `catalog:` (pnpm-workspace.yaml) — bump a range there, not per app. Every scaffold records `.slipway/manifest.json` (the answers) and `.slipway/state.json` (SHA256 + ownership of every generated file).

## 4 — Verify and fix forward

The script's last line reports `install / gate / xcodegen` status. If the gate failed, fix it in the generated project and commit — the usual cause is a breaking change in a `latest` dependency (the templates deliberately float versions so the lockfile pins fresh ones, per BP §2). Make the minimal fix, don't restructure. If a template itself is wrong, also fix the template here so the next launch is clean.

Known deliberate pin: `typescript@^6` in web/api/rn — TypeScript 7.0 ships only the `tsc` executable, and the Nest CLI + typescript-eslint need the programmatic compiler API (expected back in TS 7.1). Unpin once the ecosystem supports 7.x.

## 5 — The launch pipeline (research → briefs → mocks → marketing site)

The scaffold is the shell; `references/launch-pipeline.md` is the full procedure for filling it — read it and run the phases:

- **R — deep research** (starts first, background): decide 0-2 Dossier queries (competitive almost always; technical only for real unknowns); free CLI panel by default, ask before paid backends join; when settled, **read every report in full** (not outlines) and export into `docs/deep-research/`. The research grounds the briefs, OVERVIEW.md, and every marketing decision.
- **B — feature backlog**: seed `docs/features-to-triage/` briefs from the owner's context immediately (BRIEF-TEMPLATE.md, index rows); revise + extend when research lands, citing reports.
- **O — overview + marketing features**: fill `OVERVIEW.md` and `docs/MARKETING-FEATURES.md` (incl. the pricing recommendation) from context + research.
- **D — design**: design-craft + ux-craft mock every surface, flow, menu, modal, and empty/loading/error state into `design/mocks/html/` (inventory first in INDEX.md); mac-design-studio for native app design + the app icon; media-gen-pro (`svg: true`) generates icon vectors into `design/icon/` and the scaffolded `design/icon/audit.html` (128/64/48/32/16 + tinted + silhouette) judges the directions.
- **M — marketing site**: `design/marketing/index.html` — create-luke-content writes every word (lint it), design-craft + ux-craft build the premium single page against the researched quality bar in the reference (zero Krebs slop tells; LCP ≤2.5s with three.js out of the critical path; native scroll; motion at one or two authored moments; an interactive mock slice from phase D; pricing per the evidence table; login/signup to `/login`), media-gen-pro supplies imagery into `design/marketing/assets/`; gate with design-review. Porting it into apps/web becomes a P0 brief.
- **L — launch ops**: fill `docs/LAUNCH.md` — domain availability (namecheap MCP, read-only), legal-page drafts, App Store kit (shot-list from mocks), analytics event schema, waitlist/referral decision. Prepares everything; the owner runs anything that spends, publishes, or creates accounts.

Commit per phase; armada-sync at the end. When the user only wants the scaffold, deliver the scaffold and offer the pipeline — don't run five phases nobody asked for.

## 6 — Finish

- Walk the user through `SETUP-NEXT-STEPS.md` — the only manual parts: the `/etc/hosts` + Caddy `conf.d` mirror commands (need sudo — suggest they run them with the `!` prefix), `vercel link`, `DEVELOPMENT_TEAM` for release signing, data-service env values.
- Register the project in the portfolio: run the `armada-sync` skill so `~/Dev/ARMADA.md` gets its entry.
- Point at the first-feature route: drop a brief in `docs/features-to-triage/` and run `ship-feature`, or route it via `ship-armada`.

Native pricing follows `references/apple-commercialization.md` (IAP vs direct vs external-purchase, region flux). Deliver the scaffolded, gate-green project at the scope intended — feature work, design systems beyond the token stubs, and deploy provisioning are follow-up pipeline work, not part of setup.

## What each module gives

| Module | Contents |
|---|---|
| base (always) | Root package.json/turbo/pnpm-workspace/tsconfig.base, consolidated `.gitignore`, `.claude/settings.json` (pre-allowed build/test commands so agents work promptless from day one), prettier, husky pre-push gate (`SKIP_GATE=1` bypass), Caddyfile, CLAUDE.md+AGENTS.md (with a Documentation map), README, SETUP-NEXT-STEPS.md, and **generated durable docs** assembled from the chosen modules: `docs/ARCHITECTURE.md` (surfaces + governance table, zephyr's shape), `docs/TESTING.md` (harness map, atlas's shape), `docs/DEPLOYMENT.md` (Vercel/fastlane/notarization knowledge incl. the BLOCKED-as-UNKNOWN gotcha), `docs/AI-MODEL-USAGE.md` (dAIolog's feature→model registry, when web/api present), plus CP/BP copied from team-files and the pipeline dirs |
| web | Next.js (latest) App Router: `/api/health` + syd1 `vercel.json` with warm cron (Performance CPU is a dashboard setting — in next-steps), security headers, `output: 'standalone'`, flat ESLint, `lib/ai.ts` (AI SDK + Gateway, models in one config), and the dAIolog common-feature baseline — react-hook-form + @hookform/resolvers, @vercel/analytics (mounted in layout), @vercel/blob, @ai-sdk/react, date-fns — `.env.example`, turbo-ignore, Dockerfile (turbo prune + standalone) |
| api | NestJS on SWC for **both** dev boot and prod build (BP §15 parity), and the dAIolog platform baseline — Vercel AI SDK (`src/ai.ts`, same convention as web), global ConfigModule, ThrottlerGuard rate limiting, ScheduleModule in-process cron, helmet, global ValidationPipe (whitelist+transform), OpenAPI at `/docs` — health controller, jest+@swc/jest, `.swcrc` with decorator metadata, Dockerfile; +mongoose/ioredis when data is also selected |
| macos | XcodeGen `project.yml` (source of truth, `.xcodeproj` gitignored), SPM `AppCore` + tests, distribution-aware entitlements (direct = no sandbox; mas = App Sandbox), two shells — **window** (NavigationSplitView sidebar + top nav with `.searchable`) or **menubar** (MenuBarExtra agent, LSUIElement) — `Signing/Info-App.plist` + entitlements, Manual Developer ID signing via env `DEVELOPMENT_TEAM`, scripts: build / sign / notarize / build-dmg |
| ios | XcodeGen `project.yml`, simulator-first (no signing), generated Info.plist keys, unit-test target, build script |
| rn | Expo/React Native app in `apps/mobile`: distinct bundle id (`.mobile`) + URL scheme, monorepo-aware `metro.config.js`, root `.npmrc` with `node-linker=hoisted` (BP §18), Maestro smoke flow in `.maestro/`; **Expo modules only, never EAS/Expo cloud** — release builds are local `expo prebuild` + fastlane |
| auth | BP §9 in full: email-code sign-in (Resend + React Email templates), 15-min HS256 access JWT + rotating hashed refresh tokens in Redis, rate limits, timingSafeEqual, no existence leak, `/login` page, **dev login** route+button (server-gated, non-prod only), User model, welcome email |
| admin | `apps/admin` console on its own subdomain/port: **separate trust domain** (ADMIN_JWT_SECRET, distinct audience — BP §9.5), ADMIN_EMAILS allowlist, email-code login, 12-h sessions, server-guarded shell, audit-log guidance |
| push | APNs over HTTP/2 with ES256 .p8 token auth and JWT caching (atlas-app pattern), device-token registration route, dead-token detection |
| waitlist | Referral-loop pre-launch waitlist: `/waitlist` page + join API, share codes, queue-jumping by referral count (`lib/waitlist.ts`) — the researched pre-launch mechanic, ready to embed in the marketing page |
| rust | Cargo workspace + `crates/core` cross-OS library (rlib/staticlib/cdylib) with tests — shared logic bound into Swift (UniFFI/swift-bridge) and Node (napi-rs), never duplicated per platform |

Cross-cutting, in every relevant module: **release path** (fastlane `beta` lanes for TestFlight/App Store via App Store Connect API key on ios+macos, plus the direct sign→notarize→dmg scripts); **testing** (Playwright e2e harness in web — the acceptance-e2e skill builds suites into it; jest+@swc/jest in api — plain `.js` config, never ts-jest or jest.config.ts; Maestro flows in rn; XCTest in macos/ios; cargo test in rust); **typecheck is `tsgo` everywhere** (`@typescript/native-preview`) — never `tsc`, never `ts-node`; `typescript@^6` stays installed only as the library the ecosystem's tooling APIs need; **secrets via 1Password** (`OP_ACCOUNT`/`OP_VAULT` in `.env.local`, `op://` references resolved by `scripts/env-pull.sh`, recommended in the generated CLAUDE.md § Secrets).
| tokens | `packages/design-tokens`: `src/tokens.mjs` single source → generated `tokens.css`, drift check wired into the gate |
| data | `lib/db.ts` (cached Mongoose), `lib/models.ts`, `lib/types.ts`, `lib/redis.ts` (fail-closed), mongo+redis compose services, env keys |

## Maintaining scaffolded projects

- `scripts/drift.sh <project>` — which generated files the user has modified vs left untouched (reads state.json). Run before any template-driven change to a project.
- `scripts/upgrade.sh <project> [--apply]` — bring an existing slipway project up to the current templates. Unmodified files are replaced; where the user edited a file AND the template moved, it 3-way merges against the templates the project was born from (`template_ref` in manifest.json, rendered via `git archive`) — clean merges applied, conflicts written as a `.slipway-new` sibling for human merge; user deletions respected; state.json and template_ref refreshed on apply. Projects without a template_ref (or a checkout missing that commit) fall back to 2-way, and the report's `base` field says which mode ran. Dry-run by default; after `--apply`, run the project's gate before committing.
- `scripts/canary.sh [--quick]` — scaffold four representative module permutations (all / saas / native / site) and gate each; the weekly anti-rot check (ship-armada daemon is a good home).

## Improving the templates

When a scaffolded project needed a manual fix, or a convention changes in the team-files specs, update `templates/` (and `scripts/scaffold.sh` if behaviour changed) in the same sitting and bump the plugin version — template rot is the classic failure of scaffolding tools, and the fix is treating every launch as a test of the templates. `scripts/canary.sh` makes that a command: it scaffolds every module into a temp dir and runs the gate — run it weekly (the ship-armada daemon is a good home). Every generated project carries `.slipway/manifest.json` (slipway version + every answer) so a future upgrade/diff story is possible. Before structural changes to this skill, read `references/research-notes.md` — the distilled 5-backend research on what makes scaffolders succeed and the prioritized roadmap (state inventory → plan artifact → upgrade lifecycle → pnpm catalogs → ownership markers).
