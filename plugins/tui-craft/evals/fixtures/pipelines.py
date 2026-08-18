#!/usr/bin/env python3
"""pipelines — a pipeline status dashboard. Eval fixture, deliberately defective.

Three planted defects, none of them findable by reading this file:

  1. Every column is padded with len(), which counts characters rather than
     cells. The "build" row's status label is CJK, so that row draws three cells
     wider than its siblings and its right border is pushed off the panel edge.
  2. The footer key hint is written whole, unmeasured, so it runs past the right
     edge and continues mid-word on the row below.
  3. The "test" row's target is cut with a hard slice and no ellipsis, so nothing
     on screen says it was cut.

Standard library only. Addresses the grid with absolute cursor moves, holds the
frame, then exits.
"""

import os
import shutil
import signal
import sys
import time

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
REVERSE = "\x1b[7m"
CYAN = "\x1b[36m"
GREEN = "\x1b[32m"
RED = "\x1b[31m"
YELLOW = "\x1b[33m"

TITLE = " Pipelines "
SELECTED = 2  # index into ROWS

W_NAME, W_TARGET, W_STATUS, W_DUR = 10, 26, 12, 10

# name, target, status, status colour, duration
ROWS = [
    ("deploy", "prod-east-1", "Active", GREEN, "1m 04s"),
    ("build", "build-farm-tokyo-3", "実行中", YELLOW, "12m 41s"),
    ("test", "staging-eu-west-2-canary-shard-07", "Failed", RED, "3m 18s"),
    ("lint", "prod-west-2", "Active", GREEN, "0m 22s"),
    ("publish", "registry-internal", "Queued", DIM, "--"),
    ("notify", "hooks-slack-eng", "Active", GREEN, "0m 03s"),
]

FOOTER = ("j down  k up  Enter open  / filter  r refresh  a archive  l logs  "
          "x cancel  q quit  ? help  ^p palette  ^r rerun failed")


def pad(line, inner):
    """Pad to the panel's inner width. len() is the bug and it is deliberate."""
    return line + " " * max(0, inner - len(line))


def columns(name, target, status, duration):
    target = target[:W_TARGET]  # hard cut, no marker — defect 3
    return (f"  {name:<{W_NAME}}{target:<{W_TARGET}}"
            f"{status:<{W_STATUS}}{duration:>{W_DUR}}")


def draw(out, cols, rows):
    inner = cols - 2
    bottom = rows - 3

    dashes = inner - len(TITLE)
    out(f"\x1b[1;1H{CYAN}┌{BOLD}{TITLE}{RESET}{CYAN}"
        f"{'─' * dashes}┐{RESET}")

    head = columns("NAME", "TARGET", "STATUS", "DURATION")
    out(f"\x1b[2;1H{CYAN}│{RESET}{DIM}{pad(head, inner)}{RESET}{CYAN}│{RESET}")
    out(f"\x1b[3;1H{CYAN}├{'─' * inner}┤{RESET}")

    y = 4
    for i, (name, target, status, colour, duration) in enumerate(ROWS):
        marker = "▸" if i == SELECTED else " "
        body = pad(marker + columns(name, target, status, duration)[1:], inner)
        style = REVERSE if i == SELECTED else ""
        painted = body.replace(status, f"{colour}{status}{RESET}{style}", 1)
        out(f"\x1b[{y};1H{CYAN}│{RESET}{style}{painted}{RESET}"
            f"{CYAN}│{RESET}")
        y += 1

    while y < bottom:
        out(f"\x1b[{y};1H{CYAN}│{RESET}{' ' * inner}{CYAN}│{RESET}")
        y += 1
    out(f"\x1b[{bottom};1H{CYAN}└{'─' * inner}┘{RESET}")

    summary = f"  {len(ROWS)} pipelines  1 failing  2 running"
    out(f"\x1b[{rows - 2};1H{DIM}{summary}{RESET}")
    out(f"\x1b[{rows - 1};1H{DIM}{FOOTER}{RESET}")  # unmeasured — defect 2


def _quit(signum, frame):
    """Leave on SIGTERM/SIGINT with status 0, so a harness that ends the run does
    not have to read a signal death as a crash. Restoring the terminal is
    best-effort: if nothing is reading the pty the write would block, and hanging
    here is worse than leaving the alternate screen up."""
    try:
        os.write(1, b"\x1b[?25h\x1b[?1049l")
    except OSError:
        pass
    os._exit(0)


def main():
    signal.signal(signal.SIGTERM, _quit)
    signal.signal(signal.SIGINT, _quit)
    size = shutil.get_terminal_size(fallback=(100, 30))
    cols, rows = max(40, size.columns), max(12, size.lines)
    out = sys.stdout.write
    out("\x1b[?1049h\x1b[?25l\x1b[2J")
    try:
        draw(out, cols, rows)
        sys.stdout.flush()
        time.sleep(45)
    finally:
        out("\x1b[?25h\x1b[?1049l")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
