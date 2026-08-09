#!/usr/bin/env python3
"""r04 isolate: what actually changed between the r03 baseline render and this
one. If the crevice leaked onto a surface it should not touch, it shows here."""
import numpy as np
from PIL import Image

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/candidate-1024.png"
B = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/cand-test.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (128 / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


a, b = load(A), load(B)
dif = b - a
m = np.abs(dif) > 0.004
ys, xs = np.nonzero(m)
print(f"changed pixels: {m.sum()} ({m.mean()*100:.2f}% of the canvas)")
print(f"bbox  x {xs.min()}..{xs.max()}   y {ys.min()}..{ys.max()}")
print(f"delta  min {dif.min():+.4f}  max {dif.max():+.4f}  mean over changed {dif[m].mean():+.4f}")
print(f"pixels lighter than baseline: {(dif > 0.004).sum()}   darker: {(dif < -0.004).sum()}")
print()
print("== rows with any change, 8px bands ==")
for y0 in range(0, 1024, 8):
    band = m[y0:y0 + 8]
    if band.any():
        d = dif[y0:y0 + 8][band]
        print(f"  y {y0:4d}..{y0+7:4d}  n={band.sum():6d}  mean {d.mean():+.4f}  "
              f"worst {d[np.argmax(np.abs(d))]:+.4f}")
