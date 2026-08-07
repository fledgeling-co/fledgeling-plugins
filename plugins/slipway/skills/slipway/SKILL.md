---
name: slipway
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/*)
description: Scaffold a complete, working new project in ~/Dev from a project idea — the slipway is where new ships are launched. Use this whenever the user wants to start a new project, app, product, or prototype — "new project", "set up a project", "scaffold X", "spin up an app for…", "start building <idea>", "greenfield", "I have an idea for…" — even if they never say "scaffold". Interviews up front (modules, React Native/Expo vs native SwiftUI for mobile, macOS window-with-sidebar-and-search vs menu-bar style, codename with 3 generated options plus custom, bundle-id prefix), then one script renders the whole project from templates — pnpm/Turborepo monorepo, Next.js (latest) web app with security headers and AI SDK wiring, optional NestJS API (SWC dev/prod parity), native SwiftUI macOS and iOS apps via XcodeGen with Info.plists, representative bundle ids, build/sign/notarize/dmg scripts, optional Expo/React Native mobile app with monorepo Metro config, design-tokens package with drift gate, Mongoose/Redis data layer, Caddyfile + /etc/hosts instructions, docker-compose dev stack, Dockerfiles, husky pre-push gate, CLAUDE.md/AGENTS.md wired to the operating specs and the ARMADA manifest, git init, pnpm install, and the typecheck+build gate run. Script-first by design — the model makes decisions, the script makes files. NOT for adding an app to an existing project (edit it directly, following its conventions) and NOT for feature work after setup (use ship-feature).
---

# Slipway — launch a new project

Take a project idea to a **completely set-up, working project** in `~/Dev/<codename>`: gate-green, git-initialised, native projects generated, conventions wired. The trick is that `scripts/scaffold.sh` + `templates/` already contain everything common between projects (distilled from zephyr, perch, fledgeling-app, dAIolog and the team-files operating specs) — so your job is the **decisions**, and the script's job is the **files**. Do not hand-write files the templates cover; that is what makes setup cheap.

## 1 — Understand the idea, generate codenames

From the user's idea, decide which modules fit and generate **three codename options**: single word, lowercase, evocative rather than descriptive — the portfolio precedent is zephyr, perch, anvil, loupe, tare, sift, margin. Check `ls ~/Dev` first and never propose a name that collides with an existing directory.

## 2 — Ask the clarifying questions up front (one round)

One `AskUserQuestion` call, all questions together, before anything is created:

- **Codename** — the 3 generated options (put your recommended one first, marked "(Recommended)"); the built-in Other lets them type their own. Show what each implies: `~/Dev/<codename>`, `<codename>.local`.
- **Modules** (multiSelect) — `web` Next.js app · `api` NestJS API · `macos` SwiftUI app · `ios` SwiftUI iOS app · `rn` React Native (Expo) mobile app · `tokens` design-tokens package · `data` Mongoose+Redis layer · `auth` sign-in + emails + dev login · `admin` allowlisted admin console · `push` APNs notifications · `rust` cross-OS core crate. **Infer before asking**: a product with accounts implies auth (which implies data); "admin", "back office", "moderation" implies admin; a native/mobile app with alerts implies push; a SaaS gets web+tokens+data+auth by default; a marketing site gets web+tokens only. Put the inferred set in the options as the recommended choice and let the user adjust — ask rather than guess only when the idea genuinely doesn't settle it. Implications are automatic in the script (push→auth→data→web; admin→data).
- **Mobile approach** (only when the idea implies a mobile app and the modules answer hasn't settled it) — native Swift/SwiftUI (`ios`, XcodeGen, simulator-first) vs React Native/Expo (`rn`, one codebase for iOS+Android, hoisted pnpm + monorepo Metro per BP §18). Recommend Swift when the app is Apple-only or needs deep platform integration; Expo when Android matters or the team iterates fastest in React.
- **macOS style** (only when macos selected) — **window** (Recommended): native NavigationSplitView shell with sidebar + top nav with search · **menubar**: MenuBarExtra agent app, no Dock icon (LSUIElement). Passed as `--macos-style window|menubar`.
- **Bundle-id prefix** (only when macos/ios/rn selected) — `app.<codename>` (Recommended) · `dev.<codename>` · `com.<codename>` · custom. Apps get `.mac` / `.ios` / `.mobile` suffixes — distinct identity per sibling app from day one (BP §18).
- **1Password** — which account/team id and vault this project's secrets live in. Run `op account list` and `op vault list --account <id>` first and present the real values as options (plus "skip"). The chosen pair is passed as `--op-account` / `--op-vault` and seeded into `apps/web/.env.local` (identifiers only — actual secret values are resolved later by `scripts/env-pull.sh` via the op CLI, straight into the file, never through your context).

Anything else (ports, host, gate type, versions) has a good default in the script — don't ask about it.

## 3 — Run the scaffolder

```bash
<skill-dir>/scripts/scaffold.sh \
  --codename <codename> --display "<Display Name>" \
  --description "<one sentence>" \
  --modules web,tokens[,api,macos,ios,rn,data,auth,admin,push,rust] \
  [--macos-style window|menubar] [--bundle-prefix app.<codename>] \
  [--op-account <1password-account>] [--op-vault <vault>]
```

The script does all of this itself: renders every file with substitution, assembles Caddyfile / docker-compose / CLAUDE.md / README from per-module fragments, allocates free ports by scanning the machine's Caddy configs, copies `CODING_PRACTICES.md` + `NEW_PROJECT_BEST_PRACTICES.md` from `~/Dev/bella-team-files` into `docs/`, symlinks `AGENTS.md → CLAUDE.md`, creates the feature-pipeline dirs (`docs/features-to-triage` + LEDGER, `docs/specs`, `docs/plans`, `design/mocks/html`), inits git with a first commit, runs `pnpm install`, runs the `typecheck + build` gate, and generates the `.xcodeproj`s with xcodegen. `--dry-run` prints the plan without writing; it refuses to overwrite an existing directory; it never runs sudo.

## 4 — Verify and fix forward

The script's last line reports `install / gate / xcodegen` status. If the gate failed, fix it in the generated project and commit — the usual cause is a breaking change in a `latest` dependency (the templates deliberately float versions so the lockfile pins fresh ones, per BP §2). Make the minimal fix, don't restructure. If a template itself is wrong, also fix the template here so the next launch is clean.

Known deliberate pin: `typescript@^6` in web/api/rn — TypeScript 7.0 ships only the `tsc` executable, and the Nest CLI + typescript-eslint need the programmatic compiler API (expected back in TS 7.1). Unpin once the ecosystem supports 7.x.

## 5 — Finish

- Walk the user through `SETUP-NEXT-STEPS.md` — the only manual parts: the `/etc/hosts` + Caddy `conf.d` mirror commands (need sudo — suggest they run them with the `!` prefix), `vercel link`, `DEVELOPMENT_TEAM` for release signing, data-service env values.
- Register the project in the portfolio: run the `armada-sync` skill so `~/Dev/ARMADA.md` gets its entry.
- Point at the first-feature route: drop a brief in `docs/features-to-triage/` and run `ship-feature`, or route it via `ship-armada`.

Deliver the scaffolded, gate-green project at the scope intended — feature work, design systems beyond the token stubs, and deploy provisioning are follow-up pipeline work, not part of setup.

## What each module gives

| Module | Contents |
|---|---|
| base (always) | Root package.json/turbo/pnpm-workspace/tsconfig.base, consolidated `.gitignore`, prettier, husky pre-push gate (`SKIP_GATE=1` bypass), Caddyfile, CLAUDE.md+AGENTS.md, README, docs/ + pipeline dirs, SETUP-NEXT-STEPS.md |
| web | Next.js (latest) App Router: `/api/health` + syd1 `vercel.json` with warm cron (Performance CPU is a dashboard setting — in next-steps), security headers, `output: 'standalone'`, flat ESLint, `lib/ai.ts` (AI SDK + Gateway pattern, models in one config), `.env.example`, `vercel.json` turbo-ignore, Dockerfile (turbo prune + standalone) |
| api | NestJS on SWC for **both** dev boot and prod build (BP §15 parity), health controller, `.swcrc` with decorator metadata, Dockerfile |
| macos | XcodeGen `project.yml` (source of truth, `.xcodeproj` gitignored), SPM `AppCore` + tests, two shells — **window** (NavigationSplitView sidebar + top nav with `.searchable`) or **menubar** (MenuBarExtra agent, LSUIElement) — `Signing/Info-App.plist` + entitlements, Manual Developer ID signing via env `DEVELOPMENT_TEAM`, scripts: build / sign / notarize / build-dmg |
| ios | XcodeGen `project.yml`, simulator-first (no signing), generated Info.plist keys, unit-test target, build script |
| rn | Expo/React Native app in `apps/mobile`: distinct bundle id (`.mobile`) + URL scheme, monorepo-aware `metro.config.js`, root `.npmrc` with `node-linker=hoisted` (BP §18), Maestro smoke flow in `.maestro/`; **Expo modules only, never EAS/Expo cloud** — release builds are local `expo prebuild` + fastlane |
| auth | BP §9 in full: email-code sign-in (Resend + React Email templates), 15-min HS256 access JWT + rotating hashed refresh tokens in Redis, rate limits, timingSafeEqual, no existence leak, `/login` page, **dev login** route+button (server-gated, non-prod only), User model, welcome email |
| admin | `apps/admin` console on its own subdomain/port: **separate trust domain** (ADMIN_JWT_SECRET, distinct audience — BP §9.5), ADMIN_EMAILS allowlist, email-code login, 12-h sessions, server-guarded shell, audit-log guidance |
| push | APNs over HTTP/2 with ES256 .p8 token auth and JWT caching (atlas-app pattern), device-token registration route, dead-token detection |
| rust | Cargo workspace + `crates/core` cross-OS library (rlib/staticlib/cdylib) with tests — shared logic bound into Swift (UniFFI/swift-bridge) and Node (napi-rs), never duplicated per platform |

Cross-cutting, in every relevant module: **release path** (fastlane `beta` lanes for TestFlight/App Store via App Store Connect API key on ios+macos, plus the direct sign→notarize→dmg scripts); **testing** (Playwright e2e harness in web — the acceptance-e2e skill builds suites into it; jest+@swc/jest in api — plain `.js` config, never ts-jest or jest.config.ts; Maestro flows in rn; XCTest in macos/ios; cargo test in rust); **typecheck is `tsgo` everywhere** (`@typescript/native-preview`) — never `tsc`, never `ts-node`; `typescript@^6` stays installed only as the library the ecosystem's tooling APIs need; **secrets via 1Password** (`OP_ACCOUNT`/`OP_VAULT` in `.env.local`, `op://` references resolved by `scripts/env-pull.sh`, recommended in the generated CLAUDE.md § Secrets).
| tokens | `packages/design-tokens`: `src/tokens.mjs` single source → generated `tokens.css`, drift check wired into the gate |
| data | `lib/db.ts` (cached Mongoose), `lib/models.ts`, `lib/types.ts`, `lib/redis.ts` (fail-closed), mongo+redis compose services, env keys |

## Improving the templates

When a scaffolded project needed a manual fix, or a convention changes in the team-files specs, update `templates/` (and `scripts/scaffold.sh` if behaviour changed) in the same sitting and bump the plugin version — template rot is the classic failure of scaffolding tools, and the fix is treating every launch as a test of the templates. `scripts/canary.sh` makes that a command: it scaffolds every module into a temp dir and runs the gate — run it weekly (the ship-armada daemon is a good home). Every generated project carries `.slipway/manifest.json` (slipway version + every answer) so a future upgrade/diff story is possible. Before structural changes to this skill, read `references/research-notes.md` — the distilled 5-backend research on what makes scaffolders succeed and the prioritized roadmap (state inventory → plan artifact → upgrade lifecycle → pnpm catalogs → ownership markers).
