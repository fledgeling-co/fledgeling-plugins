#!/usr/bin/env python3
"""Copy the iPhone Duo fold module and layout helpers into a React Native / Expo app.

    python3 install_templates.py <app-root>              # module + hooks + components (adapt an app)
    python3 install_templates.py <app-root> --starter    # also starter screens (a new Expo Router app)
    python3 install_templates.py <app-root> --dry-run    # print what would be written
    python3 install_templates.py --self-test

It never overwrites an existing file: a path that already exists is reported as skipped, so an app
that already has a `lib/layout.ts` keeps it and the agent merges by hand. Import paths in the copied
files use the `~/` alias and are rewritten to the app's own root alias, read from tsconfig.json
(`@/` in a fresh create-expo-app); --alias overrides it. Tests copy only with --with-tests, because
they need @testing-library/react-native and jest-expo, which a fresh app does not have.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "..", "templates")

CORE = [
    "modules/duo-fold/package.json",
    "modules/duo-fold/expo-module.config.json",
    "modules/duo-fold/index.ts",
    "modules/duo-fold/ios/DuoFold.podspec",
    "modules/duo-fold/ios/DuoFoldModule.swift",
    "lib/fold.ts",
    "lib/layout.ts",
    "lib/readable.ts",
    "components/DetailPaneLayout.tsx",
    "components/FoldColumns.tsx",
    "components/ScreenTitle.tsx",
]
TESTS = [
    "lib/__tests__/fold.test.ts",
    "components/__tests__/detailPaneLayout.test.tsx",
]
STARTER = [
    "starter/app/_layout.tsx",
    "starter/app/index.tsx",
    "starter/app/(tabs)/_layout.tsx",
    "starter/app/(tabs)/items/_layout.tsx",
    "starter/app/(tabs)/items/index.tsx",
    "starter/app/item/[id].tsx",
]


def detect_alias(app_root: str) -> tuple[str, str]:
    """The app's root import alias and the directory it maps to, from tsconfig paths.

    ("@/*": ["./src/*"]) -> ("@/", "src"); ("~/*": ["./*"]) -> ("~/", ""). Defaults to ("~/", "").
    """
    try:
        raw = open(os.path.join(app_root, "tsconfig.json"), encoding="utf-8").read()
        cfg = json.loads(re.sub(r"//.*", "", raw))
    except (OSError, ValueError):
        return "~/", ""
    for key, targets in (cfg.get("compilerOptions", {}).get("paths") or {}).items():
        if not key.endswith("/*") or key.count("/") != 1 or not targets:
            continue
        target = targets[0].rstrip("*").strip("/")
        target = "" if target in (".", "") else target.removeprefix("./")
        return key[:-1], target
    return "~/", ""


def plan(app_root: str, starter: bool, tests: bool = False, base: str = ""):
    """Native modules stay at the project root (autolinking reads ./modules); TypeScript goes under
    the alias's directory, and routes under that directory's app/ when it has one (expo-router reads
    src/app before app)."""
    out = []
    for rel in CORE + (STARTER if starter else []) + (TESTS if tests else []):
        src = os.path.join(TEMPLATES, rel)
        dest_rel = rel[len("starter/"):] if rel.startswith("starter/") else rel
        if not dest_rel.startswith(("modules/", "plugins/")) and base:
            dest_rel = os.path.join(base, dest_rel)
        out.append((src, os.path.join(app_root, dest_rel), dest_rel))
    return out


def install(app_root: str, starter: bool, alias: str | None, dry: bool, tests: bool = False) -> int:
    if not os.path.isfile(os.path.join(app_root, "package.json")):
        print(f"not an app root (no package.json): {app_root}")
        return 2
    detected, base = detect_alias(app_root)
    alias = alias or detected
    print(f"import alias: {alias} -> ./{base or '.'}")
    written = skipped = 0
    for src, dest, rel in plan(app_root, starter, tests, base):
        if not os.path.isfile(src):
            print(f"missing template: {src}")
            return 2
        if os.path.exists(dest) and f"{os.sep}starter{os.sep}" in src:
            # --starter is for a fresh create-expo-app; its routes are replaced, not merged. The
            # originals go to .duo-craft-backup/ so nothing the user wrote is lost.
            backup = os.path.join(app_root, ".duo-craft-backup", os.path.relpath(dest, app_root))
            print(f"replace {rel} (original kept in .duo-craft-backup/)")
            if not dry:
                os.makedirs(os.path.dirname(backup), exist_ok=True)
                shutil.move(dest, backup)
        elif os.path.exists(dest):
            print(f"skip   {rel} (exists — merge by hand)")
            skipped += 1
            continue
        print(f"write  {rel}")
        written += 1
        if dry:
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if rel.endswith((".ts", ".tsx")) and not rel.startswith(("modules/", "plugins/")):
            body = open(src, encoding="utf-8").read().replace("'~/", f"'{alias}")
            # The native module stays at the project root; point each relative import at it from
            # wherever this file landed (lib/ at the root, or src/lib/ under an alias directory).
            to_modules = os.path.relpath(os.path.join(app_root, "modules"), os.path.dirname(dest))
            body = re.sub(r"'(\.\./)+modules/", f"'{to_modules}/", body)
            open(dest, "w", encoding="utf-8").write(body)
        else:
            shutil.copyfile(src, dest)
    print(f"{written} written, {skipped} skipped{' (dry run)' if dry else ''}")
    register_scene_plugin(app_root, dry)
    if starter:
        unlock_orientation(app_root, dry)
    if written and not dry:
        print("next: npx expo prebuild -p ios (if ios/ is generated) && cd ios && pod install, "
              "then build with DEVELOPER_DIR pointing at Xcode 27.1")
    return 0


SCENE_PLUGIN = ["expo-build-properties", {"ios": {"enableSceneSupport": True}}]
BUILD_PROPERTIES_RANGE = "~57.0.22"     # the first expo-build-properties with ios.enableSceneSupport


def expo_version(app_root: str) -> tuple[int, int, int] | None:
    try:
        v = json.load(open(os.path.join(app_root, "node_modules", "expo", "package.json")))["version"]
        return tuple(int(x) for x in re.findall(r"\d+", v)[:3])  # type: ignore[return-value]
    except (OSError, ValueError, KeyError):
        return None


def register_scene_plugin(app_root: str, dry: bool) -> None:
    """Below Expo SDK 58 the template has no scene delegate, and an iOS 27 SDK build crashes at
    launch. Expo's own opt-in for SDK 57 is expo-build-properties' ios.enableSceneSupport (it needs
    expo >= 57.0.23); SDK 58+ prebuild adopts scenes itself."""
    ver = expo_version(app_root)
    if ver is None:
        print("scene lifecycle: expo not installed yet; on SDK 57 add expo-build-properties with "
              '{"ios": {"enableSceneSupport": true}} to app.json plugins')
        return
    if ver[0] >= 58:
        return
    if ver[0] < 57 or ver < (57, 0, 23):
        print(f"scene lifecycle: Expo {'.'.join(map(str, ver))} cannot adopt scenes; upgrade to SDK 58, "
              "or to expo 57.0.23 or later and rerun this script")
        return
    path = os.path.join(app_root, "app.json")
    try:
        cfg = json.load(open(path))
    except (OSError, ValueError):
        print('scene lifecycle: no app.json; add expo-build-properties with {"ios": {"enableSceneSupport": true}}')
        return
    plugins = cfg.setdefault("expo", {}).setdefault("plugins", [])
    entry = next((p for p in plugins if p == "expo-build-properties" or
                  (isinstance(p, list) and p and p[0] == "expo-build-properties")), None)
    if isinstance(entry, list) and len(entry) > 1 and (entry[1].get("ios") or {}).get("enableSceneSupport"):
        return
    print("scene lifecycle: Expo SDK 57 has no scene delegate; enabling expo-build-properties "
          "ios.enableSceneSupport in app.json")
    if dry:
        return
    if entry is None:
        plugins.append(SCENE_PLUGIN)
    elif entry == "expo-build-properties":
        plugins[plugins.index(entry)] = SCENE_PLUGIN
    else:
        if len(entry) == 1:
            entry.append({})
        entry[1].setdefault("ios", {})["enableSceneSupport"] = True
    open(path, "w").write(json.dumps(cfg, indent=2) + "\n")
    pkg_path = os.path.join(app_root, "package.json")
    pkg = json.load(open(pkg_path))
    deps = pkg.setdefault("dependencies", {})
    if "expo-build-properties" not in deps:
        deps["expo-build-properties"] = BUILD_PROPERTIES_RANGE
        print(f"scene lifecycle: added expo-build-properties {BUILD_PROPERTIES_RANGE} to package.json; "
              "run npx expo install expo-build-properties")
    # The guard that keeps it fixed: fails when the opt-in leaves app.json, when expo drops below
    # 57.0.23, or when a generated ios/ still has the old window start (a black screen).
    check = os.path.join(app_root, "scripts", "check-scene-lifecycle.mjs")
    if not os.path.exists(check):
        os.makedirs(os.path.dirname(check), exist_ok=True)
        shutil.copyfile(os.path.join(TEMPLATES, "scripts", "check-scene-lifecycle.mjs"), check)
    scripts = pkg.setdefault("scripts", {})
    scripts.setdefault("check:scenes", "node scripts/check-scene-lifecycle.mjs")
    for name in ("ios", "prebuild"):
        cmd = scripts.get(name)
        if cmd and "check:scenes" not in cmd:
            scripts[name] = f"npm run check:scenes && {cmd}"
    open(pkg_path, "w").write(json.dumps(pkg, indent=2) + "\n")
    print("scene lifecycle: scripts/check-scene-lifecycle.mjs added and run before the ios script "
          "(npm run check:scenes); add it to CI as well")


def unlock_orientation(app_root: str, dry: bool) -> None:
    """create-expo-app locks portrait. The outer display honours it and the inner display rotates
    anyway, so a new Duo app takes every orientation and lays out for the width it gets."""
    path = os.path.join(app_root, "app.json")
    try:
        cfg = json.load(open(path))
    except (OSError, ValueError):
        return
    if cfg.get("expo", {}).get("orientation") != "portrait":
        return
    print('orientation: app.json locked portrait; setting "default" so every display can rotate')
    if not dry:
        cfg["expo"]["orientation"] = "default"
        open(path, "w").write(json.dumps(cfg, indent=2) + "\n")


def self_test() -> int:
    ok = True
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "package.json"), "w").write("{}")
        open(os.path.join(d, "app.json"), "w").write('{"expo":{"orientation":"portrait"}}')
        os.makedirs(os.path.join(d, "lib"))
        open(os.path.join(d, "lib", "layout.ts"), "w").write("// the app's own")
        os.makedirs(os.path.join(d, "src", "app"))
        open(os.path.join(d, "src", "app", "_layout.tsx"), "w").write("// the template's own")
        open(os.path.join(d, "tsconfig.json"), "w").write('{"compilerOptions":{"paths":{"@/*":["./src/*"]}}}')
        if install(d, starter=True, alias=None, dry=False) != 0:
            ok = False
        os.makedirs(os.path.join(d, "src", "lib"), exist_ok=True)
        if open(os.path.join(d, "lib", "layout.ts")).read() != "// the app's own":
            print("self-test: overwrote an existing file"); ok = False
        if json.load(open(os.path.join(d, "app.json")))["expo"]["orientation"] != "default":
            print("self-test: starter left orientation locked"); ok = False
        if not os.path.isfile(os.path.join(d, "modules", "duo-fold", "ios", "DuoFoldModule.swift")):
            print("self-test: module not copied"); ok = False
        if "Stack" not in open(os.path.join(d, "src", "app", "_layout.tsx")).read() or \
                open(os.path.join(d, ".duo-craft-backup", "src", "app", "_layout.tsx")).read() != "// the template's own":
            print("self-test: starter did not replace the root layout and keep the original"); ok = False
        if not os.path.isfile(os.path.join(d, "src", "app", "(tabs)", "items", "index.tsx")):
            print("self-test: starter not copied"); ok = False
        if "'@/lib/fold'" not in open(os.path.join(d, "src", "components", "FoldColumns.tsx")).read():
            print("self-test: alias not rewritten"); ok = False
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "package.json"), "w").write("{}")
        open(os.path.join(d, "app.json"), "w").write('{"expo": {"plugins": ["expo-router"]}}')
        os.makedirs(os.path.join(d, "node_modules", "expo"))
        open(os.path.join(d, "node_modules", "expo", "package.json"), "w").write('{"version": "57.0.27"}')
        install(d, starter=False, alias=None, dry=False)
        if SCENE_PLUGIN not in json.load(open(os.path.join(d, "app.json")))["expo"]["plugins"]:
            print("self-test: SDK 57 app did not get scene support"); ok = False
        pkg = json.load(open(os.path.join(d, "package.json")))
        if "expo-build-properties" not in pkg.get("dependencies", {}):
            print("self-test: SDK 57 app did not get expo-build-properties"); ok = False
        if not os.path.isfile(os.path.join(d, "scripts", "check-scene-lifecycle.mjs")) or \
                pkg.get("scripts", {}).get("check:scenes") != "node scripts/check-scene-lifecycle.mjs":
            print("self-test: SDK 57 app did not get the scene check"); ok = False
        # an existing expo-build-properties entry is merged into, not duplicated
        open(os.path.join(d, "app.json"), "w").write('{"expo": {"plugins": [["expo-build-properties", {"ios": {"deploymentTarget": "16.0"}}]]}}')
        install(d, starter=False, alias=None, dry=False)
        plugins = json.load(open(os.path.join(d, "app.json")))["expo"]["plugins"]
        if plugins != [["expo-build-properties", {"ios": {"deploymentTarget": "16.0", "enableSceneSupport": True}}]]:
            print(f"self-test: did not merge into an existing entry: {plugins}"); ok = False
        open(os.path.join(d, "node_modules", "expo", "package.json"), "w").write('{"version": "57.0.12"}')
        open(os.path.join(d, "app.json"), "w").write('{"expo": {"plugins": []}}')
        install(d, starter=False, alias=None, dry=False)
        if json.load(open(os.path.join(d, "app.json")))["expo"]["plugins"]:
            print("self-test: enabled scene support on an expo patch too old for it"); ok = False
        open(os.path.join(d, "node_modules", "expo", "package.json"), "w").write('{"version": "58.0.7"}')
        open(os.path.join(d, "app.json"), "w").write('{"expo": {"plugins": []}}')
        install(d, starter=False, alias=None, dry=False)
        if json.load(open(os.path.join(d, "app.json")))["expo"]["plugins"]:
            print("self-test: SDK 58 app got the scene plugin it does not need"); ok = False
    with tempfile.TemporaryDirectory() as d:
        if install(d, starter=False, alias=None, dry=True) != 2:
            print("self-test: accepted a directory with no package.json"); ok = False
    print("self-test: pass" if ok else "self-test: FAIL")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    alias = None
    if "--alias" in argv:
        alias = argv[argv.index("--alias") + 1]
        args = [a for a in args if a != alias]
    if not args:
        print(__doc__)
        return 2
    return install(os.path.abspath(args[0]), "--starter" in argv, alias, "--dry-run" in argv,
                   "--with-tests" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
