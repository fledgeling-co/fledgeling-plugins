---
name: proctor
description: >-
  Run a real test campaign against a native macOS app — exploratory sweep, acceptance criteria turned into executable flows, state-matrix and edge coverage, accessibility audit, visual fidelity, determinism measurement, and a report that separates what was proven from what was assumed. Drives the Proctor MCP server, which reads the accessibility tree and screen contents itself — every capture carrying its own frame trustworthiness — and actuates through the process-directed plane, so background, occluded and other-Space windows are all reachable without stealing focus. Use this when someone asks to test, QA, exercise, audit, smoke-test or find bugs in a Mac app, a SwiftUI or AppKit or Catalyst or Electron app, a menu bar app or a preference pane — when they ask whether a Mac app is ready to ship, whether a flow still works, why a test is flaky, or what breaks in dark mode or at a larger text size. Use it too for the UI/UX design side of a Mac app: checking a rendered UI against acceptance criteria or a mockup, and checking whether it is native and correct — right control sizes, right type ramp, no non-native tells — a design test the platform itself is the answer key for. Also use it when a specific test case or suite needs running against a Mac app, and when someone wants a Mac app driven end to end by an agent rather than by hand. It carries a second, much narrower lane for iOS Simulator apps — deep links through `simctl` and Maestro flow files — so use it for putting an iOS app into a named state and scoring a flow, while knowing that lane has no accessibility tree, no elements and no geometry.
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

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. Turns proctor's instrument-reading discipline into a mechanical contract on Gemini: every claim quotes the MCP tool return and field it rests on (there is no exit code to paste), the case matrix, state matrix, capture set and fidelity ledger become a filled table with denominators before the first proctor_act, and platform conformance numbers are read from the rubric files rather than recalled. Other models skip it.

## What Proctor observes, and why that is the whole point

Proctor can delegate the clicking. It does not delegate the looking, and that
asymmetry is the reason a Proctor result is worth more than the same result from
anything else that drives a Mac.

Three observation channels are Proctor's own and stay Proctor's own:

- **Capture, with frame trustworthiness attached.** Apple defines six
  `SCFrameStatus` values and makes checking them a precondition of trusting a
  frame. Every `proctor_capture` reports `status`, `contentRect`,
  `dirtyRectCount`, `dirtyArea`, `framesWaited`, `trustworthy` and a `caveat`
  naming the cause when trust fails. A stale frame is pixel-identical to a
  correct one, so those fields are the only thing separating them. General
  screenshot tools return the image and nothing else, which means a caller
  cannot tell the two apart at all.
- **The accessibility walk**, with a `TreeProvenance` saying how the tree was
  obtained, whether `AXManualAccessibility` was applied and where the walk was
  truncated.
- **The verdict layer** — assertions, the tri-observer `agree` check, settle
  reporting, determinism scoring. These are judgements about the application
  under test, which is a different job from scoring an agent.

Read the metadata rather than the image. `trustworthy: false` means this capture
is not evidence of anything, whatever it looks like when opened.

## What this owns, and what it hands off

Proctor owns **native macOS applications**. The neighbouring skills own
adjacent ground and are better at it:

| Hand off to | For |
|---|---|
| `acceptance-e2e` | End-to-end acceptance criteria traceability, multi-surface sweeps (Web, macOS, iOS, Windows), and test suite orchestration. `acceptance-e2e` invokes `proctor` for all macOS native app execution and geometry assertions. |
| `be-my-witness` | Automated visual diff-masking and comparison against reference design mocks. Proctor captures live UI frames and component slices, then hands them to `be-my-witness` to classify layout, styling, and typography deviations with mock-as-oracle discipline. |
| `design-review` | Judging whether a rendered UI is any good. Proctor supplies the captures and the accessibility data; the judgement belongs there. |
| `mac-design-studio` | The native-conformance rubric when there is no mockup: the macOS 27 control ladder, type ramp, label tiers, 8pt grid and the ten-point native-tells audit are the oracle for "is this a correct, native Mac UI". Proctor measures the rendered tree and pixels; that skill says what native is. |
| `mockup-fidelity` | React and React Native builds measured against a reference mockup. Its ledger discipline (present, divergent, absent, with the burden of proof on the build) is the right method for native fidelity too, and this skill reuses it rather than inventing a second one. |
| `macosify` | Fixing native-idiom problems. Proctor finds them; that skill refits them. |

A web view inside a Mac app is still Proctor's, because reaching it means
attaching to the host process. A pure web app in a browser is not.

## Orchestrating and implementing test instruments: Proctor, Deep Links, and XCTest / XCUITest

Proctor knows when to use, combine, and author across three testing instruments:

### 1. Proctor Native Engine (Black-Box Live Mac Testing)
- **When to use**: Testing running macOS applications (SwiftUI, AppKit, Catalyst, Electron, Chromium, menu bar extras, preference panes) without compiling test hosts or modifying source.
- **Capabilities**:
  - Live accessibility tree inspection, background process-directed actions (no cursor theft).
  - Spatial geometry assertions (`horizontalAlignment`, `alignedWith`, `containedIn`, `frameEquals`).
  - ScreenCaptureKit frames with cryptographic trust (`trustworthy: true`, `SCFrameStatus`).
  - Native 2x crop inspection (`proctor_zoom`), automated design diffs (`/be-my-witness`), and multi-run determinism scoring (`proctor_stability`).

