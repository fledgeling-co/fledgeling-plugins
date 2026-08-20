# Logic, data-integrity and scoping checklist

Loaded for any server code — Route Handlers, cron and queue consumers, webhook receivers, the
catalogue crawler, MCP tools — anything that mutates persistent state or consumes external output
and persists it.

The framework checklist (`nextjs-checklist.md`) covers the *shape* of the code. This one covers its
*behaviour* under realistic input, partial failure and concurrent access. These are the defects a
review most reliably misses, because they are not anchored to an API convention and only become
visible once you read enough of the surrounding service to see the data flow.

---

## 1. Data-integrity hazards

### 1.1 Mongo `$set` and `$unset` on overlapping paths in one update — `HIGH`

```ts
// BAD — Mongo rejects this: "Updating the path 'x.y' would create a conflict at 'x.y'"
collection.updateOne({ _id }, {
  $set:   { 'sync.google.lastSyncedAt': new Date() },
  $unset: { 'sync.google.lastSyncError': '' },
})
```

Overlapping path prefixes in one update document throw `MongoServerError`, and the write fails
silently inside a `try/catch` swallow. Split into two sequential updates, or write the desired
final shape with a single `$set`.

### 1.2 Per-source or per-provider state stored on a flat field — `HIGH`

When an entity can carry state for several sources — `rhode`, `mecca`, `sephora` in this catalogue
— storing it on a flat field means the second source's write overwrites the first.

```ts
product.sourceSync = { lastSeenAt, externalId }        // BAD — one source at a time
product.sourceSync.mecca = { lastSeenAt, externalId }  // GOOD — keyed by source
```

The same shape applies to any per-user or per-device map: a key that identifies only one of the two
dimensions collides on the other.

### 1.3 Find-then-write with no unique index or atomic upsert — `MEDIUM`, often `HIGH` under contention

```ts
const existing = await Repo.findOne({ key })
if (!existing) await Repo.create({ key, value })   // two concurrent calls both see nothing
```

Declare a unique index on the natural key and use `upsert: true`. Critical for OAuth
"find-or-create user", token consumption, catalogue "upsert product", and webhook
"find-or-process".

### 1.4 Off-by-N on a time-window or offset filter — `HIGH`

A diff introducing a look-ahead window of N days, or an offset of N before a due date, is a near
guaranteed off-by-N source. Check three things: that the query window covers exactly the offsets the
config permits; inclusive versus exclusive endpoints (`$lt` against `$lte`); and time-of-day
boundaries when a schedule fires hourly against offsets computed in days.

### 1.5 Partial-failure idempotency in a cron or queue processor — `HIGH`

When a loop processes N items and item M+1 throws: were the first M marked processed **before** the
throw? If not, the next run re-sends notifications or re-charges. Did the failure roll back the
batch? Then the M side-effects already happened in the world and the DB does not reflect them —
same duplicate-send hazard on retry.

Mark each item processed immediately after its own side-effect succeeds, inside the loop, never in
one batch update at the end.

### 1.6 `Date` parsed from external input without validation — `HIGH`

`new Date(input)` returns `Invalid Date` for malformed strings, and persisting that writes a
poisoned value that breaks every downstream comparison. Dangerous specifically for LLM tool output,
crawled page text, and third-party API formats that drift between versions. Validate with
`z.coerce.date()` plus a refine, or guard with `if (Number.isNaN(d.getTime())) throw …` before
persisting.

### 1.7 A regenerate or reset path that silently overwrites edited records — `HIGH`

`deleteMany({ source: 'SYSTEM' })` followed by `insertMany(...)` wipes any operator edit made to a
system-sourced row. Preserve edited rows behind a flag, or surface the destructive scope in the
response (`{ regenerated: N, overwroteEdits: M }`) so the UI can warn first.

### 1.8 A regenerate or reset path that skips downstream side-effects — `MEDIUM`

