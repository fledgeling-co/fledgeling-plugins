# deck-craft — proposed template additions

Gap analysis of the existing 140-template catalogue, run through the ADHD divergent-ideation
method (5 isolated frames: regulator, game design, logistics, inversion, 10-year-old), then
converged. Plus a deliberate sweep of the obvious-but-absent, which the divergent frames were
instructed to skip.

**60 new templates across 9 families.** Slot kinds follow the existing contract:
`text` · `stat` · `tableRows` · `imageRef` · `chartSpec` · `shape` · `line`.
`!` required · `?` optional · `max N` list cap.

---

## What the existing 140 is missing — the three structural holes

**1. No way to state an ask.** 140 templates and not one renders a decision, its options, the
recommendation, or the deadline. Every board pack and proposal deck has to hand-author it. Four
independent frames converged on this from different directions (`decision-request`,
`last-mile-so-what`, `consequence-fork`, `decision-queue-depth`) — the strongest signal in the run.

**2. The catalogue is listed-company-shaped.** Deep on capital raising, AGM, 4C, tenements and
resources; nearly empty on the decks most people actually build — product, engineering, customer,
commercial, internal review. No customer logos, no case study, no pricing, no competitive matrix,
no architecture diagram, no cohort curve, no RAG status.

**3. Nothing carries uncertainty or provenance as structure.** `assumptions-list` and
`sensitivity-table` exist, but every figure template renders a naked point number with no room for
its source, its derivation, its range, or what would have to be true. The regulator and inversion
frames both attacked this and produced the most novel survivors.

---

## Family A — Decision & ask (7 new)

The missing spine of every board pack and proposal deck.

| id | Layout | Slots |
|---|---|---|
| `decision-request` | The ask, stated. Decision text, options list incl. do-nothing, recommendation with one-line reason, what it unlocks/blocks, decide-by date. | `decision:text!` · `options:tableRows!` (max 4) · `recommendation:text!` · `rationale:text?` · `unlocks:text?` · `decideBy:text!` |
| `consequence-fork` | Shared premise, two mirrored paths, each with label + stat + outcome line; footer names the decision owner and date. | `premise:text!` · `pathA.label:text!` · `pathA.stat:stat?` · `pathA.outcome:text!` · `pathB.*` (same) · `owner:text?` · `decideBy:text?` |
| `routing-alternatives` | One origin fanning to 2–3 candidate paths to the same destination, each carrying cost, time and failure-mode. Shows the rejected routes with their real numbers. | `origin:text!` · `destination:text!` · `paths:tableRows!` (max 3, cols cost/time/risk) |
| `last-mile-so-what` | One full-bleed finding, then a three-slot delivery row: who acts, what changes, by when. | `finding:text!` · `audience:text!` · `action:text!` · `by:text!` |
| `decision-queue-depth` | Ranked backlog of open decisions awaiting this audience — owner, days-waiting, blocked-by, decide-by. | `title:text!` · `rows:tableRows!` (max 6) |
| `handoff-baton` | Chain of custody: what this deck hands over, who receives it, what they must do next, acknowledgement line. | `handsOver:tableRows!` (max 5) · `receiver:text!` · `nextAction:text!` · `ackLine:text?` |
| `ask-and-close` | Closing ask paired with the specific next step and contact — replaces the dead `thank-you` at the end of a persuasion deck. | `ask:text!` · `nextStep:text!` · `contact:text?` · `deadline:text?` |

## Family B — Provenance & proof (7 new)

Regulator frame. Each makes an unprovable claim structurally hard to render.

