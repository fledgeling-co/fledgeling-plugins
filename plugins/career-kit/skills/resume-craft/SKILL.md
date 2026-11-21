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

Rules marked **R** come from the research and rules marked **C** come from corrections a person
made to drafts that had passed every check. `references/evidence.md` has the source for each.

## What you need before writing

- **Everything the person has said about their work**, from every source: the old résumé, a
  profile export, answers to questions, position descriptions. Gather it per period of the
  career before drafting that period. A fact with a number is not more important because it has
  a number (C).
- **The target**: the role or ad, or the role family when there is no ad.
- **Their rules**: what they will not claim, what stays off a public copy, any wording they
  have already rejected.

Use only facts the person has given. Where a fact is missing, write `[the missing fact, as a
question]` in square brackets in the draft and list the brackets in your reply, so a gap is
impossible to miss and never reads as plausible text. A background check and an interview test
every figure, so an invented or rounded-up number costs the person more than an admitted gap
(R, C). When `career-kit:career-kit` is running the engagement, its question form collects the
answers.

## The document, top to bottom

Write the sections in this order, under these headings, in one column of plain text (R).
`references/structure.md` covers format, length, long tenure and files.

| Section | Its job | Length | Test |
| --- | --- | --- | --- |
| Name and contact line | How to reach them and their right to work | Name, then 1 line | Is every item plain text in the body, and is anything personal there that no employer needs? |
| Professional summary | Who they are in the target role's terms, which of the ad's required items they hold, what makes them different, at most one proof, naming the decision | 60 to 90 words, 1 paragraph | Could this paragraph sit on someone else's résumé? Then it has failed |
| Key skills | Things they can do | 2 to 4 labelled lines | Is each item an ability, and which line below shows it? |
| Professional experience: employer heading | Where they have worked and how they moved | 1 line, plus 1 or 2 sentences when several roles sit under one employer | Are the start date and each move true and visible? |
| Current role | Exactly what they own, how the work runs, and what happened because of them | Scope line of 1 or 2 sentences, then 3 to 5 bullets | Is each bullet one thing that happened, with a detail only they would know? |
| Roles in the last 10 to 12 years | The depth the summary claims | Scope line with scale, then 1 to 4 bullets | Does this role show something the summary says? |
| Earlier roles | That the ladder exists | Title, employer and dates; at most 1 line | Would a reader miss this line if it were cut? |
| Education and certifications | Qualifications actually held | 1 line each | Is there something to list? Leave the section out when there is not |

Left out by default: a photo, date of birth, marital status, street address, a count of years of
experience, a career objective, referee names, skill bars, and any claim to be "cleared" for
background checks (R). `references/sections.md` has each section in depth, with the reasons and
a worked example of an invented person.

## Voice

- **Paragraphs are in the first person.** The summary, the employer sentences and each scope
  paragraph are prose, and "I own… I came to product from operations" reads as a person (C).
- **Bullets open with a past-tense verb**, including in the current role. Ongoing work belongs
  in the scope paragraph; a bullet is something that happened (C).
- **No line opens with a bare present-tense verb.** "Lead discovery…" reads as a command or as
  a misspelt "Led", and beside past-tense bullets it looks as if the tense keeps changing (C).
- **Plain verbs and the local spelling.** Led, ran, cut, fixed, wrote, coached. The register
  that reads as machine-written is named in `references/voice.md`, and the lint fails on it (R).
- **State scope exactly.** Supported is not led; coordinated is not ran; one backlog in a squad
  is not the squad's backlog. People who know the real scope read the résumé (C).
- **Explain an internal name in a few words on first use**, then use it freely (R, C).
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
3. Write the experience section first, most recent role first, then the key skills from what
   the experience shows, then the summary last. The summary and the skills make claims the
   experience has to carry, so they are easier to write true once it exists.
4. Read the whole document top to bottom as the hiring manager would, in under a minute. Cut
   any fact stated twice in full: the summary names a proof in a clause and the bullet tells it,
   and a scope line does not repeat the summary. Paragraphs are where a first-person résumé gets
   heavy, so keep each scope line to 2 sentences or fewer and let the bullets carry the detail.
   Then check the summary against the ad: it names two or three of the required items the
   person holds, in the ad's words, and each of those is shown again in a scope line or a
   bullet of the current or previous role.
5. Run the lint and fix what it finds:

```bash
python3 scripts/resume_lint.py path/to/resume.md            # exit 0 clean, 1 on any error
python3 scripts/resume_lint.py --allow-gaps path/to/draft.md   # a draft that still has [gaps]
```

6. Reply with the path, the open `[gaps]` as questions, each ad requirement the résumé does not
   meet, and each place you departed from a default and why. Keep the reply under 12 lines.

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