If the primary create path fires a webhook or a sync push and the regenerate path calls the repo
directly, regenerated rows never propagate. The two write paths for one entity invoke the same
side-effect set.

### 1.9 An object whose members are all optional validates when it is empty — `HIGH`

A shape like `sentiment?: { positivePercent?: …; themes?: …; samples?: … }` makes `{}` a legal
value, so the type system reports the field as **present** while every consumer renders nothing. In
one recorded case a generator emitting a literal `chrome: {}` shipped nine records that validated,
returned 200 on every route and passed 524 content assertions — and the pages had no brand, no
navigation and no footer.

The partial form fails more quietly still: a record stating one field and omitting twelve validates,
and each unset field falls through to a default nobody chose.

Review move: for any object whose members are all optional, ask what `{}` means downstream and
whether the schema can express "stated partially" at all. If the field is only meaningful complete,
require the members together (a discriminated variant, `superRefine`) and make the consumer treat an
empty object as an error rather than an absence. `Object.keys(x).length === 0` reaching a
`{x && …}` render guard is the shape to grep for.

This is live in this repo: `redditSentiment` and `ingredientSafety` both serve behind a threshold
(`MIN_MENTIONS`, `MIN_COVERAGE`) precisely so a thin record is omitted rather than shown weakly. A
change that lets a partial record through the serve gate reintroduces the defect.

### 1.10 `$set` beside `$setOnInsert`, where the guard field is the one on `$setOnInsert` — `HIGH`

```ts
$set:         { …, record, updatedAt }
$setOnInsert: { status: 'draft', … }   // "never demote something already published"
```

The comment describes the opposite of what the line does. `$setOnInsert` protects `status`, so an
already-published row keeps `status: 'published'` — while `$set` replaces the entire record body
underneath it. A regenerated artifact nobody has reviewed is live at its public address the instant
the command returns, and the one line of output that could have said so is byte-identical to the
safe case.

Greppable shape: **an `$setOnInsert` field that is a state, approval or visibility flag, beside a
`$set` that writes the payload that flag governs.** `$setOnInsert` means "the first write decides
this forever", which is right for `createdAt` and wrong for anything consumers treat as permission.

Ask what the *second* write means. If regeneration re-derives the payload rather than editing it,
the write over a published row is refused unless an explicit flag is passed — and anything not
literally the published state is treated as overwritable, so an unrecognised future state is safe by
default.

Live sites in this repo: catalogue product upsert, bundle and release registration, and any
moderation-status write.

---

## 2. Scoping, tenancy and visibility filters

A query can silently drop a filter along any dimension the product uses to decide who sees what:
tenant, user, visibility, environment. Each drop leaks data the product intends to hide, and each
one still compiles and still passes a test written without the other tenant's rows in the fixture.
Establish in Phase 1 which dimensions this repo actually has, then check every changed query against
all of them.

### 2.1 A query missing its scope filter — `CRITICAL`

```ts
const docs = await DocsRepo.findOne({ sourceUrl: body.url })                        // every tenant
const docs = await DocsRepo.findOne({ sourceUrl: body.url, companyId: ctx.companyId })  // scoped

const rows = await Rating.find({ productId })                                       // every user
const rows = await Rating.find({ productId, userId: session.userId })               // scoped
```

Three shapes specifically, because each hides the omission differently:

- **Existence checks before insert.** `findOne({ key })` to dedupe, without the scope, lets one
  tenant's pre-existing row block another's write — and shows them the first tenant's row while
  doing it.
- **Background-job queries with no request context.** `find({ status: 'pending' })` in a cron or
  worker loads all tenants' rows together. Confirm the job either iterates per tenant or carries the
  filter.
- **Helper services keyed on something other than the scope.** `findByEmail`, `findByName`,
  `findByExternalId` that take no tenant or user argument. The gap is latent until a caller invokes
  them from a scoped path, which brings us to 2.2.

### 2.2 A new caller of an existing scope-incomplete query amplifies the leak — `HIGH`

