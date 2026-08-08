#!/usr/bin/env python3
"""Per-patch texture of the un-planed ground: bearing count and spatial energy.

Same question as m2, but the block and curl are DETECTED and dilated rather
than boxed by eye, so the clean field that survives is as large as it really is.

Anisotropy = peak-bin energy / the bin 90 deg from it. One bearing gives a big
number; a cross-hatch gives ~1 by construction. This is the statistic the
master's `grain()` docstring claims is 3.0 on the reference - tested here.
"""
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "loop-runs/r11/work")
from m1 import load, boxblur, yy, xx  # noqa: E402

W, P, STEP = 1024, 96, 32


def dilate(m, r):
    for _ in range(r):
        m = (m | np.roll(m, 1, 0) | np.roll(m, -1, 0)
             | np.roll(m, 1, 1) | np.roll(m, -1, 1))
    return m


def region(kind):
    if kind == "ref":
        g = load("loop-runs/r10-reverted/reference-1024.png")
        rough = yy < (-0.8026 * xx + 991.2 - 34)          # 34px clear of the hone
        block = dilate(g < 0.15, 14)
        curl = dilate((g > 0.60) & (xx < 540) & (yy < 460) & (xx > 130), 14)
        ang = 38.75
    else:
        g = load("loop-runs/r10-reverted/candidate-1024.png")
        a = math.radians(33.0)
        nx, ny = math.sin(a), math.cos(a)
        rough = ((xx - 543.0) * nx + (yy - 604.0) * ny) < -34
        block = dilate(g < 0.15, 14)
        curl = dilate((xx > 130) & (xx < 450) & (yy > 155) & (yy < 430), 4)
        ang = 33.0
    tile = (xx > 34) & (xx < W - 34) & (yy > 34) & (yy < W - 34)
    return g, rough & tile & ~block & ~curl, ang


def patch_stats(hp, y0, x0):
    b = hp[y0:y0 + P, x0:x0 + P]
    gx = np.zeros_like(b)
    gy = np.zeros_like(b)
    gx[:, 1:-1] = (b[:, 2:] - b[:, :-2]) * 0.5
    gy[1:-1, :] = (b[2:, :] - b[:-2, :]) * 0.5
    gx, gy = gx[2:-2, 2:-2], gy[2:-2, 2:-2]
    mag = gx * gx + gy * gy
    th = (np.degrees(np.arctan2(gy, gx)) + 90.0) % 180.0
    nb = 36
    h = np.zeros(nb)
    np.add.at(h, np.clip((th / 180.0 * nb).astype(int), 0, nb - 1), mag)
    h /= h.sum()
    pk = int(np.argmax(h))
    return b.std(), pk * 5 + 2.5, h[pk] / max(h[(pk + nb // 2) % nb], 1e-9), h


for kind in ("ref", "cand"):
    g, m, ang = region(kind)
    hp = g - boxblur(g, 12)
    rows, pool = [], np.zeros(36)
    for y0 in range(34, W - P, STEP):
        for x0 in range(34, W - P, STEP):
            if m[y0:y0 + P, x0:x0 + P].mean() < 0.999:
                continue
            sd, pk, cr, h = patch_stats(hp, y0, x0)
            pool += h
            r = math.hypot(x0 + P / 2 - 75.0, y0 + P / 2 - 25.0)
            rows.append((r, sd, pk, cr))
    rows.sort()
    sds = np.array([x[1] for x in rows])
    rr = np.array([x[0] for x in rows])
    crs = np.array([x[3] for x in rows])
    pool /= pool.sum()
    pk = int(np.argmax(pool))
    print(f"\n===== {kind.upper()}  hone {ang} deg   {len(rows)} clean {P}px windows")
    print("   sd by distance from the key (r):")
    for lo, hi in ((0, 300), (300, 450), (450, 600), (600, 750), (750, 1100)):
        s = (rr >= lo) & (rr < hi)
        if s.any():
            print(f"     r {lo:4d}-{hi:4d}  n={s.sum():3d}  sd={sds[s].mean():.4f}"
                  f"   peak/cross={crs[s].mean():5.2f}"
                  f"   bearings={sorted(set(int(x[2]) for x in rows if lo <= x[0] < hi))}")
    print(f"   POOLED dominant bearing {pk * 5 + 2.5:.1f} deg,"
          f"  peak/cross {pool[pk] / pool[(pk + 18) % 36]:.2f},"
          f"  peak/mean {pool[pk] / pool.mean():.2f}")
    print("   pooled histogram (5 deg bins):")
    for i in range(36):
        print(f"     {i * 5:3d} {pool[i] * 100:5.2f}% {'#' * int(round(pool[i] * 500))}")
