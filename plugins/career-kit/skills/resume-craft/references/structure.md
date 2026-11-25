# Structure, format and length

Read this when laying out a document, fitting it to pages, or handling a long career at one
employer. **R** marks a default from the research, **C** one from a recorded correction, and
**LG** or **LP** one from the layout research of 25 November 2026; `evidence.md` has the source
for each.

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

## Which layout

Australian guidance does not converge on one layout. It splits by who reads the résumé first,
and each layout shares one column through the body, plain type and newest role first (LG, LP):

| Layout | Use it for | Shape | Length | Type |
| --- | --- | --- | --- | --- |
| Corporate, through a hiring system | Banks, large employers and recruiters, uploaded to a portal | One column; no tables, sidebars or text boxes | Two pages; three at executive scope | Arial or Calibri 11pt, 14pt headings, 20 mm margins |
| Public sector | Government roles with a written pitch or selection criteria | One column; personal details and any clearance first, gaps explained, two named referees | Two to six pages | 11 to 12pt |
| Direct to a person | A PDF emailed to a recruiter or executive, never uploaded | Two columns on page one only | Two to three pages | 11pt in the main column |

Default to the corporate layout, and say which one you chose when the person's channel is
different. A two-column page one is acceptable only for a file that no portal will parse (LG).

## Format

Every employer runs a different hiring system, so the file has to survive all of them (R). The
rules below reduce the risk of a failed parse; no controlled test shows that a two-column
résumé always fails.

| Item | Default | Why |
| --- | --- | --- |
| Layout | One column. No tables, text boxes, sidebars, icons, skill bars or photos | Parsers interleave columns and drop text in boxes (R) |
| Headings | Professional summary, Key skills, Professional experience, Education and certifications, in sentence case | Parsers map standard headings to fields; an inventive heading may not map (R). The Australian Government Style Manual sets headings in sentence case, and no Australian example uses capitals (LG) |
| Contact details | Plain text in the body, under the name | Text in a Word header or footer can be skipped. A page number in the footer is fine (R) |
| Dates | `Mon YYYY – Mon YYYY` on every role, `Present` for the current one | Forms and ranking tools compute tenure from them; years alone hide duration (R) |
| Role line | `Title | Employer | dates`, the same pattern every time | A parser reads each role as its own record (R) |
| Bullets | A plain hyphen or round bullet | Custom glyphs can extract as stray characters (R) |
| Type | Arial or Calibri, body 11pt (10.5pt only for a dense document, never below 10), section headings 14pt bold, name 20pt, margins 20 mm on every side | 11pt is the most-cited size: a federal jobs department, SEEK's own templates, two university guides and the legibility research's favourite size. SEEK puts headings at 14 to 16pt (LG, LP). Resolve overflow by cutting, never by shrinking type (C) |
| Line spacing | Exact 13pt lines on 11pt type, 3pt between bullets, 12pt before each section heading | No Australian source gives a number. Two points of leading read fastest in Tinker's studies (LP); the spacing values are one report's inference (LG). Say so where the layout is explained (C) |
| File | Word (.docx) to an application portal, text-based PDF to a person | One vendor lists DOCX and not PDF for parsing; PDF holds its layout when forwarded. Follow the employer's instruction where it gives one (R) |
| File name | `Firstname-Lastname-Resume-Role.docx` | So the recruiter can find it |

Check which fonts actually embedded in the PDF (`pdffonts file.pdf`). A font named in the
stylesheet and missing from the machine falls back silently (C).

## Length

Two pages is the default, because it is the only length inside every source's range: a federal
jobs department says no more than two, a federal police guide for senior executives a maximum of
two, Hays about two, Robert Half two to three, a university guide two to four, SEEK one to two and
up to five for senior people, and the public service two to six (LG, LP). An employer's own
published guide can differ: one large employer's says "a CV can be 3-4 pages long" and asks for
"plenty of white space", so read the target employer's guide where it has one (LP). A third page is for evidence a
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

A figure or result the person has not confirmed, written in at the request of the person
helping so the person can correct it rather than invent it from nothing, goes between double equals signs:
`Supported access for ==about 200== home lending bankers`. The builders print it on a yellow
highlight, in the PDF and the Word file, and the lint treats it as a gap. It lives only in the
internal copy that goes to the person; the public copy, the website and the LinkedIn copy keep
the confirmed wording until the person answers. Record each one and the question it stands for
(C).
