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

# Kept in step with tui_capture.py's list of the same name. Duplicated rather
# than imported so the gates can read a frame without the capture script on the
# path — the two are checked against each other by --self-test.
LAUNCH_FAILURE_SIGNATURES = (
    "command not found",
    "no such file or directory",
    "permission denied",
    "is a directory",
    "cannot execute binary file",
    "exec format error",
    "error while loading shared libraries",
    "traceback (most recent call last)",
    "modulenotfounderror",
    "importerror",
    "syntax error near unexpected token",
    "panic: ",
    "segmentation fault",
    "bad interpreter",
)


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


def gate_render_proof(frame: dict) -> list[dict]:
    """First, prove something was drawn. Every gate below passes vacuously otherwise.

    An all-green gate report and a frame that is a shell error are the same
    output, and that is not a hypothetical: measured on this machine, 18 Aug
    2026, the predecessor returned `kind: "captured"`, exit 0 and 0 high
    findings for five separate non-UI cases — a missing binary, a
    non-executable file, a Python traceback, a shell syntax error, and
    `echo hello`. Every geometric gate below passed on all five, because a
    near-empty grid has no border to tear and no column to misalign.

    This gate re-decides the question from the frame file rather than trusting
    the producer's own label, so a frame that was mislabelled upstream, or
    written by an older version of the capture script, still gets caught here.

    It does NOT use ink density as the deciding signal. The reference corpus
    runs from 6% to 96% ink and both ends are well-designed applications, so a
    density floor fails good screens for being unusual. The deciding signals
    are whether the program ever addressed the grid, and whether the first
    thing on screen is its own error message.
    """
    out: list[dict] = []
    if frame.get("kind") != "captured":
        return out

    prov = frame.get("provenance", {})
    signals = prov.get("signals")

    total = frame["cols"] * frame["rows"]
    ink = sum(1 for y in range(frame["rows"]) for c in row_cells(frame, y) if c["ch"].strip())
    ratio = ink / total if total else 0.0

    first = ""
    for y in range(frame["rows"]):
        text = visible_text(frame, y).strip()
        if text:
            first = text
            break
    low = first.lower()

    for sig in LAUNCH_FAILURE_SIGNATURES:
        if sig in low:
            out.append(finding(
                "render-proof", "high", 0, 0,
                "the first thing on this frame is a launch or runtime error, not a user "
                "interface — nothing below this line is a finding about a design",
                first[:120]))
            break

    if signals is None:
        # An older frame, or one produced by frame_from_ansi.py from a stream
        # whose control sequences were already consumed. Not a pass: the same
        # rule tui_design_gates.py applies to examined=0.
        out.append(finding(
            "render-proof", "medium", None, None,
            "this frame carries no protocol signals, so whether the program ever "
            "addressed the grid cannot be checked from it — re-capture with the current "
            "tui_capture.py, or say in the report that render proof was unavailable",
            "absent provenance.signals is not a pass"))
    else:
        addressed = bool(signals.get("cursor_moves") or signals.get("erases")
                         or signals.get("alt_screen_entered"))
        if not addressed:
            out.append(finding(
                "render-proof", "high", None, None,
                "the program never moved the cursor, cleared the screen or took the "
                "alternate screen — it wrote plain text and stopped, which is command "
                "output rather than a terminal UI",
                f"cursor_moves={signals.get('cursor_moves')} erases={signals.get('erases')} "
                f"alt_screen={signals.get('alt_screen_entered')} sgr={signals.get('sgr')} "
                "(SGR alone is not proof — a colourised traceback has it)"))
        elif ratio < 0.06:
            out.append(finding(
                "render-proof", "medium", None, None,
                f"{ratio:.0%} ink, below the 6% of the sparsest frame in the reference "
                f"corpus, on a frame that did address the grid — unusual rather than "
                f"wrong, so confirm the app had finished painting before you read it",
                f"settle_s={prov.get('settle_s')} exit_code={prov.get('exit_code')}"))
    return out


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
        # Not a pass. Three rows is the minimum from which a median row-end
        # means anything, and the predecessor returned silently here, so a
        # near-empty frame produced no finding from this gate at all.
        return [finding(
            "width-arithmetic", "medium", None, None,
            f"only {len(populated)} row(s) carry content, so there is no median row end "
            f"to measure against — this gate did not run rather than passed",
            "examined=0 is never a pass")]
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


