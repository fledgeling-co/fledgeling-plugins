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
            ids = [i for i in re.split(r"[\s,]+",
                                       a.get("data-claims") or a.get("data-claim", ""))
                   if i]
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


# --- Text of the page, with markup and the source registry removed. -----------
# Everything below reasons over what a reader actually reads, so a source titled
# "Conflicting evidence on X" must not be mistaken for the page saying so itself.

def _prose(html: str) -> str:
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    body = re.sub(r'<ol\b[^>]*>.*?</ol>', " ", body, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", body)


# A page whose subject genuinely has no contested question is possible and rare.
# These are the constructions that carry a stated limit, not hedging words like
# "may" or "often", which appear in confident prose too.
UNCERTAINTY = re.compile(
    r"\b("
    r"disagree\w*|contradict\w*|"
    r"unverified|unresolved|contested|inconclusive|single[- ]sourced|"
    r"could not (?:be )?(?:establish|verify|confirm|resolve|find)\w*|"
    r"(?:not|never) (?:been )?(?:established|verified|confirmed|corroborated|measured)|"
    r"no (?:published|public|first-party|primary|documented|traceable) (?:figure|source|number|benchmark|data|record)|"
    r"nobody (?:has |)(?:published|written|measured|benchmark\w*|knows)|"
    r"low confidence|treat as unverified|do not tune against"
    r")\b", re.I)


def check_uncertainty(html: str, f: Findings) -> None:
    """A page that resolves everything reads as generated, and usually is.

    This is the one Tier-1 check on the argument rather than the markup, and it
    exists because two pages from this skill were measured side by side: the
    weaker carried a single uncertainty construction in 8,400 words, the stronger
    twenty-four. Both were fully cited, both passed every other gate here, and a
    blind judge in both orderings picked the second on exactly this axis.

    The check is deliberately generous - one construction anywhere clears it.
    It cannot see whether the uncertainty is load-bearing; it can see that a page
    claiming to be built on five disagreeing backends never once says so.
    """
    prose = _prose(html)
    hits = UNCERTAINTY.findall(prose)
    words = len(prose.split())
    if not hits:
        f.add(ERROR, "uncertainty",
              f"{words} words and not one stated limit, disagreement or "
              "unestablished claim. A page with real sources almost always has "
              "something it is unsure about; a page with none reads as generated. "
              "Say where the panel split and what could not be established, in "
              "every reading - see references/readings.md")
        return
    kinds = len({h.lower() for h in hits})
    if kinds < 2 and words > 3000:
        f.add(ERROR, "uncertainty",
              f"one uncertainty construction in {words} words is effectively "
              "none. The page reads as settled. Name where the panel split, what "
              "the corpus could not establish, and which figures are single-sourced "
              "- in every reading, not only in the methods note")
    elif kinds < 4 and words > 3000:
        f.add(WARN, "uncertainty",
              f"only {kinds} distinct uncertainty construction(s) across {words} "
              "words. Check the disagreements survived into all three readings "
              "rather than sitting in the methods note alone")
    else:
        f.ok("uncertainty",
             f"{len(hits)} stated limit(s)/disagreement(s), {kinds} distinct kinds")


def check_claim_graph(path: pathlib.Path, html: str, f: Findings) -> None:
    """The claim graph has to reach the markup, or nothing checks it.

    A ledger sitting in claims.json that no block references is an artifact the
    page does not use: the per-claim/reading check below silently finds nothing
    to test, and reports a clean run. That has shipped - one page carried a full
    27-claim ledger beside it and zero data-claims attributes, and every gate
    here went green.
    """
    graph = path.parent / "claims.json"
    wired = len(re.findall(r'data-claims?=', html))
    if not graph.is_file():
        if wired:
            f.ok("claim graph", f"{wired} block(s) carry claim ids")
        return

    try:
        data = json.loads(graph.read_text())
    except Exception as e:                                    # noqa: BLE001
        f.add(WARN, "claim graph", f"claims.json present but unreadable: {e}")
        return

    claims = data.get("claims") or []
    ids = {c.get("id") for c in claims if isinstance(c, dict)}
    if not wired:
        f.add(ERROR, "claim graph",
              f"claims.json holds {len(ids)} claim(s) and the page references "
              "none of them. Put data-claims on the blocks that render each "
              "claim, or the per-claim citation check has nothing to test and "
              "passes vacuously")
        return

    used = set()
    for m in re.finditer(r'data-claims?="([^"]*)"', html):
        used |= {i for i in re.split(r"[\s,]+", m.group(1)) if i}
    orphan = sorted(used - ids) if ids else []
    if orphan:
        f.add(ERROR, "claim graph",
              f"block(s) cite claim id(s) not in claims.json: {', '.join(orphan[:6])}")
    missing = sorted(ids - used)
    if missing:
        f.add(WARN, "claim graph",
              f"{len(missing)} claim(s) in the ledger reach no block: "
              + ", ".join(missing[:6])
              + ". Expected for a claim carrying omit/omitReason; a defect otherwise")
    if not orphan:
        f.ok("claim graph", f"{len(used)} claim id(s) wired into the page")

    # An inference rendered as an empirical finding is the failure the ledger's
    # kind field exists to prevent, so the page has to say the word somewhere.
    inferred = [c.get("id") for c in claims
                if isinstance(c, dict) and c.get("kind") == "inference"]
    if inferred:
        prose = _prose(html)
        if not re.search(r"\b(inference|inferred|derived, not|reasoned from|"
                         r"arithmetic on|not a measurement|order[- ]of[- ]magnitude)\b",
                         prose, re.I):
            f.add(ERROR, "inference marking",
                  f"{len(inferred)} claim(s) are marked kind=inference in the "
                  "ledger and the page never labels anything as inferred. "
                  "Something assembled by reasoning is being rendered as an "
                  "empirical finding")
        else:
            f.ok("inference marking",
                 f"{len(inferred)} inference(s) in the ledger, labelled in the page")


def check_self_description(html: str, f: Findings) -> None:
    """What the page says about its own evidence must match its own registry.

    Caught by a blind judge on a page from this skill: a colophon advertising
    "200+ primary sources" above a registry listing 21. The number is the easiest
    thing on an evidence page to check and the most damaging to get wrong, because
    a reader who checks it once stops believing the rest.
    """
    listed = len(set(re.findall(r'<li\s+id="(r[\w-]+)"', html)))
    if not listed:
        return
    prose = _prose(html)
    bad = []
    for m in re.finditer(r"\b(\d[\d,]*)\s*\+?\s*(?:primary\s+|cited\s+|first-party\s+)?sources?\b",
                         prose, re.I):
        claimed = int(m.group(1).replace(",", ""))
        # A page legitimately cites a bigger corpus than it lists - "233 sources
        # across five backends", 35 of them in the registry. A count carrying its
        # own scope is a statement about the corpus; a bare boast is a statement
        # about the list below it, and only the second is checkable here.
        window = prose[max(0, m.start() - 110):m.end() + 30].lower()
        scoped = any(w in window for w in (
            "across", "backend", "panel", "corpus", "in total", "combined",
            "between them", "read in full", "reports"))
        own = any(w in window for w in (
            "registry", "listed", "sources below", "primary sources",
            "cited below", "source list"))
        if own and not scoped and claimed > listed * 1.5:
            bad.append(f"{m.group(0).strip()} against {listed} listed")
    if bad:
        f.add(ERROR, "self-description",
              "the page advertises more sources than its registry holds: "
              + "; ".join(bad[:3]))
    else:
        f.ok("self-description", f"registry of {listed} matches what the page claims")



def check_tldr(html: str, f: Findings) -> None:
    """The TLDR band exists, leads, cites, and reaches every register.

    "Lead with the conclusion" is a principle and principles get interpreted;
    the band is the enforceable form of it. Three ways it fails while looking
    fine: it is not there at all, it is there but sits below the first argument
    block, or it renders in two registers and not the third - which is worst,
    because the register that lost it is the one a reader lands on by link.
    """
    m = re.search(r'<section\b[^>]*\bid="tldr"[^>]*>', html, re.I)
    if not m:
        f.add(ERROR, "tldr",
              'no <section id="tldr"> - every page opens with a TLDR band '
              "carrying the finding, its supporting claims and the one thing "
              "that would change it")
        return

    # Nothing carrying claims may precede it: the band is the first content block.
    before = html[:m.start()]
    early = re.search(r'<section\b[^>]*data-claims?=', before, re.I)
    if early:
        f.add(ERROR, "tldr",
              "a block carrying data-claims appears before the TLDR band - the "
              "band is the first content block after the masthead")

    end = html.find("</section>", m.end())
    band = html[m.end():end if end != -1 else len(html)]

    if 'class="cite' not in band and "class='cite" not in band:
        f.add(ERROR, "tldr",
              "the TLDR band carries no citation marker - it is the most quoted "
              "block on the page and the last place an uncited number may sit")

    regs = set()
    for attr in re.findall(r'data-reading="([^"]*)"', band):
        regs |= {r for r in re.split(r"[\s,]+", attr) if r}
    known = {"primer", "brief", "technical"}
    if not regs:
        f.add(WARN, "tldr",
              "the TLDR band carries no data-reading attributes, so one wording "
              "serves all three registers. Intended only where the wording is "
              "genuinely identical in each")
    else:
        missing = sorted(known - regs)
        if missing:
            f.add(ERROR, "tldr",
                  "the TLDR band renders for "
                  + ", ".join(sorted(regs & known))
                  + " but not " + ", ".join(missing)
                  + " - a register without the finding is a different page")
        else:
            f.ok("tldr", "band present, cited, and rendering in all three readings")


def check_motion_feedback(html: str, f: Findings) -> None:
    """GSAP is a hard requirement, and so are the states it choreographs.

    Two separate failures wear the same face. A page with no motion layer at all
    passed every earlier gate because the layer was a house rule with an escape
    hatch in it. And a page whose controls have no hover, focus or active state
    reads as broken however good its argument is - the reading toggle is the
    page's primary control, and a primary control that acknowledges a press with
    nothing is the first thing a reader distrusts.
    """
    has_gsap = re.search(r'(?:src|import)\s*[=(]\s*["\'][^"\']*gsap|'
                         r'\bgsap\.(?:to|from|timeline|registerPlugin|matchMedia|'
                         r'defaults|quickTo|set)\s*\(',
                         html, re.I) is not None
    if not has_gsap:
        f.add(ERROR, "gsap",
              "GSAP is not loaded. It is the standing motion layer on every page "
              "- entrance choreography, reveals, micro-interaction feedback, and "
              "any scrubbed or pinned episode. Where the argument has no scrubbed "
              "moment, record that in the methods note and still ship the layer")
    else:
        f.ok("gsap", "motion layer present")

    if re.search(r'\bgsap\.(?:to|from|fromTo)\s*\([^)]*:hover', html):
        f.add(WARN, "gsap",
              "a hover state appears to be driven from GSAP - tier-0 states stay "
              "in CSS so they survive a script failure")

    for sel, level, why in (
        (":focus-visible", ERROR,
         "no :focus-visible rule - the focus ring may never be removed without a "
         "visible replacement, in both themes"),
        (":hover", ERROR,
         "no :hover rule - every interactive element carries hover, focus, active "
         "and disabled"),
        (":active", WARN,
         "no :active rule - a control that does not acknowledge a press reads as "
         "broken"),
        (":disabled", WARN,
         "no :disabled rule - a disabled control that looks enabled feels broken "
         "on click"),
    ):
        if sel not in html:
            f.add(level, "micro-interaction", why)

    # outline:none is only a defect when the same block offers no other visible
    # change. A published page in this portfolio sets background and color there,
    # which is a legitimate indicator, and an unconditional check called it broken.
    for blk in re.finditer(r':focus-visible[^{]*\{([^}]*)\}', html, re.I):
        body = blk.group(1)
        if not re.search(r'outline\s*:\s*(?:none|0)\s*[;}]?', body, re.I):
            continue
        if re.search(r'\b(background|background-color|box-shadow|border|'
                     r'border-color|text-decoration|color|filter)\s*:', body, re.I):
            continue
        f.add(ERROR, "micro-interaction",
              ":focus-visible removes the outline and sets nothing else visible - "
              "the replacement has to be seen")
        break

    if "cursor:pointer" not in html.replace(" ", ""):
        f.add(WARN, "micro-interaction",
              "no cursor:pointer anywhere - a clickable card or citation marker "
              "with a default cursor reads as static text")


def check_verdict(path: pathlib.Path, html: str, f: Findings) -> None:
    """A recommendation is a judgement, and it renders as one.

    A ranking is assembled by reasoning across claims, so it is the strongest
    thing on the page and the one most likely to arrive with no evidence attached.
    Two failures this catches: a pick recorded as an empirical finding, and a
    winner with nothing it loses on - which is a product page, not a verdict.
    """
    graph = path.parent / "claims.json"
    if not graph.is_file():
        return
    try:
        data = json.loads(graph.read_text())
    except Exception:                                         # noqa: BLE001
        return

    claims = [c for c in (data.get("claims") or []) if isinstance(c, dict)]
    picks = [c for c in claims if c.get("rank") is not None or c.get("category")]
    if not picks:
        return

    bad_kind = [c.get("id") for c in picks if c.get("kind") != "inference"]
    if bad_kind:
        f.add(ERROR, "verdict",
              f"{len(bad_kind)} pick(s) are not kind=inference: "
              + ", ".join(str(i) for i in bad_kind[:6])
              + ". A ranking is assembled by reasoning across claims and renders "
                "as reasoning, not as a finding")
    no_from = [c.get("id") for c in picks
               if c.get("kind") == "inference" and not c.get("from")]
    if no_from:
        f.add(ERROR, "verdict",
              f"{len(no_from)} pick(s) name no claims in `from`: "
              + ", ".join(str(i) for i in no_from[:6])
              + ". A reader who disagrees with the ranking needs to see which "
                "claim to attack")

    cats = {c.get("category") for c in picks if c.get("category")}
    overfull = [c for c in cats
                if len([p for p in picks if p.get("category") == c]) > 3]
    if overfull:
        f.add(WARN, "verdict",
              "categories with more than three picks: " + ", ".join(sorted(overfull)[:4])
              + " - the contract is a top three")

    prose = _prose(html)
    if not re.search(r"\b(loses on|weaker|worse (?:on|at)|against it|the trade|"
                     r"downside|it is not the|falls short|costs? more)\b", prose, re.I):
        f.add(ERROR, "verdict",
              "the page recommends something and never says what the winner "
              "loses on. A winner with no stated weakness is a product page")
    if not re.search(r"\b(would change|changes? (?:the|this) pick|unless you|"
                     r"if you (?:need|have)|not the pick (?:for|if))\b", prose, re.I):
        f.add(WARN, "verdict",
              "no stated condition on the recommendation - a pick with no "
              "conditions has not been thought about")
    if not re.search(r"\bas at\b|\bas of\b|\bchecked\b|\bpriced?\s+\w+\s+20\d\d",
                     prose, re.I):
        f.add(WARN, "verdict",
              "no as-at date near the recommendation - a price or version with "
              "no date is wrong within a quarter and does not know it")
    if not (bad_kind or no_from):
        f.ok("verdict", f"{len(picks)} pick(s) across {len(cats) or 1} category(ies), "
                        "each marked as an inference")


def check_imagery(html: str, f: Findings) -> None:
    """An image is a claim, so it carries provenance.

    An uncaptioned picture on an evidence page is the one element asserting
    something with no attribution at all - and a generated illustration a reader
    could mistake for a photograph of the thing under discussion is the same
    defect the claim graph exists to prevent, arriving through the artwork.
    """
    before_rows = len(f.rows)
    figures = re.findall(r"<figure\b.*?</figure>", html, re.S | re.I)
    asset_figs = [x for x in figures if re.search(r"<(?:img|video)\b", x, re.I)]

    # Mask every figure out, then anything left is an asset with no caption near it.
    outside = re.sub(r"<figure\b.*?</figure>", " ", html, flags=re.S | re.I)
    loose = len(re.findall(r"<(?:img|video)\b", outside, re.I))
    if loose:
        f.add(WARN, "imagery",
              f"{loose} <img>/<video> outside a <figure> - an asset carrying "
              "evidence needs a caption and a provenance line")

    for fig in asset_figs:
        if not re.search(r"<figcaption\b", fig, re.I):
            f.add(ERROR, "imagery",
                  "a figure containing an image or video has no <figcaption> - "
                  "every asset carries a caption naming what it is")
            break
    for fig in asset_figs:
        cap = re.search(r"<figcaption\b.*?</figcaption>", fig, re.S | re.I)
        body = cap.group(0) if cap else ""
        if not (re.search(r'class="(?:cite|prov)', body)
                or re.search(r"\bgenerated\b|\bpress kit\b|\bpublic domain\b|"
                             r"\bCC BY\b|\bcaptured\b|\bretrieved\b", body, re.I)):
            f.add(ERROR, "imagery",
                  "an image caption carries no provenance - name the origin and "
                  "cite it into the registry, or label it as generated")
            break

    for vid in re.findall(r"<video\b[^>]*>", html, re.I):
        if "autoplay" in vid.lower():
            f.add(ERROR, "imagery",
                  "<video autoplay> - a clip never starts on its own, and never "
                  "under reduced motion")
        for attr, why in (("muted", "no muted attribute"),
                          ("playsinline", "no playsinline attribute"),
                          ("controls", "no controls attribute"),
                          ("poster", "no poster - the poster frame is the static "
                                     "figure and the reduced-motion branch")):
            if attr not in vid.lower():
                f.add(WARN, "imagery", f"<video> {why}")

    # Only claim a pass when this gate found nothing: a check whose pass and its
    # failures print side by side is indistinguishable from one that did not run.
    if asset_figs and len(f.rows) == before_rows:
        f.ok("imagery", f"{len(asset_figs)} asset figure(s), each captioned with "
                        "its provenance")


def check_figure_alternatives(html: str, f: Findings) -> None:
    """Every meaningful figure states its conclusion in text somewhere.

    A chart's text alternative names the message, not the encoding - and it is
    the only form of the figure available to a reader with a screen reader, with
    images off, or holding the page printed in greyscale. TanStack's SVG host
    refuses to render without an aria-label for this reason; a hand-authored
    figure has to be given one deliberately.
    """
    # Strip markup that only *looks* like a DOM element: an <svg> inside a
    # data:image/svg+xml favicon is a string in an attribute, and counting it
    # reported a missing label on a page whose figures were all labelled.
    scan = re.sub(r"<(?:link|meta)\b[^>]*>", " ", html, flags=re.I)
    scan = re.sub(r"data:image/svg\+xml[^\"\')]*", " ", scan, flags=re.I)

    svgs = re.findall(r"<svg\b[^>]*>", scan, re.I)
    if not svgs:
        return

    # An <svg> is covered when it is decorative, self-labelled, or sits in a
    # figure that carries a caption.
    captioned_spans = [(m.start(), m.end()) for m in
                       re.finditer(r"<figure\b.*?</figure>", scan, re.S | re.I)
                       if re.search(r"<figcaption\b", m.group(0), re.I)]

    def in_captioned_figure(pos: int) -> bool:
        return any(a <= pos < b for a, b in captioned_spans)

    bare = []
    for m in re.finditer(r"<svg\b[^>]*>", scan, re.I):
        tag = m.group(0)
        if 'aria-hidden="true"' in tag or "aria-label" in tag:
            continue
        if in_captioned_figure(m.start()):
            continue
        bare.append(tag)

    if bare:
        f.add(ERROR, "figures",
              f"{len(bare)} <svg> with no aria-label, no aria-hidden and no "
              "enclosing <figcaption> - a meaningful figure needs a text "
              "alternative stating its conclusion; a decorative one needs "
              "aria-hidden=\"true\"")
    else:
        f.ok("figures",
             f"{len(svgs)} inline figure(s), each labelled, captioned or decorative")


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
                  check_a11y, check_uncertainty, check_self_description,
                  check_tldr, check_motion_feedback, check_imagery,
                  check_figure_alternatives):
        check(html, f)
    check_claim_graph(args.page, html, f)
    check_verdict(args.page, html, f)
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
