"""r04: perpendicular cross-sections through both blocks -> shoulder + back-edge depth."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB"), float) / 255.
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGBA"), float) / 255.
cand = cand[..., :3] * cand[..., 3:4] + 0.5 * (1 - cand[..., 3:4])


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def sample(L, ang, org, lx, ly):
    a = np.radians(ang)
    ux, uy = np.cos(a), -np.sin(a)
    nx, ny = -np.sin(a), -np.cos(a)
    x = org[0] + ux * lx + nx * ly
    y = org[1] + uy * lx + ny * ly
    xi, yi = int(round(x)), int(round(y))
    if 0 <= xi < 1024 and 0 <= yi < 1024:
        return L[yi, xi]
    return np.nan


for tag, img, ang, org, frac in (("REF ", ref, 38.92, (382.0, 688.0), 613.0),
                                 ("CAND", cand, 33.00, (274.6, 778.3), 640.0)):
    L = lum(img)
    print(f"== {tag} cross-sections (local y from -30 to 300, step 10) ==")
    for f in (0.25, 0.50, 0.75):
        lx = f * frac
        vals = [sample(L, ang, org, lx, ly) for ly in range(-30, 301, 10)]
        print(f"  lx={lx:5.0f} (" + f"{f:.2f}L)")
        print("    ly:  " + " ".join(f"{ly:5d}" for ly in range(-30, 301, 10)))
        print("    L :  " + " ".join(("  nan" if np.isnan(v) else f"{v:5.2f}") for v in vals))
    print()