| id | Layout | Slots |
|---|---|---|
| `claim-provenance-ledger` | One row per assertion made elsewhere in the deck: claim, source, source date, preparer, verification status. An empty source cell is visibly unprovable. | `title:text!` · `rows:tableRows!` (max 8, cols claim/source/asAt/status) |
| `number-provenance` | One headline figure with its derivation stacked beneath: raw input → adjustment → result, each with source tag and as-at date. | `figure:stat!` · `steps:tableRows!` (max 4) · `asAt:text!` · `source:text!` |
| `non-ifrs-reconciliation` | Statutory figure → itemised add-backs → non-statutory figure, with a mandatory definition slot. Refuses the adjusted number without its ladder. | `statutory:stat!` · `addBacks:tableRows!` (max 6) · `adjusted:stat!` · `definition:text!` (CAVEAT) |
| `restatement-diff` | Prior figure, restated figure, delta, reason, effective date. Cannot render a revision without naming why. | `rows:tableRows!` (max 5, cols prior/restated/delta/reason) · `effectiveDate:text!` |
| `what-changed-since` | Diff against the prior meeting or version: prior position, current position, delta marker, reason per row. Makes drift between successive packs visible. | `priorRef:text!` · `rows:tableRows!` (max 6) |
| `returns-register` | Reverse logistics for guidance: what was promised, prior period, outcome, variance reason, kept/missed chip. | `rows:tableRows!` (max 6) |
| `definition-strip` | Compact glossary band for the 4–6 terms the deck's numbers depend on, each with its formula or inclusion rule. | `terms:tableRows!` (max 6, cols term/definition) |

## Family C — Uncertainty (5 new)

Inversion frame. The catalogue's figure templates all render naked point numbers.

| id | Layout | Slots |
|---|---|---|
| `range-not-point` | Forecast as low/base/high band with the driver that moves it and a confidence basis. **No slot for a bare point estimate.** | `metric:text!` · `low:stat!` · `base:stat!` · `high:stat!` · `driver:text!` · `basis:text?` |
| `assumption-load-bearing` | A claim with its 2–4 load-bearing assumptions, each marked verified / estimated / assumed, with owner. | `claim:text!` · `assumptions:tableRows!` (max 4, cols assumption/state/owner) |
| `disconfirming-evidence` | Thesis plus the strongest evidence against it, each with a response line and severity marker. | `thesis:text!` · `against:tableRows!` (max 4) |
| `unknowns-register` | What is *not* known, why, what would resolve it, by when, owner. Makes absence of evidence assignable. | `rows:tableRows!` (max 6) |
| `jit-assumptions` | Assumption cards ordered by when each must be resolved (now / this quarter / before scale) with a carrying cost and decay date. | `now:tableRows?` · `soon:tableRows?` · `later:tableRows?` (max 4 each) |

## Family D — Orientation & pacing (6 new)

Game-design frame. A deck is a linear level with no back button; nothing in the 140 manages position or load.

| id | Layout | Slots |
|---|---|---|
| `checkpoint-recap` | Mid-deck save state: compressed strip of covered sections, one marked active, plus a "you are here" line and the next beat. | `covered:tableRows!` (max 5) · `activeIndex:text!` · `youAreHere:text!` · `next:text?` |
| `agenda-progress` | The agenda re-shown with completed items dimmed — the running-position indicator a long deck needs. | `items:tableRows!` (max 7) · `currentIndex:text!` |
| `attention-reset` | Deliberate zero-information beat after a dense run: one oversized phrase on a flat field, tiny position marker, no data slots. | `phrase:text!` · `marker:text?` |
| `speedrun-summary` | The whole deck compressed to 6–8 numbered micro-rows (title / one-line claim / one number), sized to be photographed. | `rows:tableRows!` (max 8, cols n/claim/figure) |
| `difficulty-ramp` | Three stacked depth bands (surface claim / mechanism / underlying maths); the presenter chooses where to stop. | `surface:text!` · `mechanism:text!` · `detail:text?` · `detailStat:stat?` |
| `section-recap` | End-of-section close: the three things just established, before the next section opens. | `section:text!` · `established:tableRows!` (max 3) |

## Family E — Objection & failure (4 new)

| id | Layout | Slots |
|---|---|---|
| `objection-gate` | The objection as a question, the conditions that would resolve it, and the evidence that unlocks it. | `objection:text!` · `conditions:tableRows!` (max 3) · `evidence:stat?` · `evidenceNote:text?` |
| `failure-postmortem` | A prior claim struck through, the delta stat showing the miss, causes, and a repair row with owner and status. | `priorClaim:text!` · `miss:stat!` · `causes:tableRows!` (max 3) · `repair:tableRows!` (max 3) |
| `faq-objections` | 4–6 anticipated questions with one-line answers — the Q&A pre-empted rather than improvised. | `rows:tableRows!` (max 6) |
| `conflict-disclosure` | Party, relationship, financial interest, recusal status per decision item. Cannot render a recommendation without its interest column. | `rows:tableRows!` (max 5) |

