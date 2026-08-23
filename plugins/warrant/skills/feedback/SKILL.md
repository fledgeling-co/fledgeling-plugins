---
name: feedback
description: >-
  Turn a case where the pipeline was wrong into permanent evidence — record the escape with the model
  versions and evidence digest that were live when it happened, build it into a regression case, and
  run the corpus again to confirm the current lanes still catch every escape ever reported. Use when a defect got past
  the pipeline, when an outcome did not match what the task asked for, or before granting any class
  tier 2. This is the plugin's calibration, and it replaces a prospective reader study.
---

# Feedback — calibration from escapes

An earlier design ran a prospective reader study to establish a baseline. It was cut because it
inverted the point: it spent human review time in order to remove human review time. This skill
learns from the cases where the pipeline was wrong and someone said so.

That is cheaper and it never goes stale. A study measures one model version on one date; the
regression corpus re-measures every version against every escape ever found, and it grows.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It forbids computing the escape rate that escape_report.py refuses to print, makes the corpus case count travel beside regress_run.py's exit code so an empty corpus cannot read as a tier-2 pass, and takes the recorded model version from lanes.toml rather than from what the run knows about itself. Other models skip it.

## Procedure

1. **Record the escape.**

   ```bash
   python3 scripts/feedback_record.py --root <repo> --class <name> --item <id> \
       --missed '<what the pipeline failed to identify>' --evidence-digest <digest> \
       --expected-verdict fail
   ```

   It captures the defect class, the item, the warrant version, the model ids and versions that
   were live at the time, and the evidence digest the wrong verdict was written from. The digest is
   what makes the escape reproducible rather than anecdotal.

2. **Build the regression case.**

   ```bash
   python3 scripts/regress_build.py --root <repo> --escape-id <id> --evidence-dir <dir>
   python3 scripts/regress_build.py --root <repo> --all      # every escape not yet built
   ```

   Writes `.warrant/regression/<escape-id>/` with the inputs and the verdict that should have been
   returned. Idempotent, so re-running it on a known escape changes nothing.

3. **Run the whole corpus again.**

   ```bash
   python3 scripts/regress_run.py --root <repo> --verdict-cmd '<command>'
   ```

   Every historical escape runs against the current lanes. Exit 2 names each case no longer caught.
   This is the tier-2 entry condition: a class may be closed by machine only while the machine
   demonstrably catches everything it has previously missed in that class.

4. **Watch for wrongly-failed items.**

   ```bash
   python3 scripts/falsealarm_proxy.py --root <repo>
   ```

   Reads the ledger for churn: an item that failed, was resubmitted without a substantive change,
   then passed. Same evidence digest across a fail and a later pass is the strong case. These are
   candidates from a proxy, and the output says so.

5. **Report counts and trends.**

   ```bash
   python3 scripts/escape_report.py --root <repo>
   ```

   Escapes per class, per month, time since the last escape per class, and which classes have never
   had one.

## What this measures, and what it cannot

Three limits, each stated because the tier ladder's wording depends on them.

**No false-rejection rate.** If the pipeline wrongly fails a good item and nobody reviews it, the
error is invisible. `falsealarm_proxy.py` recovers part of it from churn and is a proxy rather than
a measurement. The cost of a false rejection is friction rather than escape, which is why the
pipeline can survive not measuring it.

**A numerator with no denominator.** You learn about escapes that were noticed. `escape_report.py`
therefore emits counts, classes and trends, and refuses to print a rate — asked for one, it exits 1
with the reason. The cautionary case is `C19`: published proficiency-test failure rates differ by
more than twentyfold depending on what is counted, 1.4% of 670,489 challenges across 665
laboratories against 32.4% of lab-parameter results across three, and both figures were correct.

**No bound on what is still hidden.** Without seeded items there is no way to estimate the misses
nobody found. The corpus proves the pipeline catches known failure modes and says nothing about
novel ones.

## Output

`feedback_record.py` appends one row to `.warrant/escapes.jsonl` and prints the escape id.
`regress_build.py` writes one directory under `.warrant/regression/`. `regress_run.py` prints one
line per case and exits 2 listing any no longer caught. `escape_report.py` prints counts and trends
and never a rate.

## Constraints

Record the model versions that were live at the time, not the current ones. An escape attributed to
today's version is an escape nobody can reproduce.

Keep every case forever. A regression corpus that prunes old cases loses exactly the evidence that
makes a tier defensible, and the cases are small.

Report a class with no escapes as having no escapes rather than as reliable. Absence of a reported
escape in a class nobody has exercised is not evidence about the class.
