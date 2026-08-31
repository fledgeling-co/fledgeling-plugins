# F25-065 upstream reader repair — fresh primary recheck

**Verdict: FAIL** against exact implementation `2de5a2e6d0ee8282232e3fd13280653b729ced62`.
The earlier primary FAIL `dd80213bd27aa880b6227aa4b961f649e0d314a0` against `68c0c5b` remains byte-preserved. I previously performed that related primary and reused unrelated review context here, so this review is same-family degraded and makes no out-of-family independence claim.

## Blocking false green

`has_reader_call` treats any configured reader stem followed by `{` as a trailing-closure call. That lexical shape also occurs in a Swift control statement. This valid caller has no reader invocation:

```swift
private func seed() { store() }
@Test func measure() { seed(); let read = false; if read { print("x") } }
```

A fully bound `attributed-helper` record through the public `vacuity-check.py <campaign> --gate` CLI exits **0**, reports the scope accepted, and removes the helper mutation from the blind denominator. The acceptance is unjustified: `if read { ... }` evaluates a Boolean and does not call a reader. The repair therefore closes the two prior false greens but introduces or exposes another call-shape false green with the same denominator consequence.

## Required boundaries and binding

Public CLI probes establish:

- `seed(); let already = 1`, `seed(); already()`, and `seed(); read` now exit 1 with `INVALID SCOPE`.
- qualified `Fixtures.read()` and `Fixtures.read { configure() }` after the helper exit 0.
- reader-before-helper, comment-only reader, and string-only reader each exit 1.
- falsy configured scope values (`false`, `0`, object, array), Boolean version/offset, integer `testEntry`, unknown fields/classification, empty reference hash, stale body/call fingerprint/call offset, unmatched file, and duplicate scope each exit 1.
- six exact-source mutants are rejected by substantive assertions, including removal of the identifier boundary and removal of required call syntax. The scanner source is restored byte-for-byte.

## Suites, corpus, and versions

The focused Swift-body suite passed **21/21 twice**. The full portable suite passed **114/114 twice**. The Perch corpus accepted **108** scope records with no `INVALID SCOPE`, retained exactly **four** blind bodies plus uncensused **REQ-056**, and exited 1 with five expected findings. Catalogue regeneration was byte-stable; plugin manifest, marketplace, and generated catalogue all report **0.16.2**.

Logs and machine-readable details are in `receipt.json`, `probe.json`, and the adjacent suite/corpus/catalogue artifacts.

## Limits

This was a lexical scanner review; it did not attempt Swift type/receiver resolution, reader independence, or output causality. I did not install, publish, edit caches, push, merge, rebase, run native/provider/Keychain/app work, or run a live campaign.
