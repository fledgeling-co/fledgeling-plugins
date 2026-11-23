# Panels — reviewing copy with several model families

## When a panel runs

Two occasions. A real choice between wordings or structures goes to a panel as a decision. And
every change to copy a reader will see is reviewed by a panel before that copy is called final,
deployed or handed over: answers incorporated, suggestions applied, cuts made for length, a new
caption on the website. Copy that passed a review and was then edited has not been reviewed.

A round takes fifteen to twenty-five minutes and five model calls, so scope it. For a small
change, point the lanes at the changed sections and the artefacts that share the changed facts.
Batch edits made close together into one round. Run the full section-by-section review when
a whole document changed, and once over everything before hand-over. Say in the report which
version each round read.

Typo fixes and layout changes that alter no wording do not need a round.

## Review is not apply

When the person asks for a review, return findings and proposed wording and change no source.
Applying them is a second step that the person starts. Keep the lanes read-only for the same
reason.

## Ask for a reading before a ruling

The source session's panels passed copy that read badly, three times, because of how they were
asked.

- A brief that asks "are tense and person consistent?" gets consistency. Subject-dropped
  present-tense verbs are consistent and read as commands. Ask first: "quote every sentence you
  stumbled on, had to re-read, or that sounded like a job ad, and say why."
- Do not pass your own style rule to the panel as settled. "No first person" went into a brief
  as a rule, the one lane that proposed first-person summaries was overruled twice by it, and
  the person later asked for exactly that.
- Ask what is missing. Reviewers judge what is on the page unless asked what is not.
- Give each section's job and test (`career-kit:resume-craft`, "The document, top to bottom")
  and ask whether the section does it.
- Give the lanes every source, including the person's original documents. Four lanes flagged
  "managed supplier relationships" as beyond the answers; it was in the old résumé, which they
  had not been given.
- When placement matters, give the page-by-page text of the built PDF. Lanes reading Markdown
  guess where page 1 ends.

## The brief

Write it to a file and keep the file. Never type it inline at the call site: the brief is the
evidence for the decision, and `decisions/<topic>/brief.md` beside the five answers is what
makes a decision auditable six weeks later.

A brief that works has six parts:

1. **The reviewer's role**, and this instruction: *"Do not hedge toward a consensus you cannot
   see."* Lanes that are told they are one of five will otherwise write toward an imagined
   middle.
2. **Absolute paths to every artefact**, with `--add-dir` for each directory, rather than
   pasted content. The lanes read the real files and the brief stays short enough that its
   instructions stay in view.
3. **The person's rules and the whole fact base**, stated as rules: what counts as a confirmed
   fact, which verbs are fixed, what may not appear publicly, and the paths to every answers file
   and the notes. A reviewer without the facts flags true statements: one lane proposed deleting
   a figure as unsourced when it was confirmed in notes it had not been given. Name what is
   settled and not open for debate, or lanes spend their words re-arguing it.
4. **The candidate options**, lettered.
5. **An exact return shape** — `VERDICT: <letter>`, then fixed headings; or per-section
   `S1: KEEP | CHANGE | REPLACE | REMOVE — why — exact replacement wording`.
6. **A word budget**, 250–450 for a single decision.

For a content review, also give the word count of every section against its limit from the
research, and ask by name for the four kinds of drift a figure check cannot see: a stronger verb
than the person confirmed, an expected outcome written as achieved, a figure whose noun changed,
and one piece of work counted in several bullets. Ask whether each requirement of each ad that the person holds
is shown in a sentence, in the ad's own words, and whether the document is weighted to the role as
well as worded for it. After a round of answers, ask whether each answer was incorporated with nothing stated beyond
it.

Strip the person's contact details from anything the brief points at. These are other vendors'
models.

## Putting your own recommendation to the panel

When the person asks for your view to go with the question, state it in the brief with its
reasons, and tell the lanes to challenge it and not defer to it. Ask each lane for the
strongest argument against its own verdict as well. On one structural decision the two
dissenting lanes each named the same narrower option as the best case against themselves, and
that option, which all five could accept, was the decision.

