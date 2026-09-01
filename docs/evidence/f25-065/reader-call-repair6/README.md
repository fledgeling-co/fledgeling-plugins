# F25-065 Swift function-reference repair

Fresh primary `9b09eca7` is an operative FAIL against `3524c027`. Its public-CLI fixture and an
independent successful `swiftc -typecheck` proved that `let function = read(_:)` references a Swift
function without invoking it. The prior reader FAIL receipts and rejected layered experiment remain
retained.

The call-shape guard now refuses parentheses containing only one or more Swift argument-label
placeholders and no values. This is separate from invocation context: assignment remains accepted,
and `let value = read(label: input)` is a permanent valid case. Parenthesized and trailing-closure
calls at conservative boundaries remain accepted; selector, enum pattern, control condition,
declaration, nested-call, substring and bare-name cases remain refused.

Three actual-scanner mutants remove call syntax, restore function-reference placeholders, or remove
invocation context. All fail the permanent direct/public-CLI suite and restore source exactly. The
focused 21-test group and full 114-test portable gate pass twice. The scanner accepts all 108 Perch
scopes with zero invalid records and retains four honest blind bodies plus uncensused REQ-056, so the
five-finding corpus exit 1 remains truthful.

CP §7 self-review covered label-placeholder grammar, assigned real calls, contextual refusals,
source faults, changelog and scope wording. The bounded lexer deliberately false-negatives ambiguous
nested calls and does not prove receiver identity, reader independence or output causality. No
schema, population, version, dependency, installation, publication, cache, Perch registry/floor,
native app, provider, Keychain or live call changed. Fresh primary and distinct additional reviews
are owed.
