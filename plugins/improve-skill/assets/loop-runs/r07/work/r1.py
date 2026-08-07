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
d = np.abs(gc - gr)
print('lum_delta whole: %.4f' % d.mean())
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]

ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang) * (X - 543))
f_ref = Y - (-0.8026 * X + 991.2)

blk_c = gc < 0.45
blk_r = gr < 0.45
print('block frac ours %.3f ref %.3f' % (blk_c.mean(), blk_r.mean()))

regions = [
    ('both-block', blk_c & blk_r),
    ('ours-block-only', blk_c & ~blk_r),
    ('ref-block-only', ~blk_c & blk_r),
    ('ground-trued(f>0)', (~blk_c) & (~blk_r) & (f_ours > 0)),
    ('ground-rough(f<=0)', (~blk_c) & (~blk_r) & (f_ours <= 0)),
]
print('%-22s %6s %8s %8s %7s %7s' % ('region', 'frac', 'mean|d|', 'contrib', 'ourL', 'refL'))
for k, m in regions:
    if m.sum() == 0:
        continue
    print('%-22s %6.3f %8.4f %8.4f %7.3f %7.3f'
          % (k, m.mean(), d[m].mean(), d[m].sum() / d.size, gc[m].mean(), gr[m].mean()))
