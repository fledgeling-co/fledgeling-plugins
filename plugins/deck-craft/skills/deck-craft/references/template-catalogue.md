# Slide-template catalogue — 200 layouts

Folded into deck-craft. Every layout here is a **base structure, never a form to fill in**: bend it,
or ignore the library and author the slide from nothing. Both are first-class and no gate penalises
hand-authoring.

Reading a row: `id` — purpose — slots. A slot is `name:kind` with `!` required and `?` optional;
`max N` is the most list entries the layout holds without overlapping. `SOURCE` means the template
will not expand without a `source` slot. `CAVEAT` means the expansion inserts a mandatory footnote
you may reword but not remove.

Slot kinds: `text` · `stat` · `list` · `tableRows` · `chartSeries` · `imageRef` · `widgetConfig`.

**Templates carry no colour and no font.** The deck theme resolves those, so the same template is
correct under every format. Never put a colour in a slot value.

Sections 1–18 are the **server-expandable template library (140)** — those ids, and only those, are
valid `templateId` values. Sections 19–27 are the deck-craft additions (60):
**hand-author composition specs**, structures you build element-by-element. Their names are
**never valid `templateId` values** — sending one is rejected at expansion (`ask-and-close` hit
exactly this). The gap analysis behind them is in `template-additions.md`, which is kept as provenance and is deliberately off the read list — it is a record of decisions already taken, and its only build-time content now lives in `slot-contract.md`. Don't read it to author a slide.

**`layout-specs.md` carries the geometry, hierarchy and UX block for every entry here, and its
`caps` override the `max N` values below** — those were measured against the frame; these were
mostly authored from intent. Where they disagree, the spec is right.

---

## Openers & section breaks

- **cover-title** — Default opener. Maximum restraint: title, subtitle, date.
  - title:text! · subtitle:text? · date:text?
- **cover-image-bleed** — Opener anchored by a real asset, site or product photograph.
  - image.1:imageRef! · title:text! · subtitle:text?
- **cover-logo-band** — Co-branded or joint-venture presentation carrying two marks.
  - title:text! · logo.1:imageRef! · logo.2:imageRef? · date:text?
- **cover-statement** — Investor day or thesis-led opener that leads with a claim, not a title.
  - statement:text! · attribution:text?
- **section-numbered** — Divider between deck sections, numbered for navigation.
  - number:text! · title:text!
- **section-image** — Section divider that needs a visual anchor.
  - image.1:imageRef! · title:text!
- **agenda-list** — The standing second slide of a results, AGM or investor-day deck.
  - title:text! · items:list! max 8

## Narrative & message

- **statement-hero** — One idea, given the whole slide. Use sparingly for it to keep working.
  - statement:text!
- **statement-support** — A claim with two or three supporting lines beneath it.
  - statement:text! · support:list? max 3
- **lead-bullets** — The default content slide: a title, a framing line, then the points.
  - title:text! · lead:text? · bullets:list! max 6
- **two-column-text** — Balanced narrative with no visual — comparison, two themes.
  - title:text! · left.heading:text! · left.body:text! · right.heading:text! · right.body:text!
- **three-point** — Strategy pillars, value drivers, three reasons to believe.
  - title:text! · point.1.heading:text! · point.1.body:text? · point.2.heading:text! · point.2.body:text? · point.3.heading:text! · point.3.body:text?
- **quote-pull** — A CEO or analyst quotation carrying the slide.
  - quote:text! · attribution:text!
- **quote-portrait** — An attributed quote where the person matters as much as the words.
  - image.1:imageRef! · quote:text! · attribution:text!
- **problem-solution** — Framing a strategic response: what was wrong, what was done.
  - title:text! · problem.heading:text! · problem.body:text! · solution.heading:text! · solution.body:text!
- **before-after** — Transformation or turnaround, stated as two states.
  - title:text! · before.heading:text! · before.body:text? · after.heading:text! · after.body:text?

## KPI & metrics

- **kpi-hero** — One number carries the slide — a record result, a headline total.
  - title:text? · kpi.1:stat! · footnote:text?
- **kpi-row-2up** — A pair of headline figures.
  - title:text! · kpi.1:stat! · kpi.2:stat! · footnote:text?
