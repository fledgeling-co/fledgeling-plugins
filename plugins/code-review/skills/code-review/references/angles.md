# The angles

Fourteen ways to look at a diff. Angles are *how* you look; the checklists in
`*-checklist.md` are *what* you know, and angle H walks them. Twelve are selected by depth; two
fire on a trigger and run at every depth including `quick`.

**Angles do not suppress each other.** When two angles flag the same line for different reasons,
record both candidates. Dedup happens in Phase 4 on evidence, never in Find on a hunch. An angle
that decides another angle already covered a line is the single cheapest way to lose a bug.

**Pass every candidate through that has a nameable failure scenario.** A finder that quietly drops
half-believed candidates bypasses the verify step entirely, and that is the dominant cause of
misses. If you can say what input or state makes the line wrong, it is a candidate.

**Candidate budget per angle:** ≤4 at `quick`, ≤6 at `standard`, ≤8 at `deep`.

| Angle | `quick` | `standard` | `deep` |
|---|---|---|---|
| A hunk scan · B removed behaviour · H checklist conformance · N conventions | yes | yes | yes |
| C caller and callee trace · D flow trace · F language pitfalls · R reuse | | yes | yes |
| G partial failure and ordering · S simplification · E efficiency · T altitude | | | yes |
| X contract drift · M mirror and adapter | on trigger | on trigger | on trigger |

---

## Correctness angles

### A — Hunk scan

Read every hunk line by line, then read the enclosing function for each hunk. Bugs in the
unchanged lines of a touched function are in scope: the change re-exposes them, or fails to fix
them.

For each line, ask what input, state, timing, or platform makes it wrong. Look for an inverted or
wrong condition, an off-by-one, a null or undefined dereference, a missing `await`, a falsy-zero
check (`count && <X/>` renders a literal `0`), a wrong-variable copy-paste, an error swallowed in a
`catch` that should propagate, an unescaped regex metacharacter.

### B — Removed behaviour

For every line the diff **deletes or replaces**, name the invariant or behaviour it enforced, then
search the new code for where that invariant is re-established. Failing to find it is a candidate:
a removed guard, a dropped error path, a narrowed validation, a `.strict()` that became
`.passthrough()`, a deleted test that covered a real case.

This angle finds what a diff scan structurally cannot, because the evidence is the absence of
something. Run it on every depth for that reason.

### C — Caller and callee trace

For each function the diff changes, grep for its callers and check whether the change breaks any
call site: a new precondition, a changed return shape, a new thrown error, a timing or ordering
dependency. Then check callees — does a parallel change in the same diff make an existing call
unsafe?

In a workspace the trace crosses packages. A changed export may have callers in a sibling package,
a changed wire field may have a consumer in a client, and two packages sharing a datastore can break
each other without either failing to compile. Grep the whole workspace, not the package — the
workspace layout comes from the Phase 1 repo profile.

### D — Flow trace, entry point to sink

For each changed entry point — an HTTP route or Route Handler, a controller method, a Server
Action, a cron or queue consumer, a webhook receiver, a CLI or MCP tool handler — trace
user-controlled input from source to sink across the diff's files.

Checklists pattern-match one file at a time, and the highest-impact defects live in flows across
files: broken object-level authorization, an auth bypass, a validation that runs on one path and
not the sibling path, a race. One traced flow beats ten pattern matches.

Ask at each hop: where did this value come from, what has validated it since, and what does the
sink trust about it.

### F — Language and framework pitfalls

The footgun sweep, scoped to the languages and frameworks the repo profile says are present. Run
only the rows that apply; record the rest as `not-applicable` with that reason. Flag any instance
the diff introduces:

- **TypeScript / JavaScript** — falsy zero, `==` coercion, a closure capturing a loop variable, a
  floating promise, `forEach(async …)`, `as unknown as T` on untrusted input, `JSON.parse` assigned
  a concrete type, a non-null `!` on a value that can genuinely be null.
