# F25-065 Unicode-reference and nested-reader repair

Fresh primary `66bb7959` and distinct additional `8f5e68ff` are operative FAIL receipts against `4fabc42`. Valid Swift Unicode-label function references such as `read(λ:)` bypassed the ASCII placeholder grammar. A stored, never-invoked closure and a literal-false branch could also lend `read()` credit to their parent caller.

Function-reference recognition now treats any colon-terminated token sequence, including Unicode and backtick-escaped labels, as a reference rather than a call. Configured-reader credit is limited to the caller body's top lexical brace level; ambiguous nested controls and immediately-invoked closures are conservatively refused. Separately bound helper calls still accept trailing closures.

Five actual-scanner mutants remove call syntax, allow label-only references, allow configured-reader trailing closures, allow nested closure readers, or remove invocation context. All fail the permanent direct/public-CLI suite and restore source exactly. Focused 21-test and full 114-test gates pass twice. The Perch corpus keeps 108 valid scopes, four honest blind bodies, and uncensused REQ-056.

CP §7 self-review covered Unicode/escaped labels, real labeled calls, accessor and default declarations, stored closures, unreachable branches, helper trailing closures, depth normalization after a helper trailing closure, mutation restoration, and unchanged version surfaces. The scanner remains deliberately lexical and does not prove reader independence or output causality. No install, publication, cache edit, push, Perch floor/credit rewrite, native app, provider, Keychain or live call occurred. Fresh primary and distinct additional reviews are owed.

Superseded status: fresh reviews `49790b37` and `e800d424` found helper-trailing-closure and conditional-compilation false greens; reader-call-repair9 is operative.
