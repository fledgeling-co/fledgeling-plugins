"""Band energy per scale, measured once at 1024 on the same pixels for both
images, so nothing depends on how a mask survives a re-render.

For a box width w, hp_w = box(g, w) - box(g, 4w) isolates the energy in the
octave-and-a-bit around w px. Averaged to 32px, one output pixel is 32 canvas
px, so the bands at w >= 33 are the ones that survive the downsample and can
still make an edge; the bands below that average away.
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


gc = gray(render_svg(CAND, 1024))
gr = gray(Image.open(REF).convert("RGBA").resize((1024, 1024), Image.LANCZOS))

# One big open patch of un-planed ground, clean in both images and clear of the
# block, the curl, the cut and the rim. Verified below by printing its extremes.
PATCH = (544, 832, 72, 168)          # y0,y1,x0,x1  (left ground below the curl)
PATCH2 = (176, 448, 72, 136)         # the strip left of the curl
PATCH3 = (64, 224, 176, 480)         # the open top band above the curl

for tag, (y0, y1, x0, x1) in (("left-lower", PATCH), ("left-strip", PATCH2), ("top-band", PATCH3)):
    a, b = gc[y0:y1, x0:x1], gr[y0:y1, x0:x1]
    print(f"===== {tag}  {a.shape}  cand mean {a.mean():.4f} [{a.min():.3f},{a.max():.3f}]  "
          f"ref mean {b.mean():.4f} [{b.min():.3f},{b.max():.3f}]")
    print("   band(px) | cand rms | ref rms | ratio")
    for w in (3, 9, 17, 33, 65):
        ha = box(a, w) - box(a, min(4 * w, min(a.shape) | 1))
        hb = box(b, w) - box(b, min(4 * w, min(b.shape) | 1))
        print(f"   {w:5d}    |  {ha.std():.4f}  | {hb.std():.4f}  | {ha.std()/max(hb.std(),1e-9):5.2f}")
    # what actually survives a 32x average
    for k in (16, 32):
        aa, bb = box(a, k + 1), box(b, k + 1)
        ha, hb = aa - box(aa, 3 * k + 1), bb - box(bb, 3 * k + 1)
        print(f"   after {k}x average: cand rms {ha.std():.4f}  ref rms {hb.std():.4f}  "
              f"ratio {ha.std()/max(hb.std(),1e-9):5.2f}")
