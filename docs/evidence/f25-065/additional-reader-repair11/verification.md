# F25-065 distinct additional review — direct-helper repair

## Verdict

**FAIL** against exact implementation `de4de21e35d314cbefc155ab0016de222ca3fd59`.

The direct, top-level, parenthesized helper rule closes the trailing-only, nested closure, false branch, `break`/`continue`, and inactive compilation false greens. Balanced helper calls also prevent readers in arguments from counting while preserving a genuine reader after nested arguments. One structural terminator boundary remains unsound.

## Blocking false green

`reader_invocation_context` permits a helper call after `return`, as intended for a returned call. The later-reader search then starts at the byte after the balanced helper call. That slice no longer contains the `return`, so the terminator check cannot reject a subsequent unreachable reader.

The exact public-CLI case below exits 0 with no invalid scope:

```swift
private func seed() -> Int { store(); return 7 }
@Test func measure() -> Int { return seed(); read(); return 0 }
```

A standalone, source-equivalent Swift fixture compiles with the expected unreachable-code warning and runs with `stores=1 reads=0`. Thus the helper mutation executes, but the cited later observation does not. The local bare `swiftc` toolchain cannot import the `Testing` module, so the exact `@Test` spelling is proved through the public CLI and the equivalent `testMeasure` body supplies the compile/runtime proof; this limitation is retained rather than hidden.

The public probe also records that a parenthesized helper followed by a trailing closure and then a reader is accepted, despite the operative documentation saying trailing-closure helper calls are refused. That is a contract mismatch, although the return-tail case alone is sufficient for FAIL.

## Gates and boundaries

- Focused Swift/public-CLI suite: 21/21 twice.
- Full safe suite: 114/114 twice.
- Nine actual-scanner mutants in an isolated extracted tree: all rejected; scanner restored byte-for-byte to SHA-256 `c394af625e90631d9b824d407cf19add41fc645ca5fb027c9448e02b85bfa275`.
- Valid direct helper plus reader and balanced nested arguments plus reader pass.
- Argument-only reader, nested false helper, and pure trailing helper fail closed.
- Corrected Perch corpus at `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical runs, 108 scopes, 0 invalid, 0 attributed helpers, 22 direct outputs, 56 failure sentinels, 30 fixture values, four blind bodies plus REQ-056, five findings, expected exit 1.
- Plugin, root marketplace, and site catalogue remain at 0.16.2; catalogue parity passes in both full runs.

## Independence, restoration, and limits

This is a repeated same-family degraded additional review. Prior F25-065 and unrelated Fleet context was reused; the return-tail attack, exact public-CLI cases, compiled runtime witness, gate runs, mutation rerun, and corpus runs in this receipt were newly executed against the named snapshot.

All scanner mutations occurred in an isolated archive and restored exactly. The shared worktree's tracked implementation and author evidence match `de4de21e`; this commit contains only this additional-review directory. No install, publish, push, cache mutation, native app, provider, Keychain, or live campaign action occurred. The bounded scanner still deliberately refuses valid nested control-flow and trailing-closure helper calls and does not prove receiver resolution, reader independence, or output causality.
