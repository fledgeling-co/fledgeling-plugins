# F25-065 multiline-terminal repair

Fresh primary `8f56e44` and distinct additional `8618624` are operative FAIL receipts against
`42ac3ea`. Both proved that Swift accepts a helper expression on the line after `return` or `throw`,
while the scanner split helper context at that newline and granted an unreachable later reader.
Block-comment-plus-newline variants bypassed the guard in the same way. Compiled runtime fixtures
executed the scoped stores and zero readers; the public CLI nevertheless exited 0.

Helper terminal context now spans ordinary newlines and masked comments. Only semicolons and
balanced block boundaries reset the current statement before the return/throw check. Permanent
public-CLI fixtures cover multiline return, multiline throw and comment-newline return. Direct and
qualified parenthesized controls remain accepted; all bare/parenthesized trailing closures, nested
control-flow helper calls, argument-only readers and return/throw helpers remain refused.

Focused 21-test and full 114-test gates pass twice. Twelve isolated actual-scanner mutants fail and
restore source byte-for-byte, including a mutant that restores newline splitting. Two byte-identical
Perch runs at corrected corpus commit `c30595e1` accept 108 scopes with zero invalid records,
0 attributed helpers, 56 failure sentinels, 22 direct outputs and 30 fixture values. Both remain
honestly red on four reviewed blind bodies plus uncensused REQ-056.

CP §7 self-review covered same-line/newline/comment return and throw forms, semicolon/block
boundaries, trailing closures, balanced arguments, direct controls, mutation restoration, corpus
classifications and docs. Arbitrary custom functions returning `Never` remain outside this lexical
proof. No install, publication, cache edit, push, native app, provider, Keychain or live call
occurred. Fresh primary and distinct additional reviews are owed.