- **kpi-row-3up** — The standard results row.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · footnote:text?
- **kpi-row-4up** — Dense results summary.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · kpi.4:stat? · footnote:text?
- **kpi-grid-2x2** — Four metrics that need room for longer labels than a row allows.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · kpi.4:stat?
- **kpi-grid-2x3** — A six-metric scorecard — divisional or quarterly.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · kpi.4:stat? · kpi.5:stat? · kpi.6:stat?
- **kpi-delta-row** — Period-on-period comparison where the movement is the point.
  - title:text! · periods:text? · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · footnote:text?
- **kpi-sparkline** — Figures that need their direction of travel shown, not just stated.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · spark.1:chartSeries? · spark.2:chartSeries? · spark.3:chartSeries?
- **kpi-chart-right** — Headline figures beside the trend that produced them.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · chart.series:chartSeries! · source:text?
- **kpi-progress** — Tracking delivery against guidance or a stated target.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · footnote:text?
- **kpi-table-compact** — More metrics than a grid holds — put them in a table instead of shrinking type.
  - title:text! · table.rows:tableRows! · footnote:text?

## Charts — single

- **chart-bleed** — The chart IS the slide — no competing content.
  - title:text? · chart.series:chartSeries! · source:text?
- **chart-takeaway** — A chart with its "so what" stated, not left to the audience.
  - title:text! · takeaway:text! · chart.series:chartSeries! · source:text?
- **chart-callouts** — Annotating specific points on a chart — an inflection, a one-off.
  - title:text! · chart.series:chartSeries! · callouts:list! max 3 · source:text?
- **chart-bar-v** — Category comparison with short labels.
  - title:text! · chart.series:chartSeries! · source:text?
- **chart-bar-h** — Rankings, or categories with long labels.
  - title:text! · chart.series:chartSeries! · source:text?
- **chart-line** — A time series: share price, output, headcount.
  - title:text! · chart.series:chartSeries! · source:text?
- **chart-area** — Composition over time.
  - title:text! · chart.series:chartSeries! · source:text?
- **chart-waterfall** — A bridge: earnings, cash movement, variance.
  - title:text! · chart.series:chartSeries! · source:text?
- **chart-donut** — Share of a total, six segments at most.
  - title:text! · chart.series:chartSeries! · source:text?
- **chart-combo** — A volume series with a rate overlaid.
  - title:text! · chart.series:chartSeries! · source:text?

## Charts — multiple & comparison

- **charts-2up** — Two views that make one point together.
  - title:text! · chart.1.label:text? · chart.1.series:chartSeries! · chart.2.label:text? · chart.2.series:chartSeries! · source:text?
- **charts-4up** — A divisional dashboard — four series at a glance.
  - title:text! · chart.1.label:text? · chart.1.series:chartSeries! · chart.2.label:text? · chart.2.series:chartSeries! · chart.3.label:text? · chart.3.series:chartSeries? · chart.4.label:text? · chart.4.series:chartSeries? · source:text?
- **chart-table** — The visual and the figures behind it, on one slide.
  - title:text! · chart.series:chartSeries! · table.rows:tableRows! · source:text?
- **chart-kpis** — A trend anchored by the headline figures it produced.
  - title:text! · chart.series:chartSeries! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · source:text?
- **chart-legend-panel** — Many series, where each needs a word of explanation.
  - title:text! · chart.series:chartSeries! · legend:list! max 6 · source:text?
- **segment-3up** — Revenue or earnings split three ways — by division, region, product.
  - title:text! · segment.1.label:text! · segment.1.series:chartSeries! · segment.2.label:text! · segment.2.series:chartSeries! · segment.3.label:text! · segment.3.series:chartSeries! · source:text?
- **variance-bridge** — Actual vs budget vs prior, with the moving parts named.
  - title:text! · chart.series:chartSeries! · notes:list? max 4 · source:text?

## Tables

- **table-simple** — Any tabular content that needs no emphasis.
  - title:text! · table.rows:tableRows! · footnote:text?
- **table-totals** — A financial summary whose total line is the point.
  - title:text! · table.rows:tableRows! · table.totals:tableRows! · footnote:text?
