# Structure, format and length

Read this when laying out a document, fitting it to pages, or handling a long career at one
employer. **R** marks a default from the research, **C** one from a recorded correction;
`evidence.md` has the source for each.

## The Markdown source

Write the résumé as one Markdown file in this subset, which
`../career-kit/scripts/build_resume.py` renders and `scripts/resume_lint.py` reads:

```markdown
# FULL NAME

City, State | mobile | email | web address | work rights

## Professional summary

One paragraph.

## Key skills

Label: ability; ability; ability
Tools: tool, tool, tool

## Professional experience

### Employer, City | Mon YYYY – Present

One or two sentences on progression.

#### Title | Employer | Mon YYYY – Present

Scope paragraph.

- Bullet.

#### Earlier title | Employer | Mon YYYY – Mon YYYY

## Education and certifications

Qualification, Institution
```

Write the document out whole, by hand. A script may render and check it; a document assembled
from sentence fragments by a script is one nobody has read as a document (C).

## Format

Every employer runs a different hiring system, so the file has to survive all of them (R). The
rules below reduce the risk of a failed parse; no controlled test shows that a two-column
résumé always fails.

| Item | Default | Why |
| --- | --- | --- |
| Layout | One column. No tables, text boxes, sidebars, icons, skill bars or photos | Parsers interleave columns and drop text in boxes (R) |
| Headings | Professional summary, Key skills, Professional experience, Education and certifications | Parsers map standard headings to fields; an inventive heading may not map (R) |
| Contact details | Plain text in the body, under the name | Text in a Word header or footer can be skipped. A page number in the footer is fine (R) |
| Dates | `Mon YYYY – Mon YYYY` on every role, `Present` for the current one | Forms and ranking tools compute tenure from them; years alone hide duration (R) |
| Role line | `Title | Employer | dates`, the same pattern every time | A parser reads each role as its own record (R) |
| Bullets | A plain hyphen or round bullet | Custom glyphs can extract as stray characters (R) |
| Type | A standard sans-serif (Arial, Calibri, Aptos), body 10.5 to 11pt, section headings 13 to 14pt, margins 18 to 22 mm | Readable print; resolve overflow by cutting, never by shrinking type (R, C) |
| File | Word (.docx) to an application portal, text-based PDF to a person | One vendor lists DOCX and not PDF for parsing; PDF holds its layout when forwarded. Follow the employer's instruction where it gives one (R) |
| File name | `Firstname-Lastname-Resume-Role.docx` | So the recruiter can find it |

Check which fonts actually embedded in the PDF (`pdffonts file.pdf`). A font named in the
stylesheet and missing from the machine falls back silently (C).

## Length

Two pages is the default, because it sits inside every source's recommendation for an
experienced person: one source says about two, another allows two to five for senior people,
and the research reports themselves range from two to three (R). A third page is for evidence a
specific role asks for, and an internal hiring manager who wants role-by-role depth is the usual
case (R). The person's market can move this default; see `au-banking-2026.md`.

What goes where:

- **Page 1**: name, contact line, summary, key skills, and the current role complete or nearly
  so. It has to make the case alone (R).
- **Page 2**: the remaining roles in full, earlier roles, education.

## Reading the built page

A page count of two is the same number whether the second page is full or 40% empty. After each
build, look at the page images (C):

```bash
pdftoppm -r 60 -png resume.pdf /tmp/resume-page
```

- The last page is at least about half full and ends on a complete line.
- No role line has wrapped so that the employer or the dates sit on their own line.
- No heading is stranded at the foot of a page with its content on the next.
- Select all, copy and paste into a plain text editor: the text comes out in reading order (R).

After uploading to a portal, read the fields it filled in (employer, title, dates, skills) and
correct them by hand. A failed parse leaves the file attached and the fields wrong (R).

## Many years at one employer

One employer heading, each role dated separately beneath it, most recent first (R).

- **Give the last 10 to 12 years in full.** Ranking tools weigh recent roles most, and so does a
  reader's attention. One documented matcher computes skill similarity twice, once on recent
  roles only (R).
- **Compress earlier roles** to a title and dates, or to one "Earlier roles" line on an external
  copy (R).
- **Keep the true start date** on the employer heading and the true dates on every role listed
  in full. Do not shift, merge or drop dates to look younger or more recent; forms and employment
  checks collect the real ones (R).
- **Never present the whole tenure as one role.** `Example Bank | 2005 – Present | Product
  Owner` tells a parser and a reader that the person has been a Product Owner for twenty years
  (R).
- **Show movement as facts.** A promotion named as a promotion, a move between divisions named
  as a move, a larger team or scope stated in the scope line. A recent example of a current
  tool or method answers a doubt about adaptability better than the word "adaptable" (R).
- **Do not count the years** anywhere in the prose. One survey found 24% of HR respondents call
  workers aged 51 to 55 "older", up from 10% two years earlier, and the same survey found
  employers already credit older workers with loyalty and reliability. The résumé needs to show
  current tools, current methods and recent results (R).
- **Leave graduation years off** older qualifications and date recent learning (R).
- **Print the official title** from the employment record, and put any plainer description in
  the scope line. In the source session "Manager, IVR Channel" became "Channel Manager", the
  title on the HR record and on LinkedIn, with "the IVR channel" in its scope line (C).
- **A corrected date can overlap the role before it.** When a start date moves earlier, flag the
  overlap and ask for the record; do not move the other role's date to close it, because that
  date is a fact too (C).

In an application form, enter each role as its own employment record even when the résumé
groups them, and count time in the target kind of role, not total tenure, when a screening
question asks for years of experience (R).

## Gaps in the document

Missing information appears as a placeholder in angle brackets, named for what is missing and
placed where the answer will go: `<Project Name>`, `<what changed as a result>`. The builders
print it in red, in the PDF and the Word file. A document with a placeholder in it goes to the
person and never to an employer; the lint exits non-zero on one unless `--allow-gaps` is given.
Square brackets are still recognised, for drafts written to the earlier convention (C).
