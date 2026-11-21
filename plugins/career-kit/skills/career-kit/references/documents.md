# The documents — one source of facts, four outputs per role

## The Markdown subset

```markdown
# Jane Doe
jane@example.com | 0400 000 000 | Sydney | linkedin.com/in/jane-doe

## Professional summary

One paragraph. Mirrors this ad's required phrases, each backed by a bullet below.

## Key skills

Product and delivery: backlog refinement; acceptance criteria; release readiness
Tools: Jira, Confluence, Power BI

## Professional experience

### Example Bank | Aug 2005 – present

#### Product Owner | Platforms | May 2025 – present

- One bullet, one claim, with the figure that evidences it.

#### Analyst | Jun 2008 – Dec 2013

- Work before the last decade gets a line or two.
```

`[anything in square brackets]` renders as a yellow highlight and prints. That is the gap
marker: an unconfirmed figure must be impossible to miss rather than plausible prose. A
document goes to the person with highlights in it, and never to an employer.

## Building

```bash
python3 -m http.server 8942 --bind 127.0.0.1 --directory rewrite &
python3 scripts/make_variants.py --facts facts.md --spec variants.json --out roles/ \
    --name "Jane Doe" --serve-url http://127.0.0.1:8942/roles --docx-python /tmp/dv/bin/python
```

The local server is not optional: Chrome's `--print-to-pdf` loads the page over HTTP.

`python-docx` is usually absent from the system interpreter:

```bash
python3 -m venv /tmp/dv && /tmp/dv/bin/pip install python-docx
```

Without it the script falls back to `textutil`, which produces an unstyled file that is
readable but does not match the PDF. The source session shipped those first and was asked for a
styled version immediately.

## Pages break, containers do not

The sheet has `min-height: 297mm` and no `height`, and no `overflow: hidden`. An earlier
version used a fixed height with a manual split at a named heading, and it cut the last bullets
off page one in all five variants with no error anywhere. The CSS that does the work:

```css
@page { size: A4; margin: 13mm 16mm 15mm }
h2, h3 { break-after: avoid }
li, h3 + p { break-inside: avoid }
@media print { .sheet { padding: 0; width: auto; min-height: 0 } }
```

`make_variants.py` prints a page count per variant and exits non-zero when one is over its
limit. Then look at the pages:

```bash
pdftoppm -r 60 -png roles/Jane-Doe-Resume-Product-Owner.pdf /tmp/role
```

Read the images. A page count inside the limit and a last line that ends mid-sentence are the
same number.

## Fonts

Check what actually embedded:

```bash
pdffonts roles/Jane-Doe-Resume-Product-Owner.pdf
```

A font named in the CSS and absent from the machine falls back silently, and the PDF and the
Word file then differ for a reason invisible in the Markdown. Arial is the safe default on
macOS; a brand font needs `fc-list` to confirm it exists before it is specified.

## One variant per role

Each variant takes the same facts and changes three things: which bullets appear and in what
order, which skill blocks appear, and the summary. Nothing else differs — not a title, not a
date, not a figure. The variant spec makes that structural rather than a matter of care.

A public variant drops the phone number and work email and softens any figure the person has
restricted. It is a variant in the same spec, not a hand-edited copy.

## Word and Google Doc

Upload the `.docx` to portals, which parse it. Send the PDF to people.

A Google Doc version was requested in the source session and never built, so this step is
designed and unproven. Check what the runtime offers — `anthropic-skills:google-workspace`
where it is installed, or a Google Drive MCP server — and create the document from the same
Markdown so the facts cannot diverge. Say which route you used and that the step has no prior
run behind it.

## What each section is for

`career-kit:resume-craft` holds the full version of this section, with the reasons, the voice
rules and a worked example; the table below is the short form.

Write this down for the person in front of you before drafting, and give it to reviewers. A
starting set, from the source session's research and its mistakes:

| Section | Its job | Test |
| --- | --- | --- |
| Summary, 60 to 100 words | Current role first, then what makes this person different, then proof they deliver now | Could this paragraph sit on someone else's résumé? Then it has failed |
| Key skills, 2 to 4 lines | Things they can do | Is each item an ability, and which line below shows it? |
| Employer heading | Progression, the true start date, a positive reason for the latest move | One or two sentences |
| Current role | A scope paragraph saying exactly what they own and how the work runs, then 3 to 5 bullets | Each bullet is one thing that happened, with a detail only they would know |
| Roles in the last 10 to 12 years | A scope line with scale, then what changed because they were there | Does it carry the depth the summary claims? |
| Earlier roles | Title and dates | At most a line |

Tools are a list and get their own line. A term from an ad is not a skill because the ad uses
it: "epics, features and stories" sat in a skills line for a day in the source session because
it was true and matched an ad, and neither of those makes it an ability.

## Use the whole career

For each period, gather everything the person has said about it from every source before
writing: the old résumé, the profile export, each round of answers. Then ask what the strongest
true thing about that period is. A fact with a confirmed number is not more important because
it has a number. The source session's summary described eighteen years before the current role
as "coordinated 5 to 10 change workstreams", because that answer had a figure and matched an
ad, while the old résumé described running workforce planning for 1,400 seats and governing
partner operations of 600 people.

## Voice, tense and person

- Paragraphs in the first person. A summary is prose, and "I lead… I took…" reads naturally.
- Bullets open with a past-tense verb, including in the current role.
- No line opens with a bare present-tense verb.
- Put ongoing work in the scope paragraph ("I own…", "I write…") and finished work in bullets.
- After a "when" clause, keep a subject or recast: "When a role held unused permissions,
  removed them" loses its subject.

## Reading the page, not only the count

A page count of two says nothing about a second page that is 40% full or a role line that has
wrapped. After each build, look at the page images. Check that no employer name or date has
dropped to its own line, and that the type sizes match the research (the source session's
research gave 10.5 to 11pt body, 13 to 14pt headings, 18 to 22 mm margins; the first builds
were 10pt with 13 mm margins to hold too many words).
