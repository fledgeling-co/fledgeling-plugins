---
name: shipyard
description: >-
  The shipyard pipeline's router and map — explains the seven stage skills (intake, triage,
  plan, design, work, verify, gap-fix), the status machine they move features through, and which
  stage a given situation calls for. Use when someone asks "how does the shipyard pipeline
  work", "which stage do I run", "what's the status flow", or invokes /shipyard without naming a
  stage. It routes and explains; the stage skills do the work, and the conductors (ship-feature,
  ship-fleet, ship-armada) drive them end to end.
---

# Shipyard — the map

Seven stage skills take a feature from rough idea to independently verified code. This skill is
the router: say which stage fits, and point at the shared canon. It never performs a stage
itself.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It turns this map's counts — seven stages, eight statuses, nine canon files — into a ledger an answer must fill, and makes the routing read the reference files rather than recall them, because a router is one sentence away from performing the stage it should be handing over. Other models skip it.

## The stages, and when each is the one you want

| You have | Run | It produces |
|---|---|---|
| A rough idea ("an app that does X") | `intake` | Briefs in `docs/features-to-triage/`, plus separable AI-proposed companions |
| A brief or ticket needing a readiness check | `triage` | The verdict + assumptions → status `To Do`, or `Needs More Info` with essential questions |
| A triaged feature needing its build plan | `plan` | A committed `docs/plans/<id>.md` with a test strategy → `Ready for AI` |
| A user-facing feature needing its UI settled | `design` | All-platform mocks + a state matrix, gated by design-review and be-my-witness |
| A planned feature ready to build | `work` | The branch in `.worktrees/<ID>` with evidence tables → `Developer Review` |
| A built feature awaiting grading | `verify` | A cross-family verdict against the running app → `Done` or `Needs More Work` |
| A failed verdict or a QA gap list | `gap-fix` | The gaps closed in code → back to `Developer Review` for re-verification |

For a whole feature end to end, use the `ship-feature` conductor; for a backlog, `ship-fleet`;
for a portfolio, `ship-armada`. Prefer a conductor whenever the goal is a finished feature
rather than one stage's artifact.

## The status machine (one enum, complete)

`(untriaged)` → `Needs More Info` | `To Do` → `Ready for AI` → `In Progress` →
`Developer Review` → `Done` | `Needs More Work` (→ `gap-fix` → `Developer Review` → …)

Only `verify` sets `Done`. Every transition requires its artifact; the full rules live in
`${CLAUDE_PLUGIN_ROOT}/references/tracker-adapter.md`, which also covers the two substrates
(markdown specs vs a tasks-MCP board).

## The shared canon

Everything the stages have in common lives once, in `${CLAUDE_PLUGIN_ROOT}/references/`:
`model-lanes.md` (who runs on what, and the two invariants), `second-opinion-lanes.md` (settle
it with a model before the human), `evidence-rules.md` (what closes a claim),
`test-strategy.md` (the coverage bar), `executor-lanes.md` + `codex-cli.md` (delegated
implementation), `operational-rules.md` (the incident ledger), and `evidence.md` (where every
rule came from).
