# F25-065 upstream accessor/default repair — fresh primary review

**Verdict: FAIL** against exact implementation `4fabc428be3ee0a0edc5a12633bbb33524b21b54`.

I performed the six related earlier primary failures and reused unrelated context. This repeated review is same-family degraded and makes no out-of-family independence claim.

## Blocking false green

The function-reference placeholder grammar only recognizes ASCII-leading labels. Swift identifiers, including argument labels, may be Unicode:

```swift
seed()
let function = read(λ:)
```

This references `read` and does not invoke it. A complete fixture passes `swiftc -typecheck` with exit 0. Through the public vacuity CLI, the exact attributed-helper scope exits 0 and excludes the helper mutation. The negative lookahead's `[A-Za-z]` label rule therefore grants false credit at an accepted assignment boundary.

## Cumulative boundaries

The repaired local `get {}` accessor rejects. Same-line and split-line nested default arguments reject, as does a valid split `func\nread()` nested declaration; Swift typechecks the split controls, confirming conservative masking rather than invalid syntax. Selectors, enum patterns, control contexts, function references with ASCII or escaped labels, nested calls, identifiers, bare names, comments, strings, and reader-before-helper reject.

Real parenthesized `read()`, assigned single/multiple labeled calls, and qualified or trailing-closure helper bindings accept. Reader trailing closures are intentionally refused by the current contract.

Strict schema and exact caller probes reject falsy configured paths, incorrect primitive types, unknown fields/classification, empty references, stale body/fingerprint/offset, unmatched files, and duplicate scopes. Four exact-source mutants independently arm call syntax, placeholder rejection, reader trailing-closure refusal, and invocation context; all fail substantive assertions and restore scanner bytes.

## Suites, corpus, and versions

Focused tests passed **21/21 twice** and the full portable suite passed **114/114 twice**. The Perch corpus accepts **108** scopes with no invalid records and retains four blind bodies plus REQ-056. Plugin, marketplace, and catalogue remain **0.16.2**, with byte-stable catalogue regeneration.

## Limits

This was lexical grammar/context review plus Swift typechecks. Ambiguous nested calls remain deliberately false-negative, and the scanner does not establish reader independence or output causality. No install, publish, cache edit, push, merge, rebase, native/provider/Keychain/app work, or live campaign was run.
