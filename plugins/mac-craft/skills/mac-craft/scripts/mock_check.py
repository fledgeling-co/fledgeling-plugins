#!/usr/bin/env python3
"""mock_check.py — the deterministic gate for a macOS interface mockup authored as HTML.

Why this file exists, stated once
--------------------------------
This skill's predecessor listed seven audits in prose. On one recorded run
(`Egress Gemini`, 2026-08-17) the model reported all five of its surfaces as PASS in a
self-authored review, named a browser engine that failed on all four invocation
attempts and never ran, and claimed "100% pass rate on contrast (>=4.5:1 on text)".
Measured afterwards: every primary button 3.65:1, every selected sidebar row 3.65:1,
and one `+` glyph at **1.00:1** — the same colour as its own background.

An instruction-only rule in this pipeline has a measured history of being reported as
satisfied without being performed. So the checks live here, with an exit code.

Stdlib only, Python 3.9+. No browser, no network, no third-party package. That is
deliberate: this house's only sanctioned browser (Obscura) never executes CSS
animations or transitions, never loads web fonts, ignores `setEmulatedMedia`, returns
`0px`/`""` for shorthand computed styles while longhands are correct, and returns the
element's own style when asked for a pseudo-element's. A gate built on it would report
zeros that read as passes. This one reads the source instead, and where the source does
not settle a question it says `UNMEASURED` and refuses rather than scoring zero.

The one invariant every check obeys
-----------------------------------
**`examined=0` is a gate that never ran, and is never recorded as a pass.** A check that
examined nothing exits non-zero with `UNMEASURED` and the reason. Silence is not success.

Verdicts
--------
  FAIL  -> stdout, exit 1. Structural breakage or a measured floor violation.
  NOTE  -> stderr, exit 0 contribution. Degradation you should know about.
  UNMEASURED -> stdout, exit 2. The check could not be performed; nothing is claimed.

Anything on stderr is a warning to read. Check the exit code, never the output: piping
this through `grep` makes `$?` grep's status and not the gate's, which is exactly how a
failure gets read as a pass.

Usage
-----
  python3 mock_check.py <mock.html> [--json] [--interactive|--static] [--allow-name]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# --------------------------------------------------------------------------------------
# Kit ground truth. Values marked (specified) in references/native-foundation.md, which
# derives them from Apple's macOS 27 UI kit deconstructed from its Sketch JSON. A value
# here is the published number; the metric block in a mock is checked against it.
# --------------------------------------------------------------------------------------

KIT_METRICS = {
    "titlebar": (33, "pt"),
    "unified-toolbar": (52, "pt"),
    "toolbar-compact": (40, "pt"),
    "toolbar-expanded": (77, "pt"),
    "control-mini": (16, "pt"),
    "control-small": (20, "pt"),
    "control-regular": (24, "pt"),
    "control-large": (28, "pt"),
    "control-xl": (36, "pt"),
    "body-type": (13, "pt"),
    "sidebar": (256, "pt"),
    "sidebar-row-small": (24, "pt"),
    "sidebar-row-medium": (32, "pt"),
    "sidebar-row-large": (40, "pt"),
    "selection-radius": (8, "pt"),
    "popover-radius": (20, "pt"),
    "scrollbar": (12, "pt"),
}

# Where a metric may legitimately come from. A row tagged nothing is a value invented.
VALID_TIERS = {"kit", "hig", "corpus", "direction", "research", "brand"}

# Metrics the native envelope owns: a `direction` tag on one of these is a defect, not a
# style choice. Chrome geometry is not inside the envelope a direction may set.
ENVELOPE_LOCKED = {
    "titlebar",
    "unified-toolbar",
    "toolbar-compact",
    "toolbar-expanded",
    "control-mini",
    "control-small",
    "control-regular",
    "control-large",
    "control-xl",
    "body-type",
    "sidebar-row-small",
    "sidebar-row-medium",
    "sidebar-row-large",
    "scrollbar",
}

# P24: the artifact is named from the content. These names name the tool or nothing.
GENERIC_NAMES = {
    "mock", "mockup", "design", "index", "untitled", "new", "page", "main",
    "app", "window", "ui", "macos", "mac", "screen", "output", "test", "demo",
    "prototype", "wireframe", "draft", "final", "v1", "v2", "temp", "tmp",
    "mac-mock", "app-mock", "ui-mock", "design-mock", "macos-mock", "mock-1",
}

# The 12 system hues `(specified)`, light / dark. Used to tell a designer's low-contrast
# accident apart from the platform's own published value — which is a different finding
# with a different fix, and conflating the two is how "the platform does it" becomes a
# licence to ship 3.5:1 text.
SYSTEM_HUES = {
    "#ff383c": "Red", "#ff4245": "Red (dark)",
    "#ff8d28": "Orange", "#ff9230": "Orange (dark)",
    "#ffcc00": "Yellow", "#ffd600": "Yellow (dark)",
    "#34c759": "Green", "#30d158": "Green (dark)",
    "#00c8b3": "Mint", "#00dac3": "Mint (dark)",
    "#00c3d0": "Teal", "#00d2e0": "Teal (dark)",
    "#00c0e8": "Cyan", "#3cd3fe": "Cyan (dark)",
    "#0088ff": "Blue", "#0091ff": "Blue (dark)",
    "#6155f5": "Indigo", "#6d7cff": "Indigo (dark)",
    "#cb30e0": "Purple", "#db34f2": "Purple (dark)",
    "#ff2d55": "Pink", "#ff375f": "Pink (dark)",
    "#ac7f5e": "Brown", "#b78a66": "Brown (dark)",
}

NAMED_COLOURS = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
    "green": (0, 128, 0), "blue": (0, 0, 255), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "silver": (192, 192, 192), "maroon": (128, 0, 0),
    "olive": (128, 128, 0), "lime": (0, 255, 0), "aqua": (0, 255, 255),
    "cyan": (0, 255, 255), "teal": (0, 128, 128), "navy": (0, 0, 128),
    "fuchsia": (255, 0, 255), "magenta": (255, 0, 255), "purple": (128, 0, 128),
    "yellow": (255, 255, 0), "orange": (255, 165, 0),
}

# Elements whose text is not rendered, so their colour is not a contrast pair.
NON_RENDERING = {"script", "style", "head", "title", "meta", "link", "template"}

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


# --------------------------------------------------------------------------------------
# Colour
# --------------------------------------------------------------------------------------

class Unresolvable(Exception):
    """The declared value cannot be reduced to an sRGB triple from the source alone."""


def parse_colour(raw: str) -> tuple[float, float, float, float] | None:
    """Return (r, g, b, a) with r/g/b in 0-255 and a in 0-1, or None for `transparent`.

    Raises Unresolvable for anything whose value depends on the rendering engine
    (gradients, `color-mix`, `light-dark`, relative colour syntax, unresolved `var`).
    Returning a guess here is how a gate reports a pass it did not measure.
    """
    v = raw.strip().lower().rstrip(";").strip()
    if not v:
        raise Unresolvable("empty value")
    if v in ("transparent", "none"):
        return None
    if v in ("inherit", "initial", "unset", "revert", "currentcolor", "auto"):
        raise Unresolvable(v)
    if v.startswith("var("):
        raise Unresolvable("unresolved custom property")
    for fn in ("linear-gradient", "radial-gradient", "conic-gradient", "repeating-",
               "color-mix", "light-dark", "image-set", "url(", "-webkit-gradient"):
        if fn in v:
            raise Unresolvable(f"engine-dependent value ({fn.rstrip('(')})")

    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            return (int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16), 1.0)
        if len(h) == 4:
            return (int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16),
                    int(h[3] * 2, 16) / 255)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
        if len(h) == 8:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16),
                    int(h[6:8], 16) / 255)
        raise Unresolvable(f"malformed hex #{h}")

    m = re.fullmatch(r"rgba?\(([^)]*)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        if len(parts) < 3:
            raise Unresolvable("rgb() with fewer than three components")
        chans = []
        for p in parts[:3]:
            if p.endswith("%"):
                chans.append(float(p[:-1]) * 255 / 100)
            else:
                chans.append(float(p))
        alpha = 1.0
        if len(parts) >= 4:
            a = parts[3]
            alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
        return (chans[0], chans[1], chans[2], max(0.0, min(1.0, alpha)))

    m = re.fullmatch(r"hsla?\(([^)]*)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        if len(parts) < 3:
            raise Unresolvable("hsl() with fewer than three components")
        h = float(re.sub(r"(deg|grad|rad|turn)$", "", parts[0])) % 360 / 360
        s = float(parts[1].rstrip("%")) / 100
        light = float(parts[2].rstrip("%")) / 100
        alpha = 1.0
        if len(parts) >= 4:
            a = parts[3]
            alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
        import colorsys
        r, g, b = colorsys.hls_to_rgb(h, light, s)
        return (r * 255, g * 255, b * 255, max(0.0, min(1.0, alpha)))

    if v in NAMED_COLOURS:
        r, g, b = NAMED_COLOURS[v]
        return (r, g, b, 1.0)

    raise Unresolvable(f"unrecognised colour `{raw.strip()}`")


def composite(fg: tuple, bg: tuple) -> tuple:
    """Alpha-composite fg over an opaque bg. The label tiers are alpha values
    (`#000` at 85%), so skipping this step measures the wrong colour entirely."""
    a = fg[3]
    return (fg[0] * a + bg[0] * (1 - a),
            fg[1] * a + bg[1] * (1 - a),
            fg[2] * a + bg[2] * (1 - a),
            1.0)


def luminance(c: tuple) -> float:
    def lin(x: float) -> float:
        x = max(0.0, min(1.0, x / 255))
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])


def contrast(a: tuple, b: tuple) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def hexof(c: tuple) -> str:
    return "#%02X%02X%02X" % (round(c[0]), round(c[1]), round(c[2]))


# --------------------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------------------

LENGTH_RE = re.compile(r"^(-?\d*\.?\d+)(px|pt|rem|em|%|vh|vw)?$")


def to_px(value: str) -> float | None:
    """Reduce a length to px. 1pt == 1px here: a mock is authored in CSS px standing in
    for macOS points, which is the convention the kit tables are read with."""
    v = value.strip().lower()
    m = LENGTH_RE.match(v)
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2) or "px"
    if unit in ("px", "pt"):
        return n
    if unit == "rem":
        return n * 16
    if unit == "em":
        return n * 16
    return None


class Rule:
    __slots__ = ("selector", "decls", "order", "media", "specificity")

    def __init__(self, selector: str, decls: dict, order: int, media: str):
        self.selector = selector.strip()
        self.decls = decls
        self.order = order
        self.media = media
        self.specificity = specificity(self.selector)


def specificity(sel: str) -> tuple[int, int, int]:
    base = re.sub(r"::[a-z-]+(\([^)]*\))?", "", sel)
    ids = len(re.findall(r"#[\w-]+", base))
    classes = (len(re.findall(r"\.[\w-]+", base))
               + len(re.findall(r"\[[^\]]+\]", base))
               + len(re.findall(r":(?!:)[a-z-]+(\([^)]*\))?", base)))
    types = len(re.findall(r"(?:^|[\s>+~])([a-z][\w-]*)", base))
    return (ids, classes, types)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", " ", css, flags=re.S)


def parse_decls(block: str) -> dict:
    out = {}
    depth = 0
    buf = []
    parts = []
    for ch in block:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == ";" and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    for p in parts:
        if ":" not in p:
            continue
        prop, _, val = p.partition(":")
        prop = prop.strip().lower()
        val = val.strip()
        if prop and val:
            out[prop] = val
    return out


def parse_css(css: str) -> tuple[list[Rule], list[str]]:
    """Flatten a stylesheet into rules tagged with their enclosing at-rule condition.

    Nested at-rules are tracked as a joined condition string so a rule inside
    `@media (prefers-color-scheme: dark)` is never mistaken for the default context.
    """
    css = strip_comments(css)
    rules: list[Rule] = []
    at_rules: list[str] = []
    stack: list[str] = []
    i = 0
    order = 0
    n = len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            break
        prelude = css[i:brace].strip()
        # Find the matching close brace for this block.
        depth = 1
        j = brace + 1
        while j < n and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        body = css[brace + 1:j - 1]
        if prelude.startswith("@"):
            at_rules.append(prelude)
            head = prelude.split()[0].lower()
            if head in ("@media", "@supports", "@container", "@layer", "@scope"):
                stack.append(prelude)
                inner, inner_at = parse_css(body)
                at_rules.extend(inner_at)
                for r in inner:
                    cond = " && ".join(stack + ([r.media] if r.media else []))
                    rules.append(Rule(r.selector, r.decls, order, cond))
                    order += 1
                stack.pop()
            # @keyframes / @font-face / @property carry no selectors to match.
        else:
            decls = parse_decls(body)
            if decls:
                for sel in split_selectors(prelude):
                    rules.append(Rule(sel, decls, order, " && ".join(stack)))
                    order += 1
        i = j
    return rules, at_rules


def split_selectors(prelude: str) -> list[str]:
    out, depth, buf = [], 0, []
    for ch in prelude:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    out.append("".join(buf))
    return [s.strip() for s in out if s.strip()]


# --------------------------------------------------------------------------------------
# DOM
# --------------------------------------------------------------------------------------

class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "text", "computed", "depth")

    def __init__(self, tag: str, attrs: dict, parent=None):
        self.tag = tag
        self.attrs = attrs
        self.children: list[Node] = []
        self.parent = parent
        self.text = ""
        self.computed: dict = {}
        self.depth = 0 if parent is None else parent.depth + 1

    @property
    def classes(self) -> set[str]:
        return set((self.attrs.get("class") or "").split())

    @property
    def nid(self) -> str:
        return self.attrs.get("id") or ""

    def path(self) -> str:
        bits = []
        n = self
        while n and n.tag != "#root":
            b = n.tag
            if n.nid:
                b += "#" + n.nid
            elif n.classes:
                b += "." + sorted(n.classes)[0]
            bits.append(b)
            n = n.parent
        # The element itself plus its three nearest ancestors. Taking the *outermost*
        # four instead points every message at <body> and makes the report unusable —
        # a bug this file shipped with once, found only by reading the output.
        return " > ".join(reversed(bits[:4]))

    def ancestors(self):
        n = self.parent
        while n is not None:
            yield n
            n = n.parent


class DOM(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.cur = self.root
        self.styles: list[str] = []
        self._in_style = False
        self.comments: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        node = Node(tag.lower(), a, self.cur)
        self.cur.children.append(node)
        if tag.lower() == "style":
            self._in_style = True
            self.cur = node
        elif tag.lower() not in VOID_TAGS:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        self.cur.children.append(Node(tag.lower(), a, self.cur))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == "style":
            self._in_style = False
        n = self.cur
        while n is not None and n.tag != t:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)
        elif data.strip():
            self.cur.text += data

    def handle_comment(self, data):
        self.comments.append(data)


def walk(node: Node):
    for c in node.children:
        yield c
        yield from walk(c)


def normalise_tree(dom: DOM):
    """Synthesise the implicit `html` > `body` a browser inserts and `html.parser` does
    not.

    Without this, a mock written as bare markup (which is normal and correct for a
    self-contained mock) has no `body` node, so `body { background: ... }` matches
    nothing, every text colour is measured against a fabricated page default, and the
    gate reports contrast failures that do not exist. It reported eleven of them once.
    """
    top = [c for c in dom.root.children if c.tag not in ("html", "!doctype")]
    if any(c.tag == "html" for c in dom.root.children):
        html_nodes = [c for c in dom.root.children if c.tag == "html"]
        for h in html_nodes:
            if not any(c.tag == "body" for c in h.children):
                body = Node("body", {}, h)
                movable = [c for c in h.children if c.tag not in ("head",)]
                for c in movable:
                    h.children.remove(c)
                    c.parent = body
                    body.children.append(c)
                h.children.append(body)
        return
    if any(c.tag == "body" for c in top):
        return
    html = Node("html", {}, dom.root)
    body = Node("body", {}, html)
    for c in list(dom.root.children):
        dom.root.children.remove(c)
        if c.tag in ("!doctype", "head", "title", "meta", "style", "link"):
            c.parent = html
            html.children.append(c)
        else:
            c.parent = body
            body.children.append(c)
    html.children.append(body)
    dom.root.children.append(html)
    _reparent_depth(dom.root, 0)


def _reparent_depth(node: Node, d: int):
    node.depth = d
    for c in node.children:
        _reparent_depth(c, d + 1)


# --------------------------------------------------------------------------------------
# Selector matching (the subset a self-contained mock actually uses)
# --------------------------------------------------------------------------------------

STATE_PSEUDO = re.compile(
    r":(hover|active|focus|focus-visible|focus-within|disabled|checked|"
    r"target|visited|placeholder-shown)\b")


def simple_match(node: Node, part: str) -> bool:
    part = re.sub(r"::[a-z-]+(\([^)]*\))?", "", part)
    part = re.sub(r":(?:not|is|where)\([^)]*\)", "", part)
    part = STATE_PSEUDO.sub("", part)
    part = re.sub(r":(?!:)[a-z-]+(\([^)]*\))?", "", part).strip()
    if not part or part == "*":
        return True
    m = re.match(r"^([a-zA-Z][\w-]*)?(.*)$", part)
    tag, rest = m.group(1), m.group(2)
    if tag and node.tag != tag.lower():
        if not (tag.lower() in (":root",) and node.tag == "html"):
            return False
    for cls in re.findall(r"\.([\w-]+)", rest):
        if cls not in node.classes:
            return False
    for i in re.findall(r"#([\w-]+)", rest):
        if node.nid != i:
            return False
    for attr in re.findall(r"\[([\w-]+)(?:[~|^$*]?=)?[\"']?([^\]\"']*)[\"']?\]", rest):
        name, want = attr[0].lower(), attr[1]
        if name not in node.attrs:
            return False
        if want and want not in node.attrs[name]:
            return False
    return True


def matches(node: Node, selector: str) -> bool:
    sel = selector.strip()
    if sel in (":root", "html:root"):
        return node.tag == "html"
    if "," in sel:
        return any(matches(node, s) for s in split_selectors(sel))
    tokens = [t for t in re.split(r"\s*([>+~])\s*|\s+", sel) if t]
    if not tokens:
        return False
    if not simple_match(node, tokens[-1]):
        return False
    # Walk the remaining compound selectors up the ancestor chain. `+`/`~` sibling
    # combinators are treated as descendant, which over-matches; over-matching a
    # background is safer than reporting a pair as unresolved when it is resolvable,
    # and the direction of the error is stated in the report.
    idx = len(tokens) - 2
    node_ptr = node
    while idx >= 0:
        tok = tokens[idx]
        if tok in (">", "+", "~"):
            idx -= 1
            continue
        found = False
        for anc in node_ptr.ancestors():
            if simple_match(anc, tok):
                node_ptr = anc
                found = True
                break
        if not found:
            return False
        idx -= 1
    return True


# --------------------------------------------------------------------------------------
# The cascade approximation
# --------------------------------------------------------------------------------------

BG_SHORTHAND_COLOUR = re.compile(
    r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsla?\([^)]*\)|\b(?:"
    + "|".join(NAMED_COLOURS) + r"|transparent)\b)")


def bg_colour_from(decls: dict) -> str | None:
    if "background-color" in decls:
        return decls["background-color"]
    if "background" in decls:
        v = decls["background"]
        if any(g in v.lower() for g in ("gradient", "url(", "image-set")):
            return v  # handed on so parse_colour raises Unresolvable with the reason
        m = BG_SHORTHAND_COLOUR.search(v)
        if m:
            return m.group(1)
    return None


def resolve_vars(value: str, root_vars: dict, seen=None) -> str:
    """Substitute `var(--x)` from the `:root` block, honouring fallbacks. Bounded so a
    circular definition cannot spin."""
    seen = seen or set()
    for _ in range(8):
        m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\)[^()]*)*))?\)",
                      value)
        if not m:
            return value
        name, fallback = m.group(1), m.group(2)
        if name in seen:
            return value
        seen = seen | {name}
        repl = root_vars.get(name)
        if repl is None:
            repl = (fallback or "").strip()
        if not repl:
            return value
        value = value[:m.start()] + repl + value[m.end():]
    return value


def context_active(rules: list[Rule], ctx: str) -> list[Rule]:
    """The rules in force for one appearance context.

    Every `prefers-*` block is an *alternate state*, not part of the default cascade, so
    including them all at once measures a surface nobody ever sees. This file shipped
    once doing exactly that: a `prefers-contrast: more` block redefined the secondary
    label and its values leaked into the plain light and dark measurements, so the gate
    reported black-on-graphite failures for a mock that had none. The bug was invisible
    in the code and obvious in the output.

    Contexts:
      light / dark            no preferences set (the default a reviewer sees)
      light+contrast / dark+contrast   increased contrast requested

    Not measured, and deliberately: `prefers-reduced-transparency` blocks change
    backgrounds, so they are a real colour context — but this house's browser accepts
    `setEmulatedMedia` and does nothing, so there is no render to check the static
    reading against. It is excluded and declared rather than guessed at.
    """
    want_dark = ctx.startswith("dark")
    want_contrast = ctx.endswith("+contrast")
    out = []
    for r in rules:
        m = r.media.lower()
        if not m:
            out.append(r)
            continue
        if "prefers-reduced-motion" in m or "prefers-reduced-transparency" in m:
            continue
        if "prefers-color-scheme" in m:
            is_dark_block = "dark" in m
            if is_dark_block != want_dark:
                continue
        if "prefers-contrast" in m and not want_contrast:
            continue
        if "print" in m:
            continue
        out.append(r)
    return out


def compute(dom: DOM, rules: list[Rule], contexts: tuple[str, ...]):
    """Apply the matching rules, in cascade order, to every node — once per appearance
    context so light and dark are measured separately rather than blended."""
    per_context = {}
    for ctx in contexts:
        active = context_active(rules, ctx)
        root_vars = {}
        for r in sorted(active, key=lambda r: (r.specificity, r.order)):
            if r.selector in (":root", "html", "html:root", "*"):
                for k, v in r.decls.items():
                    if k.startswith("--"):
                        root_vars[k] = v
        for r in sorted(active, key=lambda r: (r.specificity, r.order)):
            for k, v in r.decls.items():
                if k.startswith("--"):
                    root_vars.setdefault(k, v)
        for k in list(root_vars):
            root_vars[k] = resolve_vars(root_vars[k], root_vars)

        style = {}
        for node in walk(dom.root):
            acc = {}
            for r in sorted(active, key=lambda r: (r.specificity, r.order)):
                if matches(node, r.selector):
                    state = bool(STATE_PSEUDO.search(r.selector))
                    for k, v in r.decls.items():
                        if k.startswith("--"):
                            continue
                        acc[(k, state)] = v
            inline = parse_decls(node.attrs.get("style", ""))
            for k, v in inline.items():
                acc[(k, False)] = v
            resolved = {}
            for (k, state), v in acc.items():
                if state:
                    continue
                resolved[k] = resolve_vars(v, root_vars)
            state_only = {}
            for (k, state), v in acc.items():
                if state:
                    state_only[k] = resolve_vars(v, root_vars)
            style[id(node)] = (resolved, state_only)
        per_context[ctx] = (style, root_vars)
    return per_context


def effective_bg(node: Node, style: dict, page_default: tuple) -> tuple:
    """Nearest declared, non-transparent background walking up the tree. A text colour
    measured against the wrong surface is a number with no meaning, so an unresolvable
    ancestor background aborts the pair rather than falling through to white."""
    chain = [node] + list(node.ancestors())
    for n in chain:
        decls = style.get(id(n), ({}, {}))[0]
        raw = bg_colour_from(decls)
        if raw is None:
            continue
        col = parse_colour(raw)  # may raise Unresolvable
        if col is None:
            continue
        if col[3] >= 0.999:
            return col[:3] + (1.0,)
        below = effective_bg(n.parent, style, page_default) if n.parent else page_default
        return composite(col, below)
    return page_default


def effective_fg(node: Node, style: dict):
    """The element's text colour, **inherited** where it declares none.

    `color` is an inherited property, and a cascade walk that only reads *matched* rules
    does not model that: a `<div>` holding text under a `body { color: ... }` has no
    declared colour of its own, so the pair is skipped and never measured. This gate
    shipped that way for one revision, and the symptom was the instrument accusing the
    material — `gate_tests.sh` reported fourteen broken fixtures when the fixtures were
    fine and `examined=0` was swallowing every one of them.

    Returns (raw_value, source_node) or (None, None) when no ancestor declares one, which
    is a genuine "nothing to measure" rather than a skipped measurement.
    """
    for n in [node] + list(node.ancestors()):
        decls = style.get(id(n), ({}, {}))[0]
        raw = decls.get("color")
        if raw is None:
            continue
        if raw.strip().lower() in ("inherit", "unset", "revert", "currentcolor"):
            continue
        return raw, n
    return None, None


def inherited_prop(node: Node, style: dict, prop: str, default: str) -> str:
    """Nearest declared value of an inherited font property, for the size and weight the
    contrast floor depends on. Reading these off the element alone puts 13px on text the
    stylesheet set to 11px on an ancestor, and picks the wrong 4.5-versus-3.0 threshold."""
    for n in [node] + list(node.ancestors()):
        decls = style.get(id(n), ({}, {}))[0]
        if prop in decls:
            return decls[prop]
        if prop == "font-size" and "font" in decls:
            m = re.search(r"(\d*\.?\d+)(px|pt|rem|em)\b", decls["font"])
            if m:
                return m.group(0)
        if prop == "font-weight" and "font" in decls:
            m = re.search(r"\b(bold|bolder|[1-9]00)\b", decls["font"].lower())
            if m:
                return m.group(1)
    return default


# --------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.fails: list[str] = []
        self.notes: list[str] = []
        self.unmeasured: list[str] = []
        self.counters: dict = {}

    def fail(self, check: str, msg: str):
        # Deduplicated: two sibling elements sharing a class produce the same defect
        # once, not twice. A repeated line reads as a parser bug and buries the others.
        line = f"FAIL  [{check}] {msg}"
        if line not in self.fails:
            self.fails.append(line)

    def note(self, check: str, msg: str):
        line = f"NOTE  [{check}] {msg}"
        if line not in self.notes:
            self.notes.append(line)

    def unmeasurable(self, check: str, msg: str):
        self.unmeasured.append(f"UNMEASURED  [{check}] {msg}")

    def count(self, check: str, **kw):
        self.counters.setdefault(check, {}).update(kw)


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------

def check_naming(path: Path, rep: Report, allow: bool):
    stem = path.stem.lower()
    stripped = re.sub(r"[-_ ]?(mock|mockup|design|light|dark|v\d+|\d+)$", "", stem)
    if stem in GENERIC_NAMES or stripped in GENERIC_NAMES or not stripped:
        msg = (f"filename `{path.name}` names the tool or nothing, not the app. The "
               f"file is what the design is CALLED wherever it is opened, linked or "
               f"attached, and a generic name is unfindable a week later. Rename it "
               f"from the app — `ledgerline-main-window.html`, not `mock.html`. "
               f"(`--allow-name` if the surrounding project genuinely fixes the name.)")
        rep.note("naming", msg) if allow else rep.fail("naming", msg)
    rep.count("naming", examined=1)


def check_self_contained(html: str, rep: Report):
    findings = []
    for m in re.finditer(r"""<(link|script|img|source|video|audio|iframe)\b[^>]*"""
                         r"""\b(?:href|src)\s*=\s*["']?(https?:|//)""", html, re.I):
        findings.append(m.group(1).lower())
    for m in re.finditer(r"@import\s+(?:url\()?[\"']?(https?:|//)", html, re.I):
        findings.append("@import")
    for m in re.finditer(r"""url\(\s*["']?(https?:|//)""", html, re.I):
        findings.append("css url()")
    rep.count("self-contained", examined=1, external_refs=len(findings))
    if findings:
        kinds = ", ".join(sorted(set(findings)))
        rep.fail("self-contained",
                 f"{len(findings)} external reference(s) ({kinds}). A mock is reviewed "
                 f"offline and archived beside its spec; an external asset renders as "
                 f"nothing on the reviewer's machine and nothing warns. Web fonts are "
                 f"the common case and the worst one: this house's browser never loads "
                 f"them, so the mock silently falls back to the system stack and the "
                 f"typography you audited is not the typography you shipped. Inline the "
                 f"CSS, draw the glyphs, use the `-apple-system` stack.")


