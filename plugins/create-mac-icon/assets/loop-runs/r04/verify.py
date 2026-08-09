#!/usr/bin/env python3
"""r04 verify: the rendered ground arris against the reference's measured profile.

Same instrument as probe8, run on the new render, so the two constants are set
against the reference's numbers rather than against the composite.
"""
import sys
import numpy as np
from PIL import Image

REF = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/reference-1024.png"
CAND = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/cand-test.png"


def load(p):
    im = Image.open(p).convert("RGBA")
    a = np.asarray(im).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    return rgb * al + (128 / 255.0) * (1 - al)


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def sat(a):
    mx, mn = a.max(-1), a.min(-1)
    return np.where(mx > 1e-9, (mx - mn) / np.maximum(mx, 1e-9), 0.0)


def hue_of(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    c = mx - mn
    if c < 1e-9:
        return -1.0
    h = ((g - b) / c) % 6 if mx == r else ((b - r) / c + 2 if mx == g else (r - g) / c + 4)
    return h * 60.0


def arris(img, L, y0, y1, label):
    """Per-column: the wall 30px up, the roll's loss into the arris, the crevice
    minimum and the width of the sub-wall darkening outside the silhouette."""
    rows = []
    for x in range(320, 741, 30):
        col = L[:, x]
        edge = None
        for y in range(y0, y1):
            if col[y] - col[y + 5] > 0.05 and col[y] > 0.52:
                edge = y
                break
        if edge is None:
            continue
        # the true silhouette: the last row before the fall, refined to 1px
        while edge + 1 < y1 and col[edge + 1] < col[edge] - 0.004:
            edge += 1
        wall = float(np.median(col[edge - 32:edge - 24]))
        near = float(np.median(col[edge - 6:edge - 2]))
        mn_i = edge + 1 + int(np.argmin(col[edge + 1:edge + 16]))
        w = int(np.sum(col[edge + 1:edge + 45] < wall - 0.06))
        rows.append((wall, near - wall, float(col[mn_i]), w,
                     float(col[min(edge + 13, 1023)]), float(col[min(edge + 20, 1023)])))
    a = np.array(rows)
    print(f"  {label:10s} wall {a[:,0].mean():.3f}   roll loss {a[:,1].mean():+.3f}   "
          f"crevice min {a[:,2].mean():.3f}   sub-wall width {a[:,3].mean():4.1f}px   "
          f"+13px {a[:,4].mean():.3f}   +20px {a[:,5].mean():.3f}")
    return a


ref, cand = load(REF), load(CAND)
Lr, Lc = lum(ref), lum(cand)
print("== the ground arris, reference vs candidate ==")
arris(ref, Lr, 840, 950, "reference")
arris(cand, Lc, 700, 860, "candidate")

print()
print("== chroma of the darkest 400 contact pixels ==")
for name, img, L in (("reference", ref, Lr), ("candidate", cand, Lc)):
    S = sat(img)
    y0, y1 = (860, 960) if name == "reference" else (770, 870)
    band = L[y0:y1, 320:740]
    idx = np.dstack(np.unravel_index(np.argsort(band, axis=None)[:400], band.shape))[0]
    cols = np.array([img[y0 + p, 320 + q] for p, q in idx])
    Ls = np.array([L[y0 + p, 320 + q] for p, q in idx])
    Ss = np.array([S[y0 + p, 320 + q] for p, q in idx])
    hs = [hue_of(tuple(c)) for c in cols]
    print(f"  {name:10s} L {Ls.mean():.4f} (min {Ls.min():.4f})   S {Ss.mean():.4f}   "
          f"hue {np.mean([h for h in hs if h >= 0]):.1f}")

print()
print("== 1px profile at x=620, silhouette outward ==")
for name, L, y0 in (("reference", Lr, 890), ("candidate", Lc, 788)):
    print(f"  {name}: " + " ".join(f"{L[y0+k,620]:.3f}" for k in range(0, 30, 2)))
