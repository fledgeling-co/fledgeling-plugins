#!/usr/bin/env python3
"""A legitimately sparse but entirely valid empty state. The regression guard.

Nothing here is a defect. A tool that has been taught to distrust sparse frames
must still accept this one: it addresses the grid, takes the alternate screen,
and its emptiness is the design — an empty state that names the action which
fills it, which is what the corpus's good empty states do.
"""
import sys, time

W, H = 80, 24


def main():
    out = sys.stdout
    out.write("\x1b[?1049h\x1b[?25l\x1b[2J\x1b[H")
    msg = "No pipelines yet"
    hint = "<ENTER> to connect a repository"
    out.write(f"\x1b[{H // 2};{(W - len(msg)) // 2 + 1}H\x1b[1m{msg}\x1b[0m")
    out.write(f"\x1b[{H // 2 + 2};{(W - len(hint)) // 2 + 1}H\x1b[2m{hint}\x1b[0m")
    out.write(f"\x1b[{H};1H\x1b[2m [q] quit\x1b[0m")
    out.flush()
    time.sleep(6)


if __name__ == "__main__":
    main()
