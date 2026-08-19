# The native lane — measuring a build that is not a DOM

This skill's two existing lanes both assume a tree it can read from inside the
process under test: a DOM through CDP, or a React Native harness. Four target
shapes have neither, and until this file existed the honest answer for all four
was a screenshot and an apology.

| Target | Why the web lane cannot reach it |
|---|---|
| A native macOS app (SwiftUI, AppKit, Catalyst) built to a mock | no DOM, and no cross-process `getComputedStyle` exists on macOS |
| An Electron or Chromium app shipped as a Mac app | the DOM is reachable only by attaching to the host process |
| A React web build rendered inside a Mac web view | same, and the surrounding chrome is native |
| A web build whose divergence is in a class obscura returns `""` for | the primitive is absent from the engine, not from the build |

That last row is the one worth reading twice. `engine-capability-matrix.md`
records ten classes obscura cannot measure at all — `boxShadow`,
`backgroundImage`, `textTransform`, transitions, animations, `flex`, pseudo-
elements, `getBBox()`. **The same surface running as a Mac app can be measured
for several of them**, because the question changes from "what does CSSOM say" to
"what did the compositor resolve". A shadow obscura reports as `""` is a
`cornerRadius`, a `shadowOpacity` and a `shadowOffset` on a `CALayer`, and those
are readable.

So this is not only a lane for native targets. It is a second engine, and the
skill's own law applies to choosing between them: a class one engine cannot
measure is not a class nobody can.

## The instrument, and why it is not a screenshot

The lane drives the `proctor` skill, which owns native macOS applications. Three
of its observation channels are the reason it is admissible here where a general
screenshot tool is not:

**Frames carry their own trustworthiness.** Apple defines six `SCFrameStatus`
values and makes checking them a precondition of trusting a frame. Every
`proctor_capture` returns `status`, `contentRect`, `dirtyRectCount`, `dirtyArea`,
`framesWaited`, `trustworthy` and a `caveat` naming the cause when trust fails.
A stale frame is pixel-identical to a correct one. This skill already holds that
`ref.png` and `target.png` are supplementary and never the evidence — a stale
frame is worse than that, because it is supplementary evidence of a state that
was never on screen. **Read `trustworthy` before reading the image, and record
`false` as `inconclusive`, never as a spatial fallback.**

**`proctor_inspect` is the closest thing to computed styles that exists on
macOS.** For an app embedding `ProctorReflector` it returns the view and layer
hierarchy with resolved colours, fonts, corner radii, opacity, constraints, and
**both** the `CALayer` model values and the presentation values, against a
monotonic render revision. Without a reflector it returns `reflectorUnavailable`
rather than approximating — the same discipline this skill's probe already
enforces, arriving from the tool rather than from the caller.

**`proctor_assert` already speaks tri-state at the tool boundary.** Its own
contract: *an assertion that could not be evaluated comes back skipped with a
reason, never as a pass, and `ok` is false while anything is skipped*. That is
this skill's exit-code 3 implemented one layer down. `skipped[]` maps to
`inconclusive[]` verbatim, reason string included — relay it, do not paraphrase.

## The capability preflight for this engine

Two tiers, and which one you are in decides what a finding can claim. Establish
it before Phase 2 and record it in `PROJECT.md`, because the answer changes what
the ledger is allowed to say.

**Tier A — reflector present.** `proctor_inspect` returns a hierarchy. Colour,
font, corner radius, opacity and shadow are *measurements*. A divergence names
the resolved value on each side.

**Tier B — `reflectorUnavailable`.** The ceiling is the accessibility tree plus
pixels. Geometry, labels, roles, enabled state and hit size are measurable;
**every style class is `inconclusive` with `reflectorUnavailable` as its reason**.
An eyedropped colour is not a declared value, and reporting one as a finding is
the exact failure this skill's law forbids — a verdict from pixels wearing a
measurement's clothes.

Tier B is not a degraded Tier A that can be talked up. It is a different set of
answerable questions, and the ledger says which set it answered.

Run the preflight the same way the web lane does, with a probe rather than a
capability claim:

