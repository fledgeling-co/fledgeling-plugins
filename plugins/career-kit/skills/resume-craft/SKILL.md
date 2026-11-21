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
  by section against the job each section has. Its structure comes from cited research on how
  résumés are screened in 2026, its writing guidance from corrections people made to drafts
  that had passed every check, and a bundled lint checks both mechanically. Not for the whole
  application kit (research, question form, PDF and Word builds, LinkedIn, website, interview
  guide: use `career-kit:career-kit`), and not for cover letters or LinkedIn copy.
---

# resume-craft

A résumé has two readers and one job. Software files it: it pulls the employer, title, dates
and skills into fields, and sometimes ranks it against the ad. A person then decides, usually
in under a minute, and the realistic way to lose is a reader who meets generic copy and moves
on. So this skill writes for a reader who should finish knowing who the person is, what is
unusual about them, and that the claims are specific enough to be true.

## Two layers, and which one wins

**The research is the base (R).** Six reports on how résumés are screened and read set the
structure: the sections and their order, what each holds, how long each is, the format and the
file. No report found an employer that rejects on a score or detects AI authorship; all found
that evidence in context beats keywords in a list. `references/au-banking-2026.md` holds the one
market the research covers. For any other market, say that these defaults are untested there
and take the conventions from research or from the person.

**The writing guidance sits on top (C).** Each rule marked C is a correction a person made to a
draft that had already passed the research's checks, a lint and several reviewing models. They
are what a capable writer still gets wrong: a title where a responsibility should be, a skill
that is really a keyword, an achievement told flat, a rule applied to more than it said.
`references/evidence.md` gives the source of every rule, and `references/corrections.md` how
far each correction reaches.

When they disagree, apply them in this order:

1. What the person has said about their own résumé, including what may be published.
2. The employer's written instructions for this application.
3. The conventions of the person's market, from the research.
4. The defaults in this file.

**The structure's numbers are limits.** Section order, the summary's range, the scope line's
length and the bullet counts are what a recruiter, a ranking tool or anyone holding the
research will check first. Meet them by moving material to the section it fits. Depart from
one only on the person's instruction, or when a section cannot do its job any other way, and
list every departure in your reply with the limit, the résumé's figure and whose decision it
was. A departure nobody chose is a defect.

## What you need before writing

- **Everything the person has said about their work**, from every source: the old résumé, a
  profile export, answers to questions, position descriptions. Gather it per period of the
  career before drafting that period. What a person wrote about their own work is evidence of
  that work.
- **What they are known for**: what a manager, a review or a colleague would say they are good
  at, and what turns up in more than one of their roles. Ask if the documents do not say.
- **The target**: the role or ad, or the role family when there is no ad.
- **Their standing decisions**: what they will not claim, what stays off a public copy, a term
  they asked for by name, wording they approved or rejected. Keep these as a list. A later
  correction changes what it names and nothing else.

**Use only facts the person has given, and use all of them.** Two failures sit either side of
that line. Inventing is one: a background check and an interview test every figure, so an
invented or rounded-up number costs more than an admitted gap (R). Holding back is the other: a
fact someone volunteers about themselves carries its plain implication, so a person who lists a
team award as theirs was on the team. What an answer does not imply is anything it would take a
second fact to know: a figure, a result, a stronger verb, sole credit.

**Mark what is missing where the answer will go.** Leave a placeholder in angle brackets, named
for what is missing: "for the `<Project Name>` project", "which `<what changed as a result>`".
The builders print it in red in the PDF and the Word file. Write the sentence around it so it
reads correctly once the answer is dropped in.

**A bare fact is a question waiting to be asked.** An award: what was it for? A team they led:
what was different by the time they left? A change they made: what happened next? Write the
line with what is known, put a placeholder where the answer belongs, and ask. The answer is
often the best line in the section. `references/voice.md` has the question for each kind of
fact.

## The document, top to bottom

Write the sections in this order, under these headings, in one column of plain text (R).
`references/structure.md` covers format, length, long tenure and files, and
`references/sections.md` has each section in depth with a worked example.

