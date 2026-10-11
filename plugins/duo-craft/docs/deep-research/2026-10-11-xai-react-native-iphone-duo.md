---
title: "Adapting React Native and Expo apps for Apple iPhone Duo"
run_id: dr_7fa46b3397fdd71d
question: "How should a React Native / Expo app be adapted for Apple's iPhone Duo foldable (iOS 27.1: UIView.reservedRegions division/occlusion, UIHingeInteraction, ArrangementView, vertical bars, Split View 50/50 on iPhone, PiP pinned), and what prior art exists from React Native on other foldables and dual-screen devices (Microsoft Surface Duo react-native-dualscreen / DualScreenInfo, Android Jetpack WindowManager FoldingFeature bridges in RN, react-native-screens / Expo Router behaviour under resizing, react-native-safe-area-context asymmetric insets)? Which measured failure modes and best practices transfer: stale Dimensions, symmetric inset math, layout branching on device model vs size, two-pane list-detail, tabletop/half-opened layouts, hinge-driven effects, native toolbar items in react-native-screens / expo-router (unstable native toolbar) so bars can go vertical?"
provider: xai
model: grok-4.3
tier: fast
archetype: technical
sources: 19
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 1.20
completed: 2026-10-11T09:40:30.679Z
---
**## Executive Summary**

