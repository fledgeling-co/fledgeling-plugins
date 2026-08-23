---
name: ratchet
description: >-
  Compute the tier of authority each defect class has currently earned, apply revocations immediately
  without asking, and write promotions as proposals for the owner to sign. Use after any oracle, assay,
  panel, feedback or lot run, on a schedule, and whenever a lane's pinned model changes. It is a plain
  script rather than a model call, because the component deciding how much authority a model holds
  should not be the model.
---

# Ratchet — the governor

This is what makes the plugin a system rather than a checklist. It reads what the other planes
produced, decides what each class has earned, and takes authority away on its own.

The asymmetry is deliberate. Revocations apply immediately and need no signature. Promotions are
written as proposals, because a class gaining authority is a policy change and `warrant:charter`
owns those.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It says the tier table is the script's output rather than yours, that exit 4 is a completed revocation and not a retry, and that restoring a tier is never one of the available actions. Other models skip it.

## Procedure

1. **Run it after anything that produces evidence.**

   ```bash
   python3 scripts/ratchet.py --root <repo>
   ```

   It reads `.warrant/suite-health.json`, the regression result, `.warrant/oracle-coverage.json`,
   `.warrant/escapes.jsonl`, `.warrant/warrant.toml` and `.warrant/lanes.toml`.

2. **Read the exit code.** Exit 0 means nothing changed or a promotion was proposed. Exit 4 means a
   revocation fired and has already been applied.

3. **Check the control chart on a cadence.**

   ```bash
   python3 scripts/westgard.py --root <repo> --series <corpus-history.json>
   ```

   A multirule chart over the regression corpus pass rate across runs: 1-3s, 2-2s, R-4s, 4-1s and
   10-x. The multirule form is not decoration — a single-threshold alarm on a true-negative-heavy
   queue either never fires or fires constantly, which is why clinical laboratories stopped using
   one.

4. **Revoke by hand when you have a reason the script cannot see.**

   ```bash
   python3 scripts/revoke.py --root <repo> --class <name> --reason '<why>'
   ```

   The reason is required. A revocation with no recorded reason is indistinguishable later from a
   mistake.

## The six revocation triggers

| Trigger | Why it revokes |
|---|---|
| a pinned model id or version differs from the one recorded against the class's last regression run | the control changed, so the benchmark no longer holds (`C12`) |
| the regression run is failing | the machine no longer catches something it has already missed once |
| a new escape in a class above tier 0 | the class was closing items it should not have been |
| a Westgard violation | the corpus pass rate is drifting rather than dipping |
| oracle coverage below the class's tier-1 threshold | the deterministic plane stopped covering the surface |
| the class's calibration is older than `[staleness] calibration_max_days`, or it has none | evidence that has gone stale is not evidence, and a class whose age cannot be established is treated as stale |

## What the ladder can and cannot claim

Entry to tiers 2 and 3 is by absence of escapes rather than by a measured sensitivity, and that is
weaker evidence. Absence of escapes is bounded by what got noticed, so it gains weight from volume
and time and never becomes a rate. The plugin is built this way because the alternative was a reader
study nobody was going to run twice; `references/tiers.md` carries the full comparison and why tier 4
is in the table at all.

A class the warrant does not name sits at tier 0. That default is the safety property: a class
nobody wrote down is a class no machine may close.

## Output

`ratchet.py` prints the tier held and the tier earned per class, applies revocations, writes
promotions as proposals, and exits 4 when a revocation fired. `westgard.py` exits 2 naming the rule
that tripped. `revoke.py` prints the class, the reason and the ledger row it appended.

## Constraints

Keep this a script. A model deciding its own authority is the one structure that makes every other
guarantee here unfalsifiable, and the temptation to make the tier decision "smarter" is the
temptation to remove the property that makes it trustworthy.

Apply a revocation before reporting it. The order matters if the run is interrupted: a revocation
reported but not written is a class still holding authority it has lost.

Never restore a tier as part of a revocation run. Promotion is a separate act, by a person, in
`warrant:charter`, reading the evidence that earned it.
