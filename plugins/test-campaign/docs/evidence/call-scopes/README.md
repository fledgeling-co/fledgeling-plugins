# Auditable blind-call scopes — author evidence

Version0.16.2 adds exact per-call scope records. Body, call and referenced producer/contract hashes
must match; stale, duplicate, unmatched or ambiguous records remain gate findings. A scope removes
one occurrence and the ordinary last-mutation/later-reader analysis then restarts over earlier calls.
Attributed-helper records additionally bind an exact current caller body and named helper-call
fingerprint, and that caller must contain a configured reader after the helper call. Reports retain
the raw mutating-body denominator and count scoped calls by classification.

Target and caller records bind the parser's explicit-test posture so removing `@Test` outside an
otherwise identical body invalidates the scope. Caller bindings require a direct, top-level,
parenthesized helper call. Trailing closures and nested control-flow calls are refused because this
lexical scanner cannot prove whether or when they execute relative to the scoped mutation. Helper
calls in `return` and `throw` expressions are refused because later statements are unreachable.
Newlines and masked comments are not treated as statement boundaries for that terminal check.
The exact caller call must also survive the Swift comment/literal mask, so a matching spelling in
non-executable text cannot justify attribution.

Twenty focused tests and the complete114-test plugin gate pass. Three original disposable actual-source
faults are red: ignoring the call fingerprint, suppressing the whole body, and globally excluding
`record`. Import/syntax failures receive no fault credit. CP §7 review covered loader validation,
path/hash failures, overload/body identity, exact-call matching, helper posture, denominators and CLI
gate propagation. Hashes bind evidence but do not prove Swift receiver identity or output causality;
review rationale remains required. Perch scope records and contract faults are a separate dependent
slice after F25-064. Nothing was installed or published.

Primary review found three author gaps: Python booleans passed as integer schema fields,
configured-but-falsy scope paths were treated as absent, and attributed helpers did not bind their
named callers. The repaired suite exercises all three through the public loader or CLI and rejects an
arbitrary non-caller body. Follow-up CP §7 and Perch corpus review added eight repair mutants: caller-later-reader,
target and caller test-entry posture, strict posture schema, and trailing-closure caller matching.
Fresh fixtures reject all eight, including a reader placed only before the helper call and a helper spelling that exists only in a comment. The generated catalogue
version is kept at 0.16.2 with both manifests.

A fresh cumulative primary review then found that the later-reader check accepted `already` and a
bare `read` expression for configured reader `read`. Both false greens are now permanent public-CLI
fixtures. Attribution requires a masked reader-shaped identifier with call syntax in a conservative
invocation context.
Helper-call bindings are parenthesized only. This remains a lexical call-shape check, not receiver
resolution or output causality.

A subsequent cumulative primary found the same ambiguity in qualified syntax: `.read(let x)` in a
Swift enum associated-value pattern was accepted as a call. The interim repair limited readers to
unqualified parenthesized syntax; the contextual repair below supersedes that syntax detail while
retaining the qualified-shape refusal. This restriction does not apply to the separately bound
helper call.

A third cumulative primary proved that unqualified parenthesized syntax alone was still insufficient:
valid Swift `#selector(read(_:))` references a method without invoking it. Reader evidence therefore
begins at a conservative statement, assignment, return/try/await, or assertion-macro boundary.
That one contextual rule refuses qualified patterns, control conditions, declarations and selector
references while allowing parenthesized calls at a proved boundary. Other nested
contexts are refused rather than interpreted. This is intentionally incomplete and fail-closed; the
ordinary unscoped blind-pass heuristic remains broader.

A fourth cumulative primary found assignment-reference syntax: `let function = read(_:)` is valid
Swift but does not invoke `read`. The call-shape guard now refuses parentheses containing only one or
more argument-label placeholders and no values. A real assigned call such as
`let value = read(label: input)` remains accepted. This distinction is independent of the context
guard and has its own actual-source mutant.

A fifth cumulative primary proved that a trailing-closure-shaped configured reader can instead be
a valid computed-property accessor: `get { 1 }` declares an accessor and performs no observation.
Configured readers and separately bound helpers are now parenthesized only. Assignment context is limited to a simple binding
or assignment statement, while the balanced-body parser independently prevents a nested function's
default argument from lending reader credit to its parent before that function is called. Both are
permanent public-CLI fixtures; the accessor refusal has its own actual-source mutant.

A sixth cumulative primary found that the placeholder grammar's ASCII label start accepted valid
Swift `read(λ:)` as if it were a call. Placeholder detection now treats any colon-terminated token
sequence inside the parentheses as a function reference, including Unicode and backtick-escaped
labels. Real labeled calls remain distinguishable because they contain an argument expression.

Distinct additional review then found a stored closure whose body contains `read()` but is never
invoked, plus a literal-false branch carrying the same unreachable credit. Configured-reader credit
is now limited to the caller body's top lexical brace level.
This deliberately refuses ambiguous nested control and immediately-invoked closure bodies as well;
an explicit scope must use a directly provable observation rather than borrow one from nested code.

A seventh primary found that consuming a helper trailing closure's opening brace normalized the
closure reader to apparent top level even when the helper never invoked its parameter. A distinct
additional review found the brace-free equivalent in inactive `#if false` and false
`#if canImport(...)` regions. Readers inside all conditional-compilation regions are conservatively
refused because the scanner does not resolve the active Swift build configuration.

The first repair refused every trailing-closure helper, invalidating ten current Perch bindings,
while still accepting helper calls stored in closures or inactive branches. It also searched inside
parenthesized helper arguments, so an uninvoked `@autoclosure` looked like a later reader. A later
repair inferred trailing-closure execution from the helper body, but fresh review proved that this
does not establish whether the closure runs before or after the scoped mutation. Fresh review also
found unreachable helper calls inside false branches and loop paths after `continue` or `break`.
The operative rule therefore requires a direct top-level parenthesized helper call and balances the
entire call before searching for a later reader. Top-level `return` and `throw` terminate credit.
The ten Perch trailing-closure bindings were reviewed and reclassified as one failure sentinel:
their scoped `Issue.record` is itself the cleanup failure oracle, and caller assertions execute
before the deferred cleanup rather than observing it.

Fresh primary and additional review of that repair then found `return seed(); read()` accepted:
helper context allowed the return-position call, while the balanced suffix began after `seed()` and
lost the terminating token. The additional review also found parenthesized trailing syntax
`seed() {}; read()` still accepted despite the documented refusal. The final rule rejects helper
calls in return/throw positions and rejects a trailing closure after the balanced parentheses.

Fresh review then found that splitting helper context at a newline accepted the valid multiline
forms `return\n seed()` and `throw\n seed()` (including a masked block comment before the newline),
again discarding the terminal before later-reader analysis. Only semicolons and balanced block
boundaries now reset the terminal statement; ordinary newlines remain part of it.

Strict-schema arming initially false-greened because a prior reference-drift case had not restored its producer, so every later malformed record failed for the wrong reason. The fixture now restores that byte before the schema probes; independently removing either unknown-field guard fails its named assertion. The failed first mutation attempt is retained in command history, not counted as fault credit.
