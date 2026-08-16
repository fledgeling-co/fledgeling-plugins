#!/usr/bin/env python3
"""Turn a raw ANSI dump into the same frame schema `tui_capture.py` produces.

Frameworks already know how to render themselves into a byte stream for testing
— `teatest` for Bubble Tea, `TestBackend` for Ratatui, `run_test` for Textual,
`ink-testing-library` for Ink. Those producers are deterministic and free of
timing races, which makes them better than a pty capture when you own the source.

This converts their output into the frame the gates read, so there is one schema
and one set of checks regardless of where the bytes came from.

The frame is marked `method: "ansi-replay"` in its provenance. It carries no
information about the host terminal — colour depth, real font, actual width
handling — so it is not a substitute for one pty capture before shipping.

Usage
-----
    frame_from_ansi.py frame.ansi --cols 100 --rows 30 -o frame.json
    cat frame.ansi | frame_from_ansi.py - --cols 80 --rows 24 --dump
"""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tui_capture import (  # noqa: E402
    SCHEMA_VERSION,
    BuiltinScreen,
    _frame_from_pyte,
    dump,
    self_test,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="file containing the ANSI stream, or - for stdin")
    ap.add_argument("--cols", type=int, required=True)
    ap.add_argument("--rows", type=int, required=True)
    ap.add_argument("--parser", choices=["auto", "pyte", "builtin"], default="auto")
    ap.add_argument("--source", default="",
                    help="what produced this stream, e.g. 'teatest' — recorded in provenance")
    ap.add_argument("-o", "--out")
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.buffer.read() if args.input == "-" else Path(args.input).read_bytes()
    data = raw.decode("utf-8", errors="replace")

    used = args.parser
    if used == "auto":
        try:
            import pyte  # noqa: F401
            used = "pyte"
        except ImportError:
            used = "builtin"

    unknown = {}
    if used == "pyte":
        frame = _frame_from_pyte(args.cols, args.rows, data)
    else:
        if not self_test(verbose=False):
            print(json.dumps({"schema": SCHEMA_VERSION, "kind": "capture-blocked",
                              "reason": "builtin parser failed its golden fixtures"}),
                  file=sys.stderr)
            return 2
        screen = BuiltinScreen(args.cols, args.rows)
        screen.feed(data)
        frame = screen.to_frame()
        unknown = screen.unknown

    frame.provenance = {
        "method": "ansi-replay",
        "source": args.source or args.input,
        "size": f"{args.cols}x{args.rows}",
        "term": "n/a — replayed, not hosted",
        "parser": used,
        "parser_unknown_sequences": unknown,
        "raw_bytes": len(raw),
        "raw_sha256": sha256(raw).hexdigest()[:16],
    }

    ink = sum(1 for row in frame.cells for c in row if c.ch.strip())
    if ink == 0:
        frame.kind = "capture-blocked"
        frame.provenance["reason"] = "the stream drew nothing at this size"

    if args.out:
        Path(args.out).write_text(json.dumps(frame.to_dict(), ensure_ascii=False, indent=1))
    if args.dump or not args.out:
        print(dump(frame))
    return 2 if frame.kind == "capture-blocked" else 0


if __name__ == "__main__":
    sys.exit(main())