```jsonc
proctor_doctor {}                         // grants, attach state, toolchain, lanes
proctor_apps { "action":"attach", "bundleId":"…" }
proctor_inspect { "window":"…", "maxDepth":2 }   // reflector, or reflectorUnavailable
```

`proctor_doctor` also reports usability as `unconfirmed` where nothing has
established a tool works. **`unconfirmed` is a fact about what has been
established, not a fault and not a pass** — treat it as this skill treats a
probe that did not run.

## Which detector class goes to which tool

| Class | Tool | Tier A | Tier B |
|---|---|---|---|
| structure, containment, ordering | `proctor_snapshot` | measured | measured |
| frame geometry, alignment, containment | `proctor_assert` — `frameEquals`, `containedIn`, `alignedWith`, `horizontalAlignment` | measured | measured |
| hit-target size | `proctor_assert` — `minHitSize` | measured | measured |
| label, role, enabled, focus order | `proctor_snapshot`, `proctor_assert` — `hasLabel`, `focusOrder` | measured | measured |
| colour, font, radius, opacity, shadow | `proctor_inspect` | measured | **inconclusive** |
| contrast | `proctor_assert` — `contrast` | measured | measured (pixels) |
| a region against a reference PNG | `proctor_assert` — `regionMatches` | tripwire | tripwire |
| small text, dense detail | `proctor_zoom` | native-res crop | native-res crop |
| a control the tree does not know about | `proctor_assert` — `agree` | measured | measured |

Two rows deserve their reasons stated.

`regionMatches` is a **tripwire, never a verdict**, on the same grounds this skill
already gives for pixel diffs: the research behind that rule notes there is no
published universal tolerance making a 0.5px difference harmless, and that
screenshot-noise thresholds must not be applied to resolved values at all. A
region that matches proves nothing; a region that does not is a question.

`agree` is the only assertion here looking for a *disagreement between observers*
rather than at a value, and it is the native answer to "independently test the
detector itself" — the research's own recommendation, where a working primitive
is replaced by a constant to prove the differ returns inconclusive. It returns
typed `Disagreement` records — `unexposedControl`, `ghostNode`,
`invisibleButFocusable`, `frameMismatch`, `staleFrame`, `hitTargetMismatch`,
`contrastBelowThreshold`, `missingLabel`.

**Measured, and it does not all work.** An earlier draft of this file asserted
that `unexposedControl` catches a control-shaped region with no accessibility
node, on the strength of the tool's documentation and its worked example of "a
96×28 control-shaped region at (880,120) has no AX node". Building a fixture that
plants exactly that — `evals/fixtures/mac-settings` — and running it three times
on 20 Aug 2026 produced six to seven findings per run and **no `unexposedControl`
in any of them**, at 38×22 and again at 96×28 with a label. The divergence is
real and independently confirmed: `proctor_assert` `exists` on that control
returns `found: false` while the capture plainly shows it painted.

So `ghostNode` fired correctly in the same runs — a control the tree has and the
pixels do not — and its mirror image did not. Treat `unexposedControl` as
**unconfirmed on this build**, and reach the same finding the way this skill
already reaches an absence: compare the mock's control inventory against the tree,
where a control present in one and missing from the other is an `absent` row. That
route needs no new instrument, and it is the one the ledger is built on anyway.

Stating a capability from a vendor's documentation before anything exercises it is
the precise habit this skill exists to break, and the first draft of this file did
it. `ANSWER-KEY.md` in the fixture carries the three runs.

## UNSTABLE — the fourth state, and where tolerance comes from

The research this skill is built on names four states, not three: `MEASURED`,
`UNAVAILABLE`, `UNSTABLE`, `ERROR`. `UNSTABLE` is *repeated reads of a fixed
input varying outside calibrated bounds*, and its rule is the same as
`UNAVAILABLE`'s — **do not compare the values**. A 2026 empirical study of 262
web visual-flakiness cases found 59.9% structure-related and 40.1%
style-related, so instability is a classification problem rather than noise to be
tolerated away.

