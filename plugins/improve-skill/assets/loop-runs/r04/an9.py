"""r04: reference top-face depth = (back edge) - (shoulder), measured directly, no rise math."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB"), float) / 255.
L = 0.2126 * ref[..., 0] + 0.7152 * ref[..., 1] + 0.0722 * ref[..., 2]

a = np.radians(38.92)
ux, uy = np.cos(a), -np.sin(a)
nx, ny = -np.sin(a), -np.cos(a)
ox, oy = 382.0, 688.0


def prof(lx0, half=18):
    """mean luminance along a perpendicular ray, averaged over a band of lx"""
    out = []
    for ly in np.arange(-10, 300, 2.0):
        vals = []
        for lx in np.arange(lx0 - half, lx0 + half, 2.0):
            x = ox + ux * lx + nx * ly
            y = oy + uy * lx + ny * ly
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < 1024 and 0 <= yi < 1024:
                vals.append(L[yi, xi])
        out.append((ly, np.mean(vals) if vals else np.nan))
    return out


for lx0 in (120, 200, 280, 360, 440):
    p = prof(lx0)
    ly = np.array([q[0] for q in p])
    v = np.array([q[1] for q in p])
    # shoulder: darkest point in the lower half of the section
    lo = (ly > 10) & (ly < 130)
    sh = ly[lo][int(np.argmin(v[lo]))]
    # back edge: the steepest rise into the ground, searching outward
    hi = (ly > 150) & (ly < 290)
    d = np.gradient(v)
    be = ly[hi][int(np.argmax(d[hi]))]
    print(f"lx={lx0:4d}  shoulder ly={sh:6.1f} (L{v[lo].min():.3f})   "
          f"back edge ly={be:6.1f}   TOP-FACE DEPTH={be-sh:6.1f}")