- **table-3period** — FY24 / FY25 / FY26-style comparison across three columns.
  - title:text! · periods:list! max 3 · table.rows:tableRows! · footnote:text?
- **table-highlight** — A table where one line needs to be found immediately.
  - title:text! · table.rows:tableRows! · highlight.row:text! · footnote:text?
- **table-income** — The results slide of a full or half-year presentation. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?
- **table-balance** — Financial position: assets, liabilities, net assets. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?
- **table-cashflow** — The cash-generation narrative behind the result. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?

## Timeline, roadmap & milestones

- **timeline-h** — Company history or project phases along a single axis.
  - title:text! · events:list! max 6
- **timeline-v** — A detailed chronology where each entry needs a sentence.
  - title:text! · events:list! max 6
- **roadmap-quarters** — The next four quarters of delivery, one column each.
  - title:text! · quarter.1.label:text! · quarter.1.items:list? max 4 · quarter.2.label:text! · quarter.2.items:list? max 4 · quarter.3.label:text! · quarter.3.items:list? max 4 · quarter.4.label:text! · quarter.4.items:list? max 4
- **milestone-check** — Delivered versus outstanding, side by side.
  - title:text! · delivered.heading:text! · delivered:list! max 5 · next.heading:text! · next:list! max 5
- **phase-stepper** — A stage-gated project: five phases at most, current one nameable.
  - title:text! · phases:list! max 5
- **gantt-lite** — Overlapping workstreams where the overlap is the point.
  - title:text! · streams:list! max 5 · periods:list! max 4
- **catalyst-calendar** — Upcoming value-inflection points, dated.
  - title:text! · table.rows:tableRows! · footnote:text?
- **history-arc** — A long-run narrative in five beats.
  - title:text! · events:list! max 5

## Diagrams & relationships

- **cols-3-icon** — 3 parallel concepts, each with an icon and a line of detail.
  - title:text! · col.1.icon:imageRef? · col.1.heading:text! · col.1.body:text? · col.2.icon:imageRef? · col.2.heading:text! · col.2.body:text? · col.3.icon:imageRef? · col.3.heading:text! · col.3.body:text?
- **cols-4-icon** — 4 parallel concepts, each with an icon and a line of detail.
  - title:text! · col.1.icon:imageRef? · col.1.heading:text! · col.1.body:text? · col.2.icon:imageRef? · col.2.heading:text! · col.2.body:text? · col.3.icon:imageRef? · col.3.heading:text! · col.3.body:text? · col.4.icon:imageRef? · col.4.heading:text! · col.4.body:text?
- **matrix-2x2** — Positioning or prioritisation against two axes.
  - title:text! · axis.x:text! · axis.y:text! · quadrant.1:text! · quadrant.2:text! · quadrant.3:text! · quadrant.4:text!
- **funnel** — Pipeline, conversion, or resource-to-reserve narrowing.
  - title:text! · stages:list! max 5
- **pyramid** — A hierarchy of strategy or value.
  - title:text! · stages:list! max 4
- **process-arrows** — A linear process of up to six steps.
  - title:text! · steps:list! max 6
- **hub-spoke** — One centre with several relationships around it.
  - title:text! · hub:text! · spokes:list! max 6
- **org-chart** — Corporate or group structure, three levels deep.
  - title:text! · node.root:text! · node.level2:list! max 2 · node.level3:list! max 4

## People & governance

- **people-3up** — An executive highlight — three faces.
  - title:text! · person.1.photo:imageRef! · person.1.name:text! · person.1.role:text? · person.2.photo:imageRef! · person.2.name:text! · person.2.role:text? · person.3.photo:imageRef? · person.3.name:text? · person.3.role:text?
- **people-4up** — The leadership team.
  - title:text! · person.1.photo:imageRef! · person.1.name:text! · person.1.role:text? · person.2.photo:imageRef! · person.2.name:text! · person.2.role:text? · person.3.photo:imageRef? · person.3.name:text? · person.3.role:text? · person.4.photo:imageRef? · person.4.name:text? · person.4.role:text?
