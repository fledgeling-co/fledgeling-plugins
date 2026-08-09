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

## Does it fire on its own?

Everything above tests what the skill does once it is running. This tests whether it starts, which for a skill meant to fire unprompted is the question the rest depends on.

It took three attempts, and the first two failed for the same reason.

**Attempt 1, skill-creator's `run_loop.py`.** Twenty queries, ten positive and ten near-miss, three runs each. Iteration 1 on the shipped description: 18/36 train, 12/24 test, 0% recall. Iteration 2 on a complete rewrite: identical to the digit. Stopped after two of four iterations, because rewriting the variable under test and getting the same number means the variable under test is not what is being measured.

**Attempt 2.** A substantive-sounding prompt, in a directory containing only the skill. It did not fire, and the run said exactly why:

> There is no app here. "This app" in the prompt has no referent, so there is nothing to add offline support *to*. I also didn't ask you a clarifying question about offline strategy, deliberately. Any such question would have taken the missing app as given and made the premise look confirmed.

That is the gate behaving correctly on an empty room, and it is the same flaw as attempt 1: skill-creator warns that Claude only consults a skill for work it cannot do inline, so a prompt with nothing behind it tests nothing.

**Attempt 3, with a real app.** A small React note-taking app for site surveyors, whose README states that coverage on site is bad. The prompt: *"Surveyors keep losing notes when they walk out of coverage. Add offline support to this app. Nothing in the repo says which way to go and we have never discussed it."*

| Case | Skill offered | Tools before deciding | Fired? |
|---|---|---|---|
| Real fork, real app | yes | `Bash ×3`, `Read ×2` | **yes** |
| Near-miss: "explain what this hook does" | yes | `Bash ×4`, `Read ×2` | **no** |

Both correct. The skill was confirmed present in the session's own skills list, so a non-firing result would have meant something; and it fired only *after* reading the repo, which is the skill's own ordering rather than a reflex.

What it produced is the better evidence. It found the actual mechanism of the reported data loss, unasked:

```js
create.mutate(draft);
setDraft("");          // cleared before the POST resolves
```

Out of coverage the request fails, no error state is rendered anywhere, and the note is gone. It then named two things it had decided rather than asked about (no conflict resolution, since notes are create-only and nothing can conflict; photos out of scope, since no capture path exists), before asking one question whose recommendation carried its reason: *"the reported problem is losing writes, and this is the smallest thing that actually stops that."*

**The honest size of this.** Two runs, each with one positive and one near-miss, both agreeing. That is a control, not a benchmark, and it should not be read as a trigger rate. What it does settle is the question attempt 1 raised: the 0% recall was an artifact of queries with no work attached, not a property of the description. A real trigger rate still wants a proper eval set built on real repositories, which is the thing worth doing next.

Reproduce it with `./evals/run_trigger_check.sh`, which stages the fixture and the skill and reports whether the skill was offered as well as whether it fired. Both matter: a non-firing result means nothing if the skill was never on offer, which is the trap attempt 1 fell into.



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
