"""r12 diagnostic 6: WHAT carries C2's iron-face gradient tail?

d5 says C2's face core matches ours on mean and p90 Sobel and beats it 6:1 at p99.9.
Before authoring that tail, find out what it is: scattered pits, or a few long scratches.
Cluster the above-threshold pixels and look at their run lengths and their bearings.
"""
import sys, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

h = np.load("d_h.npy"); g = np.load("d_g.npy")
TOP = np.load("d_topface.npy")
core = ~F.dilate(~TOP, 26)

er = F.sobel_edges(h) & core
ys, xs = np.nonzero(er)
print("ref face-core edge pixels: %d over %d px (%.2f%%)" % (er.sum(), core.sum(), 100 * er.mean() * core.size / core.sum()))
print("bbox of those pixels: x %d-%d  y %d-%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

# connected components, 8-neighbour, iterative label propagation
lab = np.zeros_like(er, dtype=np.int32)
lab[er] = np.arange(1, er.sum() + 1)
for _ in range(60):
    m = lab.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            m = np.maximum(m, np.roll(np.roll(lab, dy, 0), dx, 1))
    m[~er] = 0
    if (m == lab).all():
        break
    lab = m
ids, counts = np.unique(lab[er], return_counts=True)
counts = np.sort(counts)[::-1]
print("components: %d   sizes: top10 %s" % (len(ids), counts[:10].tolist()))
print("  size<=4 px: %d comps (%.0f%% of edge px)  size>=20: %d comps (%.0f%% of edge px)"
      % ((counts <= 4).sum(), 100 * counts[counts <= 4].sum() / counts.sum(),
         (counts >= 20).sum(), 100 * counts[counts >= 20].sum() / counts.sum()))

# elongation of the big ones
print("  the 6 largest components, as (px, bbox w x h, elongation):")
for cid in [i for i in ids if (lab[er] == i).sum() >= 20][:0] or \
           sorted(ids, key=lambda i: -(lab == i).sum())[:6]:
    yy, xx = np.nonzero(lab == cid)
    w, hh = xx.max() - xx.min() + 1, yy.max() - yy.min() + 1
    print("     %5d px  %3d x %3d   elong %.1f" % (len(yy), w, hh, max(w, hh) / max(min(w, hh), 1)))

# how DEEP are the tail features? sample L at the tail pixels vs the face mean
p = np.pad(h, 1, mode="edge")
gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
mag = np.hypot(gx, gy)
tail = core & (mag > 0.40)
hp = h - F.box_mean(h, 13)
print()
print("ref tail pixels (%d): local high-pass L  mean %+.4f  p5 %+.4f  p95 %+.4f"
      % (tail.sum(), hp[tail].mean(), np.percentile(hp[tail], 5), np.percentile(hp[tail], 95)))
print("   dark side (hp<0) %.0f%% of tail; face-core mean L %.4f" % (100 * (hp[tail] < 0).mean(), h[core].mean()))

vis = np.stack([h[core.any(1)][:, core.any(0)]] * 3, -1)
box = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
v = np.stack([h[box]] * 3, -1)
v[..., 0][er[box]] = 1.0
v[..., 1][er[box]] = 0.2
v[..., 2][er[box]] = 0.2
Image.fromarray((np.clip(v, 0, 1) * 255).astype(np.uint8)).save("z-ref-face-tail.png")
