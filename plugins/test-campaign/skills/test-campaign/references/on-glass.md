# On glass — proving the thing under test actually ran

A campaign reported **100% checked, 22 armed cases, 59 passing tests** across a
macOS app and a Windows app. No GUI process had ever attached to a window server.

Every number in it was true. The Swift half initialised SwiftUI view structs in
memory; they are value types, so nothing rendered. The Windows half was C# that
had never been compiled. The screenshots on the evidence page came from an HTML
mock photographed in a browser. Nothing in the ledger could catch any of it,
because the ledger only ever asked whether cases *resolved*.

This file is the third failure mode, and the one hardest to see from inside:
**testing the parts on paper and reporting it as the product on glass.**

---

## 1. "On paper" is not a desktop problem

The desktop case is only the most visible. The shape recurs wherever the thing
that ran is not the thing that ships:

| Shape | What the test proved | What it read as |
|---|---|---|
| `XCTAssertNotNil(DashboardView(vm))` | a struct allocated | the dashboard renders |
| a component in jsdom | the tree mounted | the layout is right — jsdom puts layout "outside the scope of jsdom" and returns "zeros for many layout-related properties", so a geometry assertion compares zero against zero and agrees |
| a test renderer with no paint | the render function returned | it is visible |
| source authored, never compiled | nothing at all | the platform is covered |
| the mock photographed instead of the build | the mock renders | the build matches the mock |

The common mechanism is the same one behind vacuous truth: the assertion's
antecedent was never exercised, so the set of differences it *could* have
detected is empty, and an empty difference set is indistinguishable from
agreement. A frame collapsed to `0x0` by conflicting constraints, text clipped by
an aggressive `lineLimit(1)`, a colour with no contrast against the desktop
behind it — none of those has a representation in memory to assert against.

So the question a campaign has to answer before any pixel is read is not "did the
assertion pass" but **"did anything run, and was it this artifact?"**

---

## 2. The three proofs a `-glass` lane owes

A lane whose name ends `-glass` claims the application was running and drawn by a
display server. That is the strongest claim a campaign can make and the one
nothing else can check for it, so it carries the burden:

```bash
python3 $S/campaign.py lane <dir> --lane macos-glass \
    --artifact build/Release/App.app \
    --built-by "xcodebuild -scheme App -configuration Release" \
    --attached "pid 4412 owns window 'App' per CGWindowListCopyWindowInfo" \
    --capture "ScreenCaptureKit window-scoped, SCFrameStatus checked per frame"
```

**`--artifact`** must exist on disk. This is the check that catches code authored
and never built, and it is the cheapest one in the file. When the path is
missing, the next step is the project's documented build for that lane, not a
`--cannot-attach`.

**`--built-by`** is the command that produced it, so a stale binary from three
weeks ago is visible as a stale binary rather than as a pass.

**`--attached`** is what witnessed a process *from that artifact* reaching a
display server: a window id, a pid owning a window, a frame that arrived. Not
"the test suite exited zero" — a headless suite exits zero beautifully.

The order is load-bearing:

