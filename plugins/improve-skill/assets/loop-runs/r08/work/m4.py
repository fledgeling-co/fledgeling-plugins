import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    return rgb * al + NEUTRAL * (1 - al), a[..., 3]


rgb_c, ac = load('loop-runs/r07/candidate-1024.png')
g1024 = 0.2126 * rgb_c[..., 0] + 0.7152 * rgb_c[..., 1] + 0.0722 * rgb_c[..., 2]
H, W = g1024.shape
Y, X = np.mgrid[0:H, 0:W]
f_o = Y - (604 - math.tan(math.radians(33.0)) * (X - 543))
blk = g1024 < 0.45
regions = {
    'block': blk,
    'trued': (~blk) & (f_o > 0) & (ac > 0.9),
    'rough': (~blk) & (f_o <= 0) & (ac > 0.9),
    'outside': ac <= 0.9,
}

for size in (32, 16, 128):
    # fidelity.py renders the svg at each size; approximate with area-average downsample
    im = Image.fromarray((g1024 * 255).astype(np.uint8)).resize((size, size), Image.BOX)
    g = np.asarray(im).astype(np.float64) / 255.0
    lab = np.zeros((size, size), dtype=object)
    ids = {}
    for i, (k, m) in enumerate(regions.items()):
        mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((size, size), Image.BOX)).astype(np.float64)
        ids[k] = mm
    owner = max(ids, key=lambda k: 0)
    stack = np.stack([ids[k] for k in regions], 0)
    who = np.argmax(stack, 0)
    names = list(regions)
    p90, p10 = np.percentile(g, 90), np.percentile(g, 10)
    hi, lo = g >= p90, g <= p10
    print('size %d  p90 %.3f p10 %.3f  spread %.4f' % (size, p90, p10, p90 - p10))
    for i, n in enumerate(names):
        s90 = ((who == i) & hi).sum() / max(hi.sum(), 1)
        s10 = ((who == i) & lo).sum() / max(lo.sum(), 1)
        print('   %-8s share of p90-set %5.1f%%   of p10-set %5.1f%%' % (n, 100 * s90, 100 * s10))
