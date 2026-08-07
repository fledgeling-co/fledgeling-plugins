"""Per-cell SSIM map at 32 and 16 on the native renders, split into its three
factors (luminance / contrast / structure), and attributed to the regions from
w1. SSIM carries 0.25 of the small-size composite and sits at 0.60/0.63, which
is the only unpinned term left at those sizes; this asks which factor and which
region is spending it.
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


NAMES = ["rough", "trued", "block", "hone", "curl"]

for s in (32, 16):
    a = gray(native(s))
    b = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((s, s), Image.LANCZOS))
    w = max(3, min(11, s // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    mu_a, mu_b = box_mean(a, w), box_mean(b, w)
    va = box_mean(a * a, w) - mu_a ** 2
    vb = box_mean(b * b, w) - mu_b ** 2
    cov = box_mean(a * b, w) - mu_a * mu_b
    lum = (2 * mu_a * mu_b + c1) / (mu_a ** 2 + mu_b ** 2 + c1)
    cs = (2 * cov + c2) / (va + vb + c2)
    smap = np.clip(lum * cs, -1, 1)
    lab = np.load("loop-runs/r18/work/lab%d.npy" % s)
    print("\n%dpx window=%d   SSIM %.4f   (lum factor %.4f, contrast-structure factor %.4f)"
          % (s, w, smap.mean(), lum.mean(), cs.mean()))
    for i, k in enumerate(NAMES):
        sel = lab == i
        if not sel.any():
            continue
        print("   %-6s cells %4d  ssim %.3f  lum %.3f  cs %.3f   sd_ours %.4f sd_ref %.4f cov %+.5f"
              % (k, sel.sum(), smap[sel].mean(), lum[sel].mean(), cs[sel].mean(),
                 np.sqrt(np.maximum(va[sel], 0)).mean(), np.sqrt(np.maximum(vb[sel], 0)).mean(), cov[sel].mean()))
    np.save("loop-runs/r18/work/ssim%d.npy" % s, smap)
    if s == 32:
        # the 20 worst windows, with what they contain
        idx = np.argsort(smap.ravel())[:16]
        ys, xs = np.unravel_index(idx, smap.shape)
        print("   worst windows:")
        for y, x in zip(ys, xs):
            print("     (%2d,%2d) %-6s ssim %+.3f  ours %.3f ref %.3f  sd_o %.3f sd_r %.3f cov %+.4f"
                  % (x, y, NAMES[lab[y, x]], smap[y, x], a[y, x], b[y, x],
                     np.sqrt(max(va[y, x], 0)), np.sqrt(max(vb[y, x], 0)), cov[y, x]))
