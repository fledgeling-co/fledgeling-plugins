---
name: career-kit
description: >-
  Take one person from "I need a new résumé" to a complete, role-targeted application kit:
  country and employer research, a cited review of their current résumé and LinkedIn, one
  résumé per target role built from one source of facts as HTML, PDF (A4 paper size), Word and
  a Google Doc, paste-ready LinkedIn copy, a personal website, an interview guide, and a project record
  a later session can pick up. Use when someone wants help with a résumé, CV (curriculum vitae), job application,
  LinkedIn profile, cover letter, interview preparation, or a personal site to apply with —
  "update my résumé", "I'm applying for these roles", "rewrite my LinkedIn", "help me prepare
  for this interview", "tailor my CV to this job ad", "what's wrong with my résumé". It decides
  what it can decide with a model panel and asks the person the rest through one HTML form with
  suggested defaults and tap-to-fill examples, rather than leaving gaps in the document or
  filling them with plausible text. It works in rounds, and a model panel reviews the copy again
  after every change. Each figure in each output traces to something the person confirmed. Not for writing marketing or brand content in a named person's voice (use that
  person's content skill), and not for reviewing a UI (design-review:design-review).
---

# career-kit

A résumé is an evidence problem wearing a writing problem's clothes. Most of what goes wrong
is not prose: it is a figure nobody confirmed, a verb that drifted a grade upward, five
documents that disagree about one date, and a page that silently lost its last two bullets.
This skill exists to make those four things hard.

It is still a piece of writing, and the checks that catch those four things do not tell you
whether it reads well. The source session passed every fact, figure and consistency check on
copy that read as a list of commands, stored ad keywords in a section called "skills", and
summed up eighteen years with one minor task. A person caught each of those by reading. So
read the whole document as its reader would, before and after every change, and ask reviewers
to do the same before they check any rule.

Two commitments shape everything below.

**Nothing enters a document that the person has not confirmed.** A gap goes back to them
through a form, not into the page as plausible text. An internal panel and a background check
test every number, so an invented or rounded-up figure costs the person more than an admitted
gap. `scripts/facts_lint.py` is the gate: it fails any output carrying a figure absent from
the confirmed-facts file.

**One source of facts, many outputs.** The résumé, the website, the LinkedIn document and the
interview guide state the same titles, dates and figures, held in one facts file. A hand edit
in one place is how two documents come to state different dates for the same role.

**Facts are shared; prose is written.** Scripts render and check; they do not compose. The
source session assembled five résumés from sentence fragments in a build script, and nobody,
the author included, was reading any one of them as a document. Write each document out whole,
by hand, and let the scripts turn it into PDF and Word.

**Expect rounds.** The stages below read as a line and the work runs as a loop: answers change the
facts, the documents rebuild, a panel reviews what changed, and the review usually produces a
shorter set of new questions. The source session ran three question forms, and the third came
from a panel reading résumés that had already been called finished. Tell the person at the start
that two or three rounds is normal and that each is shorter than the last, so a second form reads
as progress. A later round quotes the person's earlier answers back to confirm or correct, and
asks nothing an earlier round settled.

**A panel reviews the copy after any change.** Whenever text a reader will see changes — new
answers incorporated, a suggestion applied, a cut made to fit the page, a new caption on the
website — run a panel over the changed artefacts before calling them final, deploying them or
handing them over (stage 8). Copy that passed review and was then edited has not passed review.
In the source session the résumés were reviewed and corrected twice, and a third panel still found
a forecast printed as a result and a count of users printed as a count of staff. Scope the panel
to what changed, give it the full fact base, and say in the report which version was reviewed.

Work through the ten stages in order. Stages 5 to 9 can be reordered to what the person needs
first, but none of them starts before stage 1 has read their documents and stage 2 has the
research.

## 1. Gather context about the person

Ask for, and read in full before asking a single question: their LinkedIn profile PDF export,
their current résumé, every job description they are targeting, and anything else that
describes their work — position descriptions, performance reviews, an email signature.

Read first, then ask. Most of the first interview's answers are in those files, and a question
whose answer was in the document they just sent reads as not having opened it.

Keep drawing on those documents all the way through. What the person wrote about their own
work is a source for that work, even where a figure in it still needs confirming. The source
session reviewed the old résumé for its faults and from then on used it only for dates, so the
drafts were built from form answers alone and carried whatever the forms happened to ask about.

