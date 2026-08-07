#!/usr/bin/env python3
"""Is the bottom-right corner reading 27 hp sd something round 8 introduced, or was it
already there? The tile is squircle-clipped, and a clip edge inside a measured patch
swamps any texture figure."""
import numpy as np
from PIL import Image, ImageFilter

D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/"


def load(p):
    im = Image.open(p).convert("L").resize((1024, 1024), Image.LANCZOS)
    g = np.asarray(im, float)
    b = np.asarray(im.filter(ImageFilter.GaussianBlur(6)), float)
    return g, g - b


BOXES = [("trued far corner", 860, 930, 90), ("trued mid-right", 760, 700, 90)]
for lbl, p in (("baseline", D + "loop-runs/r01/candidate-1024.png"), ("now", D + "icon.png")):
    g, h = load(p)
    for k, x, y, n in BOXES:
        pa = g[y:y + n, x:x + n]
        gy, gx = np.gradient(pa)
        print(f"{lbl:9s} {k:18s} hp {h[y:y+n, x:x+n].std():6.2f}  "
              f"e>4 {(np.hypot(gx, gy) > 4).mean():.3f}  L {pa.mean():6.1f}  min {pa.min():5.1f}")
