#!/usr/bin/env python3
"""Crop matching regions from reference and candidate at 3x, side by side."""
from PIL import Image
D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/"
r = Image.open(D + "r01/reference-1024.png").convert("RGB")
c = Image.open(D + "r01/candidate-1024.png").convert("RGB")
for name, (x, y, n) in {
    "ground": (90, 430, 200),
    "block": (430, 330, 200),
    "curl": (200, 240, 200),
    "lead": (210, 560, 200),
}.items():
    sheet = Image.new("RGB", (n * 3 * 2 + 18, n * 3), "black")
    sheet.paste(r.crop((x, y, x + n, y + n)).resize((n * 3, n * 3), Image.NEAREST), (0, 0))
    sheet.paste(c.crop((x, y, x + n, y + n)).resize((n * 3, n * 3), Image.NEAREST), (n * 3 + 18, 0))
    sheet.save(D + f"r02/crop-{name}.png")
    print("wrote", name)
