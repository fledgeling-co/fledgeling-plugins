# F25-065 upstream parenthesized-only repair — fresh primary review

**Verdict: FAIL** against exact implementation `d9f3d87adc96687be6fb0cfbbc998bca8249822f`.

I performed repeated related primary failures and reused unrelated context. This review is same-family degraded and makes no out-of-family independence claim. `e800d42` is distinguished as related additional-review evidence.

## Blocker 1: autoclosure false credit

```swift
private func seed(_ observation: @autoclosure () -> Int) { store() }
@Test func measure() { seed(read()) }
```

Swift captures `read()` into the autoclosure; `seed` never invokes it. The complete fixture passes `swiftc -typecheck` with exit 0. The public vacuity CLI exits 0 and accepts the attributed helper because reader search begins immediately after the consumed `seed(`. Parenthesized helper shape alone therefore does not prove that a nested argument expression executes.

## Blocker 2: current Perch corpus is invalid

The independent Perch run parses 108 scope records and retains the four blind bodies plus REQ-056, but also emits **10 INVALID SCOPE** findings for `WorkerSupervisorTests.swift:withRetryStore`, producing 15 total findings. Those current caller bindings use the now-refused helper shape.

The author `reader-call-repair9/perch-corpus.log` contains the same ten invalid rows and `findings=15`, while its receipt claims `invalidScopes: 0` and `wholeFindings: 5`. The evidence receipt is contradicted by its own log.

## Other boundaries

Direct and qualified parenthesized helper calls followed by real parenthesized readers accept. Helper trailing closures, reader trailing closures, conditional compilation, stored/unreachable closures, captures, IIFEs, defer, loops, selectors, patterns, declarations, defaults, and function references reject. Nested IIFE/capture/defer/loop executions are deliberate conservative false negatives.

Strict schema and exact caller checks reject all malformed, stale, duplicate, and unmatched records. Seven temporary-copy source mutants cover call syntax, reference placeholders, reader/helper trailing closures, nested depth, conditional compilation, and invocation context; all fail substantive assertions and restore source exactly.

Focused tests pass **21/21 twice** and full portable tests pass **114/114 twice**. Version surfaces remain **0.16.2** and catalogue regeneration is byte-stable.

## Limits

This was lexical review plus Swift typechecking. It does not establish reader independence or output causality. No install, publish, cache edit, push, merge, rebase, native/provider/Keychain/app work, or live campaign was run.
