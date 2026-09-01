# F25-065 distinct additional review — prior-terminal conservative repair

## Verdict

**PASS** against exact implementation `1fc56e939cb95b05ae1739f305de89a0aac3fc56`.

The conservative all-prior-terminal rule closes every retained helper false green. No false acceptance was found across same-line, multiline, commented, nested-block, direct, balanced-argument, or trailing-closure boundaries.

## Public and runtime boundaries

The public CLI rejects helpers after same-line and multiline `return`/`throw`, block-comment-plus-newline return, unconditional `do` return/throw, and once-running `repeat` return. It also rejects all six tested trailing spellings: unparenthesized, parenthesized, qualified parenthesized, comment-separated, newline-separated, and multiple trailing closures.

Comments and raw-string literals containing `return`/`throw` do not poison a valid direct helper. Direct and qualified calls, a nonterminating `do`, and balanced nested arguments followed by a reader pass. A reader only inside helper arguments rejects.

The compiled fixture confirms the valid comments/literals, escaped-identifier, and balanced controls execute three stores and three reads, while unconditional terminal blocks execute neither their helper nor reader. The scanner deliberately rejects the escaped `` `return` `` control even though it runs: the lexical mask removes its backticks, and the all-prior rule treats the resulting word conservatively. This is an additional explicit false-negative boundary, not a false pass; the existing contract already chooses false negatives for safe conditional terminals.

## Gates and corpus

- Focused Swift/public-CLI suite: 21/21 twice.
- Full safe suite: 114/114 twice.
- Twelve actual-scanner mutants in an isolated extracted tree: all rejected; source restored byte-for-byte to SHA-256 `6c58fdea3e61069fdb4695bbdd4d564e3eea2eedef38f9467ad1e0f2a79071e0`.
- Corrected Perch corpus at `c30595e14403240d7933c1d20ec4728eb3281770`: two byte-identical runs, 108 scopes, 0 invalid, 0 attributed helpers, 22 direct outputs, 56 failure sentinels, 30 fixture values, four blind bodies plus REQ-056, five findings, expected exit 1.
- Plugin, root marketplace, and site catalogue remain at 0.16.2; catalogue parity passes in both full runs.

## Independence, restoration, and limits

This is a repeated same-family degraded additional review. Prior F25-065 and unrelated Fleet context was reused; the conservative-terminal attack, comments/literals and trailing matrices, compiled runtime fixture, gates, mutant rerun, and corpus runs were newly executed against the named snapshot.

All mutations occurred in an isolated archive and restored exactly. The shared implementation was not edited; this commit contains only this additional-review directory and excludes the concurrent primary review directory. No install, publish, push, cache mutation, native app, provider, Keychain, or live campaign action occurred. The scanner deliberately refuses valid callers after any earlier masked return/throw, including unreachable conditional terminals and escaped keyword identifiers. It also refuses valid nested and trailing helper calls and does not prove arbitrary `Never` calls, build configuration, receiver resolution, reader independence, or output causality.
