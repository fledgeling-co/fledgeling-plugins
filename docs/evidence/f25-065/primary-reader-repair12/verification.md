# F25-065 upstream primary review — terminal-helper repair

## Verdict

**FAIL** against exact implementation `42ac3ea7aeff2c1a2db23ea83121a2f762839f1f`.

The repair closes same-line `return seed()` and `throw seed()` plus the tested bare and
parenthesized trailing-closure boundaries. It still accepts valid multiline return/throw
expressions because `helper_invocation_context` discards the terminal when it splits the statement
at every newline.

## Blocking false green

The public CLI accepts all four cases below with exit 0, one attributed-helper scope, zero invalid
scopes, and zero findings:

```swift
func testMeasure() -> Int {
    return
        seed()
    read()
    return 2
}
```

```swift
func testMeasure() throws {
    throw
        seed()
    read()
}
```

The same two forms also pass when a block comment begins after `return` or `throw` and ends on the
line containing `seed()`. Swift compiles the comment-newline fixture with exit 0, warns that both
`read()` calls are unreachable, and runtime prints only `1` and `THREW`; neither reader runs.
`probe.json` records the exact public-CLI output and expected/actual exit for every case.

The fault is source-bound: `helper_invocation_context` uses
`re.split(r"[;\n{}]", source[:start])[-1]`. In each multiline expression the selected suffix no
longer contains `return` or `throw`. The balanced suffix then begins after `seed()` and sees the
unreachable `read()` as a later observation.

## Boundaries exercised

- Same-line return and throw refuse with exit 1 and `INVALID SCOPE`.
- Bare `seed {}` and parenthesized `seed() {}` trailing closures refuse.
- Direct and qualified top-level parenthesized helper calls followed by a reader pass.
- A balanced helper argument containing `read()` does not count by itself; a distinct reader after
  the balanced call passes.
- A helper nested in control flow refuses.

These controls isolate the failure to multiline terminal retention rather than a broad loss of
helper context, call balancing, or trailing-closure refusal.

## Gates, mutants, and corpus

- Focused Swift/public-CLI suite: 21 tests, twice, both exit 0.
- Complete safe plugin suite: 114 passed / 0 failed, twice.
- Eleven independently rerun actual-scanner mutants all failed the focused oracle. They cover call
  syntax, function references, reader trailing closures, nested/conditional readers, helper
  execution context, return position, parenthesized helper trailing closure, argument/suffix
  separation, top-level terminators, and invocation context.
- Scanner source restored byte-for-byte after every mutant: SHA-256
  `47354299b1aac7cb96cfa0b08cb8ea142d288e42a66b7d72d29ddc879b2990a5` before and after.
- Corrected Perch corpus `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical
  runs; 108 scopes, 0 invalid scopes, 0 attributed helpers, 22 direct outputs, 56 failure
  sentinels, and 30 fixture values. Both remain honestly red on four blind bodies plus uncensused
  REQ-056: five findings, expected exit 1.

## Independence and limits

This is a repeated same-family degraded primary lane because workflow/out-of-family lanes were not
available in this session. I did not author the upstream scanner repair. This task reused unrelated
F25-034 and F25-015 context; I had earlier authored the separate Perch corpus disposition slice, so
that relationship is disclosed rather than treated as fresh corpus authorship. The public-CLI
probes, compiled runtime fixture, gate runs, mutant runs, and corpus runs here were newly executed
against the named implementation bytes.

Only evidence files were added. The implementation was restored exactly and never committed as
modified. No install, publish, push, cache edit, native app, provider, Keychain, or live campaign
operation occurred. The scanner remains deliberately conservative for nested control flow and
trailing closures and does not claim receiver resolution, reader independence, or output causality.
