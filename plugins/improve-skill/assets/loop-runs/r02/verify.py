#!/usr/bin/env python3
"""Re-measure the SAME clean patches used to set the targets, on the rebuilt icon,
against the reference. Patches were chosen (an3.py) to hold only field - no block edge,
no hone spill, no squircle corner - because the whole-field figure is dominated by those."""
import pathlib
import numpy as np
from PIL import Image, ImageFilter

A = pathlib.Path(__file__).resolve().parents[2]
REF = A / "icon-engineC-f5665d-2.png"
CAND = A / "icon.png"

# (label, x, y, size, target hp sd measured off C2 in the same patch)
PATCHES = [
    ("rough near key", 120, 150, 150),
    ("rough mid",      250, 300, 150),
    ("rough at cut",   430, 470, 120),
    ("trued below cut",320, 720, 150),
    ("trued far",      700, 850, 150),
    ("block face",     560, 560, 110),
    ("curl",           240, 300, 90),
]


def stats(png, box):
    im = Image.open(png).convert("L").resize((1024, 1024))
    g = np.asarray(im, float)
    h = g - np.asarray(im.filter(ImageFilter.GaussianBlur(6)), float)
    x, y, n = box
    p = g[y:y + n, x:x + n]
    gy, gx = np.gradient(p)
    return h[y:y + n, x:x + n].std(), (np.hypot(gx, gy) > 4).mean(), p.mean()


print(f"{'patch':>16s} | {'ref hp':>6s} {'cnd hp':>6s} | {'ref e>4':>7s} {'cnd e>4':>7s} | "
      f"{'ref L':>6s} {'cnd L':>6s}")
for label, x, y, n in PATCHES:
    r = stats(REF, (x, y, n))
    c = stats(CAND, (x, y, n))
    print(f"{label:>16s} | {r[0]:6.2f} {c[0]:6.2f} | {r[1]:7.3f} {c[1]:7.3f} | "
          f"{r[2]:6.1f} {c[2]:6.1f}")
