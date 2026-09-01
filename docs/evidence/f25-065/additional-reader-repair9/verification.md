# F25-065 upstream repeated DISTINCT ADDITIONAL re-review — FAIL

**Verdict: FAIL** for exact repaired implementation
`d9f3d87adc96687be6fb0cfbbc998bca8249822f`.

The reader-side repair works as stated. Readers inside stored closures, braced control flow, and all
conditional-compilation regions are refused. Unicode, backtick, and wildcard-label references
remain refused. Direct parenthesized helper calls followed by direct parenthesized readers remain
accepted. Configured-reader and attributed-helper trailing closures are now deliberately refused,
as are immediately invoked reader closures and synchronous nested `do` blocks.

## Blocking helper-call false greens

The caller binding checks only whether the parenthesized helper spelling survives comment/literal
masking at its recorded offset. It does not apply the reader's top-brace or outside-`#if` posture to
the helper call itself. Two valid Swift callers therefore receive attributed-helper credit without
executing the helper:

```swift
let invoke = { seed() }
_ = invoke
read()
```

```swift
#if false
seed()
#endif
read()
```

The complete compiled fixture runs with `seedCount == 0` and `readCount == 1` for both cases. The
direct scanner and public CLI accept each exact source-bound attributed-helper scope and exit 0.
The later reader really executes, but it cannot observe a helper mutation that never occurred.

A direct `seed(); return; read()` caller also exits 0 through the public scanner while the compiler
marks the reader unreachable and the runtime fixture observes `seedCount == 1`, `readCount == 0`.
This is a broader top-level reachability limitation; the two helper-binding failures above do not
depend on reasoning about a later reader's effect.

## Perch corpus regression and receipt contradiction

The exact Perch corpus no longer has zero invalid scopes. It loads **108** records but emits ten
`withRetryStore caller scope does not bind its named helper call` findings because those real callers
use the newly refused trailing-closure helper form. Together with four blind bodies and uncensused
REQ-056, the CLI reports **15 findings**, not five.

The author receipt says `invalidScopes: 0`, but its committed `reader-call-repair9/perch-corpus.log`
has the same `d5f923…` hash as this independent rerun and visibly contains all ten invalid-scope
lines. The receipt therefore contradicts its named artifact.

## Controls and gates

The runtime fixture confirms the intended conservative false negatives: an actually invoked helper
trailing closure, an immediately invoked reader closure, and a synchronous nested reader all execute,
while the scanner refuses them. The direct parenthesized helper/read control executes and passes.
Inactive reader-only conditional regions reject. Unknown top-level and record fields fail closed,
as does caller `testEntry` posture drift.

Seven scanner-source mutants ran in isolated temporary copies from `git show d9f3d87`: drop call
syntax, allow label references, allow configured-reader trailing closures, allow nested readers,
allow conditional-compilation readers, allow helper trailing closures, and bypass invocation
context. Every mutant failed the permanent attributed-helper fixture, and the exact snapshot source
hash remained restored.

The focused suite passed **21/21 twice**, and the portable full suite passed **114/114 twice**.
Plugin, marketplace, and committed catalogue versions remain **0.16.2**, with catalogue parity
passing in all four runs. Catalogue regeneration was not rerun because the isolated archive lacks
`yaml` and this review prohibited installs and cache mutation.

CP §7 self-review covered exact-hash binding, helper-call execution posture, public CLI behavior,
runtime counters, intentional false negatives, the corpus/receipt contradiction, strict schema and
caller posture, seven mutation failures, and source isolation. This repeated review is same-family
degraded. It reuses prior F25-065 review context plus unrelated F25-063, F25-066, F25-057, F25-034,
F25-064, and F25-067 context; no out-of-family claim is made. No implementation, install, publish,
push, cache, native app, provider, Keychain, release, or live action was performed.
