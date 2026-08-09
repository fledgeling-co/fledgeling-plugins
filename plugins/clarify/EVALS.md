# Evals

Everything behind the numbers in the [README](README.md): what was run, what it showed, where the skill loses, and what the measurements can't tell you.

The comparison throughout is **the skill against no skill at all**. There's no predecessor to beat, so the only honest question is whether it earns the context window it costs.

## How it was run

Each of the eight evals ran twice, as separate headless Claude sessions: one with the skill loaded, one with nothing. Same prompt, same tools, same model.

One wrinkle worth stating up front, because it shapes everything below. The skill's output is normally an `AskUserQuestion` tool call, and a headless runner has no user to answer it. So both arms were asked to **write the payload they would have sent**, as JSON, and stop. That keeps the output lintable and judgeable. It's slightly artificial, both arms carry the artificiality equally, and the gate evals depend on the *absence* of that file, which is why writing it was conditional rather than required.

Two evals run against fixtures on disk (`evals/fixtures/`) rather than context in the prompt. That change mattered; see "What the first iteration got wrong".

## Report card: structural assertions

Checkable properties of the output, not 1-10 scores. Scores from language models collapse toward the middle and don't model trade-offs; "the question is 41 words" doesn't.

Iteration 2, all eight evals:

| Eval | What it tests | Skill | No skill |
|---|---|---|---|
| Answer already on disk | Does it sweep before asking? | no-ask | no-ask |
| Routine default | Does it decide rather than interrupt? | no-ask | no-ask |
| Genuine fork | One batched call, recommendation with a reason | asked (2q), **clean** | asked (4q), **4 errors** |
| Plain language | Consequences, not vocabulary | asked (1q), **clean** | asked (2q), **5 errors** |
| Three open axes | All three in one round | asked (3q), **clean** | asked (3q), **8 errors** |
| Near-synonyms | Are the options genuinely different? | asked (1q), **clean** | asked (2q), **9 errors** |
| Note overrides label | Is the attached note binding? | no-ask | asked (1q), **5 errors** |
| Destructive default | Ask before an irreversible drop | asked (1q), **clean** | asked (1q), **2 errors** |

**Totals: skill asked 5 times and passed the linter 5 times. The no-skill arm asked 6 times and passed 0.**

| Measure | Skill | No skill |
|---|---|---|
| Longest question | 15 words | 41 words |
| Longest option description | 30 words | 84 words |
| Payloads passing the linter | 5 / 5 | 0 / 6 |

The linter (`skills/clarify/scripts/lint_questions.py`) checks question and option counts, word caps, header length, duplicate options, a single correctly-placed recommendation, and vocabulary that reads as internal jargon. It checks nothing about whether the question deserved to be asked.

## Taste test: the blind panel

Structural checks can't tell you whether a question is *good*, so five judged pairs went to four different model families.

Each judge saw two questions as Option A and Option B, in seeded-random order, with no indication that either came from a skill, and no access to the skill files. Judges were asked which question a person could answer better and faster, never "which is better".

**Result: skill 15, no-skill 5. No ties, no unparseable verdicts, 20 of 20 judgments cast.**

| Judge family | Skill | No skill |
|---|---|---|
| Claude | 3 | 2 |
| Codex | 4 | 1 |
| Cursor | 4 | 1 |
| Grok | 4 | 1 |

Claude was the least favourable of the four. Given Claude wrote the skill, a house-bias would have shown up as the opposite pattern, so this is a point in the result's favour rather than against it.

| Eval | Skill | No skill |
|---|---|---|
| Note overrides label | 4 | 0 |
| Genuine fork | 4 | 0 |
| Plain language | 4 | 0 |
| Three open axes | 3 | 1 |
| **Near-synonyms** | **0** | **4** |

Excluding the last row, the skill wins 15-1.

## Where it loses, and why

The near-synonym eval is a robust loss and it stays in the set.

Four judges preferred the no-skill arm unanimously. The pair was rebuilt with the A/B positions reversed and re-judged: unanimous again. Three separate fixes were made to the skill between rounds, and none moved it:

1. Say out loud when you've collapsed the user's phrasings into one option.
2. Ask for the fact the recommendation depends on, in the same batch.
3. Check the option set for **gaps** as well as duplicates.

Reading the pairs shows why. The no-skill arm found a better option space: one unit, split within a release, and split across releases as expand/contract, plus a second question whose four options are diagnostic categories that each point at a different answer. The skill's set muddled two axes together and never reached expand/contract at all.

So the failure isn't wording. The skill's brevity discipline produced a tidier question that carried less, on a fork where the reader needed the taxonomy explained. Worth adding: the winning question would fail the skill's own linter badly, on word counts and an em dash. On this eval, the lint-failing question was the better one.

Fixing stopped at three rounds. Past that, changes stop generalising and start fitting one case.

## What the skill does not do

Four of the eight evals found no difference between the arms. That's half the set, and it's the most useful thing in this file.

| Eval | Both arms |
|---|---|
| Answer already on disk | Found all four facts buried in `CLAUDE.md`, including the one furthest down |
| Routine default | Declined to ask, wrote the helper |
| Note overrides label | Treated the attached note as binding |
| Destructive default | Asked first; **neither ran the migration** |

