#!/usr/bin/env python3
"""lint_email.py - the deterministic gate on a generated digest email.

Every rule here traces to a row in references/evidence.md. Rules are grouped by
what they protect, and each carries the class of evidence behind it, because a
gate sourced to a controlled test and a gate sourced to a convention should not
fail the same way:

    ERROR   the rule has primary or measured backing, and breaking it breaks
            the email for a nameable population
    WARN    the rule is convention, or the evidence is contested, or the fix is
            a judgement call

This is the email-medium half of the gate. The reading-surface half is
ux-craft's ux-lint.py, and the two are meant to run together: contrast and
touch-target size are deliberately absent here because ux-lint.py already
resolves them properly, and a second implementation would only mean two gates
disagreeing about one standard. Two of its checks do not transfer to email
(no-focus-visible, because Gmail's allowlist has no pseudo-class support, and
state-coverage, because an email has no states); report those as not-applicable
rather than suppressing them.

The single most important thing this script does NOT do is cap the item count.
That is asserted as an anti-rule (see check_no_item_cap) because the intuitive
fix for an unreadable digest is fewer items, the largest dataset available says
the opposite, and a cap re-enters the code every time somebody reasons from
first principles instead of reading the evidence.

Usage:
    python3 lint_email.py email.html [--text email.txt] [--json] [--strict]

    --text    the plain-text MIME part, checked for parity with the HTML
    --json    machine-readable findings
    --strict  warnings become errors

Exit 0 clean, 1 on any error (or any warning under --strict).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ERROR, WARN, OK = "error", "warn", "ok"

# Gmail clips at ~102KB of HTML. The threshold is practitioner-observed across
# Mailchimp, Litmus and Klaviyo and documented by Google nowhere, so the budget
# leaves room for the ESP's own tracking rewrite, which lands after this runs.
CLIP_HARD = 102_400
BUDGET_FAIL = 92_160      # 90KB
BUDGET_WARN = 81_920      # 80KB

# Outlook.com's partial inversion targets these two values specifically rather
# than reacting to lightness, so near-black and near-white sidestep it.
PURE = re.compile(r"#(?:fff(?:fff)?|000(?:000)?)\b", re.I)

# Properties the Word engine ignores or mangles, and properties absent from
# Gmail's published allowlist. Permitted only inside an mso conditional guard.
UNSAFE_CSS = (
    "display:flex", "display:grid", "display:inline-flex",
    "flex-direction", "justify-content", "align-items", "flex-wrap", "gap:",
    "grid-template", "position:absolute", "position:fixed", "position:sticky",
    "transform:", "transition:", "animation:", "float:",
)

GENERIC_LINK = re.compile(
    r"^\s*(click here|read more|learn more|more|here|link|this|read on|"
    r"find out more|see more)\s*[.!>→]*\s*$", re.I)

WEB_SAFE = (
    "arial", "helvetica", "verdana", "georgia", "times", "times new roman",
    "courier", "courier new", "tahoma", "trebuchet", "trebuchet ms", "palatino",
    "garamond", "sans-serif", "serif", "monospace", "system-ui", "-apple-system",
    "blinkmacsystemfont", "segoe ui", "roboto", "ui-monospace",
)


class Findings:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []

    def add(self, level: str, rule: str, msg: str, basis: str) -> None:
        self.rows.append((level, rule, msg, basis))

    def ok(self, rule: str, msg: str, basis: str = "") -> None:
        self.add(OK, rule, msg, basis)

    @property
    def errors(self) -> int:
        return sum(1 for r in self.rows if r[0] == ERROR)

    @property
    def warns(self) -> int:
        return sum(1 for r in self.rows if r[0] == WARN)


class Doc(HTMLParser):
    """One pass, because several checks need the same structural facts.

    Tracks the heading outline, the table stack (role is not inherited, so a
    nested layout table needs its own), images with their attributes, links with
    their visible text, and the text nodes that appear before the first item
    block."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.headings: list[tuple[int, str]] = []
        self.tables: list[dict] = []
        self.images: list[dict] = []
        self.links: list[dict] = []
        self.text_before_items = ""
        self.paras_before_items: list[str] = []
        self._p: list[str] | None = None
        self.seen_first_item = False
        self.tiers: dict[str, int] = {"featured": 0, "spotlight": 0, "oneline": 0}
        self.summary_items = 0
        self._h: list[tuple[int, list]] = []
        self._a: list[dict] | None = None
        self._in_summary = False
        self._in_style = False
        self.style_text = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "") + " " + (a.get("data-tier") or "")
        if tag == "style":
            self._in_style = True
        if tag == "table":
            self.tables.append({"role": a.get("role"), "line": self.getpos()[0]})
        if tag == "img":
            self.images.append({**a, "line": self.getpos()[0]})
        if tag == "a":
            self._a = {**a, "text": [], "line": self.getpos()[0]}
        if re.fullmatch(r"h[1-6]", tag):
            self._h.append((int(tag[1]), []))
        for t in ("featured", "spotlight", "oneline"):
            if re.search(rf"\b(?:tier-)?{t}\b", cls):
                self.tiers[t] += 1
                self.seen_first_item = True
        if tag == "p" and not self.seen_first_item and not self._in_summary:
            self._p = []
        if re.search(r"\bsummary\b", cls):
            self._in_summary = True
        if self._in_summary and tag == "li":
            self.summary_items += 1

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
        if tag == "p" and self._p is not None:
            self.paras_before_items.append("".join(self._p).strip())
            self._p = None
        if tag == "a" and self._a is not None:
            self._a["text"] = "".join(self._a["text"]).strip()
            self.links.append(self._a)
            self._a = None
        if re.fullmatch(r"h[1-6]", tag) and self._h:
            lvl, buf = self._h.pop()
            self.headings.append((lvl, "".join(buf).strip()))
        if re.search(r"\bsummary\b", tag):
            self._in_summary = False

    def handle_data(self, data):
        if self._in_style:
            self.style_text += data
            return
        if self._a is not None:
            self._a["text"].append(data)
        for _, buf in self._h:
            buf.append(data)
        if self._p is not None:
            self._p.append(data)
        if not self.seen_first_item:
            self.text_before_items += data


