"""Where is the residual, by 64px cell and by named region."""
import numpy as np
import common as C

c, r = C.cand(), C.ref()
Lc, Lr = C.lum(c), C.lum(r)
res = np.abs(Lc - Lr)

print("global mean |dL| = %.4f" % res.mean())

# 64px cells
n = 16
cell = res.reshape(n, 64, n, 64).mean(axis=(1, 3))
print("\n64px-cell mean |dL| (rows = y):")
for j in range(n):
    print("y%4d " % (j * 64) + " ".join("%4.0f" % (cell[j, i] * 1000) for i in range(n)))

# named regions, in the icon's own frame
xs, ys = C.grid(Lc.shape)
lx_t, ly_t = C.to_local_top(xs, ys)      # sheared top-face frame
lx_f, ly_f = C.to_local(xs, ys)          # footprint frame

top_face = (lx_t > 4) & (lx_t < C.BLADE_LEN - 4) & (ly_t > 4) & (ly_t < C.BLADE_THICK - 4)
# front face: between the top-face cutting edge and the footprint cutting edge
front = (lx_f > 10) & (lx_f < C.BLADE_LEN - 10) & (ly_f > -2) & (ly_f < 2)
ground_rough = (ly_f > 40) & ~top_face
ground_true = (ly_f < -40) & ~top_face
# curl: a disc around its centre
cx, cy = 308.0, 278.0
curl = ((xs - cx) ** 2 + (ys - cy) ** 2 < 190 ** 2) & ~top_face

# squircle interior: use reference alpha-ish -> both images are opaque; use a margin
inner = (xs > 60) & (xs < 964) & (ys > 60) & (ys < 964)

for name, m in [("block top face", top_face),
                ("ground un-planed", ground_rough & inner),
                ("ground trued", ground_true & inner),
                ("curl disc", curl & inner)]:
    print("\n%-18s px=%7d  mean|dL|=%.4f  cand L=%.3f ref L=%.3f  dL(signed)=%+.4f"
          % (name, m.sum(), res[m].mean(), Lc[m].mean(), Lr[m].mean(),
             (Lc - Lr)[m].mean()))
    hc, hr = C.highpass(Lc), C.highpass(Lr)
    print("   highpass sd  cand=%.4f  ref=%.4f  ratio=%.2f"
          % (hc[m].std(), hr[m].std(), hc[m].std() / max(hr[m].std(), 1e-9)))
