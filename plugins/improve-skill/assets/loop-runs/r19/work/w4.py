"""Two questions at once.

(1) ALIASING, in its own definition: the scorer renders natively at each size, so a
feature that the rasteriser cannot resolve at 32/16 shows up as native-vs-LANCZOS
disagreement. That is the defect this round's class is named after, and it is worth
re-running on the current master before assuming the class has nothing left in it.

(2) The 3 cast-shadow FP cells at (12,24) (10,25) (11,25): read the 32px grid there
in ours, in the CAST_OP=0 twin and in C2, the way w3 read the curl's.
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


def rgba(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


big = rgba("icon.svg", 1024)
print("native vs LANCZOS-downsampled-from-1024 (pure rasteriser aliasing):")
for s in (128, 32, 16):
    a = gray(rgba("icon.svg", s))
    b = gray(big.resize((s, s), Image.LANCZOS))
    d = a - b
    print("  %3dpx  mean|d| %.4f  p99 %.4f  max|d| %.4f  signed mean %+.4f"
          % (s, np.abs(d).mean(), np.percentile(np.abs(d), 99), np.abs(d).max(), d.mean()))
    if s == 32:
        idx = np.argsort(np.abs(d).ravel())[::-1][:10]
        ys, xs = np.unravel_index(idx, d.shape)
        for y, x in zip(ys, xs):
            print("      cell (%2d,%2d) native %.3f  down %.3f  d %+.3f" % (x, y, a[y, x], b[y, x], d[y, x]))

X0, X1, Y0, Y1 = 8, 20, 16, 28
ours = gray(rgba("icon.svg", 32))
nocast = gray(rgba(str(WORK / "var_nocast.svg"), 32))
ref = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((32, 32), Image.LANCZOS))


def show(tag, g):
    print("\n%s" % tag)
    print("      " + "".join("%6d" % x for x in range(X0, X1)))
    for y in range(Y0, Y1):
        print("  y%2d " % y + "".join("%6.3f" % g[y, x] for x in range(X0, X1)))


show("32px OURS  (block, its shadow, the trued plane below it)", ours)
show("32px OURS with CAST_OP = 0", nocast)
show("32px C2 reference", ref)
show("32px what the cast shadow does (ours - nocast)", ours - nocast)
