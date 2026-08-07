"""Same measurement, on ground cells that are clean in BOTH images.

G1 = 32px rows 17..25, cols 3..6   (canvas x 96-224, y 544-832) - open un-planed
     ground below the curl, left of the block.  This is exactly the band the
     32px false-positive edge map lit up.
G2 = 32px rows 8..13, cols 2..3    (canvas x  64-128, y 256-448) - the strip left
     of the curl.
T1 = 32px rows 24..29, cols 18..27 (canvas x 576-928, y 768-960) - trued plane,
     as a control: it must not move.
"""
import pathlib, subprocess, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
CAND, REF = A / "icon.svg", A / "icon-engineC-f5665d-2.png"
NEUTRAL = 128
REGIONS = {"G1": (17, 26, 3, 7), "G2": (8, 14, 2, 4), "T1": (24, 30, 18, 28)}


def render_svg(path, size):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA"); tmp.unlink(missing_ok=True); return im


def ref_img(size):
    return Image.open(REF).convert("RGBA").resize((size, size), Image.LANCZOS)


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def box(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1); c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[: x.shape[0], : x.shape[1]]


def cut(g, size, r):
    k = size // 32
    r0, r1, c0, c1 = r
    return g[r0 * k:r1 * k, c0 * k:c1 * k]


imgs = {s: (gray(render_svg(CAND, s)), gray(ref_img(s))) for s in (32, 64, 128, 1024)}

for name, r in REGIONS.items():
    print(f"===== {name} =====")
    for size in (32, 64, 128, 1024):
        gc, gr = imgs[size]
        a, b = cut(gc, size, r), cut(gr, size, r)
        w = 3 if size <= 64 else (5 if size == 128 else 9)
        ha, hb = a - box(a, w), b - box(b, w)
        print(f"  {size:4d}px  mean L cand {a.mean():.4f} ref {b.mean():.4f}"
              f"   | high-pass rms cand {ha.std():.4f} ref {hb.std():.4f}"
              f"  ratio {ha.std()/max(hb.std(),1e-9):5.2f}"
              f"   | range cand {a.max()-a.min():.3f} ref {b.max()-b.min():.3f}")
