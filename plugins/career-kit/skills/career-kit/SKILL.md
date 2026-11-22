---
name: career-kit
description: >-
  Take one person from "I need a new résumé" to a complete application kit: research on their
  country, industry and target employers, a cited review of their current résumé and LinkedIn,
  a résumé for the roles they want (one, or one per role family) as HTML, PDF, Word and a
  Google Doc, paste-ready LinkedIn copy, a personal website, an interview guide, and a project
  record a later session can pick up. Use when someone wants help with a résumé, CV (curriculum
  vitae), job application, LinkedIn profile, interview preparation, or a personal site to apply
  with — "update my résumé", "I'm applying for these roles", "rewrite my LinkedIn", "help me
  prepare for this interview", "tailor my CV to this job ad", "what's wrong with my résumé".
  It decides what it can with a model panel and asks the person the rest, through a form with
  suggested defaults and tap-to-fill examples or a few multiple-choice questions in chat. It
  works in rounds, a model panel reads the copy again after every change, and every figure in
  every output traces to something the person confirmed. Not for writing marketing or brand
  content in a named person's voice (use that person's content skill), and not for reviewing a
  UI (design-review:design-review).
---

# career-kit

A résumé is an evidence problem and a writing problem, and each hides the other. The evidence
faults are a figure nobody confirmed, a verb that drifted a grade upward, several documents
that disagree about one date, and a page that silently lost its last two bullets. The writing
faults survive every check for those: copy that is true, consistent and matched to the ad, and
that no reader would finish. This skill runs the engagement so that both kinds get caught.

`career-kit:resume-craft` holds the rules for the words: what each section is for, the voice,
how to suit a document to a role, and how to apply a correction without over-correcting. This
skill holds everything around the words: the research, the facts, the questions, the builds,
the reviews and the record. Use the two together.

## How the work runs

**Research is the base.** The structure and conventions of every document come from research
on the person's country, industry and target employers, gathered in stage 2. Where a document
will be judged against that research, its limits are limits: meet them, and list any
departure with whose decision it was.

**Only confirmed facts, and all of them.** Nothing enters a document that the person has not
said. A background check and an interview test every number, so an invented or rounded-up
figure costs more than an admitted gap. What a person wrote about their own work, in an old
résumé or a profile, is evidence of that work, and a fact they volunteer carries its plain
implication. `scripts/facts_lint.py` fails any output carrying a figure absent from the
confirmed-facts file.

**Missing information is visible.** Where an answer is missing, the draft carries a
placeholder in angle brackets where the answer will go, such as `<what the award recognised>`.
The builders print it in red. A draft with placeholders goes to the person and never to an
employer.

**One set of facts, many documents.** The résumé, the LinkedIn copy, the website and the
interview guide state the same titles, dates and figures. When a fact changes in one, check
every other document for it in the same sitting, and say which you changed and which you left.

**Facts are shared; prose is written.** Scripts render and check. They do not compose. Write
each document out whole and read it whole; a document assembled from stored sentences is one
that nobody, the author included, has read.

**It runs in rounds.** Answers change the facts, the documents are rewritten, a panel reviews
what changed, and the review usually produces a shorter set of new questions. Tell the person
at the start that two or three rounds is normal and each is shorter than the last. A later
round quotes their earlier answers back to confirm or correct, and asks nothing already
settled.

**A panel reads the copy after any change.** Copy that passed review and was then edited has
not passed review. Scope the panel to what changed, give it the whole fact base, and say in
the report which version it read. Stage 8 has the detail.

**The person's decisions stand.** Keep a list of what they have decided: a term to use,
wording they approved or rejected, what stays off public copies. The latest instruction is not
the only one; check the list after every revision.

Work through the ten stages in order. Stages 5 to 9 can be reordered to what the person needs
first, but none starts before stage 1 has read their documents and stage 2 has the research.

## 1. Gather context about the person

Ask for, and read in full before asking a single question: their LinkedIn profile PDF export,
their current résumé, every job description they are targeting, and anything else that
describes their work, such as position descriptions, performance reviews and an email
signature.

Read first, then ask. Most of the first interview's answers are in those files. Keep drawing
on them all the way through: a review of the old résumé's faults is not a reason to stop
using what it says about the work.

Record what you learn in a facts file, marking each item as confirmed by the person, taken
from a document, or inferred. An inferred date is a question for stage 4.

Depth: `references/intake.md`.

## 2. Gather the right research

Four subjects, each of which changes the documents: résumé conventions in the person's
country; conventions in their industry; the specific target employers (which applicant
tracking system each runs, the vocabulary in their current ads, how they interview, their
stated values); and how automated screening works now.

Run three or more independent research lanes and reconcile them into one digest where every
claim carries the lanes that support it. Check anything the lanes disagree on directly
against the primary source: a careers site fetched with `curl` settles a disagreement that two
reports will argue about indefinitely.

Depth, including the lane-by-lane procedure and what each one costs: `references/research.md`.

