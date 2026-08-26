# Evidence — where every rule in this skill comes from

Two Dossier research panels, seven backends, read end to end and exported to
`docs/deep-research/`. Each rule below names the finding it rests on, the study,
and whether the panel agreed. **Where members disagreed, both positions are
here.** A rule with no citation is a design choice and is marked as one.

## Panel 1 — positioning validity, pre-commitment testing, decision aids

Dispatched 26 Aug 2026 as a 5-backend panel, archetype `academic`, tier `max`.

| Member | Model | Sources | Cost | State |
|---|---|---|---|---|
| openai | gpt-5.6-sol | 46 | ~$9.00 | completed |
| gemini | deep-research-max-preview-04-2026 | 74 | ~$7.00 | completed |
| perplexity | sonar-deep-research | 20 | ~$4.00 | completed |
| local-claude | Claude Code | 22 | $0.00 | completed |
| local-agy | — | — | $0.00 | **refused at startup**: binary identity check |

Merged deterministically with `research_synthesise`: **160 distinct sources
across 38 independent domains, 1% overlap between members.** That low overlap is
the case where merging earns its cost — and it means any claim only one backend
made is uncorroborated rather than agreed.

**A quality finding about the panel itself.** The gemini member's export carries
visible citation corruption — truncated `<cite url=)` fragments and sentences
that break mid-clause where a citation should be — and every one of its 74
sources is a `vertexaisearch.cloud.google.com` redirect, which collapses to a
single registrable domain and drove the merge's "largest single domain 46%"
warning. Its source mix leans on marketing blogs where the other members reached
primary literature. Its findings are used here only where a second member reached
the same primary source independently. This is the source-laundering failure mode
the second panel was commissioned to study, appearing in the first panel's own
output.

## The findings that changed the design

### 1 · The weighted-sum scorer is documented-unsafe for this job

The predecessor's centrepiece. All four members reached it independently.

- **Rank reversal.** Belton & Gear (*Omega*, 1983) proved that adding an
  irrelevant alternative can flip the order of the top two under sum
  normalisation; Wang & Elhag (*Decision Support Systems*, 2006) for AHP's
  distributive mode; Mohammadi (*J. Multi-Criteria Decision Analysis*, 2023) for
  weighted-sum normalisation generally. Monte Carlo work finds reversal
  probability rises when alternatives are few and close in value.
- **Splitting bias.** Weber, Eisenführ & von Winterfeldt (*Management Science*,
  1988, N = 128): an attribute weighted ~0.25 as one criterion reached 0.40–0.48
  split into three. Jacobi & Hobbs (*Decision Analysis*, 2007) replicated the
  effect on value trees.
- **Range insensitivity.** UK HM Treasury Green Book MCDA supplementary guidance:
  weights must represent the value of the swing between worst and best observed
  consequences, not abstract importance.
- **Equalising bias across every method tested.** Rezaei et al. (*J. Behavioral
  Decision Making*, 2022) compared AHP, BWM, SMART, swing weighting and point
  allocation; all five showed it.
- **Preference construction.** Payne, Bettman & Johnson, *The Adaptive Decision
  Maker* (Cambridge): preferences are constructed during elicitation, not
  retrieved.

**Where members disagreed:** local-claude said replace outright ("Do Not Use");
openai and perplexity said retain it as an *inspectable sensitivity view* while
removing it from the recommending role. The skill takes the second reading — the
weighted view is shown as rank-stability across plausible weights, never as a
rank — because two of three converged and it preserves what users expect to see.

**The honest limit, stated by openai:** `<INSUFFICIENT_EVIDENCE>No controlled
study establishes that weighted sum, AHP, BWM, SMAA, outranking or regret
analysis chooses more commercially successful positioning strategies.</INSUFFICIENT_EVIDENCE>`
The replacement is not a better oracle. → `decision-aid.md`

### 2 · Category creation is high-variance, and the popular counter-statistic is circular

