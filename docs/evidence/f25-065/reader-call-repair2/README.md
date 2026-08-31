# F25-065 reader/control-condition repair

Fresh primary commit `4c5ed872` is an operative FAIL receipt against implementation `2de5a2e6`.
Its public-CLI fixture proved that `seed(); let read = false; if read { print("x") }` cleared an
attributed-helper mutation: the lexical `read {` branch mistook a Boolean control condition for a
reader invocation. The earlier `dd80213b` identifier-boundary FAIL also remains retained.

Configured readers now require a masked identifier boundary and parenthesized call syntax. Qualified
`read()` remains valid. A reader-shaped trailing closure is deliberately refused because the bounded
lexer cannot distinguish it from `if read {}`. This does not narrow caller binding: the named helper
call may still be parenthesized or use Swift trailing-closure syntax, and its exact masked fingerprint,
body hash and explicit-test posture remain bound.

The control-condition source is a permanent direct and public-CLI refusal. Three actual-scanner
mutants remove the identifier boundary, remove parenthesized-call syntax, or restore the ambiguous
trailing-closure branch; all fail that permanent suite and restore the source exactly. The focused
21-test group and complete 114-test portable gate pass twice. The repaired scanner accepts all 108
Perch scope records with zero invalid scopes and retains the same four honest blind bodies plus
independent uncensused REQ-056, so the corpus gate's five-finding exit 1 remains truthful.

CP §7 self-review covered the masked predicate, direct/public-CLI boundary, helper-call separation,
all three actual-source faults, changelog and scope-contract wording. The check remains lexical and
does not establish reader receiver identity, independence or output causality. No schema, raw
population, plugin version, dependency, installation, publication, cache, Perch registry/floor,
native app, provider, Keychain or live call changed. This same-family degraded author repair now
requires a fresh primary and distinct additional review.
