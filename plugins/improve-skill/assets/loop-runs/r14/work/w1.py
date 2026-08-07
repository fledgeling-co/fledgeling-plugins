import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = Image.open(R + "candidate-1024.png").convert("RGB")
ref = Image.open(R + "reference-1024.png").convert("RGB")
res = Image.open(R + "residual-1024.png").convert("RGB")
ec = Image.open(R + "edges-candidate.png").convert("RGB")
er = Image.open(R + "edges-reference.png").convert("RGB")

W = 320
tiles = [cand.resize((W, W), Image.LANCZOS), ref.resize((W, W), Image.LANCZOS),
         res.resize((W, W), Image.LANCZOS), ec.resize((W, W), Image.LANCZOS),
         er.resize((W, W), Image.LANCZOS)]
sheet = Image.new("RGB", (W * 5 + 24, W), (20, 20, 20))
for i, t in enumerate(tiles):
    sheet.paste(t, (i * (W + 6), 0))
sheet.save("loop-runs/r14/work/overview.png")
print("saved overview: candidate | reference | residual | edges-cand | edges-ref")