Tell the lanes who gave any feedback being judged, where that is known. Feedback from the
person who will read the document is evidence about the reader, and outweighs a general
finding.

## Order bias

Write the brief twice, with the options in opposite orders, and split the lanes between them:

```bash
scripts/run_panel.sh --brief brief.md --brief-reversed brief-b.md \
    --out decisions/photo-panel --add-dir /path/to/project --min-bytes 600
```

A verdict that is really a preference for the first option listed then shows as a split instead
of a consensus. Five lanes reading one ordering is one experiment run five times.

## A failed lane is not a vote

`--min-bytes` catches an answer that stopped early; an empty or missing `.md` is a lane
failure whatever the exit code says, and each lane's `.log` says why. In the source session one
lane returned an empty file after a headless permission denial, and counting it as a verdict
would have turned a tool failure into a silent "no".

Report it as a failure, and tally the lanes that answered.

A lane can also fail for the account rather than the run. On 24 November 2026 one lane returned
HTTP 403, "This service has been disabled in this account for violation of Terms of Service",
on two consecutive runs, and another reported a usage limit with its reset date. Re-run once;
when the error names the account, tell the person in one line, because no retry fixes it and the
next panel will meet it too.

## A quiet lane is not yet a failed lane

One lane in the source session stopped after a one-line preamble, was recorded as failed and
retried, and then both runs returned complete answers twenty minutes after the synthesis had been
reported. That lane alone found three grounding errors the other four had missed. The synthesis
was corrected twice and every vote fraction restated.

- Decide a lane's state from outside it: is its process alive, is its file still growing.
- Start no retry while the first run is live.
- Call the result interim until every lane has answered or ended, and derive nothing from an
  interim result — no question form, no applied change.
- A late answer reopens the synthesis. Recount, correct the findings file throughout, and tell
  the person what changed.
- Two answers from one lane are one vote. Keep both files.

Expect the slowest lane to take about twice as long as the others, and set its timeout from that.

## Read the reasons yourself

A synthesis that says "five lanes stumbled on this sentence" does not say which words. In the
source session that sentence was rewritten for the wrong fault and the odd phrase in it
("teams of 5 and about 15") survived two rounds until the person read it aloud. When you
delegate a panel run, ask for the lanes' reasons quoted, and read them before editing.

## Acting on the result

- Apply a change when two or more reviewers ask for it, or when one demonstrates a
  contradiction with the person's confirmed facts.
- Do not apply a single reviewer's preference that other reviewers disagreed with.
- The person's own rules outrank every reviewer. Where a panel wants wording the person has
  ruled out, record the panel's position and keep the person's.
- Log what you declined and why, in the project notes. A declined finding that leaves no trace
  gets re-raised by the next panel.

## Several small decisions in one run

When the decision is twenty linked small ones on one evidence base, such as which answer to
recommend on each question of a form, one brief with a table to fill per item, tallied by hand,
served better than twenty runs: three lanes agreed on 18 of 22 items and split 2 to 1 on the
rest, so no second round was needed. Number the items exactly as the artefact numbers them. One
brief called the summary question 19 when the form had it at 16, and every lane had to correct
it.

## Send the proposals, not only the edits

A review's proposed wording reaches the person as soon as it is on a page or a form, so it gets
the panel's drift check before then. In the source session two proposed lines went onto a
published review page and a live form with drift from the person's confirmed words: a purpose
she had worded herself replaced with one she had rejected, and two phrases she had confirmed
separately merged into one. Only the panel run on the form caught them.

## When to stop

Stop when the remaining edits are the panel's own wording, or when a round raises only points
the person has settled. A further round then mostly re-argues decisions.

## Two mechanical cautions

A panel is only as current as the copy it read. An answer that arrives after the artefact has
changed reviews a document that no longer exists — re-run rather than applying it.

Not every lane is read-only. Where a lane has write tools and the brief names a project path,
check the project's files after the panel: the source session found one file changed that
nobody in the session had edited. Prefer lanes configured read-only, and diff afterwards.

