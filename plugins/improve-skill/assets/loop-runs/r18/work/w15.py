"""Solve OUT_LIT against the measured relationship, then read the score once.

The relationship (w14): inside the curl's own footprint, ours sits p90 +0.1700 and p99 +0.2468
above the board immediately around it; the reference sits +0.1165 and +0.1685. Both ratios are
0.68. So the outer face's excess over its board is to be scaled by 0.68 - and the constant is
solved against THAT number by rebuilding and re-measuring, not chosen off a score sweep.
"""
import subprocess
import tempfile
import pathlib
import re
import os
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r18/work")
SRC = pathlib.Path("build_icon.py").read_text()
REF = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def native(svg, size):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, size))
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


def dil(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def grow(m, px, step=5):
    out = m.copy()
    for _ in range(px // step):
        out = dil(out, step)
    return out


def build(name, trip):
    src, n = re.subn(r"OUT_LIT   = \(243, 234, 216\)",
                     "OUT_LIT   = (%d, %d, %d)" % trip, SRC, count=1)
    assert n == 1
    src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
                      "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
    p = WORK / ("gen_%s.py" % name)
    p.write_text(src)
    subprocess.run(["python3", str(p)], check=True, capture_output=True, cwd=".")
    out = WORK / ("var_%s.svg" % name)
    out.write_bytes(pathlib.Path("icon.svg").read_bytes())
    return out


g_off = gray(native(str(WORK / "var_noshaving.svg"), 1024))
g_on = gray(native("icon.svg", 1024))
g_ref = gray(REF.resize((1024, 1024), Image.LANCZOS))
M = np.abs(g_on - g_off) > 0.02
ring = grow(M, 40) & ~grow(M, 10)
ref_base = np.median(g_ref[ring])
TARGET90 = np.percentile(g_ref[M], 90) - ref_base
TARGET99 = np.percentile(g_ref[M], 99) - ref_base
print("reference target excess over its board: p90 %+.4f  p99 %+.4f" % (TARGET90, TARGET99))

for tag, trip in (("base", None), ("fit888", (216, 208, 192)), ("fit86", (209, 201, 186)),
                  ("fit91", (221, 213, 197))):
    svg = "icon.svg" if trip is None else str(build(tag, trip))
    g = gray(native(svg, 1024))
    b = np.median(g[ring])
    print("  %-8s board %.4f   excess p90 %+.4f  p99 %+.4f   (target %+.4f / %+.4f)"
          % (tag, b, np.percentile(g[M], 90) - b, np.percentile(g[M], 99) - b, TARGET90, TARGET99))

subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)
