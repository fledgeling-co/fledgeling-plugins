# A paired case: three summaries of one session

Everything in `SKILL.md` that says "measured on a paired case" points here. This is one
session, so it is an existence proof and a source of failure modes, not a rate. What makes
it worth writing down is that all three summaries come from the **same transcript**, and two
of them cover the **same window minutes apart** — which is the comparison the 121-event
baseline scan cannot make.

Source: a 4,563-row `~/Dev` orchestration session (`hopper`, a multi-runner fleet build).
The transcript stays on the authoring machine; nothing here reproduces its content beyond
short structural fragments, because it carries live project material.

## The three arms

| arm | what it is | row | chars | pinned block |
|---|---|---:|---:|---|
| **A** | Claude Code's built-in `/compact`, untouched | 3027 | 17,957 | none — straight to section 1 |
| **B** | this skill, invoked in-session as `/compaction-quality` | 4506 | 9,388 | 5,163 chars, 55% of the summary |
| **C** | the one-paragraph wire addendum (`references/compact-addendum.md`) spliced into a real compaction | 4518 | 19,377 | 5,262 chars, 27% of the summary |

A replaced rows 0–3026. **B and C both cover rows 3028–4505**, eleven minutes apart, and C
had B's finished pinned block sitting in its own context when it ran. So B→C is paired and
C's exposure is a superset of B's: anything C missed, it missed with the answer in front of
it.

Confounds, by the benchmark's own estimator so they compare to the 0.09 mean in
`evidence.md`: extractiveness A 0.285, C 0.071, B 0.027. C is 2.06× B's length. The longer,
more extractive summary is **not** the one that carried more, which is the whole reason both
confounds print beside every score.

## What the built-in dropped — the 0.3% reproducing in vivo