def check_metric_block(dom: DOM, css_text: str, rep: Report):
    """The metric table, hoisted out of a model-family side-file into the gate.

    A cell you cannot tag is a value you invented; a value declared but absent from the
    CSS is a claim the artifact does not support. Both are the same failure that put a
    48px titlebar into a mock whose own reference says 33pt.
    """
    block = None
    for c in dom.comments:
        if "mac-craft:metrics" in c:
            block = c
            break
    if block is None:
        rep.fail("metrics",
                 "no `<!-- mac-craft:metrics ... -->` block. Every chrome and control "
                 "metric in a native mock has a published number, and the recorded "
                 "failure mode is not disagreeing with it but never reading it: a run "
                 "put a 48px titlebar into a mock whose own reference specifies 33pt, "
                 "and no reviewer could tell whether that was a choice. Declare each "
                 "metric with its value and its tier "
                 f"({'/'.join(sorted(VALID_TIERS))}) before the first line of CSS.")
        rep.count("metrics", examined=0)
        return
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("mac-craft:metrics") or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            rows.append(parts)
    if not rows:
        rep.unmeasurable("metrics",
                         "the metric block is present but empty — nothing to check. An "
                         "empty declaration is not a filled one.")
        rep.count("metrics", examined=0)
        return

    examined = failures = 0
    for parts in rows:
        name = parts[0].lower().rstrip(":")
        value = parts[1]
        tier = parts[2].lower() if len(parts) >= 3 else ""
        examined += 1
        if tier not in VALID_TIERS:
            failures += 1
            rep.fail("metrics",
                     f"`{name}` = {value} carries no recognised tier (got "
                     f"`{tier or '<none>'}`). A cell you cannot tag is a value you "
                     f"invented. Tag it {'/'.join(sorted(VALID_TIERS))}, or read the "
                     f"published number and tag it `kit`.")
            continue
        if tier == "direction" and name in ENVELOPE_LOCKED:
            failures += 1
            rep.fail("metrics",
                     f"`{name}` is tagged `direction`. A direction sets identity tokens "
                     f"*within* the native envelope; chrome and control geometry is not "
                     f"inside that envelope. Take the kit value, or declare the "
                     f"deviation in the delivery as a named non-native choice.")
            continue
        if name in KIT_METRICS and tier == "kit":
            want, unit = KIT_METRICS[name]
            got = to_px(value)
            if got is None:
                failures += 1
                rep.fail("metrics",
                         f"`{name}` = `{value}` is tagged `kit` but is not a length "
                         f"this gate can read. Write it as a number plus px/pt.")
                continue
            if abs(got - want) > 0.51:
                failures += 1
                rep.fail("metrics",
                         f"`{name}` declared {value} and tagged `kit`, but the kit "
                         f"specifies {want}{unit}. A `kit` tag is a claim about a "
                         f"published value; if the design departs on purpose, tag it "
                         f"`direction` and say so in the delivery — an unmarked "
                         f"departure reads to every downstream implementer as the "
                         f"platform number.")
                continue
            # The half that makes this a gate on the artifact, not on the declaration.
            needle = re.compile(r"(?<![\d.])" + re.escape(str(int(got)) if got.is_integer()
                                                          else str(got)) + r"(px|pt|rem)?\b")
            if not needle.search(css_text):
                failures += 1
                rep.fail("metrics",
                         f"`{name}` = {value} is declared and appears nowhere in the "
                         f"CSS. A metric table that agrees with the kit and disagrees "
                         f"with the stylesheet is the worst of the three states: it "
                         f"passes a reading, and the built artifact is still wrong.")
    rep.count("metrics", examined=examined, failures=failures, rows=len(rows))
    if examined and failures == 0:
        pass


