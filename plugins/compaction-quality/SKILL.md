---
name: compaction-quality
description: >
  Write a context-compaction summary that survives being the only thing the next session
  has, and score it against the transcript it replaced. Use this whenever someone is about
  to run /compact, asks what to keep before compacting, wants to hand a long session off to
  a fresh one, writes a handover or continuation note, or asks why a session "forgot"
  something after compaction. Also use it when someone asks how good their compaction
  summaries are, wants to measure or improve them, or is tuning when auto-compaction fires.
  Ships a deterministic scorer (scripts/score_retention.py) that measures retention against
  the real transcript, so "this summary is good" is a number rather than a feeling.
---

# Compaction quality

A compaction summary is the only artifact that survives. Everything else — the reasoning,
the files you read, the dead ends you already ruled out — is gone. So the summary is not a
recap for a human. It is the **input to a stranger who has to continue your work** and who
will confidently redo whatever you left out.

That framing decides every rule below.

## What actually gets lost — measured, not assumed

225 real compaction events, matched against the transcripts they replaced, exact string
match. Retention is the fraction of items present before compaction that appear verbatim in
the summary:

| class | median retention | median items per event |
|---|---:|---:|
| file paths | 2.9% | 477 |
| backtick identifiers | 17.2% | 924 |
| user messages | 11.1% | 58 |
| **user corrections** | **12.5%** | **5** |

Three of these four numbers are fine. Most of those 477 paths are transient reads and
tool-result noise; a summary that carried them all would be worse, not better. Low recall on
bulk is correct behaviour.

**The fourth is not.** Five corrections per session, and four get dropped. A correction is
the user saying *no, not like that* — and it is the single most expensive thing to lose,
because losing it means the next session confidently repeats the mistake the user already
paid to fix. It is also the cheapest thing to keep: five items.

So the target is not "retain more". It is **retain the load-bearing minority**, and spend the
budget you save on bulk to do it.

## The keep/drop decision

Ask one question per item: *if this is missing, does the next session do something wrong, or
merely something slower?*

**Wrong** is unrecoverable and must be kept:

- **Corrections and rejected approaches.** "Don't use X", "that's not what I meant", a
  reverted commit, an approach tried and abandoned. Keep the *reason*, not just the verdict —
  "rejected: adds a dependency" survives being paraphrased, "rejected" does not.
- **Constraints the user stated once.** Scope fences, "never touch that file", a chosen
  library, a naming convention. These never repeat in the transcript, so they have exactly
  one chance to survive.
- **Verbatim strings that cannot be re-derived.** Exact error text, IDs, hashes, ports,
  version pins, the precise wording of an acceptance criterion.
- **Where the work actually stands**, including what is broken. A summary that reads as
  finished when tests are failing is worse than no summary.
- **Corrections to your own earlier claims.** If you said something wrong mid-session and
  fixed it, the *fix* must survive. Otherwise the wrong version is what carries forward.

**Slower** is recoverable and should be dropped:

- File contents. They are on disk. A path plus what matters about it beats a paste.
- Tool output you can regenerate by running the tool again.
- Intermediate reasoning that reached a conclusion you are keeping. Keep the conclusion.
- Anything already written to a file, a spec, a commit message, or a todo list. Point at it.
- Exploration that found nothing — unless somebody might repeat it, in which case one line:
  "checked X, not there."

The asymmetry is deliberate. Re-reading a file costs seconds. Re-litigating a decision the
user already made costs their patience, and repeating a mistake they corrected costs their
trust.

## Preserve exactly, never paraphrase

Inside these, reproduce byte-for-byte. Paraphrasing them silently destroys their only value —
a path that is *nearly* right sends the next session to the wrong file, and an error string
that is *nearly* right does not match a search.

- Fenced and inline code
- File paths, commands, environment variables
- URLs, IDs, hashes, ports, version numbers
- Error text and log lines
- Identifiers: symbols, functions, types, flags, table and column names
- Direct user quotes carrying a constraint