| Section | Its job | Limit (R) | Test |
| --- | --- | --- | --- |
| Name and contact line | How to reach them and their right to work | Name, then 1 or 2 lines | Is everything plain text in the body, and is anything there that no employer needs? |
| Professional summary | What they are responsible for now, which of the ad's requirements they hold, what makes them different, and the judgement their work turns on | 60 to 90 words; the research allows 100 | Could this paragraph sit on someone else's résumé? Could each sentence begin "Usually"? |
| Key skills | What they are unusually good at, as abilities that carry to another role | 2 to 4 labelled lines, plus a tools line | Is each item an ability, true in their next job, missing from most résumés with the same title, and shown by a line below? |
| Employer heading | Where they have worked and how they moved | 1 line, plus 1 or 2 sentences when several roles sit under one employer | Are the start date and each move true and visible? |
| Current role | Exactly what is theirs, then what happened because of them | Scope line of 1 or 2 sentences; 3 to 5 bullets | Is each bullet one thing that happened, ending on what it changed? |
| Roles in the last 10 to 12 years | The depth the summary claims | Scope line with scale; 2 to 4 bullets, fewer as roles get older | Does this role show something the summary says? |
| Earlier roles | That the ladder exists | Title, employer, dates; at most 1 line | Would a reader miss this line if it were cut? |
| Education and certifications | Qualifications actually held | 1 line each | Is there something to list? Leave the section out when there is not |

Left out by default: a photo, date of birth, marital status, street address, a count of years
of experience, a career objective, referee names, skill bars, and any claim to be "cleared"
for background checks (R).

**Each section speaks at its own level.** A résumé makes claims near the top and proves them
further down. The summary is about the person whatever the job. A skill is an ability that
carries to the next job. A scope line is about this role. A bullet is one occasion. Most
misplaced sentences are at the wrong level for where they sit: an incident in the summary, a
keyword in the skills, a duty in a bullet. Keep each claim and its proof apart: state the
skill generally and let a bullet show it once.

**The claim sections come from the person first and the ad second.** Strip the specifics from
a job-specific line and what is left is what everyone with that title does. For the summary
and the key skills, find what recurs across the person's roles, what others rely on them for,
and what they did that the title did not require; then see which of the ad's requirements
those meet. What every holder of the title does is the entry requirement. It is shown in the
roles, gets one "craft" line in the skills at most, and leads nothing.

**A role gives three things without three headings.** Responsibilities are the scope line.
Achievements are the bullets. What good looked like goes in a clause, only where the person's
sources state a measure. Labelled blocks under each role read as a position description and
cost a page.

## How to write it

`references/voice.md` has each of these in depth, with tables of examples.

**About the person**

- Every sentence has the person doing, owning, deciding or answering for something. "I am the
  site manager for a 40-bed ward" is a title and a fact about a ward; "I am responsible for
  the care of up to 40 patients a shift" is about them. Take the person out of a sentence; if
  it is still true, rewrite it around their responsibility.
- Paragraphs (summary, employer sentences, scope lines) are in the first person. Bullets open
  with a past-tense verb, including in the current role. No line opens with a bare
  present-tense verb: "Lead the team…" reads as a command or a misspelt "Led".
- It sounds like the person and not like their file. Where they have a stake in something
  specific, say so once in plain words: pride in a named piece of work, the reason for a move,
  how they judge their work. "Our" for what a team did.

**True**

- Scope verbs are facts. Supported is not led; coordinated is not ran; one part of a team's
  work is not the team's work. People who know the real scope read the résumé.
- Check for four kinds of drift: a stronger verb than they confirmed, an expected result
  written as achieved, a figure whose noun changed, and one piece of work counted twice.

**Worth reading**

- It sells what is true. A bullet that is accurate and flat has done half its job. Lead with
  what mattered, say what was at stake, put the scale beside the action, and end on what
  changed and not on the admin. The verb, the figures and the result stay exactly as
  confirmed; the order, the emphasis and the context are yours to choose.
- One headline, one support. Each bullet makes its point in the first sentence and carries at
  most one supporting fact, the one that most changes what the reader thinks of the person.
  How it was done, with which tools and through which process goes, unless that is the point.
- A number has to enlarge the reader's impression to stay. A large scale, a result or an exact
  count of something hard does. A range, a small team size, a duration or a tally of faults
  makes the work sound smaller. Being confirmed is the condition for printing a figure, and
  not a reason to.

**Plain**

- Each sentence has one reading. Say who does each thing and in what order.
- Every word tells this reader something. Explain an internal name in a few words on first
  use; explain nothing they already know.
- Plain verbs, the local spelling, numerals for counts. The register that reads as generic or
  machine-written is listed in `references/voice.md`, and the lint fails on it (R).

## Suiting it to a role

Read the ad's required items. For each one the person can evidence, use the ad's own phrase
once, in a sentence that shows it happening, in the summary or a recent role; ranking tools
score against the ad's stated requirements and weigh recent roles most (R). The accurate word
is never ruled out because the ad also uses it. For each requirement they cannot evidence,
leave it out and tell the person: no wording closes a gap in someone's experience, and a term
that is there only because the ad uses it is the weakest thing on the page (R, C).