- Golder & Tellis (*Journal of Marketing Research*, 1993; ~500 brands, 50
  categories, built from historical records rather than surveys of survivors):
  **47% of pioneers failed**, surviving pioneers averaged **~10% share** and
  remained leaders in only 11% of categories; **early leaders averaged ~28%
  share, failed ~8% of the time, and entered ~13 years later**.
- Play Bigger's "category kings capture 76% of category market capitalisation"
  defines a category king *by dominance* and then measures the dominant. openai
  traced the methodology: ~702,000 firms screened to 2,694 usable transactions,
  with market cap, acquisition price and private valuation used interchangeably.
  It is descriptive of selected winners, not an attempt-level success rate.
- Ahn et al. (*Strategic Management Journal*, 2026): meta-analysis of 90
  category-spanning studies, 154 effect sizes, 13,346,009 observations. Overall
  partial correlation with audience appeal **r = −.003, p = .187, 95% CI
  [−.007, .001], I² = 97.03%** — no universal penalty or premium, extreme
  heterogeneity, with moderators (bounded category systems, third-party
  assignment, simultaneous rather than sequential spanning).
- Sujan & Bettman (*Journal of Marketing Research*, 1989): moderate discrepancy
  produces differentiation inside the category; strong discrepancy produces a
  subtype or niche.

**Carried as contested.** "Market pioneer", "category creator", "category king"
and "subcategory entrant" are different constructs; no defensible
category-creation-versus-subsegment success rate currently exists.
→ `candidate-generation.md`, `positioning-frameworks.md`

### 3 · Stated preference is not demand, and the size of the gap is disputed

- Schmidt & Bijmolt (*J. Academy of Marketing Science*, 2020): meta-analysis,
  77 studies, 115 effect sizes, 24,347 hypothetical and 20,656 real observations.
  **Hypothetical WTP exceeded real WTP by 21% on average**, and indirect methods
  carried **~10 percentage points more** bias than direct ones in the full model
  — the reverse of the conventional assumption.
- gemini cited List & Gallet's payment-experiment meta-analysis for an
  overstatement nearer **a factor of three**.
- **These disagree and the skill says so.** Different corpora and different
  measures; the direction is certain, the magnitude is not. Any survey-derived
  pricing number travels with that caveat.
- Webb & Sheeran (2006): changing intention by **d = 0.66** changed behaviour by
  **d = 0.36**. Morwitz, Steckel & Gupta (2007): intentions predict worst for new
  products and long horizons — exactly where positioning work sits.
- Van Westendorp: no independent criterion validity against realised purchase
  prices was located by any member. → `decision-aid.md`

### 4 · A landing-page test without a power calculation is not a test

Per-arm visitors, two-sided, 80% power, α = .05 (openai's table; local-claude
computed the fourth row independently):

| Control | Worthwhile treatment | Visitors per arm |
|---:|---:|---:|
| 10% | 15% | ~685 |
| 10% | 12% | ~3,838 |
| 5% | 7% | ~2,211 |
| 2.0% | 2.6% | ~13,850 |

A B2B smoke test at 200–500 clicks per variant has power below 0.15 and will
still produce a winner. Plus a selection problem: ad clicks over-sample
curiosity-driven individual searchers who are frequently not the economic buyer.
→ `decision-aid.md`, `pre-commitment.template.md`

### 5 · The evidence tier decides the word "recommended"

openai's cumulative gate, adopted verbatim as the skill's labelling rule:
**Recommended** needs a revealed-behaviour test and a replication;
**conditionally recommended** needs perception and relative-choice evidence;
**promising hypothesis** is what qualitative, survey, MaxDiff or hypothetical-WTP
evidence alone earns; **no decision** is a permitted output when candidates are
practically tied.

A desk-research run of this skill produces "promising hypothesis" at best. Saying
that is the difference between this and a confident deck. → `decision-aid.md`

### 6 · The feature-list pitch has a number

