# Estimation — where the numbers come from, and what they are not

Every duration this skill prints is a **wall-clock range for one agent unit**, derived
from a measured corpus of past runs on this machine. It is not a promise, and the report
says so in the same breath as the figure.

## The corpus

Measured 30 August 2026 by parsing `~/.claude/projects/**/subagents/agent-*.jsonl` — the
transcripts Claude Code writes for every subagent it spawns. A **unit** is one sidechain
tree: the root brief plus every message descending from it, timed from its first record
to its last.

| | |
|---|---:|
| Subagent transcript files parsed | 2,230 |
| Units extracted | 2,572 |
| Units on Opus 4.8 or Opus 5 | 1,868 |
| **In the analysis band** (0.05–600 min) | **1,842** |
| Distinct parent sessions | 88 |
| Distinct projects | 31 |
| Date range | 14 Jul – 30 Aug 2026 |

Model mix in band: `claude-opus-5` 1,550 · `claude-opus-5[1m]` 124 · `claude-opus-4-8` 168.

Twenty-five units under 3 seconds were dropped (a spawn that returned immediately measures
the harness, not the work) and one over 10 hours was dropped as stalled rather than slow.
Both exclusions are small enough not to move a percentile, and both are named here rather
than folded in silently.

**Opus 5 and Opus 4.8 are pooled, and the measurement supports it.** Within the same size
band (30–80 tool calls) the medians are 10.5 min and 11.2 min respectively — a difference
smaller than the spread inside either. A separate table per model would imply a precision
the data does not carry. The 1M-context variant runs slightly longer (14.2 min median in
that band), which is noted and not modelled.

## What actually predicts duration

Stage label predicts loosely; **volume of work predicts well.** Both tables are below
because a brief carries the stage before it carries anything else, and the volume signal
only becomes readable once someone has sketched the work.

### By stage

| Stage | n | p25 | median | p75 | p90 |
|---|---:|---:|---:|---:|---:|
| build | 511 | 13.4 | **27.3** | 48.1 | 93.7 |
| research | 512 | 2.4 | **5.6** | 10.9 | 17.1 |
| verify | 109 | 2.6 | **6.0** | 12.2 | 24.3 |
| design | 27 | 6.3 | **9.8** | 26.0 | 104.6 |
| triage | 13 | 10.1 | **12.2** | 25.5 | 28.7 |
| review | 22 | 1.2 | **3.1** | 4.9 | 11.4 |

All figures in minutes. `design`, `triage` and `review` have thin samples (13–27 units) and
the report marks them as such rather than printing them at the same weight as `build`.

### By edit volume — the best single predictor

Across all 1,842 units, counting `Edit` + `Write` calls:

| Files touched | n | median | p75 | p90 |
|---|---:|---:|---:|---:|
| none (read-only) | 1,093 | 3.0 | 8.3 | 17.2 |
| 1–4 | 249 | 7.9 | 14.5 | 26.8 |
| 5–14 | 227 | 19.2 | 34.3 | 63.6 |
| 15–39 | 210 | 32.0 | 48.1 | 87.2 |
| 40+ | 63 | 63.7 | 105.4 | 140.7 |

Within `build` units specifically the same signal is cleaner still — 3–7 edits runs a 14.5
median, 20–49 edits runs 41.3, 50+ runs 63.9.

## The tiers this skill prints

Four tiers, each a p25–p90 range with the median called out. The range is wide on purpose:
measured `p90/median` is 3.4 for build work and 3.1 for research, so a ±20% band would be
a fiction. **Print the range, lead with the median, and never print a single number.**

| Tier | Shape | Range (p25–p90) | Median |
|---|---|---|---|
| `S` | read-only, or 1–2 files — a check, a small fix | 3–25 min | 8 min |
| `M` | 3–7 files, one subsystem | 7–56 min | 15 min |
| `L` | 8–19 files, or crosses a seam | 14–68 min | 25 min |
| `XL` | 20+ files, or a new surface end to end | 25–155 min | 45 min |

Evidence work — unblocking a state, building a hook, wiring an oracle — sits at `S`/`M`:
the research+verify pool (n=621) runs a 5.6 min median, p90 17.7. A blocker cluster is
sized by the hook it needs, not by the cases it returns.

## Wave arithmetic

Measured across 253 multi-member overlapping clusters in the same corpus:

- **A wave costs its slowest member, plus a little.** Median wall-clock ÷ slowest member is
  **1.05**; p75 is 1.40, p90 1.78. So `wave ≈ max(member) × 1.1` is a good central estimate
  and `× 1.8` is the pessimistic one.
- **Observed speedup is 2.2× median** (sum of member durations ÷ wall-clock), p75 2.9×,
  p90 4.0× — well short of the member count, because members rarely start together and the
  merge is serialized.
- **Peak concurrency actually reached: median 5, p75 7, p90 10, max 16.** A plan assuming
  more parallelism than this has not been observed to happen.
- **Waves of 9+ members lose the property**: their wall ÷ slowest rises to 1.55. Past about
  8 concurrent runners the wave stops costing its slowest member and starts costing more.

So the wave estimate is:

```
wave_low  = max(member_low)  × 1.05
wave_high = max(member_high) × 1.8      # ×2.2 for waves of 9+
```

Sum the waves for the project total, and label it a **schedule estimate under the stated
concurrency**, not a duration.

## What these numbers are not

**They are wall-clock, and wall-clock includes waiting.** A unit that sat behind a rate
limit measures longer than the same work would today. This inflates the upper percentiles
in a way that is honest for planning ("this is how long it took") and wrong for costing
("this is how much model time it consumed"). The report says wall-clock every time.

**They are this machine's history, not a benchmark.** 31 projects, one operator, one
hardware profile, and a fleet convention that serializes merges. A repo with a slower test
suite or a different concurrency cap will differ, and no correction factor is offered
because none was measured.

**They do not carry a failure rate.** A unit that ran 40 minutes and produced work that was
later rejected is counted the same as one that landed. The estimate answers "how long will
an agent be busy", not "how long until this is done and accepted".

**They cannot be recomputed from the ledger.** These are the only figures in the whole
pipeline not derived from `ledger.json`, which is why they live in this file with their
provenance attached, and why every rendered estimate is marked as an estimate.

## Re-measuring

The scan is worth re-running when the corpus has grown materially or a new model lands. It
reads `~/.claude/projects/**/subagents/agent-*.jsonl`, groups each file's records into
sidechain trees by `parentUuid`, and takes `max(timestamp) - min(timestamp)` per tree.
Classify the stage from the root brief's text and the tool mix; size from `Edit` + `Write`
counts. Update the tables above with the new `n`, and update the corpus block, in the same
edit — a table whose provenance line no longer matches it is worse than no table.
