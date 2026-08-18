#!/usr/bin/env python3
"""ux-lint — the deterministic gate for ux-craft.

Prose that asks is not a gate. This refuses the UX failures that ship silently:
keyboard-dead click handlers, suppressed focus with no replacement, a placeholder
standing in for a label, motion with no reduced-motion guard, a form whose only
reachable state is the terminal one, and an artifact asserting its own verification.

Two modes:

  ux-lint.py --static <paths...>     walk source and refuse what a machine can decide
  ux-lint.py --probe <url>           measure a rendered page through Obscura

Every finding names three things: what you did, what the user silently gets, and
the fix. Every run prints a never-empty "Not checked" list, because a check that
cannot measure must say so rather than reporting zero.

Exit codes
  0  no failures
  1  failures present
  2  examined zero files or zero elements (a refusal, not a pass)
  3  unrecognised configuration or bad usage
  4  a check raised while running (the run is not clean; it is unknown)

Standard library only. No dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from html.parser import HTMLParser
from pathlib import Path

VERSION = "1.0.0"

SOURCE_SUFFIXES = {".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte"}
STYLE_SUFFIXES = {".css", ".scss", ".sass", ".less"}
ALL_SUFFIXES = SOURCE_SUFFIXES | STYLE_SUFFIXES
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", "out", "coverage",
    "__pycache__", ".venv", "venv", "vendor", ".turbo", ".cache",
}

FAIL = "fail"
WARN = "warn"


# --------------------------------------------------------------------- model --

@dataclass
class Finding:
    check: str
    severity: str
    path: str
    line: int
    message: str

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        return f"[{self.severity.upper()}] {self.check} · {where}\n    {self.message}"


@dataclass
class CheckRun:
    """What one check actually managed to look at. Absence of findings is only
    meaningful alongside a count of what was examined."""
    check: str
    examined: int = 0
    findings: int = 0


@dataclass
class Report:
    mode: str
    config: dict
    findings: list[Finding] = field(default_factory=list)
    runs: dict[str, CheckRun] = field(default_factory=dict)
    not_checked: list[str] = field(default_factory=list)
    files_seen: dict[str, int] = field(default_factory=dict)
    elements_seen: int = 0
    errored_checks: list[str] = field(default_factory=list)
    unresolved_colours: int = 0
    # Run-level facts, gathered before any per-file check. A codebase has ONE focus
    # policy and one reduced-motion policy, usually in a global stylesheet, so a
    # component file that does not restate it is not a defect. Judging those per file
    # produced 11 false positives on a real site whose globals.css defines
    # `:focus-visible` once, correctly.
    run_has_focus_visible: bool = False
    run_has_reduced_motion: bool = False
    run_focus_source: str = ""

    def run_for(self, check: str) -> CheckRun:
        return self.runs.setdefault(check, CheckRun(check))

    def add(self, check: str, severity: str, path: str, line: int, message: str) -> None:
        self.findings.append(Finding(check, severity, path, line, message))
        self.run_for(check).findings += 1

    def examined(self, check: str, n: int = 1) -> None:
        self.run_for(check).examined += n

    def cannot_check(self, reason: str) -> None:
        if reason not in self.not_checked:
            self.not_checked.append(reason)

    @property
    def failures(self) -> int:
        return sum(1 for f in self.findings if f.severity == FAIL)

    @property
    def warnings(self) -> int:
        return sum(1 for f in self.findings if f.severity == WARN)


# ------------------------------------------------------------------- parsing --

CLICK_ATTRS = ("onclick", "@click", "v-on:click", "on:click")
NON_LABELLED_INPUT_TYPES = {"hidden", "submit", "button", "image", "reset"}
INTERACTIVE_TAGS = {"button", "a", "input", "select", "textarea", "summary", "details"}
PRIMARY_TOKEN = re.compile(r"\b(?:btn-)?(?:primary|cta|accent|filled)\b", re.I)
DESTRUCTIVE_LABEL = re.compile(
    r"\b(delete|remove|destroy|erase|wipe|revoke|restart|reset"
    r"|cancel all|clear all|stop all|delete all|remove all)\b", re.I)


class Element:
    __slots__ = ("tag", "attrs", "line", "parent", "children", "text")

    def __init__(self, tag: str, attrs: dict, line: int, parent):
        self.tag = tag
        self.attrs = attrs
        self.line = line
        self.parent = parent
        self.children: list["Element"] = []
        self.text: list[str] = []

    def attr(self, name: str) -> str | None:
        return self.attrs.get(name.lower())

    def has(self, name: str) -> bool:
        return name.lower() in self.attrs

    def klass(self) -> str:
        return " ".join(v for k, v in self.attrs.items()
                        if k in ("class", "classname") and v)

    def own_text(self) -> str:
        return " ".join(t.strip() for t in self.text if t.strip())


class Tree(HTMLParser):
    """A forgiving element tree. JSX gets parsed too — attribute values in
    braces come through as opaque strings, which is enough for presence checks
    and never enough for value checks, so value checks must not be built on it."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("#document", {}, 0, None)
        self.stack = [self.root]
        self.elements: list[Element] = []

    def handle_starttag(self, tag, attrs):
        d = {}
        for k, v in attrs:
            d[k.lower()] = v if v is not None else ""
        el = Element(tag.lower(), d, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(el)
        self.elements.append(el)
        if tag.lower() not in self.VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        d = {}
        for k, v in attrs:
            d[k.lower()] = v if v is not None else ""
        el = Element(tag.lower(), d, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(el)
        self.elements.append(el)

    def handle_endtag(self, tag):
        tag = tag.lower()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data.strip():
            self.stack[-1].text.append(data)


def line_of(src: str, index: int) -> int:
    return src.count("\n", 0, index) + 1


# ------------------------------------------------------------------- colours --

NAMED_COLOURS = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
    "lime": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
    "cyan": (0, 255, 255), "aqua": (0, 255, 255), "magenta": (255, 0, 255),
    "fuchsia": (255, 0, 255), "silver": (192, 192, 192), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "maroon": (128, 0, 0), "olive": (128, 128, 0),
    "green": (0, 128, 0), "purple": (128, 0, 128), "teal": (0, 128, 128),
    "navy": (0, 0, 128), "orange": (255, 165, 0), "whitesmoke": (245, 245, 245),
    "lightgray": (211, 211, 211), "lightgrey": (211, 211, 211),
    "darkgray": (169, 169, 169), "darkgrey": (169, 169, 169),
    "dimgray": (105, 105, 105), "dimgrey": (105, 105, 105),
}


def parse_colour(value: str):
    """Return (r, g, b) or None. None means unresolvable, which is a
    not-checked, never a pass."""
    if not value:
        return None
    v = value.strip().lower().rstrip(";")
    if v in NAMED_COLOURS:
        return NAMED_COLOURS[v]
    m = re.fullmatch(r"#([0-9a-f]{3})", v)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    m = re.fullmatch(r"#([0-9a-f]{6})", v)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"#([0-9a-f]{8})", v)
    if m:
        h = m.group(1)
        if int(h[6:8], 16) < 255:
            return None  # partial alpha: composite is unknown
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\(\s*([0-9.]+)[\s,]+([0-9.]+)[\s,]+([0-9.]+)"
                     r"(?:[\s,/]+([0-9.]+%?))?\s*\)", v)
    if m:
        if m.group(4) is not None:
            a = m.group(4)
            a_val = float(a.rstrip("%")) / 100 if a.endswith("%") else float(a)
            if a_val < 1.0:
                return None
        return tuple(min(255, int(round(float(m.group(i))))) for i in (1, 2, 3))
    return None  # var(), oklch(), hsl(), currentColor, transparent, inherit