Anderson, Narus & van Rossum (*Harvard Business Review*, 2006; >100 firms):
three value-proposition approaches — All Benefits, Favourable Points of
Difference, and Resonating Focus. **"All Benefits" was observed in 85% of failed
pitches.** Resonating Focus carries 1–2 quantifiable points of difference tied to
the customer's operational bottleneck. This is the predecessor's anti-all-in-one
rule, with evidence under it. → `positioning-frameworks.md`, `territory.template.md`

### 7 · Beachhead scoring has never been validated

`<MISSING_DATA>No prospective study was located that validates a startup
beachhead score against later segment-level revenue, retention or survival while
controlling for company quality and execution.</MISSING_DATA>` (openai)

local-claude added the arithmetic: ±25% error on four multiplied scoring
dimensions produces a 0.32× to 2.44× envelope, and the halo effect means founders
score segments matching their own background higher. The replacement is an
evidence ledger per segment — named-account counts rather than top-down TAM,
observed contact-to-meeting rates rather than guessed access, paid pilots or
signed LOIs rather than stated WTP. → `product-truth.md`, `customer.template.md`

### 8 · JTBD/ODI is a discovery lens, not validation

Strategyn's "86% success rate" is 18 sponsor-rated successes among 21 launched
projects from 43 contacted initiatives, retrospectively self-classified, with no
control and sponsor-chosen success metrics. openai computed the approximate
Wilson 95% CI as **65%–95%** before addressing selection bias. All three paid
members flagged it; none accepted it. Use ODI to generate and articulate
outcomes; never let an opportunity score qualify a territory.

### 9 · Blue Ocean's own critique

A peer-reviewed critical analysis found Blue Ocean Strategy lacks a clear
implementation protocol and has limited scientific validation. The skill keeps
ERRC as a *construction* instrument — it forces the Eliminate question, which is
where a model otherwise adds rather than subtracts — while `positioning-frameworks.md`
states plainly that none of the four books predicts which position will work.

### 10 · Failure is a discovery deficit more often than a technology one

perplexity: a narrative analysis of fifty failed startups found information-seeking
deficits in **35 cases** and customer-service-orientation deficits in **33** —
more common than technological shortcomings. It is the argument for Phase 2
existing at all.

## Rules here that are design choices, not findings

Stated so the citation-backed rules stay distinguishable:

- The **nine-document report suite** and its numbering.
- The **five trawl personas** instantiated for positioning — trawl's own evidence
  file grounds the frame-portfolio architecture; the specific occupational
  personas are chosen, not measured.
- The **three-tier truth ledger** (`shipped` / `designed` / `aspirational`) and
  the `PROMISSORY_MOVES` set. Mechanising the predecessor's prose rule.
- **Independent-domain floors** of 3 / 2 / 1 for high / medium / low confidence.
  The principle that support is counted in domains rather than backends comes
  from Dossier's merge; the specific floors are chosen.
- Everything in `report-design.md` about GSAP, Three.js and the design-review
  gate, which comes from `design-craft`, `ux-craft` and `design-review`'s own
  evidence files rather than from these panels.

## Panel 2 — AI market-intelligence failure profile

Dispatched 26 Aug 2026 across gemini, openai and perplexity, archetype
`technical`, tier `max`, assembled by hand because the automatic panel could not
obtain six concurrent slots. It covers fabrication rates in agentic search,
citation verification versus claim-source entailment, voice-of-customer mining
validity, panel independence and correlated error, evidence-grading schemes, and
LLM-as-judge bias. Findings land in `research-panels.md`.

One measurement was already published by the tooling and is load-bearing enough
to state before that panel returns, because it comes from Dossier's own labelled
corpus rather than from these runs: **on 30 labelled cases, token containment
passed 11 of 23 bad citations as supporting — including every overstatement and
4 of 7 outright contradictions — where a judged pass let none through.** A
contradiction states the opposite using the page's own numbers and names, so a
token check has nothing to see. That is why promissory copy takes the judged
pass.
