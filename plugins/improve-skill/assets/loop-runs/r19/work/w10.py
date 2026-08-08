"""Where is our roll's hot cell, and is it interior or silhouette?

w9, each roll measured in its own frame so registration cannot reach the number: the two
rolls cover the same area (65 cells against 64 at 32px) and hold nearly the same spread of
luminance (0.186 against 0.151), but our |grad| runs hotter at the top - p90 0.151 vs
0.131, max 0.367 vs 0.210, 1.75x at the peak. At 16px the same shape: p90 0.344 vs 0.247.

A silhouette against the dark block is a hard boundary in BOTH images and should land near
each other; an interior step that only ours has is a feature that will alias. So print the
hot cells with their canvas coordinates, mark which of them touch the roll's outer
boundary, and print each image's roll as a grid so the step can be read directly.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return gray(Image.open(t).convert("RGBA"))


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def disc(c, R, n):
    y, x = np.mgrid[0:n, 0:n]
    return ((x + 0.5) * (1024 / n) - c[0]) ** 2 + ((y + 0.5) * (1024 / n) - c[1]) ** 2 <= R * R


def hoop(n):
    m = disc((294.0, 253.0), 115.0, n) | disc((359.0, 186.0), 121.0, n)
    for i in range(1, 25):
        t = i / 25
        m |= disc((294.0 + 65.0 * t, 253.0 - 67.0 * t), 115.0 + 6.0 * t, n)
    return m


def interior(m):
    e = m.copy()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        e &= np.roll(np.roll(m, dy, 0), dx, 1)
    return e


ours = nat("icon.svg", 32)
off = nat(str(WORK / "var_noshaving.svg"), 32)
ref = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((32, 32), Image.LANCZOS))
M_o, M_r = np.abs(ours - off) > 0.004, hoop(32)
I_o, I_r = interior(M_o), interior(M_r)
so, sr = sobel(ours), sobel(ref)

for nm, s, M, I in (("ours", so, M_o, I_o), ("C2", sr, M_r, I_r)):
    hot = sorted(((s[y, x], x, y, I[y, x]) for y, x in zip(*np.nonzero(M))), reverse=True)[:8]
    print("%s hottest cells in its own roll:" % nm)
    for v, x, y, ins in hot:
        print("   (%2d,%2d) canvas (%4d,%4d)  |grad| %.3f  %s"
              % (x, y, x * 32, y * 32, v, "INTERIOR" if ins else "boundary"))
    ins = [s[y, x] for y, x in zip(*np.nonzero(I))]
    print("   interior only (%d cells): p50 %.3f  p90 %.3f  max %.3f\n"
          % (len(ins), np.percentile(ins, 50), np.percentile(ins, 90), max(ins)))

print("32px luminance grid over the roll, ours then C2 (rows y, cols x)")
for nm, g, M in (("ours", ours, M_o), ("C2", ref, M_r)):
    ys, xs = np.nonzero(M)
    print(" %s   x=%s" % (nm, "".join("%7d" % x for x in range(xs.min(), xs.max() + 1))))
    for y in range(ys.min(), ys.max() + 1):
        print("  y%2d  " % y + "".join(("%7.3f" % g[y, x]) if M[y, x] else "      ."
                                       for x in range(xs.min(), xs.max() + 1)))
