# CHANGELOG

## Unreleased

Decisions from rounds six and seven on the source engagement, 23–24 November 2026: a second,
visual review of the rewritten résumé published as a private page, a 21-question phone form with
recommended answers chosen by a panel, and the person's answers applied and reviewed.

- `career-kit`: `scripts/build_paged_form.py`, the phone form (one question per screen, Now and
  Suggested panels, Send through the share sheet), from the same spec as `build_form.py`. Both
  builders take a `"recommended"` option and a per-question `"rec"` reason: labelled, never
  pre-selected, and tagged in the transcript. `crop_snippets.py` warns when a wrapped phrase is
  only partly highlighted.
- `career-kit` `questions-form.md`: recommending an answer (from the person's own words, "only
  you know" where it is theirs, check the record where their documents disagree, from a panel);
  the "why" line is fact-checked like copy; no benefit attached to one answer; a quoted fact's
  source is named; "Something else" with a note is read narrowly; a line is checked against the
  answers file before it is called form text.
- `career-kit` `review-page.md`: a second review of the rewritten résumé — crops from the public
  copy with a build-time gate on visible text, full-width crops at full width, crops anchored on
  phrases with tight padding, sketches from PDF coordinates, claims counted before publishing,
  and private publishing at an unlisted path.
- `career-kit` `panels.md`: account-level lane failures are reported, not retried; several small
  decisions in one run with a per-item table; proposed wording goes to the panel before it reaches
  the person. `documents.md`: reorder before cutting to fit, and cut by wrap-over lines.
  `project-record.md`: keep the confirmed facts current in place, record facts that do not exist,
  and keep a note of how the person answers. `SKILL.md`: check which copy was read before acting on
  "why was this removed".
- `resume-craft`: every edit, including a grammar or space edit, gets the four drift checks;
  proposed wording keeps confirmed phrases verbatim and is checked against the corrections log;
  a review counts its claims about the ads; the official title is printed and a corrected date's
  overlap is flagged, not closed. Six correction rows and their evidence.
- Not re-run: the evals.

Decisions from a fifth round on the source engagement, 22 November 2026, in which the person sent
free-text notes on the résumé and a page of 25 questions checked how they had been read.

- `resume-craft`: the summary names the platform or field and the industry, not a niche product;
  a mechanism is described by what it protects and the person's part in it; a scope line says
  what the role was for, who it served and what it was measured on, with complexity as part of
  scale; judgement and authority are shown more than process; each part of a mixed piece of work
  takes its own verb; where an achievement happened is a fact, and one program across two roles
  is told once in each; an example the person calls weak and cannot replace comes out, with the
  requirement it showed raised. New questions to ask of a role, eleven correction rows, and the
  summary example in `sections.md` no longer uses the mechanism wording the person rejected.
- `resume-craft` `tailoring.md`: internal performance language is softened on public copies.
- `career-kit`: check your reading of free-text feedback before rewriting, with one question per
  note and nothing pre-selected; put the rules you drew back to the person as a tick list, and
  record only the ticked ones as theirs; after a round of corrections, ask which other lines do
  not represent their work and recommend wording for those from the research on how hiring
  managers read.
- Not re-run: the evals.

## 0.5.0

`career-kit:resume-craft` reviewed and rebuilt as a whole, after a day of piecemeal additions.

- `SKILL.md` is rewritten at about three-quarters of its length. It now opens on the two layers
  the skill is made of, the research as the base and the corrections as writing guidance on
  top, with one order of precedence. The sixteen voice rules are grouped under four heads:
  about the person, true, worth reading, plain. Examples are drawn from several fields.
- Three contradictions are resolved. Length and count defaults are limits that are met by
  moving material, and a departure is listed with whose decision it was; the earlier text
  called them guides in one place and limits in another. A review's proposed wording now
  carries red placeholders where a better line is waiting on an answer, matching the draft
  convention. A bullet's test no longer asks for a number, since a weak figure is taken out.
- `references/voice.md` is reordered to follow how a draft is built. The level-of-generality
  table and the six rules for applying a correction move into the references.
- The worked example and `tests/good.md` follow every current rule.
- Includes the unreleased 0.4.11 changes: where a role's measure of success goes, selling what
  is true, ranking the detail, and the stricter rule on numbers.
- `career-kit:career-kit` is reviewed and rebuilt the same way. Its `SKILL.md` opens with how
  the work runs (research as the base, only confirmed facts and all of them, visible gaps, one
  set of facts across documents, prose written whole, rounds, a panel after every change, the
  person's standing decisions) and defers to resume-craft for the words in place of repeating
  them. Its cross-stage rules are grouped under truth, the person decides, and the work.
- Contradictions removed from career-kit: "one résumé per target role" against asking the
  person; "never hand-edit an output" against writing each document whole; gaps "never in the
  document" against red placeholders; "no first-person pronouns on the résumé" in the LinkedIn
  reference; a skills line for search in the LinkedIn About.
- `references/documents.md` is rewritten around the builds and page checks, with the section
  and voice material left to resume-craft. The LinkedIn, interview, project-record and
  questions references are brought into line, and a few questions can now be asked in the
  conversation in place of a form.
- Every career-kit reference was then read line by line. `worked-example.md` is rewritten to
  tell the whole engagement, including the second day, when five assembled résumés that had
  passed every check were replaced by one written by hand; it no longer presents the variant
  build as the pattern. `evidence.md` is corrected where rows described superseded rules and
  gains five rows for the newer ones. `panels.md` is reordered and gains a section on putting
  your own recommendation to a panel; `questions-form.md` ties placeholders to questions;
  `website.md` says the site's copy is the same copy as the résumé's; `intake.md` records the
  person's standing decisions.
- `references/website.md`: the generated video hero section now opens with four things to
  settle before generating (replace or build on, placement and edges, the resting frame, the
  beats and pauses), and gains two parts from a character hero built on 21 November 2026: a
  character of the person (sheet first, model drift, grading the backdrop to the page colour)
  and clips that play as one take (join on a held pose, measure a skip, fit length in the
  script, a contact sheet is not a viewing). Five evidence rows record what each cost.
- Not re-run: the skill's evals. This release changes enough that they should be.

## 0.4.11

`career-kit:resume-craft`: where a role's measure of success goes.

- Feedback on one résumé asked for core responsibilities, success criteria and key
  achievements under every role. A five-lane panel chose none of the labelled-block options.
  `references/sections.md` now says: responsibilities are the scope line, achievements are the
  bullets, and what good looked like is a clause where the person's sources state a measure,
  with silence where they do not.
- Feedback that the achievements were lacklustre and should market the person without making
  anything up. `SKILL.md` and `references/voice.md` now say the résumé sells what is true:
  lead with what mattered, put the scale beside the action, say what was at stake, end on the
  effect, and let a supporting verb carry its own result, with the confirmed verb and figures
  unchanged. The lint warns `empty-sell` and `admin-ending`.
- Feedback that detail was reducing the apparent impact of the achievements. The skill now
  ranks detail: one headline and at most one supporting fact per bullet, with method, tools
  and process words going unless they are the point, and a term the person asked for moved or
  raised with them when it loses its place. The lint warns `headline-long` and `bullet-lists`,
  and `bullet-length` now starts at 60 words.
- The same feedback, applied more strictly to numbers: a figure stays only when it enlarges
  the reader's impression (a large scale, a result, an exact count of something hard). Ranges,
  small team sizes, durations, tallies of faults and a small figure beside a large one go. The
  lint warns `vague-range`.
- Not re-run: the skill's evals.

## 0.4.10

`career-kit:resume-craft`: a résumé that will be judged against a standard abides by it.

- `SKILL.md`: when a research digest, an employer's guide or a checklist is the measure, its
  structure and numbers are limits. They are met by moving material to the section it fits,
  departed from only on the person's instruction, and every remaining departure is listed
  with whose decision it was.
- `references/sections.md` states the research's shape for a role where the experience section
  is described.
- Missing information is now a placeholder in angle brackets where the answer will go
  ("for the `<Project Name>` project"), printed in red by `build_resume.py` and `make_docx.py`.
  Enriching questions get one too. The lint treats a placeholder as an error unless
  `--allow-gaps` is given. Square brackets are still recognised.
- Not re-run: the skill's evals.

## 0.4.9

`career-kit:resume-craft`: a bare fact is a question to ask.

- An award line went through four wordings, each a way of saying the award was received, and
  nobody asked what it was for. `SKILL.md` now says to write what is known and ask for the
  rest: what an award recognised, what a move added, what changed under their leadership.
  These enriching questions are separate from gaps, never appear as brackets, and go in the
  reply, most valuable first.
- `references/voice.md`: the question to ask for each kind of bare fact.
- `scripts/resume_lint.py` warns `award-bare` when an award is named without what it was for,
  with a self-test.
- A role paragraph glossed a product every reader knows, to carry an ad's keyword. The skill
  now says to explain only what this reader would not know, and `references/voice.md` has a
  table of words that tell the reader nothing. The lint warns `gloss-known`.
- A sentence about a tool read as the tool checking its own work. The skill now says each
  sentence has one reading, with a table of the usual traps in `references/voice.md`, and the
  lint warns `two-readings` on "use X to …, and [check]".
- The experience section's structure is held more firmly. When a scope line overflows, the
  extra moves to a bullet or the tools line before any default gives way, and every bullet
  ends on what was different afterwards or on its scale. The lint warns `bullet-no-result`.
- Not re-run: the skill's evals.

## 0.4.8

`career-kit:resume-craft`: what an answer implies, and sounding like the person.

- An award the person had listed as theirs was written as a bare fact about a project, because
  their place on the team was treated as unconfirmed. They called it impersonal and rigid, and
  asked whether they would have mentioned the award if it were not theirs. `SKILL.md` now says
  caution never withholds what the person has already told you: a volunteered fact carries its
  plain implication, and only what would take a second fact to know is asked about.
- `references/voice.md`: a table of what common answers do and do not imply, and a section on
  sounding like the person: one sentence of stake, reason or judgement per prose section, tied
  to something specific, with "our" for what a team did.
- `scripts/resume_lint.py` warns `impersonal-prose` on a sentence in the employer or role
  paragraphs that has no first person in it.
- Not re-run: the skill's evals.

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
