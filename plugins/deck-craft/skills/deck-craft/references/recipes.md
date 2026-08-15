# Recipes — deck spines by occasion

A recipe is an **optional spine**, never a constraint: add, drop, reorder, replace or hand-author slides whenever the brief warrants it. Match a template to the slide's *job*, not its shape.

Twelve established recipes (from the investor pipeline) plus nine deck-craft additions covering the deck types the original set never reached.

## Selecting

Match the brief against `whenToUse` and the signal words. One recipe at most. If none fits, pick templates directly from `template-catalogue.md` — that is always permitted and costs less than forcing a spine.

---

## Established (12)

| id | When | Spine |
|---|---|---|
| `fy-results` | Annual or full-year results. Signals: *full year, fy results, annual results* | cover-title → agenda-list → kpi-row-3up → chart-takeaway → table-income → segment-3up → guidance-actual → lead-bullets → forward-looking |
| `hy-results` | Interim or half-year results. Signals: *half year, hy results, interim results* | cover-title → kpi-row-3up → table-income → segment-3up → guidance-actual → lead-bullets → forward-looking |
| `quarterly-4c` | Quarterly activity and cash-flow reporting, incl. Appendix 4C | cover-title → quarterly-highlights → 4c-cash-summary → activities-summary → production-vs-guidance → milestones-quarter |
| `agm` | AGM proceedings, addresses, resolutions, voting results | cover-title → agm-agenda → chair-address → ceo-address → resolutions-list → proxy-results → qa |
| `investor-day` | Long-form strategy, business-unit and operating-model presentations | cover-title → agenda-list → three-point → segment-3up → roadmap-quarters → esg-metrics → qa |
| `roadshow-ndr` | Compact investor roadshow / non-deal roadshow | cover-statement → three-point → kpi-row-4up → share-price → peer-comparison → catalyst-calendar → contact |
| `capital-raising` | Placements, entitlement offers, rights issues | cover-title → offer-details → use-of-funds → cap-table-prepost → dilution-waterfall → raise-timeline → risk-matrix |
| `ipo-pitch` | Pre-IPO investor education and listing readiness | cover-statement → problem-solution → chart-donut → kpi-row-3up → pathway-to-listing → valuation-bridge → cornerstone-support → offer-details |
| `board-pack` | Executive and board performance packs | cover-title → kpi-grid-2x3 → variance-bridge → table-cashflow → risk-matrix → milestone-check → appendix-divider |
| `esg-sustainability` | Sustainability, climate, safety, governance reporting | cover-image-bleed → esg-metrics → safety-stats → kpi-progress → board-grid → forward-looking |
| `ma-scheme` | Transactions, schemes of arrangement, acquisition proposals | cover-title → statement-support → sources-and-uses → comparable-transactions → timeline-h → risk-matrix |
| `site-visit` | Investor and analyst operating-site visits | cover-image-bleed → map-pins → image-grid-2x2 → plant-throughput → production-vs-guidance → qa |

**One gap worth naming in the established set:** `board-pack` ends at `appendix-divider` and never states an ask. A board pack that informs and never requests a decision is the failure the `decision-request` template exists to prevent — append it before the appendix, or use `board-pack-decision` below.

---

## deck-craft additions (9)

| id | When | Spine |
|---|---|---|
| `board-pack-decision` | A board pack that carries a decision, not just performance. Signals: *approval, board decision, seeking endorsement* | cover-title → agenda-progress → kpi-grid-2x3 → variance-bridge → what-changed-since → risk-matrix → **decision-request** → conflict-disclosure → appendix-divider |
| `product-review` | Product or feature review, roadmap check-in. Signals: *product review, roadmap, feature update* | cover-title → metric-dashboard → product-screens-3up → cohort-retention → now-next-later → objection-gate → ask-and-close |
| `engineering-review` | Engineering or platform review, architecture proposal. Signals: *engineering review, architecture, platform, tech review* | cover-title → metric-dashboard → architecture-blocks → bottleneck-lane → incident-summary → now-next-later → decision-request |
| `postmortem` | Incident or missed-target review. Signals: *postmortem, incident review, retro, what went wrong* | cover-statement → incident-summary → failure-postmortem → sequence-flow → unknowns-register → last-mile-so-what |
| `customer-qbr` | Quarterly business review with a customer. Signals: *QBR, customer review, account review* | cover-logo-band → agenda-list → metric-dashboard → case-study → returns-register → now-next-later → ask-and-close |
| `sales-pitch` | New-business pitch or proposal. Signals: *pitch, proposal, new business, capability deck* | cover-statement → problem-solution → three-point → product-screens-3up → case-study → logo-wall → pricing-tiers → faq-objections → ask-and-close |
| `internal-strategy` | Strategy offsite, planning, operating-model change. Signals: *strategy, offsite, planning, operating model* | cover-statement → definition-strip → competitive-position → matrix-2x2 → routing-alternatives → org-target-state → decision-request |
| `budget-review` | Budget, forecast or spend review. Signals: *budget, forecast review, spend, reforecast* | cover-title → budget-variance → spend-breakdown → range-not-point → assumption-load-bearing → capacity-vs-demand → decision-request |
| `all-hands` | Company or team all-hands. Signals: *all hands, town hall, team update* | cover-image-bleed → agenda-progress → speedrun-summary → metric-dashboard → release-notes → hiring-plan → attention-reset → qa |
| `quarterly-operational-strategic` | 12-slide comprehensive quarterly operational & strategic update. Signals: *quarterly update, operational update, strategic update, 4C strategic* | cover-image-bleed → quarterly-highlights → strategy-delivery → segment-operational-split → asset-build-matrix → contracted-backlog → restructuring-roi → net-debt-trajectory → dividend-pathway → governance-director → outlook-guidance → corporate-directory |
| `capital-allocation-dividend` | Capital allocation framework & dividend reinstatement pathway. Signals: *capital allocation, dividend policy, capital framework, cash waterfall* | cover-title → capital-allocation-framework → cashflow-waterfall → balance-sheet-optimization → dividend-reinstatement-pathway → reinvestment-growth → shareholder-returns → governance-disclaimer |

---

## Adapting a spine

Three moves, all normal:

- **Drop a step** whose data doesn't exist. A slide shape chosen because it needs no figures beats a slide with an invented one.
- **Insert an orientation beat.** Any spine over ~10 slides earns an `agenda-progress` or `checkpoint-recap` around the midpoint, and `section-recap` at each section close.
- **Swap depth for the audience.** `difficulty-ramp` replaces a content slide when the room spans an executive and a specialist.
