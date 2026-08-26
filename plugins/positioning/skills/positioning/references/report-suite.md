# The report suite — nine documents, all templated

The predecessor shipped three markdown files (one per territory) and one HTML
page. Everything else the run learned — what the research cost, which claims
were verified, which candidates were cut, what shipped versus what is designed —
existed only in the conversation, which is to say it existed until the terminal
scrolled.

This suite is the run's memory. Every file has a template in
`assets/templates/`, every file is written even when a section is empty, and an
empty section says why it is empty rather than being dropped.

**All nine land in `docs/positioning/`.** The exported research sits beside them
in `docs/positioning/research/` and the ledger in `docs/positioning/work/`; see
the layout in SKILL.md. A run that scatters its output across the working root
leaves the next run unable to find it, and that has already happened once.

| # | File | Template | What it is for |
|---|---|---|---|
| 1 | `00-decision.md` | `decision.template.md` | The recommendation and the case for it. The one document a founder reads. |
| 2 | `10-territory-<slug>.md` | `territory.template.md` | One per shortlisted territory. The full positioning, all four frameworks, bound to ids. |
| 3 | `20-category-and-competitors.md` | `category.template.md` | The category line, who holds it, what they claim, where they are heading. |
| 4 | `30-customer-evidence.md` | `customer.template.md` | Segments, jobs, the words buyers use, with every quote carrying its URL and date. |
| 5 | `40-evidence-register.md` | `evidence-register.template.md` | The claim ledger rendered: claim, confidence, independent domains, verification verdict. |
| 6 | `50-product-truth.md` | `product-truth.template.md` | The truth table rendered, with the claimability count per territory. |
| 7 | `60-candidates-cut.md` | `candidates-cut.template.md` | What was generated and not shortlisted, and what killed it. |
| 8 | `70-research-decision.md` | `research-decision.template.md` | What was bought, from whom, for how much, and what was deliberately not bought. |
| 9 | `80-pre-commitment-tests.md` | `pre-commitment.template.md` | What to test before betting on the recommendation, and what each test would have to show. |

Numbered prefixes because a `docs/positioning/` directory sorted
alphabetically otherwise opens on `category-and-competitors.md`, and the
decision is the document people need first.

## Rules that hold across all nine

**Every number carries its provenance.** A figure in any of these files is
either bound to a claim id from the ledger, or marked as an estimate with the
reasoning shown, or absent. There is no fourth option. A number that appears
with neither a claim id nor an estimate marker is what `positioning_lint.py`
reports as an unsourced figure, and it is the single most common way a
positioning document becomes indefensible three weeks later when somebody asks
where 68% came from.

**Confidence travels.** A claim held at low confidence hedges in every document
that repeats it, including the executive summary. The executive summary is where
hedges go to die, because it is the section written last, shortest, and most
enthusiastically. Write it from the ledger rather than from memory of the
research.

**Contested findings stay contested.** Where two panel members disagreed, both
positions appear, attributed, in `40-evidence-register.md`, and any territory
resting on the contested claim says so in its risks section. Silently resolving
a disagreement is the most expensive kind of tidying.

**Say what was not covered.** Each file ends with what it could not establish
and why: the segment nobody writes about publicly, the competitor with no
pricing page, the geography the panel had no sources for. A gap named is a
research question; a gap unnamed reads as an absence of risk.

## `00-decision.md` — the shape that survives a founder reading it

Order matters more here than anywhere else, because this file gets read from the
top and abandoned somewhere in the middle:

1. **The recommendation, in one sentence**, with the territory's hero line
   quoted, and the confidence attached to it.
2. **Why this one** — three bullets, each naming the evidence and its claim id.
3. **What it costs you** — what leading with this position gives up. Every
   position forecloses something; a recommendation that names no cost is a
   recommendation nobody checked.
4. **The shortlist table** — every territory, one row, the four axes, the
   claimability count, and the strongest objection to each.
5. **What has to be true** — the assumptions the recommendation rests on, each
   with the pre-commitment test that would check it.
6. **What to do on Monday** — the concrete next actions, in order, with the
   three that are reversible marked as reversible.
7. **The guardrails** — what not to say, including the specific claims the
   ledger refuses and why.

Section 3 is the one that gets skipped. Include it.

## Length

`00-decision.md` runs 400–800 words. A territory file runs 900–1,400. The
evidence register is as long as the evidence. Nothing here is padded to look
thorough: a founder who wanted a thick document would have hired a consultancy,
and the thickness would have been the product.
