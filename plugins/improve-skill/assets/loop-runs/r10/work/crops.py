import sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F
A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r10/work"
c = F.render_candidate(A / "icon.svg", 1024).convert("RGB")
r = F.normalise_reference(A / "icon-engineC-f5665d-2.png", 1024).convert("RGB")
BOX = {"rough-left": (25, 690, 175, 840), "rough-tr": (620, 30, 950, 160),
       "trued-br": (640, 800, 960, 980), "blockface": (430, 300, 700, 470),
       "leadcorner": (170, 560, 380, 790)}
for name, (x0, y0, x1, y1) in BOX.items():
    w, h = x1 - x0, y1 - y0
    z = max(1, int(640 / max(w, h)))
    a = c.crop((x0, y0, x1, y1)).resize((w * z, h * z), Image.NEAREST)
    b = r.crop((x0, y0, x1, y1)).resize((w * z, h * z), Image.NEAREST)
    out = Image.new("RGB", (a.width * 2 + 12, a.height), (255, 0, 255))
    out.paste(a, (0, 0)); out.paste(b, (a.width + 12, 0))
    out.save(W / f"crop-{name}.png")
    print(name, (x0, y0, x1, y1), "zoom", z, "-> ", out.size)
