#!/usr/bin/env python3
"""Measure the two-state split polarity on a rendered 1024 icon.

The concept requires the TRUED side (already planed, local y < 0, canvas
down-right) to read brighter than the UN-PLANED side. This samples ground
pixels only - the dark block is excluded by luminance - and reports mean
perceptual L on each side of the diagonal.
"""
import math
import sys
from PIL import Image

W = 1024
ANGLE = math.radians(float(sys.argv[2])) if len(sys.argv) > 2 else math.radians(33.0)
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)
# origin: leading end of the cutting edge (matches build_icon.py)
EDGE_MID = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (552.0, 560.0)
BLADE_LEN = float(sys.argv[5]) if len(sys.argv) > 5 else 640.0
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lstar(r, g, b):
    y = 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)
    return (116 * (y ** (1 / 3)) - 16) / 100 if y > 0.008856 else (903.3 * y) / 100


img = Image.open(sys.argv[1]).convert("RGB").resize((W, W), Image.LANCZOS)
px = img.load()

rough, trued, rough_all, trued_all = [], [], [], []
for y in range(0, W, 2):
    for x in range(0, W, 2):
        r, g, b = px[x, y]
        dx, dy = x - AX, y - AY
        ly = NX * dx + NY * dy
        if abs(ly) < 60:            # skip the boundary transition band
            continue
        L = lstar(r, g, b)
        if ly > 0:
            rough_all.append(L)
            if L > 0.50:            # ground, not the block or its core shadow
                rough.append(L)
        else:
            trued_all.append(L)
            if L > 0.50:
                trued.append(L)


def m(v):
    return sum(v) / len(v) if v else float("nan")


gr, gt = m(rough), m(trued)
print(f"{sys.argv[1]}")
print(f"  ground only : un-planed L {gr:.3f}   trued L {gt:.3f}   delta {gt - gr:+.3f}"
      f"   -> {'OK trued brighter' if gt > gr else 'INVERTED'}")
print(f"  all pixels  : un-planed L {m(rough_all):.3f}   trued L {m(trued_all):.3f}")
