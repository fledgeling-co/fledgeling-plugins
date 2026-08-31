# What you emit

The authority is `libs/shared/src/investor-portal/portal-contract.ts` in the dAIolog repo. Read
it — it is short, it is Zod, and it validates. This file is the orientation, not the spec.

```jsonc
{
  "companyId": "…", "slug": "acme-paid", "category": "paid",
  "title": "Acme Limited (ASX:ACM) - Investor portal",
  "status": "draft",

  "theme":  { /* lifted from DESIGN.md; see tokens-and-motion.md */ },
  "assets": [ { "id": "hero", "url": "…", "alt": "…", "origin": "crawl" } ],

  "chrome": { "header": {…}, "tickerTape": {…}, "footer": {…} },

  "pages": [{
    "pageId": "home", "path": "/", "title": "…",
    "seo": { "noindex": true },
    "sections": [{
      "id": "facts", "kind": "companyFacts", "enabled": true, "order": 1,
      "band": "canvas", "divider": false,
      "eyebrow": "§01 · Company facts", "heading": "…", "sub": "…",
      "motion": { "kind": "reveal" },
      "assetIds": [],
      "props": { /* this kind's own shape */ }
    }]
  }],

  "ledger":  [ /* every illustrative value, with its reason */ ],
  "omitted": [ /* what was left out rather than authored, and why */ ]
}
```

## The slug is not the subdomain

Two different identifiers, and conflating them collides two companies:

- **The subdomain label** derives from the company's legal name: `acme-limited`.
- **The portal slug** is `<label>-<category>`: `acme-paid`, `acme-free`. It is **globally
  unique across every company**, which is why the category is part of it.

## `chrome` is load-bearing, and an empty object is not a value

`chrome: {}` validates and produces a portal with no brand, no navigation and no footer. On a
real generator that literal shipped to **every record it had ever produced** — nine of them —
and the consequence was invisible everywhere it was checked: the records validated, every route
returned 200, and the content assertions passed. Measured on one tenant, five pages carried
**zero internal links** and **one tab stop**, the skip link. Two declared routes resolved 200
with nothing on the site pointing at them.

So `chrome.header` is built from `identity` plus the pages the record actually declares, and
two invariants ride with it:

- **Every declared page is reachable from at least one other.** An orphan route is
  indistinguishable from a working one in every per-page check ever written.
- **Nothing about a specific company lives in a shared component.** A footer with one tenant's
  monogram, listing code and policy PDF links as literals publishes that company's constitution
  under every other tenant's address the moment the footer starts rendering. Until that is fixed,
  synthesising a footer *creates* the leak rather than closing it — which is why an absent footer
  is the honest state and a wrong one is not.

### The residue that survives the obvious pass, and how to see it

The monogram and the PDFs get found because they are proper nouns. Four literals survived that
pass on a real build, and every one of them was found by **opening a generated tenant's footer
and reading it**, not by grepping for a company name:

| What rendered on the second tenant | Cause |
|---|---|
| `ABN ᴹ` — the word, a space, and a lone illustrative-value marker | `abn: ''` rendered unconditionally |
| a **Share registry** heading over an empty marker and a link to `""` | `registry` / `registryUrl` rendered unconditionally |
| `© 2026 Metallium Ltd. 0 sites across NSW and Queensland.` | the reference's two *states*, hard-coded, under a Western Australian company, over a count of nothing |
| "the document lodged with **ASX**" | a literal venue, on every NASDAQ and NYSE tenant |

Two rules generalise out of them:

- **A labelled block renders only where the record holds something to put in it.** A heading
  over an empty value is worse than the absence: it asserts the field exists and that this
  company has nothing for it. The same applies to a derived count — `0 sites` is not a fact,
  it is a template that did not get its data.
- **A jurisdiction, venue or regulator is read from the record, never written into the
  component.** The listing code the footer already carries (`"ASX: AAL"` → `ASX`) is the venue;
  taking it from there rather than adding a prop also fixes every record written before the
  field existed.

## `composition` and the two proportion axes: absence is a choice, not a default

Three fields added to the contract after the convergence problem was counted. All three are
optional, and all three have a default that IS the reference build — which is exactly why leaving
them out is not neutral. A record that states none of them renders as the tenant every other thin
record renders as.

**`section.composition`** — which of a kind's layouts to draw. Four kinds offer a set today, and
`SECTION_COMPOSITIONS` in `portal-contract.ts` is the vocabulary rather than anything written here,
so read it there before emitting:

