"""The curl's own value distribution, in both images, on each image's own curl.

Ours comes from the SHAVING=0 difference (exact). The reference's is recovered
by fitting a smooth quadratic ground from an annulus around the curl's bounding
box and keeping the pixels inside the box that depart from that fit - so the
reference's strong ground gradient is removed before anything is called dark.

Reports the whole distribution plus the darkest-decile hue and saturation, which
is the check prior learning #1 exists for: a translucent ribbon must keep its
saturation where it turns away from the key.
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

# ours: exact
mine = np.abs(lum(cand) - lum(nocurl)) > 0.004

# reference: quadratic ground fit from an annulus around the loop's bbox
BOX = (75, 400, 170, 480)   # y0,y1,x0,x1 - the reference's ribbon, read off the render
y0, y1, x0, x1 = BOX
PAD = 70
yy, xx = np.mgrid[0:1024, 0:1024]
inbox = (yy >= y0) & (yy < y1) & (xx >= x0) & (xx < x1)
ring = ((yy >= y0 - PAD) & (yy < y1 + PAD) & (xx >= x0 - PAD) & (xx < x1 + PAD)) & ~inbox
Lr = lum(ref)
Xr = np.stack([np.ones(ring.sum()), xx[ring], yy[ring], xx[ring] ** 2, yy[ring] ** 2, xx[ring] * yy[ring]], 1)
coef, *_ = np.linalg.lstsq(Xr, Lr[ring], rcond=None)
Xb = np.stack([np.ones(inbox.sum()), xx[inbox], yy[inbox], xx[inbox] ** 2, yy[inbox] ** 2, xx[inbox] * yy[inbox]], 1)
fit = np.full(Lr.shape, np.nan)
fit[inbox] = Xb @ coef
resid = Lr - fit
theirs = inbox & (np.abs(resid) > 0.02)
print(f"ground fit residual rms on the ring: {(Lr[ring] - (Xr @ coef)).std():.4f}")
print(f"reference curl footprint {theirs.sum()} px, ours {mine.sum()} px")

for name, m, img, ground in (("MASTER", mine, cand, lum(nocurl)),
                             ("REFERENCE", theirs, ref, fit)):
    L = lum(img)[m]
    g = ground[m]
    q = np.percentile(L, [0, 5, 25, 50, 75, 95, 100])
    print(f"\n== {name}  n={m.sum()}")
    print("   L  min/p5/p25/med/p75/p95/max  " + " ".join(f"{v:.3f}" for v in q))
    print(f"   local ground under it: mean {np.nanmean(g):.3f}   curl-minus-ground mean {np.nanmean(L-g):+.4f}")
    print(f"   fraction more than 0.15 below its ground: {np.nanmean((L - g) < -0.15)*100:.1f}%")
    print(f"   fraction more than 0.25 below its ground: {np.nanmean((L - g) < -0.25)*100:.1f}%")
    dark = L <= np.percentile(L, 10)
    idx = np.nonzero(m)
    dy, dx = idx[0][dark], idx[1][dark]
    px = img[dy, dx]
    print(f"   darkest decile: L {L[dark].mean():.3f}  sat {sat(px).mean():.3f}  "
          f"rgb {px.mean(0)[0]:.3f},{px.mean(0)[1]:.3f},{px.mean(0)[2]:.3f}")
    lit = L >= np.percentile(L, 90)
    ly, lx = idx[0][lit], idx[1][lit]
    lp = img[ly, lx]
    print(f"   lightest decile: L {L[lit].mean():.3f}  sat {sat(lp).mean():.3f}  "
          f"rgb {lp.mean(0)[0]:.3f},{lp.mean(0)[1]:.3f},{lp.mean(0)[2]:.3f}")
    print(f"   dynamic range within the ribbon: {q[6]-q[0]:.3f}  (p95-p5 {q[5]-q[1]:.3f})")
