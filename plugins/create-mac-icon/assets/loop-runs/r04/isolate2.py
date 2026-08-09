#!/usr/bin/env python3
"""Where exactly are the few changed pixels above the contact ring?"""
import numpy as np
from PIL import Image

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/candidate-1024.png"
B = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/cand-test.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (128 / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


dif = load(B) - load(A)
m = np.abs(dif) > 0.004
for y0 in range(456, 600, 12):
    sub = m[y0:y0 + 12]
    if not sub.any():
        continue
    xs = np.nonzero(sub.any(0))[0]
    print(f"  y {y0}..{y0+11}: x runs " +
          ", ".join(f"{g[0]}..{g[-1]}" for g in np.split(xs, np.nonzero(np.diff(xs) > 3)[0] + 1)))
