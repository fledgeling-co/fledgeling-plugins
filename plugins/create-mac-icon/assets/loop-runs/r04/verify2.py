#!/usr/bin/env python3
"""r04 verify 2: the ground arris, with the silhouette located by the steepest
downward gradient in the column (within 1-2px in both images) rather than by a
threshold walk, which was landing inside the crevice and inflating the roll.
"""
import sys
import numpy as np
from PIL import Image

REF = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/reference-1024.png"
CAND = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/cand-test.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    return rgb * al + (128 / 255.0) * (1 - al)


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


OFFS = (-34, -26, -18, -12, -8, -4, 0, 2, 5, 9, 14, 20, 28, 40)


def profile(L, y0, y1, label):
    acc = []
    for x in range(320, 741, 20):
        col = L[:, x]
        g = col[y0:y1] - np.roll(col[y0:y1], 3)          # downward fall over 3px
        e = y0 + int(np.argmin(g)) - 2                   # the last wall row
        acc.append([col[e + k] for k in OFFS])
    a = np.array(acc)
    print(f"  {label:10s} " + " ".join(f"{k:+d}:{v:.3f}" for k, v in zip(OFFS, a.mean(0))))
    return a.mean(0)


ref, cand = lum(load(REF)), lum(load(CAND))
print("== L at signed offsets from the block's ground silhouette (mean of 22 columns) ==")
r = profile(ref, 850, 950, "reference")
c = profile(cand, 700, 850, "candidate")
print()
print("== the same, each normalised to its own wall at -34px (the shapes only) ==")
print("  reference  " + " ".join(f"{k:+d}:{v - r[0]:+.3f}" for k, v in zip(OFFS, r)))
print("  candidate  " + " ".join(f"{k:+d}:{v - c[0]:+.3f}" for k, v in zip(OFFS, c)))
print()
print(f"  roll loss into the arris (-34 -> -4):  reference {r[5]-r[0]:+.3f}   "
      f"candidate {c[5]-c[0]:+.3f}")
print(f"  crevice depth below that wall:         reference {r[7]-r[0]:+.3f}   "
      f"candidate {c[7]-c[0]:+.3f}")