```
hero          editorialSplit | statement | dataForward | index
companyFacts  table | definitionGrid | ledger
unitList      mediaRows | stack | indexRows
quickLinks    tiles | list | marquee
```

The first value of each list is what that kind drew before the field existed. A value the kind does
not offer is refused at record level, not reverted — a silent revert is indistinguishable from
never having asked, which is the failure this whole file is written against.

**`theme.structure.density`** — `comfortable` | `compact` | `editorial`. Moves the container, the
prose measure and the SECTION rhythm. It deliberately does not move the micro-spacing steps: a
button whose padding shrank because the brand asked for a denser page is a component regression
wearing a brand's name.

**`theme.structure.typeScale`** — `classic` | `tight` | `dramatic`. The display-to-body ratio, and
the axis that survives a change of typeface.

### Deriving them, and what the derivation may claim

`design-md-from-website` measures both proportion inputs and writes them down — a container width in
the layout tokens, a display size in the type table. Read the company's own figure and record the
bucket. The record carries the bucket, never the number: a measured length piped into a custom
property is the `measuredGrid` defect, which stays forbidden.

One trap, measured. The display size sits on a line whose earlier value is itself a token
reference — `display: { fontFamily: "{typography.font-display}", fontSize: "60px", … }` — so a
regex bounded by `[^}]*` stops at the brace inside that reference and never reaches the size. It
returns null silently and the axis resolves to `classic` on every brand forever, which is the
silent-default failure these fields exist to remove. Scope the match to the line.

**Say what the boundaries are.** They are placed relative to the reference build's own 1200px
container and 72px display cap. They are NOT medians over a corpus the way
`SITE_BOUNDARIES.editorialSplitMajor` is, and a corpus run on 31 Aug 2026 reached one of five sites
— the rest now refuse automated access or no longer resolve. Use them, and do not describe them as
measured.

## Sections switch off; they do not empty

`enabled: false` is the mechanism for "this company has no video". A section rendered with
nothing in it reads as broken; its absence reads as a company that does not publish video.

