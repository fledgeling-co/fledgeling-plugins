"""Side-by-side views for eyeballing: candidate, reference, residual at 512."""
import numpy as np, pathlib
from PIL import Image

B = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r06/work/base')
out = B.parent

for n in ('candidate-1024', 'reference-1024', 'residual-1024', 'edges-candidate', 'edges-reference'):
    im = Image.open(B / f'{n}.png').convert('RGB').resize((512, 512), Image.LANCZOS)
    im.save(out / f'{n}-512.png')

# a 2-up strip, candidate | reference
c = Image.open(B / 'candidate-1024.png').convert('RGB').resize((512, 512), Image.LANCZOS)
r = Image.open(B / 'reference-1024.png').convert('RGB').resize((512, 512), Image.LANCZOS)
s = Image.new('RGB', (1024, 512))
s.paste(c, (0, 0)); s.paste(r, (512, 0))
s.save(out / 'pair-512.png')
print('ok')
