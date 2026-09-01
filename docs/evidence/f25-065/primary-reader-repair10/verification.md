# F25-065 upstream primary review — direct-helper repair

**Verdict: FAIL** against exact implementation `de4de21e35d314cbefc155ab0016de222ca3fd59`.

This review reused unrelated context and follows repeated reviews from the same model family. It is degraded same-family primary evidence and makes no out-of-family claim.

## Blocking false green

The public CLI accepts this valid Swift scope and grants `attributed-helper` credit:

```swift
private func seed() -> Int { store(); return 1 }
@Test func measure() -> Int { return seed(); read() }
```

`seed()` is in return position. The helper invocation-context check permits that position, and the later-reader scan starts after the balanced `seed()` call. The suffix therefore loses the `return` token and treats `read()` as executable even though Swift reports it as unreachable. The independent runtime fixture prints `value=1 reads=0`; the public CLI nevertheless exits 0.

This violates the source-bound reader contract. Direct top-level parenthesized syntax and balanced arguments do not establish that a later lexical reader executes.

## Verification

- Public-CLI boundary matrix covers accepted direct parenthesized readers/helpers and refusals for earlier, masked, identifier, declaration, control-flow, conditional, stored, nested, autoclosure, trailing-closure, unreachable and function-reference forms.
- Sixteen strict schema and exact-binding cases reject.
- Nine isolated actual-source mutants fail and the scanner source is restored byte-for-byte.
- Focused suite: 21 tests twice, both exit 0.
- Full portable suite: 114 tests twice, both exit 0.
- Corrected Perch corpus at `c30595e14403240d7933c1d20ec4728eb3281770`: both runs are byte-identical and report 108 scope records, 0 invalid scopes, 0 attributed helpers, 56 failure sentinels, four blind bodies plus REQ-056, and five findings (expected exit 1).
- Plugin manifest, marketplace, and committed catalogue all say 0.16.2. Catalogue regeneration could not run because the local `yaml` dependency is absent; no install or cache change was allowed, and the attempted command left catalogue bytes unchanged.

No implementation, install, publish, cache, main, native, provider, Keychain, or app changes were made.
