# Journeys — the axis that is a history rather than a state

Everything else in this skill quantifies over **states**. The coverage model is a
cross-product, the sweeps are per-surface, and the reconciliation partitions
entities. A defect that exists only as a *history* — an order, an accumulation,
an interruption, an elapsed hour, a difference from last week's build — has no
cell to fall into, so nothing counts it missing.

Asked what still escapes this methodology, six independent readings converged on
the same answer first — two single-shot CLI lanes and a four-backend Dossier
research panel, run on 24 Aug 2026 and none shown the others' replies: **model
the journey, generate action sequences over it, and run each sequence against the
previous accepted build as well as this one.**

The panel's contribution beyond agreement is the part that changes what you
build: it prices each addition and says which may hold a gate and which may only
advise. Reports and the brief are in `docs/deep-research/`; the weighting between
them is in Provenance at the end, and it is not "four backends agreed".

## What a journey model carries

A screen graph is not enough. The state a journey has to track, in the shape the
out-of-family lane put it:

```text
context  = tenant/account + entity identity + authoritative revision
workflow = unstarted | partial | pending | committed | failed | compensated
history  = route stack + deep-link origin
client   = cache + draft + pending queue + idempotency key
external = durable record + provider-effect ledger
```

Four properties over that state, and each is a real assertion rather than a
principle:

1. **Intent conservation.** Every accepted intent becomes exactly one committed
   effect, a visibly pending operation, or a visible terminal failure. Never
   zero, never two.
2. **Re-entry equivalence.** Back, Forward, a deep link and a fresh-process
   relaunch reconstruct the same logical entity and revision, or disclose a
   conflict. The property underneath: **the URL is a serialization of app
   state**, so every reachable journey state's URL, cold-loaded in a fresh
   profile, must reproduce that state.
3. **Context confinement.** Work started in context A cannot mutate context B
   after a navigation or an identity switch.
4. **Cross-surface provenance.** Two surfaces agree because they read the same
   entity at the same revision, not because they render the same plausible text.
   Seed fields with canaries encoding entity, tenant, writer and revision, so
   agreement is checkable rather than coincidental.

## Generating the sequences

Order is a coverage axis and it samples like any other. **Sequence covering
arrays** (Kuhn et al., NIST, *Combinatorial Methods for Event Sequence Testing*,
2012) are the sequential analogue of the t-way sampling `coverage-model.md`
already declares: they cover every t-way *ordering* of events rather than every
t-way combination of values. Declare the event-order dimension in the sample the
same way, and the campaign's existing "a declared sample is a finished plan for
those cells" rule carries over unchanged.

For generation and shrinking, both lanes named the same three tools: `fast-check`
model-based commands, Hypothesis `RuleBasedStateMachine`, and GraphWalker. All
three shrink a failing sequence, which is what makes a 40-step failure reportable.

## Boundary-indexed interruption

Sweep B injects a fault per request and sweep L kills a process. Neither is this:
cut at each **durable boundary** of a journey step — request issued, server
committed, provider effect landed, client persisted, user acknowledged — and
assert recovery at journey level rather than process level. Online → offline →
online, granted → revoked, foreground → killed → deep-link relaunch. The
assertion is intent conservation above, plus: no orphan queue work survives
quiescence.

`simctl privacy … revoke` on iOS and `adb pm revoke` on Android give the
permission half; a browser context gives offline and permission control directly.

## Differential replay against the previous build

Once the journeys exist, run each one against build N and build N−1 from
equivalent backend snapshots and compare a normalised semantic state vector after
every action. This converts **every behaviour of the previous build into an
oracle at zero specification cost**, which is the residue a requirement inventory
structurally cannot reach: it can only defend requirements somebody wrote down.

Two rules keep it honest, and both come from the panels:

- **Every intended difference maps to an entry in an expiring change manifest.**
  An unmapped diff is a finding; a mapped one is an accept that becomes the new
  baseline. Without the manifest this degrades into a diff wall nobody reads.
- **The previous build is a witness, not the specification.** Where both builds
  violate an independent invariant, agreement still fails. Run the requirement
  and effect invariants against both.

## The rest, ranked by yield over effort

Both lanes produced a ranking; where they agreed the item is listed once, with
the cheaper lane's effort estimate. Effort: S ≈ 1–3 engineer-days, M ≈ 1–2 weeks,
L ≈ multi-week.

