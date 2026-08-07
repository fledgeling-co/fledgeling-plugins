"""Print the 32px luminance and sobel magnitude around the false-positive band,
for both images, so the spurious edges can be attributed to actual pixels."""
import pathlib, subprocess, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
CAND, REF = A / "icon.svg", A / "icon-engineC-f5665d-2.png"
NEUTRAL = 128


def render_svg(path, size):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA"); tmp.unlink(missing_ok=True); return im


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def sob(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


gc, gr = gray(render_svg(CAND, 32)), gray(Image.open(REF).convert("RGBA").resize((32, 32), Image.LANCZOS))
sc, sr = sob(gc), sob(gr)
R, C = range(5, 27), range(0, 12)
for name, m in (("cand L", gc), ("ref  L", gr), ("cand |grad|", sc), ("ref  |grad|", sr)):
    print(f"--- {name} (rows 5-26, cols 0-11; grad threshold 0.100) ---")
    print("      " + " ".join(f"c{c:02d}" for c in C))
    for r in R:
        print(f"  r{r:02d} " + " ".join(f"{m[r,c]:.2f}"[1:] for c in C))
