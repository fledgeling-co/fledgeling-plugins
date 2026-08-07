"""Viewing aids: downsample the four artifacts to something readable, and cut the
worst-residual crops at 1:1 out of both images side by side.
"""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r11/"
for name, out in (("residual-1024.png", "v-residual.png"),
                  ("edges-candidate.png", "v-edges-cand.png"),
                  ("edges-reference.png", "v-edges-ref.png"),
                  ("candidate-1024.png", "v-cand.png"),
                  ("reference-1024.png", "v-ref.png")):
    im = Image.open(R + name).convert("RGB").resize((512, 512), Image.LANCZOS)
    im.save(out)

# where is the residual worst, by 64px cell?
res = np.asarray(Image.open(R + "residual-1024.png").convert("L")).astype(float)
if res.shape[0] != 1024:
    res = np.asarray(Image.open(R + "residual-1024.png").convert("L")
                     .resize((1024, 1024))).astype(float)
cells = []
for y in range(0, 1024, 64):
    for x in range(0, 1024, 64):
        cells.append((res[y:y+64, x:x+64].mean(), x, y))
cells.sort(reverse=True)
print("worst 64px residual cells (mean brightness of the residual map):")
for v, x, y in cells[:14]:
    print(f"  ({x:4d},{y:4d})  {v:6.1f}")
print(f"  ... median cell {np.median([c[0] for c in cells]):.1f}")
