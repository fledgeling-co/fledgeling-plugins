# F25-065 upstream DISTINCT ADDITIONAL review — FAIL

**Verdict: FAIL** for exact cumulative implementation
`4fabc428be3ee0a0edc5a12633bbb33524b21b54`.

The cumulative source-bound scope mechanism remains fail-closed for strict schema drift, exact
caller posture, reader-before-helper ordering, configured reader trailing closures, and the prior
function-reference/accessor/control-pattern cases. Separately bound helper calls still accept Swift
trailing closures, and ordinary parenthesized readers still clear a correctly bound helper scope.

## Distinct blocking false green

The exact implementation accepts a parenthesized reader call after any unmatched `{` as an
executable caller observation. A valid stored closure therefore clears the attributed helper even
when the closure is never invoked:

```swift
private func seed() { store() }
func testMeasure() {
    seed()
    let observation = { read() }
    _ = observation
}
```

Swift typechecks the complete fixture with exit 0. The direct scanner and public
`vacuity-check.py <campaign> --gate` both accept the exact source-bound attributed-helper record;
the CLI exits 0 and reports no invalid scope. Constructing a closure does not execute its body, so
the helper mutation receives observation credit without any read. The valid opposite stores the
same closure and calls `observation()`; it also exits 0. A second deterministic control-flow probe,
`if false { read() }`, exposes the same false credit through an unreachable branch.

This blocker is independent of the later primary receipt at `66bb795`, which found the distinct
Unicode argument-label function reference. Both findings apply to exact `4fabc42`.

## Cumulative checks

Configured readers remain parenthesized-only: `read { configure() }` fails the public gate, while
`read()` succeeds. A helper invoked as `seed { configure() }` with a later `read()` succeeds. A
reader appearing only before the helper fails. Unknown top-level and scope-record fields fail
closed, and flipping the bound caller's `testEntry` posture fails the public CLI.

Four scanner-source mutants were created from `git show 4fabc42` in separate temporary trees. They
drop reader call syntax, allow label-placeholder references, restore configured-reader trailing
closures, or bypass invocation context. Each makes the permanent attributed-helper test fail for
the intended substantive assertion. The shared worktree source was never mutated by this review;
its dirty implementation/docs/test files belonged to the concurrent repair lane and were left
untouched.

The exact-snapshot focused suite passed **21/21 twice**, and the portable full suite passed
**114/114 twice**. The Perch corpus reports **108** valid scope records, **0** invalid scope
records, **4** blind Swift bodies, and the independent uncensused **REQ-056**, so the gate retains
five findings and exits 1. Plugin, marketplace, and committed catalogue versions are all
**0.16.2**; the permanent catalogue parity test passed in all four suite runs. Catalogue
regeneration itself was not rerun because the isolated archive has no `yaml` dependency and this
review prohibited installs and cache mutation.

CP §7 self-review covered only the new evidence bundle: exact reviewed-hash binding, public CLI
semantics, valid Swift opposites, strict schema/caller binding, mutation discrimination, temporary
isolation, log/receipt agreement, and staged-path isolation. This is a same-family degraded review.
I reused unrelated F25-063, F25-066, F25-057, F25-034, F25-064, and F25-067 context and make no
out-of-family claim. The scanner remains lexical and does not prove receiver identity, type
resolution, control-flow reachability, effect causality, or reader independence. No implementation,
install, publish, push, cache, native app, provider, Keychain, release, or live action was performed.
