# F25-065 upstream Unicode/nested repair — fresh primary review

**Verdict: FAIL** against exact implementation `2b186f8b92c2f87544b3f244289cee15a5bc62d6`.

I performed repeated related primary failures and reused unrelated context. This review is same-family degraded and makes no out-of-family independence claim. The earlier `8f5e68f` commit is distinguished as related additional-review evidence.

## Blocking false green

A trailing-closure helper call consumes its opening brace in the bound helper match before the caller suffix is passed to reader depth analysis:

```swift
private func seed(_ body: () -> Void) { store() }
@Test func measure() { seed { read() } }
```

`seed` does not invoke `body`, so `read()` never runs. The complete Swift fixture typechecks with exit 0. The public vacuity CLI nevertheless exits 0 and accepts the attributed helper. Because the suffix begins after `seed {`, the inner reader starts at apparent normalized depth zero and falsely receives top-level credit.

## Cumulative grammar and depth checks

Unicode, escaped, ASCII single-label, and multiple-label function references reject. Real single/multiple labeled calls accept. Operator tokens are not valid Swift argument labels; the compiler probe rejects that candidate.

Stored closure readers, literal-false branches, nested declarations/defaults, closure captures, and immediately invoked closures reject under the conservative top-depth contract. The capture and IIFE outcomes are deliberate false negatives. A reader after a completed qualified trailing-closure helper remains valid. Reader trailing closures remain refused.

Strict schema and exact caller probes reject falsy configured paths, incorrect primitive types, unknown fields/classification, empty references, stale body/fingerprint/offset, unmatched files, and duplicates. Five temporary-copy source mutants independently arm call syntax, reference placeholders, reader trailing-closure refusal, nested-depth refusal, and invocation context; all fail substantive assertions and restore source exactly.

## Suites, corpus, and versions

Focused tests passed **21/21 twice** and full portable tests passed **114/114 twice**. The Perch corpus accepts **108** scopes with no invalid records and retains four blind bodies plus REQ-056. Plugin, marketplace, and catalogue remain **0.16.2**; catalogue regeneration is byte-stable.

## Limits

This was lexical top-level analysis plus Swift typechecks. Nested IIFE and capture calls are deliberately false-negative, and no reader independence or output-causality proof is attempted. No install, publish, cache edit, push, merge, rebase, native/provider/Keychain/app work, or live campaign was run.
