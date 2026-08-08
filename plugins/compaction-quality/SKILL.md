---
name: compaction-quality
description: >
  Write a context-compaction summary that survives being the only thing the next session
  has, and prove it against the transcript it replaced and against Claude Code's own
  /compact. Use this whenever someone is about to run /compact, asks what to keep before
  compacting, wants to hand a long session off to a fresh one, writes a handover or
  continuation note, or asks why a session "forgot" something after compaction. Also use it
  when someone asks how good their compaction summaries are, wants to measure or improve
  them, or is tuning when auto-compaction fires. Ships a deterministic scorer
  (scripts/score_retention.py) and a head-to-head benchmark against the built-in /compact
  (scripts/benchmark_vs_compact.py), so "this summary is good" is a number rather than a
  feeling.
---

# Compaction quality

A compaction summary is the only artifact that survives. Everything else — the reasoning,
the files you read, the dead ends you already ruled out — is gone. So the summary is not a
recap for a human. It is the **input to a stranger who has to continue your work** and who
will confidently redo whatever you left out.

Write it as **two tiers**, not one. That single structural decision carries most of the
value here, and the evidence for it is in `references/evidence.md`.

## The two tiers

**Tier 1 — pinned. Reproduced verbatim, never compressed, placed first.**

Four categories, and only these four. Keeping this tier short is as important as filling
it: instruction-following degrades as instruction count rises, so a bloated pinned tier
defeats itself.

1. **Standing constraints and prohibitions** — every "always", "never", "don't", scope
   fence and boundary the user or the project set. Quote them word for word.
2. **User corrections** — every time the user rejected, redirected or corrected you.
   Quoted, with what it supersedes.
3. **Rejected approaches and dead ends, each with its reason** — "tried X, failed because
   Y, don't retry unless Z".
4. **Exact identifiers** — absolute paths, commands, error strings, failing test names,
   IDs, ports, versions, flags. The tokens a successor cannot re-derive or guess.

**Tier 2 — narrative. Genuinely summarised.**

Task state, what was built and why, what remains. Ordinary summarisation competence
applies; the marginal return on effort here is low.

The split exists because the failure is not bad prose, it is a specific span being absent.
Measured: constraint-violation rates run at 0% when the governing constraint survives into
the summary and 38% when it is dropped. Presence very nearly determines compliance, so the
job is recall of a small set of must-survive items, not overall summary quality.

## What actually gets lost — measured on real events

`scripts/benchmark_vs_compact.py` scores the built-in `/compact` against the transcripts it
replaced, using the summaries already on disk. Across **121 real compaction events**:

| class | retention by the built-in `/compact` | events |
|---|---:|---:|
| user corrections | 63.1% | 34 |
| standing constraints | 33.8% | 74 |
| **rejected approaches** | **0.3%** | 68 |
| identifiers | 48.6% | 120 |
| file paths | 16.4% | 119 |

Read the last row first: low recall on bulk is **correct**. Most paths are transient reads
and tool noise, and a summary carrying them all would be worse.

Read the bold row second. **Negative knowledge does not survive compaction at all.** Two
thirds of standing constraints go too. Those are the rows that make the next session repeat
work the user already paid for, and they are cheap to keep — a handful of items each.

## The keep/drop decision

One question per item: *if this is missing, does the next session do something **wrong**, or
merely something **slower**?*

**Wrong** is unrecoverable. It goes in Tier 1, verbatim:

- Corrections and rejected approaches, with the *reason* — "rejected: adds a dependency"
  survives paraphrase, "rejected" does not.
- Constraints stated once. They never repeat in the transcript, so they have exactly one
  chance to survive.
- Verbatim strings that cannot be re-derived: error text, IDs, hashes, ports, version pins,
  the precise wording of an acceptance criterion.
- Where the work actually stands, including what is broken. A summary that reads as
  finished when tests are failing is worse than no summary.
- Corrections to your own earlier claims. If you said something wrong and fixed it, the
  *fix* must survive, or the wrong version carries forward.

**Slower** is recoverable. Drop it:

- File contents. They are on disk; a path plus what matters about it beats a paste.
- Tool output you can regenerate.
- Intermediate reasoning that reached a conclusion you are keeping. Keep the conclusion.
- Anything already in a file, spec, commit message or todo list. Point at it.
- Exploration that found nothing — unless somebody might repeat it, in which case one line.

The asymmetry is deliberate. Re-reading a file costs seconds. Repeating a mistake the user
corrected costs their trust.

## Preserve exactly, never paraphrase

Inside Tier 1, reproduce byte for byte. Paraphrase destroys the only value these have: a
path that is *nearly* right sends the next session to the wrong file, and an error string
that is *nearly* right does not match a search.

The failure is subtler than dropping things. A constraint of "use type hints everywhere"
was compacted to "the user prefers a consistent code style with type hints" — the absolute
quantifier silently deleted, the requirement changed. Scope boundaries mutate the same way:
"remove the calls in `a.py`, leave `b.py` untouched" became a global removal instruction.

