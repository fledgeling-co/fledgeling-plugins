# Sizing the remaining work from measured rates

Use this file when a campaign has to say how long the rest will take. The schema is
`schemas/remaining-work.schema.json`, which requires each row to name its count, its unit,
the measured rate applied, and the evidence for applying that rate.

All figures below come from one campaign's own throughput on 2026-09-02 — **140 agents
across 12 lanes, 1,311 units of work.** They are a starting point for a project that has
not measured its own rates yet, and they are superseded the moment it has.

## 1 · What a duration figure is, and what it is not

**A duration here is wall-clock for one lane** — one batch of agents working one shape of
work, start to return. It is not a per-item cost and it is not a sum.

**It is a range, never a point.** A single number invites a schedule; the spread between
the ends is the honest content.

**It carries no failure rate.** Of the 12 lanes measured, **4 lost an agent**; all four
recovered by resuming from cache or by splitting the work. A lane that ran 36 minutes and
produced work later rejected counts the same in these figures as one that landed. So a
plan built by summing them assumes lanes run serially and that no lane loses an agent, and
both were false in the campaign that produced them.

## 2 · The three shapes of work

| shape | units per agent | wall minutes per lane | basis |
|---|---|---|---|
| **read-and-rule** — triage, binding, recording a reason | 8.2 median | 8 – 25 | median of 6 lanes |
| **write-a-body** — authoring a case, converting a guard | 1.0 – 4.1 | 10 – 36 | 4 lanes |
| **run-and-promote** — running a suite and promoting what passes | not agent-limited | 10 – 36 | tier-limited, not agent-limited; the range is inherited from write-a-body rather than separately measured, and is marked as such |

Worked instances behind those rows:

- binding: 146 flows by 19 agents in 8 minutes;
- guard conversion: 2.8 – 3.9 units per agent;
- body authoring: 14 bodies by 14 agents across 2 batches;
- ruling on inert cases: 82 reasons by 10 agents in 7 minutes;
- run-and-promote: 6 lanes moved the never-run count 293 → 188, 105 flows, across 3 machines.

**Run-and-promote is gated by how many isolated environments exist, not by how many agents
you start.** That campaign declared 4 environment tiers and could use 3, and the missing
tier blocked a third of run throughput all session.

## 3 · Serial and parallel totals are different numbers, and both get published

Eight remaining pieces summed to **5.6 – 32.2 h** run one after another and **2.0 – 9.6 h**
run in parallel, where the widest row governs because it waits on machines rather than on
people.

State what a total excludes. That one excluded review and release, and gave no worker time
to the two items waiting on a person's decision, because waiting is not work — an estimate
that quietly prices a decision as zero reads as a commitment to decide it.

## 4 · Concurrency — two measurements that appear to conflict and do not

**Five slots, from a correctness failure.** On 2026-08-26, running a fleet wider than five
slots killed **92 agents, 88 of them at exactly 180.0 seconds**, each leaving a four-line
transcript with no assistant message and no error row in any counter. Going wider did not
slow the wave down; it lost work invisibly. A wave of eight that loses three is slower than
a wave of five that loses none *and looks identical in every counter*.

**Nineteen lightweight agents held with zero deaths** a week later, on read-and-rule work.
The five-slot rule was wrong by nearly four times for that shape of work.

Both are true, so carry both: **the width a machine and a harness will hold is a
measurement, not a constant.** Ramp deliberately and probe. The honest probe is the
180-second one and it costs four minutes.

**What actually kills a lane is unbounded work, not brief length.** Prompts of 2,400–3,500
characters died at roughly 128 tool uses and 176k tokens. One lane died twice as a single
agent over six files; split one file per lane and six of six returned with no deaths. So
cap iterations in the brief, ask for incremental reporting, and prefer one browser
invocation over many.

## 5 · Reading the counters honestly

**Derive failure from `started − results`, never from an error field.** Deaths of this kind
write no error row.

**Assert that a fan-out actually fanned out.** After a wave, compute
`sum(agent durations) ÷ wall clock`. Under 1.2 the wave ran serially, and that is a defect
to report rather than a result to publish. It costs two timestamps.

**A concurrency verdict counts only runs in this session's window,** and liveness is not a
journal file's mtime. A liveness filter that enumerates today's wave names goes stale
within a day; one widened to any loose id string matched 26 worktrees belonging to other
sessions.

**Do not resume a workflow whose results count is far below its started count** — replay is
a sticky prefix, and resuming with `results=0` re-runs everything.

**Two ways a run becomes invisible.** Backgrounding a process inside a tool call detaches it
from the harness: no task exists, so no completion notification ever fires and the run is
absent from the task list — the owner's report of this was *"i dont see any runs going"*. And
a tool timeout shorter than the command turns a slow success into a reported failure; one
environment recycle was recorded as ineffective for a whole session on that basis and had in
fact worked.

## 6 · Blockers are sized separately, with an owner

A blocker gets its lifting condition and its owner, and the owner is what stops it being
filed as engineering work nobody can start. The four in that campaign: an environment tier
wedged on a compile (owner: harness), a standalone database process that cannot open
transactions so 11 spec files are unwritable, a mock outbound sink present in the repo and
wired into no seed tier, and a queue with no product writer at all.

Two of those four are product gaps and two are harness faults, and they schedule
differently. `schemas/remaining-work.schema.json` keeps `blocked` separate from the sized
rows for that reason.
