#!/usr/bin/env python3
"""audit_report.py — check a built report against its own ledger and the craft rules.

    python3 scripts/audit_report.py docs/reports/<slug>/

Exit 0 when every ERROR check passes, 1 otherwise. WARN never blocks; it is the list for
the person about to read the thing.

The checks worth explaining, because they are the ones that catch real defects:

  * The ledger and the page have to agree BOTH WAYS. A claim in claims.json that never
    reaches the page means the report dropped a finding; a cited source on the page with no
    ledger row means prose outran the evidence. Neither shows up by reading the report.

  * Citation markers are anchors, never buttons. A <button data-cite> is inert with
    JavaScript off, which breaks the claim-to-source bond in exactly the case the document
    is supposed to survive.

  * Inference claims have to be visibly marked as inference. The whole point of the ledger
    is that a reader can tell reasoning from finding, and that distinction only exists if it
    survives into the markup.

This audits the built artifact. It does not check whether a source actually supports the
sentence attached to it — that needs someone to read both, and it is where the real
overclaiming lives.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ERROR, WARN, PASS = "ERROR", "WARN", "PASS"

READINGS = ("primer", "brief", "technical")

# Hosts a self-contained report may legitimately reach for. Everything else is a live
# dependency on a document meant to outlast whatever is serving it.
ALLOWED_HOSTS = ("cdnjs.cloudflare.com", "cdn.jsdelivr.net", "unpkg.com")

# Floor for the gap between a text ink box and a vertical rule. The real check measures
# rendered ink (design-review's probeDividerProximity); this file can only see what was
# declared, which is why a var() resolves to a warning rather than a pass.
DIVIDER_FLOOR_PX = 16


class Findings:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, check: str, detail: str) -> None:
        self.rows.append((level, check, detail))

    def ok(self, check: str, detail: str) -> None:
        self.rows.append((PASS, check, detail))

    @property
    def failed(self) -> bool:
        return any(l == ERROR for l, _, _ in self.rows)


# --------------------------------------------------------------------------- ledger

def load_ledger(d: pathlib.Path, f: Findings):
    p = d / "claims.json"
    if not p.exists():
        f.add(ERROR, "ledger", "claims.json is missing — the citations have nothing to be generated from")
        return None
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        f.add(ERROR, "ledger", f"claims.json is not valid JSON: {e}")
        return None

    claims = data.get("claims", data if isinstance(data, list) else [])
    sources = data.get("sources", [])
    if not claims:
        f.add(ERROR, "ledger", "claims.json holds no claims")
        return None

    bad = [c.get("id", "?") for c in claims if c.get("kind") not in ("direct", "inference")]
    if bad:
        f.add(ERROR, "ledger:kind",
              f"claim(s) with no direct/inference kind: {', '.join(map(str, bad[:6]))}")

    src_ids = {s.get("id") for s in sources}
    dangling = sorted({s for c in claims for s in c.get("sources", []) if s not in src_ids})
    if dangling:
        f.add(ERROR, "ledger:sources", f"claim(s) cite unknown source id(s): {', '.join(dangling[:6])}")

    # A direct claim with no source is the defect the whole ledger exists to prevent.
    unsourced = [c.get("id", "?") for c in claims
                 if c.get("kind") == "direct" and not c.get("sources")]
    if unsourced:
        f.add(ERROR, "ledger:unsourced",
              f"direct claim(s) with no source: {', '.join(map(str, unsourced[:6]))}")

    # An inference has to say what it rests on, or it is an assertion wearing a label.
    baseless = [c.get("id", "?") for c in claims
                if c.get("kind") == "inference" and not c.get("from")]
    if baseless:
        f.add(ERROR, "ledger:inference",
              f"inference(s) that name no supporting claims: {', '.join(map(str, baseless[:6]))}")

    nolimits = [c.get("id", "?") for c in claims if not c.get("limits")]
    if nolimits:
        f.add(WARN, "ledger:limits",
              f"{len(nolimits)} claim(s) state no limits — the sentence a sceptic would need")

    f.ok("ledger", f"{len(claims)} claim(s), {len(sources)} source(s), "
                   f"{sum(1 for c in claims if c.get('kind') == 'inference')} inference(s)")
    return {"claims": claims, "sources": sources}


# --------------------------------------------------------------------------- citations

def check_citations(html: str, ledger, f: Findings) -> None:
    cites = re.findall(r'data-cite="([^"]+)"', html)
    nums = re.findall(r'data-n="([^"]+)"', html)
    reg = set(re.findall(r'<li[^>]+id="(r[^"]+)"', html))

    if not cites:
        f.add(ERROR, "citations", "no citation markers on the page")
        return

    if len(cites) != len(nums):
        f.add(ERROR, "cite markup", f"{len(cites)} data-cite but {len(nums)} carry data-n")

    missing = sorted(set(cites) - reg)
    if missing:
        f.add(ERROR, "cite->source", f"cited but never listed: {', '.join(missing[:8])}")

    unused = sorted(reg - set(cites))
    if unused:
        f.add(ERROR, "source->cite", f"listed but never cited: {', '.join(unused[:8])}")

    # One source, one number. Two numbers for one anchor reads as two sources.
    pairs = re.findall(r'data-cite="([^"]+)"[^>]*data-n="([^"]+)"', html)
    seen: dict[str, set[str]] = {}
    for c, n in pairs:
        seen.setdefault(c, set()).add(n)
    clash = {c: v for c, v in seen.items() if len(v) > 1}
    if clash:
        detail = "; ".join(f"{c}: {sorted(v)}" for c, v in list(clash.items())[:4])
        f.add(ERROR, "cite numbering", f"same source, different numbers: {detail}")

    buttons = re.findall(r'<button[^>]*data-cite="', html)
    if buttons:
        f.add(ERROR, "cite markup",
              f"{len(buttons)} citation marker(s) are <button> — inert with JS off, which breaks "
              "the claim-source bond in the case the page is meant to survive. Use <a href=\"#rN\">.")

    anchors = len(re.findall(r'<a[^>]*data-cite="', html))
    if anchors and anchors == len(cites):
        f.ok("cite markup", f"{anchors} marker(s), all anchors with a registry target")

    if 'aria-describedby' not in html:
        f.add(WARN, "cite a11y", "no aria-describedby on markers — the preview is not announced")

    if ledger:
        ids = {str(c.get("id")) for c in ledger["claims"]}
        on_page = set(re.findall(r'data-claims?="([^"]+)"', html))
        referenced = {i for group in on_page for i in group.split()}
        orphaned = sorted(ids - referenced)
        if orphaned:
            f.add(ERROR, "ledger->page",
                  f"claim(s) in the ledger that never reach the page: {', '.join(orphaned[:8])}")
        ghost = sorted(referenced - ids)
        if ghost:
            f.add(ERROR, "page->ledger",
                  f"block(s) cite claim ids with no ledger row: {', '.join(ghost[:8])}")
        if not orphaned and not ghost and referenced:
            f.ok("ledger<->page", f"{len(referenced)} claim(s) agree in both directions")

        infer = [str(c.get("id")) for c in ledger["claims"] if c.get("kind") == "inference"]
        if infer:
            marked = set(re.findall(r'data-kind="inference"[^>]*data-claims?="([^"]+)"', html))
            marked |= set(re.findall(r'data-claims?="([^"]+)"[^>]*data-kind="inference"', html))
            flat = {i for g in marked for i in g.split()}
            unmarked = sorted(set(infer) - flat)
            if unmarked:
                f.add(ERROR, "inference marking",
                      "inference(s) not marked data-kind=\"inference\" on the page: "
                      f"{', '.join(unmarked[:6])} — a reader cannot tell reasoning from finding")
            else:
                f.ok("inference marking", f"{len(infer)} inference(s) visibly marked")


# --------------------------------------------------------------------------- readings

class ReadingScanner(HTMLParser):
    """Walk the document tracking which readings each citation marker is visible under.

    An element carrying data-reading="brief technical" is visible only in those two, and
    everything inside it inherits that constraint. An element with no data-reading is
    visible in all three. So the readings a marker belongs to are the intersection of its
    own constraint with every ancestor's.

    This is the only way to answer the question that matters: "is each reading, taken
    alone, still fully cited?" A page can satisfy cite->source globally while its Primer
    lost every marker during simplification, and nothing about the whole-document check
    would notice.
    """

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, frozenset]] = []
        self.active = frozenset(READINGS)
        self.cites: dict[str, set[str]] = {r: set() for r in READINGS}
        self.claims: dict[str, set[str]] = {r: set() for r in READINGS}
        self.tagged = 0          # elements carrying data-reading at all
        self.registry: set[str] = set()
        # One record per element carrying data-claims: which claims it renders, which
        # readings it renders in, and which of those readings a citation appeared under
        # inside it. A reading that keeps a claim but drops its marker is the failure
        # this exists to catch, and "does the page cite anything" cannot see it.
        self.blocks: list[dict] = []
        self._open: list[dict] = []

    def _constraint(self, attrs: dict) -> frozenset:
        raw = attrs.get("data-reading")
        if raw is None:
            return self.active
        named = frozenset(w for w in raw.split() if w in READINGS)
        self.tagged += 1
        # An unrecognised value constrains to nothing rather than silently to everything;
        # a typo'd register should fail loudly, not render in all three.
        return self.active & named

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        here = self._constraint(a)

        if "data-cite" in a:
            for r in here:
                self.cites[r].add(a["data-cite"])
            for blk in self._open:
                blk["cited"] |= (here & blk["readings"])
        if "data-claims" in a or "data-claim" in a:
            ids = (a.get("data-claims") or a.get("data-claim", "")).split()
            for cid in ids:
                for r in here:
                    self.claims[r].add(cid)
            rec = {"claims": ids, "readings": set(here), "cited": set(), "depth": len(self.stack)}
            self.blocks.append(rec)
            self._open.append(rec)
        if tag == "li" and re.fullmatch(r"r[\w-]+", a.get("id", "")):
            self.registry.add(a["id"])

        if tag not in self.VOID:
            self.stack.append((tag, self.active))
            self.active = here

    def handle_startendtag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        here = self._constraint(a)
        if "data-cite" in a:
            for r in here:
                self.cites[r].add(a["data-cite"])
            for blk in self._open:
                blk["cited"] |= (here & blk["readings"])

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.active = self.stack[i][1]
                del self.stack[i:]
                self._open = [b for b in self._open if b["depth"] < len(self.stack)]
                return


def check_readings(html: str, ledger, f: Findings) -> None:
    s = ReadingScanner()
    try:
        s.feed(html)
    except Exception as e:                                    # noqa: BLE001
        f.add(WARN, "readings", f"could not parse the document to check readings: {e}")
        return

    if not s.tagged:
        f.add(ERROR, "readings",
              "no [data-reading] anywhere. The report ships three registers — "
              "Primer, Brief, Technical — over one ledger; see references/readings.md")
        return

    # Each reading, alone, must satisfy the same cite<->source contract as the whole page.
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

    # A source nobody cites in ANY reading is unused; one cited in only some readings is
    # fine, because registers legitimately carry different spans.
    everywhere = set().union(*s.cites.values())
    unused = sorted(s.registry - everywhere)
    if unused:
        f.add(ERROR, "source->cite", f"listed but never cited in any reading: "
                                     f"{', '.join(unused[:8])}")

    # The default register has to render with no script and no :has() evaluation, which
    # means one radio is checked in the markup and <html> mirrors it.
    if not re.search(r'<html[^>]+data-active-reading=', html):
        f.add(WARN, "readings:default",
              "no data-active-reading on <html> — print and any second script have "
              "nothing to read the current register from")
    checked = re.findall(r'<input[^>]*name="reading"[^>]*\bchecked', html)
    if len(checked) != 1:
        f.add(ERROR, "readings:default",
              f"{len(checked)} reading radios carry `checked` in the markup; exactly one "
              "must, or the document has no register with JavaScript off")

    if ledger:
        claims = ledger["claims"]
        by_id = {str(c.get("id")): c for c in claims}

        # A claim that needs a source needs its marker SOMEWHERE in every register it
        # renders in — not in every block that mentions it. A stat row repeating a claim
        # id is supporting furniture; requiring a marker there would report a defect on
        # a page that cites the claim perfectly well two blocks earlier.
        #
        # An inference cites the claims it rests on rather than a source, so it is
        # exempt; a direct claim with no sources already failed the ledger check above.
        renders: dict[tuple[str, str], bool] = {}
        for blk in s.blocks:
            for cid in blk["claims"]:
                c = by_id.get(cid, {})
                if c.get("kind") != "direct" or not c.get("sources"):
                    continue
                for r in blk["readings"]:
                    renders[(cid, r)] = renders.get((cid, r), False) or (r in blk["cited"])

        uncited = sorted(f"{cid} in {r}" for (cid, r), ok_ in renders.items() if not ok_)
        if uncited:
            f.add(ERROR, "cited:per-claim",
                  "claim(s) rendered in a reading that never cites them: "
                  + "; ".join(uncited[:6])
                  + ". Simplifying the words never removes the source")
        elif renders:
            f.ok("cited:per-claim",
                 f"{len(renders)} claim/reading pair(s) each carry a marker")

        for c in claims:
            cid, rd = str(c.get("id")), c.get("readings") or {}
            omit = set(c.get("omit") or [])
            missing = [r for r in READINGS if r not in rd and r not in omit]
            if missing:
                f.add(ERROR, "ledger:readings",
                      f"claim {cid} has no wording for {', '.join(missing)} and does not "
                      "omit them. A register with a silent gap is a different document")
            if omit and not c.get("omitReason"):
                f.add(ERROR, "ledger:readings",
                      f"claim {cid} omits {', '.join(sorted(omit))} with no omitReason")
            # The finding and the ask are the two claims no register may drop.
            if omit and c.get("role") in ("finding", "ask"):
                f.add(ERROR, "ledger:readings",
                      f"claim {cid} is the {c['role']} and may not be omitted from any "
                      "reading — a register without the conclusion is a different report")
        if not any(c.get("readings") for c in claims):
            f.add(WARN, "ledger:readings",
                  "no claim carries a `readings` object; the three registers were written "
                  "into the page rather than derived from the ledger")
        else:
            f.ok("ledger:readings", f"{sum(1 for c in claims if c.get('readings'))} of "
                                    f"{len(claims)} claims carry all three wordings")


# --------------------------------------------------------------------------- dividers

def check_dividers(html: str, f: Findings) -> None:
    """A vertical rule is drawn in a gap, never beside words.

    Source-level only, and deliberately modest about it: the gap a reader perceives runs
    from the text INK to the line, and the padding declared here belongs to a different
    element from the one painting the border. design-review's probeDividerProximity
    measures the rendered ink and is the real gate. What this catches is the cheap,
    common form — a divider declared with no gutter on that side at all.
    """
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    if not css:
        return
    # Strip comments first, or their prose is parsed as a selector and reported as one.
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    findings, unresolved, ok = [], [], 0
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
                    findings.append(
                        f"{sel} sets border-{side} with padding-{side}: {px.group(1)}px "
                        f"(floor is {DIVIDER_FLOOR_PX}px)")
                else:
                    ok += 1
            else:
                unresolved.append(f"{sel} (border-{side}, padding is {pad.group(1).strip()})")

    if findings:
        f.add(ERROR, "divider gutter",
              f"{len(findings)} rule(s) draw a vertical line with no gap beside it: "
              + "; ".join(findings[:4]))
    if unresolved:
        f.add(WARN, "divider gutter",
              f"{len(unresolved)} divider(s) whose gutter is a variable and cannot be "
              "resolved here — confirm with design-review's ink measurement: "
              + "; ".join(unresolved[:3]))
    if ok and not findings:
        f.ok("divider gutter", f"{ok} divider(s) declare a gutter at or above the floor")


# --------------------------------------------------------------------------- theme

def check_theme(html: str, f: Findings) -> None:
    """Light and dark both ship, and print is always light.

    The failure this catches is specific and renders as black on black: a token whose
    ONLY definition sits inside a dark block is undefined when the print rules land, and
    the PDF is the artifact nobody previews before sending.
    """
    has_dark = "prefers-color-scheme: dark" in html or '[data-theme="dark"]' in html
    if not has_dark:
        f.add(ERROR, "theme", "no dark rendering — both themes ship")
        return

    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    root = re.search(r":root\s*\{([^}]*)\}", css)
    base = set(re.findall(r"(--[\w-]+)\s*:", root.group(1))) if root else set()

    dark_only = set()
    for m in re.finditer(r"(?:prefers-color-scheme:\s*dark|\[data-theme=\"dark\"\])[^{]*\{(.*?)\}\s*\}?",
                         css, re.S):
        dark_only |= set(re.findall(r"(--[\w-]+)\s*:", m.group(1)))
    orphan = sorted(dark_only - base)
    if orphan:
        f.add(ERROR, "theme:tokens",
              f"token(s) defined only in a dark block: {', '.join(orphan[:6])}. "
              "They are undefined in print, which renders as ink on ink")
    else:
        # Say so on success too. A check that only ever speaks when it fails is
        # indistinguishable from a check that never ran.
        f.ok("theme", f"light defined unconditionally, {len(dark_only)} token(s) overridden in dark")

    if "@media print" in html:
        printed = re.search(r"@media\s+print\s*\{(.*)", css, re.S)
        if printed and not re.search(r":root[^{]*\{[^}]*--", printed.group(1)):
            f.add(WARN, "theme:print",
                  "the print block does not re-declare the light tokens. A reader in dark "
                  "mode prints dark token values onto a white sheet")
        else:
            f.ok("theme:print", "print re-declares the light tokens")

# --------------------------------------------------------------------------- print

def check_print(html: str, f: Findings) -> None:
    if "@media print" not in html:
        f.add(ERROR, "print", "no @media print block — the PDF will be a printed webpage")
        return

    if not re.search(r"@page\b", html):
        f.add(ERROR, "print:page", "no @page rule — the sheet size is whatever Chrome guesses")
    elif not re.search(r"@page[^{]*\{[^}]*\bA4\b", html, re.S):
        f.add(WARN, "print:page", "@page present but does not name A4")
    else:
        f.ok("print:page", "@page names A4")

    if "break-inside" not in html:
        f.add(ERROR, "print:breaks",
              "no break-inside rules — figures and tables will split across sheets")
    else:
        f.ok("print:breaks", "break-inside rules present")

    if "break-after" not in html:
        f.add(WARN, "print:headings", "no break-after on headings — one may land alone at a page foot")

    # A moving block with no static counterpart prints whatever frame it was on.
    episodes = len(re.findall(r'class="[^"]*\bepisode\b', html))
    statics = len(re.findall(r'class="[^"]*\bepisode-static\b', html))
    if episodes and statics == 0:
        f.add(ERROR, "print:static frame",
              f"{episodes} animated episode(s) with no .episode-static — print gets an arbitrary frame")
    elif episodes:
        f.ok("print:static frame", f"{statics} authored static frame(s) for {episodes} episode(s)")

    if re.search(r'\b\d+vh\b', html):
        f.add(WARN, "print:vh",
              "viewport units in play — meaningless in print, and unstable on mobile browsers")


# --------------------------------------------------------------------------- motion

def check_motion(html: str, f: Findings) -> None:
    if "normalizeScroll" in html:
        f.add(ERROR, "scrolljack",
              "normalizeScroll() forces scrolling onto the JS thread — prohibited")

    if "prefers-reduced-motion" not in html:
        if re.search(r"@keyframes|gsap\.|animate\(", html):
            f.add(ERROR, "reduced-motion", "motion present with no prefers-reduced-motion branch")
    else:
        # Motion-first fails open: a browser without support runs the motion anyway.
        if re.search(r"prefers-reduced-motion:\s*no-preference", html):
            f.ok("reduced-motion", "motion gated behind no-preference — fails safe")
        else:
            f.add(WARN, "reduced-motion",
                  "reduce-branch only. Gate motion behind (prefers-reduced-motion: no-preference) "
                  "so a browser without support keeps the static baseline")


# --------------------------------------------------------------------------- containment

def check_self_contained(path: pathlib.Path, html: str, f: Findings) -> None:
    urls = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
    stray = [u for u in urls if not any(h in u for h in ALLOWED_HOSTS)]
    # Registry links are the point of a registry; they are not assets.
    stray = [u for u in stray if f'href="{u}"' not in html or "<li" not in html.split(u)[0][-200:]]
    assets = [u for u in stray if re.search(r'\.(png|jpe?g|svg|webp|avif|css|js|woff2?)(\?|$)', u)]
    if assets:
        f.add(ERROR, "self-contained", f"external asset(s): {assets[:3]}")
    else:
        f.ok("self-contained", "no external assets off the allowlist")

    if "fonts.googleapis" in html or "fonts.gstatic" in html:
        f.add(WARN, "webfonts",
              "hosted webfont — a live CDN dependency on a document meant to outlast it, and "
              "render-blocking against LCP. Subset and inline, or say so in the methods note")

    kb = len(html.encode()) / 1024
    if kb > 1200:
        f.add(WARN, "weight", f"{kb:.0f} KB — check what is inlined")
    else:
        f.ok("weight", f"{kb:.0f} KB")

    # Referenced local assets. A generated hero arrives at whatever width the model felt
    # like and is usually the largest thing in the directory; it embeds into the PDF at
    # full size, so an unresized image costs every reader who is sent the attachment.
    d = path.parent
    refs = {m for m in re.findall(r'(?:src|href)="(?!https?:|#|data:)([^"]+)"', html)
            if re.search(r'\.(png|jpe?g|webp|avif|gif|svg)$', m, re.I)}
    heavy = []
    for r in refs:
        a = (d / r)
        if a.exists() and a.stat().st_size > 300 * 1024:
            heavy.append(f"{r} ({a.stat().st_size/1024:.0f} KB)")
    if heavy:
        f.add(WARN, "assets",
              f"image(s) over 300KB: {', '.join(heavy[:3])} — resize to display width; "
              "they embed into the PDF at full size")
    elif refs:
        f.ok("assets", f"{len(refs)} local image(s), all under 300KB")

    figs = len(re.findall(r"<figure", html))
    canvases = len(re.findall(r"<canvas", html))
    svgs = len(re.findall(r"<svg", html))
    if canvases and not svgs:
        f.add(WARN, "no-js figures",
              "canvas charts with no inline SVG or table — absent without script, and absent in print")


# --------------------------------------------------------------------------- a11y + head

def check_a11y(html: str, f: Findings) -> None:
    imgs = re.findall(r"<img\b(?![^>]*\balt=)[^>]*>", html)
    if imgs:
        f.add(ERROR, "a11y:alt", f"{len(imgs)} <img> with no alt attribute")

    if not re.search(r"<html[^>]+lang=", html):
        f.add(ERROR, "a11y:lang", "<html> has no lang attribute")

    if not re.search(r"<h1", html):
        f.add(ERROR, "structure", "no <h1>")

    if not re.search(r":focus-visible", html):
        f.add(WARN, "a11y:focus", "no :focus-visible styles — keyboard users lose the cursor")

    for pat, label in ((r"<title>", "<title>"), (r'name="description"', "meta description"),
                       (r'property="og:title"', "og:title")):
        if not re.search(pat, html):
            f.add(WARN, "head", f"missing {label}")


def check_conclusion_first(html: str, f: Findings) -> None:
    """The finding belongs in the first screen. Roughly: inside the first block."""
    body = html.split("<body", 1)[-1]
    head_slice = body[:6000]
    if re.search(r'class="[^"]*\b(tldr|finding|standfirst|lede|bottom-line)\b', head_slice):
        f.ok("conclusion first", "a finding element appears in the opening block")
    else:
        f.add(WARN, "conclusion first",
              "no tldr/finding/standfirst element near the top — median scroll depth is about "
              "half the page, so a withheld conclusion is written for readers who never arrive")


# --------------------------------------------------------------------------- main

def audit_file(path: pathlib.Path, ledger, f: Findings, *, full: bool) -> None:
    html = path.read_text(errors="ignore")
    check_citations(html, ledger if full else None, f)
    check_readings(html, ledger if full else None, f)
    check_dividers(html, f)
    check_theme(html, f)
    check_print(html, f)
    check_motion(html, f)
    check_self_contained(path, html, f)
    check_a11y(html, f)
    if full:
        check_conclusion_first(html, f)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    target = pathlib.Path(sys.argv[1]).resolve()
    d = target if target.is_dir() else target.parent

    f = Findings()
    ledger = load_ledger(d, f)

    # A tldr-only run is a legitimate shape, so the required set is what any run owes:
    # the ledger it argued from, the system it was designed against, and at least one
    # document with its PDF. Requiring all six would fail `/report tldr` against its own
    # gate, which is how a gate starts getting ignored.
    always = ["DESIGN.md", "claims.json"]
    missing = [n for n in always if not (d / n).exists()]

    pairs = [("index.html", "report.pdf"), ("tldr.html", "tldr.pdf")]
    present = [(h, p) for h, p in pairs if (d / h).exists()]
    if not present:
        missing.append("index.html or tldr.html")
    for h, p in present:
        if not (d / p).exists():
            missing.append(f"{p} (its {h} exists, so the PDF was expected)")

    if missing:
        f.add(ERROR, "outputs", f"missing: {', '.join(missing)}")
    else:
        f.ok("outputs", ", ".join(always + [n for pair in present for n in pair]))

    for name, full in (("index.html", True), ("tldr.html", False)):
        p = d / name
        if p.exists():
            f.add(PASS, "----", f"{name}")
            audit_file(p, ledger, f, full=full)

    print(f"\n=== REPORT AUDIT — {d} ===\n")
    for level, check, detail in f.rows:
        if check == "----":
            print(f"\n  -- {detail} --")
            continue
        mark = {PASS: "ok  ", ERROR: "FAIL", WARN: "warn"}[level]
        print(f"{mark}  {check.ljust(20)} {detail}")

    errs = sum(1 for l, _, _ in f.rows if l == ERROR)
    warns = sum(1 for l, _, _ in f.rows if l == WARN)
    print(f"\n{errs} error(s), {warns} warning(s)\n")
    return 1 if f.failed else 0


if __name__ == "__main__":
    sys.exit(main())