| Addition | What it catches | Effort |
|---|---|---|
| Differential journey replay vs N−1 | Every unspecified behaviour that regressed | M, low once journeys exist |
| Pseudo-localisation and RTL | Truncation, concatenation, un-externalised strings, mirroring — one build sweeps the whole class | S |
| Dual-clock temporal matrix | DST fold and gap, leap day, midnight rollover mid-journey, client/server skew, wrong "today" | S–M |
| Boundary-indexed interruption and recovery | Partial completion, duplicate effect, wedged re-entry | S–M |
| Assistive-technology task execution | The journeys a screen reader cannot complete on a surface that passes a rule engine | M |
| Performance as a correctness oracle | Jank that eats input, a control too slow to use, growth that gets the app killed | S–M |
| In-place upgrade matrix | Work lost at migration, a migration that runs twice, entry through an old schema | M |
| Telemetry contract testing | Duplicate, missing or misattributed events on a surface with no oracle at all | S–M |
| Systematic schedule exploration | A stale response overwriting a newer edit; retry racing reconnect | M–L |
| Resource-slope endurance | Listener, DOM, heap and handle accumulation that only breaks after hours | M |
| Mode confusion | Correct mechanics against the wrong tenant, version or edit mode | M–L |
| Production-trace mining | Which journeys actually matter, weighted by use | M–L |
| Input-method semantics | IME composition, dead keys, dictation, paste, grapheme deletion | S |

Two notes on reading that table. **Rank by your product, not by the row order** —
the temporal matrix is first for anything scheduling, the schedule exploration
first for anything with autosave or realtime. And an item is only an omission
here if the sweep that sounds like it does not already carry the stronger
mechanism: sweep B is per-request rather than per-boundary, sweep F is static
authorisation rather than mid-session revocation, and sweep L is process-level
rather than journey-level. Where yours already does the stronger thing, the row
is covered.

## The model oracle: what it is for, and what it may gate

A four-backend Dossier panel (24 Aug 2026) settled this more precisely than the
two CLI lanes did, and corrected them. The rule it converges on is one sentence:
**model-assisted, deterministically executed.**

Let a model select journeys, generate meaningful input, interpret ambiguous
semantics and rank diffs. Record the exact actions, the prompt, the screenshots
and the model version. **Then replay the resulting trace without the model**, and
require a deterministic confirmation — a state or effect query, a property check,
an accessibility-tree invariant, an exact text or order check, or a person —
before any release-blocking defect is declared.

| Task | What the model is for | Measured | Disposition |
|---|---|---|---|
| Scenario navigation, meaningful input | Infer intent, open hidden menus, keep history across a long workflow | ScenGen: 99 tasks / 92 apps, 86.87% coverage, 84.85% completion | Generate or repair the trace; replay deterministically |
| Semantic accessibility | Judge alt text, relationships, contextual fit — things a rule engine cannot encode | GenA11y: 95.2% precision, 87.69% recall; axe-core 12.74% recall on the same benchmark | Advisory unless converted to a deterministic predicate |
| Non-crashing visual-functional bugs | Read a screenshot sequence for wrong sort order, wrong destination, missing post-action state | VisionDroid: 50–76% precision, 42–64% recall initially | Candidate generation and triage, never the sole blocker |
| Intended-change classification | Compare an observed delta against the change description | RippleGUItester found real missed bugs across four systems | Advisory triage |
| Exact layout and geometry | Nothing defensible over a deterministic oracle | No controlled evidence a model beats a stable exact oracle | Deterministic gate |
| Server and effect correctness | Can guess the expected outcome; cannot prove a commit, idempotency or cross-system state | No head-to-head evidence | Deterministic ledger gate |
| Timing and resource bounds | Explain anomalies, cluster traces | No credible precision/recall benchmark found | Deterministic statistical gate |
| Telemetry contract | Interpret event names, spot likely omissions | No UI-specific controlled study found | Deterministic gate |

Three caveats the panel is explicit about, and each changes how a number may be
used:

- **GenA11y's benchmark is 148 pages that deliberately contain known issues.**
  That is a conformance corpus, not the distribution of defects in a live
  product. The relative result against rule engines is the strong part; the
  absolute precision is not transferable.
- **Precision is not a false-positive rate**, and the panel names relabelling one
  as the other as a specific error. Class-conditional false-positive rates across
  live product changes, repeated-run variance and provider-version sensitivity
  were all recorded as `MISSING_DATA` for both GenA11y and VisionDroid.
- **The two CLI lanes disagreed here and both were partly wrong.** One reported
  "~96% precision" for a hybrid model without naming the task; the other read the
  same figure as resting on a 110-bug synthetic benchmark, which is the
  *lifecycle-fault* corpus rather than the accessibility one. The panel's reading
  — 95.2% precision on semantic accessibility, 148 curated pages — is the one
  recorded here, because it names the task, the corpus and its provenance.

## What to gate and what to advise

The panel's ranking, reproduced with its own framing: it labels itself an
inference from reported yield, corpus size and implementation complexity rather
than a measured cross-study league table, and that label travels with it.