### 2. Deep Links (Fast Navigation & State Setup)
- **When to use**: Navigating directly into specific views, deep screens, or authenticated states without executing dozens of manual navigation clicks.
- **Capabilities**:
  - On macOS: invoke custom URL schemes via macOS `open <url>` or Apple Events, settling with `proctor_wait` or `proctor_find`.
  - On iOS Simulator: invoke `proctor_ios` with `action: "open"`, `url: "<scheme>://..."`. Proctor checks target resolution, verifies SpringBoard delivery, and measures pixel delta to confirm navigation arrived.

### 3. XCTest & XCUITest (In-Process, Exception & In-Simulator Testing)
- **When to use**:
  - Testing internal Swift / Objective-C logic, unit models, and service contracts with direct symbol access.
  - Testing low-level Mach exceptions, crashes, or assertions (such as `EXC_BAD_ACCESS`, `fatalError` trapping, or `XCTAssertThrowsError`).
  - Running Xcode schemes headlessly via `xcodebuild test` or `swift test`.
  - Driving in-device iOS accessibility elements (`XCUIElementQuery`), where external macOS accessibility APIs cannot reach.
- **When authoring tests**:
  - Author Swift Testing (`@Test`, `@Suite`, `#expect`) or XCTest (`XCTestCase`, `XCTAssertThrowsError`) targets when writing unit or regression test suites in the codebase.
  - Author Proctor flows (`proctor_flow`, `proctor_act`) for black-box end-to-end user journeys and visual verification.

## Before anything else

Run `proctor_doctor`. It costs one call and it is the difference between a
campaign and an hour of retries. It answers five questions, and each of them can
end a campaign before it starts.

**Is the server even here.** When no `proctor_*` tool is available at all, the
MCP server is not configured in this host. Point the user at `~/Dev/proctor-mcp`
— `scripts/install.sh` builds and loads it and prints the `claude mcp add` line
— and stop, since there is nothing to drive until it is there. The line it
prints ends in `--profile core`, which advertises the ten tools that drive a Mac
at roughly 6.8k tokens rather than all twenty. The catalogue is re-sent every
turn and survives compaction, so that difference is a standing cost paid before
any work happens. Widen to `--profile scripting` for flows and determinism runs,
or `--profile full` for the iOS lane, policy, `kill`, `inspect` and the CUA
schema façades.

**Which grants are in place, in three states.** Each `grants[]` row carries
`state` — `granted`, `denied` or `unconfirmed` — alongside the fail-closed
`granted` boolean. `unconfirmed` is a fact about what Proctor established, not
about the permission: the grant may be perfectly in place and the bounded probe
simply did not get an answer. Read `state` before sending anyone to System
Settings, because sending a person to fix a permission they already granted is
its own defect. A missing Accessibility grant presents as elements not being
found, which reads exactly like a selector bug and which a model will paper over
by trying again. Screen Recording cannot be granted silently on any macOS
version. `howToFix` names the exact fix for the running OS version.

**Which toolchain is present.** Proctor depends on software it does not ship,
and `tools[]` reports each one's presence, version and usability with the
evidence behind the answer — where it was found and everywhere it was looked
for. A `usability` of `unconfirmed` is a fact about what Proctor has
established, not a fault, and calling `doctor` again will not change it, because
**this call runs none of those tools.** A launchd agent does not inherit a login
shell's `PATH`, so Proctor's answer and your own shell's answer can legitimately
differ; the recorded paths are how you settle it.

**Which lanes this machine actually has.** `lanes[]` derives four rows from the
grants and the tool rows, so a lane cannot claim readiness while the thing it
needs is missing. Each carries `state` (`ready` / `unavailable` /
`unconfirmed`), a fail-closed `ready` boolean, `requires`, `blockers` and a
standing `note`.

| Lane | Needs | Missing it means |
|---|---|---|
| `mac` | the Accessibility and Screen Recording grants; no external tool | No campaign at all. This is the lane everything else in this skill describes. |
| `browser` | `obscura` | Pages inside a browser window cannot be driven. Native apps are unaffected — Proctor drives those without any browser tool. |
| `ios` | `simctl`, which means Xcode | No iOS lane on this machine. `maestro` is listed too and is deliberately not a blocker: deep links and device screenshots work without it, only flow files need it. |
| `cua` | `cua-driver` | The delegated actuation lane is unavailable. Proctor's own planes still perform every step, so this only matters when `PROCTOR_ACTUATION=cua` selected that lane. |

`ready` on a lane row and `available` on a tool row are deliberately different
words: a tool is `available` when a file of that name is there, and a lane is
`ready` when it is confirmed usable.

**What the gate will do to your next call.** The `policy` block reports the
gate's posture — its `mode` (`allowList`, `blockOnly` or `open`), the sizes of
its lists, whether an approval token is live, and whether the audit trail is
writable and verifying clean. It reports shape rather than rules, so if you need
the rules themselves, `proctor_policy` action `status` answers in full.

`secureEventInputActive: true` is not a blocker but it narrows the plan:
process-directed steps all still run, synthetic-event steps become unreliable.

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

When the attach comes back with an empty `windows` array, the app is running
with every window closed rather than being unreachable. `action: "activate"`
reopens one the way a Dock click does, waits for it, attaches, and hands back
the handles — and it is the only way in, because every actuating tool resolves a
window handle first, so the menu item that would reopen a window cannot be
reached without the window it creates.

**When a browser renders the window, the attach carries a `browser` handoff**,
and it is worth reading rather than skipping. `boundary` says which half of the
window is whose, `use` names a lane where one can help, and `why` gives the rule
that chose it, so the advice is checkable rather than oracular. Two fields
decide what you can conclude:

- **`surface`** distinguishes a `browserWindow` — tabs, an address field, many
  origins over its lifetime — from an `installedWebApp`, one site opened as an
  application with its own dock entry and session. `use == null` alone does not
  tell you which situation you are in: it means "no lane", and `surface` says
  whether that is because nothing should drive the page or because Proctor
  drives this one itself.
- **`flags`** is the machine-readable half of the prose, and it is what the
  named instrument commits you to: `actsOutsideThisWindow`, `autonomous`,
  `canActAsThisPerson`, `outsideTheAuditTrail`, `billed`. Read them before
  handing anything off, because `outsideTheAuditTrail` in particular changes
  what the campaign can later claim was recorded.

Attaching to a browser is not a reason to leave Proctor. It is a reason to know
which half of the window is whose.

## Authenticated browsers, 1Password, and Sift mail OTPs

When driving web applications or authentication flows inside a browser, Proctor coordinates across three capabilities:

### 1. Driving authenticated Chrome sessions

Proctor can drive existing, logged-in Google Chrome or Safari windows directly on its accessibility plane.

Chrome only exposes its internal web accessibility tree when accessibility is active. If `proctor_apps` attach returns an `AXWebArea` with zero children or `manualAccessibilityApplied: false`, launch Chrome with `--force-renderer-accessibility` (or restart with that flag) so that all inputs, buttons, and links populate the accessibility tree.

When a page needs autonomous navigation Proctor's own planes cannot express, `browser-use` is the second lane, and it reaches the real signed-in browser rather than a clean-slate engine. It is **off unless `PROCTOR_SECOND_LANE` names it**: `proctor_doctor` reports `secondLane` as `off`, `enabled` or `unavailable`, and `off` is this machine's standing default. Check that field before recommending it, because a lane that is named but not enabled is advice nobody can take. Obscura, the default lane, runs its own engine with its own cookie jar, so it cannot see a session or a password manager at all.

### 2. Selecting 1Password credentials and autofill

Authentication pages frequently integrate with the 1Password extension. 1Password renders autofill suggestions as native accessibility elements:

- In Google Chrome, 1Password autofill items appear in the accessibility tree as `AXButton` nodes (for example, "Apple username@example.com" or "Sign in with 1Password").
- Actuating these with an accessibility `press` step (`kind: "press"`) triggers the autofill in the background (`ranInForeground: false`). This bypasses Secure Event Input restrictions because accessibility actions do not inject synthetic hardware events.
- In Safari or custom web views, suggestions may appear as `AXMenuItem` or popups. Selecting them autofills usernames, passwords, passkeys, and triggers TOTP token insertion.
- When an overlay ignores accessibility presses, switch to synthetic coordinate clicks (`kind: "click"`, `point: [x, y]`, `foreground: true`), ensuring Secure Event Input is inactive.

### 3. Resolving OTP codes and magic links from mail

Login and verification flows often send a one-time passcode or a magic link by email. **Proctor ships no mail tool and reads no mail itself**, so this depends entirely on what else is connected to the same host.

When a mail MCP server is connected, read the code or the link from it, then feed the code back into the form with `setValue` or drive the link as a navigation. Sift is the server named for this on Luke's machines.

Two honest limits, because getting either wrong wastes a campaign:

- **Discover the tool names from the connected server's own catalogue.** They are not Proctor's, they are not reported by `proctor_doctor`, and they are not stable enough to hard-code into a plan.
- **Check it is actually connected before planning around it.** A mail server that is configured somewhere and not connected here looks identical to one that is, until the call fails.

When no mail tool is connected, the OTP step belongs to the person. Say so in the report rather than describing the flow as automated end to end.

## What the person watching sees

Proctor draws a pointer on screen while it drives an app: it travels to each
step's target before the step fires, leans into the direction of travel, and
pulses where it acts. This exists because the property that makes Proctor
useful also makes it illegible — an accessibility press actuates a button with
nothing moving on screen, so somebody watching sees menus open and text appear
with no cause.

Three things follow that matter to a campaign:

- **It never appears in a capture.** Every capture is window-scoped to the app
  under test, and the overlay belongs to the agent's own process, so it cannot
  move a state hash or change a pixel assertion. You therefore cannot verify the
  overlay through `proctor_capture`, and you do not need to account for it in
  fidelity work.
- **`PROCTOR_CURSOR=0` turns it off.** Set it for an unattended suite, or on a
  machine somebody else is working on.
- **One panel per display.** Worth knowing if you ever extend it: a single panel
  spanning the union of several displays is a large enough backing store that the
  window server accepts it, reports it `onscreen` with `alpha 1`, and never
  presents it. A panel that reports healthy and draws nothing is the failure mode
  to expect from any overlay work here.

The pointer keeps drawing when actuation is delegated, under a rule that
guarantees exactly one cursor on screen: Proctor's pointer is preferred, and the
driver's own agent cursor is requested off on every delegated call. When the
installed driver offers no such control, Proctor's pointer stands down instead,
so a person never sees two. `PROCTOR_CURSOR=0` keeps exactly its old meaning —
Proctor draws no pointer anywhere.

One honest limit rides along: Proctor's pointer draws **intent**, the target a
step is about to act on, rather than tracking a system cursor. On a delegated
run that separation widens, because the process moving anything is not the
process drawing.

A delegated backend can also escalate to the foreground on its own, and a post
the agent did not make cannot be announced in advance. That escalation surfaces
after the fact, as `unrequestedForeground` on the step, rather than as a warning
before it.

