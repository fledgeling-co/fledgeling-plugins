# Testing adequacy

A green suite is a claim about the code. These are the checks that test the claim,
drawn from `create-test-suite` and from defects found in practice.

## The rung of oracle

Every critical requirement stands on some rung, and the rung is recorded:

1. **It exists** — an element is present, a route answers.
2. **It says the right thing** — content matches an expectation.
3. **It does the right thing** — an action produces a state change.
4. **It produces the right value** — the number ties back to a source.

A requirement that moves money, publishes to the public, or asserts a disclosure fact
and stands only on rung 1 **fails the gate**. It does not pass quietly with a note.

The highest-consequence failure in a reporting product is a beautiful screen stating a
number no source supports — and that class is addressable deterministically, by tying
the value back to its source, rather than by any amount of visual judgement.

## Armed and unarmed assertions, counted apart

An unarmed assertion is one that cannot fail. They read exactly like coverage. Five
shapes, all found in real suites:

- **Self-comparison.** `expect({a, b}).toEqual({a, b})` — both sides built from the
  same locals. Found twice in one session's own work, each time under a comment
  describing behaviour the assertion did not have.
- **Type-only, where two paths raise the same type.** A guard and the code under test
  both throwing `BadRequestException` means a type assertion passes on the wrong throw
  and the subject never runs. Assert the message.
- **A fixture the product never produces.** A stripper tested against an unescaped
  string while every stored document escapes it: fourteen green cases, and a no-op in
  production.
- **A substring grep for a variable's name.** `expect(SRC).toContain('requestId')` is
  satisfied by the declaration and says nothing about the value.
- **A slice that misses its subject.** A source-reading assertion whose window stops
  before the code it is looking for fails, or passes, for the wrong reason.

**The cheapest real check is to break the thing and watch the test go red.** A test
nobody has seen fail is a test nobody has seen work. When red-arming, verify you
edited the line the test actually guards — reverting the wrong one of two similar call
sites proves nothing, and has been mistaken for a weak test more than once.

## A denominator

Cases run over cases that exist, and the skipped set named. A suite reporting green
across 13.9% of itself is reporting on 13.9% of itself, and the number is invisible
unless something prints it.

Ask three questions and record the answers: how many cases exist, how many the gate
actually selects, and which areas have nothing selected at all. Unselected areas are
where unwatched failures live — including, in one measured case, two P0s.

Marker-counting is not this. A gate that counts `skip` markers cannot see a case that
is **enabled and cannot pass**, which is strictly worse than a skip: it reads as
coverage from every angle and its only signal is a red run somebody eventually widens
away.

## Fault sensitivity, where the stakes justify it

A mutation delta, not a count. More than half of over 15,000 mutants survived a
rigorous suite at Facebook; if the selected cases have weak fault sensitivity, the
gate is weaker than its pass rate implies.

This is expensive and does not belong on every card. Reach for it when a card's whole
claim rests on its tests, or when the same area has produced repeat escapes.

## Provenance

The suite is written by the party being judged. METR documents frontier agents editing
tests, monkey-patching evaluators, and returning the scorer's own reference tensor;
one benchmark was retired over leakage. Nothing attests test provenance the way build
provenance is attested.

Practically: check whether the tests changed in the same change as the code they
guard, and whether any assertion was widened rather than fixed. An assertion loosened
until it passes is worse than a skip, because the skip is visible.
