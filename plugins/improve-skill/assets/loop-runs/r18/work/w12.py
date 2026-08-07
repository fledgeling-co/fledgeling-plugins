"""How dark is the reference's shadow, and how far does it reach - as a ratio, not a level.

The blur sweep (w11) made the 32px false positives worse, not better, which says the cast's
32px gradient is set by its DEPTH over a 3-cell Sobel window rather than by its blur radius.
So the question the reference has to answer is a material one: at a given distance from the
block, how much darker is the shadowed ground than unshadowed ground of the same field
position? Each image is normalised against its OWN far-field ground at the same u, so the
trued plane's +0.18 palette fault cancels and what is left is the shadow's own contrast.
"""
import subprocess
import tempfile
import pathlib
import math
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


t = TMP / "n.png"
subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", "icon.svg", "-o", str(t)], check=True)
im = Image.open(t).convert("RGBA")
g1 = gray(im)
gr1 = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
alpha = np.asarray(im)[..., 3] > 250

yy, xx = np.mgrid[0:1024, 0:1024]
uu, vv = (xx - 511.5) / 511.5, (yy - 511.5) / 511.5
rim = (np.abs(uu) ** 5 + np.abs(vv) ** 5) ** 0.2 > 0.86
u = (xx + yy) / math.sqrt(2.0)


def dist(mask, step=4, k=70):
    d = np.full((1024, 1024), 1e9)
    m = mask.copy()
    for i in range(k):
        d[m & (d > 1e8)] = i * step
        g = m
        for dy in (-step, 0, step):
            for dx in (-step, 0, step):
                m = m | np.roll(np.roll(g, dy, 0), dx, 1)
    return d


UBIN = 64.0
ub = (u / UBIN).astype(int)


def profile(g, name):
    dark = g < 0.42                       # this image's own solid
    D = dist(dark)
    ground = alpha & ~rim & ~dark & (g > 0.42)
    far = ground & (D > 260)
    # expectation per u-bin from this image's own far field
    exp = np.zeros_like(g)
    for b in np.unique(ub[ground]):
        sel = far & (ub == b)
        if sel.sum() < 400:
            continue
        exp[ub == b] = g[sel].mean()
    ok = ground & (exp > 0)
    print("\n%s   far-field bins covering %.1f%% of ground" % (name, 100 * ok.mean() / max(ground.mean(), 1e-9)))
    print("   dist    n      L      expected   ratio")
    out = {}
    for lo in (0, 16, 32, 48, 64, 88, 112, 144, 176, 208, 240):
        hi = lo + (16 if lo < 64 else 24 if lo < 144 else 32)
        s = ok & (D >= lo) & (D < hi)
        if s.sum() < 300:
            continue
        r = g[s].mean() / exp[s].mean()
        out[lo] = r
        print("  %3d-%3d %6d  %.4f   %.4f    %.4f" % (lo, hi, s.sum(), g[s].mean(), exp[s].mean(), r))
    return out


a = profile(g1, "ours")
b = profile(gr1, "reference")
print("\n  dist   ours ratio   ref ratio   ours deficit (ref-ours, +ve = ours too dark)")
for k in sorted(set(a) & set(b)):
    print("  %3d      %.4f      %.4f      %+.4f" % (k, a[k], b[k], b[k] - a[k]))
