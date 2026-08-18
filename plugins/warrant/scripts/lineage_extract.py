#!/usr/bin/env python3
"""Walk rendered HTML and emit one figure -> source pair per displayed number.

This is the first half of the oracle plane, and it exists because the
highest-consequence failure for the target product is a correctly rendered page
stating a figure no source supports. Nothing on such a page looks wrong, so a
vision judge cannot see it; a provenance token can be counted.

A figure is any element carrying data-figure-id. Its source is data-source-ref,
taken from the element itself or, failing that, from the nearest ancestor that
declares one -- a table section or card that names the record its rows came from
sources every figure inside it, and demanding the attribute be repeated per cell
would make the gate unusable rather than strict. Which of the two supplied the
ref is recorded as source_from, so a reviewer can see how far the inheritance
reached.

Parsing is html.parser rather than a regex: an attribute lookalike inside a
comment or a text node is not a figure, and only a parser knows the difference.
"""

from __future__ import annotations

import argparse
import html.parser
import pathlib
import sys
from typing import Any

# Sibling modules live beside this file; make that work under both `python3
# scripts/lineage_extract.py` and `import lineage_extract` from elsewhere.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402

FIGURE_ATTR = "data-figure-id"
SOURCE_ATTR = "data-source-ref"
FIELD_ATTR = "data-source-field"
EXPR_ATTR = "data-source-expr"
VALUE_ATTR = "data-value"

# Elements that never open a scope, so a missing close tag is not a nesting bug.
VOID = frozenset(("area", "base", "br", "col", "embed", "hr", "img", "input",
                  "link", "meta", "param", "source", "track", "wbr"))

SKIP_DIRS = frozenset((".git", "node_modules", ".next", "dist", "build",
                       "coverage", ".warrant", "__pycache__"))


class _Frame:
    """One open element, plus whichever figures it is contributing text to."""

    __slots__ = ("tag", "attrs", "source", "figures")

    def __init__(self, tag: str, attrs: dict[str, str], source: str | None) -> None:
        self.tag = tag
        self.attrs = attrs
        self.source = source
        self.figures: list[dict[str, Any]] = []


class FigureParser(html.parser.HTMLParser):
    """Collects figure records with their ancestor chain and their own text."""

    def __init__(self, surface: str) -> None:
        super().__init__(convert_charrefs=True)
        self.surface = surface
        self.figures: list[dict[str, Any]] = []
        self._stack: list[_Frame] = []
        self._open: list[dict[str, Any]] = []          # figures still capturing text

    # -- helpers ---------------------------------------------------------------

    def _selector(self, tag: str, attrs: dict[str, str], figure_id: str) -> str:
        parts = []
        for frame in self._stack:
            step = frame.tag
            if frame.attrs.get("id"):
                step += f"#{frame.attrs['id']}"
            elif frame.attrs.get("class"):
                step += "." + frame.attrs["class"].split()[0]
            parts.append(step)
        # Address the figure by its own token: unique even when two elements
        # claim the same id, which is a case the gate has to be able to name.
        parts.append(f'{tag}[{FIGURE_ATTR}="{figure_id}"]')
        return " > ".join(parts)

    def _inherited_source(self) -> tuple[str | None, str]:
        for frame in reversed(self._stack):
            if frame.source:
                return frame.source, "ancestor"
        return None, "none"

    # -- parser callbacks ------------------------------------------------------

    def handle_starttag(self, tag: str, attrlist: list[tuple[str, str | None]]) -> None:
        attrs = {k.lower(): (v or "") for k, v in attrlist}
        own_ref = attrs.get(SOURCE_ATTR, "").strip()
        figure_id = attrs.get(FIGURE_ATTR, "").strip()

        record: dict[str, Any] | None = None
        if figure_id:
            if own_ref:
                source: str | None = own_ref
                source_from = "self"
            else:
                source, source_from = self._inherited_source()
            record = {
                "id": figure_id,
                "source": source,
                "selector": self._selector(tag, attrs, figure_id),
                "text": "",
                "file": self.surface,
                "line": self.getpos()[0],
                "source_from": source_from,
                "field": attrs.get(FIELD_ATTR) or None,
                "expr": attrs.get(EXPR_ATTR) or None,
                "value": attrs.get(VALUE_ATTR) or None,
            }
            self.figures.append(record)

        if tag in VOID:
            # No scope, but a void element can still be a figure (an <input
            # value=…> rendering a number), so the record is kept.
            return

        frame = _Frame(tag, attrs, own_ref or None)
        if record is not None:
            frame.figures.append(record)
            self._open.append(record)
        self._stack.append(frame)

    def handle_startendtag(self, tag: str, attrlist: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrlist)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        # Unwind to the matching open tag; malformed markup closes what it can
        # rather than desynchronising the whole document.
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i].tag == tag:
                for frame in self._stack[i:]:
                    for record in frame.figures:
                        if record in self._open:
                            self._open.remove(record)
                del self._stack[i:]
                return

    def handle_data(self, data: str) -> None:
        if not self._open or not data.strip():
            return
        for record in self._open:
            record["text"] = (record["text"] + " " + data.strip()).strip()


def surfaces_for(input_path: pathlib.Path, pattern: str) -> list[pathlib.Path]:
    """The HTML files under one path: itself if a file, a sorted walk if a dir."""
    if not input_path.exists():
        raise _state.Absent(str(input_path))
    if input_path.is_file():
        return [input_path]
    found = [p for p in sorted(input_path.rglob(pattern))
             if p.is_file() and not (SKIP_DIRS & set(p.parts))]
    return found


