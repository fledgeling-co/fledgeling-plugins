import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    rgb = rgb * al + NEUTRAL * (1 - al)
    return rgb, 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


crgb, gc = load('loop-runs/r07/candidate-1024.png')
rrgb, gr = load('loop-runs/r07/reference-1024.png')
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]
f_o = Y - (604 - math.tan(math.radians(33.0)) * (X - 543))
f_r = Y - (-0.8026 * X + 991.2)
blk_c, blk_r = gc < 0.45, gr < 0.45


def dil(m, r):
    o = m.copy()
    for dy in range(-r, r + 1, max(1, r // 6)):
        for dx in range(-r, r + 1, max(1, r // 6)):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


bc, br = dil(blk_c, 50), dil(blk_r, 50)
alp = np.asarray(Image.open('loop-runs/r07/candidate-1024.png').convert('RGBA'))[..., 3] > 250
inner = alp & (X > 28) & (X < 996) & (Y > 28) & (Y < 996)
u = (X + Y) / math.sqrt(2.0)
v = (X - Y) / math.sqrt(2.0)

print('ROUGH plane: ours/ref by (u band, v band). v<0 upper-right side, v>0 lower-left')
vbands = (-450, -300, -150, 0, 150, 300, 450)
print('%6s |' % 'u', ' '.join('%13s' % ('v' + str(vv)) for vv in vbands))
for u0 in range(40, 760, 100):
    row = []
    for v0 in vbands:
        m = (u >= u0) & (u < u0 + 100) & (v >= v0 - 75) & (v < v0 + 75)
        mo = m & inner & (f_o < -40) & (~bc)
        mr = m & inner & (f_r < -40) & (~br)
        a = gc[mo].mean() if mo.sum() > 200 else float('nan')
        b = gr[mr].mean() if mr.sum() > 200 else float('nan')
        row.append('%.3f/%.3f' % (a, b) if a == a and b == b else '   -   ')
    print('%6d |' % u0, ' '.join('%13s' % r for r in row))

print()
gnd_o = inner & (~bc)
gnd_r = inner & (~br)
mo_all, mr_all = gc[gnd_o].mean(), gr[gnd_r].mean()
print('ground mean ours %.3f ref %.3f' % (mo_all, mr_all))
for nm, (x0, y0) in (('TL', (60, 60)), ('TR', (830, 60)), ('BL', (60, 830)), ('BR', (830, 830))):
    m = (X >= x0) & (X < x0 + 134) & (Y >= y0) & (Y < y0 + 134)
    ao, ar = gc[m & gnd_o].mean(), gr[m & gnd_r].mean()
    print('  %s  ours %.3f (%.2f of own mean)   ref %.3f (%.2f)' % (nm, ao, ao / mo_all, ar, ar / mr_all))
