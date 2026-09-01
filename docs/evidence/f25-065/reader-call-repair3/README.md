# F25-065 enum-pattern reader repair

Fresh primary commit `78895b88` is an operative FAIL receipt against implementation `35d7159d`.
Its public-CLI fixture proved that `.read(let x)` in a Swift enum associated-value pattern cleared an
attributed-helper mutation even though the syntax only destructures a value. The two earlier reader
FAIL receipts remain retained.

Reader evidence is now conservative: a configured stem must start an unqualified masked identifier
and use parenthesized call syntax. This refuses member-shaped calls as well as enum construction and
patterns because the bounded lexer cannot distinguish them. The restriction does not affect the
separately bound helper call, which retains qualified/unqualified parenthesized and Swift
trailing-closure forms.

The enum-pattern source is a permanent direct and public-CLI refusal. Four actual-scanner mutants
remove the identifier boundary, restore qualified shapes, remove parenthesized-call syntax, or
restore ambiguous reader trailing closures. All fail the permanent suite and restore source exactly.
The focused 21-test group and complete 114-test portable gate pass twice. The scanner accepts all
108 Perch scope records with zero invalid scopes and retains the same four honest blind bodies plus
independent uncensused REQ-056, so the five-finding corpus exit 1 remains truthful.

CP §7 self-review covered the masked predicate, direct/public-CLI cases, the helper/reader separation,
all four source faults, changelog and scope-contract wording. The result does not establish receiver
identity, reader independence or output causality. No schema, raw population, version, dependency,
installation, publication, cache, Perch registry/floor, native app, provider, Keychain or live call
changed. Fresh primary and distinct additional reviews are owed.
