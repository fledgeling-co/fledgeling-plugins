# F25-065 direct-helper repair

Fresh primary `cbda7209` and distinct additional `b0701218` are operative FAIL receipts against
`6f80131`. A trailing closure can run before its helper's scoped mutation, a multi-trailing helper
can invoke a different closure, and helpers in false branches or loop paths followed by `break` or
`continue` need not execute or reach their apparent readers. Compiled runtime counters and the
public CLI demonstrated those false greens.

Attributed-helper callers now require a direct, top-level, parenthesized helper call. The complete
balanced call ends before the later-reader search, so arguments cannot count. Trailing closures and
nested control flow are deliberately refused: this bounded lexer cannot prove whether or when they
execute relative to the scoped mutation. Reader syntax, conditional-compilation, nested-body and
top-level terminator guards remain in force.

The ten obsolete Perch trailing-closure caller bindings were not weakened into a scanner exception.
Source review showed that they all referred to one `Issue.record` inside deferred cleanup; that call
is itself the failure oracle, while caller assertions run before the defer. Perch commit `c30595e1`
reclassifies the one scope as a failure sentinel and removes those callers. Two byte-identical corpus
runs accept all 108 scopes with 0 invalid records, 0 attributed helpers, 56 failure sentinels,
22 direct outputs and 30 fixture values. Both remain honestly red on four reviewed blind bodies and
uncensused REQ-056.

Focused 21-test and full 114-test gates pass twice. Nine isolated actual-scanner mutants fail and
restore the scanner byte-for-byte. CP §7 self-review covered exact body/caller binding, direct-call
context, nested false branches, break/continue paths, trailing and multiple trailing closures,
balanced arguments, terminators, mutation restoration, docs, and the corrected Perch corpus. This
is intentionally conservative and may reject valid nested executions. No install, publication,
cache edit, push, native app, provider, Keychain or live call occurred. Fresh primary and distinct
additional reviews are owed.
