"""Base arrays for r12: the current master's 1024 render, the reference's, and the
region masks, built the same way r11/work/m1+m2 built theirs so every number this
round prints is comparable with the ones in the notes.
"""
import sys, pathlib, math, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
tag = sys.argv[1] if len(sys.argv) > 1 else "g"
g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", 1024))
np.save(f"{tag}1024.npy", g)
np.save("h1024.npy", h)

W = 1024
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX = 543.0 - UX * 320.0
AY = 604.0 - UY * 320.0
yy, xx = np.mgrid[0:W, 0:W].astype(float)
ly = NX * (xx - AX) + NY * (yy - AY)
lx = UX * (xx - AX) + UY * (yy - AY)
r_key = np.hypot(xx - 75.0, yy - 25.0)


def block_mask(img):
    return F.dilate(img < 0.42, 4)


block = block_mask(g) | block_mask(h)
rim = F.rim_mask(W)
band = np.abs(ly) < 34
rough = (ly > 0) & ~block & ~rim & ~band
trued = (ly < 0) & ~block & ~rim & ~band
np.save("ly.npy", ly); np.save("lx.npy", lx); np.save("rkey.npy", r_key)
np.save("rough.npy", rough); np.save("trued.npy", trued); np.save("block.npy", block)
print(f"rough {rough.sum()}  trued {trued.sum()}  block {block.sum()}")
print(f"plane mean L   ours rough {g[rough].mean():.4f} trued {g[trued].mean():.4f}"
      f"   ref rough {h[rough].mean():.4f} trued {h[trued].mean():.4f}")