def _channel(c: int) -> float:
    s = c / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    r, g, b = (_channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    lo, hi = sorted((l1, l2))
    return (hi + 0.05) / (lo + 0.05)


DECL = re.compile(r"([-a-z]+)\s*:\s*([^;{}]+)", re.I)
CSS_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)


def declarations(block: str) -> dict:
    return {m.group(1).lower().strip(): m.group(2).strip()
            for m in DECL.finditer(block)}


def css_rules(path: str, src: str):
    """Yield (selector, block, offset) for real CSS only.

    Running the rule regex over a whole HTML file makes the first match absorb every
    byte of preceding markup as its "selector", so a page containing
    `<button type="submit">` anywhere before its <style> block matched selector checks
    that look for `[type=`. That produced two false findings on this gate's own control
    fixture. CSS is read from stylesheets and from <style> contents, and nowhere else."""
    if path.lower().endswith((".css", ".scss", ".sass", ".less")):
        for m in CSS_RULE.finditer(src):
            yield m.group(1).strip(), m.group(2), m.start()
        return
    for blk in STYLE_BLOCK.finditer(src):
        base = blk.start(1)
        for m in CSS_RULE.finditer(blk.group(1)):
            yield m.group(1).strip(), m.group(2), base + m.start()


# -------------------------------------------------------------- the checks ---
# Each check's message names: what you did · what the user silently gets · the fix.

def check_div_onclick(rep: Report, path: str, src: str, tree: Tree) -> None:
    dead = []
    for el in tree.elements:
        if el.tag in ("div", "span", "li", "td", "tr", "p", "section", "article"):
            has_click = any(a in el.attrs for a in CLICK_ATTRS) or "onclick" in el.attrs
            if not has_click:
                continue
            rep.examined("div-onclick")
            if not el.has("role") and not el.has("tabindex"):
                dead.append(el)
    for el in dead:
        rep.add("div-onclick", FAIL, path, el.line,
                f"<{el.tag}> carries a click handler with no role and no tabindex — "
                f"the control is keyboard-dead, so every keyboard and screen-reader "
                f"user loses it entirely and nothing in the rendered page shows that "
                f"it happened; use <button type=\"button\"> (or add role=\"button\" "
                f"tabindex=\"0\" and a keydown handler for Enter and Space).")
    if len(dead) > 3:
        rep.add("div-onclick", FAIL, path, dead[0].line,
                f"{len(dead)} keyboard-dead click handlers in this file — at this "
                f"count it is the navigation pattern, not an oversight. One measured "
                f"run shipped 12 of these carrying the whole navigation of two apps; "
                f"convert the pattern, not the instances.")


def check_focus(rep: Report, path: str, src: str, tree: Tree) -> None:
    lower = src.lower()
    has_focus_style = (":focus-visible" in lower or "focus-visible:" in lower
                       or ":focus" in lower or "focus:" in lower)
    rep.examined("focus-suppressed")
    for m in re.finditer(r"outline\s*:\s*(none|0(?:px)?)\b", src, re.I):
        if not has_focus_style:
            rep.add("focus-suppressed", FAIL, path, line_of(src, m.start()),
                    "outline is removed and this file defines no focus style at all — "
                    "a keyboard user loses any indication of where they are, which is "
                    "invisible to everyone testing with a mouse; pair every "
                    "`outline: none` with a visible `:focus-visible` treatment "
                    "(ring, offset outline, or a 3:1 box-shadow).")
            break

    interactive = [e for e in tree.elements
                   if e.tag in INTERACTIVE_TAGS
                   or any(a in e.attrs for a in CLICK_ATTRS)]
    rep.examined("no-focus-visible", len(interactive))
    if not interactive:
        return
    if ":focus-visible" in lower or "focus-visible:" in lower:
        return
    if rep.run_has_focus_visible:
        # Handled elsewhere in this run, which is the normal and better arrangement.
        return
    # Focus styling may live somewhere this run cannot see. Only judge a file that
    # carries styling of its own; otherwise say so rather than failing it.
    styles_here = ("<style" in lower or "class=" in lower or "classname=" in lower
                   or path.lower().endswith((".css", ".scss", ".sass", ".less")))
    if not styles_here:
        rep.cannot_check(
            f"{path} — has {len(interactive)} interactive element(s) and carries no "
            f"styling of its own, so whether they have a visible focus state cannot be "
            f"decided from this file. Check the shared component or stylesheet that "
            f"styles them")
        return
    rep.add("no-focus-visible", FAIL, path, interactive[0].line,
            f"{len(interactive)} interactive elements, styling defined in this file, and "
            f"no `:focus-visible` anywhere in the paths given — keyboard traversal is "
            f"silent, and the artifact looks correct in every screenshot because focus "
            f"never appears in one; add a `:focus-visible` treatment, ideally once in a "
            f"global stylesheet (Tailwind's `focus:` variant is not the same thing: it "
            f"fires on mouse clicks too, which is why `focus-visible` exists). If the "
            f"focus policy lives outside the paths you passed, pass that file too — this "
            f"check reads the run, not the file. A measured run came back "
            f"`:focus-visible 0, :active 0, :disabled 0` with six `:hover` rules, which "
            f"is the signature of states designed by mouse.")


def _label_targets(tree: Tree) -> tuple[set[str], bool]:
    """Ids that a <label> points at, and whether any label points at a value this
    pass cannot resolve. JSX writes `htmlFor={fieldId}`, so the attribute name and
    the value both differ from HTML, and matching literally reports correct code as
    broken — measured: 5 of 5 label findings on a real site were labelled inputs."""
    ids: set[str] = set()
    unresolved = False
    for el in tree.elements:
        if el.tag != "label":
            continue
        target = el.attr("for") or el.attr("htmlfor")
        if not target:
            continue
        if "{" in target or "}" in target or not target.strip():
            unresolved = True
        else:
            ids.add(target)
    return ids, unresolved


def _has_sibling_label(el: Element) -> bool:
    """A <label for=…>/<label htmlFor=…> in the same container as this control is how
    the pattern is almost always written, and it survives an id this pass cannot
    resolve."""
    parent = el.parent
    if parent is None:
        return False
    for sib in parent.children:
        if sib.tag == "label" and (sib.has("for") or sib.has("htmlfor")):
            return True
    return False


