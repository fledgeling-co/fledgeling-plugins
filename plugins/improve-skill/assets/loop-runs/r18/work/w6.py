"""The trued plane's falloff again, with the shadow held out rather than assumed away.

r17 measured the reference's cast reaching ~150px from contact and half-recovering
at 64px against our 26px, so any bin drawn near the block is measuring two images'
different shadows, not their fields. This holds out everything within RCUT px of
either image's dark mass and re-profiles on u, and reports how the answer moves as
RCUT grows - a field measurement that is stable in RCUT is a field measurement.
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


def native(size, src="icon.svg"):
    t = TMP / ("%s-%d.png" % (pathlib.Path(src).stem, size))
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), src, "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


img = native(1024)
g1 = gray(img)
gr1 = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
alpha = np.asarray(img)[..., 3] > 250

ANG = math.radians(33.0)
NX, NY = -math.sin(ANG), -math.cos(ANG)
UXc, UYc = math.cos(ANG), -math.sin(ANG)
AX, AY = 543.0 - UXc * 320.0, 604.0 - UYc * 320.0
yy, xx = np.mgrid[0:1024, 0:1024]
ly = NX * (xx - AX) + NY * (yy - AY)
u = (xx + yy) / math.sqrt(2.0)
uu, vv = (xx - 511.5) / 511.5, (yy - 511.5) / 511.5
rim = (np.abs(uu) ** 5 + np.abs(vv) ** 5) ** 0.2 > 0.86

dark = (g1 < 0.45) | (gr1 < 0.45)   # the solid itself, in either image; not the vignette corners
ys, xs = np.nonzero(dark)


def dist_to_dark():
    """exact-enough: chamfer by repeated dilation on a coarse grid"""
    d = np.full((1024, 1024), 1e9)
    m = dark.copy()
    step = 8
    for k in range(45):
        d[m & (d > 1e8)] = k * step
        g = m
        for dy in (-step, 0, step):
            for dx in (-step, 0, step):
                m = m | np.roll(np.roll(g, dy, 0), dx, 1)
    return d


D = dist_to_dark()

for RCUT in (80, 160, 240, 320):
    sel = alpha & ~rim & (D > RCUT) & (ly < -40)
    rows = []
    for lo in np.arange(650, 1350, 50.0):
        b = sel & (u >= lo) & (u < lo + 50)
        if b.sum() < 600:
            continue
        rows.append((lo + 25, b.sum(), g1[b].mean(), gr1[b].mean()))
    if len(rows) < 4:
        print("RCUT %d: only %d bins" % (RCUT, len(rows)))
        continue
    a = np.array(rows)
    po = np.polyfit(a[:, 0], a[:, 2], 1)
    pr = np.polyfit(a[:, 0], a[:, 3], 1)
    mo, mr = g1[sel].mean(), gr1[sel].mean()
    print("RCUT %3d  n=%6d  u %4d-%4d (%d bins)   slope/100u ours %+.4f  ref %+.4f  ratio %.2fx"
          % (RCUT, sel.sum(), a[0, 0], a[-1, 0], len(rows), po[0] * 100, pr[0] * 100, pr[0] / po[0]))
    print("          relative slope (per 100u, as a fraction of own mean): ours %+.4f  ref %+.4f  ratio %.2fx"
          % (po[0] * 100 / mo, pr[0] * 100 / mr, (pr[0] / mr) / (po[0] / mo)))

# the winning RCUT printed in full
RCUT = 240
sel = alpha & ~rim & (D > RCUT) & (ly < -40)
print("\nRCUT=%d full profile   (ours mean %.4f, ref mean %.4f)" % (RCUT, g1[sel].mean(), gr1[sel].mean()))
print("   u      n      ours     ref    ours/mean ref/mean")
for lo in np.arange(650, 1350, 50.0):
    b = sel & (u >= lo) & (u < lo + 50)
    if b.sum() < 600:
        continue
    print("  %4d %7d   %.4f  %.4f   %.4f  %.4f" % (lo + 25, b.sum(), g1[b].mean(), gr1[b].mean(),
                                                   g1[b].mean() / g1[sel].mean(), gr1[b].mean() / gr1[sel].mean()))
