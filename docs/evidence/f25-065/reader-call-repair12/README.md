# F25-065 terminal-helper repair

Fresh primary `10924e1` and distinct additional `f986f72` are operative FAIL receipts against
`de4de21`. Both proved through the public CLI and compiled Swift that `return seed(); read()` gained
attributed-helper credit although the reader is unreachable at runtime. The helper-context check
allowed a return-position call, then the balanced suffix began after `seed()` and lost the return
token. Additional review also proved `seed() {}; read()` contradicted the documented refusal of
trailing-closure helper syntax.

Helper context now rejects calls whose current top-level statement begins with `return` or `throw`.
After balancing a parenthesized call, it also rejects an immediately following trailing closure.
Permanent public-CLI fixtures cover both forms. The prior direct/top-level, conditional-compilation,
nested-control, balanced-argument, reader-call and terminator protections remain in force.

Focused 21-test and full 114-test gates pass twice. Eleven isolated actual-scanner mutants fail and
restore source byte-for-byte, including independent return-position and parenthesized-trailing
guards. An initial attempt incorrectly ran mutation and ordinary gates concurrently against the
same scanner file; those outputs were overwritten and excluded. The recorded runs began only after
exact restoration and run without a concurrent writer.

Two byte-identical runs over corrected Perch commit `c30595e1` accept 108 scopes with zero invalid
records, 0 attributed helpers, 56 failure sentinels, 22 direct outputs and 30 fixture values. Both
remain honestly red on four reviewed blind bodies plus uncensused REQ-056. CP §7 self-review covered
the exact caller statement, return/throw variants, balanced suffix, both trailing-closure spellings,
direct valid controls, mutation restoration, corpus classifications and documentation. No install,
publication, cache edit, push, native app, provider, Keychain or live call occurred. Fresh primary
and distinct additional reviews are owed.