def check_contrast(dom: DOM, per_ctx: dict, rep: Report):
    """The check the predecessor claimed and did not run."""
    total_examined = 0
    total_failures = 0
    total_unresolved = 0
    identical = 0
    disabled_skipped = 0
    worst = []

    for ctx, (style, _vars) in per_ctx.items():
        page_default = ((255.0, 255.0, 255.0, 1.0) if ctx.startswith("light")
                        else (30.0, 30.0, 30.0, 1.0))
        for n in [dom.root] + list(walk(dom.root)):
            decls = style.get(id(n), ({}, {}))[0]
            raw_bg = bg_colour_from(decls)
            if raw_bg is not None and n.tag in ("body", "html"):
                try:
                    c = parse_colour(raw_bg)
                    if c and c[3] >= 0.999:
                        page_default = c
                except Unresolvable:
                    pass

        for node in walk(dom.root):
            if node.tag in NON_RENDERING:
                continue
            own_text = node.text.strip()
            if not own_text:
                continue
            decls, _state = style.get(id(node), ({}, {}))
            raw_fg, fg_src = effective_fg(node, style)
            if raw_fg is None:
                continue
            total_examined += 1
            try:
                fg = parse_colour(raw_fg)
            except Unresolvable as e:
                total_unresolved += 1
                where = "" if fg_src is node else f" (inherited from `{fg_src.path()}`)"
                rep.note("contrast",
                         f"{ctx}: `{node.path()}` colour `{raw_fg}`{where} is not "
                         f"resolvable from the source ({e}). NOT counted as a pass — "
                         f"this pair was not measured.")
                continue
            if fg is None:
                continue
            try:
                bg = effective_bg(node, style, page_default)
            except Unresolvable as e:
                total_unresolved += 1
                rep.note("contrast",
                         f"{ctx}: `{node.path()}` sits on a background this gate cannot "
                         f"resolve ({e}). NOT counted as a pass.")
                continue
            fgc = composite(fg, bg) if fg[3] < 0.999 else fg
            ratio = contrast(fgc, bg)
            size = to_px(inherited_prop(node, style, "font-size", "13px")) or 13.0
            weight = inherited_prop(node, style, "font-weight", "400").strip().lower()
            bold = weight in ("bold", "bolder") or (weight.isdigit() and int(weight) >= 700)
            floor = 3.0 if (size >= 24 or (size >= 18.66 and bold)) else 4.5
            worst.append((ratio, ctx, node.path(), hexof(fgc), hexof(bg), size, floor))

            # WCAG 1.4.3 exempts inactive components, and the platform's disabled tier is
            # 1.83:1 by construction. Counting it as a defect would make the gate
            # un-passable for any mock that draws a disabled control — which the skill
            # requires, because disabled dims in place and never disappears.
            disabled = ("disabled" in node.attrs
                        or "disabled" in node.classes
                        or node.attrs.get("aria-disabled") == "true")
            if disabled:
                total_examined -= 1
                disabled_skipped += 1
                continue

            if ratio < 1.05:
                identical += 1
                total_failures += 1
                rep.fail("contrast",
                         f"{ctx}: `{node.path()}` renders text at {ratio:.2f}:1 — "
                         f"{hexof(fgc)} on {hexof(bg)}, the same colour as its own "
                         f"background. The element is in the DOM, occupies layout and "
                         f"is invisible; a screenshot review reads it as an empty slot "
                         f"rather than as a defect, which is how one shipped. Give it a "
                         f"label tier (primary 85% / secondary 60% / disabled 25%).")
            elif ratio < floor:
                total_failures += 1
                hue = SYSTEM_HUES.get(hexof(bg).lower())
                if hue:
                    rep.fail("contrast",
                             f"{ctx}: `{node.path()}` is {ratio:.2f}:1 on the kit's "
                             f"system {hue} ({hexof(bg)}) at {size:g}px, floor "
                             f"{floor}:1. This is the platform's own published value, "
                             f"not your mistake — Apple's accent-filled Bordered Default "
                             f"button genuinely sits below the AA floor for body text. "
                             f"It is still a failure here, because 'the platform does it' "
                             f"is how dilution spreads. Two honest exits: darken the "
                             f"fill on text-bearing accent surfaces, or keep the hue and "
                             f"declare it in the delivery as a platform-inherited "
                             f"deviation with the measured number beside it.")
                else:
                    rep.fail("contrast",
                             f"{ctx}: `{node.path()}` is {ratio:.2f}:1, floor {floor}:1 "
                             f"({hexof(fgc)} on {hexof(bg)} at {size:g}px). Contrast "
                             f"Dilution is this corpus's dominant defect — it appears in "
                             f"72 of 135 apps — because a diluted label still looks "
                             f"deliberate. Lift the tier, not the font weight.")

    if total_examined == 0:
        rep.unmeasurable("contrast",
                         "examined=0. No element carried both a text run and a "
                         "resolvable declared colour, so no contrast pair exists to "
                         "measure. This is a gate that never ran; it is not a pass. "
                         "Either the stylesheet is not inline, the selectors do not "
                         "reach the markup, or the mock has no text.")
    rep.count("contrast", examined=total_examined, failures=total_failures,
              unresolved=total_unresolved, identical=identical,
              disabled_exempt=disabled_skipped,
              contexts=len(per_ctx))
    if worst:
        worst.sort()
        rep.note("contrast", "tightest five pairs measured: " + "; ".join(
            f"{r:.2f}:1 {p} ({f} on {b})" for r, c, p, f, b, s, fl in worst[:5]))


