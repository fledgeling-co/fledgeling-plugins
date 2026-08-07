"""r04: reference block measured in its own hone frame (38.92 deg, y=-0.8073x+996)."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGBA"), float) / 255.
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGBA"), float) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def blob(m):
    ys, xs = np.nonzero(m)
    cur = np.zeros(m.shape, bool)
    cur[int(np.median(ys)), int(np.median(xs))] = True
    while True:
        n = cur.copy()
        n[1:] |= cur[:-1]; n[:-1] |= cur[1:]
        n[:, 1:] |= cur[:, :-1]; n[:, :-1] |= cur[:, 1:]
        n &= m
        if n.sum() == cur.sum():
            return cur
        cur = n


def frame(ang_deg, ox, oy):
    a = np.radians(ang_deg)
    ux, uy = np.cos(a), -np.sin(a)          # along the edge, up-right
    nx, ny = -np.sin(a), -np.cos(a)         # away from the cut
    def to_local(px, py):
        dx, dy = px - ox, py - oy
        return ux * dx + uy * dy, nx * dx + ny * dy
    return to_local


for tag, img, thr, ang, org in (
        ("REF ", ref, 0.30, 38.92, (382.0, 688.0)),
        ("CAND", cand, 0.50, 33.00, (274.4, 778.5))):
    L = lum(img)
    m = blob(L < thr)
    ys, xs = np.nonzero(m)
    tl = frame(ang, *org)
    lx, ly = tl(xs.astype(float), ys.astype(float))
    print(f"{tag} blob n={m.sum()} ({100*m.sum()/1024**2:.2f}%)  "
          f"local x[{lx.min():.0f},{lx.max():.0f}] len={lx.max()-lx.min():.0f}  "
          f"y[{ly.min():.0f},{ly.max():.0f}] depth={ly.max()-ly.min():.0f}")
    print(f"     cross-section: local-y span at local-x =")
    for x0 in range(0, 700, 60):
        sel = (lx >= x0 - 12) & (lx < x0 + 12)
        if sel.sum() < 40:
            continue
        print(f"       lx={x0:4d}  ly[{ly[sel].min():7.1f},{ly[sel].max():6.1f}]  "
              f"depth={ly[sel].max()-ly[sel].min():6.1f}   n={sel.sum()}")
    print()
