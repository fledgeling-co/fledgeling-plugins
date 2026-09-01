# F25-065 upstream primary review — multiline-terminal repair

## Verdict

**FAIL** against exact implementation `b9366d9ea6f282610dc64760a9f38586a8144e8e`.

The repair correctly preserves `return` and `throw` across ordinary and masked-comment newlines.
It still loses terminals inside balanced blocks that execute before a later helper. Swift's `do`
body always executes, and a `repeat` body executes at least once, so their terminal makes the
helper and reader after the block unreachable. The lexical guard treats the closed block as a fresh
top-level boundary and grants attributed-helper credit.

## Blocking false greens

These three compiled public-CLI fixtures each exit 0 with one attributed-helper scope, zero invalid
scopes, and zero findings:

```swift
func testMeasure() { do { return }; seed(); read() }
func testMeasure() throws { do { throw E.boom }; seed(); read() }
func testMeasure() { repeat { return } while false; seed(); read() }
```

Swift compiles all three and warns that the helper suffix will never execute. The runtime matrix
executes same-line/newline/comment return and throw cases, prior-return, the three block-terminal
cases, and a valid `if false { return }; seed(); read()` opposite control. Its final
`stores=7 reads=1` shows that only the valid false-if control supplies the last store/read; no
terminal case executes its reader.

The source-bound cause is the interaction between the general invocation-context depth check and
`helper_invocation_context`'s current statement. Once a balanced `do` or `repeat` block closes, the
prefix returns to minimum brace depth; the terminal inside the block is ignored as nested, while
splitting on braces selects only the suffix after the block. The scanner does not prove whether a
prior block executes, so accepting this family is unsound.

## Other boundaries exercised

- Same-line, newline, and block-comment-newline `return` and `throw` helpers refuse.
- A top-level prior `return;` or `throw;` before the helper refuses.
- Bare, parenthesized, comment-separated parenthesized, and multiple trailing closures refuse.
- Direct and qualified top-level calls, balanced helper arguments followed by a distinct reader,
  ordinary semicolon-separated calls, and a helper after `if false { return }` pass.
- An argument-only reader and a helper nested in control flow refuse.

The valid false-if control demonstrates why the scanner cannot infer block execution from balanced
braces alone; conservative explicit refusal is required if it does not model Swift control flow.

## Gates, mutants, and corpus

- Focused Swift/public-CLI suite: 21 tests twice, both exit 0.
- Full safe plugin suite: 114 passed / 0 failed twice.
- Twelve isolated actual-scanner mutants all failed the focused oracle, including restoration of
  newline splitting plus the prior eleven call, reader, context, terminal, trailing, and suffix
  guards. Source restored byte-for-byte after every mutant.
- Corrected Perch corpus `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical
  runs; 108 scopes, 0 invalid, 0 attributed helpers, 22 direct outputs, 56 failure sentinels, and
  30 fixture values. Both remain honestly red on four blind bodies plus uncensused REQ-056: five
  findings, expected exit 1.

## Independence and limits

This is a repeated same-family degraded primary lane; workflow and out-of-family lanes were not
available in this session. I did not author the upstream repair. The review reused prior F25-065,
F25-034, and F25-015 context, disclosed here. All public-CLI probes, compilation/runtime checks,
gates, mutants, and corpus runs were newly executed against the named implementation bytes.

Only evidence files were added. Implementation source restored exactly and was not edited in the
commit. No install, publish, push, cache edit, native app, provider, Keychain, or live campaign
operation occurred. Receiver resolution, reader independence, output causality, and arbitrary
Never-returning calls remain outside the scanner's proof.