A has no pinned block and carries essentially no negative knowledge. Of the fifteen
distinctive rejected-approach and dead-end markers traceable in the transcript, A contains
**one**, as a subordinate clause inside *Pending Tasks* ("add a *named* reprocess
transition, never a general edge"). That is exactly the burial `SKILL.md § Structure` warns
about: the item technically survived and is positioned where a successor reading for "what
should I do next" will read past it.

## The finding: two summaries, near-disjoint pinned blocks

B and C each pinned seven or eight rejected approaches, each with its reason, each phrased so
a fresh session would not retry it. **Almost none of them are the same items.**

| | B (skill) | C (addendum) |
|---|---|---|
| adding a job program that the drain completes as stale | pinned | absent |
| the Safari extension converter that emits its own container app | pinned | absent |
| browser impersonation copied from a sibling repo | pinned | absent |
| a headless rung that returns the identical shell a plain fetch returns | pinned | absent |
| `Boolean(...)` for a default that must be `??` | pinned | absent |
| refresh-token families for the extension | pinned | absent |
| routing a model call directly, reversing merged hardening | pinned | absent |
| passing a prompt to `codex exec` on stdin | pinned | absent |
| `git log --grep=<id>` as a merge check | absent | pinned |
| blind keep-both-sides conflict resolution | absent | pinned |
| backticks in an inline `git commit -m` | absent | pinned |
| editor diagnostics as evidence of build state | self-correction | pinned |
| counting ledger states by enumerating the non-merged ones | absent | pinned |

Every one of B's eight is grounded in rows 3028–4505 — **inside C's context**. C did not
fail to retrieve them; it rebuilt its pinned block from the transcript and selected the
recent stretch, where the method errors it had just committed lived. The older
product-and-architecture decisions were further back, and went.

This is the failure mode worth naming, because "reproduce every rejected approach" does not
tell a model *where to look*, and a sweep that starts from recency finds the last two hours.

### The two kinds of negative knowledge

The split above is not random. It is a clean taxonomy:

- **Method dead ends** — how to work. Wrong verification command, a shell quoting trap, a
  tool invoked the wrong way. C got all of these and none of the others.
- **Product dead ends** — what to build. A rejected architecture, a library that does not
  fit, a coercion that corrupts stored data. B got all of these and none of the others.

Neither arm got both, on a window that contained both. A sweep prompted for "rejected
approaches" as one undifferentiated class returns whichever kind is nearer to hand.

## Where B's advantage came from, and what it cost

B opened by consolidating the method notes into a durable file and said so, naming the
file and the section — the escape hatch in `SKILL.md`, used deliberately. That is why B
could drop the method dead ends safely: they were written down, and the summary pointed at
where. The pointer checks out; the named section contains them.

The product dead ends had **no durable home** — scattered across `docs/` with no pointer —
so B pinned those verbatim. Pin-or-point, decided per item, is what produced the denser
block.

**B's cost:** its *Current Work* says "Wave 1 complete… Nothing is failing", and omits the
unfinished deliverable of the turn that was in progress. C names it ("Not yet done: the §7
close…"). B is accurate about the tree and wrong about the obligation, and a successor
reading B starts new work with a half-finished one behind it. `SKILL.md`'s rule was "state
the failure mode"; a clean tree with an open obligation is a failure mode it did not cover.

**C's cost, beyond the eight items:** its extra 10,000 characters are largely the material
the keep/drop rule already says to drop — a pasted nine-line source comment, a four-line
code fragment, a ledger row format, gate shell commands. C is twice B's length and its
pinned block is the same size. Length went to the regenerable half.

## What this says about the instrument

Scored with exact string match — what the 121-event baseline uses — the benchmark's
`rejected approaches` class reports **0.0% for both B and C** across 49 detected spans, and
`CORRECTIONS` reports `n/a (0 of 0)`. Both numbers are wrong about what happened: B and C
each carried seven or eight rejections with reasons, and both pinned the same consequential
correction.

Three instrument faults, all now fixed in `scripts/score_retention.py`:

1. **Exact match cannot see a faithful restatement.** A pinned rejection is legitimately
   reworded while keeping the reason. `retention(..., soft=True)` scores distinctive-token
   overlap for the semantic classes; exact stays for paths, ids and error strings, where
   nearly-right is worthless.
2. **Corrections were read only from `type == "user"` rows.** The one correction both
   summaries chose to pin came from a peer runner correcting the parent's false claim.
   `PEER_CORRECTION_RE` now reads non-user rows under tighter wording.
3. **User messages keyed on their first 60 characters.** Twenty-six turns collapsed onto
   four keys — five identical cron-heartbeat prefixes, the rest command wrappers. The one
   instruction C quotes verbatim keyed as
   `<command-message>goal-harness:goal-harness</command-message>` and scored as dropped by
   both. `user_key()` strips the furniture and keys on the longest interior line.

After the fixes, the same window scores user messages 35.7% (B) against 50.0% (C), corrections
1 of 1 for both, and rejected approaches 34.7% (B) against 65.3% (C) — all previously 0.0% or
`n/a`. The instrument now moves.

### But the percentages still do not settle B against C, and here is why

Read that last pair against the hand audit above: the soft matcher ranks **C nearly twice as
high on rejected approaches**, while reading the two blocks finds near-disjoint sets of
comparable size, C missing eight items that were in its own context.

Both are true, and the reason is a third instrument property that no fix removes:

**The detector samples its spans from the transcript, so a long window's span population is
dominated by its recent, denser portion — and any recall percentage over that population
rewards exactly the recency bias this case exists to document.** C pinned the recent items;
the spans are mostly recent; C scores higher. The 49 spans are also noisy in the ordinary
way of keyword heuristics: the sample includes a command wrapper, a numbered file listing and
a section header, none of which is a rejected approach.

So the ordering of the two instruments is:

1. **`--against`, and read the disjoint sets.** What one kept and the other dropped is
   concrete, checkable against the transcript, and immune to how the spans were sampled.
2. **Soft recall,** to confirm a class is not being dropped wholesale. Useful as a floor
   check, unreliable as a ranking between arms on a long window.
3. **Exact recall,** for paths, ids and error strings only.

A percentage over auto-detected spans answers "did this class survive at all". It does not
answer "which summary is better", and on this pair it points the wrong way.

**The consequence for the headline number.** `evidence.md`'s 0.3% rejected-approach
retention was measured with the exact matcher, and this case shows that matcher scoring a
*full* pinned block at 0.0%. So 0.3% is a floor on the built-in that no arm could beat as
measured — it distinguishes nothing. The claim it supports is the one A independently
demonstrates here: the built-in prompt carries almost no negative knowledge. The claim it
cannot support is any comparison between arms.

## Reproducing it

```bash
python3 scripts/score_retention.py \
  --transcript <window.jsonl> --summary <a.md> --against <b.md>
```

Compare mode prints per-class recall for both and then, per class, the spans each summary
kept that the other dropped. Two summaries scoring alike on every percentage while pinning
almost non-overlapping material is a real outcome, and no per-summary score shows it.