The diff adds a call site to an existing `findBy*` helper that does not take the scope, and the new
caller sits in a scoped path. The helper pre-existed, so Mandate 3 would normally leave it alone —
but the new call site is in the diff, and it is what makes the gap exploitable. Flag the call site
and recommend either adding the scope to the helper signature or post-filtering in the new caller.

### 2.3 A role or permission lookup that matches across tenants — `CRITICAL`

```ts
user.companyRoles.find(cr => cr.role === 'admin')                                   // any company
user.companyRoles.find(cr => cr.companyId === ctx.companyId && cr.role === 'admin')  // this one
```

A user who is admin in tenant A and an ordinary member of tenant B is granted admin in B whenever
the lookup forgets to scope by tenant. The same shape appears in permission-set membership, feature
entitlements and seat checks.

### 2.4 A tenant id taken from a header or parameter without a membership check — `HIGH`

Middleware reads `x-company-id` (or a path segment, or a query parameter) and stamps it onto the
request context without checking the value against the caller's own memberships. Any authenticated
user then escalates into any tenant by changing one header. The check is not optional and not
implicit: `if (!user.companies.includes(headerCompanyId)) throw Forbidden`.

### 2.5 Identity taken from the client rather than the session — `HIGH`

The server attributes identity from the session or token only; a handler that reads a `userId` from
the body and trusts it lets any caller write as anyone. The same applies to a role, a plan or a
capability claim carried in a request. A route with optional auth is the easiest place to get this
wrong, because both the anonymous and the signed-in path have to be right.

### 2.6 A visibility filter dropped from a list query — `HIGH`

Moderation status, soft-delete flags, draft/published state, seeded or demo data exclusions — these
are load-bearing and easy to lose in a refactor, because losing one changes the result set rather
than breaking the query.

Where the repo has one helper that applies the whole filter set, a new endpoint that hand-rolls the
filter instead is the finding, and so is an existing one that keeps half of it. Grep for the helper
before accepting a hand-rolled filter; a count that labels a list is the same query and needs the
same filter, or the label disagrees with the list under it.

### 2.7 A tenant- or environment-specific literal inside shared code — `HIGH`

The leak with no query in it. A component or module shared across tenants carries the *first*
tenant's identity as source literals — its monogram, its ticker, its policy PDF URLs, its address:

```tsx
// Footer.tsx renders for every tenant
<span className="mark">AE</span>
<span className="ftr__codes">ASX: AAL</span>
<a href="https://example-first-tenant.com/…/Constitution.pdf">Constitution</a>
```

No scope filter is missing, no query is unscoped, and every check above passes. The recorded case
shipped latent for months because no second tenant was rendering that component yet; the moment the
generator started emitting chrome, every tenant's footer would have published another tenant's
constitution under its own address.

Two tells worth grepping for in any shared, layout or design-system component: a **proper noun or
ticker as a string literal**, and an **absolute URL whose host is not the current tenant's**. Flag
both, then check the same file for a fallback that quietly substitutes the reference tenant when a
record omits a field — the same defect one indirection deeper.

The stylesheet form is the one nobody looks for: a design token left unset by tenant B falls back to
the value tenant A's build authored, so B renders A's brand colour with no error, no warning and no
diff. The environment variant is the same shape without the tenancy — an API base, a bucket name or
a webhook URL pinned to one environment inside code that several environments import.

---

## 3. Parsing, regex and text extraction

Extraction code gets reviewed as if its failure mode were a crash. Its actual failure mode is
**silently returning less than it matched**, which reads downstream as "the source did not contain
that". Any crawler, scraper, importer, log parser or LLM-output extractor in the diff routes here.

### 3.1 A quantifier bound that decides the match rather than capping it — `HIGH`

```js
/## Ingredients\n([\s\S]{0,600}?)(?=\n## |$)/     // BAD
```

