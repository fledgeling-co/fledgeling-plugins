"""Turn the measured target profiles into gradient stops on ONE shared key axis.

The axis is the key's own diagonal, (0,0) -> (1024,1024), so a stop's offset t
maps to the light-axis coordinate u = (x+y)/sqrt2 as u = 1448*t for BOTH ground
fields. New stop colour = the current field colour at that u, scaled by
target_L / current_L, with the current profile taken from a low-order fit so the
correction cannot try to divide out real features (the block's cast shadow dips
the trued profile at u=820 and has to survive). Multiplicative, so every hue -
round 1's warm-shadow finding included - is untouched.
"""
import math
import numpy as np

DIAG = 1024 * math.sqrt(2.0)

ROUGH_NOW = ((70, 20), (700, 650),
             [(0.0, (0xDB, 0xD5, 0xC7)), (0.50, (0xC2, 0xBA, 0xA8)), (1.0, (0xA1, 0x98, 0x81))])
TRUED_NOW = ((300, 430), (1090, 1120),
             [(0.0, (0xFF, 0xFD, 0xF6)), (0.40, (0xF9, 0xF3, 0xE7)), (1.0, (0xDE, 0xD4, 0xBE))])


def eval_grad(spec, u):
    (x1, y1), (x2, y2), stops = spec
    p = u / math.sqrt(2.0)
    dx, dy = x2 - x1, y2 - y1
    t = ((p - x1) * dx + (p - y1) * dy) / (dx * dx + dy * dy)
    t = min(max(t, 0.0), 1.0)
    off = [s[0] for s in stops]
    return tuple(float(np.interp(t, off, [s[1][c] for s in stops])) for c in range(3))


CUR_ROUGH = [(100, 0.808), (180, 0.791), (260, 0.776), (340, 0.744), (420, 0.726),
             (500, 0.710), (580, 0.683), (660, 0.650), (740, 0.619), (820, 0.588),
             (900, 0.584)]
CUR_TRUED = [(740, 0.915), (820, 0.865), (900, 0.874), (980, 0.893), (1060, 0.870),
             (1140, 0.844), (1220, 0.817), (1300, 0.770), (1380, 0.740)]

REF_ROUGH = [(0, 0.888), (80, 0.879), (160, 0.804), (240, 0.752), (320, 0.686),
             (400, 0.651), (480, 0.613), (560, 0.567), (640, 0.575), (720, 0.568),
             (960, 0.568)]
REF_TRUED = [(720, 0.644), (800, 0.656), (880, 0.646), (960, 0.636), (1040, 0.637),
             (1120, 0.621), (1200, 0.587), (1280, 0.548), (1400, 0.510)]

G = 1.34


def fit(prof, deg):
    u = np.array([k[0] for k in prof], float)
    l = np.array([k[1] for k in prof], float)
    return np.poly1d(np.polyfit(u, l, deg))


# The rough profile is already smooth and monotone, so it is its own fit; a
# quadratic undershoots its flat tail and would inject a bogus lift at u>900.
FR = lambda u: float(np.interp(u, [k[0] for k in CUR_ROUGH], [k[1] for k in CUR_ROUGH]))  # noqa: E731
FT = fit(CUR_TRUED, 2)


def interp(prof, u):
    return float(np.interp(u, [k[0] for k in prof], [k[1] for k in prof]))


def emit(name, spec, curfit, ref, gain, us):
    print('  <!-- %s -->' % name)
    for u in us:
        tgt = interp(ref, u) * gain
        r = tgt / float(curfit(u))
        c = eval_grad(spec, u)
        new = tuple(int(round(min(255.0, max(0.0, v * r)))) for v in c)
        print('    <stop offset="%.4f" stop-color="#%02X%02X%02X"/>  <!-- u %4d  target L %.3f  x%.3f -->'
              % (u / DIAG, new[0], new[1], new[2], u, tgt, r))


emit('roughField', ROUGH_NOW, FR, REF_ROUGH, 1.0,
     [0, 100, 180, 260, 340, 420, 500, 580, 680, 800, 940])
print()
emit('truedField', TRUED_NOW, FT, REF_TRUED, G,
     [660, 760, 860, 960, 1060, 1160, 1260, 1360, 1448])
print()
print('current fits: rough(100)=%.3f rough(900)=%.3f  trued(740)=%.3f trued(1380)=%.3f'
      % (FR(100), FR(900), FT(740), FT(1380)))
