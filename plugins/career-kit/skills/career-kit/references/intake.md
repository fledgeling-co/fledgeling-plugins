# Intake — what to collect and what to read before asking anything

## Ask for these, by name

| Document | Why it changes the work |
| --- | --- |
| LinkedIn profile PDF export (Profile → Resources → Save to PDF) | The current public story, dates included. It is almost always more out of date than the person thinks. |
| Current résumé, as the original file | The layout is half the review. A PDF carries the font and column structure a parser will meet. |
| Every target job description, full text | Each one supplies the required phrases a tailored summary mirrors. |
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
  common one. An inferred fact is a question for the form, never a line in a document.

Hold the gloss for every internal term, acronym and system name as you meet it. The first time
each appears in a document it needs a few plain words, because an external reader will not know
it and an ATS will not expand it.

## What the person decides, not you

Keep a running list of what only they can answer, and take it to the form in stage 4 rather
than asking question by question: which figures may appear in public, which roles they actually
want and in what order, how they want a sensitive episode described, and whether a number they
gave is exact or approximate.
