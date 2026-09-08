# Stage 6: a check that cannot fail is not a check

## The measurement that sets the rule

Meta's TestGen-LLM deployment filtered **75% of compiling LLM-written tests as vacuous**.
Between **30 and 54%** of generated tests carry structural smells. And static reading is
rated **Low** at detecting the two shapes that dominate, because an LLM reading a test
treats a mock as a valid fixture and cannot simulate whether an assertion ran at all.

So the rule is mechanical rather than editorial: **a test the diff touched is unproven until
an injected fault makes it fail.** Break the line it covers, watch it go red, restore from a
`cp` backup, and record it. Never `git checkout --`.

Twenty-one such checks were found in one Atlas session, and **not one was found by running
the tests**.

## The shapes, each one real

- **The filter that excludes its own subject.** A guard written so "a new navigator cannot
  be missed" walked the app and filtered to files that already declared the anchor it was
  checking for. A new navigator without one was excluded by the filter, the count stayed
  correct, and it passed green. It excluded exactly the case it existed to catch.
- **The empty collection.** `[].every(...)` is `true` and `Math.min(...[])` is `Infinity`.
  Assert the population is non-empty before reducing over it.
- **The swallowing mock.** A `next/link` stub dropped the attribute the test asserted on. A
  fireEvent press walked up to an ancestor's handler, so deleting the child's own handler
  changed nothing.
- **The wrong twin.** Three controls carried the same accessible name and only two had test
  anchors; the case pressed the third, so blanking both anchored ones left it green.
- **The sanitiser mismatch.** A redaction assertion searched for punctuation the sanitiser
  strips, so a secret stayed readable while the assertion passed.
- **The placeholder that answers for the thing.** A footer assertion read `.*repl.*` and was
  satisfied by the composer's own placeholder, "reply to Sofie...", before any reply existed.
  A second read the posted text back and was satisfied by the composer's retained input:
  two consecutive runs passed it while the document was never written.
- **The neighbour's leftover.** A test asserting a deferred push was satisfied by a timer
  the previous test had scheduled. It had never proved its own.
- **One-way coverage.** A permission check asserted every rendered item was allowed, and its
  own comment warned that the reverse would pass on an empty menu. It had the same hole in
  the other direction.

## Two ways the measurement itself lies

- **A failed runner reads as untested code.** If a suite dies, its coverage map is never
  written, and every file in that package can be reported as unreached. Three maps went
  missing in one pass and 17 files read as untested when 16 were covered. Report a file
  whose runner failed as **unmeasured**, never as unreached.
- **A directory the tool creates.** A measurement script that writes into the tree it
  measures made its own second run fail and lose a whole runner.

## Waivers

A waiver carries a reason a reviewer could argue with. Two shapes have already been caught
being false here: "one-off script" and "type declarations only". The second was hiding a
file that exports a constant another module imports at runtime.
