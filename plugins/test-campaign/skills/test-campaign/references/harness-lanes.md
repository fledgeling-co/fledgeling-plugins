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

## The desktop-on-glass lanes

A lane named `*-glass` claims the application was running and drawn. `on-glass.md`
carries the doctrine and the three proofs; this is what each platform can actually
support once it is attached.

| | macOS native | Windows native | Linux / X11 | Linux / Wayland |
|---|---|---|---|---|
| **Structure tree** | AXUIElement walk | UI Automation | AT-SPI2 | AT-SPI2 |
| **Resolved style** | **none** | **none** | **none** | **none** |
| **Geometry** | accessibility frames, assertable | `BoundingRectangle` | AT-SPI2 component extents | AT-SPI2 component extents |
| **Capture while occluded** | window-scoped yes; display-scoped no | WGC yes · `PrintWindow` yes · BitBlt no · DXGI whole-screen only | yes | compositor's decision |
| **Capture while minimised** | last frame or blank | **no — black or fails** | no | no |
| **Per-frame validity signal** | `SCFrameStatus`, six values | **none** — DXGI offers only dirty-rects and move-rects | none | none |
| **Actuate without foreground** | AX actions, yes | `InvokePattern` yes; `SendInput` no | XTEST, yes | portal or wlroots protocol |
| **Privilege boundary** | TCC grants; sandboxed drivers excluded outright | UIPI blocks lower → higher integrity | none | portal consent |
| **Runtime theme toggle** | appearance change | registry **plus** a `WM_SETTINGCHANGE` broadcast; classic Win32 may need a relaunch | toolkit-dependent | toolkit-dependent |
| **Menu bar / tray** | `NSStatusItem`, misattributed by enumeration on macOS 26 | nested shell toolbars, exposed only as `Button` | desktop-environment-dependent | desktop-environment-dependent |
| **Headless substitute** | virtual display is private API | Session 0 has no composited desktop at all | Xvfb | none equivalent |

**No desktop platform has a `getComputedStyle`.** Two independent research passes
reached the same conclusion for macOS and for Windows: there is no API by which
one process reads another's resolved colour, font stack or box model. This is not
a gap somebody will close; it is how the platforms are built. So on every lane in
this table the style vector is a triangulation or it is `inconclusive`, and the
report says which.

### macOS

Covered in `on-glass.md` §4 and §6. The two facts that most change a plan: a
background window emits frames **only while the mouse moves on its display**, so
an unattended run on a still machine can wait forever; and a sandboxed driver
cannot use the accessibility API at all, even with the user's grant.

### Windows

- **`SendInput` fails silently under UIPI, by design and by documentation.**
  Microsoft's own reference: *"This function fails when it is blocked by UIPI.
  Note that neither GetLastError nor the return value will indicate the failure
  was caused by UIPI blocking."* Injection is permitted only into applications at
  an equal or lesser integrity level. So a standard-user test driver aimed at an
  elevated app gets no error and no effect — the exact shape this skill exists to
  catch. Use `InvokePattern`, which is semantic and needs no foreground, or run
  the driver elevated, or ship it signed with `uiAccess="true"`.
- **WinUI 3 crashes the walker.** Deep UIA tree enumeration can trigger a native
  `0xc0000005` access violation inside `Microsoft.UI.Xaml.dll`. The workaround in
  the issue is structural: cap enumeration depth, wrap per-node access in
  `try`/`catch` for `COMException` and `SEHException`, and avoid deep `FindAll`
  walkers. A campaign on this lane plans shallow reads or it plans crashes.
- **Qt reports localised strings where a type belongs.** Since Qt 5.11 the UIA
  backend distinguishes controls largely by `LocalizedControlType` rather than by
  semantic control type, so a client cannot reliably identify what a thing *is*,
  and it does not raise some state-change events. Selectors on a Qt app key off
  identifiers, never off type.
