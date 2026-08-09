#!/usr/bin/env python3
"""The 12 worst changed pixels above the ground band, with their coordinates and
the actual colour before and after, so the leaking layer can be named."""
import numpy as np
from PIL import Image

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/candidate-1024.png"
B = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/cand-test.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    return rgb * al + (128 / 255.0) * (1 - al)


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


ia, ib = load(A), load(B)
d = lum(ib) - lum(ia)
d[592:] = 0
d[:456] = 0
idx = np.dstack(np.unravel_index(np.argsort(d, axis=None)[:12], d.shape))[0]
for y, x in idx:
    print(f"  ({x:4d},{y:4d})  {d[y,x]:+.4f}   before rgb "
          f"{'/'.join(f'{v:.3f}' for v in ia[y,x])}   after {'/'.join(f'{v:.3f}' for v in ib[y,x])}")
