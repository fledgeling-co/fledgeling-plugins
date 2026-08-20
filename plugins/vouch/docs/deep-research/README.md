# Research corpus

The research this skill's tax-classification guidance rests on, exported so the claims in
`skills/vouch/references/evidence.md` stay auditable from inside the plugin.

## rdti/ — the Australian R&D Tax Incentive

A five-backend panel run in August 2026 at a metered cost of US$20.32 across 110 sources.
Four reports plus their source lists; the fifth backend refused to start and is reported
as absent rather than dropped.

| File | Sources |
|---|---|
| `rdti-gemini.md` | 44 |
| `rdti-claude.md` | 27 (run locally, no metered cost) |
| `rdti-openai.md` | 21 |
| `rdti-perplexity.md` | 18 |

Read the whole of a report before relying on a finding from it, and check the matching
`.sources.md` — a URL that resolves is not the same as a URL that supports the claim.

**What the panel settled**, and what the skill does with it: eligibility under Division 355
of the *Income Tax Assessment Act 1997* attaches to activities rather than to suppliers, so
there is no eligible-vendor list and no percentage a tool can assert. Expenditure on core
technology is excluded by s 355-225(2). Notional deductions are tax-exclusive where the
entity is registered, there is a statutory minimum before the offset is available, and the
Commissioner's named apportionment method for period-of-use expenditure is R&D hours over
total employee hours.

The consequence is the rule in `SKILL.md`: a classification column states a **default
position on the face of the expense**, says so in the report, and hands the
characterisation to the accountant. The skill states arithmetic and cites documents.

## Scope of this corpus

One jurisdiction. Nothing here supports a classification column in any other tax system,
and the column is optional for that reason — omit it and the reports drop it entirely.
