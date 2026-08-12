---
name: proctor
description: Run a real test campaign against a native macOS app — exploratory sweep, acceptance criteria turned into executable flows, state-matrix and edge coverage, accessibility audit, visual fidelity, determinism measurement, and a report that separates what was proven from what was assumed. Drives the Proctor MCP server, which reads the accessibility tree and screen contents and actuates through the process-directed plane, so background, occluded and other-Space windows are all reachable without stealing focus. Use this when someone asks to test, QA, exercise, audit, smoke-test or find bugs in a Mac app, a SwiftUI or AppKit or Catalyst or Electron app, a menu bar app or a preference pane — when they ask whether a Mac app is ready to ship, whether a flow still works, why a test is flaky, or what breaks in dark mode or at a larger text size. Also use it when a macOS UI needs checking against acceptance criteria or a mockup, and when someone wants a Mac app driven end to end by an agent rather than by hand.
---

# Proctor

You are running a test campaign against a native macOS application, using
instruments rather than impressions. The distinction runs through everything
below: a screenshot you looked at is an impression, a screenshot with a frame
status and a dirty-rect summary is an instrument reading. Only one of them
can be wrong in a way you would notice.

The campaign produces a report a person can act on, in which every claim is
traceable to a tool result, and everything that could not be established is
named rather than quietly omitted.

## What this owns, and what it hands off

Proctor owns **native macOS applications**. The neighbouring skills own
adjacent ground and are better at it:

| Hand off to | For |
|---|---|
| `acceptance-e2e` | Web features and Playwright suites. Proctor is the native counterpart, not a replacement. |
| `design-review` | Judging whether a rendered UI is any good. Proctor supplies the captures and the accessibility data; the judgement belongs there. |
| `mockup-fidelity` | React and React Native builds measured against a reference mockup. Its ledger discipline — present, divergent, absent, with the burden of proof on the build — is the right method for native fidelity too, and this skill reuses it rather than inventing a second one. |
| `macosify` | Fixing native-idiom problems. Proctor finds them; that skill refits them. |

A web view inside a Mac app is still Proctor's, because reaching it means
attaching to the host process. A pure web app in a browser is not.

## Before anything else

Run `proctor_doctor`. It costs one call and it is the difference between a
campaign and an hour of retries.

When no `proctor_*` tool is available at all, the MCP server is not configured
in this host. Point the user at `~/Dev/proctor-mcp` — `scripts/install.sh`
builds and loads it and prints the `claude mcp add` line — and stop, since
there is nothing to drive until it is there.

A missing Accessibility grant presents as elements not being found, which
reads exactly like a selector bug and which a model will paper over by trying
again. Screen Recording cannot be granted silently on any macOS version, so
if the report says it is missing, a person has to click it before capture
works at all. `doctor` names the exact fix for the running OS version.

When `ready` is false, surface the blockers and stop. Proceeding produces a
report whose failures are all yours.

## Attach once

`proctor_apps` with `action: "attach"` starts a stateful session: it warms the
accessibility tree, applies `AXManualAccessibility` when the app is Chromium-
or Electron-based, starts observers, and begins retaining element references.

Attach at the start and reuse the handles. A retained reference keeps
resolving when its window moves to another Space; re-enumerating does not find
it. This is why the server is stateful and why re-attaching mid-campaign
throws away the thing that makes background windows reachable.

Read the returned `provenance`. When `manualAccessibilityApplied` is true, the
app under test is being observed in a mode it does not run in for real users:
the flag is detectable by the app and changes its performance. Carry that into
the report's methods note. A fidelity finding measured under an observer
effect is still a finding, but it is not the same finding.

## The campaign

Seven stages. Run them in order — each one's output narrows the next — and
stop early with what you have if the app turns out to be unreachable.

### 1. Exploratory sweep

