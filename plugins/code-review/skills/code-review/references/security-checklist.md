# Security Checklist (OWASP-aligned)

Loaded when the diff touches authentication, sessions, cookies, JWT, password handling, env vars, SQL/ORM queries with user input, file uploads, deserialization, redirects, public POST endpoints, headers, CSP, or CORS.

Most items are **CRITICAL** or **HIGH** by default — security findings have asymmetric cost (a missed CRITICAL can be a CVE; a false positive costs the developer 30 seconds). When in doubt, lean toward flagging on this checklist (still respecting the >85% confidence rule).

Items are organized by OWASP Top 10:2021 category, with per-framework overlays — Next.js App Router, NestJS, and the SQL and document data layers. **Run only the overlay rows for the frameworks the Phase 1 repo profile says are present**, and record the rest as `not-applicable` with that structural reason rather than dropping them silently.

The absences matter as much as the presences here, because this checklist pattern-matches on shape and shapes recur across stacks. A finding proposing a NestJS guard in a repo with no `@nestjs/*` dependency, or a Prisma call in a repo with no Prisma, is refuted at Gate 1 — the fix cannot be applied. That refutation only fires if the profile carried the absence into the verifier prompt, so establish it in discovery.

---

## Contents

- [A01:2021 — Broken Access Control](#a012021-broken-access-control)
- [A02:2021 — Cryptographic Failures](#a022021-cryptographic-failures)
- [A03:2021 — Injection](#a032021-injection)
- [A04:2021 — Insecure Design](#a042021-insecure-design)
- [A05:2021 — Security Misconfiguration](#a052021-security-misconfiguration)
- [A06:2021 — Vulnerable and Outdated Components](#a062021-vulnerable-and-outdated-components)
- [A07:2021 — Identification and Authentication Failures](#a072021-identification-and-authentication-failures)
- [A08:2021 — Software and Data Integrity Failures](#a082021-software-and-data-integrity-failures)
- [A09:2021 — Security Logging and Monitoring Failures](#a092021-security-logging-and-monitoring-failures)
- [A10:2021 — Server-Side Request Forgery (SSRF)](#a102021-server-side-request-forgery-ssrf)
- [Cross-cutting items](#cross-cutting-items)
- [Sources](#sources)

## A01:2021 — Broken Access Control

### A01.1 Missing authorization on a state-mutating operation — `CRITICAL`

The endpoint authenticates the user (knows *who*) but doesn't check authorization (whether *this user* may act on *this resource*). Insecure Direct Object Reference (IDOR).

Look for: any `db.X.update/delete/findUnique({ where: { id: input.id } })` where `id` came from the request and ownership of the row is not verified before the operation.

```ts
// Required pattern:
const row = await db.x.findUnique({ where: { id: input.id } })
if (!row || row.ownerId !== session.user.id) throw new ForbiddenException()
```

### A01.2 Missing authentication on a state-mutating endpoint — `CRITICAL`

Public-write endpoints. Server Actions, Route Handlers and NestJS controller methods all default to *no* auth — an explicit check must exist. Where the repo documents a required preamble for a mutating public request (typically an origin or CSRF check, a rate limit, a validated body, then handler logic), that order is the rule and a handler skipping a step is the finding; the Phase 1 profile records it.

### A01.3 Authorization in middleware/proxy as the *only* check — `HIGH`

Per the Next.js docs: *"A matcher change or a refactor that moves a Server Function to a different route can silently remove Proxy coverage. Always verify authentication and authorization inside each Server Function rather than relying on Proxy alone."* The same holds in NestJS, where a global guard can be bypassed by a `@Public()` decorator applied at controller level. Belt and braces: the middleware check is defence in depth, and the handler's own check is the control.

### A01.4 Auth not deny-by-default — `HIGH`

Where the codebase opts routes *into* auth one handler at a time (`@UseGuards(JwtAuthGuard)` per controller, an `await requireSession()` per handler), one missed call leaves an open route. Prefer a shared wrapper or a global guard that authenticates by default with an explicit opt-out for the rare public route, so the failure mode of forgetting is a closed route rather than an open one.

### A01.5 Unrestricted file upload — `HIGH`

File upload handlers must constrain: MIME type, file size, file extension, scan-for-virus if user-facing. Additionally: **never use the client-supplied filename for the on-disk path** — sanitize, or rename to a server-generated UUID. A path like `../../../etc/passwd` in `req.file.originalname` followed by `fs.writeFile(path.join(uploadDir, originalname), ...)` is path traversal and can overwrite arbitrary files the process can write.

### A01.7 Mass assignment / over-posting — `HIGH` (often `CRITICAL`)

Passing the entire parsed body straight into a model write lets the attacker set fields they're not supposed to control:

```ts
// BAD — the attacker sets role: 'admin', moderation.status: 'visible', isDummy: false
await User.updateOne({ _id: id }, await request.json())

// BAD — same problem
Object.assign(user, body); await user.save()
```

Required pattern: an explicit allowlist of mutable fields — a strict schema naming exactly them
(`z.object({…}).strict()`, a `class-validator` DTO behind `ValidationPipe({ whitelist: true,
forbidNonWhitelisted: true })`, a `pick`/`omit` projection at the ORM layer) — then a write built
from the parsed result. Strict rather than the permissive default, so an unexpected key is rejected
rather than silently dropped and re-added by a later refactor. Severity is `CRITICAL` when an
over-postable field is privilege-bearing — a role, an admin flag, a tenant id, a moderation status,
or a seed-data marker.

### A01.6 Open redirect — `HIGH` (or `CRITICAL` post-auth)

Redirecting to a destination URL pulled directly from the request (e.g. `Response.redirect(searchParams.get('next'))`) lets an attacker bounce through your domain to a malicious one. Allowlist redirect targets or restrict to relative paths.

Severity escalates to `CRITICAL` when the redirect happens **after** authentication or as part of an OAuth callback — those flows can leak the OAuth code/token via the malicious redirect target and lead directly to account takeover. Pre-auth open redirects are `HIGH`.

---

## A02:2021 — Cryptographic Failures

### A02.1 Plain-text password storage — `CRITICAL`

Entity has `password` not `passwordHash`. Must hash with **argon2id (preferred)** or bcrypt with a current cost factor.

### A02.2 Weak password hashing parameters — `HIGH`

- `md5`, `sha1`, `sha256` are general-purpose hashes, **not password hashes**. They're trivially crackable at modern GPU speeds.
- bcrypt: cost factor `≥ 12` (current OWASP guidance; 10 is the historical floor and is now insufficient on commodity GPUs). Bump to 13–14 if the auth latency budget allows.
- argon2: prefer the `argon2id` variant, and check `memoryCost`, `timeCost` and `parallelism` are set explicitly rather than left at the `node-argon2` defaults — quote the three values in the finding and compare them against the current OWASP cheat sheet.
- `crypto.scrypt`: acceptable but only with explicit `cost`/`blockSize`/`parallelization` parameters; default Node config is too weak for password hashing.

### A02.3 Predictable token generation — `HIGH`

`Math.random()` for password reset tokens, session IDs, or invite codes. Use `crypto.randomBytes(32).toString('hex')` or `crypto.randomUUID()`.

### A02.4 JWT signed with `none` algorithm — `CRITICAL`

`algorithm: 'none'` in JWT signing options — never permitted. Reject in code review on sight.

### A02.4b JWT algorithm confusion (HS256 / RS256 key confusion) — `HIGH`

If the verifier is asymmetric (RS256/ES256) but doesn't pin `algorithms` on `jwt.verify`, an attacker can sign a token with HS256 using the *public key* as the HMAC secret, and the verifier will accept it (because it'll try HS256 with the public key as the key). Always pin:

```ts
jwt.verify(token, publicKey, { algorithms: ['RS256'] })
```

Pin the algorithm on both sign and verify wherever the repo mints or checks a token, including any
JWKS verification path — a verifier that accepts whatever the token's header claims is the defect.
On `@nestjs/jwt`, that means both `signOptions.algorithm` and `verifyOptions.algorithms`:

```ts
JwtModule.register({
  publicKey, privateKey,
  signOptions: { algorithm: 'RS256' },
  verifyOptions: { algorithms: ['RS256'] },
})
```

### A02.5 JWT secret committed to source — `CRITICAL`

A literal secret in code — `{ secret: 'shh-is-secret' }`. Read it from the environment through the repo's own config accessor (`process.env`, a `ConfigService`, a settings object), keep the reading module off the client bundle (`import 'server-only'` or the framework's equivalent), and rotate the key — a committed secret is burned even after the line is deleted.

### A02.6 JWT with no `expiresIn` — `HIGH`

Missing `signOptions.expiresIn` = tokens never expire. 60m–24h is typical for access tokens.

### A02.7 Symmetric algorithm where asymmetric is needed — `MEDIUM`

If multiple services verify the JWT but only one signs it, RS256/ES256 is correct; HS256 means the verification service must hold the signing secret.

### A02.8 Cookies without `httpOnly`, `secure`, `sameSite` — `HIGH` for session cookies

```ts
res.cookies.set('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 60 * 60 * 24 * 7,
  path: '/',
})
```

### A02.9 `secure: false` in cookies / cookie config — `CRITICAL` in production

OK in dev. Flag any literal `secure: false`. Recommend gating on `NODE_ENV === 'production'`.

### A02.10 Secret in client bundle — `CRITICAL`

Any `process.env.<NON_NEXT_PUBLIC_*>` referenced from a `'use client'` file (or transitively imported by one) leaks. Fix with `import 'server-only'` at the top of the secret-bearing file.

### A02.11 Non-constant-time comparison of secret material — `HIGH`

`if (token === expectedToken)` (or `===` on password reset codes, API keys, hand-rolled webhook signatures) is timing-attack-vulnerable in principle. Real-world exploitability is debated, but the fix is one line:

```ts
import { timingSafeEqual } from 'node:crypto'
if (a.length !== b.length) return false
if (!timingSafeEqual(Buffer.from(a), Buffer.from(b))) return false
```

Required for: API key validation, password reset / email verification token comparison, hand-rolled HMAC signature verification, MFA code comparison.

---

## A03:2021 — Injection

### A03.1 Raw SQL with template-literal interpolation — `CRITICAL`

Building a SQL string with `${userId}` interpolated into the query body is SQL injection. Always use
parameter binding:

```ts
queryRunner.query('SELECT * FROM users WHERE id = $1', [userId])
```

In a repo with no SQL database this item is `not-applicable` and reports as such rather than as
clean — and it bites the moment a diff introduces one: an analytics warehouse client, a `postgres`
or `mysql2` dependency, a raw driver behind a reporting endpoint.

### A03.2 An ORM's raw escape hatch carrying user input — `CRITICAL`

Every ORM ships one, and its name is usually the tell. Prisma's `$queryRawUnsafe(sql)` is unsafe by
name, while `$queryRaw` (the tagged template) binds parameters safely. Drizzle's `sql.raw()`,
TypeORM's `query()`, Sequelize's `literal()` and Knex's `whereRaw()` are the same shape. Flag any of
them carrying a value that reached the process from outside it.

### A03.2b A document-store aggregation stage built from user input — `CRITICAL`

The NoSQL counterpart. In MongoDB, `$expr`, `$where`, `$function` and `$accumulator` execute
expressions server-side. A pipeline stage assembled from request data — a sort key, a projection, a
`$match` object — lets a caller reshape the query. Build the stage from a closed set of allowed
values, never from the parsed body directly.

### A03.3 NoSQL injection (Mongo-style operators) — `HIGH`

Passing the parsed body of a request as a Mongo `where` filter (e.g. `db.collection.find({ user: req.body.user })`) lets an attacker substitute `{ $ne: null }` and match every row. Strip `$`-prefixed keys from user input or validate with a strict schema before constructing the filter.

### A03.4 Shell command built from user input via `child_process` — `CRITICAL`

Invoking `child_process.exec` (or `execSync`) with a command string that interpolates user input executes the user's input through `/bin/sh`. Use `execFile` / `execFileSync` (no shell) and pass arguments as an array — the OS will not interpret metacharacters.

### A03.5 LDAP / XPath / other query languages with concatenation — `HIGH`

Same family as A03.1 — never concatenate user input into a query string.

### A03.6 Unescaped HTML rendered via `dangerouslySetInnerHTML` — `HIGH`

If `dangerouslySetInnerHTML={{ __html: userBio }}` and `userBio` is not sanitized (e.g., DOMPurify), it's stored XSS.

### A03.7 Unsafe URL `javascript:` schemes — `HIGH`

Rendering a user-controlled string as the `href` of an `<a>` allows `javascript:alert(1)` and similar XSS vectors. Validate URL schemes (`http`, `https`, `mailto`, `tel`) before rendering.

### A03.8 Prototype pollution — `HIGH`

Recursive merges (`_.merge`, `_.set`, `_.defaultsDeep` from lodash, `deepmerge`, `Object.assign` chains in a recursive helper, `JSON.parse` of attacker-controlled JSON) applied to user input can set `__proto__`, `constructor`, or `prototype` on intermediate objects, polluting `Object.prototype` for the entire process. Symptoms: random properties appearing on every object, auth bypass via `isAdmin: true` showing up on objects created later.

Fix: use `Object.create(null)` for the merge target, freeze the prototype chain, or use a merge library that explicitly rejects `__proto__` keys (lodash ≥ 4.17.5 mitigated some of these; `safe-stable-stringify` and `defu` are safer alternatives).

---

## A04:2021 — Insecure Design

### A04.1 Missing rate limiting on auth/reset/email endpoints — `HIGH`

Login, password reset, code issuance, MFA, invite and email-sending endpoints need rate limiting — `@nestjs/throttler`, a KV-backed limiter, or the platform's own. The rule extends to **every** mutating or expensive route: POST, PUT and DELETE, reports, search, token issuance, including the DELETE counterpart of any throttled PUT. Key by user id on authenticated endpoints, optionally plus IP; reserve IP-only for unauthenticated routes. Never use a raw token or its prefix as the key — hash it. A published starting point is 5 requests per 15 minutes for auth and 100 per 15 minutes for general routes; where the repo's own practices document sets figures, those win.

### A04.2 No account lockout after N failed logins — `MEDIUM`

Either lockout, exponential backoff, or CAPTCHA after repeated failures.

### A04.3 Generic 500 leaks stack trace to client — `MEDIUM`

In production a handler should not return a raw error message or a stack trace. Return a stable error code and log the detail server-side. A `catch` that spreads the caught error into the JSON response is the shape to grep for. NestJS handles this correctly by default for `HttpException`; a custom exception filter can still leak.

---

## A05:2021 — Security Misconfiguration

### A05.1 Missing security headers — `MEDIUM`

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: <strict policy>
```

Configure them where the repo's stack does: `helmet` on an Express or NestJS app, `headers()` in `next.config.*` or the proxy on Next.js, the CDN or reverse-proxy config on a static surface. Read the *served* header rather than the config before concluding it is applied — `nextjs-checklist.md` §9.7 is the worked case of a header that reads as configured and is provably never sent.

### A05.2 CORS misconfiguration — `HIGH`

Three common patterns to flag:

1. `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` (browsers reject the combo, but the misconfig signals deeper problems).
2. **Origin reflection** — a handler or proxy that copies the request's `Origin` straight back into `Access-Control-Allow-Origin` with no allowlist check, which lets every origin send credentialed requests.
3. A permissive default left in place for local development and shipped: `app.enableCors()` called with no arguments (which defaults to `*`), `{ origin: '*', credentials: true }`, or a wildcard gated on an env var that is unset in production.

Required: explicit allowlist of origins (an array or a function that checks against a list).

### A05.3 Default / debug endpoint enabled in production — `HIGH`

Swagger / GraphQL Playground / `/health` with detailed info in production.

### A05.4 Cross-origin access left unconfigured where a client calls the API from another origin — `MEDIUM`

A separate frontend, admin console or mobile web client calling the API from a different origin needs CORS configured deliberately — `app.enableCors({ origin: [...] })` on NestJS, the equivalent headers elsewhere. Missing CORS and misconfigured CORS both warrant flagging; see A05.2 for the wildcard and reflection variants.

---

## A06:2021 — Vulnerable and Outdated Components

### A06.1 New dependency without version pin — `HIGH`

Diff adds a dependency at `latest`, `^x.0.0`, or `*`. In production, dependencies should be pinned to an exact version (or a tight range with a corresponding lockfile commit) so a transitive update can't ship unverified code into the app.

### A06.2 Diff introduces a dependency with known HIGH/CRITICAL CVEs — `CRITICAL` or `HIGH`

If `npm audit` (or `pnpm audit`, `yarn audit`) reports HIGH/CRITICAL vulnerabilities introduced by a dependency added in the diff, flag it. Recommend a different package, an upstream fix, or — as a last resort — a documented compensating control.

### A06.3 Lockfile not updated alongside `package.json` — `HIGH`

If the diff modifies `package.json` but not the lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `bun.lockb`), CI installs may resolve different versions than what was reviewed. Always commit lockfile + package.json together.

### A06.4 `--legacy-peer-deps` / `--force` workaround in install scripts — `MEDIUM`

If a `postinstall` script or CI script uses `npm install --legacy-peer-deps` / `--force`, a real peer-dep conflict is being silenced. Investigate the conflict instead.

---

## A07:2021 — Identification and Authentication Failures

### A07.1 Session fixation — `HIGH`

After a successful login, the session ID must be rotated. If the diff implements login but doesn't regenerate the session, flag it.

### A07.2 Long-lived refresh tokens without rotation — `MEDIUM`

Refresh tokens should rotate on use, with the old one invalidated.

### A07.3 No CSRF protection on state-mutating Route Handler — `HIGH`

Server Actions have built-in CSRF (automatic Origin/Host comparison). Route Handlers do not. Add a custom header check, double-submit cookie, or verify Origin manually.

Caveat for Server Actions deployed behind a reverse proxy or CDN that rewrites `Host`: the built-in check fails-closed unless `experimental.serverActions.allowedOrigins` is configured in `next.config.js` (see `nextjs-checklist.md` §1.7). Don't assume "Server Actions are safe by default" — they're safe by default *given correct deployment config*.

### A07.5 Race condition in find-or-create (account / token consumption) — `MEDIUM`

Two concurrent OAuth callbacks can create duplicate users for the same provider account if the lookup-then-insert isn't atomic. Same shape: a password reset token consumed by two requests racing, or an invite link redeemed twice. Fix with a unique constraint on the natural key plus an atomic upsert — `INSERT … ON CONFLICT` on Postgres, `upsert` on Prisma, `save` with `@Unique` on TypeORM, `updateOne(…, { upsert: true })` on Mongo — and surface the conflict as a single-success outcome. See `logic-bugs-checklist.md` §1.3.

### A07.4 Email-based login enumerates accounts — `MEDIUM`

"Email not found" vs "wrong password" responses leak which emails are registered. Return a generic "invalid credentials" message.

---

## A08:2021 — Software and Data Integrity Failures

### A08.1 Webhook handler doesn't verify signature — `CRITICAL`

Stripe / GitHub / Slack / Twilio webhook handlers must verify the provider's signature header before parsing the body. The Stripe SDK exposes `stripe.webhooks.constructEvent(rawBody, sig, secret)`.

**Critical detail (high false-negative risk):** the `body` passed to `constructEvent` MUST be the **raw request body** (Buffer or string), not the parsed JSON. Computing the HMAC over a re-serialized JSON object will silently produce the wrong digest and verification will fail (or, worse, pass against attacker-tampered payloads in some setups).

- **Next.js Route Handler:** read the raw body with `await request.text()` and verify against that
  string. Do not call `request.json()` first — re-serializing changes the bytes and the digest.
- **NestJS:** create the app with `NestFactory.create(AppModule, { rawBody: true })` **and** exclude
  the webhook route from the global JSON body parser (or use `@RawBody()` on the handler). The
  `req.body` inside the controller must be a Buffer.
- **Either way, the comparison is constant-time and length-checked**, and the scheme — algorithm,
  encoding, header name — is a cross-package contract. Where the repo pins it with known-answer
  vectors on both sides, a one-sided change fails its own test; a change landing on both sides
  *without* a vector update is the finding, because nothing is left holding the scheme.

### A08.2 Insecure deserialization on user input — `CRITICAL`

`eval`, `Function(...)`, `vm.runInNewContext` applied to user-supplied strings. Almost always a bug. If the diff has it, very strong scrutiny.

### A08.3 Dependency from a registry without integrity check — `MEDIUM`

If `package.json` adds a new dependency, confirm `package-lock.json` is updated and pinned. Reject `latest` ranges in production.

---

## A09:2021 — Security Logging and Monitoring Failures

### A09.1 Logging sensitive data — `HIGH`

Logger calls that include passwords, tokens, full request bodies on auth endpoints, full session cookies, or PII without redaction. Specific anti-patterns to look for:

- `console.log(req.body)` on auth or payment endpoints.
- `logger.info(user)` where the user entity contains `passwordHash` / `mfaSecret` / refresh tokens.
- Pino / Winston configured without a `redact` allowlist (`redact: ['password', 'token', 'authorization', 'cookie', '*.passwordHash']`).
- Datadog / Sentry / Loggly clients that auto-capture request payloads without server-side scrubbing rules.

Don't false-fire on `logger.info('user logged in', { userId })` — flag only when the *value* is or transitively contains a credential, secret, or PII bundle.

### A09.2 Missing audit log for sensitive operations — `MEDIUM`

Account deletion, role change, refund, payout — these need an audit trail in addition to the operation succeeding.

---

## A10:2021 — Server-Side Request Forgery (SSRF)

### A10.1 `fetch(userProvidedUrl)` without allowlist — `HIGH`

The user can target internal services (`http://169.254.169.254/`, `http://localhost:5432/`). Allowlist hosts or block private/loopback ranges.

### A10.2 URL fetched server-side and result returned — `HIGH`

If the response of an SSRF-vulnerable fetch is returned to the user, internal data exfiltration is possible.

---

## Cross-cutting items

### XC.1 Secrets in commit history — `CRITICAL`

If the diff contains `.env`, `.env.local`, `credentials.json`, `serviceAccount.json`, AWS keys, etc., flag immediately and recommend secret rotation + git filter-branch.

### XC.2 `console.log` of sensitive variables — `MEDIUM`

Do NOT flag plain debug logs like `console.log('debug')` or `console.log(count)` — those are noise. Flag only when the logged value is, or transitively contains, one of:

- A request body (`req.body`, `request.body`, the parsed body of a Route Handler).
- A request headers object (may contain `Authorization`, `Cookie`).
- A user / session / account object (likely contains `passwordHash`, `email`, `refreshToken`).
- A token, secret, API key, JWT, or OAuth code.
- A full env / config object.

On the server, this leaks to stdout / CloudWatch / Datadog. On the client side it leaks into the browser console where any extension can read it. Same severity (`MEDIUM`); same fix (remove the log, or replace with a structured log of just the safe identifiers).

### XC.3 Disabled SSL/TLS verification in HTTP client — `CRITICAL`

`new https.Agent({ rejectUnauthorized: false })`. Never in production.

### XC.4 Hardcoded admin credentials / default password — `CRITICAL`

Comparing a literal admin password (e.g. `password === 'admin'`) anywhere in auth code is a master-password backdoor.

### XC.5 Sensitive data in URL query string — split severity

URLs are logged everywhere (browser history, server logs, analytics, referrer headers). Calibrate by what's in the query:

- **Auth tokens, password reset tokens, OAuth codes, API keys, JWTs in `?query=` — `HIGH`.** These directly enable account takeover if logs leak.
- **PII (email, SSN, account number) in `?query=` — `MEDIUM`.** Logging exposure, not direct compromise. Move to `POST` body or path segment with proper auth.

---

## Sources

- OWASP — [Top 10:2021](https://owasp.org/Top10/), [ASVS 5.0](https://owasp.org/www-project-application-security-verification-standard/)
- Next.js — [Data Security guide](https://nextjs.org/docs/app/guides/data-security)
- NestJS — [Authentication](https://docs.nestjs.com/security/authentication), [Authorization](https://docs.nestjs.com/security/authorization)
- Turbostarter — [Next.js Security Guide 2025](https://www.turbostarter.dev/blog/complete-nextjs-security-guide-2025-authentication-api-protection-and-best-practices)
- everything-claude-code — `agents/security-reviewer.md`, `skills/security-review/SKILL.md`
