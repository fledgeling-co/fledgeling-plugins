#!/usr/bin/env python3
"""r02 analysis: where is the gap, and what is its texture statistic."""
import numpy as np
from PIL import Image, ImageFilter
import math, sys

def lin(a):
    a = a / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)

def Lm(img):
    a = np.asarray(img.convert("RGB"), dtype=np.float64)
    y = 0.2126 * lin(a[..., 0]) + 0.7152 * lin(a[..., 1]) + 0.0722 * lin(a[..., 2])
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100, 903.3 * y / 100)

D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/"
ref = Image.open(D + "loop-runs/r01/reference-1024.png").convert("RGB").resize((1024, 1024), Image.LANCZOS)
cnd = Image.open(D + "loop-runs/r01/candidate-1024.png").convert("RGB").resize((1024, 1024), Image.LANCZOS)
Lr, Lc = Lm(ref), Lm(cnd)

res = np.abs(Lr - Lc)
b = res.reshape(16, 64, 16, 64).mean(axis=(1, 3))
order = np.dstack(np.unravel_index(np.argsort(-b.ravel()), b.shape))[0]
print("worst 64px tiles (top 14):")
for r, c in order[:14]:
    print(f"   x={c*64:4d} y={r*64:4d}  resid {b[r,c]:.3f}")
print("mean |dL| overall %.4f\n" % res.mean())

# high-frequency texture energy: L minus a 6px gaussian blur, per region
def hp(im, rad=6.0):
    g = np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(rad)), dtype=np.float64)
    return np.asarray(im.convert("L"), dtype=np.float64) - g

hr, hc = hp(ref), hp(cnd)

# region masks in canvas coords
ys, xs = np.mgrid[0:1024, 0:1024]
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
EDGE = (543.0, 604.0)
AX = EDGE[0] - UX * 320
AY = EDGE[1] - UY * 320
ly = NX * (xs - AX) + NY * (ys - AY)     # >0 un-planed, <0 trued
lx = UX * (xs - AX) + UY * (ys - AY)

blockish = (Lc < 0.45)                    # master's dark block
refblock = (Lr < 0.45)
ground_un = (ly > 80) & ~blockish & ~refblock
ground_tr = (ly < -80) & ~blockish & ~refblock
inside = (Lc > 0.02) | (Lr > 0.02)

def stat(name, m):
    print(f"{name:22s} n={m.sum():7d}  ref hp sd {hr[m].std():6.2f}  cand hp sd {hc[m].std():6.2f}"
          f"   ref L {Lr[m].mean():.3f}  cand L {Lc[m].mean():.3f}")

print("high-pass texture energy (8-bit units, sd of L - blur6):")
stat("un-planed ground", ground_un)
stat("trued ground", ground_tr)
stat("block (both dark)", blockish & refblock)
print()

# un-planed ground split by distance from the light (TL corner)
for lo, hi, lbl in [(80, 250, "un-planed near band"), (250, 450, "un-planed mid band"), (450, 900, "un-planed far band")]:
    m = ground_un & (ly > lo) & (ly <= hi)
    stat(lbl, m)
print()
# along-travel bands
for lo, hi, lbl in [(-600, -200, "un-pl behind blade"), (-200, 200, "un-pl beside blade"), (200, 700, "un-pl ahead blade")]:
    m = ground_un & (lx > lo) & (lx <= hi)
    stat(lbl, m)