- **people-6up** — A full board or executive team.
  - title:text! · person.1.photo:imageRef! · person.1.name:text! · person.1.role:text? · person.2.photo:imageRef! · person.2.name:text! · person.2.role:text? · person.3.photo:imageRef? · person.3.name:text? · person.3.role:text? · person.4.photo:imageRef? · person.4.name:text? · person.4.role:text? · person.5.photo:imageRef? · person.5.name:text? · person.5.role:text? · person.6.photo:imageRef? · person.6.name:text? · person.6.role:text?
- **bio-single** — A new appointment or a key hire worth a slide.
  - person.1.photo:imageRef! · person.1.name:text! · person.1.role:text! · person.1.bio:text!
- **board-grid** — The governance section: who sits on the board and since when.
  - title:text! · person.1.photo:imageRef! · person.1.name:text! · person.1.role:text? · person.2.photo:imageRef! · person.2.name:text! · person.2.role:text? · person.3.photo:imageRef? · person.3.name:text? · person.3.role:text? · person.4.photo:imageRef? · person.4.name:text? · person.4.role:text? · table.rows:tableRows!
- **advisor-strip** — The marks of advisors, brokers or partners, given equal weight.
  - title:text! · logos:list! max 8

## Imagery-led

- **image-bleed-caption** — A site, asset or product photograph given the whole slide.
  - image.1:imageRef! · caption:text!
- **image-left** — A visual beside its narrative.
  - image.1:imageRef! · title:text! · body:text!
- **image-right** — A visual beside its narrative, mirrored for rhythm across a run of slides.
  - image.1:imageRef! · title:text! · body:text!
- **image-grid-2x2** — A portfolio, several sites, or a product range.
  - title:text! · image.1:imageRef! · caption.1:text? · image.2:imageRef! · caption.2:text? · image.3:imageRef? · caption.3:text? · image.4:imageRef? · caption.4:text?
- **image-strip-3up** — A sequence or a three-way comparison.
  - title:text! · image.1:imageRef! · caption.1:text? · image.2:imageRef? · caption.2:text? · image.3:imageRef? · caption.3:text?
- **image-stat-overlay** — A photograph carrying one headline number.
  - image.1:imageRef! · kpi.1:stat! · caption:text?
- **map-pins** — An operations footprint — sites, tenements, offices.
  - title:text! · map:imageRef! · pins:list! max 6

## Investor-relations specific

- **share-price** — Standing slide in any results or investor-day deck. _[SOURCE]_
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · chart.series:chartSeries! · source:text!
- **capital-structure** — Shares on issue, options, performance rights, debt.
  - title:text! · table.rows:tableRows! · chart.series:chartSeries? · footnote:text?
- **register-breakdown** — Ownership composition — institutional, retail, board, top 20. _[SOURCE]_
  - title:text! · table.rows:tableRows! · chart.series:chartSeries? · source:text!
- **dividend-history** — For income-focused investors: what has been paid, and when.
  - title:text! · table.rows:tableRows! · chart.series:chartSeries? · footnote:text?
- **guidance-actual** — The delivery record — the most scrutinised slide in a results deck. _[CAVEAT]_
  - title:text! · kpi.1:stat! · kpi.2:stat? · chart.series:chartSeries! · footnote:text?
- **peer-comparison** — Relative valuation or performance against a named peer set. _[SOURCE]_
  - title:text! · table.rows:tableRows! · chart.series:chartSeries? · source:text!
- **analyst-coverage** — Who covers the stock, and where their targets sit. _[SOURCE]_
  - title:text! · table.rows:tableRows! · source:text!
- **esg-metrics** — The ESG section: four measures and a trend.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · kpi.4:stat? · chart.series:chartSeries? · footnote:text?
- **safety-stats** — Industrials, mining and energy: TRIFR and lost-time trend.
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · chart.series:chartSeries! · footnote:text?
- **production-summary** — Resources and manufacturing: volumes against the prior period.
  - title:text! · table.rows:tableRows! · chart.series:chartSeries? · footnote:text?

## Closing & compliance

- **disclaimer-full** — The mandatory legal page.
  - title:text! · body:text!
- **forward-looking** — Any deck carrying guidance or projections.
  - title:text! · body:text!
