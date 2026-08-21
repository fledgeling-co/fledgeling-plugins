# Quality Lenses — Performance, Tests, Dead Code, Tech Debt, Dependencies, DX

Each lens emits **candidates in the standard candidate schema** (see `process.md` and `output-format.md`) with severity and confidence — findings, not implementation plans. There is no executor; the developer reads the report and applies the fixes.

Skip anything the tooling already enforces. The Phase 1 repo profile names the repo's linter, formatter and typechecker; a candidate one of them would have caught is noise in a report a developer reads *after* the gates.

These lenses are **default-on at `deep` depth**, and individually selectable at any depth via lens keywords (`perf`, `tests`, `dead-code`, `debt`, `deps`, `dx`). At `quick`/`standard` depth they only run when explicitly requested.

A finding is only a finding with evidence. "Probably has N+1 queries somewhere" is not a candidate; `orders/api.ts:142 issues one query per order item inside a loop` is.

---

## Contents

- [Scope rules per lens](#scope-rules-per-lens)
- [Lens: perf — Performance](#lens-perf--performance)
- [Lens: tests — Test Coverage](#lens-tests--test-coverage)
- [Lens: dead-code — Dead Code](#lens-dead-code--dead-code)
- [Lens: debt — Tech Debt & Architecture](#lens-debt--tech-debt--architecture)
- [Lens: deps — Dependencies & Migrations](#lens-deps--dependencies--migrations)
- [Lens: dx — DX & Tooling](#lens-dx--dx--tooling)
- [Severity calibration for lens findings](#severity-calibration-for-lens-findings)

---

## Scope rules per lens

Mandate #3 (stay scoped to the diff) applies, with per-lens extensions — some lenses are meaningless on a diff hunk alone:

| Lens | Scope |
| --- | --- |
| `perf`, `tests` | Changed files + the call sites of changed exports. |
| `dead-code` | Changed files, plus a repo-wide `Grep` for each symbol the diff **removes the last caller of** or **exports without any importer**. |
| `debt` | Changed files; duplication checks may grep the repo for near-identical siblings of code the diff adds. |
| `deps` | The manifests the diff touches (`package.json`, lockfiles); at `deep` depth, the whole manifest. |
| `dx` | Repo-level config only when the diff touches it (CI files, lint config, scripts) — plus one repo-level candidate if there is no working verification command at all. |

When the user names an **area** (e.g. `frontend dead-code`), scope = that area's files regardless of the diff — the user is asking for a targeted sweep, not a diff review. Say in the report which scope was used.

---

## Lens: perf — Performance

Algorithmic and architectural wins, not micro-optimizations.

- **N+1 patterns**: query/fetch per item inside loops or per list-row rendering; missing batching or dataloader.
- **Wrong complexity**: nested scans over the same collection; repeated `find`/`filter` inside hot loops where a Map-keyed lookup belongs.
- **Caching gaps**: identical expensive computations or fetches repeated per request/render; missing memoization at clear function boundaries.
- **Payload size**: over-fetching (select-*, full objects where IDs suffice), missing pagination on unbounded lists, large JSON shipped to clients.
- **Frontend**: heavyweight deps for trivial use, missing code-splitting on rarely-hit routes, unoptimized images/fonts, client-side fetching for data available at render time, render waterfalls.
- **Backend**: synchronous work that belongs in a queue; missing indexes implied by query patterns (flag as needs-info — don't claim without schema evidence); connection-per-request where pooling exists.

## Lens: tests — Test Coverage

The goal is not a percentage — it's *which untested changed code is dangerous*.

- Changed critical-path code (money, auth, data mutation, tenant scoping) with zero or trivial coverage.
- Changed modules with high churn (`git log --oneline -- <file> | wc -l`) and no tests — top regression risk.
- Tests the diff adds that assert nothing meaningful, mock so heavily they test the mocks, or use flaky patterns (real timers, real network, order dependence).
- Tests the diff **weakens**: assertions removed, `.skip` added, tolerances loosened without explanation.
- Missing test-layer fit: a pure function change tested only through a slow integration path, or a cross-package wire change with no guard updated on both sides (the profile's boundary list says where those guards live, and says when there are none).
- **A state-changing test that never re-reads the observable.** A test that awaits a create, update, delete, publish or sync and asserts only on that call's return value has tested the return value. One measured census found 26 of 32 mutating test functions never re-read what they changed, and a sweep of 7 mutating operations found 3 that returned success while changing nothing.
- **An assertion that recomputes its expectation the way the code does**, so it passes by construction and can never disagree with the implementation. Expected values come from a literal, a stored fixture, or a separately written derivation.
- **A test double at the wrong boundary.** Mock at system boundaries — the network, the clock, an external API — and not your own modules. The tell is a test that breaks on a refactor when behaviour did not change. A harness that disables network access altogether is a specific trap: from inside it, "never makes a request" and "makes exactly the right request" look identical.
- **No correct seam is itself the finding.** When a regression test cannot be placed where the bug actually occurs at the call site, say so rather than writing a test somewhere adjacent — a test at the wrong seam gives false confidence, and the architecture preventing the correct one is the more useful thing to report.

## Lens: dead-code — Dead Code

- Symbols the diff orphans: the last caller of a function/component was removed but the definition remains.
- Exports with no importer anywhere in the workspace — grep every package before claiming, since two packages can consume each other's shapes without importing each other. Exclude framework-magic files, which are reachable with no direct caller: file-based routes and layouts, decorator or annotation registration, DI container providers, scheduled jobs declared in deployment config, ORM model registration, and plugin or tool registries. `verification-loop.md` Gate 5 carries the full list.
- Feature flags fully rolled out (always-true/always-false) but still branching.
- Commented-out code blocks the diff adds or leaves behind, with no explanation.
- Dependencies in the manifest no longer imported anywhere.
- Unreachable branches: conditions that types or earlier guards make impossible.

## Lens: debt — Tech Debt & Architecture

- **Duplication**: the diff re-implements logic that already exists (grep for near-identical functions/components before writing the candidate — cite both locations); divergent copies that have drifted.
- **Layering violations**: UI importing data-layer internals, new circular dependencies, additions to a "utils" junk-drawer module with high fan-in.
- **God objects**: the diff grows a file already an order of magnitude larger than the repo median; functions gaining double-digit parameters or deeper conditional nesting.
- **Inconsistent patterns**: the diff introduces a third way of doing data fetching / error handling / styling when the repo has a converged pattern — cite the exemplar file the diff should have followed.
- **Abstraction mismatches**: a premature abstraction with a single implementation, or a change that had to touch N files in lockstep because an abstraction is missing.

### The smell baseline

The five bullets above are what this repo's own shape suggests. Underneath them sits a fixed
catalogue that applies even when a repo documents nothing: the code smells from Fowler's
*Refactoring*, ch. 3. It is here because the bullets above are mostly structural, and half of what
makes a diff hard to live with is naming and coupling that no layering rule catches.

Two rules bind it, and they are what keep it from becoming a style cudgel:

- **The repo overrides.** A documented repo standard always wins. Where the repo endorses something
  the baseline would flag, suppress the smell rather than reporting a conflict.
- **Always a judgement call.** Each of these is a labelled heuristic ("possible Feature Envy"),
  never a hard violation, and it carries the lower confidence that implies. A finding that cannot
  quote the hunk it is about is not a finding.

Read each as *what it is* → *how to fix*, and match against the diff:

- **Mysterious Name** — a function, variable or type whose name does not reveal what it does or
  holds. → rename it; if no honest name comes, the design is murky and that is the real finding.
- **Duplicated Code** — the same logic shape in more than one hunk or file. → extract the shape,
  call it from both. (Overlaps the Duplication bullet above; report once.)
- **Feature Envy** — a method reaching into another object's data more than its own. → move the
  method onto the data it envies.
- **Data Clumps** — the same few fields or params travelling together, a type wanting to be born.
  → bundle them into one type and pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves
  its own type. → give the concept a small type of its own.
- **Repeated Switches** — the same `switch` or `if`-cascade on the same type recurring across the
  change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forcing scattered edits across many files in the diff.
  → gather what changes together into one module.
- **Divergent Change** — one file edited for several unrelated reasons. → split it so each module
  changes for one reason.
- **Speculative Generality** — abstraction, parameters or hooks added for needs the spec does not
  have. → delete it and inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller should not depend on. → hide the
  walk behind one method on the first object.
- **Middle Man** — a class or function that mostly delegates onward. → cut it and call the real
  target directly.
- **Refused Bequest** — a subclass or implementer ignoring or overriding most of what it inherits.
  → drop the inheritance and use composition.

## Lens: deps — Dependencies & Migrations

- New dependencies duplicating one already in the manifest (two date libs, two HTTP clients).
- Abandoned dependencies (archived repo, no release in years) newly added on critical paths.
- Deprecated APIs in use that have announced removal timelines.
- Major-version lag on core framework/runtime **only when it has a real cost** (EOL, security-fix cutoff, blocks another finding's fix) — not every minor bump.
- Lockfile/manifest drift; version-pinning inconsistencies across a monorepo.
- Run the ecosystem audit read-only at `deep` depth, using the repo's own package manager (`npm audit`, `pnpm audit`, `yarn npm audit`, `cargo audit`, `pip-audit`); report only critical and high advisories affecting reachable runtime code.

## Lens: dx — DX & Tooling

- Missing or broken typecheck script, lint config, formatter — when the diff's own quality suffered visibly for it.
- Setup drift the diff introduces: new required env var with no `.env.example` entry, README steps now wrong.
- Logging regressions: structured logging replaced with bare `console.log` on a service, error swallowed where a correlation ID used to flow.
- Slow-feedback additions: a new test suite with no watch mode, CI steps without caching.

---

## Severity calibration for lens findings

Lens findings skew lower-severity than correctness/security — calibrate accordingly and respect `output-format.md`:

| Finding class | Ceiling |
| --- | --- |
| Perf bug under expected production load | HIGH (CRITICAL only if guaranteed unbounded on user input) |
| Missing tests on changed critical path | MEDIUM (never HIGH by itself) |
| Dead code, duplication, layering, inconsistency | MEDIUM |
| Commented-out code, minor DX friction | LOW |
| Vulnerable dependency (critical advisory, reachable) | HIGH |

If a lens sweep produces more than ~5 LOW candidates, consolidate them into one multi-instance candidate per lens (Mandate #4) — lens noise is the fastest way to bury the real CRITICAL.

---

## Reporting what a lens could not check

Each lens that ran reports one of the four states in `coverage.md`. Two are common here and both
report as themselves rather than as clean.

A `perf` claim about a missing index is `no-oracle` unless the diff or the schema file declares the
indexes either way — the query implies one, and nothing available decides whether it exists. A
`deps` advisory sweep is `not-checked` when the ecosystem audit did not run, which is every depth below
`deep`. A `dead-code` claim rests on the grep you ran, so state the pattern and the scope: absence
from what you searched is *not found in what I searched*, never *not present*.
