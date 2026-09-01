# F25-065 helper-closure and conditional-compilation repair

Fresh primary `49790b37` and distinct additional `e800d424` are operative FAIL receipts against `2b186f8`. A trailing-closure helper could receive a reader from a closure the helper never invoked because helper matching consumed the opening brace. Readers in inactive `#if false` and false `#if canImport(...)` branches also remained at lexical brace baseline.

Attributed helper calls are now parenthesized-only; the bounded scanner refuses to infer closure-parameter invocation. Configured readers inside all conditional-compilation regions are refused because the scanner does not evaluate Swift build configurations. Direct parenthesized helper and reader calls remain accepted.

Seven actual-scanner mutants remove call syntax, allow label-only references, allow configured-reader trailing closures, allow nested readers, allow conditional-compilation readers, allow helper trailing closures, or remove invocation context. All fail the permanent direct/public-CLI suite and restore source exactly. Focused 21-test and full 114-test gates pass twice. The Perch corpus keeps 108 valid scopes, four honest blind bodies, and uncensused REQ-056.

CP §7 self-review covered helper call/closure separation, conditional directives, nested relative brace depth, Unicode and escaped labels, direct calls, mutation restoration, docs, and unchanged version surfaces. The contract deliberately false-negatives helper trailing closures, nested readers and conditional-compilation readers. No install, publication, cache edit, push, Perch floor/credit rewrite, native app, provider, Keychain or live call occurred. Fresh primary and distinct additional reviews are owed.