# ── structure ────────────────────────────────────────────────────────────────

def check_no_item_cap(doc: Doc, f: Findings) -> None:
    """An anti-rule, asserted so it cannot be quietly reintroduced.

    MailerLite's 317,000 campaigns and 2.9bn emails put the 21+ link bucket at
    the highest click-to-open rate in the dataset (6.72%), and the choice-overload
    meta-analysis pools to a mean effect size of virtually zero. There is no
    measured ceiling. The defect in a flat list is undifferentiated scan cost per
    item, which tiering fixes and truncation does not."""
    total = sum(doc.tiers.values())
    if total == 0:
        f.add(ERROR, "tiers",
              "no tiered items found. Mark each item block with a tier class or "
              "data-tier of featured / spotlight / oneline, or this gate and every "
              "tier rule below is measuring nothing",
              "measured: undifferentiated scan cost is the defect")
        return
    f.ok("no-item-cap",
         f"{total} items, no cap enforced (by design)",
         "measured: MailerLite 21+ links highest CTOR 6.72%; choice-overload null")


def check_tier_shape(doc: Doc, f: Findings) -> None:
    fe, co, ol = doc.tiers["featured"], doc.tiers["spotlight"], doc.tiers["oneline"]
    if not (2 <= fe <= 4):
        f.add(ERROR, "tier:featured",
              f"{fe} featured item(s); 2 to 4, default 2. Prominence is the only "
              "part of this layout with causal evidence behind it, and it stops "
              "being prominence when everything has it",
              "measured: Kong et al. detail-reading 13%->22%")
    else:
        f.ok("tier:featured", f"{fe} featured", "measured: Kong et al.")

    if co and not (2 <= co <= 5):
        f.add(WARN, "tier:spotlight",
              f"{co} spotlight item(s); 2 to 5, and three is what the row is "
              "built around. The middle tier carries imagery at reduced width, "
              "so it costs both attention and bytes in a way the one-line tail "
              "does not, and past three the columns are too narrow for a banner",
              "convention, bounded by the scan budget and image weight")
    else:
        f.ok("tier:spotlight", f"{co} spotlight")

    if fe + co + ol >= 12 and ol == 0:
        f.add(ERROR, "tier:tail",
              "a long issue with no one-line tier. Everything past the spotlight "
              "band compresses to title-only, which is what lets the item count "
              "stay uncapped",
              "measured: scan budget; no item ceiling")
    else:
        f.ok("tier:tail", f"{ol} one-liners")

    # No run of full-treatment cards long enough to read as a flat list.
    if fe > 4:
        f.add(ERROR, "tier:flat",
              "more than four consecutive full-treatment items reproduces the "
              "flat list this layout exists to replace",
              "measured: scan cost")


