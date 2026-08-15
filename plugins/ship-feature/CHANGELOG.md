# Changelog

## 2.0.0 - 2026-08-15

Moved from diolog-plugins and rebuilt as the conductor over the shipyard stages.

- Design runs in parallel with plan, gated by design-review and be-my-witness.
- Cross-family `verify` runs as a fresh agent before any merge; `Needs More Work` loops through gap-fix and re-verification, parked after three failed rounds.
- Four new pre-merge gate boxes: the verifier's verdict, a post-rebase e2e re-run, the keyboard/accessibility floor, and S3 sign-off where triage flagged it.
- A rollback procedure (revert the merge as one unit) is decided in the reference, not improvised during an incident.
- Decisions defer through the second-opinion lanes; unattended runs park questions instead of blocking.

## 1.5.3 and earlier

See the diolog-plugins history; this plugin's lineage lived there as ship-feature 1.x.
