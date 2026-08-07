"""Did the render land on the profile the new stops were designed for?

Reuses sim3.py's masks (block and curl dilated out, the hone band excluded,
alpha>240 only) but reads the freshly rendered icon.png instead of the r06
candidate, so the comparison is design-target vs achieved.
"""
import numpy as np
from PIL import Image
import sim3 as S

im = Image.open(S.A / 'icon.png').convert('RGBA')
g = S.F.to_gray(im)

TARGET_R = [(0, .888), (100, .860), (180, .791), (260, .736), (340, .677), (420, .641),
            (500, .601), (580, .569), (680, .571), (800, .568), (940, .568)]
TARGET_T = [(660, .863), (760, .871), (860, .869), (960, .852), (1060, .848),
            (1160, .809), (1260, .747), (1360, .700), (1448, .683)]


def prof(mask, us, target, was):
    wu = [k[0] for k in was]
    wl = [k[1] for k in was]
    print('%-6s %7s %7s %7s %8s' % ('u', 'was', 'got', 'target', 'miss'))
    for u in us:
        m = mask & (np.abs(S.U - u) < 20)
        if m.sum() < 300:
            continue
        got = g[m].mean()
        t = float(np.interp(u, [k[0] for k in target], [k[1] for k in target]))
        print('%-6d %7.3f %7.3f %7.3f %+8.3f'
              % (u, float(np.interp(u, wu, wl)), got, t, got - t))


WAS_R = list(zip(S.PR_U, S.PR_L))
WAS_T = list(zip(S.PT_U, S.PT_L))
print('rough plane')
prof(S.ROUGH, [100, 180, 260, 340, 420, 500, 580, 660, 740, 820, 900], TARGET_R, WAS_R)
print('\ntrued plane')
prof(S.TRUED, [740, 820, 900, 980, 1060, 1140, 1220, 1300, 1380], TARGET_T, WAS_T)

d, rg, tr = S.polarity(im)
print('\npolarity %+.3f (rough %.3f trued %.3f)  was %+.3f' % (d, rg, tr, S.polarity(S.cand)[0]))
S.report('RENDERED', im)