def check_labels(rep: Report, path: str, src: str, tree: Tree) -> None:
    labelled_ids, unresolved_targets = _label_targets(tree)
    for el in tree.elements:
        if el.tag not in ("input", "select", "textarea"):
            continue
        if (el.attr("type") or "").lower() in NON_LABELLED_INPUT_TYPES:
            continue
        rep.examined("label-missing")
        wrapped = False
        p = el.parent
        while p is not None and p.tag != "#document":
            if p.tag == "label":
                wrapped = True
                break
            p = p.parent
        own_id = el.attr("id") or ""
        named = (el.has("aria-label") or el.has("aria-labelledby")
                 or (own_id and own_id in labelled_ids) or wrapped
                 or _has_sibling_label(el))
        if named:
            continue
        if unresolved_targets or "{" in own_id:
            rep.cannot_check(
                f"{path}:{el.line} — a <{el.tag}> whose accessible name depends on an "
                f"id or a label target written as an expression, which this pass cannot "
                f"resolve. Confirm the label reaches it, in the rendered page or by "
                f"reading the component")
            continue
        if el.has("placeholder"):
            rep.add("label-missing", FAIL, path, el.line,
                    f"<{el.tag}> has a placeholder and no label — the label vanishes "
                    f"on the first keystroke, so a user who is interrupted has no way "
                    f"back to what the field was for, autofill loses its hint and a "
                    f"screen reader announces the field unnamed; add "
                    f"<label for=\"…\">, and keep the placeholder for a format "
                    f"example only (\"DD/MM/YYYY\").")
        else:
            rep.add("label-missing", FAIL, path, el.line,
                    f"<{el.tag}> has no accessible name — a screen reader announces "
                    f"an unnamed field and voice control has nothing to say, while "
                    f"the field looks fine on screen; add a visible <label for=\"…\"> "
                    f"or, where the design genuinely has no room, aria-label.")


def check_interactive_in_live_region(rep: Report, path: str, src: str, tree: Tree) -> None:
    """A screen reader reading a live region strips the roles and states of what it
    finds there, so an Undo button announced inside one arrives as the word "Undo"
    and nothing operable. Every visual check passes."""
    for el in tree.elements:
        live = (el.has("aria-live")
                or (el.attr("role") or "").lower() in ("status", "alert"))
        if not live:
            continue
        rep.examined("interactive-in-live-region")
        stack = list(el.children)
        found = []
        while stack:
            node = stack.pop()
            if node.tag in ("button", "a", "input", "select", "textarea") or any(
                    a in node.attrs for a in CLICK_ATTRS):
                found.append(node)
            stack.extend(node.children)
        for node in found:
            rep.add("interactive-in-live-region", FAIL, path, node.line,
                    f"<{node.tag}> {node.own_text()[:30]!r} sits inside a live region "
                    f"(<{el.tag}> with "
                    f"{'aria-live' if el.has('aria-live') else 'role=' + (el.attr('role') or '')})"
                    f" — assistive technology flattens a live region's contents to plain "
                    f"text, stripping the role and state, so this control is announced "
                    f"as a word and cannot be operated. The visual toast works "
                    f"perfectly, which is why this ships. Announce the outcome in the "
                    f"live region and put the control outside it as a real focusable "
                    f"element, or move the action somewhere permanent (a trash view, a "
                    f"history panel, Ctrl/Cmd+Z). A time-limited undo only mouse users "
                    f"can reach is a countdown, not an undo.")


def check_dangling_label(rep: Report, path: str, src: str, tree: Tree) -> None:
    """A label pointing at an id that does not exist announces nothing and looks
    exactly like a working label."""
    ids = {el.attr("id") for el in tree.elements if el.attr("id")}
    ids.discard(None)
    for el in tree.elements:
        if el.tag != "label":
            continue
        target = el.attr("for") or el.attr("htmlfor")
        if not target or "{" in target:
            continue
        rep.examined("dangling-label")
        if target not in ids:
            rep.add("dangling-label", FAIL, path, el.line,
                    f"<label for=\"{target}\"> points at an id that does not exist in "
                    f"this file — the label renders and reads correctly on screen while "
                    f"announcing nothing, so the field is unnamed to a screen reader and "
                    f"clicking the label does not focus the input. Nothing warns. Either "
                    f"correct the id, or confirm the control lives in another file and "
                    f"the pairing holds there.")


def check_hidden_live_region(rep: Report, path: str, src: str, tree: Tree) -> None:
    """`hidden` and `display:none` remove an element from the accessibility tree, so
    a live region carrying either announces nothing however faithfully you write text
    into it. Found in this gate's own "clean" control fixture, which had passed every
    other check — which is why the check exists."""
    for el in tree.elements:
        live = (el.has("aria-live")
                or (el.attr("role") or "").lower() in ("status", "alert", "log"))
        if not live:
            continue
        rep.examined("hidden-live-region")
        style = (el.attr("style") or "").replace(" ", "").lower()
        hidden_attr = el.has("hidden")
        display_none = "display:none" in style
        if hidden_attr or display_none:
            how = "the hidden attribute" if hidden_attr else "display:none"
            has_content = bool(el.own_text() or el.children)
            if not has_content:
                rep.add("hidden-live-region", FAIL, path, el.line,
                        f"<{el.tag}> is an empty live region carrying {how} — that "
                        f"removes it from the accessibility tree, so every message "
                        f"written into it later is announced to nobody, and the visual "
                        f"behaviour is exactly what you intended because you never "
                        f"wanted it seen. This is the hardest version of the "
                        f"live-region trap: the region does exist permanently in the "
                        f"DOM, which is the rule everyone knows, and it still cannot "
                        f"speak. Keep it in the tree and hide it visually instead — a "
                        f"clip-rect utility (`position:absolute; width:1px; height:1px; "
                        f"overflow:hidden; clip-path:inset(50%)`), never `hidden`, "
                        f"`display:none` or `visibility:hidden`. Found in this gate's "
                        f"own clean control fixture, which had passed every other "
                        f"check, which is why the check exists.")
            else:
                rep.add("hidden-live-region", WARN, path, el.line,
                        f"<{el.tag}> is a live region carrying {how} *with its content "
                        f"already inside it* — so it will be revealed complete rather "
                        f"than written into, which is the unreliable shape: some "
                        f"assistive technology announces a region that enters the tree "
                        f"carrying text and some does not, and the two are "
                        f"indistinguishable in a screenshot and in the final DOM. If "
                        f"this is a state placeholder in a mock, that is fine and the "
                        f"live role is doing nothing for it — drop the role from the "
                        f"placeholder. If it is the real announcement path, render the "
                        f"region empty and permanently visible to AT (clip-rect, not "
                        f"`hidden`) and write the text into it.")


