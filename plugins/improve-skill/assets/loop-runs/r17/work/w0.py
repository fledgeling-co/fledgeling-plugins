"""Squint sheet: candidate (top) vs reference (bottom) at 16/32/64/128, NEAREST-upscaled."""
from PIL import Image

c = Image.open('loop-runs/r16/candidate-1024.png').convert('RGB')
r = Image.open('loop-runs/r16/reference-1024.png').convert('RGB')
CELL, GAP = 256, 8
sizes = (16, 32, 64, 128)
W = len(sizes) * CELL + (len(sizes) - 1) * GAP
H = 2 * CELL + GAP
out = Image.new('RGB', (W, H), (40, 40, 40))
for j, s in enumerate(sizes):
    for i, im in enumerate((c, r)):
        d = im.resize((s, s), Image.LANCZOS).resize((CELL, CELL), Image.NEAREST)
        out.paste(d, (j * (CELL + GAP), i * (CELL + GAP)))
out.save('loop-runs/r17/work/squint.png')
print(out.size)
