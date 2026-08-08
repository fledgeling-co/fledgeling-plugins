"""Does our ground texture survive to 32/16px as noise where C2's averages away?

The 1024 crops put the two boards side by side: C2's is a fine isotropic stipple, 2-4px,
while ours is a lattice of dashes 30-60px long crossing at the fibre angles. A 40px dash is
1.25 cells at 32px and 2.5 at 16px - large enough to survive the box filter - where a 3px
stipple is 1/10 of a cell and averages to a flat field. w1 already says neither the grain
nor the fibre creates a false EDGE above 0.10, but SSIM reads local variance, not edges,
and our 32px SSIM is 0.604.

So measure the thing SSIM measures: local standard deviation over open board, in each
image's own frame, at 1024 and at 32 and 16. If ours carries variance at small size that
C2 does not, damping the texture is the in-class repair; if the two agree, the texture is
innocent and this round has nothing in it.
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


def boxstd(g, k):
    """local std over a k x k window, valid interior only"""
    p = np.cumsum(np.cumsum(np.pad(g, ((1, 0), (1, 0))), 0), 1)
    q = np.cumsum(np.cumsum(np.pad(g * g, ((1, 0), (1, 0))), 0), 1)

    def box(c):
        return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)
    m, m2 = box(p), box(q)
    return np.sqrt(np.maximum(m2 - m * m, 0.0)), m


def squircle(n, t=0.80):
    y, x = np.mgrid[0:n, 0:n]
    u = (x + 0.5 - n / 2) / (n / 2)
    v = (y + 0.5 - n / 2) / (n / 2)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 < t


REFIM = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")
print("local std over OPEN BOARD (each image's own frame; board = inside the squircle,")
print("brighter than 0.42 so the block and its hone are out, and not adjacent to them)")
print("  size  window        ours        C2      ours/C2")
for s, k in ((1024, 9), (1024, 33), (128, 3), (32, 3), (16, 3)):
    row = []
    for nm, g in (("ours", nat("icon.svg", s) if s != 1024 else nat("icon.svg", 1024)),
                  ("C2", gray(REFIM.resize((s, s), Image.LANCZOS)))):
        sd, mn = boxstd(g, k)
        o = k // 2
        core = g[o:o + sd.shape[0], o:o + sd.shape[1]]
        keep = squircle(s)[o:o + sd.shape[0], o:o + sd.shape[1]] & (core > 0.42) & (mn > 0.42)
        row.append(np.percentile(sd[keep], 75))
    print("  %4d   %2dpx      %.5f   %.5f     %.2fx" % (s, k, row[0], row[1], row[0] / row[1]))

print("\nand the same number restricted to the UPPER-LEFT rough half of the board,")
print("where our fibre and grain both live at full strength")
for s, k in ((1024, 9), (32, 3), (16, 3)):
    row = []
    for nm, g in (("ours", nat("icon.svg", s)), ("C2", gray(REFIM.resize((s, s), Image.LANCZOS)))):
        sd, mn = boxstd(g, k)
        o = k // 2
        n = sd.shape[0]
        yy, xx = np.mgrid[0:n, 0:n]
        core = g[o:o + n, o:o + n]
        keep = (squircle(s)[o:o + n, o:o + n] & (core > 0.42) & (mn > 0.42)
                & ((xx + yy) < n * 0.85))
        row.append(np.percentile(sd[keep], 75))
    print("  %4d   %2dpx      %.5f   %.5f     %.2fx" % (s, k, row[0], row[1], row[0] / row[1]))
