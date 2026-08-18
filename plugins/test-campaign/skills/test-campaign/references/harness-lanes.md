# Harness lanes — what each one can actually observe

A campaign plans to its **lane's ceiling**, not to the web lane's. The expensive
mistake is assuming parity: `proctor` states it plainly for its own iOS lane —
*"a campaign that assumes parity with the macOS lane will spend itself building a
matrix it cannot run"* — and the same is true in every direction.

So before planning a single case, read the row for each lane in scope and mark
every check the lane cannot support as `n/a: <the structural reason>` rather than
leaving it open forever.

---

## The capability matrix

| | Web (DOM) | macOS native | iOS Simulator | React Native | SwiftUI (style layer) |
|---|---|---|---|---|---|
| **Structure tree** | DOM, complete | accessibility walk with `TreeProvenance` | **none** | `axe describe-ui` / Maestro hierarchy | accessibility tree only |
| **Resolved style** | `getComputedStyle`, authoritative | only where the app embeds a reflector | none | live component tree over Metro CDP | **none — no runtime style introspection** |
| **Geometry (x/y/w/h)** | `getBoundingClientRect` | yes, and assertable (`frameEquals`, `alignedWith`, `containedIn`) | none | `measureInWindow` | via accessibility frames |
| **Capture trustworthiness** | none offered | **`SCFrameStatus` per frame** — `trustworthy` + a caveat | screenshot only, marked untrustworthy by construction | screenshot only | screenshot only |
| **Step-level driving** | yes | yes, process-directed (background-safe) | **file-level only** (Maestro runs a whole flow) | Maestro / deep link | XCUITest |
| **A11y rule engine** | axe | `performAccessibilityAudit` | none | axe on RNW, or the native audit | `performAccessibilityAudit` |
| **Determinism scoring** | re-run the spec | `proctor_stability`, per-step `firstDivergence` | repeats compared **against each other**, unit = the file | re-run the flow | XCUITest repeats |
| **Reaching a background window** | n/a | yes, and it is the lane's signature property | n/a | n/a | via XCUITest |

Three consequences that decide how a plan is written:

- **iOS has no tree.** No elements, no identifiers, no geometry assertions, no
  tri-observer check. Plan that half of a campaign around three channels — is the
  process running, what does the screen look like, what did the tooling say — and
  say in the report that the rest was out of reach for a structural reason rather
  than an unfinished one.
- **SwiftUI has no computed style.** The style layer is a **triangulation**, never
  a read: token conformance (does the app derive from the same token source as the
  design), element-scoped raster crops, and the audit's own contrast findings. A
  same-frame box with a high pixel delta and no structural finding is the signal.
- **A device screenshot is not a window capture.** On macOS every frame carries its
  own status; on a simulator it does not. Cite them differently, and never treat an
  untrustworthy frame as evidence of anything.

---

## What performs the step, and what the step proves

Two facts ride on every driven step and conflating them is how a campaign
overclaims. `proctor` separates them and the vocabulary is worth borrowing whole:

**The plane is what the result proves.** A process-directed step (an accessibility
action, an Apple Event, the app's own declared contract) reaches a window that is
not frontmost, so it proves the app works while somebody else uses the machine. A
synthetic event needs the foreground, so it proves something narrower: the app
works *when it is in front*. Say which, when it matters.

A step that *conceded* to synthetic input is itself a finding: a control reachable
only that way is a control an assistive technology cannot operate either.

**The lane is who actuated.** When actuation is delegated to another driver, the
step carries facts a native one has no equivalent of — whether the backend claims
the action landed, whether it escalated to the foreground without being asked,
whether the handle went stale and was re-resolved. A comparison whose two halves
ran through different lanes is measuring the lanes, not the application.

**Observation never delegates.** Whichever lane clicks, the capture, the tree walk
and the verdict belong to the instrument. A backend is told what to strike and
asked what it did; it is never the authority on what is there.

---

## Reaching a surface a URL cannot address

Most real defects live behind a drawer, an expanded row, or a confirmation sheet,
and none of those is a route. A campaign that can only address routes records them
all as blocked — which is how one console came to have eleven built screens and a
single capture between them.

The answer is a **closed list of actuation primitives** in the surface map, and the
closure is the point: a map entry that could run arbitrary code would be a second
test suite living in a data file, and nobody would look for it there.

```
{ click: <selector> }        { press: <key> }
{ focus: <selector> }        { fill: [<selector>, <text>] }
{ viewport: [<w>, <h>] }     { settle: <ms> }
```

One key per step, executed in order, after the route loads and before the region is
waited for. A step that cannot be performed fails **that one surface** and is
recorded with its reason, exactly as a missing region is.

On native the same job is done by deep links first — `xcrun simctl openurl` is
roughly thirty times faster than a driven tap, because every Maestro invocation
pays a fresh XCUITest driver startup of fifteen to twenty seconds. Reserve the
driver for the assertion and the few taps a deep link cannot reach, batched into
one flow so the startup tax is paid once.

**A zero exit from a deep link means the URL was delivered, not that the app went
anywhere.** The same open run twice exits zero both times and only the first
changes anything. Ask for pixel evidence and write the verdict, not the inference.

---

## Standing up a lane

| Lane | Stand it up with | The precondition that ends campaigns |
|---|---|---|
| Web | the project's own runner (discover it; never impose one) | a base URL that is a real hostname where the feature needs a secure context |
| macOS | `proctor_doctor` before anything else | the Accessibility and Screen Recording grants; a missing grant reads exactly like a selector bug |
| iOS | a booted simulator and `simctl` | Xcode; and the app must expose a URL scheme or the lane is taps-only |
| React Native | Metro + the in-app render harness | the harness's output directory must sit **outside** the Metro watch root, or the collector triggers an infinite reload |
| SwiftUI | a DEBUG fixture that boots signed-in and seeded | no live auth, no live network, no StoreKit — determinism comes from the fixture |

Where a lane's tool is genuinely absent, that is a **blocker to report, not a
licence to eyeball**. Name the tool, say what it would have established, and stop.
Falling back to a screenshot-and-reasoning ledger is the failure the whole
measurement discipline exists to prevent.

---

## One campaign, several lanes

The registry carries `lane` on every case, so a campaign spanning a web app and its
native siblings reports one coverage number without pretending the lanes are
equivalent. Two rules keep that honest:

1. **A case marked `n/a` for a structural reason names the reason in the status
   string**, so the evidence page renders `n/a: the iOS lane exposes no
   accessibility tree, so geometry cannot be asserted` rather than a bare dash.
2. **The methods section names, per lane, what could not be observed.** A reader
   who does not know the iOS half had no tree will read its thin coverage as
   neglect.