`proctor_snapshot` the main window, then walk outward: menus via the menu bar,
each window the app offers, each tab or sidebar section. Use `proctor_find`
rather than pulling whole trees once you know what you are looking for.

You are building an inventory, not testing yet: which controls exist, which
carry `AXIdentifier` (those are the durable selectors — a developer set them
deliberately, so they survive copy changes and localisation), which are
unlabelled, and where the tree goes suspiciously flat or empty. A flat subtree
under a rich-looking view is usually a custom control that never adopted
accessibility, and that is both a finding and a limit on what you can test.

### 2. Acceptance criteria into flows

Turn each criterion into a `proctor_flow` recording. Start one with
`action: "start"`, then pass its name as `record` on each `proctor_act` call so
the steps land in it, and close it with `action: "stop"`. Assert separately with
`proctor_assert` — a flow stores steps, the selector each one resolved through,
and the per-step hashes from the recording run, which is what lets a later
replay say where it diverged rather than only that it failed.

Batch the steps into as few `proctor_act` calls as the logic allows — a six-step
login is one call, and each step settles before the next runs.

Two habits are worth keeping. Prefer `AXIdentifier` selectors over titles.
And leave `foreground: false` unless a step genuinely needs the front: a flow
that runs in the background is one that can run while someone uses the
machine, and proving it works there is worth more than proving it works with
the window raised.

### 3. State matrix and edges

The states that break Mac apps are known, so cover them deliberately rather
than hoping to stumble into one: empty, single item, many items, maximum,
loading, error, offline, permission denied, first run, restored session.
Cross those with dark mode, an increased text size, a reduced-motion setting,
a narrow window, and a second display where one exists.

Record which cells you actually exercised. A matrix with unrun cells is fine;
a matrix that implies it was fully run is not.

### 4. Accessibility audit

`proctor_assert` with the auditing kinds: every interactive node has a label,
contrast meets threshold, hit targets meet a minimum size, focus order
follows visual order.

Then run the tri-observer check — `kind: "agree"`. Where the accessibility
tree, the geometry source and the pixels disagree about the same instant, the
delta is a defect with a name: an unexposed control, a ghost node, an
invisible-but-focusable element, a stale frame, a wrong hit target. This is
the pass that finds what neither a screenshot review nor a tree dump finds
alone, because it is looking for the disagreement rather than at either
source.

### 5. Visual and fidelity

`proctor_capture` each state. Every capture reports its own trustworthiness —
frame status, content rect, dirty area, frames waited. When `trustworthy` is
false, the caveat says why, and an off-screen window that only produces
complete frames when the pointer moves on its display is a real
ScreenCaptureKit behaviour rather than a bug in the run. Never treat an
untrustworthy frame as evidence; capture again with the window raised and say
that you did.

For an app that embeds `ProctorReflector`, `proctor_inspect` returns resolved
colours, fonts, corner radii, constraints and both layer model and
presentation values. That is measurement. For an app you do not own there is
no cross-process computed-style API on macOS, so the ceiling is the
accessibility tree plus pixels — say so rather than approximating a value you
cannot read.

Route the question "does this look right" to `design-review`, with your
captures attached.

### 6. Determinism

`proctor_stability` on every flow you intend to trust, five runs by default.

It returns `firstDivergence` and per-step instability. A flow whose runs
diverge at step 3 does not need its step 9 assertion investigated, and a step
with instability above zero is nondeterministic before anyone argues about
whether it is correct. This is what separates a real defect from a flaky test,
and running it before reporting failures saves reporting noise as findings.

### 7. Report

Length: proportional to what you found. A clean campaign on a small app is a
page. Do not pad a short result into a long one.

Structure it as:

- **Verdict** in one line — ready, ready with named caveats, or not ready.
- **What was proven**, each item naming the flow and the assertion.
- **Defects**, ranked by severity, each with the step that produced it, the
  evidence (a capture path, a tree excerpt, a disagreement record), and a
  reproduction as a flow name.
