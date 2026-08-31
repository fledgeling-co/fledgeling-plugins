# F25-065 upstream control-condition repair — fresh primary review

**Verdict: FAIL** against exact implementation `35d7159d6354cb776bf5a7ec1e5de67315c6388a`.

I performed the two related earlier primary failures and reused unrelated review context, so this review is same-family degraded and makes no out-of-family independence claim. The earlier evidence commits `dd80213` and `4c5ed87` remain preserved.

## Blocking false green

The repair correctly refuses the ambiguous trailing-closure-shaped control condition. However, the remaining parenthesized reader regex accepts an enum associated-value pattern as though it were a reader invocation:

```swift
private func seed() { store() }
@Test func measure() {
    seed()
    switch value {
    case .read(let x): print(x)
    default: break
    }
}
```

This is valid Swift pattern matching; `.read(let x)` destructures `value` and does not call a configured reader. A fully source-bound `attributed-helper` record through the public `vacuity-check.py <campaign> --gate` CLI exits **0**, reports the scope accepted, and removes the helper mutation from the blind denominator. The result is therefore materially false green.

## Cumulative boundaries

Public CLI probes confirm that the repaired `if read { ... }` condition now rejects. Identifier substrings, `already()`, bare reader names, reader-before-helper, comment-only and string-only readers, and a nested reader function declaration also reject. A qualified parenthesized configured reader call accepts, and a trailing-closure helper binding followed by `read()` accepts.

Strict schema and binding probes reject configured falsy scope values, Boolean version/offset, integer `testEntry`, unknown fields/classification, empty reference hash, stale body/fingerprint/offset, unmatched files, and duplicate scopes. Seven actual-source mutants fail substantive assertions, covering identifier boundaries, call syntax, the withdrawn ambiguous trailing reader shape, exact rechecking, executable caller masking, test posture, and raw-denominator preservation. The scanner is byte-restored.

## Suites, corpus, and versions

The focused suite passed **21/21 twice**, and the full portable suite passed **114/114 twice**. The Perch corpus accepts **108** scope records with no invalid-scope diagnostics and retains exactly four blind bodies plus REQ-056, for the expected five findings. Catalogue regeneration is byte-stable; plugin manifest, marketplace, and catalogue all report **0.16.2**.

Machine-readable results and exact logs are adjacent in `receipt.json`, `probe.json`, suite logs, corpus log, and catalogue log.

## Limits

This is a lexical scanner review. It does not resolve Swift types or receivers, reader independence, or output causality. I did not install, publish, edit caches, push, merge, rebase, run native/provider/Keychain/app work, or run a live campaign.