Record what you learn in a facts file (stage 10's `PROJECT-NOTES.md`), marking each item as
confirmed by the person, taken from a document, or inferred. An inferred date is a question for
stage 4, not a fact.

Depth: `references/intake.md`.

## 2. Gather the right research

Four subjects, each of which changes the document: résumé conventions in the person's country;
conventions in their industry; the specific target employers — which applicant tracking system (ATS)
each of them runs, the vocabulary in their current ads, how they interview, their stated values; and
how automated screening actually works in 2026.

Run three or more independent research lanes and reconcile them into one digest where every
claim carries the lanes that support it. Check anything the lanes disagree on directly against the
primary source — a careers site fetched with `curl` settles an ATS disagreement that two
reports will argue about indefinitely.

Depth, including the lane-by-lane procedure and what each one costs: `references/research.md`.

## 3. Review what they have now

Build one self-contained HTML page. Every finding carries four things: a real cropped image
snippet from their own document with the quoted words highlighted, a sketch of the layout
being described, why it matters with a citation to the research digest, and what to do about
it.

The snippet is the point. A finding that says "the contact line is below the fold" is an
assertion; the same finding above a crop of their actual contact line is checkable by someone
who has not opened the PDF.

```bash
pdftoppm -r 150 -png source/resume.pdf review/img/resume     # page images first
python3 scripts/crop_snippets.py --pdf source/resume.pdf --spec snippets.json --out review/img/
```

Read their résumé through `pdftotext` **without** `-layout` as well as with it. Without it you
see roughly what a parser sees, and a two-column design that reads correctly to a person comes
out interleaved.

Depth: `references/review-page.md`.

## 4. Decide what can be decided, then ask well about the rest

Decide first. Put real choices between wordings, structures or inclusions to
`decision-panel:decision-panel` — photo or no photo, which of three phrasings, whether a
section earns its place. Record each panel's brief and every lane's answer under `decisions/`.

Then ask the person only what no model can answer: facts about their work, what they are
comfortable publishing, which roles they actually want. One HTML page, generated by
`scripts/build_form.py`:

```bash
python3 scripts/build_form.py --spec questions.json --out questions.html \
    --title "Jane Doe — résumé questions" --key jane-resume-v1
```

Multiple choice where the answer is a choice, with a suggested default marked and sourced.
Free-text fields with three to five tap-to-fill example answers underneath, drawn from what
their documents already suggest. Answers saved in the browser, with Copy and Download buttons.

**An example the person taps and leaves unchanged is their answer.** The form marks it
`[example text, unchanged]` so you can see which answers were selected, not so you can discount
them. In the source session fifteen answers came back as unchanged examples, were treated as
unverified, and the person's own words overturned that. Ask before assuming.

The form counts questions the person has looked at, and exports an untouched suggested default as
`[suggested default, not touched]`. Treat that as weaker than a confirmation: before printing a
figure or an outcome that rests on one, ask. When a ticked option and the note beside it disagree,
ask one follow-up instead of choosing a reading.

Depth, including how to write an example that is safe to select: `references/questions-form.md`.

## 5. Write the résumé

Use `career-kit:resume-craft` for the words: it holds what each section is for, the structure,
the voice, how to suit the document to an ad, and a lint for structure and voice
(`../resume-craft/scripts/resume_lint.py`). This stage owns the facts file, the builds and the
page checks around it.

Before drafting, write down what each section is for and one test for it, from the research
and the person's situation: `references/documents.md` has a set to start from. A summary fails
if it could sit on someone else's résumé. A skill is something the person can do, with a line
below that shows it; a noun they work with is not one.

Write the document out whole. Ask the person whether they want one résumé or one per role
family; one is simpler to keep true and to send, and a panel can say which roles it cannot
serve. Suit it to the roles without writing for a keyword search: a required phrase goes where
it is true and natural, once, in context, and nothing goes in only because an ad uses the word.

Give it one voice and hold it: paragraphs in the first person, bullets opening with a
past-tense verb. A bare present-tense verb at the start of a line ("Lead discovery…") reads as
a command or as a misspelt "Led", and next to past-tense bullets it looks like the tense keeps
changing.

The variant builder below remains for a person who wants a version per role family. Treat its
output as a draft to read and rewrite, not as the finished text.

```bash
python3 -m http.server 8942 --bind 127.0.0.1 --directory rewrite &   # the PDF step loads over HTTP
python3 scripts/make_variants.py --facts facts.md --spec variants.json --out roles/ \
    --name "Jane Doe" --serve-url http://127.0.0.1:8942/roles --docx-python /tmp/dv/bin/python
```

That writes `.md`, `.html`, `.pdf` and `.docx` per role, prints each page count, and exits
non-zero when a variant is over its page limit. Pages break automatically; no container has a
fixed height. Set a word budget per section from the research before drafting and count against
it; resolve an overflow by cutting ranked content, never by shrinking type. Check each ad's
required phrases as exact strings, including the hyphenated and unhyphenated forms. Upload the `.docx` to portals, which parse it, and send the PDF to people.

A Google Doc version was asked for in the source session and never built, so this step is
designed rather than proven: check which document connector the runtime offers
(`anthropic-skills:google-workspace` when it is installed, or a Google Drive MCP server), and
create the document from the same Markdown. Say plainly which route you used and that this step
has no prior run behind it.

Depth, including the Markdown subset and what to check in the rendered pages:
`references/documents.md`.

## 6. Write the LinkedIn copy

Every section in LinkedIn's own order, paste-ready: headline, About, each role entry, skills,
settings to change, entries to delete, which skills to pin, and what must stay off a public
profile. Titles, employer and dates match the résumé exactly, because a recruiter comparing the
two is checking for that.

Depth: `references/linkedin.md`.

## 7. Build the personal website

Reference the real design corpus rather than inventing a layout: Mobbin for shipped patterns,
`design-craft:design-craft` and `ux-craft:ux-craft` for the build, and an image tool for any
imagery, captioned as generated. GSAP and three.js where they carry meaning and not otherwise.

Each effect needs a path for someone without WebGL, with `prefers-reduced-motion`, or on a
touch device — a real control that swaps the content, not a silently missing feature.

Show an effect cheaply before building it into the page, keep the plain version buildable, and
stop after two iterations to offer the plain version again. A control that lets the person compare
options is a review tool: serve it locally and remove it before any deploy.

Check it with a real browser at desktop and phone widths, capturing scrolled states:

```bash
node scripts/shoot.mjs http://127.0.0.1:8943/ 390 844 /tmp/site top=0 work=sel:#work
```

It prints `scrollWidth` against `innerWidth`, which is the horizontal-overflow check, and any
console error. Deploy only when the person says so, and tell them that an unlisted address with
a `noindex` header is still public. A custom domain has its own procedure, with checks to run
before offering to buy one, in the same reference.

Depth: `references/website.md`.

## 8. Review the content with a panel, after every change

This stage runs every time the copy changes, as the opening of this file says, and once more
over everything before hand-over. A request to review is a review: report findings with proposed
wording and edit nothing until the person says to apply them.

Ask for a cold read first, before any rule: "read it as the hiring manager would and quote
every sentence you stumbled on, with the reason". Then ask what is missing from the person's
career, and whether each section does the job written for it. Read the reviewers' reasons
yourself before rewriting anything they flag.

Give each lane the artefact paths, the confirmed-facts files, the person's original documents
and the person's own rules, and then ask for: a verdict per section with exact replacement wording; an overclaim check against the
confirmed facts; whether length and weighting suit each target ad, with word counts per section
supplied; and — after a round of answers — whether each answer was incorporated accurately, with
nothing stated beyond what the person said.

```bash
scripts/run_panel.sh --brief brief.md --brief-reversed brief-b.md \
    --out decisions/sections-panel --add-dir /path/to/project --min-bytes 600
```

Half the lanes read the options in the opposite order, so a verdict that is really a
first-position preference shows as a split. An empty or truncated answer file is a lane
failure, never a dissent. A lane that has gone quiet may still be running: wait for it to end
before recording a failure or starting a retry, and treat the result as interim until every lane
has settled. Act on majority agreement; a single reviewer's preference against
others' disagreement is not a finding. The person's own rules outrank every reviewer.

Depth, including how to write a brief and how to tally: `references/panels.md`.

## 9. Research and write the interview guide

How this employer interviews — stages, format, their stated values — researched rather than
assumed. Then the person's stories with the facts attached to each, likely questions per role
with example answers built only from confirmed facts, the hard questions they should expect,
and a practice plan.

Depth: `references/interview.md`.

## 10. Leave a project record

`CLAUDE.md` with the working rules, and a notes file with the confirmed facts, every decision
and its basis, the pushback and corrections in the person's own words, what is still
unconfirmed, and how the tools behaved. Written so a later session continues without the person
answering anything twice.

Depth: `references/project-record.md`.

## Rules that hold across every stage

- **State scope exactly.** An internal reader knows the truth. Reviewers in the source session
  repeatedly caught verbs that had drifted upward: "shipped" where the person supported, "runs"
  where they coordinate, "owns the squad's backlog" where they own one backlog in the squad.
  Run `scripts/facts_lint.py --verbs verbs.json` to list candidates, and judge each one.
- **Ask which figures may appear publicly, and keep a softened public copy.** A figure that is
  fine on an internal application can breach a confidentiality rule on a public page.
- **Change a fact in one place and rebuild.** Never hand-edit a generated output.
- **Look at the rendered pages.** Read the PDF page images and the site screenshots, and say in
  the report which surfaces you looked at and which you did not.
- **Strip contact details before sending any text to an outside model.** Panel lanes are other
  vendors' models.
- **Publish nothing and send nothing on the person's behalf without them saying so**, including
  a deployment, a domain purchase and a LinkedIn edit.
- **Check four kinds of drift, not one.** A stronger verb than the person confirmed; an expected
  outcome written as achieved; a figure whose noun changed (users to staff); and one piece of work
  appearing in several bullets as if it were several. `facts_lint.py` catches none of the last
  three, so put them to the panel by name.
- **Answer a question before acting on it.** "Do you see how this sounds odd?" and "before you
  change anything, explain why" are requests for an answer. Give the real cause, including a
  brief or a check of your own that produced the problem, and change nothing until asked.
- **Distrust a phrase that has survived many drafts.** Familiarity reads as correctness. Re-read
  the oldest wording in the document as if it were new.
- **Do not cut to a word count.** A numeric target is met by deleting the connecting words and
  the one sentence with a person in it. Cut by reading, then look at how full the page is.
- **Keep a short list of what is waiting on whom** and repeat it at the end of each report. Three
  open decisions spread across a long conversation get lost; three lines do not.
- **Wait in the background and say what you are waiting for.** Panels and builds take ten to
  twenty-five minutes. Start them, carry on with work that does not depend on them, and report when
  they settle. When a new instruction arrives for work that is in flight, queue it against that
  work so it is neither lost nor applied halfway.
- **Route status and long outputs to files.** Chat replies stay at two to four lines with a path.

## Scripts

| Script | What it does |
| --- | --- |
| `scripts/build_resume.py` | Markdown subset to A4 print HTML, pages breaking automatically |
| `scripts/make_variants.py` | One facts file plus a variant spec to per-role `.md`/`.html`/`.pdf`/`.docx` with page counts |
| `scripts/make_docx.py` | Styled Word file matching the PDF; needs `python-docx` |
| `scripts/crop_snippets.py` | Evidence crops from a source PDF with highlighter marks baked in |
| `scripts/build_form.py` | The question page: defaults, sources, tap-to-fill examples, copy and download |
| `scripts/shoot.mjs` | Chrome over CDP: scrolled screenshots, overflow check, console errors |
| `scripts/run_panel.sh` | Review panel with reversed-order briefs, wrapping decision-panel's runner |
| `scripts/facts_lint.py` | Gate: every figure in an output traces to the confirmed-facts file |
| `scripts/mcp_call.py` | Call one router MCP tool over HTTP when the session's own link has dropped |

## Delegation

Use a subagent for a stage that is genuinely separable and more than a handful of tool calls —
building the website while the résumé panel runs, or reading a long transcript. Cap it at three
for this skill. Give each one the artefact paths and the person's rules, and name every file it
must read by absolute path: a subagent told to work "across the session" used its own context
until it was given the transcript paths and the command to render them. Give each one the rules; two or more agents
appending to one notes file each need to re-read it immediately before writing.

Do the rest yourself. A delegated agent pays for its own copy of the context, and this work is
mostly one artefact at a time.

## Length

Chat replies while this runs: two to four lines plus a path. The résumé is two A4 pages unless
the person's country and industry say otherwise. The interview guide runs to what its questions
need. Written deliverables carry no summary section restating what they just said.