## 3. Review what they have now

Build one self-contained HTML page. Every finding carries four things: a real cropped image
from their own document with the quoted words highlighted, a sketch of the layout being
described, why it matters with a citation to the research digest, and what to do about it.
A finding above a crop of their actual page is checkable by someone who has not opened the
file.

```bash
pdftoppm -r 150 -png source/resume.pdf review/img/resume     # page images first
python3 scripts/crop_snippets.py --pdf source/resume.pdf --spec snippets.json --out review/img/
```

Read their résumé through `pdftotext` without `-layout` as well as with it. Without it you see
roughly what a parser sees, and a two-column design that reads correctly to a person comes out
interleaved.

Depth: `references/review-page.md`.

## 4. Decide what can be decided, then ask well about the rest

Decide first. Put real choices between wordings, structures or inclusions to
`decision-panel:decision-panel`, and record each panel's brief and every lane's answer under
`decisions/`.

Then ask the person only what no model can answer: facts about their work, what they are
comfortable publishing, which roles they want. Match the instrument to the number of
questions:

- **More than about five: one HTML form**, generated by `scripts/build_form.py`. Multiple
  choice where the answer is a choice, with a suggested default marked and sourced; free-text
  fields with three to five tap-to-fill examples; answers saved in the browser with Copy and
  Download.
- **Five or fewer: multiple-choice questions in the conversation**, each with a free-text
  option, where the runtime offers a question tool. Quote the line each answer will complete.

```bash
python3 scripts/build_form.py --spec questions.json --out questions.html \
    --title "Jane Doe — résumé questions" --key jane-resume-v1
```

When the person sends free-text feedback, check your reading before rewriting anything: one
question per note, quoting it, with your readings as options to tap and nothing pre-selected.
Put the general rules you drew from it back to them as a tick list. `references/questions-form.md`
has the shape.

An example the person selects and leaves unchanged is their answer. A suggested default they
never touched is weaker: before printing a figure or an outcome that rests on one, ask. When a
ticked option and the note beside it disagree, ask one follow-up instead of choosing a
reading. Ask what each bare fact was for (what an award recognised, what changed under their
leadership); the answer is often the best line in the document.

Depth, including how to write an example that is safe to select:
`references/questions-form.md`.

## 5. Write the résumé

Use `career-kit:resume-craft` for the words, and its lint
(`../resume-craft/scripts/resume_lint.py`) for structure and voice. This stage owns the facts
file, the keep list, the builds and the page checks.

Ask the person whether they want one résumé or one per role family. One is simpler to keep
true and to send, and a panel can say which roles it cannot serve. Write the terms the person
asked for, and each required phrase of the ads that they hold, one per line in a keep file,
and run the lint with `--keep` after every edit.

```bash
python3 -m http.server 8942 --bind 127.0.0.1 --directory rewrite &   # the PDF step loads over HTTP
python3 scripts/build_resume.py resume.md resume.html "Footer title"
# print resume.html to PDF with headless Chrome, then:
/tmp/dv/bin/python scripts/make_docx.py resume.md resume.docx
```

`scripts/make_variants.py` builds a version per role family from one facts file for a person
who wants several. Treat its output as a draft to read and rewrite whole.

After each build, look at the page images. A page count says nothing about a second page that
is half empty, a role line that has wrapped, or a font that fell back. Upload the Word file to
application portals, which parse it, and send the PDF to people. A Google Doc version has not
been built by this skill in practice: check which document connector the runtime offers,
create the document from the same Markdown, and say that the step has no prior run behind it.

Depth, including the Markdown subset, fonts and page checks: `references/documents.md`.

## 6. Write the LinkedIn copy

Every section in LinkedIn's own order, paste-ready: headline, About, each role entry, skills,
settings to change, entries to delete, and what must stay off a public profile. Titles,
employer and dates match the résumé exactly. The role descriptions follow resume-craft's
writing rules and the public copy's restrictions. LinkedIn's Skills section is its search
index and takes its standard terms; the About section carries none.

Depth: `references/linkedin.md`.

## 7. Build the personal website

Reference shipped design work, build with `design-craft:design-craft` and `ux-craft:ux-craft`,
and use an image or video tool for imagery. Every sentence on the site is copy about the
person and follows the same facts and writing rules as the résumé.

Show any effect cheaply before building it into the page, keep the plain version buildable,
and offer it again after two iterations. A control that lets the person compare options is a
review tool: serve it locally and remove it before any deploy. Each effect needs a real path
for someone without WebGL, with reduced motion, or on a touch device.

```bash
node scripts/shoot.mjs http://127.0.0.1:8943/ 390 844 /tmp/site top=0 work=sel:#work
```

Deploy only when the person says so, and tell them that an unlisted address with a `noindex`
header is still public. Before the site's address goes on a résumé, check every other path on
that domain. A custom domain and a generated video each have a procedure in the reference.

Depth: `references/website.md`.

## 8. Review the content with a panel, after every change

