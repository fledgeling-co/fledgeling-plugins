"""Clean version of w10: the reference's ribbon only, with the block excluded by
its own top edge line, and a ground fit taken from ribbon-free, block-free
annulus pixels. Then the same statistics for the master's ribbon.
"""
import pathlib, subprocess, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r16/work"
REF = A / "icon-engineC-f5665d-2.png"
NEUTRAL = 128


def render_svg(path, size):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA"); tmp.unlink(missing_ok=True); return im


def rgb_of(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    if a.shape[2] == 4:
        rgb, al = a[..., :3], a[..., 3:4]
        a = rgb * al + (NEUTRAL / 255.0) * (1 - al)
    return a


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def sat(a):
    mx, mn = a.max(-1), a.min(-1)
    return np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)


cand = rgb_of(render_svg(A / "icon.svg", 1024))
nocurl = rgb_of(render_svg(W / "no-curl.svg", 1024))
ref = rgb_of(Image.open(REF).convert("RGB").resize((1024, 1024), Image.LANCZOS))
yy, xx = np.mgrid[0:1024, 0:1024]

# the reference block's top-left edge, read off the render at two points
not_block = yy < 430.0 - 0.595 * (xx - 310.0) - 18
BOX = (60, 350, 175, 480)
y0, y1, x0, x1 = BOX
inbox = (yy >= y0) & (yy < y1) & (xx >= x0) & (xx < x1) & not_block
PAD = 90
ring = ((yy >= y0 - PAD) & (yy < y1 + PAD) & (xx >= x0 - PAD) & (xx < x1 + PAD)
        & ~((yy >= y0) & (yy < y1) & (xx >= x0) & (xx < x1)) & not_block
        & (xx >= 0) & (yy >= 0))
Lr = lum(ref)


def quad(m):
    return np.stack([np.ones(m.sum()), xx[m], yy[m], xx[m] ** 2, yy[m] ** 2, xx[m] * yy[m]], 1)


coef, *_ = np.linalg.lstsq(quad(ring), Lr[ring], rcond=None)
print(f"ring fit rms {(Lr[ring] - quad(ring) @ coef).std():.4f}  (n={ring.sum()})")
fit = np.full(Lr.shape, np.nan)
fit[inbox] = quad(inbox) @ coef
theirs = inbox & (np.abs(Lr - fit) > 0.025)

mine = np.abs(lum(cand) - lum(nocurl)) > 0.004

for name, m, img, ground in (("MASTER ribbon", mine, cand, lum(nocurl)),
                             ("REFERENCE ribbon", theirs, ref, fit)):
    L, g = lum(img)[m], ground[m]
    d = L - g
    q = np.percentile(L, [0, 2, 10, 50, 90, 98, 100])
    print(f"\n== {name}  n={m.sum()}")
    print("   own L  min/p2/p10/med/p90/p98/max  " + " ".join(f"{v:.3f}" for v in q))
    dq = np.nanpercentile(d, [0, 2, 10, 50, 90, 98, 100])
    print("   vs its own local ground        " + " ".join(f"{v:+.3f}" for v in dq))
    print(f"   mean {np.nanmean(d):+.4f}   below-ground by >0.15: {np.nanmean(d < -0.15)*100:5.1f}%"
          f"   >0.25: {np.nanmean(d < -0.25)*100:5.1f}%   >0.35: {np.nanmean(d < -0.35)*100:5.1f}%")
    idx = np.nonzero(m)
    for tag, sel in (("darkest 5%", L <= np.percentile(L, 5)), ("lightest 5%", L >= np.percentile(L, 95))):
        px = img[idx[0][sel], idx[1][sel]]
        print(f"   {tag:12s} L {L[sel].mean():.3f}  sat {sat(px).mean():.3f}  "
              f"rgb ({px.mean(0)[0]:.3f}, {px.mean(0)[1]:.3f}, {px.mean(0)[2]:.3f})")