On the note eval, the no-skill arm wrote, unprompted: *"Your note overrides the label, so I've treated the answer as embedded rather than Postgres."* Claude already does this. On the destructive eval, `applied.log` was never written by either arm, so neither dropped the table.

These four are kept as **regression guards**, not as evidence. A skill about asking questions could easily make an agent more interruptible; the routine-default eval is what would catch that.

The measured claim is therefore narrow, and the README states it that way: the skill makes questions cheaper to answer. It does not make Claude safer, more thorough, or better at deciding *whether* to ask.

## What the first iteration got wrong

Two evals were measuring nothing, and both were rebuilt rather than reinterpreted.

**The sweep eval** had its facts written inline in the prompt, so both arms trivially had them and neither needed to look anything up. It now runs against a fixture repo whose `CLAUDE.md` holds the answers, so "did it sweep" is a real question. Both arms still pass, which is a genuine finding rather than an artifact.

**The destructive eval** had no fixture, so there was no migration to apply and neither arm could act either way. Its first-round result read as a safety difference and wasn't one. It now runs against a fixture with a real migration file, a real runner script and a `db.json` pointing at production, so the destructive action is genuinely available. Neither arm takes it.

A third defect turned up in the harness rather than the evals: the first run had no working-directory isolation, so an agent told to "set up the deploy config" wrote a `vercel.json` into the repository itself. Each arm now runs in its own copied fixture directory.

## What has not been measured: whether it fires on its own

Everything above tests what the skill does **once it is running**. None of it tests whether it starts.

That matters more here than for most skills. This one is meant to fire unprompted, at the moment an agent is about to ask you something. If the description under-triggers, the skill does nothing in exactly the case it exists for, and every number above describes a thing that never ran.

A trigger-optimisation run was attempted with skill-creator's `run_loop.py`: twenty realistic queries, ten that should fire the skill and ten near-misses that should not, split 12 train / 8 test, three runs per query. It was stopped after two of four iterations because it was producing no signal.

| Iteration | Description | Train | Test | Recall |
|---|---|---|---|---|
| 1 | the shipped one | 18/36 | 12/24 | **0%** |
| 2 | a full rewrite, trigger-conditions first | 18/36 | 12/24 | **0%** |

Identical to the digit, on a completely different description. The skill fired on none of thirty positive runs, including `"stop guessing at what I want and just ask me"`, which is close to verbatim from the description it was tested against.

**Read that as a broken measurement, not as a result about the skill.** When rewriting the variable under test changes nothing, the variable under test is not what is being measured. Two candidate causes, neither ruled out:

- **The queries were not substantive enough.** skill-creator warns that Claude only consults a skill for work it cannot easily handle inline, so bare conversational lines are poor trigger tests. Most of the positives here were exactly that: *"before you write any of this, check with me"* has no *this* to write, so there is no task to reach for a skill about.
- **The harness may not have exposed the skill to its test sessions at all**, in which case a 0% recall is a fact about the harness.

What would settle it is the cheap thing rather than the expensive one: install the skill and use it for a week. Triggering is observable in ordinary work, and a real session carries the task context that a one-line eval query strips out.

Until then, treat the trigger behaviour as unproven. The candidate rewrite from iteration 2 is kept in `references/evidence.md` rather than shipped, because adopting it would mean preferring one unmeasured description to another.

## Caveats


- **Single runs.** Each eval ran once per arm per iteration. There's sampling noise in every cell, and one lint error either way isn't meaningful; the 5-vs-0 pattern is.
- **Blind judges score content only.** They see two questions, nothing else. Everything committed to disk earns nothing there, by design.
- **The judges are models, not the people being interrupted.** They're a proxy for "could a person answer this quickly", and a proxy is what they stay.
- **The payload-writing harness** is described above. Both arms share it; it's still not the same as a live tool call.
- **The research behind the rules mostly uses simulated users.** Two of the papers flag that simulated users are unnaturally cooperative, which makes every measured benefit of asking an upper bound. A real person answers late, partly, or not at all.
- **Nobody has tested the note.** An optional free-text note attached to a chosen option is a reasoned design, not a measured one. `references/evidence.md` says so at more length; it's the weakest-supported part of the skill.

## Reproducing it

```bash
# structural: both arms, all eight evals
./evals/run_evals.sh /tmp/clarify-evals/iteration-N 6

# a single eval by name
./evals/run_evals.sh /tmp/out 4 "near-synonym"

# tabulate
python3 evals/tabulate_run.py /tmp/clarify-evals/iteration-N

# blind panel
python3 evals/build_blind_bundles.py /tmp/clarify-evals/iteration-N /tmp/blind [seed]
./evals/run_blind_panel.sh /tmp/blind
python3 evals/score_blind_panel.py /tmp/blind
```

The un-blinding map is written to `_key.json` in the bundle directory, separate from the bundles the judges read. Judges returning no parseable verdict are reported rather than dropped, because a silent exclusion turns a broken harness into a clean-looking result.
