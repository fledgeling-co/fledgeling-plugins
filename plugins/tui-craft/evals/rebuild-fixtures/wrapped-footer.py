#!/usr/bin/env python3
"""A bordered build monitor whose footer key list outgrew its panel and wrapped.

Fixture for the overflow-wrap gate. The wrap is INSIDE the border, which is the
shape the predecessor gate could not see: it compared column 0 against the last
column, and both hold a vertical rule on any bordered app.
"""
import sys, time

W, H = 80, 24
ROWS = [
    ("api-gateway",   "passing", "2m 14s"),
    ("web-frontend",  "passing", "1m 02s"),
    ("worker-queue",  "failing", "0m 48s"),
    ("scheduler",     "queued",  "--"),
    ("notifier",      "passing", "3m 31s"),
]
KEYS = ("[j/k] move  [enter] open  [r] rerun  [f] filter  [/] search  "
        "[y] copy url  [d] diff  [?] help  [q] quit")


def main():
    out = sys.stdout
    out.write("\x1b[?1049h\x1b[?25l\x1b[2J\x1b[H")   # alt screen, hide cursor, clear
    inner = W - 4                                     # border + one pad column each side
    lines = ["╭─ Pipelines ─" + "─" * (W - 27) + " 5 total ─╮"]
    lines.append("│ " + "NAME".ljust(20) + "STATUS".ljust(12) + "DURATION".ljust(inner - 32) + " │")
    lines.append("├" + "─" * (W - 2) + "┤")
    for i, (name, status, dur) in enumerate(ROWS):
        mark = "▸" if i == 2 else " "
        body = f"{mark} {name}".ljust(20) + status.ljust(12) + dur.ljust(inner - 32)
        lines.append("│ " + body + " │")
    while len(lines) < H - 4:
        lines.append("│ " + " " * inner + " │")
    # The defect: the key list is 89 cells and the panel holds 76, so it wraps
    # mid-word onto the row below instead of being demoted to a help overlay.
    lines.append("│ " + KEYS[:inner] + " │")
    lines.append("│ " + KEYS[inner:].ljust(inner) + " │")
    lines.append("╰" + "─" * (W - 2) + "╯")
    out.write("\r\n".join(lines[:H]))
    out.write("\x1b[H")
    out.flush()
    time.sleep(6)


if __name__ == "__main__":
    main()
