#!/usr/bin/env python3
"""Compile a declarative screen spec into a terminal cell frame.

The reason this script exists rather than a convention for drawing mocks by hand:
a model asked to draw a terminal layout in a fenced code block counts characters,
and characters are not cells. `len("\U0001F680 Deploy")` is 8; it occupies 9
cells. Every column after that one is then off by one, the border does not close,
and the mock looks fine in the message that produced it. The same arithmetic goes
wrong the same way in CJK labels, in box-drawing runs, and in any string a
combining mark passes through.

So the spec never contains a column number. It declares intent -- these panels
split the screen this way, this table has these columns, this footer carries
these keys -- and the compiler does every piece of cell arithmetic, using the
same width function the capture side uses. What comes out is a frame in
tui-craft's schema, marked `kind: "mock"`, which its gates read directly.

A mock is a proposal, never evidence. The frame says so in its own kind field,
and tui-craft's gates print an advisory when they are handed one. What the
compiler *can* settle is whether a design fits at a given size, which is the
question a mock is usually drawn to answer and the one a hand-drawn mock answers
wrongly.

Usage
-----
    tui_mock.py spec.json -o frame.json        # compile
    tui_mock.py spec.json --dump               # ruler dump to read
    tui_mock.py spec.json --ansi               # paint it in this terminal
    tui_mock.py spec.json --fit                # only the fit report
    tui_mock.py --self-test                    # golden cases for the arithmetic
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path

SCHEMA_VERSION = "tui-craft/frame/1"
SPEC_VERSION = "tui-design/spec/1"

# --------------------------------------------------------------------------
# Cell arithmetic -- imported, never reimplemented
#
# This is the one thing that must not be a copy. A mock measured by different
# arithmetic from the capture it will later be compared against disagrees with
# the instrument for reasons that have nothing to do with the design, and the
# disagreement looks exactly like a layout bug.
#
# An earlier draft of this file carried its own copy of `char_width` plus a
# self-test that cross-checked it against tui-craft's. That check passed only
# because the two sat side by side in the development tree; installed as two
# separate plugins it would have silently degraded to unchecked, which is worse
# than no check at all. Both skills live in one plugin so this import is a fixed
# relative path rather than a search.
# --------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent
                      / "tui-craft" / "scripts"))
try:
    from tui_capture import char_width, string_width  # noqa: E402
except ImportError as e:  # pragma: no cover
    print("Cannot import the cell-width arithmetic from tui-craft's "
          "tui_capture.py, which sits beside this skill in the same plugin. "
          "Refusing to guess at cell widths: every column in the output would "
          f"be unverifiable. ({e})", file=sys.stderr)
    raise SystemExit(2)


def clusters(s: str) -> list[str]:
    """Split into printable units, keeping zero-width code points attached to the
    character they modify.

    This is not UAX #29 grapheme segmentation, and it should not be mistaken for
    it: it handles combining marks, ZWJ sequences and variation selectors, which
    is what terminal text actually throws at a layout, and it will get exotic
    cases wrong. Writing a full segmenter here would be the mistake the research
    warns about. Where a spec's text is user-supplied and may contain arbitrary
    Unicode, compile it and then capture the real app rather than trusting this.
    """
    out: list[str] = []
    for ch in s:
        if out and char_width(ch) == 0:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def truncate(s: str, width: int, marker: str = "…") -> tuple[str, bool]:
    """Cut a string to `width` cells, appending a marker if anything was lost.

    Returns (text, was_truncated). The marker matters: tui-craft has a gate for
    text cut with nothing to say it was cut, because a silently clipped string
    reads as a short string and the reader never learns there was more.
    """
    if string_width(s) <= width:
        return s, False
    if width <= 0:
        return "", True
    mw = string_width(marker)
    budget = width - mw
    if budget < 0:
        return marker[:width], True
    kept, used = [], 0
    for cl in clusters(s):
        w = string_width(cl)
        if used + w > budget:
            break
        kept.append(cl)
        used += w
    return "".join(kept) + marker, True


# --------------------------------------------------------------------------
# Frame
# --------------------------------------------------------------------------


@dataclass
class Cell:
    ch: str = " "
    w: int = 1          # 0 = continuation of a wide cell to its left
    fg: str = "default"
    bg: str = "default"
    bold: bool = False
    dim: bool = False
    italic: bool = False
    underline: bool = False
    reverse: bool = False


BORDERS = {
    "single": "┌┐└┘─│",
    "round":  "╭╮╰╯─│",
    "double": "╔╗╚╝═║",
    "heavy":  "┏┓┗┛━┃",
}


class Canvas:
    """A grid that clips at its own edges and records what it lost.

    Every widget paints through this. Clipping silently is what makes a
    hand-drawn mock lie, so a clip is recorded as a fit finding rather than just
    happening.
    """

    def __init__(self, cols: int, rows: int):
        self.cols, self.rows = cols, rows
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.fit: list[dict] = []

    def note(self, kind: str, **kw):
        self.fit.append({"kind": kind, **kw})

    def put(self, x: int, y: int, s: str, *, fg="default", bg="default",
            bold=False, dim=False, reverse=False, underline=False, italic=False,
            limit: int | None = None, where: str = "") -> int:
        """Write a string starting at cell (x, y). Returns cells advanced.

        `limit` is the number of cells the caller has to spend. Text longer than
        that is truncated with a marker and recorded, because a widget that
        quietly eats its own label is the defect this whole script exists to make
        visible.
        """
        if not (0 <= y < self.rows):
            self.note("row-off-frame", row=y, where=where, text=s[:40])
            return 0
        room = self.cols - x if limit is None else min(limit, self.cols - x)
        # Painting text must not erase the surface it is painted on. Passing no
        # bg means "keep what is there", not "reset to the terminal default".
        if room <= 0:
            self.note("no-room", row=y, col=x, where=where, text=s[:40])
            return 0
        text, cut = truncate(s, room)
        if cut:
            self.note("truncated", row=y, col=x, where=where,
                      wanted=string_width(s), had=room, text=s[:60])
        cx = x
        for cl in clusters(text):
            w = string_width(cl)
            if w == 0:
                continue
            if cx + w > self.cols:
                break
            under = self.cells[y][cx].bg
            eff_bg = under if bg == "default" else bg
            self.cells[y][cx] = Cell(ch=cl, w=w, fg=fg, bg=eff_bg, bold=bold, dim=dim,
                                     reverse=reverse, underline=underline, italic=italic)
            for k in range(1, w):
                self.cells[y][cx + k] = Cell(ch="", w=0, fg=fg, bg=eff_bg, bold=bold,
                                             dim=dim, reverse=reverse)
            cx += w
        return cx - x

    def fill(self, x: int, y: int, w: int, h: int, *, bg: str):
        for yy in range(max(0, y), min(self.rows, y + h)):
            for xx in range(max(0, x), min(self.cols, x + w)):
                c = self.cells[yy][xx]
                self.cells[yy][xx] = Cell(ch=c.ch, w=c.w, fg=c.fg, bg=bg, bold=c.bold,
                                          dim=c.dim, reverse=c.reverse,
                                          underline=c.underline, italic=c.italic)

    def hline(self, x: int, y: int, w: int, ch: str, **kw):
        if not (0 <= y < self.rows):
            return
        for xx in range(max(0, x), min(self.cols, x + w)):
            self.put(xx, y, ch, **kw)

    def vline(self, x: int, y: int, h: int, ch: str, **kw):
        for yy in range(max(0, y), min(self.rows, y + h)):
            self.put(x, yy, ch, **kw)


# --------------------------------------------------------------------------
# Theme
# --------------------------------------------------------------------------

# Two starting themes, each run through `tui_design_gates.py` until it reported
# no role-ladder failure. That run is what set `border`: it began at #4C5464,
# measured 2.44:1 against the dark surface, and failed the 3:1 floor an
# information-carrying line has to clear. Chosen by eye it looked fine.
#
# The floors are stricter than the reference corpus, deliberately. 27 of the 34
# colour-measurable frames in it carry at least one glyph role under 3:1, so the
# corpus is evidence about what ships, not an authority on contrast.
THEMES = {
    "dark": {
        "surface":     {"bg": "#111318"},
        "surface-lift": {"bg": "#1A1D24"},
        "text":        {"fg": "#E4E7EC"},
        "text-strong": {"fg": "#FFFFFF", "bold": True},
        "text-dim":    {"fg": "#9BA3B2"},
        "border":      {"fg": "#5A6478"},
        "border-focus": {"fg": "#6FC3E8"},
        "accent":      {"fg": "#6FC3E8"},
        "ok":          {"fg": "#63C68B"},
        "warn":        {"fg": "#D9A441"},
        "danger":      {"fg": "#E8736C"},
        "selected":    {"reverse": True},
        "selected-fill": {"fg": "#111318", "bg": "#6FC3E8"},
    },
    "light": {
        "surface":     {"bg": "#FAF9F6"},
        "surface-lift": {"bg": "#EFEDE6"},
        "text":        {"fg": "#1B1D21"},
        "text-strong": {"fg": "#000000", "bold": True},
        "text-dim":    {"fg": "#5A5F69"},
        "border":      {"fg": "#7C818B"},
        "border-focus": {"fg": "#1F5FA8"},
        "accent":      {"fg": "#1F5FA8"},
        "ok":          {"fg": "#1F6B3A"},
        "warn":        {"fg": "#7A5100"},
        "danger":      {"fg": "#A32118"},
        "selected":    {"reverse": True},
        "selected-fill": {"fg": "#FAF9F6", "bg": "#1F5FA8"},
    },
}


class Theme:
    def __init__(self, spec: dict):
        base = THEMES.get(spec.get("theme", "dark"), THEMES["dark"])
        self.roles = {k: dict(v) for k, v in base.items()}
        for k, v in (spec.get("roles") or {}).items():
            self.roles.setdefault(k, {}).update(v)
        self.name = spec.get("theme", "dark")
        self.unknown: set[str] = set()

    def style(self, role: str | None, *, default="text") -> dict:
        if role is None:
            role = default
        r = self.roles.get(role)
        if r is None:
            self.unknown.add(role)
            r = self.roles.get(default, {})
        out = {"fg": r.get("fg", "default"), "bg": r.get("bg", "default"),
               "bold": bool(r.get("bold")), "dim": bool(r.get("dim")),
               "reverse": bool(r.get("reverse")), "underline": bool(r.get("underline")),
               "italic": bool(r.get("italic"))}
        return out


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------


@dataclass
class Region:
    x: int
    y: int
    w: int
    h: int


def split(region: Region, node: dict, cv: Canvas) -> list[tuple[Region, dict]]:
    """Divide a region among children along one axis.

    Fixed sizes are honoured first, the remainder is shared by weight, and the
    rounding remainder goes to the last flexible child so the children always sum
    to exactly the parent. A layout whose children sum to one cell less than
    their parent is how a one-column gap appears down the middle of a screen for
    no reason anyone can find later.
    """
    kids = node.get("children") or []
    if not kids:
        return []
    horizontal = node.get("dir", "col") == "row"
    gap = int(node.get("gap", 0))
    total = (region.w if horizontal else region.h) - gap * (len(kids) - 1)
    if total < 0:
        cv.note("gap-exceeds-space", where=node.get("id", ""), kids=len(kids), gap=gap)
        total = 0

    sizes: list[int | None] = []
    for k in kids:
        fixed = k.get("w") if horizontal else k.get("h")
        sizes.append(int(fixed) if fixed is not None else None)

    fixed_sum = sum(s for s in sizes if s is not None)
    if fixed_sum > total:
        cv.note("fixed-children-overflow", where=node.get("id", ""),
                wanted=fixed_sum, had=total)
    free = max(0, total - fixed_sum)
    weights = [float(k.get("flex", 1)) if s is None else 0.0
               for k, s in zip(kids, sizes)]
    wsum = sum(weights)
    flexible = [i for i, s in enumerate(sizes) if s is None]
    if flexible:
        for i in flexible:
            sizes[i] = int(free * weights[i] / wsum) if wsum else 0
        drift = free - sum(sizes[i] for i in flexible)
        sizes[flexible[-1]] += drift

    out, cursor = [], (region.x if horizontal else region.y)
    for k, s in zip(kids, sizes):
        s = max(0, int(s or 0))
        r = (Region(cursor, region.y, s, region.h) if horizontal
             else Region(region.x, cursor, region.w, s))
        out.append((r, k))
        cursor += s + gap
    return out


# --------------------------------------------------------------------------
# Widgets
# --------------------------------------------------------------------------


class Painter:
    def __init__(self, cv: Canvas, theme: Theme):
        self.cv, self.th = cv, theme
        self.focus_signals: list[dict] = []
        self.regions: list[dict] = []

    def paint(self, region: Region, node: dict):
        if region.w <= 0 or region.h <= 0:
            if node:
                self.cv.note("zero-size-node", where=node.get("id", ""),
                             kind=self._kind(node), w=region.w, h=region.h)
            return
        kind = self._kind(node)
        fn = getattr(self, f"_w_{kind.replace('-', '_')}", None)
        if fn is None:
            self.cv.note("unknown-widget", where=node.get("id", ""), kind=kind)
            return
        if kind not in ("container", "blank"):
            label = node.get("id") or (node.get(kind) or {}).get("title") \
                or (node.get(kind) or {}).get("label") or kind
            self.regions.append({"kind": kind, "label": str(label),
                                 "x": region.x, "y": region.y,
                                 "w": region.w, "h": region.h})
        fn(region, node)

    @staticmethod
    def _kind(node: dict) -> str:
        if "children" in node:
            return "container"
        for k in ("panel", "table", "pairs", "text", "list", "chips",
                  "keybar", "gauge", "blank"):
            if k in node:
                return k
        return "blank"

    # -- container ---------------------------------------------------------

    def _w_container(self, region: Region, node: dict):
        for r, k in split(region, node, self.cv):
            self.paint(r, k)

    def _w_blank(self, region: Region, node: dict):
        spec = node.get("blank") or {}
        if isinstance(spec, dict) and spec.get("role"):
            st = self.th.style(spec["role"])
            self.cv.fill(region.x, region.y, region.w, region.h, bg=st["bg"])

    # -- panel -------------------------------------------------------------

    def _w_panel(self, region: Region, node: dict):
        """A bordered box whose border carries metadata.

        The border is a shelf: a title on the left of the top rule, optional
        centre and right slots, and two more on the bottom rule. That is the
        single most common move in the reference corpus and it buys a row of
        vertical space per panel over putting the same text inside.
        """
        p = node["panel"] or {}
        style_name = p.get("border", "single")
        focused = bool(p.get("focus"))
        role = p.get("border_role") or ("border-focus" if focused else "border")
        bst = self.th.style(role, default="border")

        if p.get("fill"):
            self.cv.fill(region.x, region.y, region.w, region.h,
                         bg=self.th.style(p["fill"])["bg"])

        inner = Region(region.x, region.y, region.w, region.h)
        if style_name != "none":
            if region.w < 2 or region.h < 2:
                self.cv.note("panel-too-small", where=p.get("title", ""),
                             w=region.w, h=region.h)
                return
            tl, tr, bl, br, hz, vt = BORDERS.get(style_name, BORDERS["single"])
            x0, y0 = region.x, region.y
            x1, y1 = region.x + region.w - 1, region.y + region.h - 1
            self.cv.hline(x0 + 1, y0, region.w - 2, hz, **bst)
            self.cv.hline(x0 + 1, y1, region.w - 2, hz, **bst)
            self.cv.vline(x0, y0 + 1, region.h - 2, vt, **bst)
            self.cv.vline(x1, y0 + 1, region.h - 2, vt, **bst)
            for px, py, ch in ((x0, y0, tl), (x1, y0, tr), (x0, y1, bl), (x1, y1, br)):
                self.cv.put(px, py, ch, **bst)
            self._shelf(region, p, focused, role)
            inner = Region(x0 + 1, y0 + 1, region.w - 2, region.h - 2)

        pad = int(p.get("pad", 1))
        if pad:
            inner = Region(inner.x + pad, inner.y + pad,
                           max(0, inner.w - 2 * pad), max(0, inner.h - 2 * pad))

        if focused:
            self.focus_signals.append({
                "where": p.get("title") or p.get("id") or "panel",
                "channels": sorted(set(
                    (["border-colour"] if role != "border" else [])
                    + (["title-colour"] if p.get("title") else [])
                    # Only claimable when there is a title to carry it, which
                    # is where `_shelf` draws it.
                    + (["marker"] if (p.get("focus_marker") and p.get("title"))
                       else [])
                )),
            })

        if p.get("child"):
            self.paint(inner, p["child"])

    def _shelf(self, region: Region, p: dict, focused: bool, border_role: str):
        """Write the metadata slots into the border rules.

        Each slot is padded with a space either side so it reads as sitting in a
        gap in the rule rather than colliding with it. The slots are laid out
        left, then right, then centre in the remaining middle, and a slot that
        does not fit is dropped and recorded -- overlapping shelf text is worse
        than a missing version number.
        """
        top_y, bot_y = region.y, region.y + region.h - 1
        avail = region.w - 2
        if avail <= 2:
            return
        title = p.get("title")
        if title and p.get("focus_marker") and focused:
            title = f"{p['focus_marker']} {title}"
        slots = [
            ("left", top_y, title, p.get("title_role")
             or ("border-focus" if focused else "text-strong")),
            ("right", top_y, p.get("shelf_right"), p.get("shelf_role") or "text-dim"),
            ("centre", top_y, p.get("shelf_centre"), p.get("shelf_role") or "text-dim"),
            ("left", bot_y, p.get("shelf_bottom_left"), p.get("shelf_role") or "text-dim"),
            ("right", bot_y, p.get("shelf_bottom_right"), p.get("shelf_role") or "text-dim"),
        ]
        used = {top_y: [], bot_y: []}
        for where, y, text, role in slots:
            if not text:
                continue
            label = f" {text} "
            w = string_width(label)
            if w > avail:
                self.cv.note("shelf-too-wide", row=y, where=where, text=text,
                             wanted=w, had=avail)
                continue
            if where == "left":
                x = region.x + 1
            elif where == "right":
                x = region.x + region.w - 1 - w
            else:
                x = region.x + 1 + (avail - w) // 2
            if any(not (x + w <= a or x >= b) for a, b in used[y]):
                self.cv.note("shelf-collision", row=y, where=where, text=text)
                continue
            used[y].append((x, x + w))
            self.cv.put(x, y, label, limit=w, where=f"shelf:{where}",
                        **self.th.style(role))

    # -- text --------------------------------------------------------------

    def _w_text(self, region: Region, node: dict):
        t = node["text"] or {}
        lines = t.get("lines") or ([t["line"]] if t.get("line") else [])
        st = self.th.style(t.get("role"))
        align = t.get("align", "left")
        if t.get("wrap"):
            lines = [w for ln in lines for w in wrap(ln, region.w)]
        for i, ln in enumerate(lines):
            if i >= region.h:
                self.cv.note("text-overflow-rows", where=t.get("id", "text"),
                             wanted=len(lines), had=region.h)
                break
            x = region.x + offset(ln, region.w, align)
            self.cv.put(x, region.y + i, ln, limit=region.w - (x - region.x),
                        where="text", **st)

    # -- pairs -------------------------------------------------------------

    def _w_pairs(self, region: Region, node: dict):
        """Label/value rows on two rails.

        The value rail is computed from the widest label rather than declared, so
        the values line up by construction. Labels are dim and values are the
        emphasis: the corpus does it that way round consistently, because the
        label is the part the reader already knows.
        """
        p = node["pairs"] or {}
        items = p.get("items") or []
        lst = self.th.style(p.get("label_role", "text-dim"))
        vst = self.th.style(p.get("value_role", "text-strong"))
        gap = int(p.get("gap", 2))
        widest = max((string_width(str(k)) for k, _ in items), default=0)
        rail = int(p.get("value_rail") or (widest + gap))
        if rail + 1 > region.w:
            self.cv.note("pairs-rail-overflow", where=p.get("id", "pairs"),
                         wanted=rail, had=region.w)
        for i, (k, v) in enumerate(items):
            if i >= region.h:
                self.cv.note("pairs-overflow-rows", wanted=len(items), had=region.h)
                break
            y = region.y + i
            self.cv.put(region.x, y, str(k), limit=rail, where="pairs:label", **lst)
            self.cv.put(region.x + rail, y, str(v),
                        limit=region.w - rail, where="pairs:value", **vst)

    # -- table -------------------------------------------------------------

    def _w_table(self, region: Region, node: dict):
        """A column table whose widths are solved, not declared.

        Columns may be fixed (`w`) or flexible (`flex`); flexible ones take a
        share of what is left. Every column is left-aligned unless it holds
        numbers, because a ragged right edge on text costs less than a ragged
        left edge, and the corpus is consistent about it.
        """
        t = node["table"] or {}
        cols = t.get("columns") or []
        rows = t.get("rows") or []
        if not cols:
            return
        gap = int(t.get("gap", 2))
        show_header = t.get("header", True)
        rule = t.get("header_rule", True)
        marker = str(t.get("selected_marker") or "")
        gutter = (string_width(marker) + 1) if marker else 0

        avail = region.w - gap * (len(cols) - 1) - gutter
        widths: list[int | None] = [c.get("w") for c in cols]
        natural = []
        for i, c in enumerate(cols):
            body = max((string_width(str(r[i])) for r in rows
                        if i < len(r)), default=0)
            natural.append(max(body, string_width(str(c.get("name", "")))))
        fixed = sum(w for w in widths if w)
        flexi = [i for i, w in enumerate(widths) if not w]
        free = avail - fixed
        if flexi:
            wsum = sum(float(cols[i].get("flex", 1)) for i in flexi)
            for i in flexi:
                widths[i] = max(1, int(free * float(cols[i].get("flex", 1)) / wsum))
            widths[flexi[-1]] += free - sum(widths[i] for i in flexi)
        for i, (w, n) in enumerate(zip(widths, natural)):
            if n > (w or 0):
                self.cv.note("column-too-narrow", column=cols[i].get("name", i),
                             wanted=n, had=w)

        xs, cur = [], region.x + gutter
        for w in widths:
            xs.append(cur)
            cur += (w or 0) + gap

        y = region.y
        if show_header:
            hst = self.th.style(t.get("header_role", "text-strong"))
            for c, x, w in zip(cols, xs, widths):
                name = str(c.get("name", ""))
                self.cv.put(x + offset(name, w or 0, c.get("align", "left")), y,
                            name, limit=w or 0, where="table:header", **hst)
            y += 1
            if rule:
                self.cv.hline(region.x, y, region.w, "─",
                              **self.th.style(t.get("rule_role", "border")))
                y += 1

        sel = t.get("selected")
        for ri, row in enumerate(rows):
            if y >= region.y + region.h:
                self.cv.note("table-overflow-rows", wanted=len(rows),
                             had=region.y + region.h - region.y)
                break
            is_sel = (sel is not None and ri == sel)
            if is_sel:
                sst = self.th.style(t.get("selected_role", "selected"))
                self.cv.fill(region.x, y, region.w, 1, bg=sst["bg"])
            for ci, (x, w) in enumerate(zip(xs, widths)):
                if ci >= len(row):
                    continue
                val = str(row[ci])
                # A selected row overrides its cells' semantic colour. Keeping
                # both makes the row unreadable and makes the category colour
                # mean two things; the corpus resolves it this way too.
                st = (self.th.style(t.get("selected_role", "selected")) if is_sel
                      else self.th.style(cols[ci].get("role")))
                self.cv.put(x + offset(val, w or 0, cols[ci].get("align", "left")),
                            y, val, limit=w or 0, where="table:cell", **st)
            if is_sel and marker:
                self.cv.put(region.x, y, marker, limit=gutter,
                            where="table:marker",
                            **self.th.style(t.get("marker_role", "accent")))
            y += 1

    # -- list --------------------------------------------------------------

    def _w_list(self, region: Region, node: dict):
        l = node["list"] or {}
        items = l.get("items") or []
        sel = l.get("selected")
        marker = l.get("marker", "▸")
        mw = string_width(marker) + 1
        for i, it in enumerate(items):
            if i >= region.h:
                self.cv.note("list-overflow-rows", wanted=len(items), had=region.h)
                break
            y = region.y + i
            is_sel = (sel is not None and i == sel)
            st = self.th.style(l.get("selected_role", "accent") if is_sel
                               else l.get("role"))
            if is_sel and l.get("fill"):
                self.cv.fill(region.x, y, region.w, 1,
                             bg=self.th.style(l.get("selected_role", "selected"))["bg"])
                st = self.th.style(l.get("selected_role", "selected"))
            if is_sel:
                self.cv.put(region.x, y, marker, limit=mw, where="list:marker", **st)
            self.cv.put(region.x + mw, y, str(it), limit=region.w - mw,
                        where="list:item", **st)

    # -- chips -------------------------------------------------------------

    def _w_chips(self, region: Region, node: dict):
        """Stat chips: a label and a value sharing one filled or bordered box.

        The label is dim inside the fill and the value is not, which is what
        makes a row of chips scannable -- the eye lands on four numbers, not on
        four words followed by four numbers.
        """
        c = node["chips"] or {}
        items = c.get("items") or []
        gap = int(c.get("gap", 2))
        style = c.get("style", "fill")
        x = region.x
        for it in items:
            label, value = str(it.get("label", "")), str(it.get("value", ""))
            role = it.get("role", "accent")
            body = f" {label}: {value} " if label else f" {value} "
            w = string_width(body) + (2 if style == "border" else 0)
            if x + w > region.x + region.w:
                self.cv.note("chips-overflow", where=label, wanted=w,
                             had=region.x + region.w - x)
                break
            if style == "border":
                bst = self.th.style(role)
                inner = w - 2
                self.cv.put(x, region.y, "╭" + "─" * inner + "╮",
                            limit=w, where="chip:top", **bst)
                self.cv.put(x, region.y + 1, "│", limit=1, **bst)
                self.cv.put(x + 1, region.y + 1, body, limit=inner,
                            where="chip:body", **self.th.style("text"))
                self.cv.put(x + w - 1, region.y + 1, "│", limit=1, **bst)
                self.cv.put(x, region.y + 2, "╰" + "─" * inner + "╯",
                            limit=w, where="chip:bot", **bst)
            else:
                st = self.th.style(role)
                fill = st.get("fg") if st.get("fg") != "default" else "#6FC3E8"
                ink = self.th.style("surface").get("bg", "#111318")
                self.cv.fill(x, region.y, w, 1, bg=fill)
                cx = x + 1
                if label:
                    cx += self.cv.put(cx, region.y, label + ": ", bg=fill, fg=ink,
                                      limit=w - 2, where="chip:label")
                self.cv.put(cx, region.y, value, bg=fill, fg=ink, bold=True,
                            limit=x + w - 1 - cx, where="chip:value")
            x += w + gap

    # -- keybar ------------------------------------------------------------

    def _w_keybar(self, region: Region, node: dict):
        """The footer, as a live surface rather than a static legend.

        Three styles, all observed: a keycap chip beside the label, the key in
        brackets inside the label, and plain. The key is always visually distinct
        from the word it operates, because a footer where both are the same
        colour reads as prose.
        """
        k = node["keybar"] or {}
        items = k.get("items") or []
        style = k.get("style", "chip")
        sep = k.get("sep", "  ")
        kst = self.th.style(k.get("key_role", "accent"))
        lst = self.th.style(k.get("label_role", "text-dim"))
        sst = self.th.style("text-dim")
        if k.get("fill"):
            self.cv.fill(region.x, region.y, region.w, 1,
                         bg=self.th.style(k["fill"])["bg"])
        x = region.x
        for i, it in enumerate(items):
            key, label = (str(it[0]), str(it[1])) if isinstance(it, (list, tuple)) \
                else (str(it.get("key", "")), str(it.get("label", "")))
            if style == "bracket":
                piece = [(f"[{key}]", kst), (" " + label, lst)]
                text_w = string_width(f"[{key}]") + 1 + string_width(label)
            else:
                piece = [(key, kst), (" " + label, lst)]
                text_w = string_width(key) + 1 + string_width(label)
            sep_w = string_width(sep) if i else 0
            if x + sep_w + text_w > region.x + region.w:
                self.cv.note("keybar-overflow", where=label,
                             shown=i, of=len(items))
                break
            if i:
                x += self.cv.put(x, region.y, sep, limit=sep_w, **sst)
            for s, st in piece:
                x += self.cv.put(x, region.y, s,
                                 limit=region.x + region.w - x,
                                 where="keybar", **st)

    # -- gauge -------------------------------------------------------------

    def _w_gauge(self, region: Region, node: dict):
        """A labelled bar. The number is written as text as well as drawn.

        A bar alone encodes its value in length only, which a screen reader
        cannot linearise and a reader cannot read off precisely. The corpus's
        good meters carry both.
        """
        g = node["gauge"] or {}
        label = str(g.get("label", ""))
        value = float(g.get("value", 0))
        vmax = float(g.get("max", 100)) or 100.0
        frac = max(0.0, min(1.0, value / vmax))
        readout = g.get("readout", f"{value:g}/{vmax:g}")
        role = g.get("role", "accent")
        lw = string_width(label) + (1 if label else 0)
        rw = string_width(readout) + 1
        bar_w = region.w - lw - rw
        if bar_w < 3:
            self.cv.note("gauge-too-narrow", where=label, had=region.w,
                         wanted=lw + rw + 3)
            bar_w = max(0, bar_w)
        x = region.x
        if label:
            x += self.cv.put(x, region.y, label + " ", limit=lw,
                             where="gauge:label", **self.th.style("text-dim"))
        filled = int(round(bar_w * frac))
        self.cv.put(x, region.y, g.get("glyph", "█") * filled,
                    limit=bar_w, where="gauge:bar", **self.th.style(role))
        self.cv.put(x + filled, region.y, g.get("track", "░") * (bar_w - filled),
                    limit=bar_w - filled, where="gauge:track",
                    **self.th.style("border"))
        self.cv.put(x + bar_w + 1, region.y, readout, limit=rw,
                    where="gauge:readout", **self.th.style("text"))


def offset(s: str, width: int, align: str) -> int:
    w = string_width(s)
    if align == "right":
        return max(0, width - w)
    if align in ("centre", "center"):
        return max(0, (width - w) // 2)
    return 0


def wrap(s: str, width: int) -> list[str]:
    """Wrap on spaces, measured in cells.

    Wrapping on `len()` is the same bug as everything else here, one layer up: a
    line of CJK wrapped at 60 characters is 120 cells wide and runs off the edge.
    """
    if width <= 0:
        return [s]
    out, line, lw = [], [], 0
    for word in s.split(" "):
        ww = string_width(word)
        if line and lw + 1 + ww > width:
            out.append(" ".join(line))
            line, lw = [word], ww
        else:
            lw += (1 if line else 0) + ww
            line.append(word)
    if line:
        out.append(" ".join(line))
    return out or [""]


# --------------------------------------------------------------------------
# Compile
# --------------------------------------------------------------------------


def compile_spec(spec: dict) -> dict:
    size = spec.get("size") or {}
    cols, rows = int(size.get("cols", 80)), int(size.get("rows", 24))
    cv = Canvas(cols, rows)
    th = Theme(spec)
    ground = th.style("surface").get("bg", "default")
    if ground != "default":
        cv.fill(0, 0, cols, rows, bg=ground)
    p = Painter(cv, th)
    root = spec.get("root") or {}
    p.paint(Region(0, 0, cols, rows), root)

    if th.unknown:
        cv.note("unknown-role", roles=sorted(th.unknown))

    return {
        "schema": SCHEMA_VERSION,
        "kind": "mock",
        "cols": cols,
        "rows": rows,
        "cursor": [0, 0],
        "title": spec.get("title"),
        "alt_screen": bool(spec.get("alt_screen", True)),
        "provenance": {
            "method": "spec-compile",
            "spec_schema": spec.get("schema", SPEC_VERSION),
            "compiler": "tui_mock.py",
            "size": f"{cols}x{rows}",
            "theme": th.name,
            "term": "n/a - compiled from a spec, never hosted",
            "note": ("A mock. It shows what a layout would occupy at this size; "
                     "it is not evidence about a running program."),
        },
        "fit": cv.fit,
        "focus_signals": p.focus_signals,
        "regions": p.regions,
        "roles": th.roles,
        "cells": [[asdict(c) for c in row] for row in cv.cells],
    }



def zwj_risks(frame: dict) -> list[dict]:
    """Cells whose width depends on the terminal rather than on the arithmetic.

    A ZWJ sequence collapses to one double-width glyph in a terminal that
    composes it and renders as its separate parts in one that does not. Both are
    correct, they differ by four cells on a family emoji, and no width function
    can tell you which the reader will get. A layout that fits under only one of
    the two answers is a layout that breaks for somebody, so this is reported
    rather than resolved.
    """
    out = []
    for y, row in enumerate(frame["cells"]):
        for x, c in enumerate(row):
            ch = c.get("ch") or ""
            if "\u200d" not in ch:
                continue
            parts = ch.split("\u200d")
            out.append({"kind": "zwj-width-ambiguous", "row": y, "col": x,
                        "text": ch[:24],
                        "uncomposed_cells": string_width(ch),
                        "composed_cells": max(string_width(p) for p in parts),
                        "note": ("Reserve the uncomposed width, or use a glyph "
                                 "with a single code point.")})
    return out

def dump(frame: dict, rulers: bool = True) -> str:
    """Character matrix with column rulers, which is the artifact to read.

    Misalignment that a rendered image hides is obvious against a ruler, and a
    ruler dump diffs cleanly between two versions of a screen.
    """
    cols, rows = frame["cols"], frame["rows"]
    out = []
    if rulers:
        tens = "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(cols))
        ones = "".join(str(x % 10) for x in range(cols))
        out.append("    " + tens)
        out.append("    " + ones)
    for y in range(rows):
        line = "".join(c["ch"] if c["w"] != 0 else "" for c in frame["cells"][y])
        out.append(f"{y:3d} {line}")
    return "\n".join(out)


def to_ansi(frame: dict) -> str:
    """Paint the frame into this terminal, truecolour."""
    def rgb(hexs, fg=True):
        if not hexs or hexs == "default":
            return "\x1b[39m" if fg else "\x1b[49m"
        h = hexs.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"\x1b[{38 if fg else 48};2;{r};{g};{b}m"

    lines = []
    for row in frame["cells"]:
        buf = []
        for c in row:
            if c["w"] == 0:
                continue
            buf.append(rgb(c["fg"], True) + rgb(c["bg"], False)
                       + ("\x1b[1m" if c["bold"] else "")
                       + ("\x1b[2m" if c["dim"] else "")
                       + ("\x1b[7m" if c["reverse"] else "")
                       + (c["ch"] or " ") + "\x1b[0m")
        lines.append("".join(buf))
    return "\n".join(lines)


def load_spec(path: str) -> dict:
    text = Path(path).read_text()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            print("This spec is YAML and pyyaml is not installed. Either "
                  "`pip install pyyaml` or write the spec as JSON -- the schema "
                  "is identical.", file=sys.stderr)
            sys.exit(2)
        return yaml.safe_load(text)
    return json.loads(text)


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

GOLDEN_WIDTHS = [
    ("ascii", "Deploy", 6),
    ("emoji", "\U0001F680 Deploy", 9),          # len() says 8
    ("cjk", "設定", 4),                 # len() says 2
    ("combining", "éx", 2),               # len() says 3
    # A three-person ZWJ family is 6 cells to a terminal that does not compose
    # the sequence and 2 to one that does. 6 is what this arithmetic returns
    # and what a pessimistic layout must reserve; the divergence is real and
    # unresolvable from here, which is why `zwj_risks()` reports it instead of
    # the compiler picking a side. The first draft of this table asserted 4,
    # which is neither answer.
    ("zwj-family-uncomposed", "\U0001F468‍\U0001F469‍\U0001F467", 6),
    ("box", "┌──┐", 4),
    ("nerd-pua", "", 1),
]


def self_test(verbose: bool = True) -> bool:
    """Golden cases for the arithmetic every column depends on.

    These run against tui-craft's `string_width`, imported above. They are not a
    second opinion about it -- they are the check that the shared function still
    does what this compiler assumes, so a change on the capture side that would
    silently move every column here fails loudly instead.
    """
    ok = True
    for name, s, want in GOLDEN_WIDTHS:
        got = string_width(s)
        if got != want:
            ok = False
            if verbose:
                print(f"FAIL width {name}: want {want} got {got} (len={len(s)})")
        elif verbose:
            note = " <- len() disagrees" if len(s) != want else ""
            print(f"  ok width {name}: {want}{note}")

    # Truncation must always leave a marker, and never exceed the budget.
    for s, w in (("abcdefghij", 5), ("設定設定", 5), ("ab", 5)):
        t, cut = truncate(s, w)
        if string_width(t) > w:
            ok = False
            if verbose:
                print(f"FAIL truncate overflowed: {s!r} at {w} -> {t!r}")
        if cut and "…" not in t:
            ok = False
            if verbose:
                print(f"FAIL truncate lost its marker: {s!r} at {w} -> {t!r}")

    # A split must return children summing exactly to the parent.
    cv = Canvas(80, 24)
    for spec, total in ((({"dir": "row", "children": [{"flex": 2}, {"flex": 1}]}), 80),
                        (({"dir": "row", "children": [{"w": 30}, {"flex": 1}]}), 80),
                        (({"dir": "row", "gap": 1,
                           "children": [{"flex": 1}, {"flex": 1}, {"flex": 1}]}), 78)):
        got = sum(r.w for r, _ in split(Region(0, 0, 80, 24), spec, cv))
        if got != total:
            ok = False
            if verbose:
                print(f"FAIL split sums to {got}, want {total}: {spec}")
        elif verbose:
            print(f"  ok split sums to {total}")

    if verbose:
        print("self-test: PASS" if ok else "self-test: FAIL")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="spec file (.json, or .yaml with pyyaml)")
    ap.add_argument("-o", "--out")
    ap.add_argument("--dump", action="store_true", help="ruler dump")
    ap.add_argument("--ansi", action="store_true", help="paint into this terminal")
    ap.add_argument("--fit", action="store_true", help="fit report only")
    ap.add_argument("--gate", action="store_true",
                    help="compile, then run both gate suites on the result and "
                         "combine the exit codes")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1
    if not args.spec:
        ap.error("a spec is required unless --self-test")

    if not self_test(verbose=False):
        print("Refusing to compile: the width arithmetic failed its own golden "
              "cases, so every column in the output would be suspect.",
              file=sys.stderr)
        return 2

    frame = compile_spec(load_spec(args.spec))

    if args.out:
        Path(args.out).write_text(json.dumps(frame, ensure_ascii=False, indent=1))
    if args.ansi:
        print(to_ansi(frame))
    if args.dump or (not args.out and not args.ansi and not args.fit):
        print(dump(frame))
    if args.fit or frame["fit"]:
        print(f"\nfit findings: {len(frame['fit'])}", file=sys.stderr)
        for f in frame["fit"]:
            print("  " + json.dumps(f, ensure_ascii=False), file=sys.stderr)

    rc = 1 if frame["fit"] else 0
    if args.gate:
        rc = max(rc, _run_gates(frame))
    return rc


def _run_gates(frame: dict) -> int:
    """Run the design gates and tui-craft's arithmetic gates on one compiled frame.

    Here so the loop is one command. Documented as three commands in sequence,
    it was three chances to skip the arithmetic pass, and the middle one carried
    a `../tui-craft/scripts/` path that resolves only from this skill's own
    directory. Paths are derived from this file's location instead.
    """
    import subprocess  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    here = Path(__file__).resolve().parent
    suites = [
        ("design", here / "tui_design_gates.py"),
        ("arithmetic", here.parent.parent / "tui-craft" / "scripts" / "tui_gates.py"),
    ]
    worst = 0
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        fh.write(json.dumps(frame, ensure_ascii=False))
        path = fh.name
    try:
        for label, script in suites:
            if not script.exists():
                print(f"\n{label} gates: NOT RUN — {script} is missing. That is not a "
                      f"pass; say so in the report.", file=sys.stderr)
                worst = max(worst, 2)
                continue
            print(f"\n=== {label} gates ===", file=sys.stderr)
            proc = subprocess.run([sys.executable, str(script), path, "--strict"],
                                  check=False)
            worst = max(worst, proc.returncode)
    finally:
        Path(path).unlink(missing_ok=True)
    return worst


if __name__ == "__main__":
    sys.exit(main())
