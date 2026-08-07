"""Post-build checks: did the render land on the designed profile, and did the
rubric items the gate cannot see (corner ordering, figure-ground) move?"""
import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]
CURLBOX = (X >= 178) & (X <= 492) & (Y >= 50) & (Y <= 414)


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    rgb = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2], a[..., 3]


def dil(m, r):
    o = m.copy()
    for dy in range(-r, r + 1, max(1, r // 6)):
        for dx in range(-r, r + 1, max(1, r // 6)):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


REF_R = np.array([0, 35, 65, 95, 125, 155, 185, 230, 290, 350, 410, 470, 530,
                  590, 650, 710, 770, 830, 890, 1500], float)
REF_L = np.array([.940, .9166, .8915, .8651, .8412, .8152, .7845, .7521, .7179, .6813,
                  .6523, .6500, .6250, .6016, .5778, .5655, .5655, .5643, .5483, .5483])
R = np.sqrt((X - 75.0) ** 2 + (Y - 25.0) ** 2)

TAKES = (('C2 reference', 'loop-runs/r07/reference-1024.png',
          Y - (-0.8026 * X + 991.2), CURLBOX),
         ('r07 baseline ', 'loop-runs/r07/candidate-1024.png',
          Y - (604 - math.tan(math.radians(33.0)) * (X - 543)), np.zeros((H, W), bool)),
         ('r08 candidate', 'icon.png',
          Y - (604 - math.tan(math.radians(33.0)) * (X - 543)), np.zeros((H, W), bool)))

for name, path, fline, box in TAKES:
    g, a = load(path)
    tile = (a > 0.95) & (X > 22) & (X < 1002) & (Y > 22) & (Y < 1002)
    blk = dil(g < 0.45, 55)
    rough = tile & ~blk & (fline < -45) & ~box
    trued = tile & ~blk & (fline > 45) & ~box
    ground = rough | trued
    gm = g[ground].mean()

    print('== %s ==' % name)
    print('   ground mean %.4f   rough %.4f  trued %.4f  (trued/rough %.3f)'
          % (gm, g[rough].mean(), g[trued].mean(), g[trued].mean() / g[rough].mean()))

    # corner ratios against each icon's OWN ground mean (round 10's predicate)
    C = 150
    for cn, sel in (('TL', (X < C) & (Y < C)), ('TR', (X > W - C) & (Y < C)),
                    ('BL', (X < C) & (Y > H - C)), ('BR', (X > W - C) & (Y > H - C))):
        s = ground & sel
        if s.sum() > 200:
            print('   %s %.3fx' % (cn, g[s].mean() / gm), end='')
    print()

    # figure-ground: block vs each field
    body = tile & (g < 0.45)
    if body.sum() > 500:
        bl = g[body].mean()
        print('   figure-ground  vs rough %.2f:1  vs trued %.2f:1  fields %.2f:1'
              % (g[rough].mean() / bl, g[trued].mean() / bl,
                 g[trued].mean() / g[rough].mean()))

    # designed-vs-rendered profile along r (candidate only)
    if name.startswith('r08'):
        print('   rendered f(r) vs C2 (rough side, block out):')
        for r0 in range(50, 950, 100):
            s = rough & (R >= r0) & (R < r0 + 100)
            if s.sum() < 400:
                continue
            print('      r %4d  ours %.4f   C2 %.4f   %+.4f'
                  % (r0 + 50, g[s].mean(), np.interp(r0 + 50, REF_R, REF_L),
                     g[s].mean() - np.interp(r0 + 50, REF_R, REF_L)))
    print()
