#!/usr/bin/env python3
"""How much of the change above the ground band survives the notCav clip?"""
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
for name, sl in (("above the ground band  y456..591", (slice(456, 592), slice(0, 1024))),
                 ("the ground band        y592..820", (slice(592, 821), slice(0, 1024)))):
    d = dif[sl]
    m = np.abs(d) > 0.004
    print(f"  {name}:  n={m.sum():6d}  mean {d[m].mean():+.4f}  "
          f"worst {d[m][np.argmax(np.abs(d[m]))]:+.4f}  "
          f"|d|>0.02: {(np.abs(d) > 0.02).sum()}")
