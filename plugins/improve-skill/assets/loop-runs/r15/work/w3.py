"""Characterise the reference's block-face texture, at the metric's own thresholds."""
import numpy as np
import common as C

c, r = C.cand(), C.ref()
Lc, Lr = C.lum(c), C.lum(r)
xs, ys = C.grid(Lc.shape)
lx, ly = C.to_local_top(xs, ys)
face = (lx > 8) & (lx < C.BLADE_LEN - 8) & (ly > 8) & (ly < C.BLADE_THICK - 8)
dark = (Lc < 0.45) & (Lr < 0.55) & (c[..., 0] - c[..., 2] < 0.20) & (r[..., 0] - r[..., 2] < 0.20)
m = face & dark


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy)


sc, sr = sobel(Lc), sobel(Lr)
print("METRIC-THRESHOLD edges (|sobel| > 0.40) on the face:")
print("  cand %.2f%%  ref %.2f%%" % (100 * (sc[m] > 0.4).mean(), 100 * (sr[m] > 0.4).mean()))
print("whole image: cand %.2f%%  ref %.2f%%" % (100 * (sc > 0.4).mean(), 100 * (sr > 0.4).mean()))
print("face share of all ref metric-edges: %.2f%%"
      % (100 * (sr[m] > 0.4).sum() / max((sr > 0.4).sum(), 1)))

# high-pass (3-13px) amplitude on the face, ref, by tile along local x
hp = lambda L: L - C.boxblur(L, 6)
hc, hr = hp(Lc), hp(Lr)
print("\nref face high-pass sd by local-x sixth (ly split near/far):")
for y0, y1, tag in [(8, 106, "near"), (106, 196, "far ")]:
    row = []
    for i in range(6):
        x0, x1 = 8 + i * 104, 8 + (i + 1) * 104
        t = m & (lx >= x0) & (lx < x1) & (ly >= y0) & (ly < y1)
        row.append(hr[t].std() if t.sum() > 400 else float("nan"))
    print("  %s " % tag + " ".join("%.4f" % v for v in row))

# anisotropy of the ref's face texture: directional gradient energy in the FACE frame
g_lx = np.gradient(hr, axis=1)
g_ly = np.gradient(hr, axis=0)
# rotate canvas gradients into the top-face frame
a, b = C.UX, C.UY - C.K_RISE
cc, dd = C.NX, C.NY
gu = g_lx * a + g_ly * b
gv = g_lx * cc + g_ly * dd
print("\nref face gradient energy: along-blade %.5f  across-blade %.5f  ratio %.2f"
      % ((gu[m] ** 2).mean(), (gv[m] ** 2).mean(),
         (gu[m] ** 2).mean() / max((gv[m] ** 2).mean(), 1e-12)))
gu2 = (np.gradient(hc, axis=1) * a + np.gradient(hc, axis=0) * b)
gv2 = (np.gradient(hc, axis=1) * cc + np.gradient(hc, axis=0) * dd)
print("cand face gradient energy: along %.5f  across %.5f  ratio %.2f"
      % ((gu2[m] ** 2).mean(), (gv2[m] ** 2).mean(),
         (gu2[m] ** 2).mean() / max((gv2[m] ** 2).mean(), 1e-12)))

# is the speckle chromatic? high-pass each channel of the ref
print("\nref face per-channel high-pass sd: " +
      " ".join("%.4f" % hp(r[..., k])[m].std() for k in range(3)))
print("cand face per-channel high-pass sd: " +
      " ".join("%.4f" % hp(c[..., k])[m].std() for k in range(3)))

# skew: does the speckle bias light or dark?
print("\nref face hp skew %.3f  p1 %.3f p50 %.3f p99 %.3f"
      % (float(((hr[m] - hr[m].mean()) ** 3).mean() / hr[m].std() ** 3),
         np.percentile(hr[m], 1), np.percentile(hr[m], 50), np.percentile(hr[m], 99)))

# does it survive downsampling? LANCZOS the ref, remeasure sd inside the face
from PIL import Image
for size in (256, 128):
    im = Image.fromarray((r * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    L2 = C.lum(np.asarray(im).astype(np.float64) / 255)
    mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((size, size), Image.NEAREST)) > 128
    print("ref face hp sd at %4d: %.4f  (mask px %d)" % (size, (L2 - C.boxblur(L2, max(1, 6 * size // 1024)))[mm].std(), mm.sum()))
