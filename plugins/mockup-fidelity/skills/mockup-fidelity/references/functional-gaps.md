# The functional-gaps document

## Why this exists

When you align an implemented screen to a mock, you make it **look** right. But a mock is a static picture — it shows a "Browse by sector" tab, an "Ask in plain English" search, a "Movers today" rail, a verified-holder badge — without any of the machinery behind them. The moment you add one of those affordances to the real app to match the mock, you have created a control that, by default, **does nothing real**: there's no endpoint, no query, no data source, no navigation target, no permission check.

A pixel-perfect screen wired to nothing is the most expensive kind of false-done: it passes a visual review, ships, and only fails when a user taps it. So every alignment pass **must** end with an honest, explicit list of the functional work the new/aligned UI now implies. This is the document that turns "it looks done" into a real backlog.

It is also the antidote to the **cosmetic-affordance** trap — an "AI" badge that does substring search, a mic icon with no recogniser, a filter chip that filters nothing. Those *look* like features in both the mock and the aligned app; the gap doc is where their missing behaviour is recorded instead of silently shipping.

## When to write it

Always, at the end of an alignment pass — even if the answer is short. Write it whenever you:
- add an affordance the app didn't have (a tab, a search mode, a card, a CTA, a sheet);
- align a screen whose mock shows data the app doesn't currently fetch;
- find a control that renders but isn't wired (the cosmetic-affordance case);
- discover a feature the mock implies that needs a backend that may not exist.

Save it to the repo (e.g. `docs/<surface>-functional-gaps.md`) so it survives the session and can become tickets.

## What to capture per gap

For each added or visual-only affordance, record:

- **Affordance** — what the user sees (the control/section and where).
- **Current state** — `not built` / `visual only (renders, does nothing)` / `partially wired` / `wired to placeholder/mock data`.
- **Functional work implied** — the concrete pieces: backend endpoint(s), GraphQL field / query / mutation, data source / external feed, navigation target/route, permission/role check, the empty / loading / error states the mock doesn't show, analytics events.
- **Blocking?** — does shipping the screen without this mislead the user (a dead button) or is it a graceful no-op?
- **Owner / next step** — who/what closes it, or "ticket TBD".

## Template

```markdown
# Functional gaps — <surface/screen> (aligned to <mock> on <date>)

Aligning <surface> to the mock added or surfaced UI whose behaviour is not yet
implemented. Each row is functional work the new UI now implies — not a styling
issue. "Visual only" means the control renders but is not wired to anything real.

| Affordance | Current state | Functional work implied | Blocking? | Owner / next step |
|------------|---------------|-------------------------|-----------|-------------------|
| Browse by sector tab | not built | new `sectors` query (GICS groups + company counts); sector→companies route; empty/loading states | yes — mock leads with it | ticket TBD |
| "Ask in plain English" search | visual only — "AI" badge does substring match | NL-query interpretation endpoint; results schema (companies + announcements + reasoning); error state | yes — looks AI, isn't | ticket TBD |
| Voice / mic input | not built | speech-to-text wiring; permission prompt; fallback when unsupported | no — can omit the icon for now | decision needed |
| Verified-holder badge | gated off by a flag | holding-verification flow + backing data; flag flip | no — intentionally off | tracked elsewhere |

## Notes
- <Anything the mock implies that needs product/backend decisions before it can be built.>
- <Data the screen now displays that isn't currently fetched, and where it would come from.>
```

## How it interacts with the audit

The fidelity ledger (SKILL.md Phase 5a) answers *"does the built UI match the mock?"* The functional-gaps document answers the next question the ledger raises: *"now that it matches, what doesn't actually work yet?"* A row that the ledger marks `absent` and you then **build** becomes a functional-gaps row (its wiring is the new work). A row marked `present` but flagged as cosmetic in Phase 4 becomes a functional-gaps row too. Keep the two documents distinct — one is about appearance, one is about behaviour — but produce both.
