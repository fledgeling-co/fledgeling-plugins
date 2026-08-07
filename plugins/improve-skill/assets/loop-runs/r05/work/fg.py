import numpy as np, math, sys
from PIL import Image

# figure-ground, measured through one pipeline for both files.
# WCAG contrast between the block's median and each ground field's median.


def load(p, size):
    im = Image.open(p).convert('RGBA').resize((size, size), Image.LANCZOS)
    return np.asarray(im, float) / 255


def lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def relY(a):
    return 0.2126 * lin(a[..., 0]) + 0.7152 * lin(a[..., 1]) + 0.0722 * lin(a[..., 2])


def ratio(y1, y2):
    a, b = max(y1, y2), min(y1, y2)
    return (a + 0.05) / (b + 0.05)


for p in sys.argv[1:]:
    print('---', p)
    for size in (128, 32, 16):
        a = load(p, size)
        al = a[..., 3]
        Yv = relY(a)
        inside = al > 0.98
        n = size
        Y, X = np.mgrid[0:n, 0:n]
        ang = math.radians(33.0)
        V = -math.sin(ang) * X * (1024 / n) - math.cos(ang) * (Y * (1024 / n) - 956.6)
        blk = inside & (Yv < np.percentile(Yv[inside], 22))
        up = inside & (~blk) & (V > 60)
        tr = inside & (~blk) & (V < -60)
        mb, mu, mt = np.median(Yv[blk]), np.median(Yv[up]), np.median(Yv[tr])
        print('  %3dpx  block Y %.3f  un-planed %.3f (%.2f:1)  trued %.3f (%.2f:1)'
              % (size, mb, mu, ratio(mu, mb), mt, ratio(mt, mb)))
        if size == 16:
            # vermilion footprint: strongly warm pixels
            r, g, b = a[..., 0], a[..., 1], a[..., 2]
            verm = inside & (r > 0.45) & (r - b > 0.16)
            print('        16px vermilion footprint %.2f%% of tile' % (100 * verm.mean()))
