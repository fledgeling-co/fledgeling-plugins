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