## Family F — Flow, constraint & scale (5 new)

Logistics frame plus the redeemable 10-year-old ideas — rebuilt as real dataviz forms rather than illustration.

| id | Layout | Slots |
|---|---|---|
| `bottleneck-lane` | 4–6 stage boxes with throughput under each, one rendered as a constricted neck plus a capacity-loss callout. Names the constraint. | `stages:tableRows!` (max 6) · `constraintIndex:text!` · `lossNote:text?` |
| `batch-vs-flow` | Split canvas: batched cadence (infrequent blocks) vs continuous (frequent ticks), with cycle-time and WIP per side. | `left.label:text!` · `left.stats:tableRows!` · `right.*` (same) |
| `unit-array` | One number as a dense array of identical marks with a single mark called out as the unit. A unit chart — geometry, not illustration. | `total:stat!` · `unitLabel:text!` · `arrayShape:shape!` · `caption:text?` |
| `waffle-share` | 100-cell grid with N filled — a proportion made countable. | `filled:stat!` · `label:text!` · `note:text?` |
| `scale-anchor` | A stat against explicit comparison bars at identical scale: prior period, plan, and a named external reference. | `metric:text!` · `value:stat!` · `comparisons:tableRows!` (max 3) |

## Family G — Product & engineering (10 new)

The largest absolute gap. None of these exist in any form.

| id | Layout | Slots |
|---|---|---|
| `product-screens-3up` | Three product screenshots in device or browser frames with captions. | `shots:imageRef!` (max 3) · `captions:tableRows?` |
| `screen-annotated` | One large screenshot with 2–4 numbered callouts pointing at regions. | `image:imageRef!` · `callouts:tableRows!` (max 4) |
| `before-after-screens` | Two screenshots side by side with a change summary — the UI counterpart to `before-after`. | `before:imageRef!` · `after:imageRef!` · `summary:text!` |
| `architecture-blocks` | Layered system diagram: 3–4 tiers of labelled blocks with connector lines. | `tiers:tableRows!` (max 4) · `note:text?` |
| `sequence-flow` | Left-to-right actor lanes with ordered steps between them — request/response, handoff, integration. | `actors:tableRows!` (max 4) · `steps:tableRows!` (max 6) |
| `now-next-later` | Three-column roadmap without dates, for work that isn't calendar-committed. | `now:tableRows!` · `next:tableRows!` · `later:tableRows!` (max 4 each) |
| `release-notes` | Shipped items grouped by category with a version header and date. | `version:text!` · `date:text!` · `groups:tableRows!` (max 6) |
| `incident-summary` | Timeline strip plus impact stats and the resolution line — the postmortem slide every engineering review needs. | `title:text!` · `timeline:tableRows!` (max 5) · `impact:stat!` · `duration:stat?` · `resolution:text!` |
| `metric-dashboard` | 6–8 small multiples in a grid, each a label + figure + sparkline — the working-review slide. | `tiles:tableRows!` (max 8) |
| `rag-status` | Workstream status grid with red/amber/green markers, owner, and a one-line note per row. | `rows:tableRows!` (max 7) |

## Family H — Customer & commercial (9 new)

