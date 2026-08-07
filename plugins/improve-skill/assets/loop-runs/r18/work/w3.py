"""Separate the squircle-rim windows from the artwork before reading SSIM.

edge_f1 already excludes the rim (fidelity.py:119 rim_mask) because a masked
SVG against a full-bleed raster measures the delivery format. SSIM does not
exclude it. This asks how much of the un-planed plane's 0.466 is that, and how
much is texture the round could actually repair.
"""
import subprocess
import tempfile
import pathlib
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


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


NAMES = ["rough", "trued", "block", "hone", "curl"]

for s in (32, 16):
    a = gray(native(s))
    b = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((s, s), Image.LANCZOS))
    alpha = np.asarray(native(s))[..., 3] / 255.0
    w = max(3, min(11, s // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    mu_a, mu_b = box_mean(a, w), box_mean(b, w)
    va = box_mean(a * a, w) - mu_a ** 2
    vb = box_mean(b * b, w) - mu_b ** 2
    cov = box_mean(a * b, w) - mu_a * mu_b
    smap = np.clip(((2 * mu_a * mu_b + c1) * (2 * cov + c2)) / ((mu_a ** 2 + mu_b ** 2 + c1) * (va + vb + c2)), -1, 1)
    lab = np.load("loop-runs/r18/work/lab%d.npy" % s)
    # a window is rim-contaminated if any cell it covers is not fully opaque
    part = box_mean((alpha < 0.995).astype(float), w) > 0
    rim = rim_mask(s)
    print("\n%dpx  SSIM all %.4f" % (s, smap.mean()))
    print("   windows touching a non-opaque cell: %d/%d, their ssim %.3f; the rest %.3f"
          % (part.sum(), part.size, smap[part].mean(), smap[~part].mean()))
    print("   rim_mask cells: %d, ssim %.3f; interior %.3f" % (rim.sum(), smap[rim].mean(), smap[~rim].mean()))
    for i, k in enumerate(NAMES):
        sel = (lab == i) & ~part
        if not sel.any():
            continue
        print("   %-6s clean cells %4d  ssim %.3f  sd_o %.4f sd_r %.4f cov %+.5f  corr %+.3f"
              % (k, sel.sum(), smap[sel].mean(),
                 np.sqrt(np.maximum(va[sel], 0)).mean(), np.sqrt(np.maximum(vb[sel], 0)).mean(),
                 cov[sel].mean(),
                 (cov[sel] / np.maximum(np.sqrt(np.maximum(va[sel], 0) * np.maximum(vb[sel], 0)), 1e-9)).mean()))
