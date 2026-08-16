#!/usr/bin/env python3
"""Mechanical gates over a captured cell frame.

These check the things a model reading a screenshot reliably gets wrong, because
they are arithmetic rather than perception: whether a border actually closes,
whether a wide character pushed a column off the edge, whether text was cut
without saying so. They do not judge hierarchy, colour choice, or whether the
screen is any good — that judgement belongs to design-craft and ux-craft, and it
runs on the ruler dump after these pass.

A gate finding is a defect in the frame, not an opinion about it. Every one
names the row and column so it can be looked at directly.

Usage
-----
    tui_gates.py frame.json                 # human-readable findings
    tui_gates.py frame.json --json          # machine-readable
    tui_gates.py frame.json --strict        # exit 1 on any high finding
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

BOX_VERTICAL = set("│┃║▌▐|┆┇┊┋╎╏")
BOX_HORIZONTAL = set("─━═▁▔┄┅┈┉╌╍")
BOX_CORNER = set("┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬╭╮╯╰")
BOX_ANY = BOX_VERTICAL | BOX_HORIZONTAL | BOX_CORNER
ELLIPSIS_MARKERS = ("…", "...", "·", "▸", "→", "»", ">")


def load(path: str) -> dict:
    data = json.loads(Path(path).read_text())
    if data.get("kind") == "capture-blocked":
        print(f"capture-blocked: {data.get('reason', data.get('provenance', {}).get('reason'))}",
              file=sys.stderr)
        sys.exit(2)
    if data.get("kind") == "mock":
        print("This frame is a mock, not a capture. Gates are advisory on a mock "
              "and it may not be used as evidence for a finding.", file=sys.stderr)
    return data


def row_cells(frame: dict, y: int) -> list[dict]:
    return frame["cells"][y]


def visible_text(frame: dict, y: int) -> str:
    return "".join(c["ch"] if c["w"] != 0 else "" for c in row_cells(frame, y))


def finding(gate: str, severity: str, row, col, message: str, evidence: str = "") -> dict:
    return {"gate": gate, "severity": severity, "row": row, "col": col,
            "message": message, "evidence": evidence}


# --------------------------------------------------------------------------


def gate_border_integrity(frame: dict) -> list[dict]:
    """A box that opens must close on the same column.

    The commonest terminal defect: a row of a bordered panel whose right edge is
    missing because something inside it measured wider than the code assumed.
    """
    out: list[dict] = []
    cols, rows = frame["cols"], frame["rows"]
    # Find columns that behave like a vertical border: box glyphs on 3+ rows.
    col_hits: dict[int, list[int]] = {}
    for y in range(rows):
        cells = row_cells(frame, y)
        for x in range(cols):
            if cells[x]["ch"] in BOX_VERTICAL or cells[x]["ch"] in BOX_CORNER:
                col_hits.setdefault(x, []).append(y)
    border_cols = {x: ys for x, ys in col_hits.items() if len(ys) >= 3}

    for x, ys in sorted(border_cols.items()):
        span = range(min(ys), max(ys) + 1)
        missing = [y for y in span if y not in ys]
        # Only report gaps inside an otherwise solid run — a panel that simply
        # ends is not a defect.
        if missing and len(missing) <= max(2, len(list(span)) // 3):
            for y in missing:
                ch = row_cells(frame, y)[x]["ch"] if x < cols else ""
                out.append(finding(
                    "border-integrity", "high", y, x,
                    f"column {x} is a panel border on rows {min(ys)}-{max(ys)} but row {y} "
                    f"has {'nothing' if not ch.strip() else repr(ch)} there — the box does not close",
                    visible_text(frame, y)[:cols]))
    return out


def gate_width_arithmetic(frame: dict) -> list[dict]:
    """Wide characters that pushed a row past its neighbours.

    A row holding CJK, emoji or box-drawing glyphs whose last non-blank cell sits
    further right than the rows around it is the signature of column maths done
    on character count instead of cell width.
    """
    out: list[dict] = []
    cols, rows = frame["cols"], frame["rows"]
    ends, has_wide = [], []
    for y in range(rows):
        cells = row_cells(frame, y)
        last = -1
        wide = False
        for x in range(cols):
            if cells[x]["ch"].strip():
                last = x
            if cells[x]["w"] == 2:
                wide = True
        ends.append(last)
        has_wide.append(wide)

    populated = [e for e in ends if e >= 0]
    if len(populated) < 3:
        return out
    populated.sort()
    median = populated[len(populated) // 2]

    for y in range(rows):
        if not has_wide[y] or ends[y] < 0:
            continue
        if ends[y] >= cols - 1 and median < cols - 1:
            out.append(finding(
                "width-arithmetic", "high", y, ends[y],
                f"row {y} contains double-width characters and runs to the last column "
                f"({ends[y]}) while most rows stop at {median} — the row was measured in "
                f"characters, not cells",
                visible_text(frame, y)))
        elif abs(ends[y] - median) > 2:
            out.append(finding(
                "width-arithmetic", "medium", y, ends[y],
                f"row {y} contains double-width characters and ends at column {ends[y]} "
                f"where most rows end at {median}",
                visible_text(frame, y)))
    return out


def gate_wrap(frame: dict) -> list[dict]:
    """Content that ran off the right edge and continued on the next row.

    In a full-screen TUI this is almost always a defect: a footer key list or a
    label that outgrew its box. The tell is a row filled to the last column
    followed by a short row that starts mid-word.
    """
    out: list[dict] = []
    cols, rows = frame["cols"], frame["rows"]
    for y in range(rows - 1):
        cells, nxt = row_cells(frame, y), row_cells(frame, y + 1)
        if not cells[cols - 1]["ch"].strip():
            continue
        if not nxt[0]["ch"].strip():
            continue
        # A wrap looks like a word split: last char and first char both word-ish.
        a, b = cells[cols - 1]["ch"], nxt[0]["ch"]
        if a.isalnum() and b.isalnum():
            out.append(finding(
                "overflow-wrap", "high", y, cols - 1,
                f"row {y} fills to the last column and row {y + 1} continues it mid-word "
                f"({a!r}|{b!r}) — content wrapped instead of fitting or being demoted",
                visible_text(frame, y)[-30:] + " ⏎ " + visible_text(frame, y + 1)[:30]))
    return out


def gate_truncation_marker(frame: dict) -> list[dict]:
    """Text cut at a boundary with nothing to say it was cut.

    A user cannot tell a truncated value from a short one. Every clipped string
    needs a marker; the corpus is full of apps that ship without one.
    """
    out: list[dict] = []
    cols, rows = frame["cols"], frame["rows"]
    for y in range(rows):
        cells = row_cells(frame, y)
        last = max((x for x in range(cols) if cells[x]["ch"].strip()), default=-1)
        if last < 0:
            continue
        text = visible_text(frame, y).rstrip()
        if not text:
            continue
        tail = text[-1]
        # Only suspicious when the row runs to (or one short of) the edge and
        # ends mid-word rather than at a natural boundary.
        if last >= cols - 2 and tail.isalnum() and not text.endswith(ELLIPSIS_MARKERS):
            words = text.split()
            if words and len(words[-1]) > 2:
                out.append(finding(
                    "truncation-marker", "medium", y, last,
                    f"row {y} reaches the edge and ends mid-word ({words[-1]!r}) with no "
                    f"ellipsis — a reader cannot tell this was cut",
                    text[-40:]))
    return out


def gate_shelf_containment(frame: dict) -> list[dict]:
    """A title inset in a border must leave border on both sides of it."""
    out: list[dict] = []
    cols, rows = frame["cols"], frame["rows"]
    for y in range(rows):
        cells = row_cells(frame, y)
        chars = [c["ch"] for c in cells]
        n_h = sum(1 for c in chars if c in BOX_HORIZONTAL)
        if n_h < 4:
            continue
        idx = [x for x in range(cols) if chars[x] in BOX_HORIZONTAL or chars[x] in BOX_CORNER]
        if not idx:
            continue
        left, right = min(idx), max(idx)
        run = "".join(chars[left:right + 1])
        letters = sum(1 for c in run if c.isalnum())
        if letters and letters > (right - left) * 0.5:
            out.append(finding(
                "shelf-containment", "medium", y, left,
                f"row {y} is a border line but more than half of it is text — the inset "
                f"label has crowded out the rule",
                run[:cols]))
    return out


def gate_glyph_risk(frame: dict) -> list[dict]:
    """Glyphs that depend on a font the reader may not have."""
    out: list[dict] = []
    pua, tofu = {}, {}
    for y in range(frame["rows"]):
        for x, c in enumerate(row_cells(frame, y)):
            for ch in c["ch"]:
                cp = ord(ch) if ch else 0
                if ch == "�":
                    tofu.setdefault((y, x), ch)
                elif 0xE000 <= cp <= 0xF8FF or 0xF0000 <= cp <= 0xFFFFD:
                    pua.setdefault((y, x), ch)
    if tofu:
        y, x = next(iter(tofu))
        out.append(finding(
            "glyph-risk", "high", y, x,
            f"{len(tofu)} replacement character(s) (U+FFFD) in the frame — bytes were "
            f"decoded wrongly somewhere in the pipeline",
            ""))
    if pua:
        y, x = next(iter(pua))
        out.append(finding(
            "glyph-risk", "medium", y, x,
            f"{len(pua)} private-use-area glyph(s) — these are Nerd Font icons and render "
            f"as tofu for anyone without that font. Needs a documented fallback.",
            ""))
    return out


def gate_colour_inventory(frame: dict) -> list[dict]:
    """Not a pass/fail — a count, so the palette can be argued about."""
    fg, attrs = {}, {"bold": 0, "dim": 0, "italic": 0, "underline": 0, "reverse": 0}
    for y in range(frame["rows"]):
        for c in row_cells(frame, y):
            if c["ch"].strip():
                fg[c["fg"]] = fg.get(c["fg"], 0) + 1
                for a in attrs:
                    if c.get(a):
                        attrs[a] += 1
    distinct = len([k for k in fg if k != "default"])
    sev = "medium" if distinct > 6 else "info"
    top = sorted(fg.items(), key=lambda kv: -kv[1])[:8]
    out = [finding(
        "colour-inventory", sev, None, None,
        f"{distinct} distinct foreground colours in use"
        + ("" if distinct <= 6 else " — above the point where colour stops encoding and "
                                    "starts decorating; check each one carries a meaning"),
        ", ".join(f"{k}×{v}" for k, v in top))]
    used = {k: v for k, v in attrs.items() if v}
    if not used.get("dim") and not used.get("bold"):
        out.append(finding(
            "colour-inventory", "medium", None, None,
            "no bold and no dim anywhere in the frame — every glyph carries the same "
            "weight, so the screen has no hierarchy that survives a monochrome terminal",
            ""))
    else:
        out.append(finding("colour-inventory", "info", None, None,
                           "attribute use: " + ", ".join(f"{k}×{v}" for k, v in used.items()),
                           ""))
    return out


def gate_ink(frame: dict) -> list[dict]:
    total = frame["cols"] * frame["rows"]
    ink = sum(1 for y in range(frame["rows"]) for c in row_cells(frame, y) if c["ch"].strip())
    ratio = ink / total if total else 0
    return [finding("ink-density", "info", None, None,
                    f"{ratio:.0%} of cells carry a glyph",
                    "density is a decision, not a score — both the sparsest and densest "
                    "apps in the reference corpus are well designed")]


GATES = [
    ("border-integrity", gate_border_integrity),
    ("width-arithmetic", gate_width_arithmetic),
    ("overflow-wrap", gate_wrap),
    ("truncation-marker", gate_truncation_marker),
    ("shelf-containment", gate_shelf_containment),
    ("glyph-risk", gate_glyph_risk),
    ("colour-inventory", gate_colour_inventory),
    ("ink-density", gate_ink),
]

SEV_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frame")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any high finding")
    ap.add_argument("--only", help="comma-separated gate names")
    args = ap.parse_args()

    frame = load(args.frame)
    wanted = set(args.only.split(",")) if args.only else None

    findings: list[dict] = []
    for name, fn in GATES:
        if wanted and name not in wanted:
            continue
        findings.extend(fn(frame))
    findings.sort(key=lambda f: (SEV_ORDER.get(f["severity"], 9), f["row"] or 0))

    prov = frame.get("provenance", {})
    if args.json:
        print(json.dumps({"frame": {"kind": frame.get("kind"), "size":
                                    f"{frame['cols']}x{frame['rows']}", "provenance": prov},
                          "findings": findings}, indent=1, ensure_ascii=False))
    else:
        print(f"frame  {frame['cols']}x{frame['rows']}  kind={frame.get('kind')}  "
              f"parser={prov.get('parser', '?')}  term={prov.get('term', '?')}")
        if prov.get("parser_unknown_sequences"):
            print(f"  ! parser met sequences it does not model: "
                  f"{prov['parser_unknown_sequences']} — treat the frame with suspicion")
        print()
        if not findings:
            print("no findings")
        for f in findings:
            loc = f"r{f['row']}c{f['col']}" if f["row"] is not None else "-"
            print(f"[{f['severity']:6s}] {f['gate']:20s} {loc:>8s}  {f['message']}")
            if f["evidence"]:
                print(f"{'':41s}{f['evidence']}")
        highs = sum(1 for f in findings if f["severity"] == "high")
        print(f"\n{len(findings)} finding(s), {highs} high")

    if args.strict and any(f["severity"] == "high" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
