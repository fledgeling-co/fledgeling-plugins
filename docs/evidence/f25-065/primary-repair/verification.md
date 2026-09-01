# F25-065 upstream repaired PRIMARY verification — PASS

Reviewed exact repaired HEAD `77b56328bf8de69789402a566ee2c64bc09ff2da` against the
original Perch brief, spec, plan and the prior PRIMARY FAIL at `e3178a3`. This is a same-family
degraded review in a reused thread with unrelated prior context; it does not satisfy the still-owed
distinct additional review. I did not author or alter implementation source.

## Prior blockers

All four prior blockers are closed.

- **Boolean/integer schema:** the top-level version and scope `callOffset` now require exact Python
  `int` types, excluding `bool`; caller offsets use the same rule. Independent public CLI faults for
  `version: true` and `callOffset: true` both exit 1 with their named schema diagnostics.
- **Configured falsy values:** only `None` means the optional field is absent. Independently
  configuring each of `false`, `0`, `{}` and `[]` over an otherwise clean body exits 1 solely through
  `blindScopeFile must be a nonempty string`, so malformed configuration no longer clears silently.
- **Attributed helper callers:** each attributed-helper record now requires a nonempty caller array
  with exact file, name, body hash, call offset and receiver-plus-call fingerprint. Runtime matching
  requires one current caller body and the named helper call at that offset. An unbound helper exits
  1; a receiver-qualified `Fixtures.seed()` caller with current hashes exits 0 and reports one
  attributed helper; changing only its caller-call fingerprint exits 1.
- **Catalogue:** `site/lib/catalogue.json`, the plugin manifest and marketplace entry all advertise
  0.16.2. The focused suite now guards catalogue-to-manifest version parity.

## Regression and source review

The repair is confined to strict loading, caller binding, tests/evidence, changelog wording and the
generated catalogue version. Existing exact scope identity, single-call removal, earlier-mutator
re-evaluation, raw mutating-body denominator, scoped class counts, reference drift checks and CLI
gate propagation remain unchanged. The repair records every encountered body before called-helper
exclusion, allowing a caller binding to resolve without changing the candidate/helper denominator.
Duplicate or ambiguous caller bodies fail through the exact-one-body check.

The author's four repair mutations each reached assertions and went red for boolean acceptance,
falsy-path omission, missing caller binding and stale catalogue version. The independent probe adds
the qualified valid caller and single-fingerprint drift boundary. Source hashes after all runs equal
the repaired HEAD; no implementation file is dirty.

Two focused runs each passed 19 tests. Two complete portable runs each passed the 114-test campaign
gate with 0 failures and included the same 19 focused tests. No full native, provider, Keychain,
app, install, publish, cache or main-branch operation was run.

The intended limitation remains: caller/body/call hashes bind lexical source but do not resolve Swift
types, prove receiver identity or establish effect causality. The rationale and referenced contract
still require human review; the repair does not claim otherwise.