The web lane has no instrument for this. `proctor_stability` is one: replay a
flow N times and it returns `firstDivergence` (the step index where canonical
state hashes first differed) and `stepInstability`, a 0-to-1 score per step.

That makes tolerance derivable instead of assumed. Every `proctor_assert`
geometry kind takes `tolerance` in points and defaults it to 1.0, and the
research is explicit that a numeric tolerance is defensible **only after
repeated-run measurement proves non-zero variance**. So:

- Run `proctor_stability` on the flow that reaches the surface, 5 runs, before
  measuring anything.
- A step whose `stepInstability` is above zero is nondeterministic *before*
  anyone argues about whether its divergence is a defect. Its style and geometry
  classes are `UNSTABLE`, which is `inconclusive`, and the ledger says so.
- Set `tolerance` from the measured variance on the stable steps. A default of
  1.0 carried into a report is an assumption presented as a calibration.

Two cautions the tool states about itself, and they belong in any ledger that
leans on it. A state hash inside a browser's web area walks the *page's* render
tree rather than the app's view hierarchy, so a score taken there measures the
page's churn as much as the app's — `stepBasis` says which side of that boundary
each step fell on, measured while it ran. And a step whose outcome could not be
established contributes no hash at all, because a reading taken after an action
nobody can vouch for is not a sample of that step.

## Reaching the surface, and the two planes

`proctor_act` runs steps against a window. Its default plane is
process-directed — accessibility actions and Apple Events — which reaches
non-frontmost, occluded and other-Space windows without stealing focus. Four
step kinds inject synthetic events instead (`dragPath`, `hover`, `click`, `key`),
need the window foreground, and report `plane: syntheticEvent`.

For this skill that distinction is a fidelity fact rather than a mechanical one.
**A run whose `foreground.measured` count is above zero cannot be repeated
unattended**, so a ledger row closed by such a step carries that, and a batch
lane cannot schedule it beside another. Prefer the process-directed plane, and
reserve the synthetic kinds for what accessibility cannot express — drags, canvas
surfaces, hover states, keyboard-focus behaviour itself.

Read `foreground.measured` rather than re-deriving it from the step list: a
`type` or `scroll` into an element the accessibility plane cannot write falls
back to the event stream, and no count made from the kinds would show it.

## What this lane cannot do

State these as capability facts in the ledger, not as clean rows.

- **Tier B measures no style.** Named above; it is the single largest limit here.
- **No iOS accessibility tree.** `proctor_ios` is a device lane, not a window
  lane — no elements, no geometry, no actuation steps. A device screenshot
  carries no frame status, so it comes back marked untrustworthy by construction.
  For an iOS target the React Native lane remains the answer.
- **A submenu macOS builds lazily** is reported as one item with
  `submenuPopulated: false` and is not descended into. It is `inconclusive`, not
  an absent menu.
- **A cross-platform pixel parity claim has no measured method behind it.** The
  research reached for this explicitly and found the field using SSIM as the
  approach rather than the evidence; treat any native-versus-HTML-mock pixel
  score as a tripwire and say so.
- **The reflector is a debug-build dependency.** A release build measures at Tier
  B whatever the debug build managed, so a ledger closed against a debug build
  says which build it measured.

## The forcing rule, in this lane's terms

Unchanged in substance from `measurement-enforcement.md`, and worth restating in
the tools it lands on. Per screen, before any verdict:

```
.mockup-fidelity/<screen>/
  ref.structure.json         the mock, measured once (web lane)
  target.snapshot.json       proctor_snapshot output — the ordered tree with frames
  target.inspect.json        proctor_inspect output, or the reflectorUnavailable record
  target.assert.json         proctor_assert results INCLUDING skipped[]
  target.stability.json      proctor_stability output — firstDivergence, stepInstability
  target.png                 proctor_capture, WITH its trustworthiness fields
```

A cell citing none of these is a TODO. A cell citing `target.png` alone is a
screenshot verdict, which this skill does not accept in any lane. And
`target.assert.json` is stored whole, `skipped[]` included: dropping the skipped
array on the way into the ledger converts every unaskable question into silence,
which is the one transformation this file exists to prevent.