def check_summary(doc: Doc, html: str, f: Findings) -> None:
    """Three highlights, not a contents list, and never internally anchored."""
    n = doc.summary_items
    if n and n > 4:
        f.add(ERROR, "summary:size",
              f"summary carries {n} entries. Three highlights plus category "
              "counts; reproducing every title recreates the flat list above the "
              "flat list",
              "convergent across all four backends")
    elif n:
        f.ok("summary:size", f"{n} highlights")

    total = sum(doc.tiers.values())
    if total and n and n > total * 0.25:
        f.add(WARN, "summary:ratio",
              f"summary repeats {n} of {total} titles (>25%)",
              "convention")

    anchors = [a for a in doc.links if (a.get("href") or "").startswith("#")]
    if anchors:
        f.add(ERROR, "summary:anchors",
              f"{len(anchors)} internal anchor link(s). They do not act in Apple "
              "Mail, Gmail, Outlook or Yahoo on iPhone or iPad, and Apple is "
              "62.26% of opens; they also bypass ESP redirect tracking, so the "
              "block cannot be measured even where it works",
              "measured: client testing + Litmus share")
    else:
        f.ok("summary:anchors", "no internal anchors",
             "measured: anchors fail across iOS")


def check_prose_intro(doc: Doc, f: Findings) -> None:
    """67% of readers had zero fixations on three-line newsletter intros."""
    # Only a real paragraph counts. Measuring every text node before the first
    # item swept in the masthead, the h1 and the summary bullets and reported
    # 495 characters of "prose" on a template carrying none.
    paras = [p for p in doc.paras_before_items if len(p) > 40]
    longest = max((len(p) for p in paras), default=0)
    if longest > 180:
        f.add(ERROR, "prose-intro",
              f"a {longest}-character paragraph before the first item. A "
              "prose introduction is the block two-thirds of readers never look "
              "at, and it costs both vertical space and clip budget",
              "measured: NN/g 67% zero fixations")
    else:
        f.ok("prose-intro", "no prose block ahead of the items",
             "measured: NN/g 67% zero fixations")


def check_headings(doc: Doc, f: Findings) -> None:
    levels = [l for l, _ in doc.headings]
    h1 = levels.count(1)
    if h1 != 1:
        f.add(ERROR, "headings:h1", f"{h1} <h1>; exactly one",
              "measured: WebAIM 71.6% navigate by headings")
    prev = 0
    for lvl in levels:
        if prev and lvl > prev + 1:
            f.add(ERROR, "headings:skip",
                  f"heading level jumps h{prev} to h{lvl}. Tier boundaries are "
                  "the screen-reader equivalent of visual tiering; a tier built "
                  "from styled divs gives sighted readers the benefit and screen "
                  "reader users nothing",
                  "measured: WebAIM 71.6%")
            break
        prev = lvl
    else:
        if h1 == 1:
            f.ok("headings", f"{len(levels)} headings, outline intact",
                 "measured: WebAIM 71.6%")


# ── rendering ────────────────────────────────────────────────────────────────

