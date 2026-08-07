import numpy as np
from sim3 import (report, apply, cand, PR_U, PT_U, F, BASE, FLOOR, BIAS, metrics, polarity)

# reference profiles, measured in r3.py on the same u axis (block dilated out)
REF_ROUGH = [(80, 0.879), (160, 0.804), (240, 0.752), (320, 0.686), (400, 0.651),
             (480, 0.613), (560, 0.567), (640, 0.575), (720, 0.568), (900, 0.568)]
OURS_ROUGH = [(100, 0.808), (180, 0.791), (260, 0.776), (340, 0.744), (420, 0.726),
              (500, 0.710), (580, 0.683), (660, 0.650), (740, 0.619), (820, 0.588),
              (900, 0.584)]
OUR_TRUED = [(740, 0.915), (820, 0.865), (900, 0.874), (980, 0.893), (1060, 0.870),
             (1140, 0.844), (1220, 0.817), (1300, 0.770), (1380, 0.740)]


def blend(ours, ref, w):
    """w=0 keep ours, w=1 take the reference's profile"""
    ru = [k[0] for k in ref]
    rl = [k[1] for k in ref]
    return [(u, l * (1 - w) + float(np.interp(u, ru, rl)) * w) for u, l in ours]


def shift(knots, d, scale=1.0):
    return [(u, (l + d) * scale) for u, l in knots]


print('--- rough plane only: converge its falloff shape toward the reference ---')
for w in (0.0, 0.25, 0.5, 0.75, 1.0):
    report('rough w=%.2f' % w, apply(rough_knots=blend(OURS_ROUGH, REF_ROUGH, w)))

print('\n--- trued plane only: uniform level drop ---')
for d in (0.0, -0.02, -0.04, -0.06, -0.08, -0.12):
    report('trued %+.2f' % d, apply(trued_knots=shift(OUR_TRUED, d)))

print('\n--- both ---')
for w in (0.5, 0.75, 1.0):
    for d in (-0.02, -0.04, -0.06, -0.08):
        report('rough w=%.2f trued %+.2f' % (w, d),
               apply(rough_knots=blend(OURS_ROUGH, REF_ROUGH, w),
                     trued_knots=shift(OUR_TRUED, d)))
