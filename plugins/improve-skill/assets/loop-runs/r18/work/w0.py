"""Native small-size rsvg render vs LANCZOS downsample of the 1024 render.

The scorer renders SVG candidates NATIVELY at each size (fidelity.py:51-62),
so anything that aliases in the rasteriser at 32/16 is scored, and the 1024
render is not evidence about it. This asks how big that difference is.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def native(size, src="icon.svg"):
    t = pathlib.Path(tempfile.mkdtemp()) / ("n%d.png" % size)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), src, "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


big = native(1024)
for s in (128, 32, 16):
    nat = native(s)
    down = big.resize((s, s), Image.LANCZOS)
    a, b = gray(nat), gray(down)
    d = a - b
    print("%dpx native-vs-downsampled: mean|d| %.4f  max|d| %.4f  p99 %.4f  signed mean %+.4f"
          % (s, np.abs(d).mean(), np.abs(d).max(), np.percentile(np.abs(d), 99), d.mean()))
    if s == 32:
        np.save("loop-runs/r18/work/alias32.npy", d)
        idx = np.argsort(np.abs(d).ravel())[::-1][:12]
        ys, xs = np.unravel_index(idx, d.shape)
        for y, x in zip(ys, xs):
            print("    cell (%2d,%2d) native %.3f down %.3f d %+.3f" % (x, y, a[y, x], b[y, x], d[y, x]))
