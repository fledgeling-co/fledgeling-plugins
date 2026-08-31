# F25-065 upstream DISTINCT ADDITIONAL review

**Verdict: PASS** for exact cumulative implementation head
`68c0c5b74b0d143b8738fc7e1c4283a0e2c89b6c`.

The cumulative implementation closes the original and subsequent blockers. A configured scope path
fails closed for malformed or falsy values; schema integer and Boolean fields require exact Python
types; version-one payloads reject unknown top-level fields, unknown record fields, and `callers`
on classifications where that field has no meaning. The strict-schema test restores its valid
producer after the reference-drift case, so the two recorded schema mutants fail their named
assertions rather than an unrelated stale hash.

Each scope binds file, body name, explicit-test posture, full body hash, exact call offset, mutator,
and receiver-plus-call-delimiter fingerprint. A matched scope removes only that occurrence after the
raw mutating-body denominator is counted; the ordinary last-mutation/later-reader pass then runs over
all remaining calls. The independent source mutants prove that dropping the raw denominator,
ignoring the exact offset, or globally excluding `record`, `store`, `apply`, and `update` breaks a
fresh observation. All three mutants changed the real scanner file, failed through assertions, and
restored its exact original SHA-256 in `finally` cleanup.

Attributed helpers bind exact current caller bodies and caller test-entry posture. The named helper
call must survive the Swift comment/literal mask, and a configured reader must occur later in the
masked caller body. Independent boundaries reject a reader only before the call and helper spelling
only in a block comment. A receiver-qualified Swift trailing-closure caller with a later reader is
accepted. Removing `@Test` outside an otherwise unchanged target body invalidates its posture-bound
scope while preserving the raw candidate.

The plugin manifest, marketplace manifest, and generated catalogue all advertise `0.16.2`; the
catalogue builder exits zero. Focused Swift tests passed 20/20 twice and the complete portable gate
passed 114/114 twice. The working source was byte-restored after every fault, and this commit changes
evidence files only.

This is a same-family degraded review. I reused unrelated Perch F25-063, F25-066, F25-057,
F25-034, F25-064, and F25-067 context; no out-of-family lane was used. The mechanism remains lexical:
it does not prove Swift receiver identity, type resolution, effect causality, or reader independence.
No install, publish, cache mutation, native app, provider, Keychain, or Perch corpus application was
performed.