| Rank | Addition | Yield per effort | Enforcement |
|---:|---|---|---|
| 1 | Journey-prefix interruption and process-death matrix | High — 110-fault benchmark, layers onto journeys you already have | Mechanical gate on state/effect reconciliation |
| 2 | Previous-build semantic differential with a change-intent manifest | High — RegDroid found 14 unique functional bugs, ten of them new | Gate retained invariants and undeclared differences; raw diffs advisory |
| 3 | Critical journeys with a server/effect ledger | High, medium-high setup — targets partial commits and cross-surface divergence | Mechanical gate on the highest-value workflows |
| 4 | Event-order, adjacency, repetition and race bundle | Medium-high | Gate declared coverage and deterministic failures; schedule anomalies advisory |
| 5 | Screen-reader-driven journeys plus semantic accessibility | Medium-high — rule engines demonstrably miss semantic criteria | Gate the transcript invariants; model and human judgement advisory |
| 6 | Permission, offline, time and pseudo-locale bundle | Medium, low automation cost | Mechanical where the expected transitions are explicit |
| 7 | Production trace mining and replay | Medium — finds real prefixes, but replay failure is common | Selection advisory; a successful deterministic replay gates |
| 8 | Upgrade and aged-account matrix | Medium, potentially high severity — expensive data curation, weak published yield | Gate the supported upgrade paths and high-value archetypes |
| 9 | Telemetry contract reconciliation | Medium, cheap once a collector exists | Mechanical gate for consent, purchase, onboarding, experiment events |
| 10 | Soak and resource-slope endurance | Portfolio-dependent — higher for native desktop, media, realtime | Advisory until variance is calibrated, then gate strong monotonic leaks |

Rank 2's triage cost is the one to price honestly: differential testing against
the previous build carried a **64% false-positive rate from intended changes** in
the published study, which is why the change-intent manifest is part of the
method rather than an optional tidy-up.

## Where the panel disagreed, which is the part worth reading

Four backends read 111 sources with 1% overlap, so agreement between them is
weak evidence and disagreement is strong. Three splits, unresolved on purpose:

**Pseudo-localisation: rank 1 or rank 6.** Gemini puts it first — high yield,
low effort, "only importing a string-manipulation library and a pre-flight script
to swap the locale asset during the t-way matrix you already run." OpenAI folds
it into a rank-6 bundle and calls the yield evidence for it thin. Both are right
about different things: the *cost* is genuinely near zero, and the *published
yield* genuinely is thin. Take Gemini's ranking if you ship in more than one
language, OpenAI's if you do not.

**Race detection: rank 4, rank 7, or gate-worthy.** Perplexity carries the only
hard numbers — AjaxRacer's 152 tests, 65 harmful races over 12 of 20 pages, 7
false positives — and argues from that low false-positive rate that it can be
mechanically gated. Gemini ranks it 7th on effort. OpenAI puts the bundle 4th
with schedule anomalies advisory. **Perplexity's is the only position resting on
a measured false-positive rate, so it is the one recorded in sweep U.**

**Record-replay: useful or a maintenance sink.** Perplexity is blunt that
record-replay tests of web applications break as the application evolves —
dynamic content, async timing, DOM structure invalidating recorded selectors —
and that its yield per unit effort is poor *used alone*. Its constructive form:
record to discover the flow, then abstract into a stable model, and let session
mining choose which flows are worth the abstraction. Nobody's numbers support
replay as a standing gate.

One thing all four agree on, and it is worth more than the rankings: **partial
completion against a server that already committed is a defect class no
per-surface test can reach.** A transaction authorised server-side and abandoned
client-side, returned to through a different tab, surface or deep link, is where
duplicate charges and missing confirmations live. It is the reason the effect
ledger sits outside the restored client snapshot in sweep O.

## Provenance

Two rounds, and they are weighted differently.

**Round 1, two single-shot CLI lanes**, 24 Aug 2026 —
`docs/deep-research/codex-gpt56-gap-review.md` (gpt-5.6-sol, effort high) and
`fable5-gap-review.md` (claude-fable-5, effort high), against
`gap-review-2026-08-24.prompt.md`. Both converged on the journey axis first. They
are opinion rather than sourced research, and where the panel contradicts them
the panel wins.

**Round 2, a four-backend Dossier panel** at max tier, same day, briefed on this
campaign's actual contents — `docs/deep-research/2026-08-24-panel-*.md` for
OpenAI gpt-5.6-sol, Gemini Deep Research, Perplexity Sonar and Claude Code.
Merged deterministically: **111 distinct sources across 38 independent domains,
with only 1% overlap between members.** That low overlap is the reason a
single-member claim here is marked uncorroborated rather than agreed.

Two things about that panel a reader should know before trusting a count:

- **Gemini's 57 citations are not 57 identifiable sources.** Forty-one percent of
  all merged sources sit on one domain because most of Gemini's are opaque
  `vertexaisearch` grounding redirects that never name the underlying document.
  Its identifiable sourcing is closer to 12. The figures quoted in this file come
  from the OpenAI member (31 registry sources, real DOIs and arXiv ids) and
  Perplexity (20, including NIST primary PDFs).
- **The OpenAI member's citations were checked**: 42 dereferenced, **0
  fabricated, 0 dead**, 71% opened directly and 88% shown to exist. The nine
  blocked are ACM and ResearchGate bot walls over registered DOIs. Reachability
  is not support — that still needs a reader — but fabrication is the number that
  decides whether a report can be used at all, and it passed.

The `agy` lane refused to start: Dossier resolved the binary, got version
`1.1.19`, could not identify it as Antigravity CLI, and declined to hand the
brief to an unidentified vendor. That is a refusal rather than a failure, and it
means this panel is four backends rather than five.
