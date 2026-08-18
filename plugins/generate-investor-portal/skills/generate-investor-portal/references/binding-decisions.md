# Binding decisions

> **This copy is the one that binds.** The same file exists in `create-investor-portal-free`, which
> is where these decisions were first written and which remains the **visual** reference for the
> hand-built page. Two copies of one truth drift, and the drifting one is always the one nobody
> cites — so this plugin's SKILL.md points here, and only here, for the content decisions. If the
> two ever disagree, treat the one the running skill loads as authoritative and reconcile
> deliberately rather than by whichever was edited last.
>
> `create-investor-portal-free`'s `what-the-research-says.md` and `page-structure.md` are **not**
> duplicated here and still bind on page structure. Read them there.

These are review outcomes from a real build. Where one of them meets an inference from
`what-the-research-says.md`, **this file wins** and the reasoning below explains why the two
are not actually in conflict. Read this before drafting, not after.

## The H1 says what the company says about itself

Take the headline from the company's own website language in the overview file, not from a
positioning line you write. An issuer describing itself as "mining and engineering services in
the Hunter Valley" gets that, not "Heavy engineering for the region, listed on the ASX."

*Reconciles with:* the research's first cold-visitor question, "what does this company actually
do, in one sentence." The company has already answered it, in words its own site and
announcements use. Rewriting that for rhythm makes the page's most-read line the one sentence
on it that no disclosure supports.

## Never "investor hub"

The surface is an **investor portal**. Applies to the H1 area, the brand lockup sub-label, the
nav, the footer column heading, the `<title>`, the meta description, and any prose.

## No "official company source" badge

The research names "is this the official source" as a question the visitor arrives with. A
badge asserting it is the wrong instrument: a self-applied claim, unverifiable from the page,
and exactly what a spoofed page would also say.

Answer it with evidence instead, which the page already carries:

- the registered office, and the ABN, in the footer
- the share registry named
- "Released via ASX MAP" provenance on each announcement
- every fact carrying its source disclosure and an as-at date
- the domain itself

## The facts table excludes ABN and unquoted securities

Keep: legal name, ASX code, ordinary shares on issue, net debt, dividend status, employees,
board, company secretary, registered office, share registry, financial year end.

**ABN** belongs in the footer's registered-office block, where a reader looking for corporate
identity actually goes, and where it is not competing with the figures that move.

**Unquoted securities** (performance rights, options) is detail for a capital-structure
section, not a headline fact. It dilutes a table whose value is that every row is a fact
someone might quote.

*Reconciles with:* the research's machine-readable company-facts finding, which is about the
facts being **dated, sourced and structured**, not about their number. A shorter table where
every row earns its place serves that finding better than a longer one.

## No broker list

Do not enumerate brokers with their fees. It reads as endorsement, it is stale the day it
ships, and the fee data is unsourceable from the company's own disclosures.

Say plainly that the shares trade under the code on the exchange, that any broker with access
can buy them, and explain CHESS-sponsored versus custodial holding, which is the part that
actually affects the reader.

## The Diolog banner line is fixed

> A direct line to the companies you own.

It is the live for-investors headline, and it states what an investor gets. Do not replace it
with a hosting credit ("this portal runs on Diolog"), a single action ("ask this company a
question, free"), or a feature list. Read `diolog-layer.md` for the rest of that section.

## No issue-ID labels on this surface

`ISS-01`-style identifiers belong on the disclosure-consistency artifact, where a Disclosure
Committee cross-references findings between sections. On a public portal they are internal
apparatus and read as leaked tooling.

## Nothing is invented

Every figure, name, date and quotation traces to the supplied overview or design file. Where a
fact is needed and absent, either leave the row out or mark it a visible placeholder naming
what is missing. Sample or illustrative content is disclosed as such in the footer, in plain
words, and the page carries `noindex` for as long as that is true.

Ordinary consequences of this rule, each of which was caught in review:

- no report IDs or reference numbers you made up
- no owner, due-date or "blocks release" metadata unless the source carries it
- no attribution ("corroborated statement 07") the source does not state
- no timing labels on next steps the source did not give
