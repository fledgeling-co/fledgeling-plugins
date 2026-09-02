# Calibrating the instruments that produce the numbers

Use this file before publishing any counting figure — flows bound, cases enforced, bodies
empty, waivers honoured. `references/detector-defects.md` covers ways a *check* lies about
the product; this file covers ways an *instrument* lies about the suite. The schema is
`schemas/instrument-calibration.schema.json`.

The reason it exists, from the campaign it was built in: **the instruments were wrong more
often than the product.** In one day one number was measured wrong four separate times,
each reading plausible and each published (`flow-coverage-axes.md` §4). A backlog cut from
those figures inherits their error, and nothing downstream can detect it.

## 1 · The mechanism: a specimen of planted defects

Build a fixture root carrying deliberately planted defects, and a machine-readable record
stating, **per instrument per defect**, two separate things:

- `truth` — what a correct instrument would say about this defect.
- `known` — what this instrument actually says today.

Then a checker runs every instrument across the specimen and compares its output against
`known`.

Three outcomes, and they are not the same thing:

| outcome | condition | what it means |
|---|---|---|
| **DRIFT** | `actual != known` | the instrument's behaviour changed since it was recorded. **This is the only thing that sets the exit code** — the checker is green on a healthy tree and red the moment an instrument moves in either direction. |
| **CONDEMNED** | `known != truth` | the instrument misses a defect on its own stated axis. Printed every run, never silenced. **Every figure that instrument has published on that axis is void.** |
| **UNGUARDED** | no instrument has an axis covering this defect | nobody is watching. Declared with `known: "absent"` and a reason, so silence is a written finding rather than apparent health. |

**Condemnation is a standing fact about the instrument, not a warning.** A campaign that
prints a condemned instrument's figure under a headline it cannot support is publishing a
number it has already recorded as false. Withdraw the figure on that axis, or fix the
instrument.

**Never edit `known` to quieten a break.** When an instrument is improved and now matches
`truth`, raise `known` to `truth` in the same change as the fix. That ratchets, and it is
the only direction `known` moves.

## 2 · The six pathologies

These are the specimen's contents, and they transfer to any project with a coverage count.

| | planted defect | what it does in the wild |
|---|---|---|
| **P1** | a journey whose test genuinely passes | The control. An instrument that cannot report this one cleanly says nothing usable about the other five. |
| **P2** | a journey whose test genuinely fails | Statically indistinguishable from P1. Every static instrument calls it covered and is right on its own axis. Only a run separates them — **which is why a static coverage figure is not a coverage figure.** |
| **P3** | a test whose body is empty once comments are stripped | Planted on a **live** declaration, not a parked one. A parked empty body is honest about being unfinished; a live one is counted as a pass by every runner. |
| **P4** | a test whose title reads as covering a journey while it asserts nothing | Worse than P3, because the body computes. A reader skimming the file sees a populated test, and no product change can make it fail. |
| **P5** | a test unparked in the source that self-skips every run | What it selects on no longer exists, so the guard is true every run. The journey keeps its place in a coverage count for months after the control it gripped was removed. |
| **P6** | a journey exempted by a waiver pointing at a test that is itself parked | Both halves read as fine in isolation; only following the pointer shows the hole. |

A seventh worth planting where CI arithmetic matters: **a file listed in a blocking step
under a project that ignores it** — the fourth historical mis-measurement in
`flow-coverage-axes.md` §4.

## 3 · What calibration found when it was run

Nine instrument/defect pairs condemned on first run, over eight instruments:

- The empty-body instrument **missed P3, the exact defect it is named for.** Its
  declaration regex accepts only a parked declaration, so a live empty body is invisible.
- The inert-case instrument **missed P5.** Its stated axis is every case that never
  executes, and this case never executes; it matches only a park at the declaration.
- The CI-enforcement instrument **reported 6 of 6 enforced when 2 could fail a build.** It
  is correct as a wiring figure and wrong under the headline it prints — an empty body, a
  test that asserts nothing, a self-skipping test and a parked test cannot fail anything.