Compress the prose *around* them freely. Fragments are fine. Drop articles, hedging, and
connective filler. The tokens you save here are what buys room for the corrections section.
(This is the caveman-compress rule set applied to a summary: compress the frame, never the
payload.)

## Structure

Claude Code's own `/compact` produces nine sections, and a summary landing in a Claude Code
session should match them — the next session's harness expects that shape, and matching it
costs nothing:

1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections
4. Errors and fixes
5. Problem Solving
6. All user messages
7. Pending Tasks
8. Current Work
9. Optional Next Step

Two additions worth making inside that shape, because the default summaries measurably drop
them:

- **Fold corrections into "Errors and fixes"** and mark them as user corrections rather than
  self-caught slips. The distinction matters: a user correction is a standing instruction, a
  self-caught slip is history.
- **Make "Current Work" state the failure mode if there is one.** "Tests green" and "tests
  failing on 2 auth cases" lead to completely different next actions.

Outside Claude Code — a handover note, a continuation prompt — use whatever shape fits, but
keep sections 1, 4, 7 and 8. Those four carry the unrecoverable material.

## Length

Observed median for `/compact` is ~18.4k characters, roughly 5k tokens. That is a reasonable
ceiling, not a target. A summary is too long when it contains material the next session could
regenerate; too short when a correction or constraint is missing. Length is an output, not a
goal — optimise the keep/drop call and the length follows.

If you are over budget, cut file contents and intermediate reasoning first. Never cut
corrections to fit.

## When to compact

Compaction breaks the prompt-cache prefix and pays a fresh write, so *when* matters
independently of *how well*.

| boundary | compact? | why |
|---|---|---|
| research → planning | yes | research bulk is spent, the plan is the distillate |
| planning → implementation | yes | plan is in a file or a todo list; free the context |
| after a failed approach | yes | clear the dead-end reasoning, keep the "don't do X" |
| debugging → next feature | yes | traces pollute unrelated work |
| implementation → testing | maybe | keep if tests reference recent code |
| mid-implementation | no | partial state and variable names are expensive to lose |

Measured on the same 225 events: auto-compaction fires at a median `preTokens` of **998,550**
— 99.9% of a 1M window. It has no idea where a task boundary is. Compacting deliberately at a
boundary above is strictly better than being compacted arbitrarily at the ceiling, which is
the whole argument for doing it by hand.

## Scoring a summary

Do not trust your own read of a summary you just wrote — you know what it means, which is
exactly the knowledge the next session lacks. Score it:

```bash
python3 scripts/score_retention.py --transcript <session.jsonl> --summary <summary.md>
```

It extracts paths, identifiers, user messages and corrections from the transcript and reports
retention per class, plus every correction it could not find. Exact string match, no model
judgment, so it is reproducible and free.

Read the output this way: **the correction list is the part that matters.** A dropped path is
a slower next session. A dropped correction is a wrong one. Bulk retention percentages are
context, not a score to maximise — pushing paths toward 100% would mean pasting the
transcript back in.

To measure the baseline on your own history:

```bash
python3 scripts/score_retention.py --scan-history
```

This finds real compaction events under `~/.claude/projects/` and reports retention across
all of them, which is where the table at the top of this skill came from.

## The honest limits

- Retention is measured by exact string match, so a correction faithfully *paraphrased*
  scores as lost. That makes the numbers a floor, not a verdict. The correction list is
  there so you can read the misses and judge.
- The scorer measures what was carried, not whether the summary is coherent, correctly
  ordered, or accurate about state. A summary can score well and still misdescribe where the
  work stands.
- The correction detector is a keyword heuristic ("actually", "no,", "instead", "don't"). It
  will miss politely-phrased corrections and flag some non-corrections. Treat its output as a
  candidate list to read, not a count to report.
