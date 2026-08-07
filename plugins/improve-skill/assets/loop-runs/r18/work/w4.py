"""What is the trued plane's variation actually made of, in each image?

The clean-window SSIM says the trued plane holds the right local amplitude
(sd 0.025 vs the reference's 0.027 at 32px) and almost none of the right
pattern (corr +0.33 against +0.84 everywhere else). This asks whether the
reference's variation is a smooth field or noise, by fitting a low-order
polynomial in canvas (x, y) to each image's trued ground and reporting the
share of variance it explains, at 1024 and at 32.
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


def polyfit_share(v, x, y, order):
    cols = [np.ones_like(x)]
    for i in range(1, order + 1):
        for j in range(i + 1):
            cols.append((x ** (i - j)) * (y ** j))
    A = np.stack(cols, axis=1)
    coef, *_ = np.linalg.lstsq(A, v, rcond=None)
    fit = A @ coef
    return 1 - np.var(v - fit) / np.var(v), fit, coef


ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX = 543.0 - UX * 320.0
AY = 604.0 - UY * 320.0

# trued ground at 1024, well clear of the block, the curl and the rim
g1 = gray(native(1024))
gr1 = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
alpha = np.asarray(native(1024))[..., 3] > 250
yy, xx = np.mgrid[0:1024, 0:1024]
ly = NX * (xx - AX) + NY * (yy - AY)
sel = alpha & (ly < -90) & (g1 > 0.55) & (gr1 > 0.40)
# drop anything within 60px of the block/curl silhouette by luminance dilation
dark = (g1 < 0.55)
# no scipy here: grow the dark mask by 70px with repeated max-pooling shifts
grow = dark.copy()
for _ in range(7):
    g = grow
    for dy in (-10, 0, 10):
        for dx in (-10, 0, 10):
            grow = grow | np.roll(np.roll(g, dy, 0), dx, 1)
sel = sel & ~grow
print("trued sample n=%d" % sel.sum())
x = (xx[sel] - 512) / 512.0
y = (yy[sel] - 512) / 512.0
for order in (1, 2, 3):
    ro, _, co = polyfit_share(g1[sel], x, y, order)
    rr, _, cr = polyfit_share(gr1[sel], x, y, order)
    print("  order %d: ours R2 %.3f   ref R2 %.3f" % (order, ro, rr))
print("  sd ours %.4f  sd ref %.4f" % (g1[sel].std(), gr1[sel].std()))

# residual after an order-2 fit: what is left, and at what scale
_, fo, _ = polyfit_share(g1[sel], x, y, 2)
_, fr, _ = polyfit_share(gr1[sel], x, y, 2)
print("  after order-2 fit: sd ours %.4f  sd ref %.4f" % ((g1[sel] - fo).std(), (gr1[sel] - fr).std()))

# gradient direction of the reference's fitted field vs ours (order 1)
for nm, img in (("ours", g1), ("ref", gr1)):
    _, _, c = polyfit_share(img[sel], x, y, 1)
    ang = math.degrees(math.atan2(c[2], c[1]))
    print("  %s order-1 gradient: dL/dx %+.4f per half-canvas, dL/dy %+.4f, bearing %.1f deg, magnitude %.4f"
          % (nm, c[1], c[2], ang, math.hypot(c[1], c[2])))
