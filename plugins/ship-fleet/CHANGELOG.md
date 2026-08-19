# Changelog

## 2.1.0 - 2026-08-19

- The fleet ledger carries the oracle mix across the run rather than a pass count. A fleet is where a Done column is built, so it is where an unauditable one starts: forty items closed on `presence` ship forty items nobody can audit later, and that surfaces months afterwards when the branch context is gone.
- An item returned `Unverified — no oracle` re-queues to phase 6 for oracle construction instead of to gap-fix.
- Where the repository carries a `.warrant/`, `campaign.py export-warrant` runs once at the end of the fleet, which is what lets the accumulated evidence earn a tier rather than the warrant refusing one permanently. For auditing a Done column that already exists, `warrant:lot` is named as the instrument.

## 2.0.1 - 2026-08-15

- Runner recovery routes through the `workflow-resume` skill; end-of-run questions consolidate via `whats-left`; long unattended fleets arm `better-goal` at launch.

## 2.0.0 - 2026-08-15

Moved from diolog-plugins and rebuilt over ship-feature 2.0.

- Per-item cross-family verification between ready-to-merge and merge; runners stop before verify and before merge.
- A `Needs verification` survey class: an item in review with no verdict is a gap, not a done.
- One global agent budget replaces the two caps that multiplied into rate-limit storms.
- The team-files/practices source is read from the repo's own CLAUDE.md instead of a hardcoded URL.
- The sanctioned low-cost runner shape is published, so cheaper hand-rolled briefs stop stripping safeguards.

## 1.5.2 and earlier

See the diolog-plugins history; this plugin's lineage lived there as ship-fleet 1.x.
