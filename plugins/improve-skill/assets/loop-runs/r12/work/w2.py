"""1:1 crops of the un-planed plane, reference above ours, at three stations in the
band the profile now carries. Contrast-stretched per patch so the MARKS are visible
rather than the field they sit on - this round is about mark shape, not amplitude.
"""
import numpy as np
from PIL import Image

import sys
h = np.load("h1024.npy")
g = np.load((sys.argv[1] if len(sys.argv) > 1 else "g") + "1024.npy")
N = 256
STATIONS = {"band-left": (16, 512), "band-mid": (140, 400), "band-low": (100, 700)}


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[:x.shape[0], :x.shape[1]]


def patch(img, x0, y0):
    p = img[y0:y0+N, x0:x0+N] - box(img, 25)[y0:y0+N, x0:x0+N]
    s = 3.0 * p.std()
    return np.clip(p / (2 * s) + 0.5, 0, 1)


for name, (x0, y0) in STATIONS.items():
    row = np.concatenate([patch(h, x0, y0), patch(g, x0, y0)], axis=1)
    Image.fromarray((row * 255).astype(np.uint8)).resize((N * 4, N * 2), Image.NEAREST
                                                         ).save(f"v-{name}.png")
    print(f"{name}: ref | ours -> v-{name}.png")