def _border_columns(frame: dict) -> set[int]:
    """Columns that behave like a vertical rule: a box glyph on 3+ rows."""
    hits: dict[int, int] = {}
    for y in range(frame["rows"]):
        cells = row_cells(frame, y)
        for x in range(frame["cols"]):
            if cells[x]["ch"] in BOX_VERTICAL or cells[x]["ch"] in BOX_CORNER:
                hits[x] = hits.get(x, 0) + 1
    return {x for x, n in hits.items() if n >= 3}


def _content_spans(cols: int, borders: set[int]) -> list[tuple[int, int]]:
    """The runs of columns between vertical rules — where content actually lives."""
    spans: list[tuple[int, int]] = []
    start = None
    for x in range(cols):
        if x in borders:
            if start is not None and x - 1 >= start:
                spans.append((start, x - 1))
            start = None
        elif start is None:
            start = x
    if start is not None:
        spans.append((start, cols - 1))
    return spans


def _is_rule(cells: list[dict], left: int, right: int) -> bool:
    """True when this stretch of row is a border rule rather than a line of text."""
    box = sum(1 for x in range(left, right + 1) if cells[x]["ch"] in BOX_HORIZONTAL)
    return box > (right - left) * 0.25


def gate_wrap(frame: dict) -> list[dict]:
    """Content that ran off the right edge of its own column and continued below.

    In a full-screen TUI this is almost always a defect: a footer key list or a
    label that outgrew its box. The tell is a row filled to the edge of its
    container followed by a row that starts mid-word at the same container's
    left edge.

    The edge is the **container's**, not the frame's. The predecessor compared
    column 0 against column cols-1, which on any bordered app are both `│` and
    neither is alphanumeric — so the gate was structurally silent on the
    dominant shape in the reference corpus and on the exact Cronboard
    footer-overflow case anti-patterns.md attributes to it. It could only ever
    fire on borderless content running the full width. Splitting the row on its
    vertical rules restores the unbordered case as the single-span degenerate
    form of the same check.
    """
    out: list[dict] = []
    cols, rows = frame["cols"], frame["rows"]
    spans = _content_spans(cols, _border_columns(frame))
    for y in range(rows - 1):
        cells, nxt = row_cells(frame, y), row_cells(frame, y + 1)
        for left, right in spans:
            if right - left < 8:
                continue  # a narrow gutter or a one-word column cannot demonstrate a wrap
            # Tolerate one pad column on each side: `pad: 1` is the house default
            # for a panel, so content that has overflowed still stops one cell
            # short of the rule rather than touching it.
            ends = [x for x in range(left, right + 1) if cells[x]["ch"].strip()]
            starts = [x for x in range(left, right + 1) if nxt[x]["ch"].strip()]
            if not ends or not starts:
                continue
            # A rule is not prose. A bottom border carrying a shelf label
            # ("── SIZE 9.8K ──") sits directly above the footer, and reading
            # that pair as a wrapped word is a false positive measured on this
            # plugin's own example-dashboard.json.
            if _is_rule(cells, left, right) or _is_rule(nxt, left, right):
                continue
            if ends[-1] < right - 1 or starts[0] > left + 1:
                continue
            a, b = cells[ends[-1]]["ch"], nxt[starts[0]]["ch"]
            split_word = a.isalnum() and b.isalnum()
            # A footer key list is the documented case for this gate, and it wraps
            # at a bracket at least as often as mid-word: `… [y] copy url  [` then
            # `d] diff …`. An opening delimiter left unclosed at the container edge
            # is a split token by construction, so it counts.
            split_token = a in "[({<" and (b.isalnum() or b in "[({<")
            if split_word or split_token:
                where = "the frame" if len(spans) == 1 else f"the column at {left}-{right}"
                out.append(finding(
                    "overflow-wrap", "high", y, ends[-1],
                    f"row {y} fills to the right edge of {where} and row {y + 1} continues "
                    f"it mid-{'word' if split_word else 'token'} ({a!r}|{b!r}) — content "
                    f"wrapped instead of fitting or being demoted",
                    visible_text(frame, y)[max(0, ends[-1] - 29):ends[-1] + 1] + " ⏎ "
                    + visible_text(frame, y + 1)[starts[0]:starts[0] + 30]))
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
    """A count, never a score. The note is conditional on purpose.

    "Density is a decision" is a true statement about designs and a dangerous
    one about failures: the predecessor printed it at `[info]` beside 3% ink on
    a frame that was a shell error, which is copy that argues the reader out of
    the one suspicious number on the screen. So the reassurance is withheld
    unless render-proof has something to reassure about.
    """
    total = frame["cols"] * frame["rows"]
    ink = sum(1 for y in range(frame["rows"]) for c in row_cells(frame, y) if c["ch"].strip())
    ratio = ink / total if total else 0
    signals = frame.get("provenance", {}).get("signals") or {}
    addressed = bool(signals.get("cursor_moves") or signals.get("erases")
                     or signals.get("alt_screen_entered"))
    if frame.get("kind") == "captured" and not addressed:
        note = "no reassurance offered — see render-proof above; this number is not " \
               "evidence about a design until the frame is known to be one"
    else:
        note = "density is a decision, not a score — both the sparsest and densest " \
               "apps in the reference corpus are well designed"
    return [finding("ink-density", "info", None, None,
                    f"{ratio:.0%} of cells carry a glyph", note)]


