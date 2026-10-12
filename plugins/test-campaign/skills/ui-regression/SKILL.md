---
name: ui-regression
description: Repeat a bounded UI regression journey across navigation, keyboard, light/dark themes and compact/wide widths, with current target identity and effect evidence. Use for repeated UI checks or a named flow; use test-campaign for a full application campaign.
---

# Repeatable UI regression

Keep the named journey and stopping condition. Read the existing project harness
and prior case before creating a parallel suite. This is a focused entry point
to `test-campaign:test-campaign`, not permission to run a full application audit,
fix unrelated features or publish results. Record target app/build/commit, base
URL or bundle id, account/role, data setup, source requirement, test instrument,
run time and permitted write scope. Past history or a mock cannot verify today's
running product.

## Freeze the journey and variants

Create a reusable case with a stable id, starting state, semantic navigation
targets, action sequence, expected destination and observable effect at each
step. Avoid absolute screen coordinates unless there is no supported alternative;
if required, bind them to a fresh screenshot/window geometry and fail on mismatch.
An opened tab is not proof its requested destination loaded. Read the route,
window or source state after each important transition. Keep setup and cleanup
explicit, with test data in a permitted disposable environment.

Use the project's actual theme and compact/wide breakpoints. Record exact widths
and how the theme was forced; a screenshot filename does not prove either.
Cover the requested light/dark × compact/wide combinations and include keyboard
navigation in the cells where responsive layout changes focus or controls. If a
cell cannot be reached, report blocked/inconclusive with the reason and keep it
in the denominator. Do not claim a sampled set is exhaustive. For a user request
that only names one width or theme, preserve that scope rather than expanding it.

## Execute with the right instrument

Use the project's browser/e2e harness for web and supported native instrumentation
for desktop. Route native foreground turns through `proctor:proctor` when available,
and build/suite admission through `harbourmaster:harbourmaster` where applicable.
Discover actual tool capability before relying on an AX-only instrument for
pixels or a screenshot for keyboard effects. An explicit app safety denial is a
stop for that route; never bypass a `com.mitchellh.ghostty` denial through another
CUA, shell, AppleScript or capture path. Missing instruments are a named blocker.

For each relevant variant:

- Follow the journey through actual navigation. Assert destination identity and
  the meaningful state change; a present button or the product's own success
  toast cannot alone prove an external effect.
- Exercise Tab/Shift-Tab, Enter/Space and applicable Escape/arrow behavior. Check
  focus order, visible focus, trapping and restoration after dismissal. Keep the
  expected keyboard convention tied to the actual control/platform.
- At compact width inspect collapsed navigation, overflow, clipped actions and
  retained state; at wide width inspect expansion and reading order. Test
  transitions between widths when the request concerns retained state.
- Verify rendered theme, legibility and interaction states at current capture
  targets. Retain capture lineage, build and variant identity. Route actual
  visual comparison to `be-my-witness:be-my-witness` if available; the requirement
  is the oracle and design mocks are advisory.

Reset to the declared starting state between independent variants. Restore only
temporary settings changed by this authorised test, without overwriting a user's
subsequent choice. OS-wide appearance/account changes and destructive live-data
steps require applicable authority; prefer per-app test overrides or disposable
fixtures. Do not sign the user out of their only account to manufacture a state.

## Compare and stop

Extend the project's existing tests and campaign registry where appropriate;
follow the campaign's current schema and required gates rather than inventing
ledger fields. Compare only compatible builds, states, data and capture framings.
Report every planned cell as pass, fail, blocked or inconclusive with evidence
and the number actually exercised. Preserve defects with stable ids and minimal
reproduction steps; rerun affected cells after authorised fixes, broaden only
when the change affects shared navigation/theme/breakpoints or new failures.

Stop when the selected journey has been exercised at the requested variants and
each expected effect has evidence or an explicit gap. Creating this case does
not schedule recurring QA or approve a release. Existing supervised agent work
can be handed to `flagship:fleet-console` with the exact case, artifact and owner.
