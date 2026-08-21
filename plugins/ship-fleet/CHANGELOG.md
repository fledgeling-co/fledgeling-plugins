# Changelog

## 2.3.1 - 2026-08-21

- Correction from the research panel's fourth member: a tool withheld from an agent's context produces no refusal event at all, because a denied tool's definition is removed from the request. Surfacing refusals is therefore a fix for a different failure, and the capability manifest is the only surface an absence can appear on.
- Added the one item in the sweep with a controlled effect size: putting the terminal reason on the logger cut diagnosis time 60.7%, 10.37 minutes against 25.72, across 20 programmers, at 1.4% overhead.

## 2.3.0 - 2026-08-21

- Runner failure now specifies a channel sweep rather than "read the report". The report is the channel closest to hand and routinely the one the cause is absent from: measured, the reason appeared 36 times in the event stream, in none of 56 run records, and in none of 285,950 log lines that were being read and quoted.
- Four channels enumerated in order, including the token counts: an output-to-input ratio far above 1 means the agent is reciting its artifact rather than saving it, 33.8:1 on failed runs against 1.1:1 on completed ones.
- A standing rule not to harden the output while the cause is unidentified. On the run this comes from, 41 commits went into output gates and 15 into prompts before one touched the tool list.
- And preflight: if a job must persist a file and no permitted tool can write one, fail before the model is invoked.

## 2.2.0 — 2026-08-20

### Changed

- **A *ready-to-verify* report is treated as a claim about a bundle.** An item whose evidence
  bundle is empty goes back to its runner rather than into the verify queue, because verify's
  first act would be to discover that at the cost of a whole fresh agent.
- **A new standing rule: a fleet multiplies whatever the evidence layer gets wrong.** One
  campaign's captures filed by filename is a bad page; twenty items' verdicts resting on the same
  shape is a Done column nobody can audit. Where the repo carries a campaign,
  `test-campaign`'s `capture-lineage.py <dir> --gate` runs once per repo rather than once per
  item, and its exit code gates the column.

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
