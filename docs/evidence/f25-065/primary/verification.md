# F25-065 upstream PRIMARY review — FAIL

Reviewed `83aed5312078f4cb58153f39c4645b895e0c88fd` independently from the Perch
brief, spec and plan. I previously consulted/reviewed unrelated Perch work in this reused thread;
the unavailable fresh lane makes this same-family review degraded, and a distinct additional review
remains required. I did not author or alter implementation source.

## Blocking findings

1. **The strict schema fails open for JSON booleans and configured falsy non-strings.**
   `load_blind_scopes` treats every falsy `blindScopeFile` value as absence (lines 97-101), accepts
   `version: true` because Python equates `True` and `1` (line 106), and accepts `callOffset: true`
   because `bool` is an `int` (line 124). The public CLI probe supplies an otherwise exact record
   whose real call offset is 1. It accepts both booleans, suppresses the only mutator, reports
   `direct-output=1`, and exits 0. Separate public CLI runs configure `false`, `0`, `{}` and `[]`;
   all exit 0 without `INVALID SCOPE`. A present malformed configuration therefore can silently
   clear instead of gating red.

2. **Attributed helpers are not bound to named callers.** The record schema has no caller field
   (lines 114-115), and the inclusion rule only checks that the helper body has an
   `attributed-helper` scope (lines 712-716). The public CLI probe binds `seed.write()` and supplies
   an unrelated file hash as its sole reference; it names no caller and binds no caller body or
   helper-call occurrence. The gate accepts it, reports `attributed-helper=1`, and exits 0. The
   implementation cannot enforce the plan's named, source-bound caller requirement.

3. **The generated site catalogue is stale.** The plugin and marketplace manifests advertise
   0.16.2, while `site/lib/catalogue.json:917` still advertises 0.16.1. The catalogue builder states
   that it generates this shipped site surface from the marketplace; the prior 0.16.1 release
   updated all three. This release leaves installation metadata inconsistent.

## Verified behavior and boundaries

- Exact file/name/body/call matching, receiver-plus-call spelling fingerprinting, duplicate/use
  checks, reference hash drift, and gate propagation are otherwise source-bound and fail closed for
  the covered ordinary values.
- Removing one exact call and re-evaluating earlier mutation calls is preserved. `mutating` is
  counted before removal, so the raw mutating-body denominator remains intact; scoped counts remain
  separate by class.
- Called helpers remain excluded unless an attributed-helper record exists. The missing part is the
  required caller binding, not helper discovery itself.
- A valid campaign-relative producer reference loads successfully. Scope file paths resolve from the
  campaign directory, while scope `file` identities remain relative to the selected test root.
- The author's three disposable source mutants all loaded and failed assertions rather than merely
  failing syntax/import, and their receipt records source restoration. They cover skipped call
  fingerprinting, whole-body suppression and global `record` exclusion, but do not exercise the
  three blockers above.

Both independent runs of `plugins/test-campaign/tests/run.sh` passed 114 tests with 0 failures and
the focused Swift suite passed all 17 cases. Those green suites do not cover the invalid schema
values, caller binding, or catalogue regeneration. No full native, provider, Keychain, app, install,
publish or cache operation was run.
