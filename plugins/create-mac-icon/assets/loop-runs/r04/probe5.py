#!/usr/bin/env python3
"""r04 probe 5: the recess's interior crevice, and the near-lip inner edge.

Vertical profiles crossing the cavity's far wall into its floor, on the right
half where the cast occludes neither image.
"""
import numpy as np
from PIL import Image

BASE = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/"


def load(p):
    return np.asarray(Image.open(BASE + p).convert("RGB")).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


ref, cand = load("reference-1024.png"), load("candidate-1024.png")
Lr, Lc = lum(ref), lum(cand)

print("== reference: down through the far lip into the cavity floor ==")
for x in (560, 600, 640):
    print(f"  x={x}: " + " ".join(f"{y}:{Lr[y,x]:.3f}" for y in range(470, 620, 6)))
print()
print("== candidate: same, its own cavity ==")
for x in (560, 600, 640):
    print(f"  x={x}: " + " ".join(f"{y}:{Lc[y,x]:.3f}" for y in range(400, 550, 6)))

print()
print("== reference: right-hand inner wall, horizontal into the floor ==")
for y in (600, 640, 680):
    print(f"  y={y}: " + " ".join(f"{x}:{Lr[y,x]:.3f}" for x in range(660, 780, 5)))
print()
print("== candidate: same ==")
for y in (540, 580, 620):
    print(f"  y={y}: " + " ".join(f"{x}:{Lc[y,x]:.3f}" for x in range(660, 780, 5)))

print()
print("== reference: near lip, floor -> lip crest -> top face (x=560) ==")
print("  " + " ".join(f"{y}:{Lr[y,560]:.3f}" for y in range(690, 800, 4)))
print("== candidate: same (x=560) ==")
print("  " + " ".join(f"{y}:{Lc[y,560]:.3f}" for y in range(620, 730, 4)))
