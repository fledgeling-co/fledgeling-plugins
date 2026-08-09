#!/usr/bin/env python3
"""r04 rubric + registration.

Two jobs. (1) The three ratios icon-notes tracks, on the new render, measured the
same way: mouth contrast, cast figure-ground, and the 16px read. (2) Where the
block's ground contact actually sits in each image - the number that explains why
a locally correct feature can still cost the composite.
"""
import numpy as np
from PIL import Image

A = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/"
REF = A + "loop-runs/r03/reference-1024.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (128 / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def ratio(a, b):
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


for label, path in (("r03", A + "loop-runs/r03/candidate-1024.png"), ("r04", A + "icon.png")):
    L = load(path)
    # the mouth: the darkest of the recess against the plaster face beside it
    mouth = np.percentile(L[470:640, 340:690], 8)
    face = np.percentile(L[560:700, 200:300], 50)
    # the cast tile against the plaster it sits on
    cast = np.percentile(L[300:470, 230:560], 50)
    ground = np.percentile(L[300:420, 640:820], 50)
    print(f"  {label}  mouth contrast {ratio(mouth, face):.3f}:1   "
          f"cast figure-ground {ratio(cast, ground):.3f}:1")

print()
print("== the 16px read: local contrast of the whole tile ==")
for label, path in (("r03", A + "loop-runs/r03/candidate-1024.png"), ("r04", A + "icon.png")):
    im = Image.open(path).convert("RGBA").resize((16, 16), Image.LANCZOS)
    L = load(path)
    a = np.asarray(im).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (128 / 255.0) * (1 - al)
    g = 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
    print(f"  {label}  16px sd {g.std():.4f}   range {g.min():.3f}..{g.max():.3f}")

print()
print("== where the block's ground contact sits in each image ==")
for label, path, y0, y1 in (("reference", REF, 800, 980),
                            ("candidate", A + "icon.png", 700, 900)):
    L = load(path)
    rows = []
    for x in range(360, 681, 40):
        col = L[:, x]
        g = col[y0:y1] - np.roll(col[y0:y1], 3)
        rows.append(y0 + int(np.argmin(g)) - 2)
    print(f"  {label:10s} ground silhouette y = {np.mean(rows):.0f} "
          f"(per column {rows})")
