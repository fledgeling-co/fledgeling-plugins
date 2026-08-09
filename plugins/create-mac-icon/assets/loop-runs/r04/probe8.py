#!/usr/bin/env python3
"""r04 probe 8: 1px resolution across the reference's ground arris.

The crop shows a bright hairline at the very bottom of the wall, immediately
above the dark contact seam - a bounce lift on the block's bottom roll. Sample
it at 1px so it is not stepped over, and get its height, width and the seam's
profile per column.
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


ref, cand = load("reference-1024.png"), load("candidate-1024.png")
Lr, Lc = lum(ref), lum(cand)
Sr, Sc = sat(ref), sat(cand)

print("== reference, 1px down the ground arris (x=460) ==")
print("  " + " ".join(f"{y}:{Lr[y,460]:.3f}" for y in range(866, 916)))
print("== reference, 1px (x=620) ==")
print("  " + " ".join(f"{y}:{Lr[y,620]:.3f}" for y in range(866, 916)))
print("== candidate, 1px (x=620) ==")
print("  " + " ".join(f"{y}:{Lc[y,620]:.3f}" for y in range(736, 786)))

print()
print("== reference: bounce line and seam, per column ==")
print("      x  wall(-30)  crest  crest_dy  seam_min  seam_dy  width(sub-wall)")
crest_lift, crest_offs, seam_min, widths = [], [], [], []
for x in range(320, 741, 30):
    col = Lr[:, x]
    edge = next(y for y in range(840, 950) if col[y] - col[y + 4] > 0.06 and col[y] > 0.55)
    wall = float(np.median(col[edge - 34:edge - 14]))
    win = col[edge - 12:edge + 2]
    k = int(np.argmax(win))
    crest = float(win[k])
    mn_i = edge + 1 + int(np.argmin(col[edge + 1:edge + 16]))
    w = int(np.sum(col[edge + 1:edge + 45] < wall - 0.06))
    print(f"  {x:5d}  {wall:8.3f}  {crest:.3f}  {edge-12+k-edge:+7d}  "
          f"{col[mn_i]:.3f}  {mn_i-edge:+6d}  {w:6d}")
    crest_lift.append(crest - wall)
    crest_offs.append(edge - 12 + k - edge)
    seam_min.append(float(col[mn_i]))
    widths.append(w)
print(f"  mean bounce lift over the wall {np.mean(crest_lift):+.3f} at "
      f"{np.mean(crest_offs):+.1f}px from the edge;  seam min L {np.mean(seam_min):.3f}, "
      f"sub-wall width {np.mean(widths):.1f}px")

print()
print("== chroma at the ground arris ==")
for name, L, S, img, band in (("ref", Lr, Sr, ref, (893, 906)), ("cand", Lc, Sc, cand, (793, 806))):
    y0, y1 = band
    reg = (slice(y0, y1), slice(340, 720))
    print(f"  {name} seam band y {y0}..{y1}: L {L[reg].mean():.4f}  S {S[reg].mean():.4f}  "
          f"rgb {img[reg].reshape(-1,3).mean(0).round(4)}")
