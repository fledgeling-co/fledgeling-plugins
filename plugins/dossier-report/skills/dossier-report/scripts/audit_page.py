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
from html.parser import HTMLParser

ERROR, WARN = "ERROR", "WARN"

READINGS = ("primer", "brief", "technical")

# Floor for the gap between a text ink box and a vertical rule. The real check measures
# rendered ink (design-review's probeDividerProximity); this file sees only what was
# declared, which is why a var() resolves to a warning rather than a pass.
DIVIDER_FLOOR_PX = 16


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


class ReadingScanner(HTMLParser):
    """Walk the page tracking which readings each citation marker is visible under.

    An element carrying data-reading="brief technical" is visible only in those two, and
    everything inside it inherits that constraint. An element with no data-reading is
    visible in all three. So the readings a marker belongs to are the intersection of its
    own constraint with every ancestor's.

    This answers the only question that matters here: "is each reading, taken alone, still
    fully cited?" A page can satisfy cite->source globally while its Primer lost every
    marker during simplification, and the whole-document check cannot see it.
    """

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, frozenset]] = []
        self.active = frozenset(READINGS)
        self.cites: dict[str, set[str]] = {r: set() for r in READINGS}
        self.tagged = 0
        self.registry: set[str] = set()
        # One record per element carrying data-claims: which claims it renders, which
        # readings it renders in, and which of those a citation appeared under inside it.
        self.blocks: list[dict] = []
        self._open: list[dict] = []

    def _constraint(self, a: dict) -> frozenset:
        raw = a.get("data-reading")
        if raw is None:
            return self.active
        named = frozenset(w for w in raw.split() if w in READINGS)
        self.tagged += 1
        # An unrecognised value constrains to nothing rather than silently to everything;
        # a typo'd register should fail loudly, not render in all three.
        return self.active & named

    def _mark(self, a: dict, here: frozenset) -> None:
        if "data-cite" in a:
            for r in here:
                self.cites[r].add(a["data-cite"])
            for blk in self._open:
                blk["cited"] |= (here & blk["readings"])

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        here = self._constraint(a)
        self._mark(a, here)
        if "data-claims" in a or "data-claim" in a:
            ids = (a.get("data-claims") or a.get("data-claim", "")).split()
            rec = {"claims": ids, "readings": set(here), "cited": set(),
                   "depth": len(self.stack)}
            self.blocks.append(rec)
            self._open.append(rec)
        if tag == "li" and re.fullmatch(r"r[\w-]+", a.get("id", "")):
            self.registry.add(a["id"])
        if tag not in self.VOID:
            self.stack.append((tag, self.active))
            self.active = here

    def handle_startendtag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        self._mark(a, self._constraint(a))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.active = self.stack[i][1]
                del self.stack[i:]
                self._open = [b for b in self._open if b["depth"] < len(self.stack)]
                return


def check_readings(html: str, f: Findings) -> None:
    s = ReadingScanner()
    try:
        s.feed(html)
    except Exception as e:                                    # noqa: BLE001
        f.add(WARN, "readings", f"could not parse the page to check readings: {e}")
        return

    if not s.tagged:
        f.add(ERROR, "readings",
              "no [data-reading] anywhere. The page ships three registers — Primer, "
              "Brief, Technical — over one claim graph; see references/readings.md")
        return

    for r in READINGS:
        cited = s.cites[r]
        if not cited:
            f.add(ERROR, f"cited:{r}",
                  f"the {r} reading carries no citation markers at all. Simplifying the "
                  "words never removes the sources")
            continue
        missing = sorted(cited - s.registry)
        if missing:
            f.add(ERROR, f"cite->source:{r}",
                  f"{r}: cited but never listed: {', '.join(missing[:6])}")
        else:
            f.ok(f"cite->source:{r}", f"{r}: all {len(cited)} markers resolve")

    everywhere = set().union(*s.cites.values())
    unused = sorted(s.registry - everywhere)
    if unused:
        f.add(ERROR, "source->cite",
              f"listed but never cited in any reading: {', '.join(unused[:8])}")

    # A claim rendered in a register that never cites it anywhere on the page. Per claim
    # and reading, not per block — a stat row repeating a claim id is supporting furniture
    # and requiring a marker there would report a defect on a page that cites it properly
    # two episodes earlier.
    renders: dict[tuple[str, str], bool] = {}
    for blk in s.blocks:
        for cid in blk["claims"]:
            for r in blk["readings"]:
                renders[(cid, r)] = renders.get((cid, r), False) or (r in blk["cited"])
    uncited = sorted(f"{cid} in {r}" for (cid, r), okd in renders.items() if not okd)
    if uncited:
        f.add(WARN, "cited:per-claim",
              "claim(s) rendered in a reading that never cites them: "
              + "; ".join(uncited[:6])
              + ". Expected for a claim whose source sits on another block; a defect "
                "otherwise")
    elif renders:
        f.ok("cited:per-claim", f"{len(renders)} claim/reading pair(s) each carry a marker")

    if not re.search(r'<html[^>]+data-active-reading=', html):
        f.add(WARN, "readings:default",
              "no data-active-reading on <html> — nothing mirrors the current register "
              "for share tags or a second script")
    checked = re.findall(r'<input[^>]*name="reading"[^>]*\bchecked', html)
    if len(checked) != 1:
        f.add(ERROR, "readings:default",
              f"{len(checked)} reading radios carry `checked` in the markup; exactly one "
              "must, or the page has no register with JavaScript off")