Two more supervision surfaces exist, and a campaign benefits from knowing they
are there even though no tool call reaches them. The **status window** separates
the grants from the toolchain, so a person can see which lanes their machine
has. A **run history**, reachable from the menu bar and the status window,
records what Proctor did — the runs, their steps, what each targeted, which
plane it travelled, and what came back — under bounded retention set by
`PROCTOR_HISTORY_DAYS` and `PROCTOR_HISTORY_ENTRIES`. When a report needs to
point somebody at what happened on their own machine, that is where to send
them.

Every `PROCTOR_*` switch has a home in the status window rather than only in the
environment, and the precedence between the two is deliberately not one rule.
For an ordinary switch the environment wins and the control locks, so a
deliberate `PROCTOR_ACTUATION=cua` cannot be silently overridden by a preference
saved months ago. For a capability switch — the ones that create an event tap —
off wins from either source and the control never locks, so a person whose
keyboard is being swallowed always has a switch they can press.

## The campaign

Seven stages. Run them in order — each one's output narrows the next — and
stop early with what you have if the app turns out to be unreachable.

The stages are the method, and they are unaffected by which lane performs the
clicking. What does change by lane is how much of each stage is reachable: on an
iOS target, stages 1, 3 and 4 have no accessibility tree to work with at all, so
read *The iOS lane* below before planning that half of a campaign.

**Two ways in.** When someone hands you a specific test case or a written
suite, each case is a row: you trace it to the flow and assertion that verify
it and report it passed, failed or skipped, and coverage is measured against
that suite. When the ask is open — "is this ready", "find the bugs", "does the
onboarding still work" — you build the spine yourself from the app's acceptance
criteria and the sweeps below. Either way the report is organised around a
matrix of cases to evidence, and a case with no evidence is a visible gap
rather than a silent one.

### 1. Exploratory sweep

`proctor_snapshot` the main window, then walk outward: `proctor_menu` for the
whole menu bar in one read, each window the app offers, each tab or sidebar
section. Use `proctor_find` rather than pulling whole trees once you know what
you are looking for.

`proctor_menu` is worth reaching for early. It returns every item's path,
enabled state and keyboard shortcut in a single accessibility read, reaching a
background or other-Space app, and each item comes back both as a `menuPath` you
can actuate on the accessibility plane and as the `key` plus `modifiers` pair a
synthetic shortcut needs. That gives you the app's whole command surface before
you have clicked anything. A submenu macOS has not built yet is reported with
`submenuPopulated: false` rather than invented; open it and re-read to see
inside.

You are building an inventory, not testing yet: which controls exist, which
carry `AXIdentifier` (those are the durable selectors — a developer set them
deliberately, so they survive copy changes and localisation), which are
unlabelled, and where the tree goes suspiciously flat or empty. A flat subtree
under a rich-looking view is usually a custom control that never adopted
accessibility, and that is both a finding and a limit on what you can test.

### 2. Acceptance criteria into flows

Build the case-to-evidence matrix first: every acceptance criterion, or every
case in a suite you were handed, as a row mapped to the flow and the assertion
that will verify it, each marked covered, partial or gap. Writing it before you
touch the app is what forces complete coverage and exposes the deferred and the
backend-only criteria honestly, rather than letting what is easy to click drive
what gets tested. It is the report's spine.

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

### 4. Accessibility & Geometry Assertions

`proctor_assert` validates the live accessibility tree and spatial geometry across seventeen distinct assertion kinds:
- **Structural Accessibility**: `exists`, `absent`, `valueEquals`, `valueContains`, `enabled`, `disabled`, `focused`, `hasLabel`, `minHitSize`, `contrast`, `focusOrder`.
- **Spatial Geometry & Alignment**:
  - `kind: "horizontalAlignment"`: verifies whether a row or control is aligned `leading` / `left` (or `center` / `trailing`) relative to its container or window. **Essential for catching AppKit `Menu` / `NSPopUpButton` centering defects** where SwiftUI centered button text instead of a full-width leading row.
  - `kind: "alignedWith"`: verifies alignment along specific edges (`left`, `right`, `top`, `bottom`, `centerX`, `centerY`) against another node or reference rect within a `tolerance`.
  - `kind: "containedIn"`: validates strict spatial containment inside a parent frame.
  - `kind: "frameEquals"`: asserts exact `[x, y, w, h]` bounding boxes within an epsilon tolerance.

Then run the tri-observer check — `kind: "agree"`. Where the accessibility
tree, the geometry source and the pixels disagree about the same instant, the
delta is a defect with a name: an unexposed control, a ghost node, an
invisible-but-focusable element, a stale frame, a wrong hit target. This is
the pass that finds what neither a screenshot review nor a tree dump finds
alone, because it is looking for the disagreement rather than at either
source.

### 5. Visual Fidelity, Automated Diff-Masking & Native Conformance

**Attach visual proof to live AppKit and SwiftUI windows and menu extras,
through Proctor.** A headless SPM `ImageRenderer` has no active window server,
so it emits placeholder glyphs for native controls such as `Menu` and
`NSPopUpButton` without saying that it did — which makes its output look like
evidence and behave like a guess.

`proctor_capture` each state. Every capture reports its own trustworthiness —
frame status, content rect, dirty area, frames waited. When `trustworthy` is
false, the caveat says why, and an off-screen window that only produces
complete frames when the pointer moves on its display is a real
ScreenCaptureKit behaviour rather than a bug in the run. Never treat an
untrustworthy frame as evidence; capture again with the window raised and say
that you did.

