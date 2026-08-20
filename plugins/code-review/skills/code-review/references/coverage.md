# Coverage — what ran, what did not, and how you can tell

A review that lists three findings and stops has told the reader nothing about the checks that
never executed. A pass and a cannot-run serialize identically, so silence reads as a clean bill.
This file defines the four states every check reports and the ledger the report prints.

The measured shape of the problem, from the campaign this rule comes from: 230 cases closed,
220 of 220 armed, 10 marked not-applicable with structural reasons, zero failures — and zero cases
at a rung that asked for an effect outside the process, because no such rung existed. Every gate
was green and the central claim had never been tested. The same census found 26 of 32
state-changing test functions never re-read the observable afterwards, and a sweep of 7 mutating
operations found 3 that returned success while changing nothing.

The corollary for this skill: **an angle you did not run, a checklist you did not load, a file you
did not read, and a shard that came back empty are all coverage holes, and the report names them.**

## The four states

Every angle, every loaded checklist section, and every gate resolves to exactly one.

| State | Means | Requires |
|---|---|---|
| `checked` | The check ran against the material it applies to. | Name what you read — the files, the greps, the command. |
| `not-applicable` | The check ran far enough to establish it does not apply here. | A structural reason: no file of that kind in the diff, the lens excluded it, no instruction file governs these paths. |
| `not-checked` | The check did not run. | The reason: a file not read, a tool unavailable, a shard that returned nothing, a depth budget that excluded the angle, an area filter. |
| `no-oracle` | The check ran and nothing available could decide it. | What evidence would decide it. A missing index a query implies, a production env value, an upstream vendor limit — these want an oracle built, not a better instrument. |

`not-checked` and `no-oracle` are terminal states that route to the reader, not retry conditions.
Re-running a check whose instrument is absent produces the same absence at twice the cost.

Distinguish the last two carefully, because they ask for different work. A `not-checked` wants the
run repeating with the missing input. A `no-oracle` wants somebody to decide what the right answer
would even look like.

## What the report prints

After the findings and before the verdict line, print the ledger. Include every row that is not
`checked`; suppress the `checked` rows, which are the expected case, and state their count.

```
## Not checked

- Angle G (partial failure and ordering) — not-checked: depth `standard` does not run it.
- security-checklist A05 (headers, CSP) — not-checked: `next.config.ts` is outside the area filter `mobile`.
- Shard `catalogue` (14 files) — not-checked: returned no candidates on two dispatches; those files were not reviewed.
- quality-lenses `perf` N+1 sweep — no-oracle: the query implies an index on `products.source`; no schema file in the diff declares one either way.
- 3 of 19 changed files not read in full (quick depth reads risk-bearing hunks only): lib/format.ts, lib/copy.ts, app/legal/page.tsx.

Checked: 9 angles, 4 checklists, 2 gates.
```

When every row is `checked`, print `Not checked: nothing — every selected angle, checklist and gate
ran.` A ledger that is absent and a ledger that is empty are the same ambiguity this file exists to
remove, so print the line either way.

## Degradation reporting

**When the `Agent` tool is unavailable**, do not error and do not skip angles. Run every angle and
every verification yourself, sequentially, in this context. Then say plainly in the report that
this was a single-pass review without the multi-agent fan-out, so nobody reads it as the full
pipeline. Put it in the budget line as well as the ledger:

```
standard → Agent tool unavailable → 8 inline angles → inline verify → ≤12 findings
```

The same applies to any depth setting the user asked for that the session could not deliver. State
what ran, not what was requested.

## A tool's success return is not evidence the effect happened

A shard replying `Shard catalogue: 14 candidates written to <path>` is a claim. Check the file.
This is not hypothetical for this skill: `Write` has overwrite semantics, and N parallel shards
writing one file means the last writer wins while every other shard reports success — 5 of 8
shards' output vanished this way in a live review.

The general shape recurs everywhere. A connection pool that crept one over its limit returned an
empty tool list with `200 OK`, and every client cached the empty list permanently: a successful
response, a valid payload, a total outage. An agent asked to download twenty files downloaded
three, hallucinated the rest, and reported success.

So, after any step whose effect you will depend on:

```bash
wc -l .code-review/<run-id>/candidates-*.jsonl
for f in .code-review/<run-id>/candidates-*.jsonl; do jq -c . "$f" > /dev/null || echo "Malformed JSON in $f"; done
```

Assert the observable, not the return code. The rule generalises into Gate 6 in
`verification-loop.md`: a finding claiming runtime behaviour names a command that was actually run,
with its output.

## Reconciling a fan-out

**Compare shards dispatched against shard files that exist and parse.** A harness that loses an
agent to a rate limit, a usage limit, a dropped connection or a 5xx returns `null` for that agent
with zero retries, filters the `null` out, and reports the wave `completed` — the failure count
sits in the result next to a status that says everything finished. Measured on one machine across
three runs: 96 agents started and 35 never returned; 128 and 50; 107 and 52.

The procedure:

1. Record the bucket list and the file each shard owns before dispatching.
2. After the wave returns, list the files that exist and parse. Compare against the bucket list.
3. Re-dispatch a missing or unparseable shard **once**. The usual cause is an agent that returned
   JSONL inline instead of calling `Write`; re-dispatch with that reminder.
4. If it comes back empty a second time, its files are `not-checked`. Name the shard, the file
   count, and the reason in the ledger. Do not absorb the gap into a clean report, and do not
   re-review its files yourself unless the user asks — an orchestrator that quietly picks up a
   failed shard's work has spent the fan-out budget twice.

A wave exiting without error is not a wave that did its work.

## Claiming coverage of the changed files

At `quick` depth you read only files with risk-bearing hunks. That is the depth's design, and it
becomes a lie the moment the report implies the rest were reviewed. Record the read set and the
skipped set, and print the skipped count in the ledger.

The same discipline applies to a grep-based claim. "No other caller of this symbol" rests on the
grep you ran; state the pattern and the scope. Absence from what you searched is *not found in
what I searched*, never *not present*.
