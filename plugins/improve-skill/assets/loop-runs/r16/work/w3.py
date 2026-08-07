"""How much grain energy survives to 32px, ours vs the reference, and who owns
the contrast percentiles there.

Small-size repair needs three numbers before it authors anything:
  (a) the residual amplitude of the tear AT 32px in the un-planed field,
  (b) the same at 1024 in the fine band r14 already matched (a control), and
  (c) whether the grain pixels sit anywhere near p10/p90, i.e. whether damping
      it can cost the contrast floor at all.
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


# The un-planed field at 32px, block- and curl-free, inside the rim: the two
# strips the FP map lit up plus their continuation.
def unplaned32():
    m = np.zeros((32, 32), bool)
    m[6:14, 2:8] = True     # left of the curl
    m[16:26, 2:8] = True    # left ground below the curl
    m[2:6, 3:12] = True     # top strip above the curl
    return m


for size, w in ((32, 3), (64, 3), (128, 5)):
    gc, gr = gray(render_svg(CAND, size)), gray(ref_img(size))
    m = unplaned32()
    if size != 32:
        m = np.kron(m, np.ones((size // 32, size // 32), bool))
    hc, hr = gc - box(gc, w), gr - box(gr, w)
    print(f"== {size}px un-planed field ({m.sum()} px)  high-pass rms  "
          f"cand {hc[m].std():.4f}  ref {hr[m].std():.4f}   ratio {hc[m].std()/hr[m].std():.2f}")
    print(f"   field mean L cand {gc[m].mean():.4f}  ref {gr[m].mean():.4f}   "
          f"p2-p98 cand {np.percentile(gc[m],98)-np.percentile(gc[m],2):.4f} "
          f"ref {np.percentile(gr[m],98)-np.percentile(gr[m],2):.4f}")

# who owns p10 / p90 at 32 and 16
for size in (32, 16):
    gc = gray(render_svg(CAND, size))
    p10, p90 = np.percentile(gc, 10), np.percentile(gc, 90)
    lo, hi = gc <= p10 + 1e-9, gc >= p90 - 1e-9
    print(f"== {size}px  p10 {p10:.3f} p90 {p90:.3f} spread {p90-p10:.4f}")
    for name, mask in (("p10 band", gc <= np.percentile(gc, 12)), ("p90 band", gc >= np.percentile(gc, 88))):
        ys, xs = np.nonzero(mask)
        print(f"   {name}: n={mask.sum()}  centroid ({xs.mean()/size:.2f},{ys.mean()/size:.2f}) "
              f"x[{xs.min()}-{xs.max()}] y[{ys.min()}-{ys.max()}]")
    # how far is the un-planed field from the percentiles?
    m = unplaned32() if size == 32 else unplaned32()[::2, ::2]
    print(f"   un-planed field L range {gc[m].min():.3f}-{gc[m].max():.3f} "
          f"(p10 {p10:.3f}, p90 {p90:.3f}) -> {'TOUCHES' if gc[m].max()>=p90 or gc[m].min()<=p10 else 'clear of'} the percentiles")
