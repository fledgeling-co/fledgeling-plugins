"""The pivot: the area-weighted mean of the truedField ramp over the plane it paints.

Steepening the ramp about this value leaves the plane's mean luminance where it is,
which is the point. r17 refused a variant that scored better by paying the trued
plane's +0.17 palette fault with a shadow wash; a falloff edit that moved the mean
would be the same mistake in a different layer, so the pivot is computed rather
than guessed, and lum_delta is the falsifier afterwards.
"""
import subprocess
import tempfile
import pathlib
import math
import numpy as np
from PIL import Image

TMP = pathlib.Path(tempfile.mkdtemp())
t = TMP / "n.png"
subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", "icon.svg", "-o", str(t)], check=True)
im = Image.open(t).convert("RGBA")
alpha = np.asarray(im)[..., 3] > 8   # the whole squircle, rim included: the ramp paints it all

ANG = math.radians(33.0)
UXc, UYc = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX, AY = 543.0 - UXc * 320.0, 604.0 - UYc * 320.0
yy, xx = np.mgrid[0:1024, 0:1024]
ly = NX * (xx - AX) + NY * (yy - AY)
u = (xx + yy) / math.sqrt(2.0)

plane = alpha & (ly <= 0)
print("trued plane area %d px (%.1f%% of the tile), mean u %.1f, u range %.0f-%.0f"
      % (plane.sum(), 100 * plane.mean(), u[plane].mean(), u[plane].min(), u[plane].max()))

STOPS = [(0.4558, 660, 0.863), (0.5248, 760, 0.871), (0.5939, 860, 0.869),
         (0.6629, 960, 0.852), (0.7320, 1060, 0.848), (0.8010, 1160, 0.809),
         (0.8701, 1260, 0.747), (0.9391, 1360, 0.700), (0.9999, 1448, 0.683)]
off = np.array([s[0] for s in STOPS])
lv = np.array([s[2] for s in STOPS])
t_of_u = u / (1024.0 * math.sqrt(2.0))          # the gradient's own parameter
ramp = np.interp(t_of_u[plane], off, lv)        # flat-extended below the first stop, as SVG pads
print("ramp over the plane: area-weighted mean L %.4f   min %.4f  max %.4f" % (ramp.mean(), ramp.min(), ramp.max()))
# share of the plane sitting below the first stop, where the ramp is a flat pad
below = (t_of_u[plane] < off[0]).mean()
print("share of the plane below the first stop (flat pad): %.3f" % below)

for k in (1.35, 1.50, 1.60, 1.85):
    P = ramp.mean()
    new = P + k * (lv - P)
    print("\nk=%.2f  pivot %.4f" % (k, P))
    print("  u:      " + "  ".join("%6d" % s[1] for s in STOPS))
    print("  L old:  " + "  ".join("%6.3f" % v for v in lv))
    print("  L new:  " + "  ".join("%6.3f" % v for v in new))
    print("  ratio:  " + "  ".join("%6.3f" % (n / o) for n, o in zip(new, lv)))
    nr = np.interp(t_of_u[plane], off, new)
    print("  plane mean L after: %.4f (was %.4f)" % (nr.mean(), ramp.mean()))