def check_img_alt(rep: Report, path: str, src: str, tree: Tree) -> None:
    for el in tree.elements:
        if el.tag != "img":
            continue
        rep.examined("img-alt-missing")
        if not el.has("alt"):
            rep.add("img-alt-missing", FAIL, path, el.line,
                    "<img> has no alt attribute — a screen reader falls back to "
                    "announcing the filename, and in an email with images off the "
                    "space is simply blank; add alt text describing what the image "
                    "conveys, or alt=\"\" if it is decorative (alt=\"\" is correct "
                    "and passes this check).")


def check_motion(rep: Report, path: str, src: str, _tree) -> None:
    has_keyframes = "@keyframes" in src
    has_anim = bool(re.search(r"\banimation(?:-name)?\s*:\s*(?!none)", src, re.I))
    if not (has_keyframes or has_anim):
        return
    rep.examined("motion-unguarded")
    if "prefers-reduced-motion" not in src and not rep.run_has_reduced_motion:
        m = re.search(r"@keyframes|animation\s*:", src, re.I)
        rep.add("motion-unguarded", FAIL, path, line_of(src, m.start() if m else 0),
                "this file animates and carries no `prefers-reduced-motion` block — "
                "a user who has asked their system for less motion gets the full "
                "animation anyway, which for vestibular disorders means nausea rather "
                "than annoyance, and nothing on screen indicates the preference was "
                "ignored; wrap the motion in "
                "`@media (prefers-reduced-motion: no-preference)` or supply a reduced "
                "variant. Note that no browser probe can verify this fix here — "
                "`setEmulatedMedia` is inert in the sanctioned engine, so this is a "
                "source-only guarantee.")


PLACEHOLDER_CONTENT = [
    (r"lorem\s+ipsum", "lorem ipsum"),
    (r"\bLorem\b", "Lorem"),
    (r"\bJohn Doe\b", "John Doe"),
    (r"\bJane Doe\b", "Jane Doe"),
    (r"example@example\.(com|org)", "example@example.com"),
    (r"\bfoo@bar\b", "foo@bar"),
    (r"\bJane Smith\b", "Jane Smith"),
]


def check_placeholder_content(rep: Report, path: str, src: str, _tree) -> None:
    rep.examined("placeholder-content")
    for pattern, label in PLACEHOLDER_CONTENT:
        m = re.search(pattern, src, re.I if label.islower() else 0)
        if m:
            rep.add("placeholder-content", FAIL, path, line_of(src, m.start()),
                    f"placeholder content in the artifact ({label}) — filler copy has "
                    f"an even length and a neutral shape, so it hides exactly the "
                    f"layout and comprehension problems real copy exposes: the "
                    f"40-character company name that overlaps its neighbour, the empty "
                    f"list, the heading that wraps at 360px. Write the real words, and "
                    f"where a fact is genuinely unknown mark it visibly "
                    f"([YOUR PRICE]) rather than inventing one.")


def check_novalidate(rep: Report, path: str, src: str, tree: Tree) -> None:
    for el in tree.elements:
        if el.tag != "form" or not el.has("novalidate"):
            continue
        rep.examined("novalidate-no-states")
        lower = src.lower()
        has_field_errors = ("aria-invalid" in lower or "aria-describedby" in lower
                            or re.search(r'(?:class|classname|id)="[^"]*error', lower))
        if not has_field_errors:
            rep.add("novalidate-no-states", FAIL, path, el.line,
                    "<form novalidate> with no per-field error markup — turning off "
                    "native validation removes a state machine, and shipping nothing "
                    "in its place leaves the terminal state as the only reachable one. "
                    "Its signature, measured on a real contact form: submit three "
                    "empty fields and you land on \"Not sent — your text is still in "
                    "the field above\" when there is no text in any field. Add "
                    "required markers, per-field messages wired with aria-describedby "
                    "and aria-invalid, and drive an empty submit to prove they differ "
                    "from a valid one.")


VERIFICATION_LEAK = [
    r"Verified\s*&\s*Tested", r"Verified and Tested", r"100%\s*pass",
    r"WCAG\s*AA\s*[✓✔]", r"Constant ratio", r"all checks passed",
    r"contrast ratio [\d.]+:1\s*[✓✔]", r"Verification Status",
]


def check_verification_leak(rep: Report, path: str, src: str, _tree) -> None:
    rep.examined("verification-leak")
    for pattern in VERIFICATION_LEAK:
        m = re.search(pattern, src, re.I)
        if m:
            rep.add("verification-leak", FAIL, path, line_of(src, m.start()),
                    f"the artifact asserts its own verification ({m.group(0)!r}) — the "
                    f"reader is owed provenance (source, as-at date, what the axis "
                    f"does) and gets your proof of compliance in the position a "
                    f"disclosure occupies, which tells them the surface was built for "
                    f"a gate rather than for them. Worse, the claim is usually false: "
                    f"one measured run shipped a matrix reading \"Verified & Tested\" "
                    f"on a contrast row the artifact failed on every primary button. "
                    f"Delete it; record what was run in your handoff instead.")


def check_contrast(rep: Report, path: str, src: str, tree: Tree) -> None:
    """Only pairs resolvable in the same rule or the same inline style. Anything
    inherited is unresolvable statically, and guessing it is how a gate lies."""
    unresolved = 0
    pairs = []
    for selector, block, offset in css_rules(path, src):
        decls = declarations(block)
        fg = decls.get("color")
        bg = decls.get("background-color") or decls.get("background")
        if fg and bg:
            f, b = parse_colour(fg), parse_colour(bg)
            if f and b:
                size = decls.get("font-size", "")
                pairs.append((line_of(src, offset), f, b, size, selector))
            else:
                unresolved += 1
        elif fg or bg:
            unresolved += 1
    for el in tree.elements:
        style = el.attr("style") or ""
        if not style:
            continue
        decls = declarations(style)
        fg = decls.get("color")
        bg = decls.get("background-color") or decls.get("background")
        if fg and bg:
            f, b = parse_colour(fg), parse_colour(bg)
            if f and b:
                pairs.append((el.line, f, b, decls.get("font-size", ""), f"<{el.tag}>"))
            else:
                unresolved += 1
        elif fg or bg:
            unresolved += 1

    rep.examined("contrast-below-floor", len(pairs))
    for line, f, b, size, where in pairs:
        ratio = contrast_ratio(f, b)
        large = bool(re.search(r"(1[89]|[2-9]\d)(px|pt)|[1-9]\.\d*rem", size))
        floor = 3.0 if large else 4.5
        if ratio < floor:
            rep.add("contrast-below-floor", WARN, path, line,
                    f"{where} resolves to {ratio:.2f}:1 against a floor of {floor}:1 "
                    f"(WCAG 2.1 SC 1.4.3, Level AA) — text at this ratio is legible on "
                    f"the designer's calibrated screen and gone in sunlight or on a "
                    f"dimmed laptop, and nothing warns because it renders perfectly; "
                    f"darken the foreground or lighten the ground until it clears "
                    f"{floor}:1. One measured run had every primary button at 3.65:1 "
                    f"and one glyph at 1.00:1 — invisible against its own background.")
    if unresolved:
        rep.unresolved_colours += unresolved


