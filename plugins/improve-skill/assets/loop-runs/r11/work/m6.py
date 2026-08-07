"""Two more candidate coordinates for relief visibility, both physical and both cheap
for the generator to evaluate: the field's own smoothed luminance (relief is visible
where the light rakes, and raking is what makes the field dark), and canvas y with the
block's cast shadow excluded, since a shadow is dark without being raked.
"""
import math, numpy as np

W = 1024
h = np.load("h1024.npy"); g = np.load("g1024.npy")
rough = np.load("rough.npy"); r_key = np.load("rkey.npy"); ly = np.load("ly.npy")


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w*w))[:x.shape[0], :x.shape[1]]


def sobel(img, thresh=0.10):
    p = np.pad(img, 1, mode="edge")
    gx = (p[:-2, 2:] + 2*p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2*p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thresh * 4


dens = box(sobel(h), 41)
yy, xx = np.mgrid[0:W, 0:W].astype(float)
CO = {"canvas y": yy,
      "ref field L (61px)": box(h, 61),
      "our field L (61px)": box(g, 61),
      "r from key": r_key,
      "r from (300,900)": np.hypot(xx-300, yy-900)}
m = rough
res = {}
for name, s in CO.items():
    v, d = s[m], dens[m]
    qs = np.quantile(v, np.linspace(0, 1, 25))
    idx = np.clip(np.searchsorted(qs, v, "right") - 1, 0, 23)
    r = d.copy()
    for b in range(24):
        sel = idx == b
        if sel.sum() > 50:
            r[sel] -= d[sel].mean()
    res[name] = r.std()
for name, sd in sorted(res.items(), key=lambda kv: kv[1]):
    print(f"{name:22s} {sd:.5f}")
print(f"{'flat':22s} {dens[m].std():.5f}")

# The profile we would author from, in canvas y, in the units the build speaks:
# reference relief edge-density, and its ratio to ours, in fixed 64px bands.
dc = box(sobel(g), 41)
print("\ncanvas-y profile of relief visibility on the un-planed plane:")
print(f"{'y band':>10s} {'px':>7s} {'ref d%':>7s} {'our d%':>7s} {'ref/our':>8s} "
      f"{'ref L':>6s} {'our L':>6s}")
bl, bh_ = box(h, 61), box(g, 61)
rows = []
for y0 in range(64, 960, 64):
    sel = m & (yy >= y0) & (yy < y0 + 64)
    if sel.sum() < 1500:
        continue
    rd, cd = dens[sel].mean(), dc[sel].mean()
    rows.append((y0 + 32, rd, cd))
    print(f"{y0:4d}-{y0+64:4d} {sel.sum():7d} {100*rd:7.2f} {100*cd:7.2f} "
          f"{rd/max(cd,1e-6):8.2f} {bl[sel].mean():6.3f} {bh_[sel].mean():6.3f}")
np.save("yprof.npy", np.array(rows))
