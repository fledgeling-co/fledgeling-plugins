# F25-065 upstream function-reference repair — fresh primary review

**Verdict: FAIL** against exact implementation `1e6ed483a6b9ba4dcfe1590323c7eb7dc6261ca9`.

I performed the five related earlier primary failures and reused unrelated context. This repeated review is same-family degraded and makes no out-of-family independence claim.

## Blocking false green

The call grammar accepts trailing-closure shape after an opening brace. That also accepts a local computed-property accessor declaration for the configured default reader `get`:

```swift
seed()
var value: Int {
    get { 1 }
}
```

`get {}` declares an accessor; it does not invoke a reader or observe the helper mutation. A complete fixture passes `swiftc -typecheck` with exit 0. Through the public vacuity CLI, the exact attributed-helper scope exits 0 and excludes the helper mutation from the blind denominator.

## Function-reference and call controls

Single-placeholder `read(_:)`, multiple-label `read(first:second:)`, and an escaped-label reference all typecheck or represent valid reference grammar and reject through the public CLI. Real assigned calls `read(label: input)` and `read(first: one, second: two)` accept. Ordinary `read()` and trailing-closure `read {}` also accept.

Selectors, enum patterns, control conditions, local function declarations, nested calls, identifier substrings, bare names, reader-before-helper, comments, and strings reject. Strict schema and exact caller probes reject falsy configured paths, wrong primitive types, unknown fields/classifications, empty references, stale body/fingerprint/offset, unmatched files, and duplicate scopes.

Three exact-source mutations independently prove call syntax, function-reference placeholder rejection, and invocation context are live. All fail substantive assertions and restore scanner bytes exactly.

## Suites, corpus, and versions

Focused tests passed **21/21 twice** and the full portable suite passed **114/114 twice**. The Perch corpus accepts **108** scopes with no invalid records and retains four blind bodies plus REQ-056. Plugin, marketplace, and catalogue versions remain **0.16.2**, with byte-stable catalogue regeneration.

## Limits

This was lexical grammar/context review plus Swift typechecks. Ambiguous nested calls remain deliberately false-negative, and the scanner does not establish reader independence or output causality. No install, publish, cache edit, push, merge, rebase, native/provider/Keychain/app work, or live campaign was run.
