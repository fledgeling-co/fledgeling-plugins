# F25-065 upstream repeated DISTINCT ADDITIONAL re-review — FAIL

**Verdict: FAIL** for exact repaired implementation
`2b186f8b92c2f87544b3f244289cee15a5bc62d6`.

The repair closes both operative failures against `4fabc42`. Valid Swift Unicode, escaped-keyword,
and wildcard-label function references (`read(λ:)`, ``read(`repeat`:)``, and `read(_:_:)`) fail
the attributed-helper gate. Stored closures and literal-false braced
branches no longer lend reader credit. Operator tokens are not valid Swift argument labels even
when backtick-escaped; the committed negative compiler fixture records that language boundary.

## New blocking false green

Swift conditional-compilation branches introduce no braces. The scanner therefore treats their
contents as caller-top-level source even when the compiler removes the branch:

```swift
func testMeasure() {
    seed()
    #if false
    read()
    #endif
}
```

The complete executable fixture compiles and runs with `readCount == 0`. The exact source-bound
direct scanner and public `vacuity-check.py <campaign> --gate` nevertheless accept the
attributed-helper record and exit 0. Replacing the condition with
`canImport(DefinitelyMissingF25065Module)` produces the same false credit. These are deterministic
non-invocations outside the repaired brace-depth model.

## Repaired and conservative boundaries

A direct parenthesized `read()` remains valid. A helper invoked with `seed { configure() }` followed
by a direct read remains valid even though the post-helper slice begins at a negative relative brace
depth. The same helper followed only by a nested false-branch reader is refused. Configured reader
trailing closures remain refused.

Immediately invoked closures and synchronous `do { read() }` blocks are deliberately conservative
false negatives under the documented top-level-brace policy; their valid Swift fixtures compile,
and the public gate rejects them. This review does not treat those intentional refusals as failures.
Unknown top-level and record fields fail closed, as does caller `testEntry` posture drift.

Five scanner-source mutants ran in isolated temporary trees derived from `git show 2b186f8`: drop
call syntax, allow label placeholders, allow configured-reader trailing closures, allow nested
readers, and compare brace depth with absolute zero instead of the post-helper minimum. Every mutant
failed the permanent attributed-helper fixture. The last specifically proves that helper trailing
closures need the relative brace baseline. The shared implementation tree was not mutated.

The exact-snapshot focused suite passed **21/21 twice**, and the portable full suite passed
**114/114 twice**. The Perch corpus retains **108** valid scopes, **0** invalid scopes, **4** blind
Swift bodies, and uncensused **REQ-056**; the five findings keep the gate at exit 1. Plugin,
marketplace, and committed catalogue versions remain **0.16.2**, and catalogue parity passed in all
four suite runs. Catalogue regeneration was not rerun because the isolated archive lacks `yaml` and
this review prohibited installs and cache mutation.

CP §7 self-review covered exact-hash binding, public CLI semantics, executable and compiler-negative
Swift fixtures, helper brace-baseline behavior, schema/caller binding, five mutation failures,
source isolation, and receipt/log agreement. This repeated review is same-family degraded. It reuses
the earlier F25-065 additional context plus unrelated F25-063, F25-066, F25-057, F25-034, F25-064,
and F25-067 context; no out-of-family claim is made. No implementation, install, publish, push,
cache, native app, provider, Keychain, release, or live action was performed.
