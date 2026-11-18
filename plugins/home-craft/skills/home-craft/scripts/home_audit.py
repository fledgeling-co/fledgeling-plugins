#!/usr/bin/env python3
"""home_audit: static checks for an iOS app that targets CarPlay and HomeView.

Reads a project directory (Xcode project, Swift sources, Info.plist and .entitlements files)
and reports the mistakes that the car head unit, the CarPlay Simulator or App Review would
otherwise find later. It never edits anything.

  home_audit.py <project-dir>            human-readable report, exit 1 on any error
  home_audit.py <project-dir> --json     machine-readable findings
  home_audit.py <project-dir> --strict   warnings fail too
  home_audit.py --self-test              run the bundled fixtures

Each rule names its source in the skill's references, so a finding can be argued with.
"""
from __future__ import annotations

import argparse
import json
import plistlib
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path

SKIP_DIRS = {"Pods", "DerivedData", "build", ".build", "node_modules", ".git", "Carthage", ".swiftpm"}
CARPLAY_PREFIX = "com.apple.developer.carplay-"
LEGACY_KEYS = {"com.apple.developer.playable-content", "com.apple.developer.carplay-messaging"}
COMBINABLE = {"charging", "fueling"}

BASE = {"CPListTemplate", "CPGridTemplate", "CPTabBarTemplate", "CPActionSheetTemplate", "CPAlertTemplate"}
ALL_TEMPLATES = BASE | {
    "CPNowPlayingTemplate", "CPSearchTemplate", "CPVoiceControlTemplate", "CPInformationTemplate",
    "CPPointOfInterestTemplate", "CPContactTemplate", "CPMapTemplate",
}
# category -> (templates allowed on iOS 26, templates added by iOS 27, templates whose cell is disputed)
# Source: CarPlay Developer Guide (13 Oct 2026) template matrix, as read by four research members
# and cross-checked against Apple's per-template pages; see references/capability-matrix.md.
ALLOWED = {
    "audio": (BASE | {"CPNowPlayingTemplate"}, {"CPSearchTemplate", "CPVoiceControlTemplate"}, set()),
    "video": (set(), BASE | {"CPNowPlayingTemplate", "CPSearchTemplate", "CPVoiceControlTemplate"}, set()),
    "voice-based-conversation": (
        BASE | {"CPInformationTemplate", "CPPointOfInterestTemplate", "CPVoiceControlTemplate"}, set(), set()),
    "communication": (BASE | {"CPContactTemplate", "CPInformationTemplate", "CPNowPlayingTemplate"},
                      {"CPVoiceControlTemplate"}, set()),
    "maps": (BASE | {"CPMapTemplate", "CPSearchTemplate", "CPContactTemplate", "CPInformationTemplate",
                     "CPVoiceControlTemplate"}, set(), {"CPSearchTemplate"}),
    "public-safety": (BASE | {"CPContactTemplate", "CPInformationTemplate", "CPNowPlayingTemplate",
                              "CPPointOfInterestTemplate"},
                      {"CPSearchTemplate", "CPVoiceControlTemplate"}, {"CPContactTemplate"}),
    "charging": (BASE | {"CPInformationTemplate", "CPPointOfInterestTemplate"},
                 {"CPSearchTemplate", "CPVoiceControlTemplate"}, {"CPContactTemplate"}),
    "parking": (BASE | {"CPInformationTemplate", "CPPointOfInterestTemplate"},
                {"CPSearchTemplate", "CPVoiceControlTemplate"}, {"CPContactTemplate"}),
    "fueling": (BASE | {"CPInformationTemplate", "CPPointOfInterestTemplate"},
                {"CPSearchTemplate", "CPVoiceControlTemplate"}, {"CPContactTemplate"}),
    "quick-ordering": (BASE | {"CPInformationTemplate", "CPPointOfInterestTemplate"},
                       {"CPVoiceControlTemplate"}, {"CPContactTemplate"}),
    "driving-task": (BASE | {"CPInformationTemplate", "CPPointOfInterestTemplate", "CPVoiceControlTemplate"},
                     set(), set()),
}
HOMEVIEW_CATEGORIES = {"audio", "video"}
PHONE_COPY = re.compile(r'"[^"\n]*\b(iPhone|unlock|on your phone|pick up your phone|open the app on)\b[^"\n]*"', re.I)
NAV_CALL = re.compile(r"\.(setRootTemplate|pushTemplate|presentTemplate|popTemplate|popToRootTemplate|dismissTemplate)\(")


