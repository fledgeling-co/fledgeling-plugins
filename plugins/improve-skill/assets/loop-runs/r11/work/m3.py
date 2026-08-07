"""The reference's ground relief is not flat in radius. Measure the profile, then ask
whether one point key over a rough plane with an ambient fill explains it.

Two statistics per radius bin on the un-planed plane, both after a quadratic detrend
inside the bin so the FIELD is removed and only the relief is left:
  hp_sd    - rms of the 3-12px high-pass: how much relief energy is there
  edge_d   - fraction of pixels the scorer's own Sobel calls an edge: how SHARP it is

Model. A point key at height z0 above the plane, horizontal distance r from its foot
at (75, 25), plus a constant ambient fill:
    E(r)   = z0 / (z0^2 + r^2)^1.5        direct irradiance, cosine + inverse square
    c(r)   = E / (E + a)                  contrast of a cast micro-shadow
    w(r)   = r / z0                       its width, in ridge heights
    v(r)   = c(r) * min(1, w(r) / w1)     visibility of the relief
Near the key the light is near-normal and a ridge casts nothing; far away the direct
term has died and the ambient fills the shadow in. The band between them is where the
light rakes, and that is the only place relief is legible.
"""
import numpy as np

W = 1024
g = np.load("g1024.npy"); h = np.load("h1024.npy")
rough = np.load("rough.npy"); r_key = np.load("rkey.npy")


def sobel(img, thresh=0.10):
    p = np.pad(img, 1, mode="edge")
    gx = (p[:-2, 2:] + 2*p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2*p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thresh * 4


def box(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w*w))[:x.shape[0], :x.shape[1]]


def highpass(img, lo=3, hi=13):
    return box(img, lo) - box(img, hi)


hpc, hph = highpass(g), highpass(h)
ec, eh = sobel(g), sobel(h)

BINS = [(150, 250), (250, 350), (350, 450), (450, 550), (550, 650),
        (650, 750), (750, 850), (850, 950)]
print(f"{'r':>9s} {'px':>7s} {'cand hp_sd':>10s} {'ref hp_sd':>10s} "
      f"{'cand e%':>8s} {'ref e%':>8s} {'ref/cand hp':>11s}")
prof = []
for lo, hi in BINS:
    m = rough & (r_key >= lo) & (r_key < hi)
    if m.sum() < 800:
        continue
    a, b = hpc[m].std(), hph[m].std()
    prof.append(((lo+hi)/2, b, (eh & m).mean() if m.any() else 0,
                 (eh & m).sum()/m.sum(), (ec & m).sum()/m.sum(), a, m.sum()))
    print(f"{lo:4d}-{hi:4d} {m.sum():7d} {a:10.4f} {b:10.4f} "
          f"{100*(ec&m).sum()/m.sum():8.2f} {100*(eh&m).sum()/m.sum():8.2f} {b/a:11.2f}")

# ---- fit the two-parameter light model to the reference's own edge-density profile
r = np.array([p[0] for p in prof])
d = np.array([p[3] for p in prof])       # reference edge density
wts = np.array([p[6] for p in prof], float)
wts /= wts.sum()


def model(r, z0, a, w1):
    E = z0 / (z0*z0 + r*r) ** 1.5
    return E / (E + a) * np.minimum(1.0, (r / z0) / w1)


best = None
for z0 in np.arange(120, 1400, 20.0):
    for a in 10.0 ** np.arange(-9.5, -4.0, 0.05):
        for w1 in np.arange(0.2, 6.0, 0.1):
            v = model(r, z0, a, w1)
            k = (wts * v * d).sum() / max((wts * v * v).sum(), 1e-30)
            e = (wts * (k*v - d) ** 2).sum()
            if best is None or e < best[0]:
                best = (e, z0, a, w1, k)
e, z0, a, w1, k = best
print(f"\nfit: z0 {z0:.0f}px  ambient/I {a:.3e}  w1 {w1:.2f}  scale {k:.3f}  "
      f"weighted rms {e**0.5:.4f} against a profile whose mean is {(wts*d).sum():.4f}")
v = k * model(r, z0, a, w1)
print(f"{'r':>5s} {'ref e%':>7s} {'model%':>7s}")
for i in range(len(r)):
    print(f"{r[i]:5.0f} {100*d[i]:7.2f} {100*v[i]:7.2f}")
# flat model for comparison
flat = (wts*d).sum()
print(f"\nflat-profile weighted rms {((wts*(flat-d)**2).sum())**0.5:.4f}")
np.save("refprof.npy", np.stack([r, d, np.array([p[4] for p in prof])]))
