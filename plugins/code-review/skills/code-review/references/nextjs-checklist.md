# Next.js (App Router) + React 19 Review Checklist

Calibrated to **Next.js 15 / 16** and **React 19**. Versions can differ per package in a workspace,
so read the package's own `package.json` before applying any item that depends on a major
(`verification-loop.md` Gate 2). The Phase 1 repo profile records the installed versions.

Each item gives the rule, what to grep for, the severity if violated, and the fix pattern. A section
that does not apply to the diff reports as `not-applicable` with its structural reason rather than
being dropped silently — `coverage.md` defines the states, and the report prints them.

One item sits above the sections below because it is invisible to every local gate: **a build
config branch keyed on an environment variable takes a different path in CI than on a laptop.** The
recorded case is `output: 'standalone'` gated on `process.env.VERCEL`, because Next 16.3 with
Turbopack skips `collectBuildTraces` and the standalone copy step then fails on the deploy host
only — a diff that ungates it passes every local build and breaks every deploy. Grep the Next config
and the deployment config for `process.env.<CI_VAR>` branches, and check whether the repo's own
pre-push or CI gate exercises the same branch the deploy takes. Where it does not, that is a
`no-oracle` row rather than a clean one.

---

## Contents

- [1. Server Action security](#1-server-action-security)
- [2. RSC vs Client Component boundary](#2-rsc-vs-client-component-boundary)
- [3. Async Runtime APIs (Next.js 15+)](#3-async-runtime-apis-nextjs-15)
- [4. Caching semantics (Next.js 15+)](#4-caching-semantics-nextjs-15)
- [5. React 19 hook migration](#5-react-19-hook-migration)
- [6. Hydration mismatch heuristics](#6-hydration-mismatch-heuristics)
- [7. `next/image` and `next/link`](#7-nextimage-and-nextlink)
- [8. Route Handler security (`route.ts`)](#8-route-handler-security-routets)
- [9. Middleware / Proxy](#9-middleware-proxy)
- [10. Cross-cutting Next.js conventions (low-priority — only flag in egregious cases)](#10-cross-cutting-nextjs-conventions-low-priority-only-flag-in-egregious-cases)
- [Sources](#sources)

## 1. Server Action security

The single highest-value review area in App Router projects. Server Actions (`'use server'` functions) are reachable as **direct POST endpoints**, not just from the UI that imports them. The Next.js docs explicitly state: *"Server Functions are reachable via direct POST requests, not just through your application's UI. Always verify authentication and authorization inside every Server Function."*

Two automatic defenses Next.js gives you (don't double-flag what's already covered):

- **Origin/Host CSRF check** — Next.js automatically rejects Server Action POSTs whose `Origin` header doesn't match the `Host` (or `X-Forwarded-Host`). A manual CSRF token adds nothing on that path. **However**, behind a reverse proxy or CDN that rewrites Host, the check needs `experimental.serverActions.allowedOrigins` set in `next.config.js`, and its absence there is the finding (see §1.7).
- **Action ID encryption** — closed-over variables in Server Actions are encrypted by Next.js when sent to the client and back. Per the docs: *"We don't recommend relying on encryption alone to prevent sensitive values from being exposed on the client."* Don't capture secrets in action closures even though they're encrypted (see §1.8).

### 1.1 Missing authentication inside the action — `CRITICAL` if user data, `HIGH` otherwise

Look for: any function in a file marked `'use server'` (file-level) or any function that has `'use server'` as its first statement. The function must verify a session at its top.

Bad:
```ts
'use server'
export async function deletePost(postId: string) {
  await db.post.delete({ where: { id: postId } })  // no auth check
}
```

Good (note: directives like `'use server'` must come before any imports per the React/Next compiler):
```ts
'use server'
import 'server-only'
import { auth } from '@/lib/auth'

export async function deletePost(postId: string) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')
  // ...
}
```

### 1.2 Missing authorization (IDOR) — `CRITICAL`

Even with authentication, the action must check that the *current user owns or has permission to act on the resource*. The Next.js docs warn: *"Beyond authentication (is the user logged in?), remember to check authorization (does this user have permission to act on this specific resource?). This prevents IDOR vulnerabilities."*

Bad:
```ts
const session = await auth()
if (!session?.user) throw new Error('Unauthorized')
await db.post.delete({ where: { id: postId } })  // any logged-in user can delete any post
```

Good:
```ts
const post = await db.post.findUnique({ where: { id: postId } })
if (!post || post.authorId !== session.user.id) throw new Error('Forbidden')
await db.post.delete({ where: { id: postId } })
```

### 1.3 Missing input validation — `HIGH`

Server Actions receive `FormData` or arbitrary serializable arguments from any caller. Validate with Zod (or `zod-form-data`).

Bad:
```ts
export async function createUser(formData: FormData) {
  const email = formData.get('email') as string  // unvalidated
  await db.user.create({ data: { email } })
}
```

Good:
```ts
import { z } from 'zod'
const schema = z.object({ email: z.string().email(), name: z.string().min(2).max(50) })

export async function createUser(formData: FormData) {
  const parsed = schema.safeParse(Object.fromEntries(formData))
  if (!parsed.success) return { error: parsed.error.format() }
  await db.user.create({ data: parsed.data })
}
```

For forms with multi-value fields (multi-select, multiple file upload, repeated checkbox names), `Object.fromEntries(formData)` collapses to the last value and silently loses data. Use `zod-form-data` (which preserves repeats) for any non-trivial form.

### 1.4 Missing `import 'server-only'` on files containing secrets — `HIGH`

If a file accesses `process.env.<SECRET>`, reads from the database, or uses any backend-only library, it must `import 'server-only'` at the top. This causes the bundler to throw a compile-time error if the file is ever imported into a Client Component, preventing the secret from being shipped to the browser.

The Next.js docs recommend a Data Access Layer pattern: secrets and DB access live in `data/*.ts` files marked `'server-only'`; Server Actions are thin wrappers that call DAL functions.

### 1.5 Returning raw database records — `MEDIUM`

Server Action return values are serialized and sent to the client. Returning the whole user record (with `passwordHash`, `apiKeyEncrypted`, etc.) leaks data even if the UI doesn't render those fields. Pick the fields the UI needs.

### 1.6 Mutations during render — `HIGH`

Mutations (logging users out, updating DBs, invalidating caches) **must not** be a side-effect of rendering. They belong in Server Actions invoked by user gestures or by Route Handlers invoked by webhooks. Flag any DB write or `revalidateTag` / `revalidatePath` call inside a Server Component's render path.

### 1.7 Reverse-proxy / origin mismatch — `MEDIUM`

If the project is deployed behind a reverse proxy or CDN that rewrites the `Host` header (Vercel-with-custom-domain, Cloudflare, an internal nginx), Next.js's automatic CSRF Origin/Host check will reject every Server Action POST unless `allowedOrigins` is configured. The exact shape (verify in the file by grepping for `allowedOrigins`):

```js
// next.config.js
module.exports = {
  experimental: {
    serverActions: {
      allowedOrigins: ['app.example.com', '*.preview.example.com'],
    },
  },
}
```

Flag if the repo's deployment context implies a proxy and `experimental.serverActions.allowedOrigins` is missing or empty.

### 1.8 Secret captured in Server Action closure — `MEDIUM`

Per the Next.js data-security guide: *"We don't recommend relying on encryption alone to prevent sensitive values from being exposed on the client."* Even though Next.js encrypts closed-over variables sent to the client and back, don't write code that captures DB connection strings, signing keys, third-party API tokens, or other secrets in the closure of a Server Action. Read the secret inside the action body instead.

---

## 2. RSC vs Client Component boundary

### 2.1 Browser-only API in a Server Component — `HIGH` (guaranteed crash)

Server Components run in Node, where `window`, `document`, `localStorage`, `sessionStorage`, `navigator`, and DOM APIs do not exist. Flag any actual JS access to these in a file that is NOT marked `'use client'`. (Don't false-fire on string literals containing the word `document.cookie` inside a CSP policy / docs comment / sample string — only flag real property access.)

Common offenders:
- `window.matchMedia(...)`
- `localStorage.getItem(...)`
- `document.cookie`
- `navigator.language` / `navigator.userAgent`

Fix: mark the file `'use client'`, OR move the access into a `useEffect`, OR isolate the widget with `dynamic(() => import('./Widget'), { ssr: false })`.

### 2.2 Non-deterministic value during render — `HIGH` (hydration mismatch)

`Date.now()`, `new Date()` (without explicit ISO conversion that's stable), `Math.random()`, `crypto.randomUUID()`, and locale-dependent `toLocaleString()` calls during render guarantee a hydration mismatch in any code path that renders both on server and on client.

Fix patterns:
- Pass a stable timestamp from the server as a prop.
- Compute the volatile value inside a `useEffect` after hydration.
- Wrap the widget in `dynamic({ ssr: false })`.

### 2.3 Non-serializable prop crossing the boundary — `HIGH`

Props passed from a Server Component to a Client Component must be serializable: no functions, class instances, Symbols, Maps/Sets in many cases, no Promises (unless you `use()` them inside the Client Component). Plain objects, arrays, strings, numbers, booleans, `Date` (serialized as string), and `null`/`undefined` are fine.

### 2.4 Reading secrets from a Client Component file — `CRITICAL`

If a file is marked `'use client'` (or transitively imported by one) and references `process.env.<NON_NEXT_PUBLIC_*>`, the Next.js bundler replaces the value with `''` in the client bundle. The bigger risk: the file may import from `'@/lib/db'` or another secret-bearing module, pulling the whole module into the client bundle. The fix is `import 'server-only'` at the top of the secret-bearing file (catches this at build time).

### 2.5 React Context provider in a Server Component — `MEDIUM`

`<MyContext.Provider>` only works in Client Components. If a Server Component renders a provider directly, wrap the provider in a Client Component (`'use client'` at the top, accepts `children`) and render that wrapper from the Server Component.

---

## 3. Async Runtime APIs (Next.js 15+)

### 3.1 Synchronous `cookies()` / `headers()` / `params` / `searchParams` — `HIGH` on Next.js 15+

In Next.js 15+, these APIs are async. Synchronous use is deprecated and prints warnings; future versions will throw.

Bad:
```ts
const c = cookies().get('session')
const lang = headers().get('accept-language')
const id = params.id
```

Good:
```ts
const cookieStore = await cookies()
const c = cookieStore.get('session')

const headersList = await headers()
const lang = headersList.get('accept-language')

const { id } = await props.params
```

### 3.2 `cookies().set()` outside Server Function / Route Handler — `HIGH`

Setting or deleting cookies is only valid inside a Server Action or a Route Handler. Setting cookies during a Server Component render throws (HTTP doesn't allow setting cookies after streaming starts).

### 3.3 Dynamic-rendering opt-in — informational

A route opts into dynamic rendering whenever any of the following is read during render: `cookies()`, `headers()`, `draftMode()`, `searchParams`, `noStore()`, `connection()`, an uncached `fetch(...)` (no `cache: 'force-cache'`), or `unstable_noStore()`. Not a finding by itself, but worth a `MEDIUM` flag if a route was previously cached/static and the diff just added one of these without the developer realizing they've disabled caching for the whole route segment.

---

## 4. Caching semantics (Next.js 15+)

### 4.1 Stale-cache assumption — `MEDIUM`

In Next.js 15, the default for `fetch()` is **no longer cached**. If the diff added a `fetch()` call that the developer assumed was cached (no `{ cache: 'force-cache' }`, no `next.revalidate`, no `next.tags`), every request hits the upstream.

Fix:
```ts
fetch(url, { cache: 'force-cache', next: { revalidate: 600, tags: ['posts'] } })
```

### 4.2 `revalidatePath` / `revalidateTag` outside Server Function or Route Handler — `HIGH`

These must be called inside a Server Action or Route Handler. Calling them during a Server Component render is a no-op at best, an error at worst.

### 4.3 Non-statically-analyzable `revalidate` value — `MEDIUM`

The `revalidate` route segment must be a literal:
- `export const revalidate = 600` ✓
- `export const revalidate = 60 * 10` ✗ (Next.js cannot statically analyze)

### 4.4 `unstable_cache` with implicit closure dependencies — `HIGH`

(Note: `unstable_cache` is being phased out in favor of the `'use cache'` directive / Cache Components in newer Next.js canary releases. If the project is on canary, recommend the new model. The closure-key bug below applies to both.)


`unstable_cache` keys on the explicit `keyParts` array, not on closure variables. If the wrapped function reads `cookies()`, `headers()`, or `auth()` from its enclosing scope without those values being part of the key, the cache will return cross-user data.

Bad:
```ts
const getUserPosts = unstable_cache(
  async () => {
    const session = await auth()
    return db.post.findMany({ where: { authorId: session.user.id } })
  },
  ['user-posts'],   // session.user.id is not in the key — cross-user cache leak
  { revalidate: 60 }
)
```

### 4.5 `dynamic = 'force-dynamic'` plus `cache: 'force-cache'` — `MEDIUM`

The two contradict each other. Flag the inconsistency and ask the developer which behavior they actually want.

---

## 5. React 19 hook migration

### 5.1 `useFormState` instead of `useActionState` — `HIGH` on React 19+

`useFormState` (from `react-dom`) is deprecated; `useActionState` (from `react`) is the replacement, with a slightly different return tuple `[state, dispatch, isPending]`.

### 5.2 `useFormStatus` called outside a `<form>` — `HIGH`

`useFormStatus` only returns the parent form's status. Calling it from a component not rendered inside a `<form>` always returns `pending: false`. Common bug: developer puts it in the same component that renders the `<form>`, and it silently never shows pending state.

### 5.3 `useOptimistic` outside a transition — `MEDIUM`

`useOptimistic`'s state revert behavior depends on being called inside a Transition (which `<form action={...}>` provides automatically). Outside a transition, React warns and the optimistic state behaves unpredictably.

### 5.4 Unnecessary `forwardRef` — `LOW`

In React 19, `ref` is a regular prop on function components. New code wrapping a component in `forwardRef` purely to receive a `ref` prop is obsolete. (Existing code: don't flag — refactor isn't free.)

### 5.5 Async transitions with stale state — `MEDIUM`

`startTransition(async () => { ... })` is supported in React 19, but state read inside the async callback after `await` may be stale. Flag if a long-running async callback reads `useState` values after `await` without snapshotting them first.

---

## 6. Hydration mismatch heuristics

In addition to the items in §2.2, flag:

- Conditionally rendering based on `typeof window !== 'undefined'` in render. The server renders the falsy branch; the client renders the truthy branch. Always mismatches.
- `useState` initializer that reads from `localStorage` / `sessionStorage` / `document` — e.g. `useState(() => localStorage.getItem('theme'))`. The SSR pass returns the initial-server value; the client mount returns the storage value, mismatching on every reload. Move the storage read into a `useEffect` that runs after mount and `setState`s.
- Browser auto-detection (phone numbers, dates) on iOS Safari rewriting markup. Mitigation: `<meta name="format-detection" content="telephone=no, date=no, email=no, address=no" />`.
- Incorrect HTML nesting that the React reconciler will silently rewrite: `<p>` inside `<p>`, `<div>` inside `<p>`, `<a>` inside `<a>`, `<button>` inside `<button>`.
- CSS-in-JS without an SSR-aware setup (styled-components / emotion without the proper Next.js integration).
- `suppressHydrationWarning` used as a blanket fix for a real mismatch — `MEDIUM`. The prop is a one-level escape hatch for genuinely unavoidable mismatches (e.g. timestamps that the server can't pre-compute). Using it to silence a fixable `localStorage`/`Date.now()`/`window` mismatch papers over the bug; flag any new usage and ask the developer to justify it.

---

## 7. `next/image` and `next/link`

### 7.1 `next/image` missing `alt` — `MEDIUM` (accessibility) or `LOW` if decorative

Required prop. For decorative images use `alt=""` explicitly.

### 7.2 `next/image` missing `width`/`height` (or `fill`) — `HIGH`

Causes layout shift and CLS regression. Fix by supplying both dimensions or `fill` with a sized parent.

### 7.3 `next/image` missing `sizes` when `fill` — `MEDIUM`

Without `sizes`, the optimizer requests the largest variant and wastes bandwidth.

### 7.4 External `src` not in `images.remotePatterns` — `HIGH` (build error)

Will fail the build. If `next.config.js` doesn't list the host, the diff is broken.

### 7.5 `<a>` for internal navigation instead of `<Link>` — `MEDIUM`

Loses prefetching and client-side navigation. (Don't flag for `mailto:`, `tel:`, or external links.)

### 7.6 `<Link target="_blank">` without `rel="noopener noreferrer"` — `MEDIUM`

Standard web security hygiene.

---

## 8. Route Handler security (`route.ts`)

### 8.1 Missing authn/authz on a state-mutating handler — `CRITICAL`

`POST` / `PUT` / `PATCH` / `DELETE` handlers without an explicit session check are public-write endpoints.

### 8.2 No CSRF protection on a state-mutating handler — `HIGH`

Route Handlers do **not** have built-in CSRF protection (only Server Actions do). For state-mutating handlers, either:
- Require a custom header that browsers won't auto-attach cross-origin (e.g., `X-Request-Source: web`).
- Use double-submit cookies.
- Compare `Origin` to `Host`.

### 8.3 Unawaited `context.params` — `HIGH` on Next.js 15+

```ts
export async function GET(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params  // not synchronous
}
```

### 8.4 `request.formData()` parsed without validation — `HIGH`

Same rule as Server Actions — validate with Zod / `zod-form-data` before using.

### 8.5 Cookies set without `httpOnly` / `secure` / `sameSite` — `HIGH` for session cookies

```ts
response.cookies.set('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 60 * 60 * 24 * 7,
  path: '/',
})
```

### 8.6 Webhook handler without signature verification — `CRITICAL`

Stripe / GitHub / Slack webhook endpoints must verify the signature header before doing anything else. Flag any webhook handler that uses the body before calling the provider's `verify` function.

### 8.7 Missing rate limiting on sensitive endpoints — `MEDIUM`

Auth endpoints, password reset endpoints, and email-sending endpoints should have rate limiting. (Don't flag this for every public endpoint — only for the ones where abuse has obvious cost.)

---

## 9. Middleware / Proxy

### 9.1 `middleware.ts` on Next.js 16+ — `MEDIUM`

The convention was renamed `proxy.ts` in v16. Flag if `middleware.ts` exists in a project that pins Next.js ≥ 16. Codemod available: `npx @next/codemod@canary middleware-to-proxy .`

### 9.2 Auth check in proxy without a corresponding action-level check — `HIGH`

The Next.js docs explicitly warn: *"A matcher change or a refactor that moves a Server Function to a different route can silently remove Proxy coverage. Always verify authentication and authorization inside each Server Function rather than relying on Proxy alone."* Proxy is defense in depth, not the primary check.

### 9.3 Proxy `matcher` using a non-static value — `HIGH`

The `matcher` config must be statically analyzable at build time. Variables and dynamic concatenation are silently ignored.

### 9.4 Setting upstream request headers via `NextResponse.next({ headers })` — `HIGH`

That sets *response* headers. To set headers on the *forwarded request*, use `NextResponse.next({ request: { headers: newHeaders } })`.

### 9.5 Edge-runtime-incompatible code in a proxy — `HIGH` if pinned to edge

If the proxy explicitly opts into the edge runtime, flag use of `fs`, `child_process`, `crypto.randomBytes`, native deps, or files >1 MB compiled.

### 9.6 Large headers set in proxy — `MEDIUM`

Causes 431 Request Header Fields Too Large at the CDN.


### 9.7 A response header configured in `next.config` that the framework overwrites — `HIGH` when it is cache-correctness

`headers()` in `next.config.ts` does **not** compose with the `Vary` value Next sets on app-router
responses. Next *overwrites* it with its own router list rather than appending, and the configured
value is lost:

```
configured  Vary: Host
served      vary: rsc, next-router-state-tree, next-router-prefetch, next-router-segment-prefetch
```

It reproduces on a plain local `next start`, so it is not a CDN behaviour and no edge configuration
fixes it. Where a response varies by something the router list does not name, a shared cache keyed on
path alone may serve one variant under another key.

**Middleware does not fix it either, and that is the load-bearing half.** The mechanism is one line
in Next's own app-page entry:

```js
const varyHeader = routeModule.getVaryHeader(resolvedPathname, interceptionRoutePatterns);
res.setHeader('Vary', varyHeader);      // SET, not append
```

`getVaryHeader` returns a hard-coded list and takes no configuration, and it runs when the page
handler is invoked — **after both** places a Next app normally sets a response header: the route
table, where `next.config.ts`'s `headers()` lands, and the middleware or proxy header set. Measured:
a proxy that appends `Vary: Host` *and* sets `x-probe: yes` produces a page response carrying
`x-probe` and no `Host`. Middleware runs, its headers arrive, and `Vary` alone is lost. A fix has to
run in-process before any request is served and therefore after that `setHeader` —
`instrumentation.ts` on current Next — and it must **merge** rather than replace, because the RSC
entries are load-bearing for Next's own router cache.

Three things a fix must get right, each of which reads green while broken:

- **Validate it on a PAGE route.** Route Handlers take a different send path and *do* keep the
  configured header, so a fix verified on `/api/…` looks correct and ships broken on every page.
- **Assert the existing tokens survive** and that none is duplicated — a fix that replaced the list
  passes "contains Host" and breaks client-side navigation.
- **Exclude `/_next/static`.** Those files are content-hashed and byte-identical under every key, so
  varying them multiplies their CDN cache and protects nothing.

And **delete the config entry that never arrived**, with the reason in its place. A header that is
declared and provably never served is worse than no header: it reads to every subsequent reviewer as
a satisfied constraint.

Two cheap review moves. **Read the served header off the socket, never the config** — a header that
is set and dropped is invisible in source and obvious in one `curl -I`. And any test for this boots
the built server and reads the response, because reading the config is exactly what proved nothing.
This is Gate 6 in `verification-loop.md`: a claim about runtime behaviour names the observation
behind it.

The general shape, worth flagging beyond `Vary`: any response header the framework also manages —
`Cache-Control`, `Content-Security-Policy`, `Link` — set declaratively in config and assumed to
survive.

---

## 10. Cross-cutting Next.js conventions (low-priority — only flag in egregious cases)

- `'use client'` at the top of files that don't actually need client-side reactivity (defeats RSC bundle savings).
- Massive client-side state when `nuqs` URL state would suffice for sharable filters/search.
- Missing `loading.js` / `error.js` boundaries for routes that do async data fetching (no fallback UI on slow networks).
- `next.config.js` setting `experimental.serverActions = true` when the project is already on Next.js 15+ (the flag is a no-op).

---

## Sources

- Next.js — [Mutating Data (Server Actions)](https://nextjs.org/docs/app/getting-started/mutating-data)
- Next.js — [Data Security guide](https://nextjs.org/docs/app/guides/data-security)
- Next.js — [`cookies()`](https://nextjs.org/docs/app/api-reference/functions/cookies), [`headers()`](https://nextjs.org/docs/app/api-reference/functions/headers)
- Next.js — [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- Next.js — [Caching (without Cache Components)](https://nextjs.org/docs/app/guides/caching-without-cache-components)
- Next.js — [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route)
- Next.js — [Proxy (formerly Middleware)](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
- Next.js — [Hydration error message](https://nextjs.org/docs/messages/react-hydration-error)
- React 19 — [`useActionState`](https://react.dev/reference/react/useActionState), [`useFormStatus`](https://react.dev/reference/react-dom/hooks/useFormStatus), [`useOptimistic`](https://react.dev/reference/react/useOptimistic)
- PatrickJS — [nextjs15-react19-vercelai-tailwind cursor rules](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/nextjs15-react19-vercelai-tailwind-cursorrules-prompt-file/.cursorrules)
- Turbostarter — [Next.js Security Guide 2025](https://www.turbostarter.dev/blog/complete-nextjs-security-guide-2025-authentication-api-protection-and-best-practices)