- **contact** — The closing slide: who to call, and where to look.
  - title:text! · contacts:list! max 4 · logo:imageRef?
- **thank-you** — A plain close.
  - title:text! · subtitle:text?
- **qa** — Before the discussion.
  - title:text! · image.1:imageRef?
- **appendix-divider** — The start of supporting material.
  - title:text! · subtitle:text?

## Live widget slides

- **live-price** — An investor day or AGM where the market is open.
  - title:text! · widget.config:widgetConfig! · caption:text?
- **live-poll** — An interactive session.
  - title:text! · widget.config:widgetConfig! · caption:text?
- **live-qa** — AGM or investor briefing taking questions from the room.
  - title:text! · widget.config:widgetConfig! · caption:text?
- **live-ticker** — A figure that updates while the deck is on screen.
  - title:text! · widget.config:widgetConfig! · caption:text?

## Capital raising & IPO

- **offer-details** — The terms slide of any raise. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?
- **use-of-funds** — Where the money goes — the question every investor asks first.
  - title:text! · chart.series:chartSeries! · table.rows:tableRows! · footnote:text?
- **sources-and-uses** — Funding structure shown from both sides, and they must balance.
  - title:text! · sources.rows:tableRows! · uses.rows:tableRows! · footnote:text?
- **cap-table-prepost** — Dilution made explicit, side by side, rather than described. _[CAVEAT]_
  - title:text! · pre.rows:tableRows! · post.rows:tableRows!
- **dilution-waterfall** — Shares on issue stepped through the raise. _[CAVEAT]_
  - title:text! · chart.series:chartSeries! · takeaway:text?
- **raise-timeline** — Record date, close, settlement, allotment. _[CAVEAT]_
  - title:text! · events:list! max 6
- **cornerstone-support** — Named anchor investors — only where they have consented to be named. _[SOURCE]_
  - title:text! · commitment:text! · investors:list! max 6 · source:text!
- **valuation-bridge** — Pre-money to post-money, with the steps named. _[CAVEAT]_
  - title:text! · chart.series:chartSeries! · table.rows:tableRows! · footnote:text?
- **comparable-transactions** — Precedent-transaction framing for a raise or a deal. _[SOURCE]_
  - title:text! · table.rows:tableRows! · source:text!
- **subscription-summary** — After the fact: take-up, allocation, scale-back.
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · table.rows:tableRows! · footnote:text?
- **escrow-schedule** — Post-IPO restricted securities and their release dates. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?
- **pathway-to-listing** — The pre-IPO readiness narrative: what is done, what remains. _[CAVEAT]_
  - title:text! · phases:list! max 5

## AGM & governance events

- **agm-agenda** — The standing AGM opener.
  - title:text! · items:list! max 10
- **resolutions-list** — The items being put to the meeting. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?
- **proxy-results** — Votes for, against and abstained — as received from the registry. _[SOURCE]_
  - title:text! · chart.series:chartSeries! · table.rows:tableRows! · source:text!
- **chair-address** — The chair's prepared remarks.
  - title:text! · body:text! · photo:imageRef?
- **ceo-address** — The chief executive's prepared remarks.
  - title:text! · body:text! · photo:imageRef?
- **voting-instructions** — The procedural slide for holders in the room and online.
  - title:text! · steps:list! max 3 · qr:imageRef?
- **remuneration-summary** — For the remuneration-report discussion. _[SOURCE]_
  - title:text! · chart.series:chartSeries! · table.rows:tableRows! · source:text!
- **director-election** — A candidate standing for election or re-election.
  - name:text! · role:text! · bio:text! · tenure:text? · photo:imageRef?

## Quarterly & periodic reporting

- **quarterly-highlights** — The opening summary of a quarterly update.
  - title:text! · kpi.1:stat! · kpi.2:stat! · kpi.3:stat? · kpi.4:stat? · bullets:list? max 4
- **4c-cash-summary** — Quarterly cash-flow reporters — the slide that follows the 4C. _[CAVEAT]_
  - title:text! · kpi.1:stat! · kpi.2:stat? · table.rows:tableRows!
- **activities-summary** — The operational narrative of a quarter, with supporting imagery.
  - title:text! · bullets:list! max 5 · image.1:imageRef? · image.2:imageRef?
