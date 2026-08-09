#!/usr/bin/env python3
"""r04 probe 2: locate the plaster block's edges in both images, fine profiles."""
import numpy as np
from PIL import Image

BASE = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/"


def load(p):
    return np.asarray(Image.open(BASE + p).convert("RGB")).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


ref, cand = load("reference-1024.png"), load("candidate-1024.png")
Lr, Lc = lum(ref), lum(cand)

print("== fine vertical profile at x=512, ref, y 780..930 ==")
print("  " + " ".join(f"{y}:{Lr[y,512]:.3f}" for y in range(780, 935, 5)))
print("== fine vertical profile at x=512, cand, y 700..870 ==")
print("  " + " ".join(f"{y}:{Lc[y,512]:.3f}" for y in range(700, 875, 5)))

print()
print("== horizontal profile through block left edge ==")
print("  ref y=700:  " + " ".join(f"{x}:{Lr[700,x]:.3f}" for x in range(140, 260, 5)))
print("  cand y=650: " + " ".join(f"{x}:{Lc[650,x]:.3f}" for x in range(160, 280, 5)))

print()
print("== horizontal profile through block right edge ==")
print("  ref y=760:  " + " ".join(f"{x}:{Lr[760,x]:.3f}" for x in range(780, 900, 5)))
print("  cand y=700: " + " ".join(f"{x}:{Lc[700,x]:.3f}" for x in range(800, 920, 5)))

print()
print("== block bottom-right corner region: ref, diagonal ==")
for y in range(840, 930, 10):
    print(f"  y={y}: " + " ".join(f"{x}:{Lr[y,x]:.3f}" for x in range(600, 860, 20)))
