"""Did the profile land? The achieved 3-13px high-pass rms per 64px canvas-y band on
the un-planed plane, new render against reference against the r10 render, plus the
thresholded edge density the scorer actually counts, plus the band's anisotropy and
mean wavelength - the three faults m7/m8 measured, re-read on the result.
"""
import math, sys, numpy as np
from PIL import Image

W = 1024
h = np.load("h1024.npy"); g = np.load("g1024.npy")
rough = np.load("rough.npy")
n = np.load(sys.argv[1] if len(sys.argv) > 1 else "n1024.npy")
yy, xx = np.mgrid[0:W, 0:W].astype(float)


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[:x.shape[0], :x.shape[1]]


def sobel(img, thresh=0.10):
    p = np.pad(img, 1, mode="edge")
    gx = (p[:-2, 2:] + 2*p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2*p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thresh * 4


hp = lambda i: box(i, 3) - box(i, 13)
HR, HO, HN = hp(h), hp(g), hp(n)
DR, DO, DN = box(sobel(h), 41), box(sobel(g), 41), box(sobel(n), 41)
print("un-planed plane, 3-13px high-pass rms and thresholded edge density")
print(f"{'y band':>10s} {'ref':>7s} {'r10':>7s} {'new':>7s} {'want':>6s} {'got':>6s}"
      f"   {'ref d%':>7s} {'r10 d%':>7s} {'new d%':>7s}")
for y0 in range(64, 960, 64):
    sel = rough & (yy >= y0) & (yy < y0 + 64)
    if sel.sum() < 1500:
        continue
    a, b, c = HR[sel].std(), HO[sel].std(), HN[sel].std()
    print(f"{y0:4d}-{y0+64:4d} {a:7.4f} {b:7.4f} {c:7.4f} {a/b:6.2f} {c/b:6.2f}"
          f"   {100*DR[sel].mean():7.2f} {100*DO[sel].mean():7.2f} {100*DN[sel].mean():7.2f}")
m = rough
print(f"\nwhole plane   ref {HR[m].std():.4f}  r10 {HO[m].std():.4f}  new {HN[m].std():.4f}"
      f"   edge%  ref {100*DR[m].mean():.2f}  r10 {100*DO[m].mean():.2f}"
      f"  new {100*DN[m].mean():.2f}")
print(f"plane mean L  ref {h[m].mean():.4f}  r10 {g[m].mean():.4f}  new {n[m].mean():.4f}"
      f"   (the pair's neutrality: new - r10 = {n[m].mean() - g[m].mean():+.4f})")

# --- bearings and pitch inside the band, same patches as m7
np_ = 160


def spec(img, x0, y0):
    p = img[y0:y0+np_, x0:x0+np_].astype(float)
    ry, rx = np.mgrid[0:np_, 0:np_]
    M = np.stack([np.ones(np_*np_), rx.ravel(), ry.ravel(), (rx*rx).ravel(),
                  (ry*ry).ravel(), (rx*ry).ravel()], 1)
    c, *_ = np.linalg.lstsq(M, p.ravel(), rcond=None)
    p = p - (M @ c).reshape(np_, np_)
    w = np.hanning(np_)[:, None] * np.hanning(np_)[None, :]
    P = np.abs(np.fft.fftshift(np.fft.fft2(p * w))) ** 2
    fy, fx = np.mgrid[0:np_, 0:np_] - np_//2
    r = np.hypot(fx, fy)
    keep = (r >= np_/60.0) & (r <= np_/2.2)
    th = (np.degrees(np.arctan2(fy, fx)) + 90) % 180
    bins = np.array([P[keep & (th >= i*5) & (th < (i+1)*5)].sum() for i in range(36)])
    bins /= bins.sum()
    lam = (P[keep] * (np_ / np.maximum(r[keep], 1e-9))).sum() / P[keep].sum()
    return p.std(), bins, lam


print()
for name, (x0, y0) in {"band-left": (40, 560), "band-mid": (150, 430),
                       "above-band": (300, 120)}.items():
    for lbl, img in (("ref ", h), ("r10 ", g), ("new ", n)):
        sd, bins, lam = spec(img, x0, y0)
        top = np.argsort(bins)[::-1][:3]
        pk = ", ".join(f"{(i*5 + 2.5 + 90) % 180 - 90:+5.0f}c {bins[i]*100:.0f}%"
                       for i in top)
        print(f"{name:11s} {lbl} sd {sd:.4f}  mean_lambda {lam:5.1f}px  "
              f"aniso {bins.max()/bins.mean():5.2f}  {pk}")
    print()
