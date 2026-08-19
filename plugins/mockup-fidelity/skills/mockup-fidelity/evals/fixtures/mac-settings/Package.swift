// swift-tools-version: 5.9
import PackageDescription

// A fixture app, deliberately dependency-free.
//
// The eval it serves turns on the proctor lane's capability tier, so the fixture
// has to be able to sit on BOTH sides of that line. It builds Tier B by default —
// no reflector, so `proctor_inspect` answers `reflectorUnavailable` and every
// style class is inconclusive. Building Tier A means adding ProctorReflector by
// local path, which the README spells out; it is not a dependency here because a
// fixture that cannot build without a second repository checked out is a fixture
// that does not run.
let package = Package(
    name: "SettingsFixture",
    platforms: [.macOS(.v13)],
    targets: [
        .executableTarget(name: "SettingsFixture", path: "Sources/SettingsFixture")
    ]
)
