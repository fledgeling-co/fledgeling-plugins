# F25-065 attributed-helper reader-call repair

Fresh primary commit `dd80213b` is an operative FAIL receipt against implementation `68c0c5b`.
Through the public CLI, that review proved a helper scope could clear when its later caller text was
`let already = 1` or bare `read`; neither invokes a configured reader, yet the helper mutation left
the candidate population. The FAIL is retained and is not relabelled.

The repaired attributed-helper check now requires the configured reader stem to begin a masked Swift
identifier and that identifier to use parenthesized or trailing-closure call syntax. Qualified
`read()` and `read {}` remain accepted. `already`, `already()`, and bare `read` are permanent direct
and public-CLI refusals. The scanner remains deliberately lexical: this establishes executable call
shape, not receiver identity, reader independence, or output causality.

`mutations.py` independently removes the identifier boundary and call-syntax guard in the actual
scanner. Each source fault fails the permanent test under a unique Python bytecode cache, and the
source is restored exactly. The focused21-test group and complete114-test portable gate pass twice.
Catalogue generation remains byte-stable. Running the repaired scanner over the authored Perch
corpus accepts all108 scope records and leaves the same four honest blind bodies plus independent
REQ-056, so its red exit1 remains truthful.

CP §7 self-review covered the scanner predicate, its direct/public-CLI boundaries, both actual-source
mutants, changelog, scope contract and this evidence. The predicate runs only on already-masked
source after the exact helper-call occurrence; it cannot borrow comments, strings, earlier readers,
identifier substrings or bare names. No schema, raw denominator, plugin version, dependency,
installation, publication, cache, Perch registry/floor, native app, provider, Keychain or live call
changed. This is same-family degraded author work after a same-family primary finding; fresh primary
and distinct additional review are owed.
