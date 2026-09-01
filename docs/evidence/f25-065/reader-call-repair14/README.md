# F25-065 prior-terminal conservative repair

Fresh primary `ffd412a` and distinct additional `23e76a0` are operative FAIL receipts against
`b9366d9`. Both proved that always-executed `do { return }` / `do { throw }` and once-running
`repeat { return } while false` blocks terminate before a later helper, while the scanner's
minimum-depth/current-statement checks granted that unreachable helper and reader attribution.
Compiled runtime controls recorded zero stores and reads for the blocked paths; the public CLI
nevertheless exited 0.

The bounded rule is now deliberately simpler and more conservative: any earlier masked `return` or
`throw` in the caller body refuses helper attribution. This also refuses a safe shape such as
`if false { return }; seed(); read()`; the false negative is explicit because this lexer cannot prove
which nested Swift control path executes. Permanent public-CLI fixtures pin the do-return, do-throw,
repeat-return and safe false-if refusal alongside the prior same-line/newline/comment terminal and
trailing-closure cases.

Focused 21-test and full 114-test gates pass twice. Twelve isolated actual-scanner mutants fail and
restore source byte-for-byte, including one that narrows the all-prior-terminal rule back to the
current statement. Two byte-identical Perch runs at corrected corpus commit `c30595e1` accept
108 scopes with zero invalid records, 0 attributed helpers, 56 failure sentinels, 22 direct outputs
and 30 fixture values. Both remain honestly red on four reviewed blind bodies plus REQ-056.

CP §7 self-review covered nested and top-level return/throw, comments, direct and qualified controls,
the intentional false negative, trailing syntax, balanced arguments, mutation restoration, corpus
classifications and docs. No install, publication, cache edit, push, native app, provider, Keychain
or live call occurred. Fresh primary and distinct additional reviews are owed.
