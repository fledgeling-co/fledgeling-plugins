#!/usr/bin/env python3
"""Capture a terminal application as a typed cell grid.

The frame this produces is the only evidence tui-craft accepts about how a TUI
looks. Source code is not evidence: a string template does not tell you how many
cells it occupies, and that gap is where terminal layout bugs live.

Two parsers, in preference order:

  pyte      Installed separately (`pip install pyte`, pure Python, no compiler).
            Preferred. A mature VT emulator with years of conformance fixes.
  builtin   Bundled here, zero dependency. Handles the subset real TUIs emit.
            Gated by golden fixtures: run `--self-test` and it refuses to
            report `captured` if any fixture mismatches.

A parser that quietly mis-parses is worse than no capture at all, because every
gate downstream then lies with confidence. So capture failure is a result:
this exits non-zero and emits `"kind": "capture-blocked"` rather than guessing.

Usage
-----
    # Capture a TUI after it settles, at a fixed size
    tui_capture.py --cmd "htop" --cols 100 --rows 30 --settle 1.5 -o frame.json

    # Drive it through states, capturing each one
    tui_capture.py --cmd "./myapp" --keys "j,j,Enter,wait:0.5,/,f,o,o" -o frame.json

    # Human-readable grid with column rulers (what you read to spot defects)
    tui_capture.py --cmd "./myapp" --dump

    # Verify the builtin parser against the golden fixtures
    tui_capture.py --self-test
"""

from __future__ import annotations

import argparse
import errno
import fcntl
import json
import os
import pty
import re
import select
import signal
import struct
import sys
import termios
import time
import unicodedata
from dataclasses import dataclass, field, asdict
from hashlib import sha256
from pathlib import Path

SCHEMA_VERSION = "tui-craft/frame/1"

# --------------------------------------------------------------------------
# Cell width — the arithmetic every TUI gets wrong at least once
# --------------------------------------------------------------------------

# Unicode TR11 East Asian Width: W (Wide) and F (Fullwidth) occupy two cells.
# 'A' (Ambiguous) is one cell in a Western locale and two in a CJK one; one is
# the safer default and is what every mainstream terminal does by default.
_ZERO_WIDTH_CATEGORIES = {"Mn", "Me", "Cf"}


def char_width(ch: str) -> int:
    """Cells occupied by a single code point. 0, 1, or 2."""
    if ch in ("‍", "️", "︎"):  # ZWJ and variation selectors
        return 0
    cp = ord(ch)
    if cp == 0:
        return 0
    if cp < 32 or 0x7F <= cp < 0xA0:
        return 0
    if unicodedata.category(ch) in _ZERO_WIDTH_CATEGORIES:
        return 0
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    # Emoji outside the EAW=W blocks still render double-width in most terminals.
    if 0x1F300 <= cp <= 0x1FAFF or 0x1F000 <= cp <= 0x1F0FF:
        return 2
    return 1


def string_width(s: str) -> int:
    """Cells a string occupies. This is what `len()` gets wrong."""
    return sum(char_width(c) for c in s)


# --------------------------------------------------------------------------
# The frame
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


@dataclass
class Frame:
    cols: int
    rows: int
    cells: list[list[Cell]]
    cursor: tuple[int, int] = (0, 0)
    title: str | None = None
    alt_screen: bool = False
    kind: str = "captured"
    provenance: dict = field(default_factory=dict)

    def row_text(self, y: int) -> str:
        """Row as text, with wide-cell continuations dropped.

        Column index into this string is NOT a cell column when the row holds
        wide characters. Use `cell_col_of` when the position matters.
        """
        return "".join(c.ch for c in self.cells[y] if c.w != 0).rstrip()

    def to_dict(self) -> dict:
        return {
            "schema": SCHEMA_VERSION,
            "kind": self.kind,
            "cols": self.cols,
            "rows": self.rows,
            "cursor": list(self.cursor),
            "title": self.title,
            "alt_screen": self.alt_screen,
            "provenance": self.provenance,
            "cells": [[asdict(c) for c in row] for row in self.cells],
        }

    @staticmethod
    def blank(cols: int, rows: int) -> "Frame":
        return Frame(cols, rows, [[Cell() for _ in range(cols)] for _ in range(rows)])


