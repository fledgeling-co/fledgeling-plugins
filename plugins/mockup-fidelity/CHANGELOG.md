# Changelog

All notable changes to the `mockup-fidelity` plugin.

## 3.3.0 — 2026-08-20

Eval 9 shipped in 3.2.0 defined and unrunnable: it asks what a second measurement engine can and
cannot answer about a native target, and every fixture in the suite was an HTML file. `EVALS.md`
said so rather than leaving it to be found. This is the target it was missing, and building it
sent a correction back into 3.2.0's own reference files.

### Added

- **`evals/fixtures/mac-settings`** — a real macOS app, 560×452, no dependencies, whose Settings
  pane diverges from `settings.html` in eight recorded ways. It builds **Tier B** by default, so
  `proctor_inspect` answers `reflectorUnavailable` and the style classes are inconclusive; Tier A
  is opt-in by adding `ProctorReflector` by local path, which the README spells out. A fixture
  that cannot build without a second repository checked out is a fixture that does not run.
- **A four-valued answer key**, measured against the built app rather than derived from source.
  The fourth outcome is **OVER-CLAIM**: reporting the accent-colour divergence while at Tier B is
  a failure, not a catch, because an eyedropped colour is not a declared value. A fixture whose
  only failure mode is missing something cannot test the failure mode of claiming too much.
- **AppKit rather than SwiftUI**, because `ProctorReflector`'s own documentation says SwiftUI
  subtrees walk as ordinary `NSView`s with no supported way to read resolved modifier values. A
  SwiftUI fixture would make the two tiers nearly indistinguishable, which is the one thing this
  fixture must not do.

### Changed — a capability claim withdrawn

- **`unexposedControl` is now recorded as unconfirmed rather than as a measured capability**, in
  both `references/native-lane.md` and `references/engine-capability-matrix.md`. Version 3.2.0
  asserted that `proctor_assert`'s `agree` catches a control-shaped region with no accessibility
  node, on the strength of the tool's documentation and its worked example at 96×28. The fixture
  plants exactly that. Across three runs it produced six to seven `agree` findings and **none was
  `unexposedControl`** — at 38×22, and again at 96×28 with a label — while `proctor_assert`
  `exists` on the same control returned `found: false` and the capture showed it painted.
  `ghostNode`, its mirror image, fired correctly in the same runs.

  Stating a capability from a vendor's documentation before anything exercises it is the precise
  habit this skill exists to break, and 3.2.0 did it. The route to that finding is now the mock's
  control inventory against the tree, which needs no new instrument.

### Found by the fixture, unplanted

- **An `NSButton` with a `.rounded` bezel constrained to 20pt reports `h: 22` in the
  accessibility tree and paints nothing.** `agree` called it a `ghostNode` — "that region is a
  flat fill of the window background colour" — and the capture agreed. `isBordered = false` did
  not fix it. The fixture draws its own small control instead, and the AppKit behaviour is
  recorded rather than worked around silently, because an answer key that says "hit size" over an
  invisible button is lying about what it tests.

## 3.2.0 — 2026-08-20

A report with zero findings and nine inconclusive classes was honest and useless. The classes the browser
engine cannot measure — `boxShadow`, `backgroundImage`, `textTransform`, transitions, animations, `flex`,
pseudo-elements, `getBBox()` — stayed unmeasured for every target, and the reader was left holding a
screen nobody could close.

**That ceiling belonged to the engine, not to the build**, and treating the two as the same thing is the
confusion this skill exists to prevent arriving one level up. A class one engine cannot measure is not a
class nobody can.

### Added

- **`references/native-lane.md`** — a second measurement engine, driving the `proctor` skill. It covers
  four target shapes the DOM and React Native lanes cannot reach: a native macOS app built to a mock, an
  Electron or Chromium app shipped as a Mac app, a React web build inside a Mac web view, and **a web
  build whose divergence sits in a class this engine returns `""` for**. That last one is why this is a
  second engine rather than a native-only lane: a shadow CSSOM reports as an empty string is a
  `shadowRadius`, `shadowOffset` and `shadowOpacity` on a `CALayer`, and those are readable.
