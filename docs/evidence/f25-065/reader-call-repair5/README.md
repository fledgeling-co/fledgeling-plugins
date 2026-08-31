# F25-065 invocation-context reader repair

Fresh primary commit `824e9aa0` is an operative FAIL receipt against implementation `08007d34`.
Its public-CLI fixture and an independent successful `swiftc -typecheck` proved that valid Swift
`#selector(read(_:))` references a method without invoking it. The three earlier reader FAIL receipts
remain retained.

Explicit attributed-helper scope now requires two independently live properties: reader-shaped call
syntax and a conservative invocation context. Accepted contexts are statement starts, assignment or
statement delimiters, return/try/await positions, and assertion macro names. This admits both
parenthesized and trailing-closure reader calls at those boundaries. It refuses qualified patterns,
control conditions, local declarations, nested calls and selectors rather than interpreting them.
The separately exact-bound helper call keeps its existing qualified/unqualified and trailing-closure
posture.

The selector is a permanent direct and public-CLI refusal. One actual-scanner mutant removes call
syntax and another removes invocation context; each fails the permanent suite and source restores
exactly. An earlier layered attempt is retained under `reader-call-repair4`: three old guards became
redundant under the context rule, their mutants stayed green, and that design was discarded with no
credit. The final focused 21-test group and complete 114-test portable gate pass twice. The scanner
accepts all 108 Perch scopes with zero invalid records and retains the same four honest blind bodies
plus uncensused REQ-056, so the five-finding corpus exit 1 remains truthful.

CP §7 self-review covered the masked suffix, context boundaries, helper/reader separation, both live
source faults, discarded redundant guards, changelog and scope-contract wording. The rule remains a
bounded lexical proof and deliberately false-negatives ambiguous nested calls; it does not establish
receiver identity, reader independence or output causality. No schema, population, version,
dependency, installation, publication, cache, Perch registry/floor, native app, provider, Keychain or
live call changed. Fresh primary and distinct additional reviews are owed.
