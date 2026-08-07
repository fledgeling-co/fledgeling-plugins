"""What amplitude, what pitch, what bearings - inside the band, measured.

hp_sd(3-13px) per 64px canvas-y band on the un-planed plane sets the amplitude target
(it scales linearly in a mark's luminance swing and as sqrt of the mark density).
The 2-D spectrum of a clean patch inside the band gives the bearings and the pitch, in
canvas degrees; the build authors them in the blade's local frame, so the local-frame
bearing of each family is printed too.
"""
import math, numpy as np

W = 1024
h = np.load("h1024.npy"); g = np.load("g1024.npy")
rough = np.load("rough.npy")
yy, xx = np.mgrid[0:W, 0:W].astype(float)


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w*w))[:x.shape[0], :x.shape[1]]


hp = lambda i: box(i, 3) - box(i, 13)
hpc, hph = hp(g), hp(h)
print(f"{'y band':>10s} {'px':>7s} {'ref hp_sd':>10s} {'our hp_sd':>10s} {'ref/our':>8s}")
rows = []
for y0 in range(64, 960, 64):
    sel = rough & (yy >= y0) & (yy < y0 + 64)
    if sel.sum() < 1500:
        continue
    a, b = hph[sel].std(), hpc[sel].std()
    rows.append((y0 + 32, a, b))
    print(f"{y0:4d}-{y0+64:4d} {sel.sum():7d} {a:10.4f} {b:10.4f} {a/b:8.2f}")
np.save("hpprof.npy", np.array(rows))

# ---- bearings and pitch inside the band, on a clean 160px patch
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
n = 160


def spec(img, x0, y0):
    p = img[y0:y0+n, x0:x0+n].astype(float)
    ry, rx = np.mgrid[0:n, 0:n]
    M = np.stack([np.ones(n*n), rx.ravel(), ry.ravel(), (rx*rx).ravel(),
                  (ry*ry).ravel(), (rx*ry).ravel()], 1)
    c, *_ = np.linalg.lstsq(M, p.ravel(), rcond=None)
    p = p - (M @ c).reshape(n, n)
    w = np.hanning(n)[:, None] * np.hanning(n)[None, :]
    P = np.abs(np.fft.fftshift(np.fft.fft2(p * w))) ** 2
    fy, fx = np.mgrid[0:n, 0:n] - n//2
    r = np.hypot(fx, fy)
    keep = (r >= n/60.0) & (r <= n/2.2)
    th = (np.degrees(np.arctan2(fy, fx)) + 90) % 180        # ridge bearing
    bins = np.zeros(36)
    for i in range(36):
        m = keep & (th >= i*5) & (th < (i+1)*5)
        bins[i] = P[m].sum() if m.any() else 0
    bins /= bins.sum()
    lam_e = (P[keep] * (n / np.maximum(r[keep], 1e-9))).sum() / P[keep].sum()
    return p.std(), bins, lam_e


for name, (x0, y0) in {"band-left": (40, 560), "band-mid": (150, 430),
                       "above-band": (300, 120), "above-band-2": (620, 60)}.items():
    for lbl, img in (("ref ", h), ("ours", g)):
        sd, bins, lam = spec(img, x0, y0)
        top = np.argsort(bins)[::-1][:3]
        def canv(i):
            b = (i*5 + 2.5 + 90) % 180 - 90
            return b
        def loc(i):
            b = math.radians(canv(i))
            # canvas bearing -> local-frame bearing (frame is a pure rotation by -ANG)
            return math.degrees(math.atan2(math.sin(b)*UX - math.cos(b)*UY,
                                           math.cos(b)*UX + math.sin(b)*UY))
        pk = ", ".join(f"{canv(i):+5.0f}c/{loc(i):+5.0f}L {bins[i]*100:.0f}%" for i in top)
        print(f"{name:13s} {lbl}  sd {sd:.4f}  mean_lambda {lam:5.1f}px  "
              f"aniso {bins.max()/bins.mean():4.2f}  {pk}")
    print()