def check_live_region(rep: Report, path: str, src: str, _tree) -> None:
    rep.examined("live-region-created-with-text")
    # The live region arrives complete: an innerHTML/insertAdjacentHTML/append whose
    # markup carries both the live container and its text in one insertion. The window
    # is deliberately wide because insertAdjacentHTML takes a position argument first.
    pattern = re.compile(
        r"(innerHTML|insertAdjacentHTML|outerHTML|createContextualFragment)"
        r"[^;\n]{0,240}?(aria-live|role\s*=\s*\\?[\"']?status|role\s*=\s*\\?[\"']?alert)",
        re.I)
    m = pattern.search(src)
    if m:
        rep.add("live-region-created-with-text", WARN, path, line_of(src, m.start()),
                "a live region is being inserted with its text already inside it — "
                "assistive technology watches an *existing* aria-live container for "
                "mutations, so a node that arrives complete is one atomic insertion "
                "with nothing to observe and the message is dropped silently. Both "
                "versions look identical in a screenshot and identical in the final "
                "DOM; the difference is only visible if you diff the DOM before and "
                "after the submit. Render the region empty and permanently in the DOM, "
                "then write text into it.")


def check_competing_primaries(rep: Report, path: str, src: str, tree: Tree) -> None:
    by_parent: dict[int, list[Element]] = {}
    for el in tree.elements:
        if el.tag not in ("button", "a") and not (
                el.tag == "input" and (el.attr("type") or "") in ("submit", "button")):
            continue
        if not PRIMARY_TOKEN.search(el.klass()):
            continue
        by_parent.setdefault(id(el.parent), []).append(el)
    for group in by_parent.values():
        rep.examined("competing-primaries")
        if len(group) > 1:
            labels = ", ".join(g.own_text() or f"<{g.tag}>" for g in group)
            rep.add("competing-primaries", WARN, path, group[0].line,
                    f"{len(group)} primary-weighted actions in one container "
                    f"({labels}) — when two things compete the design has not decided "
                    f"what the surface is for, and the user resolves it by picking the "
                    f"leftmost or leaving; demote all but one to outline or text. "
                    f"Measured on one run, a card header carried `Cancel All Runners` "
                    f"(red) beside `Set Max Concurrency` (blue) at equal weight, "
                    f"destructive first in reading order.")


def check_destructive_gate(rep: Report, path: str, src: str, tree: Tree) -> None:
    lower = src.lower()
    has_gate = any(t in lower for t in (
        "<dialog", "role=\"alertdialog\"", "role='alertdialog'", "confirm(",
        "type-to-confirm", "typetoconfirm", "undo", "aria-modal"))
    has_toast = "toast" in lower or "snackbar" in lower
    hits = []
    for el in tree.elements:
        if el.tag not in ("button", "a"):
            continue
        label = el.own_text() or el.attr("aria-label") or ""
        if DESTRUCTIVE_LABEL.search(label):
            rep.examined("destructive-ungated")
            hits.append((el, label))
    if hits and not has_gate:
        el, label = hits[0]
        mechanism = "a toast and nothing else" if has_toast else "no gate at all"
        rep.add("destructive-ungated", WARN, path, el.line,
                f"{len(hits)} destructive action(s) — first is {label.strip()!r} — with "
                f"{mechanism} in this file: no dialog naming the consequence, no "
                f"type-to-confirm, no undo. The user discovers the blast radius after "
                f"paying for it, and the interface gave them the same 3-second "
                f"confirmation it gives a harmless action. Tabulate every destructive "
                f"action against its gate (action · blast radius · gate built); a row "
                f"whose gate column reads \"toast\" is a defect. Friction scales with "
                f"blast radius: visual distinction, then a named-consequence dialog, "
                f"then type-to-confirm, then a cooling period.")


STATE_SIGNALS = [
    (r'data-state\s*=\s*["\']?([a-z-]+)', "data-state"),
    (r'aria-busy\s*=\s*["\']?true', "loading (aria-busy)"),
    (r'aria-invalid\s*=\s*["\']?true', "error (aria-invalid)"),
    (r'role\s*=\s*["\']?alert', "error (role=alert)"),
    (r'\b(?:class|className)="[^"]*\bskeleton\b', "loading (skeleton)"),
    (r'\b(?:class|className)="[^"]*\bempty(?:-state)?\b', "empty"),
    (r'\b(?:class|className)="[^"]*\berror\b', "error"),
    (r'\b(?:class|className)="[^"]*\bpartial\b', "partial"),
    (r'\b(?:class|className)="[^"]*\b(?:done|success|complete)\b', "done"),
]


def check_state_coverage(rep: Report, path: str, src: str, tree: Tree, expected: int) -> None:
    found: set[str] = set()
    for pattern, name in STATE_SIGNALS:
        for m in re.finditer(pattern, src, re.I):
            found.add(m.group(1).lower() if m.groups() and name == "data-state" else name)
    rep.examined("state-coverage")
    if not found:
        interactive = any(e.tag in INTERACTIVE_TAGS for e in tree.elements)
        if interactive:
            rep.add("state-coverage", WARN, path, 0,
                    f"this artifact carries no state attribute of any kind, so its "
                    f"state coverage is **not countable from the artifact** — that is "
                    f"not the same as zero coverage and must not be reported as it. "
                    f"Add `data-state` (or aria-busy / aria-invalid / role=alert) to "
                    f"the surfaces that change, then the grid can be counted: "
                    f"{expected} required cells per surface (first-run/empty, loading, "
                    f"ideal, partial, error, done), plus offline, disabled and overflow "
                    f"where they apply. A measured run given six named states and no "
                    f"count delivered one.")
    else:
        if len(found) < expected:
            rep.add("state-coverage", WARN, path, 0,
                    f"states: {len(found)} distinct of {expected} expected "
                    f"({', '.join(sorted(found))}) — report this fraction in your "
                    f"handoff rather than the words \"all states designed\"; an "
                    f"unfilled cell is visible and a claim is not. Mark any genuinely "
                    f"inapplicable state `n/a: <reason>`.")


VAGUE_LABELS = {"submit", "ok", "yes", "no", "click here", "learn more",
                "read more", "continue", "next"}


def check_vague_labels(rep: Report, path: str, src: str, tree: Tree) -> None:
    for el in tree.elements:
        if el.tag not in ("button", "a"):
            continue
        label = el.own_text().strip().lower().rstrip(" .!→")
        if not label:
            continue
        rep.examined("vague-label")
        if label in VAGUE_LABELS:
            rep.add("vague-label", WARN, path, el.line,
                    f"<{el.tag}> is labelled {el.own_text().strip()!r} — the label has "
                    f"to predict what happens, and this one does not, so the user "
                    f"either hesitates or commits without knowing to what; a screen "
                    f"reader listing links out of context gets nothing at all. Name "
                    f"the outcome: \"Save changes\", \"Send invitation\", "
                    f"\"View the update\".")