def check_keyboard(html: str, css_text: str, dom: DOM, rep: Report):
    """Conviction 7 is greppable. The recorded run measured zero on all four."""
    focus_visible = len(re.findall(r":focus-visible", css_text))
    focus_plain = len(re.findall(r":focus(?![-\w])", css_text))
    roles = len(re.findall(r"""\brole\s*=\s*["'][^"']+["']""", html, re.I))
    tabindex = len(re.findall(r"""\btabindex\s*=""", html, re.I))
    clickable_divs = 0
    for node in walk(dom.root):
        if node.tag in ("div", "span", "li", "td", "p", "section", "article"):
            if any(k.startswith("onclick") or k.startswith("onmousedown")
                   for k in node.attrs):
                if "role" not in node.attrs and "tabindex" not in node.attrs:
                    clickable_divs += 1
    interactive = sum(1 for n in walk(dom.root)
                      if n.tag in ("button", "a", "input", "select", "textarea"))
    rep.count("keyboard", examined=1, focus_visible=focus_visible,
              focus=focus_plain, role=roles, tabindex=tabindex,
              clickable_nonsemantic=clickable_divs, semantic_controls=interactive)

    if focus_visible == 0 and focus_plain == 0:
        rep.fail("keyboard",
                 "`:focus-visible` 0 and `:focus` 0. The keyboard is half a Mac app and "
                 "the focus ring is the only part of it a mock can show; without one "
                 "the design has silently specified a pointer-only interface, and the "
                 "implementer inherits that. Draw the accent-bound ring on at least the "
                 "surface's default control.")
    elif focus_visible == 0:
        rep.note("keyboard",
                 f"`:focus` {focus_plain} but `:focus-visible` 0. Bare `:focus` fires on "
                 f"mouse-down too, so the ring flashes on click — which is why the "
                 f"platform draws it only for keyboard traversal. Move the ring to "
                 f"`:focus-visible`.")
    if clickable_divs:
        rep.fail("keyboard",
                 f"{clickable_divs} non-semantic element(s) carry a click handler with "
                 f"no `role` and no `tabindex`. They are keyboard-dead and invisible to "
                 f"assistive technology, and they look identical to working controls in "
                 f"every screenshot. Use `<button>`, or add `role` plus `tabindex=\"0\"` "
                 f"plus a key handler.")
    if interactive == 0 and roles == 0:
        rep.note("keyboard",
                 "no semantic controls and no `role` attributes anywhere. If this is a "
                 "purely presentational surface that is fine; if anything on it is "
                 "meant to be operable, nothing here says so.")


