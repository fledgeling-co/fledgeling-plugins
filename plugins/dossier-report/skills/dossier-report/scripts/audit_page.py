#!/usr/bin/env python3
"""Audit a finished report page before anyone looks at it.

Deterministic checks only. This does not judge whether the page is good
- design-review does that against a real render. This catches the class
of defect that is invisible on screen and fatal in public: a citation
pointing at a source that was never listed, a source nobody cited, a
motion layer with no reduced-motion escape, a page that silently depends
on a host that may not answer.

    python3 audit_page.py path/to/index.html
    python3 audit_page.py path/to/index.html --json

Exit code 0 when every ERROR check passes, 1 otherwise. WARN never
fails the run: it is the reviewer's attention, not a gate.

The cite/ref contract this enforces is the one the existing pages use:

    <button class="cite" data-cite="r12" data-n="9">   in the prose
    <li id="r12"><a href="...">Title</a>...</li>       in the sources list

data-cite is the anchor, data-n is the number the reader sees. They are
deliberately separate: sources are numbered by first appearance for the
reader, while the anchor stays stable when a source is added mid-page.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ERROR, WARN = "ERROR", "WARN"


class Findings:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, check: str, detail: str) -> None:
        self.rows.append((level, check, detail))

    def ok(self, check: str, detail: str) -> None:
        self.rows.append(("PASS", check, detail))

    @property
    def failed(self) -> bool:
        return any(l == ERROR for l, _, _ in self.rows)


def check_citations(html: str, f: Findings) -> None:
    cites = re.findall(r'data-cite="([^"]+)"', html)
    nums = re.findall(r'data-cite="[^"]+"\s+data-n="([^"]+)"', html)
    ref_ids = re.findall(r'<li\s+id="(r[^"]+)"', html)

    if not cites and not ref_ids:
        # The skill's contract is absent. Before declaring the page uncited,
        # look for ANY citation structure: a page may use plain anchors into
        # a numbered registry, which is a valid implementation. An eval caught
        # this reporting "no citations" on a page carrying 142 of them.
        anchors = re.findall(r'<a\b[^>]+href="#([A-Za-z][\w-]*)"', html)
        targets = set(re.findall(r'<li\s+id="([\w-]+)"', html))
        resolving = [a for a in anchors if a in targets]
        cite_ish = len(re.findall(r'class="[^"]*\bcites?\b[^"]*"', html))

        if resolving or cite_ish:
            f.add(WARN, "citations",
                  f"citation structure found ({len(resolving)} anchor(s) resolving into a list, "
                  f"{cite_ish} element(s) classed as a citation) but NOT in this skill's "
                  "data-cite/data-n contract, so integrity could not be machine-checked. "
                  "Verify by hand or migrate to the contract.")
        else:
            f.add(ERROR, "citations",
                  "no citations and no sources list. An evidence page without them "
                  "does not ship.")
        return

    missing = sorted({c for c in cites if c not in ref_ids})
    if missing:
        f.add(ERROR, "cite->source", f"cited but never listed: {', '.join(missing)}")
    else:
        f.ok("cite->source", f"all {len(set(cites))} cited anchors resolve to a source")

    unused = sorted(set(ref_ids) - set(cites))
    if unused:
        f.add(ERROR, "source->cite", f"listed but never cited: {', '.join(unused)}")
    else:
        f.ok("source->cite", f"all {len(ref_ids)} listed sources are cited")

    if len(cites) != len(nums):
        f.add(ERROR, "cite markup", f"{len(cites)} data-cite but {len(nums)} carry data-n")

    # a citation whose visible number contradicts another use of the same anchor
    pairs = re.findall(r'data-cite="([^"]+)"\s+data-n="([^"]+)"', html)
    by_anchor: dict[str, set[str]] = {}
    for anchor, n in pairs:
        by_anchor.setdefault(anchor, set()).add(n)
    inconsistent = {a: v for a, v in by_anchor.items() if len(v) > 1}
    if inconsistent:
        detail = "; ".join(f"{a} shown as {sorted(v)}" for a, v in inconsistent.items())
        f.add(ERROR, "cite numbering", f"same source, different numbers: {detail}")

    # a source the reader cannot open is a source the reader cannot check
    bare = [rid for rid in ref_ids
            if not re.search(rf'<li\s+id="{re.escape(rid)}"[^>]*>.{{0,400}}?<a\s',
                             html, re.S)]
    if bare:
        f.add(WARN, "source links", f"{len(bare)} source(s) with no anchor to open")
    elif ref_ids:
        f.ok("source links", f"all {len(ref_ids)} sources are openable")

    # A marker that is a <button> is inert with JS off, so the claim-to-source
    # bond breaks in exactly the case the page is meant to survive. A blind
    # judge caught this on a page this skill produced.
    buttons = len(re.findall(r'<button[^>]+data-cite=', html))
    anchors = len(re.findall(r'<a[^>]+data-cite=', html))
    if buttons and not anchors:
        f.add(ERROR, "cite markup",
              f"all {buttons} citation markers are <button> elements with no href. "
              "They do not resolve with JavaScript disabled. Use "
              '<a class="cite" href="#rN" data-cite="rN"> and layer the popover on top.')
    elif buttons:
        f.add(WARN, "cite markup",
              f"{buttons} citation marker(s) are buttons without an href; "
              f"{anchors} are anchors. Mixed, so some break with JS off.")
    elif anchors:
        f.ok("cite markup", f"all {anchors} markers are anchors and resolve without JS")


def check_self_contained(html: str, f: Findings) -> None:
    """Everything except fonts and the two named CDN libraries must be inline.

    An external asset is a second thing that can fail, and these pages are
    archives: they should still render years after some CDN is retired.
    GSAP and three.js are the deliberate exceptions."""
    allowed = ("fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com",
               "unpkg.com", "cdn.jsdelivr.net")
    # canonical and og:url point AT this page; they are identity, not a dependency
    body = re.sub(r'<link[^>]+rel="canonical"[^>]*>', "", html)
    externals = re.findall(
        r'<(?:script|link|img)[^>]+(?:src|href)="(https?://[^"]+)"', body)
    # three.js arrives by dynamic import in the exemplar, not by a script tag
    externals += re.findall(r'import\(\s*[\'"](https?://[^\'"]+)[\'"]', body)
    stray = [u for u in externals if not any(a in u for a in allowed)]
    if stray:
        f.add(ERROR, "self-contained", f"external asset(s) off the allowlist: {stray[:4]}")
    else:
        f.ok("self-contained", f"{len(externals)} external ref(s), all on the allowlist")

    # allowlisted is not free: a webfont is a live CDN dependency on a page
    # meant to outlast the CDN, and a render-blocking request against LCP.
    fonts = [u for u in externals if "fonts.g" in u]
    if fonts:
        f.add(WARN, "webfonts",
              f"{len(fonts)} Google Fonts request(s). Zero network requests is "
              "achievable and a rival page won a blind comparison partly on it. "
              "Prefer a system stack or subset and inline the identity face.")
    elif externals:
        f.ok("webfonts", "no hosted webfonts")

    # a figure that only exists once script runs is absent with script off
    if re.search(r'<noscript>', html) and not re.search(r'<svg[^>]*>.{200,}?</svg>', html, re.S):
        f.add(WARN, "no-js figures",
              "a <noscript> block is present but no substantial inline SVG was found; "
              "check the figures are in the DOM rather than drawn by script")


def check_motion(html: str, f: Findings) -> None:
    # detect the LIBRARY, not the word: a page about scrollytelling will
    # discuss three.js in prose, and an eval caught this exact false positive.
    has_gsap = re.search(r'(?:src|import)\s*[=(]\s*["\'][^"\']*gsap|'
                         r'\bgsap\.(?:to|from|timeline|registerPlugin|matchMedia)\s*\(',
                         html, re.I) is not None
    has_three = re.search(r'(?:src|import)\s*[=(]\s*["\'][^"\']*three(?:\.module)?(?:\.min)?\.js|'
                          r'\bnew\s+THREE\.|'
                          r'THREE\.(?:Scene|WebGLRenderer|PerspectiveCamera)\s*\(', html) is not None
    reduced = "prefers-reduced-motion" in html

    # a THREE symbol with nothing that loads three.js is dead code that throws
    if has_three and not re.search(r'(?:src|import)\s*[=(]\s*["\'][^"\']*three|THREE\.REVISION', html):
        f.add(ERROR, "three.js", "THREE is referenced but three.js is never loaded")

    if (has_gsap or has_three) and not reduced:
        f.add(ERROR, "reduced-motion",
              "motion library present with no prefers-reduced-motion branch")
    elif reduced:
        f.ok("reduced-motion", "prefers-reduced-motion branch present")

    if has_three:
        if "webglcontextlost" not in html.lower():
            f.add(WARN, "webgl", "three.js present with no webglcontextlost handler")
        if not re.search(r'WebGLRenderingContext|isWebGLAvailable|catch', html):
            f.add(WARN, "webgl", "three.js present with no visible capability fallback")
        f.ok("three.js", "present - the page must state in its notes why 3D earned its place")


def check_chrome(html: str, f: Findings) -> None:
    for cls, what in (("colophon", "masthead"), ("closer", "closing band")):
        if f'class="{cls}"' in html:
            f.ok(f"chrome:{cls}", f"{what} present")
        else:
            f.add(ERROR, f"chrome:{cls}", f"{what} missing - both marketing blocks are required")
    for mark in ("dossier-research-mcp", "margin.fledgeling.app"):
        if mark not in html:
            f.add(ERROR, "chrome:links", f"no link to {mark}")


def check_head(html: str, f: Findings) -> None:
    head = html[: html.find("</head>") if "</head>" in html else 4000]
    required = {
        "<title>": "title",
        'name="description"': "meta description",
        'property="og:title"': "og:title",
        'property="og:image"': "og:image",
        'rel="canonical"': "canonical",
        'name="viewport"': "viewport",
    }
    for needle, label in required.items():
        if needle not in head:
            f.add(ERROR, "head", f"missing {label}")
    if 'rel="apple-touch-icon"' not in head:
        f.add(WARN, "head", "no apple-touch-icon - the page icon was built, wire it up")
    if not any(n in head for n in required):
        return
    f.ok("head", "share and identity tags present")

    m = re.search(r"<title>([^<]{0,200})</title>", head)
    if m and len(m.group(1)) > 70:
        f.add(WARN, "head", f"title is {len(m.group(1))} chars, truncates in search results")


def check_a11y(html: str, f: Findings) -> None:
    imgs = re.findall(r"<img\b[^>]*>", html)
    no_alt = [i for i in imgs if "alt=" not in i]
    if no_alt:
        f.add(ERROR, "a11y:alt", f"{len(no_alt)} <img> with no alt attribute")
    elif imgs:
        f.ok("a11y:alt", f"all {len(imgs)} images carry alt")

    if "<html" in html and not re.search(r"<html[^>]+lang=", html):
        f.add(ERROR, "a11y:lang", "<html> has no lang attribute")

    canvases = re.findall(r"<canvas\b[^>]*>", html)
    undesc = [c for c in canvases if "aria-" not in c and "role=" not in c]
    if undesc:
        f.add(WARN, "a11y:canvas",
              f"{len(undesc)} <canvas> with no aria-hidden or role - decorative canvas "
              "should be aria-hidden, meaningful canvas needs a text equivalent")

    for btn in re.findall(r"<button\b[^>]*>\s*</button>", html):
        if "aria-label" not in btn and "aria-expanded" not in btn:
            f.add(WARN, "a11y:button", "empty <button> with no accessible name")
            break


def check_weight(path: pathlib.Path, html: str, f: Findings) -> None:
    kb = len(html.encode()) / 1024
    level = WARN if kb > 900 else "PASS"
    msg = f"{kb:.0f}KB of HTML"
    if level == WARN:
        f.add(WARN, "weight", msg + " - over 900KB, check what is inlined")
    else:
        f.ok("weight", msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page", type=pathlib.Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.page.is_file():
        print(f"audit_page.py: no such file: {args.page}", file=sys.stderr)
        return 2

    html = args.page.read_text(errors="replace")
    f = Findings()
    for check in (check_citations, check_self_contained, check_motion,
                  check_chrome, check_head, check_a11y):
        check(html, f)
    check_weight(args.page, html, f)

    if args.json:
        print(json.dumps([{"level": l, "check": c, "detail": d} for l, c, d in f.rows], indent=2))
    else:
        width = max(len(c) for _, c, _ in f.rows)
        for level, check, detail in f.rows:
            mark = {"PASS": "ok  ", ERROR: "FAIL", WARN: "warn"}[level]
            print(f"{mark}  {check.ljust(width)}  {detail}")
        errs = sum(1 for l, _, _ in f.rows if l == ERROR)
        warns = sum(1 for l, _, _ in f.rows if l == WARN)
        print(f"\n{errs} error(s), {warns} warning(s)")

    return 1 if f.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
