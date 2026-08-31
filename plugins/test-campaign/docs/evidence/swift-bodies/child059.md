# F25-059 — specific control-diagnostic expectations

Pinned exported upstream `65119b6` reproduces **111 passed /2 failed** in
`baseline-pinned-gate.log`. Both failures returned the expected exit1, but their common expected
phrase was retired when production split missing drives from failed effect measurements.

Only the two `tests/run.sh` diagnostic expectations changed. The first requires `declaring
control(s) nothing has driven`; the second requires `whose every declared control was driven
and not one drive produced a passing effect-rung result`. Existing exit1 checks, zero-of-three
census, outcome-rung positive control and undeclared-control rejection remain intact. No production
campaign rule, case fixture, oracle threshold or registry was changed.

`child059-green1.log` and `child059-green2.log`: **113 passed /0 failed**. The pinned baseline is
retained as failed, not retroactively reclassified. `arm_control_credit.py` exports the pinned
plugin, overlays the actual updated gate test, and mutates the real campaign actuation condition
only in that disposable copy to grant structural-rung credit. `child059-structural-mutant.log`
records the named below-outcome test failing because the mutated gate exits0 instead of1. Its JSON
receipt records unchanged production source hash and the exact mutation. This is executable
negative-control evidence, not a source-string predicate.

The child shares F25-050's versioned0.16.1 delivery and fresh independent reviews. Author validation
only; no merge, push, cache installation, native app, provider, credential or live registry action.