def check_tokens(rules: list[Rule], css_text: str, rep: Report):
    root_literals = set()
    other_literals = []
    for r in rules:
        is_token_block = r.selector in (":root", "html", "html:root", "*")
        for k, v in r.decls.items():
            for m in BG_SHORTHAND_COLOUR.finditer(v):
                lit = m.group(1).lower()
                if lit in ("transparent",):
                    continue
                if is_token_block or k.startswith("--"):
                    root_literals.add(lit)
                else:
                    other_literals.append((lit, r.selector, k))
    distinct_outside = len({l for l, _, _ in other_literals})
    rep.count("tokens", examined=1, token_block_colours=len(root_literals),
              literals_outside=len(other_literals), distinct_outside=distinct_outside)
    if not root_literals:
        rep.fail("tokens",
                 "no colour custom properties declared. Without a token layer there is "
                 "nothing for a light/dark switch, an accent change or a second "
                 "platform to move: one recorded run declared 11 custom properties and "
                 "used 45 raw hex literals beside them, and the resulting artifact could "
                 "not be re-themed at all. Declare the palette on `:root` and reference "
                 "it everywhere.")
    elif distinct_outside > 6:
        rep.fail("tokens",
                 f"{distinct_outside} distinct colour literals declared outside the "
                 f"token block ({len(other_literals)} uses). Past a handful these stop "
                 f"being exceptions and become a second, undeclared palette — the "
                 f"switch that has to rewrite them will not happen. Promote them to "
                 f"`:root`.")
    elif distinct_outside:
        rep.note("tokens",
                 f"{distinct_outside} colour literal(s) outside the token block: "
                 + ", ".join(sorted({f"{l} on `{s}`" for l, s, _ in other_literals})[:6]))


