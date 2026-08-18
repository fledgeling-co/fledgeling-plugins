# EVALS

The full comparison behind the README's summary. Every number here is from a run that happened, and
where a figure rests on something weak, this file says so rather than burying it.

## What was compared

| Arm | What it is |
| --- | --- |
| **baseline** | `claude-opus-5`, no skill |
| **compressed prose** | `claude-opus-5-caveman`: the caveman `SKILL.md` body appended to the system prompt |
| **discipline** | `claude-opus-5-tokendiscipline`: the v4 block appended the same way |

All at `xhigh` effort on diolog-swe-bench, graded by that repo's own canonical spec
(`docs/SCORING.md`): binary fail-to-pass for behavioural dimensions, judge score for `optimality`
and `ui`, and the mean of the two most recent clean decided samples per model and task.

Injection is identical across arms, so the comparison is between two blocks of text and not between
two delivery mechanisms.

## Report card: baseline against compressed prose

106 tasks carry both arms.

| | baseline | compressed prose | delta |
| --- | --- | --- | --- |
| Task score | 63.3% | 55.7% | **-7.61 points** |
| Cost | $229.02 | $152.34 | -33.5% |
| Tokens | 126.1M | 73.4M | -41.8% |
| Steps per task | 24.5 | 16.5 | -32.7% |
| Tokens per step | 48.6k | 42.0k | -13.6% |

48 tasks worse, 15 better, 43 unchanged. Sign test over the 63 directional tasks: **p < 0.0001**.

### Where the saving actually came from

Steps fell 32.7% and tokens per step fell 13.6%. Those compose exactly:
`(1 - 0.327) x (1 - 0.136) = 0.582`, which is the observed -41.8%. So about **78% of the token
saving is the agent taking fewer steps**, and only the remaining fifth is terser writing.

This is the finding the whole rebuild turns on. A skill that promises shorter prose and delivers
less investigation is not mispriced, it is measuring the wrong thing, and every token dashboard
rewards it.

### By dimension

| Dimension | tasks | baseline | compressed | delta | worse / better |
| --- | --- | --- | --- | --- | --- |
| tool-use | 4 | 100.0% | 75.0% | -25.00 | 1 / 0 |
| backend | 42 | 54.8% | 46.4% | -8.33 | 8 / 3 |
| ui | 45 | 67.0% | 59.5% | -7.45 | 35 / 7 |
| optimality | 10 | 75.0% | 72.8% | -2.19 | 4 / 5 |
| frontend | 5 | 50.0% | 50.0% | 0.00 | 0 / 0 |

The tool-use row is four tasks. It is the largest delta on the sheet and the least trustworthy
number on it; treat the direction as a hint and the magnitude as noise.

### Session length is the variable that matters

| Task length (baseline arm) | tasks changed | worse | better | sign test |
| --- | --- | --- | --- | --- |
| 10 to 19 steps | 23 | 13 | 10 | p = 0.68, no effect |
| 20+ steps | 38 | **34** | **4** | **p < 0.0001** |

Compression is close to harmless on short work and reliably harmful on long agentic work. That
split also reconciles this result with JetBrains' null on Sonnet 5 at low effort, which ran shorter
tasks on a smaller model.

### The rule was barely followed anyway

Measured across 683 compressed and 370 baseline transcripts: caveman forbids decorative structure,
and **97.5% of its runs still emitted markdown**, against 98.9% of baseline runs. Median final
message fell from 2,690 to 1,979 characters, a 26% cut, against a median 1.19M tokens per task.

So the register instruction is close to a no-op, while the behavioural distortion it causes is not.
You pay the instruction-following tax without collecting the register.

## Blind taste test

The benchmark grades itself. This is a second instrument that does not.

14 pairs of real finished work were drawn from the stored transcripts, one response per arm on the
same task. Order within each pair was decided by a seeded coin, so "A" carries no information. Judges
saw the two responses and nothing else: no arm labels, no skill files, no benchmark grade, no
knowledge that a skill was involved at all.

| Judge family | preferred baseline | preferred compressed | tie |
| --- | --- | --- | --- |
| Claude | 11 | 2 | 1 |
| GPT (codex) | 10 | 4 | 0 |
| Grok | 8 | 6 | 0 |
| **Total** | **29** | **12** | **1** |

41 decisive verdicts, sign test **p = 0.0115**. Per pair, taking each pair's majority: baseline 10,
compressed 4, no splits, none undecided.

Three heterogeneous families leaned the same way. Grok leaned least, which is worth knowing: a
single-family panel reporting 11 to 2 would have overstated the effect.

Bundles, the withheld key, the raw verdicts and the scorer are in `docs/blind-panel/` and `evals/`
so the whole thing can be re-run or disputed.