def check_tables(doc: Doc, f: Findings) -> None:
    bare = [t for t in doc.tables if (t["role"] or "").lower() not in ("presentation", "none")]
    if bare:
        lines = ", ".join(str(t["line"]) for t in bare[:6])
        f.add(ERROR, "a11y:table-role",
              f"{len(bare)} of {len(doc.tables)} layout table(s) missing "
              f'role="presentation" (line {lines}). The role is not inherited, so '
              "every nested table needs its own, and without it a screen reader "
              "announces row and column positions for visual scaffolding",
              "measured: EMC 86.24% of emails fail this")
    elif doc.tables:
        f.ok("a11y:table-role", f"all {len(doc.tables)} tables marked presentational",
             "measured: EMC 86.24% failure rate")


def check_css(html: str, f: Findings) -> None:
    # Anything inside an mso conditional is Outlook-only by construction.
    stripped = re.sub(r"<!--\[if[^\]]*\]>.*?<!\[endif\]-->", " ", html, flags=re.S | re.I)
    flat = re.sub(r"\s+", "", stripped.lower())
    # Word-boundary on the left, because `text-transform` is safe and contains
    # `transform`, and `grid-template-columns` inside a comment is not a layout
    # dependency. A bare substring test failed a clean template on both.
    hits = sorted({p for p in UNSAFE_CSS
                   if re.search(r"(?<![\w-])" + re.escape(p.replace(" ", "")), flat)})
    if hits:
        f.add(ERROR, "css:unsafe",
              f"{', '.join(hits)} outside an mso guard. Outlook renders through "
              "the Word engine and Gmail publishes an allowlist that excludes "
              "every one of these; layout must survive without them",
              "primary: Gmail CSS docs + Microsoft Word engine model")
    else:
        f.ok("css:unsafe", "no layout dependency on modern CSS",
             "primary: Gmail allowlist")

    if re.search(r"<svg\b", stripped, re.I):
        f.add(ERROR, "css:svg",
              "<svg> present. Gmail strips the tag from the DOM entirely, so a "
              "vector mark does not degrade, it vanishes. Rasterise to PNG",
              "vendor documentation")
    else:
        f.ok("css:svg", "no SVG", "vendor documentation")

    pures = PURE.findall(stripped)
    if pures:
        f.add(WARN, "css:pure-values",
              f"{len(pures)} use(s) of pure #FFFFFF/#000000. Outlook.com's partial "
              "inversion targets these two values specifically rather than "
              "reacting to lightness, so near-black and near-white sidestep it",
              "heuristic against an undocumented detection rule")
    else:
        f.ok("css:pure-values", "no pure black or white",
             "heuristic, widely corroborated")


def check_dark_mode(html: str, f: Findings) -> None:
    """The meta tags are a commitment. Apple leaves markup alone without them
    and partially inverts with them and no dark styles."""
    has_meta = re.search(r'name="(?:supported-)?color-scheme"', html, re.I) is not None
    has_dark = re.search(r"prefers-color-scheme\s*:\s*dark", html, re.I) is not None
    if has_meta and not has_dark:
        f.add(ERROR, "dark:commitment",
              "colour-scheme meta present with no prefers-color-scheme:dark "
              "block. Apple Mail leaves colours untouched when the tags are "
              "absent but partially inverts when they are present without dark "
              "styles, so declaring support you have not built is worse than "
              "declaring none",
              "measured: Litmus dark-mode guidance")
    else:
        f.ok("dark:commitment",
             "meta tags and dark styles agree" if has_meta else "no dark-mode claim made",
             "measured: Litmus")


