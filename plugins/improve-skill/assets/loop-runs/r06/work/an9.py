"""Confirm the front-face reading before acting on it.

(a) A 3x zoom of each block's top/front junction, side by side.
(b) The reference's front face as a function of distance above the hone and of
    position along the length -- to reconcile with round 7's frontFall finding,
    which was taken on a 15px strip rather than the whole face.
"""
import numpy as np, pathlib, math
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
out = B.parent
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2], comp


gc, cc = load(B / 'candidate-1024.png')
gr, cr = load(B / 'reference-1024.png')
K, BB = np.load(B / 'honeline.npy')
refblock = np.load(B / 'refblock.npy')

# (a) crops centred on each block's mid-length, same physical width
ci = Image.open(B / 'candidate-1024.png').convert('RGB')
ri = Image.open(B / 'reference-1024.png').convert('RGB')
cbox = (300, 380, 700, 620)     # our block, mid-length
rbox = (360, 300, 760, 540)     # ref block, mid-length
cc2 = ci.crop(cbox).resize((800, 480), Image.NEAREST)
rc2 = ri.crop(rbox).resize((800, 480), Image.NEAREST)
s = Image.new('RGB', (800, 970), (0, 0, 0))
s.paste(cc2, (0, 0)); s.paste(rc2, (0, 490))
s.save(out / 'junction-2up.png')

# (b) reference front face vs distance above its hone line, per quarter of length
yy, xx = np.mgrid[0:1024, 0:1024]
d = (K * xx + BB - yy) / math.hypot(K, 1)          # perpendicular distance ABOVE the hone
a = math.radians(38.75)
u = math.cos(a) * xx - math.sin(a) * yy
uu = (u - u[refblock].min()) / (u[refblock].max() - u[refblock].min())
print('reference: L above its hone line, by band and by quarter of the block length')
print(f'{"band above hone":<18}' + ''.join(f'{f"u{i}":>8}' for i in range(4)))
for lo, hi in [(4, 12), (12, 25), (25, 45), (45, 75), (75, 110)]:
    row = []
    for i in range(4):
        m = refblock & (d >= lo) & (d < hi) & (uu >= i / 4) & (uu < (i + 1) / 4)
        row.append(f'{gr[m].mean():8.3f}' if m.sum() > 150 else '       .')
    print(f'{f"{lo}-{hi}px":<18}' + ''.join(row))

# ours, same construction on our own hone (33 deg through EDGE_MID)
import importlib.util, sys
spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)
sides = np.load(B / 'sides.npy')
FRONTM, OURS = sides[5], sides[6]
kc = -math.tan(math.radians(33.0))
bc = bi.EDGE_MID[1] - kc * bi.EDGE_MID[0]
dc = (kc * xx + bc - yy) / math.hypot(kc, 1)
ac = math.radians(33.0)
uc = math.cos(ac) * xx - math.sin(ac) * yy
uuc = (uc - uc[OURS].min()) / (uc[OURS].max() - uc[OURS].min())
print('\nours: same')
print(f'{"band above hone":<18}' + ''.join(f'{f"u{i}":>8}' for i in range(4)))
for lo, hi in [(4, 12), (12, 25), (25, 45), (45, 75), (75, 110)]:
    row = []
    for i in range(4):
        m = FRONTM & (dc >= lo) & (dc < hi) & (uuc >= i / 4) & (uuc < (i + 1) / 4)
        row.append(f'{gc[m].mean():8.3f}' if m.sum() > 150 else '       .')
    print(f'{f"{lo}-{hi}px":<18}' + ''.join(row))
print('\nwrote junction-2up.png (top: ours, bottom: reference, both 2x)')
