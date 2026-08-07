"""r04: reference cutting-edge extent (block pixels at ly ~ 0) and top-face back edge."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB"), float) / 255.
L = 0.2126 * ref[..., 0] + 0.7152 * ref[..., 1] + 0.0722 * ref[..., 2]

a = np.radians(38.92)
ux, uy = np.cos(a), -np.sin(a)
nx, ny = -np.sin(a), -np.cos(a)
ox, oy = 382.0, 688.0
Y, X = np.mgrid[0:1024, 0:1024]
dx, dy = X - ox, Y - oy
lx = ux * dx + uy * dy
ly = nx * dx + ny * dy

dark = L < 0.34
for lo, hi, name in ((5, 20, "just above the cut"), (60, 90, "mid front/top"), (150, 200, "top face")):
    sel = dark & (ly > lo) & (ly < hi)
    v = lx[sel]
    if len(v):
        h, _ = np.histogram(v, bins=13, range=(-60, 660))
        print(f"{name:20s} lx[{v.min():.0f},{v.max():.0f}]  counts/50px:",
              " ".join(f"{c:4d}" for c in h))

# back edge per lx: max ly of dark
print("\nback edge (max ly of dark) and shoulder (darkest ly) by lx:")
for x0 in range(20, 601, 60):
    sel = dark & (lx > x0 - 15) & (lx < x0 + 15) & (ly > -40) & (ly < 320)
    if sel.sum() < 200:
        continue
    lys = ly[sel]
    print(f"  lx={x0:4d}  back_ly={lys.max():6.1f}  n={sel.sum()}")