A request to review is a review: report findings with proposed wording and edit nothing until
the person says to apply them.

Ask for a cold read first, before any rule: "read it as the hiring manager would and quote
every sentence you stumbled on, with the reason". Then ask what is missing from the person's
career, whether each section does its job, and whether anything goes beyond the facts. Give
each lane every source, including the person's original documents, and tell it only the
person's decisions are settled; your own style defaults are open to challenge. Read the
reviewers' reasons yourself before rewriting anything they flag.

```bash
scripts/run_panel.sh --brief brief.md --brief-reversed brief-b.md \
    --out decisions/sections-panel --add-dir /path/to/project --min-bytes 600
```

Half the lanes read the options in the opposite order. An empty or truncated answer is a lane
failure, never a dissent. A lane that has gone quiet may still be running: wait for it to end
before recording a failure, and treat the result as interim until every lane has settled. Act
on majority agreement; the person's own decisions outrank every reviewer. Stop when the
remaining edits are the panel's own wording.

Once a round of the person's corrections is in, ask which other lines do not represent their
work. For the lines they flag, recommend wording grounded in the research on how hiring
managers read (stage 2), with the source beside each suggestion. The person asked for this
step in the source session; a panel's taste is not a reason to change their words.

Depth, including how to write a brief and how to tally: `references/panels.md`.

## 9. Research and write the interview guide

How this employer interviews (stages, format, stated values), researched and cited. Then the
person's stories with the facts attached to each, likely questions per role with example
answers built only from confirmed facts, the hard questions they should expect, and a practice
plan. The guide is where an example cut from the résumé for space can live.

Depth: `references/interview.md`.

## 10. Leave a project record

A `CLAUDE.md` with the working rules, and a notes file with the confirmed facts, each round of
answers, every decision and its basis, the corrections in the person's own words, the keep
list, what is still unconfirmed, and how the tools behaved. Written so a later session
continues without the person answering anything twice.

Depth: `references/project-record.md`.

## Rules that hold across every stage

**Truth**

- State scope exactly, and check four kinds of drift by name: a stronger verb than the person
  confirmed, an expected outcome written as achieved, a figure whose noun changed, and one
  piece of work counted more than once. `facts_lint.py` catches only figures.
- Ask which figures may appear publicly and keep a softened public copy. Check every public
  surface for restricted figures after each build, in rendered text and not in page source.
- Strip contact details before sending any text to an outside model.

**The person decides**

- Publish nothing and send nothing on their behalf without them saying so: a deployment, a
  purchase, a profile edit, a commit.
- Answer a question before acting on it. "Do you see how this sounds odd?" and "before you
  change anything, explain why" ask for an answer. Give the real cause, including a brief or
  a check of your own that produced the problem, and change nothing until asked.
- When they correct something, find the rule behind the fault and apply it to every section
  and every document, and say what you kept as well as what you changed. Put the rule back to
  them to confirm: a rule they confirm is a standing decision, and one they leave unconfirmed
  is your reading, not theirs.

**The work**

- Look at what you built: page images, screenshots, the live address after a deploy. Say which
  surfaces you looked at and which you did not.
- Distrust a phrase that has survived many drafts, and a check that cannot fail.
- Keep a short list of what is waiting on whom, and repeat it at the end of each report.
- Start long jobs in the background, carry on with work that does not depend on them, and
  queue a new instruction against work that is in flight.
- Route status and long outputs to files. Chat replies stay at two to four lines with a path.

## Scripts

| Script | What it does |
| --- | --- |
| `scripts/build_resume.py` | Markdown subset to print HTML, pages breaking automatically, placeholders in red |
| `scripts/make_docx.py` | Styled Word file matching the PDF; needs `python-docx` |
| `scripts/make_variants.py` | One facts file plus a variant spec to a draft per role family, with page counts |
| `scripts/facts_lint.py` | Gate: every figure in an output traces to the confirmed-facts file |
| `scripts/build_form.py` | The question page: defaults, sources, tap-to-fill examples, copy and download |
| `scripts/crop_snippets.py` | Evidence crops from a source PDF with highlighter marks baked in |
| `scripts/run_panel.sh` | Review panel with reversed-order briefs, wrapping decision-panel's runner |
| `scripts/shoot.mjs` | Chrome over CDP: scrolled screenshots, overflow check, console errors |
| `scripts/mcp_call.py` | Call one router MCP tool over HTTP when the session's own link has dropped |

## Delegation

Do the reading, judging and writing yourself. Use a subagent for mechanics that are separable
and more than a handful of tool calls: running a panel, building the website while a panel
runs, reading a long transcript. Cap it at three. Give each one the artefact paths by absolute
path and the person's decisions, and ask for reviewers' reasons quoted in full, because a
summary of a finding is how the wrong fault gets fixed.

## Length

Chat replies while this runs: two to four lines plus a path. The résumé is two pages unless
the person's market says otherwise. The interview guide runs to what its questions need.
Written deliverables carry no summary section restating what they just said.
