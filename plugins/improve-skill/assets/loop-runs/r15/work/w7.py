"""Does an ALIGNED, sparse, high-amplitude streak field pay where isotropic relief did not?

The r13/r14 rule says mark size is an SSIM term and mark direction is an edge
term. The metric's Sobel threshold is 0.10 per pixel, so only marks that clear
a 40% local step on a 0.25 face are visible to edge_f1 at all. Test both.
"""
import numpy as np
from PIL import Image
import common as C
from w5 import ssim, edge_f1, sobel_edges, comp, base, fractal, rng  # noqa

c = C.cand()
r = C.ref()
xs, ys = C.grid((1024, 1024))
lx, ly = C.to_local_top(xs, ys)
face = (lx > 0) & (lx < C.BLADE_LEN) & (ly > 0) & (ly < C.BLADE_THICK) & (C.lum(c) < 0.45)

Lr = C.lum(r)
sob = lambda g: np.hypot(*np.gradient(g)) * 0  # placeholder


def metric_edges(g, thr=0.10):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thr * 4


print("ref face metric-edge density %.2f%%" % (100 * metric_edges(Lr)[face].mean()))


def streaks(pitch, width, amp, dash=0.55, back_only=True, seed=3):
    """Marks along the blade axis on the top face: a phase field in local ly."""
    g = np.random.default_rng(seed)
    fld = np.zeros((1024, 1024))
    y = 6.0
    while y < C.BLADE_THICK - 6:
        w = width * (0.7 + 0.6 * g.random())
        a = amp * (0.6 + 0.8 * g.random()) * (1 if g.random() < 0.5 else -1)
        band = np.abs(ly - y) < w / 2
        # dashes along lx
        ph = (lx / (40 + 60 * g.random()) + g.random() * 10)
        on = (np.sin(ph * 2 * np.pi) > 1 - 2 * dash)
        w8 = 1.0
        if back_only:
            w8 = np.clip((ly - 40) / 70.0, 0.25, 1.0)
        fld = np.where(band & on & face, a * w8, fld)
        y += pitch * (0.6 + 0.8 * g.random())
    return fld


for pitch, width, amp in [(9.0, 2.2, 0.070), (14.0, 2.6, 0.090), (6.0, 1.8, 0.055)]:
    add = streaks(pitch, width, amp)
    c2 = np.clip(c + add[..., None], 0, 1)
    L2 = C.lum(c2)
    hp = (L2 - C.boxblur(L2, 6))[face].std()
    ed = 100 * metric_edges(L2)[face].mean()
    tot, line = 0.0, []
    for size in (1024, 256, 128, 32, 16):
        a_ = np.asarray(Image.fromarray((c2 * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
        b_ = np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
        ga, gb = C.lum(a_), C.lum(b_)
        m = {"lum_delta": np.abs(ga - gb).mean(), "ssim": ssim(ga, gb),
             "edge_f1": edge_f1(ga, gb), "mask_iou": 1.0}
        d = comp(size, m) - comp(size, base[size])
        tot += d
        line.append("%d %+.4f (ssim%+.4f edge%+.4f)" % (size, d, m["ssim"] - base[size]["ssim"],
                                                        m["edge_f1"] - base[size]["edge_f1"]))
    print("\npitch %.0f width %.1f amp %.3f -> face hp sd %.4f, metric-edge %.2f%%  NET %+.4f"
          % (pitch, width, amp, hp, ed, tot))
    print("   " + "  ".join(line))
