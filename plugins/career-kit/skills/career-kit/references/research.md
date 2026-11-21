# Research — four subjects, several lanes, one reconciled digest

## The four subjects

1. **Country conventions.** Length, photo, personal details, date format, education placement,
   what is illegal to ask for. These differ sharply: a convention that is correct in Germany is
   a defect in Australia.
2. **Industry conventions.** What a résumé in this field is expected to evidence, and which
   certifications actually appear in ads rather than in advice articles.
3. **The specific employers.** Which applicant tracking system each runs, the vocabulary in
   their current ads, how they interview, their stated values, and whether the internal and
   external application paths differ. This is the part generic advice cannot supply and the
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

Keep the digest's claim tags, because stage 3's review page cites them: a finding whose "why it
matters" points at a four-lane verified claim is worth more than one pointing at a single
report, and the reader can see the difference.

## What research cannot settle

Anything about this person's own work, and anything about what they are comfortable publishing.
Those are stage 4's questions, and no amount of research substitutes for them.