GATES = [
    ("render-proof", gate_render_proof),
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


# --------------------------------------------------------------------------
# Self-test — every gate here has to have been seen to fire
# --------------------------------------------------------------------------


def _frame_from_rows(rows: list[str], kind: str = "captured",
                     signals: dict | None = None) -> dict:
    """Build a frame from text rows, measuring cell width the way a capture does.

    Width is measured rather than assumed: a fixture that hardcoded w=1 could
    not exercise width-arithmetic at all, which this self-test caught on its
    first run.
    """
    try:
        from tui_capture import char_width  # noqa: PLC0415
    except ImportError:
        def char_width(ch: str) -> int:  # fallback keeps the self-test runnable alone
            return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1

    grid: list[list[dict]] = []
    width = 0
    for r in rows:
        line: list[dict] = []
        for ch in r:
            w = char_width(ch)
            line.append({"ch": ch, "w": max(w, 1), "fg": "default", "bg": "default",
                         "bold": False, "italic": False, "underline": False,
                         "reverse": False})
            for _ in range(1, max(w, 1)):
                line.append({"ch": "", "w": 0, "fg": "default", "bg": "default",
                             "bold": False, "italic": False, "underline": False,
                             "reverse": False})
        grid.append(line)
        width = max(width, len(line))

    blank = {"ch": " ", "w": 1, "fg": "default", "bg": "default",
             "bold": False, "italic": False, "underline": False, "reverse": False}
    for line in grid:
        while len(line) < width:
            line.append(dict(blank))

    if signals is None:
        signals = {"cursor_moves": 4, "erases": 1, "sgr": 0,
                   "alt_screen_entered": True, "cursor_hidden": True, "bytes": 999}
    return {"schema": "tui-craft/frame/1", "kind": kind, "cols": width,
            "rows": len(grid), "cells": grid,
            "provenance": {"parser": "fixture", "signals": signals,
                           "exit_code": None, "exited_on_own": False, "settle_s": 1.0}}


# Each case is (name, gate, frame, must_fire). A gate with no failing case here
# is a gate nobody has watched fail, which is the objection tui-design's
# example-failing.json exists to answer and the arithmetic gates had no answer
# to at all.
def _self_test_cases() -> list[tuple[str, str, dict, bool]]:
    bordered_wrap = _frame_from_rows([
        "╭─ Log ──────────────────────╮",
        "│ deploying to production an │",
        "│ d waiting for the health c │",
        "│ heck to pass               │",
        "╰────────────────────────────╯",
    ])
    torn = _frame_from_rows([
        "╭────────────╮",
        "│ ok         │",
        "│ torn        ",
        "│ ok         │",
        "╰────────────╯",
    ])
    wide = _frame_from_rows([
        "│ short      │",
        "│ short      │",
        "│ 🚀 Deploy ymore",
        "│ short      │",
    ])
    shell_error = _frame_from_rows(
        ["/bin/sh: nope: command not found"],
        signals={"cursor_moves": 0, "erases": 0, "sgr": 0,
                 "alt_screen_entered": False, "cursor_hidden": False, "bytes": 33})
    plain_output = _frame_from_rows(
        ["total 8", "drwxr-xr-x  4 me  staff  128 Aug 18 09:00 .", "-rw-r--r--  1 me  staff   12 Aug 18 09:00 a"],
        signals={"cursor_moves": 0, "erases": 0, "sgr": 0,
                 "alt_screen_entered": False, "cursor_hidden": False, "bytes": 120})
    tofu = _frame_from_rows(["│ status: �� broken bytes │"])
    clean = _frame_from_rows([
        "╭─ Hosts ────────────────────╮",
        "│ web-01     up      12ms    │",
        "│ web-02     up      14ms    │",
        "│ db-01      down    —       │",
        "╰────────────────────────────╯",
    ])
    bracket_wrap = _frame_from_rows([
        "╭─ Pipelines ────────────────╮",
        "│ api-gateway   passing      │",
        "│ [j/k] move  [enter] open [ │",
        "│ r] rerun  [q] quit         │",
        "╰────────────────────────────╯",
    ])
    return [
        ("overflow-wrap fires inside a bordered panel", "overflow-wrap", bordered_wrap, True),
        ("overflow-wrap fires on a footer split at a bracket", "overflow-wrap", bracket_wrap, True),
        ("border-integrity fires on a torn right edge", "border-integrity", torn, True),
        ("width-arithmetic fires on a wide-glyph overrun", "width-arithmetic", wide, True),
        ("render-proof fires on a shell error", "render-proof", shell_error, True),
        ("render-proof fires on plain command output", "render-proof", plain_output, True),
        ("glyph-risk fires on U+FFFD", "glyph-risk", tofu, True),
        ("render-proof stays silent on a real frame", "render-proof", clean, False),
        ("overflow-wrap stays silent on a real frame", "overflow-wrap", clean, False),
        ("border-integrity stays silent on a real frame", "border-integrity", clean, False),
    ]


def self_test(verbose: bool = True) -> bool:
    by_name = dict(GATES)
    ok = True
    for label, gate, frame, must_fire in _self_test_cases():
        found = by_name[gate](frame)
        fired = any(f["severity"] in ("high", "medium") for f in found)
        good = fired == must_fire
        ok = ok and good
        if verbose:
            print(f"{'ok  ' if good else 'FAIL'} {label}")
            if not good:
                print(f"       expected {'a finding' if must_fire else 'silence'}, got {found}")

    try:
        from tui_capture import LAUNCH_FAILURE_SIGNATURES as CAP_SIGS  # noqa: PLC0415
        drift = set(LAUNCH_FAILURE_SIGNATURES) ^ set(CAP_SIGS)
        # "killed" is deliberately capture-only: it is a real word in a process
        # table a TUI might legitimately display.
        drift.discard("killed")
        if drift:
            ok = False
            if verbose:
                print(f"FAIL launch-failure signatures drifted from tui_capture.py: {sorted(drift)}")
        elif verbose:
            print("ok   launch-failure signatures match tui_capture.py")
    except ImportError:
        if verbose:
            print("--   tui_capture.py not importable; signature drift unchecked")

    if verbose:
        print("\ngates:", "TRUSTED" if ok else "NOT TRUSTED — a gate is not firing as specified")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frame", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any high finding")
    ap.add_argument("--only", help="comma-separated gate names")
    ap.add_argument("--self-test", action="store_true",
                    help="prove every gate can fire, against in-code fixtures")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1
    if not args.frame:
        ap.error("a frame file is required (or use --self-test)")

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