- **Flaky, not broken** — anything `proctor_stability` showed to be
  nondeterministic, kept separate from defects, because conflating them sends
  someone hunting a bug that is a race.
- **Not covered**, listing the matrix cells you did not run and why.
- **Methods**, naming the OS version, whether `AXManualAccessibility` was
  applied, which settle signals were available, whether a reflector was
  embedded, and which captures came back untrustworthy. Write it out in full
  when it is asked for — a methods section handed back as headings for someone
  else to complete is the one section whose whole value is that it was actually
  filled in.

An assertion that could not be evaluated is not an assertion that passed.
Report it as skipped, with the reason.

## Honesty of a settle

Every action settles before the next runs, and settling is a conjunction —
quiet frames, quiet accessibility notifications, the app's own idle signal
where one exists, bounded by a timeout. Never a sleep.

The signals do not carry equal weight, and `SettleReport.reason` says which
one you got:

| Reason | What it means |
|---|---|
| `allSignalsQuiet` | Pixels and the tree both went quiet. The strongest evidence available by inference. |
| `reflectorIdle` | The app said it was done. The most honest signal there is, because it is the only one that is not inference — but it comes only from an app that embeds the reflector. |
| `axQuietOnly` / `captureQuietOnly` | One signal concluded. Adequate, and worth noting when a result is surprising. Watch for `captureNeverQuiet` in `signals`: it means the window animates continuously — a caret, a spinner — so pixel-quiet was unreachable and the settle concluded on the tree alone. |
| `timeout` | Nothing went quiet. The step's result is a guess; treat a failure after a timeout settle as unproven rather than as a defect. |

## Two planes, and why it matters

Actions travel through one of two planes, and every step result says which.

**Process-directed** — accessibility actions, attribute writes, Apple Events.
These are IPC to the target, so they reach non-frontmost, occluded and
other-Space windows without stealing focus, and Secure Event Input does not
block them. This is the default and it is what makes unattended testing
possible.

**Synthetic events** — `click`, `hover`, `dragPath`, `key`, and `type` into a
field whose value the accessibility plane cannot write. These enter the
single system event stream, so they need the app in the foreground and they
interfere with whoever is using the machine. Secure Event Input makes them
unreliable — it is aimed at keyboard interception, and the evidence supports
"injection unreliable, observation blocked" rather than a blanket block — while
leaving the accessibility and Apple Events planes working. Reserve them for what the accessibility plane genuinely cannot
express: drag paths, canvas surfaces, hover-only states, text composition, and
testing keyboard shortcuts or focus behaviour as such.

When a step comes back with `plane: "syntheticEvent"`, the result proves
something narrower than a process-directed one did — it proves the app works
when it is in front. Say so if it matters.

A step whose accessibility route the element refuses fails rather than quietly
becoming a synthetic event, and the error names both ways forward: re-run with
`foreground: true`, or reach the same end through an attribute write that stays
on the accessibility plane. Taking the second route keeps the result
background-safe.

## Scale

One session drives many windows concurrently, because process-directed
actuation does not contend for focus. That is where parallelism lives.

Apple silicon caps concurrent macOS guests at two, so a VM fleet is not the
answer, and more real parallelism past that is a hardware purchase rather than
a configuration change. Do not design a campaign that assumes otherwise.

## Delegating

Most campaigns run in one session. Spawn subagents only for genuinely
independent work — a separate app, or a matrix cell that needs its own window
— and cap the fan-out at four. The session state that makes this server work
lives in the agent, not in you, so parallel subagents share it and stepping on
each other's windows is the common failure.

Subagents never run git operations.

## Depth

- `references/tools.md` — the eleven tools, their arguments, and the
  decision each one exists to serve.
- `references/methodology.md` — the state matrix in full, the accessibility
  rubric, the fidelity ledger, and the disclosure requirements.
- `references/evidence.md` — the research behind every rule above, with
  citations.
