"""Reference measurements, redone on the correct split line (y = -0.8026x + 991.2).

Faces of each block in its own frame; each side's ground plane fit; the
reference's contact profile around its own block.
"""
import numpy as np, sys, pathlib, importlib.util, math
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2], comp


gc, cc = load(B / 'candidate-1024.png')
gr, cr = load(B / 'reference-1024.png')
refblock = np.load(B / 'refblock.npy')
refdist = np.load(B / 'refdist.npy')
K, BB = np.load(B / 'honeline.npy')

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def polymask(pts, nn=1024):
    im = Image.new('L', (nn, nn), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im) > 127


yy, xx = np.mgrid[0:1024, 0:1024]
OURS = polymask(bi.SILHOUETTE); CURL = polymask(bi.SHAVING_SIL)
TOPM = polymask(bi.TOP); FRONTM = polymask(bi.FRONT_FACE) & ~TOPM
CBOUND = bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * xx / 1024.
C_TRUED = (yy > CBOUND + 20) & ~OURS & ~CURL
C_ROUGH = (yy <= CBOUND - 20) & ~OURS & ~CURL
RLINE = K * xx + BB
R_TRUED = (yy > RLINE + 20) & ~refblock
R_ROUGH = (yy <= RLINE - 20) & ~refblock

print('=== block faces, each block split at its own hone ===')
rtop = refblock & (yy < RLINE - 6)
rfront = refblock & (yy >= RLINE - 6)
print(f'ours  top {gc[TOPM&~CURL].mean():.3f}   front {gc[FRONTM].mean():.3f}'
      f'   top-front {gc[TOPM&~CURL].mean()-gc[FRONTM].mean():+.3f}'
      f'   block mean {gc[OURS].mean():.3f}   [{(TOPM&~CURL).sum()} / {FRONTM.sum()} px]')
print(f'ref   top {gr[rtop].mean():.3f}   front {gr[rfront].mean():.3f}'
      f'   top-front {gr[rtop].mean()-gr[rfront].mean():+.3f}'
      f'   block mean {gr[refblock].mean():.3f}   [{rtop.sum()} / {rfront.sum()} px]')
for nm, g, m in (('ours top', gc, TOPM & ~CURL), ('ref  top', gr, rtop),
                 ('ours front', gc, FRONTM), ('ref  front', gr, rfront)):
    v = g[m]
    print(f'   {nm:<11} p5 {np.percentile(v,5):.3f}  p25 {np.percentile(v,25):.3f}'
          f'  p50 {np.percentile(v,50):.3f}  p75 {np.percentile(v,75):.3f}  p95 {np.percentile(v,95):.3f}')

print('\n=== ground planes, correct sides (angle = direction of increasing L) ===')


def fit(g, m, label):
    Y = g[m]
    X = np.stack([np.ones(int(m.sum())), xx[m] / 1000., yy[m] / 1000.], 1)
    coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
    a, b, c = coef
    print(f'{label:<12} falloff {math.hypot(b,c):5.3f}/1000px  toward {math.degrees(math.atan2(-c,-b)):6.1f} deg'
          f'  L at tile TL {a:.3f}  TR {a+b:.3f}  BL {a+c:.3f}  BR {a+b+c:.3f}   mean {Y.mean():.3f}')
    return coef


fit(gc, C_TRUED, 'cand trued'); fit(gc, C_ROUGH, 'cand rough')
fit(gr, R_TRUED, 'ref  trued'); fit(gr, R_ROUGH, 'ref  rough')
print('  (TL/TR/BL/BR are the fitted plane evaluated at the four TILE corners, comparable across rows)')

print('\n=== the reference block\'s own contact profile ===')
far = np.median(gr[R_TRUED & (refdist > 260)])
print(f'ref trued far field {far:.3f}')
for a_, b2 in [(0, 15), (15, 35), (35, 60), (60, 100), (100, 160), (160, 260)]:
    m = R_TRUED & (refdist >= a_) & (refdist < b2)
    if m.sum() > 300:
        print(f'  {a_:>3}-{b2:<4}px  L {np.median(gr[m]):.3f}  x far {np.median(gr[m])/far:.3f}  ({m.sum()} px)')
mr = R_ROUGH & (refdist > 260)
print(f'ref rough far field {np.median(gr[mr]):.3f}')
for a_, b2 in [(0, 15), (15, 35), (35, 60), (60, 100), (100, 160)]:
    m = R_ROUGH & (refdist >= a_) & (refdist < b2)
    if m.sum() > 300:
        print(f'  {a_:>3}-{b2:<4}px  L {np.median(gr[m]):.3f}  x far '
              f'{np.median(gr[m])/np.median(gr[mr]):.3f}  ({m.sum()} px)')
np.save(B / 'sides.npy', np.stack([C_TRUED, C_ROUGH, R_TRUED, R_ROUGH, TOPM & ~CURL, FRONTM, OURS, CURL]))
