"""Single-light audit: corners, faces, and the reference's own cast shadow.

Everything registered to each image's own block, because the two blocks are
different sizes and sit in different places.
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


gc, cc = load(B / 'candidate-1024.png')
gr, cr = load(B / 'reference-1024.png')
refblock = np.load(B / 'refblock.npy')

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def polymask(pts, nn=1024):
    im = Image.new('L', (nn, nn), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im) > 127


OURS = polymask(bi.SILHOUETTE)
TOPM = polymask(bi.TOP)
CURL = polymask(bi.SHAVING_SIL)

print('=== corner ground patches (80x80, inset 40 from the tile corner) ===')
print(f'{"corner":<8}{"cand":>8}{"ref":>8}{"ratio to own brightest corner":>34}')
cor = {'TL': (40, 40), 'TR': (904, 40), 'BL': (40, 904), 'BR': (904, 904)}
vals = {}
for k, (x0, y0) in cor.items():
    vals[k] = (gc[y0:y0+80, x0:x0+80].mean(), gr[y0:y0+80, x0:x0+80].mean())
mc = max(v[0] for v in vals.values()); mr = max(v[1] for v in vals.values())
for k, (a_, b_) in vals.items():
    print(f'{k:<8}{a_:8.3f}{b_:8.3f}       cand {a_/mc:.2f}   ref {b_/mr:.2f}')
print('  (single-light predicate: the corner nearest the key -- TL -- must be the brightest)')

print('\n=== each image\'s brightest ground, located ===')
for nm, g, blk in (('cand', gc, OURS | CURL), ('ref ', gr, refblock)):
    gg = g.copy(); gg[blk] = -1
    k = 24
    # coarse 32x32 block means, ignore the block
    bm = np.full((32, 32), -1.0)
    for r in range(32):
        for c in range(32):
            p = gg[r*32:(r+1)*32, c*32:(c+1)*32]
            p = p[p >= 0]
            if p.size > 400:
                bm[r, c] = p.mean()
    i = np.unravel_index(np.argmax(bm), bm.shape)
    print(f'{nm}: brightest 32x32 ground cell at canvas ({i[1]*32+16},{i[0]*32+16}) = {bm[i]:.3f}'
          f'   median ground {np.median(gg[gg>=0]):.3f}')

print('\n=== block faces, each in its own frame ===')
# ours: top face vs front face (from geometry)
FRONT = polymask(bi.FRONT_FACE) & ~TOPM
print(f'ours  top face L {gc[TOPM & ~CURL].mean():.3f} (p5 {np.percentile(gc[TOPM&~CURL],5):.3f} '
      f'p95 {np.percentile(gc[TOPM&~CURL],95):.3f})   front face L {gc[FRONT].mean():.3f}')
# reference: split its block at the hone. Find, per column, the brightest warm row (the hone),
# call everything above it top face and below it front face.
warm = (cr[..., 0] - cr[..., 2] > 0.18) & (cr[..., 0] > 0.45)
rows = []
for c in range(230, 828):
    col = np.nonzero(warm[:, c])[0]
    if col.size:
        rows.append((c, int(col.mean())))
if rows:
    xs_ = np.array([r[0] for r in rows]); ys_ = np.array([r[1] for r in rows])
    k_, b_ = np.polyfit(xs_, ys_, 1)
    print(f'ref hone line: y = {k_:.4f}x + {b_:.1f}  ({math.degrees(math.atan2(-k_,1)):.2f} deg), '
          f'{len(rows)} columns, x[{xs_.min()},{xs_.max()}]')
    yy, xx = np.mgrid[0:1024, 0:1024]
    honey = k_ * xx + b_
    rtop = refblock & (yy < honey - 8)
    rfront = refblock & (yy >= honey - 8)
    print(f'ref   top face L {gr[rtop].mean():.3f} (p5 {np.percentile(gr[rtop],5):.3f} '
          f'p95 {np.percentile(gr[rtop],95):.3f})   front/under L {gr[rfront].mean():.3f}'
          f'   [{rtop.sum()} / {rfront.sum()} px]')
    np.save(B / 'reftop.npy', rtop)

print('\n=== the reference\'s cast shadow on its own trued ground ===')
yy, xx = np.mgrid[0:1024, 0:1024]
# reference trued side = below its hone line, excluding its block
rtrued = (yy > k_ * xx + b_ + 10) & ~refblock
d = np.full((1024, 1024), 1e9)
bys, bxs = np.nonzero(refblock)
sub = np.random.default_rng(0).choice(len(bys), 2500, replace=False)
for i in sub:
    d = np.minimum(d, np.hypot(xx - bxs[i], yy - bys[i]))
far = np.median(gr[rtrued & (d > 260)])
print(f'ref trued far field (>260px from its block) = {far:.3f}')
for a_, b2 in [(0, 15), (15, 35), (35, 60), (60, 100), (100, 160), (160, 260), (260, 400)]:
    m = rtrued & (d >= a_) & (d < b2)
    if m.sum() > 300:
        print(f'  {a_:>3}-{b2:<4}px  L {np.median(gr[m]):.3f}   x far {np.median(gr[m])/far:.3f}   ({m.sum()} px)')
np.save(B / 'refdist.npy', d); np.save(B / 'reftrued.npy', rtrued)
