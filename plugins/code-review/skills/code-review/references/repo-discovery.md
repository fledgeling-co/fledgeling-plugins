# Repo discovery — learn the project before you review it

Read this in Phase 1 at every depth. It replaces the project map a project-specific reviewer would
ship with hard-coded facts, and it is the better design for the same reason a general skill needs
it: **project knowledge belongs to the target repo, at runtime.** A map written into the skill goes
stale silently; a map derived from the repo is right by construction, and it is right for every
repo the skill is pointed at.

The output of this phase is the **repo profile** — a short block of facts you inline into every
shard and verifier prompt, because a subagent has no other way to learn them. Aim for 15 to 30
lines. Anything longer is being read for its own sake rather than to decide a finding.

`scripts/repo-facts.sh` runs the mechanical half in one pass and prints a draft profile. Read its
output, then fill the judgement half yourself.

## What the profile must carry

| Field | How you establish it | Why a finding turns on it |
|---|---|---|
| Instruction files | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `CONTRIBUTING.md` at root and per package | Angle N cannot fire without them, and a convention finding must quote the governing rule |
| Workspace layout | `pnpm-workspace.yaml`, `package.json#workspaces`, `turbo.json`, `nx.json`, `lerna.json`, `Cargo.toml` `[workspace]`, `go.work`, `pyproject.toml` | Area targeting, bucketing, and the scope of every cross-package grep |
| Package manager | The lockfile present: `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lockb`, `uv.lock`, `Cargo.lock`, `go.sum` | Every command you print for the reader to run has to be the one that works here |
| Gate commands | The `scripts` block of each touched package, plus the CI workflow | Stage-2 must invoke the repo's own gate, not a tool that happens to be installed |
| Frameworks actually present | `dependencies` and `devDependencies` of each touched package, at their real versions | Checklist routing, Gate 2, and the absent-framework refutation below |
| Global controls | Grep, per the section below | Kills a false positive in Find instead of refuting it in Verify |
| Cross-package boundaries | Shared packages, hand-mirrored types, wire DTOs, generated clients, contract docs | Angles X and M, and the highest-value findings a diff review produces |
| Test layout | Where tests live and what runner runs them | A coverage claim must rest on a file list, not an impression |

## Establishing the gate commands

Read the `scripts` block, not the tool. Three failure modes, all of which produce a report that
gates on something CI does not:

- **A wrapper script.** `"typecheck": "tsgo --noEmit"` and `"typecheck": "tsc --noEmit"` are
  different compilers with different behaviour; `"lint": "oxlint"` and `"lint": "eslint ."` catch
  different things. Invoke the script, never the tool you assume is behind it.
- **A monorepo task runner.** Where `turbo.json` or `nx.json` exists, the gate is
  `<pm> turbo run typecheck --filter <package>...` rather than a bare per-package call, and the
  `...` suffix matters because it pulls in dependents.
- **A CI step the package scripts do not name.** Read `.github/workflows/*.yml`,
  `.gitlab-ci.yml`, `Jenkinsfile` or the equivalent. A contract-guard test, a build that only runs
  on the deploy target, or an env var the local run lacks all live there.

Record the gate commands verbatim in the profile. Stage-2 in `verification-loop.md` runs exactly
these.

## Establishing which frameworks the repo uses — and refuting the ones it does not

Read the `dependencies` and `devDependencies` of each package the diff touches and write the list
into the profile: the frameworks present, at their installed major versions, and the data layer.
Then state the absences that matter.

**The absences are load-bearing.** A finding that names a framework the repo does not contain is
refuted at Gate 1 — not downgraded, refuted — because the fix cannot be applied. This is the
single cheapest refutation in the pipeline and it needs the profile to fire.

The worked example this rule comes from: the project-specific ancestor of this skill served a
Next.js monorepo over Mongoose with no NestJS and no Prisma anywhere in it. Its verifier prompt
carried the sentence *"there is no NestJS and no Prisma here, so a finding that names a NestJS guard
or a Prisma call is refuted at Gate 1"*, and that one line killed a recurring class of false
positive — a checklist item pattern-matching on shape rather than on stack, proposing a fix in a
framework the repo had never installed. The mechanism was right and the constant was wrong. Derive
the constant here.

