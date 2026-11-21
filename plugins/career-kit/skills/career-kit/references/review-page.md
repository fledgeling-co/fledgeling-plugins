# The review page — a finding nobody has to take on trust

One self-contained HTML file reviewing the current résumé and LinkedIn profile. Open it in a
browser and read it before handing it over.

## What each finding carries

1. **The evidence crop.** A real image cut from their own document, with the words in question
   highlighted. Marks are composited into the PNG rather than positioned with CSS, so the
   snippet survives being copied anywhere.
2. **A layout sketch.** A small wireframe of the structure being described — the two columns,
   where the contact line sits, what a parser meets first. A finding about layout that has no
   picture of the layout is an assertion.
3. **Why it matters, with a citation.** Pointing at the research digest's claim, carrying how
   many lanes supported it.
4. **What to do.** The replacement wording, or the specific change.

## Building the crops

```bash
pdftoppm -r 150 -png source/resume.pdf review/img/resume
python3 scripts/crop_snippets.py --pdf source/resume.pdf --spec snippets.json --out review/img/
```

The spec locates a crop either by absolute PDF points or by a phrase in the text, which is what
makes it survive a redraft: a box anchored to "PROFESSIONAL EXPERIENCE" still finds the right
region after the content above it changes. `crop_snippets.py` exits non-zero when a highlight
phrase lands nowhere inside its crop, because a snippet with no marks looks finished and proves
nothing.

## Assembling the page

Inline the images as base64 so the file is one artefact the person can open from an email.
Group findings by document and by severity. A date timeline drawn as an SVG, with the résumé's
dates on one lane and LinkedIn's on the other, shows disagreement between the two at a glance
and is worth the twenty lines it takes.

Check the rendered page with `design-review:design-review` at desktop and phone widths before
handing it over. The common defects are a grid that overflows on a phone — fixed with
`grid-template-columns: minmax(0, 1fr)` — and text contrast under 4.5:1 on muted captions.

## What a review of a LinkedIn profile looks for

Dates that disagree with the résumé; a headline that is out of date, or a string of keywords
with no person in it; roles under a company name that is not the employer's official page; a skills
list from a previous career; typos in role titles, which are common and conspicuous; contact
details that are a personal address from fifteen years ago; and anything stated publicly that
their employer's social media policy would not permit.

A `linkedin` MCP server exists in this router with 24 tools including
`linkedin__get_my_profile` and `linkedin__get_person_profile`; the harness prefixes them
`mcp__router__`. They were not used in the source session, which read a PDF export instead, so
treat the export as the reliable route and the MCP as worth trying.
