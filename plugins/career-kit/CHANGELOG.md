# CHANGELOG

## 0.4.7

`career-kit:resume-craft`: an audit for over-corrections, and four rules from it.

- The person asked for the skill and one engagement's drafts to be checked for further
  over-corrections. Ten were found and are listed in `references/corrections.md`. Their common
  cause was treating the latest instruction as the only one.
- `SKILL.md`, "Applying a rule or a correction", gains four rules: a rule about form never
  licenses a new claim; a rule never forbids the accurate word; the person's standing decisions
  are kept on a list and checked after every revision; a lint warning is a prompt to read the
  line, not a fault to clear.
- `scripts/resume_lint.py --keep FILE` fails when a term the person asked for, or a required
  phrase they hold, has gone missing. The told-twice warning now needs a run of 12 shared
  words, since a required term named in the summary and shown in a role shares words by
  design. The lint prints a reminder not to edit merely to clear a warning.
- Recognition is stated as what was awarded and to whom; "I was part of the team" only when
  the person confirmed it. Skills labels use the plainest true word, whether or not the ad
  uses it.
- Not re-run: the skill's evals.

## 0.4.6

`career-kit:resume-craft`: the key skills say what the person is unusually good at.

- A skills section made general, as asked, was then described as reading "like a list of items
  to tick off from a job role". It had been built from the ads and generalised by removing
  detail, and nothing asked whether an item distinguished the person. `SKILL.md` now says
  general is not generic: the claim sections take their content from the person first and are
  checked against the ad second.
- `references/sections.md`: build the skills from what recurs across roles, what the person is
  relied on for and what the title did not require; label each line by the strength; give entry
  requirements one craft line at most, last. A same-title test for every item.
- `scripts/resume_lint.py` warns `skill-generic`, with a self-test. The worked example and
  `tests/good.md` are rewritten to match.
- Not re-run: the skill's evals.

## 0.4.5

`career-kit:resume-craft`: each section speaks at its own level of generality.

- A skills line had been rewritten to describe the bullet that proved it, and the person said
  it made them look like "a one-trick pony". `SKILL.md` has a new table, "The level each
  section speaks at": the summary is about the person whatever the job, a skill is an ability
  that carries to another role, a scope line is about this role, and a bullet is one occasion.
  The claim and its proof are kept apart.
- `references/sections.md`: a skill is stated at the level it transfers, with no employer,
  product, system or data set named; the proving line is found by reading down the page.
- `scripts/resume_lint.py` warns `skill-long` and `skill-specific`, with a self-test.
- The worked example and `tests/good.md` are rewritten to match.
- Not re-run: the skill's evals.

## 0.4.4

`career-kit:resume-craft`: rules for applying a correction without over-correcting.

- Four corrections in a row, each applied to more than it said, left a summary that never
  mentioned a twenty-year career. `SKILL.md` has a new section, "Applying a rule or a
  correction": name the fault and what it leaves alone, ask what the text was there to do,
  recast before cutting, re-run the section's whole job afterwards, and let the job win over a
  length or count default.
- New `references/corrections.md`: every correction the skill has absorbed, with what it
  forbids and what it leaves in.
- `references/sections.md`: "no count of years" removes the number and keeps the breadth; for
  a long career the summary's difference is the span, in one clause, most recent first.
- Not re-run: the skill's evals.

## 0.4.3

`career-kit:resume-craft`: a general rule that every sentence is about the person.

- A summary written to the skill's own template opened with a title and a statistic about the
  product, and the person it was for said it read as a plain fact where it should describe a
  responsibility. They asked for broader rules. `SKILL.md` and `references/voice.md` now say:
  every sentence has the person doing, owning, deciding or answering for something; a figure
  sizes their responsibility; a title is a label and lives on the role line; context goes in a
  clause. The test is to take the person out of the sentence and see whether it is still true.
- The summary's first part is now "what they are responsible for", and the worked example and
  `tests/good.md` open that way.
- `scripts/resume_lint.py` warns `label-opener`, `figure-on-object` and `not-about-person` on
  summary sentences, with a self-test.
- Not re-run: the skill's evals.

## 0.4.2

`career-kit:resume-craft`: the summary no longer ends on "one proof, naming the decision".