def check_casing_and_cursor(rules: list[Rule], rep: Report):
    upper = [(r.selector, r.decls) for r in rules
             if r.decls.get("text-transform", "").strip().lower() == "uppercase"]
    heading_upper = []
    for sel, decls in upper:
        size = to_px(decls.get("font-size", "")) or 0
        if size >= 13:
            heading_upper.append((sel, size))
    rep.count("casing", examined=len(rules), uppercase_rules=len(upper),
              uppercase_at_heading_size=len(heading_upper))
    if heading_upper:
        rep.fail("casing",
                 "tracked/uppercase labels at heading size on "
                 + ", ".join(f"`{s}` ({z:g}px)" for s, z in heading_upper[:4])
                 + ". Uppercase is native only as a tiny tertiary eyebrow (10-11px); at "
                   "heading size it is the corpus's loudest web tell, present in the "
                   "majority of its non-native captures. Do not fix the tracking — "
                   "replace it with sentence case, Semibold, secondary colour.")
    elif upper:
        rep.note("casing",
                 f"{len(upper)} uppercase rule(s), all below 13px — legitimate as a "
                 f"tiny eyebrow. Keep them tertiary-coloured.")

    hands = []
    for r in rules:
        if r.decls.get("cursor", "").strip().lower() == "pointer":
            base = re.sub(r":[a-z-]+(\([^)]*\))?", "", r.selector).strip()
            if not re.search(r"(^|[\s>,.#])a\b|link|href", base, re.I):
                hands.append(r.selector)
    rep.count("cursor", examined=len(rules), pointer_rules=len(hands))
    if hands:
        rep.fail("cursor",
                 "`cursor: pointer` on " + ", ".join(f"`{s}`" for s in hands[:5])
                 + ". The pointing hand is a web-content signal for hyperlinks; on a "
                   "button, a list row or a toolbar item macOS shows the arrow, and the "
                   "hand is the single most frequent non-native tell an experienced Mac "
                   "user names first. Keep `pointer` for true hyperlinks and marketing "
                   "surfaces only.")


