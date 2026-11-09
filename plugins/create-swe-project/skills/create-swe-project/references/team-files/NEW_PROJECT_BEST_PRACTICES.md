# NEW_PROJECT_BEST_PRACTICES.md

**Audience: AI coding assistants (Claude Code and similar agents) scaffolding or extending a Next.js + Vercel + MongoDB SaaS** that ships AI features and webhook integrations. This is a decision-and-default playbook: when a task is underspecified, adopt the default here instead of inventing one; when you deliberately diverge, say so and why. The defaults are battle-tested in production.

## How to use this document (agent protocol)

1. **Defaults are the starting point, not a menu.** Apply each section's default unless the task explicitly contradicts it or the section plainly doesn't apply (no AI features, no admin UI). When you skip a section, state which and why — never silently omit setup that a later step assumes exists.
2. **"From day one" means now, not later.** Items flagged "from day one" / "before the first feature" are far cheaper now than retrofitted. §15 (test harness), §17 (monorepo shape), §18 (RN/Expo), §19 (CI gate) are the biggest sources of avoidable rework — settle them *before* scaffolding.
3. **Decisions that branch the build, ask once.** Repo shape (single app vs monorepo, §17) and quality gate (hosted CI vs pre-push hook, §19) change everything downstream. If the task doesn't state them and you can't safely infer them, ask the user before scaffolding rather than guessing and rebuilding.
4. **Pair with the rule docs.** `CODING_PRACTICES.md` governs the code you write inside this scaffold (reviews block on it) and carries the review checklist (CP §7); `DESIGN.md` governs the pixels. Apply all three together. Where this document and `CODING_PRACTICES.md` disagree, `CODING_PRACTICES.md` wins.
5. **Verify, don't fabricate.** Install current releases the way §2 describes (newest release past the cooldown, minus the pinned exceptions) and let the lockfile pin, instead of pasting version numbers from memory. Every command, env var, and file path you emit must be real for this stack — when unsure, say so.

> **Three adjacent files are part of every project:**
> - **`docs/CODING_PRACTICES.md`** — TypeScript boundary safety, App Router rules, and an OWASP-aligned security checklist. Reviews block on it. This document (`NEW_PROJECT_BEST_PRACTICES.md`) lives beside it in `docs/`.
> - **`DESIGN.md`** — single source of truth for tokens, typography, components, voice. Generated from screenshots of a reference site with the `design-md-from-screenshots:design-md-from-screenshots` skill. Bootstrap it on day one.
> - **`CLAUDE.md`** — do NOT hand-author it. Copy **`CLAUDE-STARTER.md`** from the team-files repo to the project root as `CLAUDE.md`, fill every placeholder with *verified* project reality (real commands, real paths — never guesses), delete its instruction block, and create `AGENTS.md` as a symlink so non-Claude agents read the same text: `ln -s CLAUDE.md AGENTS.md`. The starter already wires in the CP/BP citation convention, the quality-gate done criterion with CP §7 as the review checklist, and the behaviour-under-ambiguity block.
>
> **Building a monorepo, an Expo/React-Native client, or picking your CI gate?** Read §17 (monorepo + pnpm/Turborepo), §18 (RN/Expo client), and §19 (quality gate / CI strategy) **before** scaffolding — these are the biggest sources of avoidable rework in a multi-app project and are easiest to get right on day one.
>
> **Standing up the local dev environment (proxy, Docker, design system)?** §20 (one shared Caddy fronting every repo), §21 (the Dockerized dev stack and its `node_modules` / file-watch / install gotchas), §22 (token single-source + the two-Storybook design system + mock-UI host scheme), and §23 (build + worktree hygiene for parallel agents) capture the hard-won setup that otherwise re-bites every contributor.
>
> **Shipping to multiple environments, or changing a security control?** §24 (the server is the single authority for env- and tenant-gated behaviour — flags, internal-user gating, the BFF boundary) and §25 (verify the whole request path after any auth/validation change; instrument boundaries before chasing error strings) are the operational rules that keep staging from emailing real customers and a security tweak from silently 403-ing a live feature.

---

## 1. Stack defaults

