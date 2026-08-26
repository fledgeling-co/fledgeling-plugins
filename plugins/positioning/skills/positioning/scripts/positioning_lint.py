#!/usr/bin/env python3
"""Deterministic gate over a rendered positioning report suite.

Checks the things the predecessor skill asked for in prose and had no way to
enforce: that the territories are actually distinct, that no deliverable leads
with breadth, that every figure carries a source, that the ERRC gives something
up, and that the HTML ships without a live dependency or a motionless page.

Exit 0 clean, 1 with errors. Warnings never fail the run.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SUITE = {
    "00-decision.md": "the recommendation",
    "40-evidence-register.md": "the claim register",
    "50-product-truth.md": "the truth table",
    "70-research-decision.md": "what was bought",
    "80-pre-commitment-tests.md": "what to test before betting",
}

BREADTH_BANS = [
    r"\ball[\s\-]?in[\s\-]?one\b",
    r"\bevery\w*[\s\-]app\b",
    r"\bone[\s\-]stop[\s\-]shop\b",
    r"\bthe only tool you(?:'| wi)ll ever need\b",
    r"\bswiss[\s\-]army[\s\-]knife\b",
]

# Words that read as an owned word and are not one: uncontestable, so unloseable.
ABSTRACT_WORDS = {
    "clarity", "velocity", "trust", "intelligence", "simplicity", "power",
    "innovation", "efficiency", "quality", "excellence", "seamless",
    "productivity", "insight", "agility", "empowerment", "synergy",
}

# An Eliminate row that eliminates nothing.
EMPTY_ELIMINATE = [
    r"unnecessary complexity", r"\bcomplexity\b\s*$", r"\bbloat\b\s*$",
    r"friction", r"\bwaste\b\s*$", r"manual work",
]

TERRITORY_SECTIONS = [
    "1 · The position", "2 · Who it is for", "3 · Dunford",
    "4 · The word and the enemy", "5 · Category and naming",
    "6 · Blue Ocean", "7 · Message architecture", "8 · Objections",
    "9 · Framework scorecard", "10 · Evidence fit",
]

# A figure that a reader would act on. Bare years and list indices excluded.
FIGURE = re.compile(
    r"(?<![\w.$])(?:\$\s?\d[\d,]*(?:\.\d+)?\s?(?:[kmbt]|bn|m|k)?"
    r"|\d[\d,]*(?:\.\d+)?\s?%"
    r"|\d[\d,]*(?:\.\d+)?\s?(?:x|×)\b)",
    re.I,
)
BINDING = re.compile(r"\[(?:[CT]-[\w.\-]+)\]")
ESTIMATE = re.compile(r"<ESTIMATE|\bestimate[ds]?\b|<MISSING_DATA|<CONFIDENCE:LOW|<INFERENCE",
                      re.I)
PLACEHOLDER = re.compile(r"\{\{[A-Z_0-9]+\}\}")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checked: dict[str, int] = {}

    def fail(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    def ran(self, name: str, population: int) -> None:
        self.checked[name] = self.checked.get(name, 0) + population


def field(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, re.I | re.M)
    return m.group(1).strip().strip("*`\"'.,") if m else None


def check_suite_present(root: Path, r: Report) -> None:
    r.ran("suite files", len(SUITE))
    for name, what in SUITE.items():
        if not (root / name).exists():
            r.fail(name, f"missing from the suite ({what})")


def check_placeholders(files: list[Path], root: Path, r: Report) -> None:
    r.ran("files scanned for unfilled placeholders", len(files))
    for f in files:
        left = set(PLACEHOLDER.findall(f.read_text()))
        if left:
            shown = ", ".join(sorted(left)[:4])
            r.fail(f.relative_to(root).as_posix(),
                   f"{len(left)} template placeholder(s) never filled: {shown}")


def check_breadth(files: list[Path], root: Path, r: Report) -> None:
    r.ran("files scanned for breadth-led framing", len(files))
    for f in files:
        text = f.read_text()
        for i, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith(">") and "Never" in line:
                continue
            for pat in BREADTH_BANS:
                if re.search(pat, line, re.I) and "Never" not in line and "never" not in line:
                    r.fail(f"{f.relative_to(root).as_posix()}:{i}",
                           f"breadth-led framing: {re.search(pat, line, re.I).group(0)!r}")


def check_figures(files: list[Path], root: Path, r: Report) -> None:
    total = 0
    for f in files:
        if f.name.startswith(("40-", "70-")):
            continue  # the registers ARE the sourcing; every row is a citation
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if line.lstrip().startswith(("|---", "```", "<!--")):
                continue
            figs = FIGURE.findall(line)
            if not figs:
                continue
            total += len(figs)
            if BINDING.search(line) or ESTIMATE.search(line):
                continue
            r.fail(f"{f.relative_to(root).as_posix()}:{i}",
                   f"figure {figs[0]!r} carries no claim id and is not marked an estimate")
    r.ran("figures checked for provenance", total)


def parse_territory(path: Path) -> dict[str, str | None]:
    text = path.read_text()
    return {
        "word": field(text, r"^\s*[-*]\s*\*\*Own:\*\*\s*\*?\*?`?([^`*\n—]+)"),
        "enemy": field(text, r"^\s*[-*]\s*\*\*Enemy:\*\*\s*\*?\*?([^*\n—]+)"),
        "category": field(text, r"^\s*\*\*Adopt:\*\*\s*(.+)$"),
        "beachhead": field(text, r"^\s*\*\*Beachhead:\*\*\s*(.+?)(?:\s*`\[|$)"),
        "eliminate": field(text, r"^\|\s*\*\*Eliminate\*\*\s*\|\s*([^|]+)\|"),
        "falsifier": field(text, r"^\s*[-*]\s*\*\*What would falsify this territory:\*\*\s*(.+)$"),
        "_text": text,
    }


def check_territories(terrs: dict[str, dict], r: Report) -> None:
    r.ran("territory files", len(terrs))
    if len(terrs) < 2:
        r.warn("territories", f"{len(terrs)} found; a shortlist of one is a recommendation, "
                              "not a choice")

    for name, t in terrs.items():
        for heading in TERRITORY_SECTIONS:
            if heading.split(" · ")[-1][:18].lower() not in t["_text"].lower():
                r.fail(name, f"section missing: {heading}")
        if not t["falsifier"]:
            r.fail(name, "no falsifier stated; a territory nothing could disprove is a slogan")
        w = (t["word"] or "").strip().lower()
        if not w:
            r.fail(name, "no owned word stated")
        elif w in ABSTRACT_WORDS:
            r.fail(name, f"owned word {w!r} is an abstraction: name the company that owns "
                         "it today, or pick a different axis")
        e = (t["eliminate"] or "").strip()
        if not e:
            r.fail(name, "ERRC has no Eliminate row")
        elif any(re.search(p, e, re.I) for p in EMPTY_ELIMINATE):
            r.fail(name, f"Eliminate row {e!r} names no factor the industry competes on")

    # Four-way distinctness.
    for axis in ("word", "enemy", "category", "beachhead"):
        seen: dict[str, str] = {}
        pop = 0
        for name, t in terrs.items():
            v = (t.get(axis) or "").strip().lower()
            if not v:
                continue
            pop += 1
            if v in seen:
                r.fail(f"{seen[v]} + {name}",
                       f"share the same {axis} ({v!r}): these are one territory, not two")
            seen[v] = name
        r.ran(f"territory {axis} values compared", pop)


def check_html(path: Path, r: Report) -> None:
    html = path.read_text()
    r.ran("html surfaces", 1)
    name = path.name

    externals = re.findall(r'<(?:script|link)\b[^>]*?(?:src|href)\s*=\s*["\'](https?://[^"\']+)',
                           html, re.I)
    for url in externals:
        tag = re.search(r'<(?:script|link)\b[^>]*?["\']' + re.escape(url) + r'["\'][^>]*>',
                        html, re.I)
        blob = tag.group(0) if tag else ""
        if "fonts.googleapis.com" in url or "fonts.gstatic.com" in url:
            continue
        if "integrity=" not in blob:
            r.fail(name, f"external asset with no SRI: {url}")
        else:
            r.warn(name, f"external asset (pinned + SRI): {url} — inline it for an Artifact, "
                         "whose CSP blocks every other origin silently")

    animated = bool(re.search(r"@keyframes|gsap\.|ScrollTrigger|transition\s*:", html, re.I))
    if animated and "prefers-reduced-motion" not in html:
        r.fail(name, "motion present with no prefers-reduced-motion branch")

    if re.search(r"<canvas\b", html, re.I) and not re.search(r"<svg\b|<table\b", html, re.I):
        r.fail(name, "figures drawn to canvas with no DOM mark: absent with JS off and in print")

    for pat in BREADTH_BANS:
        m = re.search(pat, html, re.I)
        if m:
            r.fail(name, f"breadth-led framing in the rendered page: {m.group(0)!r}")

    if re.search(r"\bthree\.js\b|THREE\.", html, re.I) and "webgl" not in html.lower():
        r.warn(name, "three.js present with no WebGL-absent fallback")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="the docs/positioning directory")
    ap.add_argument("--html", action="append", help="rendered HTML to check; repeatable")
    ap.add_argument("--skip-suite", action="store_true",
                    help="check territories and copy only, before the suite is complete")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")

    r = Report()
    md = sorted(p for p in root.glob("*.md"))
    terrs = {p.name: parse_territory(p) for p in md if p.name.startswith("10-territory")}

    if not args.skip_suite:
        check_suite_present(root, r)
    check_placeholders(md, root, r)
    check_breadth(md, root, r)
    check_figures(md, root, r)
    if terrs:
        check_territories(terrs, r)
    else:
        r.fail(root.as_posix(), "no territory files (10-territory-*.md) found")

    for h in args.html or []:
        p = Path(h)
        if p.exists():
            check_html(p, r)
        else:
            r.fail(h, "html not found")

    print(f"scanned {len(md)} markdown file(s), {len(terrs)} territor(ies), "
          f"{len(args.html or [])} html surface(s)")
    for k, v in sorted(r.checked.items()):
        print(f"  checked  {k}: {v}")
    for w in r.warnings:
        print(f"  warn  {w}")
    for e in r.errors:
        print(f"  FAIL  {e}")

    print(f"\n{len(r.errors)} error(s), {len(r.warnings)} warning(s)")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
