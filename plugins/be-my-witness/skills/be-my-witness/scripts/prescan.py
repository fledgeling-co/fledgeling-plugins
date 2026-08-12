#!/usr/bin/env python3
"""
prescan.py — the deterministic pass that runs BEFORE any model looks at a screenshot.

Four questions, none of which need judgement, all of which can end a run:

  1. is-evidence     a blank, uniform or near-empty capture is not evidence
  2. settled         a capture taken mid-load is a picture of a skeleton
  3. comparable      framing: is the aspect/scale close enough to compare at all
  4. tiles           where the ink actually is, so the vision pass has somewhere to start

Why this exists: a real capture suite scored design mocks against LOADING SKELETONS
for a whole run before anyone noticed, and a structural score reported four healthy
surfaces as "drifted" because a 440x275 card was being compared against a 1440x900
viewport. Both are caught here, for free, before a single token is spent.

USAGE
    python3 prescan.py shot.png [--reference mock.png] [--json] [--tiles-out DIR]

DEPENDENCIES
    Pillow if present; otherwise a pure-stdlib PNG reader (zlib + struct). No install
    step, so the skill travels to a machine that has neither.
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

# --------------------------------------------------------------------------- #
# Image loading: Pillow when available, stdlib PNG otherwise.
# --------------------------------------------------------------------------- #

def _load_pillow(path: Path):
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(path).convert("RGB")
    return im.width, im.height, im.tobytes()


def _load_png_stdlib(path: Path):
    """Decode a non-interlaced PNG to (w, h, [(r,g,b), ...]). Enough for screenshots."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path}: not a PNG, and Pillow is not installed to read it")
    pos, idat, w = 8, b"", None
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        typ = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, colour, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if depth != 8 or interlace or colour not in (2, 6):
                raise SystemExit(f"{path}: unsupported PNG (depth={depth} colour={colour}); install Pillow")
            channels = 3 if colour == 2 else 4
        elif typ == b"IDAT":
            idat += body
        elif typ == b"IEND":
            break
        pos += 12 + ln
    raw = zlib.decompress(idat)
    stride = w * channels
    out, prev = bytearray(), bytearray(stride)
    i = 0
    for _ in range(h):
        f = raw[i]; i += 1
        line = bytearray(raw[i:i + stride]); i += stride
        if f == 1:
            for x in range(channels, stride):
                line[x] = (line[x] + line[x - channels]) & 0xFF
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif f == 3:
            for x in range(stride):
                a = line[x - channels] if x >= channels else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif f == 4:
            for x in range(stride):
                a = line[x - channels] if x >= channels else 0
                c = prev[x - channels] if x >= channels else 0
                b = prev[x]
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        for x in range(0, stride, channels):
            out += bytes((line[x], line[x + 1], line[x + 2]))
        prev = line
    return w, h, bytes(out)


def load(path: Path):
    return _load_pillow(path) or _load_png_stdlib(path)


# --------------------------------------------------------------------------- #
# The four checks.
# --------------------------------------------------------------------------- #

