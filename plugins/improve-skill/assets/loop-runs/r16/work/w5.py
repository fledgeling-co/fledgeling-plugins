"""The octave-decay measurement, on cells that are clean ground in BOTH images.

A 32px cell counts as clean un-planed ground when, in both images, its whole
32x32 block at 1024 stays inside [0.45, 0.90] after a 9px box mean (which
tolerates individual grain marks but excludes the block, the curl and the
trued plane), and the cell lies inside the scorer's rim mask.

For each clean cell we ask the only question that matters at small sizes: how
fast does the tear's energy fall as the image is halved? Real fine noise loses
~half its rms per octave. Anything that does not is low-frequency structure
wearing a texture's clothes, and it will survive to 32px as spurious edges.
"""
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


def rim(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def clean_cells(gc1k, gr1k):
    sc, sr = box(gc1k, 9), box(gr1k, 9)
    ok = np.ones((32, 32), bool)
    keep = ~rim(32)
    # the un-planed side only: above the 33 deg cut through (543, 604)
    yy, xx = np.mgrid[0:32, 0:32]
    cy, cx = yy * 32 + 16, xx * 32 + 16
    above_cut = (cy - 604.0) < np.tan(np.deg2rad(33.0)) * (cx - 543.0) * -1 + 0  # y above the line
    above_cut = cy < 604.0 - np.tan(np.deg2rad(33.0)) * (cx - 543.0) - 60
    for r in range(32):
        for c in range(32):
            a = sc[r * 32:(r + 1) * 32, c * 32:(c + 1) * 32]
            b = sr[r * 32:(r + 1) * 32, c * 32:(c + 1) * 32]
            if a.min() < 0.45 or a.max() > 0.90 or b.min() < 0.45 or b.max() > 0.90:
                ok[r, c] = False
    return ok & keep & above_cut


imgs = {s: (gray(render_svg(CAND, s)), gray(ref_img(s))) for s in (32, 64, 128, 256, 1024)}
ok = clean_cells(*imgs[1024])
print(f"clean un-planed ground cells: {ok.sum()} of 1024")
print("\n".join("".join("#" if v else "." for v in row) for row in ok))

print("\n size |  cand hp rms | ref hp rms | ratio | cand/octave | ref/octave")
prev = None
for size in (1024, 256, 128, 64, 32):
    gc, gr = imgs[size]
    k = size // 32
    m = np.kron(ok, np.ones((k, k), bool))
    w = 3 if k <= 2 else (5 if k == 4 else 9)
    hc, hr = gc - box(gc, w), gr - box(gr, w)
    a, b = hc[m].std(), hr[m].std()
    line = f" {size:4d} |   {a:.4f}     |   {b:.4f}   | {a/b:5.2f} |"
    if prev:
        oct_ = np.log2(prev[0] / max(size, 1) ** 0) if False else 1
        line += f"    {a/prev[1]:.2f}     |   {b/prev[2]:.2f}"
    print(line)
    prev = (size, a, b)