- **production-vs-guidance** — Delivery against the forecast the market is holding you to. _[CAVEAT]_
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · chart.series:chartSeries! · footnote:text?
- **exploration-update** — An explorer's quarterly staple: where, what, and what next. _[SOURCE]_
  - title:text! · table.rows:tableRows! · source:text!
- **milestones-quarter** — Delivered this quarter, planned for next.
  - title:text! · delivered:list! max 5 · next:list! max 5

## Sector operating slides

- **tenement-map** — The land position — tenements, licences, permits. _[SOURCE]_
  - title:text! · map:imageRef! · legend:list! max 6 · source:text!
- **drilling-results** — Assay or intercept reporting. _[SOURCE CAVEAT]_
  - title:text! · table.rows:tableRows! · source:text!
- **resource-reserve-table** — JORC-reported estimates. _[SOURCE CAVEAT]_
  - title:text! · table.rows:tableRows! · source:text!
- **clinical-pipeline** — Life sciences: programmes by development phase. _[CAVEAT]_
  - title:text! · phases:list! max 4 · programmes:list! max 5
- **regulatory-milestones** — The approval pathway and where the company sits on it. _[CAVEAT]_
  - title:text! · events:list! max 5
- **project-economics** — NPV, IRR, payback — the study outputs. _[SOURCE CAVEAT]_
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · kpi.4:stat? · chart.series:chartSeries! · source:text!
- **offtake-summary** — The contracted revenue base. _[SOURCE]_
  - title:text! · table.rows:tableRows! · source:text!
- **plant-throughput** — Operating performance against nameplate.
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · chart.series:chartSeries! · footnote:text?

## Scenario & sensitivity

- **sensitivity-table** — One output against two input variables. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · footnote:text?
- **scenario-3case** — Low, base and high — stated as scenarios, never as forecasts. _[CAVEAT]_
  - title:text! · table.rows:tableRows! · chart.series:chartSeries?
- **assumptions-list** — The basis behind the numbers — the slide that makes the rest defensible.
  - title:text! · assumptions:list! max 8
- **valuation-range** — A range with its midpoint, and what drives each end. _[SOURCE CAVEAT]_
  - title:text! · kpi.1:stat! · kpi.2:stat? · kpi.3:stat? · chart.series:chartSeries! · source:text!
- **break-even** — Where the economics turn. _[CAVEAT]_
  - title:text! · chart.series:chartSeries! · takeaway:text!
- **risk-matrix** — Likelihood against impact, for a board pack or a risk section.
  - title:text! · axis.x:text! · axis.y:text! · risks:list! max 6

## Decision & ask

- **decision-request** — The ask, stated. Every board pack needs this; nothing in sections 1–18 renders it.
  - decision:text! · options:tableRows! max 4 · recommendation:text! · rationale:text? · unlocks:text? · decideBy:text!
- **consequence-fork** — Shared premise, two mirrored paths, named decision owner.
  - premise:text! · pathA.label:text! · pathA.stat:stat? · pathA.outcome:text! · pathB.label:text! · pathB.stat:stat? · pathB.outcome:text! · owner:text? · decideBy:text?
- **routing-alternatives** — One origin, 2–3 candidate paths to the same destination, each with cost, time and failure mode. Shows the rejected routes with real numbers.
  - origin:text! · destination:text! · paths:tableRows! max 3
- **last-mile-so-what** — One finding, then who acts, what changes, by when.
  - finding:text! · audience:text! · action:text! · by:text!
- **decision-queue-depth** — Open decisions awaiting this audience, aged.
  - title:text! · rows:tableRows! max 6
- **handoff-baton** — Chain of custody: what this deck hands over, to whom, what they do next.
  - handsOver:tableRows! max 5 · receiver:text! · nextAction:text! · ackLine:text?
- **ask-and-close** — Closing ask with its next step. Replaces `thank-you` at the end of a persuasion deck.
  - ask:text! · nextStep:text! · contact:text? · deadline:text?

## Provenance & proof

- **claim-provenance-ledger** — One row per assertion made elsewhere in the deck. An empty source cell is visibly unprovable. _[SOURCE]_
  - title:text! · rows:tableRows! max 8 · source:text!
