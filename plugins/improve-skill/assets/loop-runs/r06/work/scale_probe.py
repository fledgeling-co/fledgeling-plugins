#!/usr/bin/env python3
"""r06: the characteristic scale of C2's surface texture, per material.

The relief is a noise height field, so it needs a FREQUENCY as well as an amplitude,
and picking one by eye is how the earlier attempt ended up with a 1.8px pit that would
alias. This reads the scale off C2 directly: the 1-D autocorrelation of the high-passed
patch, reported as the lag where it first crosses zero (roughly the half-period of the
dominant feature), taken along and across the grain separately.
"""
import math
import numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r04/"
g = np.asarray(Image.open(A + "reference-1024.png").convert("RGB"), dtype=np.float64) / 255.0
g = 0.2126 * g[..., 0] + 0.7152 * g[..., 1] + 0.0722 * g[..., 2]


def highpass(q, w=9):
    v = sliding_window_view(q, (w, w))
    return q[w // 2:-(w // 2), w // 2:-(w // 2)] - v.mean(axis=(2, 3))


def zero_cross(h, axis):
    h = h - h.mean()
    n = h.shape[axis]
    ac = []
    for lag in range(1, min(24, n)):
        a = np.take(h, range(0, n - lag), axis=axis)
        b = np.take(h, range(lag, n), axis=axis)
        ac.append(float((a * b).mean() / max(h.var(), 1e-12)))
    for i, v in enumerate(ac):
        if v <= 0:
            return i + 1, ac[:6]
    return None, ac[:6]


def report(name, box, rot=None):
    y0, y1, x0, x1 = box
    q = g[y0:y1, x0:x1]
    if rot is not None:                       # sample in the material's own frame
        im = Image.fromarray((q * 255).astype(np.uint8)).rotate(rot, resample=Image.BICUBIC)
        s = int(q.shape[0] * 0.30)
        q = np.asarray(im, dtype=np.float64)[s:-s, s:-s] / 255.0
    h = highpass(q)
    zx, acx = zero_cross(h, 1)
    zy, acy = zero_cross(h, 0)
    print(f"{name:22s} sd% {100*h.std()/q.mean():5.2f}   first zero: across {zx}px  along {zy}px")
    print(f"{'':22s} ac across {[round(v,2) for v in acx]}")
    print(f"{'':22s} ac along  {[round(v,2) for v in acy]}")


# C2's grain runs parallel to its cut (38.93 deg); rotating by -38.93 puts the grain
# horizontal so "across" and "along" mean what they say.
report("C2 un-planed ground", (400, 520, 60, 260), rot=-38.93)
report("C2 top face", (330, 430, 470, 640), rot=-38.93)
report("C2 curl", (170, 300, 210, 330))
