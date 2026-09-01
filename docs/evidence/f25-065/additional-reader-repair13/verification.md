# F25-065 distinct additional review — multiline-terminal repair

## Verdict

**FAIL** against exact implementation `b9366d9ea6f282610dc64760a9f38586a8144e8e`.

The repair correctly preserves `return` and `throw` across ordinary newlines and masked comments. It still ignores an always-executed terminal nested inside an unconditional block, allowing a later top-level helper and reader to receive credit even though neither executes.

## Blocking false greens

The public CLI accepts all three source-valid forms below with exit 0 and no invalid scope:

```swift
@Test func measure() { do { return }; seed(); read() }
@Test func measure() throws { do { throw Failure() }; seed(); read() }
@Test func measure() { repeat { return } while false; seed(); read() }
```

The helper itself is top-level, but `reader_invocation_context` considers only `return`/`throw` at the minimum lexical depth. Swift always executes a plain `do` body and executes a `repeat` body once, so each terminal prevents the subsequent helper and reader. The compiled fixture emits unreachable-code warnings for all three and observes zero stores and zero reads. Its nonterminating `do` control reaches one store and one read.

## Terminal, trailing, and balanced boundaries

Same-line return/throw, multiline return/throw, block-comment-plus-newline return, line-comment-plus-newline return, and semicolon-separated return all fail closed. Six unsupported trailing spellings also reject: unparenthesized, parenthesized, qualified parenthesized, comment-separated, newline-separated, and multiple trailing closures. A direct helper followed by a reader, balanced nested arguments followed by a reader, and a nonterminating `do` followed by the helper and reader pass. A reader only inside helper arguments rejects.

## Gates and corpus

- Focused Swift/public-CLI suite: 21/21 twice.
- Full safe suite: 114/114 twice.
- Twelve actual-scanner mutants in an isolated extracted tree: all rejected; source restored byte-for-byte to SHA-256 `a9a23365aedbf12ba3daee8407a147447a72f10365feadc314e153ffd653a292`.
- Corrected Perch corpus at `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical runs, 108 scopes, 0 invalid, 0 attributed helpers, 22 direct outputs, 56 failure sentinels, 30 fixture values, four blind bodies plus REQ-056, five findings, expected exit 1.
- Plugin, root marketplace, and site catalogue remain at 0.16.2; catalogue parity passes in both full runs.

## Independence, restoration, and limits

This is a repeated same-family degraded additional review. Prior F25-065 and unrelated Fleet context was reused; the block-terminal attacks, whitespace/comment/semicolon and trailing matrices, compiled runtime witness, gates, mutant rerun, and corpus runs were newly executed against the named snapshot.

All mutations occurred in an isolated archive and restored exactly. The shared implementation was not edited; this commit contains only this additional-review directory and excludes the concurrent primary review directory. No install, publish, push, cache mutation, native app, provider, Keychain, or live campaign action occurred. The scanner deliberately refuses valid nested control-flow and trailing-closure helpers and does not prove receiver resolution, reader independence, or output causality.
