# Changelog

All notable changes to the `mockup-fidelity` plugin.

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