- **React 19** — a conditional hook, a component defined inside another component's render body,
  a value read in an effect and absent from its dep array, `setState` during render, derived state
  mirrored into state, index-as-key on a list that reorders.
- **React Native / Expo** — a screen that never unmounts, so effect cleanup does not run on
  navigate-away; a non-serializable value in navigation params; `ScrollView` where the data is
  unbounded; a token in plain AsyncStorage.
- **NestJS** — a `@Public()` or missing `@UseGuards`; a provider injected with the wrong scope; a
  DTO without `class-validator` decorators behind a `ValidationPipe` that therefore validates
  nothing. `nestjs-checklist.md` carries the full list.
- **Document stores (Mongo / Mongoose)** — `$set` and `$unset` on overlapping path prefixes in one
  update; `$setOnInsert` protecting a state flag beside a `$set` that rewrites the payload that flag
  governs; find-then-write with no unique index; `new Date(externalInput)` unguarded.
- **SQL and ORMs (Prisma, Drizzle, TypeORM, raw drivers)** — a raw-SQL escape hatch with an
  interpolated value; a transaction that does not wrap the read the write depends on; a lazy
  relation loaded inside a loop; a migration that drops or renames without a backfill.
- **Other languages the repo actually uses** — Python mutable default arguments and late-binding
  closures; Go nil-map writes, loop-variable capture and an ignored `err`; Rust `unwrap` on a
  fallible path; float equality anywhere.
- **Dates and time** — timezone and DST drift, an inclusive-versus-exclusive window endpoint, a
  schedule that fires hourly against offsets computed in days.
- **Regex** — a lazy bound like `{0,600}` that decides the match rather than capping it, a `\b`
  adjacent to a non-word literal so the branch can never fire.

### G — Partial failure and ordering

Ask what happens when the process stops halfway. Deep only, because it needs the surrounding
service read rather than the hunk.

An irreversible side effect fired before the marker recording it can be persisted; a cron loop that
marks items processed in one batch update at the end, so a mid-loop throw re-sends everything that
already succeeded; a queue consumer that trusts the enqueue-time snapshot instead of re-reading the
entity at process time; a lock released with an unconditional `del` in `finally` instead of a
compare-and-delete on the owner token; a KV counter whose `INCR` and `EXPIRE` are two operations,
so a crash between them strands a TTL-less key.

### H — Checklist conformance

Walk each checklist the Phase 2 routing table loaded, item by item, against the diff's files.

This is the angle that carries the stack-specific knowledge, so it runs at every depth. Record for
each checklist section whether you evaluated it, whether it was not applicable to these files, or
whether you could not evaluate it and why — that record is what the coverage ledger prints.
`coverage.md` defines the states.

---

## Cleanup angles

The angles above hunt bugs; these hunt cleanup in the changed code. Their candidates use the same
schema, and the `failure_scenario` field states the concrete cost — what is duplicated, wasted,
harder to maintain, or which stated rule is broken — rather than a crash. When the report cap
forces a cut, correctness outranks all five.

They are not decoration. In the code-review literature the large majority of defects human
reviewers raise are evolvability findings rather than functional ones, so a reviewer that emits
only bugs is emitting a minority of what a review is for.

### R — Reuse

Flag new code that re-implements something the repo already has. Grep the shared modules and the
files adjacent to the change, and name the existing helper to call instead. Two sites pay off most:
the repo's own utility or `lib/` modules, and the near-duplicate that lives in a *different* package
because nothing shares it — the repo profile's boundary list says where those are.

### S — Simplification

Flag unnecessary complexity the diff adds: redundant or derivable state, copy-paste with slight
variation, deep nesting, dead code left behind. Name the simpler form that does the same job.

### E — Efficiency

Flag wasted work the diff introduces: redundant computation or repeated I/O, a query per item
inside a loop, independent operations run sequentially, blocking work added to a hot path or to
module load. Also flag a long-lived object built from a closure — it keeps the whole enclosing
scope alive for the object's lifetime, which is a leak when that scope holds large values.