- A summary written to that rule ended on a single incident, and the person it was for called
  it too specific. The fourth part of a summary is now the judgement the work turns on, in a
  sentence that is true every week; the strongest example is the first bullet of the current
  role. Every sentence in a summary is standing and none reports one occasion.
- `references/sections.md` records the three ways this has gone wrong: the named incident, the
  pointer ("one such call"), and the habit made from one event. The worked example and
  `tests/good.md` are rewritten to match.
- `scripts/resume_lint.py` warns `summary-event` on a summary sentence that reports one
  occasion, with a self-test that it fires then and not otherwise.
- Not re-run: the skill's evals. The earlier rule came from them, so the next run should check
  that judges do not mark the standing sentence down as vague.

## 0.4.1

`scripts/run_panel.sh` takes its default lanes from the frontier tier of the model roster beside decision-panel's runner.

## 0.4.0

A second skill, `career-kit:resume-craft`, for the words of the résumé itself.

- `skills/resume-craft/SKILL.md`: what each of 8 sections is for with a test for each, the
  order of precedence when sources disagree, voice, suiting the document to an ad, and separate
  procedures for drafting and for reviewing.
- Five references: each section in depth with a worked example of an invented person; voice,
  verbs and cutting; structure, format and long tenure; tailoring and internal, external and
  public copies; Australian banking conventions for late 2026.
- `references/evidence.md` marks every rule as research, correction or this skill's inference,
  and says which wins where they disagree.
- `scripts/resume_lint.py`: section order and names, summary length, a count of years, personal
  details, date format, bare present-tense openers, the generic register, bullet counts, an
  empty education section and gap markers. `--self-test` runs two fixtures.
- `docs/deep-research/`: the five research reports the rules cite.
- `career-kit:career-kit` stage 5 and `references/documents.md` now point to the new skill.

## 0.3.0

From the last third of the same engagement, when the person read the panel-reviewed résumés and
found they read badly.

- `SKILL.md`: reading the document as its reader is now stated as the thing the checks do not
  cover. Prose is written whole, by hand; scripts render and check. Section jobs are written
  before drafting. One voice: first-person paragraphs, past-tense bullets.
- `references/documents.md`: what each section is for, with a test for each; using the whole
  career; voice, tense and person; reading the built page.
- `references/panels.md`: ask for a cold read before any rule; do not pass your own style rule
  as settled; ask what is missing; read the lanes' reasons yourself; when to stop.
- `references/website.md`: a generated video hero, and checking the whole domain before the
  address goes on a résumé.
- Twelve rows added to `references/evidence.md`.

## 0.2.0

From three further rounds of the same engagement on 20 November 2026: a five-lane review of the
finished résumés, a third question form, a domain registration, and six iterations on one image.

- The work is described as a loop of rounds, and a panel reviews the copy after every change,
  not once at stage 8. Both are stated at the top of `SKILL.md`.
- `references/panels.md`: when a panel runs, review against apply, giving lanes the whole fact
  base, the four kinds of drift to ask about by name, and how to handle a lane that answers late.
- `references/questions-form.md`: rounds, answer strength, a tick that contradicts its note.
- `references/website.md`: iterating on an effect, visibility, and a custom-domain procedure.
- `scripts/build_form.py` counts questions the person has looked at, and exports an untouched
  suggested default as `[suggested default, not touched]`. It used to count any question holding
  a value, so a form with pre-selected defaults read as complete before it was opened.
- Removed an employer name from a `make_variants.py` example and a person's name from a
  docstring.
- Twelve rows added to `references/evidence.md`.

## 0.1.0

First release. Built from one working session on 20 November 2026 that produced a complete
application kit for one person: four research lanes reconciled into a digest, a 20-finding
review page with cropped evidence, five role-targeted résumés from one source of facts, a
personal website, LinkedIn copy, and an interview guide.

- Ten-stage procedure in `SKILL.md`, with depth in eleven reference files.
- Nine scripts generalised out of that session: résumé and variant builds, styled Word,
  evidence cropping, the question-form generator, browser capture, the panel wrapper, a
  direct-router MCP caller, and `facts_lint.py`.
- `references/evidence.md` traces every rule to what happened in that session.
- Not registered in the marketplace, and no icon or banner yet.
