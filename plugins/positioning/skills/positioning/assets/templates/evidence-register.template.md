# {{PRODUCT}} — Evidence register

Every claim any positioning move rests on. Generated from `ledger.json`; do not
hand-edit — re-render it with `claim_ledger.py`.

**Panels:** {{PANELS}} · **Members completed:** {{COMPLETED}}/{{DISPATCHED}} · **Cost:** {{COST}}
**Citations:** {{RESOLVED}}/{{TOTAL_CITES}} resolve · {{JUDGED}} judged for support
**Counter-review:** {{COUNTER_REVIEW}}

## How to read the columns

- **Domains** counts *independent registrable domains*, not panel members. Four
  backends citing one page is one domain. A high-confidence claim needs three.
- **Verified** is `link` (the URL resolves), `judged` (a model read the page and
  found it supports the claim), or `no`. Only `judged` claims may carry
  promissory copy: on Dossier's 30-case labelled corpus, token containment
  passed 11 of 23 bad citations, including 4 of 7 outright contradictions.
- **Contested** means panel members disagreed. Both positions appear below.

| id | Claim | Conf. | Domains | Verified | Contested | Bound to |
|---|---|---|---|---|---|---|
| {{CLAIM_ROWS}} | | | | | | |

## Contested findings, both sides

{{CONTESTED_SECTION}}

## Claims gathered rather than reported

Quotes read directly from source (`reddit_gather`, `youtube_gather`) carry their
own URL and date. A quote a research report merely *reports* is a claim about a
quote and is labelled as one.

{{GATHERED_SECTION}}

## Claims that entered no recommendation

{{ORPHANS}}

Not waste: these are the findings that did not discriminate between territories,
and they are the first place to look when a new candidate appears.

## What the panel could not establish

{{GAPS}}
