# F25-065 distinct additional review — terminal-helper repair

## Verdict

**FAIL** against exact implementation `42ac3ea7aeff2c1a2db23ea83121a2f762839f1f`.

The repair rejects same-line `return seed()` and `throw seed()` and closes every tested trailing-closure spelling. Swift permits a return or throw expression to continue on the next line, however, and the helper guard loses that terminal when it splits the current statement at the newline.

## Blocking false green

Both exact public-CLI cases below exit 0 without an invalid scope:

```swift
@Test func measure() -> Int {
    return
        seed()
    read()
    return 0
}
```

```swift
@Test func measure() throws {
    throw
        seed()
    read()
}
```

`helper_invocation_context` computes the statement with `re.split(r"[;\n{}]", source[:start])[-1]`. For these valid multiline expressions, that suffix is empty before `seed`, so neither terminal is visible. The later-reader search begins after the balanced helper call and likewise cannot see it. The compiled runtime fixture warns that both reads are unreachable and finishes with two stores and zero reads.

A block-comment-plus-newline return spelling also passes. Same-line return and throw controls reject, which binds the failure to the newline split rather than to loss of the entire guard.

## Trailing, direct, and balanced boundaries

The public CLI rejects all tested unsupported trailing forms: unparenthesized, parenthesized, qualified parenthesized, comment-separated, newline-separated, and multiple trailing closures. A direct helper followed by a reader and a helper with balanced nested arguments followed by a reader pass. A reader only inside helper arguments and a helper inside a false branch reject.

## Gates and corpus

- Focused Swift/public-CLI suite: 21/21 twice.
- Full safe suite: 114/114 twice.
- Eleven actual-scanner mutants in an isolated extracted tree: all rejected; source restored byte-for-byte to SHA-256 `47354299b1aac7cb96cfa0b08cb8ea142d288e42a66b7d72d29ddc879b2990a5`.
- Corrected Perch corpus at `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical runs, 108 scopes, 0 invalid, 0 attributed helpers, 22 direct outputs, 56 failure sentinels, 30 fixture values, four blind bodies plus REQ-056, five findings, expected exit 1.
- Plugin, root marketplace, and site catalogue remain at 0.16.2; catalogue parity passes in both full runs.

## Independence, restoration, and limits

This is a repeated same-family degraded additional review. Prior F25-065 and unrelated Fleet context was reused; the multiline terminal attacks, trailing spelling matrix, compiled runtime witness, gates, mutant rerun, and corpus runs were newly executed against the exact snapshot.

All mutations occurred in an isolated archive and restored exactly. The shared implementation was not edited; this commit contains only this additional-review directory and excludes the concurrent primary review directory. No install, publish, push, cache mutation, native app, provider, Keychain, or live campaign action occurred. The scanner deliberately refuses valid nested control-flow and trailing-closure helpers and does not prove receiver resolution, reader independence, or output causality.
