"""The 32px edge ledger, and what each false positive is standing on.

edge_f1 carries 0.35 of the small-size composite and sits at 0.9336 with 20 FPs
(r17). This re-derives the sets with fidelity.py's own definitions, maps each FP
and FN back to the 32x32 canvas block it came from, and reports the reference's
own |grad| there - a candidate edge the reference has no gradient for is ours to
remove; one where the reference has a gradient too is registration.
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


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


NAMES = ["rough", "trued", "block", "hone", "curl"]

for s in (32, 16):
    a = gray(native(s))
    b = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((s, s), Image.LANCZOS))
    ga, gb = sobel(a), sobel(b)
    keep = ~rim_mask(s)
    ea, eb = (ga > 0.10) & keep, (gb > 0.10) & keep
    tp_p = (ea & dilate(eb)).sum()
    tp_r = (eb & dilate(ea)).sum()
    prec, rec = tp_p / max(ea.sum(), 1), tp_r / max(eb.sum(), 1)
    f1 = 2 * prec * rec / max(prec + rec, 1e-9)
    print("\n%dpx  cand edges %d  ref edges %d   prec %.4f  rec %.4f  f1 %.4f"
          % (s, ea.sum(), eb.sum(), prec, rec, f1))
    fp = ea & ~dilate(eb)
    fn = eb & ~dilate(ea)
    print("  FP %d   FN %d" % (fp.sum(), fn.sum()))
    lab = np.load("loop-runs/r18/work/lab%d.npy" % s)
    ys, xs = np.nonzero(fp)
    for y, x in zip(ys, xs):
        print("    FP (%2d,%2d) %-6s  ours |g| %.3f  ref |g| %.3f   ours L %.3f ref L %.3f"
              % (x, y, NAMES[lab[y, x]], ga[y, x], gb[y, x], a[y, x], b[y, x]))
    ys, xs = np.nonzero(fn)
    for y, x in zip(ys, xs):
        print("    FN (%2d,%2d) %-6s  ours |g| %.3f  ref |g| %.3f   ours L %.3f ref L %.3f"
              % (x, y, NAMES[lab[y, x]], ga[y, x], gb[y, x], a[y, x], b[y, x]))
    # what f1 would be if the n weakest FPs were removed
    for drop in (2, 4, 6, 10):
        w = np.sort(ga[fp])[:drop]
        if len(w) == 0:
            continue
        cut = w[-1]
        ea2 = ea & ~(fp & (ga <= cut))
        tp2 = (ea2 & dilate(eb)).sum()
        tr2 = (eb & dilate(ea2)).sum()
        p2, r2 = tp2 / max(ea2.sum(), 1), tr2 / max(eb.sum(), 1)
        print("  drop the %2d weakest FPs (|g|<=%.3f): f1 %.4f  (+%.4f)"
              % (drop, cut, 2 * p2 * r2 / max(p2 + r2, 1e-9), 2 * p2 * r2 / max(p2 + r2, 1e-9) - f1))