The lazy `{0,600}` reads as a safety cap. It is not — it is part of the match decision. The regex
tries the shortest body first and expands, and if the lookahead is still unsatisfied at 600
characters the whole match **fails** rather than truncating, so the section vanishes from the output
entirely. A bound that can change *whether* a match happens is a correctness bug wearing a
performance fix's clothes. Match unbounded and `.slice(0, n)` the captured group afterwards.

Same shape: `{1,N}` on a repeated group inside an alternation, and any lazy bound followed by a
required suffix. Note that this repo caps ingredient text at 8000 characters — that cap belongs on
the slice, not in the pattern.

### 3.2 A word boundary that can never fire — `MEDIUM`

`\b` asserts a transition between a `\w` and a non-`\w` character, so it **cannot sit before a
literal `(`, `)`, `-`, `.`** or any other non-word character when the preceding character is also
non-word:

```js
/\bSize\b:?\s*(\(\d+\s*ml\))/    // the \b before ( is unreachable
```

A dead branch in an alternation does not error; it never matches, so the next alternative wins. Grep
changed regexes for `\b` adjacent to a non-word literal, and prove any new branch fires against a
real input before trusting it.

### 3.3 A parser change with no test over a real payload — `MEDIUM`

Extraction rules are tuned against a sample. Assert against a **stored real document**, not a
hand-written fixture that already agrees with the regex — the fixture and the pattern were written
by the same person in the same minute, and they agree by construction.

### 3.4 One predicate answering two different questions — `HIGH`

An exclusion list written for one question gets reused for a second that sounds similar, and for some
inputs the two questions have **opposite** correct answers. In one recorded case a `BOILERPLATE`
regex written to keep privacy notices out of a company's business units — "is this a thing the
company does?" — was also used to decide which documents reached its shelves — "does this document
belong on a shelf?". On the phrase "modern slavery" the answers diverge, and four statutory filings
were dropped from every tenant.

Greppable two ways, neither needing the domain:

- **A constant named for a category, referenced from call sites that read differently.** Name the
  question each call site asks out loud; if the sentences differ, the predicate has to split.
- **A category nothing can be assigned to.** Code containing an unreachable category is telling you
  a predicate is answering the wrong question, and it is visible without running anything.

In this repo the shape lives in the grouping and dedupe predicates: the Rhode per-flavour `pdp:`
tag and the Mecca `I-` (SKU) versus `V-` (master) split, documented in
`docs/CATALOGUE_PRODUCTS_AND_SHADES.md`. A predicate reused across "is this the same product?" and
"is this the listing we serve?" is the same defect.

Fix by splitting into two predicates that share the raw list, with the second carving out the
overlapping cases explicitly. Guard the split with a case that **names the specific inputs** — "4
items matched" passes on four copies of the same thing — and that asserts the classes still
excluded, so the carve-out cannot widen silently.

---

## 4. Tests that encode the bug

The six contract boundaries in `docs/CONTRACTS.md` are guarded by test pairs, so a weakened guard
is a weakened boundary. This section is the highest-value read for any diff that touches both source
and tests.

### 4.1 A test updated to assert the OLD behaviour after a fix — `HIGH`

When a fix lands and its test changes to keep passing, read which direction the change went. A test
rewritten to expect the pre-fix output is a standing request to reintroduce the bug, and it will be
honoured, because the next person to touch that path sees a green suite asserting the broken
behaviour is correct.

Reviewable in the diff with no other context: the source hardened, and the assertion in the same
commit got **weaker**. An exact match became `toContain`. A `rejects.toThrow` became a resolved
value. A `403` expectation became a `200`. A `.strict()` schema became `.passthrough()`. A key-set
list in `dto-contract.test.ts` or `contract.test.ts` lost an entry in the same commit that dropped
the field. Ask for the reason in the test or in a comment, or reject the assertion change.

### 4.2 A test asserting a call happened rather than what it produced — `MEDIUM`

