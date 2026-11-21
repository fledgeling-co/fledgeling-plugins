---
name: resume-craft
description: >-
  Knows what belongs in each section of a résumé or CV (curriculum vitae), how the document is structured, and the
  voice it is written in. Use it whenever someone is writing, rewriting, tailoring or reviewing a
  résumé — "write my professional summary", "what should go in key skills", "fix these bullets",
  "is this résumé any good", "tailor my CV to this job ad", "how do I lay out twenty years at
  one employer", "does this read like AI wrote it", "cut this to two pages" — and whenever
  another skill reaches the point of drafting or checking résumé copy. It drafts a section or a
  whole document from facts the person has confirmed, and it reviews an existing résumé section
  by section against the job each section has. Its defaults come from cited research on how
  résumés are screened in 2026 and from recorded corrections in a real engagement, and a bundled
  lint checks structure and voice mechanically. Not for the whole application kit (research,
  question form, PDF and Word builds, LinkedIn, website, interview guide: use
  `career-kit:career-kit`), and not for cover letters or LinkedIn copy.
---

# resume-craft

A résumé has two readers and one job. Software files it: it pulls the employer, title, dates
and skills into fields, and sometimes ranks it against the ad. A person then decides, usually
in under a minute, and the realistic way to lose is a recruiter who reads generic copy and
moves on. Six research reports on Australian bank hiring found no employer that auto-rejects on
a score or detects AI authorship; they all found that evidence in context beats keywords in a
list. So this skill optimises for a reader who should finish knowing who the person is, what is
unusual about them, and that the claims are specific enough to be true.

Each section has a job, and most bad résumé copy is a sentence doing a different section's job:
a duty in a bullet, a noun in the skills, a career in a number. The rules below say what each
section is for and give a test for each.

## Whose rules win

Apply these in order when they disagree:

1. What the person has said about their own résumé, including what may be published.
2. The employer's written instructions for this application (file type, length, questions).
3. The conventions of the person's country and industry. `references/au-banking-2026.md` holds
   the one market this skill has research for; for any other, say that the defaults below are
   untested there and take the conventions from research or from the person.
4. The defaults in this file.

**When the résumé will be judged against a standard**, such as a research digest, an
employer's guide or a recruiter's checklist, treat that standard's structure and numbers as
limits and not as guides: the scope line's length, the bullet counts, the summary's range, the
section order. Meet them by moving material to the section it fits, and depart only on the
person's own instruction. Then list every remaining departure in your reply, each with the
standard's figure, the résumé's figure and whose decision it was, so the person can decide
before a judge finds it. A departure nobody chose is a defect (C).

Rules marked **R** come from the research and rules marked **C** come from corrections a person
made to drafts that had passed every check. `references/evidence.md` has the source for each.

## Applying a rule or a correction

A rule names a fault. It does not name everything near the fault. Most of the bad drafts this
skill was built from were over-corrections: "no count of years" became a summary that never
mentioned a twenty-year career, "this reads as a laundry list" became a summary with one past
job in it, and "keep to five bullets" removed the only bullet that showed a required item (C).
Each was a rule from the research or the person, applied to more than it said.

Before you cut or rewrite anything because of a rule, a reviewer's finding or the person's
feedback:

1. **Say what the fault is, in one line, and what it leaves alone.** "A number of years is an
   age signal" forbids the number. The breadth of the career is still wanted, in words.
2. **Ask what the text was there to do.** A list of four past roles was carrying range. An
   incident in the summary was carrying judgement. Keep the function and change the form.
3. **Recast before you cut.** Cutting is the last option, for text that was doing nothing.
4. **Afterwards, re-run the section's test and its whole job** from the table below. A
   paragraph can satisfy every correction made to it and no longer do what it is for.
5. **When a default and a section's job pull apart, the job wins**, and you say so in your
   reply: a summary of 98 words that does its four things beats one of 85 that dropped one.
   Length and count defaults are guides to read against, never targets to cut to. Before a
   default gives way, though, look for the section whose level the extra material fits. A
   duty that will not fit a two-sentence scope line becomes a bullet that shows it happening
   once; a tool goes on the tools line with what it is used for; a second story in a bullet
   becomes its own bullet or joins the story it belongs to. Keep the material and keep the
   structure; let a default go only when both cannot be had.
6. **A rule about form never licenses a new claim, and caution never withholds what the
   person has already told you.** A fact someone volunteers about themselves carries its plain
   implication: a person who lists a team award as theirs was on the team. What an answer does
   not imply is anything it would take another fact to know: a figure, a result, a stronger
   verb, sole credit. Use the first freely and ask about the second. `references/voice.md`
   has the line between them.