def check_vh_unit(rep: Report, path: str, src: str, _tree) -> None:
    if "100vh" not in src:
        return
    rep.examined("vh-unit")
    mobile = ("viewport" in src or "@media" in src or "max-width" in src)
    if mobile:
        m = re.search(r"100vh", src)
        rep.add("vh-unit", WARN, path, line_of(src, m.start()),
                "100vh on a surface with mobile breakpoints — mobile browser chrome "
                "is counted inside 100vh, so the bottom of the layout sits under the "
                "URL bar and the user scrolls a page that was meant to fit exactly; "
                "it looks correct in every desktop render. Use 100dvh (or min-h-dvh).")


def check_fixed_height_controls(rep: Report, path: str, src: str, _tree) -> None:
    for selector, block, offset in css_rules(path, src):
        if not re.search(r"\b(button|\.btn|\[type=|a\.|\.cta)", selector, re.I):
            continue
        decls = declarations(block)
        if "height" in decls and "min-height" not in decls:
            rep.examined("fixed-height-control")
            rep.add("fixed-height-control", WARN, path, line_of(src, offset),
                    f"{selector} sets a fixed height with no min-height — text that "
                    f"grows (a translation, a longer label, a larger system font) "
                    f"overflows the box silently, with no scrollbar and no warning. "
                    f"Measured on one run, five prominent controls spilled their own "
                    f"fixed-height boxes and one had its arrow glyph clipped by the "
                    f"button's bottom border. Use min-height with padding. This one "
                    f"only shows properly in a render: confirm with "
                    f"`--probe`, which compares scrollHeight against client height.")


def check_touch_targets(rep: Report, path: str, src: str, _tree) -> None:
    for selector, block, offset in css_rules(path, src):
        if not re.search(r"\b(button|\.btn|\[type=|a\.|\.icon|\.chip)", selector, re.I):
            continue
        decls = declarations(block)
        for prop in ("width", "height", "min-width", "min-height"):
            val = decls.get(prop, "")
            mm = re.fullmatch(r"(\d+(?:\.\d+)?)px", val.strip())
            if not mm:
                continue
            rep.examined("touch-target-small")
            px = float(mm.group(1))
            if px < 24:
                rep.add("touch-target-small", WARN, path, line_of(src, offset),
                        f"{selector} sets {prop}: {val} — below 24 CSS px, which is "
                        f"the WCAG 2.2 SC 2.5.8 Target Size (Minimum) floor at Level "
                        f"**AA**. A user with a tremor or a large thumb misses it and "
                        f"hits the neighbour, and on a mouse-driven desktop nobody "
                        f"notices. Either reach 24×24 CSS px or qualify under the "
                        f"Spacing exception: a 24 px-diameter circle centred on the "
                        f"target must overlap no other target's circle. Note the "
                        f"units: 44×44 CSS px is SC 2.5.5 at Level **AAA** (a craft "
                        f"target, not an AA failure), Apple's 44 is **pt** and "
                        f"Android's 48 is **dp** — neither is a WCAG number.")


# ------------------------------------------------------------ static driver --

def collect_files(paths: list[str], rep: Report) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            print(f"ux-lint: path does not exist: {raw}", file=sys.stderr)
            continue
        if p.is_file():
            if p.suffix.lower() in ALL_SUFFIXES:
                out.append(p)
            else:
                rep.cannot_check(f"{p} — suffix {p.suffix or '(none)'} is not a "
                                 f"surface this gate reads")
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for f in sorted(files):
                fp = Path(root) / f
                if fp.suffix.lower() in ALL_SUFFIXES:
                    out.append(fp)
    return sorted(set(out))


STATIC_CHECKS = [
    ("div-onclick", check_div_onclick),
    ("focus", check_focus),
    ("label-missing", check_labels),
    ("dangling-label", check_dangling_label),
    ("interactive-in-live-region", check_interactive_in_live_region),
    ("hidden-live-region", check_hidden_live_region),
    ("img-alt-missing", check_img_alt),
    ("motion-unguarded", check_motion),
    ("placeholder-content", check_placeholder_content),
    ("novalidate-no-states", check_novalidate),
    ("verification-leak", check_verification_leak),
    ("contrast-below-floor", check_contrast),
    ("live-region-created-with-text", check_live_region),
    ("competing-primaries", check_competing_primaries),
    ("destructive-ungated", check_destructive_gate),
    ("vague-label", check_vague_labels),
    ("vh-unit", check_vh_unit),
    ("fixed-height-control", check_fixed_height_controls),
    ("touch-target-small", check_touch_targets),
]


def run_static(paths: list[str], expected_states: int, rep: Report) -> None:
    files = collect_files(paths, rep)

    # Pre-scan for run-level policy before judging any single file. Focus and
    # reduced-motion are codebase-wide policies that normally live in one global
    # stylesheet; a component that does not restate them is not a defect.
    for fp in files:
        try:
            head = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        low = head.lower()
        if ":focus-visible" in low or "focus-visible:" in low:
            if not rep.run_has_focus_visible:
                rep.run_focus_source = str(fp)
            rep.run_has_focus_visible = True
        if "prefers-reduced-motion" in low:
            rep.run_has_reduced_motion = True
    if rep.run_has_focus_visible:
        rep.config["focus_policy"] = rep.run_focus_source

    for fp in files:
        suffix = fp.suffix.lower()
        kind = "style" if suffix in STYLE_SUFFIXES else (
            "html" if suffix in (".html", ".htm") else "component")
        rep.files_seen[kind] = rep.files_seen.get(kind, 0) + 1
        try:
            src = fp.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            rep.cannot_check(f"{fp} — could not be read ({exc})")
            continue
        tree = Tree()
        if kind != "style":
            try:
                tree.feed(src)
                tree.close()
            except Exception:
                rep.cannot_check(f"{fp} — markup could not be parsed into a tree; "
                                 f"element-scoped checks did not run on it")
        rep.elements_seen += len(tree.elements)
        rel = str(fp)
        for name, fn in STATIC_CHECKS:
            try:
                fn(rep, rel, src, tree)
            except Exception as exc:  # a check that raises must not read as clean
                rep.errored_checks.append(f"{name} on {rel}: {exc}")
        try:
            check_state_coverage(rep, rel, src, tree, expected_states)
        except Exception as exc:
            rep.errored_checks.append(f"state-coverage on {rel}: {exc}")

    if not files:
        return

    if rep.unresolved_colours:
        rep.cannot_check(
            f"contrast for {rep.unresolved_colours} colour declaration(s) across the run "
            f"whose pair is inherited, a var()/oklch()/hsl() value, or partially "
            f"transparent — a static pass cannot resolve those and the composited result "
            f"is not zero. Follow the token to its value, or use --probe on the rendered "
            f"page")

    rep.cannot_check("screen-reader output, real keyboard traversal and actual "
                     "assistive-technology behaviour — these need a device and a "
                     "person, and no static or rendered check substitutes")
    rep.cannot_check("whether a colour resolved through var()/oklch()/theme tokens "
                     "clears its contrast floor — follow the token to its value or "
                     "measure the rendered page")
    rep.cannot_check("reduced-motion behaviour — the sanctioned engine accepts "
                     "setEmulatedMedia and does nothing, so matchMedia stays false "
                     "and there is no reduced-motion pass to run")
    rep.cannot_check("whether the copy is right for the audience, whether the flow "
                     "shape is the correct one, and whether the primary action is the "
                     "one the user came for — this gate checks a class of defect, "
                     "never a surface")


