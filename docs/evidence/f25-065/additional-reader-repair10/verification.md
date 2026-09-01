# F25-065 distinct additional review — reader repair 10

## Verdict

**FAIL** against exact implementation `6f8013101300cc08da0b51d64f58755eb81fa248`.

The repair closes the previously reported nested/inactive helper-call cases, excludes readers in helper arguments until the balanced parenthesized call ends, rejects top-level `return`/`throw` before the reader, preserves strict schema and caller binding, and restores the real Perch corpus to 108 scope records, 0 invalid scopes, and 5 findings. It still grants attributed-helper credit where the required mutation/read sequence does not execute.

## Blocking false greens

1. A helper with two trailing closures can invoke its final closure parameter while the reader is in the uninvoked first closure. `seed { read() } second: {}` passes the public gate because the scanner proves only that `second` is invoked. The compiled fixture observes one store and zero reads.
2. `continue` and `break` are not recognized as terminating the later-reader path. Both `seed(); continue; read()` and `seed(); break; read()` pass the public gate; compiled execution observes one store and zero reads.
3. The selected control-block allowlist treats syntax as execution. `while false { seed() }; read()` and `if 0 == 1 { seed() }; read()` pass despite compiled execution observing zero stores and one read.

These are source-valid Swift cases and were exercised through the public CLI in `probe.json`; `execution-contexts.swift` independently compiles and proves their actual runtime behavior. Valid direct mutation/read and invoked-final-closure controls also run successfully.

The real Perch `withRetryStore` target does not rescue trailing-closure inference: its attributed mutation is `Issue.record` in deferred cleanup, while the caller closure reads occur before that mutation. It therefore cannot substantiate the general trailing-closure acceptance rule.

## Verification

- Focused Swift scanner suite: 21/21 twice.
- Full safe plugin suite: 114/114 twice.
- Ten source mutants in isolated temporary copies: every mutant makes the permanent substantive fixture fail; every copy begins from scanner SHA-256 `c547f0891de24df7d362f34b9090c76ee91014b3657bd31166a73f1977dc62a8`.
- Strict schema: unknown top-level field, unknown record field, and caller `testEntry` posture drift all fail closed.
- Public boundaries: direct parenthesized calls and the intended single invoked-final-closure case pass; stored/nested/conditional readers, function references, configured-reader trailing closures, reader-before-helper, and helper-argument-only readers fail.
- Perch corpus: 108 scope records, 0 invalid scopes, 4 blind bodies plus REQ-056, 5 findings, expected gate exit 1.
- Repair-9 receipt correction is explicit and auditable: its retained log reports 10 invalid scopes / 15 findings, and its receipt now states those values and marks the former 0/5 summary false. Repair 10's author receipt reports the restored 0/5 result.
- Plugin and root marketplace versions are both 0.16.2; the permanent catalogue parity fixture passes in both full runs.

## Independence, restoration, and limits

This is a repeated, same-family degraded additional review with no out-of-family or workflow-lane claim. Context from earlier F25-065 rounds and unrelated Fleet work was reused, but the adversarial cases, runtime witness, public CLI runs, and mutations in this receipt were newly executed against the exact implementation snapshot.

All implementation mutations ran in temporary copies extracted from the reviewed commit. The shared worktree implementation was not mutated by this reviewer; unrelated root-authored scanner/test edits already present after the reviewed commit were preserved and excluded from this evidence commit. No install, publish, push, cache mutation, native app, provider, Keychain, or live campaign action was performed. Catalogue regeneration was not run because the isolated archive lacks PyYAML and installing dependencies or changing caches was prohibited; the checked-in parity test and direct version inspection cover the claimed version consistency.
