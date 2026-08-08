"""r12 diagnostic 7: the 16px cost - is it the texture, or the filter's ALPHA?

feComposite operator="arithmetic" k1=1/sin(elev) multiplies the PREMULTIPLIED source,
alpha included, so every antialiased silhouette pixel comes out 1.31x more opaque and
clamps. At 1024 that is invisible; at 16px the block is ~10px across and a fractional
silhouette dilation is a real luminance change. Compare the alpha channel of the two
renders at every scored size, with the interior masked out.
"""
import sys, pathlib, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
h1024 = np.load("d_h.npy")

print("current icon.svg vs the r11 render kept in loop-runs/r11/candidate-1024.png")
from PIL import Image
for size in (1024, 256, 128, 32, 16):
    cur = F.render_candidate(A / "icon.svg", size)
    a_cur = np.asarray(cur)[..., 3].astype(np.float64) / 255.0
    old = Image.open(A / "loop-runs/r11/candidate-1024.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    a_old = np.asarray(old)[..., 3].astype(np.float64) / 255.0
    g_cur, g_old = F.to_gray(cur), F.to_gray(old)
    ref = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", size))
    print("  %4d  alpha sum %9.2f -> %9.2f (%+.3f%%)   meanL %.4f -> %.4f   |L-ref| %.4f -> %.4f"
          % (size, a_old.sum(), a_cur.sum(), 100 * (a_cur.sum() - a_old.sum()) / a_old.sum(),
             g_old.mean(), g_cur.mean(), np.abs(g_old - ref).mean(), np.abs(g_cur - ref).mean()))