# ------------------------------------------------------------- probe driver --

PROBE_EXPR = """(() => {
  const out = {url: location.href, doc: {}, elements: [], counts: {}, pairs: []};
  const d = document.documentElement;
  out.doc.scrollWidth = d.scrollWidth;
  out.doc.clientWidth = d.clientWidth;
  out.doc.scrollHeight = d.scrollHeight;
  out.doc.clientHeight = d.clientHeight;
  const q = (s) => document.querySelectorAll(s).length;
  out.counts.role = q('[role]');
  out.counts.tabindex = q('[tabindex]');
  out.counts.ariaLabel = q('[aria-label]');
  out.counts.ariaLive = q('[aria-live],[role=status],[role=alert]');
  out.counts.nativeFormControls = q('input,select,textarea,progress,meter');
  out.counts.animations = (document.getAnimations ? document.getAnimations().length : -1);
  const sel = 'button,a,input,select,textarea,[role=button],[onclick]';
  const nodes = Array.from(document.querySelectorAll(sel)).slice(0, 400);
  for (const el of nodes) {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    out.elements.push({
      tag: el.tagName.toLowerCase(),
      type: el.getAttribute('type') || '',
      text: (el.textContent || '').trim().slice(0, 60),
      w: Math.round(r.width * 100) / 100,
      h: Math.round(r.height * 100) / 100,
      scrollH: el.scrollHeight,
      clientH: el.clientHeight,
      scrollW: el.scrollWidth,
      clientW: el.clientWidth,
      color: cs.color,
      background: cs.backgroundColor,
      fontSize: cs.fontSize,
      paddingTop: cs.paddingTop,
      paddingLeft: cs.paddingLeft
    });
  }
  return JSON.stringify(out);
})()"""

PRIVATE_HOST = re.compile(
    r"^https?://(localhost|127\.|0\.0\.0\.0|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|\[::1\])",
    re.I)


def run_probe(url: str, rep: Report) -> int:
    if shutil.which("obscura") is None:
        print("ux-lint: obscura is not on PATH, so --probe cannot run in this "
              "environment.\n"
              "         A static run is not a substitute: it cannot see resolved "
              "colours,\n"
              "         real geometry, or a control overflowing its own box.\n"
              "         Install Obscura, or run --static and record the probe under "
              "\"Not checked\".",
              file=sys.stderr)
        return 3

    cmd = ["obscura", "fetch", url, "--eval", PROBE_EXPR]
    if PRIVATE_HOST.match(url):
        cmd.insert(1, "--allow-private-network")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"ux-lint: obscura timed out on {url} after 120s. Nothing was "
              f"measured; do not record this as a pass.", file=sys.stderr)
        return 2
    if proc.returncode != 0:
        # Relay verbatim: the message is environment-aware.
        print(f"ux-lint: obscura exited {proc.returncode}. Its output, verbatim:\n"
              f"{proc.stdout.strip()}\n{proc.stderr.strip()}", file=sys.stderr)
        return 2

    raw = proc.stdout.strip()
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        print(f"ux-lint: obscura returned no JSON payload for {url}. Nothing was "
              f"measured.\nRaw output:\n{raw[:800]}", file=sys.stderr)
        return 2
    try:
        data = json.loads(json.loads(m.group(0)) if m.group(0).startswith('"') else m.group(0))
    except (json.JSONDecodeError, TypeError):
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError as exc:
            print(f"ux-lint: could not parse the probe payload ({exc}).", file=sys.stderr)
            return 2

    els = data.get("elements", [])
    rep.elements_seen = len(els)
    doc = data.get("doc", {})
    counts = data.get("counts", {})

    rep.examined("h-overflow", 1)
    if doc.get("scrollWidth", 0) > doc.get("clientWidth", 0) + 1:
        rep.add("h-overflow", FAIL, url, 0,
                f"the document scrolls horizontally: scrollWidth "
                f"{doc['scrollWidth']}px against a viewport of {doc['clientWidth']}px "
                f"— the user drags sideways to read, and on a phone the overflow "
                f"usually hides the right edge of every row rather than announcing "
                f"itself. Find the element wider than its container (a fixed width, "
                f"an unwrapped table, a panel sized by its own content) and constrain "
                f"it to the viewport with max-width: 100vw and box-sizing: border-box.")

    for el in els:
        rep.examined("control-overflow")
        if el["scrollH"] > el["clientH"] + 1 and el["clientH"] > 0:
            rep.add("control-overflow", WARN, url, 0,
                    f"<{el['tag']}> {el['text']!r} overflows its own box: scrollHeight "
                    f"{el['scrollH']}px against clientHeight {el['clientH']}px — the "
                    f"text is clipped by the control's own border, which a longer "
                    f"label or a translation makes worse and which no source review "
                    f"catches. Replace the fixed height with min-height plus padding.")

    small = [e for e in els if 0 < e["w"] < 24 or 0 < e["h"] < 24]
    rep.examined("touch-target-small", len(els))
    for el in small[:20]:
        rep.add("touch-target-small", WARN, url, 0,
                f"<{el['tag']}> {el['text']!r} renders {el['w']}×{el['h']} CSS px — "
                f"under the 24×24 floor of WCAG 2.2 SC 2.5.8 at Level AA. It may still "
                f"conform under the Spacing exception (a 24px-diameter circle centred "
                f"on it overlapping no other target's circle), so check the "
                f"neighbours before filing it. 44×44 CSS px is SC 2.5.5 at AAA; "
                f"Apple's 44pt and Android's 48dp are craft targets in "
                f"density-independent units and are not WCAG numbers.")

    pairs = 0
    for el in els:
        fg, bg = parse_colour(el.get("color", "")), parse_colour(el.get("background", ""))
        if not fg or not bg:
            continue
        pairs += 1
        ratio = contrast_ratio(fg, bg)
        size = el.get("fontSize", "")
        mm = re.match(r"([\d.]+)px", size)
        large = bool(mm and float(mm.group(1)) >= 18.66)
        floor = 3.0 if large else 4.5
        if ratio < floor:
            rep.add("contrast-below-floor", WARN, url, 0,
                    f"<{el['tag']}> {el['text']!r} renders at {ratio:.2f}:1 against a "
                    f"{floor}:1 floor (WCAG SC 1.4.3, AA) — legible on a calibrated "
                    f"screen, gone in sunlight, and perfect in every screenshot.")
    rep.examined("contrast-below-floor", pairs)
    transparent = len(els) - pairs
    if transparent:
        rep.cannot_check(
            f"contrast for {transparent} of {len(els)} controls whose background "
            f"resolved to transparent or a non-literal colour — the composited value "
            f"behind them is not measurable this way and is not zero")

    if counts.get("nativeFormControls", 0):
        rep.cannot_check(
            f"the rendering of {counts['nativeFormControls']} native form control(s) "
            f"on this page — the sanctioned engine renders none of them at all: a real "
            f"radio input renders as nothing, which looks exactly like a missing "
            f"affordance. Never file a native control as absent from this probe; check "
            f"it in a real browser or from source")
    if counts.get("animations", -1) == 0:
        rep.cannot_check(
            "motion — CSS animations and transitions never execute in this engine "
            "(getAnimations() returned 0, which is the engine and not the page), so "
            "no motion, entry-animation or transition finding is available. An "
            "opacity:0 entry keyframe also strands its element near 0.03 here, which "
            "reads exactly like a z-index bug")
    rep.cannot_check("reduced-motion and print — setEmulatedMedia is accepted and "
                     "inert here, so matchMedia stays false and neither pass exists")
    rep.cannot_check("web-font fidelity — web fonts never load in this engine, so "
                     "font rendering is unmeasured rather than matching")
    rep.cannot_check("box-shadow, background-image, text-transform and outline — each "
                     "returns empty in this engine meaning \"not implemented\", not "
                     "\"not set\"; a missing focus outline cannot be concluded here")
    rep.cannot_check("pseudo-element content and styling — getComputedStyle ignores "
                     "the pseudo argument in this engine and returns the element's "
                     "own style, so any ::before/::after check silently measures the "
                     "wrong thing")
    rep.cannot_check("responsive behaviour at other viewports — this probe renders at "
                     "a fixed 1280x720; use obscura serve plus CDP "
                     "setDeviceMetricsOverride for breakpoint work")
    rep.cannot_check("screen-reader output and real keyboard traversal — a device and "
                     "a person, and no probe substitutes")

    rep.config["counts"] = counts
    return 0


