"""Fit the coordinate again, this time against the quantity the build actually authors:
the local rms of the 3-13px high-pass, i.e. relief AMPLITUDE, not the thresholded edge
count. r08 read this same fall-off in the blade's local frame (sd 12.6 at the cut, 18.3
at ly 285, 5.6 by ly 513) so the two candidate stories - "distance out from the pass"
and "distance down the tile" - both have prior support and only one can win.
"""
import math, numpy as np

W = 1024
h = np.load("h1024.npy"); g = np.load("g1024.npy")
rough = np.load("rough.npy"); rkey = np.load("rkey.npy"); ly = np.load("ly.npy")
yy, xx = np.mgrid[0:W, 0:W].astype(float)
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
AX, AY = 543.0 - UX*320.0, 604.0 - UY*320.0
lx = UX*(xx - AX) + UY*(yy - AY)


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w*w))[:x.shape[0], :x.shape[1]]


def relief_rms(img):
    hp = box(img, 3) - box(img, 13)
    return np.sqrt(np.maximum(box(hp*hp, 41), 0))


A, B = relief_rms(h), relief_rms(g)
CO = {"canvas y": yy, "local ly (out from the cut)": ly, "local lx": lx,
      "r from key (75,25)": rkey, "canvas x": xx,
      "u = (x+y)/sqrt2": (xx+yy)/math.sqrt(2)}
for cx, cy in ((300, 900), (150, 650), (512, 1024)):
    CO[f"r from ({cx},{cy})"] = np.hypot(xx-cx, yy-cy)

m = rough
print(f"{'coordinate':30s} {'resid sd':>9s} {'var explained':>14s}")
tot = A[m].std()
out = []
for name, s in CO.items():
    v, d = s[m], A[m]
    qs = np.quantile(v, np.linspace(0, 1, 25))
    idx = np.clip(np.searchsorted(qs, v, "right") - 1, 0, 23)
    r = d.copy()
    for b in range(24):
        sel = idx == b
        if sel.sum() > 50:
            r[sel] -= d[sel].mean()
    out.append((r.std(), name))
for sd, name in sorted(out):
    print(f"{name:30s} {sd:9.5f} {100*(1-(sd/tot)**2):13.1f}%")
print(f"{'flat':30s} {tot:9.5f} {0.0:13.1f}%")

win = sorted(out)[0][1]
s = CO[win]
print(f"\nprofile of relief amplitude along '{win}', ref and ours, 14 equal-count bins:")
qs = np.quantile(s[m], np.linspace(0, 1, 15))
print(f"{'lo':>8s} {'hi':>8s} {'px':>7s} {'ref rms':>9s} {'our rms':>9s} {'ref/our':>8s}")
prof = []
for b in range(14):
    sel = m & (s >= qs[b]) & (s < qs[b+1])
    a, c = A[sel].mean(), B[sel].mean()
    prof.append(((qs[b]+qs[b+1])/2, a, c))
    print(f"{qs[b]:8.0f} {qs[b+1]:8.0f} {sel.sum():7d} {a:9.4f} {c:9.4f} {a/c:8.2f}")
np.save("ampprof.npy", np.array(prof))
print("\ncoordinate saved as:", win)
