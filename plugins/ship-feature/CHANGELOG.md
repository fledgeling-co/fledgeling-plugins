# Changelog

## 2.1.0 - 2026-08-19

- Phase 6 invokes `test-campaign` where installed, falling back to `acceptance-e2e`. A case the campaign cannot settle resolves to `unoracled` and phase 6a builds the missing oracle, rather than the case passing quietly.
- A requirement returned as `Unverified — no oracle` routes back to phase 6 rather than to gap-fix: gap-fix closes a gap between the work and its spec, and this is a gap between the spec and anything checkable.
- Phase 7 notes that verify's table now carries the oracle rung per requirement.

## 2.0.0 - 2026-08-15

Moved from diolog-plugins and rebuilt as the conductor over the shipyard stages.

- Design runs in parallel with plan, gated by design-review and be-my-witness.
- Cross-family `verify` runs as a fresh agent before any merge; `Needs More Work` loops through gap-fix and re-verification, parked after three failed rounds.
- Four new pre-merge gate boxes: the verifier's verdict, a post-rebase e2e re-run, the keyboard/accessibility floor, and S3 sign-off where triage flagged it.
- A rollback procedure (revert the merge as one unit) is decided in the reference, not improvised during an incident.
- Decisions defer through the second-opinion lanes; unattended runs park questions instead of blocking.

## 1.5.3 and earlier

See the diolog-plugins history; this plugin's lineage lived there as ship-feature 1.x.
