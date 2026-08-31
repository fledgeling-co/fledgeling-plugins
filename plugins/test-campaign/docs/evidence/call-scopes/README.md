# Auditable blind-call scopes — author evidence

Version0.16.2 adds exact per-call scope records. Body, call and referenced producer/contract hashes
must match; stale, duplicate, unmatched or ambiguous records remain gate findings. A scope removes
one occurrence and the ordinary last-mutation/later-reader analysis then restarts over earlier calls.
Attributed-helper records additionally bind an exact current caller body and named helper-call
fingerprint, and that caller must contain a configured reader after the helper call. Reports retain
the raw mutating-body denominator and count scoped calls by classification.

Target and caller records bind the parser's explicit-test posture so removing `@Test` outside an
otherwise identical body invalidates the scope. Caller bindings recognize parenthesized and Swift
trailing-closure invocations; this remains lexical and does not claim overload or receiver identity.

Twenty focused tests and the complete114-test plugin gate pass. Three original disposable actual-source
faults are red: ignoring the call fingerprint, suppressing the whole body, and globally excluding
`record`. Import/syntax failures receive no fault credit. CP §7 review covered loader validation,
path/hash failures, overload/body identity, exact-call matching, helper posture, denominators and CLI
gate propagation. Hashes bind evidence but do not prove Swift receiver identity or output causality;
review rationale remains required. Perch scope records and contract faults are a separate dependent
slice after F25-064. Nothing was installed or published.

Primary review found three author gaps: Python booleans passed as integer schema fields,
configured-but-falsy scope paths were treated as absent, and attributed helpers did not bind their
named callers. The repaired suite exercises all three through the public loader or CLI and rejects an
arbitrary non-caller body. Follow-up CP §7 and Perch corpus review added five repair mutants: caller-later-reader,
target and caller test-entry posture, strict posture schema, and trailing-closure caller matching.
Fresh fixtures reject all five, including a reader placed only before the helper call. The generated catalogue
version is kept at 0.16.2 with both manifests.
