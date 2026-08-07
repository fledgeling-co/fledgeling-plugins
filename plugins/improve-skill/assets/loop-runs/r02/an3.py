#!/usr/bin/env python3
"""r02 analysis 3: clean-patch texture stats, so the target numbers are local."""
import numpy as np
from PIL import Image, ImageFilter
D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/"

def load(p):
    im = Image.open(p).convert("RGB").resize((1024, 1024), Image.LANCZOS)
    g = np.asarray(im.convert("L"), dtype=np.float64)
    b = np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(6)), dtype=np.float64)
    return np.asarray(im, float), g, g - b

RGB, R, hR = load(D + "r01/reference-1024.png")
CGB, C, hC = load(D + "r01/candidate-1024.png")

PATCHES = {
    "un-planed far (near key)":   (110, 150, 150),
    "un-planed mid":              (60, 430, 180),
    "un-planed near cut":         (170, 700, 150),
    "un-planed ahead of blade":   (620, 90, 150),
    "trued open field":           (720, 800, 180),
    "trued near cut":             (620, 640, 110),
    "trued far corner":           (860, 930, 90),
}
print(f"{'patch':28s} {'ref hp sd':>9s} {'cnd hp sd':>9s} {'ref e>4':>8s} {'cnd e>4':>8s} {'ref grey':>8s} {'cnd grey':>8s}")
for k, (x, y, n) in PATCHES.items():
    def st(G, h):
        p = G[y:y+n, x:x+n]
        gy, gx = np.gradient(p)
        return h[y:y+n, x:x+n].std(), (np.hypot(gx, gy) > 4).mean(), p.mean()
    a = st(R, hR); b = st(C, hC)
    print(f"{k:28s} {a[0]:9.2f} {b[0]:9.2f} {a[1]:8.3f} {b[1]:8.3f} {a[2]:8.1f} {b[2]:8.1f}")

# block top face patches, in canvas coords well inside the face
print()
BP = {"block leading third": (330, 520, 90), "block middle": (470, 380, 90), "block trailing": (630, 260, 90)}
for k, (x, y, n) in BP.items():
    def st(G, h):
        p = G[y:y+n, x:x+n]
        gy, gx = np.gradient(p)
        return h[y:y+n, x:x+n].std(), (np.hypot(gx, gy) > 4).mean(), p.mean()
    a = st(R, hR); b = st(C, hC)
    print(f"{k:28s} {a[0]:9.2f} {b[0]:9.2f} {a[1]:8.3f} {b[1]:8.3f} {a[2]:8.1f} {b[2]:8.1f}")

# curl patch
print()
for k, (x, y, n) in {"curl body": (250, 300, 80), "curl upper band": (300, 260, 70)}.items():
    def st(G, h):
        p = G[y:y+n, x:x+n]
        gy, gx = np.gradient(p)
        return h[y:y+n, x:x+n].std(), (np.hypot(gx, gy) > 4).mean(), p.mean()
    a = st(R, hR); b = st(C, hC)
    print(f"{k:28s} {a[0]:9.2f} {b[0]:9.2f} {a[1]:8.3f} {b[1]:8.3f} {a[2]:8.1f} {b[2]:8.1f}")

# darkest-pixel hue of the reference's un-planed fibre valleys vs candidate dashes
def darkhue(rgb, G, x, y, n, lbl):
    p = rgb[y:y+n, x:x+n].reshape(-1, 3)
    g = G[y:y+n, x:x+n].ravel()
    k = max(1, int(len(g) * 0.02))
    idx = np.argsort(g)[:k]
    m = p[idx].mean(axis=0) / 255.0
    j = np.argsort(g)[-k:]
    m2 = p[j].mean(axis=0) / 255.0
    print(f"  {lbl:22s} darkest2% rgb ({m[0]:.3f},{m[1]:.3f},{m[2]:.3f})   brightest2% ({m2[0]:.3f},{m2[1]:.3f},{m2[2]:.3f})")

print("\nfibre valley / crest colour, un-planed mid patch:")
darkhue(RGB, R, 60, 430, 180, "reference")
darkhue(CGB, C, 60, 430, 180, "candidate")
print("block middle:")
darkhue(RGB, R, 470, 380, 90, "reference")
darkhue(CGB, C, 470, 380, 90, "candidate")
