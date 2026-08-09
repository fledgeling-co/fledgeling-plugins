#!/usr/bin/env python3
"""r04 measurement probe: read numbers off the reference and the candidate."""
import sys
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/reference-1024.png"
C = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/candidate-1024.png"


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def sat(a):
    mx = a.max(-1); mn = a.min(-1)
    return np.where(mx > 1e-9, (mx - mn) / np.maximum(mx, 1e-9), 0.0)


ref, cand = load(R), load(C)
Lr, Lc = lum(ref), lum(cand)
Sr, Sc = sat(ref), sat(cand)

print("== background sample ==")
for name, a, L in (("ref", ref, Lr), ("cand", cand, Lc)):
    print(f"  {name}: c(5,5)={a[5,5].round(4)} L={L[5,5]:.4f} "
          f"top-mid L={L[5,512]:.4f} left-mid L={L[512,5]:.4f} "
          f"bot-mid L={L[1018,512]:.4f}")

print()
print("== vertical scan x=512, every 8px, L ==")
for name, L in (("ref", Lr), ("cand", Lc)):
    row = " ".join(f"{y}:{L[y,512]:.3f}" for y in range(300, 1000, 25))
    print(f"  {name} {row}")