def check_quoted_attrs(html: str, f: Findings) -> None:
    """A double quote inside a double-quoted style attribute ends it early.

    Total, silent, and invisible to every other check here. A font stack written
    `font-family:"Instrument Sans", ...` inside `style="..."` closes the
    attribute at the first inner quote; the browser keeps the truncated
    declaration, discards everything after it, and renders a fallback face at a
    size nobody set. This shipped once in this renderer's own history, and
    `fonts:fallback` passed it because that check reads the raw text rather than
    the parsed attribute. Single quotes are valid CSS and are the fix."""
    bad = re.findall(r'style="[^"]*"[^\s>=/]', html)
    if bad:
        f.add(ERROR, "css:quoted-attr",
              f"{len(bad)} style attribute(s) closed early by a double quote "
              f"inside the value ({bad[0][:60]!r}). Every declaration after it "
              "is discarded, and nothing else here can see it. Use single "
              "quotes inside font stacks and content values",
              "spec: HTML attribute delimiting")
    else:
        f.ok("css:quoted-attr", "no style attribute closed early by its own value")

def check_fonts(html: str, f: Findings) -> None:
    # Quotes are legal inside a stack ("Segoe UI"), so the capture must run to
    # the declaration terminator. Stopping at the first quote truncated every
    # system stack mid-list and reported 59 false failures on a clean template.
    stacks = re.findall(r"font-family\s*:\s*([^;}]+)", html, re.I)
    bad = []
    for s in stacks:
        last = s.split(",")[-1].strip().strip("'\"").lower()
        if last not in WEB_SAFE:
            bad.append(s.strip()[:52])
    if bad:
        f.add(ERROR, "fonts:fallback",
              f"{len(bad)} font stack(s) not ending in a web-safe family "
              f"({bad[0]}). Outlook falls back to Times New Roman rather than to "
              "the next font in the stack",
              "measured: Litmus web font support")
    elif stacks:
        f.ok("fonts:fallback", f"all {len(stacks)} stacks end web-safe",
             "measured: Litmus")

    if re.search(r"@font-face", html, re.I) and not re.search(r"mso-font-alt", html, re.I):
        f.add(WARN, "fonts:mso-alt",
              "@font-face without mso-font-alt, which is what stops Outlook "
              "dropping to Times New Roman",
              "practitioner")


def check_size(html: str, f: Findings) -> None:
    n = len(html.encode("utf-8"))
    kb = n / 1024
    if re.search(r'src="data:image', html, re.I):
        f.add(ERROR, "size:base64",
              "base64 image data in the HTML. Remote images do not count against "
              "the clip threshold and embedded ones do, so inlining an image "
              "spends the one budget that matters",
              "measured: clip applies to HTML only")
    if n >= BUDGET_FAIL:
        f.add(ERROR, "size:budget",
              f"{kb:.1f}KB of HTML against a {BUDGET_FAIL/1024:.0f}KB budget. Gmail "
              f"clips near {CLIP_HARD/1024:.0f}KB, truncating mid-markup and "
              "potentially hiding the unsubscribe link; the gap is headroom for "
              "the ESP's tracking rewrite, which lands after this runs",
              "practitioner-verified across three vendors, undocumented by Google")
    elif n >= BUDGET_WARN:
        f.add(WARN, "size:budget", f"{kb:.1f}KB, approaching the clip threshold",
              "practitioner")
    else:
        f.ok("size:budget", f"{kb:.1f}KB of HTML", "practitioner")


# ── images and links ─────────────────────────────────────────────────────────

def check_images(doc: Doc, f: Findings) -> None:
    missing = [i for i in doc.images if "alt" not in i]
    if missing:
        f.add(ERROR, "a11y:alt",
              f"{len(missing)} image(s) with no alt attribute (line "
              f"{missing[0]['line']}). Decorative images take alt=\"\" so a screen "
              "reader skips them; omitting the attribute is not the same thing",
              "measured: EMC 51.42% of emails fail this")
    else:
        f.ok("a11y:alt", f"all {len(doc.images)} images carry alt",
             "measured: EMC 51.42% failure rate")

    nodim = [i for i in doc.images if not (i.get("width") and i.get("height"))]
    if nodim:
        f.add(WARN, "img:dimensions",
              f"{len(nodim)} image(s) without width and height attributes",
              "convention: reduces layout shift, and Outlook needs the width")

    banners = [i for i in doc.images
               if re.search(r"\bbanner\b", (i.get("class") or "") + (i.get("data-role") or ""))]
    if len(banners) > 6:
        f.add(WARN, "img:banners",
              f"{len(banners)} banner images. The clip threshold counts HTML "
              "only, so banners do not push you toward it; what they cost is "
              "load time on a metered connection and attention against the tier "
              "below. There is no measured ceiling, which is why this warns",
              "convention: no measurement located")
    else:
        f.ok("img:banners", f"{len(banners)} banner(s)",
             "count is unconstrained by the clip budget, which is HTML-only")


