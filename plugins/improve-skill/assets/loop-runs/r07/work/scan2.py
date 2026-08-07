import numpy as np
from sim3 import report, apply

REF_ROUGH = [(80, 0.879), (160, 0.804), (240, 0.752), (320, 0.686), (400, 0.651),
             (480, 0.613), (560, 0.567), (640, 0.575), (720, 0.568), (900, 0.568)]
OURS_ROUGH = [(100, 0.808), (180, 0.791), (260, 0.776), (340, 0.744), (420, 0.726),
              (500, 0.710), (580, 0.683), (660, 0.650), (740, 0.619), (820, 0.588),
              (900, 0.584)]
OUR_TRUED = [(740, 0.915), (820, 0.865), (900, 0.874), (980, 0.893), (1060, 0.870),
             (1140, 0.844), (1220, 0.817), (1300, 0.770), (1380, 0.740)]


def blend(ours, ref, w):
    ru = [k[0] for k in ref]
    rl = [k[1] for k in ref]
    return [(u, l * (1 - w) + float(np.interp(u, ru, rl)) * w) for u, l in ours]


def taper(knots, u0, a, base=0.0):
    out = []
    for u, l in knots:
        t = 0.0 if u <= u0 else (u - u0) / (1380.0 - u0)
        out.append((u, l + base - a * t))
    return out


R1 = blend(OURS_ROUGH, REF_ROUGH, 1.0)

print('--- fine uniform trued drop, rough converged ---')
for d in (-0.02, -0.025, -0.03, -0.035):
    report('rough w=1 trued %+.3f' % d, apply(rough_knots=R1, trued_knots=taper(OUR_TRUED, 0, 0, d)))

print('\n--- shaped trued falloff (hold to u0, then taper by a), rough converged ---')
for u0 in (940, 980, 1020):
    for a in (0.06, 0.10, 0.14, 0.18, 0.22):
        report('u0=%d a=%.2f' % (u0, a), apply(rough_knots=R1, trued_knots=taper(OUR_TRUED, u0, a)))

print('\n--- shaped + small uniform ---')
for u0 in (940, 980):
    for a in (0.10, 0.16, 0.22):
        for base in (-0.015, -0.025):
            report('u0=%d a=%.2f base=%+.3f' % (u0, a, base),
                   apply(rough_knots=R1, trued_knots=taper(OUR_TRUED, u0, a, base)))