## The arm landed, and it is a split result

106 paired tasks, one sample each against the baseline's two-sample window.

| | baseline | caveman | discipline v4 |
| --- | --- | --- | --- |
| Task score | 63.3% | 55.7% | **61.6%** |
| Direction vs baseline | | 48 worse / 15 better, p < 0.0001 | **32 worse / 30 better, p = 0.90** |
| Cost | $229.02 | $152.34 | **$303.77** |
| Steps per task | 24.5 | 16.5 | 21.6 |

**The score regression is gone.** Caveman cost 7.61 points with a sign test at p < 0.0001. v4 sits
1.73 points below baseline at 32 worse against 30 better, p = 0.90, which is indistinguishable from
no difference. On the thing this rebuild was for, the work floor did its job: the block no longer
buys its saving by making the agent investigate less, and steps per task fell 12% rather than 33%.

**And it did not save anything. It cost 32.6% more than running no block at all.** That is the
opposite of the point, and it is the headline for anyone deciding whether to switch this on.

Three readings, and this measurement cannot separate them.

1. **Clause 6 may be doing too much.** "Take the steps the task needs" protects investigation, and
   protecting investigation costs money. A clause written to stop the model doing less can push it
   into doing more.
2. **The one-sample window inflates the sum.** Baseline cost is a mean over two samples per task, so
   an unlucky expensive run is halved; v4's is a single draw, so one 40-minute task lands at full
   weight. With per-task costs ranging past $5, that alone could account for much of a 33% gap. The
   two arms are not on equal footing for cost, and the score comparison is the part this run
   supports properly.
3. **The block's own token overhead is about 220 tokens per turn**, far too small to explain the gap.

**What this changes.** The claim "spend fewer tokens without doing less work" is now half-supported.
The second half is measured and holds. The first half is not supported by this run and is
contradicted by it, so until a two-sample cost arm exists the block should be described as removing
caveman's quality regression rather than as a saving.

The regression this project set out to fix is fixed. The benefit it was supposed to deliver is not
demonstrated.

## The structural gate: before and after

The two instruments above are expensive and slow. This one is deterministic, free, and runs on every
commit: `skills/discipline/scripts/block-check.py`. It exists because seven properties of this skill
were previously asserted in prose — "a test asserts they do not drift" — with no test anywhere in the
repo. Prose claiming a gate already runs is worse than prose asking for one, because it reads as
covered.

Both trees scored on the same 19 assertions. "Before" is this skill's own predecessor, the v3-era copy,
with the gate copied in and its paths remapped so the comparison is like-for-like.

| Assertion | before (v3-era) | after |
| --- | --- | --- |
| `block/retention` — every shipped literal still present | **FAIL** (2 of 3) | pass |
| `block/v4` — byte count and sha256 | n/a (no v4) | pass, 881 B |
| `block/v3` — byte count and sha256 | pass, 736 B | pass |
| `block/v1` — byte count and sha256 | pass, 1,029 B | pass |
| `block/ceiling` — inside 1,200 bytes | pass, **464 B spare** | pass, 319 B spare |
| `block/literal` — nothing that varies | pass | pass |
| `block/register` — no MUST / CRITICAL | pass | pass |
| `block/quality-floor` — all five survivors named | pass | pass |
| `block/work-floor` — clause 6 present | **FAIL** | pass |
| `block/no-verification-ban` — has not re-acquired v1 clause 4 | pass | pass |
| `block/no-self-audit` — never asks for compliance confirmation | pass | pass |
| `provenance/mark` — both marks real, one per family | **FAIL** (no registry) | pass, 24 rows |
| `provenance/promotion` — independence pinned per row | **FAIL** (no registry) | pass, 24 pins |
| `provenance/observed` — living sources dated | **FAIL** (no registry) | pass |
| `provenance/drift` — registry matches the prose | **FAIL** (no registry) | pass |
| `provenance/coverage` — no untiered figure in SKILL.md | **FAIL** (no registry) | pass, 34 figures |
| `provenance/assumed-containment` × 3 files | **FAIL** (no registry) | pass |
| `references/exist` — every pointer resolves | pass | pass |
| **Total** | **9 pass / 3 fail** (11 unscoreable) | **20 pass / 0 fail** |

**Where the older version wins, because a scorecard that only shows wins convinces nobody:** its block
is 736 bytes against 881, so it leaves 464 bytes of headroom where this one leaves 319, and it is
cheaper per turn in the cached prefix. Clause 6 is what bought those 145 bytes. Whether that trade is
worth it has never been measured — v4 has never been compared against v3 — so on pure prefix cost the
predecessor is the better artifact and the case for v4 rests on the correctness argument, not a number.

