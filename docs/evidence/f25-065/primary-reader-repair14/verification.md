# F25-065 upstream primary review — conservative prior-terminal repair

## Verdict

**PASS** against exact implementation `1fc56e939cb95b05ae1739f305de89a0aac3fc56`.

The repair implements the declared conservative boundary: an attributed helper is refused whenever
any executable, Swift-masked `return` or `throw` token precedes it in the caller body. The rule closes
the retained same-line, newline, comment-newline, `do`, and once-running `repeat` false greens. I
found no remaining false acceptance in the tested helper-call, reader-suffix, or terminal families.

## Independent boundary attack

A 26-case public-CLI matrix exercised newly generated source-bound scope hashes, offsets, caller
bindings, and test-entry booleans against the real `--gate` path. All outcomes matched:

- Direct and qualified helpers, an ordinary semicolon boundary, and balanced helper arguments
  followed by a distinct reader pass.
- Comments and string literals containing `return`/`throw` are masked and do not poison a valid
  helper.
- Same-line, newline, and block-comment-newline `return` and `throw`; prior semicolon terminals;
  unconditional `do` return/throw; and once-running `repeat` return all refuse.
- Helpers nested in control flow; a reader only inside helper arguments; and bare, parenthesized,
  comment-separated parenthesized, and multiple trailing closures all refuse.
- As the new contract deliberately requires, valid code after `if false { return }`, after a stored
  but uncalled closure containing `return`, and after an escaped `` `return`() `` call also refuses.
  These are explicit false-negative boundaries, not credited scopes.

The companion Swift fixture typechecked. At runtime it printed `stores=7 reads=1` after the terminal
matrix and `final stores=12 reads=6` after executing the conservative false-negative and valid
controls. This confirms that the unconditional terminal suffixes are unreachable while the named
false-negative controls really do reach their helpers and readers.

## Gates, mutants, and corpus

- Focused Swift/public-CLI suite: 21 tests twice, both exit 0.
- Full safe plugin suite: 114 passed / 0 failed twice.
- Twelve isolated actual-scanner mutants all failed the focused oracle: call syntax, placeholder,
  reader trailing closure, nested reader, conditional reader, helper execution context, terminal
  refusal removal, narrowing the terminal rule back to the current statement, parenthesized helper
  trailing closure, argument scanning, top-level reader terminal, and invocation context. Source
  restored byte-for-byte to SHA-256
  `6c58fdea3e61069fdb4695bbdd4d564e3eea2eedef38f9467ad1e0f2a79071e0`.
- Corrected Perch corpus `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical
  runs; 108 scopes, 0 invalid, 0 attributed helpers, 22 direct outputs, 56 failure sentinels, and
  30 fixture values. Both remain honestly red on four blind bodies plus uncensused REQ-056: five
  findings, expected exit 1.

## Independence and limits

This is a repeated same-family degraded primary lane; workflow and out-of-family lanes were not
available in this session. I did not author the upstream repair. The review reused prior F25-065,
F25-034, and F25-015 context, disclosed here. The public-CLI matrix, Swift compilation/runtime
fixture, gates, mutants, and corpus runs were freshly executed against the named implementation.

Only evidence files were added. The implementation source restored exactly and was not edited in
this commit. No install, publish, push, cache edit, native app, provider, Keychain, or live campaign
operation occurred. The deliberate conservative refusals above remain visible. Receiver resolution,
reader independence, output causality, arbitrary `Never` calls, and control-flow proof remain outside
the scanner's claim.
