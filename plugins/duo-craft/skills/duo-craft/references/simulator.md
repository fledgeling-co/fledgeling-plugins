# Running and checking an app on the iPhone Duo simulator

Everything here was measured on 2026-10-11 with Xcode 27.1 RC (build 27A9274) on macOS 27, driving a
React Native 0.88 / Expo SDK 58 app. Re-check the version numbers before trusting the paths.

## Toolchain: point each command at Xcode 27.1, never switch the system

The fold APIs (`UIView.reservedRegions`, `UIHingeInteraction`) exist only in the iOS 27.1 SDK; the
27.0 SDK has neither, and both Xcodes ship Swift 6.4, so `#if compiler(...)` cannot tell them apart.
Build the whole app with 27.1. Set it per command so the owner's other projects keep their Xcode:

```bash
export DEVELOPER_DIR=/Applications/Xcode-27.1.0-Release.Candidate.app/Contents/Developer
xcrun --sdk iphoneos --show-sdk-version          # must print 27.1 or later
```

`xcode-select -s` changes every project on the machine and needs the owner; leave it to them.

The iOS 27.1 simulator runtime is a separate 7.85 GB download:

```bash
xcodebuild -downloadPlatform iOS                 # with DEVELOPER_DIR set; ~15 min on a fast line
xcrun simctl list devicetypes | grep -i duo      # com.apple.CoreSimulator.SimDeviceType.iPhone-Duo
```

## Build without Metro

A Release build embeds the JS bundle, so the simulator needs no dev server:

```bash
cd ios && pod install                            # after adding a local module under modules/
xcodebuild -workspace App.xcworkspace -scheme App -configuration Release \
  -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath <scratch>/dd CODE_SIGNING_ALLOWED=NO build
```

An Expo project with no committed `ios/` needs `npx expo prebuild -p ios --no-install` first. Local
Expo modules autolink from `./modules/` by default (`nativeModulesDir`), so a module there is picked up
by `pod install` with no config change; the pod log prints `Installing <Pod> (1.0.0)`.

## The simulator UI is Device Hub, and it can lose its device list

Xcode 27 replaced Simulator.app with **Device Hub**
(`Xcode-27.1…app/Contents/Applications/DeviceHub.app`). Opening, closing, folding, rotating and Split
View are its on-screen controls; `simctl` has no hinge or posture command (its help lists none, and no
binary in CoreSimulator mentions one).

**Device Hub showing "No Devices" while `simctl list devices` shows booted simulators** is a stale
`CoreDeviceService`. Its log says `Created device <private> was not found in DeviceKit after
retries` (read with `/usr/bin/log show --predicate 'process == "DeviceHub"'` — zsh shadows `log`).
The fix, from a Simulator engineer at the WWDC labs via RocketSim's write-up, confirmed here:

```bash
osascript -e 'tell application id "com.apple.dt.Devices" to quit'
killall -9 CoreDeviceService                      # restarts on its own
open -a "<Xcode 27.1>/Contents/Applications/DeviceHub.app"
```

Every failed "add device" attempt still creates a simulator, so clean up duplicates afterwards.

Device Hub refuses Accessibility scripting (System Events cannot read its menu bar) and proctor cannot
attach to it, so driving poses means synthetic clicks on the owner's screen. That takes their mouse and
focus: ask first, and prefer having them set the pose while you capture.

## Capture each display separately

The Duo simulator exposes several screens; screenshot by display id:

```bash
xcrun simctl io <udid> enumerate | grep -E "Screen ID|Name:"
xcrun simctl io <udid> screenshot --display=1 outer.png   # 1398×2034 — the outer display
xcrun simctl io <udid> screenshot --display=3 inner.png   # 2853×2007 or 2007×2853 — the inner display
```

The display that is off returns an all-black frame of the right size. Check `getextrema()` before
reading one: a black frame is "that display is off", not "the app rendered nothing". The inner
display renders at the 2853×2007 App Store screenshot size (3× of 951×669pt), not its 2670×1878 panel.

Deep links open a confirmation alert ("Open in …?") that needs a tap, so navigate by deep link only
when someone can tap it; otherwise drive in-app navigation.

## The pose matrix

Capture every row, or name it as not reached and why. "Checked on the simulator" means the capture was
opened and read, ideally through `be-my-witness:be-my-witness` region by region.

| Pose | Window (pt) | What to confirm |
|---|---|---|
| Closed, portrait | 466×678, 84pt trailing bar | Bar items vertical; title clears the top; nothing under the bar |
| Closed, landscape | 678×466 | Bar still trailing; camera bottom-right; layout survives the short height |
| Open flat, landscape | 951×669, 84pt trailing bar | Two panes or two columns meeting at 475.5pt; no sidebar eating the list |
| Book (partly folded) | same, active vertical division | Nothing tappable in the band; split holds without a jump |
| Open, portrait | 669×951, 84 top / 95 bottom bars | Horizontal bars; regular-width layout, not a stretched phone column |
| Tabletop | portrait, active horizontal division | Content on the raised half, controls on the flat half |
| Split View, left | ~475×669 | Bar on the **left** edge; compact layout; insets swapped |
| Split View, right | ~475×669 | Bar on the right edge; status column present |
| PiP pinned (portrait) | height shrinks live | Layout reflows vertically with no clipped controls |