So the profile carries a line of this shape, filled from what you actually read:

```
Stack: Next.js 16 App Router + React 19 · Mongoose 8 over MongoDB · Zod 3 at the boundary.
Absent: no NestJS, no Prisma, no SQL database, no GraphQL layer.
Gates: pnpm turbo run lint typecheck test build · typecheck is `tsgo --noEmit` · lint is `oxlint`.
```

Both halves go into every shard and verifier prompt. A verifier that does not know what is absent
cannot refute on it.

Where a package is present but unused by the changed code, that is not an absence — say "present,
not used on these paths" and let Gate 5 handle reachability instead.

## Global controls worth mapping before flagging a missing guard

These are the occupants of the Phase 1 mitigating-controls map. Grep for each rather than assuming
presence or absence, and record what you actually found, where it applies, and what it covers.
A candidate a mapped control already covers should never be born.

- **Validation at the trust boundary** — a schema library at the route or handler edge (Zod,
  Valibot, class-validator, Pydantic), a framework-global validation pipe, or a typed request
  parser. Note whether it is strict: a schema that silently drops unknown keys and one that rejects
  them are different controls.
- **Authentication and session handling** — a shared session helper, a global guard or middleware
  chain, a framework auth integration. Note whether routes opt *in* or *out*, because the failure
  mode of forgetting differs.
- **The mutating-request preamble** — whatever the repo runs before handler logic on a public
  mutation: an origin or CSRF check, a rate limiter and its store, a body parse. Record the order.
- **The data layer's own constraints** — unique indexes, enums, required fields, foreign keys,
  row-level security, ORM query builders that parameterize by default. A constraint declared in the
  schema is a real control; one assumed and never declared is not, so read the schema.
- **Locks, counters and idempotency keys** — where they live, whether a release is
  compare-and-delete, whether a counter sets its TTL in the same operation.
- **Response headers and CSP** — the framework config, the middleware or proxy, the CDN config. A
  header set in config is not necessarily a header served: `nextjs-checklist.md` §9.7 is the worked
  case, and Gate 6 is the general rule.

## Cross-package boundaries

Every boundary between two packages that must agree is a place a diff can break production while
both sides typecheck. Find them before Find runs, because angles X and M fire on them.

Look for, in rough order of how often they bite:

1. **A contract document** — `docs/CONTRACTS.md`, an OpenAPI or GraphQL schema, a protobuf
   definition, an ADR index. Where one exists it names the boundaries for you; read it and check
   whether the diff's files appear in it.
2. **Hand-mirrored types with no shared package.** Two packages declaring the same shape
   independently drift silently and each side keeps compiling. Grep for a type name that appears in
   two packages with no import between them.
3. **A wire DTO or projection layer** — a field added to a model and not to its DTO never reaches a
   client; a field added to a DTO with no projection is `undefined` on every response.
4. **A generated client** — check whether the generator ran in the same diff as the schema change.
5. **A constant restated in several places because nothing shares it.** A threshold, a cap, an
   enum, a signing header name. Changing one and not the others compiles, passes every unit test on
   both sides, and changes what production serves. Grep the literal.
6. **A guard test on each side.** Where one exists, a diff that weakens it is the finding — a wire
   change landing in the same commit as a loosened assertion is the shape (`logic-bugs-checklist.md`
   §4.1). Where none exists, say so: an unguarded boundary is a `no-oracle` row, not a clean one.

## Where the repo disagrees with anything you were told

The repo wins. A `CLAUDE.md` describing a structure the tree does not have, a README naming a
command the `scripts` block dropped, a contract doc listing a file that moved — each is worth one
LOW finding of its own, and none of them overrides what you can read directly.

Record the profile with the date you derived it and the commands you derived it from, so a later
reader can tell a stale line from a current one.
