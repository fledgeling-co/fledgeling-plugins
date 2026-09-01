# F25-065 upstream fresh PRIMARY review

**Verdict: FAIL** for exact cumulative implementation author head
`68c0c5b74b0d143b8738fc7e1c4283a0e2c89b6c`.

## Blocking finding

`vacuity-check.py:816-817` treats any later text matching a configured reader prefix as the bound
caller's reader:

```python
re.search(re.escape(reader) + r"\w*", masked_caller[offset + match.end():])
```

That expression has neither an identifier boundary nor call syntax. Through the public CLI, a valid
attributed-helper scope over each of these callers exits 0 with reader vocabulary `["read"]`:

```swift
@Test func measure() { seed(); let already = 1 }
@Test func measure() { seed(); read }
```

Neither caller invokes a reader. The scope nevertheless removes the helper's mutating `store()` body
from the candidate set, so arbitrary executable identifiers can supply an unjustified helper
attribution. This is distinct from the documented reader-independence limitation: the accepted text
is not a reader call at all.

The probe isolates the boundary with valid opposites. Receiver-qualified parenthesized
`Fixtures.seed(); read()` and trailing-closure `Fixtures.seed { configure() }; read()` callers exit 0.
A reader only before the helper, a later reader only in a comment, and one only in a string each exit
1 as invalid scopes. The repair should require an executable configured reader call after the exact
helper-call occurrence while preserving the scanner's explicitly lexical posture.

## Passing evidence

The strict public loader rejects configured `false`, `0`, `{}`, and `[]`; Boolean `version` and
`callOffset`; integer `testEntry`; unknown top-level and row fields; empty producer hash; unknown
classification; stale body/call hashes; and duplicate scopes. Target and caller body/posture/call
bindings, stale call offsets, unmatched files, comment masking, parenthesized/trailing-closure
callers, exact-one-call removal, raw
mutating-body counts, earlier-call re-evaluation, and absence of global `record`/`store`/`apply`/
`update` suppression otherwise held.

Four exact-source-copy mutants failed independent assertions: whole-body suppression after one
scope, accepting a comment-only caller spelling, ignoring target test-entry posture, and globally
suppressing the four mutation verbs. The reviewed scanner source stayed byte-identical to author
HEAD (`3921b034…44b7`). Focused Swift tests passed 20/20 twice; the complete portable gate passed
114/114 twice. All three version surfaces and the generated catalogue report `0.16.2`, and catalogue
generation left its tracked bytes unchanged.

Commit `611bd1151b47f257069e184b7608f582f297200a` is later than the reviewed implementation and changes
only nine files under `docs/evidence/f25-065/additional/`; it was left intact and was not treated as
implementation.

This is a fresh primary review of the new cumulative author head by a reviewer who assessed an
earlier repair. It is same-family degraded with reused unrelated Perch F25-066, F25-034, F25-064,
and F25-067 context; it is not an out-of-family lane. No install, publish, cache edit, push, merge,
rebase, native app, provider, Keychain, or Perch corpus application was performed.

Run `python3 docs/evidence/f25-065/primary-final/probe.py` to reproduce the source-bound and public-CLI
evidence.