7. **A rule never forbids the accurate word.** When the plainest true name for something is
   also the word the ad uses, use it. The fault is a word that is there only because of the ad.
8. **Keep the person's standing decisions, and check them after every revision.** Hold a list
   of what they have asked for by name: a term to use, wording they approved, something ruled
   out. A later correction changes what it names and nothing else. In one engagement a person
   had said to use a method's name and to keep a particular word, and both disappeared three
   revisions later while unrelated feedback was being applied (C). Put those terms, and each of
   the ad's required phrases the person holds, in a file and run the lint with `--keep`.
9. **A lint warning is a prompt to read the line, not a fault to clear.** Several of the
   over-corrections above were made to silence a warning.

`references/corrections.md` lists the corrections this skill has absorbed, with what each one
forbids and what it leaves in. Read it before acting on feedback, and add to it when a person
corrects a draft.

## What you need before writing

- **Everything the person has said about their work**, from every source: the old résumé, a
  profile export, answers to questions, position descriptions. Gather it per period of the
  career before drafting that period. A fact with a number is not more important because it has
  a number (C).
- **What they are known for**: what a manager, a review or a colleague would say they are
  good at, and what turns up in more than one of their roles. Ask if the documents do not say.
- **The target**: the role or ad, or the role family when there is no ad.
- **Their rules**: what they will not claim, what stays off a public copy, any wording they
  have already rejected.

Use only facts the person has given. Where information is missing, leave a placeholder in
angle brackets where the answer will go, named for what is missing: "for the `<Project Name>`
project", "which `<what changed as a result>`". The builders print a placeholder in red, in
the PDF and the Word file, so a gap is impossible to miss and never reads as plausible text.
Write the sentence around it so that it will read correctly once the answer is dropped in.
List every placeholder in your reply as a question. A background check and an interview test
every figure, so an invented or rounded-up number costs the person more than an admitted gap
(R, C). When `career-kit:career-kit` is running the engagement, its question form collects the
answers.

**A bare fact is a question waiting to be asked.** When the person gives you a fact with no
substance behind it, write what you have and ask for the rest; do not settle for stating that
it happened. An award: what was it for, and what did they do towards it? A move between
roles: what were they asked to take on? A team they led: what changed while they led it? A
tool: what do they use it for? "The project received the award" is all an award line can say
until someone asks what the award recognised, and the answer is usually the best line in the
section (C). These enriching questions get a red placeholder too, at the point in the sentence where
the answer belongs ("received the award for `<what the award recognised>`"), so the person
sees what a better line is waiting on. Put the questions in your reply, most valuable first.
A draft with placeholders goes to the person; the copy that goes to an employer has none, and
the lint fails on one unless `--allow-gaps` is given. `references/voice.md` lists the question for each kind of bare fact.

## The document, top to bottom

Write the sections in this order, under these headings, in one column of plain text (R).
`references/structure.md` covers format, length, long tenure and files.

| Section | Its job | Length | Test |
| --- | --- | --- | --- |
| Name and contact line | How to reach them and their right to work | Name, then 1 line | Is every item plain text in the body, and is anything personal there that no employer needs? |
| Professional summary | What they are responsible for in the target role's terms, which of the ad's required items they hold, what makes them different, and the judgement the work turns on | 60 to 90 words, 1 paragraph | Could this paragraph sit on someone else's résumé? Then it has failed. Is each sentence true of the whole role, and none of one occasion? |
| Key skills | What they are unusually good at, as abilities that carry to any role | 2 to 4 labelled lines | Is each item an ability, would it be true in their next job, would it be missing from the résumé of most people with the same title, and which line below shows it? |
| Professional experience: employer heading | Where they have worked and how they moved | 1 line, plus 1 or 2 sentences when several roles sit under one employer | Are the start date and each move true and visible? |
| Current role | Exactly what they own, how the work runs, and what happened because of them | Scope line of 1 or 2 sentences, then 3 to 5 bullets | Is each bullet one thing that happened, with a detail only they would know? |
| Roles in the last 10 to 12 years | The depth the summary claims | Scope line with scale, then 1 to 4 bullets | Does this role show something the summary says? |
| Earlier roles | That the ladder exists | Title, employer and dates; at most 1 line | Would a reader miss this line if it were cut? |
| Education and certifications | Qualifications actually held | 1 line each | Is there something to list? Leave the section out when there is not |

### The level each section speaks at

