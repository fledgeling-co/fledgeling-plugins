import numpy as np, pathlib
from PIL import Image
A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
R11 = A / "loop-runs/r11"


def load(p, size=None):
    im = Image.open(p).convert("RGB")
    if size:
        im = im.resize((size, size), Image.LANCZOS)
    return np.asarray(im).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def crop(p, x0, y0, w, h, out, zoom=1):
    im = Image.open(p).convert("RGB").crop((x0, y0, x0 + w, y0 + h))
    if zoom != 1:
        im = im.resize((w * zoom, h * zoom), Image.NEAREST)
    im.save(out)
    return out
