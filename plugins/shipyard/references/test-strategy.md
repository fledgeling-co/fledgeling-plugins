# Test strategy — the coverage bar for every feature

**Canonical for the whole pipeline.** The planner writes the test strategy against this bar, the
worker builds to it, the verifier grades against it. It exists because coverage percentages are a
vanity metric (a published study found median 77% line coverage alongside median 21% mutation
score) and because AI-written suites tailored to pass the code they ship with catch nothing.

## The portfolio (per feature, planned at plan time)

| Layer | Purpose | Anti-vanity discipline |
|---|---|---|
| Unit | Local logic, validation, boundary values, pure transforms | Expected values from an **independent source of truth** (a known-good literal, a worked example, the spec) — an assertion that recomputes the value the way the code does passes by construction and can never disagree with the code |
| Contract / integration | Service boundaries, schemas, error propagation | Failure paths tested, not just the happy arm |
| **E2E UI (per flow)** | Every user flow, action, and menu in the spec, driven in the repo's own harness (via `/acceptance-e2e`) | Outcome assertions (content and behaviour), never element-existence; green **twice**; a committed spec with no recorded run is a loud failure at the next stage |
| **Visual (per state)** | The state matrix below, per surface | Curated snapshots of the matrix — not screenshots of every page; stable environment; paired with semantic assertions |
| Accessibility | Semantics and keyboard operation | Role/name/state assertions; keyboard paths; axe pass |
| Regression | The observed defect cannot recur | The red→green proof (`evidence-rules.md`) — fails against the pre-fix behaviour |

## The UI state matrix (the design stage produces it; the tests consume it)

Every surface the feature touches enumerates its states, and every cell is either covered or
explicitly waived with a reason:

| Surface | Minimum visual states | Minimum functional assertions |
|---|---|---|
| Navigation / menus | default, active, collapsed/mobile, overflow | keyboard navigation, correct route, focus visibility |
| Forms | empty, valid, invalid, server error, loading, success | validation messages, disabled/submit state, retry |
| Tables / lists | populated, empty, loading, pagination/filter | sort/filter correctness, selection persistence |
| Modals / overlays | closed, open, long-content, destructive confirm | focus trap, escape, outside-click policy, action result |
| Permissions | authorized, unauthorized, expired session | blocked server action, explanatory UI, no data leakage |
| Responsive | desktop, tablet, mobile breakpoints | no clipped controls, equivalent critical action path |

## Seams

Tests are written only at seams the plan named (existing seams preferred, the highest seam
possible, ideal count approaching one). A test at an unconfirmed seam is testing effort spent
where nobody agreed the critical path runs. When a bug has no correct seam to lock it down, that
absence **is the finding** — note it; the architecture is preventing the regression test, and that
goes to the architecture backlog rather than being papered over with a too-shallow test.

## Three anti-patterns, each with its tell

- **Implementation-coupled** — mocks internal collaborators, tests private methods, asserts via a
  side channel. *Tell:* breaks on refactor with behaviour unchanged. Mock only at system
  boundaries (external APIs, time/randomness, a test DB over a mocked one).
- **Tautological** — the assertion recomputes the expected value the way the code does. *Tell:*
  cannot fail while the code exists.
- **Horizontal-sliced** — all tests written, then all implementation. *Tell:* tests assert the
  *shape* of imagined behaviour and go insensitive to real changes. Vertical: one test → one
  implementation → repeat.

## The affected-test sweep (mechanical, mandatory)

Grep the repo's test trees (`e2e/`, `*.spec.*`, `*.test.*`) for every route, component name,
user-visible string, and behaviour the branch changes or **inverts**. Every hit is in scope:
update it to the new contract and RUN it. A spec asserting the behaviour being removed is part of
the diff — leaving it red, or `fixme`'d asserting the old world, is shipping a broken test. A
`fixme` without a ticket reference and a reason comment fails the sweep.

## Acceptance criteria are falsifiable at the base commit

Each AC names the observation that would show it false, and that observation **fails at the
commit the implementer starts from**. An AC that is already true at base, only satisfiable by
another ticket's work, or a restatement of the request grades nothing.
