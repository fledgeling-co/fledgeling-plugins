# The LinkedIn document — paste-ready, in LinkedIn's own order

One Markdown file the person works down with the profile open beside it. Every block is final
text to paste, not advice about what to write.

## Order

1. **Headline.** Their real title and what they do, in plain words. It is read by people
   before it is searched, so it is not a string of keywords.
2. **About.** First person, their voice, opening with what they are responsible for now, then
   the career most recent first, then what they care about in the work. Search terms belong
   in the Skills section, which is what LinkedIn's search reads; the About section carries
   none.
3. **Experience**, one entry per role, every role under the employer's official company page so
   the years aggregate correctly.
4. **Skills**, in LinkedIn's own standard terms, with the three to pin named explicitly. This
   section is a search index and reads as a list; the person's strengths are carried by the
   About section and the role descriptions.
5. **Settings** — the profile URL, Open to Work visibility, whether the "notify network"
   toggle should be off while they edit (it should), the banner.
6. **What to delete** — stale roles, a skills list from a previous career, old contact details.
7. **What stays off a public profile** — every figure the person restricted, internal system
   names, incident counts, anything their employer's social media policy covers.

## Rules that differ from the résumé

- Titles, employer and dates match the résumé exactly. A recruiter comparing the two is
  checking for that, and it is the cheapest discrepancy to avoid.
- The public copy is the softened one. Where the résumé carries a figure for an internal
  application, LinkedIn gets the sentence without the number.
- The role descriptions follow `career-kit:resume-craft`: a first-person scope line, bullets
  opening with a past-tense verb, one headline and one support each, and only figures that
  enlarge the reader's impression.
- State moves between roles as moves. Call one a promotion only where the person has
  confirmed it against their employment record.
- The profile address printed on the résumé and linked from the website is the one that
  exists today. Change it only in the same sitting as both, and check that it resolves;
  LinkedIn refuses automated checks, so that takes a click.

## Gaps

Mark anything still unknown in the document itself as a placeholder in angle brackets, such
as `<what the award recognised>`, in the place the answer goes. A gap in a paste-ready document is visible; a gap listed at the end is not.

## Updating the profile

An agent editing the live profile needs a browser signed in to their account, or the `linkedin`
MCP server in this router (24 tools, harness prefix `mcp__router__`, including
`linkedin__get_my_profile`). Neither was used in the source session, which produced the
document for the person to paste.

Editing someone's live profile is an outward-facing action. Do it only when they ask for it
explicitly, and never as part of finishing the document.
