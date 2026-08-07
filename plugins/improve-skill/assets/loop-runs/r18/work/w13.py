"""What is actually stepping at the curl's upper-left rim, in ours and in the reference.

w10 pinned four of the 32px false positives on the shaving: cells (7,7) (8,7) (9,7) (6,8),
ours |grad| 0.138-0.164 against the reference's 0.046-0.082, collapsing to 0.014-0.026 with
the layer off. Before touching it, this walks a line outward from the roll's centre through
each of those cells and prints L every 4px in both images, so the step's height, its width,
and what sits either side of it are read rather than inferred.
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


t = TMP / "n.png"
subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", "icon.svg", "-o", str(t)], check=True)
g1 = gray(Image.open(t).convert("RGBA"))
gr1 = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))

CX, CY = 308.0, 278.0
CELLS = [(7, 7), (8, 7), (9, 7), (6, 8)]


def samp(g, x, y):
    xi, yi = int(round(x)), int(round(y))
    if 0 <= xi < 1024 and 0 <= yi < 1024:
        return g[yi, xi]
    return float("nan")


for cx32, cy32 in CELLS:
    px, py = (cx32 + 0.5) * 32.0, (cy32 + 0.5) * 32.0
    dx, dy = px - CX, py - CY
    m = math.hypot(dx, dy)
    ux, uy = dx / m, dy / m
    print("\ncell (%d,%d) -> canvas (%.0f,%.0f), %.0fpx from the roll centre, outward (%.2f,%.2f)"
          % (cx32, cy32, px, py, m, ux, uy))
    print("   s     x     y     ours     ref")
    for s in range(-56, 57, 4):
        x, y = px + ux * s, py + uy * s
        print("  %+4d  %4.0f  %4.0f   %.4f   %.4f" % (s, x, y, samp(g1, x, y), samp(gr1, x, y)))
    # the step as the 32px sobel sees it: 32px cell means over the 3x3 neighbourhood
    print("  32px cell means, ours / ref:")
    for dy32 in (-1, 0, 1):
        row_o, row_r = [], []
        for dx32 in (-1, 0, 1):
            x0, y0 = (cx32 + dx32) * 32, (cy32 + dy32) * 32
            row_o.append(g1[y0:y0 + 32, x0:x0 + 32].mean())
            row_r.append(gr1[y0:y0 + 32, x0:x0 + 32].mean())
        print("    " + "  ".join("%.4f" % v for v in row_o) + "     " + "  ".join("%.4f" % v for v in row_r))
