"""32/16px edge audit: precision vs recall, and WHERE the misses and the false
positives sit. Small-size repair needs to know whether a feature aliases into
spurious edges (simplify it) or smears away (strengthen it)."""
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


def ref_img(size):
    im = Image.open(REF).convert("RGBA")
    return im.resize((size, size), Image.LANCZOS)


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def sobel(g, thresh=0.10):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thresh * 4


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


for size in (32, 16, 64, 128):
    gc, gr = gray(render_svg(CAND, size)), gray(ref_img(size))
    keep = ~rim(size)
    ea, eb = sobel(gc) & keep, sobel(gr) & keep
    tp_p = (ea & dilate(eb)).sum(); tp_r = (eb & dilate(ea)).sum()
    prec = tp_p / max(ea.sum(), 1); rec = tp_r / max(eb.sum(), 1)
    print(f"== {size}px  cand_edges {ea.sum():4d}  ref_edges {eb.sum():4d}  "
          f"prec {prec:.3f}  rec {rec:.3f}  f1 {2*prec*rec/max(prec+rec,1e-9):.4f}")
    fp = ea & ~dilate(eb)   # our edges with nothing near them
    fn = eb & ~dilate(ea)   # reference edges we miss
    print(f"   false-positive edges {fp.sum()}, missed reference edges {fn.sum()}")
    if size in (32, 16):
        def grid(m, ch):
            return "\n".join("".join(ch if v else "." for v in row) for row in m)
        print("   FP map (our spurious edges):"); print(grid(fp, "X"))
        print("   FN map (reference edges we miss):"); print(grid(fn, "O"))