A résumé makes claims near the top and proves them further down. Each section has its own
level of generality, and most misplaced sentences are at the wrong level for where they sit:
an incident in the summary is too specific, a bare noun in the skills is too abstract, a skill
that names this job's system is too specific, a duty in a bullet is too general (C).

| Section | It speaks at the level of | Test |
| --- | --- | --- |
| Summary | The person, whatever the job | Could each sentence begin "Usually"? |
| Key skills | An ability that carries to another role | Would it be true in their next job? |
| Scope line | This role | Does it say what is theirs here, and nothing about one occasion? |
| Bullet | One occasion | Does it have a name, a number or a date that only this work has? |

Keep the claim and its proof apart. A skill is stated generally and a bullet below shows it
once; writing the proof into the skill ("leading discovery from access data on the X platform")
turns an ability into a description of one job and tells the reader the person does one thing.
A skill named so broadly that nothing could prove it ("discovery", "stakeholders") is the
opposite fault. Aim between them: a verb and what it acts on, with no employer, product, system
or data set named.

**General is not the same as generic.** Remove the specifics from a job-specific line and what
is left is whatever everyone with that title does. The claim sections, the summary and the key
skills, have to be both: general enough to carry, and the person's own. So their content comes
from the person first and is checked against the ad second, never the other way round. Find
what recurs across their roles, what people rely on them for, and what they did that the title
did not require; then see which of the ad's requirements those meet. What every holder of the
title does is the entry requirement. It is shown in the roles, where the ad's terms sit in dated
evidence, and it leads nothing (C).

Left out by default: a photo, date of birth, marital status, street address, a count of years of
experience, a career objective, referee names, skill bars, and any claim to be "cleared" for
background checks (R). `references/sections.md` has each section in depth, with the reasons and
a worked example of an invented person.

## Voice

- **Every sentence is about the person: what they do, own, decide or answer for.** "I am the
  Product Owner for X, which has 20,000 users" is a title and a fact about X. Write what the
  title carries: "I am responsible for what 20,000 people can do in X." Test any line by taking
  the person out of it; if what is left is still true, it is a fact about the world and needs
  rewriting around their responsibility (C).
- **A figure gives the size of the person's responsibility**, and is attached to what they do
  with it. A number that describes the product, the employer or the team beside them tells the
  reader about those things (C).
- **Paragraphs are in the first person.** The summary, the employer sentences and each scope
  paragraph are prose, and "I own… I came to product from operations" reads as a person (C).
- **Bullets open with a past-tense verb**, including in the current role. Ongoing work belongs
  in the scope paragraph; a bullet is something that happened (C).
- **No line opens with a bare present-tense verb.** "Lead discovery…" reads as a command or as
  a misspelt "Led", and beside past-tense bullets it looks as if the tense keeps changing (C).
- **It sounds like the person, and not like their file.** A first-person résumé that states
  everything as a record entry ("The project received the award in 2026") is correct and
  rigid. Where the person has a stake in something, say so once, in plain words, attached to
  the specific thing: pride in a named piece of work, the reason for a move, how they judge
  their work. "Our" for what a team did. One such sentence in a section is enough; adjectives
  about themselves are still out (C).
- **Plain verbs and the local spelling.** Led, ran, cut, fixed, wrote, coached. The register
  that reads as machine-written is named in `references/voice.md`, and the lint fails on it (R).
- **State scope exactly.** Supported is not led; coordinated is not ran; one backlog in a squad
  is not the squad's backlog. People who know the real scope read the résumé (C).
- **Explain only what this reader would not know.** An internal name gets a few words on first
  use, then is used freely (R, C). A product, company or method the hiring manager already
  knows gets none: "Microsoft Copilot, an AI assistant" spends three words telling them what
  they know, and usually they are there to carry a keyword (C).
- **Each sentence has one reading.** Say who does each thing and in what order. "I use the tool
  to draft test cases, and validate the output" lets the tool do the validating; "then
  validate the output myself" does not. `references/voice.md` lists the usual traps (C).
- **Every word tells the reader something.** Take a phrase out; if the reader has lost nothing
  they did not already know, it stays out. `references/voice.md` lists the usual kinds.
- **One number, one noun, one time.** Keep a figure with the thing it counts, write an expected
  result as expected, and count one piece of work once (C).

`references/voice.md` has the verb lists, the four kinds of drift with examples, and how to cut
for length without deleting the connecting words.

## Suiting it to a role

Read the ad's required items. For each one the person can evidence, use the ad's own phrase once
in the summary or the current role, in a sentence that shows it happening; ranking tools score
against the ad's stated requirements and weigh recent roles most (R). For each one they cannot
evidence, leave it out and tell the person which requirement the résumé does not meet. No
wording closes a gap in someone's experience, and a term that is there only because the ad uses
it is the weakest thing on the page (R, C).

