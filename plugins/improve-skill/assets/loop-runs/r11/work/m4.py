"""Fit the coordinate before you fit the curve (r08's recipe), applied to relief
VISIBILITY rather than to luminance. The reference's rough-plane relief lives in a
narrow band; a point key with ambient fill predicts a broad hump and fits barely
better than a flat line, so the band is probably not a function of distance from the
light at all. Bin a smoothed edge-density field by each candidate coordinate and take
the pooled within-bin residual sd: the coordinate the band actually depends on wins.
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


dens = box(sobel(h), 41)          # reference relief visibility, smoothed
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX, AY = 543.0 - UX*320.0, 604.0 - UY*320.0
yy, xx = np.mgrid[0:W, 0:W].astype(float)
lx = UX*(xx - AX) + UY*(yy - AY)

CO = {"r from key (75,25)": r_key,
      "|ly| from the cut": np.abs(ly),
      "local x along blade": lx,
      "canvas x": xx, "canvas y": yy,
      "u = (x+y)/sqrt2": (xx + yy)/math.sqrt(2)}
for cx, cy in ((512, 512), (300, 900), (75, 25), (900, 100), (150, 650), (543, 604)):
    CO[f"r from ({cx},{cy})"] = np.hypot(xx-cx, yy-cy)

m = rough
print(f"{'coordinate':24s} {'nbins':>6s} {'within-bin resid sd':>20s}")
out = []
for name, s in CO.items():
    v = s[m]; d = dens[m]
    qs = np.quantile(v, np.linspace(0, 1, 25))
    idx = np.clip(np.searchsorted(qs, v, "right") - 1, 0, 23)
    res = d.copy()
    for b in range(24):
        sel = idx == b
        if sel.sum() > 50:
            res[sel] -= d[sel].mean()
    out.append((res.std(), name))
for sd, name in sorted(out):
    print(f"{name:24s} {24:6d} {sd:20.5f}")
print(f"{'(flat: total sd)':24s} {1:6d} {dens[m].std():20.5f}")

# the winner's own profile, and ours on the same coordinate
best = dict(CO)[sorted(out)[0][1]]
dc = box(sobel(g), 41)
qs = np.quantile(best[m], np.linspace(0, 1, 13))
print(f"\nprofile along '{sorted(out)[0][1]}' (12 equal-count bins):")
print(f"{'lo':>7s} {'hi':>7s} {'px':>7s} {'ref d%':>7s} {'cand d%':>8s}")
for b in range(12):
    sel = m & (best >= qs[b]) & (best < qs[b+1])
    print(f"{qs[b]:7.0f} {qs[b+1]:7.0f} {sel.sum():7d} {100*dens[sel].mean():7.2f} "
          f"{100*dc[sel].mean():8.2f}")
