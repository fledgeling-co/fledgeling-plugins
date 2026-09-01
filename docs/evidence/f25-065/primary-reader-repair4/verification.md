# F25-065 upstream invocation-context repair — fresh primary review

**Verdict: FAIL** against exact implementation `3524c0276bfe36747ed774e08e56d414b7aa9a23`.

I performed the four related earlier primary failures and reused unrelated review context. This repeated review is same-family degraded and makes no out-of-family independence claim.

## Blocking false green

The two-part call-syntax plus conservative-context contract still mistakes Swift labeled function-reference syntax for invocation at an accepted assignment boundary:

```swift
seed()
let function = read(_:)
```

Swift permits `read(_:)` as a reference to a function with that argument label. It does not call the function or observe state. An independent complete fixture passes `swiftc -typecheck` with exit 0. Through the public vacuity CLI, the exact source-bound attributed-helper record exits 0 and removes the helper mutation from the blind denominator.

## Contract and boundaries

The intended parenthesized `read()` and trailing-closure `read {}` calls accept. Qualified and trailing-closure helper calls remain independently bound and accepted. Selectors, enum patterns, control conditions, local declarations, nested calls, identifier substrings, bare names, reader-before-helper, comments, and strings reject; those conservative false negatives match the documented posture.

Strict schema and exact caller checks reject configured falsy paths, incorrect primitive types, unknown fields/classification, empty references, stale body/fingerprint/offset, unmatched files, and duplicate scopes. Independent actual-source mutations prove both operative conditions are live: dropping call syntax and dropping invocation context each fails a substantive assertion, and scanner bytes restore exactly.

The retained `reader-call-repair4` experiment honestly records `allRejected: false`: three of five redundant-guard mutations survived. It is explicitly described as discarded and receives no fault credit. The operative `reader-call-repair5` evidence records the two live mutations.

## Suites, corpus, and versions

Focused tests passed **21/21 twice** and the full portable suite passed **114/114 twice**. The Perch corpus accepts **108** scopes with no invalid records and retains four blind bodies plus REQ-056. Plugin, marketplace, and catalogue versions remain **0.16.2**; catalogue regeneration is byte-stable.

## Limits

This was lexical call/context review plus one Swift typecheck. Ambiguous nested and qualified calls are deliberately refused, and the scanner does not establish reader independence or output causality. No install, publish, cache edit, push, merge, rebase, native/provider/Keychain/app work, or live campaign was run.
