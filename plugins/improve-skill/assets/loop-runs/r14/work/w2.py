import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = Image.open(R + "candidate-1024.png").convert("RGB")
ref = Image.open(R + "reference-1024.png").convert("RGB")

REGIONS = [
    ("topleft-corner", 0, 0, 224, 224),
    ("curl", 80, 20, 400, 340),
    ("block-left-tip+hone", 130, 540, 450, 800),
    ("block-right-end+shadow", 780, 380, 1024, 620),
    ("bottom-left", 20, 830, 300, 1010),
]
for name, x0, y0, x1, y1 in REGIONS:
    w, h = x1 - x0, y1 - y0
    s = 2 if max(w, h) < 300 else 1
    a = cand.crop((x0, y0, x1, y1)).resize((w * s, h * s), Image.LANCZOS)
    b = ref.crop((x0, y0, x1, y1)).resize((w * s, h * s), Image.LANCZOS)
    sheet = Image.new("RGB", (w * s * 2 + 8, h * s), (255, 0, 0))
    sheet.paste(a, (0, 0))
    sheet.paste(b, (w * s + 8, 0))
    sheet.save(f"loop-runs/r14/work/crop-{name}.png")
    print("saved", name, sheet.size)
