#!/usr/bin/env python3
"""r04 probe 7: crops at 3x through the region the SSIM map names worst -
the block's ground line - side by side, reference above candidate."""
from PIL import Image

BASE = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/"
OUT = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r04/"

ref = Image.open(BASE + "reference-1024.png").convert("RGB")
cand = Image.open(BASE + "candidate-1024.png").convert("RGB")

# each crop is centred on that image's own ground line, 300 wide x 130 tall
r = ref.crop((380, 830, 680, 960)).resize((900, 390), Image.NEAREST)
c = cand.crop((380, 735, 680, 865)).resize((900, 390), Image.NEAREST)
sheet = Image.new("RGB", (900, 800), "white")
sheet.paste(r, (0, 0))
sheet.paste(c, (0, 410))
sheet.save(OUT + "crop-groundline.png")

# and the bottom-right corner, where the residual is worst outside the tilt
r2 = ref.crop((700, 760, 940, 960)).resize((720, 600), Image.NEAREST)
c2 = cand.crop((680, 660, 920, 860)).resize((720, 600), Image.NEAREST)
sheet2 = Image.new("RGB", (720, 1220), "white")
sheet2.paste(r2, (0, 0))
sheet2.paste(c2, (0, 620))
sheet2.save(OUT + "crop-corner.png")
print("wrote crop-groundline.png, crop-corner.png")