def check_links(doc: Doc, f: Findings) -> None:
    generic = [a for a in doc.links if GENERIC_LINK.match(a.get("text") or "")]
    if generic:
        f.add(ERROR, "a11y:link-text",
              f"{len(generic)} link(s) with generic text "
              f"({generic[0].get('text')!r}). Screen readers can list every link "
              "in isolation, and a list of \"Read more\" is useless",
              "measured: EMC 72.04% of emails fail this")
    else:
        f.ok("a11y:link-text", f"all {len(doc.links)} links descriptive",
             "measured: EMC 72.04% failure rate")

    empty = [a for a in doc.links if not (a.get("text") or "").strip()
             and not any(i.get("alt") for i in doc.images)]
    if empty:
        f.add(WARN, "a11y:link-empty", f"{len(empty)} link(s) with no discernible text",
              "measured: EMC")


def check_alignment(html: str, f: Findings) -> None:
    """Body text is left-aligned.

    Centred running text degrades readability, most sharply for dyslexic
    readers, by giving every line an unpredictable starting point. It is also
    the easiest defect to introduce by accident: the outer align="center" that
    centres the card in the viewport cascades text-align into every descendant,
    so a template can be centred throughout without anyone writing
    text-align:center once. That is exactly how it reached a render here."""
    body = re.search(r"<body\b.*?</body>", html, re.S | re.I)
    if not body:
        return
    inner = body.group(0)
    centred = len(re.findall(r'text-align\s*:\s*center|align="center"', inner, re.I))
    reset = len(re.findall(r'text-align\s*:\s*left|align="left"', inner, re.I))
    if centred and reset < centred:
        f.add(ERROR, "a11y:alignment",
              f"{centred} centring declaration(s) against {reset} left reset(s). "
              "Centred running text gives every line a different starting point; "
              "a card centred with align=\"center\" must reset text-align on the "
              "card or the whole email inherits it",
              "measured: accessibility guidance, corroborated across the panel")
    else:
        f.ok("a11y:alignment", f"{reset} left alignment(s) cover {centred} centring(s)",
             "measured: accessibility guidance")


def check_unsubscribe(html: str, f: Findings) -> None:
    visible = re.search(r"unsubscrib", html, re.I) is not None
    if not visible:
        f.add(ERROR, "deliver:unsubscribe",
              "no visible unsubscribe link in the body. Google requires one for "
              "bulk senders in addition to the RFC 8058 headers, and Gmail's clip "
              "can hide a footer-only link",
              "primary: Google sender guidelines, effective 2024-02-01")
    else:
        f.ok("deliver:unsubscribe", "visible unsubscribe present",
             "primary: Google sender guidelines")


