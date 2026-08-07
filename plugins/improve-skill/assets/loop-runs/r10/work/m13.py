"""The ground's own luminance field, fitted.

To make a ridge pair mean-neutral AND hold its contrast constant across the plane
(the reference's amplitude is flat in radius from the key; ours falls off), the
build needs to know what luminance the ground actually has where it puts a stroke.
Quadratic fit in canvas (x,y) over the masked rough / trued ground of the current
master, reported as coefficients the build script can evaluate directly.
"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
N = 1024
g = F.to_gray(F.render_candidate(A / "icon.svg", N))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", N))


def erode(m, r):
    im = Image.fromarray((m * 255).astype(np.uint8))
    while r > 0:
        s = min(9, 2 * r + 1); im = im.filter(ImageFilter.MinFilter(s)); r -= s // 2
    return np.asarray(im) > 127


ys, xs = np.mgrid[0:N, 0:N]
u = (xs - 511.5) / 511.5; v = (ys - 511.5) / 511.5
inside = (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 < 0.86
bl = 957.0 + (292.0 - 957.0) * xs / N
clear = erode(~(g < 0.44), 30)
REG = {"rough": (ys < bl - 24) & clear & inside,
       "trued": (ys > bl + 24) & clear & inside}

for name, m in REG.items():
    X, Y, Z = xs[m] / 1024.0, ys[m] / 1024.0, g[m]
    M = np.stack([np.ones_like(X), X, Y, X * X, Y * Y, X * Y], 1)
    c, *_ = np.linalg.lstsq(M, Z, rcond=None)
    pred = M @ c
    print(f"{name}: n={m.sum()}  rms residual {np.sqrt(((Z-pred)**2).mean()):.4f}"
          f"   range {Z.min():.3f}..{Z.max():.3f}")
    print("   coef (1, x, y, x2, y2, xy) with x,y in units of 1024:")
    print("   " + ", ".join(f"{v:+.5f}" for v in c))
    for lo in range(0, 1200, 200):
        r = np.hypot(xs - 75, ys - 25)
        mm = m & (r >= lo) & (r < lo + 200)
        if mm.sum() > 500:
            print(f"     r {lo:4d}-{lo+200:4d}  master mean {g[mm].mean():.3f}"
                  f"   ref mean {h[mm].mean():.3f}")