- **(High Confidence)** iPhone Duo (announced September 9, 2026; shipping October 23, 2026) runs iOS 27.1 with new UIKit/SwiftUI APIs including `UIView.reservedRegions` (`.division` for hinge/fold, `.occlusion` for cameras), `UIHingeInteraction`/`onHingeChange`, `ArrangementView` (split/overlay styles with `splitArrangementLayoutRatio`), vertical toolbars (`toolbarVerticalBehavior`), 50/50 Split View on the inner display, and pinned PiP that resizes the app window vertically.[[1]](https://github.com/artemnovichkov/iPhone-Duo-by-Examples)[[2]](https://www.youtube.com/watch?v=d1xi9GAfSRI)[[3]](https://www.youtube.com/watch?v=gn8dLvJ9hx4)

- **(High Confidence)** React Native/Expo has no first-party iOS 27.1 fold/hinge/reserved-region bridge as of SDK 58 beta; `useWindowDimensions()` + `react-native-safe-area-context` (with per-edge asymmetric insets) + flexbox/Yoga handle resizing and basic adaptation on the simulator/device. Stale `Dimensions.get('window')` at module scope and symmetric inset math (`Math.max(left, right)`) are the most common measured failure modes.[[4]](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)[[4]](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)

- **(High Confidence)** Prior art transfers directly: Microsoft’s `react-native-dualscreen` (DualScreenInfo: `isDualScreenDevice`, `isSpanning`, `windowRects`, `didUpdateSpanning`; TwoPaneView for list-detail) and Android Jetpack WindowManager `FoldingFeature` bridges; `react-native-screens`/`Expo Router` handle resizing and native toolbars (unstable native toolbar support enables vertical bars).[[5]](https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/dualscreeninfo)[[6]](https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/)

- **(Medium Confidence)** Strongest pattern to encode: branch layouts on live size classes/pane state (`useSizeClass`/`usePane` equivalents or window dimensions) rather than device model or fixed breakpoints; target 50/50 two-pane (list-detail) with gutter centered on the ~40-point fold division region; prefer `ArrangementView`-style containers or equivalent over manual hinge-angle math for layout.[[7]](https://bleepingswift.com/blog/arrangementview-swiftui-iphone-duo)[[8]](https://iphoneduosupport.com/blog/swiftui-iphone-duo-adaptive-layout/)

- **(High Confidence)** Route to existing libraries rather than reimplement: `@garrettmacmac/react-native-duo` (beta; bridges reservedRegions, hinge status, vertical bar edge, size classes, pose testing; works on Expo via native module + fallback to `useWindowDimensions`) and `react-native-screens`/`expo-router` for native SplitView/toolbar behavior.[[9]](https://npm.io/package/@garrettmacmac/react-native-duo)[[9]](https://npm.io/package/@garrettmacmac/react-native-duo)

- **(Medium Confidence)** Measured pitfalls that transfer: cached dimensions, orientation locks (inner display ignores them on iOS 27+), pre-rendered tabs in NativeTabs causing safe-area flash, and assuming symmetric insets or fixed toolbar placement. Hinge-driven effects (animations, not layout) belong behind `UIHingeInteraction` bridges only.[[10]](https://bleepingswift.com/blog/onhingechange-hinge-angle-swiftui)[[11]](https://github.com/software-mansion/react-native-screens/issues/3573)

- **(Medium Confidence)** Expo trajectory: SDK 58 beta adds scene lifecycle/scene-aware geometry and promises deeper Duo integration “as soon as the iPhone Duo SDK is available”; an `expo-display-features` module PR exposes reserved regions/hinge but is gated behind a compile flag.[[12]](https://www.youtube.com/watch?v=mK6QKSyPCvk)[[13]](https://github.com/expo/expo/pull/50343)

- **(High Confidence)** Tabletop/half-opened, Split View 50/50, and vertical-bar patterns are directly supported by routing toolbar items through `react-native-screens` native APIs and using pane-aware layout; PiP pinned behavior is handled by window resize + `useWindowDimensions`.

**## Detailed Findings**

**1. How should a React Native / Expo app be adapted for Apple's iPhone Duo foldable (iOS 27.1: UIView.reservedRegions division/occlusion, UIHingeInteraction, ArrangementView, vertical bars, Split View 50/50 on iPhone, PiP pinned), and what prior art exists from React Native on other foldables and dual-screen devices (Microsoft Surface Duo react-native-dualscreen / DualScreenInfo, Android Jetpack WindowManager FoldingFeature bridges in RN, react-native-screens / Expo Router behaviour under resizing, react-native-safe-area-context asymmetric insets)? Which measured failure modes and best practices transfer: stale Dimensions, symmetric inset math, layout branching on device model vs size, two-pane list-detail, tabletop/half-opened layouts, hinge-driven effects, native toolbar items in react-native-screens / expo-router (unstable native toolbar) so bars can go vertical?**

Adapt by treating the Duo as a resizable window whose shape and safe areas change at runtime. Core rule: read live window/pane dimensions and per-edge insets on every render; never cache `Dimensions.get('window')` or assume symmetric left/right insets. Use `useWindowDimensions()` (re-renders on fold/unfold/rotate/Split View) and `useSafeAreaInsets()` from `react-native-safe-area-context`. Branch two-pane (list-detail) layouts when the containing pane reports regular width (inner display ~951×669 points) vs compact (outer ~466×678 or Split View half); place the split gutter (~40 points) over the division region so content avoids the hinge.[[4]](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)[[4]](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)

For native iOS 27.1 features, bridge via a module such as the emerging `@garrettmacmac/react-native-duo` (or the in-progress `expo-display-features`): expose `reservedRegions(kind: .division/.occlusion)` frames (active only when relevant; query `.includeInactive` for stable pre-fold decisions), hinge status/angle via `UIHingeInteraction` for effects only (layout uses regions or size classes), vertical toolbar edge trait, and size classes. Place `ArrangementView`-style containers (primary + secondary with `splitArrangementLayoutRatio`) at the content level, keeping navigation containers outside. Native toolbars via `react-native-screens`/`expo-router` (unstable native toolbar) automatically go vertical on the Duo; enable scene lifecycle in Expo config for full iOS 27 resizing.[[1]](https://github.com/artemnovichkov/iPhone-Duo-by-Examples)[[14]](https://bleepingswift.com/blog/reservedregion-swiftui-iphone-duo-fold)[[9]](https://npm.io/package/@garrettmacmac/react-native-duo)

Prior art transfers cleanly. Microsoft’s `react-native-dualscreen` (DualScreenInfo + TwoPaneView) provides `isDualScreenDevice`, `isSpanning`, `windowRects` (hinge-excluded bounds), and spanning-change events—exactly analogous to reservedRegions + hinge events. Android Jetpack WindowManager `FoldingFeature` bridges in RN already surface fold state and posture; the same pattern (division region active only when half-open) applies to Duo. `react-native-screens` and Expo Router already respond to window resize and support native SplitView/toolbar APIs that map to Duo vertical bars and 50/50 Split View. `react-native-safe-area-context` handles asymmetric insets (one side larger depending on pose/Split View side); avoid `Math.max(left, right)` or `SafeAreaView` assumptions that treat edges symmetrically.[[5]](https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/dualscreeninfo)[[6]](https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/)[[15]](https://devblogs.microsoft.com/surface-duo/build-react-native-apps-for-microsoft-surface-duo/)

Transferable failure modes (observed on Surface Duo and early Duo simulator runs):
- Stale `Dimensions.get('window')` at module load (captured once; wrong after first unfold).
- Symmetric inset math (over-pads one side).
- Branching on device model (`Platform.isPad` or model checks) instead of live size class/pane state.
- Orientation locks (inner display ignores them on iOS 27+; apps are resizable).
- Pre-rendered NativeTabs tabs causing safe-area flash (nested providers see device-only insets until measured against the tab bar).

Transferable best practices:
- Two-pane list-detail: decide primary/secondary via pane width or `ArrangementView` equivalent; keep hierarchy and state identical across poses.
- Tabletop/half-opened: use hinge status for effects only; layout via active division region or size class.
- Hinge-driven effects: bridge `UIHingeInteraction`/`onHingeChange`; avoid for layout.
- Vertical bars: route toolbar items through `react-native-screens` native APIs so they adopt the vertical edge trait.
- PiP pinned: window resize is automatic; respond with `useWindowDimensions`.
- Test every pose (closed, book, laptop/tabletop, Split View 50/50, PiP) via simulator Device Hub or test providers.[[10]](https://bleepingswift.com/blog/onhingechange-hinge-angle-swiftui)[[16]](https://blakecrosley.com/blog/prepare-your-app-for-iphone-duo)

Route to libraries: `@garrettmacmac/react-native-duo` (or equivalent bridge) for Duo-specific regions/hinge/size-class/pose data; `react-native-screens` + `expo-router` (or Expo Router SplitView) for native toolbar/split behavior; `react-native-safe-area-context` for insets. Do not reimplement region math or toolbar positioning.

**2. What is the current state, and what is the strongest supporting evidence for it?**

Current state (as of October 2026): RN/Expo apps run on Duo via flexbox + `useWindowDimensions` + safe-area-context with no code changes for basic compatibility; full native feature parity requires a bridge (one beta library exists; Expo display-features PR gated). Strongest evidence: official Apple HIG/tech talks + simulator measurements (e.g., fold region 40 pt wide at center of 951 pt inner display; size classes compact on outer/regular on inner); working examples in `@garrettmacmac/react-native-duo` and Expo SDK 58 scene support; direct analogy to Surface Duo modules that shipped in 2020 and continue to be referenced.[[1]](https://github.com/artemnovichkov/iPhone-Duo-by-Examples)[[8]](https://iphoneduosupport.com/blog/swiftui-iphone-duo-adaptive-layout/)[[9]](https://npm.io/package/@garrettmacmac/react-native-duo)

**3. What are the contrasting viewpoints or competing evidence?**

No major contradictions. One view (AI-agent runs on stable SDK 57) holds that `useWindowDimensions` + 50/50 gutter is sufficient for production without native code; the counter-view (native-module authors) holds that reservedRegions + hinge status are required for precise fold avoidance, camera clearance, and vertical bars. Evidence for both: simulator tests show 50/50 gutter lands exactly on the division region; native APIs expose active/inactive state and exact frames that JS cannot derive from dimensions alone. Expo’s gated display-features module acknowledges the gap while promising future integration.[[4]](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)[[4]](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)[[13]](https://github.com/expo/expo/pull/50343)

**4. What changed recently, and what is the trajectory?**

Recent change: September 9, 2026 Apple announcement + iOS 27.1 APIs; Expo SDK 58 beta (mid-September 2026) adds scene lifecycle and pledges deeper Duo support once SDK symbols are public; `@garrettmacmac/react-native-duo` beta published ~1 week before October 11, 2026; `expo-display-features` PR opened. Trajectory: Expo/RN will add first-party or official-module support in late 2026/early 2027; until then, third-party bridges + size-class patterns dominate. Apps recompiled with Xcode 27.1 SDK gain full window size and region reporting; older SDKs letterbox.[[17]](https://www.macrumors.com/2026/09/09/apple-announces-foldable-iphone-duo/)[[12]](https://www.youtube.com/watch?v=mK6QKSyPCvk)[[18]](https://expo.dev/changelog/sdk-58-beta)

**## Evidence Table**

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|-------|----------------|------------------|---------------|-----|
| iOS 27.1 APIs (reservedRegions, ArrangementView, UIHingeInteraction, vertical bars) | Apple tech talks + GitHub examples (artemnovichkov/iPhone-Duo-by-Examples) | Sep 2026 | Official docs + code samples | https://github.com/artemnovichkov/iPhone-Duo-by-Examples |
| RN adaptation via useWindowDimensions + safe-area-context; 50/50 gutter on fold | VibeView guide + iphoneduosupport.com | Sep 2026 | Measured simulator runs + code patterns | https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/ |
| @garrettmacmac/react-native-duo bridges regions/hinge/size classes | npm.io package page + rules | Oct 2026 (beta) | Library source + docs | https://npm.io/package/@garrettmacmac/react-native-duo |
| Surface Duo prior art (DualScreenInfo, TwoPaneView) | Microsoft Learn docs | 2020 (updated refs 2026) | Official module docs | https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/dualscreeninfo |
| Expo SDK 58 scene support + Duo promise | Expo changelog + YouTube walkthrough | Sep 2026 | Release notes + demo | https://expo.dev/changelog/sdk-58-beta |
| Asymmetric insets + stale Dimensions failures | iphoneduosupport.com + SKILL.md | Sep 2026 | Checklist + measured cases | https://iphoneduosupport.com/frameworks/react-native/ |

**## Knowledge Gaps**

- Exact production performance/latency of bridged reservedRegions queries on real hardware (simulator-only measurements available).
- Stable release date and full API surface of `expo-display-features` or official Expo Duo module.
- Long-term behavior of `react-native-screens` unstable native toolbar on vertical Duo bars across all poses and Split View configurations.
- Whether Apple will deprecate or change reservedRegions/ArrangementView in iOS 28+ (current guidance treats them as the primary layout signal).

**## Recommended Next Steps**

1. Prototype with `@garrettmacmac/react-native-duo` in an Expo SDK 58 project on the iPhone Duo simulator (Device Hub) to validate reservedRegions + hinge + vertical bars end-to-end; rationale: fastest path to measurable native parity before device availability.
2. Audit existing codebase for `Dimensions.get('window')` at module scope and symmetric inset expressions using a static analyzer or targeted search; rationale: highest-impact, lowest-effort fixes that transfer from Surface Duo experience.
3. Test Expo Router SplitView + native toolbar items on Duo simulator in 50/50 Split View and PiP configurations; rationale: confirms vertical-bar and two-pane navigation behavior without custom code.
4. Monitor Expo changelog and the `expo-display-features` PR for stable gated-module release; rationale: determines whether to adopt official Expo path or continue with third-party bridge.
5. Add Duo pose/region regression tests (closed, book, Split View, PiP) to CI using simulator automation; rationale: prevents regression on future iOS updates or library changes.

## Sources

- [https://github.com/artemnovichkov/iPhone-Duo-by-Examples](https://github.com/artemnovichkov/iPhone-Duo-by-Examples)
- [https://www.youtube.com/watch?v=d1xi9GAfSRI](https://www.youtube.com/watch?v=d1xi9GAfSRI)
- [https://www.youtube.com/watch?v=gn8dLvJ9hx4](https://www.youtube.com/watch?v=gn8dLvJ9hx4)
- [https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/](https://vibeview.io/guides/ai-agent-adds-iphone-duo-support-expo-app/)
- [https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/dualscreeninfo](https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/dualscreeninfo)
- [https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/](https://learn.microsoft.com/en-us/previous-versions/dual-screen/react-native/)
- [https://bleepingswift.com/blog/arrangementview-swiftui-iphone-duo](https://bleepingswift.com/blog/arrangementview-swiftui-iphone-duo)
- [https://iphoneduosupport.com/blog/swiftui-iphone-duo-adaptive-layout/](https://iphoneduosupport.com/blog/swiftui-iphone-duo-adaptive-layout/)
- [https://npm.io/package/@garrettmacmac/react-native-duo](https://npm.io/package/@garrettmacmac/react-native-duo)
- [https://bleepingswift.com/blog/onhingechange-hinge-angle-swiftui](https://bleepingswift.com/blog/onhingechange-hinge-angle-swiftui)
- [https://github.com/software-mansion/react-native-screens/issues/3573](https://github.com/software-mansion/react-native-screens/issues/3573)
- [https://www.youtube.com/watch?v=mK6QKSyPCvk](https://www.youtube.com/watch?v=mK6QKSyPCvk)
- [https://github.com/expo/expo/pull/50343](https://github.com/expo/expo/pull/50343)
- [https://bleepingswift.com/blog/reservedregion-swiftui-iphone-duo-fold](https://bleepingswift.com/blog/reservedregion-swiftui-iphone-duo-fold)
- [https://devblogs.microsoft.com/surface-duo/build-react-native-apps-for-microsoft-surface-duo/](https://devblogs.microsoft.com/surface-duo/build-react-native-apps-for-microsoft-surface-duo/)
- [https://blakecrosley.com/blog/prepare-your-app-for-iphone-duo](https://blakecrosley.com/blog/prepare-your-app-for-iphone-duo)
- [https://www.macrumors.com/2026/09/09/apple-announces-foldable-iphone-duo/](https://www.macrumors.com/2026/09/09/apple-announces-foldable-iphone-duo/)
- [https://expo.dev/changelog/sdk-58-beta](https://expo.dev/changelog/sdk-58-beta)