### T — Altitude

Check that each change is implemented at the right depth rather than as a fragile bandaid. Special
cases layered onto shared infrastructure are the tell: prefer generalizing the underlying mechanism
over adding another special case beside the last one.

### N — Conventions

Find the instruction files that govern the changed code — the repo profile lists them. Typically the
repo-root `CLAUDE.md` or `AGENTS.md`, the per-package file of each package the diff touches (a
directory's file applies to files at or below it), a `CONTRIBUTING.md`, and any team practices
document those point at. Read each and check the diff for clear violations.

Flag a violation only when you can quote the exact rule and the exact line that breaks it. No style
preferences, no inferences about the spirit of the document. Name the file and quote the rule in
the finding, so the report can cite it. Skip anything the tooling already enforces — the repo
profile names the lint and typecheck gates, and a finding one of them would have caught is noise in
a report read after CI. If no instruction file applies to the changed paths, return nothing for this
angle and record it as `not-applicable`.

---

## Trigger-fired angles

### X — Contract drift

**Trigger:** the diff touches any file on a cross-package boundary in the Phase 1 repo profile — a
file named in a contract document, a hand-mirrored type, a wire DTO, a generated client, a schema
one side publishes and another consumes, or a constant restated in several packages.

Each side typechecks independently while the shapes diverge, so drift ships undetected and only a
review catches it. That is the whole reason this angle fires at every depth rather than waiting for
`deep`.

For each touched boundary, check three things together. The **shape on both sides** — a field added
to a server DTO and not to the client type, or the reverse. The **guard on both sides** — a
key-set parity test, known-answer vectors for a signing scheme, a snapshot, a generated-client
diff. And the **contract document entry**, which is part of the change rather than follow-up work.

Four shapes worth grepping for specifically:

- A field the consumer reads that the producer's projection never serializes, which makes a whole
  consumer path dead while both sides compile.
- A closed enum or union extended on one side only.
- A shared constant restated in several files because nothing holds it — a threshold, a cap, a
  header name, a signing algorithm. Changed in one place and not the others, it compiles, passes
  both suites, and changes what production serves.
- A guard test weakened in the same commit as the shape it guards (`logic-bugs-checklist.md` §4.1).

Where a boundary has **no** guard on either side, that is a `no-oracle` row in the ledger, not a
clean one: nothing in the repo can decide whether the two sides still agree.

### M — Mirror, wrapper and adapter correctness

**Trigger:** the diff touches a type or class that mirrors, wraps, adapts, proxies, caches or
decorates another — the repo profile's boundary list names these, and the usual tells are a name
containing `Wrapper`, `Adapter`, `Proxy`, `Cache`, `Client`, `Repository` or `Mirror`, a class whose
constructor takes an instance of the thing it fronts, and a type declared twice in two packages with
no import between them.

Enumerate the wrapper's members and check each one routes to the wrapped instance rather than back
through a registry, session, container or global — a method that resolves through the global is how
a wrapper re-enters itself or recurses. Then grep the callers and check every member they use is
actually forwarded; a partially forwarded wrapper fails only on the paths nobody exercised.

**Report the member count you walked**, so a partial walk is visible as a partial walk rather than
reading as a clean pass.

Three recurring instances:

- **A hand-mirrored type with no shared package.** A field, enum member, index or default added on
  one side is a divergence until it is added to the other. Where both sides read the same datastore,
  the divergence is a data bug rather than a type error, and nothing fails until production.
- **A projection or DTO layer.** A field added to a model and not to its DTO never reaches a client;
  a field added to a DTO with no projection behind it is `undefined` on every response.
- **A deliberately tolerant consumer.** Some adapters are designed to swallow a parse miss and
  render a fallback rather than throw. Where the repo documents that, tightening it is the finding
  and the tolerance is not — check the instruction files before flagging, and refute under Gate 3
  with `refutation_class: "by-design"` when they say so.