- **A capability preflight for the second engine, with two tiers.** `proctor_inspect` returns a resolved
  view and layer hierarchy for an app embedding `ProctorReflector`, and `reflectorUnavailable` for one
  that does not. Tier A measures colour, font, radius, opacity and shadow; **Tier B leaves every style
  class inconclusive with that reason**, because the ceiling is the tree plus pixels and an eyedropped
  colour is not a declared value. The tier is established before Phase 2 and recorded, since it decides
  what a finding may claim. It is not a degraded Tier A that can be talked up.
- **`UNSTABLE`, the fourth state.** The evidence behind this skill names four — `MEASURED`,
  `UNAVAILABLE`, `UNSTABLE`, `ERROR` — and the skill implemented three. `UNSTABLE` carries
  `UNAVAILABLE`'s rule: repeated reads of a fixed input varying outside calibrated bounds are not
  compared. A 2026 study of 262 web visual-flakiness cases split them 59.9% structure-related and 40.1%
  style-related, so instability is a classification rather than noise to be tolerated away. The web lane
  has no instrument for it; `proctor_stability` is one, returning `firstDivergence` and a per-step
  `stepInstability` from 0 to 1.
- **A calibrated geometry tolerance.** Every `proctor_assert` geometry kind takes `tolerance` in points
  and defaults it to 1.0. The research is explicit that a numeric tolerance is defensible only after
  repeated-run measurement proves non-zero variance, so stability runs first and its variance sets the
  number. A default carried into a report is an assumption wearing a calibration's clothes.
- **Three questions the browser lane cannot ask at all**, now askable: whether a capture is current
  (`SCFrameStatus`, `dirtyRectCount`, `framesWaited`, `trustworthy` — a stale frame is pixel-identical to
  a correct one and obscura offers no signal); whether an animation is in flight (`getAnimations()`
  returns 0 while one runs, and the layer's model and presentation values differ exactly while it does);
  and whether a control-shaped region has no accessibility node behind it (`proctor_assert`'s `agree`,
  returning `unexposedControl`). The third is a present-in-mock, absent-in-build finding this skill could
  not previously produce, and neither a tree dump nor a screenshot review reaches it, because each is one
  observer agreeing with itself.
- **Eval 9**, the only one whose target is not a DOM. It hands the run the zero-findings-nine-inconclusive
  report and asks for the screen to be closed out. It has not been run, and it cannot be with the current
  fixtures — its target is a running Mac app rather than an HTML file — which `EVALS.md` states rather
  than leaving to be discovered.

### Changed

- **`references/engine-capability-matrix.md` carries the second engine's rows**, because it is the single
  home for capability facts and a second copy is how nine classes stayed hidden for nine versions. It
  records the two tiers, the five classes proctor measures that obscura cannot, and the known ceilings:
  an iOS Simulator target has no accessibility tree and its screenshots carry no frame status, a lazily
  built macOS submenu is inconclusive rather than absent, and the reflector is a debug-build dependency
  so a release build measures at Tier B whatever its debug twin managed.
- **The artifact contract gains the lane's own files** — `target.snapshot.json`, `target.inspect.json`,
  `target.assert.json` **including `skipped[]`**, `target.stability.json`, and a capture stored with its
  trustworthiness fields. Dropping `skipped[]` on the way into the ledger converts every unaskable
  question into silence, which is the transformation the whole file exists to prevent.
- **A `regionMatches` against the mock is a tripwire, never a verdict**, on the grounds this skill already
  gives for pixel diffs. The research reached explicitly for a measured cross-platform parity method and
  found the field using SSIM as the approach rather than as the evidence.
- **The actuation plane is a fidelity fact, not a mechanical one.** `proctor_act`'s process-directed plane
  reaches occluded and other-Space windows without stealing focus; four step kinds inject synthetic events
  and need the window foreground. A run whose `foreground.measured` count is above zero cannot be repeated
  unattended, so a ledger row closed by such a step carries that and a batch lane cannot schedule it
  beside another.
