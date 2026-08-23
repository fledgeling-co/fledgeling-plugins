---
name: oracle
description: >-
  Close the highest-consequence defect class with arithmetic rather than judgement — source-to-render
  lineage on every displayed figure, tick-and-tie against the originating record, and taxonomy
  validation on classified fields. Use before the panel plane runs, when a rendered number
  needs to be traced to what produced it, or when a screen reads as correct and the figure on it is
  wrong. It needs no model, cannot reversion, and is the plane that runs first.
---

# Oracle — the deterministic plane

The instinct is to start with the screenshot judge, because that is the part that looks like
verification. Start here instead.

The worst thing a data-dense product can do is not a misaligned button; it is a well-rendered page
stating a figure no source supports. A vision judge cannot catch that, because nothing on the
screen looks wrong, and the best published labelled UI-display-defect detectors reach about 85%
precision and 84% recall anyway (`C17`) — a ceiling that says nothing about unsupported numbers,
which were never a visual defect. That class is closable by arithmetic (`I7`), and this skill is
the arithmetic.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It routes step 1's template markup pass to another model, gives the four-attribute sweep a per-surface denominator, and turns every coverage claim into a pasted exit code. Other models skip it.

## Procedure

1. **Mark up the surface once.** Four attributes, and they are a change to the product rather than
   to the pipeline:

   | Attribute | On every displayed figure |
   |---|---|
   | `data-figure-id` | names the figure, and is what a mismatch report cites |
   | `data-source-ref` | names the record it came from. A figure without one is the defect this plane exists to find |
   | `data-source-field` | names the field within that record |
   | `data-source-expr` | for a derived figure, the expression instead of a field: `sum(segments.amount)` or `count(segments)` |

   The expression form is what catches a total that no longer equals the sum of its parts, which is
   the most common wrong-number-on-a-right-looking-page defect there is.

2. **Extract and gate the lineage.**

   ```bash
   python3 scripts/lineage_extract.py --root <repo> --input <rendered.html> --json
   python3 scripts/lineage_gate.py --root <repo> --input <rendered.html>
   python3 scripts/lineage_gate.py --root <repo> --glob 'dist/**/*.html'   # a whole surface set
   ```

   The gate exits 2 naming every unsourced figure and writes `.warrant/oracle-coverage.json` with
   per-surface coverage. That coverage number is what `ratchet` reads to decide tier 1.

3. **Tick and tie.**

   ```bash
   python3 scripts/tick_and_tie.py --root <repo> --input <rendered.html> --sources <dir>
   ```

   Each figure is recomputed from its source record and compared. Tolerances come from the
   warrant's `[oracle.tolerance]` table: exact for integers, relative for floats. Exit 2 names the
   figure, the rendered value, the source value and the tolerance that was applied — all four,
   because a mismatch report missing the tolerance cannot be acted on.

4. **Validate the taxonomy.**

   ```bash
   python3 scripts/taxonomy_check.py --root <repo> --taxonomy <taxonomy.json> --records <dir>
   ```

   This catches the failure the other two miss: a valid-looking value sitting in the wrong field.

5. **Roll the coverage up per defect class.**

   ```bash
   python3 scripts/rollup_classes.py --root <repo>
   ```

   `lineage_gate.py` measures a surface; authority is held per defect class. This maps one onto the
   other through the class-to-surface globs in the warrant, and `ratchet` reads the result. A class
   no surface matched comes out not-green rather than absent, because no evidence is a different
   answer from a pass.

6. **Record the result.** Coverage and mismatches go to `.warrant/reports/`, and the pass or fail
   goes to the ledger through `warrant:ledger`.

## Which checks belong here rather than in the panel

A check belongs in this plane when its question can be answered without a judgement. The test is
whether two competent people reading the same record would give the same answer. "Does this figure
equal what the source says" passes that test; "does this screen look finished" does not.

Move a check here whenever it can be moved. A lens lane in `warrant:panel` costs a model call per
item forever and can reversion; a script here costs nothing per run and cannot.

## Output

`lineage_extract.py` prints a JSON report of figure-to-source pairs. `lineage_gate.py` writes
`.warrant/oracle-coverage.json` and exits 2 naming every unsourced figure. `tick_and_tie.py` exits 2
naming the figure, the rendered value, the source value and the tolerance applied.
`taxonomy_check.py` exits 2 naming the field and the disallowed value.

## Constraints

Parse HTML with `html.parser`, not with a regex. A figure inside an attribute value or a comment
is exactly the case a regex gets wrong and a parser gets right.

Report a missing source as missing rather than inferring one from the value. An inferred source is
the failure this plane exists to detect, arriving through the detector.

State coverage with its denominator. "94% covered" without the figure count is the shape the
denominator error arrives in; `references/measurement.md` carries why.