Ask the person whether they want one résumé or one per role family. Separate versions change
the summary, the skills and which bullets appear, and never a title, a date or a figure.
`references/tailoring.md` covers internal, external and public copies.

## Applying a rule or a correction

A rule names a fault. It does not name everything near the fault. Most of the weak drafts this
skill learned from were over-corrections: "no count of years" became a summary that never
mentioned a long career, "it reads as a list" became a summary with one past job in it, a
bullet limit removed the only bullet that showed a requirement. Before cutting or rewriting
because of a rule, a reviewer or the person's feedback:

1. Say what the fault is in one line, and what it leaves alone.
2. Ask what the text was there to do, and keep that. Recast before you cut.
3. Move material to the section whose level it fits before letting a limit go.
4. Afterwards, re-run the section's test and its whole job. A paragraph can satisfy every
   correction made to it and no longer do what it is for.
5. Check the standing decisions and the ad's required phrases are all still present.
6. Never let a rule about form produce a claim nobody confirmed.

The latest instruction is not the only one. `references/corrections.md` lists each correction
with what it forbids and what it leaves in; read it before acting on feedback, and add to it
when a person corrects a draft.

## Drafting

1. Gather the facts, the target and the standing decisions. Write the terms that must stay, and
   the ad's required phrases the person holds, one per line in a keep file.
2. Write down the job and the test for each section as it applies to this person, from the
   table above, and give it to any reviewer.
3. Write the experience section first, most recent role first. Then the key skills, from what
   recurs across the roles. Then the summary. The claim sections are easier to write true once
   the evidence exists.
4. Read the whole document top to bottom as the hiring manager would, in under a minute. Cut
   any story told twice. Check that each requirement the summary names is shown in a recent
   role, and that each bullet answers "so what?".
5. Run the lint. Read each warning against the section's job, and change a line only if it
   fails that job; several over-corrections were made to silence a warning.

```bash
python3 scripts/resume_lint.py --keep keep.txt path/to/resume.md          # exit 1 on any error
python3 scripts/resume_lint.py --allow-gaps --keep keep.txt path/to/draft.md   # a draft with <placeholders>
```

6. Reply in 12 lines or fewer: the path; each placeholder as a question, most valuable first;
   each requirement the résumé does not meet; each departure from a limit, with whose decision
   it was.

A draft with placeholders goes to the person. The copy that goes to an employer has none, and
the lint fails on one unless `--allow-gaps` is given. When the task is one section, do steps 1
and 2 for that section, read the sections it depends on, and write only what was asked.

## Reviewing

A request to review is a review. Report findings with proposed wording and change nothing
until the person says to apply them. When they ask why something was written, give the cause,
including any rule of this skill that produced it, and wait.

Read first, before checking any rule: go through the document as the hiring manager would and
note each sentence you stumbled on and why. A review that checks only consistency passes copy
that reads badly. Then check each section against its job and its test, check the four kinds
of drift against the facts, look for what the career shows that the résumé omits, and run the
lint.

Write the review for someone who will act on it in ten minutes: 80 lines or fewer, in these 6
parts.

1. **Verdict**, in 3 lines or fewer: whether to send it, and the two or three things that
   matter most.
2. **Overclaims**: each line that states more than the facts support, with the fact and the
   wording that fits it.
3. **What reads badly or is missing**: the sentences you stumbled on, the flat achievements
   and the section faults, each in one line with its fix.
4. **How it fits the ad**: each required item as shown, partly shown or not shown, and for one
   not shown, how to meet it honestly outside the résumé.
5. **Proposed wording**: one copy-ready version of the changed sections, from facts already
   supplied, with a red placeholder wherever a better line is waiting on an answer.
6. **Questions for the person**: one per placeholder, with what the answer would add.

Keep out of the review: the lint's raw output, a restatement of each section's job, and claims
about research or ranking tools. Refer to a restricted figure as "the internal-only figure"
and never repeat the number, so the review is safe to forward.

## Working with the rest of career-kit

This skill decides and checks the words. `career-kit:career-kit` runs the engagement around
them: the research, the question form, the builds to PDF and Word
(`../career-kit/scripts/build_resume.py`, `make_docx.py`), `facts_lint.py` for figures, and
the panel review after each change. Run both lints on a finished document. Put a real choice
between two wordings or structures to `decision-panel:decision-panel`.

## Scope and length

Deliver what was asked at the scope intended: a request for a summary gets a summary, with a
one-line note if another section contradicts it. Do the reading, judging and writing yourself;
this is one document at a time and needs no subagent. The résumé is two pages unless the
person's market says otherwise.
