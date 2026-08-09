#!/usr/bin/env python3
"""r04 probe 4: the ground-contact crevice along the block's lower silhouette.

For each column, walk down from inside the front wall, find the silhouette (the
big luminance drop), then read: the wall value just above it, the darkest value
in the first 12px outside it, the width of the sub-wall dip, and the value 40px
and 90px further out. Shapes are compared, not positions - the two blocks sit at
different heights on the canvas.
"""
import numpy as np
from PIL import Image

BASE = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/"


def load(p):
    return np.asarray(Image.open(BASE + p).convert("RGB")).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def sat(a):
    mx, mn = a.max(-1), a.min(-1)
    return np.where(mx > 1e-9, (mx - mn) / np.maximum(mx, 1e-9), 0.0)


def hue(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    c = mx - mn
    if c < 1e-9:
        return -1.0
    if mx == r:
        h = ((g - b) / c) % 6
    elif mx == g:
        h = (b - r) / c + 2
    else:
        h = (r - g) / c + 4
    return h * 60.0


def scan(img, L, y0, y1, label):
    print(f"== {label}: lower silhouette contact profile ==")
    print("     x   edge_y   wall   min_out  dip_w   +40px   +90px")
    seam_depths, seam_widths = [], []
    for x in range(300, 821, 40):
        col = L[:, x]
        # the wall: median over the 30px above the drop; find the drop first
        edge = None
        for y in range(y0, y1):
            if col[y] - col[y + 4] > 0.06 and col[y] > 0.55:
                edge = y
                break
        if edge is None:
            print(f"  {x:5d}   (no edge found)")
            continue
        wall = float(np.median(col[edge - 30:edge - 2]))
        out = col[edge + 1:edge + 13]
        mn = float(out.min())
        w = int(np.sum(col[edge + 1:edge + 40] < wall - 0.06))
        print(f"  {x:5d}   {edge:5d}   {wall:.3f}   {mn:.3f}   {w:4d}   "
              f"{col[min(edge+40,1023)]:.3f}   {col[min(edge+90,1023)]:.3f}")
        seam_depths.append(wall - mn)
        seam_widths.append(w)
    if seam_depths:
        print(f"  mean seam depth below the wall: {np.mean(seam_depths):.3f}   "
              f"mean sub-wall width: {np.mean(seam_widths):.1f}px")
    print()


ref, cand = load("reference-1024.png"), load("candidate-1024.png")
Lr, Lc = lum(ref), lum(cand)
scan(ref, Lr, 820, 960, "reference")
scan(cand, Lc, 700, 860, "candidate")

print("== hue and saturation of the darkest contact pixels ==")
for name, img, L in (("ref", ref, Lr), ("cand", cand, Lc)):
    S = sat(img)
    y0, y1 = (860, 960) if name == "ref" else (770, 860)
    band = L[y0:y1, 300:820]
    idx = np.dstack(np.unravel_index(np.argsort(band, axis=None)[:400], band.shape))[0]
    cols = np.array([img[y0 + a, 300 + b] for a, b in idx])
    Ls = np.array([L[y0 + a, 300 + b] for a, b in idx])
    Ss = np.array([S[y0 + a, 300 + b] for a, b in idx])
    hs = [hue(tuple(c)) for c in cols]
    print(f"  {name}: darkest-400 mean rgb {cols.mean(0).round(4)}  "
          f"L {Ls.mean():.4f} (min {Ls.min():.4f})  S {Ss.mean():.4f}  "
          f"hue {np.mean([h for h in hs if h >= 0]):.1f}")