**Automated Diff-Masking with `/be-my-witness`**:
When verifying an implementation against reference design mocks:
1. Capture the live window or menu extra at native 2x resolution.
2. Use `proctor_zoom` or bounding-box crops to extract component slices (e.g. Menu Header, Meter Bar, Command Rows).
3. Hand off the capture and reference mock slices to `/be-my-witness`.
4. `/be-my-witness` runs deterministic pre-scan, computes YIQ delta masks, and applies the **Dual-Oracle Discipline** (design mock is the visual oracle for layout, typography, and control hierarchy; test expectation is the behavioral oracle). Any text alignment shifts or missing trailing tokens are flagged as High-Severity Visual Regressions.

**Native Conformance Rubric (`mac-design-studio`)**:
*Is it a correct, native Mac UI* stands on its own and takes the platform as the
reference: `mac-design-studio`'s `native-foundation.md` is the rubric — the
macOS 27 control ladder, the 11-role type ramp, the label tiers, the 8pt grid,
concentric radii and Liquid Glass discipline — and its ten-point native-tells
audit is the checklist. Measure the rendered tree and the captures against it:
a control off the size ladder, body text off the 13pt ramp, a floating panel
with no scroll-edge material, tracked-uppercase labels where the platform uses
sentence case — each is a conformance defect a mockup-free app still carries,
and each is a "ui/ux design test" that neither the accessibility pass nor the
fidelity ledger names.

For an app that embeds `ProctorReflector`, `proctor_inspect` returns resolved
colours, fonts, corner radii, constraints and both layer model and
presentation values. That is measurement.

**Read small things with `proctor_zoom`, not with a bigger screenshot.**
`proctor_capture` normalises to the vision ceiling by default, and the pixels a
label, a numeric field or a glyph is written in do not survive that downscale —
so a whole-window capture is the wrong instrument for "what does that say".
`zoom` cuts a native-resolution crop of a region or a resolved node, and the
published gain is large: iterative crop-and-zoom lifts GUI grounding accuracy on
high-resolution desktop software from roughly 19% to 48–73%. The compose path is
**find → zoom → assert**, and a region around 1000px on its long edge keeps
enough context to disambiguate what you are looking at.

Route the judged question "does this look any good" to `design-review`, with
your captures attached; route "is this native" to the `mac-design-studio`
rubric above. The two are complementary — one judges craft, the other judges
platform fit — and a Mac app can pass one and fail the other.

### 6. Determinism

`proctor_stability` on every flow you intend to trust, five runs by default.

It returns `firstDivergence` and per-step instability. A flow whose runs
diverge at step 3 does not need its step 9 assertion investigated, and a step
with instability above zero is nondeterministic before anyone argues about
whether it is correct. This is what separates a real defect from a flaky test,
and running it before reporting failures saves reporting noise as findings.

**The report now says what the number was a score of, and the disclosure is as
load-bearing as the number.** Read three fields before quoting `deterministic`:

- **`backend`** — which actuation lane every pass was measured on. A determinism
  verdict without its actuation path is exactly the mismeasurement this
  instrument exists to prevent, stated as a conclusion. One value covers the
  whole report, because a session's lane is fixed.
- **`pageContent`** — present when at least one step, in at least one repeat, was
  measured over a browser's render tree rather than the application's own view
  hierarchy. It names the browser, the steps affected, and what that does to
  their numbers. A page's own render churn is not the application's
  nondeterminism, and a score that folds the two measures neither.
- **`stepBasis`** — one entry per step saying what that step's number was taken
  over and what it was computed from. Present when there is anything to disclose,
  including a repeat that withheld a hash. Where it is present it reads in
  parallel with `stepInstability`, so quote the pair rather than the number
  alone.

For the iOS lane the equivalent question is answered by `proctor_ios` action
`flow` with `runs` above 1, and its answer is coarser for a structural reason
described in the iOS section: repeats are compared against each other, the unit
is the file, and Proctor observed none of the steps.

### 7. Report

Length: proportional to what you found. A clean campaign on a small app is a
page. Cover the substance and stop; a short result padded into a long one buys
nothing and costs the reader the signal. No filler sections, no restated
summary, no closing reflection.

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
- **Methods**, naming the OS version, the agent build from `doctor`'s
  `agentBuild`, which actuation lane the run used and therefore who performed
  the steps, whether `AXManualAccessibility` was applied, which settle signals
  were available, whether a reflector was embedded, which captures came back
  untrustworthy, and — where the campaign touched iOS — that the iOS half had no
  accessibility tree available to it. Write it out in full when it is asked for:
  a methods section handed back as headings for someone else to complete is the
  one section whose whole value is that it was actually filled in.

An assertion that could not be evaluated is not an assertion that passed.
Report it as skipped, with the reason. A delegated step whose outcome came back
`indeterminate` belongs beside it, for the same reason.

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

## Planes and lanes: what a step proves, and who performed it

Two separate facts ride on every step result, and conflating them is how a
campaign comes to overclaim.

### The plane is what the result proves

`plane` names the mechanism a step travelled through, and that decides the
strength of the claim.

