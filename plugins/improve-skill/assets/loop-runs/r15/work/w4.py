"""Front face too? And what the block's other in-scope details measure."""
import numpy as np
import common as C

c, r = C.cand(), C.ref()
Lc, Lr = C.lum(c), C.lum(r)
xs, ys = C.grid(Lc.shape)
lx_f, ly_f = C.to_local(xs, ys)          # footprint frame
lx_t, ly_t = C.to_local_top(xs, ys)      # top-face frame

# The front face is the strip between the lifted cutting edge and the footprint one:
# in the footprint frame it lies at ly ~ 0, spanning `rise` px of canvas y above it.
rise = C.rise_at(np.clip(lx_f, 0, C.BLADE_LEN))
# canvas y of the footprint cutting edge at this lx
fy = C.AY + C.UY * lx_f
front = (lx_f > 30) & (lx_f < C.BLADE_LEN - 30) & (ys < fy - 6) & (ys > fy - rise + 8) & (np.abs(ly_f) < 30)
dark = (Lc < 0.5) & (Lr < 0.6) & (c[..., 0] - c[..., 2] < 0.18) & (r[..., 0] - r[..., 2] < 0.18)
mf = front & dark
hp = lambda L: L - C.boxblur(L, 6)
hc, hr = hp(Lc), hp(Lr)
print("front face co-masked px %d  L %.3f/%.3f  hp sd %.4f/%.4f  ratio %.2f"
      % (mf.sum(), Lc[mf].mean(), Lr[mf].mean(), hc[mf].std(), hr[mf].std(),
         hc[mf].std() / max(hr[mf].std(), 1e-9)))

# The back arris: is the reference's back rim brighter/narrower than ours?
print("\nprofile across the back edge (top-face frame, ly = BLADE_THICK - d), mean L:")
face = (lx_t > 120) & (lx_t < C.BLADE_LEN - 120)
for d in range(-6, 20, 2):
    band = face & (np.abs(ly_t - (C.BLADE_THICK - d)) < 1.0)
    if band.sum() < 200:
        continue
    print("  d=%3d n=%5d  cand %.3f  ref %.3f" % (d, band.sum(), Lc[band].mean(), Lr[band].mean()))

# curl: fine texture?
cx, cy = 308.0, 278.0
curl = ((xs - cx) ** 2 + (ys - cy) ** 2 < 170 ** 2) & (Lc > 0.5) & (Lr > 0.5) & (ly_f > 60)
print("\ncurl-ish region px %d  hp sd cand %.4f ref %.4f ratio %.2f"
      % (curl.sum(), hc[curl].std(), hr[curl].std(), hc[curl].std() / max(hr[curl].std(), 1e-9)))
