"""Corner luminances in both images, and a simulation of the falloff gain at 32px.

Round 7 recorded C2's corners as TL 0.869, TR 0.509, BL 0.556, BR 0.562. The
trued plane owns BR, so how far ours sits above 0.562 is the check on whether
steepening its falloff runs toward the reference or past it. The simulation
applies the same multiplicative ramp to the native 32px render on the trued
mask and re-reads SSIM: an estimate, not the verdict, but enough to refuse a
gain that would overshoot before it is authored.
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


def box_mean(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[: x.shape[0], : x.shape[1]]


def ssim(a, b):
    w = max(3, min(11, a.shape[0] // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    ma, mb = box_mean(a, w), box_mean(b, w)
    va, vb = box_mean(a * a, w) - ma ** 2, box_mean(b * b, w) - mb ** 2
    cov = box_mean(a * b, w) - ma * mb
    return float(np.clip(((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2)), -1, 1).mean())


g1 = gray(native(1024))
gr1 = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
print("corner means over a 96px box inset 40px:")
for nm, (x0, y0) in (("TL", (40, 40)), ("TR", (888, 40)), ("BL", (40, 888)), ("BR", (888, 888))):
    print("  %s  ours %.3f   ref %.3f" % (nm, g1[y0:y0 + 96, x0:x0 + 96].mean(), gr1[y0:y0 + 96, x0:x0 + 96].mean()))

ANG = math.radians(33.0)
UXc, UYc = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX, AY = 543.0 - UXc * 320.0, 604.0 - UYc * 320.0

STOPS = [(0.4558, 0.863), (0.5248, 0.871), (0.5939, 0.869), (0.6629, 0.852), (0.7320, 0.848),
         (0.8010, 0.809), (0.8701, 0.747), (0.9391, 0.700), (0.9999, 0.683)]
off = np.array([s[0] for s in STOPS])
lv = np.array([s[1] for s in STOPS])
PIVOT = 0.8368

for s in (32, 16):
    nat = native(s)
    a = gray(nat)
    b = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((s, s), Image.LANCZOS))
    al = np.asarray(nat)[..., 3] / 255.0
    yy, xx = np.mgrid[0:s, 0:s]
    cx, cy = (xx + 0.5) * 1024.0 / s, (yy + 0.5) * 1024.0 / s
    ly = NX * (cx - AX) + NY * (cy - AY)
    tpar = (cx + cy) / (1024.0 * 2.0)
    base = np.interp(tpar, off, lv)
    plane = (ly <= 0) & (al > 0.5)
    print("\n%dpx  baseline ssim %.4f  self_contrast %.4f" % (s, ssim(a, b), np.percentile(a, 90) - np.percentile(a, 10)))
    for k in (1.35, 1.5, 1.6, 1.85, 2.1):
        new = PIVOT + k * (base - PIVOT)
        ratio = np.where(plane, new / base, 1.0)
        a2 = a * ratio
        print("   k=%.2f  ssim %.4f  self_contrast %.4f  mean|d| %.4f  plane mean %.4f (was %.4f)"
              % (k, ssim(a2, b), np.percentile(a2, 90) - np.percentile(a2, 10),
                 np.abs(a2 - b).mean(), a2[plane].mean(), a[plane].mean()))