**Process-directed** — `accessibility` (accessibility actions and attribute
writes), `appleEvents`, `declared` (an AppleScript sdef or the `shortcuts` CLI,
which is the app's own contract). These are IPC to the target, so they reach
non-frontmost, occluded and other-Space windows without stealing focus, and
Secure Event Input does not block them. This is the default and it is what makes
unattended testing possible.

**Synthetic events** — `syntheticEvent`. `click`, `hover`, `dragPath`, `key`,
and `type` into a field whose value the accessibility plane cannot write. These
enter the single system event stream, so they need the app in the foreground and
they interfere with whoever is using the machine. Secure Event Input makes them
unreliable — the evidence supports "injection unreliable, observation blocked"
rather than a blanket block — while leaving the accessibility and Apple Events
planes working. Reserve them for what the accessibility plane genuinely cannot
express: drag paths, canvas surfaces, hover-only states, text composition, and
testing keyboard shortcuts or focus behaviour as such.

**`routedEvent`** — an injected event delivered to one process rather than to
the shared stream. Background-safe, and not the accessibility plane. Proctor's
own actuator cannot produce this; only a delegated backend can. Treat it as a
background-safe result, and say in the report that the delivery was an injected
event rather than an accessibility action, because a control reachable only that
way is still a control an assistive technology cannot operate.

**`unknown`** — the step was performed and this build does not recognise the
delivery mode the backend reported. The backend's own word survives verbatim in
`reportedMode`. A run holding one of these is never described as
background-safe, and `ForegroundReport.note` is non-nil to say so.

**The honesty rule.** When a step comes back with `plane: "syntheticEvent"`,
the result proves something narrower than a process-directed one did — it proves
the app works when it is in front. Say so if it matters.

Two different things can put a step on that plane, and they carry different
findings. A `dragPath`, `hover`, `click` or `key` was always going to travel
there and the narrower claim is simply what that step buys. A `type` or a
`scroll` that lands there tried every accessibility route first and conceded,
which is itself a finding: a control reachable only by synthetic input is a
control an assistive technology cannot operate either. What never happens is a
silent fallback on an outright refusal — a step whose accessibility route the
element refuses fails, and the error names both ways forward: re-run with
`foreground: true`, or reach the same end through an attribute write that stays
on the accessibility plane. Taking the second route keeps the result
background-safe.

Beside the plane, `route` names how a step got there — `valueWrite`,
`selectedText`, `scrollBar`, `scrollAction`, `action`, `eventStream`,
`appleEvent`, `declared`. That is what makes "an attribute write was found
rather than the foreground being taken" visible rather than inferred.

### The lane is who actuated

Proctor is no longer necessarily the thing posting the events. Actuation sits
behind a seam with two backends, and every step result carries `backend`:

- **`native`** — Proctor's own planes. This is the default, and it is a
  deliberate choice rather than a leftover: the native lane is maintained,
  tested, and the only one with an Apple Events plane at all.
- **`cua`** — delegated to `cua-driver`, selected with `PROCTOR_ACTUATION=cua`.
  Never automatic, and never a fallback. A run that silently changed lane
  mid-flight would make a determinism score meaningless, so a lane is chosen
  once for a session and the record says which one it was.

Read `backend` on the step rather than assuming, and carry it into the report.
A comparison whose two halves ran through different lanes is measuring the
lanes, not the application.

**The delegated lane cannot drive every window the native lane can, and the
gap is one this skill's opening promise depends on.** A driver reports an
off-Space SwiftUI window as a menu bar and nothing else, where Proctor's own
retained references keep resolving there. So a step against a window on another
Space is refused on the Cua lane with that reason named, and works on the native
one. That is a capability regression rather than a corner case: if a campaign's
value rests on reaching windows the user is not looking at, the native lane is
the one that does it.

**Addressing crosses the seam by identity, never by position.** A target is
matched into the backend's view through its `(role, label)` ancestry, and both
sides must agree about the element before anything is struck. Four refusals
follow, and each says something different:

| Refusal | What it means |
|---|---|
| `targetUnresolved` | No match, carrying what Proctor's own tree says is there. |
| `targetMoved` | A re-match found a different identity at that place. |
| `targetAmbiguous` | The driver's snapshot was truncated, so uniqueness could not be established at all. "I could not finish looking" is never reported as "it is not there". |
| off-Space, named | The regression above. |

Proctor never substitutes a coordinate for an element resolution that failed,
because a match resting on a position replays by striking an absolute point.
What the driver does internally is the driver's — some of its gestures pixel-click
an element's centre — and that is reported rather than forbidden.

**Observation never delegates.** Whichever lane actuates, the capture, the
frame-status metadata, the accessibility walk and every verdict are Proctor's.
The backend is told what to strike and asked what it did, and is never the
authority on what is there or on what changed.

**A delegated step carries facts a native one has no equivalent of**, and they
are absent rather than false on a native run:

| Field | What to do with it |
|---|---|
| `reportedMode` | The backend's own word for how it delivered the step, verbatim. Audit the plane mapping against it rather than trusting the mapping. |
| `effect` | `confirmed`, `unverifiable` or `suspectedNoOp` — what the backend claims about the action landing. Nil natively, because the native backend judges a write by reading it back rather than by reporting a confidence. Treat `suspectedNoOp` as a step that probably did nothing, and `unverifiable` as unproven. |
| `unrequestedForeground` | The backend escalated to the foreground for a step that asked to stay in the background. The machine was taken without warning. A run containing one of these cannot be repeated unattended, and it belongs in the methods note. |
| `retriedOnStale` | The element handle went stale and was re-resolved before the step ran. That is a determinism signal about a moving target, not an implementation detail. |
| `transportMs` | Round trip to the backend, separate from the step's elapsed time, which already includes settle. |

**The gate and the trail hold across the seam.** Every delegated call goes
through the same policy gate and is recorded, and the trail separates who acted,
what the driver claimed, and what Proctor observed. A step whose subprocess died
or answered too late records the outcome `indeterminate` rather than `ok` or
`refused`, because nothing can say whether the machine was touched. Read
`indeterminate` as unproven in both directions: do not report it as a defect and
do not count it as a pass.

**Supervision survives delegation, with two gaps worth knowing before you run
unattended.** A delegated run is still one somebody can see, pause and stop: the
HUD panel names the lane on the row it already has, the menu bar reports it, and
a delegated batch reads as one that *may* need the front, because every kind on
that lane is conditional. What does not carry over intact:

- **The takeover statement goes up late on an unrequested escalation.** Proctor's
  foreground guards arm before a post, from inside the process making it. A
  delegated post is made by another process, so when a step takes the front
  without being asked, the statement appears *after* the machine was taken rather
  than before. The run is supervised from the step after that one. Nothing
  available from outside another process closes the gap, so it is stated on the
  panel and in the run's note rather than engineered away.
- **When Proctor cannot identify the driver, click-to-Stop is not armed.** That
  batch takes the exclusive lane instead, so it serialises against every run
  needing the front, and it arms no input block — which means the Stop rectangle
  is never consulted and a driver event cannot press Stop. The person keeps
  Escape, the menu bar, and the gaps between steps. `doctor` says when this is
  the situation, with the reason. The trade was deliberate: a slower lane that
  holds nothing beats a hold that either eats the driver's own events or drops a
  concurrent run's.

**One caution to carry into any report.** Nothing in this lane has been
exercised against a live `cua-driver`; the seam, the vocabulary and the records
are built and tested, and the driver itself is not installed on the machine this
was developed on. The Maestro lane below *was* verified against a real
simulator. If you run with `PROCTOR_ACTUATION=cua`, treat the first delegated
step as a probe rather than as a proven path.

## The iOS lane

`proctor_ios` drives an app on a booted iOS Simulator. It is advertised only by
`--profile full`, and it needs Xcode, which is where `simctl` lives. Read the
`ios` lane row from `doctor` before planning anything with it.

### The ceiling, which is the first thing to understand

**An iOS target is not a window, and the Mac's accessibility API does not cross
into a simulated device.** A device handle looks like `dev-29fea02e`, and
`proctor_snapshot`, `proctor_find`, `proctor_assert`, `proctor_act` and
`proctor_capture` refuse one by name. So for an iOS app there is no tree, no
elements, no identifiers, no geometry assertions, no tri-observer check, no
`agree`, and no step-by-step actuation.

A campaign that assumes parity with the macOS lane will spend itself building a
matrix it cannot run. Plan the iOS half around what the three available channels
can actually establish, and say in the report that the rest was out of reach for
a structural reason rather than an unfinished one.

### The three channels, reported separately

Whether the app's process is running, what the device screen looks like, and
what `simctl` said. The tool reports each rather than blending them into a
single claim, because each supports a different strength of conclusion.

### Deep links: `open`

**A zero exit means the URL was delivered, not that the app went anywhere.** The
same open run twice exits zero both times and only the first one changes
anything. So `open` returns an evidence block and one of four verdicts:

| Verdict | What it supports |
|---|---|
| `targetChanged` | Delivered, the resolved app is running, and the screen changed. The strongest claim available here. |
| `screenChanged` | The screen moved, but the change cannot be attributed to the app the URL named — where a universal link Safari swallowed, or a system sheet, lands. |
| `deliveredOnly` | Nothing observable changed. Inconclusive rather than failed: a deep link to the screen the app is already on looks exactly like one the app ignored. |
| `refused` | The gate or the device declined it. |

**None of them claims the app reached a particular screen.** The frontmost app
on the device is not observable through this lane, so "it navigated to
Settings" is not a sentence this evidence can support. Write the verdict, not
the inference.

`pixelEvidence` defaults to true and is the only channel separating a deep link
that moved the app from one that did nothing. `changeThreshold` defaults to
0.0005, calibrated against an idle floor measured at exactly 0 and a smallest
real navigation at 0.002.

`open` never boots anything and refuses a device that is not booted, because
folding a stateful minute-long side effect into a call whose result is "did this
navigate" would make both meaningless. `boot` is the explicit, gated, audited
way in. Nothing here ever shuts a device down or reboots one; a device this
session booted is marked in `list` so a person can decide about it.

### Screenshots on a device carry no frame status

A device screenshot comes back marked untrustworthy, with that as the reason.
The pixels are real; the guarantee a window capture carries is not, because
there is no ScreenCaptureKit frame status behind it. Use it as illustration and
as the change signal `open` compares, and do not cite it the way you would cite
a `trustworthy: true` window capture.

### Flows: `action: "flow"`, which runs Maestro

Maestro is a separate binary that executes a whole file and reports at the end,
so **the unit here is the file, not the step**, and what a pass proves is
coarser than a Mac replay.

`flowPassed` means the driver executed the sequence and reported success. It
does not mean Proctor observed the app reach any state — Proctor did not run
these commands and has no independent observation of any of them. The only
observer of the steps is Maestro. Individual Maestro commands are never routed
through `proctor_act`, because a tool driving its own engine is not driving what
Proctor is attached to. Use the driver's own words in the report rather than
borrowing the stronger ones.

With `runs` above 1 the repeats are scored **against each other**, never against
a recording, because there is none. Four things to read correctly:

- `firstDivergence` is where two repeats stopped agreeing, indexed by Maestro's
  own sequence numbering.
- Maestro prepends two commands that appear in no flow file. They are marked
  `injected`, so do not map an index onto a line of your YAML without checking.
- Durations sit beside the score and are never folded into it. One unchanged
  command measured 634, 91, 88, 96 and 91 ms across five repeats, so timing here
  is not a determinism signal.
- A repeat that failed in the driver rather than the app — no per-command
  record, a failed launch, a device that went away — is excluded from the score
  and makes the sweep `truncated`. Driver flake is never published as the app's
  nondeterminism, so read `truncated` and report the surviving sample size.

Budget roughly 70 to 90 seconds for a five-run sweep, most of it driver
start-up.

### Gating and the trail

Driving an app through `open` goes through the policy gate on the app the URL
actually resolves to on the device, never on a `bundleId` the caller supplied —
that name is a consistency check, and a disagreement is reported. iOS targets
are named `ios:<bundleId>`, so a Mac app on the allow list does not silently
authorise the iOS app of the same identifier, and a block on either spelling
blocks both.

A flow's gate judges the apps the flow **declares**, which is weaker than the
device-resolved judgement `open` makes, and the result says `declared` for that
reason. Any construct Proctor cannot resolve — a script, an interpolated app id,
an unreadable include — is refused whenever an application policy is in force.
An `openLink` inside a flow is gated on what the device resolves it to.

The trail records a URL's scheme and host in the clear and reduces its path and
query to a length and a hash, because a deep link routinely carries a token. For
a flow it records the file's path and a hash of its contents, so the entry
attests to the bytes that ran.

## Scale

One session drives many windows concurrently, because process-directed
actuation does not contend for focus. That is where parallelism lives.

Apple silicon caps concurrent macOS guests at two, so a VM fleet is not the
answer, and more real parallelism past that is a hardware purchase rather than
a configuration change. Do not design a campaign that assumes otherwise.

**Several sessions on one Mac is a different question, and the server does not
yet arbitrate it.** The agent is one process behind one socket and any number of
MCP clients can connect. Nothing schedules between them today, so two campaigns
running at once interleave their steps, and the second one's synthetic click
lands in whatever window the first just raised. Reads are safe — `snapshot`,
`find`, `capture`, `menu`, `zoom` and `assert` observe without mutating.
Actuation is not. Until a scheduler exists, treat "is anything else driving this
Mac right now" as a precondition you check rather than an invariant you assume,
and keep synthetic-event work out of any campaign that might overlap another,
since those contend globally rather than per app.

## Delegating

Most campaigns run in one session. Spawn subagents only for genuinely
independent work — a separate app, or a matrix cell that needs its own window —
and cap the fan-out at four. The session state that makes this server work
lives in the agent, not in you, so parallel subagents share it and stepping on
each other's windows is the common failure. Where one subagent can cover a
track, use one rather than several.

Work you can finish in a handful of tool calls belongs in this session. A
subagent is for a wide independent investigation, not for re-checking a result
you already have.

Subagents never run git operations.

## Traps that cost real time

Each of these has cost an hour somewhere. They are cheap to avoid once named.

**An accessibility press on an Electron row selects it without navigating.**
Slack, VS Code, Discord and Chromium-shelled apps build their sidebars as
`AXOutlineRow` elements that accept `AXPress`, report `ok: true`, set
`focused` and `selected` — and do not change the view. Pressing again changes
nothing, because the press landed correctly and the app simply does not act on
it. Reach for a synthetic `click` with `foreground: true` on the same node; the
result comes back `plane: "syntheticEvent"`, which is the honest record that
this one needed the front. Check the window title or a `find` for the expected
new content rather than trusting `ok`.

**Node ids do not survive the agent restarting.** A step returning
`nodeNotFound` after an upgrade, a `launchctl kickstart`, or a crash means the
retained element cache went with the process, not that the element is gone.
Re-run `find` or `snapshot` and carry the new ids. Ids also do not survive
`attach` being called twice. When the agent itself has stopped, the status
window offers a recovery action rather than a re-check button, because a button
that only re-reads a state nobody can change was the wrong control for this.

**A device handle is not a window handle.** `proctor_snapshot`,
`proctor_find`, `proctor_assert`, `proctor_act` and `proctor_capture` refuse a
`dev-` handle by name. That refusal is the design rather than a gap: the Mac's
accessibility API does not reach into the simulator, so there is nothing for
them to read. Reaching for `proctor_act` on an iOS target is the single most
expensive wrong assumption available in this skill.

**Reach for `find`, not a screenshot, to learn whether an action landed.** A
capture costs an image in context and answers "what does it look like"; the
question after a step is almost always "did the thing I expected appear", which
is a `find` predicate and a fraction of the tokens. Screenshots earn their place
when the question is genuinely visual.

**A settle that concludes on `axQuietOnly` with `captureNeverQuiet` in its
signals is normal for a window that animates continuously** — a caret, a
spinner, a live feed. It is not a warning; pixel-quiet was simply unreachable
and the tree concluded instead. Treat it as adequate evidence and say which
signal you got if a result is surprising.

**Attach reporting `"windows": []` is not an unreachable app.** It usually means
every window is closed. `proctor_apps` with `action: "activate"` reopens one the
way a Dock click would, then attaches.

## Depth

- `references/tools.md` — all twenty tools, their arguments, the `--profile`
  cost, the decision each one exists to serve, and seven results whose obvious
  reading is wrong.
- `references/methodology.md` — the state matrix in full, the accessibility
  rubric, the fidelity ledger, and the disclosure requirements. Written for the
  macOS lane, and its tree-based passes have no iOS equivalent.
- `references/evidence.md` — the research behind every rule above, with
  citations. It predates the actuation seam, so read its two-planes section as
  the account of the native lane specifically.
