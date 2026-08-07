"""Fit each image's ground illumination as a plane, per side.

L = a + b*x + c*y over each side's ground pixels; the gradient (b,c) is the
key's direction and its magnitude is the falloff rate per 1000px. Robust to the
reference's texture because it is a least-squares fit over ~300k pixels.
"""
import numpy as np, sys, pathlib, importlib.util, math
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
NEUTRAL = 128 / 255.


def load(p, n=1024):
    im = Image.open(p).convert('RGBA')
    if n != im.width:
        im = im.resize((n, n), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2], comp


gc, _ = load(B / 'candidate-1024.png')
gr, _ = load(B / 'reference-1024.png')
refblock = np.load(B / 'refblock.npy')
rtrued = np.load(B / 'reftrued.npy')
refdist = np.load(B / 'refdist.npy')

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def polymask(pts, nn=1024):
    im = Image.new('L', (nn, nn), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im) > 127


yy, xx = np.mgrid[0:1024, 0:1024]
OURS = polymask(bi.SILHOUETTE) | polymask(bi.SHAVING_SIL)
BOUND = bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * xx / 1024.
C_TRUED = (yy > BOUND + 20) & ~OURS
C_ROUGH = (yy <= BOUND - 20) & ~OURS
# reference sides, from its own fitted hone line y = 0.8917x + 41.0
R_TRUED = rtrued & (refdist > 45)
R_ROUGH = (yy < 0.8917 * xx + 41.0 - 10) & ~refblock & (refdist > 45)


def fit(g, m, label):
    Y = g[m]
    X = np.stack([np.ones(m.sum()), xx[m] / 1000., yy[m] / 1000.], 1)
    coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
    a, b, c = coef
    mag = math.hypot(b, c)
    ang = math.degrees(math.atan2(-c, -b))   # direction of INCREASING brightness
    pred = X @ coef
    print(f'{label:<16} L(centre) {a + 0.512*b + 0.512*c:5.3f}   falloff {mag:5.3f} per 1000px'
          f'   brightening toward {ang:6.1f} deg   resid sd {np.std(Y-pred):.3f}')
    return coef


print('=== ground illumination planes (0 deg = +x right, 90 deg = up) ===')
cr_t = fit(gc, C_TRUED, 'cand trued')
cr_r = fit(gc, C_ROUGH, 'cand rough')
rr_t = fit(gr, R_TRUED, 'ref  trued')
rr_r = fit(gr, R_ROUGH, 'ref  rough')

print('\n=== the same fit as a corner-to-corner swing on each side ===')
for nm, coef, m in (('cand trued', cr_t, C_TRUED), ('cand rough', cr_r, C_ROUGH),
                    ('ref  trued', rr_t, R_TRUED), ('ref  rough', rr_r, R_ROUGH)):
    a, b, c = coef
    ys_, xs_ = np.nonzero(m)
    lo = a + b * xs_.min() / 1000 + c * ys_.min() / 1000
    corners = [(a + b * X / 1000 + c * Y / 1000) for X, Y in
               ((xs_.min(), ys_.min()), (xs_.max(), ys_.min()), (xs_.min(), ys_.max()), (xs_.max(), ys_.max()))]
    print(f'{nm:<12} fitted TL {corners[0]:.3f}  TR {corners[1]:.3f}  BL {corners[2]:.3f}  BR {corners[3]:.3f}'
          f'   (max-min {max(corners)-min(corners):.3f})')