def extract(paths: list[pathlib.Path], root: pathlib.Path | None = None) -> dict[str, Any]:
    """Parse every path and return the report the gate and tick-and-tie consume."""
    figures: list[dict[str, Any]] = []
    surfaces: list[dict[str, Any]] = []
    for path in paths:
        try:
            label = str(path.relative_to(root)) if root else str(path)
        except ValueError:
            label = str(path)
        parser = FigureParser(label)
        parser.feed(path.read_text(errors="replace"))
        parser.close()
        seen: dict[str, int] = {}
        for record in parser.figures:
            seen[record["id"]] = seen.get(record["id"], 0) + 1
        unsourced = [f for f in parser.figures if not f["source"]]
        surfaces.append({
            "file": label,
            "figures": len(parser.figures),
            "sourced": len(parser.figures) - len(unsourced),
            "unsourced": len(unsourced),
            "duplicate_ids": sorted(k for k, n in seen.items() if n > 1),
        })
        figures.extend(parser.figures)

    return {
        "figures": figures,
        "unsourced": [f for f in figures if not f["source"]],
        "surfaces": surfaces,
    }


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    target = pathlib.Path(args.input).expanduser().resolve() if args.input else root
    paths = surfaces_for(target, args.glob)
    if not paths:
        _cli.say(args, f"no files matching {args.glob} under {target}")
        return _cli.MISSING

    report = extract(paths, root if target.is_dir() else None)
    report["input"] = str(target)
    report["generated_at"] = _cli.now(args).isoformat()

    total = len(report["figures"])
    sourced = total - len(report["unsourced"])
    _cli.say(args, f"{len(paths)} surface(s), {total} figure(s)")
    _cli.say(args, "sourced: " + _cli.rate(sourced, total, "figures"))
    for surface in report["surfaces"]:
        _cli.say(args, f"  {surface['file']}: {surface['sourced']}/{surface['figures']} sourced"
                       + (f", duplicate ids {surface['duplicate_ids']}"
                          if surface["duplicate_ids"] else ""))
    for figure in report["unsourced"]:
        _cli.say(args, f"  unsourced: {figure['id']} at {figure['file']}:{figure['line']}")
    _cli.emit(args, report)
    return _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--input", help="HTML file or directory of them (default: --root)")
    p.add_argument("--glob", default="*.html", help="filename pattern when --input is a directory")


def _fixtures() -> pathlib.Path:
    return (pathlib.Path(__file__).resolve().parent.parent
            / "evals" / "fixtures" / "oracle-assay" / "lineage")


def selftest() -> list[tuple[str, bool]]:
    """Every rule observed both ways: sourced and not, inherited and not."""
    cases: list[tuple[str, bool]] = []
    fx = _fixtures()

    sound = extract([fx / "sound" / "dashboard.html"])
    by_id = {f["id"]: f for f in sound["figures"]}
    cases.append(("a file yields its figures", len(sound["figures"]) == 3))
    cases.append(("self-declared source is read",
                  by_id["headcount"]["source"] == "hr-census-2026-08"
                  and by_id["headcount"]["source_from"] == "self"))
    cases.append(("ancestor source is inherited",
                  by_id["revenue-total"]["source"] == "filing-2026-q3"
                  and by_id["revenue-total"]["source_from"] == "ancestor"))
    cases.append(("a fully sourced surface reports nothing unsourced",
                  sound["unsourced"] == []))
    cases.append(("selector names the ancestor chain and the figure",
                  by_id["revenue-total"]["selector"]
                  == 'html > body > main#dashboard > section.kpis > '
                     'span[data-figure-id="revenue-total"]'))
    cases.append(("text is captured and collapsed",
                  by_id["revenue-total"]["text"] == "$1,204,000"))
    cases.append(("a figure does not absorb a sibling figure's text",
                  by_id["headcount"]["text"] == "312"))
    cases.append(("field attribute is carried through",
                  by_id["margin"]["field"] == "margin"))
    cases.append(("no duplicate ids on a sound surface",
                  sound["surfaces"][0]["duplicate_ids"] == []))

    gap = extract([fx / "unsourced" / "kpi.html"])
    gap_ids = {f["id"]: f for f in gap["figures"]}
    cases.append(("a missing ref reads as unsourced",
                  gap_ids["guidance-fy27"]["source"] is None
                  and gap_ids["guidance-fy27"]["source_from"] == "none"))
    cases.append(("a whitespace-only ref is not a source",
                  gap_ids["npat"]["source"] is None))
    cases.append(("unsourced list names exactly the gaps",
                  sorted(f["id"] for f in gap["unsourced"]) == ["guidance-fy27", "npat"]))

    dupe = extract([fx / "duplicate" / "dupe.html"])
    cases.append(("duplicate ids are reported",
                  dupe["surfaces"][0]["duplicate_ids"] == ["revenue-total"]))
    cases.append(("duplicate figures are both sourced", dupe["unsourced"] == []))

    plain = extract([fx / "nofigures" / "plain.html"])
    cases.append(("a surface with no figures yields none", plain["figures"] == []))

    # A directory walk finds every surface; a file walk finds exactly one.
    walked = surfaces_for(fx, "*.html")
    cases.append(("directory walk finds all surfaces", len(walked) == 4))
    cases.append(("file walk finds one surface",
                  surfaces_for(fx / "sound" / "dashboard.html", "*.html")
                  == [fx / "sound" / "dashboard.html"]))
    absent = False
    try:
        surfaces_for(fx / "no-such-dir", "*.html")
    except _state.Absent:
        absent = True
    cases.append(("an absent input raises Absent (exit 3)", absent))

    # A comment that looks like a figure attribute must not become a figure.
    parser = FigureParser("inline")
    parser.feed('<div><!-- data-figure-id="ghost" --><span>1</span></div>')
    parser.close()
    cases.append(("an attribute inside a comment is not a figure", parser.figures == []))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
