# Does braindump actually work? A benchmark ran, the eval prompts did not

**The measurement layer was run and its output is committed. The thirteen eval
prompts were not run at all.** Those are two different things and this file keeps
them apart, because braindump's numbers are unusually well documented and the eval
set behind them has never produced a graded result.

What was measured: a **head-to-head against the built-in `/compact`** across six real
transcripts and three arms, plus a **40-event replication** of the baseline scan. Both
are on disk as machine-readable JSON with a run log, and both were reproduced from
those files on 2026-08-18 while this was written.

What was not: `evals/evals.json` holds **13 prompts and 67 assertions**, every one of
them checkable by exact string match or by running the skill's own scorer. There is no
`grading.json`, no results directory and no run output anywhere for them.

And the most useful thing here is a finding against the skill's own headline: **the
matcher the published numbers were measured with cannot see the thing the skill
does.** That gets its own section.

## Where the evidence is

| What | Where | State |
|---|---|---|
| The baseline replication | `docs/benchmark-cli-baseline.json` | **Run**, 40 events, one arm |
| The head-to-head | `docs/benchmark-head-to-head.json` | **Run**, 6 transcripts, 3 arms |
| The run log | `docs/benchmark-run.log` | **Run**, 45 lines, per-transcript and paired |
| The 121-event scan | `references/evidence.md` only | Reported. The raw output is **not committed** |
| The paired case study | `references/case-study-paired.md` | **Run**, one real session, three summaries, hand-audited |
| The research corpus | `docs/deep-research/` | Four reports, all with source lists |
| The eval prompts | `evals/evals.json` | **Never run.** 13 prompts, 67 assertions, no grading |

## The baseline: what the built-in prompt actually drops

The comparison arm here costs nothing, which is the cleverest thing about this skill's
harness. Every real `/compact` event under `~/.claude/projects` is a summary the tool
already wrote for a transcript that already happened, so the baseline is sitting on
disk before anyone runs anything.

`references/evidence.md` reports a 121-event scan, and the README's headline table
comes from it. **The 121-event run's raw output is not committed**, so a later reader
cannot check it. What is committed is the 40-event replication, and it reproduces
exactly. Recomputed from `docs/benchmark-cli-baseline.json` on 2026-08-18:

| Class | Retention | Events with at least one span | Matches `evidence.md` |
|---|---:|---:|---|
| identifiers | 68.2% | 39 | yes |
| constraints | 50.0% | 28 | yes |
| user corrections | 41.7% | 4 | yes |
| file paths | 23.7% | 38 | yes |
| **rejected approaches** | **0.0%** | 11 | yes |
| median summary length | 22,214 chars | 40 | yes |
| mean extractiveness | 0.078 | 40 | yes, reported as 0.08 |

`evidence.md` then does the thing most evidence files do not, and separates the robust
finding from the noisy ones: against the 121-event figures, the rejected-approach
result replicates, length and extractiveness are stable, and identifiers, file paths,
constraints and corrections all swing by 10 to 20 points between samples. Its own
conclusion is that every retention figure except the zero is a per-sample observation
that must be quoted with its n, and that citing 33.8% as *the* constraint-retention
rate overstates what 74 instances can support.

The README follows that discipline in one direction and not the other. Its badge reads
"rejected approaches retained: 0.3%", which is the claim `evidence.md` says is safe.
Its headline table then prints the four swinging figures without their n counts, where
the reference file prints them with.

## The head-to-head: three arms, six transcripts, and an honest null

From `docs/benchmark-run.log`. Three arms: `cli` is the built-in `/compact` summary
already on disk, `skill` is this skill invoked on the same transcript, and `pinning` is
the one-paragraph addendum spliced into a real compaction.

| Class | Built-in | Skill | Pinning | n |
|---|---:|---:|---:|---:|
| file paths | 49.7% | **63.6%** | 58.0% | 5 |
| identifiers | 67.6% | 67.5% | 65.6% | 6 |
| CORRECTIONS | 66.7% | 66.7% | **100.0%** | 1 |
| rejected approaches | 0.0% | 0.0% | 0.0% | 2 |
| constraints | no spans detected | | | 0 |

And the confounds, printed beside every score because a win that vanishes when these
match is not a win:

| | Built-in | Skill | Pinning |
|---|---:|---:|---:|
| median summary length | 13,927 chars | 11,486 | 13,235 |
| mean extractiveness | 0.15 | 0.14 | 0.19 |

**The log states its own null result plainly**, and it is the line worth reading twice:

> skill beat cli on correction recall in 0 of 6 paired transcripts.
> With n=6, only a large effect is resolvable; report the MDE, not just the gap.

So the honest summary of the run is: the skill retains more file paths on a 5-transcript
comparison while writing a shorter, less extractive summary, it matches the built-in on
identifiers, and on the two classes the whole skill is built around, corrections and
rejected approaches, the sample is one transcript and two transcripts respectively.
Nothing about a class with n=1 is a result.

## The finding that undercuts the headline

**The committed benchmark artifacts were scored with the exact matcher, and the skill's
own case study proves that matcher scores a full pinned block at 0.0%.**

`references/case-study-paired.md` is a hand audit of three summaries of one real
session. Two of them cover the same window eleven minutes apart, and each pinned seven
or eight rejected approaches with their reasons. Scored by exact match, both reported
**0.0% on rejected approaches across 49 detected spans**, and corrections reported
`n/a`. Both numbers are wrong about what happened.

Three instrument faults were found and all three are fixed in the scripts as they
stand today:

1. **Exact match cannot see a faithful restatement.** A pinned rejection is
   legitimately reworded while keeping its reason, so the semantic classes now score
   distinctive-token overlap. Exact match stays for paths, ids and error strings, where
   nearly-right is worthless.
2. **Corrections were read only from user rows.** The one correction both summaries
   chose to pin came from a peer runner correcting the parent's false claim. Non-user
   rows are now read under tighter wording.
3. **User messages keyed on their first 60 characters.** Twenty-six turns collapsed
   onto four keys, and one instruction quoted verbatim keyed as a command wrapper and
   scored as dropped by both arms. The key now strips the furniture.

After the fixes, the same window scores user messages 35.7% against 50.0%, corrections
1 of 1 for both, and rejected approaches 34.7% against 65.3%, all of which previously
read 0.0% or `n/a`. The instrument moves.

The committed head-to-head has not been re-run since. This is checkable rather than
inferred: `scripts/benchmark_vs_compact.py` as it stands writes a `matcher` field
alongside every class score, recording `soft` or `exact` per class. **No score object in
`docs/benchmark-head-to-head.json` or `docs/benchmark-cli-baseline.json` carries a
`matcher` key**, and neither file has a `user messages` class, which the current script
produces. So both artifacts predate the fix, and their three 0.0% rejected-approach
rows are precisely the artifact the case study identifies.

The case study draws the consequence itself, and it is the most honest sentence in the
plugin: the 0.3% rejected-approach retention is a floor on the built-in that no arm
could beat as measured, so it distinguishes nothing between arms. What it supports is
the claim the built-in independently demonstrates: **the built-in prompt carries almost
no negative knowledge.** What it cannot support is any comparison between arms.

The case study also refuses to declare a winner from its own percentages. On a long
window the detector samples most of its spans from the recent, denser portion, so any
recall percentage over that population rewards exactly the recency bias the case exists
to document. Its stated ordering is: read the disjoint sets first, use soft recall as a
floor check on whether a class is being dropped wholesale, and keep exact recall for
paths, ids and error strings only.

## The thirteen eval prompts have never been run

They are not vague. Every one is a compaction scenario with assertions checkable by
exact string match against the source, or by running `score_retention.py`, and
`evals.json` states why there is no judge: G-Eval correlates with humans at roughly
0.514 against 0.8 to 0.9 inter-human agreement, and a Claude judge marking a
Claude-written summary carries self-preference bias.

| Eval | Assertions | What it protects |
|---|---:|---|
| 1 corrections-survive | 4 | Three corrections carried as standing constraints, not narrated as history |
| 2 verbatim-preserved | 6 | A port, a path, a test name, an error string and a keychain id reproduced byte for byte |
| 3 drops-the-recoverable | 5 | Forty explored files and six test runs dropped, the one found path kept |
| 4 states-the-failure | 4 | Unfinished work described with its failure mode |
| 5 negative-knowledge-survives | 5 | The class the baseline retains at zero |
| 6 quantifier-and-scope-survive-verbatim | 5 | "only on 4.8" surviving as a scope, not a vibe |
| 7 beats-the-builtin-on-the-same-transcript | 5 | The head-to-head, as an eval rather than a script run |
| 8 both-kinds-of-dead-end-survive | 6 | Method lessons and product decisions live in different places |
| 9 pin-or-point-never-assume | 5 | From the v2 case study |
| 10 unfinished-obligation-not-just-clean-tree | 5 | A clean tree is not a finished obligation |
| 11 pinned-block-buys-the-narrative-no-slack | 5 | The pinned block is not a licence to pad the rest |
| 12 peer-agent-correction-is-a-correction | 5 | The exact fault the scorer had |
| 13 reread-list-names-the-steering-files | 7 | Which files the next session has to open again |