`expect(render).toHaveBeenCalled()` passes when the render produced the wrong data. This is the
general form of a failure that ships repeatedly: verifying **that** something happened rather than
**what** it produced. Assert the value, and where both sides come from the same source — an image's
`alt` and the heading beside it, a section title and its own payload — assert they agree.

### 4.3 A state-changing test that never re-reads the observable — `MEDIUM`

A test that performs a mutating call and asserts only on that call's return value has tested the
return value. One measured census found 32 state-changing test functions of which 6 re-read the
observable afterwards and **26 did not**; a separate sweep of 7 mutating operations found 3 that
returned success while changing nothing at all.

Greppable: an `await` on a create, update, delete, publish, retract or sync, with no subsequent read
of the thing it changed. In this repo that means a write test that never re-queries the collection,
a `publish_bundle` test that never re-reads the release, a sync test that never re-reads the product.

### 4.4 An assertion that recomputes the expected value the way the code does — `MEDIUM`

When the test derives its expectation through the same arithmetic as the implementation, it passes
by construction and can never disagree with the code. Expected values come from an independent
source: a literal, a stored fixture, or a second derivation somebody wrote separately. The Reddit
scoring constants (`docs/CONTRACTS.md` §6) are the standing example — a test that re-derives the
score from the same constants proves the constants agree with themselves.

### 4.5 A fixture that names ONE entity to stand for a CLASS — `MEDIUM`

`const OUT_OF_STOCK_PRODUCT = 'rhode-peptide-lip-tint'` — a constant chosen because that record
happened to have the property under test. Correct until the record changes class, and then several
suites fail at once in a shape that reads like a product regression rather than a stale fixture.

Greppable with no context: a **proper noun, slug or id in a test constant whose *name* describes a
category** (`EMPTY_`, `ARCHIVED_`, `NO_RATINGS_`, `HIDDEN_`). Ask for a query that selects by the
property, plus an assertion that the query returned something — a selector that matches nothing and
a suite with nothing to find serialize identically.

---

## 5. LLM output validation

The Reddit sentiment pipeline and any MCP tool that persists model output live here.

### 5.1 An LLM-emitted field persisted without schema validation — `HIGH`

When a tool call returns `{ sentiment, themes, confidence, … }` and the service persists those
fields directly, the model is one prompt injection away from controlling the database. Validate with
Zod, coerce to intended types (`z.coerce.date()`, `z.coerce.number().min(0).max(1)`), and reject and
log on parse failure rather than silently storing `null`.

### 5.2 Enum-valued output not constrained to a known set — `HIGH`

If the model returns `sentiment: string` and downstream code switches on it, an unrecognised value —
a typo, a hallucination, prompt drift — falls through every branch and is stored verbatim. Use
`z.enum([...])` for tool output and add an exhaustiveness `default` on the consuming switch. In this
repo `REDDIT_SENTIMENT_VALUES` is the closed set, pinned as a Zod enum and a Mongoose enum on both
sides.

### 5.3 A deterministic classifier replaced by an LLM call with the old enum mapping retained — `MEDIUM`

The deterministic classifier returned one vocabulary, the model returns another, and the mapping
falls through to a default — breaking the consumer that expected the old value. When a diff swaps a
deterministic path for a model call, audit the consumers.

---

## 6. Default-value and mode bypasses

### 6.1 A default on a discriminator that bypasses validation — `HIGH`

When a body carries `mode: 'a' | 'b'` with a default, and only one mode requires a field, a client
can claim the other mode to skip the requirement. Validate the discriminator and its dependent
required set together — a discriminated union in Zod, not a flat object with a default.

### 6.2 A trust-bearing claim taken from the client — `HIGH`

The channel, source, or origin a handler branches on is derived from server-trusted state: the
route the request hit, the token's row, the auth context. Never from the body. A client that can
name its own channel can pick the one with the weakest checks.

### 6.3 An anonymous or public path that remains linkable — `HIGH`