| id | Layout | Slots |
|---|---|---|
| `logo-wall` | Customer or partner marks in a disciplined grid, one optional stat line beneath. | `logos:imageRef!` (max 12) · `stat:stat?` · `caption:text?` |
| `case-study` | One customer: the situation, what changed, and the outcome as figures. | `customer:text!` · `situation:text!` · `change:text!` · `outcomes:tableRows!` (max 3) · `logo:imageRef?` |
| `testimonial-grid` | 2–3 short quotes with attribution — the multi-quote layout `quote-pull` can't do. | `quotes:tableRows!` (max 3) |
| `pricing-tiers` | 2–4 plan columns with price, inclusion list, and one highlighted tier. | `tiers:tableRows!` (max 4) · `highlightIndex:text?` |
| `feature-matrix` | Feature rows against 2–4 columns with tick/cross/partial marks. | `features:tableRows!` (max 8) · `columns:tableRows!` (max 4) |
| `competitive-position` | Named competitors on two labelled axes — a positioning map, distinct from the abstract `matrix-2x2`. | `xAxis:text!` · `yAxis:text!` · `players:tableRows!` (max 6) · `usIndex:text!` |
| `market-sizing` | TAM/SAM/SOM as three nested figures with the derivation basis for each. | `tam:stat!` · `sam:stat!` · `som:stat!` · `basis:tableRows!` (max 3) |
| `unit-economics` | Per-unit ladder: revenue → cost lines → contribution, with payback and margin. | `rows:tableRows!` (max 6) · `contribution:stat!` · `payback:stat?` |
| `cohort-retention` | Cohort curves or a retention grid with the headline retention figure called out. | `chart:chartSpec!` · `headline:stat!` · `note:text?` |

## Family I — People, plan & spend (7 new)

| id | Layout | Slots |
|---|---|---|
| `hiring-plan` | Roles by period with count, function and status. | `rows:tableRows!` (max 7) |
| `org-target-state` | Current vs target operating model side by side. | `current:tableRows!` · `target:tableRows!` (max 5 each) · `note:text?` |
| `raci` | Responsibility grid: workstreams against named owners with R/A/C/I marks. | `workstreams:tableRows!` (max 6) · `people:tableRows!` (max 5) |
| `budget-variance` | Budget vs actual vs variance by line, with a total row and a variance-driver note. | `rows:tableRows!` (max 7) · `note:text?` |
| `spend-breakdown` | Where the money goes — categories with amount, share, and an optional prior-period column. | `rows:tableRows!` (max 6) · `total:stat!` |
| `capacity-vs-demand` | Two stacked bars or lanes comparing available capacity to committed demand across periods. | `chart:chartSpec!` · `gap:stat?` · `note:text?` |
| `sources-slide` | The deck's own references: numbered sources with title, publisher and date, matching in-deck superscripts. | `rows:tableRows!` (max 8) |

---

## Traps — flagged, not built

| Idea | Why it's a trap |
|---|---|
| `the-thing-eats-this`, `the-monster-under-the-bed`, `pass-the-parcel`, `the-marble-run` | All require bespoke illustration. The slot system carries `shape`/`imageRef` only, so these render as hand-drawn SVG — the exact anti-slop violation deck-craft bans. The salvageable core of two of them (unit array, waffle) is in Family F as real chart forms. |
| `hidden-mechanic-reveal` | Needs two visual states. Templates expand to static geometry server-side; a reveal is two slides or a build, not a layout. |
| `guess-then-look` | Same two-state problem, and it's a presenter technique rather than a layout. |
| `data-lineage-strip` | Genuinely useful but overlaps `number-provenance` and `claim-provenance-ledger`; a third provenance template splits usage across all three and none gets picked. |
| `estimate-vs-actual-vintage` | Subsumed by `returns-register` plus the existing `guidance-actual`. |
| `material-change-since-last` | Merged into `what-changed-since` — same layout, two names. |
| `if-you-stood-on-it`, `everyone-in-the-class` (giant-person variant) | Redeemed as `scale-anchor` and `waffle-share` respectively; the literal versions need illustration. |

---

## Build notes

- Templates carry **no colour and no font** — the deck theme resolves those. Nothing in a slot value
  may set a colour.
- `stat.value` stays ≤14 characters, always a figure. Every stat slot above inherits that.
- Every list slot needs a `max N` the layout can hold without overlap; the caps above are proposals,
  to be set against real rendered geometry.
- `non-ifrs-reconciliation` and `conflict-disclosure` should carry `CAVEAT` (mandatory footnote).
- `claim-provenance-ledger`, `comparable-transactions`-adjacent and `scale-anchor` external
  references should carry `SOURCE` (require a `source` slot).
- Nine new recipes are implied by these families and should follow separately: board-pack-decision,
  product-review, engineering-review, customer-QBR, sales-pitch, internal-strategy,
  postmortem, budget-review, all-hands.
