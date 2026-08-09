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

## What is not yet measured

**Whether v4 beats v3, or beats nothing at all.** The work-floor clause is an argument from the
numbers above, not a result. A third arm is running as this ships; until it lands, the honest
statement is that the diagnosis is measured and the fix is reasoned.

**Whether the block's saving exceeds its own cost on real traffic.** The right measurement is total
session tokens including cache misses, never this-turn output length. A preamble can always be tuned
to shrink visible output while forcing more turns to finish the same task.

**Quality, by a human.** Both instruments above are machine graded. The blind panel is three models
judging other models.

**Sample depth.** Two samples per task and model is the window the benchmark's own spec requires. It
is thin, and JetBrains' warning applies here too: never trust a k=1 eval, and treat a two-sample
window as only a little better.

## A correction worth recording

An earlier internal brief criticised caveman for a 65% headline. That criticism is out of date. Its
current README reports 8.5% for agentic runs, links the independent JetBrains study, warns that
savings can go net negative on already-terse workloads, and says plainly that neither number is
yours. The disagreement in this repo is with the skill's rules, not with how it presents itself.

## Reproducing

```bash
# the paired comparison, from the benchmark's own store
sqlite3 "~/Library/Application Support/Benchwarmer/benchwarmer.sqlite"   # see evidence.md for the query

# the blind panel
python3 evals/build_blind_bundles.py /tmp/td-blind 14
./evals/run_blind_panel.sh /tmp/td-blind
python3 evals/score_blind_panel.py /tmp/td-blind
```
