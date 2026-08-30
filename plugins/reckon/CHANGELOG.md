# Changelog

## 1.9.2 - 2026-08-31

Two retirement-entitlement fixes, both found on one project in one morning.

**Briefs citing CASE and REQ ids resolved to no oracle at all.** The retirement rung is
computed from `case_by_surface`, which was indexed only by a case's `surface`. A brief
cites what somebody wrote in it, and that is routinely a CASE or a REQ; such a citation
resolved to nothing, `best_rung` fell to -1, and the row was reported as "the strongest
oracle behind it is 'none', below the outcome floor" -- an absent reading rendered in the
words of a weak one. Measured on graft: two briefs citing CASE-0053 (`outcome`) and
CASE-0107 (`effect-witness`) directly were both held `undecided` and routed to
spec-validation, which read the real evidence and ruled RETIRE on both. The index now
carries each case under its own id and its req ids beside its surface.

**A brief that declares its own status was never asked before being retired.** The
classifier computed whether the registry's evidence read done and never compared that to
the brief's declared `status:`. A brief filed an hour earlier, citing passing cases as
context for the refusals it exists to fix, classed as `retirable`. A declared status that
is not a done-or-waived word now blocks retirement and the row lands `undecided` with the
disagreement named -- the document and the evidence disagree, a person rules. Empty status
is honoured as no claim: most queues carry none, and their behaviour is unchanged.

Both directions were observed on the same run: two briefs wrongly held `undecided` moved
to `retirable`; six briefs wrongly `retirable` moved to `broken` because the newly-visible
citations included failing cases. The join now sees what the briefs actually cite.

## 1.9.1 - 2026-08-31

`reckon build` refused any project that had something to retire.

1.9.0 added a conservation check over the schedule: every work item must be in a wave or on
the decision list, or the total is a figure about a subset. But `build_waves` only ever
placed three of the four work kinds — it schedules `product-work` and `evidence-work` and
names `decision-work`, and `bookkeeping` was in none of them. So a `retirable` row, which
is a row already done well enough to close, was counted as work and then accounted for
nowhere, and the build exited 1 saying the directory "is not a run".

That made the check unsatisfiable rather than strict: the only projects it passed were the
ones with nothing to retire. Measured on graft, 2026-08-31 — 83 of 199 work items lost, over
a partition that was otherwise sound.

`build_waves` now returns a `bookkeeping` list beside `decisions`, and the check counts it
as accounted. Bookkeeping is named rather than scheduled for the same reason decision work
is: closing a retirable row is a person editing a ledger, and giving it a wall-clock figure
would report a filing job as an agent being busy. The check is otherwise unchanged — a
product-work or evidence-work item that falls out of every wave is still a violation.

## 1.9.0 - 2026-08-30

Reckon now schedules what it finds, and publishes a board somebody can show a room.

**The schedule.** The ledger becomes a wave plan using `ship-fleet`'s model — nodes are
work items, edges are dependencies, a wave is everything whose dependencies sit in earlier
waves. Two things differ, and both are about entitlement: a `cited` edge is a citation
somebody wrote and it blocks, while an `inferred` edge is this tool reading a shared
surface and it only orders the work; and decision work is never scheduled at all, because
a person reading two documents has no agent duration and giving it one reports waiting on
a human as though a machine were busy.

**The estimates.** Every work item and every blocker cluster carries a wall-clock range,
drawn from a corpus of 1,842 measured Opus 4.8 and Opus 5 subagent runs across 88 sessions
and 31 projects (14 Jul – 30 Aug 2026), parsed from Claude Code's own transcripts.
Provenance, method, tables and limits: `references/estimation.md`.

Three properties, each because its absence produces a specific lie:

- Always a range, never a number. Measured p90 ÷ median is 3.4 for build work and 3.1 for
  research, so a point estimate is wrong by a factor of three in the ordinary case and
  reads as precision.
- No schedule may beat what was observed. Measured speedup over serial was 2.2× median and
  4.0× p90, so the wave estimator holds its low bound to that ceiling — twenty items across
  eight slots can be arithmetically fast, and it has never actually happened.
- Wall-clock includes waiting and carries no failure rate. These answer how long an agent
  will be busy, not how long until the work is accepted.

**`reckoning.html`.** One self-contained page, no build step and no external assets:
shipped features beside remaining ones, the waves between them with sub-tasks nested under
the item that cites them, and the caveats placed where a reader hits them. It renders from
`ledger.json` alone, which is what stops the presentable half drifting from the gated half.
`reckoning.md` keeps everything and grows the per-wave item tables, the dependency edges
with their provenance, and the tier behind each estimate.

**The gate covers the schedule too.** An item in two waves, an item in none, a scheduled id
that is not work in the ledger, a total that is not the sum of its waves, an inverted bound,
or a duration attached to corroboration all fail. A board that disagrees with its own rows
is this tool's failure mode arriving through its presentation layer.

A randomised audit over 500 trials caught one real defect before release: rounding a wave's
low bound down by half a minute produced a 4.03× schedule, fractionally faster than the
ceiling it had just been held to. Bounds now round away from optimism.