def check_images_off(html: str, doc: Doc, f: Findings) -> None:
    """Strip every image and assert the email still carries its content.

    The banner's failure modes (blocked, broken, width-clipped alt, unstylable
    alt) all land on the same element, and they take the AI-generated inbox
    summary with them. So the headline lives beside the image, never inside it."""
    stripped = re.sub(r"<img\b[^>]*>", "", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", stripped)
    words = len(text.split())
    if words < 40:
        f.add(ERROR, "images-off",
              f"only {words} words survive with images stripped. Every title, "
              "description and call to action must be live HTML text",
              "measured: Outlook blocks by default and cannot style alt text")
        return
    links_left = len(re.findall(r"<a\b", stripped, re.I))
    if doc.links and links_left < len(doc.links) * 0.8:
        f.add(WARN, "images-off",
              f"{len(doc.links) - links_left} link(s) exist only as images",
              "measured: image blocking")
    else:
        f.ok("images-off", f"{words} words and {links_left} links survive image blocking",
             "measured: Outlook default blocking")


def check_text_part(html: str, text: pathlib.Path | None, f: Findings) -> None:
    if text is None:
        f.add(WARN, "mime:text",
              "no plain-text part supplied to check. A complete text/plain "
              "alternative is required for accessibility and for clients that "
              "select it",
              "convention + accessibility")
        return
    body = text.read_text(encoding="utf-8", errors="replace")
    urls_html = set(re.findall(r'href="(https?://[^"#]+)"', html))
    urls_text = set(re.findall(r"https?://\S+", body))
    missing = {u for u in urls_html if not any(u.rstrip("/") in t for t in urls_text)}
    # Tracking rewrites legitimately differ between parts; report, do not fail.
    if len(missing) > len(urls_html) * 0.5:
        f.add(WARN, "mime:parity",
              f"{len(missing)} of {len(urls_html)} HTML destinations absent from "
              "the text part",
              "convention")
    else:
        f.ok("mime:parity", f"text part carries {len(urls_text)} destinations")


def check_subject(args, f: Findings) -> None:
    """Length is a truncation constraint, not a performance lever.

    Three large practitioner datasets give three different optima (about 30, 45
    and over 70 characters) and an academic study across 455 million users found
    no direct relation between subject length and attention. So this warns and
    never fails, and the rule that does fail is the count-only one, because a
    bare count sets a scope expectation without a relevance one."""
    s = (args.subject or "").strip()
    if not s:
        f.add(WARN, "subject", "no --subject supplied, subject rules not run", "")
        return
    if re.fullmatch(r"\d+\s+new\s+\w+!?", s, re.I):
        f.add(ERROR, "subject:count-only",
              f"{s!r} is a bare count. The only causal evidence available shows "
              "that naming a relevant item raises that item's detail-reading; a "
              "number alone tells the reader how much work is coming and nothing "
              "about whether any of it matters",
              "measured: Kong et al. 15%->24% on the named item")
    elif len(s) > 70:
        f.add(WARN, "subject:length", f"{len(s)} characters; front-load the value",
              "contested: three datasets give three optima")
    else:
        f.ok("subject", f"{len(s)} characters, names something specific",
             "measured: Kong et al.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("--text", type=pathlib.Path, default=None)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    html = args.html.read_text(encoding="utf-8", errors="replace")
    doc = Doc()
    doc.feed(html)

    f = Findings()
    check_no_item_cap(doc, f)
    check_tier_shape(doc, f)
    check_summary(doc, html, f)
    check_prose_intro(doc, f)
    check_headings(doc, f)
    check_tables(doc, f)
    check_css(html, f)
    check_dark_mode(html, f)
    check_quoted_attrs(html, f)
    check_fonts(html, f)
    check_size(html, f)
    check_images(doc, f)
    check_links(doc, f)
    check_alignment(html, f)
    check_unsubscribe(html, f)
    check_images_off(html, doc, f)
    check_text_part(html, args.text, f)
    check_subject(args, f)

    if args.json:
        print(json.dumps([{"level": l, "rule": r, "message": m, "basis": b}
                          for l, r, m, b in f.rows], indent=2))
    else:
        width = max(len(r[1]) for r in f.rows)
        for level, rule, msg, basis in f.rows:
            tag = {ERROR: "FAIL", WARN: "warn", OK: "ok  "}[level]
            print(f"{tag}  {rule.ljust(width)}  {msg}")
            if basis and level != OK:
                print(f"      {' ' * width}  └─ {basis}")
        print(f"\n{f.errors} error(s), {f.warns} warning(s)")
        if f.errors == 0 and f.warns == 0:
            print("\nGates pass. They prove the email renders and is reachable;\n"
                  "only reading it proves it is worth reading.")

    return 1 if f.errors or (args.strict and f.warns) else 0


if __name__ == "__main__":
    raise SystemExit(main())
