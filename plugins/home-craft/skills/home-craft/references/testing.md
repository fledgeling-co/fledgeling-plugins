# Testing before publishing

## The tools, as they stand in Xcode 27

- **CarPlay Simulator in Device Hub.** Connect a physical iPhone over USB, select it in Device
  Hub, then Device › CarPlay Simulator. This is a Mac receiver the real iPhone drives. Xcode 27.2's
  release notes say the iOS Simulator is not supported for CarPlay, so a CI job cannot open a car
  display on a virtual device.
- **Standalone CarPlay Simulator** (Additional Tools for Xcode). WWDC26 sends video-app developers
  here; it lets you switch the simulated car's video support.
- **The older iOS Simulator path** (I/O › External Displays › CarPlay) belongs to Xcode 26 and
  earlier. Do not plan current testing around it.
- **XCTest** covers what the app owns: which templates the scene delegate builds, depth and tab
  counts, voice-state transitions, playback command routing. Instantiate the scene delegate's
  builders in a `@MainActor` test and assert on the template tree.
- **XCUITest** has no documented way to read the system-drawn CarPlay templates; one forum
  thread (831782) reports the car display exposes no accessibility tree. Treat car and HomeView
  interaction as manual release gates.
- **HomeView** has no simulator. Only a HomeView on HomeView Software 27.2 with a paired iPhone on
  iOS 27.2 shows how the app looks and behaves there.

## Pre-submission matrix

Record for each lane: app build, iOS build, receiver (model and firmware), connection, and the
outcome as **seen**, **not reached** (lane exists, not run) or **not built** (feature absent).

| Lane | Cover | Pass condition |
|---|---|---|
| `home_audit.py <project>` | the whole project | exit 0 |
| XCTest | car-only cold launch with no `WindowGroup`; template choice per category; depth, tab count, list count, voice-state count | assertions pass, including the failure paths |
| CarPlay Simulator, USB iPhone | 800×480 and 1920×720; light and dark; video support toggled mid-session; voice overlay; MiniPlayer; a 12-row list | launches with the phone locked; video tab hidden when unsupported; nothing throws at a limit |
| Real head unit, wired and wireless, TestFlight build | cold launch with the phone in a pocket; phone-call interruption and resume; radio coexistence; touch and knob input | every flow completes without touching the phone |
| CarPlay Ultra car | only if the app claims instrument-cluster or head-up behaviour | same templates; route sharing works |
| HomeView + paired iPhone | the app opening from HomeView; the widget on the Home Screen, on the Modular face and in red night mode; another household member's view; an iPad pairing | app appears and plays; widget discloses nothing private on the shared face; an iPad shows no third-party app |

Developer-observed failure modes worth a look on real hardware (single sources, November 2026):
CarPlay audio apps hanging on a loading spinner on HomeView; disappearing list section headers
(FB24061858) and single-line row truncation on iOS 27; wireless `.playAndRecord` dropping to
24 kHz mono; most production cars reporting `supportsVideoPlayback == false`, which leaves
HomeView as the main place a CarPlay video app shows video today.

For driving the Mac's CarPlay Simulator window or an iOS simulator from an agent, route to
`proctor:proctor`.
