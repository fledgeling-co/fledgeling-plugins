"""The top face's own shading, measured in each block's own frame.

u = along the block's length from its leading end (normalised 0..1)
v = across the top face from the hone side to the back edge (normalised 0..1)
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
K, BB = np.load(B / 'honeline.npy')
sides = np.load(B / 'sides.npy')
C_TRUED, C_ROUGH, R_TRUED, R_ROUGH, TOPM, FRONTM, OURS, CURL = sides
yy, xx = np.mgrid[0:1024, 0:1024]
rtop = refblock & (yy < K * xx + BB - 6)
rfront = refblock & (yy >= K * xx + BB - 6)


def frame(mask, ang_deg):
    """u along the hone direction, v perpendicular (positive away from the hone)."""
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), -math.sin(a)
    nx, ny = -math.sin(a), -math.cos(a)
    ys_, xs_ = np.nonzero(mask)
    u = ux * xs_ + uy * ys_
    v = nx * xs_ + ny * ys_
    return xs_, ys_, (u - u.min()) / (u.max() - u.min()), (v - v.min()) / (v.max() - v.min())


print('=== top face shading, 4x3 cells: u = along length (leading->trailing), v = hone edge -> back edge ===')
for nm, g, m, ang in (('ours', gc, TOPM, 33.0), ('ref ', gr, rtop, 38.75)):
    xs_, ys_, u, v = frame(m, ang)
    L = g[ys_, xs_]
    print(f'{nm}  (mean {L.mean():.3f})')
    for vi in range(2, -1, -1):
        row = []
        for ui in range(4):
            s = (u >= ui / 4) & (u < (ui + 1) / 4) & (v >= vi / 3) & (v < (vi + 1) / 3)
            row.append(f'{L[s].mean():.3f}' if s.sum() > 200 else '  .  ')
        print(f'   v{vi} (back edge)  ' if vi == 2 else f'   v{vi}             ', ' '.join(row))
    print(f'   {"":<17} u0    u1    u2    u3')

print('\n=== front face, same frame ===')
for nm, g, m, ang in (('ours', gc, FRONTM, 33.0), ('ref ', gr, rfront, 38.75)):
    xs_, ys_, u, v = frame(m, ang)
    L = g[ys_, xs_]
    print(f'{nm} (mean {L.mean():.3f}): ' +
          ' '.join(f'u{ui}={L[(u>=ui/4)&(u<(ui+1)/4)].mean():.3f}' for ui in range(4)))

print('\n=== darkest-end hue check (prior learning 1) ===')
for nm, g, c, m in (('ours top', gc, cc, TOPM), ('ref  top', gr, cr, rtop),
                    ('ours front', gc, cc, FRONTM), ('ref  front', gr, cr, rfront)):
    v = g[m]
    q = np.percentile(v, 3)
    sel = m & (g <= q)
    rgbv = c[sel].mean(0)
    sat = (rgbv.max() - rgbv.min()) / max(rgbv.max(), 1e-6)
    print(f'   {nm:<11} darkest 3%: rgb {rgbv.round(3)}  L {v[v<=q].mean():.3f}  sat {sat:.3f}'
          f'  R-B {rgbv[0]-rgbv[2]:+.3f}')
    v2 = g[m]; q2 = np.percentile(v2, 97)
    rgbv = c[m & (g >= q2)].mean(0)
    print(f'   {"":<11} lightest 3%: rgb {rgbv.round(3)}  L {v2[v2>=q2].mean():.3f}'
          f'  R-B {rgbv[0]-rgbv[2]:+.3f}')