def check_a11y_queries(at_rules: list[str], interactive: bool, rep: Report):
    joined = " ".join(at_rules).lower()
    wanted = {
        "prefers-reduced-motion": "motion",
        "prefers-reduced-transparency": "transparency",
        "prefers-contrast": "contrast",
    }
    missing = [q for q in wanted if q not in joined]
    rep.count("a11y-queries", examined=len(wanted),
              present=len(wanted) - len(missing), missing=len(missing))
    if not missing:
        return
    msg = (", ".join(missing) + " absent. The platform solidifies its own glass under "
           "Reduce Transparency and shortens its own animations under Reduce Motion; a "
           "mock that omits them specifies a surface that ignores three system settings, "
           "and the implementer copies the omission. Note also that none of the three "
           "can be *verified* here — this house's browser accepts `setEmulatedMedia` and "
           "does nothing, so their presence in the source is the whole of the evidence.")
    rep.fail("a11y-queries", msg) if interactive else rep.note("a11y-queries", msg)


def check_content(dom: DOM, html: str, rep: Report):
    text = " ".join(n.text for n in walk(dom.root) if n.tag not in NON_RENDERING)
    lorem = len(re.findall(r"\blorem ipsum\b|\bdolor sit amet\b", text, re.I))
    placeholders = re.findall(r"\{\{[^}]{1,120}\}\}", html)
    todo = len(re.findall(r"\b(TODO|FIXME|XXX|TBD|PLACEHOLDER)\b", text))
    marked = re.findall(r"\[[A-Z][A-Z /_-]{2,40}\]", text)
    rep.count("content", examined=1, lorem=lorem, template_placeholders=len(placeholders),
              todo=todo, marked_placeholders=len(marked))
    if lorem:
        rep.fail("content",
                 f"{lorem} run(s) of lorem ipsum. Filler hides two failures at once — "
                 f"whether the layout survives real string lengths, and whether the "
                 f"copy is comprehensible — and both surface for the first time in the "
                 f"built app. Write the real words.")
    if placeholders:
        rep.fail("content",
                 f"{len(placeholders)} unfilled template placeholder(s): "
                 + ", ".join(placeholders[:4])
                 + ". These render literally to whoever opens the file.")
    if todo:
        rep.note("content", f"{todo} TODO/TBD marker(s) in rendered text.")
    if marked:
        rep.note("content",
                 f"{len(marked)} marked placeholder(s) ({', '.join(marked[:3])}) — "
                 f"correct form for a fact you do not have; make sure the delivery says "
                 f"which facts they are.")


