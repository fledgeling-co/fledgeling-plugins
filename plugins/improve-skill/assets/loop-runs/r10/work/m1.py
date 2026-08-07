"""Region breakdown of |L_cand - L_ref| at 1024, plus a silhouette-band split.

Regions come from the CANDIDATE's own geometry (we know it exactly) and from a
coarse threshold on the reference for its block.
"""
import numpy as np, sys
from PIL import Image

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets"
R8 = A + "/loop-runs/r08"


def lum(p):
    im = Image.open(p).convert("RGB").resize((1024, 1024), Image.LANCZOS)
    a = np.asarray(im).astype(np.float64) / 255.0
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2], a


c, ca = lum(R8 + "/candidate-1024.png")
r, ra = lum(R8 + "/reference-1024.png")
d = np.abs(c - r)
print("global mean |dL| =", round(d.mean(), 4))

# candidate block mask: dark solid.  both images' blocks are much darker than ground.
cb = c < 0.42
rb = r < 0.42
# clean up: keep the big component only via a crude bbox on the densest rows/cols
ys, xs = np.where(cb)
print("cand block bbox", xs.min(), xs.max(), ys.min(), ys.max(), "frac", round(cb.mean(), 4))
ys, xs = np.where(rb)
print("ref  block bbox", xs.min(), xs.max(), ys.min(), ys.max(), "frac", round(rb.mean(), 4))

both = cb & rb
only_c = cb & ~rb
only_r = rb & ~cb
grd = ~cb & ~rb
n = d.size
for name, m in [("block both", both), ("block cand-only", only_c),
                ("block ref-only", only_r), ("ground both", grd)]:
    print(f"{name:18s} px%={100*m.mean():6.2f}  meanC={c[m].mean():.3f} meanR={r[m].mean():.3f} "
          f"contrib={d[m].sum()/n:.4f}")

# silhouette band: within 24px of the candidate block edge
from scipy import ndimage  # noqa
