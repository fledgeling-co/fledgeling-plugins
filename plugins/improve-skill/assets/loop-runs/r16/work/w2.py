import pathlib
from PIL import Image
A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
R = A / "loop-runs/r14"
OUT = A / "loop-runs/r16/work"
crops = {
    "curlL": (64, 192, 320, 480),     # 32px FP band rows 7-13
    "groundL": (64, 512, 320, 864),   # 32px FP band rows 17-25
}
for name, box in crops.items():
    for tag, f in (("cand", "candidate-1024.png"), ("ref", "reference-1024.png")):
        im = Image.open(R / f).convert("RGB").crop(box)
        w, h = im.size
        im.resize((w * 2, h * 2), Image.NEAREST).save(OUT / f"{name}-{tag}.png")
print("ok")
