# Changelog

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
