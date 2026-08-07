"""Where does the small-size error actually live?

Renders candidate and reference at 32 and 16 through the SAME pipeline the
scorer uses, then reports per-pixel signed residual, which pixels own the
p90/p10 spread, and the per-pixel contribution to lum_delta.
"""
import pathlib, subprocess, sys, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
CAND = A / "icon.svg"
REF = A / "icon-engineC-f5665d-2.png"
NEUTRAL = 128


def render_svg(path, size):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA")
    tmp.unlink(missing_ok=True)
    return im


def ref_img(size):
    im = Image.open(REF).convert("RGBA")
    if im.width != im.height:
        s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    return im.resize((size, size), Image.LANCZOS)


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def show(g, name):
    print(f"--- {name} ---")
    for row in g:
        print(" ".join(f"{v:4.2f}"[1:] if v < 1 else "1.0 " for v in row))


for size in (32, 16):
    gc, gr = gray(render_svg(CAND, size)), gray(ref_img(size))
    d = gc - gr
    print(f"===== {size}px =====")
    print(f"lum_delta {np.abs(d).mean():.4f}   mean signed {d.mean():+.4f}")
    print(f"cand mean {gc.mean():.4f} p10 {np.percentile(gc,10):.3f} p90 {np.percentile(gc,90):.3f}")
    print(f" ref mean {gr.mean():.4f} p10 {np.percentile(gr,10):.3f} p90 {np.percentile(gr,90):.3f}")
    # how much of |d| would vanish under a pure uniform shift?
    best = np.median(d)
    print(f"after removing median shift {best:+.4f}: lum_delta -> {np.abs(d-best).mean():.4f}")
    for k in (0.02, 0.04, 0.06):
        print(f"  shift -{k:.2f}: lum_delta -> {np.abs(d-(-k) * -1 - 0):.4f}" if False else "", end="")
    print()
    # quadrant breakdown of |d|
    h = size // 2
    q = {"TL": d[:h, :h], "TR": d[:h, h:], "BL": d[h:, :h], "BR": d[h:, h:]}
    for k, v in q.items():
        print(f"  {k}: |d| {np.abs(v).mean():.4f}  signed {v.mean():+.4f}")

    if size == 16:
        show(gc, "candidate L 16")
        show(gr, "reference L 16")
        show(d + 0.5, "signed residual +0.5 (16)")