- **number-provenance** — One figure with its derivation: raw input → adjustment → result, each source-tagged.
  - figure:stat! · steps:tableRows! max 4 · asAt:text! · source:text!
- **non-ifrs-reconciliation** — Statutory → add-backs → adjusted, with a mandatory definition. Refuses the adjusted number without its ladder. _[CAVEAT]_
  - statutory:stat! · addBacks:tableRows! max 6 · adjusted:stat! · definition:text!
- **restatement-diff** — Prior figure, restated figure, delta, reason, effective date. Cannot render a revision without naming why.
  - rows:tableRows! max 5 · effectiveDate:text!
- **what-changed-since** — Diff against the prior meeting or version. Makes drift between successive packs visible.
  - priorRef:text! · rows:tableRows! max 6
- **returns-register** — What was promised, what came back: commitment, period, outcome, variance, kept/missed.
  - rows:tableRows! max 6
- **definition-strip** — The 4–6 terms the deck's numbers depend on, each with its formula or inclusion rule.
  - terms:tableRows! max 6

## Uncertainty

- **range-not-point** — Low / base / high with the driver that moves it. No slot for a bare point estimate.
  - metric:text! · low:stat! · base:stat! · high:stat! · driver:text! · basis:text?
- **assumption-load-bearing** — A claim with the 2–4 assumptions holding it up, each marked verified / estimated / assumed.
  - claim:text! · assumptions:tableRows! max 4
- **disconfirming-evidence** — The thesis plus the strongest case against it, with a response per item.
  - thesis:text! · against:tableRows! max 4
- **unknowns-register** — What is not known, why, what would resolve it, by when, owner.
  - rows:tableRows! max 6
- **jit-assumptions** — Assumptions ordered by when each must be resolved, with carrying cost and decay date.
  - now:tableRows? max 4 · soon:tableRows? max 4 · later:tableRows? max 4

## Orientation & pacing

- **checkpoint-recap** — Mid-deck save state: covered sections, one active, plus the next beat.
  - covered:tableRows! max 5 · activeIndex:text! · youAreHere:text! · next:text?
- **agenda-progress** — The agenda re-shown with completed items dimmed. The running-position indicator a long deck needs.
  - items:tableRows! max 7 · currentIndex:text!
- **attention-reset** — Deliberate zero-information beat after a dense run. No data slots.
  - phrase:text! · marker:text?
- **speedrun-summary** — The whole deck in 6–8 micro-rows, sized to be photographed.
  - rows:tableRows! max 8
- **difficulty-ramp** — Three depth bands; the presenter chooses where to stop.
  - surface:text! · mechanism:text! · detail:text? · detailStat:stat?
- **section-recap** — The three things just established, before the next section opens.
  - section:text! · established:tableRows! max 3

## Objection & failure

- **objection-gate** — The objection as a question, what would resolve it, the evidence that unlocks it.
  - objection:text! · conditions:tableRows! max 3 · evidence:stat? · evidenceNote:text?
- **failure-postmortem** — Prior claim struck through, the miss, causes, and a repair row with owner.
  - priorClaim:text! · miss:stat! · causes:tableRows! max 3 · repair:tableRows! max 3
- **faq-objections** — 4–6 anticipated questions, answered in one line each.
  - rows:tableRows! max 6
- **conflict-disclosure** — Party, relationship, interest, recusal per decision item. Cannot render a recommendation without its interest column. _[CAVEAT]_
  - rows:tableRows! max 5

## Flow, constraint & scale

- **bottleneck-lane** — 4–6 stages with throughput each, one drawn as the constraint.
  - stages:tableRows! max 6 · constraintIndex:text! · lossNote:text?
- **batch-vs-flow** — Batched cadence against continuous, with cycle time and WIP per side.
  - left.label:text! · left.stats:tableRows! · right.label:text! · right.stats:tableRows!
- **unit-array** — One number as a dense array of identical marks, one called out as the unit. A unit chart, not an illustration.
  - total:stat! · unitLabel:text! · caption:text?
- **waffle-share** — 100-cell grid with N filled. A proportion made countable.
  - filled:stat! · label:text! · note:text?
