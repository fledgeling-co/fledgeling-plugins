# F25-065 upstream qualified-reader repair — fresh primary review

**Verdict: FAIL** against exact implementation `08007d341f2bac53b6d19d7b0dd9087a8e427085`.

I performed the three related earlier primary failures and reused unrelated review context. This repeated review is same-family degraded and makes no out-of-family independence claim; all earlier failure evidence remains preserved.

## Blocking false green

The conservative unqualified-parenthesized regex correctly refuses the earlier enum pattern. It still accepts a Swift selector reference as though it invoked the configured reader:

```swift
seed()
let selector = #selector(read(_:))
```

`#selector(read(_:))` forms an Objective-C selector referencing `read`; it does not execute the method or observe state. A complete `NSObject` fixture with the `@objc` method typechecks under `swiftc -typecheck` with exit 0. The same caller through the public `vacuity-check.py <campaign> --gate` CLI exits **0**, accepts the attributed-helper record, and excludes its mutation from the blind denominator. This is a material semantic false green.

## Cumulative checks

Public CLI probes show that the unqualified parenthesized `read()` posture accepts and a qualified trailing-closure helper binding followed by `read()` accepts. Enum associated-value patterns, `if read {}`, identifier substrings, `already()`, bare names, reader-before-helper, comments, strings, and nested declarations reject.

Strict schema and exact caller probes reject configured falsy scope values, Boolean version/offset, integer `testEntry`, unknown fields/classification, empty reference hash, stale body/fingerprint/offset, unmatched files, and duplicates. Eight exact-source mutants fail substantive assertions, covering identifier and qualification boundaries, required call syntax, trailing-shape refusal, exact rechecking, caller masking, test posture, and raw denominator preservation. Scanner bytes are restored.

## Suites, corpus, and versions

The focused suite passed **21/21 twice** and full portable suite passed **114/114 twice**. The Perch corpus accepts **108** scope records with zero invalid scopes and retains four blind bodies plus REQ-056. Plugin, marketplace, and generated catalogue report **0.16.2**; catalogue regeneration is byte-stable.

## Limits

This was a lexical scanner review plus one Swift typecheck. It does not resolve receiver semantics, reader independence, or output causality. I did not install, publish, edit caches, push, merge, rebase, run native/provider/Keychain/app work, or run a live campaign.
