"""r04: the round's cost line — focal, optical centre, safe zone, figure-ground.

The subject is taken as the connected component containing the blade, so the vignetted
corners cannot be mistaken for artwork. Focal is the larger bbox side as a fraction of the
tile edge, which is the definition icon-notes has used since round 4 (601px -> 58.7%).
Polarity comes from measure.py, not from ad-hoc field patches.
"""
from collections import deque

import numpy as np
from PIL import Image

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/"


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def component(mask, seed):
    """largest-blob flood fill from a seed, pure numpy/deque (no scipy here)"""
    out = np.zeros_like(mask)
    q = deque([seed])
    out[seed] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True
                q.append((ny, nx))
    return out


def report(name, path):
    a = np.asarray(Image.open(path).convert("RGB").resize((1024, 1024), Image.LANCZOS), float) / 255.
    L = lum(a)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    verm = (r > 0.45) & (r - b > 0.20) & (r - g > 0.12)
    blade = component(L < 0.42, (604, 500)) | verm
    ys, xs = np.nonzero(blade)
    w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    print(f"{name}")
    print(f"  blade bbox {w} x {h}   focal {max(w, h) / 1024 * 100:.1f}% of tile")
    print(f"  optical centre ({xs.mean():.0f}, {ys.mean():.0f})")
    print(f"  safe zone  L{xs.min():4d} R{1023 - xs.max():4d} T{ys.min():4d} B{1023 - ys.max():4d}"
          f"   (T = {ys.min() / 1024 * 100:.1f}% of canvas)")
    print(f"  block median L {np.median(L[blade & (L < 0.35)]):.3f}")


report("BEFORE  (r01, shipped master)", A + "loop-runs/r01/candidate-1024.png")
report("AFTER   (r04, BLADE_THICK 204)", A + "icon.png")
