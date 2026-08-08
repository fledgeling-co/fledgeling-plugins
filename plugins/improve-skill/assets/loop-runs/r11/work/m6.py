#!/usr/bin/env python3
"""Rubric-side checks the gate does not make: figure-ground at 128, the 16px
read, and the single-light corner ordering. Run on the pre-edit and post-edit
SVGs so the round can say what it cost as well as what it scored.
"""
import math
import subprocess
import sys

import numpy as np
from PIL import Image


def srgb_to_lin(a):
    a = a / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def lstar(rgb):
    y = (0.2126 * srgb_to_lin(rgb[..., 0]) + 0.7152 * srgb_to_lin(rgb[..., 1])
         + 0.0722 * srgb_to_lin(rgb[..., 2]))
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100, 903.3 * y / 100)


def render(svg, n):
    out = f"/tmp/_fg{n}.png"
    subprocess.run(["rsvg-convert", "-w", str(n), "-h", str(n), svg, "-o", out],
                   check=True)
    return np.asarray(Image.open(out).convert("RGB")).astype(np.float64)


def contrast(a, b):
    a, b = max(a, b), min(a, b)
    return (a + 0.05) / (b + 0.05)


for svg, tag in ((sys.argv[1], "BEFORE"), (sys.argv[2], "AFTER")):
    n = 128
    L = lstar(render(svg, n))
    yy, xx = np.mgrid[0:n, 0:n]
    s = n / 1024.0
    a = math.radians(33.0)
    nx, ny = math.sin(a), math.cos(a)
    d = (xx - 543.0 * s) * nx + (yy - 604.0 * s) * ny
    inside = (xx > 8) & (xx < n - 8) & (yy > 8) & (yy < n - 8)
    blk = (L < 0.42) & inside
    rough = (d < -12 * s * 8) & inside & ~blk
    trued = (d > 12 * s * 8) & inside & ~blk
    print(f"\n== {tag} ({svg})")
    print(f"   block L {L[blk].mean():.3f}  rough L {L[rough].mean():.3f}  "
          f"trued L {L[trued].mean():.3f}")
    print(f"   figure-ground 128px:  vs rough {contrast(L[rough].mean(), L[blk].mean()):.2f}:1"
          f"   vs trued {contrast(L[trued].mean(), L[blk].mean()):.2f}:1"
          f"   fields apart {contrast(L[trued].mean(), L[rough].mean()):.2f}:1")

    L16 = lstar(render(svg, 16))
    print(f"   16px spread p90-p10 {np.percentile(L16, 90) - np.percentile(L16, 10):.3f}"
          f"   sd {L16.std():.4f}")

    # single-light ordering: brightest ground corner must be nearest the key (TL)
    L2 = lstar(render(svg, 256))
    m = L2 > 0.45      # ground only
    q = 256 // 4
    gm = L2[m].mean()
    for name, (y0, x0) in (("TL", (0, 0)), ("TR", (0, 3 * q)),
                           ("BL", (3 * q, 0)), ("BR", (3 * q, 3 * q))):
        p = L2[y0 + 12:y0 + q - 4, x0 + 12:x0 + q - 4]
        pm = m[y0 + 12:y0 + q - 4, x0 + 12:x0 + q - 4]
        if pm.sum():
            print(f"     {name} {p[pm].mean() / gm:.3f}x own ground mean")
