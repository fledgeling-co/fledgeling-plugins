#!/usr/bin/env python3
"""Audit a React Native / Expo project for iPhone Duo readiness.

Each check is a fixed assumption that breaks on a foldable iPhone, found in a real app or named in
Apple's iPhone Duo guidance. The script reports file:line evidence and never edits anything.

    python3 duo_audit.py <project-root>            # human report, exit 1 if any error
    python3 duo_audit.py <project-root> --json     # machine report
    python3 duo_audit.py --self-test               # prove every check can fire, and stay quiet

Severity: error = visibly wrong on iPhone Duo; warn = likely wrong, confirm on the simulator;
info = a place to look, not a defect (most hidden headers are tabs and modals that are fine).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict

SKIP_DIRS = {"node_modules", ".git", "ios", "android", "build", "dist", ".expo", "coverage", "Pods", "__tests__"}
SRC_EXT = (".ts", ".tsx", ".js", ".jsx")


@dataclass
class Finding:
    check: str
    severity: str
    file: str
    line: int
    text: str
    why: str


CHECKS = [
    # (id, severity, regex, why)
    ("stale-dimensions", "error",
     re.compile(r"Dimensions\.get\(\s*['\"](window|screen)['\"]\s*\)"),
     "Dimensions.get is a snapshot; the window resizes as iPhone Duo opens, closes, folds and enters "
     "Split View. Use useWindowDimensions() or onLayout."),
    ("symmetric-insets", "error",
     re.compile(r"insets\.(left|right)\s*\*\s*2|2\s*\*\s*insets\.(left|right)|paddingHorizontal:\s*insets\.(left|right)"),
     "Side insets are unequal on iPhone Duo (84pt on the bar side, 0 on the other) and swap sides "
     "between Split View halves. Pad each edge from its own inset."),
    ("title-top-from-inset", "warn",
     re.compile(r"(paddingTop|marginTop|top):\s*insets\.top\s*\+\s*\d{1,2}\b"),
     "With no status bar across the top the inset is 0, so a title at insets.top + 8 touches the edge. "
     "Clear where a status bar would be (59pt) when the inset is 0."),
    ("device-branching", "warn",
     re.compile(r"Platform\.isPad|DeviceType\.(TABLET|PHONE)|deviceType\s*===|getDeviceType\(|isTablet\("),
     "Branching on device model misreads iPhone Duo (an iPhone with an iPad-width inner display). "
     "Branch on available width and on whether a fold exists."),
    ("orientation-branching", "warn",
     re.compile(r"getOrientationAsync|useDeviceOrientation|Orientation\.(PORTRAIT|LANDSCAPE)|window\.width\s*>\s*window\.height\s*\?"),
     "The inner display ignores supported orientations. Lay out from the space you have, not the "
     "orientation; aspect is fine as one input among several."),
    ("core-safeareaview", "warn",
     re.compile(r"import\s*\{[^}]*\bSafeAreaView\b[^}]*\}\s*from\s*['\"]react-native['\"]"),
     "react-native's SafeAreaView handles only the notch case. Use react-native-safe-area-context."),
    ("hard-width-breakpoint", "warn",
     re.compile(r"width\s*[<>]=?\s*(3[2-9]\d|4[0-4]\d)\b|width\s*===?\s*(375|390|393|402|414|428|430|440)\b"),
     "A breakpoint tuned to iPhone widths misfires on iPhone Duo's 382pt outer and 669/867pt inner "
     "content widths. Use size tiers from the available width."),
    ("hidden-header-own-buttons", "info",
     re.compile(r"headerShown:\s*false"),
     "A screen that hides the native header and draws its own buttons keeps them out of the vertical "
     "bar. Prefer native header/toolbar items (with an icon and a title) where the screen has actions."),
]


def iter_sources(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.endswith(SRC_EXT):
                yield os.path.join(dirpath, name)


def scan_sources(root: str) -> list[Finding]:
    out: list[Finding] = []
    for path in iter_sources(root):
        rel = os.path.relpath(path, root)
        try:
            lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith(("//", "*")):
                continue
            for cid, sev, rx, why in CHECKS:
                if rx.search(line):
                    out.append(Finding(cid, sev, rel, i, line.strip()[:160], why))
    return out


def scan_config(root: str) -> list[Finding]:
    out: list[Finding] = []
    app_json = os.path.join(root, "app.json")
    if os.path.exists(app_json):
        try:
            cfg = json.load(open(app_json)).get("expo", {})
        except (OSError, ValueError):
            cfg = {}
        if cfg.get("orientation") == "portrait":
            out.append(Finding("portrait-lock", "warn", "app.json", 1, '"orientation": "portrait"',
                               "Honoured on the outer display only; the inner display rotates anyway, so "
                               "every screen still needs a landscape layout there."))
        ios = cfg.get("ios", {})
        if ios.get("requireFullScreen") or (ios.get("infoPlist") or {}).get("UIRequiresFullScreen"):
            out.append(Finding("requires-full-screen", "warn", "app.json", 1, "requireFullScreen",
                               "iPhone Duo still resizes the app when it opens and closes, and Split View "
                               "is how people multitask on it."))
    return out


def scan_sdk() -> list[Finding]:
    try:
        ver = subprocess.run(["xcrun", "--sdk", "iphoneos", "--show-sdk-version"],
                             capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return [Finding("sdk-unknown", "warn", "(toolchain)", 0, "xcrun unavailable",
                        "Could not read the iOS SDK. iPhone Duo's fold APIs need the iOS 27.1 SDK.")]
    try:
        major, minor = (int(x) for x in (ver.split(".") + ["0"])[:2])
    except ValueError:
        return []
    if (major, minor) < (27, 1):
        import glob
        found = sorted(glob.glob("/Applications/Xcode*27.[1-9]*.app")) + sorted(glob.glob("/Applications/Xcode*2[89]*.app"))
        hint = (f"Xcode with the 27.1 SDK is installed at {found[0]}: run builds with "
                f"DEVELOPER_DIR={found[0]}/Contents/Developer (and run this audit the same way)."
                if found else "No Xcode 27.1 found in /Applications; install it, then set DEVELOPER_DIR.")
        return [Finding("sdk-too-old", "error", "(toolchain)", 0, f"iOS SDK {ver}",
                        "Below 27.1 the app stops short of the status bar and camera, bars stay "
                        "horizontal and the fold APIs do not exist. " + hint + " Leave xcode-select alone.")]
    return []


def scan_fold_module(root: str) -> list[Finding]:
    for dirpath, _dirs, files in os.walk(os.path.join(root, "modules")):
        for f in files:
            if f.endswith(".swift") and "reservedRegions" in open(os.path.join(dirpath, f), errors="replace").read():
                return []
    return [Finding("no-fold-signal", "warn", "(project)", 0, "no module reads reservedRegions",
                    "React Native has no fold API. Without a native module the app cannot tell a fold "
                    "from an iPad, so two-pane and tabletop layouts have nothing to key on.")]


def expo_major(root: str) -> int | None:
    """Installed Expo first (exact), then the declared range in package.json."""
    try:
        v = json.load(open(os.path.join(root, "node_modules", "expo", "package.json")))["version"]
    except (OSError, ValueError, KeyError):
        try:
            v = json.load(open(os.path.join(root, "package.json"))).get("dependencies", {}).get("expo", "")
        except (OSError, ValueError):
            return None
    m = re.search(r"(\d+)\.", v)
    return int(m.group(1)) if m else None


def scan_scene_lifecycle(root: str) -> list[Finding]:
    major = expo_major(root)
    if major is None or major >= 58:
        return []
    try:
        plugins = json.load(open(os.path.join(root, "app.json"))).get("expo", {}).get("plugins", [])
    except (OSError, ValueError):
        plugins = []
    for p in plugins:
        if isinstance(p, list) and p and p[0] == "expo-build-properties" and len(p) > 1 \
                and (p[1].get("ios") or {}).get("enableSceneSupport"):
            return []
    ios = os.path.join(root, "ios")
    if os.path.isdir(ios):
        for dirpath, _dirs, files in os.walk(ios):
            if "Pods" in dirpath:
                continue
            if "Info.plist" in files and "UIApplicationSceneManifest" in open(
                    os.path.join(dirpath, "Info.plist"), errors="replace").read():
                return []
    return [Finding("no-scene-lifecycle", "error", "app.json", 1, f"Expo SDK {major}, no scene delegate",
                    "Built with the iOS 27 SDK, an app with no scene delegate is stopped at launch "
                    "(_UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption). Expo 58 prebuild "
                    "adopts scenes; on SDK 57 (expo >= 57.0.23) set expo-build-properties "
                    "ios.enableSceneSupport, which install_templates.py does.")]


def audit(root: str, sdk: bool = True) -> list[Finding]:
    found = scan_sources(root) + scan_config(root) + scan_fold_module(root) + scan_scene_lifecycle(root)
    if sdk:
        found += scan_sdk()
    return found


def report(findings: list[Finding], root: str) -> str:
    if not findings:
        return f"duo-audit: {root}: no findings"
    lines = [f"duo-audit: {root}: {sum(f.severity == 'error' for f in findings)} error(s), "
             f"{sum(f.severity == 'warn' for f in findings)} warning(s)"]
    by_check: dict[str, list[Finding]] = {}
    for f in findings:
        by_check.setdefault(f.check, []).append(f)
    for cid, items in by_check.items():
        lines.append(f"\n[{items[0].severity}] {cid} ({len(items)}): {items[0].why}")
        if items[0].severity == "info":
            lines.append("  (listed with --json; review the screens that draw their own action buttons)")
            continue
        for f in items[:12]:
            lines.append(f"  {f.file}:{f.line}  {f.text}")
        if len(items) > 12:
            lines.append(f"  … {len(items) - 12} more")
    return "\n".join(lines)


def self_test() -> int:
    bad = {
        "a.tsx": "const W = Dimensions.get('window').width;\n"
                 "const s = { paddingHorizontal: insets.left };\n"
                 "const t = { paddingTop: insets.top + 8 };\n"
                 "if (Platform.isPad) {}\n"
                 "import { SafeAreaView } from 'react-native';\n"
                 "if (width > 390) {}\n"
                 "const o = { headerShown: false };\n"
                 "const w = width - insets.left * 2;\n"
                 "const r = window.width > window.height ? 1 : 0;\n",
        "app.json": json.dumps({"expo": {"orientation": "portrait"}}),
        "package.json": json.dumps({"dependencies": {"expo": "~57.0.3"}}),
    }
    good = {
        "b.tsx": "const { width } = useWindowDimensions();\n"
                 "const s = { paddingLeft: insets.left, paddingRight: insets.right };\n"
                 "const t = { paddingTop: titleTopPadding(insets.top) };\n"
                 "// Dimensions.get('window') is stale, do not use\n",
        "modules/duo-fold/ios/DuoFoldModule.swift": "reservedRegions(kind: .division)",
        "app.json": json.dumps({"expo": {"plugins": [["expo-build-properties", {"ios": {"enableSceneSupport": True}}]]}}),
        "package.json": json.dumps({"dependencies": {"expo": "~57.0.3"}}),
    }
    expected_bad = {"stale-dimensions", "symmetric-insets", "title-top-from-inset", "device-branching",
                    "core-safeareaview", "hard-width-breakpoint", "hidden-header-own-buttons",
                    "orientation-branching", "portrait-lock", "no-fold-signal", "no-scene-lifecycle"}
    ok = True
    for label, files, expect in (("bad", bad, expected_bad), ("good", good, set())):
        with tempfile.TemporaryDirectory() as d:
            for rel, body in files.items():
                p = os.path.join(d, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "w").write(body)
            got = {f.check for f in audit(d, sdk=False)}
            if got != expect:
                ok = False
                print(f"self-test {label}: expected {sorted(expect)} got {sorted(got)}")
    print("self-test: pass" if ok else "self-test: FAIL")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    root = os.path.abspath(args[0])
    findings = audit(root, sdk="--no-sdk" not in argv)
    if "--json" in argv:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(report(findings, root))
    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
