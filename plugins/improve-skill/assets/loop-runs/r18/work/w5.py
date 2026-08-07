"""The trued plane's own falloff, profiled on the coordinate the gradient is
authored on: u = (x + y)/sqrt(2), the shared key axis (build_icon.py:1279).

Both images are masked identically: alpha fully opaque, well clear of the cut,
and clear of EITHER image's dark mass and its shadow, so the reference's own
20-40px silhouette offset cannot leak the block into a ground bin. Each profile
is reported raw and divided by its own mean over the sample, because the trued
plane sits 0.179 brighter than the reference's and only the SHAPE is in class.
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


def grow(m, steps=8, step=8):
    out = m.copy()
    for _ in range(steps):
        g = out
        for dy in (-step, 0, step):
            for dx in (-step, 0, step):
                out = out | np.roll(np.roll(g, dy, 0), dx, 1)
    return out


img = native(1024)
g1 = gray(img)
gr1 = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
alpha = np.asarray(img)[..., 3] > 250

ANG = math.radians(33.0)
NX, NY = -math.sin(ANG), -math.cos(ANG)
UXc, UYc = math.cos(ANG), -math.sin(ANG)
AX = 543.0 - UXc * 320.0
AY = 604.0 - UYc * 320.0
yy, xx = np.mgrid[0:1024, 0:1024]
ly = NX * (xx - AX) + NY * (yy - AY)
u = (xx + yy) / math.sqrt(2.0)

# rim, in superellipse coordinates, matching fidelity.py's rim_mask
uu = (xx - 511.5) / 511.5
vv = (yy - 511.5) / 511.5
rim = (np.abs(uu) ** 5 + np.abs(vv) ** 5) ** 0.2 > 0.86

dark = grow((g1 < 0.60) | (gr1 < 0.52))
sel = alpha & ~rim & ~dark & (ly < -70)
print("trued sample n=%d  (%.1f%% of tile)" % (sel.sum(), 100 * sel.mean()))

bins = np.arange(700, 1330, 50.0)
print("\n   u      n     ours    ref    ours/mean  ref/mean")
mo, mr = g1[sel].mean(), gr1[sel].mean()
rows = []
for lo in bins:
    b = sel & (u >= lo) & (u < lo + 50)
    if b.sum() < 300:
        continue
    o, r = g1[b].mean(), gr1[b].mean()
    rows.append((lo + 25, b.sum(), o, r))
    print("  %4d %7d   %.3f  %.3f   %.4f   %.4f" % (lo + 25, b.sum(), o, r, o / mo, r / mr))
print("\n  sample mean ours %.4f  ref %.4f  (delta %+.3f)" % (mo, mr, mo - mr))
arr = np.array(rows)
sp_o = arr[:, 2].max() - arr[:, 2].min()
sp_r = arr[:, 3].max() - arr[:, 3].min()
print("  bin span (max-min): ours %.4f   ref %.4f   ratio ref/ours %.2fx" % (sp_o, sp_r, sp_r / sp_o))
# straight-line slope per 100 u
po = np.polyfit(arr[:, 0], arr[:, 2], 1)
pr = np.polyfit(arr[:, 0], arr[:, 3], 1)
print("  linear slope per 100u: ours %+.4f   ref %+.4f   ratio %.2fx" % (po[0] * 100, pr[0] * 100, pr[0] / po[0]))
np.save("loop-runs/r18/work/truedprof.npy", arr)

# --- the same for the un-planed plane, on its own radial coordinate
r = np.hypot(xx - 75.0, yy - 25.0)
sel2 = alpha & ~rim & ~dark & (ly > 70)
mo2, mr2 = g1[sel2].mean(), gr1[sel2].mean()
print("\nun-planed sample n=%d;  mean ours %.4f ref %.4f (delta %+.3f)" % (sel2.sum(), mo2, mr2, mo2 - mr2))
print("   r      n     ours    ref")
rows2 = []
for lo in np.arange(150, 1050, 75.0):
    b = sel2 & (r >= lo) & (r < lo + 75)
    if b.sum() < 300:
        continue
    rows2.append((lo + 37, b.sum(), g1[b].mean(), gr1[b].mean()))
    print("  %4d %7d   %.3f  %.3f" % (lo + 37, b.sum(), g1[b].mean(), gr1[b].mean()))
a2 = np.array(rows2)
print("  bin span: ours %.4f  ref %.4f  ratio %.2fx" % (a2[:, 2].max() - a2[:, 2].min(),
                                                        a2[:, 3].max() - a2[:, 3].min(),
                                                        (a2[:, 3].max() - a2[:, 3].min()) / (a2[:, 2].max() - a2[:, 2].min())))