@dataclass
class Finding:
    rule: str
    severity: str  # error | warn | info
    message: str
    location: str
    reference: str


def walk(root: Path, suffixes: tuple[str, ...]) -> list[Path]:
    found = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.name.endswith(suffixes):
            found.append(path)
    return sorted(found)


def load_plist(path: Path) -> dict | None:
    try:
        with path.open("rb") as handle:
            value = plistlib.load(handle)
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def rel(root: Path, path: Path, line: int | None = None) -> str:
    text = str(path.relative_to(root))
    return f"{text}:{line}" if line else text


def deployment_targets(root: Path) -> list[tuple[int, int]]:
    targets = []
    for pbx in walk(root, (".pbxproj",)):
        for match in re.finditer(r"IPHONEOS_DEPLOYMENT_TARGET = (\d+)\.(\d+)", pbx.read_text(errors="ignore")):
            targets.append((int(match.group(1)), int(match.group(2))))
    return targets


def audit(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    entitlement_files = walk(root, (".entitlements", ".entitlements.fragment.plist"))
    plists = [p for p in walk(root, (".plist",)) if p.name == "Info.plist" or p.name.endswith("-Info.plist")]
    pbxprojs = walk(root, (".pbxproj",))
    swift_files = walk(root, (".swift",))
    sources = {path: path.read_text(errors="ignore") for path in swift_files}
    all_swift = "\n".join(sources.values())
    pbx_text = "\n".join(p.read_text(errors="ignore") for p in pbxprojs)

    # --- entitlements -------------------------------------------------------------------------
    categories: set[str] = set()
    for path in entitlement_files:
        data = load_plist(path)
        if data is None:
            findings.append(Finding("entitlements-unreadable", "warn", "Could not parse this entitlements file.",
                                    rel(root, path), "references/entitlements-and-shipping.md"))
            continue
        keys = [k for k, v in data.items() if k.startswith(CARPLAY_PREFIX) and v is True]
        file_categories = {k[len(CARPLAY_PREFIX):] for k in keys}
        categories |= file_categories
        for legacy in LEGACY_KEYS & set(data):
            findings.append(Finding("legacy-entitlement", "warn",
                                    f"{legacy} is deprecated; CarPlay apps use one com.apple.developer.carplay-* key.",
                                    rel(root, path), "references/entitlements-and-shipping.md"))
        if len(file_categories) > 1 and file_categories != COMBINABLE:
            findings.append(Finding(
                "multiple-carplay-entitlements", "error",
                f"{len(file_categories)} CarPlay entitlements in one target ({', '.join(sorted(file_categories))}). "
                "Since iOS 26.3 only charging and fueling may be combined. Apps that play both audio and "
                "video use the audio entitlement alone, with AirPlay video.",
                rel(root, path), "references/entitlements-and-shipping.md § One entitlement"))
        unknown = file_categories - set(ALLOWED)
        for name in sorted(unknown):
            findings.append(Finding("unknown-carplay-entitlement", "warn",
                                    f"{CARPLAY_PREFIX}{name} is not one of the 11 documented CarPlay categories.",
                                    rel(root, path), "references/capability-matrix.md"))

    if not categories:
        if re.search(r"\bimport CarPlay\b", all_swift):
            findings.append(Finding(
                "carplay-without-entitlement", "warn",
                "The code imports CarPlay but no .entitlements file grants a CarPlay category. Without the "
                "granted key in the provisioning profile the car scene never connects.",
                ".", "references/entitlements-and-shipping.md"))
        return findings + widget_checks(root, sources)

    # --- scene wiring -------------------------------------------------------------------------
    plist_texts = {p: p.read_text(errors="ignore") for p in plists}
    has_role = any("CPTemplateApplicationSceneSessionRoleApplication" in t for t in plist_texts.values()) \
        or "CPTemplateApplicationSceneSessionRoleApplication" in pbx_text \
        or re.search(r"\.carTemplateApplication\b|CPTemplateApplicationSceneSessionRoleApplication", all_swift)
    if not has_role:
        findings.append(Finding(
            "no-carplay-scene", "error",
            "A CarPlay entitlement is present but nothing declares or routes a CPTemplateApplicationScene "
            "(Info.plist scene manifest, or configurationForConnecting returning a configuration for "
            ".carTemplateApplication). The car scene will never connect.",
            ".", "references/code.md § Scene routing"))
    for path, text in plist_texts.items():
        data = load_plist(path) or {}
        manifest = data.get("UIApplicationSceneManifest") or {}
        if "CPTemplateApplicationSceneSessionRoleApplication" in json.dumps(manifest) and \
                manifest.get("UIApplicationSupportsMultipleScenes") is False:
            findings.append(Finding(
                "single-scene-manifest", "warn",
                "UIApplicationSupportsMultipleScenes is false in a manifest that declares a CarPlay scene. "
                "Apple's samples set it to true; a manifest copied from a single-scene template is the usual cause.",
                rel(root, path), "references/code.md § Scene routing"))
    for path, text in sources.items():
        for match in re.finditer(r"(?m)^(?P<attrs>(?:\s*@[\w().,: ]+\s*\n)*)\s*(?:final\s+)?class\s+\w+\s*:[^{]*CPTemplateApplicationSceneDelegate", text):
            if "@MainActor" not in match.group("attrs"):
                line = text[:match.start()].count("\n") + 1 + match.group("attrs").count("\n")
                findings.append(Finding(
                    "scene-delegate-isolation", "warn",
                    "The CarPlay scene delegate is not @MainActor. CarPlay templates are main-actor types in the "
                    "iOS 27 SDK, so Swift 6 strict concurrency flags every template call made from it.",
                    rel(root, path, line), "references/code.md § Swift 6"))

    # --- templates against the category ---------------------------------------------------------
    used: dict[str, list[str]] = {}
    for path, text in sources.items():
        for name in ALL_TEMPLATES:
            for match in re.finditer(rf"\b{name}\b", text):
                line = text[:match.start()].count("\n") + 1
                used.setdefault(name, []).append(rel(root, path, line))
    targets = deployment_targets(root)
    lowest = min(targets) if targets else None
    for category in sorted(categories & set(ALLOWED)):
        base, ios27, disputed = ALLOWED[category]
        for name, places in sorted(used.items()):
            if name in base:
                continue
            if name in disputed:
                findings.append(Finding(
                    "template-cell-disputed", "warn",
                    f"{name} in a {category} app: the research members disagree on this cell of Apple's matrix. "
                    "Check the CarPlay Developer Guide table before shipping it.",
                    places[0], "references/capability-matrix.md"))
            elif name in ios27:
                if lowest and lowest < (27, 0) and not re.search(r"#available\(iOS 27", all_swift):
                    findings.append(Finding(
                        "template-needs-ios27", "warn",
                        f"{name} is allowed for {category} apps only from iOS 27, and the deployment target is "
                        f"{lowest[0]}.{lowest[1]} with no iOS 27 availability check in the sources.",
                        places[0], "references/capability-matrix.md"))
            else:
                findings.append(Finding(
                    "template-not-allowed", "error",
                    f"{name} is not permitted for a {category} app. Pushing or presenting it throws at runtime.",
                    places[0], "references/capability-matrix.md"))

    # --- behaviour rules -----------------------------------------------------------------------------
    uses_nowplaying_fw = re.search(r"\bimport NowPlaying\b|\bMediaSession\b", all_swift)
    uses_mediaplayer = re.search(r"\bMPNowPlayingInfoCenter\b|\bMPRemoteCommandCenter\b", all_swift)
    if uses_nowplaying_fw and uses_mediaplayer:
        findings.append(Finding(
            "nowplaying-mixed", "error",
            "The app uses both the NowPlaying framework (MediaSession) and MediaPlayer's "
            "MPNowPlayingInfoCenter/MPRemoteCommandCenter. Apple documents mixing them as undefined behavior; pick one.",
            ".", "references/code.md § Now Playing"))
    if categories & {"audio", "video"} and not (uses_nowplaying_fw or uses_mediaplayer):
        findings.append(Finding(
            "no-now-playing", "warn",
            "A media app with no Now Playing publisher. CPNowPlayingTemplate and the car's controls read the "
            "system Now Playing session, so they will show nothing.",
            ".", "references/code.md § Now Playing"))
    plays_video = re.search(r"\.video\b|isVideo|AVPlayerViewController|VideoPlayer\(", all_swift)
    if "audio" in categories and plays_video and not re.search(r"allowsExternalPlayback\s*=\s*true", all_swift):
        findings.append(Finding(
            "audio-app-video-without-airplay", "warn",
            "An audio-entitlement app that appears to play video but never enables AirPlay external playback. "
            "Apple's audio category requires AirPlay video for video with an audio component.",
            ".", "references/entitlements-and-shipping.md § One entitlement"))
    if "voice-based-conversation" in categories:
        if "CPVoiceControlTemplate" not in used:
            findings.append(Finding(
                "conversation-without-voice-template", "error",
                "A voice-based conversational app that never shows CPVoiceControlTemplate. The template must be on "
                "screen whenever the microphone is open, and voice must be the primary modality from launch.",
                ".", "references/design-rules.md § Voice"))
        if not re.search(r"\.playAndRecord\b", all_swift):
            findings.append(Finding(
                "conversation-audio-session", "warn",
                "No .playAndRecord audio session in a conversational app. Apple's guidance is .playAndRecord, "
                "default mode, no mixing, held only while voice is in use.",
                ".", "references/code.md § Voice"))
    if "CPTabBarTemplate" in used and "maximumTabCount" not in all_swift:
        findings.append(Finding(
            "tab-count-hardcoded", "warn",
            "CPTabBarTemplate without reading CPTabBarTemplate.maximumTabCount. The limit depends on the "
            "entitlement (4 for audio, 5 for the rest today) and Apple says it may change.",
            used["CPTabBarTemplate"][0], "references/design-rules.md § Limits"))
    if "CPListTemplate" in used and "maximumItemCount" not in all_swift:
        findings.append(Finding(
            "list-limit-unread", "info",
            "CPListTemplate without reading CPListTemplate.maximumItemCount. Some cars show 12 rows; items "
            "past the limit are dropped.",
            used["CPListTemplate"][0], "references/design-rules.md § Limits"))

    carplay_files = {p: t for p, t in sources.items() if re.search(r"\bimport CarPlay\b", t)}
    for path, text in carplay_files.items():
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            if NAV_CALL.search(line) and "await" not in line and "completion" not in line and "{" not in line.split(NAV_CALL.search(line).group(0), 1)[1]:
                findings.append(Finding(
                    "navigation-without-completion", "warn",
                    "Template navigation without a completion handler or await. Apple deprecated these forms; "
                    "a failed navigation then throws an exception instead of reporting an error.",
                    rel(root, path, lineno), "references/code.md § Navigation"))
            copy = PHONE_COPY.search(line)
            if copy:
                findings.append(Finding(
                    "copy-sends-driver-to-phone", "warn",
                    f"Car-facing text mentions the phone: {copy.group(0)}. CarPlay must never ask the driver to "
                    "use the iPhone; App Review rejects it.",
                    rel(root, path, lineno), "references/design-rules.md § Phone"))
    locked = re.compile(r"kSecAttrAccessibleWhenUnlocked\b|NSFileProtectionComplete\b|\.completeFileProtection\b(?!Until)")
    for path, text in sources.items():
        for match in locked.finditer(text):
            line = text[:match.start()].count("\n") + 1
            findings.append(Finding(
                "locked-phone-data", "warn",
                f"{match.group(0)} data is unreadable while the iPhone is locked, which is how CarPlay and "
                "HomeView usually run the app. Use an after-first-unlock class for anything the car needs.",
                rel(root, path, line), "references/design-rules.md § Phone"))

    if not categories & HOMEVIEW_CATEGORIES:
        findings.append(Finding(
            "homeview-widget-only", "info",
            f"Category {', '.join(sorted(categories))} does not appear on HomeView. The app's HomeView surface is "
            "a system-small widget from the paired iPhone.",
            ".", "references/homeview.md"))
    return findings + widget_checks(root, sources)


def widget_checks(root: Path, sources: dict[Path, str]) -> list[Finding]:
    findings = []
    for path, text in sources.items():
        if not re.search(r":\s*Widget\b", text) or "systemSmall" not in text:
            continue
        if "containerBackground(" not in text:
            findings.append(Finding(
                "widget-background", "warn",
                "A system-small widget without .containerBackground(for: .widget). CarPlay, StandBy and "
                "HomeView's Modular face remove the background, so the system needs to know which view it is.",
                rel(root, path), "references/design-rules.md § Widgets"))
        if re.search(r"containerBackgroundRemovable\(\s*false\s*\)", text):
            findings.append(Finding(
                "widget-background-fixed", "info",
                "containerBackgroundRemovable(false) keeps this widget out of CarPlay, StandBy and HomeView's "
                "Modular face.",
                rel(root, path), "references/design-rules.md § Widgets"))
    return findings


def report(findings: list[Finding], as_json: bool) -> None:
    if as_json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
        return
    order = {"error": 0, "warn": 1, "info": 2}
    for f in sorted(findings, key=lambda f: (order[f.severity], f.rule, f.location)):
        print(f"{f.severity.upper():5} {f.rule}  {f.location}\n      {f.message}\n      see {f.reference}")
    counts = {s: sum(1 for f in findings if f.severity == s) for s in order}
    print(f"home_audit: {counts['error']} error(s), {counts['warn']} warning(s), {counts['info']} note(s)")


def self_test() -> int:
    skill = Path(__file__).resolve().parent.parent
    fixtures = skill / "evals" / "fixtures"
    failures = 0
    cases = sorted(p for p in fixtures.iterdir() if p.is_dir())
    with tempfile.TemporaryDirectory() as tmp:
        # The bundled templates are the clean case: they must pass their own audit.
        clean = Path(tmp) / "templates-clean"
        shutil.copytree(skill / "templates", clean)
        cases_and_expect = [(clean, {"error": [], "warn": []})]
        for case in cases:
            cases_and_expect.append((case, json.loads((case / "expected.json").read_text())))
        for case, expect in cases_and_expect:
            found = audit(case)
            by_sev = {s: sorted({f.rule for f in found if f.severity == s}) for s in ("error", "warn")}
            ok = all(sorted(expect.get(s, [])) == by_sev[s] for s in ("error", "warn"))
            failures += not ok
            print(f"{'PASS' if ok else 'FAIL'} {case.name}: errors={by_sev['error']} warns={by_sev['warn']}")
            if not ok:
                print(f"      expected errors={sorted(expect.get('error', []))} warns={sorted(expect.get('warn', []))}")
    print(f"self-test: {len(cases_and_expect) - failures}/{len(cases_and_expect)} passed")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.project or not args.project.is_dir():
        parser.error("give a project directory")
    findings = audit(args.project.resolve())
    report(findings, args.json)
    if any(f.severity == "error" for f in findings):
        return 1
    if args.strict and any(f.severity == "warn" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