A record marked anonymous that still stores a correlation token mapping back to an identity-bearing
row is re-identifiable by anyone who can read both. Either store no token, or hash it with a
per-collection salt.

---

## 7. Authorization edge cases the framework checklists miss

### 7.1 A public route accepting the same token the private route does — `HIGH`

If the guard's algorithm check passes but the type check (`payload.type === 'dev-impersonation'` →
reject in production) is missing or runs in a different layer, the impersonation token works in
production. Verify both checks fire on the same code path.

### 7.2 An optional shared-secret check that fails open when the secret is unset — `CRITICAL` on production paths

```ts
// BAD — with the env var unset, the conditional skips and the endpoint is unauthenticated
if (process.env.CRON_SECRET) {
  if (req.headers.get('x-cron-secret') !== process.env.CRON_SECRET) throw …
}
```

Either the secret is required — throw at startup if unset — or an alternative auth mechanism always
runs. Never gate auth on the presence of an env var. This applies directly to the cron routes and
the catalogue webhook.

### 7.3 A non-constant-time comparison on secret material — `HIGH`

`provided !== expected` on a cron secret, a webhook signature, or an API key. Use `timingSafeEqual`
with a length pre-check, over the raw body and before parsing. Where the repo already has one
verifier doing this correctly, cite it as the exemplar — a second verifier that does not follow it
is the finding, and the divergence is easier to argue than the timing attack.

---

## 8. Concurrency and claim hazards

### 8.1 A worker claim with no TTL-based stale-lock recovery — `MEDIUM`

A claim pattern (`findOneAndUpdate({ status: PENDING }, { status: RUNNING, lockedBy, lockedAt })`)
without a sweep that resets `RUNNING` rows older than a TTL leaks the row forever when the worker
crashes. Pair the claim with a stale-lock sweep at the top of the job.

### 8.2 A Redis lock released unconditionally — `HIGH`

`del(key)` in a `finally` deletes the *next* holder's lock when this run outlived its TTL. Store a
unique owner token and release with a compare-and-delete. Serialize cron and long-running sync jobs
behind a single-flight `SET NX` with a TTL and a holder token; on serverless, assume invocations
overlap.

### 8.3 A counter whose `INCR` and `EXPIRE` are separate operations — `HIGH`

`INCR` then `EXPIRE` only when `n === 1` strands a TTL-less key if the process dies between the two,
which is a permanent rate-limit lockout for that key. Set the TTL in the same operation, or
re-assert `EXPIRE` whenever `ttl < 0`.

### 8.4 In-flight state change between enqueue and process — `MEDIUM`

Between enqueue at T1 and processing at T2 the entity may have changed — content removed, a user
suspended, a product delisted. The processor re-reads current state rather than trusting the
enqueue-time snapshot.

---

## 9. Side-effect ordering

### 9.1 A side effect before the durable write — `HIGH`

```ts
await push.send(notification)          // happens in the world
await queue.markSent(job.id, msgId)    // what if this throws?
```

If the marker throws, the notification went out and the queue still shows pending, so the next run
re-sends. Either commit the side effect last inside a transaction, make the receiving side
idempotent through a server-generated message id, or record `attempted` before and `succeeded` after
so retries are visible.

### 9.2 A side effect not skipped when a downstream id is unavailable — `MEDIUM`

If a sync needs both a token and an external id and one is missing, attempting it produces a
confusing 4xx instead of a no-op. Guard with an explicit precondition and record a structured
`lastSyncError` for diagnosis.

---

## 10. Sources

The access-control and behaviour patterns are drawn from OWASP A01 post-mortems where the bugs
evaded framework-shaped review because the violations were behavioural rather than structural. The
LLM-output section follows Anthropic's tool-use validation guidance and the prompt-injection threat
model. §1.9, §1.10, §3 and §4.1–4.2, §4.5 are reinstated from this skill's ancestor, where each
traces to a recorded production incident; §4.3 and §4.4 come from measured test-integrity censuses
and the tautological-assertion literature.
