#!/usr/bin/env python3
"""install_pointer.py — wire a finished gemini.md into its skill, idempotently.

A gemini.md nothing points at is a file nobody reads. The pointer is the whole
delivery mechanism, and getting it in place involves four edits in three files
that are easy to do inconsistently by hand: insert the conditional block above a
named heading in SKILL.md, bump the plugin version, and sync the same version
into the marketplace manifest (which pins it separately, so an unsynced bump
publishes the old copy).

Usage:
    install_pointer.py <path-to-SKILL.md> --before "## Heading" --summary "..."
                       [--bump minor|patch|none] [--dry-run]

    --before    the heading the pointer is inserted above. The pointer belongs
                near the top, before the first substantive section, because a
                model that has already started working will not go back for it.
    --summary   one sentence naming what this skill's gemini.md actually changes.
                Generic pointers get skipped; a specific one earns its read.
    --bump      version bump for plugin.json + marketplace.json (default minor).

Idempotent: running twice does not duplicate the pointer or double-bump.

Exit codes: 0 done · 1 refused (missing gemini.md, heading not found) · 2 usage
stdlib only.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

MARKER = "Running as a Gemini model?"

TEMPLATE = (
    "**{marker}** Read `gemini.md` in this directory first, then follow this file "
    "with the overrides it names. {summary} Other models skip it.\n\n"
)


def find_plugin_root(skill_md: pathlib.Path) -> pathlib.Path | None:
    for p in skill_md.parents:
        if (p / ".claude-plugin" / "plugin.json").is_file():
            return p
    return None


def find_marketplace(plugin_root: pathlib.Path) -> pathlib.Path | None:
    for p in plugin_root.parents:
        m = p / ".claude-plugin" / "marketplace.json"
        if m.is_file():
            return m
    return None


def bump(version: str, kind: str) -> str:
    parts = (version.split(".") + ["0", "0", "0"])[:3]
    try:
        major, minor, patch = (int(x) for x in parts)
    except ValueError:
        return version
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    if kind == "patch":
        return f"{major}.{minor}.{patch + 1}"
    return version


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    ap.add_argument("--before", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--bump", choices=("minor", "patch", "none"), default="minor")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    skill_md = pathlib.Path(a.skill)
    if not skill_md.is_file():
        print(f"no such file: {skill_md}", file=sys.stderr)
        return 2

    gemini = skill_md.parent / "gemini.md"
    if not gemini.is_file():
        print(f"refusing: no gemini.md beside {skill_md.name}. Write the file "
              f"before pointing at it.", file=sys.stderr)
        return 1

    text = skill_md.read_text(encoding="utf-8")
    actions: list[str] = []
    changed = False

    if MARKER in text:
        actions.append(f"pointer already present in {skill_md.name} — left alone")
    else:
        if a.before not in text:
            print(f"refusing: heading {a.before!r} not found in {skill_md.name}.\n"
                  f"Pass a heading that exists; the pointer must land above a real "
                  f"section, not at the end.", file=sys.stderr)
            return 1
        summary = a.summary.strip()
        if not summary.endswith((".", "!", "?")):
            summary += "."
        block = TEMPLATE.format(marker=MARKER, summary=summary)
        text = text.replace(a.before, block + a.before, 1)
        actions.append(f"pointer inserted above {a.before!r}")
        changed = True
        if not a.dry_run:
            skill_md.write_text(text, encoding="utf-8")

    # ── version, in both places that pin it ──────────────────────────────────
    # Only when something actually changed. A re-run that finds the pointer
    # already in place must be a no-op: bumping anyway publishes a new version
    # whose diff is empty, and doing it twice loses track of which version
    # carried the file.
    root = find_plugin_root(skill_md)
    if not changed:
        actions.append("nothing changed — version left alone")
    elif root is None:
        actions.append("no plugin.json found — version not bumped")
    elif a.bump == "none":
        actions.append("version bump skipped (--bump none)")
    else:
        pj = root / ".claude-plugin" / "plugin.json"
        raw = pj.read_text(encoding="utf-8")
        cur = json.loads(raw).get("version", "0.0.0")
        new = bump(cur, a.bump)
        name = json.loads(raw).get("name", root.name)
        if not a.dry_run:
            pj.write_text(raw.replace(f'"{cur}"', f'"{new}"', 1), encoding="utf-8")
        actions.append(f"plugin.json {cur} -> {new}")

        mp = find_marketplace(root)
        if mp is None:
            actions.append("no marketplace.json found — nothing to sync")
        else:
            mraw = mp.read_text(encoding="utf-8")
            pat = re.compile(
                r'("name":\s*"%s"[^}]*?"version":\s*")%s(")' % (re.escape(name),
                                                                re.escape(cur)),
                re.S)
            if pat.search(mraw):
                if not a.dry_run:
                    mp.write_text(pat.sub(rf"\g<1>{new}\g<2>", mraw, count=1),
                                  encoding="utf-8")
                actions.append(f"marketplace.json {name} {cur} -> {new}")
            elif f'"{new}"' in mraw:
                actions.append("marketplace.json already at the new version")
            else:
                actions.append("WARNING: marketplace.json entry not matched — sync "
                               "it by hand, or it will publish the old version")

    prefix = "[dry-run] " if a.dry_run else ""
    for line in actions:
        print(prefix + line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