def check_dividers(html: str, f: Findings) -> None:
    """A vertical rule is drawn in a gap, never beside words.

    Source-level only, and modest about it: the gap a reader perceives runs from the text
    INK to the line, and the padding declared here usually belongs to a different element
    from the one painting the border. design-review's probeDividerProximity measures the
    rendered ink and is the real gate. Run against a page already published from this
    skill, it returned twenty below-floor violations.
    """
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    if not css:
        return
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    findings, unresolved, good = [], [], 0
    for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, body = block.group(1).strip(), block.group(2)
        if sel.startswith("@") or not sel:
            continue
        for side in ("left", "right"):
            m = re.search(rf"border-{side}\s*:\s*([^;]+)", body)
            if not m:
                continue
            decl = m.group(1).strip()
            if re.match(r"^(0|none|hidden)\b", decl) or "transparent" in decl:
                continue
            pad = re.search(rf"padding-{side}\s*:\s*([^;]+)", body) \
                or re.search(r"padding-inline\s*:\s*([^;]+)", body) \
                or re.search(r"padding\s*:\s*([^;]+)", body)
            if not pad:
                findings.append(f"{sel} sets border-{side} with no padding-{side}")
                continue
            px = re.match(r"^\s*(\d+(?:\.\d+)?)px", pad.group(1))
            if px:
                if float(px.group(1)) < DIVIDER_FLOOR_PX:
                    findings.append(f"{sel}: border-{side} with padding-{side} "
                                    f"{px.group(1)}px (floor {DIVIDER_FLOOR_PX}px)")
                else:
                    good += 1
            else:
                unresolved.append(f"{sel} (border-{side})")

    if findings:
        f.add(ERROR, "divider gutter",
              f"{len(findings)} rule(s) draw a vertical line with no gap beside it: "
              + "; ".join(findings[:4]))
    if unresolved:
        f.add(WARN, "divider gutter",
              f"{len(unresolved)} divider gutter(s) are variables and cannot be resolved "
              "here — confirm with design-review's ink measurement: "
              + "; ".join(unresolved[:3]))
    if good and not findings:
        f.ok("divider gutter", f"{good} divider(s) declare a gutter at or above the floor")


def check_theme(html: str, f: Findings) -> None:
    """Light and dark both ship, and a token is never defined only in the dark."""
    has_dark = "prefers-color-scheme: dark" in html or '[data-theme="dark"]' in html
    if not has_dark:
        f.add(ERROR, "theme", "no dark rendering — both themes ship")
        return

    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    root = re.search(r":root\s*\{([^}]*)\}", css)
    base = set(re.findall(r"(--[\w-]+)\s*:", root.group(1))) if root else set()
    dark = set()
    for m in re.finditer(
            r"(?:prefers-color-scheme:\s*dark|\[data-theme=\"dark\"\])[^{]*\{(.*?)\}\s*\}?",
            css, re.S):
        dark |= set(re.findall(r"(--[\w-]+)\s*:", m.group(1)))
    orphan = sorted(dark - base)
    if orphan:
        f.add(ERROR, "theme:tokens",
              f"token(s) defined only in a dark block: {', '.join(orphan[:6])}. "
              "They are undefined everywhere the dark branch does not apply")
    else:
        f.ok("theme", "light defined unconditionally, dark overriding it")


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
    for check in (check_citations, check_readings, check_dividers, check_theme,
                  check_self_contained, check_motion, check_chrome, check_head,
                  check_a11y):
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
