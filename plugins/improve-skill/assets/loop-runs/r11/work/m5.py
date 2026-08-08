#!/usr/bin/env python3
"""Did the authored lobe land where the reference's lobe is?

Re-runs m3/m4's statistics on an arbitrary render so the built file can be
checked against the numbers it was authored from, rather than against the
composite. Targets, measured off C2 in m3/m4:

    un-planed   peak/mean 2.18   peak/cross 3.48   sd 0.0223   centre ~40 deg
    trued       peak/mean 1.15   peak/cross 1.25   sd 0.0086
"""
import math
import sys

import numpy as np

sys.path.insert(0, "loop-runs/r11/work")
from m1 import load, boxblur, yy, xx  # noqa: E402
from m3 import dilate, patch_stats  # noqa: E402

W, P, STEP = 1024, 96, 32
SRC = sys.argv[1] if len(sys.argv) > 1 else "loop-runs/r11/candidate-1024.png"


def stats(g, m, name):
    hp = g - boxblur(g, 12)
    rows, pool = [], np.zeros(36)
    for y0 in range(34, W - P, STEP):
        for x0 in range(34, W - P, STEP):
            if m[y0:y0 + P, x0:x0 + P].mean() < 0.999:
                continue
            sd, pk, cr, h = patch_stats(hp, y0, x0)
            pool += h
            rows.append(sd)
    if not rows:
        print(f"  {name}: no clean windows")
        return
    pool /= pool.sum()
    pk = int(np.argmax(pool))
    print(f"  {name:9s} n={len(rows):3d}  sd={np.mean(rows):.4f}  "
          f"centre={pk * 5 + 2.5:5.1f}  peak/mean={pool[pk] / pool.mean():.2f}  "
          f"peak/cross={pool[pk] / pool[(pk + 18) % 36]:.2f}")
    top = np.argsort(pool)[::-1][:5]
    print("             top bins " + ", ".join(f"{int(i) * 5}:{pool[i] * 100:.1f}%" for i in top))


g = load(SRC)
a = math.radians(33.0)
nx, ny = math.sin(a), math.cos(a)
sd_ = (xx - 543.0) * nx + (yy - 604.0) * ny
block = dilate(g < 0.15, 14)
curl = dilate((xx > 130) & (xx < 450) & (yy > 155) & (yy < 430), 4)
tile = (xx > 34) & (xx < W - 34) & (yy > 34) & (yy < W - 34)
print(f"== {SRC}")
stats(g, (sd_ < -34) & tile & ~block & ~curl, "un-planed")
stats(g, (sd_ > 40) & tile & ~block, "trued")
print("   targets  un-planed sd 0.0223 centre ~40 peak/mean 2.18 peak/cross 3.48")
print("             trued    sd 0.0086            peak/mean 1.15 peak/cross 1.25")