# ------------------------------------------------------------------ reporting --

def emit(rep: Report, as_json: bool) -> None:
    if as_json:
        print(json.dumps({
            "version": VERSION,
            "mode": rep.mode,
            "config": rep.config,
            "findings": [asdict(f) for f in rep.findings],
            "measured": {k: asdict(v) for k, v in sorted(rep.runs.items())},
            "not_checked": rep.not_checked,
            "files": rep.files_seen,
            "elements": rep.elements_seen,
            "errored_checks": rep.errored_checks,
            "failures": rep.failures,
            "warnings": rep.warnings,
        }, indent=2))
        return

    print(f"ux-lint {VERSION} · mode {rep.mode}")
    print("Config:      " + " · ".join(f"{k}={v}" for k, v in rep.config.items()
                                       if k != "counts"))
    print()

    fails = [f for f in rep.findings if f.severity == FAIL]
    warns = [f for f in rep.findings if f.severity == WARN]
    for f in fails:
        print(f.render())
        print()
    for f in warns:
        print(f.render(), file=sys.stderr)
        print(file=sys.stderr)

    total_files = sum(rep.files_seen.values())
    breakdown = ", ".join(f"{v} {k}" for k, v in sorted(rep.files_seen.items())) or "none"
    print(f"Examined:    {total_files} files ({breakdown}) · "
          f"{rep.elements_seen} elements")
    if rep.runs:
        print("Measured:")
        for name, run in sorted(rep.runs.items()):
            print(f"             {name} → examined={run.examined} "
                  f"findings={run.findings}")
    else:
        print("Measured:    nothing — no check found anything to look at")
    print("Not checked:")
    if not rep.not_checked:
        print("             NOTHING LISTED — this is itself a defect. An empty "
              "not-checked list")
        print("             means the scope of the checks was confused with the "
              "scope of the artifact.")
    for reason in rep.not_checked:
        wrapped = reason
        print(f"             - {wrapped}")
    if rep.errored_checks:
        print("Errored:")
        for e in rep.errored_checks:
            print(f"             ! {e}")
        print("             A check that raised did not run. This result is unknown, "
              "not clean.")
    print(f"Result:      {rep.failures} failures, {rep.warnings} warnings")


# ----------------------------------------------------------------------- cli --

EPILOG = """exit codes
  0  no failures
  1  failures present
  2  examined zero files or zero elements, or the probe returned nothing
     (a refusal, not a pass)
  3  unrecognised configuration, bad usage, or obscura unavailable for --probe
  4  a check raised while running; the result is unknown rather than clean

Warnings go to stderr and never change the exit code. Only exit 0 is a pass.
"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="ux-lint.py",
        description="The deterministic gate for ux-craft. Refuses UX failures "
                    "that ship silently.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="files or directories to walk")
    ap.add_argument("--static", nargs="*", dest="static_paths", metavar="PATH",
                    help="walk source files (the default mode)")
    ap.add_argument("--probe", metavar="URL",
                    help="measure a rendered page through Obscura")
    ap.add_argument("--expected-states", type=int, default=6, metavar="N",
                    help="required state cells per surface (default 6: "
                         "first-run/empty, loading, ideal, partial, error, done)")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    ap.add_argument("--version", action="version", version=f"ux-lint {VERSION}")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        return 3 if exc.code else 0

    if args.expected_states < 1 or args.expected_states > 20:
        print("ux-lint: --expected-states must be between 1 and 20; the six required "
              "cells are the floor and more than a handful of conditional ones means "
              "the grid has stopped being countable.", file=sys.stderr)
        return 3

    if args.probe:
        rep = Report(mode="probe", config={"url": args.probe, "engine": "obscura"})
        code = run_probe(args.probe, rep)
        if code:
            return code
        if rep.elements_seen == 0:
            emit(rep, args.json)
            print("ux-lint: the probe matched zero interactive elements. That is a "
                  "refusal, not a pass — a page with no buttons, links or inputs is "
                  "either the wrong URL or a page that did not render.",
                  file=sys.stderr)
            return 2
        emit(rep, args.json)
        return 4 if rep.errored_checks else (1 if rep.failures else 0)

    paths = (args.static_paths or []) + args.paths
    if not paths:
        print("ux-lint: nothing to check. Pass paths to walk, or --probe <url>.\n"
              "         Run --help for the exit-code table.", file=sys.stderr)
        return 3

    rep = Report(mode="static", config={"paths": ",".join(paths),
                                        "expected_states": args.expected_states})
    run_static(paths, args.expected_states, rep)
    emit(rep, args.json)

    if sum(rep.files_seen.values()) == 0:
        print("ux-lint: examined zero files. That is a refusal, not a pass — the "
              "paths held nothing this gate reads (.html .htm .jsx .tsx .js .ts "
              ".vue .svelte .css .scss .sass .less).", file=sys.stderr)
        return 2
    if rep.errored_checks:
        return 4
    return 1 if rep.failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