# --------------------------------------------------------------------------
# Builtin parser — the subset real TUIs emit
# --------------------------------------------------------------------------

_SGR_FG = {
    30: "black", 31: "red", 32: "green", 33: "yellow", 34: "blue",
    35: "magenta", 36: "cyan", 37: "white", 39: "default",
    90: "bright_black", 91: "bright_red", 92: "bright_green", 93: "bright_yellow",
    94: "bright_blue", 95: "bright_magenta", 96: "bright_cyan", 97: "bright_white",
}
_SGR_BG = {k + 10: v for k, v in _SGR_FG.items() if k != 39}
_SGR_BG[49] = "default"


class BuiltinScreen:
    """A minimal VT100/xterm screen model.

    Deliberately small. It implements what TUI frameworks actually emit and
    ignores the rest — but it never silently mangles: an unrecognised sequence
    is counted, and a capture with unknown sequences reports them so you can
    decide whether the frame is trustworthy.
    """

    def __init__(self, cols: int, rows: int):
        self.cols, self.rows = cols, rows
        self.reset()

    def reset(self) -> None:
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.x = self.y = 0
        self.saved = (0, 0)
        self.title: str | None = None
        self.alt_screen = False
        self.autowrap = True
        self.scroll_top, self.scroll_bot = 0, self.rows - 1
        self.attrs = dict(fg="default", bg="default", bold=False, dim=False,
                          italic=False, underline=False, reverse=False)
        self.unknown: dict[str, int] = {}
        self._pending_wrap = False

    # -- writing ---------------------------------------------------------
    def _blank(self) -> Cell:
        return Cell(" ", 1, self.attrs["fg"], self.attrs["bg"], self.attrs["bold"],
                    self.attrs["dim"], self.attrs["italic"], self.attrs["underline"],
                    self.attrs["reverse"])

    def put(self, ch: str) -> None:
        w = char_width(ch)
        if w == 0:
            # Combining mark / ZWJ / variation selector: attach to the cell
            # to its left. This is what makes a grapheme cluster one cell.
            px = self.x - 1
            while px >= 0 and self.grid[self.y][px].w == 0:
                px -= 1
            if px >= 0:
                self.grid[self.y][px].ch += ch
            return
        if self._pending_wrap and self.autowrap:
            self._pending_wrap = False
            self.x = 0
            self._index()
        if self.x + w > self.cols:
            if not self.autowrap:
                return
            self.x = 0
            self._index()
        cell = self._blank()
        cell.ch, cell.w = ch, w
        self.grid[self.y][self.x] = cell
        for k in range(1, w):
            if self.x + k < self.cols:
                cont = self._blank()
                cont.ch, cont.w = "", 0
                self.grid[self.y][self.x + k] = cont
        self.x += w
        if self.x >= self.cols:
            self.x = self.cols - 1
            self._pending_wrap = True

    def _index(self) -> None:
        if self.y == self.scroll_bot:
            self.grid.pop(self.scroll_top)
            self.grid.insert(self.scroll_bot, [Cell() for _ in range(self.cols)])
        elif self.y < self.rows - 1:
            self.y += 1

    def _reverse_index(self) -> None:
        if self.y == self.scroll_top:
            self.grid.pop(self.scroll_bot)
            self.grid.insert(self.scroll_top, [Cell() for _ in range(self.cols)])
        elif self.y > 0:
            self.y -= 1

    def _clamp(self) -> None:
        self.x = max(0, min(self.x, self.cols - 1))
        self.y = max(0, min(self.y, self.rows - 1))
        self._pending_wrap = False

    # -- CSI -------------------------------------------------------------
    def csi(self, params: str, private: str, final: str) -> None:
        nums = [int(p) if p.isdigit() else 0 for p in params.split(";")] if params else []

        def p(i: int, default: int = 1) -> int:
            return nums[i] if i < len(nums) and nums[i] else default

        if final == "H" or final == "f":
            self.y, self.x = p(0) - 1, p(1) - 1
            self._clamp()
        elif final == "A":
            self.y -= p(0); self._clamp()
        elif final == "B":
            self.y += p(0); self._clamp()
        elif final == "C":
            self.x += p(0); self._clamp()
        elif final == "D":
            self.x -= p(0); self._clamp()
        elif final == "E":
            self.y += p(0); self.x = 0; self._clamp()
        elif final == "F":
            self.y -= p(0); self.x = 0; self._clamp()
        elif final == "G" or final == "`":
            self.x = p(0) - 1; self._clamp()
        elif final == "d":
            self.y = p(0) - 1; self._clamp()
        elif final == "J":
            mode = nums[0] if nums else 0
            if mode == 0:
                for x in range(self.x, self.cols):
                    self.grid[self.y][x] = self._blank()
                for y in range(self.y + 1, self.rows):
                    self.grid[y] = [self._blank() for _ in range(self.cols)]
            elif mode == 1:
                for x in range(0, min(self.x + 1, self.cols)):
                    self.grid[self.y][x] = self._blank()
                for y in range(0, self.y):
                    self.grid[y] = [self._blank() for _ in range(self.cols)]
            else:
                self.grid = [[self._blank() for _ in range(self.cols)]
                             for _ in range(self.rows)]
        elif final == "K":
            mode = nums[0] if nums else 0
            rng = (range(self.x, self.cols) if mode == 0 else
                   range(0, min(self.x + 1, self.cols)) if mode == 1 else
                   range(0, self.cols))
            for x in rng:
                self.grid[self.y][x] = self._blank()
        elif final == "X":
            for x in range(self.x, min(self.x + p(0), self.cols)):
                self.grid[self.y][x] = self._blank()
        elif final == "@":
            n = p(0)
            row = self.grid[self.y]
            self.grid[self.y] = (row[:self.x] + [self._blank() for _ in range(n)]
                                 + row[self.x:])[:self.cols]
        elif final == "P":
            n = p(0)
            row = self.grid[self.y]
            self.grid[self.y] = (row[:self.x] + row[self.x + n:]
                                 + [self._blank() for _ in range(n)])[:self.cols]
        elif final == "L":
            n = p(0)
            for _ in range(n):
                self.grid.insert(self.y, [self._blank() for _ in range(self.cols)])
                self.grid.pop(self.scroll_bot + 1 if self.scroll_bot + 1 < len(self.grid)
                              else -1)
        elif final == "M":
            n = p(0)
            for _ in range(n):
                if self.y < len(self.grid):
                    self.grid.pop(self.y)
                    self.grid.insert(self.scroll_bot,
                                     [self._blank() for _ in range(self.cols)])
        elif final == "S":
            for _ in range(p(0)):
                self.grid.pop(self.scroll_top)
                self.grid.insert(self.scroll_bot, [self._blank() for _ in range(self.cols)])
        elif final == "T":
            for _ in range(p(0)):
                self.grid.pop(self.scroll_bot)
                self.grid.insert(self.scroll_top, [self._blank() for _ in range(self.cols)])
        elif final == "r":
            self.scroll_top = (p(0) - 1) if nums else 0
            self.scroll_bot = (p(1, self.rows) - 1) if len(nums) > 1 else self.rows - 1
            self.scroll_top = max(0, min(self.scroll_top, self.rows - 1))
            self.scroll_bot = max(self.scroll_top, min(self.scroll_bot, self.rows - 1))
            self.x = self.y = 0
        elif final == "m":
            self.sgr(nums or [0])
        elif final in ("h", "l"):
            on = final == "h"
            for n in nums:
                if private == "?":
                    if n in (1049, 1047, 47):
                        self.alt_screen = on
                        if on:
                            self.grid = [[Cell() for _ in range(self.cols)]
                                         for _ in range(self.rows)]
                    elif n == 7:
                        self.autowrap = on
        elif final == "s":
            self.saved = (self.x, self.y)
        elif final == "u":
            self.x, self.y = self.saved
            self._clamp()
        elif final in ("t", "n", "c", "p", "q"):
            pass  # window ops / device status / cursor style: no visual effect here
        else:
            self.unknown[f"CSI {private}{final}"] = self.unknown.get(
                f"CSI {private}{final}", 0) + 1

    def sgr(self, nums: list[int]) -> None:
        i = 0
        while i < len(nums):
            n = nums[i]
            if n == 0:
                self.attrs.update(fg="default", bg="default", bold=False, dim=False,
                                  italic=False, underline=False, reverse=False)
            elif n == 1:
                self.attrs["bold"] = True
            elif n == 2:
                self.attrs["dim"] = True
            elif n == 3:
                self.attrs["italic"] = True
            elif n == 4:
                self.attrs["underline"] = True
            elif n == 7:
                self.attrs["reverse"] = True
            elif n == 22:
                self.attrs["bold"] = self.attrs["dim"] = False
            elif n == 23:
                self.attrs["italic"] = False
            elif n == 24:
                self.attrs["underline"] = False
            elif n == 27:
                self.attrs["reverse"] = False
            elif n in _SGR_FG:
                self.attrs["fg"] = _SGR_FG[n]
            elif n in _SGR_BG:
                self.attrs["bg"] = _SGR_BG[n]
            elif n in (38, 48):
                key = "fg" if n == 38 else "bg"
                if i + 1 < len(nums) and nums[i + 1] == 5:
                    self.attrs[key] = f"idx{nums[i + 2]}" if i + 2 < len(nums) else "default"
                    i += 2
                elif i + 1 < len(nums) and nums[i + 1] == 2:
                    rgb = nums[i + 2:i + 5]
                    if len(rgb) == 3:
                        self.attrs[key] = "#%02x%02x%02x" % tuple(rgb)
                    i += 4
            i += 1

    # -- stream ----------------------------------------------------------
    _CSI_RE = re.compile(r"\x1b\[([?><!]?)([0-9;:]*)([@-~])")
    _OSC_RE = re.compile(r"\x1b\](\d+);([^\x07\x1b]*)(?:\x07|\x1b\\)")
    _ESC_RE = re.compile(r"\x1b([()#][0-9A-Za-z]|[0-9A-Za-z=><])")
    _DCS_RE = re.compile(r"\x1b(?:P|_|\^|X)[^\x1b]*(?:\x1b\\|\x07)", re.S)

    def feed(self, data: str) -> None:
        i, n = 0, len(data)
        while i < n:
            ch = data[i]
            if ch == "\x1b":
                for rx, handler in (
                    (self._CSI_RE, "csi"),
                    (self._OSC_RE, "osc"),
                    (self._DCS_RE, "dcs"),
                    (self._ESC_RE, "esc"),
                ):
                    m = rx.match(data, i)
                    if not m:
                        continue
                    if handler == "csi":
                        self.csi(m.group(2), m.group(1), m.group(3))
                    elif handler == "osc":
                        if m.group(1) in ("0", "2"):
                            self.title = m.group(2)
                    elif handler == "dcs":
                        self.unknown["DCS/APC (graphics?)"] = \
                            self.unknown.get("DCS/APC (graphics?)", 0) + 1
                    else:
                        code = m.group(1)
                        if code == "7":
                            self.saved = (self.x, self.y)
                        elif code == "8":
                            self.x, self.y = self.saved; self._clamp()
                        elif code == "M":
                            self._reverse_index()
                        elif code in ("D", "E"):
                            if code == "E":
                                self.x = 0
                            self._index()
                        elif code == "c":
                            self.reset()
                    i = m.end()
                    break
                else:
                    self.unknown["bare ESC"] = self.unknown.get("bare ESC", 0) + 1
                    i += 1
                continue
            if ch == "\r":
                self.x = 0; self._pending_wrap = False
            elif ch == "\n":
                self._index(); self._pending_wrap = False
            elif ch == "\b":
                self.x = max(0, self.x - 1); self._pending_wrap = False
            elif ch == "\t":
                self.x = min(self.cols - 1, (self.x // 8 + 1) * 8)
            elif ch == "\x07":
                pass
            elif ord(ch) < 32:
                pass
            else:
                self.put(ch)
            i += 1

    def to_frame(self) -> Frame:
        return Frame(self.cols, self.rows, [list(r) for r in self.grid],
                     (self.x, self.y), self.title, self.alt_screen)


# --------------------------------------------------------------------------
# pyte adapter — same schema, better parser
# --------------------------------------------------------------------------


def _frame_from_pyte(cols: int, rows: int, data: str):
    import pyte  # noqa: PLC0415

    screen = pyte.Screen(cols, rows)
    stream = pyte.Stream(screen)
    stream.feed(data)
    frame = Frame.blank(cols, rows)
    for y in range(rows):
        x = 0
        while x < cols:
            pch = screen.buffer[y][x]
            ch = pch.data or " "
            w = string_width(ch) or 1
            frame.cells[y][x] = Cell(
                ch=ch, w=w,
                fg=str(pch.fg), bg=str(pch.bg), bold=bool(pch.bold),
                italic=bool(pch.italics), underline=bool(pch.underscore),
                reverse=bool(pch.reverse),
            )
            for k in range(1, w):
                if x + k < cols:
                    frame.cells[y][x + k] = Cell(ch="", w=0, fg=str(pch.fg), bg=str(pch.bg))
            x += max(1, w)
    frame.cursor = (screen.cursor.x, screen.cursor.y)
    frame.title = getattr(screen, "title", None) or None
    return frame


# --------------------------------------------------------------------------
# PTY capture
# --------------------------------------------------------------------------

KEYMAP = {
    "Enter": "\r", "Return": "\r", "Tab": "\t", "Esc": "\x1b", "Escape": "\x1b",
    "Space": " ", "Backspace": "\x7f", "Up": "\x1b[A", "Down": "\x1b[B",
    "Right": "\x1b[C", "Left": "\x1b[D", "Home": "\x1b[H", "End": "\x1b[F",
    "PageUp": "\x1b[5~", "PageDown": "\x1b[6~", "Delete": "\x1b[3~",
}


def _resolve_key(token: str) -> tuple[str, float]:
    token = token.strip()
    if token.startswith("wait:"):
        return "", float(token[5:])
    if token in KEYMAP:
        return KEYMAP[token], 0.05
    if token.startswith("C-") and len(token) == 3:
        return chr(ord(token[2].lower()) - 96), 0.05
    return token, 0.03


def capture(cmd: str, cols: int, rows: int, settle: float, keys: str | None,
            timeout: float, env_extra: dict[str, str], parser: str):
    raw = bytearray()
    pid, fd = pty.fork()
    if pid == 0:  # child
        env = os.environ.copy()
        env.update({"TERM": env_extra.get("TERM", "xterm-256color"),
                    "COLUMNS": str(cols), "LINES": str(rows)})
        env.update(env_extra)
        env.pop("COLORTERM", None) if env_extra.get("NO_COLORTERM") else None
        try:
            os.execvp("/bin/sh", ["/bin/sh", "-c", cmd])
        finally:
            os._exit(127)

    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
    deadline = time.time() + timeout

    def pump(until: float) -> None:
        while time.time() < until and time.time() < deadline:
            r, _, _ = select.select([fd], [], [], 0.05)
            if not r:
                continue
            try:
                chunk = os.read(fd, 65536)
            except OSError as e:
                if e.errno in (errno.EIO, errno.EBADF):
                    return
                raise
            if not chunk:
                return
            raw.extend(chunk)

    pump(time.time() + settle)
    if keys:
        for token in keys.split(","):
            seq, pause = _resolve_key(token)
            if seq:
                os.write(fd, seq.encode())
            pump(time.time() + max(pause, 0.05))
    pump(time.time() + 0.35)

    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.08)
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        os.waitpid(pid, os.WNOHANG)
        os.close(fd)
    except OSError:
        pass

    data = raw.decode("utf-8", errors="replace")
    used = parser
    if parser == "auto":
        try:
            import pyte  # noqa: F401,PLC0415
            used = "pyte"
        except ImportError:
            used = "builtin"

    unknown: dict[str, int] = {}
    if used == "pyte":
        frame = _frame_from_pyte(cols, rows, data)
    else:
        screen = BuiltinScreen(cols, rows)
        screen.feed(data)
        frame = screen.to_frame()
        unknown = screen.unknown

    frame.provenance = {
        "method": "pty",
        "command": cmd,
        "size": f"{cols}x{rows}",
        "term": env_extra.get("TERM", "xterm-256color"),
        "keys": keys or "",
        "settle_s": settle,
        "parser": used,
        "parser_unknown_sequences": unknown,
        "raw_bytes": len(raw),
        "raw_sha256": sha256(bytes(raw)).hexdigest()[:16],
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    return frame, bytes(raw)


# --------------------------------------------------------------------------
# Ruler dump — the artifact you actually read
# --------------------------------------------------------------------------


def dump(frame: Frame, show_cursor: bool = True) -> str:
    out: list[str] = []
    cols = frame.cols
    hundreds = "".join(str((c // 100) % 10) for c in range(cols))
    tens = "".join(str((c // 10) % 10) for c in range(cols))
    ones = "".join(str(c % 10) for c in range(cols))
    pad = "     "
    if cols > 99:
        out.append(pad + hundreds)
    out.append(pad + tens)
    out.append(pad + ones)
    out.append(pad + "-" * cols)
    for y, row in enumerate(frame.cells):
        line = "".join(c.ch if c.w != 0 else "" for c in row)
        out.append(f"{y:3d} |{line}")
    out.append(pad + "-" * cols)
    meta = [f"{cols}x{frame.rows}", f"parser={frame.provenance.get('parser', '?')}"]
    if show_cursor:
        meta.append(f"cursor={frame.cursor}")
    if frame.alt_screen:
        meta.append("alt-screen")
    if frame.title:
        meta.append(f"title={frame.title!r}")
    out.append(pad + "  ".join(meta))
    return "\n".join(out)


# --------------------------------------------------------------------------
# Golden fixtures — the builtin parser is only trusted while these pass
# --------------------------------------------------------------------------

FIXTURES: list[tuple[str, str, int, int, list[str]]] = [
    ("plain", "hello", 10, 2, ["hello", ""]),
    ("cr_lf", "ab\r\ncd", 10, 2, ["ab", "cd"]),
    ("cup", "\x1b[2;3Hx", 10, 2, ["", "  x"]),
    ("erase_line", "abcdef\x1b[1G\x1b[Kzz", 10, 1, ["zz"]),
    ("erase_display", "abc\r\ndef\x1b[2J", 10, 2, ["", ""]),
    ("wide_cjk", "│日本│", 10, 1, ["│日本│"]),
    ("combining", "e\u0301x", 10, 1, ["e\u0301x"]),
    ("zwj_emoji", "a\U0001F468\u200D\U0001F4BBb", 10, 1,
     ["a\U0001F468\u200D\U0001F4BBb"]),
    ("sgr_ignored_in_text", "\x1b[1;31mred\x1b[0m", 10, 1, ["red"]),
    ("cursor_back", "abc\x1b[2Dz", 10, 1, ["azc"]),
    ("insert_chars", "abcd\x1b[1G\x1b[2@xy", 10, 1, ["xyabcd"]),
    ("delete_chars", "abcdef\x1b[1G\x1b[2P", 10, 1, ["cdef"]),
    ("box", "┌──┐\r\n│  │\r\n└──┘", 6, 3, ["┌──┐", "│  │", "└──┘"]),
    ("autowrap", "abcdef", 3, 2, ["abc", "def"]),
    ("osc_title", "\x1b]0;My App\x07hi", 10, 1, ["hi"]),
    ("scroll_up", "a\r\nb\r\nc\r\n", 4, 3, ["b", "c", ""]),
]


def self_test(verbose: bool = True) -> bool:
    ok = True
    for name, data, cols, rows, expect in FIXTURES:
        screen = BuiltinScreen(cols, rows)
        screen.feed(data)
        frame = screen.to_frame()
        got = [frame.row_text(y) for y in range(rows)]
        if got != expect:
            ok = False
            if verbose:
                print(f"FAIL {name}\n  expected {expect}\n  got      {got}")
        elif verbose:
            print(f"ok   {name}")
    if verbose:
        extra = f"width('日本')={string_width('日本')} (expect 4), " \
                f"width('e\\u0301')={string_width(chr(101) + chr(0x301))} (expect 1)"
        print(extra)
    ok = ok and string_width("日本") == 4 and string_width("é") == 1
    if verbose:
        print("\nbuiltin parser:", "TRUSTED" if ok else "NOT TRUSTED — do not report captured frames")
    return ok


# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cmd", help="command to run under a pty")
    ap.add_argument("--cols", type=int, default=100)
    ap.add_argument("--rows", type=int, default=30)
    ap.add_argument("--settle", type=float, default=1.0,
                    help="seconds to wait for first paint before sending keys")
    ap.add_argument("--keys", help="comma-separated: j,k,Enter,C-c,wait:0.5,/,f,o,o")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--term", default="xterm-256color")
    ap.add_argument("--no-color", action="store_true",
                    help="set NO_COLOR=1 to test the degraded path")
    ap.add_argument("--parser", choices=["auto", "pyte", "builtin"], default="auto")
    ap.add_argument("-o", "--out", help="write frame JSON here")
    ap.add_argument("--raw-out", help="write the raw byte stream here")
    ap.add_argument("--dump", action="store_true", help="print the ruler grid")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1

    if not args.cmd:
        ap.error("--cmd is required (or use --self-test)")

    if args.parser == "builtin" or (args.parser == "auto" and "pyte" not in sys.modules):
        try:
            import pyte  # noqa: F401
        except ImportError:
            if not self_test(verbose=False):
                print(json.dumps({"schema": SCHEMA_VERSION, "kind": "capture-blocked",
                                  "reason": "builtin parser failed its golden fixtures; "
                                            "install pyte (pip install pyte) or fix the parser"}),
                      file=sys.stderr)
                return 2

    env_extra = {"TERM": args.term}
    if args.no_color:
        env_extra["NO_COLOR"] = "1"

    frame, raw = capture(args.cmd, args.cols, args.rows, args.settle, args.keys,
                         args.timeout, env_extra, args.parser)

    ink = sum(1 for row in frame.cells for c in row if c.ch.strip())
    if ink == 0:
        frame.kind = "capture-blocked"
        frame.provenance["reason"] = "nothing was drawn — command failed, exited " \
                                     "immediately, or needs a longer --settle"

    if args.raw_out:
        Path(args.raw_out).write_bytes(raw)
    if args.out:
        Path(args.out).write_text(json.dumps(frame.to_dict(), ensure_ascii=False, indent=1))
    if args.dump or not args.out:
        print(dump(frame))
    if frame.kind == "capture-blocked":
        print(f"\ncapture-blocked: {frame.provenance.get('reason')}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
