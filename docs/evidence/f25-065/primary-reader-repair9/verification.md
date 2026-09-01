# F25-065 executable-helper repair — fresh primary review

**Verdict: FAIL** against exact implementation `6f8013101300cc08da0b51d64f58755eb81fa248`.

I performed repeated related primary failures and reused unrelated context. This review is same-family degraded and makes no out-of-family independence claim.

## Blocking order false green

```swift
private func seed(_ body: () -> Void) { body(); store() }
@Test func measure() { seed { read() } }
```

The helper invokes its closure, but the reader runs **before** the scoped `store()` mutation. It cannot observe that mutation. The fixture passes `swiftc -typecheck`, while the public vacuity CLI exits 0 and accepts the attributed helper. `invokes_trailing_closure` records only whether a direct invocation exists anywhere in the helper body; it does not compare that invocation with the exact scoped target `callOffset`.

## Cumulative behavior

A trailing helper whose body calls the closure after `store()` accepts. Non-invoking trailing helpers, autoclosure arguments, helper calls stored in closures or inactive directives, readers after return, conditional readers, nested closures, captures, IIFEs, loops, defer, declarations, patterns, and references reject. Direct/qualified parenthesized helpers followed by real calls accept. Balanced helper arguments prevent argument readers from counting as later observations.

Strict schema and exact caller probes reject malformed, stale, duplicate, and unmatched records. Ten temporary-copy source mutants independently arm call syntax, reference placeholders, reader trailing closure, nested depth, conditional compilation, helper execution context, closure-invocation proof, balanced call tails, terminators, and general invocation context. All fail substantive assertions and restore scanner bytes.

Focused tests pass **21/21 twice** and full portable tests pass **114/114 twice**. The Perch corpus now reproduces **108 scopes, zero invalid scopes, four blind bodies, REQ-056, and five findings**. The repair-9 receipt honestly retains its prior 10-invalid/15-finding values and adds an explicit correction. Version surfaces remain **0.16.2** and catalogue generation is byte-stable.

## Limits

The scanner does not relate helper closure invocation order to the exact scoped mutation offset, nor prove receiver identity, reader independence, or output causality. No install, publish, cache edit, push, merge, rebase, native/provider/Keychain/app work, or live campaign was run.
