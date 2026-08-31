# Auditable blind-call scopes — author evidence

Version0.16.2 adds exact per-call scope records. Body, call and referenced producer/contract hashes
must match; stale, duplicate, unmatched or ambiguous records remain gate findings. A scope removes
one occurrence and the ordinary last-mutation/later-reader analysis then restarts over earlier calls.
Reports retain the raw mutating-body denominator and count scoped calls by classification.

Seventeen focused tests and the complete114-test plugin gate pass. Three disposable actual-source
faults are red: ignoring the call fingerprint, suppressing the whole body, and globally excluding
`record`. Import/syntax failures receive no fault credit. CP §7 review covered loader validation,
path/hash failures, overload/body identity, exact-call matching, helper posture, denominators and CLI
gate propagation. Hashes bind evidence but do not prove Swift receiver identity or output causality;
review rationale remains required. Perch scope records and contract faults are a separate dependent
slice after F25-064. Nothing was installed or published.
