# Mac Settings fixture

A running macOS app whose Settings pane is deliberately wrong in eight specific ways, paired with
`settings.html` as its design of record.

It exists because **eval 9 could not be run**. That eval asks what a second measurement engine
can and cannot answer about a native target, and every other fixture in this suite is an HTML
file — so the eval shipped defined and unrunnable, which `EVALS.md` said out loud rather than
leaving to be discovered. This is the target it was missing.

## What makes it a fixture rather than a demo

**It sits on both sides of the capability line.** The eval turns on the proctor lane's tier, so
the fixture has to be able to be either. It builds **Tier B** by default — no reflector, so
`proctor_inspect` answers `reflectorUnavailable` and every style class is inconclusive. Tier A is
opt-in, below.

**Three of the eight divergences are unmeasurable at the default tier, on purpose.** That mirrors
the HTML fixture, where three of ten planted defects cannot be measured by the browser engine —
an answer key that assumes every class can run will bless exactly the failure the skill exists to
prevent.

**One outcome in the key is over-claiming rather than missing.** The accent-colour divergence is
plainly visible in a capture, so a Tier B run can "find" it by eyedropping. Reporting it is a
failure, not a catch. `ANSWER-KEY.md` has the four-valued key.

## Build and run

```bash
swift build
./.build/debug/SettingsFixture &
```

macOS 13+, no dependencies. It draws a 560×452 window titled "Settings Fixture" and sets a
regular activation policy, so it is attachable without an `.app` bundle.

## Tier A — adding the reflector

`ProctorReflector` is a package in the `proctor-mcp` repository. It is deliberately **not** a
dependency here: a fixture that cannot build without a second repository checked out is a fixture
that does not run.

To measure at Tier A, add it by local path and compile the call in:

```swift
// Package.swift
dependencies: [.package(path: "/path/to/proctor-mcp")],
targets: [.executableTarget(
    name: "SettingsFixture",
    dependencies: [.product(name: "ProctorReflector", package: "proctor-mcp")],
    path: "Sources/SettingsFixture",
    swiftSettings: [.define("PROCTOR_REFLECTOR")])]
```

`main.swift` already carries the guarded `ProctorReflector.start()`. The package compiles its
implementation only under `DEBUG` or `PROCTOR_REFLECTOR`, so a release build without the flag
carries no socket and `start()` returns immediately — which is why Tier A is a property of the
build rather than of the app.

## Files

| | |
|---|---|
| `settings.html` | the design of record, longhand CSS, defect locations commented |
| `Sources/SettingsFixture/main.swift` | the app, with the eight divergences in one `Divergence` table |
| `ANSWER-KEY.md` | the four-valued key, measured against the built app rather than derived from source |

## What it is not

It is not an application, and it should not grow into one. Every control on it exists to carry a
planted divergence or to give one a neighbour to be measured against. A ninth defect is cheap to
add and makes the key harder to keep honest, so add one only when a real gap in the eval calls
for it.
