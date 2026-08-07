"""Re-do the face measurement on pixels BOTH images agree are block, and crop for eyes."""
import numpy as np
from PIL import Image
import common as C

c, r = C.cand(), C.ref()
Lc, Lr = C.lum(c), C.lum(r)
xs, ys = C.grid(Lc.shape)
lx, ly = C.to_local_top(xs, ys)

face = (lx > 8) & (lx < C.BLADE_LEN - 8) & (ly > 8) & (ly < C.BLADE_THICK - 8)
# both agree it is block: dark, and not the hone glow
dark = (Lc < 0.45) & (Lr < 0.55) & (c[..., 0] - c[..., 2] < 0.20) & (r[..., 0] - r[..., 2] < 0.20)
m = face & dark
print("co-masked face px", m.sum(), "of", face.sum())

print("\n band(px)      cand      ref   ratio")
for k1, k2 in [(0, 1), (1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 64)]:
    bc = (C.boxblur(Lc, k1) if k1 else Lc) - C.boxblur(Lc, k2)
    br = (C.boxblur(Lr, k1) if k1 else Lr) - C.boxblur(Lr, k2)
    print("  %2d-%3d   %8.5f %8.5f   %5.2f"
          % (2 * k1 + 1, 2 * k2 + 1, bc[m].std(), br[m].std(),
             bc[m].std() / max(br[m].std(), 1e-9)))

hc, hr = C.highpass(Lc, 6), C.highpass(Lr, 6)
print("\nper-tile, co-masked:")
for y0, y1 in [(8, 106), (106, 196)]:
    for ix in range(4):
        x0, x1 = 8 + ix * 156, 8 + (ix + 1) * 156
        t = m & (lx >= x0) & (lx < x1) & (ly >= y0) & (ly < y1)
        if t.sum() < 500:
            print("  lx %3d-%3d ly %3d-%3d  n=%6d  (skip)" % (x0, x1, y0, y1, t.sum()))
            continue
        print("  lx %3d-%3d ly %3d-%3d  n=%6d  L %.3f/%.3f  hp sd %.4f/%.4f  ratio %.2f"
              % (x0, x1, y0, y1, t.sum(), Lc[t].mean(), Lr[t].mean(),
                 hc[t].std(), hr[t].std(), hc[t].std() / max(hr[t].std(), 1e-9)))

# edge density: fraction of pixels above a gradient threshold, the r08 instrument
def edge_frac(L, thr=4 / 255):
    gy, gx = np.gradient(L)
    return (np.hypot(gx, gy) > thr)
ec, er = edge_frac(Lc), edge_frac(Lr)
print("\nedge density (>4/255) on face: cand %.1f%%  ref %.1f%%"
      % (100 * ec[m].mean(), 100 * er[m].mean()))

# crops for the eye: block face, 2x
def crop(a, box, name, z=2):
    x0, y0, x1, y1 = box
    im = Image.fromarray((np.clip(a[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8))
    im = im.resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST)
    im.save(name)

crop(c, (430, 220, 690, 400), "crop-face-cand.png")
crop(r, (430, 220, 690, 400), "crop-face-ref.png")
crop(c, (250, 470, 510, 650), "crop-faceL-cand.png")
crop(r, (250, 470, 510, 650), "crop-faceL-ref.png")
print("\nwrote crops")
