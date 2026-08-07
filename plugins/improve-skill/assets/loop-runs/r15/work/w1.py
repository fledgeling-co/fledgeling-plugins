"""The block's top face: which spatial band is missing, and where on the face."""
import numpy as np
import common as C

c, r = C.cand(), C.ref()
Lc, Lr = C.lum(c), C.lum(r)
xs, ys = C.grid(Lc.shape)
lx, ly = C.to_local_top(xs, ys)
face = (lx > 8) & (lx < C.BLADE_LEN - 8) & (ly > 8) & (ly < C.BLADE_THICK - 8)

print("face px", face.sum())
print("\nband-limited sd on the block top face (L, band = blur(k1)-blur(k2)):")
print(" band(px)      cand      ref   ratio")
for k1, k2 in [(0, 1), (1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 64)]:
    bc = (C.boxblur(Lc, k1) if k1 else Lc) - C.boxblur(Lc, k2)
    br = (C.boxblur(Lr, k1) if k1 else Lr) - C.boxblur(Lr, k2)
    print("  %2d-%3d   %8.5f %8.5f   %5.2f"
          % (2 * k1 + 1, 2 * k2 + 1, bc[face].std(), br[face].std(),
             bc[face].std() / max(br[face].std(), 1e-9)))

# where on the face: 4 x 2 tiles in local coords
print("\nper-tile (local lx bands x ly halves): mean L and highpass(k=6) sd")
hc, hr = C.highpass(Lc, 6), C.highpass(Lr, 6)
for jy, (y0, y1) in enumerate([(8, 106), (106, 196)]):
    for ix in range(4):
        x0, x1 = 8 + ix * 156, 8 + (ix + 1) * 156
        m = face & (lx >= x0) & (lx < x1) & (ly >= y0) & (ly < y1)
        if m.sum() < 500:
            continue
        print("  lx %3d-%3d ly %3d-%3d  n=%6d  L %.3f/%.3f  hp sd %.4f/%.4f  ratio %.2f"
              % (x0, x1, y0, y1, m.sum(), Lc[m].mean(), Lr[m].mean(),
                 hc[m].std(), hr[m].std(), hc[m].std() / max(hr[m].std(), 1e-9)))

# saturation and hue of the face, and its darkest pixels
for name, a, L in [("cand", c, Lc), ("ref", r, Lr)]:
    s = C.sat(a)
    v = L[face]
    idx = np.argsort(v)
    px = a[face]
    dk = px[idx[:max(1, len(idx)//200)]].mean(axis=0)
    bt = px[idx[-max(1, len(idx)//200):]].mean(axis=0)
    print("\n%s face: L p10 %.3f p50 %.3f p90 %.3f  sat mean %.3f"
          % (name, np.percentile(v, 10), np.percentile(v, 50), np.percentile(v, 90),
             s[face].mean()))
    print("   darkest 0.5%% rgb %s  sat %.3f" % (np.round(dk * 255).astype(int),
          (dk.max() - dk.min()) / max(dk.max(), 1e-6)))
    print("   lightest 0.5%% rgb %s  sat %.3f" % (np.round(bt * 255).astype(int),
          (bt.max() - bt.min()) / max(bt.max(), 1e-6)))
