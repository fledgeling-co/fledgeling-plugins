# Changelog

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
