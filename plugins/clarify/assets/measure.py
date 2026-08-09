#!/usr/bin/env python3
"""Measure the fidelity reference so rounds are fitted rather than guessed.

Every entry in the skill's material-recipes library that cost rounds came from
assuming a relationship instead of sampling it, so this reads numbers off the
raster: card silhouettes, per-face luminance, edge-roll profiles, the accent's
ramp and rim, and the shadow falloff.

    python3 measure.py [reference.png] [probe ...]
"""
import sys

import numpy as np
from PIL import Image

REF = sys.argv[1] if len(sys.argv) > 1 else "icon-engineC-4c230c-2-masked.png"
PROBES = sys.argv[2:] or ["boxes", "profile", "accent", "shadow"]

im = Image.open(REF).convert("RGBA")
if im.size != (1024, 1024):
    im = im.resize((1024, 1024), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
bg.alpha_composite(im)
a = np.asarray(bg.convert("RGB")).astype(np.float32) / 255
lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
mx, mn = a.max(2), a.min(2)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)


def hx(p):
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in p)


if "boxes" in PROBES:
    print("== ground and card structure")
    for t in np.linspace(0.08, 0.92, 8):
        x, y = int(1024 * (0.06 + 0.88 * t)), int(1024 * (0.06 + 0.88 * t))
        print(f"  tile diagonal t={t:.2f} ({x},{y}) {hx(a[y, x])} L={lum[y, x]:.3f}")
    print("  column scans (x fixed, listing runs darker than the local ground):")
    for x in (300, 512, 700):
        col = lum[:, x]
        edges = np.nonzero(np.abs(np.diff(col)) > 0.012)[0]
        print(f"   x={x}: {len(edges)} steps at y={list(edges[:24])}")

if "profile" in PROBES:
    print("== perpendicular luminance profiles across a card's lower arris")
    for x in (360, 520):
        col = lum[:, x]
        # the strongest downward step in the upper half is a face->wall arris
        d = np.diff(col)
        y = int(np.argmin(d[200:560])) + 200
        print(f"  x={x} steepest fall at y={y}:")
        for dy in range(-18, 31, 3):
            print(f"    dy={dy:+3d} y={y + dy} {hx(a[y + dy, x])} L={lum[y + dy, x]:.3f}")

if "accent" in PROBES:
    print("== the accent")
    m = (sat > 0.40) & (a[..., 0] > a[..., 2])
    ys, xs = np.nonzero(m)
    print(f"  accent px {m.sum()} ({100 * m.sum() / 1024 ** 2:.2f}% of tile) "
          f"bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}")
    # split dot (left cluster) from note (right cluster)
    split = (xs.min() + xs.max()) / 2
    for name, sel in (("dot", xs < split), ("note", xs >= split)):
        sx, sy = xs[sel], ys[sel]
        if len(sx) < 20:
            continue
        px = a[sy, sx]
        lp = 0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]
        k = np.argsort(lp)
        print(f"  {name}: bbox x {sx.min()}-{sx.max()} y {sy.min()}-{sy.max()} "
              f"n={len(sx)} L {lp.min():.3f}..{lp.max():.3f}")
        for label, idx in (("darkest 2%", k[:max(1, len(k) // 50)]),
                           ("median", k[len(k) // 2:len(k) // 2 + max(1, len(k) // 50)]),
                           ("brightest 2%", k[-max(1, len(k) // 50):])):
            p = px[idx].mean(0)
            s = (p.max() - p.min()) / max(p.max(), 1e-6)
            print(f"    {label:12s} {hx(p)} L={lp[idx].mean():.3f} S={s:.3f}")

if "shadow" in PROBES:
    print("== shadow falloff below the lowest card")
    m = lum < 0.86
    ys, xs = np.nonzero(m)
    yb = int(np.percentile(ys, 99.5))
    x = int(np.median(xs))
    for dy in range(-10, 46, 4):
        y = min(1023, yb + dy)
        print(f"  x={x} y={y} {hx(a[y, x])} L={lum[y, x]:.3f}")