def cell_stats(w, h, px, cols, rows):
    """Per cell: mean luminance and the within-cell luminance RANGE.

    The range is what separates a populated surface from a placeholder. Text puts
    near-black on near-white inside one cell (range -> 1.0). A shimmer block puts
    light grey on white (range -> 0.15). Cross-cell variance cannot tell them
    apart because both are mostly white overall.
    """
    cells = []
    for r in range(rows):
        for c in range(cols):
            x0, x1 = c * w // cols, max((c + 1) * w // cols, c * w // cols + 1)
            y0, y1 = r * h // rows, max((r + 1) * h // rows, r * h // rows + 1)
            lo, hi, tot, n = 1.0, 0.0, 0.0, 0
            ys = max(1, (y1 - y0) // 16)
            xs = max(1, (x1 - x0) // 16)
            for y in range(y0, y1, ys):
                base = y * w
                for x in range(x0, x1, xs):
                    i = (base + x) * 3
                    L = (0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2]) / 255
                    lo = L if L < lo else lo
                    hi = L if L > hi else hi
                    tot += L
                    n += 1
            cells.append({"mean": tot / n if n else 1.0, "range": hi - lo})
    return cells


def analyse(path: Path, cols=16, rows=10):
    w, h, px = load(path)
    cells = cell_stats(w, h, px, cols, rows)
    means = [c["mean"] for c in cells]
    ranges = [c["range"] for c in cells]
    mean = sum(means) / len(means)

    # A cell carrying real content has strong internal contrast.
    contentful = sum(1 for r in ranges if r > 0.45) / len(ranges)
    # A cell carrying a placeholder block has weak but non-zero contrast.
    faint = sum(1 for r in ranges if 0.04 < r <= 0.28) / len(ranges)
    blank = sum(1 for r in ranges if r <= 0.04) / len(ranges)

    return {
        "path": str(path), "width": w, "height": h,
        "aspect": round(w / h, 4) if h else None,
        "meanLuminance": round(mean, 4),
        "contentfulCells": round(contentful, 4),
        "faintCells": round(faint, 4),
        "blankCells": round(blank, 4),
        "cells": cells, "cols": cols, "rows": rows,
    }


def verdicts(a, ref=None):
    out, notes = {}, []

    # Evidence: at least a few cells carry real contrast, and the frame is not
    # almost entirely blank.
    out["isEvidence"] = a["contentfulCells"] >= 0.02 and a["blankCells"] < 0.97
    if not out["isEvidence"]:
        notes.append(
            f"Only {a['contentfulCells']:.1%} of cells carry real contrast and "
            f"{a['blankCells']:.1%} are blank. This is not a picture of a populated surface."
        )

    # Skeleton: lots of faint blocks, almost no real content. Measured against a
    # real shimmer capture, which sat at faint~0.5 / contentful~0.0.
    out["settled"] = not (a["faintCells"] > 0.18 and a["contentfulCells"] < 0.06)
    if not out["settled"]:
        notes.append(
            f"{a['faintCells']:.0%} of cells are faint placeholder blocks and only "
            f"{a['contentfulCells']:.0%} carry real content — the signature of a loading "
            "skeleton. Capture again once the surface settles."
        )

    if ref:
        ar = a["aspect"] / ref["aspect"] if ref["aspect"] else None
        scale = (a["width"] / ref["width"]) if ref["width"] else None
        out["framingComparable"] = bool(ar and 0.8 <= ar <= 1.25)
        out["aspectRatioOfRatios"] = round(ar, 3) if ar else None
        out["scaleRatio"] = round(scale, 3) if scale else None
        if not out["framingComparable"]:
            notes.append(
                f"Framing differs: {a['width']}x{a['height']} vs reference "
                f"{ref['width']}x{ref['height']} (aspect ratio {round(ar, 2)}). "
                "This is a FRAMING difference, not visual drift — re-crop to the same "
                "region before drawing any conclusion about how it looks."
            )
    return out, notes


def tiles(a, k=6):
    """The k cells carrying the most local contrast — where to look first."""
    g = [c["range"] for c in a["cells"]]
    cols, rows, w, h = a["cols"], a["rows"], a["width"], a["height"]
    # Rank by how much real content the cell carries — that is where a defect can
    # actually be seen, and where a model should be pointed first.
    scored = [(v, i % cols, i // cols) for i, v in enumerate(g)]
    scored.sort(reverse=True)
    seen, out = set(), []
    for _, c, r in scored:
        if (c, r) in seen:
            continue
        seen.add((c, r))
        out.append({
            "x": c * w // cols, "y": r * h // rows,
            "w": max(w // cols, 1) * 2, "h": max(h // rows, 1) * 2,
        })
        if len(out) >= k:
            break
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", type=Path)
    ap.add_argument("--reference", type=Path, help="the mock or expected image to compare framing against")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--tiles", type=int, default=6, help="how many inspection tiles to emit")
    args = ap.parse_args()

    a = analyse(args.image)
    ref = analyse(args.reference) if args.reference else None
    v, notes = verdicts(a, ref)
    result = {
        "image": {k: a[k] for k in ("path", "width", "height", "aspect", "meanLuminance",
                                    "contentfulCells", "faintCells", "blankCells")},
        "reference": {k: ref[k] for k in ("path", "width", "height", "aspect")} if ref else None,
        "checks": v,
        "notes": notes,
        "inspectionTiles": tiles(a, args.tiles),
        "proceed": v["isEvidence"] and v["settled"],
    }

    if args.json:
        print(json.dumps(result, indent=1))
    else:
        print(f"{args.image}  {a['width']}x{a['height']}  content={a['contentfulCells']:.1%} "
              f"faint={a['faintCells']:.1%} blank={a['blankCells']:.1%}")
        for k, val in v.items():
            print(f"  {k}: {val}")
        for n in notes:
            print(f"  ! {n}")
        print(f"  proceed: {result['proceed']}")
        for t in result["inspectionTiles"]:
            print(f"  tile: {t['x']},{t['y']},{t['w']},{t['h']}")

    # Exit 2 means "do not judge this image" — a suite can branch on it.
    sys.exit(0 if result["proceed"] else 2)


if __name__ == "__main__":
    main()