Ask the person whether they want one résumé or one per role family. One is simpler to keep true;
separate versions change the summary, the skills and which bullets appear, and never a title, a
date or a figure (R, C). `references/tailoring.md` covers internal, external and public copies.

## Drafting

1. Gather the facts and the target as above, and note the person's rules.
2. Write down the job and the test for each section as it applies to this person. The table
   above is the starting set; adjust it to them and give it to any reviewer.
3. Write the experience section first, most recent role first, then the key skills from what recurs across the roles and
   what the person is relied on for, checked against what
   the experience shows, then the summary last. The summary and the skills make claims the
   experience has to carry, so they are easier to write true once it exists.
4. Read the whole document top to bottom as the hiring manager would, in under a minute. Cut
   any fact stated twice in full: the summary says what the work turns on and the first bullet
   shows it happening once,
   and a scope line does not repeat the summary. Paragraphs are where a first-person résumé gets
   heavy, so keep each scope line to 2 sentences or fewer and let the bullets carry the detail.
   Then check the summary against the ad: it names two or three of the required items the
   person holds, in the ad's words, and each of those is shown again in a scope line or a
   bullet of the current or previous role.
5. Run the lint and fix what it finds:

```bash
python3 scripts/resume_lint.py path/to/resume.md            # exit 0 clean, 1 on any error
python3 scripts/resume_lint.py --allow-gaps path/to/draft.md   # a draft that still has <gaps>
```

6. Reply with the path, the open `<placeholders>` as questions, the enriching questions for any bare
   fact, each ad requirement the résumé does not meet, each departure from the research or
   other standard it will be judged against, and each place you departed from a default and why. Keep the reply under 12 lines.

When the task is one section, do steps 1 and 2 for that section, read the sections it depends
on, and write only what was asked.

## Reviewing

A request to review is a review. Report findings with proposed wording and change nothing until
the person says to apply them (C).

Read first, before checking any rule: go through the document as the hiring manager would and
note each sentence you stumbled on and why. A review that checks only consistency passes copy
that reads badly (C). Then check each of the 8 sections against its job and its test, check for
the four kinds of drift against the facts supplied, look for what the career shows that the
résumé omits, and run the lint.

Write the review for someone who will act on it in ten minutes. Blind judges preferred a shorter
review that ended in a usable draft over a longer one that showed its working (evals). The file
has these 6 parts, in this order, and runs to 80 lines or fewer:

1. **Verdict**, in 3 lines or fewer: whether to send it, and the two or three things that
   matter most.
2. **Overclaims**: a table of each line that states more than the facts support, with the fact
   and the wording that fits it.
3. **What reads badly or is missing**: the sentences you stumbled on and the section faults,
   each in one line with its fix. Merge a point that appears under two headings into one.
4. **How it fits the ad**: each required item as shown, partly shown or not shown. For an item
   not shown, say in one line how to meet it honestly outside the résumé, in a cover letter or
   at interview, and what nearby experience the person does have.
5. **Proposed wording**: one clean, copy-ready version of the résumé's changed sections, using
   only facts already supplied. It contains no brackets and no unconfirmed material, so it
   could be sent as it stands.
6. **Questions for the person**: each missing fact as one question, with what it would add and
   where. Six blind verdicts out of six asked for these to sit outside the draft, so a draft
   can never go out with a placeholder in it (evals).

Keep out of the file: the lint's raw output (state its error count in one line and fold its
findings into part 3), a per-section restatement of each job and test, and claims about
research or ranking tools. When a figure is restricted, such as one marked internal only, refer
to it as "the internal-only figure" and do not repeat the number anywhere in the review, quotes
included, so the review itself is safe to forward.

## Working with the rest of career-kit

This skill decides and checks the words. `career-kit:career-kit` runs the engagement around
them: the research, the question form, the build to PDF and Word
(`../career-kit/scripts/build_resume.py`, `make_docx.py`), `facts_lint.py` for figures, and the
panel review after each change. The lint here checks structure and voice; `facts_lint.py`
checks that each figure was confirmed. Run both on a finished document. Put a real choice
between two wordings to `decision-panel:decision-panel`.

## Scope and length

Deliver what was asked at the scope intended: a request for a summary gets a summary, with a
one-line note if another section contradicts it. Do the reading, judging and writing yourself;
this work is one document at a time and needs no subagent. The résumé itself is two pages unless
the person's market says otherwise.
