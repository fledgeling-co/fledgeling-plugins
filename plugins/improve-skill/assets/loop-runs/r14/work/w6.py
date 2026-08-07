import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB")).astype(np.float32) / 255.
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB")).astype(np.float32) / 255.
lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
Y, X = np.mgrid[0:1024, 0:1024].astype(np.float32)

DC, OC, DR, ORF = 34.0, 791.9, 41.0, 763.5


def prof(img, deg, off, xa, xb, half=18):
    L = lum(img)
    t = np.radians(deg)
    s = Y * np.cos(t) + X * np.sin(t) - off
    reg = (X >= xa) & (X < xb) & (L > 0.02)
    out = np.full((2 * half + 1, 4), np.nan)
    for i, d in enumerate(range(-half, half + 1)):
        m = reg & (s >= d - 0.5) & (s < d + 0.5)
        if m.sum() > 25:
            out[i, :3] = img[m].mean(0)
            out[i, 3] = L[m].mean()
    return out


print("REFERENCE, three stations along its own cut (x window), L only")
stations = [(20, 130), (130, 240), (240, 350)]
tab = [prof(ref, DR, ORF, a, b) for a, b in stations]
print("  d " + "".join(f"  x{a}-{b}" for a, b in stations))
for i, d in enumerate(range(-18, 19)):
    print(f"{d:+4d} " + "".join(f"  {t[i,3]:.4f}" for t in tab))

print("\nRGB of the reference's cut features (whole left strip x 20-350):")
p = prof(ref, DR, ORF, 20, 350)
def hsv(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    return (mx - mn) / mx if mx > 0 else 0.0
for nm, d in (("un-planed plateau", -16), ("crest", -1), ("seam", 3), ("lip peak", 8), ("trued plateau", 16)):
    i = d + 18
    r, g, b = p[i, :3]
    print(f"  {nm:18s} d={d:+3d}  RGB {r:.3f} {g:.3f} {b:.3f}   L {p[i,3]:.4f}   sat {hsv((r,g,b)):.3f}   R-B {r-b:+.3f}")

print("\nCANDIDATE, same treatment on its own cut:")
q = prof(cand, DC, OC, 20, 350)
for nm, d in (("un-planed plateau", -16), ("crest", -1), ("seam", 3), ("lip peak", 8), ("trued plateau", 16)):
    i = d + 18
    r, g, b = q[i, :3]
    print(f"  {nm:18s} d={d:+3d}  RGB {r:.3f} {g:.3f} {b:.3f}   L {q[i,3]:.4f}   sat {hsv((r,g,b)):.3f}   R-B {r-b:+.3f}")
print("\ncand full L profile:", " ".join(f"{v:.3f}" for v in q[:, 3]))
