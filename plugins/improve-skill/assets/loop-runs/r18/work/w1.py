"""Where the 32/16px error actually lives, by region, on the NATIVE renders.

Regions are recovered from the build, not guessed:
  curl   = pixels that change when SHAVING=0
  block  = the dark solid, by the top/front face polygons (luminance-free)
  hone   = redness > 0.20
  ground = the rest, split by the 33 deg cut through EDGE_MID
Per-region mean offset is removed before the detrended residual, because the
palette fault (trued ground +0.18) would otherwise own every cell.
"""
import subprocess
import tempfile
import pathlib
import os
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


# --- build the no-shaving twin once, to recover the curl footprint exactly
if not pathlib.Path("loop-runs/r18/work/noshave.svg").exists():
    env = dict(os.environ, SHAVING="0")
    subprocess.run(["python3", "build_icon.py"], env=env, check=True, capture_output=True)
    pathlib.Path("loop-runs/r18/work/noshave.svg").write_bytes(pathlib.Path("icon.svg").read_bytes())
    subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

c1024 = native(1024)
n1024 = native(1024, "loop-runs/r18/work/noshave.svg")
gc, gn = gray(c1024), gray(n1024)
curl = np.abs(gc - gn) > 0.004

rgb = np.asarray(c1024.convert("RGB"), float) / 255.0
redness = rgb[..., 0] - 0.5 * (rgb[..., 1] + rgb[..., 2])
hone = redness > 0.20

import math
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX = 543.0 - UX * 320.0
AY = 604.0 - UY * 320.0
yy, xx = np.mgrid[0:1024, 0:1024]
ly = NX * (xx - AX) + NY * (yy - AY)

alpha = np.asarray(c1024)[..., 3] > 16
block = (gc < 0.45) & ~hone & ~curl & alpha
ground = alpha & ~block & ~hone & ~curl
rough = ground & (ly > 0)
trued = ground & (ly <= 0)

masks = {"rough": rough, "trued": trued, "block": block, "hone": hone, "curl": curl}
print("region shares at 1024:", {k: round(float(v.mean()), 4) for k, v in masks.items()})

ref = Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS)
gr = gray(ref)

print("\n1024 per-region means (ours / ref / delta), ref sampled on OUR mask:")
for k, m in masks.items():
    print("  %-6s n=%7d  ours %.3f  ref %.3f  d %+.3f" % (k, m.sum(), gc[m].mean(), gr[m].mean(), gc[m].mean() - gr[m].mean()))

# --- small sizes: downsample the masks by majority, score on native renders
for s in (32, 16):
    a = gray(native(s))
    b = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((s, s), Image.LANCZOS))
    f = 1024 // s
    d = a - b
    print("\n%dpx  mean|d| %.4f" % (s, np.abs(d).mean()))
    lab = np.zeros((s, s), int)
    frac = {}
    for i, (k, m) in enumerate(masks.items(), start=1):
        frac[k] = m.reshape(s, f, s, f).mean(axis=(1, 3))
    dom = max(frac, key=lambda k: 0)
    stack = np.stack([frac[k] for k in masks])
    lab = np.argmax(stack, axis=0)
    for i, k in enumerate(masks):
        sel = lab == i
        if sel.sum() == 0:
            continue
        dd = d[sel]
        print("   %-6s cells %4d  mean d %+.3f  mean|detrended| %.3f  worst %+.3f"
              % (k, sel.sum(), dd.mean(), np.abs(dd - dd.mean()).mean(), dd[np.argmax(np.abs(dd - dd.mean()))] - dd.mean()))
    np.save("loop-runs/r18/work/lab%d.npy" % s, lab)
    np.save("loop-runs/r18/work/d%d.npy" % s, d)