- **P4 and P6 had no instrument at all.** Nothing in that repository could tell a test that
  asserts from one that only computes, or read a waiver's pointer.
- The title-binding instrument **was correct on its own axis, and its figure was still not
  a coverage figure**: it bound all six specimen flows, including the four that cannot
  fail a build.

One defect found while building the specimen and left standing: the empty-body instrument
finds its declarations in **raw** source, so a declaration written inside a comment
matches. The first draft of P3's header comment made the instrument report P3 correctly
for entirely the wrong reason.

## 4 · Containment, proved rather than asserted

A specimen full of planted defects contaminates every real count unless it is kept out of
them. Put it outside every path a real instrument walks, and have the checker **prove**
it: run the static instruments — four, in that campaign — against the real project root as
well as the specimen, and fail on any specimen id or specimen path appearing in a real
count. In that campaign the
real figures with the specimen in the tree were unchanged — that run's own four counts,
552 enforced, 913 bound, 97 inert, 29 empty bodies, came back identical with and without
it. Its bound figure is 913 where the published axes table says 889; the two were read
at different moments by different instruments, and a disagreement of that size on one
axis is itself a calibration finding rather than a rounding difference.

Where a repository forbids mock or placeholder code, the specimen is a declared permanent
exception and the reason goes next to it: **a calibration standard with no known defects
measures nothing.** Deleting the fixtures to satisfy the guardrail removes the only thing
that can tell you a coverage instrument has stopped working.

**The declared weakness, which belongs in the record rather than in a caveat:** a
conservator's standard is inert and shares no material with the painting. This one is made
of the same stuff as the suite and lives in the same repository. It can tell you an
instrument changed; it cannot tell you the whole toolchain drifted together.

## 5 · Instrument pathologies worth carrying between projects

Each measured, each having produced a published wrong number:

- **An instrument that counts is not an instrument that matches.** A gate reading different
  arithmetic from its instrument is worse than no gate.
- **A gate glob can read the wrong population.** Identical counts across independent specs
  mean one shared cause, not agreement.
- **File-level inertness over-reports.** One park in a 40-case spec called 26 cards inert.
- **`git ls-files` makes untracked specs invisible** to any instrument built on it.
- **Summing per-item steps double-counts.** Count distinct flows: three flows bound to two
  files each turned a ceiling of 123 into 126.
- **"Does this string appear in the file" cannot distinguish a rewrite from a removal.** It
  reported seven assertions as deleted when every one had been replaced by a stronger form.
- **Parse JSON as JSON.** A regex extractor keyed on field order missed 3 of 17 records;
  "the first list found in the JSON" picked the wrong key. Key on the named field.
- **One field name, agreed before the writers run.** A gate read `existingCard` while agents
  wrote `card`, and one wrote `cardId`.
- **A derived file goes stale.** Derive counts from the spec tree at read time rather than
  from a checked-in tally.
- **Shell traps that fake a zero:** `grep -c` prints `0` and exits 1, so
  `$(grep -c … || echo 0)` yields `"0\n0"`; `grep -cE '^PASS'` read a working 7-of-7
  selftest as 0 because the output is indented; `rc=$?` after a pipeline reads the last
  command's status, and `${PIPESTATUS[0]}` does not exist in zsh.

## 6 · Arming — the only evidence a test can fail

Calibrating an instrument answers whether the count is honest. Arming answers whether the
case is. The loop: **back up with `cp` and verify the copy's size → break the thing → watch
RED for the intended reason → restore → watch GREEN.**

Three ways it goes wrong, all measured: an arming that **passes** is an unfinished arming,
not a pass; an arm can go red for the **wrong reason**, which proves nothing about the
assertion; and a false red is the mirror of an inert arm. One destructive trap is worth
naming because it silently empties the file it was protecting: writing a restore as
`open(p,'w').write(open(p+'.bak').read())` truncates the target before evaluating the read.

Where the task runner caches results, a cached target replays its previous PASS against
code you have just broken, and the run looks identical to a real one. Invoke the test
runner directly, or pass the cache-skipping flag, whenever the point of the run is to see
a red.
