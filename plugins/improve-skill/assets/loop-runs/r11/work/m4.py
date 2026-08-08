#!/usr/bin/env python3
"""The TRUED plane's texture: how much, and on what bearing, in each image.

The un-planed side is measured in m3. This asks the same of the finished side,
because the edge maps show the master's lattice running right across it while
the reference's trued plane looks swept clean. If that holds numerically it is
a second, independent reason the cross-hatch is wrong: it is drawing structure
into a region where the reference has none, which costs SSIM covariance rather
than earning it.
"""
import math
import sys

import numpy as np

sys.path.insert(0, "loop-runs/r11/work")
from m1 import load, boxblur, yy, xx  # noqa: E402
from m3 import dilate, patch_stats  # noqa: E402

W, P, STEP = 1024, 96, 32


def trued(kind):
    if kind == "ref":
        g = load("loop-runs/r10-reverted/reference-1024.png")
        side = yy > (-0.8026 * xx + 991.2 + 40)
    else:
        g = load("loop-runs/r10-reverted/candidate-1024.png")
        a = math.radians(33.0)
        nx, ny = math.sin(a), math.cos(a)
        side = ((xx - 543.0) * nx + (yy - 604.0) * ny) > 40
    block = dilate(g < 0.15, 14)
    tile = (xx > 34) & (xx < W - 34) & (yy > 34) & (yy < W - 34)
    return g, side & tile & ~block


for kind in ("ref", "cand"):
    g, m = trued(kind)
    hp = g - boxblur(g, 12)
    rows, pool = [], np.zeros(36)
    for y0 in range(34, W - P, STEP):
        for x0 in range(34, W - P, STEP):
            if m[y0:y0 + P, x0:x0 + P].mean() < 0.999:
                continue
            sd, pk, cr, h = patch_stats(hp, y0, x0)
            pool += h
            rows.append((sd, pk, cr))
    sds = np.array([r[0] for r in rows])
    pool /= pool.sum()
    pk = int(np.argmax(pool))
    print(f"\n== {kind.upper()} TRUED  n={len(rows)} windows  "
          f"sd mean={sds.mean():.4f} max={sds.max():.4f}")
    print(f"   dominant bearing {pk * 5 + 2.5:.1f}  peak/cross "
          f"{pool[pk] / pool[(pk + 18) % 36]:.2f}  peak/mean {pool[pk] / pool.mean():.2f}")
    top = np.argsort(pool)[::-1][:6]
    print("   top bins: " + ", ".join(f"{int(i) * 5}-{int(i) * 5 + 5}:{pool[i] * 100:.1f}%"
                                      for i in top))
