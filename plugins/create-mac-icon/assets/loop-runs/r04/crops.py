#!/usr/bin/env python3
"""3x crops of the ground contact at the two side corners and the front, plus the
mouth rim, so the crevice is judged by eye as well as by profile."""
from PIL import Image

D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/"
im = Image.open(D + "cand-test.png").convert("RGB")
ref = Image.open("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/reference-1024.png").convert("RGB")

for name, box in (("corner-l", (140, 540, 340, 700)),
                  ("corner-r", (700, 540, 900, 700)),
                  ("mouth", (270, 410, 760, 690))):
    im.crop(box).resize(((box[2]-box[0])*3, (box[3]-box[1])*3), Image.NEAREST).save(D + f"crop-{name}.png")

# the front contact, candidate over reference, same object in each
im.crop((300, 700, 760, 840)).resize((1380, 420), Image.NEAREST).save(D + "crop-front-cand.png")
ref.crop((300, 800, 760, 940)).resize((1380, 420), Image.NEAREST).save(D + "crop-front-ref.png")
print("wrote crops")
