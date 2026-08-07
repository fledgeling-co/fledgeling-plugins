"""r04: boundary line fit + block corner extraction + curl extents."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGBA"), dtype=np.float64) / 255.
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGBA"), dtype=np.float64) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


Lr, Lc = lum(ref), lum(cand)

print("== ground split: strongest vertical luminance step per column, outside the block ==")
for tag, L, dark in (("REF ", Lr, 0.30), ("CAND", Lc, 0.45)):
    pts = []
    for x in range(0, 1024, 24):
        col = L[:, x]
        # smooth then differentiate
        k = np.ones(9) / 9.
        s = np.convolve(col, k, mode="same")
        d = np.diff(s)
        # ignore rows inside the dark object and the outer 60px rim
        ok = np.ones(len(d), bool)
        ok[:70] = False
        ok[-70:] = False
        ok &= (col[:-1] > dark) & (col[1:] > dark)
        if not ok.any():
            continue
        dd = np.where(ok, d, 0)
        y = int(np.argmax(dd))
        if dd[y] > 0.004:
            pts.append((x, y, dd[y]))
    if len(pts) > 4:
        px = np.array([p[0] for p in pts], float)
        py = np.array([p[1] for p in pts], float)
        A = np.polyfit(px, py, 1)
        ang = np.degrees(np.arctan(-A[0]))
        print(f"  {tag} n={len(pts)} slope={A[0]:+.4f} angle={ang:.2f}deg  "
              f"y@x=0 {A[1]:.0f}  y@x=512 {A[0]*512+A[1]:.0f}  y@x=1023 {A[0]*1023+A[1]:.0f}")
        print("        pts:", " ".join(f"({p[0]},{p[1]})" for p in pts[:6]), "...",
              " ".join(f"({p[0]},{p[1]})" for p in pts[-6:]))
