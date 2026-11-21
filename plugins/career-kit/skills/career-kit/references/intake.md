# Intake — what to collect and what to read before asking anything

## Ask for these, by name

| Document | Why it changes the work |
| --- | --- |
| LinkedIn profile PDF export (Profile → Resources → Save to PDF) | The current public story, dates included. It is almost always more out of date than the person thinks. |
| Current résumé, as the original file | The layout is half the review. A PDF carries the font and column structure a parser will meet. |
| Every target job description, full text | Each one lists the requirements the résumé has to show evidence for, in the employer's own words. |
| Position description for their current role | The official scope, in the employer's own vocabulary. |
| Recent performance reviews | Outcomes somebody else already wrote down, which makes them safe to cite. |
| Email signature | The exact job title and team name as the employer writes them. |

Also establish, in one short exchange: the country and city, whether the move is internal or
external, whether their manager knows, and who is relaying answers if it is not the person
themselves.

## Read everything before the first question

Read each file completely. Most of the interview's answers are in them, and a question whose
answer was in the document they just sent reads as not having opened it.

Read the résumé twice:

```bash
pdftotext source/resume.pdf -            # roughly what a parser sees
pdftotext -layout source/resume.pdf -    # what a person sees
pdffonts source/resume.pdf               # fonts actually embedded
pdfinfo source/resume.pdf                # page count and size
```

The unlayouted pass is the one that matters. A two-column design reads correctly to a person
and comes out interleaved to a parser, and that single difference accounts for a large share of
what a review finds.

## Write the facts file as you read

Each item records its status, because the status decides what you may do with it:

- **confirmed** — the person said it, in their own words or by selecting an example.
- **from a document** — it is in their résumé, LinkedIn or position description. Usable, worth
  confirming where a figure is involved.
- **inferred** — you worked it out. A role end date derived from the next role's start is the
  common one. An inferred fact is a question for the person, never a line in a document.

The status says how far to trust a figure. It does not rank the work: what the person wrote
about a job in their old résumé is evidence of that job, and a fact they volunteer carries its
plain implication. As you read, note for each period the strongest true thing about it, and
across periods what recurs, because that is what the summary and the key skills are built
from. A fact is not more important for having a number.

Hold the gloss for every internal term, acronym and system name as you meet it. The first time
each appears in a document it needs a few plain words, because an external reader will not know
it and an applicant tracking system will not expand it. A product, company or method the
reader already knows needs none.

## What the person decides, not you

Keep a running list of what only they can answer, and take it to stage 4 as one round of
questions: which figures may appear in public, which roles they actually
want and in what order, how they want a sensitive episode described, and whether a number they
gave is exact or approximate.

Keep a second list, of what they decide as you go: a term they want used, wording they approve
or reject, what stays off public copies. These standing decisions outlast the round they were
made in, and every later revision is checked against them.