- **Black frames have four separate causes**, and none of them errors: a minimised
  window (the compositor keeps only the last bitmap it drew), a window on an
  inactive virtual desktop (Windows Graphics Capture simply stops delivering), a
  window opted out with `WDA_EXCLUDEFROMCAPTURE`, and a hybrid-GPU mismatch where
  desktop duplication fails with `DXGI_ERROR_UNSUPPORTED`. Remote sessions add a
  fifth: a policy that deliberately returns black to prevent exfiltration.
- **BitBlt cannot see a GPU-accelerated UI at all** — WPF, Chromium and game
  engines come back black. If the lane's capture path is BitBlt, half the modern
  frameworks are invisible to it.
- **WPF and WinForms are only as addressable as their authors made them.** With no
  `AutomationProperties.AutomationId` or `AccessibleName`, every selector becomes
  tree-walking, which is the brittleness this skill's selector discipline is for.
- **The tooling has thinned out.** WinAppDriver has had no stable release since
  v1.2.1 in November 2020 and is closed-source, so it cannot be forked; Appium's
  Windows driver inherits that; White is archived; Playwright's desktop support is
  experimental and Electron-only. FlaUI, an MIT-licensed UIA2/UIA3 wrapper, is the
  maintained option. Check this before planning, because a dead driver is a lane
  that will not stand up.

### Linux

- **Wayland deliberately removed the X11 automation model.** On X11, `XTEST` lets
  an unprivileged process inject input and capture the screen globally. On
  Wayland that is gone by design: a harness negotiates an XDG Desktop Portal
  session (`org.freedesktop.portal.RemoteDesktop`) with `libei` for input.
- **The portal asks a human.** That handshake raises an interactive permission
  dialog, which stops an unattended pipeline dead unless a `restore_token` was
  cached beforehand. Provisioning that token is the Wayland lane's real setup
  cost, and doing it in an ephemeral CI environment is an open problem rather than
  a solved one.
- **wlroots compositors have a side door.** Sway, Hyprland and their kin expose
  `wlr-virtual-pointer-unstable-v1` and `wlr-screencopy-unstable-v1`, which skip
  portal consent where the compositor permits the binding. That makes the lane
  cheap on those compositors and says nothing about GNOME or KDE.
- **AT-SPI2 is the tree, and sandboxes hide from it.** It exposes a detailed
  widget tree for GTK and Qt; applications that do not implement the D-Bus
  interface — including some Flatpak configurations and custom renderers — are
  simply invisible. An empty tree here means "not instrumented", not "no
  elements", and the two must not be recorded the same way.
- **Xvfb proves less than it looks like it proves.** An in-memory X display shows
  the view layer renders without crashing. It does not exercise a real
  compositor, hardware acceleration, or the portal permission flow — so a Wayland
  product verified on Xvfb has not been verified on its own display server.

### Continuous integration

- A hosted `windows-latest` runner **does** give an interactive desktop with a
  composited window manager, so UI Automation works there. Its default resolution
  is **1024×768**, which clips modern layouts designed for 1080p — a defect the
  runner introduces and the campaign would otherwise attribute to the build. Set
  it explicitly, or declare the viewport as part of the sample.
- **Windows services run in Session 0, which has no interactive desktop.** A GUI
  test running as a service is testing nothing, and it will not say so.
- **Closing an RDP connection locks the desktop and destroys the GUI context**,
  so any running automation fails at that moment. The documented workaround is to
  redirect the session back to the physical console with
  `tscon %sessionname% /dest:console` rather than disconnecting normally.
- On macOS, an SSH-driven session needs its capture grant pre-seeded, which
  requires disabling SIP — so treat "capture works over SSH" as a machine you
  configured, never as a default.

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
| Windows | a maintained UIA client, and the driver's integrity level decided up front | an interactive desktop, not Session 0; and a driver at or above the target's integrity level, because UIPI failure is silent |
| Linux / X11 | `XTEST` and AT-SPI2 on a real display | the app must actually implement AT-SPI2; a sandbox that does not is invisible rather than empty |
| Linux / Wayland | a portal session with a cached `restore_token`, or a wlroots compositor | the consent dialog — without a pre-provisioned token an unattended run stops at a prompt nobody is there to accept |

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
