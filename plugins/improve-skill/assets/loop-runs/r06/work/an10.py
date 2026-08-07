"""The block's cross-section profile, both images, at five stations along the length.

Perpendicular to each block's own hone, from just below the cutting edge up
across the front face, the junction, and the top face to the back silhouette.
This is the measurement the whole round turns on, so it is taken as a profile
rather than as region means.
"""
import numpy as np, pathlib, math, sys, importlib.util
from PIL import Image

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
K, BB = np.load(B / 'honeline.npy')


def sample(g, x, y):
    xi, yi = int(round(x)), int(round(y))
    if 0 <= xi < 1024 and 0 <= yi < 1024:
        return g[yi, xi]
    return np.nan


def profile(g, ang_deg, x0, y0, length, stations, depths):
    """x0,y0 = leading end of the hone; ang = hone angle; walk along then up."""
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), -math.sin(a)
    px, py = -math.sin(a), -math.cos(a)     # 'up' the face, away from the ground
    rows = []
    for s in stations:
        cx, cy = x0 + ux * length * s, y0 + uy * length * s
        rows.append([sample(g, cx + px * d, cy + py * d) for d in depths])
    return np.array(rows)


DEPTHS = [-14, -6, 0, 6, 12, 20, 30, 42, 56, 72, 90, 110, 135, 160, 190]
STATIONS = [0.12, 0.30, 0.50, 0.70, 0.88]

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)

print('=== ours: L across the cross-section (depth in px above the cutting edge) ===')
po = profile(gc, 33.0, bi.AX, bi.AY, bi.BLADE_LEN, STATIONS, DEPTHS)
# reference: hone endpoints from the chroma fit, extended over its block
rx0, ry0 = 300.0, K * 300.0 + BB
rlen = math.hypot(760 - 300, (K * 760 + BB) - ry0)
pr = profile(gr, 38.75, rx0, ry0, rlen, STATIONS, DEPTHS)

hdr = 'station ' + ''.join(f'{d:>7}' for d in DEPTHS)
for nm, p in (('ours', po), ('ref ', pr)):
    print(f'\n{nm}   {hdr}')
    for s, row in zip(STATIONS, p):
        print(f'      u={s:<4}' + ''.join('      .' if np.isnan(v) else f'{v:7.3f}' for v in row))

print('\n=== ours minus reference, same cross-section ===')
print('        ' + ''.join(f'{d:>7}' for d in DEPTHS))
for s, a_, b_ in zip(STATIONS, po, pr):
    print(f'  u={s:<4}' + ''.join('      .' if (np.isnan(x) or np.isnan(y)) else f'{x-y:+7.3f}'
                                  for x, y in zip(a_, b_)))
print('\nref block depth: its front face reaches ~55px at the leading end, ~90px at the trailing;')
print('ours reaches 48 -> 132. Compare by relative depth as well as absolute.')