| Layer | Pick | Notes |
|---|---|---|
| Framework | **Next.js 16 App Router** | Server Components by default, `"use client"` only when needed |
| Language | **TypeScript 6.0**, strict (hold at 6) | `"strict": true`, `noUncheckedIndexedAccess: true`. `typescript@latest` is now 7.0, which ships no compiler API; typescript-eslint and `@nestjs/cli` need one (§2). Optionally run 7.0's native compiler beside it for a faster typecheck (§23) |
| Runtime | **Node.js 24** (Vercel's default) | Node 26 becomes Active LTS on 28 Oct 2026. Floor 22.12: AI SDK 7 and Vitest 5 need it. Never lock yourself to the Edge runtime unless you've measured the cold-start win |
| Hosting | **Vercel** | Link the project on day one (`vercel link`); env vars live there, not in CI |
| Package mgr | **npm** (single app) · **pnpm** (monorepo) | One lockfile, and the release-age cooldown configured for either (§2). For a monorepo, pnpm workspaces + Turborepo — see §17. Both work on Vercel |
| DB | **MongoDB Atlas + Mongoose** | Section 4 |
| Cache | **Redis (optional)** via `redis` (node-redis) | Section 5 — only if you actually need shared state |
| AI | **Vercel AI SDK** + **AI Gateway** | Section 6. Use **AI Elements** for chat UI |
| Storage | **Vercel Blob** | Client-upload pattern (Section 7) |
| Email | **Resend** | Section 8 |
| Auth | **JWT in httpOnly cookie + email-code sign-in** | Section 9 |
| Bot/messaging (opt) | **Vercel Chat SDK** (`chat`) + `@chat-adapter/*` | Slack / Teams / Google Chat / Discord / Telegram / WhatsApp behind one interface |
| Lint | **ESLint 9 flat config** (hold at 9) | `next lint` was removed in Next 16; use `eslint-config-next` directly (a Next lint gate WITHOUT it is hollow — see CODING_PRACTICES §6.9). Three plugins it bundles (`eslint-plugin-react`, `eslint-plugin-jsx-a11y`, `eslint-plugin-import`) still declare peer ranges that stop at ESLint 9, so `eslint@latest` (10.x) fails npm's peer check |
| Local dev proxy | **One shared Caddy** on `:80` + `<project>.localhost` | A single machine-wide proxy fronts every repo; real origins, no port collisions — see §20 |
| Local dev stack | **Docker Compose** (one service/app) behind Caddy | Source bind-mounts only; isolated `node_modules` volumes; event-based file-watch, polling only where §21 says — see §21 |
| Design system | **Two Storybooks (HTML ref ⇄ React host) + token single-source** | 1:1 parity; every token generated from one file — see §22 |
| Repo shape | **single app** → standalone · **multi-deployable** → monorepo | pnpm workspaces + Turborepo from day one — see §17 |
| Native client (opt) | **Expo / React Native** | SDK 58 / RN 0.88, New Architecture only. In-monorepo conventions + a pure-`lib/` test gate — see §18 |

Versions in this document were checked against the npm registry on 2026-10-18. Re-check a major (`npm view <pkg> dist-tags`) before relying on it.

`tsconfig.json`: keep the path alias `"@/*": ["./*"]` and import everything cross-tree as `@/lib/foo`. Reduces churn on file moves. Leave `baseUrl` out: TypeScript 7 rejects it, and `paths` resolve from the tsconfig's own directory without it.

---

## 2. Install current versions, after a cooldown

When adding any dependency, install its newest release that has been public for at least a day, and let the lockfile pin the version. Don't paste version numbers from old project READMEs — they age out within months.

**Keep the release-age cooldown on.** It keeps a freshly compromised release out of your lockfile until the registry has had time to pull it; the 2025 npm worms (Shai-Hulud and its successors) spread through freshly published versions.
- **pnpm 11+** defaults `minimumReleaseAge` to 1440 minutes and fails the install on unapproved build scripts (§17). Keep both.
- **npm 11.10+** applies no cooldown by default: add `min-release-age=1` (days) to the project `.npmrc`. If you also set `ignore-scripts=true`, npm skips every lifecycle script, including the root `prepare` that installs the husky gate (§19): run `npm rebuild <pkg> --ignore-scripts=false` for each reviewed package that needs a native build, and `npm run prepare` once after install.

```bash
npm install next@latest react@latest react-dom@latest
npm install --save-dev typescript@~6.0 eslint@^9 @types/node@24 @types/react@latest   # pinned exceptions below; @types/node tracks your Node major
npm install ai@latest @ai-sdk/anthropic@latest        # AI SDK 7: ESM-only, Node 22+
npm install mongoose@latest redis@latest               # data layer
npm install @vercel/blob@latest                        # storage
npm install resend@latest                              # email
npm install zod@latest jose@latest server-only@latest  # validation/JWT/boundary
```

**Pinned exceptions (checked 2026-10-18).** `@latest` currently breaks two tools in this stack, so hold these until the blocker closes:

| Package | Hold at | Why | Lift when |
|---|---|---|---|
| `typescript` | `~6.0` | TypeScript 7.0 ships no compiler API; typescript-eslint (peer range `<6.1.0`) and `@nestjs/cli` need one. `next build` accepts 6 or 7. Optionally run 7.0 beside 6.0 for a faster typecheck (§23). | typescript-eslint (typescript-eslint#10940, targeted at TypeScript 7.1) and, in a NestJS repo, `@nestjs/cli` (nest-cli#3479) both support 7 |
| `eslint` | `^9` | Three plugins `eslint-config-next` 16.4 bundles (`eslint-plugin-react`, `eslint-plugin-jsx-a11y`, `eslint-plugin-import`) declare peer ranges that stop at ESLint 9; vercel/next.js#91702 was closed as a duplicate, not fixed. | those three plugins' peer ranges include ESLint 10 |

For majors, run codemods first when available: `npx @next/codemod@latest upgrade latest`, `npx @ai-sdk/codemod v7`. If peer-dep noise blocks an install, `npm install --save-dev @types/react@latest --legacy-peer-deps` as a one-off — never bake `--legacy-peer-deps` into install scripts (CODING_PRACTICES §4, A03). Read each major's release notes — App Router, AI SDK, and Mongoose all ship breaking changes regularly.

Keep `package.json` clean: don't pin to `~` or `^` arbitrarily — let `npm install` write `^` and trust the lockfile for reproducibility. The pinned exceptions above are the deliberate ones.

---

## 3. Project layout

```
app/
  page.tsx                 landing
  (marketing)/             grouped routes that share a marketing layout
  (app)/                   authenticated app shell
  [slug]/                  public pages
  api/
    <resource>/route.ts    Route Handlers — Promise<NextResponse>, Zod-validated
    webhooks/<provider>/   HMAC-verify-then-process
components/                shared client/server components
lib/
  db.ts, models.ts         data access + schemas (server-only)
  redis.ts                 cache + rate-limit helpers (server-only)
  storage.ts               Vercel Blob wrapper (server-only)
  ai.ts                    AI SDK wrapper (server-only)
  email.ts                 Resend wrapper (server-only)
  auth-server.ts           JWT mint/verify, cookie helpers (server-only)
  auth.ts                  thin client wrapper around /api/auth/me
  handlers/                long-form domain logic shared across entry points
scripts/                   tsx scripts: seed, invite, migrate
public/                    static assets, brand
```

**Server-only boundary:** every file in `lib/` that reads env secrets, hits the DB, or owns server-side handlers must `import 'server-only'` at the top. The package errors at build time if a Client Component imports it — your single best safeguard against accidental secret leaks.

`lib/auth.ts` is the only `lib/` file that's `"use client"`. Don't add `server-only` to it.

---

## 4. Database — MongoDB + Mongoose

- **Single connection cache**: in `lib/mongodb.ts`, cache the Mongoose connection on `globalThis` to survive Next.js dev hot reloads and serverless function reuse.
- **Models in one file**: `lib/models.ts`. Define schemas, indexes, and discriminators here; export typed model accessors from `lib/db.ts` so call sites never touch raw Mongoose.
- **Types in another**: `lib/types.ts` is the single source of truth for entity shapes — define the TS types there, derive Zod schemas from them at boundaries, mirror them in Mongoose schemas. Keep all three in sync in one edit.
- **Indexes are code**: declare every index in the schema file. Don't rely on the Atlas UI; it diverges from prod silently.
- **Lean reads**: use `.lean()` for read-only queries — returns POJOs, no Mongoose doc overhead.
- **Strict queries that fail loudly**: `mongoose.set('strictQuery', 'throw')`. With `true`, Mongoose silently drops filter keys that aren't in the schema, so a misspelt `{ tenatId: x }` becomes `{}` and the query matches every tenant's documents; `'throw'` raises an error instead.
- **Migrations**: write one-shot scripts under `scripts/` invoked via `tsx --conditions=react-server scripts/migrate-*.ts` so they can import `server-only` modules.

Alternatives if MongoDB is wrong for the shape of your data: **Postgres via Neon** (Vercel Marketplace one-click) with **Drizzle** or **Prisma**. Neon's branching makes preview-deploy DBs trivial.

---

## 5. Cache — Redis (optional)

Only add Redis when you have a *concrete* need for cross-request shared state:
- **Rate limits** (per-IP, per-email)
- **Email codes / one-time tokens** with TTL
- **Webhook idempotency keys**
- **Chat SDK thread state**

If you only need request-scoped memoisation, use React's `cache()` instead — no infra. If you only need page-level caching, use Next 16 Cache Components (`"use cache"` + `cacheLife`/`cacheTag`), knowing it rules out the nonce CSP in §12 (CP §6.7).

When you do reach for Redis:
- **`redis`** (node-redis) for raw access: ioredis's own README now recommends node-redis for new projects, so keep ioredis only where a library you depend on requires it. **`@upstash/redis`** if you want HTTP-only (works on the Edge runtime).
- Wrap in `lib/redis.ts` with `import 'server-only'`. Expose a small `getKV()` helper plus typed helpers (`incr`, `expire`, `setEx`).
- **Provision on Vercel Marketplace** (Upstash Redis or Redis Cloud) — env var auto-injected, region picked for you.
- **Fail closed on every deployed environment, previews included**: if `REDIS_URL` is missing, throw at boot. The in-memory fallback is for local dev and tests only (CP §6.8).

---

## 6. AI — Vercel AI SDK + AI Gateway + AI Elements

**Default to the AI SDK (`ai` package) over raw provider SDKs.** It puts streaming, tool calling, structured output and provider switching behind one API, so a model or provider swap doesn't touch call sites.

```ts
// lib/ai.ts
import 'server-only';
import { generateText, streamText, Output } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

// Pass model as "provider/model" string so AI Gateway routes it transparently
// when AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN is set. Falls back to the
// direct provider for local dev with just ANTHROPIC_API_KEY. Gateway IDs use
// dots in the version ("claude-haiku-5.5"); the direct Anthropic API uses
// dashes ("claude-haiku-5-5") — normalise or the fallback 404s.
function resolveModel(id: string) {
  if (process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN) return id;
  return anthropic(id.replace(/^anthropic\//, '').replace(/\./g, '-'));
}

const MODELS = { summariser: 'anthropic/claude-sonnet-5.5' } as const; // one place for model IDs
const summarySchema = z.object({ tldr: z.string(), bullets: z.array(z.string()) });
type Summary = z.infer<typeof summarySchema>;

export async function summarise(input: string): Promise<Summary> {
  const { output } = await generateText({
    model: resolveModel(MODELS.summariser),
    prompt: input,
    output: Output.object({ schema: summarySchema }),
  });
  return output; // schema-validated object
}
```

- **AI Gateway** is the default routing layer. Configure once via `AI_GATEWAY_API_KEY` (or Vercel OIDC in prod) and you get multi-provider failover, cost tracking, and rate-limit insulation without touching call sites.
- **Structured output is non-negotiable for data**: enforce every LLM payload your code consumes as data (as opposed to chat prose streamed to a person) by passing `output: Output.object({ schema })` (a Zod schema) to `generateText`/`streamText` and reading the validated `output` from the result. No regex-based JSON salvage. (Older releases spelled it `experimental_output`; AI SDK 7 removed that alias, and `npx @ai-sdk/codemod v7` rewrites it.)
- **AI SDK 7 renames and requirements.** v7 (June 2026) is ESM-only and needs Node 22+; a CommonJS NestJS app loads it through `require(esm)`. On `generateText`, `streamText` and the agent classes it renamed `system` → `instructions`, `onFinish` → `onEnd` and `onStepFinish` → `onStepEnd` (the old names remain as deprecated aliases), deprecated `StreamTextResult.fullStream` in favour of `stream`, and moved final-step data to `result.finalStep`. The React hooks such as `useObject` keep `onFinish`, and transcription results keep `fullStream`. Run `npx @ai-sdk/codemod v7` when upgrading.
- **Streaming**: with `output` set, `streamText` exposes `textStream` (typewriter effect) and `partialOutputStream` (the schema-shaped object as it forms, for server-side consumers). For a browser client, return `result.toTextStreamResponse()` and read it with the `useObject` hook, which parses the streamed JSON text itself. Streaming errors arrive *in the stream*, not as thrown exceptions — handle them via the `onError` callback.
- **Models**: keep model IDs in *one* config object (`MODELS.captioner`, `MODELS.extractor`) so swaps are one-line. Default to **Claude Sonnet 5.5** (`anthropic/claude-sonnet-5.5`) for quality work and **Claude Haiku 5.5** (`anthropic/claude-haiku-5.5`) for high-volume / latency-sensitive paths; reach for **Claude Opus 5.5** (`anthropic/claude-opus-5.5`) when a single hard task justifies the cost. **Claude Fable 5.1** (`anthropic/claude-fable-5.1`) is the model Anthropic positions as its most capable widely released one, at 2.5× Opus 5.5's input and output token price; keep it for the hardest long-horizon work. (IDs and prices checked 2026-10-18.) Model IDs age out in months — verify against the live list (`curl -s https://ai-gateway.vercel.sh/v1/models`) instead of pasting from memory, per §2.
- **Tool calls need a stop condition.** When you give the model tools, set the loop/stop control (`stopWhen: isStepCount(n)`; AI SDK 7 renamed `stepCountIs`, which remains as an alias). `generateText` and `streamText` default to one step, so without it the run halts the instant a tool executes and never generates the final text: you get a tool result and an *empty answer*. This is the single most common "the model returned nothing" bug with tools. (`ToolLoopAgent` defaults to 20 steps.)
- **Forced tool choice no longer applies on the newest Claude models.** Claude Opus 5.5, Sonnet 5.5 and Fable 5.1 reject forced tool use, so `@ai-sdk/anthropic` downgrades `toolChoice: 'required'` or a named tool to `auto` with only a warning. Steer tool use from the prompt, and use `output: Output.object(...)` when you need guaranteed JSON; the provider uses native structured outputs for these models.
- **Pin provider routing so a fallback can't silently bill you.** When the Gateway routes by a preference list, pass it as both the allow-filter and the order (`only` + `order`) so a request can't quietly fall through to a provider you didn't mean to pay for. And some providers reject parts of a JSON schema others accept: Bedrock's structured outputs accept `type: 'integer'` but reject `minimum`/`maximum`/`multipleOf` and `minLength`/`maxLength`, which Zod emits for `.int()` (safe-integer bounds) and for `.max(n)` on a string. Strip those keywords from the *wire* schema and re-validate the result against your original Zod, rather than dropping the constraint everywhere.
- **Missing AI credentials**: in local dev and previews, return a sentinel object with a friendly "missing key" message rather than crashing the host page. In production, validate the AI env vars at boot and fail the deploy (CP §6.8), because a sentinel there is the masking fallback §26 rules out.

### AI Elements — when building chat or agent UIs

**Use [Vercel AI Elements](https://elements.ai-sdk.dev)** (the prebuilt React component library) instead of building chat bubbles, message lists, tool-call cards, code blocks, and reasoning panels from scratch. They're styled with shadcn/ui and integrate directly with the AI SDK's hooks.

```bash
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/all.json   # or pick components; needs `npx shadcn@latest init` first
```

AI Elements is moving into shadcn/ui: the standalone `ai-elements` CLI is deprecated at the end of November 2026, so install through the shadcn CLI as above and follow https://ui.shadcn.com/docs/ai-elements once that version ships.

When **not** to use AI Elements:
- One-off "summarise this" / "generate a caption" features with no chat surface — plain components are simpler.
- Marketing copy generation that renders inside an existing form — use the form, not a chat shell.

If the product *is* a chat interface, AI Elements supplies the chat UI plumbing (message list, prompt input, streaming and tool-call rendering) with a coherent design language out of the box.

---

## 7. File uploads — Vercel Blob client-upload

**Never POST file bytes through a Route Handler.** Vercel's Function body cap is 4.5 MB and you'll lose to it the first time a user uploads a phone photo.

Use the **client-upload pattern**:

```ts
// app/api/uploads/photo-token/route.ts (server)
import { BlobError } from '@vercel/blob';
import { handleUpload } from '@vercel/blob/client';
import { getSession } from '@/lib/auth-server';
import { isAllowedOrigin, rateLimitUser } from '@/lib/guards'; // the shared browser-mutation guards (CP §6.1, §6.11)
import { logger } from '@/lib/logger';

class UploadDenied extends Error {
  readonly status: 401 | 403 | 429;
  constructor(status: 401 | 403 | 429) { super('Upload not allowed'); this.status = status; }
}

export async function POST(req: Request): Promise<Response> {
  try {
    const result = await handleUpload({
      request: req,
      body: await req.json(), // handleUpload checks its type and verifies the completion callback's signature
      // This hook runs only for the browser's token request. Vercel's completion callback carries
      // no session and no Origin, so the browser guards live here, per token, not at the top.
      onBeforeGenerateToken: async (pathname) => {
        if (!isAllowedOrigin(req)) throw new UploadDenied(403);
        const session = await getSession();
        if (!session) throw new UploadDenied(401);                       // no token for anonymous callers (CP §3)
        if (!(await rateLimitUser(session.userId, 'upload-token'))) throw new UploadDenied(429);
        if (!pathname.startsWith(`users/${session.userId}/`)) throw new UploadDenied(403); // the browser picks the pathname
        return {
          allowedContentTypes: ['image/jpeg', 'image/png', 'image/webp', 'image/heic'],
          maximumSizeInBytes: 10 * 1024 * 1024,
          addRandomSuffix: true, // defaults to false, so two uploads of photo.jpg would collide
          tokenPayload: JSON.stringify({ userId: session.userId }), // scope the upload to its owner
        };
      },
      onUploadCompleted: async ({ blob, tokenPayload }) => { /* persist blob.url against the owner in tokenPayload */ },
    });
    return Response.json(result);   // handleUpload returns a plain object, not a Response
  } catch (err) {
    if (err instanceof UploadDenied) return Response.json({ error: err.message }, { status: err.status });
    // Malformed JSON, an unknown event type or a bad callback signature: the request's fault.
    // (BLOB_READ_WRITE_TOKEN is checked at boot, CP §6.8, so a BlobError here isn't a config gap.)
    if (err instanceof SyntaxError || err instanceof BlobError) {
      return Response.json({ error: 'Invalid upload request' }, { status: 400 });
    }
    logger.error({ err }, 'upload route failed'); // session store or persistence: a server fault, not bad input
    return Response.json({ error: 'Upload failed' }, { status: 500 });
  }
}
```

Browser:

```ts
import { upload } from '@vercel/blob/client';
const blob = await upload(`users/${userId}/${file.name}`, file, { // the token route rejects any other prefix
  access: 'private',          // personal photos; 'public' only for assets anyone may see
  handleUploadUrl: '/api/uploads/photo-token',
});
```

Serve a private blob through an authenticated route with the SDK's `get()` or a short-lived presigned GET URL (CP §3 "File uploads"). Private access needs a private Blob store and `@vercel/blob` 2.3+.

For server-side fetches (e.g. webhook media downloads from Meta, Slack, etc.), use `put()` from `@vercel/blob` (wrapped in `lib/storage.ts`) directly — no browser involved, no body cap.

---

## 8. Email — Resend

- **Resend** for transactional. React Email components for templates so designers can preview them. Do NOT inline-style HTML by hand.
- One env var (`RESEND_API_KEY`) plus a `RESEND_FROM_EMAIL` for the verified sender.
- Wrap in `lib/email.ts` with named exports per template (`sendWelcomeEmail`, `sendSignInCodeEmail`, etc.).
- React Email components escape interpolated text for you, so `escapeHtml()` belongs only where code builds raw HTML strings (CP §6.6). Encode each interpolated part of a `mailto:` link or query string with `encodeURIComponent` — never the whole URL — and validate the scheme of any user-supplied link. Keep both helpers in `lib/html-escape.ts` and unit-test them.

For inbound email parsing, use **Resend Inbound** (or a webhook from Postmark/SES). Verify the signature before parsing — same rules as any other webhook.

---

## 9. Auth — self-signed JWT + email-code sign-in

The pattern that holds up for early-stage SaaS (`CODING_PRACTICES.md` §4 "Auth & sessions" and §6.1–§6.2 cover the full ruleset):

1. **Sign-in via email code.** `POST /api/auth/request-code { email }` — generate a 6-digit code with `crypto.randomInt`, store `HMAC-SHA256(code, JWT_SECRET)` in Redis under `signin:code:<email>` with a 10-min TTL, send via Resend. Rate-limit to **3 requests per email per hour**. Return success even when the account doesn't exist (no existence leak — OWASP A07).
2. **Verify with `crypto.timingSafeEqual`.** Cap **5 verify attempts per code** before purging, counting attempts atomically (`INCR`). On success, consume the code with an atomic compare-and-delete (a short Lua script) before minting the JWT and setting the cookie, so a code works once even under concurrent requests.
3. **JWT pinned to HS256.** Always set `iss`, `aud`, `iat`, `exp`. Always pass `algorithms: [ALGORITHM]` to the verifier — prevents alg-confusion attacks.
4. **Cookie**: `httpOnly: true`, `secure: true` (in prod), `sameSite: 'strict'`, `path: '/'`, `maxAge: 30 days`. Strict SameSite gives you CSRF coverage on first-party POSTs for free.
5. **Distinct trust domains use distinct secrets.** An admin UI never shares the user `JWT_SECRET`. A single-operator v1 console uses `ADMIN_PASSWORD` and derives its session key from it (CP §6.1); once more than one person administers, move them to email-code accounts signed with a separate `ADMIN_JWT_SECRET` and a different `aud` claim. A salon-side key compromise must not mint admin tokens.
6. **No third-party auth provider until you need OAuth.** Adding Auth0/Clerk/Better Auth to a 50-user pilot is overkill — it's another vendor, another bill, another integration to debug. Reach for **Clerk** (Vercel Marketplace native) or **Better Auth** when you need social login or B2B SSO. Auth.js (NextAuth) passed to the Better Auth team in September 2025 and gets security fixes only; its maintainers point new projects to Better Auth, and its v5 never left beta.
7. **When you have a token-refresh / re-auth round-trip (native OAuth, refresh tokens), classify the failure — don't retry a dead session forever.** A refresh rejected as expired or revoked — **401/403** from your own API, or **400 `invalid_grant`** from an OAuth token endpoint (RFC 6749 §5.2) — means the session is over: clear it and drop to signed-out **once**. (An OAuth `invalid_client` is a configuration error, not a signed-out user.) A **network error / 5xx / gateway timeout** is transient: keep the session and let the next request retry. Collapsing both into "transient" floods the logs with "refresh failed" and never recovers; collapsing both into "logout" signs people out on a blip. This depends on the response handler **preserving the HTTP status**: a failing serverless/proxied endpoint often returns a **non-JSON** error page (a platform "An error occurred" / gateway-timeout page — plain text, frequently starting with a stray character), so a handler that `JSON.parse`s the body *before* checking `res.ok` throws an opaque "invalid JSON" that **discards the status** — turning a classifiable 401/504 into an unclassifiable error and the infinite retry above. Read the body, branch on `res.ok` + content-type, and surface the status on the thrown error.

**IDOR is the #1 bug in App Router APIs.** A Route Handler that reads or mutates a resource scopes the query itself to the caller — `findOne({ _id, tenantId: session.tenantId })`, and the same filter on the update — rather than fetching by id and comparing afterwards: Mongoose `findById` will happily return any tenant's document, and a check-then-write by id can act on a record whose ownership changed in between (CP §4).

---

## 10. Route Handlers — conventions

Every `app/api/**/route.ts`:

```ts
import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/auth-server';
import { isAllowedOrigin, rateLimitUser } from '@/lib/guards'; // CP §6.1, §6.11

// Node.js is the default runtime. Without Cache Components you may pin it with
// `export const runtime = 'nodejs'` (Mongoose and the Redis client need Node APIs);
// with Cache Components that segment config is rejected, so leave it out.

const bodySchema = z.strictObject({ name: z.string().trim().min(1).max(120) });

export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  const session = await getSession();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  if (!(await rateLimitUser(session.userId, 'items:create'))) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  let json: unknown;
  try {
    json = await req.json();
  } catch {
    return NextResponse.json({ error: 'Malformed JSON' }, { status: 400 });
  }
  const parsed = bodySchema.safeParse(json);
  if (!parsed.success) {
    return NextResponse.json({ error: 'Invalid body', issues: parsed.error.issues }, { status: 400 });
  }
  // ... ownership check, mutation, response
}
```

Rules:
- **Always** declare the return type explicitly (CP §1) — `Promise<Response>`, which also admits the AI SDK's and other libraries' `Response` helpers: an inferred return type changes silently when the handler body changes.
- **Always** validate with Zod *before* reading, and catch malformed JSON separately so it returns 400, not 500. PATCH bodies use `z.strictObject()` (or `.strict()`) so an attacker can't slip in `{ accountId: '<other-tenant>' }`.
- **Always** call `getSession()` (or your equivalent) at the top when auth is required.
- **Never** rely on dynamic-route `params` shape — they're `Promise<{...}>` in Next 15+. Always `await` before reading.

For multipart uploads, use `formData.getAll('image')` — `Object.fromEntries(formData)` silently drops repeat keys.

---

## 11. Webhooks

- **Verify the signature BEFORE parsing the body.** Read the raw bytes and verify them with the provider's documented scheme, *then* `JSON.parse`. Most providers sign an HMAC-SHA256 of the body, often with a timestamp; Discord signs Ed25519 over the timestamp plus the body, checked with your app's public key. Parsing untrusted JSON before verification is a free DoS vector.
- **Ack within the provider's timeout** (Slack allows 3 s; check each provider's documented limit). Before returning 2xx, persist the verified event or enqueue it durably (a Vercel Queue, a DB row), then process it from there. `after()` alone loses the event when the background work fails after the provider has its 2xx, because the provider won't retry.
- **Idempotency**: store the event under a unique index on the provider's event ID, in the same write that hands it off durably, with a status (`received` → `processing` → `done` or `failed`). A retry that finds `done` gets a 2xx and nothing more; one that finds `failed`, or `processing` past its lease, is processed again. A bare `SET NX` claim taken before the handoff is the trap: if the handoff then fails, the 5xx brings a retry that finds the claim and skips the event. Keep the records for the provider's whole retry window — Stripe retries for up to three days — rather than 24 hours.
- **Retries belong to the provider, so check each one's documentation.** Stripe retries non-2xx responses and timeouts; GitHub doesn't redeliver failed deliveries on its own, so a GitHub integration redelivers them itself through the API on a schedule.
- For **chat platforms** (WhatsApp, Slack, Telegram, etc.) use **Vercel Chat SDK** — one abstraction over all of them, signature verification baked in.

---

## 12. Security

These live in `next.config.mjs` (static headers) and `proxy.ts` (the per-request CSP nonce) from day one. Don't defer security headers to "after launch" — adding them later breaks every embed and inline script.

- **CSP**: nonce-based, no `'unsafe-inline'` in `script-src`. Generate the nonce in `proxy.ts` and pass it on the forwarded request headers; CP §6.7 has the full pattern, including why a nonce CSP doesn't combine with Cache Components and why experimental SRI doesn't replace it on static pages. `'unsafe-eval'` only in dev (React's dev-only `eval`).
- **HSTS**: `max-age=63072000; includeSubDomains; preload`. `includeSubDomains` forces HTTPS on the subdomains too as soon as a browser sees the header, so confirm none of them still serves plain HTTP before enabling it, and start with a short `max-age` before raising it. Submitting to the preload list is a separate, harder-to-reverse step: browsers hard-code the entry, and removal takes months.
- **X-Frame-Options: DENY** (or use CSP `frame-ancestors`).
- **X-Content-Type-Options: nosniff**.
- **Referrer-Policy: strict-origin-when-cross-origin**.
- **Permissions-Policy**: deny everything you don't use (`camera=()`, `microphone=()`, `geolocation=()`).

When you add a new external origin (image CDN, analytics, AI provider with a custom domain), add it to the relevant `*-src` directive — the CSP will block it otherwise.

**Audit log** any admin-initiated mutation: who, when, what changed (before/after). Persist it in the same DB transaction as the mutation so a write can't succeed without its log entry; CP §6.8 covers audit sinks that live outside the database, and external effects such as refunds, which a database transaction can't make atomic.

---

## 13. Environment variables

- `.env.example` is the **canonical** list of required vars. Tracked in git. Every key documented with a one-line comment.
- `.env.local` is local-only. Gitignore `.env` and `.env.*` with an exception for `.env.example` (CP §6.8).
- **Vercel env** is the source of truth for prod/preview. `vercel env pull .env.local` keeps local in sync.
- **Distinct secrets per trust domain**: `JWT_SECRET` for users; for admins, `ADMIN_PASSWORD` on a single-operator v1 console or `ADMIN_JWT_SECRET` once admins have their own accounts (§9); `CRON_SECRET` for scheduled jobs. Generate each with `openssl rand -base64 32`.

---

## 14. Scripts & tooling

- `scripts/*.ts` invoked via `tsx --conditions=react-server scripts/foo.ts` so they can import `server-only` modules.
- Add the `react-server` flag to every script entry in `package.json` — easy to forget, breaks the next person who copies a script.
- Wrap corporate-cert handling at the npm-script level: `NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem next dev`.
- **Use Caddy for local routing (and HTTPS when you need it).** Commit a root `Caddyfile` from day one when the project has secure cookies, OAuth/webhooks, native clients, or any WebSocket/SSE sidecar. Use a product-owned host such as `<project>.localhost`, route local WebSocket/SSE paths through Caddy under the same origin where possible, and keep `allowedDevOrigins` (`next.config`), `.env.example` app URLs, and CSP `connect-src` in sync with the Caddy host in the same change. **The full proxy model (one shared machine-wide Caddy fronting every repo, the `conf.d/` mirror rule, and the host scheme for design surfaces) is §20 + §22.**

---

## 15. Testing

Default posture: most early-stage SaaS over-invests in unit tests and under-invests in end-to-end coverage. Bias the harness accordingly. Default stack:

- **Playwright** for end-to-end flows (sign-up, sign-in, the golden path of your product). Wire a smoke subset into the gate (§19), run against the built app; the hermetic `test` task below doesn't run them.
- **Vitest** for pure logic (date math, parsing, schema transforms) and for route-handler / Server Action tests, per the day-one harness below. Don't unit-test thin wrappers.
- **No tests that depend on live model output.** Snapshot the prompt + schema, test your handling of valid, invalid and failed responses with the AI SDK's mock models (`ai/test`), and assert on the schema-validated shape, not the model's exact words.
- **Type checking *is* a test.** Run `tsc --noEmit` in the gate, over test files too — `tsc` checks them even though Vitest skips type errors. But a green typecheck is **not** a green build: a duplicate declaration / bad import can pass a noisy type-error baseline yet break the *bundle* so the app won't boot — run the built app (or a smoke E2E) before claiming a change works.
- **If a framework pins you to Jest (NestJS 12 still does for CommonJS projects), use `@swc/jest` as the transform — never `ts-jest`.** In its default mode `ts-jest` type-checks every file on every worker, repeating the gate's type-check (above); the runner only needs types *stripped*, which SWC does without a type-check pass. For NestJS the SWC config **must** emit decorator metadata or DI silently fails to resolve: `jsc.parser.decorators`, `jsc.transform.{legacyDecorator, decoratorMetadata}`, `keepClassNames`, `module.type: 'commonjs'`; pair it with `coverageProvider: 'v8'` (so Jest doesn't re-instrument SWC's output with Babel). On Jest 30 also set `testEnvironmentOptions.globalsCleanup: 'on'`, a `workerIdleMemoryLimit`, and gate coverage + `maxWorkers` to CI so local runs stay lean (a 16-core box shouldn't run 8 heavy workers interactively). *(Vitest on Vite 8 emits decorator metadata itself, so NestJS DI works without this setup; on Vite 6 or 7 add `unplugin-swc` — CP §2 "Tests".)*
- **Assert real *data*, not just "it rendered."** A screen that paints fine while every value shows a placeholder (`—`, `N/A`, `Unknown`, a blank cell) passes a naive "page loads" test but hides a broken data pipeline. For a **known-good fixture** (a real entity the backend definitely has), assert the field renders a *value-shaped* string — a digit, a `$`, a `%`, a date — and explicitly **not** the placeholder. Catalogue every placeholder-fallback site so each gets a value-presence assertion; this is what catches a field silently dropped between the data source and the screen. (A formatter that emits `$0.00` for a `0` passes a naive `$` check — require a digit / non-zero where the real value can't be zero.) Keep the coverage doc honest, too: a flow-map that lists test files which don't exist on disk overstates reality and hides the gaps that matter — list only flows that exist.

For UI work, drive the actual feature in a browser with Playwright before reporting it done.

### Scaffold the test harness on day one (don't backfill)

A common expensive failure mode is every app shipping untested and a later "add coverage everywhere" sweep — far more costly than test-as-you-go, and the sweep repeatedly *finds real bugs* (a proxy 500 on a malformed cookie, a `$set`-into-null first-write 500, an out-of-range date formatter rendering `"1 undefined 2026"`). Set up the harness before the first feature:

- **In-memory Mongo** (`mongodb-memory-server`; its `MongoMemoryReplSet` wherever the code uses transactions, as audit logging does — CP §6.8) for handler / Server-Action / model tests; a Redis in-memory fallback; **jsdom + RTL** for UI.
- **A `server-only` no-op alias stub** in the vitest config — the real `server-only` package throws in a Node test env, blocking any direct unit test of App Router server/`lib/` modules.
- **Separate hermetic unit tests from server/DB-dependent integration tests** into two Vitest projects (`test.projects` in one config; in Vitest 5 projects inherit the root config) with named scripts: `test` = the hermetic project only (explicit `tests/**` exclude); `test:integration` = black-box against a seeded server. The gate runs the hermetic suite; a default `test` must never accidentally require Docker.
- **Risk-weighted "done" bar:** the most security-sensitive app (admin/auth) gets the *strongest* coverage, not the weakest. Privileged/mutating Server Actions need a test asserting the authz gate denies unauthorized callers, the data invariant holds, and PII/secrets never reach audit logs. The proxy/middleware gate, queue happy-paths, and SSR hydration-sensitive UI must be covered before "done".
- **Tests are part of the feature:** every pure `lib/` helper with logic of its own (not a thin wrapper) gets a co-located unit test and every route handler / Server Action gets a handler test *when it is written* — not in a later module-by-module sweep.

---

## 16. Deployment

- **Link the project to Vercel before the first commit.** `vercel link` writes `.vercel/project.json` (gitignored). Preview deployments per PR are free productivity.
- **Promote to prod via merge to main.** Don't use the Vercel UI to promote; the Git history should be the source of truth for what's in prod.
- **Use Vercel Marketplace** for managed infra (Mongo Atlas, Neon, Upstash, Clerk, Resend) — env vars auto-provisioned, billing rolled into your Vercel invoice, no extra dashboards to log into.
- **Cron jobs**: Vercel Cron, with the route handler rejecting any request whose `Authorization` header isn't `Bearer <CRON_SECRET>` and failing closed when `CRON_SECRET` is unset. If part of your stack runs as a **persistent process** (a long-lived container, not a serverless function), schedule its jobs **in-process** there (e.g. a cron decorator) and reserve HTTP-triggered serverless cron for the serverless layer — don't add a `CRON_SECRET` HTTP endpoint for work the persistent process can run directly.
- **Background work**: `after()` from `next/server` for fire-and-forget. **Vercel Workflow SDK** (the `workflow` package, formerly the Workflow Development Kit) when you need durable, retry-able, multi-step orchestration (e.g. multi-stage AI pipelines, payment + provisioning flows).
- **Mind the function `maxDuration` vs cold-start bootstrap.** A server framework that connects to a DB/cache *during bootstrap* (NestJS/Fastify/Express wrapped in a serverless function) can exceed the function's `maxDuration` on a **cold** start — every cold request then 504s (`FUNCTION_INVOCATION_TIMEOUT`) while warm requests are fine, so it reads as "intermittent." Three compounding traps: **buffered logging** (logs flushed only after init completes) emits *nothing* when init hangs, hiding where it's stuck; a **warm-up cron** that hits the same cold-capped endpoint can't warm a function that can't bootstrap within the limit (chicken-and-egg); and an explicit low `maxDuration` in `vercel.json` caps it below the real bootstrap cost. Cache the connection/app **promise** across invocations (so two concurrent cold invocations don't both bootstrap), give bootstrap realistic headroom, and turn off log buffering while diagnosing.

---

## 17. Monorepo (pnpm workspaces + Turborepo)

If you anticipate more than one deployable (web API + operator console + native client, etc.), start as a **pnpm-workspaces + Turborepo monorepo on day one** — retrofitting standalone npm repos into one workspace is expensive (an app scaffolded standalone, with its own `git init` + `package-lock.json`, has to be unpicked and redone later).

**Layout**

```
apps/
  <web-api>/         Next.js → Vercel
  <admin>/           Next.js → Vercel
  <native>/          Expo / React Native (no Vercel project)
packages/
  contract/          shared wire DTO types (see §18 + CODING_PRACTICES §6.10)
docs/<project>/      durable per-project docs
CLAUDE.md            root entry point
apps/*/CLAUDE.md     per-app detail; root points at them
.gitignore           ONE consolidated root file (no per-app .gitignore)
pnpm-workspace.yaml  turbo.json  pnpm-lock.yaml
```

**Rules**

- **pnpm only, one lockfile.** Never run `npm install` inside an app; never commit `package-lock.json`. `pnpm install` at the root installs the whole workspace.
- **Run gates through Turborepo** (`pnpm turbo run lint typecheck test build`), not per-app npm scripts — caching makes the full gate cheap.
- **No nested `git init`.** One root repo, no submodules. Pick which repo's history to keep before merging; archive the rest.
- **One consolidated root `.gitignore`** — write per-tool / local-state patterns with a leading `**/` (e.g. `**/.env.local`, `**/.claude/settings.local.json`) so they reach inside every `apps/*`. A slash-anchored pattern matches only the repo root and once leaked an `apps/*` file into a commit. Anchor generated-dir patterns to root with a leading slash (`/coverage`) so a bare glob doesn't swallow a nested source file. Verify with `git check-ignore -v` on a nested path before the first commit.
- **Vercel: one project per deployable**, each with Root Directory = `apps/<name>`. Leave Vercel's automatic skipping of unaffected projects on, so a push touching one app doesn't redeploy the others; for a project that doesn't qualify for it, Vercel now recommends an ignored-build step built on `turbo query affected` rather than `npx turbo-ignore`. Native / App-Store apps get no Vercel project.
- **Docker:** one root Dockerfile using `turbo prune --docker` + Next.js `output: 'standalone'`, one image per app via a build-arg. Set `output: 'standalone'` from the start on any Next app that must run in Docker (not just Vercel): it produces the lean image this layout assumes, and Vercel ignores it, so it's safe everywhere. (`next start` with installed `node_modules` also runs in a container; standalone is what keeps the image small.) Use **exec-form** `CMD` (JSON array) so the process is PID 1 and receives SIGTERM for graceful shutdown.

### pnpm workspace mechanics (pnpm 11/12)

- **`overrides` and the native-build `allowBuilds` allowlist live in `pnpm-workspace.yaml`**, NOT in any `package.json` `pnpm.*` / `overrides` field. pnpm 11 ignores the package.json block and auto-writes an `allowBuilds:` stub — confusing churn. pnpm 12 also errors on unknown keys in `pnpm-workspace.yaml`, so copy setting names exactly.
- **pnpm 11+ fails the install on an unapproved build script** (`strictDepBuilds: true`, supply-chain safety). Pre-approve only the native binaries the toolchain genuinely needs (`esbuild`, `sharp`, `protobufjs`, `mongodb-memory-server`, native resolvers) in `allowBuilds`. (pnpm 10 skipped unapproved builds silently, which surfaced later as cryptic runtime failures.)
- **No phantom deps.** pnpm exposes only a package's *declared* dependencies (no flat hoisted `node_modules`). An unresolved import = an undeclared dependency: add it to that app's `package.json`. **Never** add `shamefully-hoist` to paper over it. Migrating from npm/yarn surfaces these; run the full gate with `--continue` to flush them all in one pass.
- **Never silence peer-dependency conflicts globally** (`legacy-peer-deps`, `shamefully-hoist`). Pin the specific offending transitive peer to the root version via a scoped `overrides` entry — a blanket setting masks *other* real conflicts that then surface only on re-resolve.

### Cross-app contracts are part of the gate

In a monorepo where the gate is a pre-push hook (no hosted CI) and apps are independently typed, **TypeScript can't catch a shape mismatch across two apps** — each side compiles green while the wire shape diverges. Scaffold the cross-app safety net *with the first cross-app feature*, not after a review finds drift:

- a shared `packages/contract` for wire DTOs (preferred), or
- twin key-set parity tests on producer and consumer, wired into the `test` gate.

Treat the wire-DTO parity test as part of a cross-app feature's definition of done. Full detail and the bidirectional-guard rule live in CODING_PRACTICES §6.10.

**If the wire contract is a GraphQL schema**, put codegen + a schema-drift check in the gate. A consumer whose generated types are hand-synced from the backend schema breaks every operation that uses a field the backend renames or removes, and mishandles a field whose nullability changes; additive fields are safe. Regenerate types from the live schema in the gate and fail on drift — the same role the parity test plays for REST DTOs.

---

## 18. React Native / Expo client (in a monorepo)

When a pnpm-workspace monorepo includes an Expo/RN app:

- **Use pnpm's default isolated layout.** Expo supports isolated (non-hoisted) installs from SDK 54, so a new monorepo needs no hoisting. If a native dependency still fails to resolve, fall back to `nodeLinker: hoisted` in `pnpm-workspace.yaml` (pnpm 12 errors on misspelt keys there) and add `pnpm-workspace.yaml` to Turborepo `globalDependencies` so the change busts the cache.
- **Leave Metro's monorepo config to Expo.** Since SDK 52 Expo configures `watchFolders` and resolver paths for workspaces automatically. Delete hand-written `watchFolders`, `resolver.nodeModulesPaths`, `extraNodeModules` and `disableHierarchicalLookup` from `metro.config.js`; they now fight the defaults.
- **New Architecture only.** From SDK 55 (SDK 58 ships React Native 0.88) Expo ignores `newArchEnabled`, so a library that only supports the legacy architecture has to be replaced, not flagged off.
- **Native / App-Store apps get no Vercel project**, but they still get a test gate — see below.
- **Give every sibling app a distinct identity — from day one.** When two native apps ship from one codebase (a fork, or a customer + operator variant), a shared **bundle/application id** makes them *install over each other* on a device/simulator and share a keychain / secure-store namespace (one app reads the other's stored session — a real "logged in as the wrong app's user" bug), and a shared **URL scheme** or **OAuth redirect** makes them race for the same deep link. Make each unique per app and change them **together**: the native id (`ios.bundleIdentifier` / `android.package`), the URL `scheme`, the OAuth/PKCE redirect URI, and the deep-link linking `prefixes`. Two coordination traps: the linking-config `prefixes` must include the **declared** scheme (a prefix that doesn't match the registered scheme is dead — incoming links never resolve), and any reminder/notification that emits a deep link must use that same scheme. Changing an id has **external** follow-ups the code can't do — add the new redirect URI to the OAuth app's allowed-callback list, and re-register the new id with the push/analytics provider (a new Firebase app + fresh `GoogleService-Info.plist` / `google-services.json`) — flag these explicitly, because the app silently loses sign-in / push until they're done.

### Test gate for an RN/Expo client

Run a **Node-env Vitest over the PURE, framework-free `lib/` helpers only** (ratings math, date/name formatting, adapters, country/city tables). Wire it into the Turborepo `test` gate alongside the web apps — even the first such tests tend to catch real bugs (e.g. an out-of-range month rendering `"1 undefined 2026"`).

- Keep those `lib/` modules free of *runtime* react-native / expo imports: use `import type` for RN types, never value-imports, and don't `require()` image assets in pure modules.
- Modules that touch the RN runtime, reanimated, or asset `require()`s are out of scope for the Node suite — device / E2E-test them. Mock the module that pulls assets rather than aliasing/stubbing image requires.
- Document this boundary in the app's `CLAUDE.md` so testers don't rediscover it per file.

### Device / E2E coverage for an RN/Expo client

The Node-`lib/` suite above is the cheap unit gate; the user-facing flows still need a device E2E pass (**Maestro** or **Detox**):

- **Test the return paths, not just the forward path.** Every pushed screen, modal, and sheet must expose a working Back / Close / dismiss affordance that lands the user where they came from — a screen with no reachable back control is a stranded dead-end. Assert the back/close on *every* pushed screen, including the **second** route inside a nested stack (its Back must pop one level, not jump to the root) and a modal **Close** (a different control from a header Back chevron).
- **Seed the data a flow needs; presence-guard only what is genuinely optional.** A flow that opens a list row / detail that only exists when the backend has data will flake, but a guard that skips when the entry control is missing also skips when a regression hides it. Seed deterministic fixtures for required flows and fail when their entry point is absent; wrap only optional steps in a "run if visible" guard, and surface what was skipped so a silent skip doesn't read as coverage.
- **Selector gotchas that silently break flows.** Text matchers in these runners are usually **anchored** (full-string), so `text: "Legal"` does **not** match a row rendered as "Legal & disclaimers" — use a substring/wildcard. A touchable with `accessible` set (the default for a `Pressable`/button) **collapses its child text into one combined accessibility label**, so an individual label isn't matchable on its own — match the combined label, or better, add a `testID`. Put stable `testID`s on the controls each flow taps and the data cells it asserts; matching on copy breaks every time the copy changes.
- **Drive the *built* app.** Boot the installed app and run at least one flow before claiming a change works — a bundling/integration error (duplicate declaration, bad import) that a noisy typecheck baseline misses fails the bundle outright.

### Finding the gaps systematically

When auditing E2E coverage for any non-trivial client, fan the analysis out across **independent dimensions** rather than one linear pass — input/forms, navigation + return paths, data-integrity (placeholder vs real value, §15), and error/empty/loading/auth-gate/deep-link states. Each dimension surfaces gaps the others miss, and the sweep reliably turns up *real bugs* alongside missing tests (a deep-link scheme that doesn't match the registered one, push routes pointing at screens that don't exist, a redirect to a route that was renamed). Catalogue both — gaps and bugs — and prioritise.

---

## 19. Quality gate / CI strategy (decide day one)

Decide and **write down** the quality-gate mechanism before any spec says the word "CI" — otherwise an agent reads "CI runs …" and scaffolds a GitHub Actions pipeline that then gets torn out. Left unstated, this churn repeats — sometimes within an hour — until the decision is recorded.

Two viable shapes:

| Gate | When | Cost |
|---|---|---|
| **Hosted CI** (GitHub Actions) | open-source, many contributors, required status checks | runner minutes, secrets in CI |
| **husky pre-push hook** | small trusted team, monorepo, want true Vercel parity locally | per-clone `vercel link` / `vercel pull`, no cloud feedback on PRs |

For a small trusted team, a strong gate is a **husky pre-push hook** running `turbo lint+typecheck+test` + a **real `vercel build`** (not a cheaper `next build` approximation — true parity catches `standalone` / CSP-nonce / build-time-env bugs the static gates miss), with `SKIP_VERCEL_BUILD=1` as the only bypass and no hosted CI at all.

- Install the hook automatically via the root `package.json` `prepare` / husky script so every clone is gated with no manual step.
- A real `vercel build` needs `vercel link` + `vercel pull` per clone and a gitignored `.vercel/`.
- Treat any spec phrase "CI runs X" as "the gate runs X". Record the decision in the monorepo / setup doc so it isn't re-litigated.

### Scope the gate to what the push changes

A monolithic gate that runs every app's typecheck + build + smoke on *every* push wastes minutes when a push touches only one app, the docs, or an npm-isolated native island (§18) the gate doesn't even cover. Make the hook **path-aware**: read the refs being pushed from the hook's stdin (one `local-ref local-sha remote-ref remote-sha` line each), diff each `remote-sha..local-sha` range, and run each area's checks only when that area — or shared code that all apps consume — is in the union of those diffs.

- **Map changed paths → affected gates.** `apps/<web>/**` → web lint + typecheck + test + build + the Playwright smoke subset (§15); `apps/<api>/**` → api lint + typecheck (test files included) + test + build + smoke; **`libs/**` / `packages/**` / lockfile / base `tsconfig` / workspace config → all of them** (cross-cutting code forces a full revalidate). A push that touches only a native app runs its `lib/` suite (§18) and not the web/api checks; a push that touches only documentation `*.md` runs none (Markdown the build renders counts as code).
- **Fail safe, never skip on doubt.** If a range can't be computed (a new branch whose remote SHA is all zeros, detached HEAD, shallow clone), run **everything**. Skipping is only ever for a change you can *prove* is out of scope.
- **Tier the broad-but-cheap checks.** A diff-scoped code review is worth running for any code change but can skip a docs-only push; type/build/smoke skip whenever their app isn't affected.
- **Give it an escape hatch.** `GATE_FULL=1 git push` forces the whole suite — for lockfile bumps, toolchain changes, or a belt-and-suspenders run.

---

## 20. Local dev proxy — one shared Caddy for the whole machine

Run **one machine-wide Caddy on `:80`** that fronts *every* repo on the dev machine — not Docker's port mapping, not a per-project nginx. Containers publish only high ports, bound to loopback (`127.0.0.1:3010:3000`, `127.0.0.1:3020:3000`, …) so they aren't reachable from the LAN; Caddy host-routes `:80` to them by hostname. Every app gets a real, stable origin, so cookies, OAuth redirects, CSP and WebSockets behave close to prod, and any number of repos coexist without port collisions.

**Two-file layout**
- **Machine config** (e.g. `/opt/homebrew/etc/Caddyfile` on macOS/Homebrew): the global options block **plus** `import conf.d/*.caddy`. It owns the one global block for the whole machine.
- **Per-repo route file** (`<caddy-etc>/conf.d/<repo>.caddy`): only the `http://<host> { reverse_proxy localhost:<port> }` route blocks for that repo.
- **Repo-local `Caddyfile`** (committed): the same routes **plus** a leading `{ auto_https off }` global, so a contributor can run the repo standalone with `caddy run --config Caddyfile`.

**Mirroring the repo `Caddyfile` into `conf.d/` is NOT a plain `cp`.** The machine `Caddyfile` already owns the global block, and Caddy requires globals to be **first** in the combined config — so an imported `conf.d/*.caddy` that carries its own `{ … }` global fails validation with *"server block without any key is global configuration, and if used, it must be first."* Strip the global block; mirror only the route blocks; `caddy validate --config <machine Caddyfile>` before reloading.

**Operating it**
- **Use `<project>.localhost` names.** macOS 26+ resolves `*.localhost` to loopback with no `/etc/hosts` entry, and Chrome and Firefox treat `http://*.localhost` as a secure context. On older macOS, add `127.0.0.1 <host>` and `::1 <host>` lines to `/etc/hosts`. A `.local` name belongs to Bonjour (mDNS): it needs both lines on every macOS version, or each lookup stalls for seconds before falling back.
- **No sudo.** macOS lets an unprivileged process bind `:80` on the wildcard address (`0.0.0.0`), so start Caddy with `brew services start caddy` and reload with `caddy reload --config <machine Caddyfile>`. `sudo brew services` only moves the job to a boot-time daemon and leaves root-owned files behind. The wildcard bind does put Caddy's sites on the LAN: anyone there can reach them by sending the right `Host` header. A phone can't use the `*.localhost` names (they resolve to the phone itself), so a test device needs a LAN-resolvable hostname with a matching Caddy site, or a tunnel. To keep Caddy off the network, set `default_bind 127.0.0.1` in the machine Caddyfile's global block, which then does need root.
- **HTTPS when you need it.** Plain HTTP covers most work on `*.localhost`. When an OAuth provider or Safari needs real HTTPS, change that site's address from `http://<host>` to `https://<host>` with a `tls internal` line, drop `auto_https off` from the repo-local Caddyfile, run `caddy trust` once to install Caddy's local CA, and move Vite's `server.ws.clientPort` to 443.
- **A 502 from a proxied host = Caddy can't reach the upstream** — the container is down, or a stale proxy (old nginx) still holds `:80`. Check the container first.
- **Add another repo:** drop `conf.d/<repo>.caddy` (plus its `/etc/hosts` lines, if you added them) + reload. No other repo is touched.

---

## 21. Dockerized local dev stack

Run the whole stack — every app plus its infra (DB, Redis, a mock email server) — under **one `docker-compose.dev.yml`**, fronted by the shared Caddy (§20). Run the dev MongoDB as a single-node replica set (`--replSet rs0`, then `rs.initiate()` once), because the audit-log transactions in CP §6.8 need one. Each gotcha below comes from a real "works on host, breaks in container" (or vice-versa) failure; they are the difference between a dev stack that boots clean and one that crash-loops into 502s.

**Never bind-mount `node_modules`.** Mount source only; give each app a **named volume** for `/app/node_modules` *and* for every nested `/app/apps/<x>/node_modules`. Two failures this prevents:
- The container's `pnpm install` writing into a host-bind-mounted `node_modules` **clobbers the host's** modules — the next host `tsc`/`build` fails with hundreds of "cannot find module". (If it happens, restore with a host `pnpm install --frozen-lockfile`.)
- macOS/Windows host modules mounted into a Linux container resolve to broken native binaries / symlinks.
Give **each service its own** isolated `node_modules` + pnpm-store volumes (not one shared store) so parallel services don't fight.

**Check that file events reach the container before turning on polling.** An open 2024 report (docker/for-mac#7246) found that VirtioFS on Docker Desktop for Mac delivers create and modify events for bind mounts but not deletes, and Vite's docs mention polling only for WSL2. Earlier setups here still missed hot reloads, so test once on the actual setup: create, edit, rename and delete a source file and watch the container's logs. If an event you rely on never fires, force polling **scoped to Docker only** so native/CI runs keep efficient event-based watching:
- nodemon / chokidar: `CHOKIDAR_USEPOLLING=true` (+ `CHOKIDAR_INTERVAL` matched to the rebuild cost — e.g. ~3s for a full-process restart like NestJS; polling faster just burns CPU).
- Next.js: `next dev` runs Turbopack, which documents no polling option and ignores webpack config, so `WATCHPACK_POLLING` has no effect there. If events don't arrive, run `next dev --webpack` with `WATCHPACK_POLLING=true` in the container, or run the Next dev server on the host.
- Vite **through the proxy**: set `server.allowedHosts` and `server.ws.clientPort` = Caddy's port (80 for HTTP, 443 once the site is HTTPS; Vite 8 deprecates the old `server.hmr.clientPort`) in every setup, so the HMR websocket reconnects to `<host>` and not `localhost:5173`; env-gate `server.watch.usePolling` for the cases above.
Add a watch **ignore list** of files the watched process never loads — tests, `__fixtures__`/`__mocks__` (unless Storybook or the app imports them), `*.d.ts`, `.DS_Store` — plus files the process writes itself at boot, such as generated schema files, which would otherwise restart it in a loop. Keep watching anything the running process reads.

**Mask heavy *unused* subtrees nested under a bind mount — on macOS they exhaust the host's *system-wide* file table and `ENFILE` unrelated apps.** A container that bind-mounts a parent dir (`./apps`) inherits **every** child under it — including apps it never imports (an npm-isolated native island excluded from the workspace, §18) and their giant generated trees: that island's own `node_modules` (100k+ files *each*) and CNG-generated native dirs (`ios/Pods`, `android/**/build` — tens of thousands of files). On **macOS** with Docker Desktop's Apple Virtualization framework VMM (the setup this was observed on; Docker VMM is built differently), Docker's file-sharing runs inside one VM process (`com.apple.Virtualization.VirtualMachine`) that was seen holding an **open file descriptor per shared/watched file**; with the polling watchers above traversing those trees across several containers, that single process can accumulate **tens of thousands of FDs and exhaust the system-wide `kern.maxfiles`** — *not* the per-process `ulimit`. The tell is **`ENFILE` / "too many open files in system" in a completely unrelated app** (a native build tool aborting, a browser unable to open tabs) while every per-process limit looks fine. Diagnose with `sysctl kern.num_files kern.maxfiles` (near-equal ⇒ exhausted) and `lsof -nP -p <vm-pid> | wc -l` to find the hog.

Fix: **mask each heavy/unused subtree with an empty anonymous volume** in *every* service that bind-mounts the parent — a container path with no host source tells Docker to shadow the host dir, so the container's watchers never traverse it. Re-run the `lsof` count on the VM process afterwards to confirm the host side dropped too, because descriptor behaviour depends on the VMM and file-sharing backend:

```yaml
volumes:
  - ./apps:/app/apps:cached                       # legit: the workspace apps THIS container builds
  # mask trees no container here needs — an isolated native island + its native build output:
  - /app/apps/<native-island>/node_modules
  - /app/apps/<native-island>/ios
  - /app/apps/<native-island>/android
```

It's the same mechanism as the per-app `node_modules` named volumes above (an empty mount shadowing a path *inside* a bind mount) generalised to **any** big subtree, not just `node_modules`. Restarting Docker reclaims the FDs instantly, but they re-accumulate until the masks are in place — the masks are the durable fix.

**Raise the macOS file ceiling for headroom** — check the current value with `sysctl kern.maxfiles`; it is too low for a box running Docker + a native/IDE toolchain + browsers at once. A higher ceiling buys time; the masks above are what stop the leak:

```bash
sudo sysctl -w kern.maxfiles=524288 kern.maxfilesperproc=262144   # runtime
```

To persist it, use one LaunchDaemon (`RunAtLoad`) that runs that same `sysctl -w` command. `launchctl limit maxfiles` is not a substitute: it sets launchd's per-process `RLIMIT_NOFILE`, not the system-wide table, and SIP blocks it on current macOS. Remove older maxfiles settings first — other `maxfiles` plists in `/Library/LaunchDaemons` and `kern.maxfiles` / `kern.maxfilesperproc` lines in `/etc/sysctl.conf`, after checking what installed them — because two persisted settings race at boot; confirm after a reboot with `sysctl kern.maxfiles kern.maxfilesperproc`.

**Keep installs lean and lockfile-honest.**
- For a small static surface (a mock-UI app, a docs site), `pnpm install --filter <app>` (+ `--ignore-scripts` to skip native postinstalls it never needs) instead of a full workspace install — minutes → ~1 min startup.
- `--frozen-lockfile` validates the **entire** workspace even with `--filter`. A stale lockfile or out-of-date **workspace exclusions** (after a directory rename) then fail **every boot** with `ERR_PNPM_OUTDATED_LOCKFILE`. Keep the globs and exclusions in `pnpm-workspace.yaml` current after a rename, and in the root `package.json` `workspaces` too if another tool in the repo reads that field.
- If any dependency is patched (`patchedDependencies` in `pnpm-workspace.yaml`; pnpm 11 ignores the `pnpm` block in `package.json`), the install reads the patch files — **mount/COPY `./patches`** into every install context (the dev container *and* `Dockerfile.base`), or the install ENOENTs. Use an optional glob (`patches[/]*`) in Dockerfiles so branches with no `patches/` dir still build.
- **Pin pnpm per island** when a standalone app ships an old lockfile (a v6 lockfile can't be read by pnpm 10) — that island runs `--ignore-workspace` and declares its own `packageManager`.

**Image / process gotchas.**
- `node:*-alpine` sets no `$SHELL`; `chokidar-cli` throws *"$SHELL environment variable is not set"* and (via `concurrently --kill-others`) takes the whole container down → 502. Set `SHELL=/bin/sh`.
- Healthchecks: probe **`127.0.0.1`**, not `localhost` — busybox `wget` resolves `localhost` to `::1`, but `sirv`/Vite bind IPv4 `0.0.0.0` only, so a `localhost` probe is refused and the service reads as falsely "unhealthy".
- Set per-service `mem_limit` and raise `ulimits.nofile` (watchers, polling ones especially, exhaust the default FD limit).
- Any Next app that must run in Docker should use `output: 'standalone'` and an **exec-form** `CMD` (JSON array) so it's PID 1 and receives SIGTERM (see §17).

---

## 22. Design system: token single-source, Storybook & mock-UI surfaces

A multi-surface product (web + native + marketing) drifts visually unless tokens have **one source** and components have **one catalogue**. Set both up before the second surface exists — retrofitting a token source across N hand-synced copies is exactly the rework this avoids.

**Tokens: one source, everything generated.** Keep design tokens in a single library (`libs/design-tokens/src/tokens.ts`) and **generate** every downstream copy — CSS custom properties, a Tailwind preset, a Chakra/shadcn fragment, React-Native token objects. A `tokens:sync` script writes them; a `tokens:check` script regenerates in memory and **fails CI on any drift**. Apps that can't import the lib (npm-isolated native islands, §18) get a **generated + committed** copy guarded by the same drift gate. **Never hand-edit a generated token file.**

**Two Storybooks in 1:1 parity.**
- **HTML-reference Storybook** — raw HTML/CSS using the exact tokens. The source of truth for *how it should look*. Organise as `foundation/` (tokens) → `primitives/` → `patterns/` (composed combinations) → `pages/` (full compositions) → `consistency/` (the do/don't + "one way" rules).
- **React host Storybook** — the production components with Controls. The source of truth for *how it's built*. It **composes the HTML reference via `refs`**. The ref loads in the browser, so its URL has to be one the browser can reach. This setup uses the reference Storybook's **published port**: Storybook accepts any reachable URL, but a proxied top-level host didn't work as a ref when this was written, so check one loads before switching to it.
- **Parity is the rule:** every HTML story has a React counterpart and vice-versa — no orphans. Converting an AI-designed HTML mock to React means matching its reference story exactly.

**Mock-UI preview app (optional, high-leverage for design handoff).** A lean standalone app that renders full-page mock-ups + a component gallery, with an `index.html` **hub** linking every design surface. Keep it dependency-light — an in-browser transform (`@babel/standalone`) + a static server (`sirv`) + a file watcher (`chokidar`) is enough; it needs *none* of the product's heavy deps, which is what makes its container install tiny (the lean filtered install in §21). Treat its built HTML as a build product — never hand-edit it; edit the `*.jsx` source and let the watcher rebuild.

**Serving scheme (ties §20 + §21 together).** Put the design surfaces on a predictable host map: a **hub** host plus, per system, `<system>` (interactive preview/flow) and `<system>-atlas` (its component catalogue / Storybook):

```
<project>.localhost                       → web app
api.<project>.localhost                   → API (dev convenience only; the BFF rule still applies)
mock.<project>.localhost                  → design-system HUB (landing page linking every surface below)
web.mock.<project>.localhost              → web preview / mock-UI app
web-atlas.mock.<project>.localhost        → web React Storybook
<native>.mock.<project>.localhost         → native flow (react-native-web)
<native>-atlas.mock.<project>.localhost   → native Storybook
```

- Use **dedicated `-atlas` subdomains, not `/atlas` sub-paths** — sub-path routing breaks Storybook's absolute asset URLs. `<system>` vs `<system>-atlas` is grep-able and lets every surface reload independently.
- The hostnames are a convention (`*.localhost` resolves to loopback on macOS 26+, and through `/etc/hosts` before that); keep the repo `Caddyfile` host map and the compose port map as the single readable index of what's where.

**Storybook in a monorepo:** scope `vite-tsconfig-paths` (or any tsconfig-path plugin) to **each app's own tsconfig** in `.storybook/main.ts`. Left unscoped it eagerly crawls *every* tsconfig in the workspace (sibling apps, agent worktrees) and aborts the build if any `extends` can't resolve.

---

## 23. Build & worktree hygiene (parallel-agent DX)

When many agents (or many feature branches) build in parallel, the toolchain itself becomes the bottleneck. Settle these once.

**Fast, crash-free typecheck.** The JS-based compiler (TypeScript 6) can hit a V8 stack overflow (exit 134) on a large monorepo, and it's slow. TypeScript 7.0 (July 2026) is the native compiler that `tsgo` / `@typescript/native-preview` previewed (that package is retiring). While §2 holds `typescript` at 6.0 for typescript-eslint and `@nestjs/cli`, you can optionally run 7.0 beside it — worth it when typecheck time matters — with Microsoft's side-by-side layout:

```json
"devDependencies": {
  "@typescript/native": "npm:typescript@^7.0.2",
  "typescript": "npm:@typescript/typescript6@~6.0.2"
}
```

`npx tsc` then runs 7.0, `tsc6` runs 6.0, and tools that `require('typescript')` keep the 6.0 API. Point the `typecheck` target at `tsc`. TypeScript 7 turns every option 6.0 deprecated (`baseUrl`, `moduleResolution: node`, …) into a hard error, so fix those first, and keep a `typecheck:tsc6` script as the fallback. In this layout `next build` resolves the `typescript` package and runs its `tsc6`, so Next's own type-check stays on 6.0 while your `typecheck` script uses 7.0; both should pass. Run gates with the Nx/Turbo daemon disabled or bounded parallelism so N worktrees don't all spawn daemons at once.

**Git worktrees for parallel work — install, don't symlink.** Each worktree carries its own `node_modules` tree (pnpm hard-links or clones from its store on the same volume and copies across volumes), is watched by watchman, and can spawn its own Nx/Turbo daemon — so stale ones tax disk and idle CPU.
- **Do a real `pnpm install` in each worktree, not a `node_modules` symlink.** A symlink satisfies `tsc`, but Turbopack `next build` panics (*"symlink points out of filesystem root"*). A real install also recreates `.husky/_`, so the **pre-push gate actually runs** — a bare `git worktree add` leaves no `.husky/_` and the gate silently no-ops. Wrap worktree creation in a script that bootstraps husky.
- **Prune merged worktrees periodically.** A prune script should remove a worktree **only** when its tree is clean **and** its HEAD is an ancestor of `origin/main`/`origin/staging` (fully integrated — nothing is lost, git keeps the branch + history); stop that worktree's daemon before removal; default to a dry run, with `--apply` to act.
- Add a `.watchmanconfig` to bound the watch surface.

---

## 24. Environment- and tenant-correct behaviour

The server is the only thing that reliably knows *which environment* and *which tenant* a request belongs to. Push these decisions to the backend and have the client consume the answer.

- **The backend is the single authority for environment-dependent behaviour.** A client/SSR build often *can't* tell staging from production — many frameworks set `NODE_ENV=production` for **every** non-dev build, staging included — so any "do X in staging but not prod" decision made in the web/client build is wrong half the time. Resolve environment-gated behaviour (feature flags, test-only affordances, internal-user visibility) on the server/API by its **own runtime environment**, and have the client just read the resolved answer. Never branch on `NODE_ENV` / a public env var in client code for these.
- **Feature flags: env-targeted, evaluated server-side, for *complete* features only.** Persist them (DB) with a per-environment config and evaluate on the API by its runtime env; the client reads the resolved value. Flags are for rollout / A-B / kill-switch of **finished** features — never to hide incomplete, mocked, or fallback code.
- **Gate internal / test users — environment-aware, at the data source.** Staff/test accounts (e.g. everyone on your own email domain) must be hidden from customer-facing people-pickers / lists / counts **in production only** (kept visible in staging so the team can test assign/share/approve flows), and — critically — the **only** recipients of outbound email / push / notifications in **non-production** (a staging test run must never email or notify a real customer). Enforce both at the **backend data source and the outbound choke points** (the tenant-scoped finder, the email sender, the notification dispatcher), not in the client — per the single-authority rule. A separate service that owns its own outbound (e.g. a standalone push service) needs the same guard replicated, or staging push leaks to real devices.
- **The browser never calls the backend directly — go through your own API layer (BFF).** All client HTTP goes through your app's route handlers, which attach auth + tenant context server-side. The exceptions are explicit: direct-to-storage uploads with a BFF-issued token (§7), and WebSocket/SSE connections the BFF can't carry. Enforce the rule with a lint rule that blocks the public backend URL and `axios` in client code, so the boundary can't erode.
- **Multi-tenant context is server-authoritative.** The active tenant is a selection held server-side or in a signed httpOnly cookie, and the backend checks the session's membership of that tenant on every request: `httpOnly` only hides a cookie from JavaScript, it doesn't make its value trustworthy. The selection is forwarded as a header to the backend; any client-side copy (sessionStorage) is a non-authoritative cache — always populated *from* server responses, never the source of an access decision. Never hardcode a tenant fallback id (`'default-company'`); resolve it from the session or fail closed. Centralise session-validation and header-building in **one** shared helper each — don't let every route handler reinvent them (drift is how an auth check gets skipped).

---

## 25. Changing a security control safely + debugging the request path

Security tightening repeatedly ships *working-but-breaks-a-legit-flow*. Request layers fail **in order** and each failure **masks the next** (input sanitisation 400 → auth 401 → RBAC 403 → schema validation 400 → handler) — so after changing any one layer, exercise the affected endpoints **end-to-end with a real payload and the real auth mode**; don't conclude from the first error that there's only one bug. Each recurring failure below is a generalizable rule:

- **An internal secret-authed endpoint needs every global layer reviewed in one change.** Replace user auth/RBAC with the endpoint's own secret check, then decide layer by layer whether the rest (input sanitisation, size limits, logging) still applies, because exempting one layer at a time exposes the next as a "new" bug. Keep the input checks that still fit: the endpoint still receives untrusted bytes. Keep the path match **segment-anchored** so the exemption can't leak to sibling routes, and confirm the endpoint's own secret check still rejects a missing/wrong secret.
- **Calibrate size/validation caps against the largest *real* payload, not a guess.** A `@MaxLength` / `.max()` set to a round number has rejected real production documents. The cap's job is to stop unbounded abuse, not to encode a guess about typical size.
- **Tighten a schema against what the *producer actually emits*, never by adding new required fields.** Requiring a field the producer doesn't always send rejects every valid payload. Tighten with `.optional()` fields, array/size caps, and dropping `.passthrough()` / `.loose()`: a plain `z.object()` strips undeclared extras without rejecting valid existing data. Switch to `z.strictObject()` only once you know the producer sends nothing extra. Grep the producer (and a stored payload) before requiring anything.
- **`forbidNonWhitelisted` / strict shapes break clients that round-trip persisted objects** — edit forms re-send server-managed fields (`_id`, timestamps). Audit every caller and have them send only the whitelisted fields.
- **Never register a route permission no role actually grants** — it silently 403s every user of the feature. Confirm the permission string exists in some role's grant list before registering it. If every signed-in user should reach the route, say so explicitly in the route's config instead of registering a permission nobody holds; a missing grant never falls through to plain authentication.
- **Sign OAuth `state` and bind it to a nonce cookie.** For any OAuth connect/callback flow, HMAC-sign the `state` and bind it to a short-lived httpOnly nonce cookie — unsigned/base64-only state lets an attacker craft `{ userId: <victim> }` and graft their own token onto the victim's account. The signing secret is required at runtime; throw if it's unset.

**Debug the request path by instrumenting boundaries first — don't chase error strings.** In a multi-hop system (browser → BFF → backend), add logging at the boundary points (route handler, controller) to capture the *actual* status, a correlation id and the body's shape — field names, sizes, redacted values (CP §4 A09) — **before** searching the codebase for the error text. The reported string is often stale (a previous version), transformed by an intermediate layer, or a fallback message masking the real error. Two specific traps: a global **response interceptor that wraps handler returns** in `{ success, data, … }` means consumers must unwrap exactly one level — a double-wrap or a missing unwrap reads as a "shape" bug; and **don't assume JWT claims are populated** (in some local/impersonation setups `email`/`name` are empty) — look the user up from the DB rather than trusting the token fields.

---

## 26. Anti-patterns to avoid

- **Don't add features behind feature flags from day one.** Real users haven't validated anything yet. Ship straight to main, revert with git.
- **Don't write abstraction layers over a single use case.** "Repository pattern" over Mongoose, "Service layer" over a single Route Handler — premature. Three similar lines beats a premature abstraction.
- **Don't mock third-party APIs in integration tests.** Run them against real test accounts (Stripe test mode, a Resend sandbox domain, a MongoDB Atlas test cluster), because a mock passes while production fails. In-memory fakes of your own infrastructure (`mongodb-memory-server`, an in-memory KV) are fine for the hermetic unit and handler suite (§15).
- **Don't take a dependency release the hour it ships.** Keep the package manager's release-age cooldown on, and hold the pinned exceptions until their blockers close (§2).
- **Don't store secrets in `next.config.mjs` or anywhere bundled.** Even server-only files — keep secrets in env, not source.
- **Don't add `any` to silence the type checker.** Use `unknown` and narrow, or fix the upstream type. Every `any` is a future bug.
- **Don't skip the `import 'server-only'` line.** It's two seconds. It will save you a `BLOB_READ_WRITE_TOKEN` leak someday.
- **Don't ship features untested and plan a "coverage sweep" later.** Backfilling tests, contracts, a logging facade, and security headers across N apps is a top rework driver — and the sweep keeps finding real production bugs. Scaffold the harness (§15) and test-as-you-go.
- **Don't let a spec's word "CI" auto-summon GitHub Actions.** Decide the gate first (§19). A pipeline scaffolded on reflex, then torn out, is pure churn.
- **Don't cast untrusted input into a type.** `as` and `as unknown as T` are not validation, and a `.loose()` (formerly `.passthrough()`) parse validates only the declared fields while keeping the rest unchecked, so persist only the declared fields. Parse with Zod at every boundary (`res.json()`, webhook bodies, queue messages, pagination cursors). See CODING_PRACTICES §1.
- **Don't bind-mount `node_modules` into a dev container.** The container's install clobbers the host's modules (or symlinks break across OSes). Mount source only; use named module volumes (§21).
- **Don't turn on polling by reflex, and don't expect it to reach Next 16.** Check whether file events reach the container first (§21). Turbopack ignores `WATCHPACK_POLLING`, so a Next dev server that misses events needs `next dev --webpack` or the host.
- **Don't let a bind-mounted parent dir drag heavy *unused* subtrees into the macOS VM.** An isolated island's `node_modules` + native `ios`/`android` build dirs shared into every container can exhaust the host's system-wide `kern.maxfiles` and `ENFILE` *unrelated* apps (native build tools, browsers) — a baffling failure since per-process limits look fine. Mask them with empty anonymous volumes and raise `kern.maxfiles` (§21).
- **Don't route a Storybook / atlas under a sub-path.** Its absolute asset URLs break — give it its own subdomain (§22).
- **Don't hand-edit a generated token file or a built mock HTML.** Edit the source (`tokens.ts`, the `*.jsx`) and re-run the generator/watcher; the drift gate will catch you otherwise (§22).
- **Don't symlink `node_modules` into a worktree.** It satisfies `tsc` but Turbopack `next build` panics, and it skips husky so the pre-push gate silently no-ops. Real `pnpm install` per worktree (§23).
- **Don't ship a fallback that masks a real failure.** Returning canned text / mock data / `null` when the real path errors (`if (!x) return "…generic message…"`) hides the bug and ships a broken feature as "working." Throw with context; if you can't implement it for real, say so and stop — don't paper over it. Mocks live only in tests.
- **Don't let a partial upstream object short-circuit field population.** A resolver/mapper that returns early on "the object exists" silently drops fields a richer source *has* but the partial lacks (a curated summary present, the live metrics null). Merge/backfill from the authoritative source — and gate an expensive backfill behind an "is this field actually requested" (selection-set) check so it doesn't fan out across a list query.
- **Don't `JSON.parse` a response before checking its status.** A failing serverless endpoint returns a non-JSON error page; parsing first throws an opaque error that discards the real HTTP status and (for auth refresh) drives an infinite retry (§9).
- **Don't ship two apps from one codebase under a shared bundle id / URL scheme.** They install over each other, share a keychain/secure-store namespace, and race for the same deep link. Distinct identity per app, changed together (§18).
- **Don't branch on `NODE_ENV` in client code to tell staging from prod** — it's `production` for both. Resolve env-gated behaviour (flags, test affordances, staff gating) on the server (§24).
- **Don't run the whole quality gate on every push regardless of scope.** Path-scope it (fail-safe), or a mobile/docs-only push pays for a full web+api build it can't affect (§19).
- **Don't change one security layer and ship.** Layered failures mask each other — exercise the affected endpoints end-to-end after any sanitisation / auth / RBAC / validation change (§25).

---

## 27. Day-one setup checklist

```
# Decide first (§2, §17, §19) — everything after depends on these
[ ] DECIDE repo shape: single app vs pnpm + Turborepo monorepo (§17) — retrofitting later is expensive
[ ] DECIDE quality gate: hosted CI vs husky pre-push hook, and write it down (§19)
[ ] Package-manager release-age cooldown + the pinned exceptions: TypeScript 6, ESLint 9 (§2)

# Scaffold
[ ] Monorepo only, before scaffolding: pnpm-workspace.yaml + turbo.json + ONE root .gitignore; overrides/allowBuilds/patchedDependencies in the workspace file (§17)
[ ] npx create-next-app@latest --typescript --eslint --app   (Turbopack is the default in 16; --webpack opts out). In a monorepo, run it inside apps/ with --use-pnpm --skip-install --disable-git, then install once at the root
[ ] Pin what the scaffold wrote to the §1 holds: create-next-app 16.4 writes typescript ^5 and @types/node ^20, so set typescript ~6.0 and @types/node ^24 before the first install
[ ] Add `import 'server-only'` package: npm install server-only
[ ] Set up tsconfig path alias @/* → ./* (no baseUrl)
[ ] vercel link
[ ] Provision DB (Mongo Atlas or Neon) via Vercel Marketplace
[ ] Provision Redis (Upstash) via Vercel Marketplace — only if needed
[ ] Copy CODING_PRACTICES.md + NEW_PROJECT_BEST_PRACTICES.md into docs/
[ ] Add DESIGN.md: run the design-md-from-screenshots:design-md-from-screenshots skill against your reference site; where that skill isn't installed, write it by hand from screenshots, following the team-files DESIGN.md's 12 sections (colour, type, spacing, shape, motion, components, accessibility and the rest)
[ ] Copy CLAUDE-STARTER.md → CLAUDE.md (fill every placeholder with verified reality, delete the instruction block) and `ln -s CLAUDE.md AGENTS.md`
[ ] Scaffold the test harness (in-memory Mongo, server-only stub, hermetic vs integration split) BEFORE the first feature (§15)
[ ] Configure static security headers in next.config.mjs and the nonce CSP in proxy.ts (CP §6.7)
[ ] Pick the local domain (`<project>.localhost`), add a root `Caddyfile`, add `/etc/hosts` lines only on macOS before 26, and set app/WebSocket env vars to the Caddy origin

# First features
[ ] Wire Vercel AI SDK + AI Gateway env vars
[ ] Wire Resend + verified sender domain
[ ] Add JWT_SECRET, plus ADMIN_PASSWORD for a single-operator v1 console or ADMIN_JWT_SECRET once admins have their own accounts (openssl rand -base64 32; §9, CP §6.1)
[ ] Set up email-code sign-in flow
[ ] First Playwright test: sign-up → sign-in → first authenticated page
[ ] Open a PR; confirm preview deploy URL works end-to-end

# If multi-app / monorepo / native (see §17–§23):
[ ] Expo/RN app: pnpm's default isolated install + Expo's automatic Metro monorepo config; no hand-written watchFolders (§18)
[ ] Cross-app wire shapes: shared packages/contract OR bidirectional parity tests wired into the gate (CODING_PRACTICES §6.10)
[ ] Native: distinct bundle id / URL scheme / OAuth redirect / deep-link prefix per sibling app; flag the OAuth-callback + push-provider re-registration follow-ups (§18)
[ ] Native: device E2E (Maestro/Detox) covering return paths (back/close/dismiss) + testIDs on entry points and data cells (§18)
[ ] Gate: make the pre-push path-aware — run each app's checks only when it or shared code changed; fail-safe; force-all escape hatch (§19)
[ ] Resolve env-gated behaviour (flags, test affordances, staff visibility) on the server, not the client build; gate internal/test users + non-prod outbound at the data source (§24)

# Local dev environment (see §20–§23):
[ ] One shared machine-wide Caddy on :80; per-repo conf.d/<repo>.caddy mirrors the repo Caddyfile route blocks (strip the global block) (§20)
[ ] docker-compose.dev.yml: one service per app + infra; ports published on 127.0.0.1; MongoDB as a single-node replica set; source bind-mounts only; per-service node_modules + pnpm-store volumes (NEVER bind-mount node_modules) (§21)
[ ] File watching: confirm create/edit/rename/delete events reach the containers; Vite through Caddy gets allowedHosts + server.ws.clientPort = Caddy's port; poll only where §21 says (§21)
[ ] Mount ./patches into every install context; SHELL=/bin/sh on alpine; healthchecks probe 127.0.0.1; keep workspace exclusions in sync after renames (§21)
[ ] Mask heavy unused subtrees nested under a bind mount (isolated-island node_modules, native ios/android) with empty anonymous volumes; raise macOS kern.maxfiles to 524288 for headroom (§21)
[ ] Design tokens: single libs/design-tokens source + tokens:sync / tokens:check drift gate; islands get a generated+committed copy (§22)
[ ] Storybook: HTML-reference ⇄ React-host in 1:1 parity (host composes reference via refs); -atlas subdomains, not /atlas sub-paths (§22)
[ ] Worktrees: real pnpm install (not symlink) via a husky-bootstrapping wrapper; periodic prune of clean+merged worktrees; optional TypeScript 7 tsc for a faster typecheck (§23)
```

If a section here doesn't apply (e.g. no AI features, no admin UI), skip it — but read it once so you know what you're skipping.

---

## Sources (checked 2026-10-18)

Version and behaviour claims were re-verified against the npm registry, the shipped type definitions of the packages named, and these pages. Re-check the relevant entry when you bump a major.

- TypeScript 7.0 and the side-by-side layout: https://devblogs.microsoft.com/typescript/announcing-typescript-7-0 · typescript-eslint and TS 7: https://github.com/typescript-eslint/typescript-eslint/issues/10940 · Nest CLI and TS 7: https://github.com/nestjs/nest-cli/issues/3479 · `next build` type-check: https://nextjs.org/docs/app/api-reference/config/next-config-js/useTypeScriptCli
- Node.js schedule: https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule · Vercel Node versions: https://vercel.com/docs/functions/runtimes/node-js/node-js-versions
- AI SDK 7: https://vercel.com/changelog/ai-sdk-7 · forced tool choice on Opus 5.5 / Sonnet 5.5 / Fable 5.1: the `@ai-sdk/anthropic` 4.0.82 changelog · AI Gateway models: https://ai-gateway.vercel.sh/v1/models
- Package managers: https://pnpm.io/blog/releases/11.0 · https://pnpm.io/blog/releases/12.0 · npm `min-release-age`: https://docs.npmjs.com/cli/v11/using-npm/config
- ESLint 10: https://eslint.org/blog/2026/02/eslint-v10.0.0-released · eslint-config-next and ESLint 10: https://github.com/vercel/next.js/issues/91702
- Vitest 5: https://vitest.dev/blog/vitest-5.html · Vite's polling scope: https://vite.dev/config/server-options
- Mongoose: https://mongoosejs.com/docs/migrating_to_9.html · `strictQuery`: https://mongoosejs.com/docs/tutorials/query_casting.html
- Expo monorepos: https://docs.expo.dev/guides/monorepos
- Vercel: https://vercel.com/docs/functions/limitations · https://vercel.com/docs/vercel-blob/private-storage · https://vercel.com/docs/project-configuration/vercel-ts · https://vercel.com/docs/monorepos/turborepo
- Next.js 16: https://nextjs.org/docs/app/guides/upgrading/version-16 · https://nextjs.org/docs/app/guides/content-security-policy
- Auth.js → Better Auth: https://github.com/nextauthjs/next-auth/discussions/13252 · Redis clients: https://github.com/redis/ioredis
- Local dev: https://caddyserver.com/docs/automatic-https · `*.localhost` on macOS 26: https://bugs.webkit.org/show_bug.cgi?id=160504 · `.local` lookups: https://github.com/Automattic/studio/issues/3655 · VirtioFS events: https://github.com/docker/for-mac/issues/7246 · `launchctl limit` and SIP: https://developer.apple.com/forums/thread/735798
