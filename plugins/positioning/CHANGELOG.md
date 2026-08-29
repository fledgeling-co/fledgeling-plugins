# Changelog

## 0.1.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

## 0.1.0

First release. A rebuild of `positioning-pipeline` 1.0.1 by DiologIR, which is
credited in the README and whose four-book distillation, territory template and
product-research persona are carried forward.

**Research runs inside the pipeline.** The predecessor emitted two Gemini Deep
Research prompts and a launcher page and asked the user to run the research in a
browser. This runs Dossier panels itself across the free CLI lane and the paid
API lane, decomposed by archetype, and keeps the verification: citation
resolution, judged claim-source verification for anything entering promissory
copy, four-lens counter-review, and a deterministic merge that counts support in
independent registrable domains rather than in how many backends agreed. The old
workflow survives as `references/gemini-lane.md`, with what you give up by taking
it stated in the file.

**The weighted-slider scorer is gone.** All four members of the first research
panel independently found the family documented-unsafe for a 3-5 option strategic
choice: rank reversal under sum normalisation, splitting bias moving a criterion
from ~0.25 to 0.40-0.48, range insensitivity, equalising bias across all five
elicitation methods tested, and compensability that lets a trivial high score
outvote a fatal failure. `references/decision-aid.md` replaces it with vetoes,
a natural-unit consequence table, dominance screening, even swaps, rank stability
across plausible weights, scenario regret, and a permitted no-decision output.

**Two gates instead of two prose rules.** `scripts/claim_ledger.py` binds every
positioning move to a product-truth row and a verified claim, and fails when a
hero line rests on unshipped capability, on an unverified citation, or on a
confidence label claimed across too few independent domains.
`scripts/positioning_lint.py` fails on breadth-led framing, unsourced figures,
territories sharing any of the four distinctness axes, an abstract owned word, an
Eliminate row that eliminates nothing, and HTML with an unpinned external asset
or motion with no reduced-motion branch. Both proven in both directions: 41
errors on a broken fixture, 0 on a clean one.

**Candidates before research.** Generation moved ahead of the panels and routes
through `/trawl:trawl` with five positioning-shaped personas, so the research
discriminates between named candidates rather than describing the market. The
status quo is carried as a labelled option throughout.

**Nine templated reports and one designed decision page**, built through
`/design-craft` and `/ux-craft` against the project's DESIGN.md or an authored
one, and gated by a `/design-review` pass before the user sees it.

**Evidence labels.** A territory is `recommended`, `conditionally recommended`,
`promising hypothesis`, `not recommended` or `no decision`, with the tier of
evidence each requires. A desk-research run produces `promising hypothesis` at
best and says so.
