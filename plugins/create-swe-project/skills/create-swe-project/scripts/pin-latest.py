#!/usr/bin/env python3
"""Rewrite every "latest" specifier in a scaffolded project to the range it resolved.

Templates float versions so a fresh project gets current releases, but a committed
package.json that says "latest" never says which release it means (BP §2: let the
install write ^x.y.z; CP §4 A03: no `latest` in production). After the first,
cooldown-respecting install, this reads `pnpm list -r --json --depth 0` and writes
the resolved version back as a caret range: into each workspace package.json, and
into the pnpm-workspace.yaml catalog. A prerelease resolves to its exact version.

Usage: pin-latest.py <project-dir> <pnpm-list.json>
Exits non-zero, writing nothing, if a "latest" specifier has no resolved version.
"""
import json
import pathlib
import re
import sys


def caret(version: str) -> str:
    return version if "-" in version else f"^{version}"


def main() -> int:
    root, listing = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    projects = json.loads(listing.read_text())
    resolved: dict[str, dict[str, str]] = {}  # project path -> {dep: version}
    anywhere: dict[str, str] = {}             # dep -> version, for catalog entries
    for proj in projects:
        deps: dict[str, str] = {}
        for group in ("dependencies", "devDependencies", "optionalDependencies"):
            for name, info in (proj.get(group) or {}).items():
                version = info.get("version", "")
                if re.match(r"^\d", version):  # skip link:/workspace: entries
                    deps[name] = version
                    anywhere.setdefault(name, version)
        resolved[str(pathlib.Path(proj["path"]).resolve())] = deps

    edits: list[tuple[pathlib.Path, str]] = []
    missing: list[str] = []
    for pj in [root / "package.json", *root.glob("apps/*/package.json"), *root.glob("packages/*/package.json")]:
        data = json.loads(pj.read_text())
        versions = resolved.get(str(pj.parent.resolve()), {})
        changed = False
        for group in ("dependencies", "devDependencies"):
            for name, spec in (data.get(group) or {}).items():
                if spec != "latest":
                    continue
                if name not in versions:
                    missing.append(f"{pj.relative_to(root)}: {name}")
                    continue
                data[group][name] = caret(versions[name])
                changed = True
        if changed:
            edits.append((pj, json.dumps(data, indent=2) + "\n"))

    ws = root / "pnpm-workspace.yaml"
    lines = ws.read_text().splitlines(keepends=True)
    in_catalog = False
    for i, line in enumerate(lines):
        if re.match(r"^catalog:\s*$", line):
            in_catalog = True
            continue
        if in_catalog and line.strip() and not line.startswith(" "):
            in_catalog = False
        m = re.match(r'^(\s+)("?)([^":]+)\2:\s*"latest"\s*$', line) if in_catalog else None
        if not m:
            continue
        name = m.group(3)
        if name not in anywhere:
            # A catalog entry no workspace member uses resolves to nothing; drop it
            # rather than commit a range nobody installed.
            lines[i] = ""
            continue
        lines[i] = f'{m.group(1)}"{name}": "{caret(anywhere[name])}"\n'
    edits.append((ws, "".join(lines)))

    if missing:
        print("pin-latest: no resolved version for: " + ", ".join(missing), file=sys.stderr)
        return 1
    for path, text in edits:
        path.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
