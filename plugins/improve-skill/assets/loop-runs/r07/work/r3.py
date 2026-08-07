import math
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def load(p):
    im = Image.open(p).convert('RGBA')
    a = np.asarray(im).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    rgb = rgb * al + NEUTRAL * (1 - al)
    g = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    return rgb, g


crgb, gc = load('loop-runs/r06/candidate-1024.png')
rrgb, gr = load('loop-runs/r06/reference-1024.png')
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]

ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang) * (X - 543))
f_ref = Y - (-0.8026 * X + 991.2)

blk_c, blk_r = gc < 0.45, gr < 0.45


def dilate(m, r):
    out = m.copy()
    for dy in range(-r, r + 1, max(1, r // 5)):
        for dx in range(-r, r + 1, max(1, r // 5)):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


bc, br = dilate(blk_c, 45), dilate(blk_r, 45)
alp = np.asarray(Image.open('loop-runs/r06/candidate-1024.png').convert('RGBA'))[..., 3] > 250
inner = alp & (X > 24) & (X < 1000) & (Y > 24) & (Y < 1000)

# ONE light axis: 45 deg out of the top-left corner. u = (x+y)/sqrt2
u = (X + Y) / math.sqrt(2.0)

sets = [
    ('rough', inner & (f_ours < -40) & (~bc), inner & (f_ref < -40) & (~br)),
    ('trued', inner & (f_ours > 40) & (~bc), inner & (f_ref > 40) & (~br)),
]
print('mean L along the 45deg light axis u=(x+y)/sqrt2, ground only, block dilated out')
for name, mo, mr in sets:
    print('\n== %s ==   %8s %8s %8s %8s' % (name, 'ours', 'ref', 'n_o', 'n_r'))
    for lo in range(0, 1500, 80):
        hi = lo + 80
        a = mo & (u >= lo) & (u < hi)
        b = mr & (u >= lo) & (u < hi)
        if a.sum() < 500 and b.sum() < 500:
            continue
        so = '%8.3f' % gc[a].mean() if a.sum() >= 500 else '       -'
        sr = '%8.3f' % gr[b].mean() if b.sum() >= 500 else '       -'
        print('  u %4d %s %s %8d %8d' % (lo, so, sr, a.sum(), b.sum()))

# overlap band: where both sides exist at the same u, the finish step
print('\nfinish step (trued - rough) at matched u:')
for lo in range(400, 1300, 80):
    hi = lo + 80
    ro = inner & (f_ours < -40) & (~bc) & (u >= lo) & (u < hi)
    to = inner & (f_ours > 40) & (~bc) & (u >= lo) & (u < hi)
    rr = inner & (f_ref < -40) & (~br) & (u >= lo) & (u < hi)
    tr = inner & (f_ref > 40) & (~br) & (u >= lo) & (u < hi)
    if min(ro.sum(), to.sum(), rr.sum(), tr.sum()) < 500:
        continue
    print('  u %4d  ours %+.3f (%.3f/%.3f)   ref %+.3f (%.3f/%.3f)'
          % (lo, gc[to].mean() - gc[ro].mean(), gc[to].mean(), gc[ro].mean(),
             gr[tr].mean() - gr[rr].mean(), gr[tr].mean(), gr[rr].mean()))
