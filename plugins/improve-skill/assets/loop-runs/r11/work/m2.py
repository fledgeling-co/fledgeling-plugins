#!/usr/bin/env python3
"""Per-patch texture: where the reference's tear lives, and on what bearing.

m1 pooled the whole un-planed plane, which mixes clean field with the boundary
edge. This slides a window, keeps only windows that are 100% un-planed ground
and 0% block/curl, and reports each window's texture sd, dominant ridge
bearing and anisotropy. Two questions at once:

  1. how many bearings (one lobe or two, 90 apart)
  2. how the tear's ENERGY is distributed in space - the reference's edge map
     says it is dense near the boundary and absent near the key, which the
     master does not do.

Anisotropy here is peak-bin energy / opposite-bin energy at +-90 deg, which is
the statistic that separates "one bearing" from "a cross". The doubled-angle
coherence used in m1 cannot: a 90-deg cross cancels in it exactly.
"""
import math

import numpy as np
from PIL import Image

W, P = 1024, 160

import sys
sys.path.insert(0, "loop-runs/r11/work")
from m1 import load, boxblur, yy, xx  # noqa: E402


def region(kind):
    if kind == "ref":
        rough = yy < (-0.8026 * xx + 991.2)
        block = (xx > 190) & (xx < 830) & (yy > 120) & (yy < 720)
        curl = (xx > 150) & (xx < 500) & (yy > 40) & (yy < 420)
        src, ang = "loop-runs/r10-reverted/reference-1024.png", 38.75
    else:
        a = math.radians(33.0)
        nx, ny = math.sin(a), math.cos(a)
        rough = ((xx - 543.0) * nx + (yy - 604.0) * ny) < 0
        block = (xx > 150) & (xx < 840) & (yy > 120) & (yy < 800)
        curl = (xx > 120) & (xx < 460) & (yy > 140) & (yy < 440)
        src, ang = "loop-runs/r10-reverted/candidate-1024.png", 33.0
    tile = (xx > 40) & (xx < W - 40) & (yy > 40) & (yy < W - 40)
    return load(src), rough & tile & ~block & ~curl, ang


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
    cross = h[(pk + nb // 2) % nb]
    return b.std(), pk * 5 + 2.5, h[pk] / max(cross, 1e-9), h[pk] / h.mean()


for kind in ("ref", "cand"):
    g, m, ang = region(kind)
    hp = g - boxblur(g, 12)
    rows = []
    for y0 in range(40, W - P, 80):
        for x0 in range(40, W - P, 80):
            if not m[y0:y0 + P, x0:x0 + P].all():
                continue
            sd, pk, cr, pr = patch_stats(hp, y0, x0)
            # distance from the fitted key, the coordinate r08 showed the field runs on
            r = math.hypot(x0 + P / 2 - 75.0, y0 + P / 2 - 25.0)
            rows.append((r, x0, y0, sd, pk, cr, pr))
    rows.sort()
    print(f"\n===== {kind.upper()}  hone {ang} deg   {len(rows)} clean windows")
    print("    r   x0   y0   sd      bearing  peak/cross  peak/mean")
    for r, x0, y0, sd, pk, cr, pr in rows:
        print(f"  {r:4.0f} {x0:4d} {y0:4d}  {sd:.4f}   {pk:5.1f}    {cr:6.2f}     {pr:5.2f}")
    sds = np.array([x[3] for x in rows])
    rr = np.array([x[0] for x in rows])
    print(f"  -- sd near key (r<400): {sds[rr < 400].mean():.4f}   "
          f"far (r>700): {sds[rr > 700].mean():.4f}   "
          f"ratio far/near {sds[rr > 700].mean() / sds[rr < 400].mean():.2f}")
    print(f"  -- median peak/cross {np.median([x[5] for x in rows]):.2f}")
