"""Predict the metric response of adding face relief, before authoring it.

Multiply the candidate's block face by a synthetic relief field with the
reference's measured spectrum / amplitude / skew, then recompute the metrics
the way fidelity.py does. Uncorrelated detail costs SSIM and buys edge_f1
(r02); this says by how much, here, at this area share.
"""
import numpy as np
from PIL import Image
import common as C

rng = np.random.default_rng(11)
NEUTRAL = 128 / 255


def box_mean(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[: x.shape[0], : x.shape[1]]


def ssim(a, b):
    w = max(3, min(11, a.shape[0] // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    ma, mb = box_mean(a, w), box_mean(b, w)
    va = box_mean(a * a, w) - ma ** 2
    vb = box_mean(b * b, w) - mb ** 2
    cov = box_mean(a * b, w) - ma * mb
    s = ((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2))
    return float(np.clip(s, -1, 1).mean())


def sobel_edges(g, thresh=0.10):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thresh * 4


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def edge_f1(a, b):
    ea, eb = sobel_edges(a), sobel_edges(b)
    keep = ~rim_mask(a.shape[0])
    ea, eb = ea & keep, eb & keep
    tp_p = (ea & dilate(eb)).sum()
    tp_r = (eb & dilate(ea)).sum()
    prec = tp_p / max(ea.sum(), 1)
    rec = tp_r / max(eb.sum(), 1)
    return float(2 * prec * rec / max(prec + rec, 1e-9))


def comp(size, m):
    lu = 1 - min(m["lum_delta"] * 4, 1.0)
    if size >= 128:
        parts = [(0.40, m["ssim"]), (0.35, lu), (0.25, m["edge_f1"])]
    else:
        parts = [(0.35, m["edge_f1"]), (0.25, m["mask_iou"]), (0.25, m["ssim"]), (0.15, lu)]
    return sum(w * v for w, v in parts)


def fractal(shape, octaves=3, f0=0.55):
    """fractalNoise-alike: octaves of smoothed white noise, 1/f amplitude."""
    out = np.zeros(shape)
    amp = 1.0
    for o in range(octaves):
        k = max(1, int(round(1 / (f0 * 2 ** o) / 2)))
        n = rng.standard_normal(shape)
        out += amp * C.boxblur(n, k) * (2 * k + 1)
        amp *= 0.5
    return out / out.std()


c = C.cand()
r = C.ref()
Lr_full = C.lum(r)
xs, ys = C.grid((1024, 1024))
lx, ly = C.to_local_top(xs, ys)
face = (lx > 0) & (lx < C.BLADE_LEN) & (ly > 0) & (ly < C.BLADE_THICK)
# only where the candidate actually paints block (the face path), not ground
face = face & (C.lum(c) < 0.45)
print("simulated face px", face.sum(), "= %.1f%% of tile" % (100 * face.mean()))

base = {}
gc0 = C.lum(c)
gr = Lr_full
for size in (1024, 256, 128, 32, 16):
    a = np.asarray(Image.fromarray((c * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
    b = np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
    ga, gb = C.lum(a), C.lum(b)
    base[size] = {"lum_delta": np.abs(ga - gb).mean(), "ssim": ssim(ga, gb),
                  "edge_f1": edge_f1(ga, gb), "mask_iou": 1.0,
                  "sc": np.percentile(ga, 90) - np.percentile(ga, 10)}

print("\n(simulated baseline, LANCZOS not rsvg -- read DELTAS only)")
for s in (1024, 256, 128, 32, 16):
    m = base[s]
    print("  %4d ssim %.4f edge %.4f lum %.4f  comp %.4f  sc %.4f"
          % (s, m["ssim"], m["edge_f1"], m["lum_delta"], comp(s, m), m["sc"]))

noise = fractal((1024, 1024))
for skew_pow, target_sd in [(1.0, 0.018), (1.0, 0.030), (2.0, 0.018), (2.0, 0.026)]:
    n = noise.copy()
    if skew_pow != 1.0:                       # bright-biased: expand the upper tail
        n = np.where(n > 0, n ** skew_pow / np.abs(noise[noise > 0] ** skew_pow).std(), n)
        n = (n - n.mean()) / n.std()
    mod = np.ones((1024, 1024))
    lvl = C.lum(c)
    mod[face] = 1 + n[face] * target_sd / np.maximum(lvl[face], 1e-3)
    c2 = c * mod[..., None]
    c2 = np.clip(c2, 0, 1)
    got = (C.lum(c2) - C.boxblur(C.lum(c2), 6))[face].std()
    tot = 0.0
    line = []
    for size in (1024, 256, 128, 32, 16):
        a = np.asarray(Image.fromarray((c2 * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
        b = np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
        ga, gb = C.lum(a), C.lum(b)
        m = {"lum_delta": np.abs(ga - gb).mean(), "ssim": ssim(ga, gb),
             "edge_f1": edge_f1(ga, gb), "mask_iou": 1.0}
        d = comp(size, m) - comp(size, base[size])
        tot += d
        sc = np.percentile(ga, 90) - np.percentile(ga, 10)
        line.append("%d: %+.4f (ssim%+.4f edge%+.4f sc%+.4f)"
                    % (size, d, m["ssim"] - base[size]["ssim"],
                       m["edge_f1"] - base[size]["edge_f1"], sc - base[size]["sc"]))
    print("\nskew_pow %.1f target_sd %.3f -> achieved face hp sd %.4f   NET %+.4f"
          % (skew_pow, target_sd, got, tot))
    for l in line:
        print("   " + l)
