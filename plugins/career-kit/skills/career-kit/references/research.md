# Research — four subjects, several lanes, one reconciled digest

## The four subjects

1. **Country conventions.** Length, photo, personal details, date format, education placement,
   what is illegal to ask for, and the layout and type: body and heading sizes, margins, line
   spacing, and whether there is one accepted layout or several. These differ sharply: a
   convention that is correct in Germany is a defect in Australia. Ask the layout question
   separately and early. In the source session it was researched only after the résumé had been
   through seven rounds, and it moved the body from 10.5 to 11pt, the headings from capitals to
   sentence case, and found that Australian guidance accepts three layouts by channel rather
   than one.
2. **Industry conventions.** What a résumé in this field is expected to evidence, and which
   certifications actually appear in ads rather than in advice articles.
3. **The specific employers.** Which applicant tracking system each runs, the vocabulary in
   their current ads, how they interview, their stated values, whether the internal and
   external application paths differ, and any CV guide of their own. One employer group's guide
   said "a CV can be 3-4 pages long" while every public source said about two. This is the part generic advice cannot supply and the
   part that most changes the document.
4. **How automated screening works now.** What parsers do with layout, whether keyword stuffing
   is read as such, and what a model-based screen weighs.

## Lanes

Run several independent lanes and reconcile them. One report is one model's reading.

**Deep-research MCP (Dossier).** Through the router these are `dossier__research_plan`,
`dossier__research_start`, `dossier__research_status`, `dossier__research_export`,
`dossier__research_budget`, `dossier__research_doctor` — 39 tools in all; the harness prefixes
them `mcp__router__`. Plan first: `dossier__research_plan` and `dossier__research_local_start`
are free. A paid panel run is a spend, so say what it will cost and get the person's agreement
before starting one. Start each provider as its own run with a label and tags, poll
`research_status`, and export to the project's `research/` directory.

**A hand-written prompt for the person to run themselves.** Where they have a deep-research
subscription of their own, write the brief and put it on their clipboard
(`pbcopy < prompt.md`), then take the report back as a file. Write this brief by hand: a
research tool's own auto-generated prompt is templated for its usual subject and in the source
session produced a legal-research template for a résumé question.

**A headless run of another model.** A background CLI run can be pinned to a specific model
where the in-session agent tool cannot. Tell it to use web search only, to spawn no subagents,
and to weight primary sources in the person's own country.

**Direct checks.** Anything two reports disagree about gets settled against the primary source:

```bash
curl -sL -A "<a browser user agent>" "https://<employer>/careers" | grep -oE \
  "myworkdayjobs\.com|oraclecloud\.com/hcmUI|taleo\.net|avature\.net|pageuppeople\.com|successfactors|eightfold\.ai"
```

That one grep settles which ATS an employer runs, which two reports will otherwise argue about
indefinitely. Check the internal careers section separately: a large employer often runs a
different system for internal applicants than for external ones.

## The digest

One file. Every claim tags which lanes support it, with a separate mark for anything verified
directly. Where lanes conflict, say so and say which evidence settled it. Where a claim has one
lane and no verification, mark it as such rather than promoting it.

`dossier-report:dossier-report` will build this digest from the exported reports.

Give the digest a short table of limits: the sections and their order, the length of the
summary, the number of bullets per role, the page count, the type sizes and margins, the file
type for a portal. The documents are built to those and may later be judged against them, so a
departure has to be a decision somebody made.

Quote a source only from its own page. A report's quotation is a lead, not a quote: in the
source session one report quoted a recruiter as saying "months as well as years", which its page
does not say, and another attributed a type specification to a recruiter whose page gave other
sizes. Before a quotation reaches anything the person or an employer reads, open the page, copy
the sentence, and record the date you checked it. Where a page cannot be opened, because it builds
its text in the browser or refuses the request, say so beside the quote and give the wording as
the report's.

Check what a cited page shows as well as what it says. A source cited for "one column" can link a
template that is not one: the source session's cited job-board page linked three "ATS-optimised"
templates, two of them built with a sidebar from Word tables, and another of its articles
recommended two columns on page one. Open each page, look at its own example layout, and record
in the digest whether it matches the claim it is cited for, so a reader who follows a citation
does not find the opposite advice.

Where a deep-research report's copy and export controls are unavailable, as with one browser
report in the source session, read its text from the page's accessibility tree and say so in the
file's header; citation chips then arrive as fragments, and the source list as link titles
without addresses.

Keep the digest's claim tags, because stage 3's review page cites them: a finding whose "why it
matters" points at a four-lane verified claim is worth more than one pointing at a single
report, and the reader can see the difference.

## What research cannot settle

Anything about this person's own work, and anything about what they are comfortable publishing.
Those are stage 4's questions, and no amount of research substitutes for them.