### The gate was mutation-tested, because a gate that only ever passes is decoration

Twenty-six deliberate defects were introduced one at a time into a scratch copy. **All twenty-six were
caught**, each with a message naming the silent downstream consequence rather than just "invalid":

*Block* — same-length edit to a literal · block over the byte ceiling · a date inside the literal ·
`CRITICAL:` in the register · quality floor losing a survivor · work floor removed · v1's verification
ban returning · a self-audit clause added · a retained literal deleted · a dead reference pointer.

*Provenance shape* — an invented mark · a single bare mark · two independence marks · two verification
marks · the two families written in the wrong order · `assumed` paired with a verification state ·
`none` paired with a real source · a living-source date stripped · a date in the future · the registry
drifting from the prose · an untiered figure added to SKILL.md · an assumed figure moved into the
argument.

*Promotion* — `self-report` → `independent` · `anecdote` → `independent` · `assumed` → `first-party` ·
a new row added with no pin. And the converse case is checked too: a legitimate move along the
verification axis (`summarised` → `results-read`, once someone reads the PDF) still **passes**, because
a guard that blocked real corrections would just get switched off.

Four of those defects were not hypothetical. On its first run against the real tree the gate failed
`provenance/assumed-containment` and `provenance/drift`, finding that the README stated an unmeasured
output share as though it were a finding, and that the Giskard figures the prose claimed to carry had
gone missing in a migration. It then caught two more figures the author added untiered while writing
this very section — and one in this very paragraph.

The promotion guard exists because of a miss. The first version of the two-family check passed a row
that had been quietly changed from `self-report` to `independent`, since both marks are individually
well-formed and a stateless gate has no history. Pinning each row's independence mark inside the script,
the same way the block literals are pinned, is what closed it: independence can still be changed, but
not without editing the gate in the same commit.

## What is not yet measured

**Whether v4 beats v3.** The arm above compares v4 against no block, not against v3. Nothing here
says the work-floor clause improves on the block that preceded it.

**Whether v4 saves anything.** It did not on this run. A cost claim needs a two-sample arm measured
on the same footing as the baseline.

**Whether the block's saving exceeds its own cost on real traffic.** The right measurement is total
session tokens including cache misses, never this-turn output length. A preamble can always be tuned
to shrink visible output while forcing more turns to finish the same task.

**Quality, by a human.** Both instruments above are machine graded. The blind panel is three models
judging other models.

**Sample depth.** Two samples per task and model is the window the benchmark's own spec requires. It
is thin, and JetBrains' warning applies here too: never trust a k=1 eval, and treat a two-sample
window as only a little better.

## A correction worth recording, and then a correction to the correction

An earlier internal brief criticised caveman for a 65% headline. A later version of this file said
that criticism was out of date because caveman's README now reported 8.5% for agentic runs and linked
the independent JetBrains study.

**Both documents were fetched on 18 August 2026, and that second claim does not hold.** The README's
headline is still 65%; the string `8.5` appears in neither the README nor its
`docs/HONEST-NUMBERS.md`; neither mentions JetBrains.

What is verbatim there, and is genuinely to caveman's credit: an "Honest number warning" stating that
only output tokens shrink, that the skill adds roughly 1 to 1.5k input tokens per turn, and that
savings can go net negative on already-terse workloads. `HONEST-NUMBERS.md` goes further than this
repo had credited and lists the aggregate output reduction as "Not published", telling readers to
measure their own A/B.

So the substance survives — **the disagreement here is with the skill's rules, not with how it
presents itself** — but the sentence describing a third-party document did not, and it was wrong in
four files at once for about a week. The fix is structural rather than editorial: every figure now has
a row in `skills/discipline/references/provenance.md`, and a row citing a living document must carry
the date it was read. `scripts/block-check.py` fails the build on one that does not.

That is the most useful thing in this file for anyone building something similar. A claim about what a
competitor's README "currently says" has a shelf life, and without a date on it nobody can tell
whether it has expired.

## Reproducing

```bash
# the structural gate: block pins, byte stability, register, floors, provenance tiering
python3 skills/discipline/scripts/block-check.py --verbose   # must exit 0

# the paired comparison, from the benchmark's own store
sqlite3 "~/Library/Application Support/Benchwarmer/benchwarmer.sqlite"   # see evidence.md for the query

# the blind panel
python3 evals/build_blind_bundles.py /tmp/td-blind 14
./evals/run_blind_panel.sh /tmp/td-blind
python3 evals/score_blind_panel.py /tmp/td-blind
```

The gate is the only one of the three that is deterministic and free, so it is the one that runs on
every commit. Check its exit code rather than its output: piping it through `grep` makes `$?` grep's
status and not the gate's, which is how a failing gate gets read as a pass.