Corollary: a section must look right anywhere in the order, because with sections toggling you
cannot know its neighbours. Band alternation is derived at render time, so choose `band` for
meaning (`dark` for the company's own world, `sunken` for context) rather than for rhythm.

## Provenance, which the contract enforces

| `from` | carries | must not |
|---|---|---|
| `record` | `asAt`, `source`, `sourceHref` | — |
| `illustrative` | `why` (required), a `ledger[]` entry (required) | cite `sourceHref` |
| `unavailable` | a `label`, and a `reason` | carry a `value` at all |

**There is no default.** An omitted `from` is a validation error. It used to default to `record`,
which meant an omission silently made the strongest claim available — the single most dangerous
line in the first version of this contract.

### `unavailable` needs a reason, because one state cannot say two opposite things

"We are not obliged to hold this" and "we are obliged and do not" render identically today, and
they mean opposite things to a reader and to a regulator. The reason codes:

| `reason` | means |
|---|---|
| `notRequired` | this entity has no obligation to prepare or hold it |
| `notPrepared` | required of some entities, not prepared by this one |
| `notLodged` | prepared and not yet lodged with the exchange |
| `notHeldByPortal` | it exists and is lodged; we do not hold a copy |
| `awaitingApproval` | held, and not cleared for the portal |
| `sourceConflict` | two sources disagree and neither has been resolved |

`notHeldByPortal` is the honest state for an optional document. It is **not** the honest state for
a mandatory current disclosure: there, the research is explicit that a visible unavailable does not
cure a legal omission, and the prescribed handling is a publication block plus escalation
(`references/evidence.md`, E10). The gate cannot make that call for you, because deciding what is
mandatory needs the entity classification the record does not carry — so it is a named limit rather
than a silent pass.

**And the marker has to be readable.** WCAG 1.4.1: information carried by colour or by a glyph must
also be available as text. `ABN ᴹ` — a label, a space, and a lone superscript marker — is the
failure, and a pale blank is the same failure with less to see.

### The fields a figure should carry, beyond the three it already does

The research panel's minimum source-bound representation for a displayed financial figure is longer
than `asAt` / `source` / `sourceHref`, and three of its additions are worth having because each
names a real error class:

- **`unit` and `currency`.** A figure without a scale or a currency is the arithmetic-error channel:
  `4.2` is not a number a reader can use, and `$4.2m` and `A$4.2m` are different disclosures.
- **`assuranceStatus`** — audited / reviewed / unaudited / forecast / management estimate. An
  unaudited management estimate rendered in the same type as an audited figure is a claim the record
  never made.
- **`precision`**, in words, where the source's precision is coarser than the field's — see
  "Precision is a claim" below.

The full list the research proposes also covers `period_start` / `period_end`, `source_page`,
`retrieval_timestamp`, `source_hash` and `calculation_expression`. Those are a filing-grade schema
rather than a portal record's; they are recorded in `references/evidence.md` so the case for adding
one later does not have to be rebuilt from scratch.

Category rules the schema enforces, so you cannot ship past them:

- a **free** portal rejects any illustrative value outright — there is no third option on the
  record-only surface
- a **report** rejects them too; a fabricated detail in a compliance artifact is worse than a
  missing one
- a **paid** portal rejects an illustrative value that is not in `ledger[]`, because the
  "what is illustrative here" page is generated from that array
- a category may only place the section kinds it owns

## Precision is a claim

If the overview publishes month-and-year against a disclosure, emit month-and-year. Inventing a
lodgement day to make a timeline tidier fabricates specificity the record does not support, and
on a regulated surface a fabricated date is a fabricated fact. Say the precision you hold, in
words, in the section's `sub`.

Do not derive figures either. Market capitalisation from price × shares is arithmetic, not data;
if either input is unavailable, the output is `unavailable`, not approximate.

## A kind's props are claims, not fields

The most expensive defect this generator has shipped was not an invented figure. It was prose put
into `governanceGroup.docs[]`, whose renderer draws a PDF affordance per row, counts the rows into an
**"N documents"** heading, and reserves a date column. Eleven prose items became eleven documents a
company does not publish, on the page where that claim matters most. The array validated, the route
returned 200, and the tokens were right.

So before choosing a kind, read what its renderer **asserts** about whatever you hand it — a count,
an affordance, a date, a marker, a badge — and check each assertion against the material. A field
that merely *accepts* your data is not a field that *means* your data.

Three that carry claims worth checking against the source every time:

| Kind | What it asserts beyond the values |
|---|---|
| `governanceGroup` | these are lodged documents; there are N of them; each has a date and a PDF |
| `latestDisclosures`, `announcementTimeline`, `reportIndex` | these were released to a market operator |
| `companyFacts` with `leadFigures` | these are the figures a reader should carry away |

Where the material is prose the company publishes rather than documents it lodges, `values` renders a
name and a body and asserts nothing about a document existing.

## Six shapes that look like data and are typography

Each of these is a field whose *rendering contract* is not what its type suggests, and each has
produced a visible defect:

- **A hero `headline` array is LINES.** The line-mask wraps every element in its own
  `display:block`, so `['We build the system underneath ', 'sustainability', '.']` gives the full
  stop a line of its own. Two elements, and the stop travels with the word it ends.
- **`identity.freeHeadline` is the OPPOSITE** — `[before, emphasised, after]`, inline runs, where a
  trailing `'.'` is correct. Same-shaped array, opposite semantics, and nothing in the record
  distinguishes them.
- **`prose` renders one `<span>{props.body}</span>` and no eyebrow or heading.** An array body
  renders run-on with no separators, and an eyebrow or `index` on it is written and never drawn.
- **A `§` ordinal only counts if its kind renders an eyebrow.** Put one on a kind that does not and
  the *rendered* index gains a gap, which is the completeness claim the ordinal exists to make.
  Which kinds render one is empirical — read it off a capture, not off the record.
- **A `badge`, `chip` or `eyebrowBadge` string does not wrap.** A 68-character eyebrow measured 471px
  inside a 375px viewport and scrolled the whole document sideways. Write them to fit a phone.
- **The `ledger` is joined to the page by LABEL.** A ledger entry whose label qualifies the figure's
  own label ("AASB S2 readiness, governance" against a figure labelled "Governance") does not match,
  and the value reads as undisclosed. Generate the ledger **from the values** rather than writing it
  beside them, and the join cannot drift.

## Writing `chrome` replaces it, so carry every field it had

`chrome.header` is an override, and it is taken **wholesale**: the layout uses
`header ?? headerFromRecord(record)`. Omit one field and you get the component's default, which on at
least one field is the reference tenant's own literal — a header written without `mark` published
`AE`, Alfabs' monogram, on another company's masthead.

The footer merges (`{...footerFromRecord(record)} {...(footer ?? {})}`) and the header does not, so
the two behave differently from the same-looking record edit. Prefer writing no `chrome` at all and
letting the layout derive it; write one only where derivation gives the wrong answer, and then carry
every field the derived version would have set.