def check_states(dom: DOM, css_text: str, rep: Report):
    states = {
        "hover": len(re.findall(r":hover", css_text)),
        "active": len(re.findall(r":active", css_text)),
        "disabled": len(re.findall(r":disabled|\[disabled\]|\.disabled", css_text)),
    }
    empty_markers = len(re.findall(
        r"empty[-_]?state|first[-_]?run|no[-_]?(results|items|content)",
        css_text + " ".join(n.attrs.get("class", "") for n in walk(dom.root)), re.I))
    rep.count("states", examined=1, empty_state_markers=empty_markers, **states)
    if empty_markers == 0:
        rep.note("states",
                 "no empty-state or first-run markup found. States are where quality "
                 "lives, and the ideal state is a third of a design; if the empty state "
                 "is specified in the state matrix rather than rendered, say so in the "
                 "delivery so nobody reads its absence as a decision.")
    for name, count in states.items():
        if count == 0:
            rep.note("states", f"no `:{name}` rule anywhere — that state is unspecified.")


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Deterministic gate for a macOS HTML interface mockup.")
    ap.add_argument("mock", help="path to the mock .html")
    ap.add_argument("--json", action="store_true", help="machine-readable summary")
    ap.add_argument("--interactive", dest="interactive", action="store_true",
                    default=None, help="treat as an interactive deliverable")
    ap.add_argument("--static", dest="interactive", action="store_false",
                    help="treat as a static mock")
    ap.add_argument("--allow-name", action="store_true",
                    help="downgrade the filename check to a note")
    args = ap.parse_args(argv)

    path = Path(args.mock)
    if not path.exists():
        print(f"UNMEASURED  [input] {path} does not exist. Nothing was checked.")
        return 2
    html = path.read_text(encoding="utf-8", errors="replace")
    if not html.strip():
        print(f"UNMEASURED  [input] {path} is empty. Nothing was checked.")
        return 2

    dom = DOM()
    try:
        dom.feed(html)
        dom.close()
        normalise_tree(dom)
    except Exception as e:  # noqa: BLE001 - a parse failure must not read as a pass
        print(f"UNMEASURED  [input] could not parse {path.name} ({e}). No check ran, "
              f"and nothing here is a pass.")
        return 2

    css_text = strip_comments("\n".join(dom.styles))
    inline_styles = " ".join(n.attrs.get("style", "") for n in walk(dom.root))
    rules, at_rules = parse_css("\n".join(dom.styles))

    rep = Report()

    if not css_text.strip() and not inline_styles.strip():
        rep.unmeasurable("input",
                         "no inline <style> block and no inline style attributes. "
                         "Every visual check below depends on declared values; with "
                         "none present this gate measured nothing. A mock that keeps "
                         "its CSS in a separate file is also not self-contained.")

    interactive = args.interactive
    if interactive is None:
        interactive = bool(re.search(r":hover|:active|transition|@keyframes|animation",
                                     css_text))

    check_naming(path, rep, args.allow_name)
    check_self_contained(html, rep)
    check_metric_block(dom, css_text, rep)
    check_tokens(rules, css_text, rep)
    check_casing_and_cursor(rules, rep)
    check_a11y_queries(at_rules, interactive, rep)
    check_keyboard(html, css_text, dom, rep)
    check_content(dom, html, rep)
    check_states(dom, css_text, rep)

    if rules:
        at_joined = " ".join(at_rules).lower()
        contexts = ["light"]
        if "prefers-color-scheme" in at_joined and "dark" in at_joined:
            contexts.append("dark")
        if "prefers-contrast" in at_joined:
            contexts.append("light+contrast")
            if "dark" in contexts:
                contexts.append("dark+contrast")
        try:
            per_ctx = compute(dom, rules, tuple(contexts))
            check_contrast(dom, per_ctx, rep)
        except Unresolvable as e:
            rep.unmeasurable("contrast",
                             f"the cascade could not be resolved ({e}). No contrast "
                             f"pair was measured, and none is claimed.")
        if "prefers-reduced-transparency" in at_joined:
            rep.note("contrast",
                     "a `prefers-reduced-transparency` block is present and its colour "
                     "effect is NOT measured: it changes backgrounds, so it is a real "
                     "contrast context, but this house's browser accepts "
                     "`setEmulatedMedia` and does nothing, so there is no render to "
                     "check a static reading against. Declared rather than guessed.")
    else:
        rep.unmeasurable("contrast",
                         "no CSS rules parsed, so no colour pair exists to measure. "
                         "examined=0 is a gate that never ran.")

    # ---- output ----------------------------------------------------------------------
    if args.json:
        print(json.dumps({
            "file": str(path),
            "interactive": interactive,
            "counters": rep.counters,
            "fails": rep.fails,
            "notes": rep.notes,
            "unmeasured": rep.unmeasured,
            "verdict": ("unmeasured" if rep.unmeasured
                        else "fail" if rep.fails else "pass"),
        }, indent=2))
    else:
        print(f"mock_check {path.name}  "
              f"({'interactive' if interactive else 'static'} deliverable)")
        print("-" * 72)
        for check in sorted(rep.counters):
            bits = " ".join(f"{k}={v}" for k, v in rep.counters[check].items())
            print(f"  {check:<16} {bits}")
        print("-" * 72)
        for line in rep.unmeasured:
            print(line)
        for line in rep.fails:
            print(line)
        for line in rep.notes:
            print(line, file=sys.stderr)
        print("-" * 72)
        verdict = ("FAIL" if rep.fails
                   else "UNMEASURED" if rep.unmeasured else "PASS")
        print(f"{verdict}: {len(rep.fails)} failure(s), {len(rep.notes)} note(s), "
              f"{len(rep.unmeasured)} unmeasurable check(s)")
        if rep.fails and rep.unmeasured:
            print("Both a failure and an unmeasurable check are present. The exit code "
                  "reports the failure, because that is the stronger signal — the "
                  "unmeasurable check is still open once the failures are fixed.")
        if rep.notes:
            print("Notes went to stderr; anything on stderr is a warning to read.")

    # Exit-code precedence: a proven failure outranks an unmeasurable check.
    #
    # This ran the other way round for one revision and it was wrong. Every check that
    # could not be performed pushed the exit code to 2, so a mock with a 1.00:1 glyph AND
    # one unresolvable pair reported "could not measure" — the failures still printed, but
    # the code a caller branches on said the wrong thing, and a runner reading it chases
    # the indeterminate check while the invisible glyph sits there. If you can prove it is
    # broken, "broken" is the verdict. Unmeasurable only wins when nothing failed, which
    # is the case it is actually about: no failures found AND no confidence that none
    # exist. Both counts are on the summary line either way, so the softer signal is
    # reported rather than lost.
    if rep.fails:
        return 1
    if rep.unmeasured:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
