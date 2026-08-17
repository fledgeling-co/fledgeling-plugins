#!/usr/bin/env python3
"""Design-quality gates over a cell frame.

tui-craft's gates decide arithmetic: does the border close, did a wide glyph push
a column off the edge, was text cut without saying so. They deliberately stop
short of asking whether the screen is any good, and its own EVALS name that as
the unmeasured gap. These gates take a few bites out of it -- the parts of "is
this well designed" that turn out to be countable.

Two kinds of check, and the difference matters more than any individual rule:

  ENFORCED  An imposed principle. It can fail a frame. Each one is a rule about
            how information has to be carried, not a number lifted off a corpus.

  REPORTED  A measurement with no pass mark. Printed with its denominator so a
            reader can see the shape of the screen, and never used to fail.

Nothing measured from the reference corpus is a fail threshold, and that is a
deliberate correction rather than caution. The 48-app corpus is what people
shipped, not a contrast authority: 27 of its 34 colour-measurable frames carry
at least one glyph role under 3:1. Its median of 5.5 chromatic roles and 0.86
rail concentration describe a habit; turning a habit into a gate would fail good
screens for being unusual and pass bad ones for being typical. So the numbers are
context in the output, and the pass marks come from principles.

Usage
-----
    tui_design_gates.py frame.json            # human-readable
    tui_design_gates.py frame.json --json
    tui_design_gates.py frame.json --strict   # exit 1 on any enforced failure
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

BOX = set("│┃║▌▐┆┇┊┋╎╏─━═▁▔┄┅┈┉╌╍┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬╭╮╯╰")

# The reference corpus, for context in the output only. Measured over 47 frames
# extracted from 48 shipped apps; the colour figures over the 34 that were not
# GIF-palette-dithered. Never a threshold -- see the module docstring.
CORPUS = {
    "chromaticRoles": {"n": 34, "p25": 3, "median": 5.5, "p75": 7, "max": 16},
    "railTop3Cover": {"n": 38, "min": 0.20, "p25": 0.75, "median": 0.86, "max": 1.00},
    "subThreeToOne": {"frames": 27, "of": 34},
    "darkGround": {"frames": 33, "of": 34},
}


# --------------------------------------------------------------------------
# Colour
# --------------------------------------------------------------------------


def parse_hex(c: str):
    if not isinstance(c, str) or not c.startswith("#") or len(c) != 7:
        return None
    try:
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        return None


def luminance(rgb) -> float:
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def saturation(rgb) -> float:
    mx, mn = max(rgb), min(rgb)
    return 0.0 if mx == 0 else (mx - mn) / mx


# --------------------------------------------------------------------------
# Frame helpers
# --------------------------------------------------------------------------


class F:
    def __init__(self, d: dict):
        self.d = d
        self.cols, self.rows = d["cols"], d["rows"]
        self.cells = d["cells"]
        self.kind = d.get("kind", "captured")
        self.regions = d.get("regions") or []
        self.roles = d.get("roles") or {}
        self.focus_signals = d.get("focus_signals") or []

    def cell(self, x, y):
        return self.cells[y][x]

    def ground(self) -> str:
        bgs = Counter(c["bg"] for row in self.cells for c in row)
        return bgs.most_common(1)[0][0]

    def region_cells(self, r):
        for y in range(r["y"], min(self.rows, r["y"] + r["h"])):
            for x in range(r["x"], min(self.cols, r["x"] + r["w"])):
                yield x, y, self.cells[y][x]


def finding(gate, level, msg, **kw):
    return {"gate": gate, "level": level, "message": msg, **kw}


# --------------------------------------------------------------------------
# ENFORCED: the role ladder
# --------------------------------------------------------------------------


def gate_role_ladder(f: F) -> tuple[list, dict]:
    """Text roles must be ordered by contrast, and the ones carrying primary
    information must clear a floor.

    Flat WCAG on every glyph is the wrong instrument for a terminal. Quiet
    secondary ink is a real and deliberate device -- a dim timestamp beside a
    bright message is doing hierarchy work that a terminal has almost no other
    way to do, because there is one font at one size. Failing it at 4.5:1 would
    delete the only subtle channel the medium has.

    What can be insisted on instead is that the ladder is a ladder. Every role
    that carries information sits above 3:1 so it is not decoration, the roles
    the reader must be able to read sit above 4.5:1, and no role that is supposed
    to be quieter than another is in fact brighter. That last one is the check
    that catches a palette assembled a token at a time, where `text-dim` ends up
    with more contrast than `text` and the hierarchy silently inverts.
    """
    out = []
    ground = f.ground()
    grgb = parse_hex(ground)

    # Which roles actually appear, and on which backgrounds.
    used: dict[str, Counter] = {}
    role_of: dict[str, str] = {}
    for name, spec in f.roles.items():
        if spec.get("fg"):
            role_of[spec["fg"]] = name
    for row in f.cells:
        for c in row:
            fg, bg = c["fg"], c["bg"]
            if not parse_hex(fg) or (c["ch"] or " ").strip() == "":
                continue
            used.setdefault(fg, Counter())[bg] += 1

    if not used or not grgb:
        return out, {"examined": 0,
                     "note": ("No hex colours in this frame, so the ladder is "
                              "unmeasurable here. A captured frame carries ANSI "
                              "names or 'default', which resolve only in the "
                              "reader's own palette -- that is a real property "
                              "of the medium, not a gap in this gate. Compile a "
                              "spec, or query the terminal, to check a ladder.")}

    # 'Information' floors, imposed. A role naming itself dim/muted/subtle is
    # allowed the lower one; everything else must be readable.
    QUIET = ("dim", "muted", "subtle", "faint", "ghost", "border", "rule", "track")
    measured = []
    for fg, bgs in sorted(used.items(), key=lambda kv: -sum(kv[1].values())):
        name = role_of.get(fg, fg)
        quiet = any(q in name.lower() for q in QUIET)
        for bg, n in bgs.items():
            brgb = parse_hex(bg) or grgb
            cr = contrast(parse_hex(fg), brgb)
            floor = 3.0 if quiet else 4.5
            measured.append({"role": name, "fg": fg, "bg": bg, "cells": n,
                             "contrast": round(cr, 2), "floor": floor,
                             "quiet": quiet})
            if cr < floor:
                out.append(finding(
                    "role-ladder", "high",
                    f"role {name} reads at {cr:.2f}:1 on {bg}, below its {floor}:1 floor",
                    role=name, fg=fg, bg=bg, contrast=round(cr, 2), floor=floor,
                    cells=n))

    # Ordering: a role named as quieter must not out-contrast the one it is
    # quieter than. Checked on the ground only, where the comparison is defined.
    ladder = [("text-dim", "text"), ("text", "text-strong"), ("border", "text-dim")]
    for lo, hi in ladder:
        a, b = f.roles.get(lo, {}).get("fg"), f.roles.get(hi, {}).get("fg")
        ra, rb = parse_hex(a or ""), parse_hex(b or "")
        if not ra or not rb:
            continue
        ca, cb = contrast(ra, grgb), contrast(rb, grgb)
        if ca > cb:
            out.append(finding(
                "role-ladder", "high",
                f"{lo} ({ca:.2f}:1) out-contrasts {hi} ({cb:.2f}:1) — the "
                f"hierarchy is inverted, so emphasis reads as recession",
                lower=lo, higher=hi))

    return out, {"examined": len(measured), "ground": ground, "roles": measured}


# --------------------------------------------------------------------------
# ENFORCED: every state needs a carrier that survives colour loss
# --------------------------------------------------------------------------


def distinguished_rows(f: F, r: dict) -> list[int]:
    """Rows inside a region styled differently from their siblings.

    This is how selection shows up in a frame without being told about it: one
    row carries a background, or reverse video, that the rows around it do not.
    Works the same on a captured frame as on a compiled one, which is the point.
    """
    sig = {}
    for y in range(r["y"], min(f.rows, r["y"] + r["h"])):
        row = [f.cells[y][x] for x in range(r["x"], min(f.cols, r["x"] + r["w"]))]
        glyphs = [c["ch"] for c in row if (c["ch"] or " ").strip()]
        if not glyphs:
            continue
        if all(g in BOX for g in glyphs):
            continue    # a rule, not a state
        bgs = Counter(c["bg"] for c in row)
        sig[y] = (bgs.most_common(1)[0][0], any(c["reverse"] for c in row))
    if len(sig) < 2:
        return []
    common = Counter(sig.values()).most_common(1)[0][0]
    return [y for y, s in sig.items() if s != common]


def gate_state_carrier(f: F) -> tuple[list, dict]:
    """A distinguished row must stay distinguished when colour is removed.

    Colour is the cheapest way to mark a selected row and the least reliable one
    available. It is gone under `NO_COLOR`, gone when the output is piped, gone
    for a reader with a palette that maps the chosen index somewhere unhelpful,
    and gone for anyone who cannot separate those two hues. A terminal has no
    hover, no shadow and no focus ring, so the fallbacks are few and have to be
    used on purpose: a marker glyph in the gutter, reverse video, bold, or a
    label change.

    A background fill is not one of them. Filling a row's background is a colour
    change wearing different clothes -- strip colour and it is gone. Reverse
    video survives, because it is an attribute the terminal applies rather than a
    colour the app picked, which is exactly why the corpus's careful apps reach
    for it.
    """
    out = []
    checked = 0
    regions = f.regions or [{"kind": "frame", "label": "whole frame",
                             "x": 0, "y": 0, "w": f.cols, "h": f.rows}]
    for r in regions:
        if r["kind"] not in ("table", "list", "frame"):
            continue
        rows = distinguished_rows(f, r)
        if not rows:
            continue
        for y in rows:
            checked += 1
            cells = [f.cells[y][x] for x in range(r["x"],
                                                  min(f.cols, r["x"] + r["w"]))]
            carriers = []
            if any(c["reverse"] for c in cells):
                carriers.append("reverse")
            if any(c["bold"] for c in cells):
                carriers.append("bold")
            if any(c["underline"] for c in cells):
                carriers.append("underline")
            # A marker glyph: ink in a leading column that the sibling rows leave
            # blank. That is the gutter marker the corpus uses constantly.
            first = next((i for i, c in enumerate(cells)
                          if (c["ch"] or " ").strip()), None)
            if first is not None:
                sibling_first = []
                for yy in range(r["y"], min(f.rows, r["y"] + r["h"])):
                    if yy == y:
                        continue
                    sc = [f.cells[yy][x] for x in range(r["x"],
                                                        min(f.cols, r["x"] + r["w"]))]
                    fi = next((i for i, c in enumerate(sc)
                               if (c["ch"] or " ").strip()), None)
                    if fi is not None:
                        sibling_first.append(fi)
                if sibling_first and first < min(sibling_first):
                    carriers.append("gutter-marker")
            if not carriers:
                out.append(finding(
                    "state-carrier", "high",
                    f"row {y} in {r['label']!r} is distinguished by colour alone; "
                    f"strip colour and it is an ordinary row",
                    row=y, region=r["label"],
                    fix=("add a gutter marker, reverse video, or bold — a "
                         "background fill is still colour")))
    if not checked:
        return out, {"examined": 0,
                     "note": ("No row in any table or list is styled differently "
                              "from its siblings, so there is no selection or "
                              "highlight to check. A screen with a list and no "
                              "visible cursor position is worth a look on its "
                              "own account.")}
    return out, {"examined": checked}


# --------------------------------------------------------------------------
# ENFORCED: focus is signalled more than once
# --------------------------------------------------------------------------


def gate_focus_channels(f: F) -> tuple[list, dict]:
    """Focus needs two channels, because a terminal gives you no third chance.

    On the web a focused control has a ring, a shadow, a cursor change and a
    hover state that preceded it. In a terminal there is the border, the title,
    the footer, and a marker. Every app in the reference corpus that reads
    clearly signals focus at least twice; the ones that signal once are the ones
    where you cannot tell which pane is live.
    """
    out = []
    signals = f.focus_signals
    if not signals:
        return out, {"examined": 0,
                     "note": ("Nothing in this frame declares itself focused. On "
                              "a compiled spec, set `focus` on the active panel. "
                              "On a captured frame, focus is not recoverable from "
                              "cells alone -- capture the same screen with focus "
                              "moved and compare.")}
    for s in signals:
        ch = s.get("channels") or []
        if len(ch) < 2:
            out.append(finding(
                "focus-channels", "high",
                f"{s['where']!r} signals focus on {len(ch)} channel"
                f"{'' if len(ch) == 1 else 's'} ({', '.join(ch) or 'none'})",
                where=s["where"], channels=ch,
                fix=("add a second: brighten the title as well as the border, "
                     "change the footer to that pane's keys, or put a marker on "
                     "the active row")))
    return out, {"examined": len(signals)}


# --------------------------------------------------------------------------
# REPORTED: measurements with no pass mark
# --------------------------------------------------------------------------


def report_role_budget(f: F) -> dict:
    fgs = Counter()
    for row in f.cells:
        for c in row:
            if (c["ch"] or " ").strip():
                fgs[c["fg"]] += 1
    chromatic, neutral = [], []
    for fg, n in fgs.items():
        rgb = parse_hex(fg)
        if rgb is None:
            neutral.append((fg, n))
        elif saturation(rgb) > 0.22:
            chromatic.append((fg, n))
        else:
            neutral.append((fg, n))
    return {"foregrounds": len(fgs), "chromatic": len(chromatic),
            "neutral": len(neutral),
            "top": [{"fg": k, "cells": v} for k, v in fgs.most_common(8)],
            "corpus": CORPUS["chromaticRoles"],
            "note": ("Corpus context only. Both ends of that range are apps "
                     "people like; the number is a description of this screen, "
                     "not a score for it.")}


def report_rails(f: F) -> dict:
    """Left-alignment discipline, measured per container.

    Screen-global rails are close to meaningless on a multi-pane layout: each
    pane has its own left edge, and pooling them reports a two-pane screen as
    undisciplined for being two panes. So this measures inside each region and
    reports them separately.
    """
    out = []
    regions = [r for r in f.regions
               if r["kind"] in ("table", "list", "pairs", "text")] or \
              [{"kind": "frame", "label": "whole frame", "x": 0, "y": 0,
                "w": f.cols, "h": f.rows}]
    for r in regions:
        starts = []
        for y in range(r["y"], min(f.rows, r["y"] + r["h"])):
            xs = [x for x in range(r["x"], min(f.cols, r["x"] + r["w"]))
                  if (f.cells[y][x]["ch"] or " ").strip()
                  and f.cells[y][x]["ch"] not in BOX]
            if xs:
                starts.append(xs[0] - r["x"])
        if len(starts) < 3:
            continue
        hist = Counter(starts)
        top3 = hist.most_common(3)
        out.append({"region": r["label"], "kind": r["kind"],
                    "contentRows": len(starts),
                    "distinctStarts": len(hist),
                    "top3Cover": round(sum(n for _, n in top3) / len(starts), 3),
                    "top3": [[x, n] for x, n in top3]})
    return {"regions": out, "corpus": CORPUS["railTop3Cover"],
            "note": ("A canvas app -- a plot, a map, a treemap -- has no rails "
                     "by design and should read low here. That is the layout "
                     "being spatial, not sloppy.")}


def report_fill(f: F) -> dict:
    """How much of each panel's interior carries ink.

    A panel eight rows of content tall stretched over twenty-eight rows is not a
    bug and no threshold catches it, but it is usually a layout that was written
    for one data volume and is being shown another. Worth seeing.
    """
    out = []
    for r in f.regions:
        if r["kind"] != "panel":
            continue
        inner = {"x": r["x"] + 1, "y": r["y"] + 1,
                 "w": max(0, r["w"] - 2), "h": max(0, r["h"] - 2)}
        total = inner["w"] * inner["h"]
        if total <= 0:
            continue
        ink = sum(1 for _, _, c in F.region_cells(f, inner)
                  if (c["ch"] or " ").strip() and c["ch"] not in BOX)
        out.append({"panel": r["label"], "interior": total,
                    "inkCells": ink, "fill": round(ink / total, 3)})
    return {"panels": out}


def report_chrome(f: F) -> dict:
    box = sum(1 for row in f.cells for c in row if c["ch"] in BOX)
    ink = sum(1 for row in f.cells for c in row
              if (c["ch"] or " ").strip())
    total = f.cols * f.rows
    return {"boxCells": box, "inkCells": ink, "cells": total,
            "chromeShareOfInk": round(box / ink, 3) if ink else 0.0,
            "inkShareOfFrame": round(ink / total, 3),
            "note": ("Border cells as a share of all ink. High is not wrong -- "
                     "the border is a shelf that carries titles and counts -- but "
                     "chrome outweighing content is worth a second look.")}


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------

ENFORCED = [
    ("role-ladder", gate_role_ladder),
    ("state-carrier", gate_state_carrier),
    ("focus-channels", gate_focus_channels),
]


def run(frame: dict) -> dict:
    f = F(frame)
    findings, coverage = [], {}
    for name, fn in ENFORCED:
        fs, cov = fn(f)
        findings.extend(fs)
        coverage[name] = cov
    return {
        "kind": f.kind,
        "size": f"{f.cols}x{f.rows}",
        "enforced": {"findings": findings,
                     "failed": sum(1 for x in findings if x["level"] == "high"),
                     "coverage": coverage},
        "reported": {"roleBudget": report_role_budget(f),
                     "rails": report_rails(f),
                     "panelFill": report_fill(f),
                     "chrome": report_chrome(f)},
    }


def render(res: dict) -> str:
    L = []
    L.append(f"frame {res['size']}  kind={res['kind']}")
    if res["kind"] == "mock":
        L.append("  a mock: these gates judge the design it proposes, never the "
                 "behaviour of a program")
    L.append("")
    L.append("ENFORCED")
    cov = res["enforced"]["coverage"]
    for name, _ in ENFORCED:
        c = cov.get(name, {})
        n = c.get("examined", 0)
        fs = [x for x in res["enforced"]["findings"] if x["gate"] == name]
        state = "not run" if n == 0 else ("pass" if not fs else f"{len(fs)} failing")
        L.append(f"  {name:<16} examined={n:<4} {state}")
        if n == 0 and c.get("note"):
            L.append(f"      {c['note']}")
        for x in fs:
            L.append(f"      [{x['level']}] {x['message']}")
            if x.get("fix"):
                L.append(f"              fix: {x['fix']}")
    L.append("")
    L.append("REPORTED (no pass mark)")
    rb = res["reported"]["roleBudget"]
    cp = rb["corpus"]
    L.append(f"  role budget      {rb['foregrounds']} foreground colours "
             f"({rb['chromatic']} chromatic, {rb['neutral']} neutral)")
    L.append(f"                   corpus n={cp['n']}: p25={cp['p25']} "
             f"median={cp['median']} p75={cp['p75']} max={cp['max']} chromatic")
    for r in res["reported"]["rails"]["regions"]:
        L.append(f"  rails            {r['region']!r} ({r['kind']}): "
                 f"{r['top3Cover']:.2f} of {r['contentRows']} content rows on "
                 f"{min(3, r['distinctStarts'])} of {r['distinctStarts']} rails")
    for p in res["reported"]["panelFill"]["panels"]:
        L.append(f"  panel fill       {p['panel']!r}: {p['fill']:.2f} "
                 f"({p['inkCells']}/{p['interior']} cells)")
    ch = res["reported"]["chrome"]
    L.append(f"  chrome           {ch['boxCells']} box cells, "
             f"{ch['chromeShareOfInk']:.2f} of all ink; "
             f"ink covers {ch['inkShareOfFrame']:.2f} of the frame")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frame")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any enforced gate has a failure")
    args = ap.parse_args()

    res = run(json.loads(Path(args.frame).read_text()))
    print(json.dumps(res, indent=1, ensure_ascii=False) if args.json else render(res))
    return 1 if (args.strict and res["enforced"]["failed"]) else 0


if __name__ == "__main__":
    sys.exit(main())