Evals 8 through 12 come from the paired case study, so each encodes a failure mode
observed in a real session rather than a hypothesised one. Eval 7 is the head-to-head
expressed as an eval, which means the benchmark that has run and the eval set that has
not overlap at exactly one point.

There is no adversarial case in the set. The standard asks for one, and the obvious
shape is a prompt that rewards padding: a session with almost nothing load-bearing in
it, where the correct pinned block is short or empty and the tempting answer is to fill
it.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| Do the committed baseline figures reproduce from the committed JSON | **Yes, all seven, to the decimal.** Recomputed independently, including the median convention (40 events, so the mean of the 20th and 21st values, 22,214.5). |
| Do the committed artifacts match the current scripts' output shape | **No**, and that is the finding above. No `matcher` field, no `user messages` class. |
| `SKILL.md` frontmatter parses | Passes. `name: braindump` matches the directory and the plugin manifest. This plugin keeps its SKILL.md at the plugin root rather than under `skills/`, which the site's conformance gate handles explicitly. |
| SKILL.md against the 500-line conformance ceiling | Passes, at 411 lines. |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 4. |
| Both scripts byte-compile | Passes: `score_retention.py`, `benchmark_vs_compact.py`. |
| Everything the plugin claims to ship exists | Passes. The three references, the two scripts, the four deep-research reports with their source lists, and the three benchmark artifacts. The README's "what's in the box" listing resolves item for item. |
| Does the scorer's own gate fail on a bad input | **Not applicable in the usual sense.** `score_retention.py` is a measuring instrument rather than a gate: it reports per-class recall and exits, so there is no bad fixture that makes it refuse. The three faults above were found by hand-auditing its output against a transcript, which is the only method that would have found them. |
| The README's external claim | Traceable, and already caveated in place. The 0% and 38% constraint-violation figures are from ConstraintRot, and `references/evidence.md` records that they were read from the abstract only, with no scenario counts, domains or per-family breakdown. |
| Version agreement | Passes. `plugin.json` and `marketplace.json` both say 2.3.0. |
| Conformance | One failure that is not an evals failure: `assets/icon.png` is missing, which the repository gate reports separately. |

## What would settle what is still open

Three tasks, cheapest first.

1. **Re-run the head-to-head with the fixed matcher and commit the output.** The
   scripts already do it; nobody has pointed them at the six transcripts since the fix.
   This is the cheapest run in the plugin, the baseline arm is free, and it is the only
   way to find out whether the skill's advantage on the two classes it exists for is
   real or was hidden by an instrument that could not see a reworded rejection. Commit
   the JSON with its `matcher` fields so the next reader can tell which matcher produced
   which number.
2. **Run the thirteen eval prompts and grade them.** Every assertion is
   string-checkable, so this needs no judge and no panel: one arm with the skill, one
   arm with the built-in prompt on the same transcript, and an independent grader
   marking each assertion with the quoted string it found or failed to find. Eval 7
   overlaps the benchmark, so it doubles as a cross-check on the harness. Add the
   missing adversarial case in the same pass.
3. **Commit the 121-event scan's raw output.** The README's headline table rests on it
   and the file is not in the repository, so the strongest-sounding numbers in the
   plugin are the least checkable ones. Committing the JSON also makes it possible to
   re-score the same 121 events with the fixed matcher, which would say how much of the
   built-in's reported retention was real and how much was the instrument.

## Caveats, stated rather than buried

- **The n counts are small and the log says so.** Corrections rest on one transcript,
  rejected approaches on two, file paths on five. With six paired transcripts only a
  large effect is resolvable.
- **The correction detector is a keyword heuristic.** It misses politely phrased
  corrections and flags things that are not corrections. The README says to treat its
  output as a list to read rather than a number to quote, and the case study found its
  49-span sample included a command wrapper, a file listing and a section header.
- **The paired case study is one session.** It is an existence proof and a source of
  failure modes, not a rate, and it says so in its first paragraph.
- **No judged layer at all, by choice.** There is no blind panel here and there should
  not be one: a summary cannot be graded by the family that wrote it, and the
  literature on judge agreement is why every assertion is a string match instead.
- **Length is a confound, and it points the useful way.** In the case study the
  longer, more extractive summary is not the one that carried more, which is why both
  confounds print beside every score.
