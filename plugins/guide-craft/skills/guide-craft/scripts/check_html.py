#!/usr/bin/env python3
"""Validate generated season-guide HTML files for mechanical defects.

Checks every .html file in a directory (or one file) for:
1. Nested <a> elements (citation links inside clickable card links shatter CSS grids).
2. Digit-leading id attributes (e.g. id="5k2k" throws SyntaxError in querySelectorAll).
3. Unresolved [[rN]] citation tokens left in rendered HTML.
4. Missing local <img src="..."> targets (skips http/https/data URIs).

Exit 0 when all checks pass, exit 1 on any defect.
Run --self-test to verify every check fails on a bad fixture and passes on a good one.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import tempfile
from html.parser import HTMLParser
from typing import List, Tuple

UNRESOLVED_RE = re.compile(r"\[\[r\d+\]\]")
DIGIT_ID_RE = re.compile(r"^[0-9]")


class GuideHTMLChecker(HTMLParser):
    def __init__(self, html_path: pathlib.Path, root_dir: pathlib.Path | None) -> None:
        super().__init__(convert_charrefs=True)
        self.html_path = html_path
        self.root_dir = root_dir
        self.anchor_depth = 0
        self.errors: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        line, _ = self.getpos()
        t = tag.lower()
        if t == "a":
            if self.anchor_depth > 0:
                self.errors.append(f"{self.html_path.name}:{line}: nested <a> element")
            self.anchor_depth += 1
        elem_id = attr_map.get("id", "")
        if elem_id and DIGIT_ID_RE.match(elem_id):
            self.errors.append(
                f"{self.html_path.name}:{line}: digit-leading id=\"{elem_id}\" breaks querySelectorAll"
            )
        if t == "img":
            src = attr_map.get("src", "").strip()
            if src and not src.startswith(("http://", "https://", "data:", "//")):
                clean_src = src.split("?", 1)[0].split("#", 1)[0]
                if clean_src.startswith("/") and self.root_dir is not None:
                    target = self.root_dir / clean_src.lstrip("/")
                else:
                    target = (self.html_path.parent / clean_src).resolve()
                if not target.exists():
                    self.errors.append(f"{self.html_path.name}:{line}: missing local image {src}")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self.anchor_depth > 0:
            self.anchor_depth -= 1


def check_file(path: pathlib.Path, root_dir: pathlib.Path | None = None) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = GuideHTMLChecker(path, root_dir)
    parser.feed(text)
    parser.close()
    errors = list(parser.errors)
    for idx, line in enumerate(text.splitlines(), 1):
        for m in UNRESOLVED_RE.finditer(line):
            errors.append(f"{path.name}:{idx}: unresolved citation token {m.group(0)}")
    return errors


def check_target(target: pathlib.Path, root_dir: pathlib.Path | None = None) -> Tuple[int, List[str]]:
    if target.is_file():
        files = [target]
    else:
        files = sorted(target.glob("*.html"))
    if not files:
        return 0, [f"no .html files found under {target}"]
    errors: List[str] = []
    for f in files:
        errors.extend(check_file(f, root_dir=root_dir))
    return len(files), errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "img").mkdir()
        (root / "img" / "ok.png").write_bytes(b"\x89PNG\r\n\x1a\n")

        good = root / "good.html"
        good.write_text(
            '<!doctype html><section id="uw-5k2k">'
            '<article class="card"><a class="link" href="a.html">Pick</a>'
            '<sup><a href="#r1">1</a></sup><img src="img/ok.png" alt="ok"></article>'
            "</section>",
            encoding="utf-8",
        )
        n_good, errs_good = check_target(good, root_dir=root)
        assert n_good == 1 and not errs_good, f"expected clean good fixture, got {errs_good}"

        bad = root / "bad.html"
        bad.write_text(
            '<!doctype html><section id="5k2k">'
            '<a class="card" href="a.html">Pick <sup><a href="#r1">1</a></sup></a>'
            '<p>Unresolved [[r42]]</p><img src="img/missing.webp" alt="missing">'
            "</section>",
            encoding="utf-8",
        )
        n_bad, errs_bad = check_target(bad, root_dir=root)
        assert n_bad == 1 and len(errs_bad) == 4, f"expected 4 errors on bad fixture, got {errs_bad}"
        kinds = ["digit-leading", "nested <a>", "missing local image", "unresolved citation"]
        for k in kinds:
            assert any(k in e for e in errs_bad), f"missing expected error class {k!r} in {errs_bad}"

    print("check_html.py --self-test: PASS (good fixture 0 errors; bad fixture 4/4 defect classes caught)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate generated guide HTML files.")
    ap.add_argument("target", nargs="?", help="HTML file or directory containing *.html")
    ap.add_argument("--root", help="Site root for absolute /path image checks")
    ap.add_argument("--self-test", action="store_true", help="Run built-in positive and negative fixture tests")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.target:
        ap.error("provide a target file/directory or --self-test")

    target = pathlib.Path(args.target)
    root_dir = pathlib.Path(args.root) if args.root else (target if target.is_dir() else target.parent)
    count, errors = check_target(target, root_dir=root_dir)
    if errors:
        for err in errors:
            print(f"FAIL {err}")
        print(f"check_html: {len(errors)} error(s) across {count} file(s)")
        return 1
    print(f"check_html: ok ({count} file(s), 0 errors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
