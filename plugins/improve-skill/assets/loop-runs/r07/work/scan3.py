import numpy as np
from sim3 import report, apply

# The reference's own measured profiles on the shared light axis u = (x+y)/sqrt2
REF_ROUGH = [(80, 0.879), (160, 0.804), (240, 0.752), (320, 0.686), (400, 0.651),
             (480, 0.613), (560, 0.567), (640, 0.575), (720, 0.568), (900, 0.568)]
REF_TRUED = [(720, 0.644), (800, 0.656), (880, 0.646), (960, 0.636), (1040, 0.637),
             (1120, 0.621), (1200, 0.587), (1280, 0.548), (1400, 0.510)]

OURS_ROUGH_U = [100, 180, 260, 340, 420, 500, 580, 660, 740, 820, 900]
OURS_TRUED_U = [740, 820, 900, 980, 1060, 1140, 1220, 1300, 1380]


def at(prof, us, gain=1.0):
    pu = [k[0] for k in prof]
    pl = [k[1] for k in prof]
    return [(u, float(np.interp(u, pu, pl)) * gain) for u in us]


R = at(REF_ROUGH, OURS_ROUGH_U)
print('rough on the reference profile; trued on the reference profile x finish gain g')
for g in (1.26, 1.30, 1.32, 1.34, 1.36, 1.38, 1.42):
    report('g=%.2f' % g, apply(rough_knots=R, trued_knots=at(REF_TRUED, OURS_TRUED_U, g)))

print('\nsame, but the rough plane only 75%% of the way to the reference')
OURS_ROUGH = [(100, 0.808), (180, 0.791), (260, 0.776), (340, 0.744), (420, 0.726),
              (500, 0.710), (580, 0.683), (660, 0.650), (740, 0.619), (820, 0.588),
              (900, 0.584)]
R75 = [(u, 0.25 * l + 0.75 * r[1]) for (u, l), r in zip(OURS_ROUGH, R)]
for g in (1.30, 1.34, 1.38):
    report('r75 g=%.2f' % g, apply(rough_knots=R75, trued_knots=at(REF_TRUED, OURS_TRUED_U, g)))

print('\ncomponent isolation')
report('rough only (on reference)', apply(rough_knots=R))
for g in (1.34, 1.38):
    report('trued only g=%.2f' % g, apply(trued_knots=at(REF_TRUED, OURS_TRUED_U, g)))
