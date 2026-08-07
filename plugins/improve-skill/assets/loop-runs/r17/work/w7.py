"""Attribution: which feature owns each small-size false-positive edge?

Runs the edge audit on the real master and on a probe variant, and reports which
FP cells the probe removes. A cell the probe clears is owned by whatever the
probe switched off.
"""
import subprocess
import sys
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def lum(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    c = a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def rsvg(svg, size):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


def sobel(g, thresh=0.10):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy)


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


def audit(svg, ref, s, verbose=False):
    gc, gr = lum(rsvg(svg, s)), lum(ref.resize((s, s), Image.LANCZOS))
    mc, mr = sobel(gc), sobel(gr)
    keep = ~rim_mask(s)
    ec, er = (mc > 0.4) & keep, (mr > 0.4) & keep
    fp, fn = ec & ~dilate(er), er & ~dilate(ec)
    prec = (ec & dilate(er)).sum() / max(ec.sum(), 1)
    rec = (er & dilate(ec)).sum() / max(er.sum(), 1)
    f1 = 2 * prec * rec / max(prec + rec, 1e-9)
    return dict(ec=ec, er=er, fp=fp, fn=fn, f1=f1, prec=prec, rec=rec, mc=mc, mr=mr)


ref = Image.open('icon-engineC-f5665d-2.png')
base = sys.argv[1]
probes = sys.argv[2:]
for s in (32, 128, 256):
    a = audit(base, ref, s)
    print(f'=== {s}px  base: edges {a["ec"].sum()} FP {a["fp"].sum()} FN {a["fn"].sum()} f1 {a["f1"]:.4f}')
    for p in probes:
        b = audit(p, ref, s)
        cleared = (a['fp'] & ~b['ec']).sum()
        print(f'    {pathlib.Path(p).name:26s} edges {b["ec"].sum():5d} FP {b["fp"].sum():5d} '
              f'FN {b["fn"].sum():5d} f1 {b["f1"]:.4f}   of base FP cleared: {cleared}/{a["fp"].sum()}')
    if s == 32:
        ys, xs = np.nonzero(a['fp'])
        print('    base FP cells (y,x) -> canvas box, cand|grad|, ref|grad|:')
        for y, x in zip(ys, xs):
            print(f'      ({y:2d},{x:2d}) canvas x{x*1024//s}-{(x+1)*1024//s} y{y*1024//s}-{(y+1)*1024//s}'
                  f'  cand {a["mc"][y,x]:.2f} ref {a["mr"][y,x]:.2f}')