1. **Find the documented build** for the lane (`xcodebuild`, `swift build`,
   `msbuild`, `cargo build`, the repo's fastlane / notarize script).
2. **Run it** so `--artifact` exists. A missing `.app` / `.exe` / `.ipa` is a
   build job. Recording `cannot-attach: no signed app is on disk` is how a
   campaign once left glass closed while the source sat unbuilt.
3. **Launch** the result and record `--attached` with a pid, window id, or
   frame that arrived.
4. **`--cannot-attach`** only after that, and only for a structural block that
   the build cannot remove: no interactive desktop on this host, no signing
   identity in the keychain, Session 0, a display server this machine cannot
   reach. `campaign.py lane` refuses a reason that describes a missing binary.

A structural block recorded as blocked is finished work. A missing app
recorded as blocked is the paper-versus-glass failure wearing a reason
string. A blocked lane reported as green is the failure this whole file is
about.

---

## 3. Classify the launch before you read the picture

The ordering is load-bearing, and it is the one rule here with direct
experimental support: when the thing under test did not launch, the geometric
gates **must not run at all**, because they would be vacuous. A harness that
normalised its exit status to `0` made every downstream gate pass vacuously, and
that is the documented root cause rather than a hypothesis about one.

So the sequence per case is: process state, then capture validity, then content.

- **Process state first.** Read the raw wait status, not the shell's conflated
  view: `127` is strong evidence the program never launched, `126` that it was
  found and not executable, `128+N` that it died on a signal. `127` is a
  convention rather than a guarantee, so it is evidence and not a verdict.
- **Stream separation is an illusion under a pty.** "stderr was empty" proves
  nothing when the harness merged the two, which several drivers do.
- **A protocol signal is one-way evidence.** Its presence is a strong positive;
  its absence is not a definitive negative.

---

## 4. Ask the capture channel what it thinks of its own frame

The most useful thing a mature capture API gives is not the image, it is the
image's own status. On macOS, `SCStreamFrameInfo.status` carries `SCFrameStatus`
with six values — `complete`, `idle`, `blank`, `suspended`, `stopped` and one
more — and Apple's own sample code guards on `!= .complete` and returns nil. A
campaign that stores the frame without the status has thrown away the only
channel that says whether the frame means anything.

Cite the status with the capture, and treat anything but a complete frame as
`inconclusive`, never as evidence:

```bash
python3 $S/campaign.py set <dir> --case CASE-0114 --status pass \
    --evidence evidence/shots/dashboard.png --armed \
    --capture-method "ScreenCaptureKit window-scoped" --frame-status complete
```

Four measured ways this channel produces nothing while returning successfully:

- **An idle machine yields no frames for a background window.** Off-screen
  windows emit completed frames *only* when there is mouse movement on the
  display containing the window, and only when the stream is configured to
  capture the pointer. An unattended run on a still machine can wait forever.
- **`idle` has been reported as the permanent status** in at least one binding,
  so a stream that never advances looks like a display that never changed.
- **Occlusion is designed to stop rendering.** Hidden includes occluded, on
  another Space, and screensaver-on; there is no supported way to force the
  compositor to draw an occluded window from outside the app. Window-scoped
  capture does see behind other windows — display-scoped does not, and will
  photograph the screensaver.
- **A locked session is not a quiet session.** Every real application returns
  `cgWindowNotFound`; only the login window is reachable.

---

## 5. There is no entropy gate here, deliberately

The obvious next move is to score the picture — reject a capture whose entropy,
unique-colour count or ink density falls below a floor. This skill does not,
because the measurement does not separate the two cases it would need to:

> no single geometric or textual metric (such as "ink density") is sufficient to
> distinguish a failed capture from a legitimately sparse screen

An empty-state surface is mostly background *by design*, and a shell error
message has much the same ink as the empty state it replaced. A density floor
therefore fails in both directions, and it fails silently — which is the property
this skill exists to remove, not add.

What is decidable from the bytes is decided, in `campaign.py`:

- the file exists, is non-empty, and starts with a raster magic number — a failed
  capture routinely writes an HTML error page to the path the test expected a
  screenshot at
- its dimensions are larger than a placeholder
- it is **not byte-identical to another case's artifact** — one screenshot
  standing in for twelve cases is the cheapest way a wall of captures comes to
  mean nothing, and it is exact to detect

Density is recorded as `bytesPerPixel` and never gates. It is a regression signal
for runs already known to have launched, which is the only role the evidence
supports.

---

## 6. What the pixels still cannot tell you

Getting on glass buys the render. It does not buy introspection, and the gap is
structural rather than a tooling gap somebody will close:

- **There is no `getComputedStyle` for a foreign native window.** No resolved
  colour, font stack, box model, z-index or specificity, on any desktop platform.
  Every richer mechanism requires the target to be your own debuggable build.
  So the style vector on a native lane is a triangulation — token conformance,
  element-scoped raster crops, the platform audit's own contrast findings — and
  the report says triangulation rather than measurement.
- **The accessibility tree is not the view tree.** It supplies role, label,
  value, identifier and frame; Apple documents that what it exposes is not
  necessarily one-to-one with what a sighted user sees. SwiftUI merges a label
  and its toggle into one element, which changes what a selector can address.
- **Reading the tree can change the application.** Chromium and Electron
  materialise their accessibility tree only when a client asks for it, so the
  first walk returns empty and later walks succeed — a pipeline that bails on the
  first miss falls back to OCR and never says so. A target can detect this and
  behave differently, which means an accessibility-driven suite is measuring the
  application in its assistive-technology configuration.
- **No visual-fidelity product covers native desktop apps.** The commercial
  visual-testing tools are web and mobile only. A native differential is
  hand-built or absent, and "absent" is a legitimate answer that must be written
  down rather than filled with a screenshot somebody looked at.

---

## 7. Preconditions that silently yield nothing

Each of these produces an empty or successful-looking run rather than an error,
which is why they are preconditions and not troubleshooting:

| Precondition | What happens when it is missing |
|---|---|
| Accessibility grant | selector misses that read exactly like a selector bug |
| Screen Recording grant | cannot be pre-granted by policy on macOS, user-toggled only |
| An unsandboxed driver | the accessibility API is unavailable to a sandboxed app **even if the user grants permission** |
| A GUI session with a display | the accessibility plane still works and pixels do not — display-scoped capture needs an enumerated display, and the headless substitutes are private API |
| Not fast-user-switched away | every plane fails |
| A settled frame | a caret that blinks can never go pixel-quiet, so a wait for quiet must say what it actually got |

Establish these with the lane's own doctor command before planning a single case.
Where the tool is genuinely absent, that is **a blocker to report, not a licence
to eyeball**: name the tool, say what it would have established, and stop.

---

## 8. Interactive event actuation on glass — testing the flow, not just the frame

Capturing a static window screenshot proves a visual surface was composited on
glass. It does not prove interactive flow execution: that a click on a cancel
button dispatches a daemon RPC, drains a queue item, and renders an animated
toast.

The `interactive-glass` oracle rung tests that on-glass interaction chain:

- **Synthetic UI event dispatch.** Button presses, text-field entry, and
  navigation clicks dispatched to live window views.
- **Runloop pumping.** UI runloops and async message pumps process state
  updates and trigger re-renders.
- **Flow atom verification.** Each declared observable atom in a critical
  flow (`FLOW-*`) is traced from user action to the resulting on-glass
  state change.

A critical flow whose atoms are only verified on headless model structs is a
data-model test. `interactive-glass` on a `-glass` lane is the rung that
asserts the journey under a real window server. It still owes the three
proofs in §2: if the app is not on disk, build it, then attach, then
actuate. `campaign.py` counts the rung as an effect only on a lane whose
name ends `-glass`.

---

## 9. What this changes in the ledger

Three states, kept apart because they are three different claims:

| Status | Means |
|---|---|
| `n/a: <reason>` | the lane structurally cannot support this check, ever |
| `inconclusive: <reason>` | it was attempted and the instrument could not measure |
| `blocked: <reason>` | the thing under test never ran, so nothing below it is valid |

`n/a` is a decision and clears the gate. The other two hold it shut, because "we
do not know" is a weaker claim than "no difference found" and a different one
from "does not apply here". The gate also prints its own population —
`6/8 cases produced a measurement · 2 could not be measured` — since *34 of 42
measured and all 34 equal* is not 100% agreement, and the two read identically
unless the denominator sits beside them.
