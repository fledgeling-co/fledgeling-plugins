---
name: assay
description: >-
  Measure the test suite's fault sensitivity before any verdict built on it is believed — mutation
  survival over the tests CI actually selects, a scan for assertions that cannot fail, and the gap
  between authored and selected tests by surface. Use before granting any class tier 2, when a suite
  is green and trusted without evidence, or when a defect escaped a passing pipeline. It reports a
  number rather than an opinion, and a first run that returns a bad number is a success.
---

# Assay — measure the tests before believing them

Every downstream number inherits the suite's fault sensitivity, and a green suite can have very
little of it. More than half of over 15,000 generated mutants survived a rigorous unit, integration
and system suite that was passing (`C18`). That was one company's codebase; nobody has measured
mutation survival for browser or end-to-end suites at all, which is exactly why it has to be
measured here rather than assumed from the literature.

The second reason this plane exists is subtler. A suite can pass because it is not looking. An
assertion with no matcher, a matcher comparing a value to itself, a swallowed exception — each
reads as coverage and tests nothing.

## Procedure

1. **Mutate the set CI actually runs.**

   ```bash
   python3 scripts/mutate.py --root <repo> --targets <file-list> --test-cmd '<command>'
   ```

   Mutate against the selected set, not the authored one. The selected set is what gates a merge,
   so its sensitivity is the one that matters — and in the target repository CI selects 420 of
   roughly 3,011 authored instances across 137 spec files (`C23`), so the two numbers are far
   apart. The script copies to a temporary directory and never mutates the working tree.

   It writes `.warrant/suite-health.json` with a ratchet: the score may rise and the high-water
   mark rises with it, and a drop below the mark exits 2.

2. **Scan for assertions that cannot fail.**

   ```bash
   python3 scripts/cannotfail_scan.py --root <repo> --glob 'apps/web/e2e/**/*.spec.ts'
   ```

   Eight patterns, each of which passes a suite while testing nothing: an `expect(...)` with no
   matcher; a matcher whose expected value is the actual value; a constant compared to a constant;
   a `catch` block that swallows the failure; an assertion inside a callback that is never awaited;
   `test.skip` and `test.todo`; a discarded `expect.soft`; and a spec file with zero `expect` calls.

   This one reports rather than gates, because the count is a trend and a first number has nothing
   to be compared against.

3. **Find the surfaces with no gate on them.**

   ```bash
   python3 scripts/selection_gap.py --root <repo> --authored <list> --selected <list>
   ```

   Authored tests that never run in CI, grouped by the surface they cover. A surface whose tests
   are all outside the selection is a surface with no gate, and no verdict about it should be
   trusted at tier 2 or above.

4. **Roll the result up per defect class.**

   ```bash
   python3 scripts/rollup_classes.py --root <repo>
   ```

   It writes the `classes` block and the single `green` flag that `charter_validate.py` and
   `ratchet` read. A mutation score with no recorded high-water mark is green on its own score; a
   score below the mark is not; no measurement at all is not.

5. **Record all three.** `ratchet` reads `suite-health.json` and will not grant tier 2 to a class
   whose surface appears in the selection gap.

## What a bad first number means

It means the measurement worked. A mutation score of 40% is information; the absence of a mutation
score is not. Record it, set the ratchet, and improve from there.

What is not acceptable is a suite that has never been measured being treated as evidence. That is
the state the whole plane exists to end.

## Output

`mutate.py` writes `.warrant/suite-health.json` and prints the score with its numerator, its
denominator and the breakdown by mutation kind. `cannotfail_scan.py` prints file, line and pattern
per finding, with a count. `selection_gap.py` prints never-run tests grouped by surface.

## Constraints

Never mutate the working tree. Copy to a temporary directory and run there, so an interrupted run
cannot leave a mutant in the repository.

Report the mutation score with its numerator and denominator, and with the mutation kinds broken
out. An aggregate score hides the case where one operator class is never killed, which is the
finding worth acting on.

Treat `cannotfail_scan.py` findings as candidates rather than defects. A skipped test is sometimes
correct, and the scan cannot tell; the human-readable output says which pattern matched so the
reader can judge.
