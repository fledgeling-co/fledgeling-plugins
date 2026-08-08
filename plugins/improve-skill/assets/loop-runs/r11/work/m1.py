#!/usr/bin/env python3
"""Orientation content of the un-planed ground: reference vs master.

Question: how many bearings does the reference's torn field actually run on?
The master authors TWO crossing families on the claim that the reference is a
cross-hatched lattice. That claim is tested here, not assumed.

Method: high-pass the plane (subtract a wide box mean, so the field's own
lighting ramp drops out and only texture survives), build the gradient
structure tensor, and histogram gradient ENERGY by orientation. A lattice puts
two peaks 90 deg apart into the histogram; a planed/torn surface puts one.
Ridge bearing = gradient bearing + 90.
"""
import math
import sys

import numpy as np
from PIL import Image

W = 1024


def lin(a):
    a = a / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def load(p):
    im = Image.open(p).convert("RGB").resize((W, W), Image.LANCZOS)
    a = lin(np.asarray(im).astype(np.float64))
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def boxblur(g, r):
    """Separable running-mean, reflect-padded. r px half-width."""
    k = 2 * r + 1
    for ax in (0, 1):
        p = np.pad(g, [(r, r) if i == ax else (0, 0) for i in range(2)], mode="reflect")
        c = np.cumsum(p, axis=ax)
        c = np.concatenate([np.zeros_like(np.take(c, [0], axis=ax)), c], axis=ax)
        lo = np.take(c, range(0, g.shape[ax]), axis=ax)
        hi = np.take(c, range(k, k + g.shape[ax]), axis=ax)
        g = (hi - lo) / k
    return g


yy, xx = np.mgrid[0:W, 0:W]


def masks(kind):
    """Un-planed ground only, block and curl excluded.

    Boundary lines are each icon's own measured hone: the reference's fitted
    y = -0.8026x + 991.2 (38.75 deg, round 9), the master's built 33.0 deg
    through the edge midpoint. Exclusion boxes are drawn wide on purpose - this
    measures orientation, and a clean patch is worth more than a big one.
    """
    if kind == "ref":
        rough = yy < (-0.8026 * xx + 991.2)
        block = (xx > 190) & (xx < 830) & (yy > 120) & (yy < 720)
        curl = (xx > 150) & (xx < 500) & (yy > 40) & (yy < 420)
    else:
        a = math.radians(33.0)
        # ux,uy along the hone; the un-planed side is local n > 0 (canvas up-left)
        nx, ny = math.sin(a), math.cos(a)
        ex, ey = 543.0, 604.0
        rough = ((xx - ex) * nx + (yy - ey) * ny) < 0
        block = (xx > 150) & (xx < 840) & (yy > 120) & (yy < 800)
        curl = (xx > 120) & (xx < 460) & (yy > 140) & (yy < 440)
    tile = (xx > 60) & (xx < W - 60) & (yy > 60) & (yy < W - 60)
    return rough & tile & ~block & ~curl


def orient(g, m, label):
    hp = g - boxblur(g, 12)
    gx = np.zeros_like(g)
    gy = np.zeros_like(g)
    gx[:, 1:-1] = (hp[:, 2:] - hp[:, :-2]) * 0.5
    gy[1:-1, :] = (hp[2:, :] - hp[:-2, :]) * 0.5
    mag = gx * gx + gy * gy
    # only pixels fully inside the mask carry a valid gradient
    mm = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
    gx, gy, mag = gx[mm], gy[mm], mag[mm]
    # ridge bearing = gradient bearing + 90, mod 180, in CANVAS degrees (y down)
    th = (np.degrees(np.arctan2(gy, gx)) + 90.0) % 180.0
    nb = 36
    h = np.zeros(nb)
    idx = np.clip((th / 180.0 * nb).astype(int), 0, nb - 1)
    np.add.at(h, idx, mag)
    h /= h.sum()
    # coherence from the doubled-angle resultant: 1 = one bearing, 0 = isotropic
    c = math.hypot(float((mag * np.cos(np.radians(2 * th))).sum()),
                   float((mag * np.sin(np.radians(2 * th))).sum())) / mag.sum()
    peak = int(np.argmax(h))
    print(f"\n== {label}   n={mm.sum()}  texture sd={hp[mm].std():.4f}  coherence={c:.3f}")
    print(f"   dominant ridge bearing {peak * 5 + 2.5:.1f} deg   share {h[peak] * 100:.1f}%")
    for i in range(nb):
        bar = "#" * int(round(h[i] * 400))
        print(f"   {i * 5:3d}-{i * 5 + 5:3d} {h[i] * 100:5.2f}% {bar}")
    return h, c


if __name__ == "__main__":
    ref = load("loop-runs/r10-reverted/reference-1024.png")
    cand = load("loop-runs/r10-reverted/candidate-1024.png")
    orient(ref, masks("ref"), "REFERENCE un-planed")
    orient(cand, masks("cand"), "MASTER un-planed")