Compress the prose *around* the quotes freely. Fragments are fine; drop articles, hedging
and connective filler. The tokens you save are what buys room for Tier 1.

## Order of work: extract, then compress, then verify

1. **Extract first.** Walk the transcript for Tier 1 items and quote them before writing any
   prose. Extraction before generation measurably improves faithfulness, and doing it second
   means the narrative has already decided what mattered.
2. **Then compress** Tier 2 into the remaining budget.
3. **Then verify against the transcript** — not against your summary. Re-read the source
   asking "did every correction, constraint and dead end reach Tier 1?" That is a retrieval
   check with external evidence. Re-reading only your own summary is intrinsic
   self-correction, which does not reliably improve output and sometimes degrades it.

## Structure

Claude Code's `/compact` produces nine sections, and a summary landing in a Claude Code
session should match them — the harness expects that shape and matching it costs nothing:

1. Primary Request and Intent · 2. Key Technical Concepts · 3. Files and Code Sections ·
4. Errors and fixes · 5. Problem Solving · 6. All user messages · 7. Pending Tasks ·
8. Current Work · 9. Optional Next Step

Put **Tier 1 first, before section 1**, as an explicit pinned block. Do not scatter it
through the nine sections: the whole point is that these items are exempt from summarisation
rather than well-summarised, and burying a constraint inside "Errors and fixes" invites the
paraphrase that kills it.

Two additions inside the standard shape:

- **Mark user corrections as standing instructions**, not as history. A correction is a
  rule that still binds; a self-caught slip is past tense.
- **Make "Current Work" state the failure mode.** "Tests green" and "tests failing on 2 auth
  cases" lead to completely different next actions.

Outside Claude Code, use whatever shape fits, but keep the pinned tier and sections 1, 4, 7
and 8.

## Length

Observed median for `/compact` is about 20.6k characters. That is a ceiling, not a target. A
summary is too long when it contains material the next session could regenerate, too short
when a correction or constraint is missing. If you are over budget, cut file contents and
intermediate reasoning first. **Never cut Tier 1 to fit.**

## When to compact — and when to do something else

Compaction is the lossiest tool available, not the default one. Measured against other
context-management strategies it is the weakest: roughly +2.6 to +2.7 points on task
success, and *negative* for one frontier model, where moving work into tool calls bought
+9.4 to +13.3. Simply masking old tool outputs matched summarisation's solve rate at about
half the cost.

So before compacting, ask whether the cheaper thing works: clear old tool results, offload
state to a file, or start a fresh session pointed at a progress file.

When you do compact, the boundary matters:

| boundary | compact? | why |
|---|---|---|
| research → planning | yes | research bulk is spent; the plan is the distillate |
| planning → implementation | yes | the plan is in a file; free the context |
| after a failed approach | yes | clear the dead-end reasoning, keep the "don't do X" |
| debugging → next feature | yes | traces pollute unrelated work |
| implementation → testing | maybe | keep if tests reference recent code |
| mid-implementation | no | partial state and variable names are expensive to lose |

Auto-compaction fires at a median of 998,550 `preTokens` — 99.9% of a 1M window — with no
idea where a task boundary is. Compacting deliberately at a boundary beats being compacted
arbitrarily at the ceiling, which is the whole argument for doing it by hand.

## The escape hatch: write it down instead

For anything in Tier 1 that must survive *several* compactions, do not trust the summary
channel at all. Write it to a durable file the next session reads — `CLAUDE.md`, a progress
file, a decisions log — and have the summary point at it. Compaction is a lossy channel by
construction, and routing the load-bearing minority around it is more reliable than
compressing it well.

## Scoring

Do not trust your own read of a summary you just wrote — you know what it means, which is
exactly the knowledge the next session lacks.

```bash
python3 scripts/score_retention.py --transcript <session.jsonl> --summary <summary.md>
python3 scripts/score_retention.py --scan-history          # baseline across your history
python3 scripts/benchmark_vs_compact.py --arms cli         # score the built-in, free
python3 scripts/benchmark_vs_compact.py --arms cli,skill -n 8   # head-to-head
```

The correction and rejected-approach lists are the part that matters. A dropped path is a
slower next session; a dropped correction is a wrong one. Bulk percentages are context, not
a score to maximise — pushing paths toward 100% would mean pasting the transcript back in.

**Two confounds the benchmark reports beside every score, because they will otherwise decide
the result:** summary length, and extractiveness. A summary that "wins" by copying more has
not won, and judges reward copied text regardless of whether it helped.

## The honest limits

- Retention is exact string match, so a faithfully *paraphrased* correction scores as lost.
  The numbers are a floor, and the miss list is there so you can read them and judge.
- The scorer measures what was carried, not whether the summary is coherent or accurate
  about state. A summary can score well and still misdescribe where the work stands.
- The correction and rejection detectors are keyword heuristics. They miss politely-phrased
  corrections and flag some non-corrections; treat the output as a candidate list to read,
  not a count to report.
- The head-to-head is paired on identical transcripts, but n is small. Report the effect and
  the sample, never a bare percentage.
- Evidence, with citations and the numbers' provenance: `references/evidence.md`.