- **scale-anchor** — A stat against comparison bars at identical scale: prior period, plan, external reference. _[SOURCE]_
  - metric:text! · value:stat! · comparisons:tableRows! max 3 · source:text!

## Product & engineering

- **product-screens-3up** — Three screenshots in device or browser frames.
  - shots:imageRef! max 3 · captions:tableRows?
- **screen-annotated** — One screenshot with 2–4 numbered callouts.
  - image:imageRef! · callouts:tableRows! max 4
- **before-after-screens** — Two screenshots with a change summary. The UI counterpart to `before-after`.
  - before:imageRef! · after:imageRef! · summary:text!
- **architecture-blocks** — Layered system diagram, 3–4 tiers of labelled blocks.
  - tiers:tableRows! max 4 · note:text?
- **sequence-flow** — Actor lanes left to right with ordered steps between them.
  - actors:tableRows! max 4 · steps:tableRows! max 6
- **now-next-later** — Three-column roadmap without dates, for work that isn't calendar-committed.
  - now:tableRows! max 4 · next:tableRows! max 4 · later:tableRows! max 4
- **release-notes** — Shipped items by category with version and date.
  - version:text! · date:text! · groups:tableRows! max 6
- **incident-summary** — Timeline, impact stats, resolution. The postmortem slide every engineering review needs.
  - title:text! · timeline:tableRows! max 5 · impact:stat! · duration:stat? · resolution:text!
- **metric-dashboard** — 6–8 small multiples, each label + figure + sparkline.
  - tiles:tableRows! max 8
- **rag-status** — Workstream status with red/amber/green, owner, one-line note.
  - rows:tableRows! max 7

## Customer & commercial

- **logo-wall** — Customer or partner marks in a disciplined grid.
  - logos:imageRef! max 12 · stat:stat? · caption:text?
- **case-study** — One customer: situation, what changed, outcomes as figures.
  - customer:text! · situation:text! · change:text! · outcomes:tableRows! max 3 · logo:imageRef?
- **testimonial-grid** — 2–3 short quotes with attribution. The multi-quote layout `quote-pull` can't do.
  - quotes:tableRows! max 3
- **pricing-tiers** — 2–4 plan columns with price, inclusions, one highlighted.
  - tiers:tableRows! max 4 · highlightIndex:text?
- **feature-matrix** — Feature rows against 2–4 columns with tick/cross/partial.
  - features:tableRows! max 8 · columns:tableRows! max 4
- **competitive-position** — Named competitors on two labelled axes. Distinct from the abstract `matrix-2x2`. _[SOURCE]_
  - xAxis:text! · yAxis:text! · players:tableRows! max 6 · usIndex:text! · source:text!
- **market-sizing** — TAM/SAM/SOM as three nested figures with the derivation basis for each. _[SOURCE]_
  - tam:stat! · sam:stat! · som:stat! · basis:tableRows! max 3 · source:text!
- **unit-economics** — Per-unit ladder: revenue → cost lines → contribution, with payback.
  - rows:tableRows! max 6 · contribution:stat! · payback:stat?
- **cohort-retention** — Cohort curves with the headline retention figure called out.
  - chart.series:chartSeries! · headline:stat! · note:text?

## People, plan & spend

- **hiring-plan** — Roles by period with count, function, status.
  - rows:tableRows! max 7
- **org-target-state** — Current against target operating model.
  - current:tableRows! max 5 · target:tableRows! max 5 · note:text?
- **raci** — Workstreams against named owners with R/A/C/I marks.
  - workstreams:tableRows! max 6 · people:tableRows! max 5
- **budget-variance** — Budget, actual, variance by line, with a driver note.
  - rows:tableRows! max 7 · note:text?
- **spend-breakdown** — Categories with amount, share, optional prior period.
  - rows:tableRows! max 6 · total:stat!
- **capacity-vs-demand** — Available capacity against committed demand across periods.
  - chart.series:chartSeries! · gap:stat? · note:text?
- **sources-slide** — The deck's own references, numbered to match in-deck superscripts. _[SOURCE]_
  - rows:tableRows! max 8 · source:text!
