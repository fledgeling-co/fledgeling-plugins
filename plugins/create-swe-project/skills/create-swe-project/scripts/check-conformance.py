#!/usr/bin/env python3
"""Fail when references/team-files-conformance.md and the bundled specs disagree.

Three checks, each a reason to exit 1:
  1. A numbered section of NEW_PROJECT_BEST_PRACTICES.md ("## N.") or of
     CODING_PRACTICES.md ("## N." and "### 6.N") has no row in the map.
  2. The map has a row for a section the specs no longer contain.
  3. A backticked `templates/...` or `scripts/...` path in the map does not exist.

Run after scripts/sync-team-files.sh and after any template move.
Usage: check-conformance.py   (no arguments; paths resolve from this file)
"""
import pathlib
import re
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
SPECS = SKILL / "references" / "team-files"
MAP = SKILL / "references" / "team-files-conformance.md"


def sections(path: pathlib.Path, prefix: str, sub: str | None) -> set[str]:
    text = path.read_text()
    found = {f"{prefix} §{m}" for m in re.findall(r"^## (\d+)\.", text, re.M)}
    if sub:
        children = {f"{prefix} §{m}" for m in re.findall(rf"^### ({sub}\.\d+)\b", text, re.M)}
        if children:  # the parent heading is only a container for its numbered children
            found = (found - {f"{prefix} §{sub}"}) | children
    return found


def main() -> int:
    expected = sections(SPECS / "NEW_PROJECT_BEST_PRACTICES.md", "BP", None)
    expected |= sections(SPECS / "CODING_PRACTICES.md", "CP", "6")
    text = MAP.read_text()
    rows = set(re.findall(r"^\| ((?:BP|CP) §[\d.]+) \|", text, re.M))
    problems = []
    for missing in sorted(expected - rows):
        problems.append(f"no row for {missing}")
    for stale in sorted(rows - expected):
        problems.append(f"row for {stale}, which the specs no longer contain")
    for cited in sorted(set(re.findall(r"`((?:templates|scripts)/[^`\s]+)`", text))):
        if not (SKILL / cited.rstrip("/")).exists():
            problems.append(f"cited path does not exist: {cited}")
    for p in problems:
        print(f"check-conformance: {p}", file=sys.stderr)
    if problems:
        return 1
    print(f"check-conformance: {len(expected)} sections mapped, every cited path exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
